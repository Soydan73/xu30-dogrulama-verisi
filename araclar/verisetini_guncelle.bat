@echo off
chcp 65001 >nul
title XU30 veriseti guncelleme
cd /d "%~dp0"
set "PYCMD="
where py >nul 2>nul && set "PYCMD=py -3"
if not defined PYCMD where python >nul 2>nul && set "PYCMD=python"
if not defined PYCMD goto :pythonyok
%PYCMD% "%~dp0veri_akisi.py" "%~dp0." %*
goto :son
:pythonyok
echo [HATA] Python bulunamadi. https://www.python.org/downloads/ adresinden kurun
echo        (kurulumda "Add python.exe to PATH" kutusunu isaretleyin).
:son
echo.
if /i not "%~1"=="/sessiz" pause
