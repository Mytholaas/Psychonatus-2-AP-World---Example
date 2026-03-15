@echo off
echo ================================================
echo   Launching FModel - Psychonauts 2 Asset Viewer
echo ================================================
echo.
echo FModel will open in a new window.
echo.
echo FIRST-TIME SETUP:
echo 1. Click Settings (gear icon)
echo 2. Set Game Directory to:
echo    C:\Program Files (x86)\Steam\steamapps\common\Psychonauts 2
echo 3. Set UE Version to: GAME_UE4_27
echo 4. Click OK
echo.
echo Then double-click Psychonauts2-WindowsNoEditor.pak to load it!
echo.
echo See FMODEL_GUIDE.md for detailed instructions.
echo.
pause

cd /d "%~dp0\tools\fmodel"
start FModel.exe

echo.
echo FModel launched!
echo.
echo When you're done extracting, export files to:
echo %~dp0extracted_fmodel_data\
echo.
