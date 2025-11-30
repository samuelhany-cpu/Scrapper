@echo off
echo Cleaning up unnecessary files...

REM Delete inspect files
if exist inspect_liitem.py del inspect_liitem.py
if exist inspect_match_item.py del inspect_match_item.py
if exist inspect_yallakora.py del inspect_yallakora.py
if exist inspect_yallakora2.py del inspect_yallakora2.py
if exist inspect_yallakora3.py del inspect_yallakora3.py

REM Delete test sports files
if exist test_sports.py del test_sports.py
if exist test_sports_direct.py del test_sports_direct.py
if exist test_sports_simple.py del test_sports_simple.py

REM Delete Twitter test files
if exist test_twitter_auth.py del test_twitter_auth.py
if exist test_twitter_now.py del test_twitter_now.py
if exist test_twitter_scraper.py del test_twitter_scraper.py
if exist test_twitter_stealth.py del test_twitter_stealth.py

REM Delete Firefox test files
if exist test_firefox.py del test_firefox.py
if exist test_firefox_stealth.py del test_firefox_stealth.py

REM Delete other test files
if exist test_gallerydl.py del test_gallerydl.py
if exist test_ytdlp.py del test_ytdlp.py
if exist test_api_key.py del test_api_key.py
if exist test_bot_config.py del test_bot_config.py
if exist test_method.py del test_method.py
if exist test_direct_scraper.py del test_direct_scraper.py
if exist quick_test_ytdlp.py del quick_test_ytdlp.py

REM Delete Twitter scraper files (outdated)
if exist twitter_auth_scraper.py del twitter_auth_scraper.py
if exist twitter_direct_scraper.py del twitter_direct_scraper.py
if exist twitter_firefox_stealth.py del twitter_firefox_stealth.py
if exist twitter_gallerydl_auth.py del twitter_gallerydl_auth.py
if exist twitter_gallerydl_scraper.py del twitter_gallerydl_scraper.py
if exist twitter_scraper.py del twitter_scraper.py
if exist twitter_stealth_scraper.py del twitter_stealth_scraper.py
if exist twitter_ytdlp_scraper.py del twitter_ytdlp_scraper.py

REM Delete temporary files
if exist match_structure.txt del match_structure.txt
if exist sports_test_output.txt del sports_test_output.txt
if exist setup_twitter_credentials.bat del setup_twitter_credentials.bat

REM Delete outdated documentation files
if exist API_TEST_RESULTS.md del API_TEST_RESULTS.md
if exist COMPLETE_BOT_READY.md del COMPLETE_BOT_READY.md
if exist COMPLETE_SYSTEM_GUIDE.md del COMPLETE_SYSTEM_GUIDE.md
if exist FREE_ALTERNATIVES.md del FREE_ALTERNATIVES.md
if exist GET_FREE_AI_KEY.md del GET_FREE_AI_KEY.md
if exist QUICKSTART.md del QUICKSTART.md
if exist SUPPORTED_SITES.md del SUPPORTED_SITES.md
if exist TELEGRAM_BOT_UPDATED.md del TELEGRAM_BOT_UPDATED.md
if exist TEST_RESULTS.md del TEST_RESULTS.md
if exist TWITTER_CHOOSE_METHOD.md del TWITTER_CHOOSE_METHOD.md
if exist TWITTER_COMPLETE_GUIDE.md del TWITTER_COMPLETE_GUIDE.md
if exist TWITTER_COOKIES_GUIDE.md del TWITTER_COOKIES_GUIDE.md
if exist TWITTER_FINAL_SOLUTION.md del TWITTER_FINAL_SOLUTION.md
if exist TWITTER_QUICKSTART.md del TWITTER_QUICKSTART.md
if exist TWITTER_SETUP_GUIDE.md del TWITTER_SETUP_GUIDE.md

REM Clean logs directory (keep directory)
if exist logs\*.log del /Q logs\*.log

REM Clean output directory (keep directory, remove old CSVs)
if exist output\test_*.csv del /Q output\test_*.csv
if exist output\firefox_test.csv del output\firefox_test.csv
if exist output\twitter_media rmdir /S /Q output\twitter_media

REM Clean reports directory (keep directory, remove old PDFs)
if exist reports\*.pdf del /Q reports\*.pdf

echo Cleanup complete!
echo.
echo Kept files:
echo - Core scraper files
echo - Universal detection system
echo - Main documentation
echo - Configuration files
echo.
pause
