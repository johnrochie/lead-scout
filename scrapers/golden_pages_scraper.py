#!/usr/bin/env python3
"""
Golden Pages Ireland Scraper
Real business data for Dublin
"""

import requests
import time
import csv
import re
from bs4 import BeautifulSoup
import random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}

def search_golden_pages(query, location="Dublin", max_results=20):
    """Search Golden Pages for businesses"""
    base_url = "https://www.goldenpages.ie"
    
    # Golden Pages search pattern
    search_url = f"{base_url}/q/{query}/{location}/"
    
    print(f"Searching Golden Pages: {query} in {location}")
    
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        businesses = []
        
        # Look for business listings - Golden Pages structure
        listings = soup.find_all('div', {'class': ['listing', 'result']})
        
        if not listings:
            # Try alternative class names
            listings = soup.find_all('article', {'class': 'listing'})
        
        print(f"Found {len(listings)} listings on page")
        
        for listing in listings[:max_results]:
            business = extract_golden_pages_info(listing, query)
            if business:
                businesses.append(business)
        
        return businesses
        
    except Exception as e:
        print(f"Error searching Golden Pages: {e}")
        return []

def extract_golden_pages_info(listing, category):
    """Extract business info from Golden Pages listing"""
    try:
        # Name
        name_elem = listing.find('h2') or listing.find('h3') or listing.find('a', {'class': 'listing__title'})
        name = name_elem.get_text(strip=True) if name_elem else "Unknown"
        
        # Address
        address_elem = listing.find('p', {'class': 'listing__address'}) or \
                      listing.find('address') or \
                      listing.find('div', {'class': 'address'})
        address = address_elem.get_text(strip=True) if address_elem else ""
        
        # Phone
        phone_elem = listing.find('a', {'href': re.compile(r'^tel:')}) or \
                    listing.find('span', {'class': 'phone'}) or \
                    listing.find('div', {'class': 'telephone'})
        phone = phone_elem.get_text(strip=True) if phone_elem else ""
        
        # Website
        website_elem = listing.find('a', {'href': re.compile(r'^https?://')})
        website = ""
        if website_elem and website_elem.get('href'):
            href = website_elem['href']
            if 'goldenpages.ie' not in href:  # Don't include Golden Pages links
                website = href
        
        # Clean up data
        if address and 'Dublin' not in address and 'Co. Dublin' not in address:
            address = f"{address}, Dublin"  # Ensure Dublin location
        
        return {
            'name': name,
            'address': address,
            'website': website,
            'phone': phone,
            'category': category,
            'location': 'Dublin, Ireland',
            'source': 'goldenpages.ie'
        }
    except Exception as e:
        print(f"Error extracting Golden Pages info: {e}")
        return None

def save_to_csv(businesses, filename):
    """Save businesses to CSV"""
    if not businesses:
        print("No businesses to save")
        return
    
    fieldnames = ['name', 'address', 'website', 'phone', 'category', 'location', 'source']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for business in businesses:
            writer.writerow(business)
    
    print(f"✅ Saved {len(businesses)} businesses to {filename}")

def test_golden_pages():
    """Test Golden Pages scraper with real data"""
    print("=== TESTING GOLDEN PAGES SCRAPER ===")
    print("This will fetch real Dublin business data...")
    
    # Start with small test
    search_terms = ['restaurants', 'dentists']
    all_businesses = []
    
    for term in search_terms:
        print(f"\nSearching: {term}")
        businesses = search_golden_pages(term, max_results=5)
        print(f"Found: {len(businesses)} businesses")
        all_businesses.extend(businesses)
        
        # Be polite - random delay between requests
        delay = random.uniform(2, 4)
        time.sleep(delay)
    
    if all_businesses:
        save_to_csv(all_businesses, 'data/golden_pages_test.csv')
        print(f"\n✅ Saved {len(all_businesses)} real businesses")
        
        print("\n=== SAMPLE REAL RESULTS ===")
        for i, biz in enumerate(all_businesses[:5], 1):
            print(f"{i}. {biz['name']} ({biz['category']})")
            print(f"   Address: {biz['address']}")
            print(f"   Website: {biz['website'] or 'Not found'}")
            print(f"   Phone: {biz['phone'] or 'Not found'}")
            print()
        
        # Quick analysis
        websites_found = sum(1 for b in all_businesses if b['website'])
        print(f"📊 Quick stats:")
        print(f"   Total businesses: {len(all_businesses)}")
        print(f"   With website: {websites_found} ({websites_found/len(all_businesses)*100:.1f}%)")
        print(f"   Without website: {len(all_businesses) - websites_found}")
        
    else:
        print("\n❌ No businesses found from Golden Pages")
        print("   This could be due to:")
        print("   - Website structure changed")
        print("   - Network/blocking issues")
        print("   - Need to adjust scraping logic")

def full_scrape(output_file='data/golden_pages_full.csv'):
    """Full scrape of Dublin businesses"""
    print("=== FULL GOLDEN PAGES SCRAPE ===")
    
    # Common business categories in Dublin
    categories = [
        'restaurants', 'dentists', 'plumbers', 'cafes', 'hotels',
        'electricians', 'solicitors', 'accountants', 'doctors',
        'hairdressers', 'builders', 'carpenters', 'painters'
    ]
    
    all_businesses = []
    
    for category in categories:
        print(f"\nScraping: {category}")
        businesses = search_golden_pages(category, max_results=15)
        print(f"Found: {len(businesses)} businesses")
        all_businesses.extend(businesses)
        
        # Random delay to avoid blocking
        delay = random.uniform(3, 6)
        time.sleep(delay)
        
        # Save progress every 3 categories
        if len(all_businesses) >= 20:
            save_to_csv(all_businesses, output_file)
    
    # Final save
    if all_businesses:
        save_to_csv(all_businesses, output_file)
        print(f"\n🎉 COMPLETE: Saved {len(all_businesses)} Dublin businesses")
    else:
        print("\n❌ No businesses collected")

if __name__ == "__main__":
    # Run test first
    test_golden_pages()