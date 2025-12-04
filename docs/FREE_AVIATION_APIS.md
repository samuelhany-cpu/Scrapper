# Free Aviation APIs for Flight Data & Tail Numbers

## 🆓 COMPLETELY FREE APIs (No Credit Card Required)

### 1. **AviationStack** ⭐ RECOMMENDED
- **Website**: https://aviationstack.com/
- **Free Tier**: 500 requests/month (No credit card)
- **Features**:
  - Real-time flight status
  - Flight schedules
  - Route information
  - Airline data
  - Airport information
- **Limitations**: No tail numbers in free tier
- **Best For**: Flight schedules and route data

**Registration Steps**:
1. Go to https://aviationstack.com/
2. Click "Sign Up Free"
3. Enter email and password
4. Verify email
5. Get API key from dashboard

---

### 2. **OpenSky Network** ⭐ BEST FOR TAIL NUMBERS (100% FREE)
- **Website**: https://opensky-network.org/
- **Free Tier**: UNLIMITED (Community project)
- **Features**:
  - ✅ **Real-time aircraft positions**
  - ✅ **ICAO24 addresses (aircraft identifiers)**
  - ✅ **Flight tracking**
  - ✅ **Historical data**
  - ✅ **Aircraft registration lookup**
  - ✅ **Completely FREE - No API key needed!**
- **Best For**: Real-time tracking and aircraft identification
- **API Docs**: https://openskynetwork.github.io/opensky-api/

**No Registration Required!** - Just use the API directly

---

### 3. **ADSB Exchange** ⭐ FREE ALTERNATIVE
- **Website**: https://www.adsbexchange.com/
- **Free Tier**: RapidAPI Free tier (limited calls)
- **Features**:
  - Real-time aircraft tracking
  - Tail numbers
  - Flight positions
  - Military aircraft tracking
- **API**: Via RapidAPI (you already have RapidAPI key!)

---

### 4. **FlightAware AeroAPI** (Limited Free)
- **Website**: https://www.flightaware.com/commercial/aeroapi/
- **Free Tier**: Limited free tier for personal use
- **Features**:
  - ✅ Flight tracking
  - ✅ Tail numbers
  - ✅ Flight history
  - ✅ Aircraft details
- **Limitations**: Approval required, limited calls

---

### 5. **Aviation Edge** (Trial)
- **Website**: https://aviation-edge.com/
- **Free Trial**: 30 days (requires credit card)
- **Features**:
  - Flight schedules
  - Airline routes
  - Aircraft data
  - Airport information
- **Note**: Not truly free (trial only)

---

### 6. **Cirium (formerly FlightStats)** (Trial)
- **Website**: https://www.cirium.com/
- **Free Trial**: Limited trial
- **Features**: Premium data
- **Note**: Requires business contact

---

## 🎯 RECOMMENDED SETUP (100% FREE)

### **Best Combination for EgyptAir Scraper:**

1. **OpenSky Network** (FREE, Unlimited)
   - Get aircraft positions and ICAO24 codes
   - Track flights in real-time
   - **No API key needed!**
   
2. **AviationStack** (FREE, 500/month)
   - Get flight schedules
   - Route information
   - Airline data

3. **AeroDataBox** (Already have via RapidAPI)
   - Flight departures/arrivals
   - Some tail numbers
   - Airport schedules

---

## 📋 API Comparison Table

| API | Free Tier | Tail Numbers | Registration | Credit Card | Best For |
|-----|-----------|--------------|--------------|-------------|----------|
| **OpenSky Network** | ✅ Unlimited | ✅ Yes | ❌ No | ❌ No | Real-time tracking |
| **AviationStack** | ✅ 500/month | ⚠️ Limited | ✅ Yes | ❌ No | Schedules |
| **AeroDataBox** | ✅ RapidAPI | ⚠️ Some | ✅ Yes | ❌ No | Airport data |
| **ADSB Exchange** | ⚠️ Limited | ✅ Yes | ✅ Yes | ❌ No | Military tracking |
| **FlightAware** | ⚠️ Limited | ✅ Yes | ✅ Yes | ⚠️ Maybe | Professional use |

---

## 🚀 QUICK START GUIDE

### Option 1: OpenSky Network (Recommended - No signup!)

```python
import requests

# No API key needed!
url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()

# Get EgyptAir flights (callsign starts with MSR)
egyptair_flights = [
    flight for flight in data['states'] 
    if flight[1] and flight[1].startswith('MSR')
]
```

### Option 2: AviationStack (500 free requests/month)

```python
import requests

api_key = "YOUR_AVIATIONSTACK_KEY"
url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&airline_iata=MS"
response = requests.get(url)
flights = response.json()
```

---

## 🔗 Registration Links

1. **AviationStack**: https://aviationstack.com/signup/free
2. **OpenSky Network**: https://opensky-network.org/ (No signup needed for API!)
3. **ADSB Exchange**: https://rapidapi.com/adsbx/api/adsbexchange-com1/
4. **FlightAware**: https://www.flightaware.com/commercial/aeroapi/portal.rvt

---

## 💡 NEXT STEPS

### To Collect Real EgyptAir Data with Tail Numbers:

1. **Get AviationStack key** (2 minutes):
   - Go to https://aviationstack.com/
   - Sign up free (no credit card)
   - Copy API key

2. **Use OpenSky Network** (No signup!):
   - Already integrated in code
   - Just run the script

3. **Run Enhanced Collector**:
   ```bash
   python scripts/collect_egyptair_multi_api.py
   ```

This will give you:
- ✅ Flight schedules (AviationStack)
- ✅ Real-time tracking (OpenSky)
- ✅ Tail numbers (OpenSky + AeroDataBox)
- ✅ Airport data (AeroDataBox)
- ✅ Complete coverage of EgyptAir fleet

---

## 📞 Support

If you need help getting API keys or have questions:
- Check API documentation
- Most APIs have free community support
- OpenSky Network has active forum

---

**Last Updated**: November 30, 2025
**Best Free Options**: OpenSky Network (unlimited) + AviationStack (500/month)
