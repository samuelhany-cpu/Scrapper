"""
TELEGRAM BOT FOR UNIVERSAL WEB SCRAPER
Send URL → Get CSV, PDF Report, and Logs back!
"""
import os
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

from config import Config
from logger import ScraperLogger
from adaptive_scraper import AdaptiveSmartScraper
from twitter_scraper import TwitterMediaScraper
from twitter_ytdlp_scraper import TwitterYTDLPScraper
from twitter_gallerydl_auth import TwitterGalleryDLScraperAuth
from report_generator import ReportGenerator
from language import LanguageSupport, t

# Bot Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

class ScraperBot:
    def __init__(self):
        self.active_tasks = {}
        self.user_languages = {}  # Store user language preferences
        Config.ensure_directories()
    
    def get_user_language(self, update: Update):
        """
        Get user's preferred language
        Auto-detect from Telegram settings or message content
        """
        user_id = update.effective_user.id
        
        # Check if we have stored preference
        if user_id in self.user_languages:
            return self.user_languages[user_id]
        
        # Try to get from Telegram user settings
        if update.effective_user.language_code:
            if update.effective_user.language_code.startswith('ar'):
                self.user_languages[user_id] = 'ar'
                return 'ar'
        
        # Detect from message text
        message = update.message or update.edited_message
        if message and message.text:
            detected = LanguageSupport.detect_language(message.text)
            self.user_languages[user_id] = detected
            return detected
        
        # Default to English
        self.user_languages[user_id] = 'en'
        return 'en'
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        message = update.message or update.edited_message
        if not message:
            return
            
        welcome_message = """
🤖 **Universal Web Scraper Bot**

Welcome! I can scrape any website and extract data for you.

**� How to Use:**
Just send me any URL - no commands needed!

**Examples:**
`https://example.com`
`https://twitter.com/username/status/123`
`https://en.wikipedia.org/wiki/Web_scraping`

**✨ Features:**
• 🌐 Universal web scraper (any site)
• 🐦 Twitter media downloader (authenticated)
• 🤖 AI-powered extraction (FREE Gemini)
• 📊 CSV data export
• 📄 PDF reports
• 📋 Detailed logs

**📋 Optional Commands:**
/start - Show this message
/scrape <URL> - Alternative way to scrape
/help - Detailed help
/stats - View statistics

**🎯 Supported:**
✅ News sites, blogs, Wikipedia
✅ E-commerce, product pages
✅ Twitter/X images & videos
✅ Tables, lists, articles
✅ Any public website!

Try it now! Just paste a URL 👇
        """
        await message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        message = update.message or update.edited_message
        if not message:
            return
            
        help_text = """
📖 **How to Use This Bot**

**⚡ Quick Method (Recommended):**
Just paste any URL - bot auto-detects and scrapes!
`https://example.com`

**📋 Command Method (Optional):**
`/scrape https://example.com`

**📊 What You Get:**
✅ CSV file with extracted data
✅ PDF report with statistics  
✅ Detailed log file
✅ For Twitter: Images & Videos downloaded!

**🐦 Twitter/X Special Features:**
• 🔐 Authenticated scraping (uses browser cookies)
• 🖼 Downloads all images
• 🎥 Downloads all videos
• 📱 Works with public & private tweets (if you follow them)
• 🚫 No API limits!

**🎯 Supported Sites:**
• E-commerce (Amazon, eBay, etc.)
• News websites & Blogs
• Wikipedia & Documentation
• Twitter/X media (images/videos)
• Product listings & Tables
• Any public website!

**🤖 Smart Features:**
• Auto-detects website type
• Adapts extraction strategy
• Uses FREE Gemini AI
• Handles JavaScript sites
• Extracts tables, lists, articles

**⚡ Examples:**
`https://en.wikipedia.org/wiki/Web_scraping`
`https://news.ycombinator.com`
`https://quotes.toscrape.com`

**❓ Need Help?**
Contact: @YourUsername
        """
        await message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def scrape_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /scrape command"""
        # Handle both new and edited messages
        message = update.message or update.edited_message
        if not message:
            return
            
        if not context.args:
            await message.reply_text(
                "❌ Please provide a URL!\n\nUsage: `/scrape https://example.com`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        url = context.args[0]
        await self.process_scraping(update, url)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle plain text messages (URLs)"""
        # Handle both new and edited messages
        message = update.message or update.edited_message
        if not message:
            return
            
        text = message.text.strip()
        
        # Check if it's a URL
        if text.startswith('http://') or text.startswith('https://'):
            await self.process_scraping(update, text)
        else:
            await message.reply_text(
                "❓ Please send a valid URL starting with http:// or https://\n\n"
                "Example: `https://example.com`\n\n"
                "Or use /help for more information.",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def process_scraping(self, update: Update, url: str):
        """Process the scraping request"""
        # Handle both new and edited messages
        message = update.message or update.edited_message
        if not message:
            return
            
        user_id = update.effective_user.id
        username = update.effective_user.username or update.effective_user.first_name
        
        # Check if it's a Twitter/X URL
        is_twitter = 'twitter.com' in url or 'x.com' in url
        
        # Send initial message
        scraper_type = "🐦 Twitter Media Scraper" if is_twitter else "🌐 Universal Scraper"
        status_message = await message.reply_text(
            f"🚀 **Starting scrape...**\n\n"
            f"🔗 URL: `{url}`\n"
            f"👤 User: {username}\n"
            f"🔧 Mode: {scraper_type}\n\n"
            f"⏳ Please wait...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        try:
            # Create logger for this scrape
            session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            logger = ScraperLogger(session_id)
            
            # Update: Initializing
            await status_message.edit_text(
                f"🔧 **Initializing scraper...**\n\n"
                f"🔗 URL: `{url}`\n"
                f"🤖 Using AI + Adaptive Strategy\n\n"
                f"⏳ Loading page...",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Use Twitter scraper for Twitter/X URLs
            if is_twitter:
                await self.process_twitter_scraping(update, url, status_message, logger)
                return
            
            # Create scraper
            scraper = AdaptiveSmartScraper(logger)
            
            # Update: Scraping
            await status_message.edit_text(
                f"🔍 **Scraping in progress...**\n\n"
                f"🔗 URL: `{url}`\n"
                f"📊 Analyzing structure...\n"
                f"🤖 Extracting data...\n\n"
                f"⏳ This may take 30-60 seconds...",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Run scraping
            success = scraper.scrape_url(url)
            
            if not success:
                # Check log for specific error
                error_msg = "❌ **Scraping failed!**\n\n" f"🔗 URL: `{url}`\n\n"
                
                # Get last log entry for detailed error
                if logger.log_file and os.path.exists(logger.log_file):
                    try:
                        with open(logger.log_file, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            for line in reversed(lines[-20:]):  # Check last 20 lines
                                if '🔒' in line or 'authentication' in line.lower():
                                    error_msg += (
                                        "**Reason:** Site requires authentication\n\n"
                                        "❌ This site (X/Twitter, Facebook, LinkedIn, etc.) "
                                        "requires login to view content.\n\n"
                                        "💡 **Try these alternatives:**\n"
                                        "• Public websites without login\n"
                                        "• News sites\n"
                                        "• Wikipedia pages\n"
                                        "• E-commerce product pages\n"
                                        "• Public blogs\n"
                                    )
                                    break
                                elif 'timeout' in line.lower():
                                    error_msg += (
                                        "**Reason:** Page load timeout\n\n"
                                        "⚠️ The site took too long to respond (>60s)\n\n"
                                        "� **Possible causes:**\n"
                                        "• Very heavy JavaScript site\n"
                                        "• Slow server response\n"
                                        "• Anti-bot protection\n"
                                        "• Network issues\n\n"
                                        "Try a simpler website or try again later."
                                    )
                                    break
                            else:
                                error_msg += (
                                    "**Possible reasons:**\n"
                                    "• Invalid URL format\n"
                                    "• Site blocked by firewall\n"
                                    "• Server not responding\n"
                                    "• Anti-scraping protection\n\n"
                                    "Please check the URL and try again."
                                )
                    except:
                        pass
                else:
                    error_msg += (
                        "**Possible reasons:**\n"
                        "• Invalid URL format\n"
                        "• Site blocked by firewall\n"
                        "• Server not responding\n\n"
                        "Please check the URL and try again."
                    )
                
                await status_message.edit_text(error_msg, parse_mode=ParseMode.MARKDOWN)
                return
            
            # Update: Processing
            await status_message.edit_text(
                f"✅ **Scraping completed!**\n\n"
                f"📊 Processing data...\n"
                f"💾 Generating CSV...\n"
                f"📄 Creating PDF report...\n\n"
                f"⏳ Almost done...",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Get data
            data = scraper.get_data()
            metadata = scraper.get_metadata()
            structure_info = scraper.get_structure_analysis()
            
            # Save CSV
            csv_file = scraper.save_to_csv()
            
            # Generate report
            report_gen = ReportGenerator(logger, scraper)
            report_file = report_gen.generate_report(csv_file)
            
            # Get stats
            stats = logger.get_stats()
            log_file = logger.get_log_file()
            
            # Update: Sending files
            await status_message.edit_text(
                f"📤 **Sending results...**\n\n"
                f"✅ {len(data)} items extracted\n"
                f"⏱ Duration: {stats['duration']:.2f}s\n\n"
                f"📦 Preparing files...",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Create summary
            patterns = structure_info['structure'].get('patterns', [])
            strategy = structure_info['strategy'].get('type', 'general')
            
            summary = f"""
✅ **Scraping Complete!**

🔗 **URL:** `{url}`
📊 **Domain:** {metadata.get('domain', 'N/A')}
📄 **Title:** {metadata.get('title', 'N/A')[:50]}...

📈 **Results:**
• Items extracted: {len(data)}
• Duration: {stats['duration']:.2f} seconds
• Pages scraped: {stats['pages_scraped']}

🧠 **AI Analysis:**
• Detected patterns: {', '.join(patterns) if patterns else 'general webpage'}
• Strategy used: {strategy}
• AI provider: {'Gemini (FREE)' if Config.GEMINI_API_KEY else 'Traditional'}

📦 **Files:**
"""
            
            await status_message.edit_text(summary, parse_mode=ParseMode.MARKDOWN)
            
            # Send CSV file
            if csv_file and os.path.exists(csv_file):
                with open(csv_file, 'rb') as f:
                    await message.reply_document(
                        document=f,
                        filename=os.path.basename(csv_file),
                        caption="📊 **CSV Data File**\nExtracted data in spreadsheet format"
                    )
            
            # Send PDF report
            if report_file and os.path.exists(report_file):
                with open(report_file, 'rb') as f:
                    await message.reply_document(
                        document=f,
                        filename=os.path.basename(report_file),
                        caption="📄 **PDF Report**\nDetailed analysis and statistics"
                    )
            
            # Send log file
            if log_file and os.path.exists(log_file):
                with open(log_file, 'rb') as f:
                    await message.reply_document(
                        document=f,
                        filename=os.path.basename(log_file),
                        caption="📋 **Log File**\nDetailed scraping activity log"
                    )
            
            # Final message with options
            keyboard = [
                [InlineKeyboardButton("🔄 Scrape Another", callback_data='scrape_new')],
                [InlineKeyboardButton("📊 View Stats", callback_data='view_stats')],
                [InlineKeyboardButton("❓ Help", callback_data='show_help')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await message.reply_text(
                "🎉 **All done!** What would you like to do next?",
                reply_markup=reply_markup
            )
            
        except Exception as e:
            error_msg = f"❌ **Error occurred!**\n\n`{str(e)}`\n\nPlease try again or contact support."
            await status_message.edit_text(error_msg, parse_mode=ParseMode.MARKDOWN)
    
    async def process_twitter_scraping(self, update: Update, url: str, status_message, logger):
        """Process Twitter/X media scraping"""
        message = update.message or update.edited_message
        
        try:
            # Update: Twitter mode
            await status_message.edit_text(
                f"🐦 **Twitter Media Scraper (AUTHENTICATED)**\n\n"
                f"🔗 URL: `{url}`\n\n"
                f"� Using browser cookies for authentication...\n"
                f"📡 Accessing Twitter with your session...\n"
                f"⏳ This may take 30-60 seconds...",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Create Twitter scraper - Gallery-DL with authentication
            logger.info("🎯 Using Gallery-DL with Firefox cookies (authenticated)")
            twitter_scraper = TwitterGalleryDLScraperAuth(logger, use_browser='firefox')
            media_items = twitter_scraper.scrape_twitter_media(url, download=True)
            
            if not media_items:
                error_msg = (
                    f"❌ **No media found!**\n\n"
                    f"🔗 URL: `{url}`\n\n"
                    f"**Possible reasons:**\n"
                    f"• Tweet has no images/videos\n"
                    f"• Tweet is deleted or private\n"
                    f"• Authentication failed (cookies expired)\n"
                    f"• Twitter blocked the request\n\n"
                    f"💡 **To fix authentication:**\n"
                    f"1. Open Firefox on the server\n"
                    f"2. Log in to Twitter (twitter.com)\n"
                    f"3. Keep Firefox open\n"
                    f"4. Try again\n\n"
                    f"Or check `TWITTER_COOKIES_GUIDE.md` for alternatives\n\n"
                    f"💡 **Other solutions:**\n"
                    f"• Make sure the tweet exists and is public\n"
                    f"• Check if tweet has media attached\n"
                    f"• Try again in a few minutes"
                )
                
                await status_message.edit_text(error_msg, parse_mode=ParseMode.MARKDOWN)
                
                # Close driver
                if hasattr(twitter_scraper, 'close'):
                    twitter_scraper.close()
                return
            
            # Update: Processing
            await status_message.edit_text(
                f"✅ **Media extracted!**\n\n"
                f"📊 Found {len(media_items)} items\n"
                f"📥 Downloaded files\n\n"
                f"⏳ Preparing files...",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Save media list to CSV
            csv_file = twitter_scraper.save_to_csv()
            download_dir = twitter_scraper.get_download_directory()
            
            # Count by type
            images = [m for m in media_items if m['type'] == 'image']
            videos = [m for m in media_items if m['type'] == 'video']
            
            # Send summary
            summary = (
                f"🎉 **Twitter Media Extracted!**\n\n"
                f"📊 **Results:**\n"
                f"🖼 Images: {len(images)}\n"
                f"🎥 Videos: {len(videos)}\n"
                f"📦 Total: {len(media_items)}\n\n"
                f"📂 Files downloaded to:\n`{download_dir}`\n\n"
                f"📋 Sending files..."
            )
            await status_message.edit_text(summary, parse_mode=ParseMode.MARKDOWN)
            
            # Send CSV file
            if csv_file and os.path.exists(csv_file):
                with open(csv_file, 'rb') as f:
                    await message.reply_document(
                        document=f,
                        filename=os.path.basename(csv_file),
                        caption="📊 **Media List CSV**\nAll media URLs and local paths"
                    )
            
            # Send media files (limit to first 10 to avoid flooding)
            sent_count = 0
            max_send = 10
            
            for item in media_items[:max_send]:
                if item.get('status') == 'downloaded' and item.get('local_path'):
                    filepath = item['local_path']
                    if os.path.exists(filepath):
                        try:
                            with open(filepath, 'rb') as f:
                                if item['type'] == 'image':
                                    await message.reply_photo(
                                        photo=f,
                                        caption=f"🖼 {item['filename']}"
                                    )
                                elif item['type'] == 'video':
                                    await message.reply_video(
                                        video=f,
                                        caption=f"🎥 {item['filename']}"
                                    )
                            sent_count += 1
                        except Exception as e:
                            logger.error(f"Failed to send {filepath}: {str(e)}")
            
            # Final message
            final_msg = (
                f"✅ **Complete!**\n\n"
                f"📤 Sent {sent_count} media files\n"
            )
            
            if len(media_items) > max_send:
                final_msg += f"\n⚠️ Only showing first {max_send} of {len(media_items)} files\n"
                final_msg += f"📂 All files saved in:\n`{download_dir}`\n"
            
            final_msg += f"\n💡 Check the CSV for all media URLs"
            
            await message.reply_text(final_msg, parse_mode=ParseMode.MARKDOWN)
            
            # Close driver
            if hasattr(twitter_scraper, 'close'):
                twitter_scraper.close()
            
        except Exception as e:
            logger.error(f"Twitter scraping error: {str(e)}")
            import traceback
            logger.debug(traceback.format_exc())
            
            await status_message.edit_text(
                f"❌ **Twitter scraping failed!**\n\n"
                f"`{str(e)}`\n\n"
                f"💡 This might be because:\n"
                f"• Gallery-dl not found or not working\n"
                f"• Firefox not open or cookies unavailable\n"
                f"• Tweet is private or deleted\n"
                f"• Network connectivity issues\n\n"
                f"📖 See `TWITTER_COOKIES_GUIDE.md` for setup help\n\n"
                f"Try a different tweet or try again later.",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Close driver
            try:
                if hasattr(twitter_scraper, 'close'):
                    twitter_scraper.close()
            except:
                pass
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'scrape_new':
            await query.message.reply_text(
                "🔗 Send me a new URL to scrape!\n\nExample: `https://example.com`",
                parse_mode=ParseMode.MARKDOWN
            )
        elif query.data == 'view_stats':
            await query.message.reply_text(
                "📊 **Your Statistics**\n\nFeature coming soon!",
                parse_mode=ParseMode.MARKDOWN
            )
        elif query.data == 'show_help':
            await self.help_command(query, context)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        print(f"Update {update} caused error {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again later."
            )
    
    def run(self):
        """Run the bot"""
        print("=" * 60)
        print("🤖 UNIVERSAL WEB SCRAPER TELEGRAM BOT")
        print("=" * 60)
        print("\n✅ Starting bot...")
        
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Register handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("scrape", self.scrape_command))
        
        # Handle both new and edited messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.UpdateType.EDITED_MESSAGE, self.handle_message))
        
        application.add_handler(CallbackQueryHandler(self.button_handler))
        application.add_error_handler(self.error_handler)
        
        print("✅ Bot is ready!")
        print("\nBot Commands:")
        print("  /start - Welcome message")
        print("  /help - Help information")
        print("  /scrape <URL> - Scrape a website")
        print("\nOr just send any URL directly!")
        print("\n" + "=" * 60)
        print("🚀 Bot is running... Press Ctrl+C to stop")
        print("=" * 60 + "\n")
        
        # Run bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    bot = ScraperBot()
    bot.run()

if __name__ == '__main__':
    main()
