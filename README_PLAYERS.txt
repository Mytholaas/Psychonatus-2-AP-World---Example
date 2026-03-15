# 🎮 Psychonauts 2 Archipelago - Player Installation Guide

Welcome! This package contains everything you need to start playing Psychonauts 2 with Archipelago.

## 📦 What's Included

- **psychonauts2.apworld** - The Psychonauts 2 world file for Archipelago
- **Psychonauts2_Player.yaml** - Your player configuration template
- **This file** - Installation instructions

## ⚡ Quick Start (5 Minutes)

### Step 1: Install Archipelago

1. Download Archipelago from https://archipelago.gg
2. Install it (recommended location: `C:\ProgramData\Archipelago`)
3. Run the Archipelago Launcher once to set up

### Step 2: Install the Psychonauts 2 World

**Option A: Double-Click Installation (Easiest)**
1. Double-click `psychonauts2.apworld`
2. It will automatically install to your Archipelago custom worlds folder
3. You're done! Skip to Step 3.

**Option B: Manual Installation**
1. Open your Archipelago installation folder
2. Navigate to `lib\worlds\` (or `custom_worlds\` depending on version)
3. Copy `psychonauts2.apworld` into this folder
4. Done!

### Step 3: Configure Your Player Settings

1. Open `Psychonauts2_Player.yaml` in a text editor (Notepad, VS Code, etc.)
2. Change the following:
   ```yaml
   name: Player1          # ← Change to your name
   ```
3. Choose your win condition:
   ```yaml
   win_condition: normal  # Options: normal, all_bosses, all_scav_hunt, scav_hunt_and_maligula
   ```
4. Choose your starting outfit:
   ```yaml
   starting_outfit: normal_outfit  # Options: normal_outfit, tried_and_true, circus_skivvies, suit
   ```
5. Decide on shop items:
   ```yaml
   include_shop_items: true  # true = 607 locations, false = 559 locations
   ```
6. Save the file

### Step 4: Generate Your Seed

1. Copy your edited `Psychonauts2_Player.yaml` to Archipelago's `Players` folder
   - Usually: `C:\ProgramData\Archipelago\Players\`
2. Run **ArchipelagoGenerate.exe** (or use the Launcher)
3. Your seed will be created in the `output` folder!

### Step 5: Host or Join a Game

**To Host:**
1. Run **ArchipelagoServer.exe**
2. Select your generated `.archipelago` file from the `output` folder
3. Share your server address (e.g., `localhost:38281`) with other players

**To Join:**
1. Get the server address from your host
2. You'll connect using the game mod (coming soon!)

## 🎯 Win Conditions Explained

| Option | What You Need to Do |
|--------|---------------------|
| **normal** | Get core abilities, unlock key areas, defeat Maligula |
| **all_bosses** | Get all 8 psychic abilities, complete 4 boss worlds, defeat Maligula |
| **all_scav_hunt** | Collect all 16 scavenger hunt items (game ends immediately - no boss!) |
| **scav_hunt_and_maligula** | Collect all 16 scavenger items to unlock Maligula, then defeat her |

### Which Should I Choose?

- **New to randomizers?** → `normal` (balanced difficulty)
- **Want a challenge?** → `all_bosses` (must complete more content)
- **Love collecting?** → `all_scav_hunt` (no boss fight required)
- **Want both?** → `scav_hunt_and_maligula` (collection + boss)

## 🎨 Starting Outfits

You can choose which outfit Raz starts with. The other 3 will be randomized!

- **normal_outfit** - Default Psychonauts 2 look
- **tried_and_true** - Classic Psychonauts 1 outfit (nostalgia!)
- **circus_skivvies** - Circus performance costume
- **suit** - Sharp formal suit

## 🛍️ Shop Items Option

**include_shop_items: true** (Recommended)
- All 48 shop locations are randomized
- Shop items can appear anywhere in the world
- 607 total location checks
- More variety and challenge

**include_shop_items: false**
- Shop items stay in their normal locations
- You'll still visit shops to get vanilla items
- 559 total location checks
- Slightly shorter game

## 🎲 Playing with Friends (Multiworld)

To play with friends in different games:

1. Each player creates their own YAML file with their game choice
2. Name each file differently: `Alice.yaml`, `Bob.yaml`, etc.
3. Put all YAMLs in the `Players` folder together
4. Generate the seed - it creates one `.archipelago` file for everyone
5. Host the server and everyone connects!

Example:
- Alice plays Psychonauts 2 (your YAML)
- Bob plays A Link to the Past (his YAML)
- When Alice finds checks, Bob might get items and vice versa!

## ⚙️ Advanced Options

### Death Link
```yaml
death_link: true  # When you die, your multiworld partners die too (and vice versa!)
```
Only enable if you want extra challenge and coordination!

### Progression Balancing
```yaml
progression_balancing: 50  # 0-99, higher = more of your items stay in your world
```
- 0 = Your items are likely in other players' worlds
- 99 = Your items are likely in your world
- 50 = Balanced (recommended)

### Start Inventory
```yaml
start_inventory:
  Progressive Telekinesis: 1  # Start with Telekinesis already unlocked
  Smelling Salts: 5           # Start with 5 Smelling Salts
```

### Local/Non-Local Items
```yaml
local_items:
  - Progressive Levitation     # This will ALWAYS be in your world
  
non_local_items:
  - Progressive Time Bubble    # This will NEVER be in your world
```

## 🐛 Troubleshooting

### "The world 'Psychonauts 2' is not recognized"
- Make sure `psychonauts2.apworld` is in the correct folder
- Try restarting Archipelago
- Check that the file isn't corrupted (re-download if needed)

### "Failed to generate seed"
- Open your YAML and check for typos
- Make sure indentation is correct (use spaces, not tabs)
- Verify all option names are spelled correctly

### "No module named 'worlds.psychonauts2'"
- The .apworld file needs to be installed
- Try Option B (manual installation) from Step 2

## 📝 Example YAML

Here's a complete example for a player named "Raz" who wants a challenging run:

```yaml
name: Raz
game: Psychonauts 2

Psychonauts 2:
  win_condition: all_bosses
  starting_outfit: tried_and_true
  include_shop_items: true
  death_link: false

accessibility: locations
progression_balancing: 50
```

## 🎮 Game Mod Status

**Important**: The Psychonauts 2 game mod is currently in development.

- ✅ The world file (this package) is COMPLETE and generates seeds
- ⚠️ The in-game mod is being worked on
- 📅 Estimated completion: 4-6 months

You can generate seeds NOW and be ready to play when the mod releases!

## 🔗 Helpful Links

- **Archipelago Website**: https://archipelago.gg
- **Archipelago Discord**: https://discord.gg/archipelago
- **Setup Tutorial**: https://archipelago.gg/tutorial/
- **Psychonauts 2**: https://www.doublefine.com/games/psychonauts-2

## 📞 Need Help?

- Join the Archipelago Discord: https://discord.gg/archipelago
- Ask in the #psychonauts-2 channel
- Check the Archipelago setup guide
- Read the troubleshooting section above

## 🎉 You're Ready!

That's it! You now have:
- ✅ Psychonauts 2 world installed
- ✅ Player YAML configured
- ✅ Knowledge of all options
- ✅ Ability to generate seeds

Generate your first seed and get ready for an amazing randomized adventure through the minds of Psychonauts 2!

Happy randomizing! 🧠✨

---

**Version**: 1.0
**Last Updated**: 2026
**Supported Archipelago Version**: 0.4.0+

