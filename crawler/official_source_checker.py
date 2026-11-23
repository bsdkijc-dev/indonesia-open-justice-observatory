"""Official source checker for robots.txt, domain ownership, and access status."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse
import urllib.robotparser

import requests


ALLOWED_OFFICIAL_DOMAINS = (
    "mahkamahagung.go.id",
    "peraturan.bpk.go.id",
)


@dataclass
class SourceCheckResult:
    url: str
    is_official_domain: bool
    robots_accessible: bool
    crawl_allowed: Optional[bool]
    http_status: Optional[int]
    notes: str


def is_official_domain(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in ALLOWED_OFFICIAL_DOMAINS)


def check_source_access(url: str, user_agent: str = "IOJO-ResearchBot/1.0", timeout: int = 10) -> SourceCheckResult:
    if not is_official_domain(url):
        return SourceCheckResult(
            url=url,
            is_official_domain=False,
            robots_accessible=False,
            crawl_allowed=False,
            http_status=None,
            notes="Domain is not on the approved official domain allowlist.",
        )

    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        resp = requests.get(robots_url, headers={"User-Agent": user_agent}, timeout=timeout)
        if resp.status_code == 200:
            rp = urllib.robotparser.RobotFileParser()
            rp.parse(resp.text.splitlines())
            allowed = rp.can_fetch(user_agent, url)
            return SourceCheckResult(
                url=url,
                is_official_domain=True,
                robots_accessible=True,
                crawl_allowed=allowed,
                http_status=resp.status_code,
                notes="robots.txt parsed successfully.",
            )
        return SourceCheckResult(
            url=url,
            is_official_domain=True,
            robots_accessible=False,
            crawl_allowed=None,
            http_status=resp.status_code,
            notes=f"robots.txt returned HTTP {resp.status_code}; manual review required.",
        )
    except requests.RequestException as exc:
        return SourceCheckResult(
            url=url,
            is_official_domain=True,
            robots_accessible=False,
            crawl_allowed=None,
            http_status=None,
            notes=f"Network/access unavailable: {exc.__class__.__name__}",
        )
