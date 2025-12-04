# 🎯 EgyptAir Scraper Architecture & Workflow

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  scripts/run_egyptair_scraper.py                                 │
│  ├─ Interactive configuration (date interval, bidirectional)     │
│  ├─ Progress display & statistics                                │
│  └─ Error handling & recovery                                    │
│                                                                   │
│  scripts/test_egyptair_scraper.py                                │
│  └─ Single route test (Cairo → Dubai)                            │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│                    CORE SCRAPER ENGINE                           │
├─────────────────────────────────────────────────────────────────┤
│  src/egyptair_scraper.py                                         │
│  ├─ EgyptAirFlightScraper (Main Class)                           │
│  │   ├─ setup_driver()          → Firefox + Stealth Mode         │
│  │   ├─ get_all_destinations()  → 100+ Worldwide Airports        │
│  │   ├─ search_flights()        → Human-like Form Filling        │
│  │   ├─ extract_flight_results()→ BeautifulSoup Data Extraction  │
│  │   ├─ scrape_all_routes_year()→ Main Loop (All Routes/Dates)   │
│  │   ├─ save_to_csv()           → UTF-8 CSV Export               │
│  │   └─ get_statistics()        → Comprehensive Stats            │
│  │                                                                │
│  └─ Helper Methods                                               │
│      ├─ human_delay()           → Random delays (0.05-60s)       │
│      ├─ human_typing()          → Char-by-char typing            │
│      ├─ random_mouse_movement() → ActionChains movements         │
│      └─ random_scroll()         → Realistic scrolling            │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│                    SELENIUM LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  Firefox WebDriver (GeckoDriver)                                 │
│  ├─ Stealth Mode: navigator.webdriver = false                    │
│  ├─ Custom User Agent                                            │
│  ├─ Browser Fingerprint Spoofing                                 │
│  ├─ Privacy Settings                                             │
│  └─ ActionChains for mouse movements                             │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│                    TARGET WEBSITE                                │
├─────────────────────────────────────────────────────────────────┤
│  https://www.egyptair.com/en/Plan/Pages/timetable.aspx          │
│  └─ Flight timetable search form                                 │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPUT LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│  outputs/egyptair_flights_YYYYMMDD_HHMMSS.csv                    │
│  ├─ Flight numbers, times, duration, stops, aircraft             │
│  ├─ Origin/destination with codes                                │
│  ├─ Country and region metadata                                  │
│  └─ Scraped timestamp                                            │
│                                                                   │
│  logs/egyptair_scraper.log                                       │
│  └─ Detailed scraping logs with errors and progress              │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Scraping Workflow

```
START
  │
  ├─ Initialize Logger
  │
  ├─ Setup Firefox WebDriver
  │   ├─ Install GeckoDriver
  │   ├─ Configure stealth mode
  │   ├─ Set user agent
  │   └─ Inject anti-detection JS
  │
  ├─ Visit Homepage (Human Behavior)
  │   ├─ Wait 3-5 seconds
  │   ├─ Random scroll
  │   └─ Random mouse movement
  │
  ├─ Load Destinations (100+)
  │   ├─ Egypt: 7 cities
  │   ├─ Middle East: 15+ cities
  │   ├─ Europe: 20+ cities
  │   ├─ Africa: 15+ cities
  │   ├─ Asia: 15+ cities
  │   ├─ Americas: 6 cities
  │   └─ Oceania: 2 cities
  │
  ├─ Generate Date Range
  │   ├─ Start: Today
  │   ├─ End: Today + 365 days
  │   └─ Interval: User choice (1-30 days)
  │
  ├─ FOR EACH Egyptian Origin (7)
  │   │
  │   ├─ FOR EACH Destination (100+)
  │   │   │
  │   │   ├─ Skip if same city
  │   │   │
  │   │   ├─ FOR EACH Date (52-365)
  │   │   │   │
  │   │   │   ├─ Navigate to timetable page
  │   │   │   │
  │   │   │   ├─ Fill Form with Human Behavior:
  │   │   │   │   ├─ Select one-way
  │   │   │   │   │   └─ Move mouse → Click → Delay
  │   │   │   │   │
  │   │   │   │   ├─ Enter origin
  │   │   │   │   │   └─ Move mouse → Click → Type char-by-char → Delay
  │   │   │   │   │
  │   │   │   │   ├─ Enter destination
  │   │   │   │   │   └─ Move mouse → Click → Type char-by-char → Delay
  │   │   │   │   │
  │   │   │   │   ├─ Enter date
  │   │   │   │   │   └─ Move mouse → Click → Type char-by-char → Delay
  │   │   │   │   │
  │   │   │   │   └─ Click search
  │   │   │   │       └─ Move mouse → Click → Wait 5-8 seconds
  │   │   │   │
  │   │   │   ├─ Extract Flight Results:
  │   │   │   │   ├─ Parse HTML with BeautifulSoup
  │   │   │   │   ├─ Find flight containers
  │   │   │   │   └─ Extract: number, times, duration, stops, aircraft
  │   │   │   │
  │   │   │   ├─ Save flights to list
  │   │   │   │
  │   │   │   ├─ Human delay (3-6 seconds)
  │   │   │   │
  │   │   │   └─ IF (date_count % 10 == 0)
  │   │   │       └─ Extended break (10-20 seconds)
  │   │   │
  │   │   └─ Route delay (5-10 seconds)
  │   │
  │   ├─ IF bidirectional enabled:
  │   │   │
  │   │   └─ FOR EACH International Destination
  │   │       └─ Repeat above (Destination → Origin)
  │   │
  │   └─ IF (route_count % 20 == 0)
  │       ├─ Log milestone
  │       ├─ Extended break (30-60 seconds)
  │       └─ Auto-save progress CSV
  │
  ├─ Close browser
  │
  ├─ Save final CSV
  │   └─ outputs/egyptair_flights_TIMESTAMP.csv
  │
  ├─ Generate statistics
  │   ├─ Total flights
  │   ├─ Unique routes
  │   ├─ Unique flight numbers
  │   ├─ Date range
  │   ├─ Origins count
  │   └─ Destinations count
  │
  └─ Display results
      ├─ Success message
      ├─ Statistics summary
      └─ File path
      
END
```

## 🤖 Human Behavior Simulation Flow

```
SEARCH FORM FILLING (Human-Like)
  │
  ├─ Step 1: Select One-Way
  │   ├─ Random delay (0.5-1.5s)
  │   ├─ Move mouse to element
  │   ├─ Delay (0.3-0.7s)
  │   ├─ Click element
  │   └─ Delay (0.5-1s)
  │
  ├─ Step 2: Enter Origin
  │   ├─ Random delay (0.5-1.5s)
  │   ├─ Move mouse to input field
  │   ├─ Delay (0.3-0.7s)
  │   ├─ Click input
  │   ├─ Delay (0.2-0.5s)
  │   ├─ Clear existing text
  │   ├─ FOR EACH character in "CAI":
  │   │   ├─ Type character
  │   │   └─ Delay (0.05-0.2s)
  │   └─ Delay (0.5-1s)
  │
  ├─ Step 3: Random Mouse Movement
  │   ├─ Generate random x, y coordinates
  │   ├─ Move cursor to position
  │   └─ Delay (0.2-0.5s)
  │
  ├─ Step 4: Enter Destination
  │   ├─ (Same as Step 2)
  │   └─ Type "DXB" char-by-char
  │
  ├─ Step 5: Random Scroll
  │   ├─ Generate random scroll amount
  │   ├─ Scroll page
  │   └─ Delay (0.5-1s)
  │
  ├─ Step 6: Enter Date
  │   ├─ (Same as Step 2)
  │   └─ Type "15/01/2024" char-by-char
  │
  ├─ Step 7: Final Mouse Movement
  │   └─ Random position before clicking search
  │
  └─ Step 8: Click Search
      ├─ Delay (1-2s)
      ├─ Move mouse to button
      ├─ Delay (0.5-1s)
      ├─ Click button
      └─ Wait for results (5-8s)
```

## 📊 Data Flow

```
USER INPUT
   ↓
[Date Interval Choice]
   ↓
[Bidirectional Enable/Disable]
   ↓
SCRAPER CONFIGURATION
   ↓
[Load 100+ Destinations]
   ↓
[Generate Date Range]
   ↓
ROUTE GENERATION
   ↓
┌─────────────────────┐
│ Egyptian Origins    │ ────┐
│ • Cairo (CAI)       │     │
│ • Alexandria (ALY)  │     │
│ • Sharm (SSH)       │     ├─→ [COMBINATIONS]
│ • Hurghada (HRG)    │     │       ↓
│ • Luxor (LXR)       │     │   ~1,400 Routes
│ • Aswan (ASW)       │     │       ↓
│ • Marsa Alam (RMF)  │     │   × 52 Dates
│ (7 cities)          │     │       ↓
└─────────────────────┘     │   ~72,800 Searches
                            │       ↓
┌─────────────────────┐     │   WEBSITE QUERIES
│ Global Destinations │ ────┘       ↓
│ • 100+ cities       │         [RESPONSES]
│ • All continents    │             ↓
└─────────────────────┘         [PARSING]
                                    ↓
                            [DATA EXTRACTION]
                                    ↓
                           ┌────────────────┐
                           │ Flight Records │
                           │ • Number       │
                           │ • Times        │
                           │ • Duration     │
                           │ • Stops        │
                           │ • Aircraft     │
                           └────────────────┘
                                    ↓
                            [ACCUMULATION]
                                    ↓
                          ┌──────────────────┐
                          │ Progress Saves   │
                          │ Every 20 routes  │
                          └──────────────────┘
                                    ↓
                            [FINAL EXPORT]
                                    ↓
                        ┌──────────────────────┐
                        │ CSV FILE             │
                        │ ~10,000-50,000 rows  │
                        │ UTF-8, Excel-ready   │
                        └──────────────────────┘
```

## 🔒 Anti-Detection Layers

```
Layer 1: BROWSER FINGERPRINT
├─ User Agent: Mozilla/5.0 ...
├─ Languages: en-US, en
├─ Plugins: Spoofed
└─ Timezone: System default

Layer 2: WEBDRIVER DETECTION
├─ navigator.webdriver = false
├─ Automated flags removed
└─ Browser automation hidden

Layer 3: TIMING PATTERNS
├─ Variable delays (not fixed)
├─ Random ranges (3-6s, 5-10s, 30-60s)
└─ Human-like inconsistency

Layer 4: MOUSE BEHAVIOR
├─ Random movements
├─ Smooth ActionChains
└─ Pre-click positioning

Layer 5: TYPING PATTERNS
├─ Character-by-character
├─ Random keystroke delays
└─ Natural typing speed

Layer 6: SESSION BEHAVIOR
├─ Homepage visit first
├─ Scrolling and exploring
├─ Periodic breaks
└─ Extended pauses

Layer 7: ERROR HANDLING
├─ Graceful failures
├─ Retry logic
└─ No rapid requests
```

## 📈 Performance Optimization

```
OPTIMIZATION STRATEGIES:

1. Smart Date Sampling
   ├─ User chooses granularity
   ├─ Daily → Weekly → Monthly
   └─ Trade completeness for speed

2. Progressive Saving
   ├─ Save every 20 routes
   ├─ No data loss on crash
   └─ Resume capability

3. Efficient Parsing
   ├─ BeautifulSoup (fast)
   ├─ Selective element search
   └─ Minimal DOM traversal

4. Memory Management
   ├─ Append-only list
   ├─ Periodic CSV dumps
   └─ Log rotation

5. Network Efficiency
   ├─ Single browser session
   ├─ No redundant requests
   └─ Smart navigation
```

## 🎯 Success Metrics

```
QUALITY INDICATORS:

✅ High Success Rate
   └─ >90% of searches return data

✅ No Bot Detection
   └─ Zero CAPTCHAs or blocks

✅ Consistent Timing
   └─ Predictable completion time

✅ Data Completeness
   └─ All fields populated

✅ No Crashes
   └─ Runs to completion

✅ Progress Tracking
   └─ Real-time feedback

✅ Clean Output
   └─ Valid CSV format
```

---

**This architecture ensures robust, human-like, large-scale scraping!** 🚀
