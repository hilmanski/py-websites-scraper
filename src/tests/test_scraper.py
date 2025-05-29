import asyncio
from py_websites_scraper import scrape_urls

def test_scrape_urls(monkeypatch):
    # monkeypatch a fake fetch_and_parse to avoid network calls
    results = asyncio.run(scrape_urls(["http://example.com"]))
    assert isinstance(results, list)
    assert "url" in results[0]
