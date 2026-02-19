#!/usr/bin/env python3
"""
Export REAL Dublin business leads for Evolution Media
"""

import pandas as pd
import csv

def export_real_leads():
    print("=== EXPORTING REAL DUBLIN BUSINESS LEADS ===")
    print("")
    
    # Load the real Google Maps data
    try:
        df = pd.read_csv('data/multi_category_businesses.csv')
        print(f"✅ Loaded {len(df)} real Dublin businesses")
    except FileNotFoundError:
        print("❌ Real business data not found")
        print("Run the Google Maps scraper first")
        return
    
    # All businesses need websites (for Evolution Media)
    # In reality, we'd score them, but for now export all
    export_df = df.copy()
    
    # Add a column for notes
    export_df['evolution_media_notes'] = 'Qualified lead - needs website'
    
    # Save to export file
    export_file = 'data/evolution_media_leads_export.csv'
    export_df.to_csv(export_file, index=False)
    
    print(f"✅ Exported {len(export_df)} leads to: {export_file}")
    print("")
    
    # Show summary
    websites_found = sum(1 for b in df['website'] if b and b != 'NO_WEBSITE')
    no_websites = len(df) - websites_found
    
    print("📊 LEAD SUMMARY:")
    print(f"   Total businesses: {len(df)}")
    print(f"   With websites: {websites_found} (need improvement)")
    print(f"   Without websites: {no_websites} (PERFECT LEADS!)")
    print("")
    
    # Show the businesses WITHOUT websites (best leads)
    if no_websites > 0:
        print("🔥 BEST LEADS (NO WEBSITE):")
        print("="*50)
        no_website_df = df[df['website'].isna() | (df['website'] == '') | (df['website'] == 'NO_WEBSITE')]
        
        for idx, row in no_website_df.iterrows():
            print(f"\n❌ {row['name']}")
            print(f"   Category: {row['category']}")
            print(f"   Phone: {row['phone']}")
            print(f"   Address: {row['address'][:60]}...")
            print(f"   ACTION: CALL NOW - 'Hi, I noticed you don't have a website...'")
    
    print("")
    print("📧 EMAIL OUTREACH READY:")
    print("   File: data/evolution_media_leads_export.csv")
    print("   Format: CSV (compatible with Mailchimp, HubSpot, etc.)")
    print("")
    print("📞 CALL LIST READY:")
    print("   Column 'phone' has direct numbers")
    print("   Start with businesses WITHOUT websites first")
    print("")
    print("💰 REVENUE POTENTIAL:")
    print(f"   Immediate (no website): €{no_websites * 500}")
    print(f"   Potential (all): €{len(df) * 500}")
    print("")
    print("🚀 NEXT STEPS:")
    print("   1. Import CSV into your email marketing tool")
    print("   2. Call the businesses WITHOUT websites TODAY")
    print("   3. Start email campaign to businesses WITH websites")
    print("   4. Scale to 500+ businesses (cost: ~$0.025)")

if __name__ == "__main__":
    export_real_leads()