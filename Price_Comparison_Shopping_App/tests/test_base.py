from app.scrapers.base import parse_brl_price


def test_parse_brl_price_with_thousands_separator():
    assert parse_brl_price("R$ 1.234,56") == 1234.56


def test_parse_brl_price_without_thousands_separator():
    assert parse_brl_price("R$ 99,90") == 99.90


def test_parse_brl_price_plain_dot_decimal():
    assert parse_brl_price("129.99") == 129.99


def test_parse_brl_price_empty_returns_none():
    assert parse_brl_price("") is None
    assert parse_brl_price(None) is None


def test_parse_brl_price_garbage_returns_none():
    assert parse_brl_price("indisponível") is None
