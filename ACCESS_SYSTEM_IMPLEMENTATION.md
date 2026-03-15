# ACCESS SYSTEM IMPLEMENTATION GUIDE
# Psychonauts 2 Archipelago Randomizer

## CORRECTED ACCESS SYSTEM

### Overview
ALL locations are LOCKED by default except Collective Unconscious.
Access items are RANDOMIZED in the item pool (not tied to specific locations).

### Starting Inventory
Player starts with:
- 1x Physical Area Access (random: Motherlobe/QA/Quarry/GNG)
- 1x Mental World Access (random: one of 12 mental worlds)
- Collective Unconscious (always unlocked, no item needed)

### Access Items to Add

#### Physical Area Access (4 items)
1. Motherlobe Access - Also unlocks Sasha's Lab
2. Questionable Area Access - Also unlocks Forgetful Forest  
3. Quarry Access
4. Green Needle Gulch Access

#### Mental World Access (12 items)
5. Brain Tumbler Access
6. Hollis' Classroom Access
7. Hollis' Hot Streak Access
8. Compton's Cookoff Access
9. Bob's Bottles Access
10. Cassie's Collection Access
11. Ford's Lucktopus Access
12. Ford's Fractured Mind Access
13. Gristol's Mind Access
14. Fatherland Follies Access
15. Strike City Access
16. Cruller's Correspondence Access

#### Special Access (1 item - EVENT BASED)
17. Maligula Access - Unlocked by event/story requirements, NOT randomized in pool

Total: 17 access items (16 randomized + 1 event)


## ITEM ID ASSIGNMENTS

### Physical Area Access
- Motherlobe Access: 300_000_001
- Questionable Area Access: 300_000_002
- Quarry Access: 300_000_003
- Green Needle Gulch Access: 300_000_004

### Mental World Access
- Brain Tumbler Access: 300_001_001
- Hollis' Classroom Access: 300_001_002
- Hollis' Hot Streak Access: 300_001_003
- Compton's Cookoff Access: 300_001_004
- Bob's Bottles Access: 300_001_005
- Cassie's Collection Access: 300_001_006
- Ford's Lucktopus Access: 300_001_007
- Ford's Fractured Mind Access: 300_001_008
- Gristol's Mind Access: 300_001_009
- Fatherland Follies Access: 300_001_010
- Strike City Access: 300_001_011
- Cruller's Correspondence Access: 300_001_012

### Special
- Maligula Access: 300_002_001

## PYTHON RANDOMIZER CHANGES

### 1. Update Psychonauts_2_Item_List.csv

Add these rows to the CSV:

Access_Motherlobe,Motherlobe Access,Archipelago,Progression,1
Access_QuestionableArea,Questionable Area Access,Archipelago,Progression,1
Access_Quarry,Quarry Access,Archipelago,Progression,1
Access_GreenNeedleGulch,Green Needle Gulch Access,Archipelago,Progression,1
Access_BrainTumbler,Brain Tumbler Access,Archipelago,Progression,1
Access_HollisClassroom,Hollis' Classroom Access,Archipelago,Progression,1
Access_HollisHotStreak,Hollis' Hot Streak Access,Archipelago,Progression,1
Access_ComptonsCookoff,Compton's Cookoff Access,Archipelago,Progression,1
Access_BobsBottles,Bob's Bottles Access,Archipelago,Progression,1
Access_CassiesCollection,Cassie's Collection Access,Archipelago,Progression,1
Access_FordsLucktopus,Ford's Lucktopus Access,Archipelago,Progression,1
Access_FordsFracturedMind,Ford's Fractured Mind Access,Archipelago,Progression,1
Access_GristolsMind,Gristol's Mind Access,Archipelago,Progression,1
Access_FatherlandFollies,Fatherland Follies Access,Archipelago,Progression,1
Access_StrikeCity,Strike City Access,Archipelago,Progression,1
Access_CrullersCorrespondence,Cruller's Correspondence Access,Archipelago,Progression,1
Access_Maligula,Maligula Access,Event,Progression,1

### 2. Update items.py

Add to item_name_to_id dictionary:
    # Physical area access
    'Access_Motherlobe': 300_000_001,
    'Access_QuestionableArea': 300_000_002,
    'Access_Quarry': 300_000_003,
    'Access_GreenNeedleGulch': 300_000_004,
    
    # Mental world access
    'Access_BrainTumbler': 300_001_001,
    'Access_HollisClassroom': 300_001_002,
    'Access_HollisHotStreak': 300_001_003,
    'Access_ComptonsCookoff': 300_001_004,
    'Access_BobsBottles': 300_001_005,
    'Access_CassiesCollection': 300_001_006,
    'Access_FordsLucktopus': 300_001_007,
    'Access_FordsFracturedMind': 300_001_008,
    'Access_GristolsMind': 300_001_009,
    'Access_FatherlandFollies': 300_001_010,
    'Access_StrikeCity': 300_001_011,
    'Access_CrullersCorrespondence': 300_001_012,
    
    # Special
    'Access_Maligula': 300_002_001,

### 3. Update options.py

Add new options for starting areas:

class StartingPhysicalArea(Choice):
    display_name = 'Starting Physical Area'
    option_random = 0
    option_motherlobe = 1
    option_questionable_area = 2
    option_quarry = 3
    option_green_needle_gulch = 4
    default = 0

class StartingMentalWorld(Choice):
    display_name = 'Starting Mental World'
    option_random = 0
    option_brain_tumbler = 1
    option_hollis_classroom = 2
    option_hollis_hot_streak = 3
    option_comptons_cookoff = 4
    option_bobs_bottles = 5
    option_cassies_collection = 6
    option_fords_lucktopus = 7
    option_fords_fractured_mind = 8
    option_gristols_mind = 9
    option_fatherland_follies = 10
    option_strike_city = 11
    option_crullers_correspondence = 12
    default = 0

### 4. Update __init__.py

In create_items():

    # Determine starting access items
    physical_areas = ['Access_Motherlobe', 'Access_QuestionableArea', 'Access_Quarry', 'Access_GreenNeedleGulch']
    mental_worlds = ['Access_BrainTumbler', 'Access_HollisClassroom', 'Access_HollisHotStreak',
                     'Access_ComptonsCookoff', 'Access_BobsBottles', 'Access_CassiesCollection',
                     'Access_FordsLucktopus', 'Access_FordsFracturedMind', 'Access_GristolsMind',
                     'Access_FatherlandFollies', 'Access_StrikeCity', 'Access_CrullersCorrespondence']
    
    # Select starting physical area
    if self.options.starting_physical_area == 0:  # Random
        starting_physical = self.random.choice(physical_areas)
    else:
        starting_physical = physical_areas[self.options.starting_physical_area.value - 1]
    
    # Select starting mental world
    if self.options.starting_mental_world == 0:  # Random
        starting_mental = self.random.choice(mental_worlds)
    else:
        starting_mental = mental_worlds[self.options.starting_mental_world.value - 1]
    
    # Add to starting inventory
    self.multiworld.push_precollected(self.create_item(starting_physical))
    self.multiworld.push_precollected(self.create_item(starting_mental))
    
    # Add remaining access items to pool
    all_access_items = physical_areas + mental_worlds
    for access_item in all_access_items:
        if access_item not in [starting_physical, starting_mental]:
            self.multiworld.itempool.append(self.create_item(access_item))
    
    # Note: Maligula Access is NOT added to pool - it's granted by event

### 5. Update rules.py

Add access requirements for all locations:

    # Physical area access
    for loc in world.get_region('Motherlobe').locations:
        add_rule(loc, lambda state: state.has('Access_Motherlobe', world.player))
    
    for loc in world.get_region('Sasha_Lab').locations:
        add_rule(loc, lambda state: state.has('Access_Motherlobe', world.player))  # Linked to Motherlobe
    
    for loc in world.get_region('Questionable_Area').locations:
        add_rule(loc, lambda state: state.has('Access_QuestionableArea', world.player))
    
    for loc in world.get_region('Forgetful_Forest').locations:
        add_rule(loc, lambda state: state.has('Access_QuestionableArea', world.player))  # Linked to QA
    
    for loc in world.get_region('Quarry').locations:
        add_rule(loc, lambda state: state.has('Access_Quarry', world.player))
    
    for loc in world.get_region('Green_Needle_Gulch').locations:
        add_rule(loc, lambda state: state.has('Access_GreenNeedleGulch', world.player))
    
    # Collective Unconscious - NO ACCESS REQUIRED (always available)
    # No rules needed for CU locations
    
    # Mental world access
    for loc in world.get_region('Brain_Tumbler').locations:
        add_rule(loc, lambda state: state.has('Access_BrainTumbler', world.player))
    
    for loc in world.get_region('Hollis_Classroom').locations:
        add_rule(loc, lambda state: state.has('Access_HollisClassroom', world.player))
    
    # ... Continue for all 12 mental worlds ...
    
    # Maligula's Mind - Special event-based access
    for loc in world.get_region('Maligula_Mind').locations:
        add_rule(loc, lambda state: state.has('Access_Maligula', world.player))

## UE4 MOD CHANGES

### Update FastTravelManager.cpp

In InitializeDestinations():

ALL destinations should start LOCKED except Collective Unconscious.

Physical areas:
- Motherlobe (requires Motherlobe Access)
- Sasha's Lab (requires Motherlobe Access - same as Motherlobe)
- Questionable Area (requires QA Access)
- Forgetful Forest (requires QA Access - same as QA)
- Quarry (requires Quarry Access)
- Green Needle Gulch (requires GNG Access)

Mental worlds (all require their own access item):
- Brain Tumbler, Hollis' Classroom, Hollis' Hot Streak, etc.

Special:
- Collective Unconscious (NO ACCESS REQUIRED - always unlocked)
- Maligula's Mind (requires Maligula Access from event)

In OnItemReceived():

    // Physical area access
    if (ItemId == 300_000_001) { // Motherlobe Access
        UnlockDestination('Motherlobe');
        UnlockDestination('SashaLab');  // Also unlock Sasha's Lab
    }
    else if (ItemId == 300_000_002) { // Questionable Area Access
        UnlockDestination('QuestionableArea');
        UnlockDestination('ForgetfulForest');  // Also unlock Forgetful Forest
    }
    else if (ItemId == 300_000_003) { // Quarry Access
        UnlockDestination('Quarry');
    }
    else if (ItemId == 300_000_004) { // Green Needle Gulch Access
        UnlockDestination('GreenNeedleGulch');
    }
    // Mental world access
    else if (ItemId == 300_001_001) { UnlockDestination('BrainTumbler'); }
    else if (ItemId == 300_001_002) { UnlockDestination('HollisClassroom'); }
    else if (ItemId == 300_001_003) { UnlockDestination('HollisHotStreak'); }
    else if (ItemId == 300_001_004) { UnlockDestination('ComptonsCookoff'); }
    else if (ItemId == 300_001_005) { UnlockDestination('BobsBottles'); }
    else if (ItemId == 300_001_006) { UnlockDestination('CassiesCollection'); }
    else if (ItemId == 300_001_007) { UnlockDestination('FordsLucktopus'); }
    else if (ItemId == 300_001_008) { UnlockDestination('FordsFracturedMind'); }
    else if (ItemId == 300_001_009) { UnlockDestination('GristolsMind'); }
    else if (ItemId == 300_001_010) { UnlockDestination('FatherlandFollies'); }
    else if (ItemId == 300_001_011) { UnlockDestination('StrikeCity'); }
    else if (ItemId == 300_001_012) { UnlockDestination('CrullersCorrespondence'); }
    // Special
    else if (ItemId == 300_002_001) { UnlockDestination('MalikulasMind'); }

## TESTING CHECKLIST

- [ ] Player starts with exactly 1 physical area unlocked
- [ ] Player starts with exactly 1 mental world unlocked
- [ ] Collective Unconscious is always available
- [ ] All other locations start LOCKED
- [ ] Receiving Motherlobe Access unlocks both Motherlobe AND Sasha's Lab
- [ ] Receiving QA Access unlocks both Questionable Area AND Forgetful Forest
- [ ] Each access item unlocks the correct destination
- [ ] Fast travel menu shows only unlocked destinations
- [ ] Maligula Access is granted by event, not found in pool
- [ ] Save/load preserves unlock state

## IMPLEMENTATION SUMMARY

This system ensures:
✅ No locations accessible without finding their access item
✅ Prevents early sequence breaks
✅ Creates meaningful progression through finding access items
✅ Starting inventory guarantees at least 2 explorable areas
✅ Linked unlocks (Motherlobe→Sasha's Lab, QA→Forgetful Forest) reduce busywork
✅ Maligula access controlled by story progression
✅ Collective Unconscious always available as hub

