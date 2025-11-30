#!/bin/bash

echo "🌐 Universal Web Scraper - Setup Script"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Error: Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv .venv

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create virtual environment!"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies!"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created! Please edit it and add your API keys."
fi

# Create necessary directories
echo ""
echo "Creating output directories..."
mkdir -p logs
mkdir -p output
mkdir -p reports

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file and add your API keys (optional)"
echo "2. Activate virtual environment: source .venv/bin/activate"
echo "3. Run test: python test_universal_scraper.py"
echo "4. Start UI: streamlit run app.py"
echo ""
echo "Happy scraping! 🚀"
