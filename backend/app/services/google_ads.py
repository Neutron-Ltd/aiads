"""
Google Ads API service - production integration.
Fetches real campaign data, metrics, keywords, and search terms from Google Ads.
"""
from __future__ import annotations

from app.config import settings


def get_client():
    """Return configured Google Ads client, or None if not configured."""
    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ImportError:
        return None

    if not settings.google_ads_configured:
        return None

    credentials = {
        "developer_token": settings.google_ads_developer_token,
        "client_id": settings.google_ads_client_id,
        "client_secret": settings.google_ads_client_secret,
        "refresh_token": settings.google_ads_refresh_token,
    }
    if settings.google_ads_login_customer_id:
        credentials["login_customer_id"] = settings.google_ads_login_customer_id

    return GoogleAdsClient.load_from_dict(credentials)


def normalize_customer_id(customer_id: str) -> str:
    """Convert customer ID to format without dashes (required by API)."""
    return customer_id.replace("-", "")


def fetch_campaign_metrics(customer_id: str) -> list[dict]:
    """
    Fetch real campaign metrics from Google Ads API.
    Returns list of dicts with campaign name, spend, conversions, clicks, impressions, etc.
    """
    client = get_client()
    if not client:
        raise RuntimeError(
            "Google Ads API is not configured. Set GOOGLE_ADS_* environment variables."
        )

    customer_id_clean = normalize_customer_id(customer_id)

    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.clicks,
            metrics.impressions,
            metrics.average_cpc
        FROM campaign
        WHERE campaign.status != 'REMOVED'
        AND segments.date DURING LAST_30_DAYS
    """

    try:
        response = ga_service.search_stream(
            customer_id=customer_id_clean, query=query
        )
        results = []
        for batch in response:
            for row in batch.results:
                metrics = row.metrics
                results.append({
                    "campaign_id": row.campaign.id,
                    "campaign_name": row.campaign.name,
                    "status": row.campaign.status.name,
                    "cost_micros": metrics.cost_micros,
                    "cost": metrics.cost_micros / 1_000_000,
                    "conversions": metrics.conversions,
                    "conversions_value": metrics.conversions_value,
                    "clicks": metrics.clicks,
                    "impressions": metrics.impressions,
                    "average_cpc_micros": metrics.average_cpc,
                    "average_cpc": metrics.average_cpc / 1_000_000 if metrics.average_cpc else 0,
                })
        return results
    except Exception as ex:
        try:
            from google.ads.googleads.errors import GoogleAdsException

            if isinstance(ex, GoogleAdsException):
                raise RuntimeError(
                    f"Google Ads API error: {ex.failure.errors[0].message}"
                    if ex.failure.errors
                    else str(ex)
                )
        except ImportError:
            pass
        raise


def fetch_search_terms(customer_id: str, limit: int = 100) -> list[dict]:
    """
    Fetch search terms report for optimization recommendations.
    Returns list of dicts with search term, clicks, impressions, cost, conversions.
    """
    client = get_client()
    if not client:
        raise RuntimeError(
            "Google Ads API is not configured. Set GOOGLE_ADS_* environment variables."
        )

    customer_id_clean = normalize_customer_id(customer_id)

    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            search_term_view.search_term,
            search_term_view.status,
            metrics.clicks,
            metrics.impressions,
            metrics.cost_micros,
            metrics.conversions
        FROM search_term_view
        WHERE segments.date DURING LAST_30_DAYS
        AND metrics.impressions > 0
        ORDER BY metrics.impressions DESC
        LIMIT {limit}
    """

    try:
        response = ga_service.search(
            customer_id=customer_id_clean, query=query
        )
        return [
            {
                "search_term": row.search_term_view.search_term,
                "status": row.search_term_view.status.name,
                "clicks": row.metrics.clicks,
                "impressions": row.metrics.impressions,
                "cost_micros": row.metrics.cost_micros,
                "cost": row.metrics.cost_micros / 1_000_000,
                "conversions": row.metrics.conversions,
            }
            for row in response
        ]
    except Exception as ex:
        try:
            from google.ads.googleads.errors import GoogleAdsException

            if isinstance(ex, GoogleAdsException):
                raise RuntimeError(
                    f"Google Ads API error: {ex.failure.errors[0].message}"
                    if ex.failure.errors
                    else str(ex)
                )
        except ImportError:
            pass
        raise
