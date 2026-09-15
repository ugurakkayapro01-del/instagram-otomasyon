#!/usr/bin/env python3
"""
Uğur Akkaya Digital Pro — Carousel İçerik Üretim Scripti
===========================================================
MASTER_PROJECT_HANDOFF.md kurallarına ve mevcut konu listelerine göre,
Claude'a (Anthropic Workload Identity Federation ile, statik API key
KULLANMADAN) bugünün 7 slaytlık carousel içeriğini ürettirir ve
yapılandırılmış JSON olarak state/current_carousel.json'a yazar.

Bu script HTML üretmez — sadece İÇERİK üretir (başlık, metin, ikon,
caption). HTML'i build_html.py, sabit ve doğrulanmış bir Python
şablonlama mantığıyla dolduracak. Bu ayrım bilerek yapıldı: progress
bar yüzdesi / sayfa numarası gibi hataya açık noktalar hiçbir zaman
LLM'e bırakılmıyor (bkz. MASTER_PROJECT_HANDOFF.md Bölüm 14 madde 6).

Kimlik doğrulama: ANTHROPIC_API_KEY YOK. Ortam değişkenlerinden
(ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID,
ANTHROPIC_IDENTITY_TOKEN_FILE) otomatik okunan WIF kimlik bilgileri
kullanılır — bunlar workflow tarafından sağlanır.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import anthropic

import state as st

REPO_ROOT = Path(__file__).resolve().parent.parent
SLIDE_COUNT = 7  # Otomasyon her zaman standart 7 slaytlık eğitim carousel'i üretir.
MODEL = os.environ.get("CAROUSEL_MODEL", "claude-sonnet-5")
OUTPUT_PATH = REPO_ROOT / "state" / "current_carousel.json"

ALLOWED_INNER_CLASSES = {
    "timeline", "trow", "tsec", "tconnect", "ttime", "tdesc",
    "funnel", "fun-step", "s1f", "s2f", "s3f", "s4f",
    "price-main", "split-row", "split-col", "sval", "slabel",
    "tier-row", "best", "tier-rank",
    "risk-row", "high", "med", "risk-dot", "thr-badge", "warn", "danger",
    "cmp-row", "cmp-col", "hl",
    "formula-box", "flabel", "fval",
    "chk-item", "chk-mark", "chk-txt",
    "bignum", "bignumsub",
}


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def build_system_prompt() -> str:
    handoff = read("MASTER_PROJECT_HANDOFF.md")
    topics_used = read("content/topics_used.md")
    topics_backlog = read("content/topics_backlog.md")
    caption_template = read("content/caption_template.md")
    last_special = st.last_special_kind() or "(yok)"
    allowed = ", ".join(sorted(ALLOWED_INNER_CLASSES))

    return f"""Sen Uğur Akkaya Digital Pro Instagram hesabı için carousel içeriği üreten bir sistemsin.
Aşağıdaki kural dosyasına harfiyen uy. Bu kurallar hiçbir zaman ihlal edilemez.

=== MASTER_PROJECT_HANDOFF.md ===
{handoff}

=== content/topics_used.md (ASLA TEKRAR ETME) ===
{topics_used}

=== content/topics_backlog.md ===
{topics_backlog}

=== content/caption_template.md ===
{caption_template}

=== GÖREVİN ===
1. Konu seç: Önce topics_backlog.md'deki "Hazır Bekleyen Konular" listesinden bir tane seç.
   Liste boşsa veya konu havuzu tükenmek üzereyse, topics_backlog.md'nin kendi
   "Yeni Konu Üretme Kuralları"na göre TAM OLARAK 4 yeni ileri seviye konu üret
   (topics_used.md'dekilerle asla örtüşmesin), bunlardan birini seç, kalan 3'ünü
   new_backlog_candidates alanına yaz.
2. Seçilen konu için TAM OLARAK {SLIDE_COUNT} slaytlık içerik yaz (Bölüm 4-6 kurallarına göre):
   - Slayt 1: hook (tag, title, subtitle)
   - Slayt 2, 5: light (açık zemin bilgi)
   - Slayt 3, 4, 6: dark veya special (koyu zemin bilgi ya da özel görsel tipi)
   - Slayt 7: cta
   Slayt 3-6 arasından TAM OLARAK BİRİNİ "special" tipinde yap (timeline, funnel,
   tier, risk, comparison, formula veya stat — çeşitlilik için en son kullanılan
   tip şuydu, onu TEKRAR KULLANMA: {last_special}).
3. "special" slaytın inner_html alanında SADECE şu CSS sınıflarını kullanabilirsin
   (başka hiçbir class veya <script>/<style>/<a>/on*= attribute KULLANMA):
   {allowed}
   inner_html, slaydın num/icon/title başlığından SONRA, pill/logo/sayfa numarası
   ayağından ÖNCE gelen içerik alanını doldurur — kendi başlık/footer'ını üretme.
4. Caption'ı content/caption_template.md şablonuna göre TAM OLARAK 10 hashtag
   (2-3 niche + 7-8 sabit genel havuzdan) ile yaz.
5. SADECE aşağıdaki JSON şemasında, başka hiçbir açıklama/markdown olmadan cevap ver:

{{
  "topic": "string",
  "is_new_topic": true/false,
  "new_backlog_candidates": ["string", ...],
  "special_kind": "timeline|funnel|tier|risk|comparison|formula|stat",
  "slides": [
    {{"kind": "hook", "tag": "string", "title": "satır1\\nsatır2\\n**vurgu**", "subtitle": "string"}},
    {{"kind": "light|dark", "num_label": "string", "icon": "emoji", "title": "string", "body": "string (düz metin, checklist ise madde başına \\n)", "is_checklist": false, "pill": "string"}},
    {{"kind": "special", "background": "light|dark", "num_label": "string", "icon": "emoji", "title": "string", "inner_html": "string", "pill": "string"}},
    {{"kind": "cta", "label": "string", "title": "string"}}
  ],
  "caption": "string (tam caption, hashtag'ler dahil)"
}}

Sadece geçerli JSON döndür. Markdown kod bloğu (```) KULLANMA."""


def call_claude(system_prompt: str) -> str:
    client = anthropic.Anthropic()  # WIF ortam değişkenlerinden otomatik kimlik doğrulama
    message = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        system=system_prompt,
        messages=[{"role": "user", "content": "Bugünün carousel içeriğini üret."}],
    )
    return "".join(block.text for block in message.content if block.type == "text")


def parse_json_response(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def validate(data: dict) -> None:
    assert data.get("topic"), "topic eksik"
    slides = data.get("slides")
    assert isinstance(slides, list) and len(slides) == SLIDE_COUNT, (
        f"{SLIDE_COUNT} slayt bekleniyordu, {len(slides) if slides else 0} geldi"
    )
    assert slides[0]["kind"] == "hook", "ilk slayt hook olmalı"
    assert slides[-1]["kind"] == "cta", "son slayt cta olmalı"
    assert data.get("caption"), "caption eksik"
    special_count = sum(1 for s in slides if s.get("kind") == "special")
    assert special_count == 1, f"tam olarak 1 special slayt bekleniyordu, {special_count} geldi"


def main() -> None:
    system_prompt = build_system_prompt()

    last_error = None
    for attempt in range(2):
        try:
            raw = call_claude(
                system_prompt
                if attempt == 0
                else system_prompt + f"\n\nÖNCEKİ CEVABIN GEÇERSİZ JSON'DI ({last_error}). SADECE geçerli JSON döndür."
            )
            data = parse_json_response(raw)
            validate(data)
            break
        except (json.JSONDecodeError, AssertionError, KeyError) as e:
            last_error = str(e)
            if attempt == 1:
                print(f"HATA: içerik üretimi 2 denemede de geçerli JSON üretmedi: {e}", file=sys.stderr)
                sys.exit(1)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ İçerik üretildi: {data['topic']}")
    print(f"  -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
