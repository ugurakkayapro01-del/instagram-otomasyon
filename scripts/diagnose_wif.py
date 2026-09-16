#!/usr/bin/env python3
"""
GEÇİCİ TEŞHİS SCRIPTİ — WIF 401 hatasının gerçek kaynağını bulmak için.

Bu script, anthropic SDK'nın `anthropic/lib/credentials/_workload.py` içindeki
`WorkloadIdentityCredentials.__call__` metodunun GÖNDERDİĞİ İSTEĞİN BİREBİR
AYNISINI (aynı URL, aynı 2 beta header, aynı body alanları) doğrudan urllib ile
kendimiz gönderir ve SDK'nın redakte ettiği/kısalttığı hata gövdesini DEĞİL,
Anthropic'in döndürdüğü HAM (ama güvenli şekilde maskelenmiş) yanıtı gösterir.

GÜVENLİK: JWT'nin (assertion) kendisi, Authorization başlığı veya SDK
tarafından üretilen access_token HİÇBİR ZAMAN yazdırılmaz. Yanıt gövdesinde
JWT'yi andıran (bizim gönderdiğimiz assertion ile eşleşen veya 100+ karakter
uzunluğunda) herhangi bir string maskelenir.

Kaynak: anthropic SDK sürüm 1.6.0, anthropic/lib/credentials/_workload.py ve
_constants.py dosyalarının kendisi okunarak doğrulanmış istek biçimi kullanılıyor.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
import urllib.error

ENV_FEDERATION_RULE_ID = "ANTHROPIC_FEDERATION_RULE_ID"
ENV_ORGANIZATION_ID = "ANTHROPIC_ORGANIZATION_ID"
ENV_SERVICE_ACCOUNT_ID = "ANTHROPIC_SERVICE_ACCOUNT_ID"
ENV_WORKSPACE_ID = "ANTHROPIC_WORKSPACE_ID"
ENV_IDENTITY_TOKEN_FILE = "ANTHROPIC_IDENTITY_TOKEN_FILE"
ENV_API_KEY = "ANTHROPIC_API_KEY"

TOKEN_ENDPOINT = "https://api.anthropic.com/v1/oauth/token"
# _constants.py: bu iki beta header BİRLİKTE gönderilmezse istek yanlış
# backend'e (Python oauth_server) yönlenir ve "unsupported grant_type" ile
# farklı şekilde başarısız olur. SDK bunu otomatik ekliyor, biz de aynısını
# manuel gönderiyoruz ki SDK'yı bypass eden ham bir test olsun.
BETA_HEADER = "oauth-2025-04-20,oidc-federation-2026-04-01"


def mask(value: str | None, keep: int = 6) -> str:
    if not value:
        return "(BOŞ/YOK)"
    if len(value) <= keep * 2:
        return value  # zaten kısa, tamamı non-secret ID formatı
    return f"{value[:keep]}...{value[-keep:]} (len={len(value)})"


def redact_jwt_like(obj, assertion_value: str):
    """JSON yanıtındaki string alanları, assertion'ı yansıtan veya aşırı uzun
    (JWT'yi andıran) her şeyi maskeleyerek güvenli hale getirir."""
    if isinstance(obj, dict):
        return {k: redact_jwt_like(v, assertion_value) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact_jwt_like(v, assertion_value) for v in obj]
    if isinstance(obj, str):
        if assertion_value and assertion_value in obj:
            return "<< ASSERTION JWT YANSIMASI — MASKELENDİ >>"
        if len(obj) > 120:
            return f"<< uzun string, maskelendi (len={len(obj)}) >>"
        return obj
    return obj


def main() -> int:
    print("=" * 70)
    print("WIF 401 TEŞHİS RAPORU")
    print("=" * 70)

    # --- 1) SDK sürümü ve hangi credential yönteminin seçildiği ---
    try:
        import anthropic
        print(f"\n[1] Kurulu anthropic SDK sürümü: {anthropic.__version__}")
    except Exception as e:
        print(f"\n[1] anthropic import edilemedi: {e}")
        return 1

    has_api_key = bool(os.environ.get(ENV_API_KEY))
    print(f"    ANTHROPIC_API_KEY set mi? {has_api_key} (True ise WIF DEVRE DIŞI kalır — beklenen: False)")

    federation_rule_id = os.environ.get(ENV_FEDERATION_RULE_ID)
    organization_id = os.environ.get(ENV_ORGANIZATION_ID)
    service_account_id = os.environ.get(ENV_SERVICE_ACCOUNT_ID)
    workspace_id = os.environ.get(ENV_WORKSPACE_ID) or None
    identity_token_file = os.environ.get(ENV_IDENTITY_TOKEN_FILE)

    would_use_federation = (
        not has_api_key
        and bool(federation_rule_id)
        and bool(organization_id)
        and bool(identity_token_file)
    )
    print(f"    SDK'nın credential zinciri (Step 2a->4) şunu seçer: "
          f"{'WorkloadIdentityCredentials (federation)' if would_use_federation else 'BAŞKA BİR YÖNTEM veya HİÇBİRİ — SORUN BURADA OLABİLİR'}")

    # --- 2) 4 kimlik ID'sinin biçim kontrolü (değerler secret değil) ---
    print(f"\n[2] Kimlik ID'leri (secret değil — biçim + tam değer):")
    print(f"    ANTHROPIC_FEDERATION_RULE_ID  = {federation_rule_id!r} "
          f"{'OK (fdrl_ ile başlıyor)' if (federation_rule_id or '').startswith('fdrl_') else '!! BEKLENEN BİÇİM: fdrl_...'}")
    print(f"    ANTHROPIC_ORGANIZATION_ID     = {organization_id!r} "
          f"{'OK (UUID benzeri, 36 karakter)' if organization_id and len(organization_id) == 36 else '!! BEKLENEN BİÇİM: UUID (36 karakter, tire ile)'}")
    print(f"    ANTHROPIC_SERVICE_ACCOUNT_ID  = {service_account_id!r} "
          f"{'OK (svac_ ile başlıyor)' if (service_account_id or '').startswith('svac_') else '!! BEKLENEN BİÇİM: svac_...'}")
    workspace_ok = (
        workspace_id is None
        or (workspace_id or "").startswith("wrkspc_")
        or workspace_id == "default"
    )
    workspace_label = "OK (wrkspc_ ile başlıyor veya default)" if workspace_ok else "BEKLENEN BİÇİM: wrkspc_... veya default"
    print(f"    ANTHROPIC_WORKSPACE_ID        = {workspace_id!r} {workspace_label}")

    if not identity_token_file:
        print(f"\n[!] ANTHROPIC_IDENTITY_TOKEN_FILE ayarlı değil — JWT bulunamıyor, çıkılıyor.")
        return 1

    try:
        with open(identity_token_file, "r", encoding="utf-8") as f:
            jwt = f.read().strip()
    except OSError as e:
        print(f"\n[!] Identity token dosyası okunamadı ({identity_token_file}): {e}")
        return 1

    parts = jwt.split(".")
    print(f"\n[3] Identity token dosyası okundu: {len(jwt)} karakter, {len(parts)} segment "
          f"{'(geçerli JWT yapısı: 3 segment)' if len(parts) == 3 else '!! JWT 3 segmentli OLMALI'}")
    print("    (JWT'nin kendisi güvenlik nedeniyle yazdırılmıyor)")

    # --- 4) SDK'nın gönderdiği isteğin birebir aynısını, SDK'yı bypass ederek gönder ---
    body = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt,
        "federation_rule_id": federation_rule_id,
        "organization_id": organization_id,
    }
    if service_account_id:
        body["service_account_id"] = service_account_id
    if workspace_id:
        body["workspace_id"] = workspace_id

    print(f"\n[4] Anthropic token endpoint'ine HAM istek gönderiliyor (SDK bypass edilerek):")
    print(f"    POST {TOKEN_ENDPOINT}")
    print(f"    Body alanları (assertion hariç): "
          f"{ {k: (mask(v) if k != 'assertion' else '<< JWT, gösterilmiyor >>') for k, v in body.items()} }")
    print(f"    Header: anthropic-beta: {BETA_HEADER}")

    req = urllib.request.Request(
        TOKEN_ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "anthropic-beta": BETA_HEADER,
            "Content-Type": "application/json",
            "User-Agent": f"instagram-otomasyon-wif-diagnose/1.0 (anthropic-python/{anthropic.__version__})",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            resp_body = resp.read().decode("utf-8", errors="replace")
            resp_headers = dict(resp.headers)
    except urllib.error.HTTPError as e:
        status = e.code
        resp_body = e.read().decode("utf-8", errors="replace")
        resp_headers = dict(e.headers)
    except Exception as e:
        print(f"\n[!] İstek gönderilemedi (ağ/bağlantı hatası): {type(e).__name__}: {e}")
        return 1

    request_id = resp_headers.get("Request-Id") or resp_headers.get("request-id") or "(yok)"

    print(f"\n[5] YANIT:")
    print(f"    HTTP durum kodu: {status}")
    print(f"    Request-Id: {request_id}")

    try:
        parsed = json.loads(resp_body)
        safe_parsed = redact_jwt_like(parsed, jwt)
        print(f"    Yanıt gövdesi (JWT/token maskelenerek, TAM içerik — SDK'nın 256 karakter/3-alan kısıtlaması YOK):")
        print(json.dumps(safe_parsed, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        safe_text = resp_body if len(resp_body) <= 500 else resp_body[:500] + "...(kırpıldı)"
        print(f"    Yanıt JSON değil, ham metin: {safe_text}")

    print("\n" + "=" * 70)
    if status == 200:
        print("SONUÇ: Token exchange BAŞARILI. (generate_carousel.py'nin neden farklı davrandığını ayrıca kontrol et.)")
    else:
        print(f"SONUÇ: Token exchange BAŞARISIZ (HTTP {status}). Yukarıdaki 'error' alanındaki")
        print("gerçek hata koduna göre (örn. federation_rule_id_not_found, match_audience,")
        print("workspace_id_required, vb.) Anthropic Console'da tam olarak neyin uyuşmadığı")
        print("belirlenebilir.")
    print("=" * 70)

    return 0 if status == 200 else 1


if __name__ == "__main__":
    sys.exit(main())
