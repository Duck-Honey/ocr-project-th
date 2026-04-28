"""Simple whitelist storage and matching for license plates."""

from __future__ import annotations

import os
from pathlib import Path

WHITELIST_PATH = Path(__file__).resolve().parent / "plate_whitelist.txt"


def _normalize(plate: str) -> str:
    return "".join(plate.upper().split())


def load_whitelist() -> set[str]:
    if not WHITELIST_PATH.exists():
        return set()
    lines = WHITELIST_PATH.read_text(encoding="utf-8").splitlines()
    return {_normalize(line) for line in lines if line.strip()}


def save_whitelist(plates: set[str]) -> None:
    items = sorted({_normalize(p) for p in plates if p.strip()})
    WHITELIST_PATH.write_text("\n".join(items) + ("\n" if items else ""), encoding="utf-8")


def add_plate(plate: str) -> set[str]:
    wl = load_whitelist()
    wl.add(_normalize(plate))
    save_whitelist(wl)
    return wl


def remove_plate(plate: str) -> set[str]:
    wl = load_whitelist()
    wl.discard(_normalize(plate))
    save_whitelist(wl)
    return wl


def should_allow_plate(plate: str, whitelist: set[str] | None = None) -> bool:
    """Allow all when PLATE_WHITELIST_ALLOW_ALL=1, otherwise require whitelist match."""
    if os.environ.get("PLATE_WHITELIST_ALLOW_ALL", "0").strip() == "1":
        return True
    wl = whitelist if whitelist is not None else load_whitelist()
    return _normalize(plate) in wl
