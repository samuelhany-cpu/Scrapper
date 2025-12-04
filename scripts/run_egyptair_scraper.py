"""
EgyptAir Comprehensive Worldwide Flight Scraper Runner Script

This script runs the EgyptAir flight schedule scraper to collect
COMPREHENSIVE flight data for ALL routes worldwide over a full year period.

Features:
- 🌍 Covers 100+ worldwide destinations across all continents
- 🇪🇬 All Egyptian cities as origins (Cairo, Alexandria, Sharm El-Sheikh, etc.)
- 🔄 Bidirectional routes (Egypt → World AND World → Egypt)
- 🤖 Human-like behavior with Firefox stealth mode
- 📅 Full year coverage with customizable date intervals
- 💾 Auto-saves progress every 20 routes
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.egyptair_scraper import EgyptAirFlightScraper
from src.logger import ScraperLogger
from datetime import datetime


def main():
    print("="*100)
    print(" "*25 + "🌍 EGYPTAIR COMPREHENSIVE WORLDWIDE FLIGHT SCRAPER 🌍")
    print("="*100)
    print()
    print("📋 This will scrape EgyptAir flight schedules for ALL routes worldwide over a full year.")
    print()
    print("🎯 Coverage:")
    print("   • 100+ worldwide destinations (all continents)")
    print("   • Egypt, Middle East, Europe, Africa, Asia, Americas, Oceania")
    print("   • ALL Egyptian cities as origins (Cairo, Alexandria, etc.)")
    print("   • Bidirectional routes (outbound AND inbound)")
    print()
    print("🤖 Anti-Detection Features:")
    print("   • Firefox browser with stealth mode")
    print("   • Human-like typing and mouse movements")
    print("   • Random delays (3-60 seconds)")
    print("   • Periodic breaks to simulate real user")
    print()
    print("💾 Data Collection:")
    print("   • Flight numbers, times, duration, stops, aircraft")
    print("   • Auto-saves progress every 20 routes")
    print("   • Exports to CSV with UTF-8 encoding")
    print()
    print("⏱️  ESTIMATED TIME:")
    
    # Get user preference
    print("\n📅 Select date interval:")
    print("   1. Daily (365 days) - COMPREHENSIVE but SLOW (est. 50-100 hours)")
    print("   2. Every 3 days (122 days) - Detailed (est. 15-30 hours)")
    print("   3. Weekly (52 weeks) - Balanced (est. 4-8 hours) [RECOMMENDED]")
    print("   4. Every 2 weeks (26 samples) - Quick (est. 2-4 hours)")
    print("   5. Monthly (12 samples) - Fast (est. 1-2 hours)")
    
    choice = input("\nChoose interval (1-5, default=3): ").strip()
    
    interval_map = {
        '1': (1, 'Daily'),
        '2': (3, 'Every 3 days'),
        '3': (7, 'Weekly'),
        '4': (14, 'Every 2 weeks'),
        '5': (30, 'Monthly')
    }
    
    days_interval, interval_name = interval_map.get(choice, (7, 'Weekly'))
    
    print(f"\n✅ Selected: {interval_name} sampling ({365//days_interval} dates)")
    
    # Ask about bidirectional
    print("\n🔄 Check both directions?")
    print("   YES: Egypt→World AND World→Egypt (recommended, 2x routes)")
    print("   NO: Only Egypt→World (faster)")
    
    bidirectional = input("\nCheck both directions? (yes/no, default=yes): ").strip().lower()
    check_both = bidirectional not in ['no', 'n']
    
    print(f"✅ Bidirectional: {'YES' if check_both else 'NO'}")
    
    print("\n" + "="*100)
    print("⚠️  WARNING: This is a comprehensive scrape!")
    print("   • Will take several hours to complete")
    print("   • Progress is auto-saved every 20 routes")
    print("   • You can stop anytime with Ctrl+C")
    print("   • Make sure you have Firefox installed")
    print("="*100)
    
    response = input("\n🚀 Ready to start? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Scraping cancelled.")
        return
    
    print("\n" + "="*100)
    print(f"🚀 STARTING SCRAPER at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100 + "\n")
    
    # Initialize logger and scraper
    logger = ScraperLogger('egyptair_worldwide')
    scraper = EgyptAirFlightScraper(logger)
    
    start_time = datetime.now()
    
    try:
        # Run the comprehensive worldwide scraper
        flights = scraper.scrape_all_routes_year(
            days_interval=days_interval,
            check_both_directions=check_both
        )
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n" + "="*100)
        print("✅ SCRAPING COMPLETED SUCCESSFULLY!")
        print("="*100)
        
        if flights:
            # Save final results
            filepath = scraper.save_to_csv()
            
            # Get comprehensive statistics
            stats = scraper.get_statistics()
            
            print(f"\n📊 COMPREHENSIVE STATISTICS:")
            print(f"   {'='*90}")
            print(f"   ⏱️  Duration: {duration.total_seconds()/3600:.2f} hours ({duration.total_seconds()/60:.1f} minutes)")
            print(f"   ✈️  Total Flights Found: {stats['total_flights']:,}")
            print(f"   🛫 Unique Routes: {stats['unique_routes']:,}")
            print(f"   🔢 Unique Flight Numbers: {stats['unique_flight_numbers']}")
            print(f"   📅 Date Range: {stats['date_range']}")
            print(f"   🌍 Origin Airports: {len(stats['origins'])} cities")
            print(f"   🌍 Destination Airports: {len(stats['destinations'])} cities")
            print(f"   {'='*90}")
            
            print(f"\n📍 Origins ({len(stats['origins'])}):")
            print(f"   {', '.join(stats['origins'][:20])}...")
            
            print(f"\n📍 Destinations ({len(stats['destinations'])}):")
            print(f"   {', '.join(stats['destinations'][:20])}...")
            
            print(f"\n💾 Final data saved to:")
            print(f"   📄 {filepath}")
            
            print("\n" + "="*100)
            print("🎉 SUCCESS! All EgyptAir flight data has been collected.")
            print("="*100)
        else:
            print("\n⚠️  WARNING: No flights were found.")
            print("   • Check if EgyptAir website is accessible")
            print("   • Check logs for detailed error messages")
            print("   • Try running again with different date range")
    
    except KeyboardInterrupt:
        print("\n\n" + "="*100)
        print("⚠️  SCRAPING INTERRUPTED BY USER (Ctrl+C)")
        print("="*100)
        
        if scraper.all_flights:
            print(f"\n💾 Saving {len(scraper.all_flights)} flights collected so far...")
            filepath = scraper.save_to_csv(f"egyptair_partial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            print(f"✅ Partial data saved to: {filepath}")
        else:
            print("\n❌ No data to save.")
    
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        print("Check logs for details.")
        
        if scraper.all_flights:
            print(f"\n💾 Saving {len(scraper.all_flights)} flights collected before error...")
            filepath = scraper.save_to_csv(f"egyptair_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            print(f"✅ Data saved to: {filepath}")
    
    finally:
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
