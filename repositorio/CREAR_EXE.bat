@echo off
setlocal
cd /d "%~dp0"
py -c "import tkinter, venv" >nul 2>&1
if not errorlevel 1 (
  py -m venv .venv-build
  goto entorno
)
python -c "import tkinter, venv" >nul 2>&1
if not errorlevel 1 (
  python -m venv .venv-build
  goto entorno
)
echo No se encontro Python con Tkinter y venv.
pause
exit /b 1
:entorno
if errorlevel 1 goto error
".venv-build\Scripts\python.exe" -m pip install -r requirements-build.txt
if errorlevel 1 goto error
".venv-build\Scripts\python.exe" -m PyInstaller --onefile --windowed --name CookieAutoClicker --noconfirm cookie_autoclicker.py
if errorlevel 1 goto error
echo Listo: dist\CookieAutoClicker.exe
pause
exit /b 0
:error
echo No se pudo crear el ejecutable. Revisa el error de arriba.
pause
exit /b 1
