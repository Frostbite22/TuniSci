import requests
import json
import re
import time
import random
from pathlib import Path
from datetime import datetime
from parsel import Selector
from scholarly import scholarly
from tqdm import tqdm
from typing import Dict, List, Optional
import logging

from tunisian_academic_keywords import TunisianAcademicKeywords

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scholar_scraper.log'),
        logging.StreamHandler()
    ]
)

class ScholarScraper:
    def __init__(self, output_dir: str = "data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize scholarly without proxy to avoid compatibility issues
        self._configure_scholarly()
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
        }
        
        # Initialize Tunisian keywords
        self.keywords = TunisianAcademicKeywords()

    def _configure_scholarly(self):
        """Configure scholarly with basic settings."""
        try:
            scholarly.use_defaults()
        except Exception as e:
            logging.warning(f"Failed to configure scholarly with defaults: {str(e)}")

    def _get_search_query(self) -> str:
        """Generate the search query using the comprehensive keywords list."""
        return self.keywords.get_search_query()

    def _make_request(self, url: str, params: Dict, retry_count: int = 3) -> Optional[requests.Response]:
        """Make HTTP request with retry mechanism and random delays."""
        for attempt in range(retry_count):
            try:
                # Random delay between requests
                time.sleep(random.uniform(2, 5))
                response = requests.get(url, params=params, headers=self.headers, timeout=30)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == retry_count - 1:
                    logging.error(f"Failed to make request after {retry_count} attempts")
                    return None
                time.sleep(random.uniform(5, 10))  # Longer delay between retries

    def scrape_profiles(self) -> List[Dict]:
        """Scrape Google Scholar profiles."""
        params = {
            "view_op": "search_authors",
            "mauthors": self._get_search_query(),
            "astart": 0
        }
        
        profile_results = []
        
        while True:
            logging.info(f"Extracting authors at page #{params['astart'] // 10 + 1}")
            
            response = self._make_request("https://scholar.google.com/citations", params)
            if not response:
                break
                
            selector = Selector(text=response.text)
            
            # Extract profiles from current page
            for profile in selector.css(".gsc_1usr"):
                profile_data = {
                    "profile_name": profile.css(".gs_ai_name a::text").get(),
                    "profile_link": f'https://scholar.google.com{profile.css(".gs_ai_name a::attr(href)").get()}',
                    "profile_affiliations": profile.css(".gs_ai_aff").xpath("normalize-space()").get(),
                    "profile_email": profile.css(".gs_ai_eml").xpath("normalize-space()").get(),
                    "profile_cited_by": profile.css(".gs_ai_cby::text").get(),
                    "profile_interests": profile.css(".gs_ai_one_int::text").getall(),
                    "scrape_date": datetime.now().isoformat()
                }
                profile_results.append(profile_data)
            
            # Check for next page
            next_button = selector.css("button.gs_btnPR::attr(onclick)").get()
            if not next_button:
                break
                
            # Extract next page token
            after_author_match = re.search(r"after_author\\x3d(.*)\\x26", next_button)
            if not after_author_match:
                break
                
            params["after_author"] = after_author_match.group(1)
            params["astart"] += 10
        
        return profile_results

    def fetch_citation_indices(self, profiles: List[Dict]) -> List[Dict]:
        """Fetch citation indices for each profile using scholarly."""
        for profile in tqdm(profiles, desc="Fetching citation indices"):
            try:
                # Search for author and get first result
                search_query = scholarly.search_author(profile["profile_name"])
                author_data = next(search_query)
                
                # Fill in citation indices
                author_info = scholarly.fill(author_data, sections=['indices'])
                
                # Update profile with citation indices
                profile.update({
                    "hindex": author_info.get('hindex', 0),
                    "hindex5y": author_info.get('hindex5y', 0),
                    "i10index": author_info.get('i10index', 0),
                    "i10index5y": author_info.get('i10index5y', 0)
                })
                
                # Random delay to avoid rate limiting
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logging.error(f"Error fetching indices for {profile['profile_name']}: {str(e)}")
                # Set default values if fetch fails
                profile.update({
                    "hindex": 0,
                    "hindex5y": 0,
                    "i10index": 0,
                    "i10index5y": 0
                })
        
        return profiles

    def save_results(self, data: List[Dict], filename: str):
        """Save results to JSON file with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"{filename}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, indent=2, ensure_ascii=False, fp=f)
        
        logging.info(f"Results saved to {output_file}")

def main():
    # Initialize scraper
    scraper = ScholarScraper()
    
    # Scrape profiles
    logging.info("Starting profile scraping...")
    profiles = scraper.scrape_profiles()
    scraper.save_results(profiles, "authors_raw")
    
    # Fetch citation indices
    logging.info("Fetching citation indices...")
    profiles_with_indices = scraper.fetch_citation_indices(profiles)
    scraper.save_results(profiles_with_indices, "authors_with_indices")
    
    logging.info("Scraping completed successfully!")

if __name__ == "__main__":
    main()