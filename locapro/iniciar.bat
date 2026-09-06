@echo off
title LocaPro - Sistema de Gestao
color 0A
cd /d "%~dp0"

echo.
echo  ==========================================
echo    LOCAPRO - Sistema de Gestao
echo  ==========================================
echo.

:: Verifica Python
py --version >nul 2>&1
if errorlevel 1 (
    echo  [ERRO] Python nao encontrado!
    echo  Instale em: https://python.org/downloads
    pause & exit
)

:: Instala dependencias
echo  [1/4] Instalando dependencias...
py -m pip install django pillow --quiet --disable-pip-version-check

:: Migrations
echo  [2/4] Criando banco de dados...
py manage.py makemigrations inventario --no-input >nul 2>&1
py manage.py makemigrations eventos --no-input >nul 2>&1
py manage.py migrate --no-input

:: Seed de demonstracao
echo  [3/4] Carregando dados...
py manage.py seed_data

:: Abre navegador e inicia servidor
echo  [4/4] Iniciando servidor...
echo.
echo  ==========================================
echo    Acesse: http://127.0.0.1:8000
echo    Para encerrar o servidor, finalize o processo Python no Gerenciador de Tarefas.
echo  ==========================================
echo.

set CHROME_PATH=
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set "CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

if defined CHROME_PATH (
    start "" "%CHROME_PATH%" --app=http://127.0.0.1:8000
) else (
    start "" http://127.0.0.1:8000
)

py manage.py runserver
