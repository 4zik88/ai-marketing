# 🚀 Quick Start - AI Marketing

## Get your first results in 5 minutes!

### Step 1: Installation (2 minutes)

```bash
# Navigate to project directory
cd "/Users/4zik/Work/AI Marketing"

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_web.txt  # For web application
```

### Step 2: API Key Setup (1 minute)

1. Get a FREE API key from Google: https://makersuite.google.com/app/apikey

2. Create `.env` file:
```bash
echo "GOOGLE_API_KEY=your_key_here" > .env
echo "AI_PROVIDER=google" >> .env
echo "AI_MODEL=gemini-2.0-flash" >> .env
```

3. Edit the `.env` file and add your key:
```env
GOOGLE_API_KEY=AIzaSyB...your_actual_key_here
AI_PROVIDER=google
AI_MODEL=gemini-2.0-flash
```

### Step 3: First Run (2 minutes)

#### 🌐 Web Application (Recommended)
```bash
python web_app.py
# Open browser: http://localhost:8000
```

#### 💻 Command Line
```bash
python main.py analyze https://example.com
```

## 📊 What Will You Get?

Excel file with sheets:
- ✅ Website information
- ✅ FAB analysis (Features-Advantages-Benefits)
- ✅ Ready Google Ads
- ✅ Keywords

## 💡 Command Examples

```bash
# Full analysis
python main.py analyze https://mysite.com

# Keywords only
python main.py analyze https://mysite.com --keywords-only

# With custom filename
python main.py analyze https://mysite.com --output my_ads.xlsx

# Parsing only (no AI)
python main.py parse https://mysite.com
```

## 🆓 FREE AI Providers

### Google Gemini (Recommended)
- ✅ 60 requests/minute FREE
- ✅ Excellent quality
- ✅ Works immediately

### Groq (Alternative)
- ✅ 30 requests/minute FREE
- ✅ Very fast
- ✅ Good quality

### Ollama (Local)
- ✅ 100% FREE forever
- ✅ Works without internet
- ⚠️ Requires installation

## 🆘 Problems?

### Error: "No module named 'google'"
```bash
pip install google-generativeai
```

### Error: "API key not found"
Check the `.env` file - key should start with `AIza`

### Website parsing error
Some websites block parsing. Try a different URL.

### Port 5000 busy
```bash
# Web app automatically uses port 8000
python web_app.py
# Open: http://localhost:8000
```

## 🎯 Next Steps

- Read full documentation: [README.md](README.md)
- Check code examples: [example_usage.py](example_usage.py)
- Study FAB methodology in code

## 💰 Cost

**Google Gemini (recommended):**
- 🆓 **FREE** up to 60 requests per minute
- 🆓 **FREE** up to 1,500 requests per day

**Groq:**
- 🆓 **FREE** up to 30 requests per minute
- 🆓 **FREE** up to 14,400 requests per day

**Ollama:**
- 🆓 **100% FREE** forever (local)

## 📞 Need Help?

Check the log file:
```bash
cat ai_marketing.log
```

Happy marketing! 🎉