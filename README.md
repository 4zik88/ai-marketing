# AI Marketing - Advertising Content Generator

Intelligent Python application for automatic generation of advertising materials based on the FAB methodology (Features, Advantages, Benefits).

## 🎯 Features

- **Website Content Parsing** - Automatic information extraction from websites
- **FAB Analysis** - Application of Features-Advantages-Benefits methodology to content
- **Keyword Generation** - Creation of relevant keywords for SEO and contextual advertising
- **Google Ads Creation** - Automatic ad generation with technical constraints compliance
- **Excel Export** - Convenient tables for further work

## 📋 Requirements

- Python 3.8+
- API key from OpenAI or Anthropic

## 🚀 Installation

1. Clone the repository or download files:
```bash
cd "/Users/4zik/Work/AI Marketing"
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your API keys:
```bash
cp .env.example .env
```

5. Edit the `.env` file and add your API key:
```env
# For OpenAI (recommended)
OPENAI_API_KEY=sk-your-key-here
AI_PROVIDER=openai
AI_MODEL=gpt-4-turbo-preview

# Or for Anthropic
# ANTHROPIC_API_KEY=your-key-here
# AI_PROVIDER=anthropic
# AI_MODEL=claude-3-sonnet-20240229
```

## 💡 Usage

### Complete Website Analysis

Parses website, analyzes with FAB methodology, generates keywords and ads:

```bash
python main.py analyze https://example.com
```

With custom filename:
```bash
python main.py analyze https://example.com --output my_report.xlsx
```

With AI provider selection:
```bash
python main.py analyze https://example.com --ai-provider openai --model gpt-4
```

### Keywords Only Generation

```bash
python main.py analyze https://example.com --keywords-only
```

### Parsing Without AI Analysis

Content extraction only:
```bash
python main.py parse https://example.com
```

With JSON saving:
```bash
python main.py parse https://example.com --output data.json
```

### View Configuration

```bash
python main.py config-info
```

### Command Help

```bash
python main.py --help
python main.py analyze --help
```

## 📊 Project Structure

```
AI Marketing/
├── main.py                 # Main application with CLI
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── .env                   # API keys (create yourself)
├── .env.example          # Configuration example
├── README.md             # Documentation
│
├── parsers/              # Parsing modules
│   ├── __init__.py
│   └── website_parser.py # Website parser
│
├── fab/                  # FAB methodology
│   ├── __init__.py
│   └── fab_methodology.py # FAB logic
│
├── ai/                   # AI generation
│   ├── __init__.py
│   └── ai_generator.py   # AI API integration
│
├── exporters/            # Data export
│   ├── __init__.py
│   └── excel_exporter.py # Excel export
│
└── output/               # Output files (created automatically)
```

## 🎓 FAB Methodology

### What is FAB?

FAB (Features, Advantages, Benefits) is a proven sales and marketing methodology:

1. **Feature (Characteristic)** - what you sell, technical parameters
2. **Advantage (Benefit)** - why it's good
3. **Benefit (Value)** - what value the client gets

### BAB Method (Reverse FAB)

For emotional impact, use reverse order:
**Benefit → Advantage → Feature**

**Example:**
- ❌ Bad: "We have a 24-megapixel camera" (Feature)
- ✅ Good: "Capture every detail of your memories (Benefit) with crystal-clear shots (Advantage) using a 24-megapixel sensor (Feature)"

## 📦 Output Files

The application creates Excel files with the following sheets:

### Complete Report (`complete_report_*.xlsx`)
1. **Website Info** - website information
2. **FAB Analysis** - FAB methodology analysis
3. **Google Ads** - ready-made advertisements

### Ads Only (`google_ads_*.xlsx`)
1. **All Ads** - all ad variations
2. **Headlines** - headlines only with length validation
3. **Descriptions** - descriptions only with length validation
4. **Keywords** - keywords by groups

## 🔧 Google Ads Technical Parameters

The application automatically monitors Google Ads limitations:

- **Headline**: maximum 30 characters
- **Description**: maximum 90 characters
- **Path**: maximum 15 characters

## 🤖 Supported AI Models

### OpenAI (recommended)
- `gpt-4-turbo-preview` - most powerful model (recommended)
- `gpt-4` - stable GPT-4 version
- `gpt-3.5-turbo` - fast and cheap

### Anthropic
- `claude-3-opus-20240229` - most powerful Claude model
- `claude-3-sonnet-20240229` - balance of speed and quality

## 📝 Usage Examples

### Example 1: E-commerce Store Analysis

```bash
python main.py analyze https://myshop.com --output shop_ads.xlsx
```

Result:
- Product and service analysis
- 5-7 ad variations
- Keywords for different match types
- Ready Excel file for Google Ads upload

### Example 2: SEO Keywords Only

```bash
python main.py analyze https://myblog.com --keywords-only --output seo_keywords.xlsx
```

### Example 3: Quick Competitor Parsing

```bash
python main.py parse https://competitor.com --output competitor_data.json
```

## 🔐 Security

- Never commit the `.env` file with API keys
- API keys are stored locally only
- All AI API requests use HTTPS

## 🐛 Debugging

Logs are saved to `ai_marketing.log` file:

```bash
tail -f ai_marketing.log  # Real-time viewing
```

## 📈 Best Practices

1. **For best results** - use GPT-4
2. **For speed** - use GPT-3.5-turbo
3. **For accuracy** - analyze main page or product page
4. **For variety** - run analysis multiple times with different pages

## 🛠️ Development

### Development Mode Installation

```bash
pip install -e .
```

### Run Tests

```bash
pytest tests/
```

## 📄 License

MIT License

## 🤝 Support

If you encounter problems:
1. Check the `ai_marketing.log` file
2. Make sure the API key is correct
3. Check internet connection
4. Ensure the website is accessible for parsing

## 🚀 Roadmap

- [x] **Google Ads API Direct Upload Support** ✅ (via MCP Server)
- [x] **Web Interface** ✅
- [ ] Competitor Analysis
- [ ] A/B Testing for Ads
- [ ] Yandex.Direct Integration
- [ ] Multi-language Support
- [ ] Ad Performance Analysis

## 🆕 Google Ads API Integration (NEW!)

The application is now integrated with **Google Ads API MCP Server**!

### Capabilities:

- 📊 **Campaign Reports** - Get performance metrics
- 🔍 **Keyword Analysis** - Quality scores, CTR, cost metrics
- 🎯 **Diagnostics** - Automatically find problem areas
- 💬 **Natural Language** - Ask questions about data in plain language
- 📈 **Geographic and Device Analytics**

### Quick Start:

```bash
# Install dependencies
pip install google-ads PyYAML

# Setup credentials
cp google-ads.yaml.example google-ads.yaml
# Fill in your API keys

# Check campaigns
python main.py google-ads campaigns

# Run diagnostics
python main.py google-ads diagnose-quality
```

📖 **Complete Documentation**: 
- Quick Start: `QUICKSTART_GOOGLE_ADS.md`
- Detailed Setup: `GOOGLE_ADS_SETUP.md`

### New CLI Commands:

```bash
python main.py google-ads list-accounts        # List accounts
python main.py google-ads campaigns            # Campaigns
python main.py google-ads keywords             # Keywords
python main.py google-ads search-terms         # Search queries
python main.py google-ads diagnose-quality     # Quality diagnostics
python main.py google-ads diagnose-cost        # Expensive campaigns
```

### Web API Endpoints:

```bash
GET  /api/google-ads/status                    # Integration status
GET  /api/google-ads/campaigns                 # Campaigns
GET  /api/google-ads/keywords                  # Keywords
POST /api/google-ads/nlp                       # Natural language
GET  /api/google-ads/diagnose/quality-score    # Diagnostics
```

## 📞 Contact

For questions and suggestions, create an Issue in the repository.

---

**Made with ❤️ for marketers and SEO specialists**