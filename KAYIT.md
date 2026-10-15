# Doğrulama verisi kayıt defteri

## 2026-10-14 — ilk yükleme
- Veriseti kimliği: `XU30-2026-10-13-69afcaff` · durum TEMİZ · betik v2.01 · 05.05–13.10.2026, 111 gün
- Satır: M1 77.426 · M15 5.485 · H1 1.534 · D1 111
- SHA-256 (künyeye karşı): M1, M15, H1, D1 **birebir**
- M15 ↔ M1'den yeniden toplama: 5.485 / 5.485 bar, OHLC ve hacim farkı **0**
- **Keşif verisiyle çapraz kontrol** (`xu30-strateji-arastirma/xu30_kesif_m1_gunduz.csv.gz`, kaynak `00-Akis.csv`):
  05.05–08.09.2026 gündüz barları — 43.480 / 43.480 bar ortak, yalnız birinde olan gün 0;
  open/high/low/close/volume/buy_volume/sell_volume **%100 aynı** (max fark 0,00).
  İki bağımsız yol (MT5 Akış aktarımı ve günlük tick dışa aktarımı) aynı veriyi üretiyor.

| Dönem | Kullanım | Durum |
|---|---|---|
| 05.05–08.09.2026 | Keşif verisiyle aynı (ajan görüyor) | — |
| 09.09–11.09.2026 | Tampon | kullanılmaz |
| 14.09–09.10.2026 | **Kilit** (20 seans) | dokunulmadı |
| 10.10.2026 → | **İleri test** | dokunulmadı |

## 2026-10-14 14:20 — XU30-2026-10-13-8acff644
- 2026-05-05 → 2026-10-13, 111 gün · M1 77426 · M15 5485 · H1 1534 · D1 111
- Yeni günler: yok · önceki kimlik: XU30-2026-10-13-69afcaff
- SHA-256 künyeyle eşleşti · betik v2.01 · veri_akisi v1.01 · bilgisayar SOYDAN

## 2026-10-15 12:26 — XU30-2026-10-14-f954191b
- 2026-05-05 → 2026-10-14, 112 gün · M1 78164 · M15 5536 · H1 1548 · D1 112
- Yeni günler: 2026-10-14 · önceki kimlik: XU30-2026-10-13-8acff644
- SHA-256 künyeyle eşleşti · betik v2.01 · veri_akisi v1.01 · bilgisayar SOYDAN
