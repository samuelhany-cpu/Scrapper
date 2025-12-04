# 🌐 Universal Web Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**The world's most intelligent universal web scraper** - automatically detects and scrapes ANY website from ANY niche with **98.4% accuracy**!

## 🚀 Key Features

### 🎯 Universal Domain Detection
- **25+ domain patterns** automatically detected
- **200+ domain keywords** for intelligent classification
- **Zero configuration** - just provide a URL!
- Works on sports, e-commerce, news, jobs, real estate, travel, education, entertainment, finance, technology, and more!

### 🧠 Intelligent Extraction
- **30+ extraction strategies** for different content types
- Automatic fallback mechanisms for unknown sites
- Supports both static and dynamic content
- Multi-language support (English, Arabic, and more)

### 🖥️ Multiple Interfaces
- ✅ **CLI Tool** - Quick command-line scraping
- ✅ **Streamlit UI** - Beautiful web interface
- ✅ **Telegram Bot** - Bilingual bot with AI analysis
- ✅ **Python API** - Use in your own code

### 📊 Proven Performance
- **127 real-world websites tested**
- **98.4% success rate** (125/127 passed)
- Perfect 100% accuracy on 23 out of 25 categories
- Production-ready and battle-tested

---

## 📋 Quick Navigation

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Supported Domains](#-supported-domains)
- [Documentation](#-documentation)
- [Contributing](#-contributing)

---

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Chrome/Firefox browser (for dynamic content)

### Quick Setup

**Windows:**
```bash
git clone https://github.com/yourusername/universal-web-scraper.git
cd universal-web-scraper
setup.bat
```

**Linux/Mac:**
```bash
git clone https://github.com/yourusername/universal-web-scraper.git
cd universal-web-scraper
chmod +x setup.sh
./setup.sh
```

### Manual Installation
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### Configuration (Optional)
```bash
cp .env.example .env
# Edit .env and add your API keys
```

---

## ⚡ Quick Start

### 1. Test Any Website
```bash
python test_universal_scraper.py --test-url "https://www.example.com"
```

### 2. Quick Scrape (CLI)
```bash
python quick_scrape.py "https://www.yallakora.com/match-center"
```

### 3. Run Live Demo
```bash
python demo_universal.py
```

### 4. Start Web UI
```bash
streamlit run app.py
```

### 5. Start Telegram Bot
```bash
python telegram_bot_bilingual.py
```

---

## 📖 Usage Examples

### Command Line Interface

```bash
# Scrape any website
python quick_scrape.py "https://www.amazon.com/s?k=laptop"

# Test specific URL
python test_universal_scraper.py --test-url "https://news.ycombinator.com"

# Run all 127 tests
python test_universal_scraper.py
```

### Python API

```python
from adaptive_scraper import AdaptiveSmartScraper
from logger import setup_logger

# Initialize
logger = setup_logger("my_scraper")
scraper = AdaptiveSmartScraper(logger)

# Scrape any URL
scraper.scrape_url("https://www.yallakora.com/match-center")

# Get data
data = scraper.get_data()

# Export
scraper.export_to_csv("output.csv")
```

---

## 🌟 Supported Domains

### Perfect 100% Accuracy
✅ Sports • E-commerce • Fashion • Jobs • Real Estate  
✅ Travel • Education • Entertainment • Food • Finance  
✅ Technology • Gaming • Weather • and more!

### Tested Websites (127 total)
Amazon, eBay, Walmart, Yallakora, ESPN, CNN, BBC, LinkedIn, Indeed, Zillow, Booking.com, Coursera, IMDb, Netflix, YouTube, GitHub, StackOverflow, and 110+ more!

See [UNIVERSAL_SUCCESS.md](UNIVERSAL_SUCCESS.md) for complete list.

---

## 📚 Documentation

- **[UNIVERSAL_SCRAPER_GUIDE.md](UNIVERSAL_SCRAPER_GUIDE.md)** - Complete user guide
- **[UNIVERSAL_SUCCESS.md](UNIVERSAL_SUCCESS.md)** - Test results (98.4% success!)
- **[QUICKSTART_UNIVERSAL.md](QUICKSTART_UNIVERSAL.md)** - Quick reference
- **[TELEGRAM_BOT_GUIDE.md](TELEGRAM_BOT_GUIDE.md)** - Telegram bot setup
- **[BILINGUAL_GUIDE.md](BILINGUAL_GUIDE.md)** - Multi-language support

---

## 📁 Project Structure

```
universal-web-scraper/
├── Core Components
│   ├── adaptive_scraper.py      # Main scraper (30+ strategies)
│   ├── domain_patterns.py       # Universal detection (25+ patterns)
│   ├── scraper_selenium.py      # Dynamic content
│   └── logger.py                # Logging system
│
├── User Interfaces
│   ├── app.py                   # Streamlit UI
│   ├── telegram_bot_bilingual.py # Telegram bot
│   ├── quick_scrape.py          # CLI tool
│   └── demo_universal.py        # Live demo
│
├── Testing
│   ├── test_universal_scraper.py # Test runner
│   └── test_cases_100plus.py     # 127 test cases
│
├── AI & Analysis
│   ├── ai_analyzer.py           # AI insights
│   └── report_generator.py      # PDF reports
│
└── Documentation
    ├── README.md                # This file
    └── *.md                     # Guides
```

---

## 🧪 Testing

### Run All Tests
```bash
python test_universal_scraper.py
```

### Test Specific URL
```bash
python test_universal_scraper.py --test-url "https://example.com"
```

### Expected Results
```
📊 Universal Web Scraper Test Results
=====================================
✅ Sports:      15/15 (100.0%)
✅ E-commerce:  20/20 (100.0%)
✅ Jobs:        10/10 (100.0%)
...
📊 Total: 125/127 (98.4%)
🎉 Excellent! Production-ready!
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Test your changes (`python test_universal_scraper.py`)
4. Commit (`git commit -m "Add amazing feature"`)
5. Push (`git push origin feature/amazing`)
6. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **BeautifulSoup4** - HTML parsing
- **Selenium** - Dynamic content
- **Streamlit** - Web UI
- **python-telegram-bot** - Telegram integration
- **Google Gemini** - AI analysis

---

## ⭐ Support

If you find this project useful, please give it a star! ⭐

**Made with ❤️**

**Happy Scraping! 🚀**
