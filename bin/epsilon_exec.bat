@echo off
setlocal
REM Ejecutamos los requerimientos
set SCRIPT_PATH=%~dp0\..\src\epsilon\epsilon.py
REM Ejecutando el script...
python "%SCRIPT_PATH%"
REM El script ha terminado de ejecutarse
endlocal