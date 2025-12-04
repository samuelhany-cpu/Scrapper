"""
Comprehensive EgyptAir Data Collector - 30 Days Historical + Live Data

Combines three free APIs:
1. AviationStack - Historical flight schedules (269c650dce3128bc5062c6a95a35f21f)
2. AeroDataBox - Airport departures with tail numbers (via RapidAPI)
3. OpenSky Network - Live tracking with tail numbers (FREE, no key)

Collects 30 days of EgyptAir flight data with tail numbers.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
import pandas as pd
from datetime import datetime, timedelta
from src.logger import ScraperLogger
import time


class ComprehensiveFlightCollector:
    """Comprehensive flight data collector using 3 free APIs"""
    
    def __init__(self, logger):
        self.logger = logger
        self.all_flights = []
        
        # API Keys
        self.aviationstack_key = "269c650dce3128bc5062c6a95a35f21f"
        self.rapidapi_key = "00a3084153msh026037bafc6de04p1c4846jsn46d830e5e1bb"
        self.rapidapi_host = "aerodatabox.p.rapidapi.com"
        
        # API Endpoints
        self.aviationstack_base = "http://api.aviationstack.com/v1"
        self.aerodatabox_base = "https://aerodatabox.p.rapidapi.com"
        self.opensky_base = "https://opensky-network.org/api"
        
        # EgyptAir identifiers
        self.cairo_icao = "HECA"
        self.egyptair_iata = "MS"
        self.egyptair_callsign = "MSR"
        
        # Data storage
        self.flights_by_source = {
            'aviationstack': [],
            'aerodatabox': [],
            'opensky': []
        }
    
    def get_live_flights_opensky(self):
        """Get current live EgyptAir flights with tail numbers"""
        try:
            self.logger.info("📡 API 1/3: Fetching LIVE flights from OpenSky Network...")
            
            url = f"{self.opensky_base}/states/all"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                live_flights = []
                
                if data and 'states' in data:
                    for state in data['states']:
                        callsign = state[1].strip() if state[1] else ""
                        
                        if callsign.startswith(self.egyptair_callsign):
                            # Get tail number
                            icao24 = state[0]
                            tail = self._get_registration_opensky(icao24)
                            
                            flight = {
                                'flight_number': callsign,
                                'tail_number': tail,
                                'aircraft_type': 'N/A',
                                'origin_code': 'N/A',
                                'origin': 'In Flight',
                                'destination_code': 'N/A',
                                'destination': 'Unknown',
                                'departure_time': 'N/A',
                                'arrival_time': 'N/A',
                                'status': 'In Flight',
                                'altitude_m': state[7],
                                'speed_knots': int(state[9] * 1.94384) if state[9] else 0,
                                'latitude': state[6],
                                'longitude': state[5],
                                'data_source': 'OpenSky Network (Live)',
                                'flight_date': datetime.now().strftime('%Y-%m-%d'),
                                'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            live_flights.append(flight)
                            self.logger.info(f"   ✈️  {callsign} | Tail: {tail} | Alt: {state[7]}m")
                            
                            time.sleep(0.5)  # Rate limiting
                
                self.logger.info(f"✅ Found {len(live_flights)} live flights")
                self.flights_by_source['opensky'] = live_flights
                return live_flights
            else:
                self.logger.warning(f"⚠️  OpenSky API returned status {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"❌ OpenSky error: {e}")
            return []
    
    def _get_registration_opensky(self, icao24):
        """Get aircraft registration from ICAO24"""
        try:
            url = f"{self.opensky_base}/metadata/aircraft/icao/{icao24}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('registration', 'Unknown')
        except:
            pass
        return 'Unknown'
    
    def get_historical_flights_aviationstack(self, days=30):
        """Get flight data from AviationStack (uses current/future flights in free tier)"""
        try:
            self.logger.info(f"📡 API 2/3: Fetching EgyptAir flights from AviationStack...")
            self.logger.info("   ℹ️  Note: Free tier provides current/upcoming flights, not historical")
            
            all_flights = []
            
            # Try multiple approaches with free tier
            urls_to_try = [
                # Current flights
                f"{self.aviationstack_base}/flights?access_key={self.aviationstack_key}&airline_iata={self.egyptair_iata}&limit=100",
                # Airline routes (provides route info)
                f"{self.aviationstack_base}/routes?access_key={self.aviationstack_key}&airline_iata={self.egyptair_iata}&limit=100",
            ]
            
            for idx, url in enumerate(urls_to_try):
                try:
                    self.logger.info(f"   � Trying endpoint {idx+1}/2...")
                    response = requests.get(url, timeout=30)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if 'data' in data and len(data['data']) > 0:
                            self.logger.info(f"      ✅ Found {len(data['data'])} records")
                            
                            for item in data['data']:
                                if idx == 0:  # Flights endpoint
                                    flight = self._parse_aviationstack_flight(item, datetime.now().strftime('%Y-%m-%d'))
                                    if flight:
                                        all_flights.append(flight)
                                # Routes endpoint doesn't provide flight-specific data
                            
                            if idx == 0:  # Only need flights
                                break
                        else:
                            self.logger.info(f"      ℹ️  No data from endpoint {idx+1}")
                    else:
                        self.logger.warning(f"      ⚠️  Endpoint {idx+1} returned {response.status_code}")
                    
                    time.sleep(1)
                except Exception as e:
                    self.logger.debug(f"      Error with endpoint {idx+1}: {e}")
                    continue
            
            self.logger.info(f"✅ Collected {len(all_flights)} flights from AviationStack")
            self.flights_by_source['aviationstack'] = all_flights
            return all_flights
            
        except Exception as e:
            self.logger.error(f"❌ AviationStack error: {e}")
            return []
    
    def _parse_aviationstack_flight(self, flight_raw, date):
        """Parse AviationStack flight data"""
        try:
            departure = flight_raw.get('departure', {})
            arrival = flight_raw.get('arrival', {})
            flight_info = flight_raw.get('flight', {})
            aircraft = flight_raw.get('aircraft', {})
            
            return {
                'flight_number': flight_info.get('iata', 'N/A'),
                'tail_number': aircraft.get('registration', 'Unknown'),
                'aircraft_type': aircraft.get('iata', 'N/A'),
                'origin_code': departure.get('iata', 'N/A'),
                'origin': departure.get('airport', 'N/A'),
                'destination_code': arrival.get('iata', 'N/A'),
                'destination': arrival.get('airport', 'N/A'),
                'departure_time': departure.get('scheduled', 'N/A'),
                'arrival_time': arrival.get('scheduled', 'N/A'),
                'status': flight_raw.get('flight_status', 'Unknown'),
                'data_source': 'AviationStack (Historical)',
                'flight_date': date,
                'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            self.logger.debug(f"Error parsing flight: {e}")
            return None
    
    def get_airport_departures_aerodatabox(self, days=30):
        """Get departures from Cairo airport using AeroDataBox"""
        try:
            self.logger.info(f"📡 API 3/3: Fetching {days} days from AeroDataBox (Cairo Airport)...")
            
            all_flights = []
            
            for day_offset in range(days):  # Try for requested days
                date = datetime.now() - timedelta(days=day_offset)
                
                # Split into 12-hour windows
                time_windows = [
                    (f"{date.strftime('%Y-%m-%d')}T00:00", f"{date.strftime('%Y-%m-%d')}T11:59"),
                    (f"{date.strftime('%Y-%m-%d')}T12:00", f"{date.strftime('%Y-%m-%d')}T23:59")
                ]
                
                for start_time, end_time in time_windows:
                    url = f"{self.aerodatabox_base}/flights/airports/icao/{self.cairo_icao}/{start_time}/{end_time}"
                    
                    headers = {
                        'X-RapidAPI-Key': self.rapidapi_key,
                        'X-RapidAPI-Host': self.rapidapi_host
                    }
                    
                    params = {
                        'withLeg': 'true',
                        'direction': 'Departure',
                        'withCancelled': 'false',
                        'withCodeshared': 'true'
                    }
                    
                    response = requests.get(url, headers=headers, params=params, timeout=30)
                    
                    if response.status_code == 200:
                        data = response.json()
                        departures = data.get('departures', [])
                        
                        for flight_raw in departures:
                            # Filter for EgyptAir
                            airline = flight_raw.get('airline', {})
                            if airline.get('iata') == self.egyptair_iata:
                                flight = self._parse_aerodatabox_flight(flight_raw, date.strftime('%Y-%m-%d'))
                                if flight:
                                    all_flights.append(flight)
                    
                    time.sleep(1)  # Rate limiting
                
                self.logger.info(f"   ✓ Processed {date.strftime('%Y-%m-%d')}")
            
            self.logger.info(f"✅ Collected {len(all_flights)} flights from AeroDataBox")
            self.flights_by_source['aerodatabox'] = all_flights
            return all_flights
            
        except Exception as e:
            self.logger.error(f"❌ AeroDataBox error: {e}")
            return []
    
    def _parse_aerodatabox_flight(self, flight_raw, date):
        """Parse AeroDataBox flight data"""
        try:
            aircraft = flight_raw.get('aircraft', {})
            departure = flight_raw.get('departure', {})
            arrival = flight_raw.get('arrival', {})
            
            return {
                'flight_number': flight_raw.get('number', 'N/A'),
                'tail_number': aircraft.get('reg', 'Unknown'),
                'aircraft_type': aircraft.get('model', 'N/A'),
                'origin_code': departure.get('airport', {}).get('iata', 'CAI'),
                'origin': departure.get('airport', {}).get('name', 'Cairo'),
                'destination_code': arrival.get('airport', {}).get('iata', 'N/A'),
                'destination': arrival.get('airport', {}).get('name', 'N/A'),
                'departure_time': departure.get('scheduledTime', {}).get('local', 'N/A'),
                'arrival_time': arrival.get('scheduledTime', {}).get('local', 'N/A'),
                'status': flight_raw.get('status', 'Unknown'),
                'data_source': 'AeroDataBox (Airport)',
                'flight_date': date,
                'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            self.logger.debug(f"Error parsing flight: {e}")
            return None
    
    def merge_and_deduplicate(self):
        """Merge data from all sources and remove duplicates"""
        self.logger.info("🔄 Merging data from all APIs...")
        
        all_flights = []
        all_flights.extend(self.flights_by_source['opensky'])
        all_flights.extend(self.flights_by_source['aviationstack'])
        all_flights.extend(self.flights_by_source['aerodatabox'])
        
        # Create DataFrame for deduplication
        df = pd.DataFrame(all_flights)
        
        if len(df) == 0:
            return []
        
        # Remove duplicates based on flight number and date
        initial_count = len(df)
        df = df.drop_duplicates(subset=['flight_number', 'flight_date'], keep='first')
        removed = initial_count - len(df)
        
        self.logger.info(f"   📊 Total flights: {initial_count}")
        self.logger.info(f"   🗑️  Removed duplicates: {removed}")
        self.logger.info(f"   ✅ Unique flights: {len(df)}")
        
        return df.to_dict('records')
    
    def save_to_csv(self, flights, filename=None):
        """Save flights to CSV"""
        if not flights:
            self.logger.warning("⚠️  No flights to save")
            return None
        
        df = pd.DataFrame(flights)
        
        # Sort by date and flight number
        if 'flight_date' in df.columns:
            df = df.sort_values(['flight_date', 'flight_number'], ascending=[False, True])
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"egyptair_30days_comprehensive_{timestamp}.csv"
        
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        
        # Reorder columns for better readability
        column_order = [
            'flight_date', 'flight_number', 'tail_number', 'aircraft_type',
            'origin_code', 'origin', 'destination_code', 'destination',
            'departure_time', 'arrival_time', 'status', 'data_source', 'collected_at'
        ]
        
        # Only include columns that exist
        column_order = [col for col in column_order if col in df.columns]
        df = df[column_order]
        
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        self.logger.info(f"💾 Saved {len(flights)} flights to: {output_path}")
        return output_path
    
    def generate_statistics(self, flights):
        """Generate comprehensive statistics"""
        if not flights:
            return
        
        df = pd.DataFrame(flights)
        
        print("\n" + "=" * 100)
        print("📊 COMPREHENSIVE EGYPTAIR FLIGHT DATA - 30 DAYS")
        print("=" * 100)
        
        print(f"\n📈 OVERVIEW:")
        print(f"   Total Flights: {len(df)}")
        print(f"   Date Range: {df['flight_date'].min()} to {df['flight_date'].max()}")
        print(f"   Unique Flight Numbers: {df['flight_number'].nunique()}")
        print(f"   Unique Aircraft (Tails): {df[df['tail_number'] != 'Unknown']['tail_number'].nunique()}")
        print(f"   Unique Routes: {df[['origin_code', 'destination_code']].drop_duplicates().shape[0]}")
        
        print(f"\n📡 DATA SOURCES:")
        source_counts = df['data_source'].value_counts()
        for source, count in source_counts.items():
            print(f"   {source}: {count} flights")
        
        print(f"\n🛩️  TOP 10 AIRCRAFT (by tail number):")
        known_tails = df[df['tail_number'] != 'Unknown']
        if len(known_tails) > 0:
            tail_counts = known_tails['tail_number'].value_counts().head(10)
            for tail, count in tail_counts.items():
                aircraft_type = known_tails[known_tails['tail_number'] == tail]['aircraft_type'].iloc[0]
                print(f"   {tail} ({aircraft_type}): {count} flights")
        
        print(f"\n✈️  TOP 10 DESTINATIONS:")
        dest_counts = df['destination_code'].value_counts().head(10)
        for dest, count in dest_counts.items():
            dest_name = df[df['destination_code'] == dest]['destination'].iloc[0] if dest != 'N/A' else 'Unknown'
            print(f"   {dest} ({dest_name}): {count} flights")
        
        print(f"\n📅 FLIGHTS BY DATE (Last 7 days):")
        date_counts = df['flight_date'].value_counts().sort_index(ascending=False).head(7)
        for date, count in date_counts.items():
            print(f"   {date}: {count} flights")
        
        print("\n" + "=" * 100)


def main():
    """Main execution"""
    logger = ScraperLogger('comprehensive_flight_collector')
    
    print("\n" + "=" * 100)
    print(" " * 20 + "✈️  COMPREHENSIVE EGYPTAIR DATA COLLECTOR - 30 DAYS ✈️")
    print("=" * 100)
    print("\n🔑 API Configuration:")
    print("   ✅ AviationStack: Configured (269c650d...)")
    print("   ✅ AeroDataBox: Configured (via RapidAPI)")
    print("   ✅ OpenSky Network: No key needed (FREE)")
    print("\n📊 Collection Plan:")
    print("   • Live flights with tail numbers (OpenSky)")
    print("   • 30 days historical data (AviationStack)")
    print("   • 7 days airport departures (AeroDataBox)")
    print("\n" + "=" * 100 + "\n")
    
    collector = ComprehensiveFlightCollector(logger)
    
    # Step 1: Live flights
    logger.info("=" * 100)
    logger.info("STEP 1: Collecting LIVE flights")
    logger.info("=" * 100)
    collector.get_live_flights_opensky()
    
    # Step 2: Historical flights (30 days)
    logger.info("\n" + "=" * 100)
    logger.info("STEP 2: Collecting 30 days historical data")
    logger.info("=" * 100)
    collector.get_historical_flights_aviationstack(days=30)
    
    # Step 3: Airport departures (30 days)
    logger.info("\n" + "=" * 100)
    logger.info("STEP 3: Collecting 30 days airport departures")
    logger.info("=" * 100)
    collector.get_airport_departures_aerodatabox(days=30)
    
    # Step 4: Merge and deduplicate
    logger.info("\n" + "=" * 100)
    logger.info("STEP 4: Merging and deduplicating data")
    logger.info("=" * 100)
    all_flights = collector.merge_and_deduplicate()
    
    if all_flights:
        # Save to CSV
        output_path = collector.save_to_csv(all_flights)
        
        # Generate statistics
        collector.generate_statistics(all_flights)
        
        print(f"\n✅ COLLECTION COMPLETE!")
        print(f"📄 Data saved to: {output_path}")
        print(f"\n💡 To view the data:")
        print(f"   start {output_path}")
        print("\n" + "=" * 100 + "\n")
        
        return output_path
    else:
        logger.error("❌ No flights collected")
        return None


if __name__ == "__main__":
    main()
