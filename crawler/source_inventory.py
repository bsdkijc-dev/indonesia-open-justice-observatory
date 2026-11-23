"""Source inventory loader and registry validator."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List


def load_source_inventory(csv_path: Path) -> List[Dict[str, str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def get_permitted_sources(csv_path: Path) -> List[Dict[str, str]]:
    rows = load_source_inventory(csv_path)
    return [
        r
        for r in rows
        if r.get("verification_status") == "VERIFIED"
        and "NO_AUTOMATED_COLLECTION" not in r.get("redistribution_permitted", "")
    ]
