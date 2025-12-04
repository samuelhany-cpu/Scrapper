"""
Real EgyptAir Flight Data Collector using Aviation APIs

This script collects REAL flight data from aviation APIs:
1. AviationStack - Flight schedules and routes
2. FlightAware - Real-time flight tracking with tail numbers
3. AeroDataBox - Aircraft registration details

Features:
- Real flight schedules
- Aircraft tail numbers (registration)
- Live flight tracking
- Historical data
- Route information
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
import pandas as pd
from datetime import datetime, timedelta
from src.logger import ScraperLogger
import time


class RealFlightDataCollector:
    """Collect real flight data from aviation APIs"""
    
    def __init__(self, logger):
        self.logger = logger
        self.all_flights = []
        
        # API Keys - Users should replace with their own
        # Get free API keys from:
        # AviationStack: https://aviationstack.com/ (Free: 500 requests/month)
        # AeroAPI (FlightAware): https://www.flightaware.com/commercial/aeroapi/
        # AeroDataBox: https://www.aerodatabox.com/
        
        self.aviation_stack_key = "YOUR_AVIATIONSTACK_KEY"  # Replace with actual key
        self.flightaware_key = "YOUR_FLIGHTAWARE_KEY"  # Replace with actual key
        self.aerodatabox_key = "00a3084153msh026037bafc6de04p1c4846jsn46d830e5e1bb"  # RapidAPI Key
        self.rapidapi_host = "aerodatabox.p.rapidapi.com"  # RapidAPI Host
        
        # API endpoints
        self.aviation_stack_base = "http://api.aviationstack.com/v1"
        self.flightaware_base = "https://aeroapi.flightaware.com/aeroapi"
        self.aerodatabox_base = "https://aerodatabox.p.rapidapi.com"
        
    def get_egyptair_routes_aviationstack(self):
        """Get EgyptAir routes using AviationStack API"""
        self.logger.info("Fetching EgyptAir routes from AviationStack...")
        
        try:
            url = f"{self.aviation_stack_base}/routes"
            params = {
                'access_key': self.aviation_stack_key,
                'airline_iata': 'MS',  # EgyptAir IATA code
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    self.logger.info(f"✅ Found {len(data['data'])} routes")
                    return data['data']
                else:
                    self.logger.warning(f"API Response: {data}")
            else:
                self.logger.error(f"API Error: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error fetching routes: {e}")
        
        return []
    
    def get_flights_by_route_aviationstack(self, dep_iata, arr_iata, date=None):
        """Get flights for a specific route using AviationStack"""
        if date is None:
            date = datetime.now()
        
        try:
            url = f"{self.aviation_stack_base}/flights"
            params = {
                'access_key': self.aviation_stack_key,
                'airline_iata': 'MS',
                'dep_iata': dep_iata,
                'arr_iata': arr_iata,
                'flight_date': date.strftime('%Y-%m-%d')
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                self.logger.warning(f"Error for {dep_iata}→{arr_iata}: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error: {e}")
        
        return []
    
    def get_flight_with_tail_flightaware(self, flight_number, date=None):
        """Get flight details including tail number from FlightAware"""
        if date is None:
            date = datetime.now()
        
        try:
            # FlightAware AeroAPI endpoint
            url = f"{self.flightaware_base}/flights/{flight_number}"
            headers = {
                'x-apikey': self.flightaware_key
            }
            params = {
                'start': date.strftime('%Y-%m-%dT00:00:00Z'),
                'end': date.strftime('%Y-%m-%dT23:59:59Z')
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                flights = data.get('flights', [])
                
                if flights:
                    flight = flights[0]
                    return {
                        'tail_number': flight.get('registration', 'N/A'),
                        'aircraft_type': flight.get('aircraft_type', 'N/A'),
                        'origin': flight.get('origin', {}).get('code', 'N/A'),
                        'destination': flight.get('destination', {}).get('code', 'N/A'),
                        'departure_time': flight.get('scheduled_off', 'N/A'),
                        'arrival_time': flight.get('scheduled_on', 'N/A'),
                        'status': flight.get('status', 'N/A')
                    }
                    
        except Exception as e:
            self.logger.error(f"FlightAware error for {flight_number}: {e}")
        
        return None
    
    def get_aircraft_details_aerodatabox(self, tail_number):
        """Get aircraft details from AeroDataBox"""
        try:
            url = f"{self.aerodatabox_base}/aircrafts/reg/{tail_number}"
            headers = {
                'X-RapidAPI-Key': self.aerodatabox_key,
                'X-RapidAPI-Host': self.rapidapi_host
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'registration': data.get('reg', 'N/A'),
                    'aircraft_type': data.get('typeName', 'N/A'),
                    'manufacturer': data.get('manufacturerName', 'N/A'),
                    'model': data.get('model', 'N/A'),
                    'airline': data.get('airlineName', 'N/A'),
                    'built_year': data.get('built', 'N/A')
                }
                
        except Exception as e:
            self.logger.error(f"AeroDataBox error for {tail_number}: {e}")
        
        return None
    
    def collect_egyptair_data(self, use_demo_mode=False):
        """
        Collect comprehensive EgyptAir flight data
        
        Args:
            use_demo_mode: If True, uses demo data. If False, uses real APIs
        """
        
        if use_demo_mode or self.aviation_stack_key == "YOUR_AVIATIONSTACK_KEY":
            self.logger.info("⚠️  Running in DEMO mode (no API keys configured)")
            self.logger.info("To use real APIs, get free keys from:")
            self.logger.info("  • AviationStack: https://aviationstack.com/")
            self.logger.info("  • FlightAware: https://www.flightaware.com/")
            self.logger.info("  • AeroDataBox: https://rapidapi.com/aerodatabox/")
            return self._collect_demo_data_with_tails()
        
        self.logger.info("🚀 Collecting REAL flight data from APIs...")
        
        # Egyptian airports
        egyptian_airports = ['CAI', 'ALY', 'SSH', 'HRG', 'LXR', 'ASW', 'RMF']
        
        # Major international destinations
        destinations = [
            'DXB', 'AUH', 'JED', 'RUH', 'KWI', 'DOH',  # Middle East
            'LHR', 'CDG', 'FRA', 'FCO', 'ATH', 'IST',  # Europe
            'NBO', 'ADD', 'JNB', 'LOS',  # Africa
            'BOM', 'BKK', 'SIN', 'JFK'  # Asia & Americas
        ]
        
        # Collect data for next 30 days
        start_date = datetime.now()
        
        for origin in egyptian_airports:
            for dest in destinations:
                for day_offset in range(0, 30, 7):  # Weekly sampling
                    date = start_date + timedelta(days=day_offset)
                    
                    self.logger.info(f"📍 Fetching: {origin} → {dest} on {date.strftime('%Y-%m-%d')}")
                    
                    # Get flights from AviationStack
                    flights = self.get_flights_by_route_aviationstack(origin, dest, date)
                    
                    for flight_data in flights:
                        flight_number = flight_data.get('flight', {}).get('iata', '')
                        
                        # Get tail number from FlightAware
                        tail_info = self.get_flight_with_tail_flightaware(flight_number, date)
                        
                        flight_record = {
                            'origin': flight_data.get('departure', {}).get('airport', ''),
                            'origin_code': flight_data.get('departure', {}).get('iata', ''),
                            'destination': flight_data.get('arrival', {}).get('airport', ''),
                            'destination_code': flight_data.get('arrival', {}).get('iata', ''),
                            'flight_number': flight_number,
                            'departure_time': flight_data.get('departure', {}).get('scheduled', ''),
                            'arrival_time': flight_data.get('arrival', {}).get('scheduled', ''),
                            'aircraft_type': flight_data.get('aircraft', {}).get('iata', ''),
                            'tail_number': tail_info.get('tail_number', 'N/A') if tail_info else 'N/A',
                            'airline': 'EgyptAir',
                            'status': flight_data.get('flight_status', ''),
                            'search_date': date.strftime('%Y-%m-%d'),
                            'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        self.all_flights.append(flight_record)
                        self.logger.info(f"  ✅ {flight_number} - Tail: {flight_record['tail_number']}")
                    
                    # Rate limiting
                    time.sleep(2)
        
        return self.all_flights
    
    def _collect_demo_data_with_tails(self):
        """Generate demo data with realistic tail numbers"""
        self.logger.info("📊 Generating demo data with tail numbers...")
        
        # EgyptAir fleet - realistic tail numbers
        egyptair_fleet = [
            {'tail': 'SU-GDL', 'type': 'Boeing 777-300ER'},
            {'tail': 'SU-GDM', 'type': 'Boeing 777-300ER'},
            {'tail': 'SU-GDN', 'type': 'Boeing 777-300ER'},
            {'tail': 'SU-GDO', 'type': 'Boeing 777-300ER'},
            {'tail': 'SU-GDR', 'type': 'Boeing 777-300ER'},
            {'tail': 'SU-GEM', 'type': 'Boeing 787-9'},
            {'tail': 'SU-GEN', 'type': 'Boeing 787-9'},
            {'tail': 'SU-GEO', 'type': 'Boeing 787-9'},
            {'tail': 'SU-GEP', 'type': 'Boeing 787-9'},
            {'tail': 'SU-GEQ', 'type': 'Boeing 787-9'},
            {'tail': 'SU-GBZ', 'type': 'Airbus A330-300'},
            {'tail': 'SU-GCA', 'type': 'Airbus A330-300'},
            {'tail': 'SU-GCB', 'type': 'Airbus A330-300'},
            {'tail': 'SU-GCC', 'type': 'Airbus A330-300'},
            {'tail': 'SU-GCD', 'type': 'Airbus A330-300'},
            {'tail': 'SU-GDE', 'type': 'Airbus A330-200'},
            {'tail': 'SU-GCE', 'type': 'Airbus A321-200'},
            {'tail': 'SU-GCF', 'type': 'Airbus A321-200'},
            {'tail': 'SU-GCG', 'type': 'Airbus A321-200'},
            {'tail': 'SU-GCH', 'type': 'Airbus A320-200'},
            {'tail': 'SU-GCI', 'type': 'Airbus A320-200'},
            {'tail': 'SU-GCJ', 'type': 'Airbus A320-200'},
            {'tail': 'SU-GCK', 'type': 'Boeing 737-800'},
            {'tail': 'SU-GCL', 'type': 'Boeing 737-800'},
            {'tail': 'SU-GCM', 'type': 'Boeing 737-800'},
        ]
        
        routes = [
            {'origin': 'Cairo', 'origin_code': 'CAI', 'dest': 'Dubai', 'dest_code': 'DXB', 'flights': ['MS915', 'MS917', 'MS919']},
            {'origin': 'Cairo', 'origin_code': 'CAI', 'dest': 'London', 'dest_code': 'LHR', 'flights': ['MS777', 'MS779']},
            {'origin': 'Cairo', 'origin_code': 'CAI', 'dest': 'Paris', 'dest_code': 'CDG', 'flights': ['MS799', 'MS797']},
            {'origin': 'Cairo', 'origin_code': 'CAI', 'dest': 'New York', 'dest_code': 'JFK', 'flights': ['MS985', 'MS986']},
            {'origin': 'Cairo', 'origin_code': 'CAI', 'dest': 'Jeddah', 'dest_code': 'JED', 'flights': ['MS667', 'MS669', 'MS671']},
            {'origin': 'Cairo', 'origin_code': 'CAI', 'dest': 'Riyadh', 'dest_code': 'RUH', 'flights': ['MS631', 'MS633']},
            {'origin': 'Cairo', 'origin_code': 'CAI', 'dest': 'Istanbul', 'dest_code': 'IST', 'flights': ['MS735', 'MS737']},
            {'origin': 'Cairo', 'origin_code': 'CAI', 'dest': 'Frankfurt', 'dest_code': 'FRA', 'flights': ['MS787', 'MS789']},
        ]
        
        import random
        
        flights = []
        start_date = datetime.now()
        
        for route in routes:
            for day in range(30):
                date = start_date + timedelta(days=day)
                
                for flight_num in route['flights']:
                    # Assign aircraft
                    aircraft = random.choice(egyptair_fleet)
                    
                    # Generate times
                    if 'London' in route['dest'] or 'Paris' in route['dest'] or 'New York' in route['dest']:
                        dep_time = f"{random.randint(22, 23)}:{random.randint(0, 59):02d}"
                        duration_hours = random.randint(4, 11)
                    elif 'Dubai' in route['dest'] or 'Jeddah' in route['dest']:
                        dep_time = f"{random.randint(6, 20)}:{random.randint(0, 59):02d}"
                        duration_hours = random.randint(3, 4)
                    else:
                        dep_time = f"{random.randint(8, 18)}:{random.randint(0, 59):02d}"
                        duration_hours = random.randint(3, 6)
                    
                    dep_hour, dep_min = map(int, dep_time.split(':'))
                    arr_hour = (dep_hour + duration_hours) % 24
                    arr_min = (dep_min + random.randint(0, 59)) % 60
                    arr_time = f"{arr_hour:02d}:{arr_min:02d}"
                    
                    flight = {
                        'origin': route['origin'],
                        'origin_code': route['origin_code'],
                        'destination': route['dest'],
                        'destination_code': route['dest_code'],
                        'flight_number': flight_num,
                        'tail_number': aircraft['tail'],  # ← TAIL NUMBER!
                        'aircraft_type': aircraft['type'],
                        'departure_time': dep_time,
                        'arrival_time': arr_time,
                        'duration': f"{duration_hours}h {random.randint(0, 59)}m",
                        'airline': 'EgyptAir',
                        'status': 'Scheduled',
                        'search_date': date.strftime('%Y-%m-%d'),
                        'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    flights.append(flight)
        
        self.all_flights = flights
        return flights
    
    def save_to_csv(self, filename=None):
        """Save flights to CSV"""
        if not self.all_flights:
            self.logger.warning("No flights to save")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"egyptair_real_flights_{timestamp}.csv"
        
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        df = pd.DataFrame(self.all_flights)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        self.logger.info(f"✅ Saved {len(self.all_flights)} flights to: {filepath}")
        return filepath


def main():
    print("="*100)
    print(" "*20 + "✈️  REAL EGYPTAIR FLIGHT DATA COLLECTOR ✈️")
    print("="*100)
    print()
    print("📡 Data Sources:")
    print("   • AviationStack API - Flight schedules")
    print("   • FlightAware API - Real-time tracking + Tail numbers")
    print("   • AeroDataBox API - Aircraft registration details")
    print()
    print("🔑 API Keys:")
    print("   • Get free keys from the websites mentioned above")
    print("   • Edit this script and add your API keys")
    print("   • Free tiers provide 500-1000 requests/month")
    print()
    print("="*100)
    
    # Initialize
    logger = ScraperLogger('egyptair_real_data')
    collector = RealFlightDataCollector(logger)
    
    # Check if API keys are configured
    has_api_keys = (
        collector.aviation_stack_key != "YOUR_AVIATIONSTACK_KEY" and
        collector.flightaware_key != "YOUR_FLIGHTAWARE_KEY"
    )
    
    if has_api_keys:
        print("\n✅ API keys detected - collecting REAL data...")
        print("⏳ This will take several minutes...")
    else:
        print("\n⚠️  No API keys configured - using DEMO mode")
        print("📊 Generating realistic demo data with tail numbers...")
    
    print("\n" + "="*100)
    
    start_time = datetime.now()
    
    # Collect data
    flights = collector.collect_egyptair_data(use_demo_mode=not has_api_keys)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    if flights:
        # Save to CSV
        filepath = collector.save_to_csv()
        
        # Statistics
        df = pd.DataFrame(flights)
        
        print("\n" + "="*100)
        print("📊 COLLECTION STATISTICS")
        print("="*100)
        print(f"⏱️  Duration: {duration.total_seconds():.1f} seconds")
        print(f"✈️  Total Flights: {len(flights):,}")
        print(f"🛫 Unique Routes: {df[['origin_code', 'destination_code']].drop_duplicates().shape[0]}")
        print(f"🔢 Unique Flight Numbers: {df['flight_number'].nunique()}")
        print(f"✈️  Unique Aircraft (Tails): {df['tail_number'].nunique()}")
        print(f"🛩️  Aircraft Types: {df['aircraft_type'].nunique()}")
        print(f"📅 Date Range: {df['search_date'].min()} to {df['search_date'].max()}")
        
        print(f"\n💾 Data saved to: {filepath}")
        
        # Show sample with tail numbers
        print("\n" + "="*100)
        print("📝 SAMPLE FLIGHTS WITH TAIL NUMBERS (First 15)")
        print("="*100)
        print(df[['flight_number', 'tail_number', 'aircraft_type', 'origin_code', 'destination_code', 'departure_time']].head(15).to_string(index=False))
        
        # Aircraft usage statistics
        print("\n" + "="*100)
        print("✈️  AIRCRAFT USAGE (Top 10 by flights)")
        print("="*100)
        aircraft_usage = df.groupby(['tail_number', 'aircraft_type']).size().sort_values(ascending=False).head(10)
        for (tail, aircraft_type), count in aircraft_usage.items():
            print(f"   {tail} ({aircraft_type}): {count} flights")
        
        print("\n" + "="*100)
        print("🎉 DATA COLLECTION COMPLETE!")
        print("="*100)
        
        if not has_api_keys:
            print("\n💡 To collect REAL data:")
            print("   1. Get API keys (free tiers available)")
            print("   2. Edit this script and add your keys")
            print("   3. Run again to get live flight data")
        
        print("\n📄 Open CSV file:")
        print(f"   start {filepath}")
        print("="*100)
    
    else:
        print("\n❌ No flights collected")


if __name__ == "__main__":
    main()
