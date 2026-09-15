#!/usr/bin/env python3
"""
Uğur Akkaya Digital Pro — Otomasyon Yayın Adımı
====================================================
scripts/publish_to_instagram.py dosyasını (HİÇ DEĞİŞTİRİLMEDEN, doğrudan
Python modülü olarak import ederek) kullanıp state/current_carousel.json +
state/hosted_urls.json'daki hazır içerik ve doğrulanmış URL'lerle gerçek
Instagram yayınını yapar. Sonucu (başarı/hata, post ID) state/last_run.json'a
yazar.

IG_ACCESS_TOKEN ortam değişkeni workflow tarafından GitHub Secrets'tan
sağlanır — bu script token'ı asla loglamaz veya dosyaya yazmaz
(publish_to_instagram.py'nin kendi güvenlik tasarımı korunuyor).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import publish_to_instagram as pub  # noqa: E402  (sys.path ayarından sonra import)
import state as st  # noqa: E402

CONTENT_JSON = REPO_ROOT / "state" / "current_carousel.json"
HOSTED_URLS_JSON = REPO_ROOT / "state" / "hosted_urls.json"


def main() -> None:
    data = json.loads(CONTENT_JSON.read_text(encoding="utf-8"))
    hosted = json.loads(HOSTED_URLS_JSON.read_text(encoding="utf-8"))
    topic = data["topic"]
    special_kind = data.get("special_kind")
    caption = data["caption"]
    image_urls = hosted["urls"]

    token = pub.get_access_token()

    try:
        print(f"'{topic}' konulu carousel yayınlanıyor ({len(image_urls)} slayt)...")
        child_ids = []
        for i, url in enumerate(image_urls, start=1):
            cid = pub.create_image_container(url, token)
            pub.wait_until_ready(cid, token)
            print(f"  ✓ Slayt {i}/{len(image_urls)} hazır")
            child_ids.append(cid)

        carousel_id = pub.create_carousel_container(child_ids, caption, token)
        pub.wait_until_ready(carousel_id, token)
        post_id = pub.publish_container(carousel_id, token)
        print(f"✓ YAYINLANDI. Instagram medya ID: {post_id}")

        st.append_run({
            "topic": topic,
            "special_kind": special_kind,
            "status": "success",
            "instagram_media_id": post_id,
            "slide_count": len(image_urls),
        })

    except pub.InstagramAPIError as e:
        print(f"HATA: yayın başarısız: {e}", file=sys.stderr)
        st.append_run({
            "topic": topic,
            "special_kind": special_kind,
            "status": "failed",
            "error": str(e),
        })
        sys.exit(1)


if __name__ == "__main__":
    main()
