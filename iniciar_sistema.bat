@echo off
cd /d "%~dp0locapro"

:: Iniciar o servidor em uma nova janela de terminal para evitar erro de redirecionamento
start "Servidor Django LocaPro" cmd /c "py manage.py runserver"

:: Aguardar 3 segundos para o servidor ligar
timeout /t 3 /nobreak >nul

:: Tenta abrir no modo app do Edge
start "" msedge --app=http://127.0.0.1:8000 --window-size=1280,800 2>nul
if errorlevel 1 (
  :: Tenta Chrome modo app
  start "" chrome --app=http://127.0.0.1:8000 --window-size=1280,800 2>nul
  if errorlevel 1 (
    :: Fallback: navegador padrao
    start "" http://127.0.0.1:8000
  )
)
exit
