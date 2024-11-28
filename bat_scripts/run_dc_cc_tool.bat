@echo off
REM Move up one directory, then into src
cd /d "%~dp0.."
REM Run the Python script
python src\graphical_interface.py