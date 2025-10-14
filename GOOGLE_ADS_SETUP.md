# Google Ads API MCP Server Setup Guide

This guide will help you set up the Google Ads API integration with Model Context Protocol (MCP) support for natural language interaction with your Google Ads data.

## 🎯 What You Can Do

With Google Ads MCP integration, you can:

- **Query Campaign Data**: Get performance metrics, budgets, and status
- **Analyze Keywords**: View keyword performance, quality scores, and search terms
- **Diagnose Issues**: Find low-quality keywords, high-cost campaigns, disapproved ads
- **Natural Language Interface**: Ask questions like "Show me campaigns with high cost but low conversions"
- **Geographic & Device Analysis**: Understand performance across locations and devices

## 📋 Prerequisites

1. **Google Ads Account**: You need access to a Google Ads account
2. **Python 3.8+**: Already installed if you're using this project
3. **Google Cloud Project**: For OAuth2 credentials

## 🚀 Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Ads API**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Ads API"
   - Click "Enable"

### Step 2: Create OAuth2 Credentials

1. In Google Cloud Console, go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Choose "Desktop app" as the application type
4. Name it (e.g., "AI Marketing App")
5. Download the credentials JSON file
6. Note down your **Client ID** and **Client Secret**

### Step 3: Get Google Ads Developer Token

1. Sign in to your [Google Ads account](https://ads.google.com/)
2. Click the tools icon (wrench) in the upper right
3. Under "Setup", click "API Center"
4. Apply for a developer token (if you don't have one)
5. For testing, you can use your account without full approval

**Important**: 
- Test accounts can work with your own Google Ads accounts immediately
- For production/client accounts, you need Google's approval (can take a few days)

### Step 4: Generate Refresh Token

Run this command to generate your refresh token:

```bash
python -c "from google.ads.googleads import oauth2; oauth2.get_refresh_token()"
```

Or use the Google Ads API helper script:

```bash
python -m google.ads.googleads.client --generate_refresh_token
```

This will:
1. Open your browser for Google authentication
2. Ask you to authorize the application
3. Return a refresh token - **save this securely!**

### Step 5: Create Configuration File

Create a file named `google-ads.yaml` in your project directory or home directory:

```yaml
# google-ads.yaml
client_id: YOUR_CLIENT_ID_HERE
client_secret: YOUR_CLIENT_SECRET_HERE
refresh_token: YOUR_REFRESH_TOKEN_HERE
developer_token: YOUR_DEVELOPER_TOKEN_HERE
login_customer_id: YOUR_CUSTOMER_ID_HERE  # Without dashes, e.g., 1234567890
```

**Template file**: We've created `google-ads.yaml.example` - copy and fill in your values.

```bash
cp google-ads.yaml.example google-ads.yaml
# Edit google-ads.yaml with your credentials
```

**Finding Your Customer ID**:
- Log into Google Ads
- Look at the top right corner - you'll see a number like "123-456-7890"
- Remove dashes: `1234567890`
- This is your `login_customer_id`

### Step 6: Install Dependencies

Install the Google Ads API library:

```bash
pip install google-ads
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

### Step 7: Test Your Setup

Test that everything is working:

```bash
# CLI test
python main.py google-ads list-accounts

# Or test in Python
python -c "from google_ads import GoogleAdsClient; client = GoogleAdsClient(); print(client.validate_credentials())"
```

If successful, you should see your Google Ads accounts listed!

## 📖 Usage Examples

### CLI Commands

```bash
# List all accessible accounts
python main.py google-ads list-accounts

# Get account summary
python main.py google-ads account-summary

# Get all campaigns
python main.py google-ads campaigns

# Get campaign performance
python main.py google-ads campaigns --campaign-id 123456789

# Get keywords performance
python main.py google-ads keywords --campaign-id 123456789

# Get search terms report
python main.py google-ads search-terms

# Diagnostics - find low quality keywords
python main.py google-ads diagnose-quality

# Diagnostics - find high cost campaigns
python main.py google-ads diagnose-cost

# Custom GAQL query
python main.py google-ads query "SELECT campaign.name, metrics.clicks FROM campaign WHERE segments.date DURING LAST_30_DAYS"
```

### Web API Endpoints

Start the web app:

```bash
python web_app.py
```

Then use these endpoints:

- `GET /api/google-ads/accounts` - List accounts
- `GET /api/google-ads/campaigns` - Get campaigns
- `GET /api/google-ads/keywords?campaign_id=123` - Get keywords
- `POST /api/google-ads/query` - Run custom query
- `GET /api/google-ads/diagnose/quality-score` - Quality diagnostics

### Python API

```python
from google_ads import GoogleAdsMCPServer

# Initialize MCP server
mcp = GoogleAdsMCPServer()

# Natural language query
result = mcp.process_natural_language_request(
    "Show me campaigns with high cost but low conversions"
)
print(result)

# Direct tool usage
campaigns = mcp.get_campaigns(date_range="LAST_7_DAYS")
print(f"Found {campaigns['count']} campaigns")

# Diagnostics
low_quality = mcp.diagnose_low_quality_scores()
print(f"Found {low_quality['count']} keywords with quality score < 5")

# Custom query
result = mcp.run_custom_query("""
    SELECT 
        campaign.name,
        metrics.impressions,
        metrics.clicks,
        metrics.ctr
    FROM campaign
    WHERE segments.date DURING LAST_30_DAYS
    ORDER BY metrics.impressions DESC
""")
```

## 🔒 Security Best Practices

1. **Never commit credentials**: Add `google-ads.yaml` to `.gitignore`
2. **Use environment variables**: For production, use env vars instead of YAML
3. **Restrict OAuth scopes**: Only request necessary permissions
4. **Rotate tokens**: Regularly refresh your tokens
5. **Use test accounts**: Test with test accounts before production

## 🐛 Troubleshooting

### "Authentication failed"

- Check your client_id and client_secret are correct
- Ensure refresh_token hasn't expired (generate a new one)
- Verify your Google Ads API is enabled in Cloud Console

### "Developer token invalid"

- Make sure you've applied for a developer token in Google Ads
- For testing, ensure you're querying your own accounts
- Check if you need approval for production access

### "Customer ID not found"

- Verify you're using the correct customer ID (without dashes)
- Make sure your OAuth2 account has access to this customer
- Try listing accessible accounts first: `python main.py google-ads list-accounts`

### "Permission denied"

- Ensure your OAuth2 credentials have the right scopes
- Check that the Google Ads account has API access enabled
- Verify you're not querying a manager account when you need a client account

### "Import error: No module named 'google.ads'"

```bash
pip install google-ads
```

## 📚 Additional Resources

- [Google Ads API Documentation](https://developers.google.com/google-ads/api/docs/start)
- [Python Client Library](https://developers.google.com/google-ads/api/docs/client-libs/python)
- [GAQL Query Language](https://developers.google.com/google-ads/api/docs/query/overview)
- [Google Ads API Forum](https://groups.google.com/g/adwords-api)
- [Official MCP Server Blog Post](https://ads-developers.googleblog.com/2025/10/open-source-google-ads-api-mcp-server.html)
- [GitHub Repository](https://github.com/googleads/google-ads-mcp)

## 🎓 Understanding MCP (Model Context Protocol)

MCP enables AI assistants to interact with external data sources. With this integration:

- **AI can query your data**: Ask questions in natural language
- **Context-aware responses**: AI understands your campaign structure
- **Automated diagnostics**: AI can identify issues proactively
- **Report generation**: Generate custom reports using conversational interface

## 💡 Pro Tips

1. **Start with read-only**: The current integration is read-only (safe for testing)
2. **Use manager accounts**: If managing multiple accounts, use a manager account login_customer_id
3. **Cache results**: Campaign data doesn't change every second - cache when appropriate
4. **Date ranges**: Use appropriate date ranges (LAST_7_DAYS, LAST_30_DAYS, etc.)
5. **Combine with FAB analysis**: Use Google Ads data to inform your content generation

## 🔄 Integration with AI Marketing Features

Combine Google Ads data with content generation:

```python
from google_ads import GoogleAdsMCPServer
from ai import AIGenerator

# Get top performing keywords from existing campaigns
mcp = GoogleAdsMCPServer()
keywords_data = mcp.get_keywords(date_range="LAST_30_DAYS")

# Extract high-performing keywords
top_keywords = [
    kw['keyword'] 
    for kw in keywords_data['keywords'][:10]
    if kw.get('metrics', {}).get('conversions', 0) > 0
]

# Use them to generate new ads
ai_gen = AIGenerator()
new_ads = ai_gen.generate_google_ads(
    fab_analysis=your_fab_data,
    keywords=top_keywords
)

print(f"Generated {len(new_ads['ads'])} new ads based on your top keywords!")
```

## ✅ Ready to Go!

Once setup is complete, you can:

1. Query your Google Ads data from CLI or web interface
2. Get natural language insights into campaign performance
3. Automate diagnostics and reporting
4. Combine real campaign data with AI-generated content

---

**Questions?** Check the troubleshooting section or open an issue on GitHub!

