#!/usr/bin/env python3
"""
Google Maps Scraper for Dublin Businesses
Extracts: name, address, website, phone, category
"""

import requests
import time
import csv
import re
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def search_google_maps(query, location="Dublin, Ireland", max_results=10):
    """Search Google Maps for businesses"""
    base_url = "https://www.google.com/maps/search/"
    search_query = f"{query}+{location}"
    url = base_url + quote_plus(search_query)
    
    print(f"Searching: {query} in {location}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract business cards (simplified - real scraping needs more work)
        businesses = []
        
        # Look for business listings
        # Note: Google Maps HTML structure changes frequently
        # This is a simplified example
        business_cards = soup.find_all('div', {'class': 'section-result'})
        
        for card in business_cards[:max_results]:
            business = extract_business_info(card, query)
            if business:
                businesses.append(business)
        
        return businesses
        
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return []

def extract_business_info(card, category):
    """Extract business info from a card"""
    try:
        # Name
        name_elem = card.find('h3', {'class': 'section-result-title'})
        name = name_elem.get_text(strip=True) if name_elem else "Unknown"
        
        # Address
        address_elem = card.find('span', {'class': 'section-result-location'})
        address = address_elem.get_text(strip=True) if address_elem else ""
        
        # Phone (might not be in initial listing)
        phone = ""
        
        # Website (usually requires clicking through)
        website = ""
        
        return {
            'name': name,
            'address': address,
            'website': website,
            'phone': phone,
            'category': category,
            'location': 'Dublin, Ireland'
        }
    except Exception as e:
        print(f"Error extracting business info: {e}")
        return None

def save_to_csv(businesses, filename):
    """Save businesses to CSV"""
    if not businesses:
        print("No businesses to save")
        return
    
    fieldnames = ['name', 'address', 'website', 'phone', 'category', 'location']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for business in businesses:
            writer.writerow(business)
    
    print(f"Saved {len(businesses)} businesses to {filename}")

def main():
    """Main function"""
    search_terms = ['restaurants', 'dentists', 'plumbers', 'cafes', 'hotels']
    all_businesses = []
    
    for term in search_terms:
        businesses = search_google_maps(term, max_results=2)  # Small for testing
        all_businesses.extend(businesses)
        time.sleep(2)  # Rate limiting
    
    # Save results
    save_to_csv(all_businesses, '../data/leads.csv')
    
    # Print sample
    print("\n=== SAMPLE RESULTS ===")
    for i, business in enumerate(all_businesses[:5], 1):
        print(f"{i}. {business['name']} - {business['category']}")
        print(f"   Address: {business['address']}")
        print()

if __name__ == "__main__":
    main()