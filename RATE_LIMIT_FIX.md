# 🔧 Fixing Google Gemini Rate Limit Error (429)

## ❌ Error Message

```
Error: Google Gemini API error: 429 You exceeded your current quota
```

## 🎯 Quick Solutions

### Solution 1: Switch to Groq (Recommended - FREE & Fast) ⚡

**On Railway:**
1. Go to **Variables** in your Railway project
2. Add/Update:
   ```env
   AI_PROVIDER=groq
   AI_MODEL=llama-3.1-70b-versatile
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. Get free API key: https://console.groq.com
4. Railway will auto-redeploy

**Benefits:**
- ✅ **FREE** - 30 requests/minute
- ✅ **Very fast** - fastest inference
- ✅ **14,400 requests/day** free
- ✅ No rate limit issues

### Solution 2: Switch to Ollama (100% FREE Forever) 🆓

**On Railway:**
1. Go to **Variables** in Railway
2. Add/Update:
   ```env
   AI_PROVIDER=ollama
   AI_MODEL=llama3.1
   ```
3. **Note:** Ollama requires local installation, so this works best on VPS

**For Local Development:**
```bash
# Install Ollama
brew install ollama  # macOS
# or download from ollama.com

# Pull model
ollama pull llama3.1

# Run app
python web_app.py
```

### Solution 3: Wait for Rate Limit Reset ⏰

Google Gemini free tier limits:
- **60 requests per minute**
- **1,500 requests per day**

Wait 1 minute for per-minute limit, or wait until next day for daily limit.

### Solution 4: Upgrade Google Gemini Plan 💰

1. Go to https://ai.google.dev/pricing
2. Upgrade to paid plan for higher limits
3. Keep using `AI_PROVIDER=google`

## 🚀 Recommended: Use Groq

**Why Groq is best:**
- ✅ **FREE** forever
- ✅ **Very fast** (faster than Gemini)
- ✅ **Higher limits** (14,400/day vs 1,500/day)
- ✅ **No credit card** required
- ✅ **Same quality** results

### Setup Groq (2 minutes):

1. **Get API Key:**
   - Visit: https://console.groq.com
   - Sign up (free)
   - Create API key

2. **Add to Railway:**
   ```env
   AI_PROVIDER=groq
   AI_MODEL=llama-3.1-70b-versatile
   GROQ_API_KEY=gsk_your_key_here
   ```

3. **Done!** Railway will redeploy automatically

## 📊 Provider Comparison

| Provider | Free Tier | Speed | Daily Limit | Setup |
|----------|-----------|-------|-------------|-------|
| **Groq** | ✅ Yes | ⚡⚡⚡ Very Fast | 14,400 | 2 min |
| **Ollama** | ✅ Yes | ⚡ Fast | Unlimited | 5 min |
| **Google Gemini** | ✅ Yes | ⚡⚡ Fast | 1,500 | 1 min |
| **OpenAI** | ❌ Paid | ⚡⚡ Fast | - | 1 min |

## 🔄 Automatic Fallback

The app now has **automatic fallback**:
- If Google Gemini hits rate limit (429)
- App automatically tries **Groq** first
- If Groq fails, tries **Ollama**
- You'll see fallback messages in logs

## 🧪 Test Your Setup

After switching providers, test:

```bash
# Via CLI
python main.py analyze https://example.com --ai-provider groq

# Or via web interface
# Just use the app - it will use new provider automatically
```

## 📝 Environment Variables Reference

### For Groq:
```env
AI_PROVIDER=groq
AI_MODEL=llama-3.1-70b-versatile
GROQ_API_KEY=gsk_...
```

### For Ollama:
```env
AI_PROVIDER=ollama
AI_MODEL=llama3.1
```

### For Google (when limit resets):
```env
AI_PROVIDER=google
AI_MODEL=gemini-2.0-flash
GOOGLE_API_KEY=AIza...
```

## 🆘 Still Having Issues?

1. **Check Railway logs:**
   - Railway Dashboard → Your Project → Deployments → View Logs

2. **Verify API key:**
   - Make sure key is correct
   - Check key hasn't expired

3. **Try different model:**
   - Groq: `llama-3.1-8b-instant` (faster)
   - Groq: `mixtral-8x7b-32768` (better quality)

## ✅ Success!

After switching to Groq, you should see:
- ✅ No more 429 errors
- ✅ Faster responses
- ✅ More requests per day

---

**Recommendation: Use Groq for production - it's free, fast, and reliable!** 🚀

