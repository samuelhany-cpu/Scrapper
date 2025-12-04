"""
Multi-API EgyptAir Flight Data Collector

This script combines multiple FREE aviation APIs:
1. OpenSky Network - Real-time tracking (100% FREE, unlimited, no API key!)
2. AviationStack - Flight schedules (FREE: 500 requests/month)
3. AeroDataBox - Airport data (via RapidAPI)

Features:
- Real-time aircraft positions with tail numbers
- Flight schedules and routes
- Complete EgyptAir fleet tracking
- ICAO24 to registration mapping
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
import pandas as pd
from datetime import datetime, timedelta
from src.logger import ScraperLogger
import time
import json


class MultiAPIFlightCollector:
    """Collect flight data from multiple free APIs"""
    
    def __init__(self, logger):
        self.logger = logger
        self.all_flights = []
        
        # API Keys (get free keys from the APIs)
        self.aviationstack_key = "269c650dce3128bc5062c6a95a35f21f"  # AviationStack API key
        self.rapidapi_key = "00a3084153msh026037bafc6de04p1c4846jsn46d830e5e1bb"  # RapidAPI key
        
        # OpenSky Network - NO API KEY NEEDED! (100% FREE)
        self.opensky_base = "https://opensky-network.org/api"
        
        # AviationStack
        self.aviationstack_base = "http://api.aviationstack.com/v1"
        
        # AeroDataBox
        self.aerodatabox_base = "https://aerodatabox.p.rapidapi.com"
        
        # EgyptAir identifiers
        self.egyptair_iata = "MS"
        self.egyptair_icao = "MSR"
        self.egyptair_callsign_prefix = "MSR"
        
        # Cache for ICAO24 to registration mapping
        self.icao24_to_registration = {}
        
    def get_live_egyptair_flights_opensky(self):
        """
        Get live EgyptAir flights from OpenSky Network
        100% FREE - No API key needed!
        """
        try:
            url = f"{self.opensky_base}/states/all"
            
            self.logger.info("📡 Fetching live flights from OpenSky Network (FREE API)...")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data or 'states' not in data:
                    self.logger.warning("⚠️  No aircraft data returned")
                    return []
                
                # Filter for EgyptAir flights (callsign starts with MSR)
                egyptair_flights = []
                
                for state in data['states']:
                    # state[1] is callsign
                    callsign = state[1].strip() if state[1] else ""
                    
                    if callsign.startswith(self.egyptair_callsign_prefix):
                        flight_data = {
                            'icao24': state[0],  # Unique aircraft identifier
                            'callsign': callsign,
                            'origin_country': state[2],
                            'longitude': state[5],
                            'latitude': state[6],
                            'altitude': state[7],  # meters
                            'velocity': state[9],  # m/s
                            'heading': state[10],  # degrees
                            'vertical_rate': state[11],  # m/s
                            'on_ground': state[8],
                            'last_contact': datetime.fromtimestamp(state[4]).strftime('%Y-%m-%d %H:%M:%S'),
                            'data_source': 'OpenSky Network',
                            'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        egyptair_flights.append(flight_data)
                        
                        self.logger.info(f"✈️  {callsign} | ICAO24: {state[0]} | Alt: {state[7]}m | "
                                       f"Speed: {int(state[9] * 1.94384) if state[9] else 0} knots")
                
                self.logger.info(f"✅ Found {len(egyptair_flights)} live EgyptAir flights")
                return egyptair_flights
            else:
                self.logger.error(f"❌ OpenSky API Error: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"❌ Error fetching from OpenSky: {e}")
            return []
    
    def get_aircraft_registration_opensky(self, icao24):
        """
        Get aircraft registration from ICAO24 address using OpenSky Network
        Returns the tail number (e.g., SU-GDB)
        """
        try:
            # Check cache first
            if icao24 in self.icao24_to_registration:
                return self.icao24_to_registration[icao24]
            
            url = f"{self.opensky_base}/metadata/aircraft/icao/{icao24}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                registration = data.get('registration', 'Unknown')
                
                # Cache the result
                self.icao24_to_registration[icao24] = registration
                
                return registration
            else:
                return 'Unknown'
                
        except Exception as e:
            self.logger.debug(f"Could not get registration for {icao24}: {e}")
            return 'Unknown'
    
    def enrich_with_registrations(self, flights):
        """Add tail numbers (registrations) to flight data"""
        self.logger.info("🔍 Looking up aircraft registrations (tail numbers)...")
        
        for flight in flights:
            if 'icao24' in flight:
                registration = self.get_aircraft_registration_opensky(flight['icao24'])
                flight['tail_number'] = registration
                
                if registration != 'Unknown':
                    self.logger.info(f"   ✓ {flight['callsign']} → Tail: {registration}")
                
                time.sleep(0.5)  # Be nice to the free API
        
        return flights
    
    def get_egyptair_routes_aviationstack(self):
        """
        Get EgyptAir routes from AviationStack API
        Requires free API key from https://aviationstack.com/
        """
        if self.aviationstack_key == "YOUR_AVIATIONSTACK_KEY":
            self.logger.warning("⚠️  AviationStack API key not configured")
            return []
        
        try:
            url = f"{self.aviationstack_base}/routes"
            params = {
                'access_key': self.aviationstack_key,
                'airline_iata': self.egyptair_iata,
                'limit': 100
            }
            
            self.logger.info("📡 Fetching EgyptAir routes from AviationStack...")
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                routes = data.get('data', [])
                self.logger.info(f"✅ Found {len(routes)} routes")
                return routes
            else:
                self.logger.error(f"❌ AviationStack Error: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"❌ Error fetching routes: {e}")
            return []
    
    def get_egyptair_schedules_aviationstack(self, limit=100):
        """
        Get EgyptAir flight schedules from AviationStack
        """
        if self.aviationstack_key == "YOUR_AVIATIONSTACK_KEY":
            self.logger.warning("⚠️  AviationStack API key not configured")
            return []
        
        try:
            url = f"{self.aviationstack_base}/flights"
            params = {
                'access_key': self.aviationstack_key,
                'airline_iata': self.egyptair_iata,
                'limit': limit
            }
            
            self.logger.info("📡 Fetching EgyptAir schedules from AviationStack...")
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                flights = data.get('data', [])
                
                parsed_flights = []
                for flight in flights:
                    parsed = {
                        'flight_number': flight.get('flight', {}).get('iata', 'N/A'),
                        'airline': flight.get('airline', {}).get('name', 'EgyptAir'),
                        'origin_code': flight.get('departure', {}).get('iata', 'N/A'),
                        'origin': flight.get('departure', {}).get('airport', 'N/A'),
                        'destination_code': flight.get('arrival', {}).get('iata', 'N/A'),
                        'destination': flight.get('arrival', {}).get('airport', 'N/A'),
                        'departure_time': flight.get('departure', {}).get('scheduled', 'N/A'),
                        'arrival_time': flight.get('arrival', {}).get('scheduled', 'N/A'),
                        'status': flight.get('flight_status', 'Unknown'),
                        'aircraft_type': flight.get('aircraft', {}).get('type', 'N/A'),
                        'tail_number': flight.get('aircraft', {}).get('registration', 'Unknown'),
                        'data_source': 'AviationStack',
                        'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    parsed_flights.append(parsed)
                
                self.logger.info(f"✅ Found {len(parsed_flights)} scheduled flights")
                return parsed_flights
            else:
                self.logger.error(f"❌ AviationStack Error: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"❌ Error fetching schedules: {e}")
            return []
    
    def combine_data_sources(self, live_flights, scheduled_flights):
        """Combine data from multiple sources"""
        self.logger.info("🔄 Combining data from multiple APIs...")
        
        all_data = []
        
        # Add live flights
        for flight in live_flights:
            all_data.append({
                'flight_type': 'LIVE',
                'flight_number': flight.get('callsign', 'N/A'),
                'tail_number': flight.get('tail_number', 'Unknown'),
                'icao24': flight.get('icao24', 'N/A'),
                'latitude': flight.get('latitude', 'N/A'),
                'longitude': flight.get('longitude', 'N/A'),
                'altitude_m': flight.get('altitude', 'N/A'),
                'speed_knots': int(flight.get('velocity', 0) * 1.94384) if flight.get('velocity') else 'N/A',
                'heading': flight.get('heading', 'N/A'),
                'on_ground': flight.get('on_ground', False),
                'data_source': 'OpenSky Network',
                'last_contact': flight.get('last_contact', 'N/A'),
                'collected_at': flight.get('collected_at', 'N/A')
            })
        
        # Add scheduled flights
        for flight in scheduled_flights:
            all_data.append({
                'flight_type': 'SCHEDULED',
                'flight_number': flight.get('flight_number', 'N/A'),
                'origin_code': flight.get('origin_code', 'N/A'),
                'origin': flight.get('origin', 'N/A'),
                'destination_code': flight.get('destination_code', 'N/A'),
                'destination': flight.get('destination', 'N/A'),
                'departure_time': flight.get('departure_time', 'N/A'),
                'arrival_time': flight.get('arrival_time', 'N/A'),
                'tail_number': flight.get('tail_number', 'Unknown'),
                'aircraft_type': flight.get('aircraft_type', 'N/A'),
                'status': flight.get('status', 'Unknown'),
                'data_source': 'AviationStack',
                'collected_at': flight.get('collected_at', 'N/A')
            })
        
        self.logger.info(f"✅ Combined {len(all_data)} total flights")
        return all_data
    
    def save_to_csv(self, flights, filename=None):
        """Save flights to CSV file"""
        if not flights:
            self.logger.warning("⚠️  No flights to save")
            return None
        
        # Create DataFrame
        df = pd.DataFrame(flights)
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"egyptair_multi_api_{timestamp}.csv"
        
        # Ensure outputs directory exists
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, filename)
        
        # Save to CSV
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        self.logger.info(f"💾 Saved {len(flights)} flights to: {output_path}")
        
        return output_path
    
    def analyze_data(self, flights):
        """Generate analysis of collected flight data"""
        if not flights:
            return
        
        df = pd.DataFrame(flights)
        
        print("\n" + "=" * 100)
        print("📊 MULTI-API FLIGHT DATA ANALYSIS")
        print("=" * 100)
        
        print(f"\n📈 OVERVIEW:")
        print(f"   Total Flights: {len(df)}")
        
        if 'flight_type' in df.columns:
            print(f"\n✈️  FLIGHT TYPES:")
            type_counts = df['flight_type'].value_counts()
            for ftype, count in type_counts.items():
                print(f"   {ftype}: {count} flights")
        
        if 'data_source' in df.columns:
            print(f"\n📡 DATA SOURCES:")
            source_counts = df['data_source'].value_counts()
            for source, count in source_counts.items():
                print(f"   {source}: {count} flights")
        
        # Tail numbers
        if 'tail_number' in df.columns:
            known_tails = df[df['tail_number'] != 'Unknown']
            print(f"\n🛩️  AIRCRAFT WITH TAIL NUMBERS: {len(known_tails)} flights")
            
            if len(known_tails) > 0:
                tail_counts = known_tails['tail_number'].value_counts().head(10)
                for tail, count in tail_counts.items():
                    print(f"   {tail}: {count} flights")
        
        # Sample data
        print(f"\n📋 SAMPLE FLIGHTS:")
        sample = df.head(10)
        display_cols = [col for col in ['flight_number', 'tail_number', 'origin_code', 
                                        'destination_code', 'status', 'data_source'] 
                       if col in df.columns]
        if display_cols:
            print(sample[display_cols].to_string(index=False))
        
        print("\n" + "=" * 100)


def main():
    """Main execution function"""
    # Initialize logger
    logger = ScraperLogger('egyptair_multi_api_collector')
    
    print("\n" + "=" * 100)
    print(" " * 30 + "✈️  EGYPTAIR MULTI-API FLIGHT COLLECTOR ✈️")
    print("=" * 100)
    print("\n📡 Data Sources:")
    print("   1. OpenSky Network - Live tracking (100% FREE, unlimited, no API key!)")
    print("   2. AviationStack - Schedules (FREE: 500/month)")
    print("   3. AeroDataBox - Airport data (via RapidAPI)")
    print("\n" + "=" * 100 + "\n")
    
    # Initialize collector
    collector = MultiAPIFlightCollector(logger)
    
    # Step 1: Get live flights from OpenSky (FREE, no API key!)
    logger.info("=" * 100)
    logger.info("STEP 1: Getting LIVE EgyptAir flights (OpenSky Network - FREE)")
    logger.info("=" * 100)
    live_flights = collector.get_live_egyptair_flights_opensky()
    
    # Step 2: Enrich with tail numbers
    if live_flights:
        logger.info("\n" + "=" * 100)
        logger.info("STEP 2: Looking up aircraft registrations (tail numbers)")
        logger.info("=" * 100)
        live_flights = collector.enrich_with_registrations(live_flights)
    
    # Step 3: Get scheduled flights from AviationStack (if API key configured)
    logger.info("\n" + "=" * 100)
    logger.info("STEP 3: Getting scheduled flights (AviationStack)")
    logger.info("=" * 100)
    scheduled_flights = collector.get_egyptair_schedules_aviationstack(limit=50)
    
    # Step 4: Combine data
    logger.info("\n" + "=" * 100)
    logger.info("STEP 4: Combining data from all sources")
    logger.info("=" * 100)
    all_flights = collector.combine_data_sources(live_flights, scheduled_flights)
    
    if all_flights:
        # Save to CSV
        output_path = collector.save_to_csv(all_flights)
        
        # Analyze data
        collector.analyze_data(all_flights)
        
        print("\n✅ COLLECTION COMPLETE!")
        print(f"📄 Data saved to: {output_path}")
        print("\n💡 To view the data:")
        print(f"   start {output_path}")
        print("\n📚 To get more API keys, see: docs/FREE_AVIATION_APIS.md")
        print("=" * 100 + "\n")
    else:
        logger.error("❌ No flights collected")
        print("\n💡 TIPS:")
        print("   1. OpenSky Network works without API key - might be no flights flying now")
        print("   2. Get free AviationStack key: https://aviationstack.com/")
        print("   3. Check docs/FREE_AVIATION_APIS.md for more options")


if __name__ == "__main__":
    main()
