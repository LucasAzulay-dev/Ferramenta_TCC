@echo off
REM Move up one directory, then into src
cd /d "%~dp0..\src"
REM Run the Python script
python graphical_interface.py