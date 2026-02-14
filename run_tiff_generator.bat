@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONPATH=%CD%\UmiOCR-data\site-packages
echo 正在运行TIFF生成器（简化版）...
echo.
UmiOCR-data\runtime\python.exe generate_test_tiff_simple.py
echo.
pause
