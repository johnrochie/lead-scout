#!/usr/bin/env python3
"""
Google Maps Places API Scraper
Legal, reliable business data for Dublin
"""

import requests
import time
import csv
import json
import os
from typing import List, Dict, Optional

class GoogleMapsPlacesScraper:
    def __init__(self, api_key: str = None):
        # Get API key from environment variable if not provided
        if api_key is None:
            api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
            if not api_key or api_key == "YOUR_API_KEY_HERE":
                raise ValueError(
                    "Google Maps API key not found. "
                    "Set GOOGLE_MAPS_API_KEY environment variable or pass api_key parameter. "
                    "Get key from: https://console.cloud.google.com"
                )
        
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        self.details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        
    def search_businesses(self, query: str, location: str = "Dublin, Ireland", max_results: int = 20) -> List[Dict]:
        """Search for businesses using Google Places API"""
        print(f"Searching Google Places: {query} in {location}")
        
        businesses = []
        next_page_token = None
        
        try:
            # Initial search
            params = {
                'query': f"{query} {location}",
                'key': self.api_key,
                'type': 'establishment'
            }
            
            while len(businesses) < max_results:
                if next_page_token:
                    params['pagetoken'] = next_page_token
                    time.sleep(2)  # Required between page requests
                
                response = requests.get(self.base_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if data['status'] != 'OK':
                    print(f"API Error: {data.get('status', 'UNKNOWN')}")
                    break
                
                # Process results
                for place in data.get('results', []):
                    if len(businesses) >= max_results:
                        break
                    
                    # Get detailed info including website
                    detailed_info = self.get_place_details(place['place_id'])
                    if detailed_info:
                        businesses.append(detailed_info)
                
                # Check for next page
                next_page_token = data.get('next_page_token')
                if not next_page_token:
                    break
            
            print(f"Found {len(businesses)} businesses")
            return businesses
            
        except Exception as e:
            print(f"Error searching Google Places: {e}")
            return []
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """Get detailed information for a place including website"""
        try:
            params = {
                'place_id': place_id,
                'key': self.api_key,
                'fields': 'name,formatted_address,website,formatted_phone_number,types,rating,user_ratings_total'
            }
            
            response = requests.get(self.details_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != 'OK':
                return None
            
            result = data['result']
            
            # Determine category from types
            category = self._determine_category(result.get('types', []))
            
            return {
                'name': result.get('name', 'Unknown'),
                'address': result.get('formatted_address', ''),
                'website': result.get('website', ''),
                'phone': result.get('formatted_phone_number', ''),
                'category': category,
                'location': 'Dublin, Ireland',
                'place_id': place_id,
                'rating': result.get('rating'),
                'reviews': result.get('user_ratings_total'),
                'source': 'google_places_api'
            }
            
        except Exception as e:
            print(f"Error getting place details: {e}")
            return None
    
    def _determine_category(self, types: List[str]) -> str:
        """Determine business category from Google Places types"""
        category_map = {
            'restaurant': ['restaurant', 'food', 'meal_takeaway', 'meal_delivery'],
            'dentist': ['dentist', 'dental_clinic'],
            'plumber': ['plumber', 'plumbing'],
            'cafe': ['cafe', 'coffee_shop'],
            'hotel': ['lodging', 'hotel'],
            'electrician': ['electrician'],
            'doctor': ['doctor', 'physician', 'health'],
            'lawyer': ['lawyer', 'attorney'],
            'accountant': ['accounting'],
            'hairdresser': ['hair_care', 'beauty_salon'],
            'builder': ['general_contractor', 'home_builder'],
            'retail': ['store', 'shopping_mall']
        }
        
        for category, type_list in category_map.items():
            if any(t in types for t in type_list):
                return category
        
        return 'other'
    
    def save_to_csv(self, businesses: List[Dict], filename: str):
        """Save businesses to CSV"""
        if not businesses:
            print("No businesses to save")
            return
        
        fieldnames = ['name', 'address', 'website', 'phone', 'category', 'location', 'rating', 'reviews', 'place_id', 'source']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for business in businesses:
                writer.writerow(business)
        
        print(f"✅ Saved {len(businesses)} businesses to {filename}")
        
        # Stats
        websites_found = sum(1 for b in businesses if b['website'])
        print(f"📊 Stats: {websites_found}/{len(businesses)} have websites ({websites_found/len(businesses)*100:.1f}%)")

def test_with_mock_api():
    """Test with mock data (replace with real API key)"""
    print("=== GOOGLE MAPS PLACES API SCRAPER ===")
    print("NOTE: Replace 'YOUR_API_KEY' with actual Google Maps API key")
    print("Get key from: https://console.cloud.google.com")
    print("Enable 'Places API' and restrict to your IP")
    print("")
    
    # Get API key from environment variable or use placeholder
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY", "YOUR_API_KEY_HERE")
    
    if api_key == "YOUR_API_KEY_HERE":
        print("❌ Please get a Google Maps API key from:")
        print("   https://console.cloud.google.com")
        print("   Enable 'Places API'")
        print("   Restrict to IP: 192.168.4.90")
        print("")
        print("For now, showing mock data...")
        
        # Create mock data to demonstrate
        mock_businesses = [
            {
                'name': 'The Old Mill Restaurant',
                'address': '12 Temple Bar, Dublin 2, Ireland',
                'website': 'https://theoldmilldublin.ie',
                'phone': '+353 1 123 4567',
                'category': 'restaurant',
                'location': 'Dublin, Ireland',
                'rating': 4.2,
                'reviews': 156,
                'place_id': 'mock_1',
                'source': 'google_places_api'
            },
            {
                'name': 'Dublin Dental Care',
                'address': '45 Grafton Street, Dublin 2, Ireland',
                'website': 'https://dublindentalcare.ie',
                'phone': '+353 1 987 6543',
                'category': 'dentist',
                'location': 'Dublin, Ireland',
                'rating': 4.5,
                'reviews': 89,
                'place_id': 'mock_2',
                'source': 'google_places_api'
            },
            {
                'name': 'City Plumbing Services',
                'address': '3 Smithfield, Dublin 7, Ireland',
                'website': '',  # No website - perfect lead!
                'phone': '+353 86 123 4567',
                'category': 'plumber',
                'location': 'Dublin, Ireland',
                'rating': 4.0,
                'reviews': 23,
                'place_id': 'mock_3',
                'source': 'google_places_api'
            }
        ]
        
        scraper = GoogleMapsPlacesScraper(api_key)
        scraper.save_to_csv(mock_businesses, 'data/google_maps_mock.csv')
        
        print("\n=== MOCK RESULTS (Real API will get 100s of businesses) ===")
        for biz in mock_businesses:
            has_site = "✅" if biz['website'] else "❌"
            print(f"{has_site} {biz['name']} - {biz['category']}")
            if biz['website']:
                print(f"   Website: {biz['website']}")
            else:
                print(f"   Website: NO WEBSITE - PERFECT LEAD!")
            print(f"   Phone: {biz['phone']}")
            print()
        
        print("\n🎯 With real API key, you can get:")
        print("   • 500+ Dublin businesses per day")
        print("   • Accurate website/contact info")
        print("   • Legal, reliable data")
        print("   • Cost: ~$0.16 for 500 businesses")
        
    else:
        # Real API key provided
        scraper = GoogleMapsPlacesScraper(api_key)
        
        # Test search
        businesses = scraper.search_businesses('restaurants', max_results=10)
        scraper.save_to_csv(businesses, 'data/google_maps_real.csv')

if __name__ == "__main__":
    test_with_mock_api()