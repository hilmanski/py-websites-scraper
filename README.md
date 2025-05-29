# About
Scrape main content on multiple websites using Python in parallel. 

## Dependency
- [AsyncIO](https://docs.python.org/3/library/asyncio.html)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [Readability-lxml](https://pypi.org/project/readability-lxml/)

## How to use 
```
pip install py-web-scraper
```

Quick usage:
```
import asyncio
from py_websites_scraper import scrape_urls

urls = ["https://news.ycombinator.com", "https://example.com"]
data = asyncio.run(scrape_urls(urls, max_concurrency=5))
for item in data:
    print(item["url"], item.get("title"))
```

You can add any parameters for aiohttp to perform the request like headers, proxy, and more. Please check [aiohttp documentation](https://docs.aiohttp.org/en/stable/client_reference.html#clientrequest) for reference.

Example:
```
urls = []
results = await scrape_urls(
    urls,
    proxy="YOUR_PROXY_INFO",
    headers={"User-Agent": "USER_AGENT_INFO"},
)
```

## Limitation
- Gated content
- Dynamic generated content

## How the test the package locally for Dev
Install in editable mode:
```
pip install -e .
```

Run any file that importing this package
```
python test_local.py
```