# Contributing to Universal Web Scraper

First off, thank you for considering contributing to Universal Web Scraper! 🎉

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Description**: Clear and concise description of the bug
- **Steps to Reproduce**: Step-by-step instructions
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, browser version
- **Logs**: Relevant log output from `logs/` directory
- **Screenshots**: If applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use Case**: Describe the problem you're trying to solve
- **Proposed Solution**: How you think it should work
- **Alternatives**: Other solutions you've considered
- **Additional Context**: Screenshots, examples, etc.

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/universal-web-scraper.git
   cd universal-web-scraper
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
   - Add tests for new features

4. **Test your changes**
   ```bash
   # Run existing tests
   python test_universal_scraper.py
   
   # Test your specific changes
   python test_universal_scraper.py --test-url "your-test-url"
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```
   
   Use clear commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `test:` for tests
   - `refactor:` for code refactoring

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Provide a clear description
   - Link related issues
   - Include screenshots if relevant

## 🎯 Areas for Contribution

### High Priority
- 🌐 **Add more domain patterns** (see `domain_patterns.py`)
- 🌍 **Add more language support** (see `language.py`)
- 🧪 **Add more test cases** (see `test_cases_100plus.py`)
- 📝 **Improve documentation**

### Medium Priority
- 🐛 **Fix edge cases** (Bloomberg Markets, CarMax)
- ⚡ **Performance optimizations**
- 🎨 **UI improvements** (Streamlit, Telegram bot)
- 🔧 **Better error handling**

### Low Priority
- 🌟 **New features** (scheduling, webhooks, etc.)
- 🐳 **Docker support**
- 📦 **Package distribution** (PyPI)

## 📝 Code Style

### Python Style Guide
- Follow PEP 8
- Use meaningful variable names
- Add docstrings for functions/classes
- Keep functions focused and small
- Use type hints where appropriate

Example:
```python
def extract_product_data(soup: BeautifulSoup) -> list[dict]:
    """
    Extract product information from e-commerce page.
    
    Args:
        soup: BeautifulSoup object of the page
        
    Returns:
        List of dictionaries containing product data
    """
    products = []
    # Implementation...
    return products
```

### Documentation Style
- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Update README if adding features

### Commit Message Format
```
<type>: <subject>

<body>

<footer>
```

Example:
```
feat: Add support for job listing websites

- Added LinkedIn pattern detection
- Added Indeed extraction strategy
- Updated test cases with job websites

Closes #123
```

## 🧪 Testing

### Adding Test Cases

When adding support for a new website or domain:

1. **Add test case to `test_cases_100plus.py`**:
```python
{
    'url': 'https://www.newsite.com',
    'expected_type': 'new_pattern_type',
    'category': 'New Category'
}
```

2. **Add domain pattern to `domain_patterns.py`**:
```python
'new_pattern': {
    'keywords': ['keyword1', 'keyword2', 'newsite.com'],
    'indicators': ['.selector1', '#selector2'],
    'type': 'new_pattern_type',
    'priority': 10
}
```

3. **Add extraction strategy to `adaptive_scraper.py`**:
```python
def _extract_new_pattern(self, soup):
    """Extract data for new pattern type"""
    # Implementation...
    return data
```

4. **Test your changes**:
```bash
python test_universal_scraper.py --test-url "https://www.newsite.com"
```

### Running Tests

```bash
# Run all tests
python test_universal_scraper.py

# Test specific URL
python test_universal_scraper.py --test-url "URL"

# Quick test (no fetching)
python test_universal_scraper.py --quick

# Run demo
python demo_universal.py
```

## 🐛 Debugging

### Enable Debug Logging

In `logger.py`, change level to DEBUG:
```python
logger.setLevel(logging.DEBUG)
```

### Check Logs

All logs are saved in `logs/` directory:
```bash
tail -f logs/scraper_*.log
```

### Test Individual Components

```python
# Test domain detection only
from domain_patterns import detect_domain_type
result = detect_domain_type(url, None)
print(result)

# Test extraction only
from adaptive_scraper import AdaptiveSmartScraper
scraper = AdaptiveSmartScraper(logger)
data = scraper._extract_sports_matches(soup)
```

## 📋 Checklist Before Submitting

- [ ] Code follows project style
- [ ] Added/updated comments and docstrings
- [ ] Tested changes thoroughly
- [ ] All existing tests still pass
- [ ] Updated documentation if needed
- [ ] Added test cases for new features
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] PR description is complete

## 🎓 Resources

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)

## 💬 Community

- **Issues**: [GitHub Issues](https://github.com/yourusername/universal-web-scraper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/universal-web-scraper/discussions)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Every contribution, no matter how small, helps make Universal Web Scraper better for everyone!

**Happy Contributing! 🚀**
