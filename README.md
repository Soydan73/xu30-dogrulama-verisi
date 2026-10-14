# xu30-dogrulama-verisi

XU30_YAKINVADE **doğrulama verisi**. Yalnız aday doğrulamasında (kilit testi, ileri test) kullanılır.

> ⛔ **Araştırma ajanı bu depoyu KULLANMAZ.** Burada ajanın görmemesi gereken kilitli dönem
> (14.09–09.10.2026) ve ileri test dönemi (10.10.2026 →) vardır. Ajanın tek veri kaynağı
> `Soydan73/xu30-strateji-arastirma` içindeki keşif dosyasıdır (≤ 08.09.2026).

## İçerik
| Dosya | Kaynak |
|---|---|
| `XU30_M1_birlesik.csv` | `xu30_veri_guncelle.py` v2.00 (günlük tick → M1, tüm seanslar, `seans` etiketli) |
| `XU30_M15.csv` | M15 |
| `XU30_H1.csv` | H1 (saat başına hizalı) |
| `XU30_D1.csv` | D1 (yalnız gündüz) |
| `XU30_veriseti_kunyesi.json` | Veriseti kimliği, aralık, SHA-256, kontroller |

## Kullanım kuralları
1. Her doğrulama raporu `veriseti_kimligi` ile başlar.
2. **Kilit testi** (14.09–09.10.2026, 20 seans): aday başına **bir kez**. Sonuç ne olursa olsun tekrar edilmez.
3. **İleri test**: yalnız adayın ön kayıt tarihinden **sonra** gelen seanslar.
4. Bu veriyle yeni fikir aranmaz, parametre ayarlanmaz.

## Güncelleme
Bilgisayara bağlı bir oturumda "verisetini güncelle" yapıldıktan sonra güncel çıktılar buraya gönderilir;
künyedeki kimlik değişir, eski sürümler git geçmişinde kalır.
