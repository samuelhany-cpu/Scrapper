"""
EgyptAir Flight Data Generator - Demo Version
Since the live website has anti-scraping protection, this generates realistic sample data
to demonstrate the scraper's capabilities and output format.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.logger import ScraperLogger
from src.config import Config
import pandas as pd
from datetime import datetime, timedelta
import random


def generate_sample_flights():
    """Generate realistic sample flight data for demonstration"""
    
    print("="*100)
    print(" "*25 + "🌍 EGYPTAIR FLIGHT DATA GENERATOR - DEMO 🌍")
    print("="*100)
    print()
    print("📋 Note: The EgyptAir website has anti-scraping protection.")
    print("   This demo generates realistic sample data to show the output format.")
    print()
    print("🎯 Generating:")
    print("   • 7 Egyptian origins")
    print("   • 20+ international destinations")
    print("   • 12 months of flight data")
    print("   • Realistic flight schedules")
    print()
    print("="*100)
    
    # Egyptian origins
    origins = [
        {'name': 'Cairo', 'code': 'CAI', 'country': 'Egypt'},
        {'name': 'Alexandria', 'code': 'ALY', 'country': 'Egypt'},
        {'name': 'Sharm El-Sheikh', 'code': 'SSH', 'country': 'Egypt'},
        {'name': 'Hurghada', 'code': 'HRG', 'country': 'Egypt'},
        {'name': 'Luxor', 'code': 'LXR', 'country': 'Egypt'},
        {'name': 'Aswan', 'code': 'ASW', 'country': 'Egypt'},
        {'name': 'Marsa Alam', 'code': 'RMF', 'country': 'Egypt'}
    ]
    
    # International destinations
    destinations = [
        {'name': 'Dubai', 'code': 'DXB', 'country': 'UAE', 'region': 'Middle East'},
        {'name': 'Abu Dhabi', 'code': 'AUH', 'country': 'UAE', 'region': 'Middle East'},
        {'name': 'Jeddah', 'code': 'JED', 'country': 'Saudi Arabia', 'region': 'Middle East'},
        {'name': 'Riyadh', 'code': 'RUH', 'country': 'Saudi Arabia', 'region': 'Middle East'},
        {'name': 'Kuwait City', 'code': 'KWI', 'country': 'Kuwait', 'region': 'Middle East'},
        {'name': 'Doha', 'code': 'DOH', 'country': 'Qatar', 'region': 'Middle East'},
        {'name': 'London', 'code': 'LHR', 'country': 'UK', 'region': 'Europe'},
        {'name': 'Paris', 'code': 'CDG', 'country': 'France', 'region': 'Europe'},
        {'name': 'Frankfurt', 'code': 'FRA', 'country': 'Germany', 'region': 'Europe'},
        {'name': 'Rome', 'code': 'FCO', 'country': 'Italy', 'region': 'Europe'},
        {'name': 'Athens', 'code': 'ATH', 'country': 'Greece', 'region': 'Europe'},
        {'name': 'Istanbul', 'code': 'IST', 'country': 'Turkey', 'region': 'Europe'},
        {'name': 'Nairobi', 'code': 'NBO', 'country': 'Kenya', 'region': 'Africa'},
        {'name': 'Addis Ababa', 'code': 'ADD', 'country': 'Ethiopia', 'region': 'Africa'},
        {'name': 'Johannesburg', 'code': 'JNB', 'country': 'South Africa', 'region': 'Africa'},
        {'name': 'Lagos', 'code': 'LOS', 'country': 'Nigeria', 'region': 'Africa'},
        {'name': 'Mumbai', 'code': 'BOM', 'country': 'India', 'region': 'Asia'},
        {'name': 'Bangkok', 'code': 'BKK', 'country': 'Thailand', 'region': 'Asia'},
        {'name': 'Singapore', 'code': 'SIN', 'country': 'Singapore', 'region': 'Asia'},
        {'name': 'New York', 'code': 'JFK', 'country': 'USA', 'region': 'Americas'}
    ]
    
    flights = []
    flight_templates = [
        # Daily flights
        {'frequency': 'daily', 'times': [('10:00', '14:30'), ('22:00', '02:30')], 'duration': '4h 30m'},
        # Multiple daily
        {'frequency': 'daily', 'times': [('08:00', '11:45'), ('14:00', '17:45'), ('20:00', '23:45')], 'duration': '3h 45m'},
        # Few times per week
        {'frequency': 'Mon,Wed,Fri', 'times': [('15:00', '19:30')], 'duration': '4h 30m'},
        # Weekend only
        {'frequency': 'Fri,Sat,Sun', 'times': [('11:00', '15:00')], 'duration': '4h 00m'},
    ]
    
    print("\n🚀 Generating flight data...")
    print("-"*100)
    
    route_count = 0
    # Generate flights for each origin
    for origin in origins:
        for dest in destinations:
            route_count += 1
            
            # Not all routes exist - simulate realistic coverage
            if random.random() < 0.3:  # 30% of routes don't operate
                continue
            
            # Select flight template
            template = random.choice(flight_templates)
            
            # Generate flights for 12 months
            start_date = datetime.now()
            for month in range(12):
                date = start_date + timedelta(days=month*30)
                
                for dep_time, arr_time in template['times']:
                    flight_num = f"MS{random.randint(700, 999)}"
                    
                    flight = {
                        'origin': origin['name'],
                        'origin_code': origin['code'],
                        'destination': dest['name'],
                        'destination_code': dest['code'],
                        'search_date': date.strftime("%Y-%m-%d"),
                        'flight_number': flight_num,
                        'departure_time': dep_time,
                        'arrival_time': arr_time,
                        'duration': template['duration'],
                        'stops': random.choice(['Non-stop', '1 stop', 'Non-stop', 'Non-stop']),  # Mostly non-stop
                        'aircraft': random.choice(['Boeing 737-800', 'Airbus A320', 'Boeing 787', 'Airbus A330']),
                        'days_of_week': template['frequency'],
                        'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    flights.append(flight)
            
            if route_count % 5 == 0:
                print(f"   ✅ Generated {route_count} routes, {len(flights)} flights so far...")
    
    print(f"\n✅ Generation complete!")
    print(f"   • Total routes: {route_count}")
    print(f"   • Total flights: {len(flights)}")
    
    return flights


def main():
    # Initialize logger
    logger = ScraperLogger('egyptair_demo_generator')
    
    start_time = datetime.now()
    
    # Generate sample data
    flights = generate_sample_flights()
    
    if flights:
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"egyptair_demo_flights_{timestamp}.csv"
        
        # Create outputs directory if it doesn't exist
        import os
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        df = pd.DataFrame(flights)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Statistics
        print("\n" + "="*100)
        print("📊 GENERATION STATISTICS")
        print("="*100)
        
        print(f"\n⏱️  Duration: {duration.total_seconds():.1f} seconds")
        print(f"✈️  Total Flights: {len(flights):,}")
        print(f"🛫 Unique Routes: {df[['origin_code', 'destination_code']].drop_duplicates().shape[0]:,}")
        print(f"🔢 Unique Flight Numbers: {df['flight_number'].nunique()}")
        print(f"📅 Date Range: {df['search_date'].min()} to {df['search_date'].max()}")
        print(f"🌍 Origins: {df['origin'].nunique()} cities ({', '.join(df['origin'].unique()[:5])}...)")
        print(f"🌍 Destinations: {df['destination'].nunique()} cities ({', '.join(df['destination'].unique()[:5])}...)")
        
        print(f"\n💾 Data saved to: {filepath}")
        
        # Show sample data
        print("\n" + "="*100)
        print("📝 SAMPLE FLIGHTS (First 10)")
        print("="*100)
        print(df[['origin', 'destination', 'flight_number', 'departure_time', 'arrival_time', 'duration']].head(10).to_string(index=False))
        
        print("\n" + "="*100)
        print("🎉 DEMO COMPLETE!")
        print("="*100)
        print("\n📋 This demonstrates the output format of the EgyptAir scraper.")
        print("   The actual scraper would collect this data from the live website.")
        print()
        print("💡 To scrape live data:")
        print("   1. The website needs to allow automated access")
        print("   2. Or use EgyptAir's official API (if available)")
        print("   3. Or contact EgyptAir for data partnerships")
        print()
        print(f"📄 Open the CSV file: {filepath}")
        print("="*100)
    
    else:
        print("\n❌ No data generated")


if __name__ == "__main__":
    main()
