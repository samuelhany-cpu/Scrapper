# Professional Web Scraper Workflow

## 🎯 Overview

An intelligent, automated web scraping system that learns website structure, generates custom scrapers, extracts data, performs analysis, and produces professional PDF reports.

## 🚀 Quick Start

```bash
# Run the complete workflow
python scripts/auto_scraper_workflow.py <url>

# Example
python scripts/auto_scraper_workflow.py https://example.com
```

## 📋 Workflow Steps

The system automatically executes **5 steps**:

### 1. **HTML Structure Analysis**
- Fetches the target webpage
- Analyzes HTML structure, tags, classes, and patterns
- Identifies main content areas
- Detects repeating structures (lists, cards, articles)
- Generates scraping strategy
- **Output**: `*_analysis.json`

### 2. **Custom Scraper Generation**
- Reads the analysis results
- Auto-generates a Python scraper script
- Includes proper selectors based on learned patterns
- Adds error handling and rate limiting
- **Output**: `*_scraper.py`

### 3. **Data Extraction**
- Executes the generated scraper
- Extracts structured data from the website
- Saves results to CSV and JSON
- **Output**: `scraped_*.csv`, `scraped_*.json`

### 4. **Data Analysis**
- Loads extracted data
- Performs statistical analysis
- Generates insights
- Creates visualizations (charts and graphs)
- **Output**: `*_data_analysis.json`, `charts/*.png`

### 5. **PDF Report Generation**
- Compiles all analysis results
- Creates professional PDF report with:
  - Executive summary
  - Column-by-column analysis
  - Key insights
  - Data visualizations
- **Output**: `*_report.pdf`

## 📁 Project Structure

```
F:/Scrapper/
├── scripts/
│   ├── auto_scraper_workflow.py      # Main orchestrator
│   ├── intelligent_analyzer.py       # Step 1: HTML analyzer
│   ├── scraper_generator.py          # Step 2: Code generator
│   ├── data_analyzer.py              # Step 4: Data analysis
│   └── pdf_generator.py              # Step 5: PDF creation
├── outputs/
│   ├── *_analysis.json               # Structure analysis
│   ├── *_scraper.py                  # Generated scraper
│   ├── scraped_*.csv                 # Extracted data
│   ├── *_data_analysis.json          # Data insights
│   ├── *_report.pdf                  # Final report
│   ├── *_workflow.json               # Execution log
│   └── charts/                       # Visualizations
│       ├── data_completeness.png
│       ├── distribution_*.png
│       └── histogram_*.png
└── .venv/                            # Python environment
```

## 🛠️ Requirements

```bash
# Install dependencies
pip install requests beautifulsoup4 lxml pandas matplotlib seaborn reportlab
```

**Required packages:**
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast XML/HTML parser
- `pandas` - Data manipulation
- `matplotlib` - Plotting
- `seaborn` - Statistical visualizations
- `reportlab` - PDF generation

## 📖 Usage Examples

### Basic Usage
```bash
python scripts/auto_scraper_workflow.py http://quotes.toscrape.com
```

### With Custom Output Directory
```bash
python scripts/auto_scraper_workflow.py https://example.com F:/CustomOutput
```

### Running Individual Steps

#### Step 1: Analyze HTML Only
```bash
python scripts/intelligent_analyzer.py <url> <output.json>
```

#### Step 2: Generate Scraper from Analysis
```bash
python scripts/scraper_generator.py <analysis.json> <scraper.py>
```

#### Step 3: Run Custom Scraper
```bash
python outputs/your_scraper.py
```

#### Step 4: Analyze Data
```bash
python scripts/data_analyzer.py <data.csv> <analysis.json>
```

#### Step 5: Generate PDF Report
```bash
python scripts/pdf_generator.py <analysis.json> <report.pdf>
```

## 🎨 Features

### Intelligent HTML Analysis
- ✅ Detects main content containers
- ✅ Identifies repeating patterns (lists, cards)
- ✅ Analyzes class names and structure
- ✅ Detects pagination links
- ✅ Finds data attributes
- ✅ Analyzes internal/external links

### Dynamic Scraper Generation
- ✅ Auto-generates Python code
- ✅ Selector-based extraction
- ✅ Multiple fallback strategies
- ✅ Rate limiting (respectful scraping)
- ✅ Error handling
- ✅ CSV and JSON output

### Data Analysis
- ✅ Basic statistics (mean, median, std)
- ✅ Missing data detection
- ✅ Column type analysis
- ✅ Distribution analysis
- ✅ Insight generation
- ✅ Automated visualizations

### PDF Reports
- ✅ Professional formatting
- ✅ Cover page with metadata
- ✅ Executive summary
- ✅ Column-by-column breakdown
- ✅ Key insights section
- ✅ Embedded charts
- ✅ Auto-opens when complete

## 📊 Example Output

### Workflow Execution
```
====================================================================================================
🤖 INTELLIGENT WEB SCRAPER WORKFLOW
====================================================================================================

🌐 Target URL: http://quotes.toscrape.com
📁 Output Directory: F:\Scrapper\outputs

STEP 1: ANALYZING HTML STRUCTURE ✅
STEP 2: GENERATING CUSTOM SCRAPER ✅
STEP 3: RUNNING SCRAPER TO EXTRACT DATA ✅
  → Extracted 14 items
STEP 4: ANALYZING SCRAPED DATA ✅
  → Generated 9 insights
  → Created 5 visualizations
STEP 5: GENERATING PDF REPORT ✅
  → Report: quotes_toscrape_com_20251204_230556_report.pdf

====================================================================================================
✅ WORKFLOW COMPLETE
====================================================================================================

📁 Files Generated (11):
   📄 quotes_toscrape_com_20251204_230556_analysis.json (1.3 KB)
   📄 quotes_toscrape_com_20251204_230556_scraper.py (5.5 KB)
   📄 scraped_quotes_toscrape_com_20251204_230601.csv (6.9 KB)
   📄 quotes_toscrape_com_20251204_230556_data_analysis.json (4.6 KB)
   📄 data_completeness.png (33.9 KB)
   📄 distribution_content.png (57.0 KB)
   📄 distribution_classes.png (27.1 KB)
   📄 distribution_title.png (23.1 KB)
   📄 distribution_link.png (61.7 KB)
   📄 quotes_toscrape_com_20251204_230556_report.pdf (302.1 KB)
   📄 quotes_toscrape_com_20251204_230556_workflow.json (2.8 KB)
```

## 🔧 Configuration

### Customizing the Analyzer
Edit `scripts/intelligent_analyzer.py`:
- Change user agent
- Modify timeout values
- Adjust content detection heuristics

### Customizing the Scraper Generator
Edit `scripts/scraper_generator.py`:
- Add custom extraction methods
- Modify selector strategies
- Change output formats

### Customizing Visualizations
Edit `scripts/data_analyzer.py`:
- Add custom chart types
- Modify color schemes
- Adjust chart dimensions

### Customizing PDF Reports
Edit `scripts/pdf_generator.py`:
- Change page layout
- Modify fonts and colors
- Add custom sections

## 🚨 Best Practices

1. **Respect robots.txt**: Check if scraping is allowed
2. **Rate limiting**: The scraper includes 1-second delays
3. **User agent**: Identifies as a legitimate browser
4. **Error handling**: Gracefully handles failures
5. **Data validation**: Checks for missing/invalid data

## 🐛 Troubleshooting

### Issue: No data extracted
- Check if the website requires authentication
- Verify the URL is accessible
- Check if the site uses JavaScript rendering (requires Selenium)

### Issue: Unicode/Encoding errors
- Ensure output files use UTF-8 encoding
- Check Windows console encoding settings

### Issue: PDF generation fails
- Verify reportlab is installed
- Check that chart files exist
- Ensure write permissions in output directory

### Issue: Timeout errors
- Increase timeout in analyzer/scraper
- Check network connection
- Verify target site is accessible

## 📝 Workflow JSON Structure

```json
{
  "url": "http://example.com",
  "started_at": "2025-12-04 23:05:56",
  "steps": [
    {
      "name": "html_analysis",
      "status": "success",
      "timestamp": "2025-12-04 23:05:58"
    },
    ...
  ],
  "files_generated": [...]
}
```

## 🎯 Use Cases

- **Market Research**: Scrape competitor data
- **Price Monitoring**: Track product prices
- **Content Aggregation**: Collect articles/news
- **Data Collection**: Research datasets
- **SEO Analysis**: Analyze website structure
- **Lead Generation**: Collect contact information

## 📄 License

This project is part of the Scrapper repository.

## 🤝 Contributing

Feel free to enhance the workflow:
- Add new analysis features
- Improve pattern detection
- Create custom visualization types
- Enhance PDF report layouts

## 📞 Support

For issues or questions, check the generated `*_workflow.json` file for detailed execution logs.

---

**Note**: Always comply with website Terms of Service and robots.txt when scraping.
