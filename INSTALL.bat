@echo off
echo ========================================
echo Psychonauts 2 Archipelago Installer
echo ========================================
echo.

REM Check if Archipelago is installed
set "AP_PATH=C:\ProgramData\Archipelago"
if not exist "%AP_PATH%" (
    set "AP_PATH=%LOCALAPPDATA%\Archipelago"
)
if not exist "%AP_PATH%" (
    set "AP_PATH=%APPDATA%\Archipelago"
)

if not exist "%AP_PATH%" (
    echo [ERROR] Archipelago not found!
    echo.
    echo Please install Archipelago first from:
    echo https://archipelago.gg
    echo.
    pause
    exit /b 1
)

echo [OK] Found Archipelago at: %AP_PATH%
echo.

REM Determine world installation path
set "WORLDS_PATH=%AP_PATH%\lib\worlds"
if not exist "%WORLDS_PATH%" (
    set "WORLDS_PATH=%AP_PATH%\custom_worlds"
)

if not exist "%WORLDS_PATH%" (
    mkdir "%WORLDS_PATH%"
)

echo Installing Psychonauts 2 world...
copy /Y "psychonauts2.apworld" "%WORLDS_PATH%\" >nul
if errorlevel 1 (
    echo [ERROR] Failed to copy world file!
    pause
    exit /b 1
)

echo [OK] Installed psychonauts2.apworld
echo.

REM Copy YAML template to Players folder
set "PLAYERS_PATH=%AP_PATH%\Players"
if not exist "%PLAYERS_PATH%" (
    mkdir "%PLAYERS_PATH%"
)

echo Copying player template...
copy /Y "Psychonauts2_Player.yaml" "%PLAYERS_PATH%\" >nul
if errorlevel 1 (
    echo [WARNING] Could not copy YAML to Players folder
    echo You can copy it manually later.
) else (
    echo [OK] Copied Psychonauts2_Player.yaml to Players folder
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit Psychonauts2_Player.yaml in: %PLAYERS_PATH%
echo 2. Run ArchipelagoGenerate.exe to create your seed
echo 3. Host or join a multiworld game!
echo.
echo See README_PLAYERS.txt for detailed instructions.
echo.
pause
