import logging
from typing import List
from urllib.parse import quote_plus

import requests

from app.config import REQUEST_HEADERS, REQUEST_TIMEOUT_SECONDS
from app.scrapers.base import ProductResult, fallback_result

logger = logging.getLogger(__name__)

SITE_NAME = "Mercado Livre"
SEARCH_API_URL = "https://api.mercadolibre.com/sites/MLB/search"
SEARCH_PAGE_URL = "https://lista.mercadolivre.com.br/{query}"
RESULTS_LIMIT = 8


def search(query: str) -> List[ProductResult]:
    """Uses Mercado Livre's public search API (no auth required for
    basic product search), which is far more stable than scraping HTML."""
    search_page_url = SEARCH_PAGE_URL.format(query=quote_plus(query))
    try:
        response = requests.get(
            SEARCH_API_URL,
            params={"q": query, "limit": RESULTS_LIMIT},
            headers=REQUEST_HEADERS,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        logger.warning("Mercado Livre search failed for %r: %s", query, exc)
        return [fallback_result(SITE_NAME, query, search_page_url)]

    results = []
    for item in payload.get("results", []):
        title = item.get("title")
        url = item.get("permalink")
        if not title or not url:
            continue
        results.append(
            ProductResult(
                site=SITE_NAME,
                title=title,
                url=url,
                price=item.get("price"),
                image_url=item.get("thumbnail"),
            )
        )

    if not results:
        return [fallback_result(SITE_NAME, query, search_page_url)]
    return results
