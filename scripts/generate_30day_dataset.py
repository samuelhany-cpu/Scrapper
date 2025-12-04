"""
30-Day Flight Data Generator
Uses 7 days of REAL collected data and intelligently extends to 30 days
based on weekly schedule patterns (flights typically repeat weekly)
"""

import pandas as pd
from datetime import datetime, timedelta
import os


def extend_7days_to_30days(input_csv, output_csv):
    """
    Extend 7 days of real flight data to 60 days by repeating weekly patterns
    Airlines typically have weekly schedules that repeat
    """
    
    print("=" * 100)
    print("📊 EXTENDING 7-DAY DATA TO 60-DAY DATASET")
    print("=" * 100)
    
    # Read the 7-day data
    print("\n📖 Reading 7-day data...")
    df = pd.read_csv(input_csv, encoding='utf-8-sig')
    
    print(f"   ✅ Loaded {len(df)} flights from {df['flight_date'].min()} to {df['flight_date'].max()}")
    
    # Convert flight_date to datetime
    df['flight_date'] = pd.to_datetime(df['flight_date'])
    
    # Get date range
    min_date = df['flight_date'].min()
    max_date = df['flight_date'].max()
    days_collected = (max_date - min_date).days + 1
    
    print(f"   📅 Date range: {days_collected} days")
    
    # Create extended dataset
    print(f"\n🔄 Extending to 60 days using weekly pattern repetition...")
    
    all_flights = []
    
    # Keep original 7 days
    all_flights.append(df.copy())
    print(f"   Week 1 (Real data): {len(df)} flights")
    
    # Replicate for additional weeks (60 days = ~8.5 weeks)
    for week in range(1, 9):  # Weeks 2-9 (to get 60+ days)
        week_df = df.copy()
        
        # Shift dates by week offset
        week_df['flight_date'] = week_df['flight_date'] + timedelta(days=week*7)
        
        # Update collected_at timestamp
        week_df['collected_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Add note about data source
        week_df['data_source'] = week_df['data_source'] + f' (Week {week+1} projection)'
        
        all_flights.append(week_df)
        print(f"   Week {week+1} (Projected): {len(week_df)} flights")
    
    # Combine all weeks
    extended_df = pd.concat(all_flights, ignore_index=True)
    
    # Trim to exactly 60 days
    target_end_date = min_date + timedelta(days=59)
    extended_df = extended_df[extended_df['flight_date'] <= target_end_date]
    
    # Sort by date and flight number
    extended_df = extended_df.sort_values(['flight_date', 'flight_number'])
    
    print(f"\n📊 EXTENDED DATASET SUMMARY:")
    print(f"   Total Flights: {len(extended_df)}")
    print(f"   Date Range: {extended_df['flight_date'].min().strftime('%Y-%m-%d')} to {extended_df['flight_date'].max().strftime('%Y-%m-%d')}")
    print(f"   Days Covered: {(extended_df['flight_date'].max() - extended_df['flight_date'].min()).days + 1}")
    print(f"   Unique Flight Numbers: {extended_df['flight_number'].nunique()}")
    print(f"   Unique Aircraft: {extended_df[extended_df['tail_number'] != 'Unknown']['tail_number'].nunique()}")
    print(f"   Unique Routes: {extended_df[['origin_code', 'destination_code']].drop_duplicates().shape[0]}")
    
    # Save to CSV
    print(f"\n💾 Saving to: {output_csv}")
    extended_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    
    print(f"✅ COMPLETE!")
    print("=" * 100)
    
    return output_csv, extended_df


def analyze_30day_data(df):
    """Generate comprehensive analysis"""
    
    print("\n" + "=" * 100)
    print("📊 60-DAY EGYPTAIR FLIGHT DATA ANALYSIS")
    print("=" * 100)
    
    print(f"\n📈 OVERVIEW:")
    print(f"   Total Flights: {len(df)}")
    print(f"   Date Range: {df['flight_date'].min().strftime('%Y-%m-%d')} to {df['flight_date'].max().strftime('%Y-%m-%d')}")
    print(f"   Duration: {(pd.to_datetime(df['flight_date'].max()) - pd.to_datetime(df['flight_date'].min())).days + 1} days")
    print(f"   Average per Day: {len(df) / ((pd.to_datetime(df['flight_date'].max()) - pd.to_datetime(df['flight_date'].min())).days + 1):.1f} flights")
    
    print(f"\n✈️  FLEET:")
    known_tails = df[df['tail_number'] != 'Unknown']
    print(f"   Unique Aircraft: {known_tails['tail_number'].nunique()}")
    print(f"   Flights with Tail Numbers: {len(known_tails)} ({len(known_tails)/len(df)*100:.1f}%)")
    
    print(f"\n🌍 ROUTES:")
    print(f"   Unique Routes: {df[['origin_code', 'destination_code']].drop_duplicates().shape[0]}")
    print(f"   Unique Flight Numbers: {df['flight_number'].nunique()}")
    
    print(f"\n🛩️  TOP 10 MOST ACTIVE AIRCRAFT:")
    if len(known_tails) > 0:
        tail_counts = known_tails['tail_number'].value_counts().head(10)
        for tail, count in tail_counts.items():
            aircraft_type = known_tails[known_tails['tail_number'] == tail]['aircraft_type'].iloc[0]
            print(f"   {tail} ({aircraft_type}): {count} flights")
    
    print(f"\n✈️  TOP 10 DESTINATIONS:")
    dest_counts = df[df['destination_code'] != 'N/A']['destination_code'].value_counts().head(10)
    for dest, count in dest_counts.items():
        dest_name = df[df['destination_code'] == dest]['destination'].iloc[0]
        print(f"   {dest} ({dest_name}): {count} flights")
    
    print(f"\n📅 FLIGHTS PER WEEK:")
    df['flight_date'] = pd.to_datetime(df['flight_date'])
    df['week'] = df['flight_date'].dt.isocalendar().week
    week_counts = df.groupby('week').size().sort_index()
    for week, count in week_counts.items():
        week_dates = df[df['week'] == week]['flight_date']
        print(f"   Week {week}: {count} flights ({week_dates.min().strftime('%b %d')} - {week_dates.max().strftime('%b %d')})")
    
    print("\n" + "=" * 100)


def main():
    """Main execution"""
    
    # File paths
    script_dir = os.path.dirname(__file__)
    outputs_dir = os.path.join(script_dir, '..', 'outputs')
    
    input_csv = os.path.join(outputs_dir, 'egyptair_30days_comprehensive_20251130_180822.csv')
    output_csv = os.path.join(outputs_dir, f'egyptair_FULL_60DAYS_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    
    print("\n" + "=" * 100)
    print(" " * 25 + "✈️  60-DAY EGYPTAIR FLIGHT DATA GENERATOR ✈️")
    print("=" * 100)
    print("\n📋 Method: Weekly Pattern Replication")
    print("   • Airlines typically repeat schedules weekly")
    print("   • Using 7 days of REAL data from AeroDataBox")
    print("   • Projecting 8 additional weeks based on pattern")
    print("   • Result: Realistic 60-day dataset\n")
    
    # Extend data
    output_path, df = extend_7days_to_30days(input_csv, output_csv)
    
    # Analyze
    analyze_30day_data(df)
    
    # Final message
    print(f"\n✅ SUCCESS!")
    print(f"📄 60-day dataset saved to:")
    print(f"   {output_path}")
    print(f"\n💡 To view:")
    print(f"   start {output_path}")
    print("\n" + "=" * 100 + "\n")
    
    return output_path


if __name__ == "__main__":
    output_file = main()
    
    # Auto-open the file
    import subprocess
    subprocess.run(['start', output_file], shell=True)
