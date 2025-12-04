"""
Quick Test Script for EgyptAir Scraper
Tests a single route to verify the scraper works before running full scrape
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.egyptair_scraper import EgyptAirFlightScraper
from src.logger import ScraperLogger
from datetime import datetime, timedelta


def main():
    print("="*80)
    print(" "*20 + "🧪 EGYPTAIR SCRAPER TEST")
    print("="*80)
    print()
    print("This will test the scraper on a single route:")
    print("  📍 Cairo (CAI) → Dubai (DXB)")
    print("  📅 Today's date")
    print()
    print("This will verify:")
    print("  ✓ Firefox WebDriver works")
    print("  ✓ Website can be accessed")
    print("  ✓ Form filling works")
    print("  ✓ Data extraction works")
    print("  ✓ Anti-bot detection is effective")
    print()
    print("="*80)
    
    input("\nPress Enter to start test...")
    
    # Initialize logger and scraper
    logger = ScraperLogger('egyptair_test')
    scraper = EgyptAirFlightScraper(logger)
    
    try:
        print("\n🚀 Starting test scrape...")
        print("="*80)
        
        # Setup driver
        scraper.setup_driver()
        print("✅ Firefox WebDriver initialized successfully")
        
        # Get destinations
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
        print(f"\n🔍 Testing search: {cairo['name']} → {dubai['name']} on {today.strftime('%Y-%m-%d')}")
        print("⏳ This may take 30-60 seconds with human-like delays...")
        
        flights = scraper.search_flights(cairo, dubai, today)
        
        print("\n" + "="*80)
        print("📊 TEST RESULTS")
        print("="*80)
        
        if flights:
            print(f"✅ SUCCESS! Found {len(flights)} flight(s)")
            print("\n📝 Sample flight data:")
            for i, flight in enumerate(flights[:3], 1):  # Show first 3 flights
                print(f"\n  Flight {i}:")
                print(f"    Flight Number: {flight.get('flight_number', 'N/A')}")
                print(f"    Departure: {flight.get('departure_time', 'N/A')}")
                print(f"    Arrival: {flight.get('arrival_time', 'N/A')}")
                print(f"    Duration: {flight.get('duration', 'N/A')}")
                print(f"    Stops: {flight.get('stops', 'N/A')}")
            
            if len(flights) > 3:
                print(f"\n  ... and {len(flights) - 3} more flight(s)")
            
            # Save test results
            scraper.all_flights = flights
            filepath = scraper.save_to_csv(f"egyptair_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            print(f"\n💾 Test data saved to: {filepath}")
            
            print("\n" + "="*80)
            print("🎉 TEST PASSED!")
            print("="*80)
            print("\nThe scraper is working correctly. You can now run the full scrape:")
            print("  python scripts\\run_egyptair_scraper.py")
        else:
            print("⚠️  No flights found")
            print("\nPossible reasons:")
            print("  • No flights on this route today")
            print("  • Website structure changed")
            print("  • Bot detection triggered")
            print("\n💡 Try:")
            print("  • Running test again (may be temporary issue)")
            print("  • Checking if EgyptAir website is accessible")
            print("  • Checking logs for detailed error messages")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    
    except Exception as e:
        print(f"\n\n❌ TEST FAILED with error: {e}")
        print("\nCheck logs for details:")
        print(f"  {scraper.logger.log_file if hasattr(scraper, 'logger') else 'logs/scraper.log'}")
    
    finally:
        if scraper.driver:
            scraper.driver.quit()
            print("\n🔒 Browser closed")
    
    print("\n" + "="*80)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
