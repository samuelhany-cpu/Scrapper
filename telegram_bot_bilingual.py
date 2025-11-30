"""
BILINGUAL TELEGRAM BOT - English & Arabic Support
Updated to support both English and Arabic languages
"""
import os
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

from src.config import Config
from src.logger import ScraperLogger
from src.adaptive_scraper import AdaptiveSmartScraper
from src.report_generator import ReportGenerator
from src.language import LanguageSupport, t

# Bot Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

class BilingualScraperBot:
    def __init__(self):
        self.active_tasks = {}
        self.user_languages = {}  # Store user language preferences
        Config.ensure_directories()
    
    def get_user_language(self, update: Update):
        """Get user's preferred language - auto-detect from Telegram or message"""
        user_id = update.effective_user.id
        
        # Check stored preference
        if user_id in self.user_languages:
            return self.user_languages[user_id]
        
        # Try Telegram language settings
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
    
    def set_user_language(self, user_id, lang):
        """Set user's language preference"""
        self.user_languages[user_id] = lang
    
    async def lang_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /lang command - switch language"""
        message = update.message or update.edited_message
        if not message:
            return
        
        user_id = update.effective_user.id
        current_lang = self.get_user_language(update)
        
        # Toggle language
        new_lang = 'ar' if current_lang == 'en' else 'en'
        self.set_user_language(user_id, new_lang)
        
        if new_lang == 'ar':
            response = """
✅ **تم تغيير اللغة إلى العربية**

الآن جميع الرسائل ستكون بالعربية.

لتغيير اللغة مرة أخرى، استخدم: /lang
            """
        else:
            response = """
✅ **Language changed to English**

All messages will now be in English.

To change language again, use: /lang
            """
        
        await message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        message = update.message or update.edited_message
        if not message:
            return
        
        lang = self.get_user_language(update)
        
        if lang == 'ar':
            welcome = """
🤖 **بوت استخراج البيانات الشامل**

مرحباً! يمكنني استخراج البيانات من أي موقع ويب لك.

**🚀 كيفية الاستخدام:**
فقط أرسل لي أي رابط - لا حاجة للأوامر!

**أمثلة:**
`https://example.com`
`https://twitter.com/username/status/123`
`https://ar.wikipedia.org/wiki/استخراج_البيانات`

**✨ المميزات:**
• 🌐 مستخرج ويب شامل (أي موقع)
• 🐦 مُنزِّل وسائط تويتر (مصادق)
• 🤖 استخراج بالذكاء الاصطناعي (Gemini مجاناً)
• 📊 تصدير بيانات CSV
• 📄 تقارير PDF
• 📋 سجلات مفصلة
• 🌍 يدعم العربية والإنجليزية

**📋 أوامر اختيارية:**
/start - عرض هذه الرسالة
/scrape <رابط> - طريقة بديلة للاستخراج
/help - مساعدة مفصلة
/lang - تغيير اللغة (English/العربية)
/stats - عرض الإحصائيات

**🎯 المدعوم:**
✅ مواقع الأخبار، المدونات، ويكيبيديا
✅ التجارة الإلكترونية، صفحات المنتجات
✅ صور وفيديوهات تويتر/X
✅ الجداول، القوائم، المقالات
✅ أي موقع عام!

جربه الآن! فقط الصق رابط 👇
            """
        else:
            welcome = """
🤖 **Universal Web Scraper Bot**

Welcome! I can scrape any website and extract data for you.

**🚀 How to Use:**
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
• 🌍 Supports English & Arabic

**📋 Optional Commands:**
/start - Show this message
/scrape <URL> - Alternative way to scrape
/help - Detailed help
/lang - Change language (English/العربية)
/stats - View statistics

**🎯 Supported:**
✅ News sites, blogs, Wikipedia
✅ E-commerce, product pages
✅ Twitter/X images & videos
✅ Tables, lists, articles
✅ Any public website!

Try it now! Just paste a URL 👇
            """
        
        await message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        message = update.message or update.edited_message
        if not message:
            return
        
        lang = self.get_user_language(update)
        
        if lang == 'ar':
            help_text = """
📖 **كيفية استخدام هذا البوت**

**⚡ الطريقة السريعة (موصى بها):**
فقط الصق أي رابط - البوت يكتشف تلقائياً ويستخرج!
`https://example.com`

**📋 طريقة الأوامر (اختيارية):**
`/scrape https://example.com`

**📊 ما ستحصل عليه:**
✅ ملف CSV مع البيانات المستخرجة
✅ تقرير PDF مع الإحصائيات
✅ ملف سجل مفصل
✅ لتويتر: تحميل الصور والفيديوهات!

**🐦 مميزات خاصة لتويتر/X:**
• 🔐 استخراج مصادق (يستخدم ملفات تعريف ارتباط المتصفح)
• 🖼 تحميل جميع الصور
• 🎥 تحميل جميع الفيديوهات
• 📱 يعمل مع التغريدات العامة والخاصة (إذا كنت تتابعها)
• 🚫 بلا حدود API!

**🎯 المواقع المدعومة:**
• التجارة الإلكترونية (أمازون، إيباي، إلخ.)
• مواقع الأخبار والمدونات
• ويكيبيديا والتوثيق
• وسائط تويتر/X (صور/فيديوهات)
• قوائم المنتجات والجداول
• أي موقع عام!

**🤖 الميزات الذكية:**
• كشف تلقائي لنوع الموقع
• تكييف استراتيجية الاستخراج
• يستخدم ذكاء اصطناعي مجاني (Gemini)
• يتعامل مع مواقع JavaScript
• يستخرج الجداول، القوائم، المقالات

**⚡ أمثلة:**
`https://ar.wikipedia.org/wiki/استخراج_البيانات`
`https://twitter.com/username/status/123`
`https://quotes.toscrape.com`

**🌍 تغيير اللغة:**
استخدم `/lang` للتبديل بين العربية والإنجليزية

**❓ تحتاج مساعدة؟**
فقط أرسل رابط وسأستخرج البيانات لك!
            """
        else:
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
`https://twitter.com/username/status/123`
`https://quotes.toscrape.com`

**🌍 Change Language:**
Use `/lang` to switch between English and Arabic

**❓ Need Help?**
Just send a URL and I'll scrape it for you!
            """
        
        await message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def scrape_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /scrape command"""
        message = update.message or update.edited_message
        if not message:
            return
        
        lang = self.get_user_language(update)
        
        if not context.args:
            if lang == 'ar':
                await message.reply_text(
                    "❌ يرجى تقديم رابط!\n\nالاستخدام: `/scrape https://example.com`",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await message.reply_text(
                    "❌ Please provide a URL!\n\nUsage: `/scrape https://example.com`",
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        url = context.args[0]
        await self.process_scraping(update, url)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle plain text messages (URLs)"""
        message = update.message or update.edited_message
        if not message:
            return
        
        text = message.text.strip()
        lang = self.get_user_language(update)
        
        # Check if it's a URL
        if text.startswith('http://') or text.startswith('https://'):
            await self.process_scraping(update, text)
        else:
            if lang == 'ar':
                await message.reply_text(
                    "❓ يرجى إرسال رابط صالح يبدأ بـ http:// أو https://\n\n"
                    "مثال: `https://example.com`\n\n"
                    "أو استخدم /help لمزيد من المعلومات.",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await message.reply_text(
                    "❓ Please send a valid URL starting with http:// or https://\n\n"
                    "Example: `https://example.com`\n\n"
                    "Or use /help for more information.",
                    parse_mode=ParseMode.MARKDOWN
                )
    
    async def process_scraping(self, update: Update, url: str):
        """Process scraping request with bilingual support"""
        message = update.message or update.edited_message
        if not message:
            return
        
        user_id = update.effective_user.id
        username = update.effective_user.username or update.effective_user.first_name
        lang = self.get_user_language(update)
        
        # Check if Twitter URL
        is_twitter = 'twitter.com' in url or 'x.com' in url
        
        # Bilingual initial message
        if lang == 'ar':
            scraper_type = "🐦 مستخرج وسائط تويتر" if is_twitter else "🌐 مستخرج شامل"
            status_message = await message.reply_text(
                f"🚀 **بدء الاستخراج...**\n\n"
                f"🔗 الرابط: `{url}`\n"
                f"👤 المستخدم: {username}\n"
                f"🔧 الوضع: {scraper_type}\n\n"
                f"⏳ يرجى الانتظار...",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
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
            session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            logger = ScraperLogger(session_id)
            
            # Use Twitter scraper for Twitter URLs
            if is_twitter:
                await self.process_twitter_scraping_bilingual(update, url, status_message, logger, lang)
                return
            
            # Update: Initializing
            if lang == 'ar':
                await status_message.edit_text(
                    f"🔧 **تهيئة المستخرج...**\n\n"
                    f"🔗 الرابط: `{url}`\n"
                    f"🤖 استخدام الذكاء الاصطناعي + استراتيجية تكيفية\n\n"
                    f"⏳ تحميل الصفحة...",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await status_message.edit_text(
                    f"🔧 **Initializing scraper...**\n\n"
                    f"🔗 URL: `{url}`\n"
                    f"🤖 Using AI + Adaptive Strategy\n\n"
                    f"⏳ Loading page...",
                    parse_mode=ParseMode.MARKDOWN
                )
            
            # Create scraper
            scraper = AdaptiveSmartScraper(logger)
            
            # Update: Scraping
            if lang == 'ar':
                await status_message.edit_text(
                    f"🔍 **جارٍ الاستخراج...**\n\n"
                    f"🔗 الرابط: `{url}`\n"
                    f"📊 تحليل البنية...\n"
                    f"🤖 استخراج البيانات...\n\n"
                    f"⏳ قد يستغرق هذا 30-60 ثانية...",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
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
                if lang == 'ar':
                    error_msg = f"❌ **فشل الاستخراج!**\n\n🔗 الرابط: `{url}`\n\n"
                    error_msg += "**الأسباب المحتملة:**\n"
                    error_msg += "• تنسيق رابط غير صالح\n"
                    error_msg += "• الموقع محظور بواسطة جدار الحماية\n"
                    error_msg += "• الخادم لا يستجيب\n"
                    error_msg += "• حماية ضد الاستخراج\n\n"
                    error_msg += "يرجى التحقق من الرابط والمحاولة مرة أخرى."
                else:
                    error_msg = f"❌ **Scraping failed!**\n\n🔗 URL: `{url}`\n\n"
                    error_msg += "**Possible reasons:**\n"
                    error_msg += "• Invalid URL format\n"
                    error_msg += "• Site blocked by firewall\n"
                    error_msg += "• Server not responding\n"
                    error_msg += "• Anti-scraping protection\n\n"
                    error_msg += "Please check the URL and try again."
                
                await status_message.edit_text(error_msg, parse_mode=ParseMode.MARKDOWN)
                return
            
            # Success - process results
            data = scraper.get_data()
            metadata = scraper.get_metadata()
            structure_info = scraper.get_structure_analysis()
            csv_file = scraper.save_to_csv()
            report_gen = ReportGenerator(logger, scraper)
            report_file = report_gen.generate_report(csv_file)
            stats = logger.get_stats()
            log_file = logger.get_log_file()
            
            # Create summary
            patterns = structure_info['structure'].get('patterns', [])
            strategy = structure_info['strategy'].get('type', 'general')
            
            if lang == 'ar':
                summary = f"""
✅ **اكتمل الاستخراج!**

🔗 **الرابط:** `{url}`
📊 **النطاق:** {metadata.get('domain', 'غير متوفر')}
📄 **العنوان:** {metadata.get('title', 'غير متوفر')[:50]}...

📈 **النتائج:**
• العناصر المستخرجة: {len(data)}
• المدة: {stats['duration']:.2f} ثانية
• الصفحات المستخرجة: {stats['pages_scraped']}

🧠 **تحليل الذكاء الاصطناعي:**
• الأنماط المكتشفة: {', '.join(patterns) if patterns else 'صفحة ويب عامة'}
• الاستراتيجية المستخدمة: {strategy}
• مزود الذكاء الاصطناعي: {'Gemini (مجاناً)' if Config.GEMINI_API_KEY else 'تقليدي'}

📦 **الملفات:**
"""
            else:
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
            
            # Send files
            caption_csv = "📊 **ملف بيانات CSV**\nالبيانات المستخرجة بصيغة جدول" if lang == 'ar' else "📊 **CSV Data File**\nExtracted data in spreadsheet format"
            caption_pdf = "📄 **تقرير PDF**\nتحليل مفصل وإحصائيات" if lang == 'ar' else "📄 **PDF Report**\nDetailed analysis and statistics"
            caption_log = "📋 **ملف السجل**\nسجل نشاط الاستخراج المفصل" if lang == 'ar' else "📋 **Log File**\nDetailed scraping activity log"
            
            if csv_file and os.path.exists(csv_file):
                with open(csv_file, 'rb') as f:
                    await message.reply_document(document=f, filename=os.path.basename(csv_file), caption=caption_csv)
            
            if report_file and os.path.exists(report_file):
                with open(report_file, 'rb') as f:
                    await message.reply_document(document=f, filename=os.path.basename(report_file), caption=caption_pdf)
            
            if log_file and os.path.exists(log_file):
                with open(log_file, 'rb') as f:
                    await message.reply_document(document=f, filename=os.path.basename(log_file), caption=caption_log)
            
            # Final message
            final_msg = "🎉 **تم!** ماذا تريد أن تفعل بعد ذلك?" if lang == 'ar' else "🎉 **All done!** What would you like to do next?"
            await message.reply_text(final_msg, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            if lang == 'ar':
                error_msg = f"❌ **حدث خطأ!**\n\n`{str(e)}`\n\nيرجى المحاولة مرة أخرى أو الاتصال بالدعم."
            else:
                error_msg = f"❌ **Error occurred!**\n\n`{str(e)}`\n\nPlease try again or contact support."
            await status_message.edit_text(error_msg, parse_mode=ParseMode.MARKDOWN)
    
    async def process_twitter_scraping_bilingual(self, update: Update, url: str, status_message, logger, lang):
        """Process Twitter scraping with bilingual support"""
        message = update.message or update.edited_message
        
        try:
            # Update status
            if lang == 'ar':
                await status_message.edit_text(
                    f"🐦 **مستخرج وسائط تويتر (مصادق)**\n\n"
                    f"🔗 الرابط: `{url}`\n\n"
                    f"🔐 استخدام ملفات تعريف ارتباط المتصفح للمصادقة...\n"
                    f"📡 الوصول إلى تويتر باستخدام جلستك...\n"
                    f"⏳ قد يستغرق هذا 30-60 ثانية...",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await status_message.edit_text(
                    f"🐦 **Twitter Media Scraper (AUTHENTICATED)**\n\n"
                    f"🔗 URL: `{url}`\n\n"
                    f"🔐 Using browser cookies for authentication...\n"
                    f"📡 Accessing Twitter with your session...\n"
                    f"⏳ This may take 30-60 seconds...",
                    parse_mode=ParseMode.MARKDOWN
                )
            
            # Create Twitter scraper
            logger.info("🎯 Using Gallery-DL with Firefox cookies (authenticated)")
            twitter_scraper = TwitterGalleryDLScraperAuth(logger, use_browser='firefox')
            media_items = twitter_scraper.scrape_twitter_media(url, download=True)
            
            if not media_items:
                if lang == 'ar':
                    error_msg = (
                        f"❌ **لم يتم العثور على وسائط!**\n\n"
                        f"🔗 الرابط: `{url}`\n\n"
                        f"**الأسباب المحتملة:**\n"
                        f"• التغريدة لا تحتوي على صور/فيديوهات\n"
                        f"• التغريدة محذوفة أو خاصة\n"
                        f"• فشلت المصادقة (انتهت صلاحية ملفات تعريف الارتباط)\n"
                        f"• تويتر حظر الطلب\n\n"
                        f"💡 **لإصلاح المصادقة:**\n"
                        f"1. افتح فايرفوكس على الخادم\n"
                        f"2. سجل الدخول إلى تويتر (twitter.com)\n"
                        f"3. أبق فايرفوكس مفتوحاً\n"
                        f"4. حاول مرة أخرى\n\n"
                        f"أو راجع `TWITTER_COOKIES_GUIDE.md` للبدائل"
                    )
                else:
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
                        f"Or check `TWITTER_COOKIES_GUIDE.md` for alternatives"
                    )
                
                await status_message.edit_text(error_msg, parse_mode=ParseMode.MARKDOWN)
                
                if hasattr(twitter_scraper, 'close'):
                    twitter_scraper.close()
                return
            
            # Success - send media
            csv_file = twitter_scraper.save_to_csv()
            download_dir = twitter_scraper.get_download_directory()
            
            images = [m for m in media_items if m['type'] == 'image']
            videos = [m for m in media_items if m['type'] == 'video']
            
            if lang == 'ar':
                summary = (
                    f"🎉 **تم استخراج وسائط تويتر!**\n\n"
                    f"📊 **النتائج:**\n"
                    f"🖼 الصور: {len(images)}\n"
                    f"🎥 الفيديوهات: {len(videos)}\n"
                    f"📦 المجموع: {len(media_items)}\n\n"
                    f"📂 تم تنزيل الملفات إلى:\n`{download_dir}`\n\n"
                    f"📋 إرسال الملفات..."
                )
            else:
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
            
            # Send CSV
            if csv_file and os.path.exists(csv_file):
                caption = "📊 **قائمة الوسائط CSV**\nجميع روابط الوسائط والمسارات المحلية" if lang == 'ar' else "📊 **Media List CSV**\nAll media URLs and local paths"
                with open(csv_file, 'rb') as f:
                    await message.reply_document(document=f, filename=os.path.basename(csv_file), caption=caption)
            
            # Send media files (limit 10)
            sent_count = 0
            max_send = 10
            
            for item in media_items[:max_send]:
                if item.get('status') == 'downloaded' and item.get('local_path'):
                    filepath = item['local_path']
                    if os.path.exists(filepath):
                        try:
                            with open(filepath, 'rb') as f:
                                if item['type'] == 'image':
                                    await message.reply_photo(photo=f, caption=f"🖼 {item['filename']}")
                                elif item['type'] == 'video':
                                    await message.reply_video(video=f, caption=f"🎥 {item['filename']}")
                            sent_count += 1
                        except Exception as e:
                            logger.error(f"Failed to send {filepath}: {str(e)}")
            
            # Final message
            if lang == 'ar':
                final_msg = f"✅ **مكتمل!**\n\n📤 تم إرسال {sent_count} ملف وسائط\n"
                if len(media_items) > max_send:
                    final_msg += f"\n⚠️ عرض أول {max_send} من {len(media_items)} ملف فقط\n"
                    final_msg += f"📂 جميع الملفات محفوظة في:\n`{download_dir}`\n"
                final_msg += f"\n💡 راجع CSV لجميع روابط الوسائط"
            else:
                final_msg = f"✅ **Complete!**\n\n📤 Sent {sent_count} media files\n"
                if len(media_items) > max_send:
                    final_msg += f"\n⚠️ Only showing first {max_send} of {len(media_items)} files\n"
                    final_msg += f"📂 All files saved in:\n`{download_dir}`\n"
                final_msg += f"\n💡 Check the CSV for all media URLs"
            
            await message.reply_text(final_msg, parse_mode=ParseMode.MARKDOWN)
            
            if hasattr(twitter_scraper, 'close'):
                twitter_scraper.close()
            
        except Exception as e:
            logger.error(f"Twitter scraping error: {str(e)}")
            import traceback
            logger.debug(traceback.format_exc())
            
            if lang == 'ar':
                error_msg = (
                    f"❌ **فشل استخراج تويتر!**\n\n"
                    f"`{str(e)}`\n\n"
                    f"💡 قد يكون هذا بسبب:\n"
                    f"• Gallery-dl غير موجود أو لا يعمل\n"
                    f"• فايرفوكس غير مفتوح أو ملفات تعريف الارتباط غير متوفرة\n"
                    f"• التغريدة خاصة أو محذوفة\n"
                    f"• مشاكل اتصال الشبكة\n\n"
                    f"📖 راجع `TWITTER_COOKIES_GUIDE.md` للحصول على مساعدة الإعداد\n\n"
                    f"جرب تغريدة مختلفة أو حاول مرة أخرى لاحقاً."
                )
            else:
                error_msg = (
                    f"❌ **Twitter scraping failed!**\n\n"
                    f"`{str(e)}`\n\n"
                    f"💡 This might be because:\n"
                    f"• Gallery-dl not found or not working\n"
                    f"• Firefox not open or cookies unavailable\n"
                    f"• Tweet is private or deleted\n"
                    f"• Network connectivity issues\n\n"
                    f"📖 See `TWITTER_COOKIES_GUIDE.md` for setup help\n\n"
                    f"Try a different tweet or try again later."
                )
            
            await status_message.edit_text(error_msg, parse_mode=ParseMode.MARKDOWN)
            
            try:
                if hasattr(twitter_scraper, 'close'):
                    twitter_scraper.close()
            except:
                pass
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        print(f"Update {update} caused error {context.error}")
        if update and update.effective_message:
            lang = self.get_user_language(update)
            error_msg = "❌ حدث خطأ. يرجى المحاولة مرة أخرى لاحقاً." if lang == 'ar' else "❌ An error occurred. Please try again later."
            await update.effective_message.reply_text(error_msg)
    
    def run(self):
        """Run the bot"""
        print("=" * 60)
        print("🤖 BILINGUAL WEB SCRAPER BOT (English & Arabic)")
        print("🌍 بوت استخراج البيانات ثنائي اللغة (العربية والإنجليزية)")
        print("=" * 60)
        print("\n✅ Starting bot...")
        print("✅ جارٍ بدء البوت...")
        
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Register handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("scrape", self.scrape_command))
        application.add_handler(CommandHandler("lang", self.lang_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.UpdateType.EDITED_MESSAGE, self.handle_message))
        application.add_error_handler(self.error_handler)
        
        print("✅ Bot is ready! | البوت جاهز!")
        print("\nBot Commands | أوامر البوت:")
        print("  /start - Welcome | ترحيب")
        print("  /help - Help | مساعدة")
        print("  /scrape <URL> - Scrape | استخراج")
        print("  /lang - Change language | تغيير اللغة")
        print("\nOr just send any URL! | أو فقط أرسل أي رابط!")
        print("\n" + "=" * 60)
        print("🚀 Bot is running... | البوت يعمل...")
        print("Press Ctrl+C to stop | اضغط Ctrl+C للإيقاف")
        print("=" * 60 + "\n")
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    bot = BilingualScraperBot()
    bot.run()

if __name__ == '__main__':
    main()
