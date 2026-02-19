#!/usr/bin/env python3
"""
Yell.ie Scraper for Dublin Businesses
Simpler than Google Maps
"""

import requests
import time
import csv
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def search_yell(query, location="Dublin", max_results=10):
    """Search Yell.ie for businesses"""
    base_url = "https://www.yell.ie"
    search_url = f"{base_url}/s/{query}/{location}"
    
    print(f"Searching Yell.ie: {query} in {location}")
    
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        businesses = []
        
        # Look for business listings
        listings = soup.find_all('div', {'class': 'businessCapsule'})
        
        for listing in listings[:max_results]:
            business = extract_yell_info(listing, query)
            if business:
                businesses.append(business)
        
        return businesses
        
    except Exception as e:
        print(f"Error searching Yell.ie: {e}")
        return []

def extract_yell_info(listing, category):
    """Extract business info from Yell listing"""
    try:
        # Name
        name_elem = listing.find('h2', {'class': 'businessCapsule--title'})
        name = name_elem.get_text(strip=True) if name_elem else "Unknown"
        
        # Address
        address_elem = listing.find('span', {'itemprop': 'address'})
        address = address_elem.get_text(strip=True) if address_elem else ""
        
        # Phone
        phone_elem = listing.find('span', {'class': 'business--telephoneNumber'})
        phone = phone_elem.get_text(strip=True) if phone_elem else ""
        
        # Website
        website_elem = listing.find('a', {'class': 'businessCapsule--ctaItem'})
        website = website_elem['href'] if website_elem and website_elem.get('href') else ""
        
        return {
            'name': name,
            'address': address,
            'website': website,
            'phone': phone,
            'category': category,
            'location': 'Dublin, Ireland',
            'source': 'yell.ie'
        }
    except Exception as e:
        print(f"Error extracting Yell info: {e}")
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
    
    print(f"Saved {len(businesses)} businesses to {filename}")

def test_yell():
    """Test Yell.ie scraper"""
    print("=== TESTING YELL.IE SCRAPER ===")
    
    search_terms = ['restaurants', 'dentists']
    all_businesses = []
    
    for term in search_terms:
        print(f"\nSearching: {term}")
        businesses = search_yell(term, max_results=3)
        print(f"Found: {len(businesses)} businesses")
        all_businesses.extend(businesses)
        time.sleep(1)  # Be polite
    
    if all_businesses:
        save_to_csv(all_businesses, 'data/yell_test.csv')
        print(f"\n✅ Saved {len(all_businesses)} businesses")
        
        print("\n=== SAMPLE RESULTS ===")
        for i, biz in enumerate(all_businesses[:5], 1):
            print(f"{i}. {biz['name']} ({biz['category']})")
            print(f"   Address: {biz['address']}")
            print(f"   Website: {biz['website'] or 'Not found'}")
            print(f"   Phone: {biz['phone'] or 'Not found'}")
            print()
    else:
        print("\n❌ No businesses found from Yell.ie")

if __name__ == "__main__":
    test_yell()
