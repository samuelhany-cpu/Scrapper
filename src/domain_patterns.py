"""
Universal Domain Pattern Detection System
Supports 100+ test cases across multiple niches and domains
"""

DOMAIN_PATTERNS = {
    # ==================== SPORTS & GAMES ====================
    'sports_live': {
        'keywords': ['livescore', 'live-score', 'flashscore', 'sofascore', 'espn', 'score', 'goal', 
                    'sport', 'match', 'fixture', 'yallakora', 'kooora', 'filgoal', 'koora', 
                    'sportskeeda', 'bleacherreport', 'skysports', 'bbc/sport', 'nbcsports',
                    'sportradar', 'theathletic', 'transfermarkt', 'whoscored', 'fotmob'],
        'indicators': ['div[class*="match"]', 'div[class*="fixture"]', 'div[class*="score"]',
                      'div[class*="team"]', 'span[class*="time"]'],
        'type': 'sports_matches',
        'priority': 10
    },
    
    'sports_news': {
        'keywords': ['sportingnews', 'cbssports', 'si.com', 'marca', 'as.com', 'lequipe',
                    'gazzetta', 'sport.es', 'ole.com', 'fourfourtwo', 'football365',
                    'bleacherreport', 'nbcsports', 'theathletic', 'bbc.com/sport'],
        'indicators': ['article', 'div[class*="post"]', 'h2[class*="title"]'],
        'type': 'sports_news',
        'priority': 11  # Very high priority to override sports_matches
    },
    
    # ==================== E-COMMERCE ====================
    'ecommerce_major': {
        'keywords': ['amazon', 'ebay', 'alibaba', 'aliexpress', 'walmart', 'target', 'bestbuy',
                    'etsy', 'shopify', 'woocommerce', 'magento', 'bigcommerce', 'wayfair',
                    'overstock', 'newegg', 'rakuten', 'mercadolibre', 'flipkart', 'snapdeal',
                    'zalando', 'asos', 'boohoo', 'shein', 'temu', 'wish'],
        'indicators': ['div[class*="product"]', 'div[class*="item"]', 'span[class*="price"]',
                      'div[class*="cart"]', 'button[class*="buy"]'],
        'type': 'ecommerce_products',
        'priority': 10
    },
    
    'ecommerce_fashion': {
        'keywords': ['nike', 'adidas.com', 'zara', 'h&m', 'hm.com', 'uniqlo', 'gap', 'forever21', 'mango',
                    'pullbear', 'bershka', 'stradivarius', 'urbanoutfitters', 'anthropologie',
                    'freepeople', 'revolve', 'farfetch', 'net-a-porter', 'ssense', 'asos', 
                    'shein', 'zalando', 'boohoo', '-shoes', '/women', '/men'],
        'indicators': ['div[class*="product"]', 'div[class*="outfit"]', 'div[class*="look"]'],
        'type': 'fashion_products',
        'priority': 12  # Very high priority
    },
    
    # ==================== NEWS & MEDIA ====================
    'news_major': {
        'keywords': ['cnn', 'bbc.com/news', 'reuters', 'apnews', 'nytimes', 'washingtonpost', 'theguardian',
                    'telegraph', 'independent', 'dailymail', 'huffpost', 'buzzfeed', 'vice',
                    'vox', 'axios', 'politico', 'thehill', 'newsweek', 'time', 'usatoday',
                    'wsj', 'ft.com', 'aljazeera', 'dw.com', 'france24', 'rt.com'],
        'indicators': ['article', 'div[class*="story"]', 'div[class*="news"]', 'h1[class*="headline"]'],
        'type': 'news_articles',
        'priority': 10  # Higher priority
    },
    
    'news_tech': {
        'keywords': ['techcrunch', 'theverge', 'wired', 'arstechnica', 'engadget', 'gizmodo',
                    'cnet', 'zdnet', 'thenextweb', 'mashable', 'digitaltrends', 'androidpolice',
                    '9to5mac', 'macrumors', 'xda-developers', 'androidauthority'],
        'indicators': ['article', 'div[class*="post"]', 'div[class*="entry"]'],
        'type': 'tech_news',
        'priority': 9
    },
    
    # ==================== SOCIAL MEDIA ====================
    'social_major': {
        'keywords': ['twitter', 'facebook', 'instagram', 'pinterest',
                    'tumblr', 'tiktok', 'snapchat', 'discord', 'telegram', 'whatsapp', 'wechat', 'weibo'],
        'indicators': ['div[class*="post"]', 'div[class*="feed"]', 'div[class*="tweet"]',
                      'div[class*="story"]'],
        'type': 'social_media',
        'priority': 7  # Lower priority to allow specific detections
    },
    
    'social_video': {
        'keywords': ['youtube', 'vimeo', 'dailymotion', 'twitch'],
        'indicators': ['video', 'iframe', 'div[class*="video"]'],
        'type': 'video_content',
        'priority': 10  # Higher priority for video platforms
    },
    
    'social_professional': {
        'keywords': ['linkedin'],
        'indicators': ['div[class*="job"]', 'div[class*="profile"]', 'div[class*="post"]'],
        'type': 'job_listings',  # LinkedIn jobs should be detected as jobs
        'priority': 11  # Very high priority
    },
    
    'social_forum': {
        'keywords': ['reddit', '/r/', 'subreddit'],
        'indicators': ['div[class*="thread"]', 'div[class*="post"]', 'div[class*="comment"]'],
        'type': 'forum_threads',
        'priority': 10  # Higher than general social media
    },
    
    # ==================== ENTERTAINMENT ====================
    'entertainment_streaming': {
        'keywords': ['netflix', 'hulu', 'disneyplus', 'hbo', 'max', 'primevideo', 'amazon/prime',
                    'paramountplus', 'peacock', 'showtime', 'starz', 'crunchyroll', 'funimation',
                    'spotify', 'applemusic', 'soundcloud', 'deezer', 'tidal', 'pandora', 'twitch'],
        'indicators': ['div[class*="title"]', 'div[class*="card"]', 'div[class*="media"]', 
                      'div[class*="stream"]', 'div[class*="channel"]'],
        'type': 'streaming_content',
        'priority': 11  # Higher priority than video_content for streaming platforms
    },
    
    'entertainment_movies': {
        'keywords': ['imdb', 'rottentomatoes', 'metacritic', 'letterboxd', 'themoviedb', 'trakt',
                    'mubi', 'criterion', 'fandango', 'moviefone', 'filmaffinity'],
        'indicators': ['div[class*="title"]', 'span[class*="rating"]', 'div[class*="review"]'],
        'type': 'movie_reviews',
        'priority': 9
    },
    
    # ==================== EDUCATION ====================
    'education_platforms': {
        'keywords': ['coursera', 'udemy', 'edx', 'khanacademy', 'skillshare', 'pluralsight',
                    'linkedin/learning', 'udacity', 'codecademy', 'datacamp', 'treehouse',
                    'masterclass', 'brilliant', 'duolingo', 'memrise', 'babbel'],
        'indicators': ['div[class*="course"]', 'div[class*="lesson"]', 'div[class*="class"]'],
        'type': 'educational_courses',
        'priority': 8
    },
    
    'education_academic': {
        'keywords': ['scholar.google', 'researchgate', 'academia.edu', 'jstor', 'pubmed',
                    'arxiv', 'sciencedirect', 'springer', 'ieee', 'acm', 'nature', 'science'],
        'indicators': ['div[class*="paper"]', 'div[class*="article"]', 'div[class*="publication"]'],
        'type': 'academic_papers',
        'priority': 9
    },
    
    # ==================== JOBS & CAREER ====================
    'jobs_platforms': {
        'keywords': ['linkedin/jobs', 'indeed', 'glassdoor', 'monster', 'careerbuilder', 'ziprecruiter',
                    'dice', 'simplyhired', 'snagajob', 'flexjobs', 'remote.co', 'weworkremotely',
                    'angel.co', 'hired', 'toptal', 'upwork', 'freelancer', 'fiverr', 'guru'],
        'indicators': ['div[class*="job"]', 'div[class*="position"]', 'div[class*="listing"]'],
        'type': 'job_listings',
        'priority': 9
    },
    
    # ==================== REAL ESTATE ====================
    'real_estate': {
        'keywords': ['zillow', 'trulia', 'realtor.com', 'redfin', 'apartments.com', 'rightmove',
                    'zoopla', 'immobilienscout24', 'seloger', 'idealista', 'propertypal',
                    'daft.ie', 'trovit', 'mitula', 'nestoria', 'lamudi'],
        'indicators': ['div[class*="property"]', 'div[class*="listing"]', 'span[class*="price"]'],
        'type': 'real_estate_listings',
        'priority': 9
    },
    
    # ==================== TRAVEL & BOOKING ====================
    'travel_booking': {
        'keywords': ['booking', 'expedia', 'hotels', 'airbnb', 'vrbo', 'tripadvisor', 'kayak',
                    'skyscanner', 'priceline', 'hotwire', 'agoda', 'hostelworld', 'trivago',
                    'momondo', 'cheapflights', 'orbitz', 'travelocity', 'lastminute'],
        'indicators': ['div[class*="hotel"]', 'div[class*="flight"]', 'div[class*="room"]'],
        'type': 'travel_listings',
        'priority': 9
    },
    
    # ==================== FOOD & RECIPES ====================
    'food_recipes': {
        'keywords': ['allrecipes', 'foodnetwork', 'tasty', 'epicurious', 'bonappetit', 'seriouseats',
                    'thekitchn', 'simplyrecipes', 'delish', 'yummly', 'cookpad', 'food52',
                    'bbcgoodfood', 'jamieoliver', 'recipetineats'],
        'indicators': ['div[class*="recipe"]', 'div[class*="ingredient"]', 'div[class*="instruction"]'],
        'type': 'recipe_content',
        'priority': 8
    },
    
    'food_delivery': {
        'keywords': ['ubereats', 'doordash', 'grubhub', 'deliveroo', 'justeat', 'postmates',
                    'seamless', 'yelp', 'zomato', 'swiggy', 'foodpanda', 'talabat'],
        'indicators': ['div[class*="restaurant"]', 'div[class*="menu"]', 'div[class*="dish"]'],
        'type': 'restaurant_menus',
        'priority': 8
    },
    
    # ==================== FINANCE & CRYPTO ====================
    'finance_markets': {
        'keywords': ['bloomberg/markets', 'reuters/markets', 'cnbc', 'marketwatch', 'seekingalpha', 
                    'finance.yahoo', 'yahoo.com/finance', 'investing.com', 'tradingview', 'stocktwits', 
                    'finviz', 'wsj/markets', 'ft.com/markets', 'barrons', 'thestreet', 'morningstar'],
        'indicators': ['div[class*="stock"]', 'table[class*="quote"]', 'div[class*="ticker"]'],
        'type': 'financial_data',
        'priority': 11  # Higher than general news
    },
    
    'crypto_markets': {
        'keywords': ['coinbase', 'binance', 'kraken', 'coinmarketcap', 'coingecko', 'crypto.com',
                    'gemini', 'bitstamp', 'bitfinex', 'huobi', 'okx', 'kucoin', 'gate.io',
                    'cryptocompare', 'messari', 'glassnode', 'nansen'],
        'indicators': ['div[class*="coin"]', 'div[class*="crypto"]', 'div[class*="token"]'],
        'type': 'crypto_prices',
        'priority': 10
    },
    
    # ==================== HEALTH & FITNESS ====================
    'health_medical': {
        'keywords': ['webmd', 'mayoclinic', 'healthline', 'medicalnewstoday', 'medscape', 'drugs.com',
                    'patient.info', 'nhs.uk', 'clevelandclinic', 'hopkinsmedicine', 'nih.gov',
                    'cdc.gov', 'who.int', 'health.harvard'],
        'indicators': ['article', 'div[class*="symptom"]', 'div[class*="condition"]'],
        'type': 'medical_info',
        'priority': 8
    },
    
    'fitness_apps': {
        'keywords': ['myfitnesspal', 'fitbit', 'strava', 'nike/training', 'peloton', 'classpass',
                    'headspace', 'calm', 'noom', 'loseit', 'strongapp', 'jefit', 'bodybuilding'],
        'indicators': ['div[class*="workout"]', 'div[class*="exercise"]', 'div[class*="routine"]'],
        'type': 'fitness_tracking',
        'priority': 7
    },
    
    # ==================== TECHNOLOGY & DEV ====================
    'dev_platforms': {
        'keywords': ['github', 'gitlab', 'bitbucket', 'stackoverflow', 'stackexchange', 'devto',
                    'hashnode', 'medium', 'dev.to', 'hackernoon', 'freecodecamp', 'codepen',
                    'jsfiddle', 'codesandbox', 'replit', 'glitch'],
        'indicators': ['div[class*="repo"]', 'div[class*="code"]', 'pre', 'code'],
        'type': 'developer_content',
        'priority': 9
    },
    
    'dev_docs': {
        'keywords': ['docs', 'documentation', 'api', 'developer', 'reference', 'guide', 'tutorial',
                    'mdn', 'w3schools', 'devdocs', 'readthedocs', 'swagger', 'postman'],
        'indicators': ['article', 'div[class*="doc"]', 'code', 'pre'],
        'type': 'documentation',
        'priority': 8
    },
    
    # ==================== FORUMS & COMMUNITIES ====================
    'forums': {
        'keywords': ['forum', 'community', 'board', 'discussion', 'discourse', 'phpbb', 'vbulletin',
                    'quora', 'askubuntu', 'superuser', 'serverfault', 'reddit', '4chan',
                    'hackforums', 'digitalpoint', 'warriorforum', 'blackhatworld'],
        'indicators': ['div[class*="thread"]', 'div[class*="post"]', 'div[class*="reply"]'],
        'type': 'forum_threads',
        'priority': 7
    },
    
    # ==================== WEATHER ====================
    'weather': {
        'keywords': ['weather.com', 'accuweather', 'weather.gov', 'weatherunderground', 'metoffice',
                    'wunderground', 'yr.no', 'meteo', 'weather', 'forecast', 'clima'],
        'indicators': ['div[class*="weather"]', 'div[class*="forecast"]', 'div[class*="temperature"]'],
        'type': 'weather_data',
        'priority': 8
    },
    
    # ==================== E-LEARNING & KIDS ====================
    'kids_education': {
        'keywords': ['abcmouse', 'starfall', 'funbrain', 'coolmathgames', 'mathplayground',
                    'brainpop', 'education.com', 'ixl', 'prodigy', 'pbskids', 'nickjr'],
        'indicators': ['div[class*="game"]', 'div[class*="activity"]', 'div[class*="lesson"]'],
        'type': 'kids_content',
        'priority': 6
    },
    
    # ==================== GOVERNMENT & LEGAL ====================
    'government': {
        'keywords': ['gov', 'govt', 'government', 'parliament', 'congress', 'senate', 'whitehouse',
                    'europa.eu', 'un.org', 'data.gov', 'census', 'irs', 'sec.gov'],
        'indicators': ['div[class*="document"]', 'div[class*="legislation"]', 'table'],
        'type': 'government_data',
        'priority': 9
    },
    
    # ==================== AUTOMOTIVE ====================
    'automotive': {
        'keywords': ['cars.com', 'autotrader', 'carvana', 'carmax', 'edmunds', 'kbb', 'motortrend',
                    'caranddriver', 'autoblog', 'jalopnik', 'bring-a-trailer', 'mobile.de',
                    'autoscout24', 'leboncoin', 'coches.net', 'subito.it', '/cars', '/vehicles'],
        'indicators': ['div[class*="vehicle"]', 'div[class*="car"]', 'div[class*="listing"]'],
        'type': 'vehicle_listings',
        'priority': 11  # Higher priority to override streaming
    },
    
    # ==================== GAMING ====================
    'gaming': {
        'keywords': ['steam', 'epicgames', 'gog', 'origin', 'ubisoft', 'playstation', 'xbox',
                    'nintendo', 'ign', 'gamespot', 'polygon', 'kotaku', 'pcgamer', 'eurogamer',
                    'gamefaqs', 'twitch', 'mixer', 'mmorpg', 'minecraft', 'roblox', 'fortnite'],
        'indicators': ['div[class*="game"]', 'div[class*="review"]', 'div[class*="score"]'],
        'type': 'gaming_content',
        'priority': 8
    },
    
    # ==================== BUSINESS & B2B ====================
    'business': {
        'keywords': ['salesforce', 'hubspot', 'zendesk', 'slack', 'asana', 'trello', 'monday',
                    'notion', 'confluence', 'jira', 'crunchbase', 'owler', 'zoominfo',
                    'linkedin/company', 'glassdoor/companies', 'inc.com', 'fastcompany'],
        'indicators': ['div[class*="company"]', 'div[class*="business"]', 'div[class*="profile"]'],
        'type': 'business_data',
        'priority': 8
    },
}

# Additional HTML structure patterns
HTML_PATTERNS = {
    'tabular': {
        'indicators': ['table', 'thead', 'tbody', 'tr', 'td', 'th'],
        'min_count': 1,
        'type': 'tabular_data'
    },
    'listing': {
        'indicators': ['ul > li', 'ol > li', 'div[class*="list"]'],
        'min_count': 5,
        'type': 'list_content'
    },
    'gallery': {
        'indicators': ['div[class*="gallery"]', 'div[class*="grid"]', 'img'],
        'min_count': 6,
        'type': 'image_gallery'
    },
    'video': {
        'indicators': ['video', 'iframe[src*="youtube"]', 'iframe[src*="vimeo"]'],
        'min_count': 1,
        'type': 'video_content'
    },
    'form': {
        'indicators': ['form', 'input', 'textarea', 'select'],
        'min_count': 3,
        'type': 'form_data'
    }
}


def detect_domain_type(url, soup):
    """
    Detect domain type based on URL and HTML structure
    Returns: (type, confidence, matched_pattern)
    """
    url_lower = url.lower()
    detected = []
    
    # Check domain patterns
    for pattern_name, pattern_data in DOMAIN_PATTERNS.items():
        confidence = 0
        
        # Check URL keywords
        for keyword in pattern_data['keywords']:
            if keyword in url_lower:
                confidence += 30
                break
        
        # Check HTML indicators
        if soup:
            indicator_matches = 0
            for indicator in pattern_data['indicators']:
                try:
                    if soup.select(indicator):
                        indicator_matches += 1
                except:
                    pass
            
            if indicator_matches > 0:
                confidence += min(indicator_matches * 15, 60)
        
        if confidence > 0:
            detected.append({
                'type': pattern_data['type'],
                'confidence': min(confidence, 100),
                'priority': pattern_data.get('priority', 5),
                'pattern_name': pattern_name
            })
    
    # Check HTML structure patterns
    if soup:
        for pattern_name, pattern_data in HTML_PATTERNS.items():
            count = 0
            for indicator in pattern_data['indicators']:
                try:
                    count += len(soup.select(indicator))
                except:
                    pass
            
            if count >= pattern_data['min_count']:
                detected.append({
                    'type': pattern_data['type'],
                    'confidence': min(50 + count * 5, 90),
                    'priority': 6,
                    'pattern_name': pattern_name
                })
    
    # Sort by priority then confidence
    if detected:
        detected.sort(key=lambda x: (x['priority'], x['confidence']), reverse=True)
        return detected[0]['type'], detected[0]['confidence'], detected[0]['pattern_name']
    
    return 'general_content', 50, 'fallback'
