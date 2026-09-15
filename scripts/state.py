"""
Ortak durum (state) yardımcıları — state/last_run.json dosyasını okur/yazar.

Bu dosya diğer scriptler tarafından import edilir (CLI aracı değildir).
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from datetime import datetime, timezone

STATE_PATH = Path("state/last_run.json")
MAX_HISTORY = 50


def read_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"runs": []}


def append_run(entry: dict) -> None:
    """Bir çalıştırmanın sonucunu (başarı/hata) state dosyasına ekler."""
    state = read_state()
    entry = dict(entry)
    entry.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    state.setdefault("runs", []).append(entry)
    state["runs"] = state["runs"][-MAX_HISTORY:]
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def last_special_kind() -> str | None:
    """Çeşitlilik için: en son kullanılan özel slayt tipini döner (varsa)."""
    state = read_state()
    for run in reversed(state.get("runs", [])):
        kind = run.get("special_kind")
        if kind:
            return kind
    return None


def slugify(text: str) -> str:
    """Konuyu dosya/URL güvenli bir slug'a çevirir (Türkçe karakterleri sadeleştirir)."""
    replacements = {
        "ı": "i", "İ": "i", "ğ": "g", "Ğ": "g", "ü": "u", "Ü": "u",
        "ş": "s", "Ş": "s", "ö": "o", "Ö": "o", "ç": "c", "Ç": "c",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:60] or "carousel"
