# Psychonauts 2 Pak File Extraction Guide

## Overview

This method extracts game data directly from Psychonauts 2's pak files using **QuickBMS**, a safe read-only extraction tool. This approach:

✅ **Does NOT modify the game** (read-only)  
✅ **Works without running the game**  
✅ **Extracts exact class names and paths**  
✅ **Includes ALL levels** (including Grulovia)  
✅ **No performance impact or crashes**

---

## What Was Installed

### QuickBMS v4.0.1
- Location: `tools/quickbms/`
- Purpose: Extract files from Unreal Engine pak archives
- Safe: Read-only, does not modify game files

### Unreal Engine 4 Extraction Script
- Location: `tools/quickbms/unreal_tournament_4.bms`
- Purpose: Tells QuickBMS how to read UE4 pak files
- Compatible: Works with UE4.0 - UE4.27 (Psychonauts 2 uses 4.27)

### Python Extraction Tool
- Location: `tools/pak_extractor.py`
- Purpose: Automates extraction and cataloging of collectibles

---

## How to Use

### Quick Method (Recommended)

1. **Run the extraction script:**
   ```
   extract_pak_data.bat
   ```

2. **Choose option 1** (Quick extract - collectibles only)

3. **Wait for extraction** (may take 5-15 minutes depending on system)

4. **Review results** in `extracted_pak_data/`

### Manual Method

If you want more control:

```bash
cd tools
python pak_extractor.py
```

---

## What Gets Extracted

The pak file contains:
- **Blueprint files (.uasset)** - Object definitions with class names
- **Map files (.umap)** - Level layouts with actor placements  
- **Localization files** - Item names and descriptions
- **Data tables** - Collectible counts and properties

### Collectible Types We're Looking For:

1. **Psi Cards** - Class: `BP_PsiCard_C` or similar
2. **Figments** - Class: `BP_Figment_C` or similar  
3. **Nuggets of Wisdom** - Class: `BP_Nugget_C` or similar
4. **Emotional Baggage** - Class: `BP_Baggage_C` or similar
5. **Memory Vaults** - Class: `BP_MemoryVault_C` or similar
6. **Half-A-Minds** - Class: `BP_HalfAMind_C` or similar

---

## After Extraction

### Step 1: Analyze the Data

Run the updated extraction analyzer:
```bash
python tools\extract_and_match.py
```

This will:
- Parse the extracted .uasset files
- Find collectible class definitions
- Match against your existing CSVs
- Generate a comprehensive report

### Step 2: Review the Report

Check `match_report.txt` for:
- ✅ Items correctly matched between pak and CSV
- ⚠️ Items in pak but missing from CSV (need to add)
- ❌ Items in CSV but not found in pak (typos or incorrect names)

### Step 3: Update Your CSVs

Based on the report, update:
- `worlds/psychonauts2/data/Psychonauts_2_Item_List.csv`
- `worlds/psychonauts2/data/Psychonauts_2_Check_List.csv`

---

## Troubleshooting

### "QuickBMS failed to extract"
- Make sure you have at least **10 GB free disk space**
- Check that the pak file exists at:  
  `C:\Program Files (x86)\Steam\steamapps\common\Psychonauts 2\Psychonauts2\Content\Paks\`
- Try running `extract_pak_data.bat` as Administrator

### "Python script error"
- Make sure Python 3.7+ is installed
- Required modules: `os`, `subprocess`, `json`, `pathlib` (all standard library)

### "Extraction too slow"
- Use option 1 (Quick extract) instead of full extraction
- The targeted extraction only pulls collectible-related files
- Full extraction (30GB) can take 30+ minutes

---

## Technical Details

### File Structure After Extraction

```
extracted_pak_data/
├── Psychonauts2/
│   ├── Content/
│   │   ├── Blueprints/
│   │   │   ├── Collectibles/
│   │   │   │   ├── BP_PsiCard_Base.uasset
│   │   │   │   ├── BP_Figment_Base.uasset
│   │   │   │   └── ...
│   │   ├── Levels/
│   │   │   ├── Motherlobe/
│   │   │   ├── Grulovia/
│   │   │   └── ...
│   │   └── Data/
│   │       └── CollectibleTables/
│   └── ...
└── collectibles_catalog.json
```

### What to Look For in .uasset Files

- **Class Names**: The actual UE4 class used (e.g., `BP_PsiCard_ML01_C`)
- **Object Paths**: Full path to the object (e.g., `/Game/Levels/Motherlobe/Collectibles/ML_PsiCard_01`)
- **Properties**: Location data, display names, item IDs

---

## Next Steps

1. ✅ Extract pak data using `extract_pak_data.bat`
2. ⏳ Parse extracted files to find exact class names
3. ⏳ Update CSVs with correct object paths
4. ⏳ Test Archipelago integration

---

## Why This Works Better Than UE4SS

| Feature | UE4SS | Pak Extraction |
|---------|-------|----------------|
| Game stability | ❌ Crashes | ✅ No impact |
| Grulovia access | ❌ Need to visit | ✅ All levels |
| Reliability | ❌ Mod didn't load | ✅ Always works |
| Speed | ⏱️ In-game only | ⏱️ Anytime |
| Data completeness | ⚠️ Partial | ✅ Complete |

---

**Created:** March 14, 2026  
**Method:** QuickBMS + UE4 extraction  
**Status:** Ready to use
