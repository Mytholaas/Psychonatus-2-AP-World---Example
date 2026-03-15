# Psychonauts 2 Archipelago - Complete Integration Guide

## Overview

This repository contains a **complete Archipelago randomizer implementation** for Psychonauts 2, consisting of:

1. **Python Randomizer** (`Psychonauts-2-AP-World---Example/worlds/psychonauts2/`) - Logic, rules, and multiworld server integration
2. **UE4 Game Mod** (`Psychonauts2-AP-Mod/`) - In-game implementation with floor modifications and server communication

Both components work together seamlessly to provide full Archipelago randomizer functionality.

## Quick Start

### For Players
1. Install Archipelago client from https://archipelago.gg
2. Extract UE4 mod to `Psychonauts2/Psychonauts2/Plugins/Psychonauts2AP/`
3. Generate world with `archipelago generate` using Psychonauts2.yaml
4. Connect in-game via Main Menu → Archipelago Settings

### For Developers
1. Python: Edit `worlds/psychonauts2/*.py` files, test with pytest
2. UE4: Open `Psychonauts2AP.sln`, build in Visual Studio
3. Test: Run AP server + launch game with mod installed

## Key Integration Points

- **CSV Data** defines item/location IDs used by both Python and UE4
- **Python Randomizer** generates logic and communicates via AP server
- **UE4 Mod** implements floor modifications, fast travel access, and item tracking
- **WebSocket** (port 38281) synchronizes state between components

## Access System

**All locations are LOCKED by default** except Collective Unconscious.

**Starting Inventory**:
- 1x Random Physical Area Access (Motherlobe/QA/Quarry/GNG)
- 1x Random Mental World Access (one of 12)
- Collective Unconscious (always unlocked)

**Access Items** (17 total):
- 4 Physical Area Access items
- 12 Mental World Access items
- 1 Special (Maligula Access - event-based)

See `ACCESS_SYSTEM_IMPLEMENTATION.md` for detailed implementation guide.

## Documentation

- [Python Randomizer](Psychonauts-2-AP-World---Example/README.md)
- [UE4 Mod](Psychonauts2-AP-Mod/README.md)
- [Access System Implementation](ACCESS_SYSTEM_IMPLEMENTATION.md)
- [Access System Quick Reference](ACCESS_SYSTEM_QUICKREF.md)
