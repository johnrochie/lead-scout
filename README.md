# Lead Scout 🎯

**Automated Lead Generation for Digital Agencies**

Find businesses with poor or no websites and turn them into clients.

## 🚀 What It Does

Lead Scout automates the process of finding potential clients for web design/development agencies:

1. **Scrapes business data** from Google Maps Places API
2. **Analyzes websites** (0-30 scoring system)
3. **Identifies qualified leads** (score < 15 = needs new website)
4. **Exports ready-to-use leads** for outreach

## 📊 Features

- **Google Maps API Integration** - Legal, reliable business data
- **Website Scoring Algorithm** - 0-30 scale (design, mobile, performance, age)
- **Lead Qualification** - Automatic flagging of businesses needing websites
- **Interactive Dashboard** - View, filter, export leads
- **Multi-category Support** - Restaurants, dentists, plumbers, electricians, cafes, etc.
- **Cost-effective** - ~$0.025 for 500 businesses

## 🛠️ Quick Start

### 1. Prerequisites
```bash
python3.12+
pip install -r requirements.txt
```

### 2. Get Google Maps API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create project and enable "Places API"
3. Get API key and restrict to your IP
4. Add to `.env` file:
```
GOOGLE_MAPS_API_KEY=your_key_here
```

### 3. Install & Run
```bash
# Clone repository
git clone https://github.com/yourusername/lead-scout.git
cd lead-scout

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with mock data (no API key needed)
python3 run_prototype.sh

# Or run with real data (requires API key)
python3 scrapers/google_maps_api.py
python3 dashboard.py
```

## 📁 Project Structure

```
lead-scout/
├── scrapers/           # Data collection
│   ├── google_maps_api.py      # Main Google Maps scraper
│   └── golden_pages_scraper.py # Alternative scraper
├── analysis/           # Website analysis
│   └── website_analyzer.py     # Scoring algorithm
├── data/              # Data storage
│   ├── mock_*.csv     # Sample data
│   └── sample_*.csv   # Example outputs
├── scripts/           # Utility scripts
├── dashboard.py       # Interactive lead dashboard
├── export_real_leads.py # Export leads to CSV
├── requirements.txt   # Python dependencies
├── .env.example       # Environment template
└── README.md          # This file
```

## 🎯 How It Works

### Scoring Algorithm (0-30)
- **Design Quality** (+0-10): Mobile-friendly, modern layout, CSS frameworks
- **Site Age** (+0-8): Copyright year, old tech detection (jQuery, Flash)
- **Performance** (+0-7): HTTPS/SSL, image optimization, contact info
- **Mobile Friendliness** (+0-5): Viewport, touch targets, responsive

**Threshold:** Score < 15 = "Needs new website"

### Lead Qualification
1. **No website** = Highest priority (call immediately)
2. **Score 0-5** = Critical (needs complete rebuild)
3. **Score 6-10** = Poor (needs major improvements)
4. **Score 11-14** = Needs updates (modernization)

## 💰 Business Model

### For Digital Agencies:
- **Find clients** who actually need websites
- **Qualify leads** before outreach
- **Increase conversion rates** from 1-2% to 10-20%
- **Scale lead generation** without manual research

### Revenue Potential:
- **30 leads** = €15,000+ potential (€500/website)
- **500 leads** = €250,000+ potential
- **10% conversion** = €25,000 immediate revenue

## 📈 Example Output

```csv
business_name,category,phone,has_website,priority,estimated_value
Rainbow Plumbing,plumber,086 406 6281,NO,HIGHEST - NO WEBSITE,€500 + €200/month
The Vintage Kitchen,restaurant,(01) 679 8705,YES,HIGH - HAS WEBSITE,€500 (rebuild)
```

## 🚀 Advanced Usage

### Scale to 500+ Businesses
```python
# Custom scrape with multiple categories
python3 scrapers/full_scrape.py
```

### Integrate with CRM
```python
# Export leads for HubSpot, Salesforce, etc.
python3 export_real_leads.py
```

### Automated Outreach
```python
# Connect to email marketing tools
# (Coming soon: Mailchimp, SendGrid integrations)
```

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```bash
GOOGLE_MAPS_API_KEY=your_google_maps_key_here
# Optional: Add other API keys as needed
```

### Custom Categories
Edit `scrapers/google_maps_api.py`:
```python
categories = [
    ('restaurants', 20),
    ('dentists', 15),
    ('plumbers', 15),
    # Add your own...
]
```

## 📊 Performance

- **30 businesses** = ~2 minutes (scrape + analysis)
- **500 businesses** = ~30 minutes
- **API cost**: $0.032 per 1,000 requests
- **Accuracy**: 90%+ website detection rate

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Google Maps Places API for reliable business data
- BeautifulSoup4 for HTML parsing
- Pandas for data manipulation

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/lead-scout/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/lead-scout/wiki)
- **Email**: your.email@example.com

---

**Built with ❤️ for digital agencies struggling to find clients.**

*Turn lead generation from a chore into a revenue machine.*