@echo off
echo ================================================
echo   Psychonauts 2 Save File Restore Utility
echo ================================================
echo.
echo This will restore your save files from the backup
echo created on 2026-03-14 at 15:35:12
echo.
echo WARNING: This will overwrite your current saves!
echo.
pause

set "BACKUP_PATH=%LOCALAPPDATA%\Psychonauts2\Saved\SaveGames_BACKUP_2026-03-14_15-35-12"
set "SAVE_PATH=%LOCALAPPDATA%\Psychonauts2\Saved\SaveGames"

if not exist "%BACKUP_PATH%" (
    echo [ERROR] Backup not found at: %BACKUP_PATH%
    pause
    exit /b 1
)

echo.
echo Restoring saves from backup...
echo.

xcopy "%BACKUP_PATH%\*.*" "%SAVE_PATH%\" /Y /E /I

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Saves restored successfully!
    echo.
) else (
    echo.
    echo [ERROR] Failed to restore saves
    echo.
)

pause
