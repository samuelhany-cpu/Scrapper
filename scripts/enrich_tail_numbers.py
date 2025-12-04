"""
Enrich tail_number (replace 'Unknown') in historical datasets by inference.
Strategy (multi-pass):
 1) flight_number -> most common tail_number (across dataset)
 2) (flight_number, origin_code, destination_code) -> most common tail
 3) (origin_code, destination_code) -> most common tail
 4) aircraft_type -> most common tail
If a mapping exists, fill Unknown with inferred tail and add a provenance column showing which rule was used.

This script writes an enriched CSV and prints improvement statistics.
"""

import pandas as pd
import os
from datetime import datetime
import glob


def find_latest_historical_file(outputs_dir):
    pattern = os.path.join(outputs_dir, 'egyptair_HISTORICAL_2015-2025_*.csv')
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No files match {pattern}")
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]


def most_common_mapping(df, key_cols, value_col='tail_number'):
    """Return dict mapping key tuple -> most common non-Unknown value"""
    grouped = df[df[value_col] != 'Unknown'].groupby(key_cols)[value_col]
    # calculate mode for each group
    mapping = {}
    for key, series in grouped:
        # series is a Series of tail_numbers; value_counts gives counts
        counts = series.value_counts()
        if len(counts) == 0:
            continue
        mapping[key if isinstance(key, tuple) else (key,)] = counts.idxmax()
    return mapping


def apply_mapping_single(df, mapping, key_cols, value_col='tail_number', provenance_col='inferred_by', method_name='method'):
    """Apply mapping to rows where value_col == 'Unknown'. Returns number filled."""
    # Build keys for rows
    def make_key(row):
        if len(key_cols) == 1:
            return (row[key_cols[0]],)
        return tuple(row[c] for c in key_cols)

    mask_unknown = df[value_col] == 'Unknown'
    count_filled = 0
    for idx, row in df[mask_unknown].iterrows():
        key = make_key(row)
        if key in mapping:
            df.at[idx, value_col] = mapping[key]
            df.at[idx, provenance_col] = method_name
            count_filled += 1
    return count_filled


def enrich_file(input_path, output_path=None):
    print(f"\n🔎 Loading file: {input_path}")
    df = pd.read_csv(input_path, encoding='utf-8-sig', low_memory=False)

    # Ensure columns exist
    for c in ['tail_number', 'flight_number', 'origin_code', 'destination_code', 'aircraft_type']:
        if c not in df.columns:
            df[c] = 'N/A'

    # Normalize Unknown markers
    df['tail_number'] = df['tail_number'].fillna('Unknown')

    total_before = (df['tail_number'] == 'Unknown').sum()
    print(f"   Unknown tail numbers before: {total_before:,} / {len(df):,} rows")

    # Prepare provenance column
    if 'inferred_by' not in df.columns:
        df['inferred_by'] = ''

    # PASS 1: flight_number -> tail
    print("\n1) Inferring by flight_number -> most common tail...")
    map1 = most_common_mapping(df, ['flight_number'])
    filled1 = apply_mapping_single(df, map1, ['flight_number'], method_name='flight_number_mode')
    print(f"   Filled by pass 1: {filled1:,}")

    # PASS 2: (flight_number, origin, dest) -> tail
    print("\n2) Inferring by (flight_number, origin_code, destination_code) -> tail...")
    map2 = most_common_mapping(df, ['flight_number', 'origin_code', 'destination_code'])
    filled2 = apply_mapping_single(df, map2, ['flight_number', 'origin_code', 'destination_code'], method_name='flight_route_mode')
    print(f"   Filled by pass 2: {filled2:,}")

    # PASS 3: (origin, dest) -> tail
    print("\n3) Inferring by (origin_code, destination_code) -> most common tail on that route...")
    map3 = most_common_mapping(df, ['origin_code', 'destination_code'])
    filled3 = apply_mapping_single(df, map3, ['origin_code', 'destination_code'], method_name='route_mode')
    print(f"   Filled by pass 3: {filled3:,}")

    # PASS 4: aircraft_type -> most common tail
    print("\n4) Inferring by aircraft_type -> most common tail (last resort)...")
    map4 = most_common_mapping(df, ['aircraft_type'])
    filled4 = apply_mapping_single(df, map4, ['aircraft_type'], method_name='aircraft_type_mode')
    print(f"   Filled by pass 4: {filled4:,}")

    total_after = (df['tail_number'] == 'Unknown').sum()
    print(f"\n✅ Done. Unknown tail numbers after: {total_after:,} / {len(df):,} rows")

    # If any remain unknown, optionally assign a synthetic placeholder per flight number
    remain = total_after
    if remain > 0:
        print(f"\n5) Assigning synthetic placeholders for remaining {remain:,} rows...")
        # For each remaining row, set tail to 'Inferred_<flight_number>' to enable full dataset
        mask_unknown = df['tail_number'] == 'Unknown'
        for idx, row in df[mask_unknown].iterrows():
            flight = row['flight_number']
            placeholder = f'Inferred-{flight}' if flight not in (None, '', 'N/A') else 'Inferred-Unknown'
            df.at[idx, 'tail_number'] = placeholder
            df.at[idx, 'inferred_by'] = 'synthetic_placeholder'
        print(f"   Assigned placeholders to {remain:,} rows")

    # Save enriched file
    if output_path is None:
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        base = os.path.basename(input_path)
        output_path = os.path.join(os.path.dirname(input_path), base.replace('.csv', f'_enriched_{ts}.csv'))

    print(f"\n💾 Saving enriched file to: {output_path}")
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    # Print top inferred mappings (for user verification)
    print("\nTop tail assignments by flight_number (sample):")
    samp = df.groupby('flight_number')['tail_number'].agg(lambda s: s.value_counts().index[0] if len(s)>0 else 'Unknown').head(10)
    print(samp.to_string())

    return output_path, df


def main():
    script_dir = os.path.dirname(__file__)
    outputs_dir = os.path.join(script_dir, '..', 'outputs')

    try:
        input_path = find_latest_historical_file(outputs_dir)
    except FileNotFoundError as e:
        print(str(e))
        return

    print(f"\nStarting enrichment for: {input_path}")
    out, df = enrich_file(input_path)
    print(f"\nFinished. Enriched file: {out}")

if __name__ == '__main__':
    main()
