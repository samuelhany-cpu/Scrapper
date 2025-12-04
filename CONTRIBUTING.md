# Contributing to Intelligent Web Scraper

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/samuelhany-cpu/Scrapper.git
   cd Scrapper
   ```

2. **Set up development environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### Example:
```python
def extract_data(url: str) -> dict:
    """
    Extract structured data from a given URL.
    
    Args:
        url (str): The target URL to scrape
        
    Returns:
        dict: Extracted data with metadata
    """
    pass
```

## 🧪 Testing

- Add unit tests for new features
- Ensure all existing tests pass
- Test with different websites and edge cases

```bash
# Run tests
python -m pytest tests/
```

## 📚 Documentation

- Update README.md if adding new features
- Add docstrings to new functions
- Update workflow documentation if changing process
- Include code examples for complex features

## 🔧 Pull Request Process

1. **Update documentation**
   - README.md
   - Docstrings
   - Code comments

2. **Test your changes**
   - Run existing tests
   - Add new tests if needed
   - Test manually with different URLs

3. **Commit with clear messages**
   ```bash
   git commit -m "feat: Add support for pagination"
   git commit -m "fix: Handle Unicode characters in PDF generation"
   git commit -m "docs: Update installation instructions"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**
   - Provide clear description
   - Reference related issues
   - Include test results
   - Add screenshots if relevant

## 🎯 Areas for Contribution

### High Priority
- [ ] Support for more website types
- [ ] Improved JavaScript handling
- [ ] Better error recovery
- [ ] Performance optimization

### Medium Priority
- [ ] Additional export formats (Excel, SQLite)
- [ ] Web UI improvements
- [ ] CLI enhancements
- [ ] More visualization types

### Documentation
- [ ] Video tutorials
- [ ] More examples
- [ ] API documentation
- [ ] Troubleshooting guide

## 🐛 Bug Reports

When reporting bugs, include:
- Python version
- Operating system
- Full error traceback
- Minimal reproducible example
- Expected vs actual behavior

## 💡 Feature Requests

When suggesting features, include:
- Use case description
- Proposed implementation
- Example usage
- Potential challenges

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow project guidelines

## 📧 Questions?

Feel free to open an issue for:
- Questions about usage
- Feature discussions
- Implementation help
- General feedback

---

Thank you for contributing! 🙏
