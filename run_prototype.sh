#!/bin/bash
# Lead Scout Prototype - Complete Workflow

echo "=========================================="
echo "LEAD SCOUT PROTOTYPE - Evolution Media"
echo "=========================================="

cd /home/jr/.openclaw/workspace/lead-scout

# Activate virtual environment
source venv/bin/activate

echo ""
echo "1. 📊 GENERATING MOCK BUSINESS DATA"
echo "   (Real scraping needs API/directory access)"
python3 -c "
import pandas as pd
import random

# Generate realistic mock data
categories = ['Restaurant', 'Dentist', 'Plumber', 'Cafe', 'Hotel', 'Electrician', 'Solicitor']
areas = ['Dublin 1', 'Dublin 2', 'Dublin 4', 'Dublin 6', 'Dublin 8', 'Dublin 12']

businesses = []
for i in range(50):
    category = random.choice(categories)
    name = f\"{category} {random.choice(['Premier', 'City', 'Metro', 'Prime', 'Elite'])} {random.choice(['Dublin', 'Capital', 'Irish'])}\"
    
    # Simulate website quality
    has_website = random.random() > 0.3  # 70% have websites
    if has_website:
        website = f\"https://{name.lower().replace(' ', '')}.ie\"
        # Simulate quality
        score = random.randint(0, 30)
        needs_website = score < 15
    else:
        website = \"NO_WEBSITE\"
        score = 0
        needs_website = True
    
    businesses.append({
        'name': name,
        'address': f\"{random.randint(1, 100)} {random.choice(['Main St', 'Grafton St', 'O\\'Connell St', 'Camden St'])}, {random.choice(areas)}\",
        'website': website,
        'phone': f\"+353 {random.randint(1, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}\",
        'category': category,
        'location': 'Dublin, Ireland',
        'mock_score': score,
        'needs_website': needs_website
    })

df = pd.DataFrame(businesses)
df.to_csv('data/mock_realistic.csv', index=False)
print(f\"✅ Generated {len(df)} realistic mock businesses\")
print(f\"   With website: {df[df['website'] != 'NO_WEBSITE'].shape[0]}\")
print(f\"   Need website: {df['needs_website'].sum()}\")
"

echo ""
echo "2. 🔍 ANALYZING WEBSITES"
echo "   (Using mock scoring - real analysis would fetch websites)"
python3 -c "
import pandas as pd
import random

df = pd.read_csv('data/mock_realistic.csv')
results = []

for idx, row in df.iterrows():
    if row['website'] == 'NO_WEBSITE':
        score = 0
        details = 'No website'
        needs_website = True
    else:
        # Use mock score with some variation
        base_score = row['mock_score']
        variation = random.randint(-3, 3)
        score = max(0, min(30, base_score + variation))
        
        # Generate realistic analysis details
        details_parts = []
        if score > 20:
            details_parts.append('Modern design')
            details_parts.append('Mobile friendly')
        elif score > 10:
            details_parts.append('Basic design')
            details_parts.append('Needs improvement')
        else:
            details_parts.append('Poor design')
            details_parts.append('Needs complete rebuild')
        
        if 'https://' in row['website']:
            details_parts.append('HTTPS secure')
        
        details = ' | '.join(details_parts)
        needs_website = score < 15
    
    results.append({
        'name': row['name'],
        'address': row['address'],
        'website': row['website'],
        'phone': row['phone'],
        'category': row['category'],
        'location': row['location'],
        'score': score,
        'analysis_details': details,
        'needs_website': needs_website
    })

results_df = pd.DataFrame(results)
results_df.to_csv('data/analyzed_realistic.csv', index=False)

total = len(results_df)
needs = results_df['needs_website'].sum()
print(f\"✅ Analyzed {total} businesses\")
print(f\"   Need Evolution Media: {needs} ({needs/total*100:.1f}%)\")
print(f\"   Average score: {results_df['score'].mean():.1f}/30\")
"

echo ""
echo "3. 📈 VIEWING DASHBOARD"
echo ""
python3 dashboard.py <<< "5"

echo ""
echo "=========================================="
echo "PROTOTYPE COMPLETE"
echo "=========================================="
echo ""
echo "🎯 WHAT WORKS:"
echo "   • Business data pipeline"
echo "   • Website scoring algorithm (0-30)"
echo "   • Lead qualification (score < 15 = needs Evolution Media)"
echo "   • Dashboard for viewing/filtering leads"
echo ""
echo "🔧 WHAT'S NEEDED FOR PRODUCTION:"
echo "   1. Real business data source (API/directory)"
echo "   2. Real website analysis (fetch & analyze HTML)"
echo "   3. Integration with Evolution Media pipeline"
echo "   4. Automated outreach system"
echo ""
echo "📁 FILES CREATED:"
echo "   • data/mock_realistic.csv - 50 mock Dublin businesses"
echo "   • data/analyzed_realistic.csv - Analysis results"
echo "   • scrapers/ - Scraper templates (needs adjustment)"
echo "   • analysis/website_analyzer.py - Scoring logic"
echo "   • dashboard.py - Interactive dashboard"
echo ""
echo "🚀 NEXT STEPS:"
echo "   1. Find reliable Irish business data source"
echo "   2. Test on 100 real businesses"
echo "   3. Connect to Evolution Media quote system"
echo "   4. Build outreach automation"
echo ""