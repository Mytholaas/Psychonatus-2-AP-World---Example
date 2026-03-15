# FModel Setup and Usage Guide for Psychonauts 2

## What is FModel?

FModel is a professional asset viewer for Unreal Engine games. It supports:
- ✅ UE4.27 (Psychonauts 2's engine version)
- ✅ Encrypted/custom pak files
- ✅ GUI interface - no command line needed
- ✅ Direct export of assets and data
- ✅ JSON export for easy parsing

---

## Installation Complete

✅ **FModel installed at:**
```
C:\Users\adkin\source\repos\Psychonauts-2-AP-World---Example\tools\fmodel\FModel.exe
```

---

## How to Use FModel

### Step 1: Launch FModel

Double-click: `launch_fmodel.bat`

Or manually run:
```
C:\Users\adkin\source\repos\Psychonauts-2-AP-World---Example\tools\fmodel\FModel.exe
```

### Step 2: First-Time Setup

When FModel opens for the first time:

1. **Click "Settings" (gear icon)**

2. **Set the Game Directory:**
   - Click "..." next to "Game's Directory"
   - Navigate to: `C:\Program Files (x86)\Steam\steamapps\common\Psychonauts 2`
   - Click "Select Folder"

3. **Select Unreal Engine Version:**
   - From dropdown, select: **"GAME_UE4_27"**

4. **Click "OK"** to save settings

### Step 3: Load the Pak File

1. **In the left panel**, you'll see:
   - `Psychonauts2-WindowsNoEditor.pak`

2. **Double-click** the pak file to load it

3. **Wait** for FModel to index the file (1-2 minutes for 29GB)

### Step 4: Navigate to Collectibles

In the file tree, navigate to:
```
Psychonauts2/Content/Blueprints/Collectibles/
```

Or use the search bar at the top to search for:
- `PsiCard`
- `Figment`
- `Nugget`
- `Baggage`
- `Memory`
- `HalfAMind`

### Step 5: Export Data

**For individual assets:**
1. **Click** on an asset (e.g., `BP_PsiCard_ML01`)
2. **Right-click** → "Save Properties (.json)"
3. Choose export location

**For bulk export:**
1. **Select multiple files** (Ctrl+Click or Shift+Click)
2. **Right-click** → "Export Raw Data (.uasset)"
3. Or "Save Properties (.json)" for all

### Step 6: Export to Our Project

**Recommended export location:**
```
C:\Users\adkin\source\repos\Psychonauts-2-AP-World---Example\extracted_fmodel_data\
```

---

## What to Look For

### Collectible Blueprint Locations

Expected paths in the pak:
```
Psychonauts2/Content/Blueprints/Collectibles/
├── PsiCards/
│   ├── BP_PsiCard_Base.uasset
│   ├── BP_PsiCard_ML01.uasset  (Motherlobe)
│   ├── BP_PsiCard_GR01.uasset  (Grulovia)
│   └── ...
├── Figments/
│   ├── BP_Figment_Base.uasset
│   └── ...
├── Nuggets/
├── Baggage/
├── Memories/
└── HalfAMinds/
```

### Level Data Locations

```
Psychonauts2/Content/Levels/
├── Motherlobe/
├── Grulovia/
├── CassieBrain/
├── HollisBrain/
└── ...
```

### What Each Asset Contains

When you export as JSON, you'll get:
- **Class name** (e.g., `BP_PsiCard_ML01_C`)
- **Object path** (e.g., `/Game/Blueprints/Collectibles/PsiCards/BP_PsiCard_ML01`)
- **Properties** (location coordinates, display name, item ID, etc.)
- **Parent class** references

---

## Tips for Efficient Extraction

### Use the Search Filter

1. **Click the funnel icon** (filter)
2. **Enable filters:**
   - ☑ "Show Only Blueprints"
   - ☑ "Show Only DataTables"

3. **In search bar, type:**
   - `Collectible` - finds all collectible-related files
   - `PsiCard` - finds all Psi Cards
   - `Table` - finds data tables (often have counts/lists)

### Export Strategy

**Best approach:**
1. Export all blueprint files as JSON
2. Export any DataTable files (these often contain lists)
3. Parse the JSON files with our Python script

---

## After Extraction

### Step 1: Parse the Exported JSON

We'll create a Python script to parse FModel's JSON exports:
```bash
python tools\parse_fmodel_json.py
```

This will:
- Read all exported JSON files
- Extract class names, object paths, and properties
- Generate a CSV matching our format

### Step 2: Match with Existing Data

Run the matching tool:
```bash
python tools\extract_and_match.py
```

This will compare the extracted data with your 558 items and 608 checks.

### Step 3: Update CSVs

Based on the match report, update:
- `worlds/psychonauts2/data/Psychonauts_2_Item_List.csv`
- `worlds/psychonauts2/data/Psychonauts_2_Check_List.csv`

---

## Advantages of FModel

| Feature | QuickBMS | FModel |
|---------|----------|--------|
| UE4.27 support | ❌ Failed | ✅ Yes |
| Custom pak formats | ❌ No | ✅ Yes |
| GUI interface | ❌ No | ✅ Yes |
| JSON export | ❌ No | ✅ Yes |
| Asset preview | ❌ No | ✅ Yes |
| Search/filter | ❌ No | ✅ Yes |

---

## Troubleshooting

### "Failed to load pak file"
- Make sure you selected the correct game directory
- Verify UE version is set to GAME_UE4_27
- Try restarting FModel

### "Assets not showing"
- Check that the pak loaded (look for green checkmark)
- Try refreshing the file list (F5)
- Make sure filters aren't hiding files

### "Export failed"
- Make sure export directory exists and is writable
- Try exporting to a simpler path (e.g., C:\Temp)
- Check disk space (need at least 5GB free)

---

## Next Steps

1. ✅ FModel installed
2. ⏳ **Launch FModel** (use `launch_fmodel.bat`)
3. ⏳ Configure settings (game directory + UE4.27)
4. ⏳ Load Psychonauts2-WindowsNoEditor.pak
5. ⏳ Navigate to collectibles
6. ⏳ Export to JSON
7. ⏳ Parse with Python script
8. ⏳ Match with existing CSV data

---

**Ready to start!** Run `launch_fmodel.bat` to begin.
