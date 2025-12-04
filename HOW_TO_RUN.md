# Running the Professional Intelligent Web Scraper

## Quick Start

### Method 1: Run the Streamlit App (Recommended)

```bash
# Navigate to project directory
cd F:\Scrapper

# Activate virtual environment
.venv\Scripts\activate

# Run the new professional app
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## What's New

### Enhanced Features

1. **Professional UI** - No emojis, clean enterprise design
2. **Advanced HTML Analysis** - 10+ analysis scenarios including:
   - E-commerce detection
   - Blog/news identification
   - Social media pattern recognition
   - Table/form analysis
   - AJAX/SPA detection
   - Pagination strategies
   - Structured data extraction

3. **Professional Logging System**
   - Rotating file handlers
   - Separate error logs
   - Performance metrics
   - Structured logging with metadata

4. **Intelligent Analyzer V2**
   - 10 website type patterns
   - Advanced DOM depth analysis
   - Semantic HTML5 detection
   - Media element analysis
   - JSON-LD and Open Graph extraction
   - Complexity scoring

---

## File Structure

```
F:\Scrapper\
├── streamlit_app.py                    # NEW: Professional Streamlit UI
├── scripts/
│   ├── intelligent_analyzer.py         # UPDATED: Removed emojis
│   ├── intelligent_analyzer_v2.py      # NEW: Advanced analyzer
│   ├── professional_logger.py          # NEW: Enterprise logging
│   ├── scraper_generator.py            # Existing
│   ├── data_analyzer.py                # Existing
│   └── pdf_generator.py                # Existing
└── logs/                                # NEW: Log files directory
```

---

## Features Comparison

### Old App (app.py)
- Basic Selenium scraping
- Limited analysis
- Generic patterns
- Simple logging

### New App (streamlit_app.py)
- Intelligent workflow automation
- 10+ analysis scenarios
- Advanced pattern detection
- Professional logging system
- Clean professional UI
- Real-time progress tracking
- Comprehensive reports

---

## Usage Examples

### 1. Analyze a Website

1. Open `streamlit_app.py` in browser
2. Enter URL: `http://quotes.toscrape.com`
3. Configure options in sidebar
4. Click "Start Workflow"
5. Download results (CSV, PDF, Analysis JSON)

### 2. Advanced Configuration

**Sidebar Options:**
- Auto-execute scraper: YES/NO
- Perform data analysis: YES/NO
- Generate PDF report: YES/NO
- Request delay: 0.5-5.0 seconds
- Scraper timeout: 30-600 seconds
- Max pages: 1-100

### 3. View Logs

Logs are saved in `logs/` directory:
- `intelligent_scraper_YYYYMMDD.log` - All logs
- `intelligent_scraper_errors_YYYYMMDD.log` - Errors only

---

## Supported Website Types

The analyzer can detect and optimize for:

1. **E-commerce** - Products, prices, reviews
2. **Blogs** - Articles, authors, comments
3. **News** - Headlines, stories, breaking news
4. **Social Media** - Posts, profiles, interactions
5. **Directories** - Listings, catalogs
6. **Forums** - Threads, replies, discussions
7. **Documentation** - API docs, guides
8. **Job Boards** - Positions, companies
9. **Real Estate** - Properties, listings
10. **Events** - Calendars, schedules

---

## Output Files

For each workflow execution, you get:

1. **analysis.json** - Complete HTML structure analysis
2. **scraper.py** - Generated scraper code
3. **scraped_data.csv** - Extracted data
4. **data_analysis.json** - Statistical analysis
5. **charts/** - Data visualizations (PNG)
6. **report.pdf** - Professional PDF report
7. **workflow.json** - Execution summary

---

## Logging Levels

```
DEBUG   - Detailed diagnostic information
INFO    - General informational messages  
WARNING - Warning messages
ERROR   - Error messages with context
CRITICAL - Critical failures
```

View logs in real-time in the app's "Execution Logs" section.

---

## Performance Metrics

The system tracks:
- Page load time (ms)
- Total elements analyzed
- Patterns detected
- Data extraction speed
- Report generation time

---

## Troubleshooting

### App won't start
```bash
# Check Streamlit installation
pip install streamlit

# Run with verbose output
streamlit run streamlit_app.py --logger.level=debug
```

### Import errors
```bash
# Ensure all dependencies installed
pip install -r requirements.txt
```

### No data extracted
- Check website's robots.txt
- Try increasing timeout
- Enable JavaScript rendering (if SPA detected)
- Check execution logs for details

---

## Keyboard Shortcuts

- `Ctrl+R` - Rerun app
- `Ctrl+C` - Stop app (in terminal)

---

## Next Steps

1. Test with sample URLs (provided in sidebar)
2. Review generated analysis.json
3. Customize scraper_generator.py for specific needs
4. Export data to your preferred format

---

##Happy Scraping! 

**Support:** Check logs/ directory for detailed execution logs
