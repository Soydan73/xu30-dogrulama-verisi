# XU30 veri akışı — kurulum ve kullanım (v1.01)

Amaç: veriseti güncellemesini **hangi bilgisayarda olursan ol** tek tıkla yapmak ve sonucu
GitHub `Soydan73/xu30-dogrulama-verisi` deposuna göndermek. Claude oturumunun bilgisayara
bağlı olması **gerekmez**; Claude güncel veriyi GitHub'dan okur.

## Nasıl çalışır
```
MT5 tick dışa aktarımı ──► Veriseti klasörü (Google Drive ile senkron)
                               │  çift tık: verisetini_guncelle.bat
                               ▼
                    xu30_veri_guncelle.py v2.01  →  M1 / M15 / H1 / D1 + künye
                               │  yalnız TEMİZ ise
                               ▼
                    GitHub: xu30-dogrulama-verisi  ──►  Claude (bulut, bilgisayar kapalıyken de)
```
Bu dosyalar Veriseti klasörünün **içinde** durur. Klasör Google Drive ile senkron olduğu için
her bilgisayarda aynı dosyalar vardır.

## Her bilgisayarda bir kez yapılacak kurulum (~10 dakika)
1. **Google Drive (masaüstü)**: https://www.google.com/drive/download/ → kur, lazercim@gmail.com ile giriş yap.
   Drive'daki Veriseti klasörü (tick dosyalarının olduğu klasör) bilgisayarda bir sürücü olarak görünür
   (ör. `G:\Drive'ım\...`). Klasöre sağ tık → "Çevrimdışı kullanılabilir" seç (dosyalar hep yerelde dursun).
2. **Python 3**: https://www.python.org/downloads/ → kurulumun ilk ekranında **"Add python.exe to PATH"**
   kutusunu işaretle. (pandas'ı ilk çalıştırmada akış kendisi kurar.)
3. **Git for Windows**: https://git-scm.com/download/win → varsayılan ayarlarla kur.
4. **İlk çalıştırma**: Veriseti klasöründe `verisetini_guncelle.bat`'a çift tıkla. İlk seferde GitHub
   giriş penceresi açılır → **Soydan73** hesabıyla giriş yap (SoydanAkdeniz değil). Bir daha sorulmaz.

## Günlük kullanım
1. Kapanıştan sonra MT5'ten günün tick dosyasını her zamanki gibi dışa aktar, **Veriseti klasörüne** kaydet.
2. `verisetini_guncelle.bat`'a çift tıkla. Ekranda sonuç yazar:
   - `TAMAM. Doğrulama deposu güncellendi: XU30-…` → bitti.
   - `[INCELE] …` → eski günlerden biri değişmiş/kaybolmuş; depo **güncellenmez**. Claude'a sor.
   - `Depo zaten güncel` → yeni dosya yok.
   Her çalıştırma `veri_akisi_log.txt`'ye yazılır.

İstersen **otomatik**: `otomatik_gorev_kur.bat`'a bir kez çift tıkla → her iş günü 23:20'de kendiliğinden
çalışır (bilgisayar açıksa). Tick dışa aktarımını yine sen yaparsın; dosya yoksa akış "depo zaten güncel" der.

## Sorun giderme
| Mesaj | Çözüm |
|---|---|
| Python bulunamadı | Adım 2; "Add to PATH" işaretli olmalı. Kurulumdan sonra yeni pencere aç. |
| Git bulunamadı | Adım 3. |
| git clone / push başarısız | GitHub girişinin **Soydan73** hesabıyla yapıldığını kontrol et. Windows "Kimlik Bilgisi Yöneticisi" → github.com kaydını silip tekrar dene. |
| xu30_veri_guncelle.py sürümü < 2.01 | Klasördeki betik eski; Claude'dan v2.01'i iste. |
| SHA-256 uyuşmuyor | Çalışma sırasında dosya değişmiş (Drive senkronu); birkaç dakika sonra tekrar çalıştır. |

## Kurallar
- Doğrulama deposu **yalnız TEMİZ** sonuçla güncellenir; eski sürümler git geçmişinde kalır.
- Bu veri araştırma ajanının deposuna (`xu30-strateji-arastirma`) **asla** konmaz (kilitli dönem içerir).
- Aynı Veriseti klasörünü iki bilgisayarda **aynı anda** çalıştırma (Drive çakışması).
