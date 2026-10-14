@echo off
chcp 65001 >nul
rem Hafta ici her gun 23:20'de veriseti guncellemesini otomatik calistirir.
schtasks /create /f /tn "XU30 Veriseti Guncelle" /sc weekly /d MON,TUE,WED,THU,FRI /st 23:20 /tr "\"%~dp0verisetini_guncelle.bat\" /sessiz"
if %errorlevel%==0 (echo Zamanlanmis gorev kuruldu: her is gunu 23:20.) else (echo [HATA] Gorev kurulamadi.)
pause
