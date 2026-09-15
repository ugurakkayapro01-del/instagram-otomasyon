#!/usr/bin/env python3
"""
Uğur Akkaya Digital Pro — Otomasyon için JPEG Export Scripti
================================================================
build_html.py'nin ürettiği HER SLAYT İÇİN AYRI, izole HTML dosyasını
(state/build_meta.json -> slide_html_paths) tek tek yükleyip 420x525
viewport'ta ekran görüntüsü alır (device_scale_factor=2.571 ile çıktı
otomatik 1080x1350px olur).

Neden tek dosyada üst üste dizip piksel offsetiyle kırpmıyoruz (orijinal
templates/export_slides.py'nin yöntemi): gerçek içerikle test edildiğinde,
bir slaytın metni 525px'i taşarsa (LLM içeriği elle uzunluk ayarı
yapılmadığı için bu artık olası bir durum) flex kutusu beklenenden uzun
render oluyor ve piksel offsetine dayalı kırpma TÜM sonraki slaytları
birbirine karıştırıyor. İzole render (her slayt kendi sayfasında, sadece
görünen viewport'un ekran görüntüsü alınıyor) bu riski ortadan kaldırır:
en kötü ihtimalle bir slaydın alt kısmı kırpılır, ama slaytlar asla
birbirine karışmaz.

templates/export_slides.py'ye HİÇ DOKUNULMADI — o dosya manuel/referans
kullanım için orijinal (stack+clip) yöntemle PNG üretmeye devam ediyor.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_META = REPO_ROOT / "state" / "build_meta.json"

VIEW_W = 420
VIEW_H = 525
TARGET_W = 1080
SCALE = TARGET_W / VIEW_W  # ≈ 2.571
JPEG_QUALITY = 92


async def export_slides(slide_html_paths: list[str], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": VIEW_W, "height": VIEW_H},
            device_scale_factor=SCALE,
        )

        for i, html_path in enumerate(slide_html_paths):
            html_content = Path(html_path).read_text(encoding="utf-8")
            await page.set_content(html_content, wait_until="networkidle")
            await page.wait_for_timeout(2500)  # fontlar/gömülü görsel için bekleme

            out_path = out_dir / f"slide_{i + 1:02d}.jpg"
            # clip YOK — sadece görünen 420x525 viewport'un ekran görüntüsü alınır.
            await page.screenshot(path=str(out_path), type="jpeg", quality=JPEG_QUALITY)
            written.append(out_path)
            print(f"✓ Slayt {i + 1}/{len(slide_html_paths)} -> {out_path}")

        await browser.close()

    return written


def main() -> None:
    meta = json.loads(BUILD_META.read_text(encoding="utf-8"))
    out_dir = REPO_ROOT / "output" / meta["slug"]

    written = asyncio.run(export_slides(meta["slide_html_paths"], out_dir))

    manifest_path = out_dir / "slides.json"
    manifest_path.write_text(
        json.dumps({"slug": meta["slug"], "files": [p.name for p in written]}, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Tamamlandı. {len(written)} JPEG üretildi -> {out_dir}")


if __name__ == "__main__":
    main()
