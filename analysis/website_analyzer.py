#!/usr/bin/env python3
"""
Website Analyzer for Lead Scout
Scores websites 0-30 to identify businesses needing Evolution Media
"""

import requests
import re
import time
from urllib.parse import urlparse
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def analyze_website(url, timeout=10):
    """
    Analyze a website and return score 0-30
    Higher score = better website (less need for Evolution Media)
    """
    if not url or url == "NO_WEBSITE" or "http://" not in url and "https://" not in url:
        return {
            'score': 0,
            'has_website': False,
            'details': 'No website found',
            'needs_website': True
        }
    
    try:
        print(f"Analyzing: {url}")
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        html = response.text
        
        score = 0
        details = []
        
        # 1. HTTPS/SSL (2 points)
        if url.startswith('https://'):
            score += 2
            details.append('HTTPS/SSL: +2')
        
        # 2. Mobile friendly check (3 points)
        if 'viewport' in html.lower():
            score += 3
            details.append('Mobile viewport: +3')
        
        # 3. Modern framework detection (3 points)
        modern_frameworks = ['react', 'vue', 'angular', 'next.js', 'nuxt.js', 'svelte']
        if any(framework in html.lower() for framework in modern_frameworks):
            score += 3
            details.append('Modern framework: +3')
        
        # 4. Old tech detection (negative indicators)
        old_tech = ['jquery', 'flash', 'marquee', '<table> for layout', 'frameset']
        old_tech_found = []
        for tech in old_tech:
            if tech in html.lower():
                old_tech_found.append(tech)
        
        if old_tech_found:
            details.append(f'Old tech found: {", ".join(old_tech_found)}')
            # Don't subtract, just don't add points
        
        # 5. Copyright year check (3 points if recent)
        current_year = datetime.now().year
        copyright_pattern = r'copyright.*?(\d{4})'
        match = re.search(copyright_pattern, html.lower())
        if match:
            year = int(match.group(1))
            if year >= current_year - 2:  # Updated in last 2 years
                score += 3
                details.append(f'Recent copyright ({year}): +3')
        
        # 6. Image optimization check (2 points)
        img_tags = len(re.findall(r'<img', html.lower()))
        if img_tags > 0:
            # Check for alt attributes (accessibility)
            alt_imgs = len(re.findall(r'alt=', html.lower()))
            if alt_imgs / max(img_tags, 1) > 0.5:  # More than 50% have alt
                score += 2
                details.append('Good image alt text: +2')
        
        # 7. Contact info detection (2 points)
        contact_patterns = [
            r'contact.*?form', r'@.*?\.(com|ie|eu)', r'phone', r'tel:', r'email'
        ]
        contact_found = sum(1 for pattern in contact_patterns if re.search(pattern, html.lower()))
        if contact_found >= 2:
            score += 2
            details.append('Contact info present: +2')
        
        # 8. Social media links (2 points)
        social_patterns = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com']
        social_found = sum(1 for pattern in social_patterns if pattern in html.lower())
        if social_found >= 1:
            score += 2
            details.append(f'Social media links: +2')
        
        # 9. Professional design indicators (3 points)
        # Check for CSS frameworks, good structure
        css_indicators = ['bootstrap', 'tailwind', 'material', 'font-awesome', 'google-fonts']
        if any(indicator in html.lower() for indicator in css_indicators):
            score += 3
            details.append('CSS framework: +3')
        
        # Cap score at 30
        score = min(score, 30)
        
        # Determine if needs website
        needs_website = score < 15  # Threshold
        
        return {
            'score': score,
            'has_website': True,
            'details': ' | '.join(details),
            'needs_website': needs_website,
            'url': url
        }
        
    except requests.exceptions.RequestException as e:
        print(f"  Error analyzing {url}: {e}")
        return {
            'score': 0,
            'has_website': False,
            'details': f'Error: {str(e)[:50]}',
            'needs_website': True,
            'url': url
        }
    except Exception as e:
        print(f"  Unexpected error analyzing {url}: {e}")
        return {
            'score': 0,
            'has_website': False,
            'details': f'Unexpected error',
            'needs_website': True,
            'url': url
        }

def analyze_businesses_from_csv(csv_file, output_file=None):
    """Analyze businesses from CSV file"""
    import pandas as pd
    
    print(f"=== ANALYZING BUSINESSES FROM {csv_file} ===")
    
    # Read CSV
    df = pd.read_csv(csv_file)
    
    results = []
    for idx, row in df.iterrows():
        print(f"\n{idx+1}/{len(df)}: {row['name']}")
        
        analysis = analyze_website(row['website'])
        
        result = {
            'name': row['name'],
            'address': row['address'],
            'original_website': row['website'],
            'phone': row['phone'],
            'category': row['category'],
            'location': row['location'],
            'score': analysis['score'],
            'has_website': analysis['has_website'],
            'analysis_details': analysis['details'],
            'needs_website': analysis['needs_website']
        }
        results.append(result)
        
        # Be polite to servers
        time.sleep(0.5)
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    # Save if output file specified
    if output_file:
        results_df.to_csv(output_file, index=False)
        print(f"\n✅ Saved analysis to {output_file}")
    
    # Print summary
    print(f"\n=== ANALYSIS SUMMARY ===")
    print(f"Total businesses: {len(results_df)}")
    print(f"With website: {results_df['has_website'].sum()}")
    print(f"Need website (score < 15): {results_df['needs_website'].sum()}")
    
    # Show worst websites
    print(f"\n=== TOP CANDIDATES FOR EVOLUTION MEDIA ===")
    candidates = results_df[results_df['needs_website']].sort_values('score').head(5)
    for idx, row in candidates.iterrows():
        print(f"{row['name']} - Score: {row['score']}/30")
        print(f"  {row['analysis_details'][:100]}...")
        print(f"  Website: {row['original_website']}")
        print()
    
    return results_df

if __name__ == "__main__":
    # Test with mock data
    analyze_businesses_from_csv('data/mock_leads.csv', 'data/analyzed_leads.csv')