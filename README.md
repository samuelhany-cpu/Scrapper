# 🕷️ Intelligent Web Scraper# 🌐 Universal Web Scraper



<div align="center">[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Professional automated web scraping toolkit with AI-powered analysis and PDF reporting**

**The world's most intelligent universal web scraper** - automatically detects and scrapes ANY website from ANY niche with **98.4% accuracy**!

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)## 🚀 Key Features



</div>### 🎯 Universal Domain Detection

- **25+ domain patterns** automatically detected

---- **200+ domain keywords** for intelligent classification

- **Zero configuration** - just provide a URL!

## 🌟 Overview- Works on sports, e-commerce, news, jobs, real estate, travel, education, entertainment, finance, technology, and more!



A comprehensive web scraping framework that combines **intelligent HTML analysis**, **dynamic scraper generation**, **statistical data analysis**, and **professional PDF reporting** into a single automated workflow.### 🧠 Intelligent Extraction

- **30+ extraction strategies** for different content types

### ✨ Key Features- Automatic fallback mechanisms for unknown sites

- Supports both static and dynamic content

- 🤖 **Intelligent Analysis**: Automatically learns website structure and patterns- Multi-language support (English, Arabic, and more)

- 🎯 **Dynamic Generation**: Creates custom scrapers for any website

- 📊 **Data Analysis**: Statistical insights with visualizations### 🖥️ Multiple Interfaces

- 📄 **PDF Reports**: Professional reports with charts and summaries- ✅ **CLI Tool** - Quick command-line scraping

- ⚡ **Zero Configuration**: Just provide a URL and get results- ✅ **Streamlit UI** - Beautiful web interface

- 🔄 **Fully Automated**: 5-step workflow with error handling- ✅ **Telegram Bot** - Bilingual bot with AI analysis

- ✅ **Python API** - Use in your own code

---

### 📊 Proven Performance

## 🚀 Quick Start- **127 real-world websites tested**

- **98.4% success rate** (125/127 passed)

### Installation- Perfect 100% accuracy on 23 out of 25 categories

- Production-ready and battle-tested

```bash

# Clone the repository---

git clone https://github.com/samuelhany-cpu/Scrapper.git

cd Scrapper## 📋 Quick Navigation



# Create virtual environment- [Installation](#-installation)

python -m venv .venv- [Quick Start](#-quick-start)

- [Usage Examples](#-usage-examples)

# Activate virtual environment- [Supported Domains](#-supported-domains)

# Windows:- [Documentation](#-documentation)

.venv\Scripts\activate- [Contributing](#-contributing)

# Linux/Mac:

source .venv/bin/activate---



# Install dependencies## 🔧 Installation

pip install -r requirements.txt

```### Prerequisites

- Python 3.8 or higher

### Basic Usage- pip (Python package installer)

- Chrome/Firefox browser (for dynamic content)

```bash

# Run the complete automated workflow### Quick Setup

python scripts/auto_scraper_workflow.py <URL>

**Windows:**

# Example```bash

python scripts/auto_scraper_workflow.py http://quotes.toscrape.comgit clone https://github.com/yourusername/universal-web-scraper.git

```cd universal-web-scraper

setup.bat

**That's it!** The system will automatically:```

1. Analyze the website structure

2. Generate a custom scraper**Linux/Mac:**

3. Extract all data```bash

4. Create visualizationsgit clone https://github.com/yourusername/universal-web-scraper.git

5. Generate a professional PDF reportcd universal-web-scraper

chmod +x setup.sh

---./setup.sh

```

## 📁 Project Structure

### Manual Installation

``````bash

Scrapper/python -m venv .venv

├── scripts/                          # Core scraping tools.venv\Scripts\activate  # Windows

│   ├── auto_scraper_workflow.py     # ⭐ Main orchestrator# or

│   ├── intelligent_analyzer.py       # HTML structure analyzersource .venv/bin/activate  # Linux/Mac

│   ├── scraper_generator.py          # Dynamic scraper generator

│   ├── data_analyzer.py              # Statistical analysispip install -r requirements.txt

│   ├── pdf_generator.py              # PDF report generator```

│   │

│   # EgyptAir Flight Data Tools### Configuration (Optional)

│   ├── collect_egyptair_*.py         # Flight data collectors```bash

│   ├── generate_*day_dataset.py      # Dataset generatorscp .env.example .env

│   ├── enrich_tail_numbers.py        # Data enrichment# Edit .env and add your API keys

│   └── fix_status_column.py          # Data cleaning```

│

├── src/                              # Source modules---

├── docs/                             # Documentation

│   ├── PROFESSIONAL_SCRAPER_WORKFLOW.md## ⚡ Quick Start

│   ├── FREE_AVIATION_APIS.md

│   └── *.md### 1. Test Any Website

│```bash

├── examples/                         # Sample outputspython test_universal_scraper.py --test-url "https://www.example.com"

│   ├── quotes_toscrape_com_*         # Example workflow```

│   ├── charts/                       # Sample visualizations

│   └── *.pdf                         # Example report### 2. Quick Scrape (CLI)

│```bash

├── outputs/                          # Generated files (gitignored)python quick_scrape.py "https://www.yallakora.com/match-center"

├── tests/                            # Unit tests```

├── .env.example                      # Environment template

├── requirements.txt                  # Python dependencies### 3. Run Live Demo

└── README.md                         # This file```bash

```python demo_universal.py

```

---

### 4. Start Web UI

## 🎯 Use Cases```bash

streamlit run app.py

### 1. General Web Scraping```

Extract structured data from any website automatically:

```bash### 5. Start Telegram Bot

python scripts/auto_scraper_workflow.py https://example.com```bash

```python telegram_bot_bilingual.py

```

### 2. Flight Data Collection (EgyptAir Example)

Collect and analyze aviation data:---

```bash

# Collect current flight data## 📖 Usage Examples

python scripts/collect_egyptair_multi_api.py

### Command Line Interface

# Generate historical dataset

python scripts/generate_11year_dataset.py```bash

# Scrape any website

# Enrich with tail numberspython quick_scrape.py "https://www.amazon.com/s?k=laptop"

python scripts/enrich_tail_numbers.py

```# Test specific URL

python test_universal_scraper.py --test-url "https://news.ycombinator.com"

### 3. E-commerce Price Monitoring

Track product prices over time:# Run all 127 tests

```bashpython test_universal_scraper.py

python scripts/auto_scraper_workflow.py https://shop.example.com/products```

```

### Python API

---

```python

## 📊 Workflow Detailsfrom adaptive_scraper import AdaptiveSmartScraper

from logger import setup_logger

### The 5-Step Automated Process

# Initialize

#### Step 1: HTML Structure Analysislogger = setup_logger("my_scraper")

- Fetches and parses the target webpagescraper = AdaptiveSmartScraper(logger)

- Identifies main content containers

- Detects repeating patterns (lists, cards, articles)# Scrape any URL

- Analyzes class names and data attributesscraper.scrape_url("https://www.yallakora.com/match-center")

- Generates scraping strategy

# Get data

**Output**: `*_analysis.json`data = scraper.get_data()



#### Step 2: Custom Scraper Generation# Export

- Creates Python scraper code based on analysisscraper.export_to_csv("output.csv")

- Implements optimal selectors```

- Adds error handling and rate limiting

- Includes CSV and JSON export---



**Output**: `*_scraper.py`## 🌟 Supported Domains



#### Step 3: Data Extraction### Perfect 100% Accuracy

- Executes the generated scraper✅ Sports • E-commerce • Fashion • Jobs • Real Estate  

- Extracts structured data✅ Travel • Education • Entertainment • Food • Finance  

- Saves to multiple formats✅ Technology • Gaming • Weather • and more!



**Output**: `scraped_*.csv`, `scraped_*.json`### Tested Websites (127 total)

Amazon, eBay, Walmart, Yallakora, ESPN, CNN, BBC, LinkedIn, Indeed, Zillow, Booking.com, Coursera, IMDb, Netflix, YouTube, GitHub, StackOverflow, and 110+ more!

#### Step 4: Data Analysis

- Statistical analysis (mean, median, distributions)See [UNIVERSAL_SUCCESS.md](UNIVERSAL_SUCCESS.md) for complete list.

- Data quality checks

- Insight generation---

- Visualization creation

## 📚 Documentation

**Output**: `*_data_analysis.json`, `charts/*.png`

- **[UNIVERSAL_SCRAPER_GUIDE.md](UNIVERSAL_SCRAPER_GUIDE.md)** - Complete user guide

#### Step 5: PDF Report Generation- **[UNIVERSAL_SUCCESS.md](UNIVERSAL_SUCCESS.md)** - Test results (98.4% success!)

- Professional document with:- **[QUICKSTART_UNIVERSAL.md](QUICKSTART_UNIVERSAL.md)** - Quick reference

  - Cover page- **[TELEGRAM_BOT_GUIDE.md](TELEGRAM_BOT_GUIDE.md)** - Telegram bot setup

  - Executive summary- **[BILINGUAL_GUIDE.md](BILINGUAL_GUIDE.md)** - Multi-language support

  - Column-by-column analysis

  - Key insights---

  - Embedded visualizations

## 📁 Project Structure

**Output**: `*_report.pdf` (auto-opens)

```

---universal-web-scraper/

├── Core Components

## 🛠️ Advanced Usage│   ├── adaptive_scraper.py      # Main scraper (30+ strategies)

│   ├── domain_patterns.py       # Universal detection (25+ patterns)

### Individual Steps│   ├── scraper_selenium.py      # Dynamic content

│   └── logger.py                # Logging system

Run specific workflow steps independently:│

├── User Interfaces

```bash│   ├── app.py                   # Streamlit UI

# 1. Analyze HTML structure only│   ├── telegram_bot_bilingual.py # Telegram bot

python scripts/intelligent_analyzer.py <url> analysis.json│   ├── quick_scrape.py          # CLI tool

│   └── demo_universal.py        # Live demo

# 2. Generate scraper from analysis│

python scripts/scraper_generator.py analysis.json scraper.py├── Testing

│   ├── test_universal_scraper.py # Test runner

# 3. Run custom scraper│   └── test_cases_100plus.py     # 127 test cases

python scraper.py│

├── AI & Analysis

# 4. Analyze extracted data│   ├── ai_analyzer.py           # AI insights

python scripts/data_analyzer.py data.csv analysis.json│   └── report_generator.py      # PDF reports

│

# 5. Generate PDF report└── Documentation

python scripts/pdf_generator.py analysis.json report.pdf    ├── README.md                # This file

```    └── *.md                     # Guides

```

### Custom Configuration

---

Edit scripts to customize:

- User agent and headers## 🧪 Testing

- Rate limiting delays

- Chart styles and colors### Run All Tests

- PDF layout and fonts```bash

- Selector strategiespython test_universal_scraper.py

```

---

### Test Specific URL

## 📚 Documentation```bash

python test_universal_scraper.py --test-url "https://example.com"

- [Professional Scraper Workflow](docs/PROFESSIONAL_SCRAPER_WORKFLOW.md) - Complete guide```

- [Free Aviation APIs](docs/FREE_AVIATION_APIS.md) - API integration guide

- [EgyptAir Scraper](EGYPTAIR_SCRAPER_COMPLETE.md) - Aviation data collection### Expected Results

```

---📊 Universal Web Scraper Test Results

=====================================

## 📦 Dependencies✅ Sports:      15/15 (100.0%)

✅ E-commerce:  20/20 (100.0%)

### Core Requirements✅ Jobs:        10/10 (100.0%)

- `requests` - HTTP requests...

- `beautifulsoup4` - HTML parsing📊 Total: 125/127 (98.4%)

- `lxml` - Fast XML/HTML parser🎉 Excellent! Production-ready!

- `pandas` - Data manipulation```



### Analysis & Visualization---

- `matplotlib` - Plotting library

- `seaborn` - Statistical visualizations## 🤝 Contributing

- `numpy` - Numerical computing

Contributions welcome! Please:

### Report Generation

- `reportlab` - PDF creation1. Fork the repository

- `Pillow` - Image processing2. Create a feature branch (`git checkout -b feature/amazing`)

3. Test your changes (`python test_universal_scraper.py`)

### Optional4. Commit (`git commit -m "Add amazing feature"`)

- `playwright` / `selenium` - JavaScript-heavy sites5. Push (`git push origin feature/amazing`)

- `streamlit` - Web UI6. Open a Pull Request

- `openai` - AI features

---

See [requirements.txt](requirements.txt) for complete list.

## 📄 License

---

MIT License - see [LICENSE](LICENSE) file for details.

## 🎨 Example Output

---

### Console Output

```## 🙏 Acknowledgments

====================================================================================================

🤖 INTELLIGENT WEB SCRAPER WORKFLOW- **BeautifulSoup4** - HTML parsing

====================================================================================================- **Selenium** - Dynamic content

- **Streamlit** - Web UI

🌐 Target URL: http://quotes.toscrape.com- **python-telegram-bot** - Telegram integration

📁 Output Directory: F:\Scrapper\outputs- **Google Gemini** - AI analysis



STEP 1: ANALYZING HTML STRUCTURE ✅---

STEP 2: GENERATING CUSTOM SCRAPER ✅

STEP 3: RUNNING SCRAPER TO EXTRACT DATA ✅## ⭐ Support

  → Extracted 14 items

STEP 4: ANALYZING SCRAPED DATA ✅If you find this project useful, please give it a star! ⭐

  → Generated 9 insights

  → Created 5 visualizations**Made with ❤️**

STEP 5: GENERATING PDF REPORT ✅

  → Report: quotes_toscrape_com_report.pdf**Happy Scraping! 🚀**


====================================================================================================
✅ WORKFLOW COMPLETE
====================================================================================================

📁 Files Generated (11):
   📄 analysis.json (1.3 KB)
   📄 scraper.py (5.5 KB)
   📄 data.csv (6.9 KB)
   📄 data_analysis.json (4.6 KB)
   📄 5 × charts (PNG)
   📄 report.pdf (302.1 KB) ← Auto-opens
   📄 workflow.json (2.8 KB)
```

### Generated Files
- Custom Python scraper
- Extracted data (CSV + JSON)
- Statistical analysis
- 5+ data visualizations
- Professional PDF report

See [examples/](examples/) folder for sample outputs.

---

## 🚨 Best Practices

### Legal & Ethical
- ✅ Always check `robots.txt`
- ✅ Respect website Terms of Service
- ✅ Use rate limiting (included by default)
- ✅ Identify with proper User-Agent

### Technical
- ✅ Handle errors gracefully (built-in)
- ✅ Validate extracted data
- ✅ Use UTF-8 encoding
- ✅ Log execution for debugging

### Performance
- ✅ Implement delays between requests
- ✅ Cache responses when appropriate
- ✅ Use connection pooling
- ✅ Monitor resource usage

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: No data extracted
- **Solution**: Check if site requires authentication or JavaScript rendering

**Issue**: Unicode/encoding errors
- **Solution**: Ensure UTF-8 encoding in all files

**Issue**: PDF generation fails
- **Solution**: Verify reportlab installation and write permissions

**Issue**: Website blocks requests
- **Solution**: Adjust User-Agent, add delays, or use Playwright for JS sites

See [workflow.json](outputs/) for detailed execution logs.

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- BeautifulSoup4 for HTML parsing
- Pandas for data manipulation
- ReportLab for PDF generation
- Matplotlib/Seaborn for visualizations

---

## 📧 Contact

**Repository**: [samuelhany-cpu/Scrapper](https://github.com/samuelhany-cpu/Scrapper)

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ by [samuelhany-cpu](https://github.com/samuelhany-cpu)

</div>
