@echo off
REM Move up one directory, then into src
cd /d "%~dp0..\src"
REM Run the Python script
python interface_grafica.py