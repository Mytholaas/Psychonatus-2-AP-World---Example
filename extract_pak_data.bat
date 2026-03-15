@echo off
echo ================================================
echo   Psychonauts 2 Pak File Extractor
echo ================================================
echo.
echo This will extract collectible data from the game's pak files
echo using QuickBMS (a safe, read-only extraction tool).
echo.
echo The extraction will focus on collectible-related files only
echo to save time and disk space.
echo.
pause

cd /d "%~dp0"
python tools\pak_extractor.py

echo.
echo ================================================
echo   Extraction Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Review the extracted files in extracted_pak_data\
echo 2. Run tools\extract_and_match.py to analyze the data
echo 3. Compare with your existing CSV files
echo.
pause
