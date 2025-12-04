"""
Auto-start EgyptAir Flight Scraper (Monthly sampling for quick demo)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.egyptair_scraper import EgyptAirFlightScraper
from src.logger import ScraperLogger
from datetime import datetime


def main():
    print("="*100)
    print(" "*25 + "🌍 EGYPTAIR SCRAPER - QUICK DEMO MODE 🌍")
    print("="*100)
    print()
    print("📋 Configuration:")
    print("   • Sampling: Monthly (12 dates per route)")
    print("   • Bidirectional: NO (Egypt→World only)")
    print("   • Estimated time: 30-60 minutes")
    print("   • This is a DEMO - for full scrape use run_egyptair_scraper.py")
    print()
    print("="*100)
    print(f"🚀 STARTING SCRAPER at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100 + "\n")
    
    # Initialize logger and scraper
    logger = ScraperLogger('egyptair_demo')
    scraper = EgyptAirFlightScraper(logger)
    
    start_time = datetime.now()
    
    try:
        # Run quick demo scraper (monthly sampling, no bidirectional)
        flights = scraper.scrape_all_routes_year(
            days_interval=30,  # Monthly sampling
            check_both_directions=False  # One-way only for speed
        )
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n" + "="*100)
        print("✅ SCRAPING COMPLETED!")
        print("="*100)
        
        if flights:
            # Save final results
            filepath = scraper.save_to_csv()
            
            # Get statistics
            stats = scraper.get_statistics()
            
            print(f"\n📊 STATISTICS:")
            print(f"   {'='*90}")
            print(f"   ⏱️  Duration: {duration.total_seconds()/60:.1f} minutes")
            print(f"   ✈️  Total Flights: {stats['total_flights']:,}")
            print(f"   🛫 Unique Routes: {stats['unique_routes']:,}")
            print(f"   🔢 Flight Numbers: {stats['unique_flight_numbers']}")
            print(f"   📅 Date Range: {stats['date_range']}")
            print(f"   🌍 Origins: {len(stats['origins'])} cities")
            print(f"   🌍 Destinations: {len(stats['destinations'])} cities")
            print(f"   {'='*90}")
            
            print(f"\n💾 Data saved to: {filepath}")
            
            print("\n" + "="*100)
            print("🎉 SUCCESS! Flight data has been collected.")
            print("="*100)
            print("\n📝 For comprehensive worldwide scrape, run:")
            print("   python scripts\\run_egyptair_scraper.py")
            print("   (Choose Weekly + Bidirectional for full coverage)")
        else:
            print("\n⚠️  WARNING: No flights were found.")
            print("   Check logs for details")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  SCRAPING INTERRUPTED")
        if scraper.all_flights:
            filepath = scraper.save_to_csv(f"egyptair_partial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            print(f"💾 Partial data saved: {filepath}")
    
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        if scraper.all_flights:
            filepath = scraper.save_to_csv(f"egyptair_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            print(f"💾 Data saved: {filepath}")
    
    print("\n" + "="*100)
    print("DONE!")
    print("="*100)


if __name__ == "__main__":
    main()
