#!/usr/bin/env python3
"""
Uğur Akkaya Digital Pro — Konu Listelerini Güncelleme
=========================================================
state/current_carousel.json'daki sonuca göre content/topics_used.md ve
content/topics_backlog.md dosyalarını DETERMİNİSTİK metin işlemeriyle
günceller (LLM'e dosya düzenletmiyoruz — bu, dosya bütünlüğünü garanti
eder). Tekrar yasağının (MASTER_PROJECT_HANDOFF.md Bölüm 12 madde 1)
garantisi burasıdır.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_JSON = REPO_ROOT / "state" / "current_carousel.json"
TOPICS_USED = REPO_ROOT / "content" / "topics_used.md"
TOPICS_BACKLOG = REPO_ROOT / "content" / "topics_backlog.md"

ROW_PATTERN = re.compile(r"^\|\s*(\d+)\s*\|", re.MULTILINE)
BACKLOG_SECTION_PATTERN = re.compile(
    r"(## Hazır Bekleyen Konular\n)(.*?)(\n## )", re.DOTALL
)


def update_topics_used(topic: str) -> None:
    text = TOPICS_USED.read_text(encoding="utf-8")
    numbers = [int(m.group(1)) for m in ROW_PATTERN.finditer(text)]
    next_n = (max(numbers) + 1) if numbers else 1
    new_row = f"| {next_n} | {topic} | 7 | Otomatik üretildi ({date.today().isoformat()}) |\n"

    lines = text.split("\n")
    last_row_idx = None
    for i, line in enumerate(lines):
        if ROW_PATTERN.match(line):
            last_row_idx = i
    assert last_row_idx is not None, "topics_used.md içinde tablo satırı bulunamadı"

    lines.insert(last_row_idx + 1, new_row.rstrip("\n"))
    TOPICS_USED.write_text("\n".join(lines), encoding="utf-8")


def update_topics_backlog(chosen_topic: str, new_candidates: list[str]) -> None:
    text = TOPICS_BACKLOG.read_text(encoding="utf-8")
    match = BACKLOG_SECTION_PATTERN.search(text)
    assert match, "topics_backlog.md içinde 'Hazır Bekleyen Konular' bölümü bulunamadı"

    body = match.group(2)
    existing_lines = [ln for ln in body.split("\n") if ln.strip()]

    # Seçilen konuyu havuzdan çıkar (backlog'tan seçildiyse)
    remaining = [
        ln for ln in existing_lines
        if chosen_topic.strip().lower() not in ln.strip("- ").strip().lower()
    ]

    # Yeni adayları ekle (zaten varsa tekrar ekleme)
    existing_texts = {ln.strip("- ").strip().lower() for ln in remaining}
    for candidate in new_candidates:
        candidate = candidate.strip()
        if candidate and candidate.lower() not in existing_texts:
            remaining.append(f"- {candidate}")
            existing_texts.add(candidate.lower())

    new_body = "\n" + "\n".join(remaining) + "\n" if remaining else "\n"
    new_text = text[: match.start(2)] + new_body + text[match.end(2):]
    TOPICS_BACKLOG.write_text(new_text, encoding="utf-8")


def main() -> None:
    data = json.loads(CONTENT_JSON.read_text(encoding="utf-8"))
    topic = data["topic"]
    new_candidates = data.get("new_backlog_candidates") or []

    update_topics_used(topic)
    update_topics_backlog(topic, new_candidates)

    print(f"✓ topics_used.md güncellendi: '{topic}' eklendi")
    print(f"✓ topics_backlog.md güncellendi ({len(new_candidates)} yeni aday eklendi)")


if __name__ == "__main__":
    main()
