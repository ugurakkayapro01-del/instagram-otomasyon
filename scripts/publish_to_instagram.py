#!/usr/bin/env python3
"""
Uğur Akkaya Digital Pro — Instagram Otomatik Carousel Yayınlama Scripti
=========================================================================
Meta Graph API v26.0 kullanarak, halihazırda herkese açık bir HTTPS
adresinde barındırılan JPEG görselleri Instagram carousel gönderisi
olarak yayınlar.

BU SCRIPT NE YAPMAZ (bilerek):
  - Görselleri barındırmaz / yüklemez. --images parametresine verilen
    her adres, Meta'nın sunucularının erişebileceği herkese açık bir
    HTTPS URL olmalı (hosting adımı ayrı bir aşamada ele alınacak).
  - Zamanlama veya otomasyon yapmaz — elle çalıştırılan bir araçtır.
  - Access token'ı hiçbir yerde saklamaz, dosyaya yazmaz veya loglamaz.

GÜVENLİK — ACCESS TOKEN:
  Token kod içine YAZILMAZ, sabit bir dosyada da tutulmaz. Ortam
  değişkeninden okunur:

      export IG_ACCESS_TOKEN="senin_tokenin"
      python3 publish_to_instagram.py --check-connection

  Bu satırı shell geçmişine kalıcı yazmamak için başına bir boşluk
  koyarak çalıştırman (çoğu shell'de HISTCONTROL=ignorespace ile
  geçmişe hiç yazılmaz) ya da bir .env dosyasından `source` ile
  yüklemen (o .env dosyasını asla git'e/senkronize klasöre eklemeden)
  daha güvenlidir.

SABİT HESAP TANIMLAYICILARI (bunlar gizli değil, Meta panelinde görünür):
  Facebook Page ID              : 148509715019398
  Instagram Business Account ID : 17841467623788252

KULLANIM:
  1) Bağlantıyı ve izinleri doğrula — HİÇBİR ŞEY PAYLAŞMAZ:
       python3 publish_to_instagram.py --check-connection

  2) Kuru deneme — container'ları oluşturur, YAYINLAMAZ:
       python3 publish_to_instagram.py --images URL1 URL2 URL3 --caption "..."

  3) Gerçek yayın — DİKKAT: hesapta gerçekten, geri alınamaz şekilde
     paylaşım yapar. Sadece açıkça --publish verilirse çalışır:
       python3 publish_to_instagram.py --images URL1 URL2 URL3 --caption "..." --publish

REFERANS: https://developers.facebook.com/docs/instagram-platform/content-publishing/
"""

import os
import sys
import time
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error

GRAPH_API_VERSION = "v26.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

# Sabit hesap tanımlayıcıları — gizli değil, Meta App/Business panelinde görünür.
FACEBOOK_PAGE_ID = "148509715019398"
INSTAGRAM_BUSINESS_ACCOUNT_ID = "17841467623788252"

# Token SADECE bu ortam değişkeninden okunur — koda yazılmaz.
TOKEN_ENV_VAR = "IG_ACCESS_TOKEN"

MIN_CAROUSEL_ITEMS = 2
MAX_CAROUSEL_ITEMS = 10
CONTAINER_POLL_INTERVAL_SEC = 2
CONTAINER_POLL_TIMEOUT_SEC = 60


class InstagramAPIError(Exception):
    """Graph API'den dönen hataları okunabilir haliyle taşır."""


def get_access_token() -> str:
    token = os.environ.get(TOKEN_ENV_VAR)
    if not token:
        raise SystemExit(
            f"HATA: {TOKEN_ENV_VAR} ortam değişkeni bulunamadı.\n"
            f"Güvenlik gereği token koda yazılmıyor. Önce şunu çalıştır:\n\n"
            f'  export {TOKEN_ENV_VAR}="senin_tokenin"\n\n'
            f"sonra bu scripti tekrar çalıştır."
        )
    return token


def _request(method: str, path: str, params: dict) -> dict:
    """Graph API'ye tek bir istek atar ve JSON döner.
    Hata durumunda Meta'nın döndürdüğü mesajı içeren bir istisna fırlatır."""
    url = f"{GRAPH_API_BASE}/{path}"
    encoded = urllib.parse.urlencode(params).encode("utf-8")

    if method == "GET":
        req = urllib.request.Request(f"{url}?{encoded.decode()}", method="GET")
    elif method == "POST":
        req = urllib.request.Request(url, data=encoded, method="POST")
    else:
        raise ValueError(f"Desteklenmeyen HTTP metodu: {method}")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            err = json.loads(body).get("error", {})
            message = err.get("message", body)
            code = err.get("code", e.code)
            err_subcode = err.get("error_subcode")
        except json.JSONDecodeError:
            message, code, err_subcode = body, e.code, None
        extra = f" (subcode: {err_subcode})" if err_subcode else ""
        raise InstagramAPIError(f"Graph API hatası [{code}]{extra}: {message}") from None
    except urllib.error.URLError as e:
        raise InstagramAPIError(f"Ağ hatası: {e.reason}") from None


def check_connection(token: str) -> None:
    """Sadece hesap bilgisini okur — hiçbir şey paylaşmaz.
    Token'ın geçerli olduğunu ve doğru izinlere sahip olduğunu doğrulamak için kullan."""
    print("Bağlantı kontrol ediliyor (hiçbir şey paylaşılmayacak)...")
    info = _request(
        "GET",
        INSTAGRAM_BUSINESS_ACCOUNT_ID,
        {
            "fields": "username,name,profile_picture_url,followers_count",
            "access_token": token,
        },
    )
    print("✓ Bağlantı başarılı. Hesap bilgisi:")
    print(json.dumps(info, indent=2, ensure_ascii=False))


def create_image_container(image_url: str, token: str) -> str:
    result = _request(
        "POST",
        f"{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media",
        {
            "image_url": image_url,
            "is_carousel_item": "true",
            "access_token": token,
        },
    )
    return result["id"]


def wait_until_ready(container_id: str, token: str, timeout: int = CONTAINER_POLL_TIMEOUT_SEC) -> None:
    """Container'ın Meta tarafında işlenmesini bekler (status_code == FINISHED)."""
    start = time.time()
    while time.time() - start < timeout:
        status = _request(
            "GET",
            container_id,
            {"fields": "status_code", "access_token": token},
        )
        code = status.get("status_code")
        if code == "FINISHED":
            return
        if code == "ERROR":
            raise InstagramAPIError(f"Container {container_id} işlenirken hata oluştu.")
        time.sleep(CONTAINER_POLL_INTERVAL_SEC)
    raise InstagramAPIError(f"Container {container_id} {timeout} saniyede hazır olmadı (timeout).")


def create_carousel_container(children_ids: list, caption: str, token: str) -> str:
    params = {
        "media_type": "CAROUSEL",
        "children": ",".join(children_ids),
        "access_token": token,
    }
    if caption:
        params["caption"] = caption
    result = _request("POST", f"{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media", params)
    return result["id"]


def publish_container(creation_id: str, token: str) -> str:
    result = _request(
        "POST",
        f"{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish",
        {"creation_id": creation_id, "access_token": token},
    )
    return result["id"]


def publish_carousel(image_urls: list, caption: str, token: str, really_publish: bool) -> None:
    if not (MIN_CAROUSEL_ITEMS <= len(image_urls) <= MAX_CAROUSEL_ITEMS):
        raise SystemExit(
            f"Instagram carousel {MIN_CAROUSEL_ITEMS}-{MAX_CAROUSEL_ITEMS} görsel gerektirir, "
            f"{len(image_urls)} verildi."
        )

    print(f"{len(image_urls)} görsel için medya container'ları oluşturuluyor...")
    child_ids = []
    for i, url in enumerate(image_urls, start=1):
        cid = create_image_container(url, token)
        wait_until_ready(cid, token)
        print(f"  ✓ Slayt {i}/{len(image_urls)} hazır (container: {cid})")
        child_ids.append(cid)

    print("Carousel container oluşturuluyor...")
    carousel_id = create_carousel_container(child_ids, caption, token)
    wait_until_ready(carousel_id, token)
    print(f"  ✓ Carousel container hazır: {carousel_id}")

    if not really_publish:
        print("\n--publish VERİLMEDİ: HİÇBİR ŞEY PAYLAŞILMADI (kuru deneme tamamlandı).")
        print(f"Gerçek yayın için aynı komutu --publish ile tekrar çalıştır.")
        return

    print("Yayınlanıyor...")
    post_id = publish_container(carousel_id, token)
    print(f"✓ YAYINLANDI. Instagram medya ID: {post_id}")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--check-connection", action="store_true",
        help="Sadece token/izinleri doğrula, hiçbir şey paylaşma.",
    )
    parser.add_argument(
        "--images", nargs="+",
        help="Herkese açık, HTTPS üzerinden erişilebilir JPEG görsel URL'leri (2-10 adet, sırayla).",
    )
    parser.add_argument("--caption", default="", help="Gönderi açıklaması (opsiyonel).")
    parser.add_argument(
        "--publish", action="store_true",
        help="Bu bayrak verilmezse script varsayılan olarak KURU DENEME yapar (yayınlamaz). "
             "Gerçekten paylaşmak için açıkça --publish vermen gerekir.",
    )
    args = parser.parse_args()

    token = get_access_token()

    if args.check_connection:
        check_connection(token)
        return

    if not args.images:
        parser.error("--images gerekli (veya sadece --check-connection kullan).")

    if not args.publish:
        print("NOT: --publish verilmedi — bu bir KURU DENEME, hiçbir şey paylaşılmayacak.\n")

    try:
        publish_carousel(args.images, args.caption, token, really_publish=args.publish)
    except InstagramAPIError as e:
        print(f"\nHATA: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
