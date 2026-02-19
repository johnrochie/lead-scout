#!/usr/bin/env python3
"""
Full Dublin Business Scrape
Get 100+ businesses across multiple categories
"""

import time
import random
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.google_maps_api import GoogleMapsPlacesScraper

def main():
    print("=== FULL DUBLIN BUSINESS SCRAPE ===")
    print("Getting 100+ businesses across 10 categories...")
    print("")
    
    # Initialize scraper - will use environment variable
    scraper = GoogleMapsPlacesScraper()
    
    # Dublin business categories
    categories = [
        ('restaurants', 15),
        ('dentists', 10),
        ('plumbers', 10),
        ('cafes', 10),
        ('hotels', 10),
        ('electricians', 10),
        ('solicitors', 10),
        ('accountants', 10),
        ('hairdressers', 10),
        ('builders', 10)
    ]
    
    all_businesses = []
    
    for category, max_results in categories:
        print(f"📊 Scraping: {category} ({max_results} businesses)")
        
        businesses = scraper.search_businesses(
            query=category,
            location="Dublin, Ireland",
            max_results=max_results
        )
        
        all_businesses.extend(businesses)
        print(f"   Found: {len(businesses)} businesses")
        print(f"   Total so far: {len(all_businesses)}")
        print("")
        
        # Random delay to avoid rate limits
        delay = random.uniform(3, 6)
        time.sleep(delay)
    
    # Save all businesses
    if all_businesses:
        scraper.save_to_csv(all_businesses, 'data/full_dublin_businesses.csv')
        
        # Quick stats
        websites_found = sum(1 for b in all_businesses if b['website'])
        print("="*50)
        print("🎉 SCRAPE COMPLETE!")
        print("="*50)
        print(f"Total businesses: {len(all_businesses)}")
        print(f"With websites: {websites_found} ({websites_found/len(all_businesses)*100:.1f}%)")
        print(f"Without websites: {len(all_businesses) - websites_found}")
        print(f"Estimated API cost: ${len(all_businesses) * 0.00005:.4f}")
        print("")
        print("📁 Saved to: data/full_dublin_businesses.csv")
        print("")
        print("🎯 Next: Run website analysis to identify leads")
        
        # Show sample
        print("\n=== SAMPLE BUSINESSES ===")
        for i, biz in enumerate(all_businesses[:3], 1):
            has_site = "✅" if biz['website'] else "❌"
            print(f"{has_site} {biz['name']} ({biz['category']})")
            print(f"   Phone: {biz['phone']}")
            if biz['website']:
                print(f"   Website: {biz['website']}")
            else:
                print(f"   Website: NO WEBSITE - PERFECT LEAD!")
            print()
    else:
        print("❌ No businesses collected")

if __name__ == "__main__":
    main()