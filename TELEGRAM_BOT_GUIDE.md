# 🤖 TELEGRAM BOT SETUP GUIDE

## Quick Setup (5 Minutes!)

### Step 1: Create Your Telegram Bot

1. **Open Telegram** and search for `@BotFather`

2. **Start a chat** with BotFather and send:
   ```
   /newbot
   ```

3. **Choose a name** for your bot (e.g., "My Web Scraper")

4. **Choose a username** (must end with 'bot', e.g., "mywebscraper_bot")

5. **Copy the token** - BotFather will give you something like:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

6. **Add token to .env file:**
   ```
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

---

### Step 2: Run Your Bot

#### Option 1: Run Locally (On Your Computer)

```bash
.venv\Scripts\python telegram_bot.py
```

Your bot is now running! It will work as long as your computer is on.

#### Option 2: Run on Free Cloud (24/7)

See "FREE HOSTING OPTIONS" section below.

---

### Step 3: Test Your Bot

1. Open Telegram
2. Search for your bot username (e.g., @mywebscraper_bot)
3. Click "Start"
4. Send a URL: `https://example.com`
5. Get CSV, PDF, and logs back!

---

## 📋 Bot Commands

Once your bot is running, users can interact with it:

### Basic Commands:
- `/start` - Welcome message and instructions
- `/help` - Detailed help and examples
- `/scrape <URL>` - Scrape a specific URL
- Just send URL directly - No command needed!

### Examples:
```
/scrape https://en.wikipedia.org/wiki/Web_scraping
https://news.ycombinator.com
https://quotes.toscrape.com
```

---

## 🎯 Bot Features

### 1. **Smart Adaptive Scraping**
- Automatically analyzes website structure
- Detects: Tables, Products, Articles, Lists
- Adapts extraction strategy accordingly
- Uses FREE Gemini AI for intelligence

### 2. **Multiple File Outputs**
- 📊 CSV file (data in spreadsheet format)
- 📄 PDF report (statistics and analysis)
- 📋 Log file (detailed activity log)

### 3. **Structure Detection**
The bot automatically detects:
- **E-commerce sites** → Extracts products, prices, images
- **News sites** → Extracts articles, dates, authors
- **Tables** → Parses table data properly
- **Lists** → Structures list items
- **General pages** → Smart content extraction

### 4. **Real-time Updates**
- Shows progress while scraping
- Updates status dynamically
- Sends files when ready

---

## 🆓 FREE HOSTING OPTIONS

### Option 1: Render.com (Recommended)

**✅ Completely FREE**
**✅ 24/7 running**
**✅ Easy setup**

1. **Create account:** https://render.com
2. **Create new Web Service**
3. **Connect your GitHub repo** (or upload files)
4. **Build command:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Start command:**
   ```bash
   python telegram_bot.py
   ```
6. **Add environment variables:**
   - `GEMINI_API_KEY` = your Gemini key
   - `TELEGRAM_BOT_TOKEN` = your bot token
7. **Deploy!**

Free tier: 750 hours/month (enough for 24/7!)

---

### Option 2: Railway.app

**✅ FREE $5/month credit**
**✅ Auto-deploys**
**✅ Easy setup**

1. **Create account:** https://railway.app
2. **New Project → Deploy from GitHub**
3. **Select your repo**
4. **Add environment variables**
5. **Deploy!**

---

### Option 3: PythonAnywhere (Free)

**✅ 100% Free tier**
**✅ Browser-based**
**✅ Simple**

1. **Create account:** https://www.pythonanywhere.com
2. **Upload your files**
3. **Open Console and run:**
   ```bash
   python telegram_bot.py
   ```

Note: Free tier has some limitations but works!

---

### Option 4: Heroku (Requires Credit Card)

1. **Create app on Heroku**
2. **Add Procfile:**
   ```
   worker: python telegram_bot.py
   ```
3. **Deploy**

Note: Heroku removed free tier, but still affordable (~$5/month)

---

## 🔧 Configuration

### Required:
```env
TELEGRAM_BOT_TOKEN=your_bot_token
GEMINI_API_KEY=your_gemini_key (FREE)
```

### Optional:
```env
OPENAI_API_KEY=your_openai_key (PAID)
ANTHROPIC_API_KEY=your_claude_key (PAID)
```

The bot prioritizes Gemini (free) first!

---

## 📱 Bot Usage Examples

### Example 1: Scrape Wikipedia
```
https://en.wikipedia.org/wiki/Python_(programming_language)
```
**Gets:** Article content, tables, references

### Example 2: Scrape News Site
```
https://news.ycombinator.com
```
**Gets:** Headlines, links, scores

### Example 3: Scrape Product Page
```
https://quotes.toscrape.com
```
**Gets:** Quotes, authors, tags

### Example 4: With Command
```
/scrape https://example.com
```

---

## 🎨 Customization

### Change Bot Messages:
Edit `telegram_bot.py`:
- `start_command()` - Welcome message
- `help_command()` - Help text
- `process_scraping()` - Status messages

### Add Commands:
```python
async def stats_command(self, update, context):
    # Your code here
    pass

# Register:
application.add_handler(CommandHandler("stats", self.stats_command))
```

### Change Scraping Behavior:
Edit `adaptive_scraper.py`:
- Modify `analyze_structure()` for structure detection
- Adjust `determine_strategy()` for strategy selection
- Customize extraction methods

---

## 🐛 Troubleshooting

### Bot doesn't respond?
1. Check token is correct in `.env`
2. Ensure bot is running (see terminal output)
3. Try `/start` command first

### Scraping fails?
1. Check internet connection
2. Some sites block scrapers (normal)
3. Check logs for details

### Files not sending?
1. Check file size (Telegram limit: 50MB)
2. Ensure directories exist (output/, reports/, logs/)
3. Check file permissions

### Bot stops randomly?
1. Use free cloud hosting (see above)
2. Check error messages in terminal
3. Restart bot: `.venv\Scripts\python telegram_bot.py`

---

## 📊 Bot Statistics (Coming Soon)

Track:
- Total scrapes
- Success rate
- Most scraped domains
- User statistics

---

## 🔒 Security Tips

1. **Never share your bot token**
2. **Keep .env file private**
3. **Don't commit tokens to Git**
4. **Use environment variables in deployment**
5. **Monitor bot usage**

---

## 📈 Scaling

### For Heavy Usage:

1. **Use queue system:**
   - Add Redis
   - Queue scraping tasks
   - Process async

2. **Add database:**
   - Store scrape history
   - Track users
   - Cache results

3. **Add rate limiting:**
   - Prevent abuse
   - Fair usage policy

---

## 💡 Advanced Features (Add Later)

- Schedule scraping
- Monitor URL changes
- Webhook integration
- Multi-page scraping
- Batch URL processing
- Custom export formats
- Notifications

---

## 🆘 Support

**Issues?** Check:
1. Bot token is correct
2. Gemini API key is set
3. All dependencies installed
4. Bot is running
5. Internet connection works

**Still stuck?**
- Check logs in `logs/` directory
- Review error messages
- Test with simple URL first

---

## ✅ Checklist

Before deploying:
- [ ] Bot token obtained from @BotFather
- [ ] Token added to .env
- [ ] Gemini API key configured (FREE)
- [ ] Dependencies installed
- [ ] Bot tested locally
- [ ] Hosting platform chosen
- [ ] Environment variables configured
- [ ] Bot deployed and running
- [ ] Tested with real URLs

---

## 🎉 You're Done!

Your Telegram bot is ready!

**Test it:**
1. Open Telegram
2. Search your bot
3. Send: `https://example.com`
4. Get results!

**Share it:**
- Give bot username to friends
- Use in groups
- Integrate with other services

---

**ENJOY YOUR 24/7 WEB SCRAPING BOT! 🚀**
