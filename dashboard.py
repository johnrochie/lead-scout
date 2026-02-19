#!/usr/bin/env python3
"""
Simple Dashboard for Lead Scout
View and filter potential leads
"""

import pandas as pd
import sys

def show_dashboard(csv_file='data/analyzed_leads.csv'):
    """Display interactive dashboard"""
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"❌ File not found: {csv_file}")
        print("Run the analyzer first: python3 analysis/website_analyzer.py")
        return
    
    print("\n" + "="*60)
    print("LEAD SCOUT DASHBOARD - Evolution Media Lead Generator")
    print("="*60)
    
    # Summary stats
    total = len(df)
    with_website = df['has_website'].sum()
    needs_website = df['needs_website'].sum()
    avg_score = df['score'].mean()
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total businesses: {total}")
    print(f"   With website: {with_website} ({with_website/total*100:.1f}%)")
    print(f"   Need website: {needs_website} ({needs_website/total*100:.1f}%)")
    print(f"   Average score: {avg_score:.1f}/30")
    
    # Score distribution
    print(f"\n📈 SCORE DISTRIBUTION:")
    bins = [0, 5, 10, 15, 20, 25, 30]
    labels = ['0-5 (Critical)', '6-10 (Poor)', '11-15 (Needs Help)', '16-20 (Okay)', '21-25 (Good)', '26-30 (Excellent)']
    
    for i in range(len(bins)-1):
        count = len(df[(df['score'] >= bins[i]) & (df['score'] < bins[i+1])])
        if count > 0:
            print(f"   {labels[i]}: {count} businesses")
    
    # Show worst offenders
    print(f"\n🔴 TOP 5 CANDIDATES (Most Need Evolution Media):")
    candidates = df[df['needs_website']].sort_values('score').head(5)
    
    for idx, row in candidates.iterrows():
        score_color = "🟥" if row['score'] < 5 else "🟧" if row['score'] < 10 else "🟨"
        print(f"\n{score_color} {row['name']}")
        print(f"   Category: {row['category']}")
        print(f"   Score: {row['score']}/30")
        print(f"   Address: {row['address']}")
        print(f"   Phone: {row['phone']}")
        if row['has_website']:
            print(f"   Website: {row['original_website']}")
        else:
            print(f"   Website: ❌ NO WEBSITE")
        print(f"   Analysis: {row['analysis_details'][:80]}...")
    
    # Export options
    print(f"\n💾 EXPORT OPTIONS:")
    print("   1. Export all businesses needing websites")
    print("   2. Export by category")
    print("   3. Export by score range")
    print("   4. View all data")
    print("   5. Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == '1':
        needs_df = df[df['needs_website']]
        export_file = 'data/leads_needing_websites.csv'
        needs_df.to_csv(export_file, index=False)
        print(f"✅ Exported {len(needs_df)} leads to {export_file}")
        
    elif choice == '2':
        categories = df['category'].unique()
        print("\nAvailable categories:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat}")
        
        cat_choice = input("\nSelect category number: ").strip()
        try:
            cat_idx = int(cat_choice) - 1
            selected_cat = categories[cat_idx]
            cat_df = df[df['category'] == selected_cat]
            export_file = f'data/leads_{selected_cat}.csv'
            cat_df.to_csv(export_file, index=False)
            print(f"✅ Exported {len(cat_df)} {selected_cat} leads to {export_file}")
        except:
            print("❌ Invalid selection")
    
    elif choice == '3':
        min_score = input("Minimum score (0-30): ").strip()
        max_score = input("Maximum score (0-30): ").strip()
        try:
            min_score = int(min_score)
            max_score = int(max_score)
            score_df = df[(df['score'] >= min_score) & (df['score'] <= max_score)]
            export_file = f'data/leads_score_{min_score}_to_{max_score}.csv'
            score_df.to_csv(export_file, index=False)
            print(f"✅ Exported {len(score_df)} leads (score {min_score}-{max_score}) to {export_file}")
        except:
            print("❌ Invalid score range")
    
    elif choice == '4':
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(df.to_string())
    
    print("\n🎯 Next steps:")
    print("   - Run on real business data (Golden Pages scraper)")
    print("   - Improve scoring algorithm")
    print("   - Add automated outreach")
    print("   - Integrate with Evolution Media pipeline")

if __name__ == "__main__":
    show_dashboard()