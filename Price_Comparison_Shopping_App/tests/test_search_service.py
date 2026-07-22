from app.scrapers.base import ProductResult
from app.services.search import cheapest, compare_prices


def test_compare_prices_sorts_by_price_and_pushes_no_price_last(monkeypatch):
    import app.services.search as search_module

    class FakeScraper:
        def __init__(self, name, results):
            self.__name__ = name
            self._results = results

        def search(self, query):
            return self._results

    scrapers = [
        FakeScraper("a", [ProductResult(site="A", title="a", url="u", price=300.0)]),
        FakeScraper("b", [ProductResult(site="B", title="b", url="u", price=None)]),
        FakeScraper("c", [ProductResult(site="C", title="c", url="u", price=100.0)]),
    ]
    monkeypatch.setattr(search_module, "SCRAPERS", scrapers)

    results = compare_prices("qualquer coisa")

    assert [r.site for r in results] == ["C", "A", "B"]
    assert cheapest(results).site == "C"


def test_cheapest_returns_none_when_no_priced_results():
    results = [ProductResult(site="A", title="a", url="u", price=None)]
    assert cheapest(results) is None
