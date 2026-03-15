# UE4 Mod Requirements for Psychonauts 2 Archipelago

## CRITICAL: Collective Unconscious Accessibility

### Problem
Collective Unconscious lacks walkable floors to all mental world doors.
Without Mental Connection, players cannot reach doors → SOFTLOCK.

### Solution Required in UE4 Mod
Add walkable floor paths connecting spawn to all 13 mental world doors.

### Implementation Options

**Option 1: Invisible Floor Meshes (Recommended)**
- Spawn invisible collision meshes in CU
- Create paths from spawn to each door
- Add safety net below
- Natural gameplay feel

**Option 2: Enable Flight in CU**
- Modify player movement when in CU
- Easier implementation
- Less natural feel

### Mental World Doors (13)
1. Loboto's Labyrinth
2. Hollis Classroom
3. Hollis Hot Streak
4. Compton's Cookoff
5. Psi King's Sensorium
6. Ford's Follicles
7. Strike City
8. Cruller's Correspondence
9. Tomb of the Sharkophagus
10. Bob's Bottles
11. Cassie's Collection
12. Lucrecia's Lament
13. Fatherland Follies

### Python Randomizer Status
✓ CSV data verified - no Mental Connection required for access
✓ 96 checks correctly use Mental Connection for collectibles
✓ No softlocks in randomizer logic

### UE4 Mod Status  
⚠️ Specification created
⚠️ Implementation required
⚠️ Testing needed

### Priority: CRITICAL
Without this change, randomizer can create unwinnable seeds.

### References
- UE4_MOD_SPECIFICATION.txt (detailed spec)
- PSI_CARD_CU_VERIFICATION.md (verification report)
