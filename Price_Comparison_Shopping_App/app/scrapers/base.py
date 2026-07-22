import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote_plus


@dataclass
class ProductResult:
    site: str
    title: str
    url: str
    price: Optional[float] = None
    image_url: Optional[str] = None
    note: Optional[str] = None

    @property
    def has_price(self) -> bool:
        return self.price is not None


def build_query_url(base_url: str, query: str) -> str:
    return base_url.format(query=quote_plus(query))


_PRICE_CLEAN_RE = re.compile(r"[^\d,.]")


def parse_brl_price(raw: str) -> Optional[float]:
    """Parses strings like 'R$ 1.234,56' or '1234.56' into a float."""
    if not raw:
        return None
    cleaned = _PRICE_CLEAN_RE.sub("", raw).strip()
    if not cleaned:
        return None
    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


def fallback_result(site: str, query: str, search_url: str) -> ProductResult:
    """Used when a scraper can't extract structured results, so the client
    still gets a usable link instead of an empty response."""
    return ProductResult(
        site=site,
        title=f'Buscar "{query}" em {site}',
        url=search_url,
        price=None,
        note="Não foi possível ler os preços automaticamente. Abra o link e confira manualmente.",
    )
