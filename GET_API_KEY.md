# GET GOOGLE MAPS API KEY

## **🎯 STEP-BY-STEP GUIDE:**

### **1. Go to Google Cloud Console**
https://console.cloud.google.com

### **2. Create New Project**
- Click project dropdown (top left)
- Click "NEW PROJECT"
- Name: `Evolution Media Lead Scout`
- Click "CREATE"

### **3. Enable Places API**
- In search bar: type "Places API"
- Click "Places API"
- Click "ENABLE"

### **4. Create API Key**
- Go to "Credentials" (left menu)
- Click "+ CREATE CREDENTIALS"
- Select "API key"
- Copy the key that appears

### **5. Restrict API Key (IMPORTANT!)**
- Click on your new API key
- Under "API restrictions": Select "Restrict key"
- Choose "Places API" from dropdown
- Under "Application restrictions": Select "IP addresses"
- Add: `192.168.4.90` (your server IP)
- Click "SAVE"

### **6. Enable Billing (Free $300 Credit)**
- You need billing enabled (but get $300 free credit)
- Cost: $0.032 per 1,000 requests
- 500 businesses = ~$0.16

## **🔑 YOUR API KEY WILL LOOK LIKE:**
```
AIzaSyBx3xVxVxVxVxVxVxVxVxVxVxVxVxVxVxVxVxV
```

## **🚀 QUICK TEST:**

Once you have the API key, run:
```bash
cd /home/jr/.openclaw/workspace/lead-scout
source venv/bin/activate

# Edit the scraper with your real API key
nano scrapers/google_maps_api.py
# Change: api_key = "YOUR_API_KEY_HERE" to your real key

# Run test
python3 scrapers/google_maps_api.py
```

## **💰 COST ESTIMATE:**

| Action | Cost | Example |
|--------|------|---------|
| Text search | $0.032 per 1,000 | 500 businesses = $0.016 |
| Place details | $0.017 per 1,000 | 500 details = $0.0085 |
| **Total per 500** | **~$0.025** | Very affordable |

## **🎯 WHAT YOU GET:**

1. **Business names, addresses, phone numbers**
2. **Website URLs** (when available)
3. **Ratings & reviews** (social proof)
4. **Accurate, up-to-date data**
5. **Legal access** (no scraping issues)

## **📊 EXPECTED RESULTS:**

- **70-80%** of businesses will have websites
- **20-30%** will have poor/no websites = Evolution Media leads
- **500 Dublin businesses** in 1 hour
- **100-150 qualified leads** ready for outreach

## **⚠️ IMPORTANT NOTES:**

1. **Keep API key secret** - don't commit to GitHub
2. **Rate limits:** 100 requests per 100 seconds
3. **Use environment variables** for production:
   ```bash
   export GOOGLE_MAPS_API_KEY="your_key_here"
   ```

## **🚀 NEXT STEPS AFTER GETTING KEY:**

1. Test with 50 businesses
2. Run through website analyzer
3. View leads in dashboard
4. Export for outreach
5. Scale to 500+ businesses

**Get your API key now and we'll have real lead generation running in 30 minutes!**