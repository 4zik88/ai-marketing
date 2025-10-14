# Google Ads MCP Quick Start Guide

Get started with Google Ads API integration in 5 minutes!

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
pip install google-ads PyYAML
```

### 2. Get Your Credentials

You need 4 things:
1. **Client ID** & **Client Secret** - from Google Cloud Console
2. **Developer Token** - from Google Ads account
3. **Refresh Token** - generated via OAuth2

### 3. Create Configuration File

Copy the example and fill in your credentials:

```bash
cp google-ads.yaml.example google-ads.yaml
```

Edit `google-ads.yaml`:

```yaml
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN
developer_token: YOUR_DEVELOPER_TOKEN
login_customer_id: YOUR_CUSTOMER_ID  # Without dashes
```

### 4. Test Your Setup

```bash
python main.py google-ads list-accounts
```

If you see your accounts - you're all set! 🎉

## 📖 Basic Usage

### CLI Examples

```bash
# View all campaigns
python main.py google-ads campaigns

# Get campaign performance
python main.py google-ads campaigns --campaign-id 12345678

# Check keyword quality scores
python main.py google-ads diagnose-quality

# Find expensive campaigns
python main.py google-ads diagnose-cost

# Get search terms report
python main.py google-ads search-terms --date-range LAST_7_DAYS
```

### Web API Examples

Start the server:

```bash
python web_app.py
```

Test endpoints:

```bash
# Check status
curl http://localhost:8000/api/google-ads/status

# Get campaigns
curl http://localhost:8000/api/google-ads/campaigns?date_range=LAST_7_DAYS

# Get keywords
curl http://localhost:8000/api/google-ads/keywords?campaign_id=12345678

# Natural language query
curl -X POST http://localhost:8000/api/google-ads/nlp \
  -H "Content-Type: application/json" \
  -d '{"request": "Show me campaigns with high cost"}'
```

### Python API Examples

```python
from google_ads import GoogleAdsMCPServer

# Initialize
mcp = GoogleAdsMCPServer()

# Get campaigns
campaigns = mcp.get_campaigns(date_range="LAST_30_DAYS")
print(f"Found {campaigns['count']} campaigns")

# Diagnose quality issues
quality_issues = mcp.diagnose_low_quality_scores()
for kw in quality_issues['low_quality_keywords']:
    print(f"Low QS keyword: {kw['keyword']}")

# Natural language query
result = mcp.process_natural_language_request("Show me keywords")
print(result)
```

## 🎯 Use Cases

### 1. Daily Performance Check

```bash
python main.py google-ads account-summary --date-range LAST_7_DAYS
python main.py google-ads diagnose-quality
python main.py google-ads diagnose-cost
```

### 2. Campaign Optimization

```python
from google_ads import GoogleAdsMCPServer

mcp = GoogleAdsMCPServer()

# Find underperforming keywords
keywords = mcp.get_keywords(min_impressions=100)
low_ctr = [k for k in keywords['keywords'] 
           if k.get('metrics', {}).get('ctr', 0) < 0.02]

print(f"Found {len(low_ctr)} keywords with CTR < 2%")
```

### 3. Search Terms Analysis

```bash
# See what people are actually searching for
python main.py google-ads search-terms --campaign-id 12345678
```

### 4. Combine with Content Generation

```python
from google_ads import GoogleAdsMCPServer
from ai import AIGenerator

# Get top performing keywords from your account
mcp = GoogleAdsMCPServer()
keywords_data = mcp.get_keywords(date_range="LAST_30_DAYS")

# Extract high-converting keywords
top_keywords = [
    kw['keyword'] 
    for kw in keywords_data['keywords'][:20]
    if kw.get('metrics', {}).get('conversions', 0) > 0
]

# Generate new ads using your best keywords
ai_gen = AIGenerator()
new_ads = ai_gen.generate_google_ads(
    fab_analysis=your_fab_data,
    keywords=top_keywords
)

print(f"Generated {len(new_ads['ads'])} new ads!")
```

## 🔧 Troubleshooting

### "google-ads.yaml not found"

```bash
cp google-ads.yaml.example google-ads.yaml
# Edit the file with your credentials
```

### "Authentication failed"

- Check your credentials are correct
- Regenerate refresh token:
  ```bash
  python -m google.ads.googleads.client --generate_refresh_token
  ```

### "Customer not found"

- Remove dashes from customer ID
- Make sure you have access to this account
- Try listing accounts first:
  ```bash
  python main.py google-ads list-accounts
  ```

### "Module not found: google.ads"

```bash
pip install google-ads
```

## 📚 Next Steps

- **Full Setup Guide**: See `GOOGLE_ADS_SETUP.md` for detailed instructions
- **API Documentation**: Check Google Ads API docs for GAQL queries
- **Examples**: Look at the code in `google_ads/` directory
- **Support**: Open an issue if you need help!

## 🎓 Key Concepts

### GAQL (Google Ads Query Language)

Similar to SQL, used to query your data:

```sql
SELECT 
  campaign.name,
  metrics.impressions,
  metrics.clicks
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.impressions DESC
```

### Date Ranges

Common values:
- `LAST_7_DAYS`
- `LAST_30_DAYS`
- `LAST_WEEK`
- `LAST_MONTH`
- `THIS_MONTH`
- `YESTERDAY`
- `TODAY`

### MCP (Model Context Protocol)

Enables AI assistants to interact with your Google Ads data using natural language!

---

**Ready to go?** Run your first command:

```bash
python main.py google-ads account-summary
```

🎉 Happy advertising!

