@echo off
setlocal
cd /d "%~dp0"
py -c "import tkinter" >nul 2>&1
if not errorlevel 1 (
  py cookie_autoclicker.py
  goto resultado
)
python -c "import tkinter" >nul 2>&1
if not errorlevel 1 (
  python cookie_autoclicker.py
  goto resultado
)
echo No se encontro Python con Tkinter. Si no tienes Python, usa el .exe de Releases.
pause
exit /b 1
:resultado
if errorlevel 1 (
  echo No se pudo iniciar. Revisa el error de arriba.
  pause
  exit /b 1
)
exit /b 0
