"""
Multi-Language Support Module
Supports English and Arabic languages
"""

class LanguageSupport:
    """
    Language translations for English and Arabic
    """
    
    TRANSLATIONS = {
        'en': {
            # Bot messages
            'welcome': '🤖 Universal Web Scraper Bot',
            'welcome_desc': 'Welcome! I can scrape any website and extract data for you.',
            'how_to_use': '🚀 How to Use:',
            'just_send_url': 'Just send me any URL - no commands needed!',
            'examples': 'Examples:',
            'features': '✨ Features:',
            'commands': '📋 Optional Commands:',
            'supported': '🎯 Supported:',
            'try_now': 'Try it now! Just paste a URL 👇',
            
            # Scraping messages
            'starting_scrape': '🚀 Starting scrape...',
            'url': '🔗 URL',
            'user': '👤 User',
            'mode': '🔧 Mode',
            'please_wait': '⏳ Please wait...',
            'initializing': '🔧 Initializing scraper...',
            'loading_page': '⏳ Loading page...',
            'scraping_progress': '🔍 Scraping in progress...',
            'analyzing_structure': '📊 Analyzing structure...',
            'extracting_data': '🤖 Extracting data...',
            'this_may_take': '⏳ This may take 30-60 seconds...',
            
            # Twitter messages
            'twitter_scraper': '🐦 Twitter Media Scraper',
            'twitter_auth': '🐦 Twitter Media Scraper (AUTHENTICATED)',
            'using_cookies': '🔐 Using browser cookies for authentication...',
            'accessing_twitter': '📡 Accessing Twitter with your session...',
            'extracting_media': '📡 Extracting and downloading media...',
            
            # Success messages
            'scraping_complete': '✅ Scraping Complete!',
            'media_extracted': '✅ Media extracted!',
            'twitter_complete': '🎉 Twitter Media Extracted!',
            'processing_data': '📊 Processing data...',
            'generating_csv': '💾 Generating CSV...',
            'creating_pdf': '📄 Creating PDF report...',
            'almost_done': '⏳ Almost done...',
            'sending_results': '📤 Sending results...',
            
            # Results
            'results': '📈 Results:',
            'items_extracted': 'Items extracted',
            'duration': 'Duration',
            'pages_scraped': 'Pages scraped',
            'images': '🖼 Images',
            'videos': '🎥 Videos',
            'total': '📦 Total',
            'files': '📦 Files:',
            
            # Error messages
            'error_occurred': '❌ Error occurred!',
            'scraping_failed': '❌ Scraping failed!',
            'no_media_found': '❌ No media found!',
            'possible_reasons': '**Possible reasons:**',
            'tweet_no_media': '• Tweet has no images/videos',
            'tweet_deleted': '• Tweet is deleted or private',
            'auth_failed': '• Authentication failed (cookies expired)',
            'twitter_blocked': '• Twitter blocked the request',
            'to_fix_auth': '💡 To fix authentication:',
            'open_firefox': '1. Open Firefox on the server',
            'login_twitter': '2. Log in to Twitter (twitter.com)',
            'keep_firefox_open': '3. Keep Firefox open',
            'try_again': '4. Try again',
            
            # Help
            'help_title': '📖 How to Use This Bot',
            'quick_method': '⚡ Quick Method (Recommended):',
            'just_paste': 'Just paste any URL - bot auto-detects and scrapes!',
            'command_method': '📋 Command Method (Optional):',
            'what_you_get': '📊 What You Get:',
            'csv_file': '✅ CSV file with extracted data',
            'pdf_report': '✅ PDF report with statistics',
            'log_file': '✅ Detailed log file',
            'twitter_downloads': '✅ For Twitter: Images & Videos downloaded!',
            
            # Other
            'domain': '📊 Domain',
            'title': '📄 Title',
            'ai_analysis': '🧠 AI Analysis',
            'detected_patterns': 'Detected patterns',
            'strategy_used': 'Strategy used',
            'ai_provider': 'AI provider',
            'send_url': '🔗 Send me a new URL to scrape!',
            'invalid_url': '❓ Please send a valid URL starting with http:// or https://',
        },
        
        'ar': {
            # Bot messages
            'welcome': '🤖 بوت استخراج البيانات الشامل',
            'welcome_desc': 'مرحباً! يمكنني استخراج البيانات من أي موقع ويب لك.',
            'how_to_use': '🚀 كيفية الاستخدام:',
            'just_send_url': 'فقط أرسل لي أي رابط - لا حاجة للأوامر!',
            'examples': 'أمثلة:',
            'features': '✨ المميزات:',
            'commands': '📋 أوامر اختيارية:',
            'supported': '🎯 المدعوم:',
            'try_now': 'جربه الآن! فقط الصق رابط 👇',
            
            # Scraping messages
            'starting_scrape': '🚀 بدء الاستخراج...',
            'url': '🔗 الرابط',
            'user': '👤 المستخدم',
            'mode': '🔧 الوضع',
            'please_wait': '⏳ يرجى الانتظار...',
            'initializing': '🔧 تهيئة أداة الاستخراج...',
            'loading_page': '⏳ تحميل الصفحة...',
            'scraping_progress': '🔍 جارٍ الاستخراج...',
            'analyzing_structure': '📊 تحليل البنية...',
            'extracting_data': '🤖 استخراج البيانات...',
            'this_may_take': '⏳ قد يستغرق هذا 30-60 ثانية...',
            
            # Twitter messages
            'twitter_scraper': '🐦 مستخرج وسائط تويتر',
            'twitter_auth': '🐦 مستخرج وسائط تويتر (مصادق)',
            'using_cookies': '🔐 استخدام ملفات تعريف الارتباط للمصادقة...',
            'accessing_twitter': '📡 الوصول إلى تويتر باستخدام جلستك...',
            'extracting_media': '📡 استخراج وتحميل الوسائط...',
            
            # Success messages
            'scraping_complete': '✅ اكتمل الاستخراج!',
            'media_extracted': '✅ تم استخراج الوسائط!',
            'twitter_complete': '🎉 تم استخراج وسائط تويتر!',
            'processing_data': '📊 معالجة البيانات...',
            'generating_csv': '💾 إنشاء ملف CSV...',
            'creating_pdf': '📄 إنشاء تقرير PDF...',
            'almost_done': '⏳ على وشك الانتهاء...',
            'sending_results': '📤 إرسال النتائج...',
            
            # Results
            'results': '📈 النتائج:',
            'items_extracted': 'العناصر المستخرجة',
            'duration': 'المدة',
            'pages_scraped': 'الصفحات المستخرجة',
            'images': '🖼 الصور',
            'videos': '🎥 الفيديوهات',
            'total': '📦 المجموع',
            'files': '📦 الملفات:',
            
            # Error messages
            'error_occurred': '❌ حدث خطأ!',
            'scraping_failed': '❌ فشل الاستخراج!',
            'no_media_found': '❌ لم يتم العثور على وسائط!',
            'possible_reasons': '**الأسباب المحتملة:**',
            'tweet_no_media': '• التغريدة لا تحتوي على صور/فيديوهات',
            'tweet_deleted': '• التغريدة محذوفة أو خاصة',
            'auth_failed': '• فشلت المصادقة (انتهت صلاحية ملفات تعريف الارتباط)',
            'twitter_blocked': '• تويتر حظر الطلب',
            'to_fix_auth': '💡 لإصلاح المصادقة:',
            'open_firefox': '1. افتح فايرفوكس على الخادم',
            'login_twitter': '2. سجل الدخول إلى تويتر (twitter.com)',
            'keep_firefox_open': '3. أبق فايرفوكس مفتوحاً',
            'try_again': '4. حاول مرة أخرى',
            
            # Help
            'help_title': '📖 كيفية استخدام هذا البوت',
            'quick_method': '⚡ الطريقة السريعة (موصى بها):',
            'just_paste': 'فقط الصق أي رابط - البوت يكتشف تلقائياً ويستخرج!',
            'command_method': '📋 طريقة الأوامر (اختيارية):',
            'what_you_get': '📊 ما ستحصل عليه:',
            'csv_file': '✅ ملف CSV مع البيانات المستخرجة',
            'pdf_report': '✅ تقرير PDF مع الإحصائيات',
            'log_file': '✅ ملف سجل مفصل',
            'twitter_downloads': '✅ لتويتر: تحميل الصور والفيديوهات!',
            
            # Other
            'domain': '📊 النطاق',
            'title': '📄 العنوان',
            'ai_analysis': '🧠 تحليل الذكاء الاصطناعي',
            'detected_patterns': 'الأنماط المكتشفة',
            'strategy_used': 'الاستراتيجية المستخدمة',
            'ai_provider': 'مزود الذكاء الاصطناعي',
            'send_url': '🔗 أرسل لي رابط جديد للاستخراج!',
            'invalid_url': '❓ يرجى إرسال رابط صالح يبدأ بـ http:// أو https://',
        }
    }
    
    @staticmethod
    def get_text(key, lang='en'):
        """
        Get translated text for a key
        
        Args:
            key: Translation key
            lang: Language code ('en' or 'ar')
        
        Returns:
            Translated text or key if not found
        """
        return LanguageSupport.TRANSLATIONS.get(lang, {}).get(key, key)
    
    @staticmethod
    def detect_language(text):
        """
        Detect if text contains Arabic characters
        
        Args:
            text: Text to check
        
        Returns:
            'ar' if Arabic detected, 'en' otherwise
        """
        if not text:
            return 'en'
        
        # Check for Arabic Unicode range
        arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        
        # If more than 20% Arabic characters, consider it Arabic
        if arabic_chars > len(text) * 0.2:
            return 'ar'
        
        return 'en'
    
    @staticmethod
    def format_message(template, lang='en', **kwargs):
        """
        Format a message with variables
        
        Args:
            template: Translation key
            lang: Language code
            **kwargs: Variables to format
        
        Returns:
            Formatted message
        """
        text = LanguageSupport.get_text(template, lang)
        
        try:
            return text.format(**kwargs)
        except:
            return text
    
    @staticmethod
    def is_rtl(lang):
        """
        Check if language is Right-to-Left
        
        Args:
            lang: Language code
        
        Returns:
            True if RTL, False otherwise
        """
        return lang == 'ar'


# Convenience function
def t(key, lang='en'):
    """
    Quick translation function
    
    Args:
        key: Translation key
        lang: Language code ('en' or 'ar')
    
    Returns:
        Translated text
    """
    return LanguageSupport.get_text(key, lang)


# Export
__all__ = ['LanguageSupport', 't']
