"""
Flask Web App for AI Marketing
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import logging
from datetime import datetime
from pathlib import Path
import tempfile
import zipfile

# Import our modules
from parsers import WebsiteParser
from ai import AIGenerator
from exporters import ExcelExporter
from config import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ai-marketing-secret-key-change-in-production')

# Setup HTTP Basic Authentication
auth = HTTPBasicAuth()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for session data
session_data = {}

# Authentication verification function
@auth.verify_password
def verify_password(username, password):
    """Verify username and password for HTTP Basic Auth"""
    # If authentication is disabled, allow access
    if not settings.auth_enabled:
        return True
    
    # Check credentials
    if username == settings.auth_username and password == settings.auth_password:
        return username
    
    # If password is empty, authentication is not properly configured
    if not settings.auth_password:
        logger.warning("Authentication enabled but AUTH_PASSWORD not set!")
        return False
    
    return False

# Decorator to protect routes (only if auth is enabled)
def require_auth(f):
    """Decorator to require authentication if enabled"""
    if settings.auth_enabled:
        return auth.login_required(f)
    return f

@app.route('/')
@require_auth
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
@require_auth
def analyze_website():
    """API endpoint for website analysis"""
    try:
        data = request.json
        url = data.get('url')
        ai_provider = data.get('ai_provider', settings.ai_provider)
        ai_model = data.get('ai_model', settings.ai_model)
        keywords_only = data.get('keywords_only', False)
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Step 1: Parse website
        logger.info(f"Parsing website: {url}")
        parser = WebsiteParser()
        website_data = parser.parse_url(url)
        
        # Step 2: FAB Analysis
        logger.info("Running FAB analysis...")
        ai_generator = AIGenerator(provider=ai_provider, model=ai_model)
        fab_analysis = ai_generator.analyze_with_fab(website_data)
        
        # Step 3: Generate keywords
        logger.info("Generating keywords...")
        keywords_data = ai_generator.generate_keywords(fab_analysis)
        
        if keywords_only:
            # Export only keywords
            exporter = ExcelExporter(settings.output_dir)
            filename = f"keywords_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = exporter.export_keywords(keywords_data, filename)
            
            return jsonify({
                'success': True,
                'type': 'keywords_only',
                'website_data': website_data,
                'fab_analysis': fab_analysis,
                'keywords_data': keywords_data,
                'download_file': filename
            })
        
        # Step 4: Generate Google Ads
        logger.info("Generating Google Ads...")
        keywords_list = []
        if isinstance(keywords_data, dict) and 'keywords' in keywords_data:
            keywords_list = [kw.get('keyword', kw) if isinstance(kw, dict) else kw 
                           for kw in keywords_data['keywords']]
        
        ads_data = ai_generator.generate_google_ads(fab_analysis, keywords_list[:20])
        
        # Step 5: Export complete report
        logger.info("Exporting to Excel...")
        exporter = ExcelExporter(settings.output_dir)
        filename = f"complete_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = exporter.export_complete_report(
            website_data, fab_analysis, keywords_data, ads_data, filename
        )
        
        # Store session data
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        session_data[session_id] = {
            'website_data': website_data,
            'fab_analysis': fab_analysis,
            'keywords_data': keywords_data,
            'ads_data': ads_data,
            'filepath': filepath
        }
        
        return jsonify({
            'success': True,
            'type': 'complete',
            'session_id': session_id,
            'website_data': website_data,
            'fab_analysis': fab_analysis,
            'keywords_data': keywords_data,
            'ads_data': ads_data,
            'download_file': filename
        })
        
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
@require_auth
def download_file(filename):
    """Download generated files"""
    try:
        filepath = settings.output_dir / filename
        if filepath.exists():
            return send_file(str(filepath), as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai-providers')
@require_auth
def get_ai_providers():
    """Get available AI providers and models"""
    providers = {
        'ollama': {
            'name': 'Ollama (Local)',
            'free': True,
            'description': '100% free, runs locally',
            'models': ['llama3.1', 'llama3.1:8b', 'mistral', 'qwen2.5'],
            'setup_required': 'Install Ollama and download model'
        },
        'google': {
            'name': 'Google Gemini',
            'free': True,
            'description': 'Free API, excellent quality',
            'models': ['gemini-2.0-flash', 'gemini-2.5-pro', 'gemini-2.0-flash-lite'],
            'setup_required': 'Get API key from Google AI Studio'
        },
        'groq': {
            'name': 'Groq',
            'free': True,
            'description': 'Free API, very fast',
            'models': ['llama-3.1-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768'],
            'setup_required': 'Get API key from Groq Console'
        },
        'openai': {
            'name': 'OpenAI',
            'free': False,
            'description': 'Paid API, best quality',
            'models': ['gpt-4-turbo-preview', 'gpt-4', 'gpt-3.5-turbo'],
            'setup_required': 'Get API key from OpenAI'
        },
        'anthropic': {
            'name': 'Anthropic Claude',
            'free': False,
            'description': 'Paid API, excellent quality',
            'models': ['claude-3-opus-20240229', 'claude-3-sonnet-20240229'],
            'setup_required': 'Get API key from Anthropic'
        }
    }
    return jsonify(providers)

@app.route('/api/config', methods=['GET', 'POST'])
@require_auth
def config():
    """Get or update configuration"""
    if request.method == 'GET':
        return jsonify({
            'ai_provider': settings.ai_provider,
            'ai_model': settings.ai_model,
            'has_openai_key': bool(settings.openai_api_key),
            'has_anthropic_key': bool(settings.anthropic_api_key),
            'has_google_key': bool(settings.google_api_key),
            'has_groq_key': bool(settings.groq_api_key)
        })
    
    elif request.method == 'POST':
        data = request.json
        # Update environment variables (for this session)
        if 'ai_provider' in data:
            settings.ai_provider = data['ai_provider']
        if 'ai_model' in data:
            settings.ai_model = data['ai_model']
        
        return jsonify({'success': True})

@app.route('/health')
def health():
    """Health check endpoint (no auth required)"""
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_provider': settings.ai_provider
    })


# Google Ads MCP Integration Endpoints

@app.route('/api/google-ads/status')
@require_auth
def google_ads_status():
    """Check if Google Ads integration is available"""
    try:
        from google_ads import GoogleAdsMCPServer
        # Try to initialize to check if credentials are valid
        try:
            mcp = GoogleAdsMCPServer()
            return jsonify({
                'available': True,
                'configured': True,
                'customer_id': mcp.customer_id
            })
        except FileNotFoundError:
            return jsonify({
                'available': True,
                'configured': False,
                'message': 'google-ads.yaml not found. Please configure API credentials.'
            })
        except Exception as e:
            return jsonify({
                'available': True,
                'configured': False,
                'error': str(e)
            })
    except ImportError:
        return jsonify({
            'available': False,
            'configured': False,
            'message': 'Google Ads API not installed. Run: pip install google-ads'
        })


@app.route('/api/google-ads/accounts')
@require_auth
def google_ads_accounts():
    """List all accessible Google Ads accounts"""
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.list_accounts()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error listing accounts: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/account/summary')
@require_auth
def google_ads_account_summary():
    """Get account summary"""
    date_range = request.args.get('date_range', 'LAST_30_DAYS')
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.get_account_summary(date_range)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting summary: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/campaigns')
@require_auth
def google_ads_campaigns():
    """Get campaigns with performance metrics"""
    campaign_id = request.args.get('campaign_id')
    date_range = request.args.get('date_range', 'LAST_30_DAYS')
    status = request.args.get('status')
    
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        
        if campaign_id:
            result = mcp.get_campaign_performance(campaign_id, date_range)
        else:
            result = mcp.get_campaigns(date_range, status)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting campaigns: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/ad-groups')
@require_auth
def google_ads_ad_groups():
    """Get ad groups with performance metrics"""
    campaign_id = request.args.get('campaign_id')
    date_range = request.args.get('date_range', 'LAST_30_DAYS')
    
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.get_ad_groups(campaign_id, date_range)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting ad groups: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/keywords')
@require_auth
def google_ads_keywords():
    """Get keyword performance"""
    campaign_id = request.args.get('campaign_id')
    date_range = request.args.get('date_range', 'LAST_30_DAYS')
    min_impressions = int(request.args.get('min_impressions', 0))
    
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.get_keywords(campaign_id, date_range, min_impressions)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting keywords: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/search-terms')
@require_auth
def google_ads_search_terms():
    """Get search terms report"""
    campaign_id = request.args.get('campaign_id')
    date_range = request.args.get('date_range', 'LAST_7_DAYS')
    
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.get_search_terms(campaign_id, date_range)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting search terms: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/ads')
@require_auth
def google_ads_ads():
    """Get ads with performance metrics"""
    campaign_id = request.args.get('campaign_id')
    ad_group_id = request.args.get('ad_group_id')
    date_range = request.args.get('date_range', 'LAST_30_DAYS')
    
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.get_ads(campaign_id, ad_group_id, date_range)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting ads: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/performance/geographic')
@require_auth
def google_ads_geographic():
    """Get geographic performance"""
    campaign_id = request.args.get('campaign_id')
    date_range = request.args.get('date_range', 'LAST_30_DAYS')
    
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.get_geographic_performance(campaign_id, date_range)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting geographic performance: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/performance/device')
@require_auth
def google_ads_device():
    """Get device performance"""
    campaign_id = request.args.get('campaign_id')
    date_range = request.args.get('date_range', 'LAST_30_DAYS')
    
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.get_device_performance(campaign_id, date_range)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting device performance: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/diagnose/quality-score')
@require_auth
def google_ads_diagnose_quality():
    """Diagnose low quality score keywords"""
    min_impressions = int(request.args.get('min_impressions', 100))
    
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.diagnose_low_quality_scores(min_impressions)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error diagnosing quality scores: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/diagnose/high-cost')
@require_auth
def google_ads_diagnose_cost():
    """Diagnose high cost campaigns"""
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.diagnose_high_cost_campaigns()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error diagnosing high cost campaigns: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/diagnose/disapproved-ads')
@require_auth
def google_ads_diagnose_disapproved():
    """Find disapproved ads"""
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.find_disapproved_ads()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error finding disapproved ads: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/query', methods=['POST'])
@require_auth
def google_ads_custom_query():
    """Execute a custom GAQL query"""
    try:
        data = request.json
        query = data.get('query')
        customer_id = data.get('customer_id')
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'}), 400
        
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.run_custom_query(query, customer_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error executing custom query: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/nlp', methods=['POST'])
@require_auth
def google_ads_natural_language():
    """Process a natural language request"""
    try:
        data = request.json
        request_text = data.get('request')
        
        if not request_text:
            return jsonify({'success': False, 'error': 'Request text is required'}), 400
        
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        result = mcp.process_natural_language_request(request_text)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error processing NL request: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/google-ads/tools')
@require_auth
def google_ads_tools():
    """Get list of available Google Ads MCP tools"""
    try:
        from google_ads import GoogleAdsMCPServer
        mcp = GoogleAdsMCPServer()
        tools = mcp.get_available_tools()
        return jsonify({'success': True, 'tools': tools})
    except Exception as e:
        logger.error(f"Error getting tools: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    # Create output directory
    settings.output_dir.mkdir(exist_ok=True)
    
    # Run the app on port 8000 (to avoid macOS AirPlay conflict)
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
