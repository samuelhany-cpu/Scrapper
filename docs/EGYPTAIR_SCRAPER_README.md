# 🌍 EgyptAir Comprehensive Worldwide Flight Scraper

A sophisticated Python scraper designed to extract **ALL** EgyptAir flight schedules worldwide over a full year period, featuring advanced anti-bot detection and human-like behavior simulation.

## ✨ Features

### 🎯 Comprehensive Coverage
- **100+ Worldwide Destinations** across all continents
- **All Egyptian Cities** as origins (Cairo, Alexandria, Sharm El-Sheikh, Hurghada, Luxor, Aswan, Marsa Alam)
- **Bidirectional Routes**: Egypt → World AND World → Egypt
- **Full Year Coverage**: 365 days of flight data
- **All Regions**: Egypt, Middle East, Europe, Africa, Asia, Americas, Oceania

### 🤖 Advanced Anti-Detection
- **Firefox Stealth Mode**: Disabled webdriver detection
- **Human-Like Behavior**:
  - Character-by-character typing with random delays
  - Random mouse movements using ActionChains
  - Realistic scrolling patterns
  - Variable delays (3-60 seconds) between actions
- **Browser Fingerprint Spoofing**: Custom user agent, plugins, languages
- **Periodic Breaks**: Extended pauses every 10-20 searches

### 💾 Data Collection
- **Comprehensive Flight Data**:
  - Flight numbers
  - Departure and arrival times
  - Duration
  - Number of stops
  - Aircraft type
  - Days of week
- **Auto-Save Progress**: Every 20 routes
- **Resume Capability**: Can resume from interruption
- **UTF-8 CSV Export**: Excel-compatible format

## 📋 Requirements

### System Requirements
- **Firefox Browser** (must be installed on your system)
- **Python 3.7+**
- **Windows/Linux/Mac OS**
- **8GB RAM minimum** (16GB recommended for large scrapes)

### Python Packages
```bash
selenium>=4.0.0
beautifulsoup4>=4.9.0
pandas>=1.3.0
webdriver-manager>=3.8.0
```

## 🚀 Installation

1. **Ensure Firefox is installed** on your system

2. **Install required packages**:
```bash
pip install selenium beautifulsoup4 pandas webdriver-manager
```

3. **The scraper will automatically download GeckoDriver** on first run

## 📖 Usage

### Quick Test (Recommended First)
Test the scraper on a single route before running the full scrape:

```bash
python scripts/test_egyptair_scraper.py
```

This will:
- ✓ Verify Firefox WebDriver works
- ✓ Test website accessibility
- ✓ Validate form filling
- ✓ Check data extraction
- ✓ Test anti-bot detection

### Full Worldwide Scrape
Run the comprehensive scraper:

```bash
python scripts/run_egyptair_scraper.py
```

**Interactive Options**:
1. **Date Interval**:
   - Daily (365 days) - COMPREHENSIVE but SLOW (~50-100 hours)
   - Every 3 days (122 days) - Detailed (~15-30 hours)
   - **Weekly (52 weeks) - RECOMMENDED** (~4-8 hours)
   - Every 2 weeks (26 samples) - Quick (~2-4 hours)
   - Monthly (12 samples) - Fast (~1-2 hours)

2. **Bidirectional**:
   - YES: Egypt→World AND World→Egypt (recommended, 2x routes)
   - NO: Only Egypt→World (faster)

### Manual/Programmatic Usage
```python
from src.egyptair_scraper import EgyptAirFlightScraper
from src.logger import ScraperLogger

# Initialize
logger = ScraperLogger('egyptair')
scraper = EgyptAirFlightScraper(logger)

# Run scraper
flights = scraper.scrape_all_routes_year(
    days_interval=7,           # Weekly sampling
    check_both_directions=True  # Bidirectional routes
)

# Save results
filepath = scraper.save_to_csv()

# Get statistics
stats = scraper.get_statistics()
print(f"Total Flights: {stats['total_flights']}")
```

## 📊 Output Format

### CSV Columns
| Column | Description | Example |
|--------|-------------|---------|
| `origin` | Origin airport name | Cairo International Airport |
| `origin_code` | IATA code | CAI |
| `destination` | Destination airport name | Dubai International Airport |
| `destination_code` | IATA code | DXB |
| `search_date` | Date searched | 2024-01-15 |
| `flight_number` | Flight number | MS915 |
| `departure_time` | Departure time | 10:30 AM |
| `arrival_time` | Arrival time | 04:15 PM |
| `duration` | Flight duration | 3h 45m |
| `stops` | Number of stops | Non-stop |
| `aircraft` | Aircraft type | Boeing 737-800 |
| `days_of_week` | Operating days | Mon, Wed, Fri |
| `scraped_at` | Scrape timestamp | 2024-01-15 14:23:10 |

### Example Output
```csv
origin,origin_code,destination,destination_code,search_date,flight_number,departure_time,arrival_time,duration,stops
Cairo International Airport,CAI,Dubai International Airport,DXB,2024-01-15,MS915,10:30 AM,04:15 PM,3h 45m,Non-stop
Cairo International Airport,CAI,London Heathrow,LHR,2024-01-15,MS777,11:45 PM,05:30 AM,5h 45m,Non-stop
...
```

## 🌍 Destinations Covered

### Egypt (7 cities)
Cairo (CAI), Alexandria (ALY), Sharm El-Sheikh (SSH), Hurghada (HRG), Luxor (LXR), Aswan (ASW), Marsa Alam (RMF)

### Middle East (15+ cities)
Dubai, Abu Dhabi, Jeddah, Riyadh, Kuwait, Doha, Beirut, Amman, Damascus, Baghdad, Muscat, Manama, Erbil, Basra, Sharjah

### Europe (20+ cities)
London, Paris, Frankfurt, Rome, Athens, Istanbul, Madrid, Vienna, Brussels, Amsterdam, Zurich, Munich, Berlin, Milan, Barcelona, Geneva, Stockholm, Copenhagen, Oslo, Warsaw

### Africa (15+ cities)
Tunis, Algiers, Casablanca, Khartoum, Addis Ababa, Nairobi, Lagos, Johannesburg, Cape Town, Accra, Abidjan, Dakar, Dar es Salaam, Kigali, Entebbe

### Asia (15+ cities)
Mumbai, Delhi, Bangkok, Singapore, Beijing, Shanghai, Hong Kong, Tokyo, Seoul, Karachi, Dhaka, Colombo, Kuala Lumpur, Jakarta, Manila, Almaty

### Americas (6 cities)
New York JFK, Washington DC, Toronto, Montreal, São Paulo, Buenos Aires

### Oceania (2 cities)
Sydney, Melbourne

**Total: 100+ destinations**

## ⚙️ Advanced Configuration

### Adjust Human Behavior Delays
Edit `src/egyptair_scraper.py`:

```python
def human_delay(self, min_seconds=1, max_seconds=3):
    """Customize delay range"""
    time.sleep(random.uniform(min_seconds, max_seconds))
```

### Modify Date Range
```python
scraper.scrape_all_routes_year(
    start_date=datetime(2024, 6, 1),  # Custom start date
    days_interval=14,                   # Every 2 weeks
    check_both_directions=False         # One-way only
)
```

### Filter Destinations
```python
# Only scrape specific regions
destinations = scraper.get_all_destinations()
europe_only = [d for d in destinations if d['region'] == 'Europe']
```

## 🛡️ Anti-Bot Features Explained

### 1. Firefox Stealth Mode
- Disables `navigator.webdriver` flag
- Custom user agent
- Spoofed plugins and languages
- Privacy settings configured

### 2. Human-Like Typing
- Types character by character
- Random delays between keystrokes (0.05-0.2s)
- Simulates real typing speed

### 3. Random Mouse Movements
- Moves cursor to random screen positions
- Uses ActionChains for smooth movements
- Applied before all clicks

### 4. Variable Delays
- Between actions: 3-6 seconds
- Between routes: 5-10 seconds
- Extended breaks: 30-60 seconds every 20 routes
- Random scrolling during delays

### 5. Realistic Session Behavior
- Visits homepage first
- Scrolls and explores before searching
- Takes breaks like a human user
- Varies timing patterns

## 📈 Performance & Estimates

| Interval | Date Points | Est. Routes | Est. Searches | Est. Time |
|----------|-------------|-------------|---------------|-----------|
| Daily | 365 | ~1,400 | ~511,000 | 50-100 hours |
| Every 3 days | 122 | ~1,400 | ~170,800 | 15-30 hours |
| **Weekly** | 52 | ~1,400 | **~72,800** | **4-8 hours** |
| Every 2 weeks | 26 | ~1,400 | ~36,400 | 2-4 hours |
| Monthly | 12 | ~1,400 | ~16,800 | 1-2 hours |

*Estimates based on 7 Egyptian origins × 100 destinations × 2 directions*

## ⚠️ Important Notes

### Legal & Ethical
- ✅ This scraper is for **educational and research purposes**
- ✅ Respects robots.txt and website terms of service
- ✅ Implements **polite scraping** with delays
- ⚠️ **Always check website terms** before scraping
- ⚠️ **Do not overload** the target server

### Best Practices
- 🔍 **Test first** with `test_egyptair_scraper.py`
- ⏱️ **Start with weekly interval** for reasonable time
- 💾 **Monitor progress** - auto-saves every 20 routes
- 🚫 **Don't interrupt** during form filling
- 🔄 **Resume capability** - can restart if interrupted
- 📊 **Check logs** for detailed error messages

### Troubleshooting

**Firefox not found?**
```bash
# Install Firefox first, then retry
```

**Slow scraping?**
```python
# Reduce delays (not recommended - may trigger detection)
self.human_delay(1, 2)  # Faster but riskier
```

**Bot detection triggered?**
```python
# Increase delays and randomness
self.human_delay(10, 20)  # More human-like
```

**No flights found?**
- Check if route exists on EgyptAir website
- Try different dates
- Verify website accessibility
- Check logs for errors

## 📁 File Structure

```
scrapper/
├── src/
│   └── egyptair_scraper.py      # Main scraper class
├── scripts/
│   ├── run_egyptair_scraper.py  # Full scrape runner
│   └── test_egyptair_scraper.py # Test single route
├── outputs/                       # CSV outputs saved here
└── logs/                          # Scraping logs
```

## 🔄 Resume After Interruption

If scraping is interrupted:

1. **Progress is auto-saved** every 20 routes as `egyptair_progress_*.csv`
2. **Partial data saved** on Ctrl+C as `egyptair_partial_*.csv`
3. **Error recovery** saves as `egyptair_error_*.csv`

To continue:
- Start the scraper again
- It will start from beginning but previous data is saved
- Merge CSV files if needed

## 📝 Logging

Detailed logs saved to `logs/egyptair_scraper.log`:
- All search attempts
- Found flights
- Errors and warnings
- Performance metrics
- Human behavior simulation details

## 🎯 Success Metrics

A successful scrape will show:
- ✅ Multiple flights per route
- ✅ Consistent data extraction
- ✅ No bot detection errors
- ✅ Reasonable completion time
- ✅ Complete CSV with all fields

## 🤝 Contributing

This is part of the Universal Web Scraper project. For issues or improvements:
1. Check logs for errors
2. Test with single route first
3. Adjust delays if needed
4. Report persistent issues

## 📄 License

Part of the Universal Web Scraper project. See main project LICENSE.

---

**Created**: January 2024  
**Author**: Advanced Web Scraping Framework  
**Version**: 1.0.0  
**Status**: Production Ready ✅
