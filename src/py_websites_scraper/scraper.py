import re
import asyncio
import aiohttp
from readability import Document
from typing import List, Dict, Any, Optional

async def fetch_and_parse(
    session: aiohttp.ClientSession,
    url: str,
    **kwargs: Any
) -> Dict[str, Any]:
    """Fetch an HTML page and extract title + main content."""
    try:
        async with session.get(url, **kwargs) as resp:
            if resp.status != 200:
                return {"url": url, "success": False, "error": f"Status {resp.status}"}
            html = await resp.text()
    except Exception as e:
        return {"url": url, "success": False, "error": f"Fetch error: {e}"}

    try:
        doc = Document(html)
        title = doc.short_title()
        summary_html = doc.summary()
        
        # clean up tags
        # Potentially, we can support optional param to clean HTML or not
        text = re.sub(r"<[^>]+>", "", summary_html)
        text = re.sub(r"\s+", " ", text).strip()
        return {"url": url, "success": True, "title": title, "content": text}
    except Exception as e:
        return {"url": url, "success": False, "error": f"Parse error: {e}"}

async def scrape_urls(
    urls: List[str],
    max_concurrency: int = 10,
    **kwargs: Any
) -> List[Dict[str, Any]]:
    """Scrape a list of URLs concurrently and return their extracted data.
    
    Args:
        urls: List of URLs to scrape
        max_concurrency: Maximum number of concurrent requests
        **kwargs: Any additional parameters to pass to aiohttp.ClientSession.get()
                 These parameters will be applied to all requests.
                 Common parameters include:
                 - headers: Dict[str, str] - HTTP headers
                 - proxy: str - Proxy URL
                 - timeout: Union[int, float, aiohttp.ClientTimeout] - Request timeout
                 - ssl: Union[bool, ssl.SSLContext] - SSL verification settings
                 - cookies: Union[Dict[str, str], aiohttp.CookieJar] - Request cookies
                 See aiohttp documentation for all available parameters.
    """
    sem = asyncio.Semaphore(max_concurrency)
    async with aiohttp.ClientSession() as session:
        async def bound_fetch(u):
            async with sem:
                return await fetch_and_parse(session, u, **kwargs)

        tasks = [bound_fetch(u) for u in urls]
        return await asyncio.gather(*tasks)
