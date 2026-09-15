#!/usr/bin/env python3
"""
Uğur Akkaya Digital Pro — Yayın Öncesi Görsel URL Doğrulama
===============================================================
output/{slug}/slides.json'dan üretilen JPEG dosya adlarını okur, jsDelivr
CDN üzerinden (raw.githubusercontent.com yerine — daha üretim-dostu,
doğru Content-Type başlıklarıyla servis eder) herkese açık URL'leri
oluşturur ve Instagram'a göndermeden önce GERÇEKTEN erişilebilir
olduklarını doğrular (push sonrası CDN'in dosyayı çekmesi birkaç
saniye/dakika sürebilir, bu yüzden yeniden deneme mantığı var).

Doğrulanan URL listesini state/hosted_urls.json'a yazar.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_META = REPO_ROOT / "state" / "build_meta.json"
HOSTED_URLS_OUT = REPO_ROOT / "state" / "hosted_urls.json"

# GitHub Actions bunu otomatik "owner/repo" olarak sağlar; yoksa sabit değere düş.
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "ugurakkayapro01-del/instagram-otomasyon")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")

MAX_ATTEMPTS = 18
RETRY_DELAY_SEC = 10  # 18 x 10s ≈ 3 dakika toplam bekleme payı


def jsdelivr_url(slug: str, filename: str) -> str:
    return f"https://cdn.jsdelivr.net/gh/{GITHUB_REPOSITORY}@{BRANCH}/output/{slug}/{filename}"


def is_reachable(url: str) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get("Content-Type", "")
            return resp.status == 200 and content_type.startswith("image/")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return False


def wait_until_reachable(url: str) -> bool:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        if is_reachable(url):
            return True
        print(f"  ... henüz erişilebilir değil ({attempt}/{MAX_ATTEMPTS}), {RETRY_DELAY_SEC}s bekleniyor: {url}")
        time.sleep(RETRY_DELAY_SEC)
    return False


def main() -> None:
    meta = json.loads(BUILD_META.read_text(encoding="utf-8"))
    slug = meta["slug"]
    manifest_path = REPO_ROOT / "output" / slug / "slides.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    urls = []
    for filename in manifest["files"]:
        url = jsdelivr_url(slug, filename)
        print(f"Doğrulanıyor: {url}")
        if not wait_until_reachable(url):
            print(f"HATA: {url} {MAX_ATTEMPTS * RETRY_DELAY_SEC} saniye içinde erişilebilir olmadı.", file=sys.stderr)
            sys.exit(1)
        print("  ✓ erişilebilir")
        urls.append(url)

    HOSTED_URLS_OUT.write_text(
        json.dumps({"slug": slug, "urls": urls}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"✓ {len(urls)} görsel doğrulandı -> {HOSTED_URLS_OUT}")


if __name__ == "__main__":
    main()
