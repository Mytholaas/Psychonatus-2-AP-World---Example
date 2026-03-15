@echo off
cls
echo ========================================
echo  Psychonauts 2 Data Extraction Helper
echo ========================================
echo.
echo This helper will guide you through the extraction process.
echo.
echo BEFORE RUNNING THIS:
echo 1. Make sure Psychonauts 2 is closed
echo 2. Save the Python scripts from Visual Studio
echo.
pause
echo.
echo ========================================
echo  Verification Check
echo ========================================
echo.

set "GAME_DIR=C:\Program Files (x86)\Steam\steamapps\common\Psychonauts 2\Psychonauts2\Binaries\Win64"

if exist "%GAME_DIR%\UE4SS.dll" (
    echo [OK] UE4SS installed
) else (
    echo [ERROR] UE4SS not found!
    pause
    exit /b 1
)

if exist "%GAME_DIR%\Mods\PN2DataExtractor\main.lua" (
    echo [OK] Extraction mod installed
) else (
    echo [ERROR] Extraction mod not found!
    pause
    exit /b 1
)

if exist "extracted_data" (
    echo [OK] Output directory exists
) else (
    echo [WARN] Creating output directory...
    mkdir extracted_data
)

echo.
echo ========================================
echo  Ready to Extract!
echo ========================================
echo.
echo INSTRUCTIONS:
echo.
echo 1. Launch Psychonauts 2 from Steam
echo 2. Load your save file
echo 3. Visit each major area (see list below)
echo 4. Press CTRL+F1 in each area
echo 5. Wait for confirmation in UE4SS console
echo 6. Move to next area
echo.
echo AREAS TO VISIT:
echo   - Motherlobe
echo   - Questionable Area
echo   - All mental world levels
echo   - (Grulovia is optional)
echo.
echo After visiting all areas, come back and:
echo   1. Close Psychonauts 2
echo   2. Run this script again
echo   3. Choose option to process data
echo.
pause
echo.
echo Do you want to:
echo   1. Check extracted data
echo   2. Run matching tool
echo   3. Exit
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" goto check_data
if "%choice%"=="2" goto run_matcher
if "%choice%"=="3" goto end

:check_data
echo.
echo Checking extracted data...
echo.
if exist "extracted_data\extracted_data.json" (
    echo [OK] extracted_data.json found
    for %%F in ("extracted_data\extracted_data.json") do echo     Size: %%~zF bytes
) else (
    echo [WARN] extracted_data.json not found
    echo        Have you extracted data from the game yet?
)

if exist "extracted_data\extracted_data.txt" (
    echo [OK] extracted_data.txt found
) else (
    echo [WARN] extracted_data.txt not found
)

if exist "extracted_data\all_classes_detailed.txt" (
    echo [OK] all_classes_detailed.txt found
) else (
    echo [WARN] all_classes_detailed.txt not found
)
echo.
pause
goto menu_start

:run_matcher
echo.
echo Running Python matching tool...
echo.
if not exist "tools\extract_and_match.py" (
    echo [ERROR] extract_and_match.py not found!
    echo         Did you save it from Visual Studio?
    pause
    goto end
)

python tools\extract_and_match.py
echo.
if exist "worlds\psychonauts2\match_report.txt" (
    echo [OK] Match report generated
    echo.
    echo Opening match report...
    start "" "worlds\psychonauts2\match_report.txt"
)
pause
goto menu_start

:menu_start
cls
echo.
echo ========================================
echo  What would you like to do?
echo ========================================
echo.
echo 1. Check extracted data status
echo 2. Run matching tool
echo 3. View verification summary
echo 4. Exit
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto check_data
if "%choice%"=="2" goto run_matcher
if "%choice%"=="3" (
    if exist "VERIFICATION_COMPLETE.txt" (
        start "" "VERIFICATION_COMPLETE.txt"
    )
    goto menu_start
)
if "%choice%"=="4" goto end

:end
echo.
echo Thank you for using the extraction helper!
echo.
exit /b 0
