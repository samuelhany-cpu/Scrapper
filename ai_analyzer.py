import json
import os
from config import Config

class AIContentAnalyzer:
    def __init__(self, logger):
        self.logger = logger
        self.client = None
        self.ai_type = None
        
        # Try different AI providers in order of preference
        if self._init_gemini():
            pass
        elif self._init_groq():
            pass
        elif self._init_openai():
            pass
        else:
            self.logger.warning("No AI API key found. AI analysis will be disabled.")
            self.logger.info("To enable AI: Add GEMINI_API_KEY, GROQ_API_KEY, or OPENAI_API_KEY to .env file")
    
    def _init_gemini(self):
        """Initialize Google Gemini (FREE)"""
        gemini_key = os.getenv('GEMINI_API_KEY') or Config.__dict__.get('GEMINI_API_KEY')
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                self.client = genai.GenerativeModel('gemini-2.5-flash')  # Latest stable model
                self.ai_type = 'gemini'
                self.logger.info("AI analyzer initialized with Google Gemini 2.5 Flash (FREE)")
                return True
            except ImportError:
                self.logger.warning("Google Gemini library not installed. Run: pip install google-generativeai")
                return False
            except Exception as e:
                self.logger.warning(f"Failed to initialize Gemini: {str(e)}")
                return False
        return False
    
    def _init_groq(self):
        """Initialize Groq (FREE)"""
        groq_key = os.getenv('GROQ_API_KEY') or Config.__dict__.get('GROQ_API_KEY')
        if groq_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=groq_key)
                self.ai_type = 'groq'
                self.logger.info("AI analyzer initialized with Groq (FREE)")
                return True
            except ImportError:
                self.logger.warning("Groq library not installed. Run: pip install groq")
                return False
            except Exception as e:
                self.logger.warning(f"Failed to initialize Groq: {str(e)}")
                return False
        return False
    
    def _init_openai(self):
        """Initialize OpenAI (PAID)"""
        if Config.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
                self.ai_type = 'openai'
                self.logger.info("AI analyzer initialized with OpenAI")
                return True
            except Exception as e:
                self.logger.warning(f"Failed to initialize OpenAI: {str(e)}")
                return False
        return False
    
    def _call_ai(self, prompt, system_message="You are a helpful assistant."):
        """Universal AI calling method that works with all providers"""
        try:
            if self.ai_type == 'gemini':
                # Google Gemini
                full_prompt = f"{system_message}\n\n{prompt}"
                response = self.client.generate_content(full_prompt)
                return response.text
                
            elif self.ai_type == 'groq':
                # Groq
                response = self.client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=Config.AI_TEMPERATURE
                )
                return response.choices[0].message.content
                
            elif self.ai_type == 'openai':
                # OpenAI
                response = self.client.chat.completions.create(
                    model=Config.AI_MODEL,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=Config.AI_TEMPERATURE,
                    response_format={"type": "json_object"}
                )
                return response.choices[0].message.content
            
            return None
        except Exception as e:
            self.logger.error(f"AI call failed: {str(e)}")
            return None
    
    def analyze_page_structure(self, html_content, url):
        """Analyze page structure and identify data patterns using AI"""
        if not self.client:
            self.logger.debug("AI analysis skipped - no API key")
            return None
        
        try:
            prompt = f"""Analyze this webpage HTML and identify the main data structure.
            
URL: {url}

Identify:
1. What type of content is this? (e.g., product listing, article, table data, blog post)
2. What are the main data fields present? (e.g., title, price, description, author, date)
3. What is the best way to structure this data for CSV export?
4. Are there repeating patterns or lists of items?

HTML Preview (first 5000 chars):
{html_content[:5000]}

Return a JSON object with:
- content_type: string
- data_fields: list of field names
- structure_type: "single_item" or "multiple_items"
- recommended_columns: list of column names for CSV
- extraction_hints: object with CSS selectors or patterns for each field

Be specific and practical. Respond ONLY with valid JSON."""

            system_msg = "You are an expert web scraping analyst. Analyze HTML structure and provide practical extraction guidance in JSON format."
            
            response_text = self._call_ai(prompt, system_msg)
            
            if response_text:
                # Extract JSON from response (some models may include extra text)
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                    self.logger.info(f"AI Analysis: {analysis.get('content_type', 'Unknown')} - {analysis.get('structure_type', 'Unknown')}")
                    return analysis
            
            return None
            
        except Exception as e:
            self.logger.error(f"AI analysis failed: {str(e)}")
            return None
    
    def extract_structured_data(self, html_content, schema_hint=None):
        """Use AI to extract structured data from HTML"""
        if not self.client:
            return None
        
        try:
            schema_text = f"\nExpected schema: {json.dumps(schema_hint)}" if schema_hint else ""
            
            prompt = f"""Extract all meaningful data from this HTML content.{schema_text}

HTML Content (first 6000 chars):
{html_content[:6000]}

Extract data in a structured format. Return JSON with:
- data: array of objects, where each object represents one data item/record
- metadata: object with title, description, and any other page-level info

Focus on extracting actual content, not navigation or UI elements.
If this is a single page (article, product), return one item.
If this is a listing page, return multiple items.

Respond ONLY with valid JSON."""

            system_msg = "You are an expert at extracting structured data from HTML. Extract clean, accurate data."
            
            response_text = self._call_ai(prompt, system_msg)
            
            if response_text:
                # Extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    extracted = json.loads(json_match.group())
                    return extracted
            
            return None
            
        except Exception as e:
            self.logger.error(f"AI extraction failed: {str(e)}")
            return None
    
    def is_available(self):
        return self.client is not None
