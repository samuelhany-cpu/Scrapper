"""Quick viewer for generated flight data"""
import pandas as pd

df = pd.read_csv('F:/Scrapper/outputs/egyptair_demo_flights_20251130_171251.csv')

print("="*100)
print("📊 EGYPTAIR DEMO FLIGHT DATA")
print("="*100)

print("\n📝 SAMPLE FLIGHTS (First 20):\n")
print(df[['origin', 'destination', 'flight_number', 'departure_time', 'arrival_time', 'duration', 'stops']].head(20).to_string(index=False))

print("\n" + "="*100)
print("📈 STATISTICS")
print("="*100)
print(f"Total Flights: {len(df):,}")
print(f"Unique Routes: {df[['origin', 'destination']].drop_duplicates().shape[0]}")
print(f"Origins: {df['origin'].nunique()} cities - {', '.join(df['origin'].unique())}")
print(f"Destinations: {df['destination'].nunique()} cities")
print(f"Date Range: {df['search_date'].min()} to {df['search_date'].max()}")

print("\n📍 Routes by Origin:")
for origin in df['origin'].unique():
    count = len(df[df['origin'] == origin])
    dests = df[df['origin'] == origin]['destination'].nunique()
    print(f"  {origin}: {count} flights to {dests} destinations")

print("\n✈️ Top 10 Routes:")
routes = df.groupby(['origin', 'destination']).size().sort_values(ascending=False).head(10)
for (origin, dest), count in routes.items():
    print(f"  {origin} → {dest}: {count} flights")

print("\n" + "="*100)
print("✅ Data file: F:/Scrapper/outputs/egyptair_demo_flights_20251130_171251.csv")
print("="*100)
