#!/usr/bin/env python3
"""
Test script for Google Maps scraper
Run a small test first
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.google_maps_scraper import search_google_maps, save_to_csv

def test_small():
    """Test with just 2 businesses per category"""
    print("=== TESTING GOOGLE MAPS SCRAPER ===")
    print("Searching for Dublin businesses...")
    
    search_terms = ['restaurants', 'dentists']
    all_businesses = []
    
    for term in search_terms:
        print(f"\nSearching: {term}")
        businesses = search_google_maps(term, max_results=2)
        print(f"Found: {len(businesses)} businesses")
        all_businesses.extend(businesses)
    
    # Save test results
    if all_businesses:
        save_to_csv(all_businesses, 'data/test_leads.csv')
        print(f"\n✅ Saved {len(all_businesses)} test businesses to data/test_leads.csv")
        
        # Show what we got
        print("\n=== TEST RESULTS ===")
        for i, biz in enumerate(all_businesses, 1):
            print(f"{i}. {biz['name']} ({biz['category']})")
            print(f"   Address: {biz['address']}")
            print(f"   Website: {biz['website'] or 'Not found'}")
            print(f"   Phone: {biz['phone'] or 'Not found'}")
            print()
    else:
        print("\n❌ No businesses found. Google Maps structure may have changed.")
        print("We might need to use a different approach or library.")

if __name__ == "__main__":
    test_small()