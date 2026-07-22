from app.scrapers import mercado_livre


class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

    def json(self):
        return self._json_data


def test_search_parses_results(monkeypatch):
    fake_payload = {
        "results": [
            {"title": "Fone Bluetooth JBL", "permalink": "https://ml/1", "price": 199.9, "thumbnail": "https://img/1"},
            {"title": "Fone Bluetooth Sony", "permalink": "https://ml/2", "price": 249.0, "thumbnail": "https://img/2"},
        ]
    }
    monkeypatch.setattr(
        mercado_livre.requests, "get", lambda *a, **k: FakeResponse(fake_payload)
    )

    results = mercado_livre.search("fone bluetooth")

    assert len(results) == 2
    assert results[0].price == 199.9
    assert results[0].site == "Mercado Livre"


def test_search_falls_back_on_error(monkeypatch):
    def raise_error(*args, **kwargs):
        raise mercado_livre.requests.RequestException("network down")

    monkeypatch.setattr(mercado_livre.requests, "get", raise_error)

    results = mercado_livre.search("fone bluetooth")

    assert len(results) == 1
    assert results[0].price is None
    assert "fone bluetooth" in results[0].title


def test_search_falls_back_on_empty_results(monkeypatch):
    monkeypatch.setattr(
        mercado_livre.requests, "get", lambda *a, **k: FakeResponse({"results": []})
    )

    results = mercado_livre.search("produto inexistente")

    assert len(results) == 1
    assert results[0].price is None
