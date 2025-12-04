"""
Automated Test Script for EgyptAir Scraper (No user input required)
Tests a single route to verify the scraper works
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.egyptair_scraper import EgyptAirFlightScraper
from src.logger import ScraperLogger
from datetime import datetime


def main():
    print("="*80)
    print(" "*20 + "🧪 EGYPTAIR SCRAPER AUTO-TEST")
    print("="*80)
    print()
    print("Testing Cairo (CAI) → Dubai (DXB) route")
    print("="*80)
    
    # Initialize logger and scraper
    logger = ScraperLogger('egyptair_test')
    scraper = EgyptAirFlightScraper(logger)
    
    try:
        print("\n🚀 Starting test scrape...")
        print("-"*80)
        
        # Setup driver
        print("⏳ Initializing Firefox WebDriver...")
        scraper.setup_driver()
        print("✅ Firefox WebDriver initialized successfully")
        
        # Get destinations
        print("\n⏳ Loading destinations...")
        destinations = scraper.get_all_destinations()
        print(f"✅ Loaded {len(destinations)} destinations")
        
        # Find Cairo and Dubai
        cairo = next((d for d in destinations if d['code'] == 'CAI'), None)
        dubai = next((d for d in destinations if d['code'] == 'DXB'), None)
        
        if not cairo or not dubai:
            print("❌ Could not find Cairo or Dubai in destinations")
            return
        
        # Test search
        today = datetime.now()
        print(f"\n🔍 Testing search: {cairo['name']} → {dubai['name']}")
        print(f"📅 Date: {today.strftime('%Y-%m-%d')}")
        print("⏳ This may take 30-60 seconds with human-like delays...")
        print("-"*80)
        
        flights = scraper.search_flights(cairo, dubai, today)
        
        print("\n" + "="*80)
        print("📊 TEST RESULTS")
        print("="*80)
        
        if flights:
            print(f"✅ SUCCESS! Found {len(flights)} flight(s)\n")
            
            for i, flight in enumerate(flights[:3], 1):
                print(f"Flight {i}:")
                print(f"  • Flight Number: {flight.get('flight_number', 'N/A')}")
                print(f"  • Departure: {flight.get('departure_time', 'N/A')}")
                print(f"  • Arrival: {flight.get('arrival_time', 'N/A')}")
                print(f"  • Duration: {flight.get('duration', 'N/A')}")
                print(f"  • Stops: {flight.get('stops', 'N/A')}")
                print()
            
            if len(flights) > 3:
                print(f"... and {len(flights) - 3} more flight(s)\n")
            
            # Save test results
            scraper.all_flights = flights
            filepath = scraper.save_to_csv(f"egyptair_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            print(f"💾 Test data saved to: {filepath}\n")
            
            print("="*80)
            print("🎉 TEST PASSED!")
            print("="*80)
            print("\n✅ The scraper is working correctly!")
            print("📝 Next step: Run the full scrape")
            print("   python scripts\\run_egyptair_scraper.py")
        else:
            print("⚠️  No flights found\n")
            print("Possible reasons:")
            print("  • No flights on this route today")
            print("  • Website structure changed")
            print("  • Bot detection triggered")
            print("\n💡 Suggestions:")
            print("  • Try running again")
            print("  • Check EgyptAir website accessibility")
            print("  • Review logs for detailed errors")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    
    except Exception as e:
        print(f"\n\n❌ TEST FAILED")
        print(f"Error: {e}")
        print("\nCheck logs for details:")
        if hasattr(scraper, 'logger'):
            print(f"  {scraper.logger.log_file}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
    
    finally:
        if hasattr(scraper, 'driver') and scraper.driver:
            scraper.driver.quit()
            print("\n🔒 Browser closed")
        
        print("\n" + "="*80)


if __name__ == "__main__":
    main()
