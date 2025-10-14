"""
Google Ads Query Templates
Pre-built GAQL queries for common reporting and diagnostics
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta


class GoogleAdsQueries:
    """
    Collection of useful Google Ads Query Language (GAQL) queries
    """
    
    @staticmethod
    def get_campaigns_overview(
        date_range: str = "LAST_30_DAYS",
        status_filter: Optional[str] = None
    ) -> str:
        """
        Get overview of all campaigns with performance metrics
        
        Args:
            date_range: Date range for metrics (LAST_7_DAYS, LAST_30_DAYS, etc.)
            status_filter: Optional status filter (ENABLED, PAUSED, REMOVED)
        
        Returns:
            GAQL query string
        """
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                campaign.bidding_strategy_type,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions,
                metrics.cost_per_conversion
            FROM campaign
            WHERE segments.date DURING {date_range}
        """
        
        if status_filter:
            query += f" AND campaign.status = {status_filter}"
        
        query += " ORDER BY metrics.impressions DESC"
        
        return query
    
    @staticmethod
    def get_ad_groups_performance(
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS"
    ) -> str:
        """
        Get ad groups with performance metrics
        
        Args:
            campaign_id: Optional campaign ID to filter by
            date_range: Date range for metrics
        
        Returns:
            GAQL query string
        """
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                ad_group.id,
                ad_group.name,
                ad_group.status,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions
            FROM ad_group
            WHERE segments.date DURING {date_range}
        """
        
        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"
        
        query += " ORDER BY metrics.cost_micros DESC"
        
        return query
    
    @staticmethod
    def get_keywords_performance(
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS",
        min_impressions: int = 0
    ) -> str:
        """
        Get keywords with performance metrics
        
        Args:
            campaign_id: Optional campaign ID to filter by
            date_range: Date range for metrics
            min_impressions: Minimum impressions filter
        
        Returns:
            GAQL query string
        """
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                ad_group.id,
                ad_group.name,
                ad_group_criterion.keyword.text,
                ad_group_criterion.keyword.match_type,
                ad_group_criterion.status,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions,
                metrics.quality_score
            FROM keyword_view
            WHERE segments.date DURING {date_range}
                AND metrics.impressions >= {min_impressions}
        """
        
        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"
        
        query += " ORDER BY metrics.impressions DESC"
        
        return query
    
    @staticmethod
    def get_search_terms_report(
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_7_DAYS"
    ) -> str:
        """
        Get search terms report (actual queries that triggered ads)
        
        Args:
            campaign_id: Optional campaign ID to filter by
            date_range: Date range for metrics
        
        Returns:
            GAQL query string
        """
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                ad_group.id,
                ad_group.name,
                search_term_view.search_term,
                search_term_view.status,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.cost_micros,
                metrics.conversions
            FROM search_term_view
            WHERE segments.date DURING {date_range}
        """
        
        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"
        
        query += " ORDER BY metrics.impressions DESC"
        
        return query
    
    @staticmethod
    def get_ads_performance(
        campaign_id: Optional[str] = None,
        ad_group_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS"
    ) -> str:
        """
        Get ads with performance metrics
        
        Args:
            campaign_id: Optional campaign ID to filter by
            ad_group_id: Optional ad group ID to filter by
            date_range: Date range for metrics
        
        Returns:
            GAQL query string
        """
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                ad_group.id,
                ad_group.name,
                ad_group_ad.ad.id,
                ad_group_ad.ad.type,
                ad_group_ad.status,
                ad_group_ad.ad.responsive_search_ad.headlines,
                ad_group_ad.ad.responsive_search_ad.descriptions,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions
            FROM ad_group_ad
            WHERE segments.date DURING {date_range}
        """
        
        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"
        if ad_group_id:
            query += f" AND ad_group.id = {ad_group_id}"
        
        query += " ORDER BY metrics.impressions DESC"
        
        return query
    
    @staticmethod
    def get_campaign_budget_info(campaign_id: Optional[str] = None) -> str:
        """
        Get campaign budget information
        
        Args:
            campaign_id: Optional campaign ID to filter by
        
        Returns:
            GAQL query string
        """
        query = """
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                campaign_budget.amount_micros,
                campaign_budget.delivery_method,
                campaign.target_spend.cpc_bid_ceiling_micros,
                campaign.target_spend.target_spend_micros
            FROM campaign
        """
        
        if campaign_id:
            query += f" WHERE campaign.id = {campaign_id}"
        
        return query
    
    @staticmethod
    def get_negative_keywords(campaign_id: Optional[str] = None) -> str:
        """
        Get negative keywords at campaign and ad group level
        
        Args:
            campaign_id: Optional campaign ID to filter by
        
        Returns:
            GAQL query string
        """
        query = """
            SELECT
                campaign.id,
                campaign.name,
                campaign_criterion.criterion_id,
                campaign_criterion.keyword.text,
                campaign_criterion.keyword.match_type,
                campaign_criterion.negative
            FROM campaign_criterion
            WHERE campaign_criterion.negative = TRUE
        """
        
        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"
        
        return query
    
    @staticmethod
    def get_geographic_performance(
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS"
    ) -> str:
        """
        Get performance by geographic location
        
        Args:
            campaign_id: Optional campaign ID to filter by
            date_range: Date range for metrics
        
        Returns:
            GAQL query string
        """
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                geographic_view.country_criterion_id,
                geographic_view.location_type,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.cost_micros,
                metrics.conversions
            FROM geographic_view
            WHERE segments.date DURING {date_range}
        """
        
        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"
        
        query += " ORDER BY metrics.impressions DESC"
        
        return query
    
    @staticmethod
    def get_device_performance(
        campaign_id: Optional[str] = None,
        date_range: str = "LAST_30_DAYS"
    ) -> str:
        """
        Get performance by device type
        
        Args:
            campaign_id: Optional campaign ID to filter by
            date_range: Date range for metrics
        
        Returns:
            GAQL query string
        """
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                segments.device,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions
            FROM campaign
            WHERE segments.date DURING {date_range}
        """
        
        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"
        
        query += " ORDER BY segments.device, metrics.impressions DESC"
        
        return query
    
    @staticmethod
    def get_account_summary(date_range: str = "LAST_30_DAYS") -> str:
        """
        Get high-level account summary
        
        Args:
            date_range: Date range for metrics
        
        Returns:
            GAQL query string
        """
        return f"""
            SELECT
                customer.id,
                customer.descriptive_name,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions,
                metrics.cost_per_conversion
            FROM customer
            WHERE segments.date DURING {date_range}
        """
    
    @staticmethod
    def diagnose_low_quality_score(min_impressions: int = 100) -> str:
        """
        Find keywords with low quality scores
        
        Args:
            min_impressions: Minimum impressions threshold
        
        Returns:
            GAQL query string
        """
        return f"""
            SELECT
                campaign.id,
                campaign.name,
                ad_group.id,
                ad_group.name,
                ad_group_criterion.keyword.text,
                ad_group_criterion.keyword.match_type,
                metrics.quality_score,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr
            FROM keyword_view
            WHERE segments.date DURING LAST_30_DAYS
                AND metrics.impressions >= {min_impressions}
                AND metrics.quality_score < 5
            ORDER BY metrics.impressions DESC
        """
    
    @staticmethod
    def diagnose_high_cost_low_conversion() -> str:
        """
        Find campaigns with high cost but low conversions
        
        Returns:
            GAQL query string
        """
        return """
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                metrics.cost_micros,
                metrics.conversions,
                metrics.cost_per_conversion
            FROM campaign
            WHERE segments.date DURING LAST_30_DAYS
                AND metrics.cost_micros > 100000000
                AND metrics.conversions < 10
            ORDER BY metrics.cost_micros DESC
        """
    
    @staticmethod
    def find_disapproved_ads() -> str:
        """
        Find all disapproved ads that need attention
        
        Returns:
            GAQL query string
        """
        return """
            SELECT
                campaign.id,
                campaign.name,
                ad_group.id,
                ad_group.name,
                ad_group_ad.ad.id,
                ad_group_ad.policy_summary.approval_status,
                ad_group_ad.policy_summary.review_status
            FROM ad_group_ad
            WHERE ad_group_ad.policy_summary.approval_status = 'DISAPPROVED'
        """

