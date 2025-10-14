#!/usr/bin/env python3
"""
Example script demonstrating Google Ads MCP integration
Shows how to combine Google Ads data with AI-generated content
"""
import logging
from datetime import datetime
from google_ads import GoogleAdsMCPServer
from ai import AIGenerator
from exporters import ExcelExporter
from config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_1_basic_queries():
    """Example 1: Basic Google Ads queries"""
    print("\n" + "="*60)
    print("Example 1: Basic Google Ads Queries")
    print("="*60 + "\n")
    
    # Initialize MCP server
    mcp = GoogleAdsMCPServer()
    
    # List accounts
    print("📋 Your Google Ads accounts:")
    accounts = mcp.list_accounts()
    if accounts['success']:
        for acc in accounts['accounts'][:5]:
            print(f"  - {acc['id']}: {acc['resource_name']}")
    
    # Get account summary
    print("\n📊 Account summary (Last 30 days):")
    summary = mcp.get_account_summary("LAST_30_DAYS")
    if summary['success'] and summary['summary']:
        metrics = summary['summary'].get('metrics', {})
        print(f"  Impressions: {metrics.get('impressions', 0):,}")
        print(f"  Clicks: {metrics.get('clicks', 0):,}")
        print(f"  Cost: ${metrics.get('cost_micros', 0) / 1_000_000:.2f}")
        print(f"  Conversions: {metrics.get('conversions', 0):.1f}")
    
    # Get campaigns
    print("\n🎯 Top campaigns:")
    campaigns = mcp.get_campaigns("LAST_30_DAYS")
    if campaigns['success']:
        for i, camp in enumerate(campaigns['campaigns'][:5], 1):
            camp_data = camp.get('campaign', {})
            metrics = camp.get('metrics', {})
            print(f"  {i}. {camp_data.get('name', 'N/A')}")
            print(f"     Impressions: {metrics.get('impressions', 0):,}, "
                  f"Clicks: {metrics.get('clicks', 0):,}")


def example_2_diagnostics():
    """Example 2: Automated diagnostics"""
    print("\n" + "="*60)
    print("Example 2: Automated Diagnostics")
    print("="*60 + "\n")
    
    mcp = GoogleAdsMCPServer()
    
    # Find low quality keywords
    print("🔍 Checking for low quality score keywords...")
    quality_issues = mcp.diagnose_low_quality_scores(min_impressions=100)
    
    if quality_issues['success']:
        count = quality_issues['count']
        if count > 0:
            print(f"⚠️  Found {count} keywords with quality score < 5")
            print(f"💡 Recommendation: {quality_issues.get('recommendation', '')}")
            
            for kw in quality_issues['low_quality_keywords'][:3]:
                print(f"\n  Keyword: {kw.get('keyword', 'N/A')}")
                print(f"  Quality Score: {kw.get('quality_score', 'N/A')}")
                print(f"  Impressions: {kw.get('metrics', {}).get('impressions', 0):,}")
        else:
            print("✅ No quality issues found!")
    
    # Find expensive campaigns
    print("\n💰 Checking for high-cost low-conversion campaigns...")
    cost_issues = mcp.diagnose_high_cost_campaigns()
    
    if cost_issues['success']:
        count = cost_issues['count']
        if count > 0:
            print(f"⚠️  Found {count} campaigns with high cost but low conversions")
            print(f"💡 Recommendation: {cost_issues.get('recommendation', '')}")
        else:
            print("✅ No cost issues found!")


def example_3_natural_language():
    """Example 3: Natural language queries"""
    print("\n" + "="*60)
    print("Example 3: Natural Language Queries")
    print("="*60 + "\n")
    
    mcp = GoogleAdsMCPServer()
    
    # Example queries
    queries = [
        "Show me campaigns",
        "Find keywords with low quality",
        "Get search terms",
        "Show me keywords"
    ]
    
    for query in queries:
        print(f"\n💬 Query: '{query}'")
        result = mcp.process_natural_language_request(query)
        
        if result['success']:
            count = result.get('count', 0)
            print(f"   ✓ Found {count} results")
        else:
            print(f"   ✗ Error: {result.get('error', 'Unknown')}")


def example_4_combine_with_content_generation():
    """Example 4: Combine Google Ads data with AI content generation"""
    print("\n" + "="*60)
    print("Example 4: Combine Google Ads Data with Content Generation")
    print("="*60 + "\n")
    
    # Step 1: Get top performing keywords from Google Ads
    print("📊 Step 1: Getting top performing keywords from your account...")
    mcp = GoogleAdsMCPServer()
    keywords_result = mcp.get_keywords(date_range="LAST_30_DAYS", min_impressions=100)
    
    if not keywords_result['success']:
        print(f"Error getting keywords: {keywords_result.get('error')}")
        return
    
    # Extract high-performing keywords (those with conversions)
    all_keywords = keywords_result['keywords']
    top_keywords = [
        kw.get('keyword', '')
        for kw in all_keywords[:20]
        if kw.get('metrics', {}).get('conversions', 0) > 0
    ]
    
    # Fallback to high-impression keywords if no conversions
    if not top_keywords:
        top_keywords = [kw.get('keyword', '') for kw in all_keywords[:20]]
    
    print(f"✓ Found {len(top_keywords)} high-performing keywords:")
    for i, kw in enumerate(top_keywords[:5], 1):
        print(f"  {i}. {kw}")
    
    # Step 2: Use these keywords with FAB analysis to generate new ads
    print("\n🤖 Step 2: Generating new ads based on your top keywords...")
    
    # Create a simple FAB analysis (in real use, this would come from website parsing)
    fab_analysis = {
        'product_name': 'Your Product',
        'target_audience': 'Your Target Audience',
        'unique_value_proposition': 'Your unique value',
        'fab_statements': [
            {
                'feature': 'Premium Quality',
                'advantage': 'Lasts Longer',
                'benefit': 'Save Money',
                'bab_format': 'Save money with products that last longer thanks to premium quality'
            }
        ]
    }
    
    try:
        ai_gen = AIGenerator()
        new_ads = ai_gen.generate_google_ads(fab_analysis, top_keywords[:10])
        
        print(f"✓ Generated {len(new_ads.get('ads', []))} new ad variations")
        
        # Show first ad
        if new_ads.get('ads'):
            first_ad = new_ads['ads'][0]
            print("\n📝 Example generated ad:")
            print(f"   Headlines: {', '.join(first_ad.get('headlines', [])[:3])}")
            print(f"   Description: {first_ad.get('descriptions', [''])[0]}")
        
        # Export to Excel
        print("\n💾 Step 3: Exporting to Excel...")
        exporter = ExcelExporter(settings.output_dir)
        
        # Prepare keywords data for export
        keywords_data = {
            'keywords': [
                {'keyword': kw, 'match_type': 'BROAD', 'category': 'From Google Ads'}
                for kw in top_keywords[:20]
            ]
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"google_ads_integration_{timestamp}.xlsx"
        filepath = exporter.export_google_ads(keywords_data, new_ads, filename)
        
        print(f"✓ Saved to: {filepath}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        logger.exception("Error in content generation")


def example_5_search_terms_analysis():
    """Example 5: Analyze actual search terms"""
    print("\n" + "="*60)
    print("Example 5: Search Terms Analysis")
    print("="*60 + "\n")
    
    mcp = GoogleAdsMCPServer()
    
    print("🔍 Getting search terms (what users actually searched for)...")
    result = mcp.get_search_terms(date_range="LAST_7_DAYS")
    
    if result['success']:
        terms = result['search_terms']
        print(f"✓ Found {result['count']} search terms\n")
        
        print("Top search terms by impressions:")
        for i, term in enumerate(terms[:10], 1):
            metrics = term.get('metrics', {})
            print(f"  {i}. {term.get('search_term', 'N/A')}")
            print(f"     Impressions: {metrics.get('impressions', 0):,}, "
                  f"Clicks: {metrics.get('clicks', 0):,}, "
                  f"Cost: ${metrics.get('cost_micros', 0) / 1_000_000:.2f}")
    else:
        print(f"Error: {result.get('error')}")


def example_6_custom_gaql_query():
    """Example 6: Custom GAQL query"""
    print("\n" + "="*60)
    print("Example 6: Custom GAQL Query")
    print("="*60 + "\n")
    
    mcp = GoogleAdsMCPServer()
    
    # Custom query to get campaigns with specific metrics
    query = """
        SELECT 
            campaign.id,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.cost_micros
        FROM campaign
        WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.impressions DESC
        LIMIT 5
    """
    
    print("📊 Running custom GAQL query:")
    print(query)
    
    result = mcp.run_custom_query(query)
    
    if result['success']:
        print(f"\n✓ Query returned {result['count']} results\n")
        for i, row in enumerate(result['results'], 1):
            camp = row.get('campaign', {})
            metrics = row.get('metrics', {})
            print(f"  {i}. {camp.get('name', 'N/A')}")
            print(f"     Impressions: {metrics.get('impressions', 0):,}, "
                  f"Clicks: {metrics.get('clicks', 0):,}")
    else:
        print(f"Error: {result.get('error')}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("Google Ads MCP Integration Examples")
    print("="*60)
    
    try:
        # Check if Google Ads is configured
        print("\n🔧 Checking Google Ads configuration...")
        mcp = GoogleAdsMCPServer()
        
        if not mcp.client.validate_credentials():
            print("❌ Google Ads credentials not valid!")
            print("\n📖 Please follow the setup guide:")
            print("   1. See GOOGLE_ADS_SETUP.md for detailed instructions")
            print("   2. Or see QUICKSTART_GOOGLE_ADS.md for quick start")
            return
        
        print("✅ Google Ads API is configured and working!\n")
        
        # Run examples
        example_1_basic_queries()
        example_2_diagnostics()
        example_3_natural_language()
        example_5_search_terms_analysis()
        example_6_custom_gaql_query()
        
        # This one might take longer due to AI generation
        print("\n" + "="*60)
        run_generation = input("\nRun content generation example? (y/n): ").lower()
        if run_generation == 'y':
            example_4_combine_with_content_generation()
        
        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60 + "\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n📖 Setup required:")
        print("   1. Copy google-ads.yaml.example to google-ads.yaml")
        print("   2. Fill in your API credentials")
        print("   3. See GOOGLE_ADS_SETUP.md for help")
        
    except ImportError:
        print("\n❌ Error: Google Ads library not installed")
        print("\n📦 Install with:")
        print("   pip install google-ads PyYAML")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.exception("Error running examples")


if __name__ == '__main__':
    main()

