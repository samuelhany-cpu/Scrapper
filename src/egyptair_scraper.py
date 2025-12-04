"""
EgyptAir Flight Schedule Scraper - Advanced Edition
Extracts ALL flights for ALL worldwide destinations over a full year
Features:
- Firefox with stealth mode
- Human-like behavior (random delays, mouse movements, scrolling)
- Anti-bot detection
- Comprehensive worldwide coverage
- Real browser simulation
"""
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import json
from .config import Config
from .logger import ScraperLogger

class EgyptAirFlightScraper:
    def __init__(self, logger=None, headless=False):
        self.logger = logger or ScraperLogger('egyptair_scraper')
        self.driver = None
        self.all_flights = []
        self.routes = []
        self.headless = headless
        self.worldwide_destinations = []
        
    def human_delay(self, min_seconds=1, max_seconds=3):
        """Simulate human-like delay"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def human_typing(self, element, text):
        """Type like a human with random delays between characters"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def random_mouse_movement(self):
        """Simulate random mouse movements"""
        try:
            actions = ActionChains(self.driver)
            # Move to random positions
            for _ in range(random.randint(1, 3)):
                x_offset = random.randint(-100, 100)
                y_offset = random.randint(-100, 100)
                actions.move_by_offset(x_offset, y_offset).perform()
                time.sleep(random.uniform(0.1, 0.3))
        except:
            pass
    
    def random_scroll(self):
        """Simulate random scrolling behavior"""
        try:
            scroll_amount = random.randint(100, 500)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            self.human_delay(0.5, 1.5)
            self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount//2});")
            self.human_delay(0.3, 0.8)
        except:
            pass
        
    def setup_driver(self):
        """Setup Firefox driver with stealth mode and anti-detection"""
        self.logger.info("Setting up Firefox driver with stealth mode...")
        
        firefox_options = FirefoxOptions()
        
        # Stealth mode settings
        if self.headless:
            firefox_options.add_argument('--headless')
        
        # Anti-detection preferences
        firefox_options.set_preference("dom.webdriver.enabled", False)
        firefox_options.set_preference('useAutomationExtension', False)
        firefox_options.set_preference("general.useragent.override", 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0")
        
        # Privacy settings
        firefox_options.set_preference("privacy.trackingprotection.enabled", False)
        firefox_options.set_preference("dom.webnotifications.enabled", False)
        firefox_options.set_preference("media.navigator.enabled", False)
        
        # Performance settings
        firefox_options.set_preference("browser.cache.disk.enable", True)
        firefox_options.set_preference("browser.cache.memory.enable", True)
        firefox_options.set_preference("network.http.pipelining", True)
        
        try:
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=firefox_options
            )
        except:
            # Fallback: try using system Firefox
            self.logger.info("Trying system Firefox...")
            self.driver = webdriver.Firefox(options=firefox_options)
        
        # Set window size
        self.driver.set_window_size(1920, 1080)
        
        # Execute stealth JavaScript
        stealth_js = """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false
        });
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
        """
        self.driver.execute_script(stealth_js)
        
        self.driver.implicitly_wait(10)
        self.logger.info("✅ Firefox driver setup complete with stealth mode")
        
    def get_all_destinations(self):
        """Extract all available destinations from the website"""
        self.logger.info("Fetching all available destinations...")
        
        try:
            # Go to timetable page
            self.driver.get("https://www.egyptair.com/en/Plan/Pages/timetable.aspx")
            time.sleep(3)
            
            # Click "Show countries and cities list" for departure
            try:
                show_from = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Show contries and cities list')]"))
                )
                show_from.click()
                time.sleep(2)
                
                # Extract all cities from the list
                cities_from = self.driver.find_elements(By.CSS_SELECTOR, ".city-item, .destination-item, option")
                
                destinations = []
                for city in cities_from:
                    text = city.text.strip()
                    value = city.get_attribute('value')
                    if text and value:
                        destinations.append({
                            'name': text,
                            'code': value
                        })
                
                self.logger.info(f"Found {len(destinations)} destinations")
                return destinations
                
            except Exception as e:
                self.logger.error(f"Error extracting destinations: {e}")
                # Fallback: use common EgyptAir destinations
                return self.get_default_destinations()
                
        except Exception as e:
            self.logger.error(f"Error accessing timetable page: {e}")
            return self.get_default_destinations()
    
    def get_default_destinations(self):
        """Return comprehensive worldwide destinations for EgyptAir"""
        self.logger.info("Loading comprehensive worldwide destination list...")
        
        # COMPREHENSIVE WORLDWIDE DESTINATIONS
        destinations = [
            # ========== EGYPT (Domestic) ==========
            {'name': 'Cairo', 'code': 'CAI', 'country': 'Egypt', 'region': 'North Africa'},
            {'name': 'Alexandria', 'code': 'ALY', 'country': 'Egypt', 'region': 'North Africa'},
            {'name': 'Sharm El Sheikh', 'code': 'SSH', 'country': 'Egypt', 'region': 'North Africa'},
            {'name': 'Hurghada', 'code': 'HRG', 'country': 'Egypt', 'region': 'North Africa'},
            {'name': 'Luxor', 'code': 'LXR', 'country': 'Egypt', 'region': 'North Africa'},
            {'name': 'Aswan', 'code': 'ASW', 'country': 'Egypt', 'region': 'North Africa'},
            {'name': 'Marsa Alam', 'code': 'RMF', 'country': 'Egypt', 'region': 'North Africa'},
            
            # ========== MIDDLE EAST ==========
            # UAE
            {'name': 'Dubai', 'code': 'DXB', 'country': 'UAE', 'region': 'Middle East'},
            {'name': 'Abu Dhabi', 'code': 'AUH', 'country': 'UAE', 'region': 'Middle East'},
            {'name': 'Sharjah', 'code': 'SHJ', 'country': 'UAE', 'region': 'Middle East'},
            
            # Saudi Arabia
            {'name': 'Jeddah', 'code': 'JED', 'country': 'Saudi Arabia', 'region': 'Middle East'},
            {'name': 'Riyadh', 'code': 'RUH', 'country': 'Saudi Arabia', 'region': 'Middle East'},
            {'name': 'Dammam', 'code': 'DMM', 'country': 'Saudi Arabia', 'region': 'Middle East'},
            {'name': 'Medina', 'code': 'MED', 'country': 'Saudi Arabia', 'region': 'Middle East'},
            {'name': 'Abha', 'code': 'AHB', 'country': 'Saudi Arabia', 'region': 'Middle East'},
            
            # Kuwait, Qatar, Bahrain, Oman
            {'name': 'Kuwait City', 'code': 'KWI', 'country': 'Kuwait', 'region': 'Middle East'},
            {'name': 'Doha', 'code': 'DOH', 'country': 'Qatar', 'region': 'Middle East'},
            {'name': 'Manama', 'code': 'BAH', 'country': 'Bahrain', 'region': 'Middle East'},
            {'name': 'Muscat', 'code': 'MCT', 'country': 'Oman', 'region': 'Middle East'},
            
            # Levant
            {'name': 'Beirut', 'code': 'BEY', 'country': 'Lebanon', 'region': 'Middle East'},
            {'name': 'Amman', 'code': 'AMM', 'country': 'Jordan', 'region': 'Middle East'},
            {'name': 'Aqaba', 'code': 'AQJ', 'country': 'Jordan', 'region': 'Middle East'},
            {'name': 'Baghdad', 'code': 'BGW', 'country': 'Iraq', 'region': 'Middle East'},
            {'name': 'Erbil', 'code': 'EBL', 'country': 'Iraq', 'region': 'Middle East'},
            
            # ========== EUROPE ==========
            # Western Europe
            {'name': 'London Heathrow', 'code': 'LHR', 'country': 'UK', 'region': 'Western Europe'},
            {'name': 'Manchester', 'code': 'MAN', 'country': 'UK', 'region': 'Western Europe'},
            {'name': 'Paris CDG', 'code': 'CDG', 'country': 'France', 'region': 'Western Europe'},
            {'name': 'Frankfurt', 'code': 'FRA', 'country': 'Germany', 'region': 'Western Europe'},
            {'name': 'Munich', 'code': 'MUC', 'country': 'Germany', 'region': 'Western Europe'},
            {'name': 'Amsterdam', 'code': 'AMS', 'country': 'Netherlands', 'region': 'Western Europe'},
            {'name': 'Brussels', 'code': 'BRU', 'country': 'Belgium', 'region': 'Western Europe'},
            {'name': 'Zurich', 'code': 'ZRH', 'country': 'Switzerland', 'region': 'Western Europe'},
            {'name': 'Geneva', 'code': 'GVA', 'country': 'Switzerland', 'region': 'Western Europe'},
            
            # Southern Europe
            {'name': 'Rome Fiumicino', 'code': 'FCO', 'country': 'Italy', 'region': 'Southern Europe'},
            {'name': 'Milan Malpensa', 'code': 'MXP', 'country': 'Italy', 'region': 'Southern Europe'},
            {'name': 'Venice', 'code': 'VCE', 'country': 'Italy', 'region': 'Southern Europe'},
            {'name': 'Athens', 'code': 'ATH', 'country': 'Greece', 'region': 'Southern Europe'},
            {'name': 'Madrid', 'code': 'MAD', 'country': 'Spain', 'region': 'Southern Europe'},
            {'name': 'Barcelona', 'code': 'BCN', 'country': 'Spain', 'region': 'Southern Europe'},
            {'name': 'Lisbon', 'code': 'LIS', 'country': 'Portugal', 'region': 'Southern Europe'},
            
            # Eastern Europe
            {'name': 'Istanbul', 'code': 'IST', 'country': 'Turkey', 'region': 'Eastern Europe'},
            {'name': 'Ankara', 'code': 'ESB', 'country': 'Turkey', 'region': 'Eastern Europe'},
            {'name': 'Vienna', 'code': 'VIE', 'country': 'Austria', 'region': 'Eastern Europe'},
            {'name': 'Prague', 'code': 'PRG', 'country': 'Czech Republic', 'region': 'Eastern Europe'},
            {'name': 'Budapest', 'code': 'BUD', 'country': 'Hungary', 'region': 'Eastern Europe'},
            {'name': 'Warsaw', 'code': 'WAW', 'country': 'Poland', 'region': 'Eastern Europe'},
            {'name': 'Moscow', 'code': 'SVO', 'country': 'Russia', 'region': 'Eastern Europe'},
            
            # ========== AFRICA ==========
            # North Africa
            {'name': 'Tunis', 'code': 'TUN', 'country': 'Tunisia', 'region': 'North Africa'},
            {'name': 'Algiers', 'code': 'ALG', 'country': 'Algeria', 'region': 'North Africa'},
            {'name': 'Casablanca', 'code': 'CMN', 'country': 'Morocco', 'region': 'North Africa'},
            {'name': 'Tripoli', 'code': 'TIP', 'country': 'Libya', 'region': 'North Africa'},
            
            # East Africa
            {'name': 'Khartoum', 'code': 'KRT', 'country': 'Sudan', 'region': 'East Africa'},
            {'name': 'Addis Ababa', 'code': 'ADD', 'country': 'Ethiopia', 'region': 'East Africa'},
            {'name': 'Nairobi', 'code': 'NBO', 'country': 'Kenya', 'region': 'East Africa'},
            {'name': 'Dar es Salaam', 'code': 'DAR', 'country': 'Tanzania', 'region': 'East Africa'},
            {'name': 'Entebbe', 'code': 'EBB', 'country': 'Uganda', 'region': 'East Africa'},
            {'name': 'Djibouti', 'code': 'JIB', 'country': 'Djibouti', 'region': 'East Africa'},
            
            # West Africa
            {'name': 'Lagos', 'code': 'LOS', 'country': 'Nigeria', 'region': 'West Africa'},
            {'name': 'Abuja', 'code': 'ABV', 'country': 'Nigeria', 'region': 'West Africa'},
            {'name': 'Accra', 'code': 'ACC', 'country': 'Ghana', 'region': 'West Africa'},
            {'name': 'Abidjan', 'code': 'ABJ', 'country': 'Ivory Coast', 'region': 'West Africa'},
            
            # Southern Africa
            {'name': 'Johannesburg', 'code': 'JNB', 'country': 'South Africa', 'region': 'Southern Africa'},
            {'name': 'Cape Town', 'code': 'CPT', 'country': 'South Africa', 'region': 'Southern Africa'},
            
            # ========== ASIA ==========
            # South Asia
            {'name': 'Mumbai', 'code': 'BOM', 'country': 'India', 'region': 'South Asia'},
            {'name': 'Delhi', 'code': 'DEL', 'country': 'India', 'region': 'South Asia'},
            {'name': 'Bangalore', 'code': 'BLR', 'country': 'India', 'region': 'South Asia'},
            {'name': 'Karachi', 'code': 'KHI', 'country': 'Pakistan', 'region': 'South Asia'},
            {'name': 'Islamabad', 'code': 'ISB', 'country': 'Pakistan', 'region': 'South Asia'},
            {'name': 'Dhaka', 'code': 'DAC', 'country': 'Bangladesh', 'region': 'South Asia'},
            
            # Southeast Asia
            {'name': 'Bangkok', 'code': 'BKK', 'country': 'Thailand', 'region': 'Southeast Asia'},
            {'name': 'Singapore', 'code': 'SIN', 'country': 'Singapore', 'region': 'Southeast Asia'},
            {'name': 'Kuala Lumpur', 'code': 'KUL', 'country': 'Malaysia', 'region': 'Southeast Asia'},
            {'name': 'Jakarta', 'code': 'CGK', 'country': 'Indonesia', 'region': 'Southeast Asia'},
            {'name': 'Manila', 'code': 'MNL', 'country': 'Philippines', 'region': 'Southeast Asia'},
            
            # East Asia
            {'name': 'Beijing', 'code': 'PEK', 'country': 'China', 'region': 'East Asia'},
            {'name': 'Shanghai', 'code': 'PVG', 'country': 'China', 'region': 'East Asia'},
            {'name': 'Guangzhou', 'code': 'CAN', 'country': 'China', 'region': 'East Asia'},
            {'name': 'Hong Kong', 'code': 'HKG', 'country': 'Hong Kong', 'region': 'East Asia'},
            {'name': 'Tokyo', 'code': 'NRT', 'country': 'Japan', 'region': 'East Asia'},
            {'name': 'Seoul', 'code': 'ICN', 'country': 'South Korea', 'region': 'East Asia'},
            
            # Central Asia
            {'name': 'Almaty', 'code': 'ALA', 'country': 'Kazakhstan', 'region': 'Central Asia'},
            
            # ========== AMERICAS ==========
            # North America
            {'name': 'New York JFK', 'code': 'JFK', 'country': 'USA', 'region': 'North America'},
            {'name': 'Washington DC', 'code': 'IAD', 'country': 'USA', 'region': 'North America'},
            {'name': 'Toronto', 'code': 'YYZ', 'country': 'Canada', 'region': 'North America'},
            {'name': 'Montreal', 'code': 'YUL', 'country': 'Canada', 'region': 'North America'},
            
            # South America
            {'name': 'Sao Paulo', 'code': 'GRU', 'country': 'Brazil', 'region': 'South America'},
            {'name': 'Buenos Aires', 'code': 'EZE', 'country': 'Argentina', 'region': 'South America'},
            
            # ========== OCEANIA ==========
            {'name': 'Sydney', 'code': 'SYD', 'country': 'Australia', 'region': 'Oceania'},
            {'name': 'Melbourne', 'code': 'MEL', 'country': 'Australia', 'region': 'Oceania'},
        ]
        
        self.logger.info(f"✅ Loaded {len(destinations)} worldwide destinations covering all continents")
        return destinations
    
    def search_flights(self, origin, destination, date):
        """Search for flights on a specific route and date with human-like behavior"""
        try:
            self.logger.info(f"🔍 Searching: {origin['name']} ({origin['code']}) → {destination['name']} ({destination['code']}) on {date.strftime('%Y-%m-%d')}")
            
            # Try multiple possible URLs for EgyptAir timetable
            urls_to_try = [
                "https://www.egyptair.com/en/fly/flight-schedule",
                "https://www.egyptair.com/en/Plan/Pages/timetable.aspx",
                "https://www.egyptair.com/en/plan/timetable",
                "https://www.egyptair.com/en-us/plan/flight-schedule"
            ]
            
            page_loaded = False
            for url in urls_to_try:
                try:
                    self.driver.get(url)
                    self.human_delay(3, 5)
                    
                    # Check if page loaded successfully by looking for any form element
                    if self.driver.find_elements(By.CSS_SELECTOR, "input, select, button"):
                        page_loaded = True
                        self.logger.info(f"✅ Successfully loaded: {url}")
                        break
                except:
                    continue
            
            if not page_loaded:
                self.logger.warning("Could not load any timetable page")
                return []
            
            # Random mouse movement
            self.random_mouse_movement()
            
            # Random scroll to simulate reading
            self.random_scroll()
            
            # Try to find and fill the form with multiple selector strategies
            # Multiple possible selectors for origin input
            origin_selectors = [
                ("ID", "fromStation"),
                ("ID", "origin"),
                ("ID", "from"),
                ("NAME", "origin"),
                ("NAME", "from"),
                ("CSS", "input[placeholder*='From'], input[placeholder*='Origin']"),
                ("CSS", "input[name*='origin'], input[name*='from']"),
                ("CSS", ".origin-input, .from-input"),
                ("XPATH", "//input[contains(@placeholder, 'From') or contains(@placeholder, 'Origin')]")
            ]
            
            from_input = None
            for selector_type, selector_value in origin_selectors:
                try:
                    self.human_delay(0.5, 1.5)
                    if selector_type == "ID":
                        from_input = self.driver.find_element(By.ID, selector_value)
                    elif selector_type == "NAME":
                        from_input = self.driver.find_element(By.NAME, selector_value)
                    elif selector_type == "CSS":
                        from_input = self.driver.find_element(By.CSS_SELECTOR, selector_value)
                    elif selector_type == "XPATH":
                        from_input = self.driver.find_element(By.XPATH, selector_value)
                    
                    if from_input:
                        self.logger.info(f"✅ Found origin input using {selector_type}: {selector_value}")
                        break
                except:
                    continue
            
            if not from_input:
                self.logger.warning("Could not find origin input field with any selector")
                return []
            
            # Fill origin with human typing
            try:
                
                # Move to element
                actions = ActionChains(self.driver)
                actions.move_to_element(from_input).perform()
                self.human_delay(0.2, 0.5)
                
                from_input.click()
                self.human_delay(0.2, 0.4)
                from_input.clear()
                self.human_delay(0.1, 0.3)
                
                # Type with human-like delays
                self.human_typing(from_input, origin['code'])
                self.human_delay(1, 2)
                
                # Select from dropdown
                first_option = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-menu-item, .autocomplete-item, li[role='option']"))
                )
                
                # Move to dropdown option
                actions.move_to_element(first_option).perform()
                self.human_delay(0.3, 0.6)
                first_option.click()
                self.human_delay(0.5, 1)
            except Exception as e:
                self.logger.warning(f"Could not set origin: {e}")
                return []
            
            # Find destination input with multiple selectors
            dest_selectors = [
                ("ID", "toStation"),
                ("ID", "destination"),
                ("ID", "to"),
                ("NAME", "destination"),
                ("NAME", "to"),
                ("CSS", "input[placeholder*='To'], input[placeholder*='Destination']"),
                ("CSS", "input[name*='destination'], input[name*='to']"),
                ("CSS", ".destination-input, .to-input"),
                ("XPATH", "//input[contains(@placeholder, 'To') or contains(@placeholder, 'Destination')]")
            ]
            
            to_input = None
            for selector_type, selector_value in dest_selectors:
                try:
                    self.human_delay(0.5, 1.5)
                    if selector_type == "ID":
                        to_input = self.driver.find_element(By.ID, selector_value)
                    elif selector_type == "NAME":
                        to_input = self.driver.find_element(By.NAME, selector_value)
                    elif selector_type == "CSS":
                        to_input = self.driver.find_element(By.CSS_SELECTOR, selector_value)
                    elif selector_type == "XPATH":
                        to_input = self.driver.find_element(By.XPATH, selector_value)
                    
                    if to_input:
                        self.logger.info(f"✅ Found destination input using {selector_type}: {selector_value}")
                        break
                except:
                    continue
            
            if not to_input:
                self.logger.warning("Could not find destination input field")
                return []
            
            # Fill destination with human typing
            try:
                # Move to element
                actions = ActionChains(self.driver)
                actions.move_to_element(to_input).perform()
                self.human_delay(0.2, 0.5)
                
                to_input.click()
                self.human_delay(0.2, 0.4)
                to_input.clear()
                self.human_delay(0.1, 0.3)
                
                # Type with human-like delays
                self.human_typing(to_input, destination['code'])
                self.human_delay(1, 2)
                
                # Select from dropdown
                first_option = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-menu-item, .autocomplete-item, li[role='option']"))
                )
                
                # Move to dropdown option
                actions.move_to_element(first_option).perform()
                self.human_delay(0.3, 0.6)
                first_option.click()
                self.human_delay(0.5, 1)
            except Exception as e:
                self.logger.warning(f"Could not set destination: {e}")
                return []
            
            # Set departure date with human-like behavior
            try:
                self.human_delay(0.5, 1)
                date_input = self.driver.find_element(By.ID, "departureDate")
                
                # Move to element
                actions = ActionChains(self.driver)
                actions.move_to_element(date_input).perform()
                self.human_delay(0.2, 0.5)
                
                date_input.click()
                self.human_delay(0.2, 0.4)
                date_input.clear()
                self.human_delay(0.1, 0.3)
                
                # Type date with human-like delays
                self.human_typing(date_input, date.strftime("%d/%m/%Y"))
                self.human_delay(0.5, 1)
            except Exception as e:
                self.logger.warning(f"Could not set date: {e}")
            
            # Random mouse movement before clicking search
            self.random_mouse_movement()
            
            # Click search with human-like behavior
            try:
                self.human_delay(1, 2)
                search_btn = self.driver.find_element(By.ID, "btnSearch")
                
                # Move to search button
                actions = ActionChains(self.driver)
                actions.move_to_element(search_btn).perform()
                self.human_delay(0.5, 1)
                
                search_btn.click()
                self.logger.info("⏳ Waiting for search results...")
                
                # Wait for results with longer delay
                self.human_delay(5, 8)
            except Exception as e:
                self.logger.warning(f"Could not click search: {e}")
                return []
            
            # Extract flight results
            flights = self.extract_flight_results(origin, destination, date)
            
            return flights
            
        except Exception as e:
            self.logger.error(f"Error searching flights: {e}")
            return []
    
    def extract_flight_results(self, origin, destination, date):
        """Extract flight information from search results"""
        flights = []
        
        try:
            # Wait for results to load
            time.sleep(3)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Look for flight result containers
            flight_containers = soup.find_all(['div', 'tr'], class_=lambda x: x and ('flight' in x.lower() or 'result' in x.lower()))
            
            if not flight_containers:
                # Try different selectors
                flight_containers = soup.find_all('tr', class_=lambda x: x and 'row' in x.lower())
            
            self.logger.info(f"Found {len(flight_containers)} flight containers")
            
            for container in flight_containers:
                try:
                    flight_data = {
                        'origin': origin['name'],
                        'origin_code': origin['code'],
                        'destination': destination['name'],
                        'destination_code': destination['code'],
                        'search_date': date.strftime("%Y-%m-%d"),
                        'flight_number': '',
                        'departure_time': '',
                        'arrival_time': '',
                        'duration': '',
                        'stops': '',
                        'aircraft': '',
                        'days_of_week': '',
                        'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Extract flight number
                    flight_num = container.find(['span', 'td'], class_=lambda x: x and ('flight' in x.lower() or 'number' in x.lower()))
                    if flight_num:
                        flight_data['flight_number'] = flight_num.get_text(strip=True)
                    
                    # Extract times
                    times = container.find_all(['span', 'td'], class_=lambda x: x and 'time' in x.lower())
                    if len(times) >= 2:
                        flight_data['departure_time'] = times[0].get_text(strip=True)
                        flight_data['arrival_time'] = times[1].get_text(strip=True)
                    
                    # Extract duration
                    duration = container.find(['span', 'td'], class_=lambda x: x and 'duration' in x.lower())
                    if duration:
                        flight_data['duration'] = duration.get_text(strip=True)
                    
                    # Extract stops
                    stops = container.find(['span', 'td'], class_=lambda x: x and 'stop' in x.lower())
                    if stops:
                        flight_data['stops'] = stops.get_text(strip=True)
                    
                    # Only add if we have flight number
                    if flight_data['flight_number']:
                        flights.append(flight_data)
                        
                except Exception as e:
                    self.logger.warning(f"Error extracting flight data: {e}")
                    continue
            
            self.logger.info(f"Extracted {len(flights)} flights")
            
        except Exception as e:
            self.logger.error(f"Error extracting flight results: {e}")
        
        return flights
    
    def scrape_all_routes_year(self, start_date=None, days_interval=1, check_both_directions=True):
        """
        Scrape ALL routes worldwide over a full year period
        
        Args:
            start_date: Starting date (default: today)
            days_interval: Days between searches (default: 1 for comprehensive coverage)
            check_both_directions: Check both origin->dest and dest->origin (default: True)
        """
        if start_date is None:
            start_date = datetime.now()
        
        self.logger.info("="*100)
        self.logger.info("🌍 EGYPTAIR COMPREHENSIVE WORLDWIDE FLIGHT SCHEDULE SCRAPER 🌍")
        self.logger.info("="*100)
        self.logger.info("📋 Configuration:")
        self.logger.info(f"   • Start Date: {start_date.strftime('%Y-%m-%d')}")
        self.logger.info(f"   • Period: Full Year (365 days)")
        self.logger.info(f"   • Days Interval: {days_interval} day(s)")
        self.logger.info(f"   • Bidirectional: {check_both_directions}")
        self.logger.info("="*100)
        
        try:
            # Setup driver with stealth mode
            self.setup_driver()
            
            # Simulate human visiting homepage first
            self.logger.info("🏠 Visiting homepage first (human behavior)...")
            self.driver.get("https://www.egyptair.com/")
            self.human_delay(3, 5)
            self.random_scroll()
            self.random_mouse_movement()
            
            # Get all worldwide destinations
            destinations = self.get_all_destinations()
            self.worldwide_destinations = destinations
            self.logger.info(f"✅ Loaded {len(destinations)} worldwide destinations")
            
            # Generate comprehensive date range
            dates = []
            current_date = start_date
            end_date = start_date + timedelta(days=365)
            
            while current_date <= end_date:
                dates.append(current_date)
                current_date += timedelta(days=days_interval)
            
            self.logger.info(f"📅 Generated {len(dates)} date points across the year")
            
            # ALL Egyptian cities as origins (not just Cairo)
            egyptian_origins = [d for d in destinations if d.get('country') == 'Egypt']
            self.logger.info(f"🇪🇬 Egyptian origins: {len(egyptian_origins)}")
            
            # All non-Egyptian destinations
            international_destinations = [d for d in destinations if d.get('country') != 'Egypt']
            self.logger.info(f"🌍 International destinations: {len(international_destinations)}")
            
            # Calculate total routes to scrape
            total_routes_estimate = len(egyptian_origins) * len(destinations)
            if check_both_directions:
                total_routes_estimate *= 2
            total_searches_estimate = total_routes_estimate * len(dates)
            
            self.logger.info("="*100)
            self.logger.info(f"📊 SCRAPING PLAN:")
            self.logger.info(f"   • Routes to check: ~{total_routes_estimate:,}")
            self.logger.info(f"   • Total searches: ~{total_searches_estimate:,}")
            self.logger.info(f"   • Estimated time: {total_searches_estimate * 10 / 3600:.1f} hours")
            self.logger.info("="*100)
            
            input("\n⚠️  This is a comprehensive scrape. Press Enter to continue or Ctrl+C to cancel...")
            
            total_routes_done = 0
            total_flights_found = 0
            
            # Loop through ALL Egyptian origins
            for origin_idx, origin in enumerate(egyptian_origins, 1):
                self.logger.info("\n" + "="*100)
                self.logger.info(f"🛫 ORIGIN {origin_idx}/{len(egyptian_origins)}: {origin['name']} ({origin['code']}) - {origin['country']}")
                self.logger.info("="*100)
                
                # Loop through ALL destinations (including domestic and international)
                for dest_idx, destination in enumerate(destinations, 1):
                    if origin['code'] == destination['code']:
                        continue  # Skip same city
                    
                    total_routes_done += 1
                    
                    self.logger.info(f"\n📍 Route {total_routes_done}: {origin['name']} → {destination['name']} ({destination['country']})")
                    
                    # Check ALL dates for this route
                    route_flights = 0
                    for date_idx, date in enumerate(dates, 1):
                        flights = self.search_flights(origin, destination, date)
                        
                        if flights:
                            self.all_flights.extend(flights)
                            route_flights += len(flights)
                            total_flights_found += len(flights)
                            self.logger.info(f"   ✅ Date {date_idx}/{len(dates)} ({date.strftime('%Y-%m-%d')}): Found {len(flights)} flight(s)")
                        else:
                            self.logger.info(f"   ⚪ Date {date_idx}/{len(dates)} ({date.strftime('%Y-%m-%d')}): No flights")
                        
                        # Human-like delay between date searches
                        self.human_delay(3, 6)
                        
                        # Random break every 10 searches
                        if date_idx % 10 == 0:
                            self.logger.info("   ☕ Taking a short break (human behavior)...")
                            self.random_scroll()
                            self.random_mouse_movement()
                            self.human_delay(10, 20)
                    
                    self.logger.info(f"   📊 Route total: {route_flights} flights")
                    
                    # Delay between routes
                    self.human_delay(5, 10)
                    
                    # Longer break every 20 routes
                    if total_routes_done % 20 == 0:
                        self.logger.info(f"\n🎉 Milestone: {total_routes_done} routes completed, {total_flights_found} flights found")
                        self.logger.info("☕ Taking extended break (30-60 seconds)...")
                        self.human_delay(30, 60)
                        
                        # Save progress
                        if self.all_flights:
                            temp_file = self.save_to_csv(f"egyptair_progress_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
                            self.logger.info(f"💾 Progress saved to: {temp_file}")
                
                # Check reverse direction if enabled
                if check_both_directions:
                    self.logger.info(f"\n🔄 Checking reverse routes FROM international destinations TO {origin['name']}")
                    
                    for destination in international_destinations:
                        if origin['code'] == destination['code']:
                            continue
                        
                        total_routes_done += 1
                        self.logger.info(f"\n📍 Route {total_routes_done}: {destination['name']} → {origin['name']}")
                        
                        route_flights = 0
                        for date in dates:
                            flights = self.search_flights(destination, origin, date)
                            
                            if flights:
                                self.all_flights.extend(flights)
                                route_flights += len(flights)
                                total_flights_found += len(flights)
                            
                            self.human_delay(3, 6)
                        
                        self.logger.info(f"   📊 Route total: {route_flights} flights")
                        self.human_delay(5, 10)
            
            self.logger.info("="*80)
            self.logger.info(f"SCRAPING COMPLETE: Found {len(self.all_flights)} flights")
            self.logger.info("="*80)
            
            return self.all_flights
            
        except Exception as e:
            self.logger.error(f"Error during scraping: {e}")
            return self.all_flights
            
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed")
    
    def save_to_csv(self, filename=None):
        """Save scraped flights to CSV"""
        if not self.all_flights:
            self.logger.warning("No flights to save")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"egyptair_flights_{timestamp}.csv"
        
        Config.ensure_directories()
        filepath = Config.get_output_path(filename)
        
        df = pd.DataFrame(self.all_flights)
        
        # Add UTF-8 BOM for Excel compatibility
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        self.logger.info(f"✅ Saved {len(self.all_flights)} flights to: {filepath}")
        
        return filepath
    
    def get_statistics(self):
        """Get statistics about scraped flights"""
        if not self.all_flights:
            return {}
        
        df = pd.DataFrame(self.all_flights)
        
        stats = {
            'total_flights': len(df),
            'unique_routes': len(df[['origin_code', 'destination_code']].drop_duplicates()),
            'unique_flight_numbers': df['flight_number'].nunique(),
            'origins': df['origin'].unique().tolist(),
            'destinations': df['destination'].unique().tolist(),
            'date_range': f"{df['search_date'].min()} to {df['search_date'].max()}"
        }
        
        return stats


def main():
    """Main function for standalone execution"""
    logger = ScraperLogger('egyptair_main')
    scraper = EgyptAirFlightScraper(logger)
    
    # Scrape flights for the next year
    # Sample every 7 days to reduce load
    flights = scraper.scrape_all_routes_year(days_interval=7)
    
    # Save results
    if flights:
        filepath = scraper.save_to_csv()
        
        # Print statistics
        stats = scraper.get_statistics()
        print("\n" + "="*80)
        print("EGYPTAIR FLIGHT SCRAPING STATISTICS")
        print("="*80)
        print(f"Total Flights: {stats['total_flights']}")
        print(f"Unique Routes: {stats['unique_routes']}")
        print(f"Unique Flight Numbers: {stats['unique_flight_numbers']}")
        print(f"Date Range: {stats['date_range']}")
        print(f"Origins ({len(stats['origins'])}): {', '.join(stats['origins'][:10])}...")
        print(f"Destinations ({len(stats['destinations'])}): {', '.join(stats['destinations'][:10])}...")
        print("="*80)
        print(f"\n✅ Data saved to: {filepath}")
    else:
        print("❌ No flights were scraped")


if __name__ == "__main__":
    main()
