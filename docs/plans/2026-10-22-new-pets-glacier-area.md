# PLAN (not built yet): 12 new pets + area 7 "Frostfall Glacier"

Agreed with the owner 2026-10-22. Nothing is in Studio yet. When the owner says to start, build in this order:
spec, concept sheet for the owner's OK, then pets in batches.

## The owner's decisions

- **ONE new area after Celestial**, with 6 pets.
- **+1 new pet in each existing area**, so every area has 6.
- The new pets are NOT all secrets. They are spread over the tiers: a new starter, mediums, highs, an ultra-rare and
  mythics.
- **Odds can go below 1%, minimum 0.1%.**
- **No second slingshot.** The runway simply extends past Celestial. Players reach the new area with more Slingshot
  Power levels (e.g. Lv 26-30+), with rebirth locks like the current levels; Robux +1 LV skips the lock.
- Total new pets: 12. Total in the game: 42 (7 areas × 6).

## Area 7: 🧊 FROSTFALL GLACIER, 🥚 Glacier Egg

Icy blue floors (eggs must stand out), blizzard-coloured waves, one trench, a VIP hideout, side decor only (lanes
clean, owner rule).

| Pet | Tier | Odds | Concept |
|---|---|---|---|
| Frostfang Lynx | Starter | 50% | Lean ice cat, frost-tufted ears, icicle claws |
| Ice Mammoth | Medium | 26% | Huge woolly brute, cracked ice tusks (remake the old unused IceMammoth in the FIERCE style) |
| Glacier Yeti | Big | 14% | Hunched snow beast, ice-plated arms, ground-slam act |
| Blizzard Roc | High | 7.4% | Giant white bird of prey, flies, frost trail from its wings |
| Permafrost Titan | Secret | 2.5% | Walking ice giant, glowing blue chest core, crystal crown |
| Absolute Zero Dragon | MYTHIC | 0.1% | Crystal-ice dragon, gold horn crown, frozen breath; the rarest pet in the game |

## +1 pet per existing area (new full odds tables, each sums to 100)

| Area / egg | New pet | Tier | New odds table |
|---|---|---|---|
| 🌿 Grass / Wood | **Bramble Badger** (thorn-backed angry badger) | Starter | Badger 40, Tortoise 30, Stag 16, Treant 8.5, Basilisk 3.5, Mantis 2 |
| 💧 Water / Tide | **Coral Crusher Crab** (giant armoured crab, coral-spiked claws) | Medium | Kappa 45, Turtle 25, Crab 15, Kraken 9, Hammerjaw 4.5, Orca 1.5 |
| ⚡ Thunder / Storm | **Volt Rhino** (charging rhino, lightning horn) | High | Raiju 50, Bull 25, Wyvern 14, Volt Rhino 6, Thunderbird 4, Thunder Rex 1 |
| 🔥 Fire / Magma | **Cinder Wyrm Overlord** (volcanic serpent dragon, obsidian crown) | Ultra-rare | Boar 53.5, Golem 27, Cerberus 13, Ivonrath 4, Phoenix 2, Wyrm 0.5 |
| 🌑 Shadow / Void | **Wraith Hound** (ghost hound, smoky mane, purple eyes) | Medium-high | Panther 50, Stallion 25, Wraith Hound 10, Black Dragon 9.5, Asparuh 4, Weaver 1.5 |
| ✨ Celestial | **Eclipse Seraph** (six-winged celestial lion-angel, eclipse halo) | Mythic | Solar Lion 54.9, Griffin 27, Celestial Dragon 13, Cvetibara 4, Leviathan 1, Seraph 0.1 |

## Money from rarity

The existing formula already handles odds below 1%: `rarityMult = max(1, (50 / odds%)^0.35)`.

| Odds | Money bonus |
|---|---|
| 40% | ×1 |
| 10% | ×1.8 |
| 2% | ×3.1 |
| 0.5% | ×5 |
| 0.1% | ×8.8 |

The area 7 base income continues the ×5.5 step: `AREA_INCOME[7]` ≈ $300K.

## Systems to touch

- **Pets:** `CreatureConfig` (odds per pet; secret / mythic flags), `IndexConfig` (6 cards per tab + a Glacier tab, bump
  `version`s, PORTRAITS), `IndexClient` (6-card layout).
- **Runway:** `EggSpawner` (KG tables for area 7), `WaveConfig` (runway end moves, waves start at the new end, a faster
  or new wave type for area 7), the AreaTitle banner, `Map.Bounds` + MapGuard, the end wall moves past area 7.
- **Progression:** `UpgradeConfig` (Slingshot Power levels to reach area 7, rebirth locks), `RebirthConfig` (Glacier
  pets in the top rebirth requirements), `SpeedStat` curve (beatable area 7 waves).
- **Other systems:** weather area lists, analytics Area Ladder, streak / starter pack / playtime pet pools (never
  secrets/mythics), ChatAnnounce (0.1% = always announce), CreatureVFX / PetEventFX.
- **Before any build:** re-run the economy simulators (`SLINGSHOT Creatures/economy/*.py`) and show the owner the
  pacing table.

## How to build the pets

The FIERCE pipeline: `PetsV3/FIERCE_GUIDE.md`, one `pets/<Name>.py` per pet, headless Blender.
1. Every model and its clips (idle, walk/fly/swim, roar, signature act) are approved by a reviewer subagent. Per the
   current memory rule: reviewers = Haiku, builders = Opus.
2. Animation references come from animationreference.org first.
3. Batches of about 4-6 pets, with a lineup screenshot to the owner after each batch.
4. Export to `C:\cdimp`, import with Keep Zero Influence Bones (creator ZAB Studio), PetSetup3, group-owned portraits
   via the FBX carrier.
5. Small VFX only.
6. Test on TestFreshSave. The owner does Save + Publish.

## Still open (ask the owner when starting)

- Final names OK?
- Frost theme OK, or a different zone theme?
- Extend rebirths past R20?
