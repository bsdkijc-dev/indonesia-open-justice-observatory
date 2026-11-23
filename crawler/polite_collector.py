"""Polite, resumable, cached collector with exponential backoff and provenance logging."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Callable, Optional

import requests

from crawler.provenance import ProvenanceRecord, compute_sha256, record_provenance, utc_now_iso


class PoliteCollector:
    def __init__(
        self,
        cache_dir: Path,
        provenance_log: Path,
        min_delay_sec: float = 2.0,
        max_retries: int = 3,
        user_agent: str = "IOJO-ResearchBot/1.0 (+https://github.com/bsdkijc-dev/indonesia-open-justice-observatory)",
        http_get: Optional[Callable[..., requests.Response]] = None,
    ) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.provenance_log = provenance_log
        self.min_delay_sec = min_delay_sec
        self.max_retries = max_retries
        self.user_agent = user_agent
        self._http_get = http_get or requests.get
        self._last_request_ts = 0.0
        self._visited_urls: set[str] = set()

    def _cache_key(self, url: str) -> str:
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    def _respect_rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request_ts
        if elapsed < self.min_delay_sec:
            time.sleep(self.min_delay_sec - elapsed)
        self._last_request_ts = time.monotonic()

    def fetch(self, url: str, source_id: str, job_id: str, file_format: str = "html") -> Optional[bytes]:
        key = self._cache_key(url)
        cached_file = self.cache_dir / f"{key}.{file_format}"
        cached_meta = self.cache_dir / f"{key}.meta.json"

        # Resumable / duplicate-prevention check via cache
        if cached_file.exists() and cached_meta.exists():
            content = cached_file.read_bytes()
            record_provenance(
                ProvenanceRecord(
                    job_id=job_id,
                    source_id=source_id,
                    url=url,
                    retrieval_timestamp=utc_now_iso(),
                    collection_method="CACHE_HIT",
                    http_status=200,
                    file_checksum=compute_sha256(content),
                    file_format=file_format,
                    extraction_status="CACHED",
                    validation_status="VERIFIED",
                ),
                self.provenance_log,
            )
            return content

        if url in self._visited_urls:
            return None
        self._visited_urls.add(url)

        backoff = 1.0
        for attempt in range(1, self.max_retries + 1):
            self._respect_rate_limit()
            try:
                resp = self._http_get(url, headers={"User-Agent": self.user_agent}, timeout=15)
                if resp.status_code in (401, 403, 429):
                    record_provenance(
                        ProvenanceRecord(
                            job_id=job_id,
                            source_id=source_id,
                            url=url,
                            retrieval_timestamp=utc_now_iso(),
                            collection_method="HTTP_GET",
                            http_status=resp.status_code,
                            file_checksum=None,
                            file_format=file_format,
                            extraction_status="HALTED_ACCESS_RESTRICTION",
                            validation_status="UNVERIFIED",
                            error_details=f"Stopped on HTTP {resp.status_code}; never bypass restrictions.",
                        ),
                        self.provenance_log,
                    )
                    return None

                if resp.status_code >= 500:
                    raise requests.HTTPError(f"Server error {resp.status_code}")

                resp.raise_for_status()
                content = resp.content
                checksum = compute_sha256(content)
                cached_file.write_bytes(content)
                cached_meta.write_text(
                    json.dumps({"url": url, "checksum": checksum, "status": resp.status_code}),
                    encoding="utf-8",
                )
                record_provenance(
                    ProvenanceRecord(
                        job_id=job_id,
                        source_id=source_id,
                        url=url,
                        retrieval_timestamp=utc_now_iso(),
                        collection_method="HTTP_GET",
                        http_status=resp.status_code,
                        file_checksum=checksum,
                        file_format=file_format,
                        extraction_status="COLLECTED",
                        validation_status="VERIFIED",
                    ),
                    self.provenance_log,
                )
                return content
            except requests.RequestException as exc:
                if attempt == self.max_retries:
                    record_provenance(
                        ProvenanceRecord(
                            job_id=job_id,
                            source_id=source_id,
                            url=url,
                            retrieval_timestamp=utc_now_iso(),
                            collection_method="HTTP_GET",
                            http_status=None,
                            file_checksum=None,
                            file_format=file_format,
                            extraction_status="FAILED",
                            validation_status="UNVERIFIED",
                            error_details=f"{exc.__class__.__name__}: {exc}",
                        ),
                        self.provenance_log,
                    )
                    return None
                time.sleep(backoff)
                backoff *= 2.0
        return None
