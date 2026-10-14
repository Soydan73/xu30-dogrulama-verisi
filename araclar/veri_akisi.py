# -*- coding: utf-8 -*-
"""
XU30 veri akışı — v1.01 (14.10.2026)

Tek tıkla: Veriseti klasöründeki günlük tick dosyalarından M1/M15/H1/D1 kurar
(xu30_veri_guncelle.py, aynı klasörde) ve sonuç TEMİZ ise çıktıları GitHub
`Soydan73/xu30-dogrulama-verisi` deposuna gönderir.

Hangi bilgisayarda olursa olsun aynı çalışır. Bu dosya ve `verisetini_guncelle.bat`
Veriseti klasörünün İÇİNDE durur; klasör Google Drive ile senkronsa her bilgisayarda
aynı dosyalar vardır.

Kullanım:  py veri_akisi.py                 (klasör = bu dosyanın bulunduğu klasör)
           py veri_akisi.py "D:\\baska\\klasor"
           py veri_akisi.py --gonderme       (GitHub'a gönderme, yalnız güncelle)
Çıkış kodu: 0 = tamam, 2 = INCELE (gönderilmedi), 1 = hata
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SURUM = "1.01"
DEPO_URL = "https://github.com/Soydan73/xu30-dogrulama-verisi.git"
BETIK = "xu30_veri_guncelle.py"
EN_AZ_BETIK_SURUMU = (2, 1)
CIKTILAR = ["XU30_M1_birlesik.csv", "XU30_M15.csv", "XU30_H1.csv", "XU30_D1.csv",
            "XU30_donusum_raporu.csv", "XU30_veriseti_kunyesi.json"]
SHA_DOSYALARI = ["XU30_M1_birlesik.csv", "XU30_M15.csv", "XU30_H1.csv", "XU30_D1.csv"]

KLASOR = None
LOG = []


def yaz(msg=""):
    print(msg, flush=True)
    LOG.append(msg)


def dur(kod, msg):
    yaz(msg)
    if KLASOR:
        try:
            with open(KLASOR / "veri_akisi_log.txt", "a", encoding="utf-8") as f:
                f.write(f"\n===== {datetime.now():%Y-%m-%d %H:%M:%S} (kod {kod}) =====\n")
                f.write("\n".join(LOG) + "\n")
        except OSError:
            pass
    sys.exit(kod)


def calistir(komut, cwd=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    r = subprocess.run(komut, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def sha256(yol):
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for p in iter(lambda: f.read(1 << 20), b""):
            h.update(p)
    return h.hexdigest()


def pandas_hazir():
    try:
        import pandas  # noqa: F401
        return True
    except ImportError:
        yaz("pandas kurulu değil, kuruluyor (pip install pandas) ...")
        kod, cikti = calistir([sys.executable, "-m", "pip", "install", "--user", "pandas"])
        if kod != 0:
            yaz(cikti[-1500:])
            return False
        return True


def betik_surumu(yol):
    for satir in open(yol, encoding="utf-8", errors="replace"):
        if satir.startswith("SURUM"):
            s = satir.split("=")[1].strip().strip('"').strip("'")
            try:
                return tuple(int(x) for x in s.split("."))
            except ValueError:
                return (0,)
    return (0,)


def depo_hazirla(depo):
    git = shutil.which("git")
    if not git:
        return None, ("Git bulunamadı. https://git-scm.com/download/win adresinden 'Git for Windows' kurun "
                      "(kurulumda varsayılanlar yeterli), sonra bu dosyayı tekrar çalıştırın.")
    if (depo / ".git").exists():
        kod, cikti = calistir([git, "pull", "--ff-only"], cwd=depo)
        if kod != 0:
            return None, "git pull başarısız:\n" + cikti[-1500:]
    else:
        depo.parent.mkdir(parents=True, exist_ok=True)
        yaz(f"Doğrulama deposu ilk kez indiriliyor: {depo}")
        kod, cikti = calistir([git, "clone", DEPO_URL, str(depo)])
        if kod != 0:
            return None, ("git clone başarısız. GitHub'da Soydan73 hesabıyla oturum açılması gerekebilir "
                          "(ilk seferde tarayıcı penceresi açılır).\n" + cikti[-1500:])
    # yeni bilgisayarda git kimliği tanımlı değilse commit başarısız olur: depoya özel tanımla
    for anahtar, deger in (("user.name", "Soydan73"),
                           ("user.email", "Soydan73@users.noreply.github.com")):
        kod, cikti = calistir([git, "config", anahtar], cwd=depo)
        if kod != 0 or not cikti.strip():
            calistir([git, "config", anahtar, deger], cwd=depo)
    return git, None


def main():
    global KLASOR
    args = [a for a in sys.argv[1:] if not a.startswith("--") and a.lower() != "/sessiz"]
    gonder = "--gonderme" not in sys.argv
    KLASOR = Path(args[0]).resolve() if args else Path(__file__).resolve().parent
    depo = Path(os.environ.get("XU30_DOGRULAMA_DEPO",
                               Path.home() / "xu30-dogrulama-verisi"))

    yaz(f"XU30 veri akışı v{SURUM} · {datetime.now():%d.%m.%Y %H:%M}")
    yaz(f"Bilgisayar   : {os.environ.get('COMPUTERNAME', '?')}")
    yaz(f"Veriseti     : {KLASOR}")
    yaz(f"Python       : {sys.version.split()[0]}")

    betik = KLASOR / BETIK
    if not betik.exists():
        dur(1, f"[HATA] {BETIK} bu klasörde yok. Veriseti klasörünü doğru seçtiğinizden emin olun.")
    sv = betik_surumu(betik)
    if sv < EN_AZ_BETIK_SURUMU:
        dur(1, f"[HATA] {BETIK} sürümü {'.'.join(map(str, sv))}; en az 2.01 gerekli (M15 çıktısı).")
    if not pandas_hazir():
        dur(1, "[HATA] pandas kurulamadı.")

    # 1) güncelle
    yaz("\n--- 1/3 Veriseti güncelleniyor ---")
    kod, cikti = calistir([sys.executable, str(betik), str(KLASOR)], cwd=KLASOR)
    ozet = cikti[cikti.find("--- ÖZET ---"):] if "--- ÖZET ---" in cikti else cikti[-2500:]
    yaz(ozet.strip())
    kunye_yol = KLASOR / "XU30_veriseti_kunyesi.json"
    if not kunye_yol.exists():
        dur(1, "[HATA] künye dosyası oluşmadı; betik çıktısına bakın.")
    kunye = json.load(open(kunye_yol, encoding="utf-8"))
    if kod != 0 or kunye.get("durum") != "TEMIZ":
        dur(2, "\n[INCELE] Veriseti TEMİZ değil. Doğrulama deposu GÜNCELLENMEDİ.\n"
               "Ayrıntı için XU30_veriseti_kunyesi.json ve XU30_donusum_raporu.csv'ye bakın; "
               "önceki çıktılar _onceki_surum klasöründe.")

    # 2) SHA kontrolü
    yaz("\n--- 2/3 Çıktılar künyeyle karşılaştırılıyor ---")
    for ad in SHA_DOSYALARI:
        if sha256(KLASOR / ad) != kunye["sha256"][ad]:
            dur(1, f"[HATA] {ad} SHA-256 künyeyle uyuşmuyor.")
        yaz(f"   OK  {ad}")

    if not gonder:
        dur(0, "\n--gonderme verildi: GitHub'a gönderilmedi. Tamam.")

    # 3) doğrulama deposu
    yaz("\n--- 3/3 Doğrulama deposuna gönderiliyor ---")
    git, hata = depo_hazirla(depo)
    if hata:
        dur(1, "[HATA] " + hata)
    eski = None
    ek = depo / "XU30_veriseti_kunyesi.json"
    if ek.exists():
        try:
            eski = json.load(open(ek, encoding="utf-8")).get("veriseti_kimligi")
        except (OSError, ValueError):
            pass
    kimlik = kunye["veriseti_kimligi"]
    if eski == kimlik:
        dur(0, f"\nDepo zaten güncel ({kimlik}). Gönderilecek yeni veri yok. Tamam.")
    for ad in CIKTILAR:
        shutil.copy2(KLASOR / ad, depo / ad)
    s = kunye["satir"]
    yeni = ", ".join(kunye.get("gerileme", {}).get("yeni_gunler", [])) or "yok"
    satir = (f"\n## {datetime.now():%Y-%m-%d %H:%M} — {kimlik}\n"
             f"- {kunye['ilk_gun']} → {kunye['son_gun']}, {kunye['gun_sayisi']} gün · "
             f"M1 {s.get('M1')} · M15 {s.get('M15')} · H1 {s.get('H1')} · D1 {s.get('D1')}\n"
             f"- Yeni günler: {yeni} · önceki kimlik: {eski or '-'}\n"
             f"- SHA-256 künyeyle eşleşti · betik v{kunye.get('betik_surumu')} · "
             f"veri_akisi v{SURUM} · bilgisayar {os.environ.get('COMPUTERNAME', '?')}\n")
    with open(depo / "KAYIT.md", "a", encoding="utf-8") as f:
        f.write(satir)
    for komut in (["add", "-A"], ["commit", "-m", f"veriseti {kimlik}"], ["push"]):
        kod, cikti = calistir([git] + komut, cwd=depo)
        if kod != 0:
            dur(1, f"[HATA] git {komut[0]} başarısız:\n{cikti[-1500:]}")
    dur(0, f"\nTAMAM. Doğrulama deposu güncellendi: {kimlik} ({kunye['gun_sayisi']} gün, yeni: {yeni}).")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # beklenmeyen hata da kayda geçsin
        dur(1, f"[HATA] beklenmeyen: {type(e).__name__}: {e}")
