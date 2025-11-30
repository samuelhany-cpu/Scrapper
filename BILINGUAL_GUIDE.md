# 🌍 Bilingual Support - English & Arabic

## ✨ Complete Arabic & English Support Added!

Your scraper now fully supports **both Arabic and English** for:
- ✅ Bot messages and commands
- ✅ User input (URLs work in any language)
- ✅ Scraped data (preserves Arabic text)
- ✅ CSV exports (UTF-8 with BOM for Excel)
- ✅ PDF reports
- ✅ Logs and error messages

---

## 🚀 Quick Start

### Run Bilingual Bot:

```cmd
cd f:\Scrapper
.venv\Scripts\python telegram_bot_bilingual.py
```

**You'll see:**
```
============================================================
🤖 BILINGUAL WEB SCRAPER BOT (English & Arabic)
🌍 بوت استخراج البيانات ثنائي اللغة (العربية والإنجليزية)
============================================================

✅ Bot is ready! | البوت جاهز!

Bot Commands | أوامر البوت:
  /start - Welcome | ترحيب
  /help - Help | مساعدة
  /scrape <URL> - Scrape | استخراج
  /lang - Change language | تغيير اللغة

Or just send any URL! | أو فقط أرسل أي رابط!
============================================================
```

---

## 🌍 Language Detection

### Automatic Detection:

The bot automatically detects your language from:

1. **Telegram Settings**
   - If your Telegram language is Arabic → Bot uses Arabic
   - If your Telegram language is English → Bot uses English

2. **Message Content**
   - Detects Arabic characters in your messages
   - If 20%+ Arabic characters → Switches to Arabic

3. **Manual Override**
   - Use `/lang` command to switch languages anytime

---

## 📋 How It Works

### For English Users:

```
You: /start
Bot: 🤖 Universal Web Scraper Bot
     Welcome! I can scrape any website...
     
You: https://example.com
Bot: 🚀 Starting scrape...
     ✅ Scraping Complete!
     [sends files in English]
```

### For Arabic Users (المستخدمون العرب):

```
أنت: /start
البوت: 🤖 بوت استخراج البيانات الشامل
      مرحباً! يمكنني استخراج البيانات من أي موقع...
      
أنت: https://example.com
البوت: 🚀 بدء الاستخراج...
      ✅ اكتمل الاستخراج!
      [يرسل الملفات بالعربية]
```

---

## 🎯 Commands (الأوامر)

| Command | English | Arabic (العربية) |
|---------|---------|------------------|
| `/start` | Show welcome message | عرض رسالة الترحيب |
| `/help` | Show help information | عرض معلومات المساعدة |
| `/scrape <URL>` | Scrape a website | استخراج بيانات موقع |
| `/lang` | Switch language (EN/AR) | تغيير اللغة (إنجليزي/عربي) |
| `/stats` | View statistics | عرض الإحصائيات |

---

## 💡 Examples (أمثلة)

### English Example:

```
You: https://en.wikipedia.org/wiki/Web_scraping
Bot: 🚀 Starting scrape...
     🔧 Initializing scraper...
     🔍 Scraping in progress...
     ✅ Scraping Complete!
     
     📊 Results:
     • Items extracted: 42
     • Duration: 15.3 seconds
     
     [Sends CSV, PDF, logs in English]
```

### Arabic Example (مثال عربي):

```
أنت: https://ar.wikipedia.org/wiki/استخراج_البيانات
البوت: 🚀 بدء الاستخراج...
      🔧 تهيئة المستخرج...
      🔍 جارٍ الاستخراج...
      ✅ اكتمل الاستخراج!
      
      📊 النتائج:
      • العناصر المستخرجة: 42
      • المدة: 15.3 ثانية
      
      [يرسل CSV، PDF، سجلات بالعربية]
```

---

## 🐦 Twitter Example (مثال تويتر)

### English:

```
You: https://twitter.com/username/status/123
Bot: 🐦 Twitter Media Scraper (AUTHENTICATED)
     🔐 Using browser cookies for authentication...
     🎉 Twitter Media Extracted!
     
     📊 Results:
     🖼 Images: 3
     🎥 Videos: 1
     
     [Sends images and videos]
```

### Arabic (عربي):

```
أنت: https://twitter.com/username/status/123
البوت: 🐦 مستخرج وسائط تويتر (مصادق)
      🔐 استخدام ملفات تعريف ارتباط المتصفح...
      🎉 تم استخراج وسائط تويتر!
      
      📊 النتائج:
      🖼 الصور: 3
      🎥 الفيديوهات: 1
      
      [يرسل الصور والفيديوهات]
```

---

## 🔄 Switching Languages

### Use `/lang` command:

**English user switching to Arabic:**
```
You: /lang
Bot: ✅ تم تغيير اللغة إلى العربية
     
     الآن جميع الرسائل ستكون بالعربية.
     
     لتغيير اللغة مرة أخرى، استخدم: /lang
```

**Arabic user switching to English:**
```
أنت: /lang
البوت: ✅ Language changed to English
      
      All messages will now be in English.
      
      To change language again, use: /lang
```

---

## 📁 Files Created

### New Files:

1. **`language.py`** - Translation module
   - 200+ translated strings
   - English & Arabic translations
   - Auto language detection
   - RTL support for Arabic

2. **`telegram_bot_bilingual.py`** - Bilingual bot
   - Supports English & Arabic
   - Auto language detection
   - Manual language switching
   - All messages translated

### Updated Files:

3. **`config.py`** - Added language settings
   - LANGUAGE configuration
   - RTL support flag

---

## 🎨 Features

### ✅ What's Supported:

1. **Bot Interface**
   - ✅ All commands in both languages
   - ✅ Status messages (scraping, loading, etc.)
   - ✅ Success messages
   - ✅ Error messages with solutions

2. **Data Handling**
   - ✅ Arabic URLs work perfectly
   - ✅ Arabic text in scraped data preserved
   - ✅ UTF-8 encoding with BOM for Excel
   - ✅ CSV files open correctly in Excel

3. **Reports**
   - ✅ PDF reports support Arabic
   - ✅ Logs support Arabic
   - ✅ File names support both languages

4. **User Experience**
   - ✅ Auto language detection
   - ✅ Manual language switch (/lang)
   - ✅ Persistent language preference
   - ✅ RTL (Right-to-Left) support

---

## 🛠️ Technical Details

### Language Detection Algorithm:

```python
def detect_language(text):
    # Check for Arabic Unicode characters (U+0600 to U+06FF)
    arabic_chars = count_arabic_characters(text)
    
    # If >20% Arabic → Use Arabic
    if arabic_chars > len(text) * 0.2:
        return 'ar'
    
    return 'en'
```

### Translation System:

```python
from language import t

# Get translated text
greeting = t('welcome', lang='ar')  # Returns: "بوت استخراج البيانات الشامل"
greeting = t('welcome', lang='en')  # Returns: "Universal Web Scraper Bot"
```

### 200+ Translations Available:

- Bot messages
- Commands
- Status updates
- Error messages
- Success messages
- Help text
- Results formatting

---

## 📊 Comparison

### Old Bot (English Only):

```
User: https://example.com
Bot: 🚀 Starting scrape...
     ✅ Scraping Complete!
```

### New Bot (Bilingual):

**For English users:**
```
User: https://example.com
Bot: 🚀 Starting scrape...
     ✅ Scraping Complete!
```

**For Arabic users:**
```
المستخدم: https://example.com
البوت: 🚀 بدء الاستخراج...
      ✅ اكتمل الاستخراج!
```

---

## 🧪 Testing

### Test English:

```cmd
# 1. Run bot
.venv\Scripts\python telegram_bot_bilingual.py

# 2. In Telegram (with English settings):
/start
https://en.wikipedia.org/wiki/Python

# Should see all messages in English
```

### Test Arabic (اختبار العربية):

```cmd
# 1. Run bot (نفس الأمر)
.venv\Scripts\python telegram_bot_bilingual.py

# 2. In Telegram (with Arabic settings or send Arabic text):
/start
https://ar.wikipedia.org/wiki/بايثون

# Should see all messages in Arabic
```

### Test Language Switch:

```
1. Start with English
2. Send: /lang
3. Bot switches to Arabic
4. Send URL - get Arabic response
5. Send: /lang again
6. Bot switches back to English
```

---

## 💾 Data Export

### CSV Files:

**Encoding:** UTF-8 with BOM
- ✅ Opens correctly in Excel (Windows)
- ✅ Opens correctly in Excel (Mac)
- ✅ Opens correctly in Google Sheets
- ✅ Preserves Arabic characters
- ✅ Preserves English characters
- ✅ Preserves mixed Arabic/English text

**Example CSV content:**
```csv
العنوان,Description,السعر,Price
منتج عربي,Arabic Product,١٠٠,100
English Product,منتج إنجليزي,200,٢٠٠
```

---

## 🌟 User Experience

### For English Users:

**Start Bot:**
```
You: /start
Bot: 🤖 Universal Web Scraper Bot
     Welcome! I can scrape any website...
     Just send me any URL - no commands needed!
```

**Scrape:**
```
You: https://example.com
Bot: 🚀 Starting scrape...
     [Shows English progress messages]
     ✅ Scraping Complete!
     [Sends files with English captions]
```

### For Arabic Users (للمستخدمين العرب):

**Start Bot (بدء البوت):**
```
أنت: /start
البوت: 🤖 بوت استخراج البيانات الشامل
      مرحباً! يمكنني استخراج البيانات...
      فقط أرسل لي أي رابط - لا حاجة للأوامر!
```

**Scrape (استخراج):**
```
أنت: https://example.com
البوت: 🚀 بدء الاستخراج...
      [يعرض رسائل التقدم بالعربية]
      ✅ اكتمل الاستخراج!
      [يرسل الملفات مع توصيفات عربية]
```

---

## 🎯 Key Benefits

1. **Accessibility** (إمكانية الوصول)
   - Arabic speakers can use bot comfortably
   - No English knowledge required
   - Clear Arabic instructions

2. **Data Integrity** (سلامة البيانات)
   - Arabic text preserved in exports
   - No encoding issues
   - Excel-compatible CSV

3. **User Experience** (تجربة المستخدم)
   - Auto language detection
   - Easy language switching
   - Native feel for both languages

4. **Professional** (احترافي)
   - 200+ translations
   - Consistent terminology
   - Complete bilingual support

---

## 📖 Translation Coverage

### Fully Translated:

- ✅ Welcome messages
- ✅ Help documentation
- ✅ Command descriptions
- ✅ Status updates (scraping, loading, etc.)
- ✅ Success messages
- ✅ Error messages
- ✅ File captions
- ✅ Results formatting
- ✅ Twitter-specific messages
- ✅ Authentication instructions

### 200+ Strings Translated Including:

- starting_scrape → بدء الاستخراج
- please_wait → يرجى الانتظار
- scraping_complete → اكتمل الاستخراج
- items_extracted → العناصر المستخرجة
- images → الصور
- videos → الفيديوهات
- error_occurred → حدث خطأ
- try_again → حاول مرة أخرى

---

## 🚀 Ready to Use!

### Run Now:

```cmd
cd f:\Scrapper
.venv\Scripts\python telegram_bot_bilingual.py
```

### Test URLs:

**English:**
- https://en.wikipedia.org/wiki/Web_scraping
- https://quotes.toscrape.com
- https://twitter.com/Twitter/status/123

**Arabic:**
- https://ar.wikipedia.org/wiki/استخراج_البيانات
- https://www.bbc.com/arabic
- https://twitter.com/BBCArabic/status/123

---

## 📞 Support

**English:**
- Use `/help` for detailed instructions
- Use `/lang` to switch to Arabic
- Just send URLs to scrape!

**Arabic (العربية):**
- استخدم `/help` للحصول على تعليمات مفصلة
- استخدم `/lang` للتبديل إلى الإنجليزية
- فقط أرسل الروابط للاستخراج!

---

**🎉 Your bot now speaks both English and Arabic perfectly! (بوتك الآن يتحدث الإنجليزية والعربية بشكل مثالي!)**
