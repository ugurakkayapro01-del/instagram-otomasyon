"""
UĞUR AKKAYA DIGITAL PRO — CAROUSEL EXPORT SCRIPTİ
====================================================
Kullanım:
    python3 export_slides.py <html_dosya_yolu> <cikti_klasoru> <toplam_slayt_sayisi>

Örnek:
    python3 export_slides.py /home/claude/carousel_source.html /mnt/user-data/outputs/adfatigue 7

Bu script, carousel_template.html mantığıyla üretilmiş (tüm slaytları tek
sayfada alt alta içeren) bir HTML dosyasını alır ve her slaytı ayrı
1080x1350px PNG olarak dışa aktarır.

ÖNEMLİ: HTML'in tasarım genişliği HER ZAMAN 420px, yüksekliği HER ZAMAN
525px/slayt olmalı. Bu değerleri değiştirme — sadece SCALE otomatik
1080/420 oranını hesaplar, tasarım hiç bozulmaz.
"""

import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright

# --- SABİT DEĞERLER (değiştirme) ---
VIEW_W = 420
VIEW_H = 525
TARGET_W = 1080
SCALE = TARGET_W / VIEW_W  # ≈ 2.571 -> final PNG 1080x1350px


async def export_slides(html_path: str, output_dir: str, total_slides: int):
    input_html = Path(html_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": VIEW_W, "height": VIEW_H * total_slides},
            device_scale_factor=SCALE,
        )

        html_content = input_html.read_text(encoding="utf-8")
        await page.set_content(html_content, wait_until="networkidle")
        # Google Fonts ve base64 gömülü görsellerin tam yüklenmesi için bekleme
        await page.wait_for_timeout(4000)

        for i in range(total_slides):
            y = i * VIEW_H
            out_path = out_dir / f"slide_{i + 1:02d}.png"
            await page.screenshot(
                path=str(out_path),
                clip={"x": 0, "y": y, "width": VIEW_W, "height": VIEW_H},
            )
            print(f"✓ Slide {i + 1}/{total_slides} -> {out_path}")

        await browser.close()

    print("Tamamlandı! Tüm slaytlar 1080x1350px PNG olarak dışa aktarıldı.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    html_file = sys.argv[1]
    output_folder = sys.argv[2]
    slide_count = int(sys.argv[3])

    asyncio.run(export_slides(html_file, output_folder, slide_count))
