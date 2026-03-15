@echo off
echo ========================================
echo  Psychonauts 2 UE4SS Installation Check
echo ========================================
echo.

set "GAME_DIR=C:\Program Files (x86)\Steam\steamapps\common\Psychonauts 2\Psychonauts2\Binaries\Win64"
set "REPO_DIR=C:\Users\adkin\source\repos\Psychonauts-2-AP-World---Example"

echo Checking UE4SS installation...
echo.

if exist "%GAME_DIR%\UE4SS.dll" (
    echo [OK] UE4SS.dll found
) else (
    echo [ERROR] UE4SS.dll NOT found
)

if exist "%GAME_DIR%\dwmapi.dll" (
    echo [OK] dwmapi.dll found
) else (
    echo [ERROR] dwmapi.dll NOT found
)

if exist "%GAME_DIR%\UE4SS-settings.ini" (
    echo [OK] UE4SS-settings.ini found
) else (
    echo [ERROR] UE4SS-settings.ini NOT found
)

if exist "%GAME_DIR%\Mods\PN2DataExtractor\main.lua" (
    echo [OK] PN2DataExtractor mod found
) else (
    echo [ERROR] PN2DataExtractor mod NOT found
)

findstr /C:"PN2DataExtractor : 1" "%GAME_DIR%\Mods\mods.txt" >nul 2>&1
if %errorlevel%==0 (
    echo [OK] PN2DataExtractor is enabled
) else (
    echo [WARNING] PN2DataExtractor may not be enabled
)

echo.
echo Checking repository folders...
echo.

if exist "%REPO_DIR%\extracted_data" (
    echo [OK] extracted_data folder exists
) else (
    echo [ERROR] extracted_data folder NOT found
)

if exist "%REPO_DIR%\worlds\psychonauts2\data\Psychonauts_2_Item_List.csv" (
    echo [OK] Item List CSV found
) else (
    echo [ERROR] Item List CSV NOT found
)

if exist "%REPO_DIR%\worlds\psychonauts2\data\Psychonauts_2_Check_List.csv" (
    echo [OK] Check List CSV found
) else (
    echo [ERROR] Check List CSV NOT found
)

echo.
echo ========================================
echo  Summary
echo ========================================
echo.
echo If all checks show [OK], you're ready to extract!
echo.
echo To extract data:
echo   1. Launch Psychonauts 2
echo   2. Load a save file
echo   3. Press CTRL+F1 in any level
echo   4. Check extracted_data folder for output
echo.
echo Press any key to exit...
pause >nul
