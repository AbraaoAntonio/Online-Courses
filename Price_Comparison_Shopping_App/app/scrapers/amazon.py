import logging
from typing import List
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from app.config import REQUEST_HEADERS, REQUEST_TIMEOUT_SECONDS
from app.scrapers.base import ProductResult, fallback_result, parse_brl_price

logger = logging.getLogger(__name__)

SITE_NAME = "Amazon"
SEARCH_PAGE_URL = "https://www.amazon.com.br/s?k={query}"
RESULTS_LIMIT = 8


def search(query: str) -> List[ProductResult]:
    """Best-effort HTML scraping. Amazon has no free public product-search
    API and actively changes its markup / blocks bots, so this is fragile
    by nature. If parsing fails or returns nothing, we fall back to a
    plain search link so the user still has something actionable.
    See README for notes on swapping this for a paid API (e.g. SerpApi)."""
    search_url = SEARCH_PAGE_URL.format(query=quote_plus(query))
    try:
        response = requests.get(
            search_url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Amazon search failed for %r: %s", query, exc)
        return [fallback_result(SITE_NAME, query, search_url)]

    soup = BeautifulSoup(response.text, "lxml")
    results = []
    for card in soup.select('div[data-component-type="s-search-result"]')[:RESULTS_LIMIT]:
        title_el = card.select_one("h2 span")
        link_el = card.select_one("h2 a")
        price_el = card.select_one("span.a-price > span.a-offscreen")
        image_el = card.select_one("img.s-image")

        if not title_el or not link_el or not link_el.get("href"):
            continue

        href = link_el["href"]
        url = href if href.startswith("http") else f"https://www.amazon.com.br{href}"
        results.append(
            ProductResult(
                site=SITE_NAME,
                title=title_el.get_text(strip=True),
                url=url,
                price=parse_brl_price(price_el.get_text()) if price_el else None,
                image_url=image_el["src"] if image_el and image_el.get("src") else None,
            )
        )

    if not results:
        return [fallback_result(SITE_NAME, query, search_url)]
    return results
