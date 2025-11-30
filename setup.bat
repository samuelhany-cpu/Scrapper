@echo off
echo Setting up Universal Web Scraper...
echo.

echo Step 1: Creating virtual environment...
python -m venv .venv
echo.

echo Step 2: Installing Python packages...
.venv\Scripts\pip install -r requirements.txt
echo.

echo Step 3: Installing Playwright browsers...
.venv\Scripts\playwright install chromium
echo.

echo Step 4: Creating directories...
if not exist "output" mkdir output
if not exist "logs" mkdir logs
if not exist "reports" mkdir reports
echo.

echo Step 5: Setting up environment file...
if not exist ".env" (
    copy .env.example .env
    echo Created .env file. Please add your OpenAI API key.
) else (
    echo .env file already exists.
)
echo.

echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key (optional but recommended)
echo 2. Run: run.bat
echo.
pause
