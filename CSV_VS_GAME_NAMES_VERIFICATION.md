# Psychonauts 2 - CSV vs Game Class Name Verification

## ⚠️ CRITICAL FINDING

**Your CSV files use CUSTOM naming conventions, NOT the actual in-game blueprint class names!**

---

## Comparison

### Your CSV Format (Simplified)
```
ML_PsiCard1
ML_PsiCard2
ML_Figment1
BOBZ_Nugget1
CASS_Figment1
```

### Actual Game Class Names (From FModel Extraction)
```
PKUP_Exp_PSIChallengeCard
PKUP_Figment
PKUP_Figment_CASS
PKUP_BOBZ_Nugget
PKUP_CASS_Nugget
PKUP_HalfAMind
PKUP_BagTag_Base
```

---

## Found Game Pickup Classes

### Nuggets of Wisdom (Level-Specific)
- `PKUP_BOBZ_Nugget` - Bobby Z's Nugget
- `PKUP_CASS_Nugget` - Cassie's Nugget  
- `PKUP_COMP_Nugget` - Compton's Nugget
- `PKUP_FORB_Nugget` - Ford's Brain Nugget (Part B?)
- `PKUP_FORC_Nugget` - Ford's Brain Nugget (Part C?)
- `PKUP_FORH_Nugget` - Ford's Brain Nugget (Part H?)
- `PKUP_GRIS_Nugget` - Gristol's Nugget
- `PKUP_HELM_Nugget` - Helmut's Nugget
- `PKUP_HOLL_Nugget` - Hollis's Nugget
- `PKUP_LOBO_Nugget` - Loboto's Nugget
- `PKUP_MALI_Nugget` - Mailroom Nugget

### Figments (Level-Specific)
- `PKUP_Figment` - Base/Generic Figment
- `PKUP_Figment_CASS` - Cassie's Figments
- `PKUP_Figment_CASS_Book` - Cassie Book Figment (special)
- `PKUP_Figment_COMPT` - Compton's Figments
- `PKUP_Figment_FORB` - Ford Brain Figments
- `PKUP_Figment_GRIS` - Gristol's Figments  
- `PKUP_Figment_HELM` - Helmut's Figments
- `PKUP_Figment_HOLL` - Hollis's Figments
- `PKUP_Figment_LOBO` - Loboto's Figments
- `PKUP_Figment_MALI` - Mailroom Figments

### Psi Cards
- `PKUP_Exp_PSIChallengeCard` - Psi Challenge Cards (all of them use this base class)
- `PKUP_Exp_PSIChallengeMarker` - Psi Challenge Marker

### Emotional Baggage
- `PKUP_BagTag_Base` - Base Bag Tag
- `PKUP_BagTag_DuffleBag` - Duffle Bag Tag
- `PKUP_BagTag_DuffleBag_CASS` - Cassie's Duffle Bag Tag
- `PKUP_BagTag_HatBox` - Hat Box Tag
- `PKUP_BagTag_HatBox_CASS` - Cassie's Hat Box Tag
- `PKUP_BagTag_Purse` - Purse Tag
- `PKUP_BagTag_SteamerTrunk` - Steamer Trunk Tag
- `PKUP_BagTag_Suitcase` - Suitcase Tag

### Half-A-Minds
- `PKUP_HalfAMind` - Standard Half-A-Mind
- `PKUP_HalfAMind_HELM` - Helmut-specific Half-A-Mind

### Other Pickups (Reference)
- `PKUP_Health_Small` - Small Health Pickup
- `PKUP_Health_Med` - Medium Health Pickup
- `PKUP_Health_Large` - Large Health Pickup
- `PKUP_Consumable_BitOfFluff` - Dream Fluff
- `PKUP_Ammo_PsiBlast` - Psi Blast Ammo
- `PKUP_PSIMoney_Base` - Psitanium (currency)

---

## Level Code Mapping

| CSV Code | Game Code | Level Name |
|----------|-----------|------------|
| ML | HQIN | Motherlobe/HQ Interior |
| BOBZ | BOBZ | Bob's Bottles |
| CASS | CASS | Cassie's Collection |
| COMP | COMP/COMPT | Compton's Cookout |
| FORB/FORC/FORH | FORB/FORC/FORH | Ford's Brain Parts |
| GRIS | GRIS | Gristol's Brain |
| HELM | HELM | Helmut's Brain |
| HOLL | HOLL | Hollis's Brain |
| LOBO | LOBO | Loboto's Labyrinth |
| MALI | MALI | Mailroom |

---

## The Problem

Your CSV has entries like:
```csv
ML_PsiCard1,Motherlobe Psi Card 1
ML_PsiCard2,Motherlobe Psi Card 2
```

But the **actual game** doesn't have individual `ML_PsiCard1`, `ML_PsiCard2` classes!

Instead, all Psi Cards use the same base class: **`PKUP_Exp_PSIChallengeCard`**

Individual cards are differentiated by:
1. **Level placement** (which map they're in)
2. **Actor instance name** in the level
3. **Properties/IDs** in the instance data

---

## What This Means for Your AP Mod

### Current Situation:
Your CSV uses simplified, human-readable names that don't match the game's blueprint class structure.

### Two Possibilities:

**1. The AP Mod Uses Custom Mapping (Likely)**
- The mod might have its own internal ID system
- It maps `ML_PsiCard1` → actual collectible by location/index
- The CSV is just for organization, not direct game integration

**2. The Names Need to Be Updated (If Mod Uses Direct Matching)**
- CSV should reference actual blueprint classes: `PKUP_Exp_PSIChallengeCard`
- Would need additional data (level, instance ID) to distinguish individual items

---

## Verification Needed

To verify if names matter, check:

1. **Your AP mod code** (`worlds/psychonauts2/` Python files)
   - How does it reference items?
   - Does it use the CSV "Item" column directly?
   - Or does it have a separate mapping system?

2. **Game integration** 
   - Does the mod inject code that looks for `ML_PsiCard1`?
   - Or does it track by location + collectible type?

---

## Recommendation

**Option A:** If the mod works currently:
- The CSV names are likely just internal identifiers
- No changes needed - the mod has its own mapping logic

**Option B:** If you need exact game class matching:
- Update CSV to use: `PKUP_Exp_PSIChallengeCard`, `PKUP_Figment_CASS`, etc.
- Add columns for: Level, Instance Index, Actor Name
- Create proper mapping between AP items and game blueprints

---

## Files to Check

Look at these files in your repository to understand the mapping:
- `worlds/psychonauts2/__init__.py` - Main world logic  
- `worlds/psychonauts2/items.py` - Item definitions
- `worlds/psychonauts2/locations.py` - Location/check definitions  
- `worlds/psychonauts2/regions.py` - Region/level definitions

These will show you HOW the CSV data is actually used by the AP mod.

---

**SUMMARY:**  
✅ Extracted actual game class names from pak file  
⚠️ Your CSV uses custom simplified names, NOT game class names  
❓ Need to check AP mod code to see if this is intentional or a problem  

---

**Created:** Based on FModel extraction of Psychonauts2-WindowsNoEditor.pak  
**Source:** `Psychonauts2/Content/Gameplay/Pickups/` folder
