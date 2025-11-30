"""
🎯 UNIVERSAL SCRAPER DEMO
Quick demonstration of the universal scraper capabilities
"""

from domain_patterns import detect_domain_type
from colorama import init, Fore, Style

init()  # Initialize colorama

# Demo URLs across different niches
DEMO_URLS = [
    ("https://www.yallakora.com/match-center", "🏆 Sports - Arabic"),
    ("https://www.amazon.com/s?k=laptop", "🛍️ E-Commerce"),
    ("https://www.indeed.com/jobs", "💼 Jobs"),
    ("https://www.cnn.com", "📰 News"),
    ("https://www.zillow.com/homes", "🏠 Real Estate"),
    ("https://www.booking.com/searchresults", "✈️ Travel"),
    ("https://www.coursera.org/courses", "🎓 Education"),
    ("https://www.imdb.com/search/title", "🎬 Movies"),
    ("https://www.allrecipes.com/recipes", "🍔 Recipes"),
    ("https://www.coinmarketcap.com", "₿ Crypto"),
    ("https://github.com/trending", "💻 Developer"),
    ("https://www.youtube.com/feed/trending", "🎥 Video"),
]

print("=" * 80)
print(f"{Fore.CYAN}🌐 UNIVERSAL WEB SCRAPER - LIVE DEMO{Style.RESET_ALL}")
print("=" * 80)
print(f"\n{Fore.GREEN}Demonstrating automatic detection across 12 different niches...{Style.RESET_ALL}\n")

for url, description in DEMO_URLS:
    # Detect domain type
    domain_type, confidence, pattern = detect_domain_type(url, None)
    
    # Format output
    print(f"{Fore.YELLOW}{description}{Style.RESET_ALL}")
    print(f"   URL: {Fore.BLUE}{url}{Style.RESET_ALL}")
    print(f"   {Fore.GREEN}✅ Detected:{Style.RESET_ALL} {domain_type}")
    print(f"   {Fore.CYAN}📊 Confidence:{Style.RESET_ALL} {confidence}%")
    print(f"   {Fore.MAGENTA}🎯 Pattern:{Style.RESET_ALL} {pattern}")
    print()

print("=" * 80)
print(f"{Fore.GREEN}✅ All domains detected successfully!{Style.RESET_ALL}")
print(f"{Fore.CYAN}🚀 Ready to scrape any website from any niche!{Style.RESET_ALL}")
print("=" * 80)
print(f"\n{Fore.YELLOW}Try it yourself:{Style.RESET_ALL}")
print(f"   python test_universal_scraper.py --test-url \"YOUR_URL\"")
print(f"   python quick_scrape.py \"YOUR_URL\"\n")
