# MASTER PROJECT HANDOFF
## Uğur Akkaya Digital Pro — Instagram Carousel İçerik Sistemi

Bu doküman, bu sohbette baştan kurulan Instagram carousel üretim sisteminin tam devir dosyasıdır. Yeni bir Claude Cowork oturumuna doğrudan yapıştırılıp kullanılabilir. Hiçbir varsayım eklenmemiştir — tamamı bu projede fiilen üretilen ve onaylanan içeriklerden derlenmiştir.

---

## 1. HESABIN İÇERİK KONUSU VE HEDEF KİTLESİ

- **Hesap adı:** Uğur Akkaya Digital Pro
- **Instagram handle:** @ugurakkaya_djitalpro
- **Kimlik:** Dijital Pazarlama Uzmanı & Meta Reklam Danışmanı
- **İçerik konusu:** Meta (Facebook & Instagram) reklamcılığı — performans pazarlama, dönüşüm optimizasyonu, reklam stratejisi
- **Hedef kitle:** E-ticaret sahipleri (birincil), küçük işletmeler ve girişimciler (ikincil)
- **İçeriğin amacı:** Kullanıcıya gerçek, uygulanabilir, teknik derinliği olan bilgi vermek — hem öğretici hem "kaydetmeye değer" olmalı. İkincil amaç: hesabı Meta reklam danışmanlığı hizmeti için müşteri kazanma aracına dönüştürmek.

---

## 2. İÇERİK ÜRETİM STRATEJİSİ

- Her paylaşım bir **7 (standart) veya 8-10 (özel durum) slaytlık carousel** formatında üretilir.
- İçerik döngüsü: Kullanıcı "sıradaki carousel" dediğinde, sistem önce **daha önce işlenmiş başlıkların listesini** gösterir, sonra 4-5 yeni ve tekrar etmeyen konu önerir.
- Her içerik **tek bir dar konuya** odaklanır (ör. "A/B test", "CAPI", "Ad Fatigue") — genel/yüzeysel konular ("Facebook Pixel nedir" gibi) reddedilir.
- Marka kimliği (renk, font, profil fotoğrafı, handle) her carousel'de sabit kalır; sadece konu ve slayt içeriği değişir.
- İki tür carousel üretilir:
  1. **Eğitim/bilgi carousel'i** (varsayılan, 7 slayt) — uzman taktik ve teknik bilgi verir.
  2. **Hizmet tanıtım carousel'i** (8 slayt, nadiren) — Meta Reklam Danışmanlığı hizmetinin süreç ve fiyatlandırmasını tanıtır.

---

## 3. KONU SEÇME KURALLARI

1. **ASLA daha önce kullanılmış bir başlığı tekrar önerme.** Her yeni öneri turunda, işlenmiş konular listesi kontrol edilir (bkz. Bölüm 13 ve `content/topics_used.md`).
2. Kullanıcıya her zaman **interaktif buton seçimi** ile sorulur:
   - Soru 1: "Konu ne olsun?" → 4-5 seçenek (henüz işlenmemiş, ileri seviye Meta reklamcılık konuları)
   - Soru 2: "Kaç slide?" → "7 slide" / "10 slide" (bazen "8 slide" hizmet tanıtımı için)
3. Konular **yüzeysel/temel düzeyde olamaz.** Kullanıcı örneğin "Facebook Pixel nedir, nasıl kurulur?" önerisini "çok saçma ve basit" diyerek reddetmiştir — bundan sonra her konu somut sayı, eşik değeri, mekanizma açıklaması içermelidir.
4. Konu havuzu tükenmeye başladığında yeni ileri seviye konular üretilir (örnek havuz: Rakip analizi/Meta Ads Library, Dinamik ürün reklamları/DPA, UGC reklamcılığı, Meta Advantage+ otomasyonu, vb.)

---

## 4. 7 SLAYTLIK CAROUSEL YAPISI (STANDART İSKELET)

| Slayt | Tip | Zemin | Amaç |
|---|---|---|---|
| 1 | Hook | Koyu lacivert gradient | Dikkat çekici başlık + alt cümle + marka kimliği + fiyat/rozet (varsa) |
| 2 | Bilgi 1 | Açık zemin | İlk taktik/kural, checklist veya paragraf |
| 3 | Bilgi 2 / Özel görsel | Koyu zemin veya özel (tier/risk/threshold/timeline) | İkinci taktik, genelde en "teknik" slayt |
| 4 | Bilgi 3 / Özel görsel | Koyu zemin | Üçüncü taktik veya karşılaştırma/formül kutusu |
| 5 | Bilgi 4 | Açık zemin | Dördüncü taktik |
| 6 | Bilgi 5 / Özet | Koyu zemin | Beşinci taktik veya "en büyük hata" uyarısı |
| 7 | CTA | Turkuaz-lacivert gradient | Kapanış cümlesi + 3 aksiyon butonu + marka kimliği |

**10 slaytlık versiyonda** 2-8 arası bilgi slaytları 7'ye çıkarılır (aynı yapı, daha fazla taktik).
**8 slaytlık hizmet tanıtımında** yapı: Hook+Fiyat → Kurulum → Hedefleme → Strateji(funnel) → Yönetim → Raporlama → Fiyat detay kartı → CTA.

Açık/koyu zeminler **art arda değişerek** (alternating) görsel ritim oluşturur.

---

## 5. HER SLAYTTA BULUNMASI GEREKEN ÖĞELER

**Her slaytta zorunlu:**
- Alt köşede ilerleme çubuğu (progress bar) — dolu oran = (slayt no / toplam) × 100
- Sağ kenarda kaydırma oku (son slayt hariç) — ince chevron SVG, kenardan içe gradient
- Sağ alt köşede sayfa numarası ("3 / 7" formatında)
- Marka mini-logosu ("UA DIGITAL PRO") köşede (hook ve CTA hariç diğer slaytlarda)

**Hook slaytında (1. slayt) ek olarak:**
- Üstte küçük etiket (tag) — konuyu kategorize eden 3-5 kelime
- İnce turkuaz çizgi ayraç
- Büyük Playfair Display başlık, en az bir vurgulu kelime turkuaz renkte (`<em>`)
- Alt cümle (subtitle) — merak/acı noktası
- Alt kısımda: profil fotoğrafı (yuvarlak, turkuaz kenarlık) + isim + handle + "DIGITAL PRO" rozeti

**Bilgi slaytlarında:**
- Küçük numara etiketi ("İpucu 01 / 07" / "Adım 01" / "Sinyal 01" gibi)
- Emoji ikon (36-42px)
- Playfair Display alt başlık (kısa, vurgulu)
- DM Sans gövde metni (kısa paragraf veya checklist, 2-4 madde)
- Alt kısımda vurgulu "pill" etiket — o slaytın özetini tek satırda veren aksiyon cümlesi

**CTA slaytında (son slayt) ek olarak:**
- Kapanış başlığı (Playfair Display, iddialı/özet cümle)
- 3 buton: 1 birincil (dolu, beyaz zemin) + 2 ikincil (yarı saydam outline) — "Kaydet", "Yorum yap", "Takip et" aksiyonları
- Profil fotoğrafı + isim + handle (hook slaytıyla aynı format)

---

## 6. YAZI DİLİ VE ANLATIM TARZI

- **Dil:** Türkçe, her zaman.
- **Ton:** Samimi ama otoriter — "dünya çapında deneyimli Meta reklam uzmanı" kimliğiyle konuşulur.
- **Cümleler kısa** olmalı. Gereksiz jargon yok; teknik terim kullanılıyorsa (CAPI, ROAS, Lookalike, event_id gibi) açıklanarak kullanılır.
- Madde işaretleri (bullet) kullanılabilir, gövde metni 2-4 cümleyi geçmemeli.
- Her bilgi **uygulanabilir** olmalı — soyut tavsiye değil, somut sayı/eşik/adım içermeli (örnek: "%60-30-10 bütçe kuralı", "frekans 5+ tehlike bölgesi", "event_id ile deduplication").
- Kapanışta her zaman bir "bunu yapmazsan ne olur" veya "en büyük hata" vurgusu tercih edilir.

---

## 7. GÖRSEL TASARIM KURALLARI

- **Format:** Instagram carousel standardı, dikey **4:5 oran** (tasarım tabanı 420×525px, export 1080×1350px).
- **Zemin dönüşümü:** Açık (#F0F6FA) ve koyu (#020818 / #051630) zeminler slayt slayt değişir (görsel ritim için).
- **Üst ince çizgi (topbar):** Açık/koyu bilgi slaytlarında üstte 3px kalınlığında gradient çizgi (mavi→turkuaz→açık turkuaz).
- **Köşe parlama efektleri (glow):** Hook ve CTA slaytlarında büyük, bulanık, yarı saydam turkuaz/mavi daireler (radial-gradient) arka planda derinlik verir.
- **İkonlar:** Emoji kullanılır (🎯 📊 🔁 ⚡ 🧠 vb.) — özel ikon/illüstrasyon üretilmez, kod içinde emoji yeterlidir.
- **Özel slayt görselleri** (konuya göre değişir, çeşitlilik için):
  - İstatistik vurgusu (büyük sayı, ör. "%70")
  - Zaman çizelgesi / timeline (dairesel zaman işaretleri + bağlantı çizgisi)
  - Huni (funnel) grafiği (daralan barlar)
  - Fiyat kartları (bölünmüş ödeme kutuları)
  - Sıralama/tier listesi (01-04 numaralı, en iyisi vurgulu)
  - Risk/eşik rozetleri (renk kodlu: güvenli=turkuaz, uyarı=sarı #C89614, tehlike=turuncu-kırmızı #C4501C)
  - Karşılaştırma kartları (yan yana iki seçenek, biri vurgulu)
  - Formül kutusu (öne çıkan kural/formül metni çerçeve içinde)
  - Checklist (onay kutulu madde listesi)

---

## 8. RENK, FONT, KOMPOZİSYON VE MARKA KURALLARI

### Renk Paleti (Hex kodları — SABİT, değiştirilmez)
| Renk | Hex | Kullanım |
|---|---|---|
| Lacivert en koyu | `#020818` | Ana koyu zemin, gradient başlangıcı |
| Lacivert orta | `#051630` / `#051e3e` | Koyu bilgi slaytı zemini |
| Lacivert aksan | `#082444` | Gradient bitişi |
| Ana mavi | `#0077B6` | Birincil aksan, pill/buton zemini |
| Turkuaz | `#00B4D8` | Marka rengi, vurgu kelimeler, progress bar |
| Açık turkuaz | `#48CAE4` | İkincil vurgu, koyu zeminde etiket rengi |
| Ekstra açık | `#6BD4EB` | Funnel gradient ucu |
| Açık zemin | `#F0F6FA` | Açık slayt arka planı |
| Gövde metni (açık zemin) | `#4a5568` / `#2d3748` | Paragraf metni |
| Uyarı (orta risk) | `#C89614` | Risk rozetleri |
| Tehlike (yüksek risk) | `#C4501C` | Risk rozetleri |

### Fontlar
- **Başlıklar:** `Playfair Display` — ağırlık 700/800/900 (Google Fonts)
- **Gövde/UI metni:** `DM Sans` — ağırlık 300/400/500/600 (Google Fonts)
- İkisi de her HTML dosyasının `<head>` kısmında Google Fonts linkiyle çağrılır.

### Marka Kimliği Sabitleri
- İsim: **Uğur Akkaya**
- Marka: **Uğur Akkaya Digital Pro**
- Handle: **@ugurakkaya_djitalpro**
- Rozet metni: **"DIGITAL PRO"**
- Profil fotoğrafı: Siyah-beyaz, dramatik ışıklı portre (bkz. `brand/assets/ugur_profil_resmi.jpg`) — HTML'e **base64 data URI** olarak gömülür, hook ve CTA slaytlarında yuvarlak, turkuaz kenarlıklı avatar olarak kullanılır.
- Kapak görseli (YouTube/kanal banner'ı) mevcut ama carousel'lerde kullanılmıyor — sadece referans.

---

## 9. GÖRSEL ÜRETİM PROMPTLARININ YAPISI (TEKNİK PIPELINE)

Görseller **AI görsel üretimi ile değil, kod (HTML/CSS) ile** üretilir — bu, marka tutarlılığı ve tekrar üretilebilirlik için kritik bir karardır.

**Adımlar:**
1. Python ile profil fotoğrafı base64'e çevrilir: `base64.b64encode(open(path,'rb').read()).decode()`
2. Tüm slaytları içeren tek bir HTML dosyası oluşturulur — her slayt `<div class="slide ...">` bloğu, hepsi `.wrap` içinde dikey sıralanır (üst üste, sayfa aşağı uzar).
3. **Playwright** ile bu HTML render edilir:
   - Viewport genişliği: **420px** (tasarım tabanı)
   - Viewport yüksekliği: **525 × toplam slayt sayısı** (tüm slaytlar tek sayfada alt alta)
   - `device_scale_factor = 1080 / 420 ≈ 2.571` (bu, çıktının otomatik olarak 1080px genişliğe ölçeklenmesini sağlar — HTML'de hiçbir boyut değişmez, sadece render çözünürlüğü artar)
   - `wait_until="networkidle"` + `wait_for_timeout(4000)` — Google Fonts ve gömülü görsellerin tam yüklenmesi için bekleme
4. Her slayt için ayrı `page.screenshot(clip={x:0, y:i*525, width:420, height:525})` çağrısı yapılır → `slide_01.png`, `slide_02.png` ... şeklinde kaydedilir.
5. Çıktı: her biri **1080×1350px, yüksek kalite PNG**, Instagram carousel'e doğrudan yüklenebilir.

Tam çalışan export scripti için bkz. `templates/export_slides.py`.
Tam CSS/HTML iskeleti için bkz. `templates/carousel_template.html`.

---

## 10. INSTAGRAM AÇIKLAMASI (CAPTION) YAZMA FORMATI

Sabit format, her carousel için bu şablon doldurulur:

```
[HOOK — 2 cümle, acı noktasını veya yaygın yanlışı doğrudan söyler] 👇

[Kısa bağlam cümlesi — sorunu netleştirir veya merak uyandırır]
[Çözümün carousel'de olduğunu belirten 1 satır] 👆

─────────────────────
[emoji] [Slayt 1 özeti — kısa madde]
[emoji] [Slayt 2 özeti — kısa madde]
[emoji] [Slayt 3 özeti — kısa madde]
[emoji] [Slayt 4 özeti — kısa madde]
[emoji] [Slayt 5 özeti — kısa madde]
─────────────────────

[Opsiyonel: "En büyük hata:" vurgusu + 1-2 kısa cümle]

[Kapanış — kısa, güven veren 1-2 cümle]

💾 Kaydet — [o konuya özel kullanım anı, ör. "kampanya kurarken aç"]
💬 [Konuya özel, kişisel yanıt tetikleyen soru] Yorumda söyle!

#[niche-hashtag-1] #[niche-hashtag-2] #[niche-hashtag-3]
#[genel-hashtag] #[genel-hashtag] #[genel-hashtag]
#[genel-hashtag] #[genel-hashtag] #[genel-hashtag] #[genel-hashtag]
```

**Kurallar:**
- Toplam **10 hashtag** — 2-3 niche (konuya özel: #adfatigue, #lookalikeaudience, #conversionapi gibi) + 7-8 genel (#metareklamlari #facebookads #dijitalpazarlama #eticaret #performancemarketing #eticaretsahipleri #reklamstratejisi gibi sabit havuzdan).
- Caption **carousel'in tekrarı değil, özeti + duygusal çerçevesi** olmalı.
- Her caption'ın sonunda kısa bir "neden bu şekilde yazıldı" açıklaması kullanıcıya ayrıca (caption'ın dışında, sohbet içinde) sunulur — bu caption'ın kendi içinde yer almaz.

---

## 11. BAŞLIK, CTA VE HASHTAG KURALLARI

**Başlık (Hook) kuralları:**
- Playfair Display, büyük, en fazla 4 satıra bölünmüş kısa kelime grupları.
- En az bir kelime/ifade turkuaz renkte vurgulanır (`<em>` etiketiyle, CSS'te turkuaz renk).
- Şaşırtıcı, ters köşe veya doğrudan acı noktası içermeli ("Çoğu A/B Test Yalan Söylüyor", "Pixel'in Verisi Eksik. Fark Ettin mi?" gibi).

**CTA kuralları (slayt içi):**
- Her zaman 3 aksiyon: 1) Kaydet, 2) Yorum yap (konuya özel soru), 3) Takip et.
- Buton metinleri emoji ile başlar (🔖 💬 👆).
- Birincil buton dolu/beyaz zemin, ikincil butonlar yarı saydam outline.

**Hashtag kuralları:**
- Sabit genel havuz: `#metareklamlari #facebookads #dijitalpazarlama #eticaret #performancemarketing #eticaretsahipleri #reklamstratejisi #instagramreklamlari`
- Her carousel'e özgü 2-3 niche hashtag eklenir (konunun İngilizce/teknik terimi, ör. #capi #adfatigue #lookalikeaudience #cro #targetaudience).
- Toplam her zaman 10 hashtag.

---

## 12. DEĞİŞTİRİLMEMESİ GEREKEN ÖZEL TALİMATLAR

Bunlar kullanıcının sohbet boyunca açıkça verdiği, **asla ihlal edilmemesi gereken** kurallardır:

1. **Tekrar yasağı:** Daha önce işlenmiş bir carousel başlığı/konusu ASLA tekrar önerilmez veya üretilmez. Her yeni carousel önerisinden önce işlenmiş konular listesi kontrol edilir.
2. **Yüzeysellik yasağı:** İçerik asla "saçma ve basit" seviyede olamaz. Her konu gerçek sayı, eşik değeri, mekanizma veya somut adım içermeli. (Kullanıcı bunu doğrudan ve sert şekilde belirtmiştir.)
3. **Dil:** Her zaman Türkçe.
4. **Marka bilgileri sabit ve bilinir kabul edilir** — isim, handle, renkler, fontlar, profil fotoğrafı her seferinde yeniden sorulmaz.
5. **Görsel üretim yöntemi:** AI ile tek seferlik composite görsel üretmek yerine (kullanıcı bir örnekte bunu denemiş ve kalitesinden memnun kalmamıştır), her zaman kurulu HTML/CSS/Playwright şablon sistemi kullanılır. Kullanıcının kendi sözü: *"senin sistemine şablonuna uygun üretelim, her zamanki gibi ürettiğimiz bilgi amaçlı carousel döngü şeklinde belki daha iyi olur"* — bu onaylanmış ve tercih edilen yöntemdir.
6. **Soru sayısı sınırı:** Yeni bir carousel üretmeden önce en fazla 2 hızlı soru sorulur (konu + slayt sayısı), interaktif buton seçimiyle. Fazla soru sorulmaz.
7. **Video/Reels seslendirme ve AI video prompt işi** bir kez denenmiş, kullanıcı tarafından *"boş ver bunları, carousel üretelim"* denilerek terk edilmiştir — bu iş akışının bir parçası DEĞİLDİR, tekrar talep edilmedikçe gündeme getirilmez.
8. **Teslimat formatı:** Her carousel için PNG dosyaları `present_files` ile sunulur; Instagram açıklaması sadece ayrıca istendiğinde yazılır (otomatik eklenmez).
9. **Hizmet tanıtım carousel'i** normal eğitim içeriğinden farklı bir yapı kullanır (checklist + fiyat kartı + funnel grafiği) ama AYNI marka renk/font/görsel sistemini kullanır — asla farklı bir tasarım diline geçilmez.

---

## 13. ŞİMDİYE KADAR ÜRETİLEN İÇERİKLER (TEKRAR EDİLMEMELİ)

Aşağıdaki 13 carousel bu projede üretilmiştir. Yeni içerik önerirken bu liste MUTLAKA kontrol edilmelidir:

| # | Başlık | Slayt | Öne çıkan özel bilgi/görsel |
|---|---|---|---|
| 1 | Dönüşüm oranını artıran 7 reklam ipucu | 7 | Hook/native kreatif/retargeting/ROAS/hız/hedefleme |
| 2 | Instagram algoritması nasıl çalışır? | 7 | İlk 30 dakika kuralı, kaydet > beğeni, niche hashtag |
| 3 | Reklam kreatifi — Hook → Body → CTA | 7 | Hook formülleri, body yapısı (problem→çözüm→kanıt), tek CTA kuralı |
| 4 | Sepet terk eden müşteriye nasıl ulaşılır? | 7 | %70 istatistiği, 0-1s/1-3g/4-7g zaman çizelgesi, deduplication öncesi segmentasyon |
| 5 | Reklam bütçesi nasıl doğru yönetilir? | 7 | **60/30/10 kuralı** (soğuk/sıcak/mevcut müşteri), max %20 bütçe artışı |
| 6 | Ürün sayfası optimizasyonu | 7 | Fayda>özellik, 6 maddelik checklist |
| 7 | A/B test nasıl doğru kurulur? | 7 | Min. 50 dönüşüm/3.000 gösterim eşiği, öncelik hiyerarşisi (Hook>Görsel>CTA>Renk) |
| 8 | CAPI / iOS14+ sonrası izleme | 7 | Pixel vs CAPI karşılaştırması, **event_id ile deduplication** |
| 9 | Lookalike Audience — kaynak & büyüklük | 7 | Kaynak kalite sıralaması (Purchase>AddToCart>Video>Sayfa beğeni), min 1.000 kişi, %1-3 kuralı |
| 10 | Meta Reklam Danışmanlığı (hizmet tanıtımı) | 8 | 8.000 TL fiyat, 4.000+4.000 TL ödeme planı, risk garantisi, funnel grafiği |
| 11 | Video reklam kurgusu — ilk 3 saniye | 7 | 0s/1s/2s/3s kurgu haritası, %85 sessiz izleme istatistiği |
| 12 | Reklam hesabı kısıtlama/ban önleme | 7 | Renk kodlu risk seviyeleri (yüksek/orta), ödeme istikrarı, IP/çoklu hesap riski |
| 13 | Reklam yorgunluğu (Ad Fatigue) — frekans yönetimi | 7 | **Frekans eşikleri: 1-2 güvenli / 3-4 izleme / 5+ tehlike**, doygunluk vs yorgunluk farkı |

Güncel liste her zaman `content/topics_used.md` dosyasında tutulur — yeni içerik üretilince oraya eklenir.

**Henüz kullanılmamış, öneri havuzunda bekleyen konular:**
- Rakip analizi — Meta Ads Library'den strateji çıkarma
- Dinamik ürün reklamları (DPA) — katalog tabanlı otomasyon
- UGC (Kullanıcı Üretimi İçerik) reklamı neden daha çok satar
- Meta Advantage+ kampanyaları — otomasyon ne zaman işe yarar

---

## 14. GÜNLÜK İÇERİK ÜRETİMİ — BAŞTAN SONA İŞ AKIŞI

1. **Konu belirleme:** `content/topics_used.md` okunur → kullanılmamış 4-5 ileri seviye konu belirlenir → kullanıcıya (veya otomasyon kararına) sunulur.
2. **Slayt sayısı kararı:** 7 (standart) veya 10 (detaylı) seçilir.
3. **İçerik yazımı:** Seçilen konu için 7 slaytlık gerçek, teknik derinlikli içerik yazılır (Bölüm 4-6 kurallarına uyularak). Her slayt için: numara etiketi, ikon, başlık, gövde metni, alt pill cümlesi belirlenir.
4. **Özel görsel seçimi:** İçeriğe en uygun 1-2 özel slayt tipi seçilir (timeline, tier list, risk badge, funnel, formül kutusu, checklist, karşılaştırma vb.) — çeşitlilik için art arda aynı özel tip kullanılmaz.
5. **HTML üretimi:** `templates/carousel_template.html` iskeleti temel alınarak, profil fotoğrafı base64 olarak gömülür, tüm slaytlar tek dosyada birleştirilir.
6. **Progress bar doğrulaması:** Her slaytın ilerleme yüzdesi ve sayfa numarası formülle kontrol edilir: `yüzde = (slayt_no / toplam) × 100`, `numara = "slayt_no/toplam"`. (Bu adımda daha önce bir numaralandırma hatası fark edilip düzeltilmiştir — otomasyonda bu kontrol scriptleştirilmeli.)
7. **Export:** `templates/export_slides.py` çalıştırılır → 1080×1350px PNG dosyaları üretilir.
8. **Kalite kontrolü:** İlk slayt görsel olarak kontrol edilir (metin taşması, kesilme var mı).
9. **Teslimat:** PNG dosyaları çıktı klasörüne kopyalanır, `present_files` ile sunulur.
10. **Caption yazımı (istenirse):** Bölüm 10'daki şablona göre Instagram açıklaması yazılır.
11. **Kayıt:** Üretilen konu `content/topics_used.md` dosyasına eklenir (bir sonraki tekrar kontrolü için).

---

## 15. COWORK OTOMASYONU İÇİN DOSYA/KLASÖR YAPISI

```
ugur-akkaya-carousel-sistemi/
│
├── MASTER_PROJECT_HANDOFF.md          # Bu dosya — tüm sistem kuralları
│
├── brand/
│   ├── profile.md                     # Marka kimliği, renk/font referansı (Bölüm 8 özeti)
│   └── assets/
│       ├── ugur_profil_resmi.jpg      # Hook & CTA slaytlarında kullanılan avatar
│       └── ugur_kapak_resmi.png       # Referans (carousel'lerde kullanılmıyor)
│
├── templates/
│   ├── carousel_template.html         # Tam CSS iskeleti + tüm slayt tipi örnekleri
│   └── export_slides.py               # Parametrik Playwright export scripti
│
├── content/
│   ├── topics_used.md                 # İşlenmiş 13 konunun tam listesi (Bölüm 13)
│   ├── topics_backlog.md              # Henüz kullanılmamış konu havuzu
│   └── caption_template.md            # Bölüm 10'daki caption şablonu
│
└── output/
    ├── {konu-slug}/
    │   ├── slide_01.png ... slide_07.png
    │   └── caption.txt
    └── ...
```

**Kullanım mantığı:** Cowork her yeni carousel talebinde önce `content/topics_used.md`'yi okur, `templates/carousel_template.html`'i temel alarak yeni içerik yazar, `templates/export_slides.py`'yi çalıştırıp `output/{konu-slug}/` altına kaydeder, sonra `topics_used.md`'yi günceller.

---

## 16. MANUEL YAPILAN VE OTOMASYONA GEÇİRİLMESİ GEREKEN İŞLER

| # | Şu ana kadar manuel yapılan iş | Otomasyona geçiş önerisi |
|---|---|---|
| 1 | Kullanıcıya "konu ne olsun / kaç slayt" diye interaktif soru sorma | Cowork'te sabit bir günlük/haftalık rotasyon listesi tanımlanabilir (`topics_backlog.md`'den sırayla çekilir), böylece soru sormaya gerek kalmaz |
| 2 | Her carousel için 7 slaytlık içerik metnini sıfırdan yazma | Bu, LLM'in yaratıcı görevi olarak kalmalı — ama Bölüm 4-6'daki kurallar bir "prompt şablonu" olarak Cowork'e verilirse tutarlılık artar |
| 3 | Progress bar yüzde/numara hatalarını elle fark edip düzeltme | Export öncesi otomatik doğrulama scripti eklenmeli: her slaytın `width:%` değeri ve `"n/toplam"` etiketi formülle çapraz kontrol edilsin |
| 4 | Profil fotoğrafını her carousel'de yeniden base64'e çevirme | Base64 string bir kere üretilip `brand/profile.md` içine sabit olarak kaydedilmeli, her seferinde yeniden encode edilmemeli |
| 5 | Üretilen PNG'leri konuya özel isimlerle `outputs/` klasörüne kopyalama | Script otomatik olarak `output/{konu-slug}/` klasörü oluşturup kaydetsin |
| 6 | Instagram açıklamasını ayrı bir adımda, istek üzerine yazma | İsteğe bağlı kalabilir, ama otomasyonda her carousel ile birlikte bir `caption.txt` otomatik üretilip klasöre konabilir (kullanıcı istemese de hazır dursun) |
| 7 | İşlenmiş konular listesini insan hafızasında/sohbet geçmişinde tutma | `content/topics_used.md` dosyası her üretimden sonra otomatik güncellenmeli — bu, tekrar yasağının (Bölüm 12, madde 1) garantisi için KRİTİK |
| 8 | Görsel kalite kontrolü (ilk slaytı elle açıp bakma) | Basit bir görüntü boyutu/dosya bütünlüğü kontrolü otomatikleştirilebilir; içerik/tasarım kontrolü yine de son onay için insana veya bir gözden geçirme adımına bırakılmalı |

---

*Bu doküman, Uğur Akkaya Digital Pro Instagram hesabı için kurulan carousel üretim sisteminin tam ve eksiksiz devridir. Yeni bir Claude Cowork oturumunda bu dosya + `templates/` ve `content/` klasörleri yüklenerek sistem birebir devam ettirilebilir.*
