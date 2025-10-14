#!/bin/bash
# Deployment script for various platforms

echo "🚀 AI Marketing Web App Deployment"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "web_app.py" ]; then
    echo "❌ Error: web_app.py not found. Run this script from the project root."
    exit 1
fi

echo ""
echo "Choose deployment platform:"
echo "1) Heroku (Free tier available)"
echo "2) Railway (Free tier available)"
echo "3) Render (Free tier available)"
echo "4) Docker (Local/Cloud)"
echo "5) PythonAnywhere (Free tier available)"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "📦 Deploying to Heroku..."
        echo ""
        echo "Steps:"
        echo "1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli"
        echo "2. Login: heroku login"
        echo "3. Create app: heroku create your-app-name"
        echo "4. Set environment variables:"
        echo "   heroku config:set AI_PROVIDER=google"
        echo "   heroku config:set GOOGLE_API_KEY=your_key"
        echo "5. Deploy: git push heroku main"
        echo ""
        echo "✅ Files ready for Heroku deployment!"
        ;;
    2)
        echo "🚂 Deploying to Railway..."
        echo ""
        echo "Steps:"
        echo "1. Go to: https://railway.app"
        echo "2. Connect your GitHub repository"
        echo "3. Set environment variables in Railway dashboard:"
        echo "   AI_PROVIDER=google"
        echo "   GOOGLE_API_KEY=your_key"
        echo "4. Deploy automatically!"
        echo ""
        echo "✅ Files ready for Railway deployment!"
        ;;
    3)
        echo "🎨 Deploying to Render..."
        echo ""
        echo "Steps:"
        echo "1. Go to: https://render.com"
        echo "2. Connect your GitHub repository"
        echo "3. Create new Web Service"
        echo "4. Set environment variables:"
        echo "   AI_PROVIDER=google"
        echo "   GOOGLE_API_KEY=your_key"
        echo "5. Deploy!"
        echo ""
        echo "✅ Files ready for Render deployment!"
        ;;
    4)
        echo "🐳 Docker deployment..."
        echo ""
        echo "Local development:"
        echo "  docker-compose up"
        echo ""
        echo "Production build:"
        echo "  docker build -t ai-marketing ."
        echo "  docker run -p 5000:5000 -e AI_PROVIDER=google -e GOOGLE_API_KEY=your_key ai-marketing"
        echo ""
        echo "✅ Docker files ready!"
        ;;
    5)
        echo "🐍 PythonAnywhere deployment..."
        echo ""
        echo "Steps:"
        echo "1. Go to: https://pythonanywhere.com"
        echo "2. Create free account"
        echo "3. Upload files via Files tab"
        echo "4. Create Web App (Flask)"
        echo "5. Set environment variables in Web tab:"
        echo "   AI_PROVIDER=google"
        echo "   GOOGLE_API_KEY=your_key"
        echo "6. Reload web app"
        echo ""
        echo "✅ Files ready for PythonAnywhere!"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎯 FREE AI Setup Options:"
echo "========================="
echo ""
echo "1. Google Gemini (Recommended for web):"
echo "   - Get API key: https://makersuite.google.com/app/apikey"
echo "   - Free: 60 requests/minute"
echo "   - Set: AI_PROVIDER=google, GOOGLE_API_KEY=your_key"
echo ""
echo "2. Groq (Very fast):"
echo "   - Get API key: https://console.groq.com"
echo "   - Free: 30 requests/minute"
echo "   - Set: AI_PROVIDER=groq, GROQ_API_KEY=your_key"
echo ""
echo "3. Ollama (Local, but needs server setup):"
echo "   - Install Ollama on server"
echo "   - Download model: ollama pull llama3.1"
echo "   - Set: AI_PROVIDER=ollama"
echo ""
echo "📝 Environment Variables to Set:"
echo "=================================="
echo "AI_PROVIDER=google"
echo "GOOGLE_API_KEY=your_google_api_key"
echo "GROQ_API_KEY=your_groq_api_key"
echo "OPENAI_API_KEY=your_openai_key (if using paid)"
echo ""
echo "🎉 Ready to deploy!"
