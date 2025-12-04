"""
Enhance dataset with future flights for better realism
- Extend dataset to include next 30 days (Dec 2025)
- This gives realistic mix of past (Landed) and future (Scheduled) flights
- Today's flights get live statuses (En Route, Boarding, etc.)
"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os

def extend_with_future_flights(input_path, output_path=None):
    """Add future flights to make dataset more realistic"""
    
    print("\n" + "=" * 100)
    print("🚀 EXTENDING DATASET WITH FUTURE FLIGHTS")
    print("=" * 100)
    
    print(f"\n📖 Loading: {input_path}")
    df = pd.read_csv(input_path, encoding='utf-8-sig', low_memory=False)
    
    df['flight_date'] = pd.to_datetime(df['flight_date'])
    
    original_count = len(df)
    max_date = df['flight_date'].max()
    
    print(f"   Current flights: {original_count:,}")
    print(f"   Current date range: {df['flight_date'].min().date()} to {max_date.date()}")
    
    # Get the last 7 days as pattern
    pattern_start = max_date - timedelta(days=6)
    pattern_df = df[df['flight_date'] >= pattern_start].copy()
    
    print(f"\n🔄 Using last 7 days as pattern ({pattern_start.date()} to {max_date.date()})")
    print(f"   Pattern flights: {len(pattern_df)}")
    
    # Extend for next 30 days
    future_flights = []
    days_to_add = 30
    
    print(f"\n📅 Adding {days_to_add} days of future flights...")
    
    for week_offset in range(1, 5):  # 4 weeks
        week_df = pattern_df.copy()
        
        # Shift dates forward
        week_df['flight_date'] = week_df['flight_date'] + timedelta(days=week_offset * 7)
        
        # Update status to Scheduled for all future flights
        week_df['status'] = 'Scheduled'
        
        # Update data source
        if 'data_source' in week_df.columns:
            week_df['data_source'] = week_df['data_source'] + f' (Future projection - Week +{week_offset})'
        
        # Update collected_at
        week_df['collected_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        future_flights.append(week_df)
        print(f"   Week +{week_offset}: {len(week_df)} flights")
    
    # Combine
    print(f"\n📦 Combining all data...")
    all_flights = pd.concat([df] + future_flights, ignore_index=True)
    
    # Trim to exactly 30 days future
    now = datetime.now()
    cutoff_date = now + timedelta(days=30)
    all_flights = all_flights[all_flights['flight_date'] <= cutoff_date]
    
    # Sort
    all_flights = all_flights.sort_values(['flight_date', 'flight_number'])
    
    print(f"\n✅ EXTENDED DATASET:")
    print(f"   Total flights: {len(all_flights):,} (was {original_count:,})")
    print(f"   New date range: {all_flights['flight_date'].min().date()} to {all_flights['flight_date'].max().date()}")
    print(f"   Added: {len(all_flights) - original_count:,} future flights")
    
    # Status distribution
    print(f"\n📊 STATUS DISTRIBUTION:")
    status_counts = all_flights['status'].value_counts()
    for status, count in status_counts.items():
        print(f"   {status}: {count:,} ({count/len(all_flights)*100:.1f}%)")
    
    # Save
    if output_path is None:
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(os.path.dirname(input_path), 
                                   f'egyptair_COMPLETE_2015-2025_EXTENDED_{ts}.csv')
    
    print(f"\n💾 Saving to: {output_path}")
    all_flights.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print("\n✅ COMPLETE!")
    print("=" * 100)
    
    return output_path, all_flights


def main():
    # Use the status-fixed file
    input_path = 'F:/Scrapper/outputs/egyptair_HISTORICAL_2015-2025_20251130_183044_enriched_20251130_183634_status_fixed_20251130_184452.csv'
    
    output_path, df = extend_with_future_flights(input_path)
    
    print(f"\n📄 Final output: {output_path}")
    
    # Show breakdown by date range
    now = datetime.now()
    today = now.date()
    
    past = len(df[pd.to_datetime(df['flight_date']).dt.date < today])
    today_count = len(df[pd.to_datetime(df['flight_date']).dt.date == today])
    future = len(df[pd.to_datetime(df['flight_date']).dt.date > today])
    
    print(f"\n📊 TEMPORAL BREAKDOWN:")
    print(f"   Past (Landed): {past:,} flights")
    print(f"   Today (Live): {today_count:,} flights")
    print(f"   Future (Scheduled): {future:,} flights")
    
    print("\n🔄 Opening in Excel...")
    import subprocess
    try:
        subprocess.run(['start', output_path], shell=True)
    except:
        pass


if __name__ == '__main__':
    main()
