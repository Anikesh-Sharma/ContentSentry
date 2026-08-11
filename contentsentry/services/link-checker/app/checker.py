import json
import httpx
from bs4 import BeautifulSoup
from .config import settings

def check_links(html: str) -> dict:
    """
    Parse HTML, find all <a href> links, and check each one.
    Returns a summary dict: total_links, broken_links, details.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Collect all http/https links
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http://") or href.startswith("https://"):
            links.append(href)

    results = []
    broken = 0

    for url in links:
        try:
            resp = httpx.head(
                url,
                timeout=settings.link_timeout,
                follow_redirects=True,
            )
            status = resp.status_code
            ok = status < 400
        except Exception as e:
            status = 0
            ok = False

        if not ok:
            broken += 1

        results.append({"url": url, "status": status, "ok": ok})

    return {
        "total_links": len(links),
        "broken_links": broken,
        "details": json.dumps(results),
    }
