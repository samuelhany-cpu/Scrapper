"""
View and analyze flight data with tail numbers
"""

import pandas as pd
import sys
import os

# Load the data
csv_file = 'F:/Scrapper/outputs/egyptair_real_flights_20251130_173546.csv'
df = pd.read_csv(csv_file)

print("="*120)
print(" "*40 + "✈️  EGYPTAIR FLIGHT DATA WITH TAIL NUMBERS")
print("="*120)

# Overview statistics
print("\n📊 OVERVIEW")
print("-"*120)
print(f"Total Flights: {len(df):,}")
print(f"Unique Routes: {df[['origin_code', 'destination_code']].drop_duplicates().shape[0]}")
print(f"Unique Flight Numbers: {df['flight_number'].nunique()}")
print(f"Unique Aircraft (Tail Numbers): {df['tail_number'].nunique()}")
print(f"Aircraft Types: {', '.join(df['aircraft_type'].unique())}")
print(f"Date Range: {df['search_date'].min()} to {df['search_date'].max()}")

# Sample flights with all details
print("\n" + "="*120)
print("📝 SAMPLE FLIGHTS - COMPLETE DETAILS")
print("="*120)
sample_cols = ['flight_number', 'tail_number', 'aircraft_type', 'origin_code', 'destination_code', 
               'departure_time', 'arrival_time', 'duration', 'search_date']
print(df[sample_cols].head(20).to_string(index=False, max_colwidth=20))

# Aircraft fleet details
print("\n" + "="*120)
print("✈️  EGYPTAIR FLEET - ALL AIRCRAFT WITH TAIL NUMBERS")
print("="*120)
fleet = df[['tail_number', 'aircraft_type']].drop_duplicates().sort_values('tail_number')
print(f"\nTotal Aircraft in Fleet: {len(fleet)}\n")

for aircraft_type in sorted(fleet['aircraft_type'].unique()):
    tails = fleet[fleet['aircraft_type'] == aircraft_type]['tail_number'].tolist()
    print(f"\n{aircraft_type}:")
    for i, tail in enumerate(tails, 1):
        flights_count = len(df[df['tail_number'] == tail])
        print(f"   {i}. {tail} - {flights_count} flights")

# Aircraft utilization
print("\n" + "="*120)
print("📈 AIRCRAFT UTILIZATION ANALYSIS")
print("="*120)

print("\n🔝 Top 10 Most Used Aircraft:")
top_aircraft = df['tail_number'].value_counts().head(10)
for tail, count in top_aircraft.items():
    aircraft_type = df[df['tail_number'] == tail]['aircraft_type'].iloc[0]
    print(f"   {tail} ({aircraft_type}): {count} flights")

print("\n🔻 Top 10 Least Used Aircraft:")
bottom_aircraft = df['tail_number'].value_counts().tail(10)
for tail, count in bottom_aircraft.items():
    aircraft_type = df[df['tail_number'] == tail]['aircraft_type'].iloc[0]
    print(f"   {tail} ({aircraft_type}): {count} flights")

# Route-specific aircraft assignment
print("\n" + "="*120)
print("🛫 ROUTE-SPECIFIC AIRCRAFT ASSIGNMENTS")
print("="*120)

for route in df[['origin_code', 'destination_code']].drop_duplicates().values:
    origin, dest = route
    route_flights = df[(df['origin_code'] == origin) & (df['destination_code'] == dest)]
    
    print(f"\n{origin} → {dest}:")
    print(f"   Total flights: {len(route_flights)}")
    print(f"   Aircraft used: {route_flights['tail_number'].nunique()}")
    print(f"   Aircraft types: {', '.join(route_flights['aircraft_type'].unique())}")
    
    # Most common aircraft on this route
    common_aircraft = route_flights['tail_number'].value_counts().head(3)
    print(f"   Most used aircraft:")
    for tail, count in common_aircraft.items():
        aircraft_type = route_flights[route_flights['tail_number'] == tail]['aircraft_type'].iloc[0]
        print(f"      • {tail} ({aircraft_type}): {count} flights")

# Flight number to tail number mapping
print("\n" + "="*120)
print("🔗 FLIGHT NUMBER → TAIL NUMBER MAPPING")
print("="*120)

for flight_num in sorted(df['flight_number'].unique()):
    flight_data = df[df['flight_number'] == flight_num]
    route = f"{flight_data['origin_code'].iloc[0]} → {flight_data['destination_code'].iloc[0]}"
    tails = flight_data['tail_number'].unique()
    
    print(f"\n{flight_num} ({route}):")
    print(f"   Route: {route}")
    print(f"   Total operations: {len(flight_data)}")
    print(f"   Aircraft rotation ({len(tails)} aircraft):")
    
    for tail in tails:
        count = len(flight_data[flight_data['tail_number'] == tail])
        aircraft_type = flight_data[flight_data['tail_number'] == tail]['aircraft_type'].iloc[0]
        percentage = (count / len(flight_data)) * 100
        print(f"      • {tail} ({aircraft_type}): {count} flights ({percentage:.1f}%)")

# Daily aircraft schedule example
print("\n" + "="*120)
print("📅 SAMPLE DAILY SCHEDULE - Aircraft Tracking")
print("="*120)

sample_date = df['search_date'].iloc[0]
daily_flights = df[df['search_date'] == sample_date].sort_values('departure_time')

print(f"\nDate: {sample_date}")
print(f"Total flights: {len(daily_flights)}\n")

print(f"{'Time':<12} {'Flight':<10} {'Route':<15} {'Tail Number':<12} {'Aircraft Type':<20}")
print("-"*80)

for _, flight in daily_flights.iterrows():
    time = flight['departure_time']
    flight_num = flight['flight_number']
    route = f"{flight['origin_code']}→{flight['destination_code']}"
    tail = flight['tail_number']
    aircraft = flight['aircraft_type']
    
    print(f"{time:<12} {flight_num:<10} {route:<15} {tail:<12} {aircraft:<20}")

# Statistics summary
print("\n" + "="*120)
print("📊 FLEET STATISTICS SUMMARY")
print("="*120)

print(f"\n✈️  Fleet Composition:")
for aircraft_type in sorted(df['aircraft_type'].unique()):
    count = len(df[df['aircraft_type'] == aircraft_type]['tail_number'].unique())
    total_flights = len(df[df['aircraft_type'] == aircraft_type])
    avg_flights = total_flights / count if count > 0 else 0
    print(f"   {aircraft_type}: {count} aircraft, {total_flights} total flights (avg {avg_flights:.1f} flights/aircraft)")

print(f"\n📈 Overall Metrics:")
print(f"   Average flights per aircraft: {len(df) / df['tail_number'].nunique():.1f}")
print(f"   Average aircraft per route: {df.groupby(['origin_code', 'destination_code'])['tail_number'].nunique().mean():.1f}")
print(f"   Average aircraft per flight number: {df.groupby('flight_number')['tail_number'].nunique().mean():.1f}")

print("\n" + "="*120)
print("✅ ANALYSIS COMPLETE")
print("="*120)

print(f"\n📄 Data source: {csv_file}")
print("\n💡 This data shows the relationship between:")
print("   • Flight numbers (e.g., MS915)")
print("   • Tail numbers/registrations (e.g., SU-GDN)")  
print("   • Aircraft types (e.g., Boeing 777-300ER)")
print("   • Routes and schedules")

print("\n🔑 Key Insights:")
print("   • Each flight number can be operated by multiple aircraft")
print("   • Aircraft rotate across different routes")
print("   • Tail numbers uniquely identify each physical airplane")
print("   • Long-haul routes use larger aircraft (777, 787, A330)")

print("\n" + "="*120)
