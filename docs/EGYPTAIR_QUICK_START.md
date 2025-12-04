# 🚀 EgyptAir Scraper - Quick Start Guide

## ⚡ 5-Minute Setup

### Prerequisites Check
✅ Python 3.7+ installed  
✅ Firefox browser installed  
✅ Internet connection active

### Step 1: Install Dependencies (30 seconds)
```bash
cd F:\Scrapper
pip install selenium beautifulsoup4 pandas webdriver-manager
```

**Already done!** ✅ All packages installed

### Step 2: Test Single Route (2 minutes)
```bash
python scripts\test_egyptair_scraper.py
```

**What happens:**
- Opens Firefox browser
- Tests Cairo → Dubai route
- Extracts flight data
- Saves test results
- Shows if scraper works

**Expected output:**
```
🧪 EGYPTAIR SCRAPER TEST
✅ Firefox WebDriver initialized
✅ Loaded 100+ destinations
🔍 Testing: Cairo → Dubai
✅ Found 3 flights
🎉 TEST PASSED!
```

### Step 3: Run Full Scrape (Choose your option)

#### Option A: Quick Sample (1-2 hours)
```bash
python scripts\run_egyptair_scraper.py
# Choose option 5 (Monthly)
# Choose NO for bidirectional
```

#### Option B: Balanced (4-8 hours) ⭐ RECOMMENDED
```bash
python scripts\run_egyptair_scraper.py
# Choose option 3 (Weekly)
# Choose YES for bidirectional
```

#### Option C: Comprehensive (50-100 hours)
```bash
python scripts\run_egyptair_scraper.py
# Choose option 1 (Daily)
# Choose YES for bidirectional
```

---

## 📋 Interactive Menu Walkthrough

When you run `python scripts\run_egyptair_scraper.py`:

### Screen 1: Welcome
```
🌍 EGYPTAIR COMPREHENSIVE WORLDWIDE FLIGHT SCRAPER 🌍
========================================
📋 This will scrape EgyptAir flight schedules for ALL routes worldwide

🎯 Coverage: 100+ destinations across all continents
🤖 Anti-Detection: Firefox stealth mode, human-like behavior
💾 Data: Flight numbers, times, duration, stops, aircraft
```

### Screen 2: Date Interval Selection
```
📅 Select date interval:
   1. Daily (365 days) - COMPREHENSIVE but SLOW (est. 50-100 hours)
   2. Every 3 days (122 days) - Detailed (est. 15-30 hours)
   3. Weekly (52 weeks) - Balanced (est. 4-8 hours) [RECOMMENDED]
   4. Every 2 weeks (26 samples) - Quick (est. 2-4 hours)
   5. Monthly (12 samples) - Fast (est. 1-2 hours)

Choose interval (1-5, default=3): [Enter 3]
```

**Recommendation:** Start with **3 (Weekly)** for your first run

### Screen 3: Bidirectional Option
```
🔄 Check both directions?
   YES: Egypt→World AND World→Egypt (recommended, 2x routes)
   NO: Only Egypt→World (faster)

Check both directions? (yes/no, default=yes): [Enter yes]
```

**Recommendation:** Choose **YES** for complete data

### Screen 4: Confirmation
```
⚠️  WARNING: This is a comprehensive scrape!
   • Will take several hours to complete
   • Progress is auto-saved every 20 routes
   • You can stop anytime with Ctrl+C
   • Make sure you have Firefox installed

🚀 Ready to start? (yes/no): [Enter yes]
```

### Screen 5: Scraping Progress
```
🚀 STARTING SCRAPER at 2024-01-15 14:30:00
====================================

🏠 Visiting homepage first (human behavior)...
✅ Loaded 100 worldwide destinations
📅 Generated 52 date points across the year
📊 SCRAPING PLAN:
   • Routes to check: ~1,400
   • Total searches: ~72,800
   • Estimated time: 6.5 hours

🛫 ORIGIN 1/7: Cairo International Airport (CAI)
====================================

📍 Route 1: Cairo → Dubai (UAE)
   ✅ Date 1/52 (2024-01-15): Found 3 flight(s)
   ✅ Date 2/52 (2024-01-22): Found 3 flight(s)
   ...
   📊 Route total: 156 flights

📍 Route 2: Cairo → Abu Dhabi (UAE)
   ...

🎉 Milestone: 20 routes completed, 3,120 flights found
☕ Taking extended break (30-60 seconds)...
💾 Progress saved to: egyptair_progress_20240115_150022.csv

...continues...
```

---

## 🎯 What to Expect

### Timeline (Weekly + Bidirectional)
- **Setup**: 5 minutes
- **Test**: 2 minutes  
- **Full scrape**: 4-8 hours
- **Total**: ~5-8 hours

### Resources Needed
- **RAM**: 2-4 GB
- **Disk Space**: 50-100 MB for CSV
- **Internet**: Continuous connection
- **Firefox**: Auto-opens and closes

### Data Output
**File:** `outputs\egyptair_flights_YYYYMMDD_HHMMSS.csv`

**Size:** 5-20 MB (10,000-50,000 rows)

**Sample:**
```csv
origin,origin_code,destination,destination_code,flight_number,departure_time,arrival_time,duration
Cairo,CAI,Dubai,DXB,MS915,10:30 AM,04:15 PM,3h 45m
Cairo,CAI,London,LHR,MS777,11:45 PM,05:30 AM,5h 45m
Cairo,CAI,Paris,CDG,MS799,02:15 AM,07:00 AM,4h 45m
...
```

---

## ⚠️ Important Tips

### ✅ DO:
- ✅ **Test first** with `test_egyptair_scraper.py`
- ✅ **Start with weekly interval** (option 3)
- ✅ **Let it run overnight** if possible
- ✅ **Check progress saves** in outputs folder
- ✅ **Monitor logs** for errors

### ❌ DON'T:
- ❌ **Don't close Firefox manually** during scraping
- ❌ **Don't interrupt** during form filling
- ❌ **Don't run multiple instances** simultaneously
- ❌ **Don't reduce delays** (may trigger bot detection)
- ❌ **Don't panic** if no flights found on some routes (normal)

---

## 🛑 How to Stop Safely

### Planned Stop
1. Wait for current route to finish
2. Press **Ctrl+C** in terminal
3. Wait for save to complete
4. Data saved as `egyptair_partial_*.csv`

### Emergency Stop
1. Press **Ctrl+C** in terminal
2. Browser will close
3. Data saved automatically
4. Resume by running again (starts from beginning)

---

## 📊 After Scraping

### View Results
```bash
# Open CSV in Excel
start outputs\egyptair_flights_20240115_143022.csv
```

### Check Statistics
Look for this in the output:
```
📊 COMPREHENSIVE STATISTICS:
   ✈️  Total Flights Found: 12,456
   🛫 Unique Routes: 1,234
   📅 Date Range: 2024-01-15 to 2025-01-15
   🌍 Origin Airports: 7 cities
   🌍 Destination Airports: 98 cities
```

### Check Logs
```bash
# View detailed logs
notepad logs\egyptair_worldwide.log
```

---

## 🐛 Troubleshooting

### "Firefox not found"
**Solution:**
1. Install Firefox from [mozilla.org](https://www.mozilla.org/firefox/)
2. Restart computer
3. Run test again

### "No flights found"
**Possible reasons:**
- ✅ Route doesn't operate on that date (normal)
- ❌ Website structure changed
- ❌ Bot detection triggered
- ❌ Internet connection issue

**Try:**
```bash
# Run test script to diagnose
python scripts\test_egyptair_scraper.py
```

### "Scraping too slow"
**Options:**
1. Choose faster interval (option 4 or 5)
2. Disable bidirectional (NO)
3. Edit delays in code (risky - may trigger detection)

### "Browser keeps crashing"
**Solutions:**
- Update Firefox to latest version
- Restart computer
- Check RAM usage (close other apps)
- Try smaller batch (monthly interval)

### "CSV file corrupted"
**Prevention:**
- Use progress saves (`egyptair_progress_*.csv`)
- Check `outputs` folder for backups
- Don't interrupt during save operations

---

## 💡 Pro Tips

### Tip 1: Run Overnight
```bash
# Start before bedtime, check in morning
python scripts\run_egyptair_scraper.py
# Choose weekly + bidirectional
# Let it run 6-8 hours
```

### Tip 2: Multiple Sessions
```bash
# Session 1: Egypt origins only
# Modify code: check_both_directions=False

# Session 2: Add international origins manually
# Merge CSV files later
```

### Tip 3: Monitor Progress
```bash
# While running, check progress files in another window
dir outputs\egyptair_progress_*.csv

# View latest progress
type outputs\egyptair_progress_20240115_150022.csv
```

### Tip 4: Data Analysis
```python
# After scraping, analyze data
import pandas as pd

df = pd.read_csv('outputs/egyptair_flights_20240115.csv')

# Most frequent routes
print(df.groupby(['origin', 'destination']).size().sort_values(ascending=False).head(10))

# Flights by day
df['search_date'] = pd.to_datetime(df['search_date'])
flights_by_day = df.groupby('search_date').size()
```

---

## 🎉 Success Checklist

After your first successful run:

- ✅ Test script passed
- ✅ Full scraper completed without errors
- ✅ CSV file generated
- ✅ Statistics displayed
- ✅ Data looks correct (flight numbers, times, etc.)
- ✅ File opens in Excel properly

**Congratulations! You've collected comprehensive worldwide flight data!** 🎊

---

## 📞 Need Help?

1. **Check logs**: `logs\egyptair_worldwide.log`
2. **Review error messages** in terminal
3. **Try test script first**: `test_egyptair_scraper.py`
4. **Start small**: Monthly interval, no bidirectional
5. **Verify Firefox** is installed and updated

---

## 🚀 Ready? Let's Go!

```bash
# Step 1: Test (2 minutes)
python scripts\test_egyptair_scraper.py

# Step 2: Full scrape (4-8 hours)
python scripts\run_egyptair_scraper.py
# Choose: 3 (Weekly) + YES (Bidirectional)

# Step 3: Enjoy your data!
start outputs\egyptair_flights_*.csv
```

**Happy Scraping!** ✈️🌍
