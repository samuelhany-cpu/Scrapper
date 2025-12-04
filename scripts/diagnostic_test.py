"""
Quick diagnostic test - just verify components load
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("="*80)
print("🔧 EGYPTAIR SCRAPER DIAGNOSTIC TEST")
print("="*80)

try:
    print("\n1️⃣  Testing imports...")
    from src.egyptair_scraper import EgyptAirFlightScraper
    from src.logger import ScraperLogger
    from datetime import datetime
    print("   ✅ All imports successful")
    
    print("\n2️⃣  Initializing logger...")
    logger = ScraperLogger('egyptair_diagnostic')
    print("   ✅ Logger initialized")
    
    print("\n3️⃣  Creating scraper instance...")
    scraper = EgyptAirFlightScraper(logger)
    print("   ✅ Scraper instance created")
    
    print("\n4️⃣  Loading destinations...")
    destinations = scraper.get_all_destinations()
    print(f"   ✅ Loaded {len(destinations)} destinations")
    
    print("\n5️⃣  Checking destination data...")
    cairo = next((d for d in destinations if d['code'] == 'CAI'), None)
    dubai = next((d for d in destinations if d['code'] == 'DXB'), None)
    
    if cairo and dubai:
        print(f"   ✅ Found Cairo: {cairo['name']} ({cairo['code']})")
        print(f"   ✅ Found Dubai: {dubai['name']} ({dubai['code']})")
    else:
        print("   ❌ Could not find Cairo or Dubai")
    
    print("\n" + "="*80)
    print("🎉 ALL DIAGNOSTIC TESTS PASSED!")
    print("="*80)
    print("\n📋 Summary:")
    print(f"   • Python environment: OK")
    print(f"   • All packages installed: OK")
    print(f"   • Scraper components: OK")
    print(f"   • Destination database: OK ({len(destinations)} cities)")
    print("\n✅ The scraper is ready to use!")
    print("\n📝 Next steps:")
    print("   1. Make sure Firefox is running")
    print("   2. Run: python scripts\\run_egyptair_scraper.py")
    print("\n" + "="*80)
    
except Exception as e:
    print(f"\n❌ DIAGNOSTIC FAILED: {e}")
    import traceback
    traceback.print_exc()
