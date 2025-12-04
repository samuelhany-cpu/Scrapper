"""
11-Year Historical Flight Data Generator (2015-2025)
Uses 7 days of REAL collected data and intelligently extends to 11 years
based on weekly schedule patterns (flights typically repeat weekly)
"""

import pandas as pd
from datetime import datetime, timedelta
import os


def extend_to_historical_range(input_csv, output_csv, start_date, end_date):
    """
    Extend 7 days of real flight data to any date range by repeating weekly patterns
    Airlines typically have weekly schedules that repeat
    
    Args:
        input_csv: Path to 7-day real data CSV
        output_csv: Path for output CSV
        start_date: Start date (datetime object)
        end_date: End date (datetime object)
    """
    
    total_days = (end_date - start_date).days + 1
    total_years = total_days / 365.25
    
    print("=" * 100)
    print(f"📊 EXTENDING 7-DAY DATA TO {total_days:,} DAYS ({total_years:.1f} YEARS)")
    print("=" * 100)
    
    # Read the 7-day data
    print("\n📖 Reading 7-day real data...")
    df = pd.read_csv(input_csv, encoding='utf-8-sig')
    
    print(f"   ✅ Loaded {len(df)} flights from {df['flight_date'].min()} to {df['flight_date'].max()}")
    
    # Convert flight_date to datetime
    df['flight_date'] = pd.to_datetime(df['flight_date'])
    
    # Get the 7-day pattern
    original_min_date = df['flight_date'].min()
    original_max_date = df['flight_date'].max()
    pattern_days = (original_max_date - original_min_date).days + 1
    
    print(f"   📅 Pattern: {pattern_days} days of real data")
    print(f"   🎯 Target: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"   📊 Total: {total_days:,} days ({total_years:.1f} years)")
    
    # Calculate how many weeks we need
    total_weeks = (total_days // 7) + 2  # Extra buffer
    
    print(f"\n🔄 Generating {total_weeks:,} weeks of flight data...")
    print(f"   (This will create approximately {len(df) * total_weeks:,} flight records)")
    
    all_flights = []
    
    # Generate data by replicating weekly pattern
    for week_num in range(total_weeks):
        if week_num % 100 == 0:  # Progress indicator every 100 weeks
            print(f"   Processing week {week_num:,}/{total_weeks:,}...")
        
        week_df = df.copy()
        
        # Calculate date offset from original pattern
        # Shift to start from target start_date
        days_offset = (start_date - original_min_date).days + (week_num * 7)
        
        # Shift dates
        week_df['flight_date'] = week_df['flight_date'] + timedelta(days=days_offset)
        
        # Update collected_at timestamp
        week_df['collected_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Add note about data source (for historical data)
        if week_num == 0:
            week_df['data_source'] = week_df['data_source'] + ' (Pattern baseline)'
        else:
            # Calculate which year this week falls into
            year = week_df['flight_date'].iloc[0].year
            week_df['data_source'] = week_df['data_source'] + f' (Historical projection - {year})'
        
        all_flights.append(week_df)
    
    print(f"\n📦 Combining {len(all_flights):,} weeks of data...")
    
    # Combine all weeks
    extended_df = pd.concat(all_flights, ignore_index=True)
    
    print(f"   ✅ Combined: {len(extended_df):,} total flight records")
    
    # Trim to exactly the target date range
    print(f"\n✂️  Trimming to exact date range...")
    extended_df = extended_df[
        (extended_df['flight_date'] >= start_date) & 
        (extended_df['flight_date'] <= end_date)
    ]
    
    print(f"   ✅ Trimmed to: {len(extended_df):,} flights")
    
    # Sort by date and flight number
    print(f"\n🔄 Sorting by date and flight number...")
    extended_df = extended_df.sort_values(['flight_date', 'flight_number'])
    
    print(f"\n📊 FINAL DATASET SUMMARY:")
    print(f"   Total Flights: {len(extended_df):,}")
    print(f"   Date Range: {extended_df['flight_date'].min().strftime('%Y-%m-%d')} to {extended_df['flight_date'].max().strftime('%Y-%m-%d')}")
    print(f"   Days Covered: {(extended_df['flight_date'].max() - extended_df['flight_date'].min()).days + 1:,}")
    print(f"   Years Covered: {((extended_df['flight_date'].max() - extended_df['flight_date'].min()).days + 1) / 365.25:.1f}")
    print(f"   Unique Flight Numbers: {extended_df['flight_number'].nunique()}")
    print(f"   Unique Aircraft: {extended_df[extended_df['tail_number'] != 'Unknown']['tail_number'].nunique()}")
    print(f"   Unique Routes: {extended_df[['origin_code', 'destination_code']].drop_duplicates().shape[0]}")
    
    # Save to CSV
    print(f"\n💾 Saving to: {output_csv}")
    print(f"   File size estimate: ~{len(extended_df) * 0.5 / 1024:.1f} MB")
    
    extended_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    
    print(f"✅ COMPLETE!")
    print("=" * 100)
    
    return output_csv, extended_df


def analyze_historical_data(df):
    """Generate comprehensive analysis for historical data"""
    
    print("\n" + "=" * 100)
    print("📊 11-YEAR EGYPTAIR HISTORICAL FLIGHT DATA ANALYSIS (2015-2025)")
    print("=" * 100)
    
    df['flight_date'] = pd.to_datetime(df['flight_date'])
    
    print(f"\n📈 OVERVIEW:")
    print(f"   Total Flights: {len(df):,}")
    print(f"   Date Range: {df['flight_date'].min().strftime('%Y-%m-%d')} to {df['flight_date'].max().strftime('%Y-%m-%d')}")
    print(f"   Duration: {(df['flight_date'].max() - df['flight_date'].min()).days + 1:,} days")
    print(f"   Duration: {((df['flight_date'].max() - df['flight_date'].min()).days + 1) / 365.25:.1f} years")
    print(f"   Average per Day: {len(df) / ((df['flight_date'].max() - df['flight_date'].min()).days + 1):.1f} flights")
    print(f"   Average per Year: {len(df) / (((df['flight_date'].max() - df['flight_date'].min()).days + 1) / 365.25):,.0f} flights")
    
    print(f"\n✈️  FLEET:")
    known_tails = df[df['tail_number'] != 'Unknown']
    print(f"   Unique Aircraft: {known_tails['tail_number'].nunique()}")
    print(f"   Flights with Tail Numbers: {len(known_tails):,} ({len(known_tails)/len(df)*100:.1f}%)")
    
    print(f"\n🌍 ROUTES:")
    print(f"   Unique Routes: {df[['origin_code', 'destination_code']].drop_duplicates().shape[0]}")
    print(f"   Unique Flight Numbers: {df['flight_number'].nunique()}")
    
    print(f"\n🛩️  TOP 10 MOST ACTIVE AIRCRAFT (ALL-TIME):")
    if len(known_tails) > 0:
        tail_counts = known_tails['tail_number'].value_counts().head(10)
        for tail, count in tail_counts.items():
            aircraft_type = known_tails[known_tails['tail_number'] == tail]['aircraft_type'].iloc[0]
            print(f"   {tail} ({aircraft_type}): {count:,} flights")
    
    print(f"\n✈️  TOP 10 DESTINATIONS (ALL-TIME):")
    dest_counts = df[df['destination_code'] != 'N/A']['destination_code'].value_counts().head(10)
    for dest, count in dest_counts.items():
        dest_name = df[df['destination_code'] == dest]['destination'].iloc[0]
        print(f"   {dest} ({dest_name}): {count:,} flights")
    
    print(f"\n📅 FLIGHTS PER YEAR:")
    df['year'] = df['flight_date'].dt.year
    year_counts = df.groupby('year').size().sort_index()
    for year, count in year_counts.items():
        print(f"   {year}: {count:,} flights")
    
    print(f"\n📊 YEARLY STATISTICS:")
    yearly_stats = df.groupby('year').agg({
        'flight_number': 'count',
        'tail_number': lambda x: (x != 'Unknown').sum()
    }).rename(columns={'flight_number': 'total_flights', 'tail_number': 'flights_with_tails'})
    
    for year, row in yearly_stats.iterrows():
        tail_pct = (row['flights_with_tails'] / row['total_flights'] * 100) if row['total_flights'] > 0 else 0
        print(f"   {year}: {row['total_flights']:,} flights, {row['flights_with_tails']:,} with tail numbers ({tail_pct:.1f}%)")
    
    print("\n" + "=" * 100)


def main():
    """Main execution"""
    
    # File paths
    script_dir = os.path.dirname(__file__)
    outputs_dir = os.path.join(script_dir, '..', 'outputs')
    
    input_csv = os.path.join(outputs_dir, 'egyptair_30days_comprehensive_20251130_180822.csv')
    output_csv = os.path.join(outputs_dir, f'egyptair_HISTORICAL_2015-2025_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    
    print("\n" + "=" * 100)
    print(" " * 20 + "✈️  11-YEAR EGYPTAIR HISTORICAL FLIGHT DATA GENERATOR ✈️")
    print("=" * 100)
    print("\n📋 Method: Weekly Pattern Replication")
    print("   • Airlines typically repeat schedules weekly")
    print("   • Using 7 days of REAL data from AeroDataBox (Nov 2025)")
    print("   • Projecting back to January 1, 2015")
    print("   • Result: Realistic 11-year historical dataset (2015-2025)")
    print("\n⚠️  NOTE: This is a large dataset generation (~450,000 flights)")
    print("   • Processing time: 1-2 minutes")
    print("   • File size: ~200-250 MB")
    print("   • Memory usage: High (ensure sufficient RAM)\n")
    
    # Define date range: Jan 1, 2015 to Nov 30, 2025
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2025, 11, 30)
    
    # Extend data
    print("🚀 Starting generation...\n")
    output_path, df = extend_to_historical_range(input_csv, output_csv, start_date, end_date)
    
    # Analyze
    analyze_historical_data(df)
    
    # Final message
    print(f"\n✅ SUCCESS!")
    print(f"📄 11-year historical dataset saved to:")
    print(f"   {output_path}")
    print(f"\n💡 To view:")
    print(f"   start {output_path}")
    print(f"\n⚠️  WARNING: Large file - Excel may take time to open or may require splitting")
    print(f"   Consider using Python/Pandas for analysis if file is too large for Excel")
    print("\n" + "=" * 100 + "\n")
    
    return output_path


if __name__ == "__main__":
    output_file = main()
    
    # Auto-open the file
    print("🔄 Attempting to open file in Excel...")
    import subprocess
    try:
        subprocess.run(['start', output_file], shell=True)
    except Exception as e:
        print(f"⚠️  Could not auto-open file: {e}")
        print(f"   Please open manually: {output_file}")
