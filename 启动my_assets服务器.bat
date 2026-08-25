@echo off
setlocal

rem Keep this launcher ASCII-only because cmd.exe may read UTF-8 batch files with the wrong code page.
cd /d "%~dp0"
title my_assets Local Server
color 0A
cls

echo =========================================================
echo              my_assets Local Resource Server
echo =========================================================
echo.
echo  Keep this window open while the server is running.
echo  Local:  http://127.0.0.1:8766/
echo  LAN:    http://YOUR-LAN-IP:8766/
echo.

set "PY_CMD="
where python >nul 2>&1
if not errorlevel 1 (
  python --version >nul 2>&1
  if not errorlevel 1 set "PY_CMD=python"
)

if not defined PY_CMD (
  where py >nul 2>&1
  if not errorlevel 1 (
    py --version >nul 2>&1
    if not errorlevel 1 set "PY_CMD=py"
  )
)

if not defined PY_CMD if exist "C:\Users\ELevin\AppData\Local\Programs\Python\Python314\python.exe" set "PY_CMD=C:\Users\ELevin\AppData\Local\Programs\Python\Python314\python.exe"

if not defined PY_CMD (
  echo [ERROR] Python was not found.
  echo Install Python 3.7+ and enable "Add Python to PATH", or edit PY_CMD in this file.
  pause
  exit /b 1
)

echo [INFO] Python: %PY_CMD%
%PY_CMD% --version
echo.

netstat -ano | findstr ":8766" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
  echo [WARN] Port 8766 is already in use.
  echo Try this command after changing the port to 8767:
  echo   %PY_CMD% serve_assets.py --port 8767 --host 0.0.0.0
  echo.
)

echo [START] %PY_CMD% serve_assets.py --port 8766 --host 0.0.0.0
echo.
%PY_CMD% serve_assets.py --port 8766 --host 0.0.0.0

echo.
echo ---------------------------------------------------------
if errorlevel 1 (
  echo [my_assets] Server exited with an error.
  echo Common causes: Python, port 8766, firewall, or permissions.
) else (
  echo [my_assets] Server stopped.
)
echo ---------------------------------------------------------
pause
