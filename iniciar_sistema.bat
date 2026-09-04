@echo off
cd /d "C:\ArtTendas\arttendas"
start /b py manage.py runserver --noreload >nul 2>&1
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
py manage.py runserver --noreload >nul 2>&1
