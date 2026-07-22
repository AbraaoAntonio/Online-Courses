import logging
from typing import List
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from app.config import REQUEST_HEADERS, REQUEST_TIMEOUT_SECONDS
from app.scrapers.base import ProductResult, fallback_result, parse_brl_price

logger = logging.getLogger(__name__)

SITE_NAME = "Magazine Luiza"
SEARCH_PAGE_URL = "https://www.magazineluiza.com.br/busca/{query}/"
RESULTS_LIMIT = 8


def search(query: str) -> List[ProductResult]:
    """Best-effort HTML scraping. Magazine Luiza renders search results
    client-side with React, so a plain HTTP GET frequently returns none
    of the product cards (they're injected by JS after load). This will
    usually fall back to a plain search link — a headless browser
    (Playwright/Selenium) would be needed for reliable scraping here.
    See README for details."""
    search_url = SEARCH_PAGE_URL.format(query=quote_plus(query))
    try:
        response = requests.get(
            search_url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Magazine Luiza search failed for %r: %s", query, exc)
        return [fallback_result(SITE_NAME, query, search_url)]

    soup = BeautifulSoup(response.text, "lxml")
    results = []
    for card in soup.select('[data-testid="product-card-container"]')[:RESULTS_LIMIT]:
        title_el = card.select_one('[data-testid="product-title"]')
        price_el = card.select_one('[data-testid="price-value"]')
        link_el = card if card.name == "a" else card.select_one("a")
        image_el = card.select_one("img")

        if not title_el or not link_el or not link_el.get("href"):
            continue

        href = link_el["href"]
        url = href if href.startswith("http") else f"https://www.magazineluiza.com.br{href}"
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
