# QUICK REFERENCE: Access System Changes

## Key Changes from Original Design

### BEFORE (Incorrect):
- Locations unlocked by default or through story
- Green Needle Gulch was the only special unlock
- No starting area randomization

### AFTER (Correct):
- **ALL locations LOCKED by default** (except Collective Unconscious)
- **17 Access Items** added to randomizer
- **Starting inventory**: 1 physical area + 1 mental world (randomized)

## Access Items Summary

**Physical Areas (4)**:
1. Motherlobe Access (also → Sasha's Lab)
2. Questionable Area Access (also → Forgetful Forest)
3. Quarry Access
4. Green Needle Gulch Access

**Mental Worlds (12)**:
5-16. One access item for each of 12 mental worlds

**Special (1)**:
17. Maligula Access (event-based, NOT in random pool)

## Item ID Ranges

- Physical Access: 300_000_001 to 300_000_004
- Mental Access: 300_001_001 to 300_001_012
- Special Access: 300_002_001

## Starting Inventory Logic

Player ALWAYS starts with:
- Collective Unconscious (no item needed)
- 1x Random Physical Area Access
- 1x Random Mental World Access

This guarantees 3 explorable areas from the start.

## Files That Need Updates

### Python Randomizer:
- ✅ Psychonauts_2_Item_List.csv (add 17 access items)
- ✅ items.py (add item IDs)
- ✅ options.py (add starting area options)
- ✅ __init__.py (add starting inventory logic)
- ✅ rules.py (add access requirements to all locations)

### UE4 Mod:
- ✅ FastTravelManager.cpp (update InitializeDestinations & OnItemReceived)
- ✅ FastTravelManager.h (update item ID constants)

See ACCESS_SYSTEM_IMPLEMENTATION.md for detailed code changes.
