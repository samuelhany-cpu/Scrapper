"""
Analyze today's flights and add more realistic live data
"""
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Load the status-fixed file
file_path = 'F:/Scrapper/outputs/egyptair_HISTORICAL_2015-2025_20251130_183044_enriched_20251130_183634_status_fixed_20251130_184452.csv'

print("=" * 100)
print("📊 ANALYZING TODAY'S FLIGHTS")
print("=" * 100)

df = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False)
df['flight_date'] = pd.to_datetime(df['flight_date'])

now = datetime.now()
today = now.date()

# Get today's flights
today_flights = df[df['flight_date'].dt.date == today]

print(f"\nCurrent time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n✈️  TODAY'S FLIGHTS ({today}):")
print(f"   Total: {len(today_flights)} flights")

if len(today_flights) > 0:
    print(f"\n📊 Status breakdown:")
    status_counts = today_flights['status'].value_counts()
    for status, count in status_counts.items():
        print(f"   {status}: {count}")
    
    print(f"\n⏰ Sample of today's flights:")
    sample = today_flights[['flight_number', 'origin_code', 'destination_code', 
                            'scheduled_departure', 'scheduled_arrival', 'status', 'tail_number']].head(20)
    print(sample.to_string(index=False))

# Check last few days
print(f"\n📅 Recent days flight counts:")
for i in range(7):
    check_date = today - timedelta(days=i)
    count = len(df[df['flight_date'].dt.date == check_date])
    print(f"   {check_date}: {count} flights")

print("\n" + "=" * 100)
