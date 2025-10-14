#!/bin/bash
# Quick setup script for AI Marketing Web App

echo "🚀 AI Marketing Web App Setup"
echo "============================="

# Install missing dependencies
echo "📦 Installing AI dependencies..."
pip install ollama google-generativeai groq

# Create .env file with Google Gemini (free)
echo "🔑 Setting up Google Gemini (FREE AI)..."
cat > .env << EOF
# Free AI Provider - Google Gemini
AI_PROVIDER=google
AI_MODEL=gemini-pro
GOOGLE_API_KEY=your_google_api_key_here

# Other providers (optional)
# AI_PROVIDER=groq
# GROQ_API_KEY=your_groq_key_here

# AI_PROVIDER=ollama
# AI_MODEL=llama3.1
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "🔑 Next steps:"
echo "1. Get FREE Google API key: https://makersuite.google.com/app/apikey"
echo "2. Edit .env file and add your key:"
echo "   GOOGLE_API_KEY=your_actual_key_here"
echo "3. Run web app: python3 web_app.py"
echo "4. Open browser: http://localhost:8000"
echo ""
echo "🎉 Ready to use!"
