import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from app.config import REQUEST_TIMEOUT_SECONDS
from app.scrapers import SCRAPERS
from app.scrapers.base import ProductResult

logger = logging.getLogger(__name__)


def compare_prices(query: str) -> List[ProductResult]:
    """Queries every configured site concurrently and returns results
    sorted so the cheapest priced item comes first; items with no
    parsed price (fallback links) are listed last."""
    results: List[ProductResult] = []

    with ThreadPoolExecutor(max_workers=len(SCRAPERS)) as executor:
        futures = {executor.submit(scraper.search, query): scraper for scraper in SCRAPERS}
        try:
            for future in as_completed(futures, timeout=REQUEST_TIMEOUT_SECONDS + 5):
                scraper = futures[future]
                try:
                    results.extend(future.result())
                except Exception as exc:
                    logger.warning("Scraper %s raised an exception: %s", scraper.__name__, exc)
        except TimeoutError:
            logger.warning("Some scrapers did not finish within the time budget")

    results.sort(key=lambda r: (r.price is None, r.price))
    return results


def cheapest(results: List[ProductResult]):
    priced = [r for r in results if r.has_price]
    return priced[0] if priced else None
