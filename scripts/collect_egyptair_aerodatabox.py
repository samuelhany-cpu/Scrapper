"""
Real EgyptAir Flight Data Collector using AeroDataBox API (RapidAPI)

This script collects REAL flight data from AeroDataBox API via RapidAPI:
- Real-time flight schedules from Cairo Airport
- Aircraft tail numbers (registration)
- Complete flight details
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


class AeroDataBoxCollector:
    """Collect real flight data from AeroDataBox API"""
    
    def __init__(self, logger):
        self.logger = logger
        self.all_flights = []
        
        # RapidAPI Configuration
        self.rapidapi_key = "00a3084153msh026037bafc6de04p1c4846jsn46d830e5e1bb"
        self.rapidapi_host = "aerodatabox.p.rapidapi.com"
        self.base_url = "https://aerodatabox.p.rapidapi.com"
        
        # Cairo Airport ICAO code
        self.cairo_icao = "HECA"
        
    def get_flights_for_date(self, date, direction='Departure'):
        """
        Get all flights from Cairo Airport for a specific date
        API requires time windows ≤ 12 hours, so we'll make 2 requests per day
        
        Args:
            date: datetime object for the date to query
            direction: 'Departure' or 'Arrival'
        """
        all_flights = []
        
        # Split day into two 12-hour windows
        time_windows = [
            (f"{date.strftime('%Y-%m-%d')}T00:00", f"{date.strftime('%Y-%m-%d')}T11:59"),
            (f"{date.strftime('%Y-%m-%d')}T12:00", f"{date.strftime('%Y-%m-%d')}T23:59")
        ]
        
        for start_time, end_time in time_windows:
            url = f"{self.base_url}/flights/airports/icao/{self.cairo_icao}/{start_time}/{end_time}"
            flights = self._fetch_flights(url, direction, start_time, end_time)
            all_flights.extend(flights)
            time.sleep(1)  # Small delay between requests
        
        self.logger.info(f"✅ Found {len(all_flights)} total flights for {date.strftime('%Y-%m-%d')}")
        return all_flights
    
    def _fetch_flights(self, url, direction, start_time, end_time):
        """Internal method to fetch flights from API"""
        
        headers = {
            'X-RapidAPI-Key': self.rapidapi_key,
            'X-RapidAPI-Host': self.rapidapi_host
        }
        
        params = {
            'withLeg': 'true',
            'direction': direction,
            'withCancelled': 'false',
            'withCodeshared': 'true',
            'withCargo': 'false',
            'withPrivate': 'false',
            'withLocation': 'false'
        }
        
        try:
            self.logger.info(f"📡 Fetching {direction.lower()}s {start_time} to {end_time}...")
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                flights = data.get('departures', []) if direction == 'Departure' else data.get('arrivals', [])
                
                self.logger.info(f"   ✓ {len(flights)} flights in this window")
                return flights
            elif response.status_code == 429:
                self.logger.warning("⚠️  Rate limit reached. Waiting 60 seconds...")
                time.sleep(60)
                return self._fetch_flights(url, direction, start_time, end_time)
            else:
                self.logger.error(f"❌ API Error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            self.logger.error(f"❌ Error fetching flights: {e}")
            return []
    
    def parse_flight_data(self, flight_raw, search_date):
        """Parse raw flight data from API into standardized format"""
        try:
            # Basic flight info
            flight_number = flight_raw.get('number', 'N/A')
            airline_info = flight_raw.get('airline', {})
            airline_name = airline_info.get('name', 'N/A')
            airline_iata = airline_info.get('iata', 'N/A')
            
            # Aircraft info
            aircraft_info = flight_raw.get('aircraft', {})
            aircraft_model = aircraft_info.get('model', 'N/A')
            tail_number = aircraft_info.get('reg', 'N/A')  # Registration number
            
            # Departure info
            departure_info = flight_raw.get('departure', {})
            dep_airport = departure_info.get('airport', {})
            dep_iata = dep_airport.get('iata', 'CAI')
            dep_name = dep_airport.get('name', 'Cairo International Airport')
            dep_terminal = departure_info.get('terminal', 'N/A')
            
            dep_time_info = departure_info.get('scheduledTime', {})
            dep_time_local = dep_time_info.get('local', 'N/A')
            
            # Arrival info
            arrival_info = flight_raw.get('arrival', {})
            arr_airport = arrival_info.get('airport', {})
            arr_iata = arr_airport.get('iata', 'N/A')
            arr_name = arr_airport.get('name', 'N/A')
            arr_terminal = arrival_info.get('terminal', 'N/A')
            
            arr_time_info = arrival_info.get('scheduledTime', {})
            arr_time_local = arr_time_info.get('local', 'N/A')
            
            # Status
            status = flight_raw.get('status', 'Unknown')
            
            # Calculate duration if times are available
            duration = 'N/A'
            if dep_time_local != 'N/A' and arr_time_local != 'N/A':
                try:
                    dep_dt = datetime.fromisoformat(dep_time_local.replace('Z', '+00:00'))
                    arr_dt = datetime.fromisoformat(arr_time_local.replace('Z', '+00:00'))
                    duration_minutes = int((arr_dt - dep_dt).total_seconds() / 60)
                    hours = duration_minutes // 60
                    minutes = duration_minutes % 60
                    duration = f"{hours}h {minutes}m"
                except:
                    duration = 'N/A'
            
            # Extract just the time from local datetime
            dep_time = 'N/A'
            arr_time = 'N/A'
            if dep_time_local != 'N/A':
                try:
                    dep_time = datetime.fromisoformat(dep_time_local.replace('Z', '+00:00')).strftime('%H:%M')
                except:
                    dep_time = dep_time_local
            if arr_time_local != 'N/A':
                try:
                    arr_time = datetime.fromisoformat(arr_time_local.replace('Z', '+00:00')).strftime('%H:%M')
                except:
                    arr_time = arr_time_local
            
            return {
                'origin': dep_name,
                'origin_code': dep_iata,
                'destination': arr_name,
                'destination_code': arr_iata,
                'flight_number': flight_number,
                'tail_number': tail_number if tail_number and tail_number != 'N/A' else 'Unknown',
                'aircraft_type': aircraft_model,
                'departure_time': dep_time,
                'departure_terminal': dep_terminal,
                'arrival_time': arr_time,
                'arrival_terminal': arr_terminal,
                'duration': duration,
                'airline': airline_name,
                'airline_code': airline_iata,
                'status': status,
                'search_date': search_date.strftime('%Y-%m-%d'),
                'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error parsing flight: {e}")
            return None
    
    def collect_egyptair_flights(self, start_date, days=7):
        """
        Collect EgyptAir flights from Cairo Airport
        
        Args:
            start_date: Starting date for collection
            days: Number of days to collect (default: 7, max: 30 for free tier)
        """
        self.logger.info("=" * 100)
        self.logger.info("🚀 Starting EgyptAir flight data collection from AeroDataBox API")
        self.logger.info("=" * 100)
        
        all_flights = []
        egyptair_flights = []
        
        for day_offset in range(days):
            current_date = start_date + timedelta(days=day_offset)
            
            # Get departures for this date
            flights = self.get_flights_for_date(current_date, direction='Departure')
            
            if flights:
                for flight_raw in flights:
                    # Parse flight data
                    parsed = self.parse_flight_data(flight_raw, current_date)
                    
                    if parsed:
                        all_flights.append(parsed)
                        
                        # Filter for EgyptAir flights (MS code)
                        if parsed['airline_code'] == 'MS' or 'EgyptAir' in parsed['airline']:
                            egyptair_flights.append(parsed)
                            self.logger.info(f"✈️  {parsed['flight_number']}: {parsed['origin_code']}→{parsed['destination_code']} "
                                           f"| {parsed['aircraft_type']} | Tail: {parsed['tail_number']}")
            
            # Rate limiting: small delay between requests
            if day_offset < days - 1:
                time.sleep(2)  # 2 second delay to avoid rate limits
        
        self.logger.info("=" * 100)
        self.logger.info(f"📊 Collection complete!")
        self.logger.info(f"   Total flights from Cairo: {len(all_flights)}")
        self.logger.info(f"   EgyptAir flights (MS): {len(egyptair_flights)}")
        self.logger.info("=" * 100)
        
        return egyptair_flights if egyptair_flights else all_flights
    
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
            filename = f"egyptair_aerodatabox_flights_{timestamp}.csv"
        
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
        print("📊 FLIGHT DATA ANALYSIS")
        print("=" * 100)
        
        print(f"\n📈 OVERVIEW:")
        print(f"   Total Flights: {len(df)}")
        print(f"   Unique Routes: {df[['origin_code', 'destination_code']].drop_duplicates().shape[0]}")
        print(f"   Unique Flight Numbers: {df['flight_number'].nunique()}")
        print(f"   Unique Aircraft (Tails): {df[df['tail_number'] != 'Unknown']['tail_number'].nunique()}")
        print(f"   Aircraft Types: {df['aircraft_type'].nunique()}")
        print(f"   Airlines: {df['airline'].nunique()}")
        
        # Top destinations
        print(f"\n✈️  TOP 10 DESTINATIONS:")
        dest_counts = df['destination_code'].value_counts().head(10)
        for dest, count in dest_counts.items():
            dest_name = df[df['destination_code'] == dest]['destination'].iloc[0]
            print(f"   {dest} ({dest_name}): {count} flights")
        
        # Aircraft with known tail numbers
        known_tails = df[df['tail_number'] != 'Unknown']
        if len(known_tails) > 0:
            print(f"\n🛩️  AIRCRAFT WITH TAIL NUMBERS ({len(known_tails)} flights):")
            tail_counts = known_tails['tail_number'].value_counts().head(10)
            for tail, count in tail_counts.items():
                aircraft = known_tails[known_tails['tail_number'] == tail]['aircraft_type'].iloc[0]
                print(f"   {tail} ({aircraft}): {count} flights")
        
        # Sample flights with complete data
        print(f"\n📋 SAMPLE FLIGHTS WITH TAIL NUMBERS:")
        sample = df[df['tail_number'] != 'Unknown'].head(10)
        if len(sample) > 0:
            print(sample[['flight_number', 'tail_number', 'aircraft_type', 'origin_code', 
                         'destination_code', 'departure_time', 'status']].to_string(index=False))
        else:
            print("   (No flights with tail numbers found)")
        
        print("\n" + "=" * 100)


def main():
    """Main execution function"""
    # Initialize logger
    logger = ScraperLogger('egyptair_aerodatabox_collector')
    
    print("\n" + "=" * 100)
    print(" " * 35 + "✈️  EGYPTAIR FLIGHT DATA COLLECTOR ✈️")
    print(" " * 38 + "(Using AeroDataBox API)")
    print("=" * 100)
    print("\n📡 Data Source: AeroDataBox API via RapidAPI")
    print("🔑 API Key: Configured")
    print("🛫 Airport: Cairo International (HECA)")
    print("=" * 100 + "\n")
    
    # Initialize collector
    collector = AeroDataBoxCollector(logger)
    
    # Collection parameters
    start_date = datetime.now()
    days_to_collect = 7  # Collect 7 days of flight data
    
    logger.info(f"📅 Collection period: {days_to_collect} days starting from {start_date.strftime('%Y-%m-%d')}")
    
    # Collect flights
    flights = collector.collect_egyptair_flights(start_date, days=days_to_collect)
    
    if flights:
        # Save to CSV
        output_path = collector.save_to_csv(flights)
        
        # Analyze data
        collector.analyze_data(flights)
        
        print("\n✅ COLLECTION COMPLETE!")
        print(f"📄 Data saved to: {output_path}")
        print("\n💡 To open the CSV file, run:")
        print(f"   start {output_path}")
        print("=" * 100 + "\n")
    else:
        logger.error("❌ No flights collected")


if __name__ == "__main__":
    main()
