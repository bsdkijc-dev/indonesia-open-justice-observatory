"""Source discovery helper for identifying official judicial document links."""

from __future__ import annotations

from typing import List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


def extract_official_links(html: str, base_url: str, extensions: tuple[str, ...] = (".pdf", ".csv", ".xlsx")) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    base_host = (urlparse(base_url).hostname or "").lower()
    discovered: List[str] = []
    seen = set()

    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        abs_url = urljoin(base_url, href)
        parsed = urlparse(abs_url)
        host = (parsed.hostname or "").lower()
        if host != base_host and not host.endswith(".mahkamahagung.go.id"):
            continue
        if any(parsed.path.lower().endswith(ext) for ext in extensions):
            if abs_url not in seen:
                seen.add(abs_url)
                discovered.append(abs_url)
    return discovered
