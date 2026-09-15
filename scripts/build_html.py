#!/usr/bin/env python3
"""
Uğur Akkaya Digital Pro — İçerikten HTML Üretimi
===================================================
state/current_carousel.json'daki içeriği, templates/carousel_template.html'in
AYNI CSS'iyle (hiç değiştirilmeden) deterministik Python şablonlamasıyla
gerçek bir carousel HTML dosyasına dönüştürür.

BİLEREK DETERMİNİSTİK: progress bar yüzdesi ve sayfa numarası formülle
hesaplanır, hiçbir zaman LLM çıktısına güvenilmez (bkz. MASTER_PROJECT_HANDOFF.md
Bölüm 14 madde 6 — bu konuda daha önce bir hata yapılıp fark edilmiş).

Marka/tasarım dosyalarına (templates/carousel_template.html, brand/) dokunmaz,
sadece CSS bloğunu ve profil fotoğrafını olduğu gibi okuyup kullanır.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

import state as st

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_JSON = REPO_ROOT / "state" / "current_carousel.json"
TEMPLATE_HTML = REPO_ROOT / "templates" / "carousel_template.html"
PROFILE_B64_FILE = REPO_ROOT / "brand" / "assets" / "profile_b64.txt"

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
# inner_html içinde bunların dışında hiçbir tehlikeli/beklenmeyen etiket olmamalı
FORBIDDEN_PATTERN = re.compile(
    r"<script|<style|<a\s|<img|on\w+\s*=", re.IGNORECASE
)
CLASS_ATTR_PATTERN = re.compile(r'class="([^"]*)"')


def extract_style_block() -> str:
    """carousel_template.html'deki <style>...</style> bloğunu aynen çıkarır."""
    text = TEMPLATE_HTML.read_text(encoding="utf-8")
    match = re.search(r"<style>.*?</style>", text, re.DOTALL)
    assert match, "carousel_template.html içinde <style> bloğu bulunamadı"
    return match.group(0)


def profile_data_uri() -> str:
    b64 = PROFILE_B64_FILE.read_text(encoding="utf-8").strip()
    return f"data:image/jpeg;base64,{b64}"


def render_title(raw: str) -> str:
    """'satır1\\nsatır2\\n**vurgu**' -> '<br>' ve '<em>' ile HTML."""
    lines = [html.escape(line) for line in raw.split("\n")]
    out = "<br>".join(lines)
    out = re.sub(r"\*\*(.+?)\*\*", r"<em>\1</em>", out)
    return out


def is_inner_html_safe(inner_html: str) -> bool:
    if FORBIDDEN_PATTERN.search(inner_html):
        return False
    for classes in CLASS_ATTR_PATTERN.findall(inner_html):
        for cls in classes.split():
            if cls not in ALLOWED_INNER_CLASSES:
                return False
    return True


def progress_markup(n: int, total: int, dark: bool) -> str:
    pct = round(n / total * 100, 1)
    if dark:
        track_bg, fill_bg, num_color = "rgba(255,255,255,.12)", "#fff", "rgba(255,255,255,.4)"
    else:
        track_bg, fill_bg, num_color = "rgba(0,0,0,.08)", "#0077B6", "rgba(0,0,0,.3)"
    return (
        f'<div class="prog"><div class="prog-track" style="background:{track_bg}">'
        f'<div class="prog-fill" style="width:{pct}%;background:{fill_bg}"></div></div>'
        f'<span class="prog-num" style="color:{num_color}">{n}/{total}</span></div>'
    )


def arrow_markup(dark: bool, is_last: bool) -> str:
    if is_last:
        return ""
    if dark:
        stroke, grad = "rgba(255,255,255,.35)", "rgba(255,255,255,.08)"
    else:
        stroke, grad = "rgba(0,0,0,.25)", "rgba(0,0,0,.06)"
    return (
        f'<div class="arr" style="background:linear-gradient(to right,transparent,{grad})">'
        f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none">'
        f'<path d="M9 6l6 6-6 6" stroke="{stroke}" stroke-width="2.5" '
        f'stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
    )


def render_hook(slide: dict, n: int, total: int, avatar: str) -> str:
    return f"""<div class="slide s1">
  <div class="g1"></div><div class="g2"></div>
  <div>
    <div class="tag">{html.escape(slide['tag'])}</div>
    <div class="line"></div>
    <div class="ttl">{render_title(slide['title'])}</div>
  </div>
  <div class="sub">{html.escape(slide['subtitle'])}</div>
  <div class="brand">
    <div class="identity">
      <div class="av"><img src="{avatar}"/></div>
      <div><div class="nm">Uğur Akkaya</div><div class="hd">@ugurakkaya_djitalpro</div></div>
    </div>
    <div class="badge">DIGITAL PRO</div>
  </div>
  {arrow_markup(dark=True, is_last=False)}
  {progress_markup(n, total, dark=True)}
</div>"""


def render_body(slide: dict) -> str:
    if slide.get("is_checklist"):
        items = [line.strip("- ").strip() for line in slide["body"].split("\n") if line.strip()]
        rows = "\n".join(
            f'<div class="chk-item"><div class="chk-mark">✓</div>'
            f'<div class="chk-txt">{html.escape(item)}</div></div>'
            for item in items
        )
        return f'<div class="body">{rows}</div>'
    return f'<div class="body">{html.escape(slide["body"])}</div>'


def render_info(slide: dict, n: int, total: int) -> str:
    dark = slide["kind"] == "dark"
    cls = "sd" if dark else "sl"
    pill_bg_note = ""  # pill rengi CSS'te zaten .sl/.sd altında tanımlı
    return f"""<div class="slide {cls}">
  <div class="topbar"></div>
  <div>
    <div class="num">{html.escape(slide['num_label'])}</div>
    <div class="icon">{slide['icon']}</div>
    <div class="ttl">{html.escape(slide['title'])}</div>
    {render_body(slide)}
  </div>
  <div class="foot">
    <div class="pill">→ {html.escape(slide['pill'])}</div>
    <div><div class="logo">UA DIGITAL PRO</div><div class="pgn">{n} / {total}</div></div>
  </div>
  {arrow_markup(dark=dark, is_last=False)}
  {progress_markup(n, total, dark=dark)}
</div>"""


def render_special(slide: dict, n: int, total: int) -> str:
    dark = slide["background"] == "dark"
    cls = "sd" if dark else "sl"
    inner = slide["inner_html"]
    if not is_inner_html_safe(inner):
        # Güvenli olmayan/izin verilmeyen markup -> düz metne düşür, pipeline'ı durdurma.
        inner = f'<div class="body">{html.escape(re.sub("<[^>]+>", "", inner))}</div>'
    return f"""<div class="slide {cls}">
  <div class="topbar"></div>
  <div>
    <div class="num">{html.escape(slide['num_label'])}</div>
    <div class="icon">{slide['icon']}</div>
    <div class="ttl">{html.escape(slide['title'])}</div>
    {inner}
  </div>
  <div class="foot">
    <div class="pill">→ {html.escape(slide['pill'])}</div>
    <div><div class="logo">UA DIGITAL PRO</div><div class="pgn">{n} / {total}</div></div>
  </div>
  {arrow_markup(dark=dark, is_last=False)}
  {progress_markup(n, total, dark=dark)}
</div>"""


def render_cta(slide: dict, n: int, total: int, avatar: str) -> str:
    buttons = slide.get("buttons") or [
        {"icon": "🔖", "text": "Kaydet & Uygula"},
        {"icon": "💬", "text": "Yorumda söyle!"},
        {"icon": "👆", "text": "Takip et — her hafta yeni taktik"},
    ]
    btn_html = []
    for i, b in enumerate(buttons):
        variant = "p" if i == 0 else "s"
        btn_html.append(f'<div class="btn {variant}">{b["icon"]} &nbsp;{html.escape(b["text"])}</div>')
    return f"""<div class="slide scta">
  <div class="cg"></div><div class="cg2"></div>
  <div>
    <div class="lbl">{html.escape(slide['label'])}</div>
    <div class="ttl">{html.escape(slide['title'])}</div>
  </div>
  <div class="btns">
    {''.join(btn_html)}
  </div>
  <div class="cbrand">
    <div class="av"><img src="{avatar}"/></div>
    <div><div class="cnm">Uğur Akkaya Digital Pro</div><div class="chd">@ugurakkaya_djitalpro</div></div>
  </div>
  {progress_markup(n, total, dark=True)}
</div>"""


def build_slide_html(slide: dict, n: int, total: int, avatar: str) -> str:
    kind = slide["kind"]
    if kind == "hook":
        return render_hook(slide, n, total, avatar)
    if kind in ("light", "dark"):
        return render_info(slide, n, total)
    if kind == "special":
        return render_special(slide, n, total)
    if kind == "cta":
        return render_cta(slide, n, total, avatar)
    raise ValueError(f"Bilinmeyen slayt tipi: {kind}")


FONTS_LINK = (
    '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900'
    '&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">'
)
# Vieportu (ve dolayısıyla ekran görüntüsünü) 525px'e sabitler — bir slaytın içeriği
# taşarsa (ör. LLM'in ürettiği metin beklenenden uzun olursa) alttan kırpılır; bu,
# tek bir slaytın alt kısmının eksik görünmesi riskini, TÜM sonraki slaytların
# birbirine karışması riskiyle değiştirir (çok daha güvenli bir hata modu).
VIEWPORT_LOCK_STYLE = "<style>html,body{overflow:hidden;height:525px;}</style>"


def wrap_single_slide(style_block: str, slide_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
{FONTS_LINK}
{style_block}
{VIEWPORT_LOCK_STYLE}
</head>
<body>
<div class="wrap">
{slide_html}
</div>
</body>
</html>"""


def main() -> None:
    data = json.loads(CONTENT_JSON.read_text(encoding="utf-8"))
    slides = data["slides"]
    total = len(slides)
    avatar = profile_data_uri()
    style_block = extract_style_block()

    slide_htmls = [
        build_slide_html(slide, i + 1, total, avatar) for i, slide in enumerate(slides)
    ]

    slug = st.slugify(data["topic"])
    out_dir = REPO_ROOT / "output" / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    # Referans/insan incelemesi için: tüm slaytları tek dosyada gösteren birleşik HTML.
    combined_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
{FONTS_LINK}
{style_block}
</head>
<body>
<div class="wrap">
{''.join(slide_htmls)}
</div>
</body>
</html>"""
    (out_dir / "source.html").write_text(combined_html, encoding="utf-8")

    # Export için: HER SLAYT AYRI, izole bir HTML dosyası olarak da yazılır.
    # Nedeni: tek dosyada üst üste dizip piksel offsetiyle kırpmak (orijinal
    # export_slides.py'nin yöntemi), slaytlardan biri 525px'i taşarsa (LLM içeriği
    # elle ayarlanmadığı için bu artık olası) sonraki TÜM slaytların kaymasına yol
    # açıyor (bu, gerçek içerikle test edilirken tespit edildi). İzole render bu
    # riski ortadan kaldırır.
    slide_paths = []
    for i, slide_html in enumerate(slide_htmls):
        slide_doc = wrap_single_slide(style_block, slide_html)
        slide_path = out_dir / f"slide_{i + 1:02d}.html"
        slide_path.write_text(slide_doc, encoding="utf-8")
        slide_paths.append(str(slide_path))

    meta_path = REPO_ROOT / "state" / "build_meta.json"
    meta_path.write_text(
        json.dumps(
            {"slug": slug, "total_slides": total, "slide_html_paths": slide_paths},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"✓ HTML üretildi: {out_dir} ({total} slayt, her biri izole render için ayrı dosya)")


if __name__ == "__main__":
    main()
