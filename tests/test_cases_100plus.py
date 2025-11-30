"""
Comprehensive Test Suite: 100+ Websites Across Multiple Domains
Tests the universal scraper's ability to detect and handle different niches
"""

TEST_CASES = [
    # ==================== SPORTS (15 tests) ====================
    {"url": "https://www.yallakora.com/match-center", "expected": "sports_matches", "category": "Sports - Arabic"},
    {"url": "https://www.espn.com/soccer/fixtures", "expected": "sports_matches", "category": "Sports - English"},
    {"url": "https://www.livescore.com", "expected": "sports_matches", "category": "Sports - Live Scores"},
    {"url": "https://www.goal.com/en/fixtures", "expected": "sports_matches", "category": "Sports - Fixtures"},
    {"url": "https://www.skysports.com/football", "expected": "sports_matches", "category": "Sports - Football"},
    {"url": "https://www.sofascore.com", "expected": "sports_matches", "category": "Sports - Scores"},
    {"url": "https://www.flashscore.com", "expected": "sports_matches", "category": "Sports - Flash Scores"},
    {"url": "https://www.kooora.com", "expected": "sports_matches", "category": "Sports - Arabic"},
    {"url": "https://www.transfermarkt.com/premier-league", "expected": "sports_matches", "category": "Sports - Transfers"},
    {"url": "https://www.whoscored.com", "expected": "sports_matches", "category": "Sports - Stats"},
    {"url": "https://www.marca.com/futbol", "expected": "sports_news", "category": "Sports News - Spanish"},
    {"url": "https://www.bleacherreport.com", "expected": "sports_news", "category": "Sports News"},
    {"url": "https://www.cbssports.com", "expected": "sports_news", "category": "Sports News"},
    {"url": "https://www.nbcsports.com", "expected": "sports_news", "category": "Sports News"},
    {"url": "https://www.theathletic.com", "expected": "sports_news", "category": "Sports News Premium"},
    
    # ==================== E-COMMERCE (20 tests) ====================
    {"url": "https://www.amazon.com/s?k=laptop", "expected": "ecommerce_products", "category": "E-commerce - Amazon"},
    {"url": "https://www.ebay.com/sch/i.html?_nkw=phone", "expected": "ecommerce_products", "category": "E-commerce - eBay"},
    {"url": "https://www.aliexpress.com/wholesale", "expected": "ecommerce_products", "category": "E-commerce - AliExpress"},
    {"url": "https://www.walmart.com/browse", "expected": "ecommerce_products", "category": "E-commerce - Walmart"},
    {"url": "https://www.target.com/c", "expected": "ecommerce_products", "category": "E-commerce - Target"},
    {"url": "https://www.bestbuy.com/site", "expected": "ecommerce_products", "category": "E-commerce - BestBuy"},
    {"url": "https://www.etsy.com/search", "expected": "ecommerce_products", "category": "E-commerce - Etsy"},
    {"url": "https://www.newegg.com/Laptops", "expected": "ecommerce_products", "category": "E-commerce - Newegg"},
    {"url": "https://www.wayfair.com/furniture", "expected": "ecommerce_products", "category": "E-commerce - Wayfair"},
    {"url": "https://www.overstock.com", "expected": "ecommerce_products", "category": "E-commerce - Overstock"},
    {"url": "https://www.nike.com/w/mens-shoes", "expected": "fashion_products", "category": "Fashion - Nike"},
    {"url": "https://www.adidas.com/us/men-shoes", "expected": "fashion_products", "category": "Fashion - Adidas"},
    {"url": "https://www.zara.com/us/en/woman", "expected": "fashion_products", "category": "Fashion - Zara"},
    {"url": "https://www.hm.com/us/women", "expected": "fashion_products", "category": "Fashion - H&M"},
    {"url": "https://www.asos.com/women", "expected": "fashion_products", "category": "Fashion - ASOS"},
    {"url": "https://www.shein.com/Women-Clothing", "expected": "fashion_products", "category": "Fashion - Shein"},
    {"url": "https://www.zalando.com", "expected": "fashion_products", "category": "Fashion - Zalando"},
    {"url": "https://www.uniqlo.com/us/en/women", "expected": "fashion_products", "category": "Fashion - Uniqlo"},
    {"url": "https://www.gap.com/browse", "expected": "fashion_products", "category": "Fashion - Gap"},
    {"url": "https://www.urbanoutfitters.com", "expected": "fashion_products", "category": "Fashion - Urban Outfitters"},
    
    # ==================== NEWS (15 tests) ====================
    {"url": "https://www.cnn.com", "expected": "news_articles", "category": "News - CNN"},
    {"url": "https://www.bbc.com/news", "expected": "news_articles", "category": "News - BBC"},
    {"url": "https://www.reuters.com", "expected": "news_articles", "category": "News - Reuters"},
    {"url": "https://www.nytimes.com", "expected": "news_articles", "category": "News - NYT"},
    {"url": "https://www.theguardian.com/international", "expected": "news_articles", "category": "News - Guardian"},
    {"url": "https://www.washingtonpost.com", "expected": "news_articles", "category": "News - WashPost"},
    {"url": "https://www.aljazeera.com", "expected": "news_articles", "category": "News - Al Jazeera"},
    {"url": "https://www.bloomberg.com/markets", "expected": "news_articles", "category": "News - Bloomberg"},
    {"url": "https://www.techcrunch.com", "expected": "tech_news", "category": "Tech News - TechCrunch"},
    {"url": "https://www.theverge.com", "expected": "tech_news", "category": "Tech News - The Verge"},
    {"url": "https://www.wired.com", "expected": "tech_news", "category": "Tech News - Wired"},
    {"url": "https://www.arstechnica.com", "expected": "tech_news", "category": "Tech News - Ars Technica"},
    {"url": "https://www.engadget.com", "expected": "tech_news", "category": "Tech News - Engadget"},
    {"url": "https://www.cnet.com", "expected": "tech_news", "category": "Tech News - CNET"},
    {"url": "https://www.zdnet.com", "expected": "tech_news", "category": "Tech News - ZDNet"},
    
    # ==================== JOBS (10 tests) ====================
    {"url": "https://www.linkedin.com/jobs", "expected": "job_listings", "category": "Jobs - LinkedIn"},
    {"url": "https://www.indeed.com/jobs", "expected": "job_listings", "category": "Jobs - Indeed"},
    {"url": "https://www.glassdoor.com/Job", "expected": "job_listings", "category": "Jobs - Glassdoor"},
    {"url": "https://www.monster.com/jobs", "expected": "job_listings", "category": "Jobs - Monster"},
    {"url": "https://www.careerbuilder.com", "expected": "job_listings", "category": "Jobs - CareerBuilder"},
    {"url": "https://www.ziprecruiter.com/jobs", "expected": "job_listings", "category": "Jobs - ZipRecruiter"},
    {"url": "https://www.dice.com/jobs", "expected": "job_listings", "category": "Jobs - Dice (Tech)"},
    {"url": "https://www.upwork.com/nx/find-work", "expected": "job_listings", "category": "Freelance - Upwork"},
    {"url": "https://www.freelancer.com/jobs", "expected": "job_listings", "category": "Freelance - Freelancer"},
    {"url": "https://www.fiverr.com/categories", "expected": "job_listings", "category": "Freelance - Fiverr"},
    
    # ==================== REAL ESTATE (8 tests) ====================
    {"url": "https://www.zillow.com/homes", "expected": "real_estate_listings", "category": "Real Estate - Zillow"},
    {"url": "https://www.trulia.com/for_sale", "expected": "real_estate_listings", "category": "Real Estate - Trulia"},
    {"url": "https://www.realtor.com/realestateandhomes-search", "expected": "real_estate_listings", "category": "Real Estate - Realtor"},
    {"url": "https://www.redfin.com", "expected": "real_estate_listings", "category": "Real Estate - Redfin"},
    {"url": "https://www.apartments.com", "expected": "real_estate_listings", "category": "Real Estate - Apartments"},
    {"url": "https://www.rightmove.co.uk", "expected": "real_estate_listings", "category": "Real Estate - UK"},
    {"url": "https://www.zoopla.co.uk", "expected": "real_estate_listings", "category": "Real Estate - UK"},
    {"url": "https://www.immobilienscout24.de", "expected": "real_estate_listings", "category": "Real Estate - Germany"},
    
    # ==================== TRAVEL (8 tests) ====================
    {"url": "https://www.booking.com/searchresults", "expected": "travel_listings", "category": "Travel - Booking.com"},
    {"url": "https://www.expedia.com/Hotel-Search", "expected": "travel_listings", "category": "Travel - Expedia"},
    {"url": "https://www.airbnb.com/s/homes", "expected": "travel_listings", "category": "Travel - Airbnb"},
    {"url": "https://www.hotels.com/search", "expected": "travel_listings", "category": "Travel - Hotels.com"},
    {"url": "https://www.tripadvisor.com/Hotels", "expected": "travel_listings", "category": "Travel - TripAdvisor"},
    {"url": "https://www.kayak.com/flights", "expected": "travel_listings", "category": "Travel - Kayak"},
    {"url": "https://www.skyscanner.com/flights", "expected": "travel_listings", "category": "Travel - Skyscanner"},
    {"url": "https://www.agoda.com/search", "expected": "travel_listings", "category": "Travel - Agoda"},
    
    # ==================== EDUCATION (8 tests) ====================
    {"url": "https://www.coursera.org/courses", "expected": "educational_courses", "category": "Education - Coursera"},
    {"url": "https://www.udemy.com/courses", "expected": "educational_courses", "category": "Education - Udemy"},
    {"url": "https://www.edx.org/search", "expected": "educational_courses", "category": "Education - edX"},
    {"url": "https://www.khanacademy.org", "expected": "educational_courses", "category": "Education - Khan Academy"},
    {"url": "https://www.skillshare.com/browse", "expected": "educational_courses", "category": "Education - Skillshare"},
    {"url": "https://scholar.google.com", "expected": "academic_papers", "category": "Academic - Google Scholar"},
    {"url": "https://www.researchgate.net", "expected": "academic_papers", "category": "Academic - ResearchGate"},
    {"url": "https://arxiv.org", "expected": "academic_papers", "category": "Academic - arXiv"},
    
    # ==================== ENTERTAINMENT (10 tests) ====================
    {"url": "https://www.imdb.com/search/title", "expected": "movie_reviews", "category": "Movies - IMDb"},
    {"url": "https://www.rottentomatoes.com/browse/movies_at_home", "expected": "movie_reviews", "category": "Movies - Rotten Tomatoes"},
    {"url": "https://www.metacritic.com/browse/movies", "expected": "movie_reviews", "category": "Movies - Metacritic"},
    {"url": "https://www.themoviedb.org/movie", "expected": "movie_reviews", "category": "Movies - TMDB"},
    {"url": "https://www.netflix.com/browse", "expected": "streaming_content", "category": "Streaming - Netflix"},
    {"url": "https://www.youtube.com/feed/trending", "expected": "video_content", "category": "Video - YouTube"},
    {"url": "https://www.twitch.tv/directory", "expected": "streaming_content", "category": "Streaming - Twitch"},
    {"url": "https://www.spotify.com/browse", "expected": "streaming_content", "category": "Music - Spotify"},
    {"url": "https://www.soundcloud.com/discover", "expected": "streaming_content", "category": "Music - SoundCloud"},
    {"url": "https://www.vimeo.com/watch", "expected": "video_content", "category": "Video - Vimeo"},
    
    # ==================== FOOD (6 tests) ====================
    {"url": "https://www.allrecipes.com/recipes", "expected": "recipe_content", "category": "Recipes - AllRecipes"},
    {"url": "https://www.foodnetwork.com/recipes", "expected": "recipe_content", "category": "Recipes - Food Network"},
    {"url": "https://www.tasty.co/search", "expected": "recipe_content", "category": "Recipes - Tasty"},
    {"url": "https://www.epicurious.com/recipes-menus", "expected": "recipe_content", "category": "Recipes - Epicurious"},
    {"url": "https://www.ubereats.com/category", "expected": "restaurant_menus", "category": "Food Delivery - Uber Eats"},
    {"url": "https://www.doordash.com/food-delivery", "expected": "restaurant_menus", "category": "Food Delivery - DoorDash"},
    
    # ==================== FINANCE (6 tests) ====================
    {"url": "https://finance.yahoo.com/quote", "expected": "financial_data", "category": "Finance - Yahoo Finance"},
    {"url": "https://www.investing.com/currencies", "expected": "financial_data", "category": "Finance - Investing.com"},
    {"url": "https://www.marketwatch.com/markets", "expected": "financial_data", "category": "Finance - MarketWatch"},
    {"url": "https://www.coinmarketcap.com", "expected": "crypto_prices", "category": "Crypto - CoinMarketCap"},
    {"url": "https://www.coingecko.com", "expected": "crypto_prices", "category": "Crypto - CoinGecko"},
    {"url": "https://www.binance.com/en/markets", "expected": "crypto_prices", "category": "Crypto - Binance"},
    
    # ==================== TECHNOLOGY (8 tests) ====================
    {"url": "https://github.com/trending", "expected": "developer_content", "category": "Dev - GitHub"},
    {"url": "https://stackoverflow.com/questions", "expected": "developer_content", "category": "Dev - StackOverflow"},
    {"url": "https://dev.to", "expected": "developer_content", "category": "Dev - DEV Community"},
    {"url": "https://www.reddit.com/r/programming", "expected": "forum_threads", "category": "Forum - Reddit"},
    {"url": "https://developer.mozilla.org/en-US/docs", "expected": "documentation", "category": "Docs - MDN"},
    {"url": "https://www.w3schools.com", "expected": "documentation", "category": "Docs - W3Schools"},
    {"url": "https://docs.python.org", "expected": "documentation", "category": "Docs - Python"},
    {"url": "https://reactjs.org/docs", "expected": "documentation", "category": "Docs - React"},
    
    # ==================== AUTOMOTIVE (5 tests) ====================
    {"url": "https://www.cars.com/shopping", "expected": "vehicle_listings", "category": "Auto - Cars.com"},
    {"url": "https://www.autotrader.com/cars-for-sale", "expected": "vehicle_listings", "category": "Auto - AutoTrader"},
    {"url": "https://www.carvana.com/cars", "expected": "vehicle_listings", "category": "Auto - Carvana"},
    {"url": "https://www.carmax.com/cars", "expected": "vehicle_listings", "category": "Auto - CarMax"},
    {"url": "https://www.edmunds.com/inventory", "expected": "vehicle_listings", "category": "Auto - Edmunds"},
    
    # ==================== GAMING (5 tests) ====================
    {"url": "https://store.steampowered.com", "expected": "gaming_content", "category": "Gaming - Steam"},
    {"url": "https://www.ign.com/games", "expected": "gaming_content", "category": "Gaming - IGN"},
    {"url": "https://www.gamespot.com/games", "expected": "gaming_content", "category": "Gaming - GameSpot"},
    {"url": "https://www.pcgamer.com", "expected": "gaming_content", "category": "Gaming - PC Gamer"},
    {"url": "https://www.polygon.com/games", "expected": "gaming_content", "category": "Gaming - Polygon"},
    
    # ==================== WEATHER (3 tests) ====================
    {"url": "https://www.weather.com", "expected": "weather_data", "category": "Weather - Weather.com"},
    {"url": "https://www.accuweather.com", "expected": "weather_data", "category": "Weather - AccuWeather"},
    {"url": "https://www.wunderground.com", "expected": "weather_data", "category": "Weather - Wunderground"},
]

print(f"✅ Total Test Cases: {len(TEST_CASES)}")
print(f"\nCategories:")
categories = {}
for test in TEST_CASES:
    cat = test['category'].split(' - ')[0]
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items()):
    print(f"   • {cat}: {count} tests")
