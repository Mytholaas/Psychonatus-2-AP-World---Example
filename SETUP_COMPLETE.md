# Psychonauts 2 UE4SS Data Extraction Setup - Complete

## Summary

Successfully set up UE4SS v3.0.1 for Psychonauts 2 to extract exact game data and link it to your Archipelago world repository.

## What Has Been Installed

### 1. UE4SS Installation ✓
- **Location**: C:\Program Files (x86)\Steam\steamapps\common\Psychonauts 2\Psychonauts2\Binaries\Win64\
- **Version**: 3.0.1 (latest stable)
- **Status**: Fully configured with console enabled

### 2. Custom PN2DataExtractor Mod ✓
**Features**:
- CTRL+F1: Extract current area
- CTRL+F3: GLOBAL extraction (ALL levels including Grulovia!)
- CTRL+F2: Dump all classes (debug)

**Extracts**:
- PSI Cards, Figments, Nuggets
- Emotional Baggage, Memory Vaults, Half-a-Minds
- Coordinates and object paths
- Level names and class names

### 3. Python Tools ✓
- extract_and_match.py - Matching tool (supports global extraction)
- update_csvs.py - CSV updater with backups

### 4. Documentation ✓
- GRULOVIA_SOLUTION.txt - How to extract without visiting
- GRULOVIA_QUICK_GUIDE.txt - Quick reference
- EXTRACTION_CHECKLIST.txt - Progress tracker
- Complete helper scripts

## Recommended Workflow

### Step 1: Launch Game
1. Open Psychonauts 2 from Steam
2. Load ANY save file
3. Wait for game to load

### Step 2: Extract Data
Press CTRL+F3 for global extraction
- This extracts ALL levels at once
- Includes Grulovia without visiting it
- Saves to: extracted_data\global_extraction.txt

### Step 3: Process Data
```
python tools\extract_and_match.py
```

### Step 4: Review Results
- global_extraction.txt - All game data by level
- match_report.txt - Matching analysis  
- extracted_game_items.csv - CSV format

## Key Bindings

| Key | Function |
|-----|----------|
| CTRL+F1 | Extract current area |
| CTRL+F2 | Dump classes |
| CTRL+F3 | Global extraction (recommended!) |
| ~ or  | Toggle console |

## Grulovia Solution

**Problem**: Can't access Grulovia in save file

**Solution**: CTRL+F3 global extraction gets it automatically!

Global extraction uses FindAllOf() to search ALL game objects in memory, including from unloaded/inaccessible levels.

## Files Created

### Game Directory:
- UE4SS.dll, dwmapi.dll
- UE4SS-settings.ini (modified)
- Mods\PN2DataExtractor\main.lua (v3.0)

### Repository:
- tools\extract_and_match.py (12,395 bytes)
- tools\update_csvs.py
- SETUP_COMPLETE.md (this file)
- extraction_helper.bat
- verify_setup.bat
- Documentation files

## Next Steps

1. Close file tabs in Visual Studio
2. Open saved files from disk (Ctrl+O)
3. Launch Psychonauts 2
4. Press CTRL+F3 for global extraction
5. Run: python tools\extract_and_match.py
6. Review match_report.txt

## Status

✅ UE4SS Installed
✅ Global Extraction Enabled
✅ Python Tools Ready
✅ Documentation Complete
✅ Grulovia Solution Implemented

**Ready to extract! Press CTRL+F3 in-game!**
