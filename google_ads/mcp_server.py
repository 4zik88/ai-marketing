"""
Google Ads MCP Server
Model Context Protocol server for natural language interaction with Google Ads API
"""
import logging
from typing import Optional, Dict, Any, List, Callable
import json

from .ads_client import GoogleAdsClient
from .ads_queries import GoogleAdsQueries

logger = logging.getLogger(__name__)


class GoogleAdsMCPServer:
    """
    MCP Server for Google Ads API
    Provides natural language interface to Google Ads data
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize MCP server
        
        Args:
            config_path: Path to google-ads.yaml config file
        """
        self.client = GoogleAdsClient(config_path)
        self.queries = GoogleAdsQueries()
        self.customer_id = self.client.get_customer_id()
        
        # Register available tools
        self.tools = self._register_tools()
        
        logger.info("Google Ads MCP Server initialized")
    
    def _register_tools(self) -> Dict[str, Callable]:
        """Register all available MCP tools"""
        return {
            # Account Management
            'list_accounts': self.list_accounts,
            'get_account_info': self.get_account_info,
            'get_account_summary': self.get_account_summary,
            
            # Campaign Reporting
            'get_campaigns': self.get_campaigns,
            'get_campaign_performance': self.get_campaign_performance,
            'get_campaign_budget': self.get_campaign_budget,
            
            # Ad Group Reporting
            'get_ad_groups': self.get_ad_groups,
            
            # Keyword Reporting
            'get_keywords': self.get_keywords,
            'get_search_terms': self.get_search_terms,
            'get_negative_keywords': self.get_negative_keywords,
            
            # Ad Reporting
            'get_ads': self.get_ads,
            
            # Performance Analysis
            'get_geographic_performance': self.get_geographic_performance,
            'get_device_performance': self.get_device_performance,
            
            # Diagnostics
            'diagnose_low_quality_scores': self.diagnose_low_quality_scores,
            'diagnose_high_cost_campaigns': self.diagnose_high_cost_campaigns,
            'find_disapproved_ads': self.find_disapproved_ads,
            
            # Custom Query
            'run_custom_query': self.run_custom_query,
        }
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools with descriptions"""
        return [
            {
                'name': 'list_accounts',
                'description': 'List all accessible Google Ads accounts',
                'parameters': {}
            },
            {
                'name': 'get_account_info',
                'description': 'Get detailed information about a specific account',
                'parameters': {'customer_id': 'string (optional)'}
            },
            {
                'name': 'get_account_summary',
                'description': 'Get high-level performance summary for the account',
                'parameters': {'date_range': 'string (default: LAST_30_DAYS)'}
            },
            {
                'name': 'get_campaigns',
                'description': 'Get all campaigns with performance metrics',
                'parameters': {
                    'date_range': 'string (default: LAST_30_DAYS)',
                    'status_filter': 'string (optional: ENABLED, PAUSED, REMOVED)'
                }
            },
            {
                'name': 'get_campaign_performance',
                'description': 'Get detailed performance for a specific campaign',
                'parameters': {
                    'campaign_id': 'string (required)',
                    'date_range': 'string (default: LAST_30_DAYS)'
                }
            },
            {
                'name': 'get_keywords',
                'description': 'Get keyword performance data',
                'parameters': {
                    'campaign_id': 'string (optional)',
                    'date_range': 'string (default: LAST_30_DAYS)',
                    'min_impressions': 'int (default: 0)'
                }
            },
            {
                'name': 'get_search_terms',
                'description': 'Get search terms report (actual searches)',
                'parameters': {
                    'campaign_id': 'string (optional)',
                    'date_range': 'string (default: LAST_7_DAYS)'
                }
            },
            {
                'name': 'diagnose_low_quality_scores',
                'description': 'Find keywords with quality scores below 5',
                'parameters': {'min_impressions': 'int (default: 100)'}
            },
            {
                'name': 'diagnose_high_cost_campaigns',
                'description': 'Find campaigns with high spend but low conversions',
                'parameters': {}
            },
            {
                'name': 'run_custom_query',
                'description': 'Execute a custom GAQL query',
                'parameters': {
                    'query': 'string (required)',
                    'customer_id': 'string (optional)'
                }
            }
        ]
    
    # Account Management Tools
    
    def list_accounts(self) -> Dict[str, Any]:
        """List all accessible accounts"""
        try:
            customers = self.client.list_accessible_customers()
            return {
                'success': True,
                'count': len(customers),
                'accounts': customers
            }
        except Exception as e:
            logger.error(f"Error listing accounts: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_account_info(self, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """Get account information"""
        try:
            cid = customer_id or self.customer_id
            if not cid:
                return {'success': False, 'error': 'No customer ID provided'}
            
            info = self.client.get_customer_info(cid)
            return {
                'success': True,
                'account': info
            }
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_account_summary(self, date_range: str = "LAST_30_DAYS") -> Dict[str, Any]:
        """Get account summary with performance metrics"""
        try:
            query = self.queries.get_account_summary(date_range)
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'summary': results[0] if results else {},
                'date_range': date_range
            }
        except Exception as e:
            logger.error(f"Error getting account summary: {e}")
            return {'success': False, 'error': str(e)}
    
    # Campaign Tools
    
    def get_campaigns(
        self,
        date_range: str = "LAST_30_DAYS",
        status_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get all campaigns with metrics"""
        try:
            query = self.queries.get_campaigns_overview(date_range, status_filter)
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'campaigns': results,
                'date_range': date_range
            }
        except Exception as e:
            logger.error(f"Error getting campaigns: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_campaign_performance(
        self,
        campaign_id: str,
        date_range: str = "LAST_30_DAYS"
    ) -> Dict[str, Any]:
        """Get detailed campaign performance"""
        try:
            query = self.queries.get_campaigns_overview(date_range)
            results = self.client.search(self.customer_id, query)
            
            # Filter for specific campaign
            campaign_data = [r for r in results if str(r.get('campaign', {}).get('id')) == str(campaign_id)]
            
            return {
                'success': True,
                'campaign': campaign_data[0] if campaign_data else None,
                'date_range': date_range
            }
        except Exception as e:
            logger.error(f"Error getting campaign performance: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_campaign_budget(self, campaign_id: Optional[str] = None) -> Dict[str, Any]:
        """Get campaign budget information"""
        try:
            query = self.queries.get_campaign_budget_info(campaign_id)
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'budgets': results
            }
        except Exception as e:
            logger.error(f"Error getting budget info: {e}")
            return {'success': False, 'error': str(e)}
    
    # Ad Group Tools
    
    def get_ad_groups(
        self,
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS"
    ) -> Dict[str, Any]:
        """Get ad groups with performance"""
        try:
            query = self.queries.get_ad_groups_performance(campaign_id, date_range)
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'ad_groups': results,
                'date_range': date_range
            }
        except Exception as e:
            logger.error(f"Error getting ad groups: {e}")
            return {'success': False, 'error': str(e)}
    
    # Keyword Tools
    
    def get_keywords(
        self,
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS",
        min_impressions: int = 0
    ) -> Dict[str, Any]:
        """Get keyword performance"""
        try:
            query = self.queries.get_keywords_performance(campaign_id, date_range, min_impressions)
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'keywords': results,
                'date_range': date_range
            }
        except Exception as e:
            logger.error(f"Error getting keywords: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_search_terms(
        self,
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_7_DAYS"
    ) -> Dict[str, Any]:
        """Get search terms report"""
        try:
            query = self.queries.get_search_terms_report(campaign_id, date_range)
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'search_terms': results,
                'date_range': date_range
            }
        except Exception as e:
            logger.error(f"Error getting search terms: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_negative_keywords(self, campaign_id: Optional[str] = None) -> Dict[str, Any]:
        """Get negative keywords"""
        try:
            query = self.queries.get_negative_keywords(campaign_id)
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'negative_keywords': results
            }
        except Exception as e:
            logger.error(f"Error getting negative keywords: {e}")
            return {'success': False, 'error': str(e)}
    
    # Ad Tools
    
    def get_ads(
        self,
        campaign_id: Optional[str] = None,
        ad_group_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS"
    ) -> Dict[str, Any]:
        """Get ads with performance"""
        try:
            query = self.queries.get_ads_performance(campaign_id, ad_group_id, date_range)
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'ads': results,
                'date_range': date_range
            }
        except Exception as e:
            logger.error(f"Error getting ads: {e}")
            return {'success': False, 'error': str(e)}
    
    # Performance Analysis Tools
    
    def get_geographic_performance(
        self,
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS"
    ) -> Dict[str, Any]:
        """Get performance by geography"""
        try:
            query = self.queries.get_geographic_performance(campaign_id, date_range)
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'geographic_data': results,
                'date_range': date_range
            }
        except Exception as e:
            logger.error(f"Error getting geographic performance: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_device_performance(
        self,
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS"
    ) -> Dict[str, Any]:
        """Get performance by device"""
        try:
            query = self.queries.get_device_performance(campaign_id, date_range)
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'device_data': results,
                'date_range': date_range
            }
        except Exception as e:
            logger.error(f"Error getting device performance: {e}")
            return {'success': False, 'error': str(e)}
    
    # Diagnostic Tools
    
    def diagnose_low_quality_scores(self, min_impressions: int = 100) -> Dict[str, Any]:
        """Find keywords with low quality scores"""
        try:
            query = self.queries.diagnose_low_quality_score(min_impressions)
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'low_quality_keywords': results,
                'recommendation': 'Review ad relevance, landing pages, and expected CTR'
            }
        except Exception as e:
            logger.error(f"Error diagnosing quality scores: {e}")
            return {'success': False, 'error': str(e)}
    
    def diagnose_high_cost_campaigns(self) -> Dict[str, Any]:
        """Find campaigns with high cost but low conversions"""
        try:
            query = self.queries.diagnose_high_cost_low_conversion()
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'campaigns': results,
                'recommendation': 'Review targeting, ad copy, and landing page conversion rate'
            }
        except Exception as e:
            logger.error(f"Error diagnosing high cost campaigns: {e}")
            return {'success': False, 'error': str(e)}
    
    def find_disapproved_ads(self) -> Dict[str, Any]:
        """Find all disapproved ads"""
        try:
            query = self.queries.find_disapproved_ads()
            results = self.client.search(self.customer_id, query)
            return {
                'success': True,
                'count': len(results),
                'disapproved_ads': results,
                'recommendation': 'Review policy violations and update ad copy'
            }
        except Exception as e:
            logger.error(f"Error finding disapproved ads: {e}")
            return {'success': False, 'error': str(e)}
    
    # Custom Query
    
    def run_custom_query(
        self,
        query: str,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute a custom GAQL query"""
        try:
            cid = customer_id or self.customer_id
            results = self.client.search(cid, query)
            return {
                'success': True,
                'count': len(results),
                'results': results
            }
        except Exception as e:
            logger.error(f"Error executing custom query: {e}")
            return {'success': False, 'error': str(e)}
    
    def process_natural_language_request(self, request: str) -> Dict[str, Any]:
        """
        Process a natural language request and map it to appropriate tool
        
        This is a simple keyword-based router. In production, you'd use
        an LLM to parse the intent and extract parameters.
        
        Args:
            request: Natural language request string
        
        Returns:
            Tool execution result
        """
        request_lower = request.lower()
        
        # Account queries
        if any(word in request_lower for word in ['accounts', 'list accounts']):
            return self.list_accounts()
        
        if 'account summary' in request_lower or 'overview' in request_lower:
            return self.get_account_summary()
        
        # Campaign queries
        if 'campaigns' in request_lower and 'performance' not in request_lower:
            return self.get_campaigns()
        
        # Keyword queries
        if 'keywords' in request_lower:
            if 'low quality' in request_lower or 'quality score' in request_lower:
                return self.diagnose_low_quality_scores()
            elif 'negative' in request_lower:
                return self.get_negative_keywords()
            else:
                return self.get_keywords()
        
        # Search terms
        if 'search terms' in request_lower or 'search queries' in request_lower:
            return self.get_search_terms()
        
        # Diagnostics
        if 'high cost' in request_lower or 'expensive' in request_lower:
            return self.diagnose_high_cost_campaigns()
        
        if 'disapproved' in request_lower or 'rejected' in request_lower:
            return self.find_disapproved_ads()
        
        # Performance by dimension
        if 'geographic' in request_lower or 'location' in request_lower:
            return self.get_geographic_performance()
        
        if 'device' in request_lower:
            return self.get_device_performance()
        
        # Default
        return {
            'success': False,
            'error': 'Could not understand request. Please use one of the available tools.',
            'available_tools': self.get_available_tools()
        }

