"""
Google Ads API Client
Handles authentication and API interactions with Google Ads
"""
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import yaml

try:
    from google.ads.googleads.client import GoogleAdsClient as GadsClient
    from google.ads.googleads.errors import GoogleAdsException
    GOOGLE_ADS_AVAILABLE = True
except ImportError:
    GOOGLE_ADS_AVAILABLE = False
    GadsClient = None
    GoogleAdsException = Exception

logger = logging.getLogger(__name__)


class GoogleAdsClient:
    """
    Wrapper for Google Ads API client with MCP support
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize Google Ads client
        
        Args:
            config_path: Path to google-ads.yaml config file
        """
        if not GOOGLE_ADS_AVAILABLE:
            raise ImportError(
                "Google Ads API library not installed. "
                "Install with: pip install google-ads"
            )
        
        self.config_path = config_path or self._get_default_config_path()
        self.client = None
        self._initialize_client()
    
    def _get_default_config_path(self) -> str:
        """Get default config path from home directory"""
        home = Path.home()
        config_file = home / 'google-ads.yaml'
        
        if not config_file.exists():
            # Also check current directory
            config_file = Path('google-ads.yaml')
            if not config_file.exists():
                raise FileNotFoundError(
                    "google-ads.yaml not found. Please create it with your API credentials.\n"
                    "See: https://developers.google.com/google-ads/api/docs/client-libs/python/configuration"
                )
        
        return str(config_file)
    
    def _initialize_client(self):
        """Initialize the Google Ads API client"""
        try:
            self.client = GadsClient.load_from_storage(self.config_path)
            logger.info(f"Google Ads client initialized from {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to initialize Google Ads client: {e}")
            raise
    
    def get_customer_id(self) -> Optional[str]:
        """Get the login customer ID from config"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('login_customer_id')
        except Exception as e:
            logger.error(f"Error reading customer ID: {e}")
            return None
    
    def list_accessible_customers(self) -> List[Dict[str, str]]:
        """
        List all accessible customer accounts
        
        Returns:
            List of customer dictionaries with id and descriptive_name
        """
        try:
            customer_service = self.client.get_service("CustomerService")
            accessible_customers = customer_service.list_accessible_customers()
            
            customers = []
            for resource_name in accessible_customers.resource_names:
                customer_id = resource_name.split('/')[-1]
                customers.append({
                    'id': customer_id,
                    'resource_name': resource_name
                })
            
            logger.info(f"Found {len(customers)} accessible customers")
            return customers
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error: {ex}")
            raise
        except Exception as e:
            logger.error(f"Error listing customers: {e}")
            raise
    
    def get_customer_info(self, customer_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a customer account
        
        Args:
            customer_id: The customer ID (without dashes)
        
        Returns:
            Dictionary with customer information
        """
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            
            query = """
                SELECT
                    customer.id,
                    customer.descriptive_name,
                    customer.currency_code,
                    customer.time_zone,
                    customer.manager,
                    customer.test_account
                FROM customer
                WHERE customer.id = {customer_id}
            """.format(customer_id=customer_id)
            
            response = ga_service.search(customer_id=customer_id, query=query)
            
            for row in response:
                customer = row.customer
                return {
                    'id': customer.id,
                    'name': customer.descriptive_name,
                    'currency': customer.currency_code,
                    'time_zone': customer.time_zone,
                    'is_manager': customer.manager,
                    'is_test': customer.test_account
                }
            
            return {}
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error: {ex}")
            raise
        except Exception as e:
            logger.error(f"Error getting customer info: {e}")
            raise
    
    def search(self, customer_id: str, query: str) -> List[Dict[str, Any]]:
        """
        Execute a Google Ads Query Language (GAQL) query
        
        Args:
            customer_id: The customer ID
            query: GAQL query string
        
        Returns:
            List of result rows as dictionaries
        """
        try:
            ga_service = self.client.get_service("GoogleAdsService")
            response = ga_service.search(customer_id=customer_id, query=query)
            
            results = []
            for row in response:
                results.append(self._row_to_dict(row))
            
            logger.info(f"Query returned {len(results)} results")
            return results
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error: {ex}")
            self._handle_google_ads_exception(ex)
            raise
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    def _row_to_dict(self, row) -> Dict[str, Any]:
        """Convert a search result row to dictionary"""
        result = {}
        
        # Extract common fields
        if hasattr(row, 'campaign'):
            result['campaign'] = {
                'id': row.campaign.id,
                'name': row.campaign.name,
                'status': row.campaign.status.name if hasattr(row.campaign, 'status') else None
            }
        
        if hasattr(row, 'ad_group'):
            result['ad_group'] = {
                'id': row.ad_group.id,
                'name': row.ad_group.name,
                'status': row.ad_group.status.name if hasattr(row.ad_group, 'status') else None
            }
        
        if hasattr(row, 'metrics'):
            result['metrics'] = {
                'impressions': row.metrics.impressions,
                'clicks': row.metrics.clicks,
                'cost_micros': row.metrics.cost_micros,
                'conversions': row.metrics.conversions if hasattr(row.metrics, 'conversions') else 0
            }
        
        return result
    
    def _handle_google_ads_exception(self, ex: GoogleAdsException):
        """Handle and log Google Ads API exceptions"""
        logger.error(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}"'
        )
        
        for error in ex.failure.errors:
            logger.error(f'\tError: {error.message}')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    logger.error(f'\t\tOn field: {field_path_element.field_name}')
    
    def validate_credentials(self) -> bool:
        """
        Validate that credentials are working
        
        Returns:
            True if credentials are valid
        """
        try:
            customers = self.list_accessible_customers()
            return len(customers) > 0
        except Exception as e:
            logger.error(f"Credential validation failed: {e}")
            return False

