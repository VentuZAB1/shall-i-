# SLINGSHOT hub makeover: FINAL (2026-10-22, ~00:20 local)

**State:** built in the owner's open Studio. Studio ends in **Edit** with **TestFreshSave = false**.

The place is **not saved and not published**. The owner does Save, Publish and Migrate. The full ledger is in `progress.md`, the design in `DESIGN.md`, and every shot in `shots/`.

## What changed

- **Rule #1: no trees, bushes, flowers or benches.**
  - These are gone from the hub: the trees, benches, permanent garden, gate beds, alley bed, backdrop island + tree, Halloween garden, 16 small spiders, and the 8 lamp posts.
  - All of them sit in `ServerStorage._Backup_HubMakeover.Before.Removed`.
- **Placements snapped:**
  - Upgrade / Sell stalls square to the front wall, counters +Z, rings mirror-exact at (±70, -48.36) on their decks.
  - 4 boards in the inward 45° arena around the chest at (±26, 3 / 37), each now double-sided (`<Board>_Back`).
  - Free Gift chest + pad ring at (0, 20).
  - Spawn moved out of the chest to (0, 52).
- **Walls:** 13 new wall models (`Map.Hub.Walls.E1..E13`, 189 parts):
  - base band, studded recessed panel, cream coping at **22.4**
  - pillars, corner pilasters, 2 runway-junction towers
- **Ground:**
  - warm mid-tan paving (tone C)
  - subtle lanes with edge lines, gate aprons, 3-wide wall aprons, low plot kerbs
  - medallion recoloured
- **Wall decor (the only decor besides the floor pumpkins), one feature per bay, mirror-symmetric:**
  - the 2 pumpkin **hands** (VineGrip) on the back coping under the giant head
  - **12 garlands** in alternating bays
  - 3 static **bat** flocks
  - 4 corner **webs**, each with one of the 4 big spiders on it
  - **8 wall lanterns** (cage + pumpkin + iron bracket) on mirror-pair pillars
- **Floor:** 5 pumpkin clusters at the wall foot: the alley end, the two runway junctions, the two corridor ends.

## Before / after (same fixed cameras)

| Camera | Before | After |
|---|---|---|
| C1 top | `shots/before_01_top.jpg` | `shots/after_01_top.jpg` |
| C2 runway | `shots/before_02_front.jpg` | `shots/after_02_runway.jpg` |
| C3 chest | `shots/before_03_chest.jpg` | `shots/after_03_chest.jpg` |
| C4 Upgrade | `shots/before_04_upgrade.jpg` | `shots/after_04_upgrade.jpg` |
| C5 Sell | `shots/before_05_sell.jpg` | `shots/after_05_sell.jpg` |
| C6 gate 1 | `shots/before_06_gate1.jpg` | `shots/after_06_gate1.jpg` |
| C7 gate 3 | `shots/before_07_gate3.jpg` | `shots/after_07_gate3.jpg` |
| C8 boards | `shots/before_08_boards.jpg` | `shots/after_08_boards.jpg` |
| C9 hero | `shots/before_09_hero.jpg` | `shots/after_09_hero.jpg` |
| C10 alley | `shots/before_10_alley.jpg` | `shots/after_10_alley.jpg` |
| C11 corridor | `shots/before_11_corridor.jpg` | `shots/after_11_corridor.jpg` |
| Night | `../build/final_plaza_night.png` (render; a night "before" needs a Play client, so none was taken in Stage A) | `shots/final_night_C10_alley.jpg`, `final_night_C2_runway.jpg`, `final_night_C9_hero.jpg`, `final_night_junction.jpg` (Play client, Settings night) |

Per-pass shots, including the rejected tries: `shots/p1_*` … `shots/p6_*`.

## Tests (one Play session, TestFreshSave true -> false)

| Test | Result |
|---|---|
| T11.1 placements, walls, lanterns, pumpkins, budget, Validate | **16/16** |
| T11.2 avenue walker, gate 1 -> 6 -> 1 along z -30 (+ client window monitor) | **2/2**; closest 12.2 outside a ring; no window opened |
| Stall rings: step on -> own window | **2/2** |
| Free Gift zone opens the window; FREE! sign + sparkles off once claimed | **2/2** (see note 1) |
| T11.3 pathfinding from the Spawn: 6 gates, 6 plots, rings, chest, alley end, corridor ends, slingshot | **19/19** |
| T10.11 boards drew Row01 (8/8), FREE! anchor over the chest, 16 lantern lights at night values | **3/3** |
| Night switch: 8 pumpkin lights to night range and back | **8/8** |
| T11.4 walls hold (push + jump, no escape over or through, not stuck) | first run 3 fail / 3 pass (test bug, note 2); ad-hoc re-run with the fixed limit **5/5** on 5 walls |
| HubV2Kit.Validate (live) | **0 fails** |
| Layout tool `hub_layout.py` | **ALL PASS (75)** |
| Output | **0 errors** server + client (CorePackages noise excluded) |

Notes:

1. **Free Gift first entry.** The first entry, teleported straight from the Sell ring into the chest zone in one step, did not open the window. Re-entry did. The client logic is unchanged, and the case can't happen on foot (about 97 studs apart). Flagged, not fixed.
2. **T11.4 limit.** The limit was the floor edge, but the panel sits 0.8 behind it. The fixed limits (+2 extra walls) are saved in T11.4, but that edited version has **not yet been run** as T11.4.
3. **Checked statically, not in Play:**
   - intro cameras (Validate 7)
   - launch zone (Validate 4)
   - Trailer S10 sight line: crosses at y 40-48, and the walls are now lower than designed
   - tutorial stall targets (zone names unchanged)

## Part count

- Workspace: **4,662** parts. That was 4,824 before the makeover and 5,142 at its peak (pass 4). The budget is 11,000.
- Map.Hub 2,476; HalloweenDecor 93.
- Bats: 12 (≤ 16).
- Every new piece is anchored. Decor is no-collide, no-query, no-touch.

## Rulings (details + cost-if-wrong in `progress.md`)

1. "Pumpkin hands" = the VineGrip on the back wall; garlands as well (review note 1).
2. Owner rule #1 cancels the corner-trees allowance; every tree, bush, flower and bench is removed.
3. Stalls face +Z, square to the walls.
4. Stall rings stay at the owner's corners, fully on their decks (proven by the avenue walker).
5. Sell ring + zone moved 1.13 so the stalls mirror exactly.
6. Boards keep the inward arena and become double-sided.
7. Front boards at x ±26 (intro camera clearance).
8. Spawn moved to (0, 52).
9. Lamps become 8 wall lanterns.
10. The FreeGift pad ring keeps its pivot rotation (it was stood up once, then fixed).
11. Wall coping 22.4, not 25.6 (R5 plot A/B; the giant head's grin clears the wall).
12. Paving tone C, warm mid-tan (A/B/C at C8).
13. Garlands alternate: 39 -> 21 -> 18 -> **12**. Even bays, skipping the bays that already hold a web or a lantern, so each bay has one feature and the pattern stays mirror-symmetric (A/B at C2/C9/C10/C11).
14. Lanterns hang lower (arm 16) to clear the garland hooks and the hands; corridor-end lanterns sit on the pilaster legs.
15. Hands scaled 0.9 about their grip.
16. The 4 big spiders sit flat on the webs with BobAmp 0 (their bob axis now points into the wall). HalloweenClient is unchanged.
17. Revert rehearsed as a **dry run** (every step resolves, problems: none), not a real round trip at night.

## Revert

`ServerStorage._Backup_HubMakeover.Before.Revert`. The README holds the two command-bar lines, dry run first.

- It restores: names, CFrames (91 snapshots), 71 removed or moved instances, colours / BobAmp / collisions, and the 3 scripts.
- It destroys the 31 makeover-built instances.
- The builders `HubV2Kit.Makeover.Walls / Ground / WallDecor` can rebuild any one layer on its own.

## Fix round (2026-10-22, 00:25-01:12): VISUAL_REVIEW.md "FIX THEN SHIP"

All 5 MUSTs and all 3 SHOULDs are applied. The details, numbers and rulings are in `progress.md`, under "Fix round".

### MUSTs

- **M1, wall palette** (3 measured tries; `review/M1_*`; `tools/measure.py`, the review's crops):
  - Final palette: panel (128,138,162), pillar / base (98,104,124), cap (244,190,138), foot (66,68,92). It is also saved in the `Makeover.Walls` builder.
  - The coping renders H39 warm sandstone; it was H180 cyan.
  - The pillars render R 65 / 31 (was 18 / 1) with S ≤ 0.63, and sit 0.13-0.16 L darker than the panel.
  - The panel is 0.01-0.02 outside its L/S window (L 0.59 near, S 0.51 far). Ruling: no single colour fits both distances.
- **M2:** an orange `Cornice` (214,112,44) on all 13 edges, built by the builder. The webs and spiders sit 1.0 lower.
- **M3:** **38 pumpkin finials**. Ruling: all of them, not every other; the A/B at C2/C10/C11/R03 shows gaps read busier (`review/M3_*`). The room-corner finials sit on the pilaster caps.
- **M4:** SlotBed → (100,148,66) in `BaseBuilder` line 16 (backed up first, in Revert) and on the 6 live beds. It renders H96-99 S0.41-0.49 L0.58-0.60, and the plot grass stays brighter.
- **M5:** the junction bat flocks are re-centred (x ∓95.5, squeezed 0.65) and mirror-exact. They clear the tower by 2.19 and the pillar by 2.14.

### SHOULDs

- **12 gate clusters**, each a small pumpkin + candles (1.50 tall, mirror-exact, no candle lights). Validate 21 caps them at 1.6.
- **Junction towers** rise to 40 (the runway-wall top), with a finial on top.
- **8 finial PointLights**, only on the long dark runs. They are night-boosted by attribute; no script change, nothing doubled. There are 27 lights in HalloweenDecor in total.

### Closed in Play (TestFreshSave true → false)

| Check | Result |
|---|---|
| T11.4 walls (the saved version) | **10/10** |
| T11.1 | **16/16** |
| T10.11 | **3/3** |
| Tutorial steps 8 / 9 / 10 on plot 1 + plot 6 | Arrows point to the Upgrade ring, then the own treadmill (B1 / B6), then Upgrade (or the pad with no money): **6/6** |
| Intro freezes (13 times) | No hub solid near or ahead of the lens; the puppet is clear. The owner's boards appear in the background (ruling: they're not blocking) |
| Slingshot launch (real Space hold/release) | Camera-to-player line never crossed (0/56); landed z -160 |
| Trailer S10 | Lens-to-pumpkin clear 7/7; the pumpkin centred over the back wall |
| Free Gift teleport | **Not reproduced**: the window opens in the same frame. No change |
| Night | 8/8 finial lights boost |
| Logs | 0 errors |

**Part count:** 4,737 (budget 11,000). **Validate:** 0 fails. **Revert dry run:** no problems.

**Shots:** `shots/fix_01_top` … `fix_11_corridor` (pairs with `after_01` … `after_11`), plus night `fix_night_C10_alley / C2_runway / junction / C11_corridor` (pairs with `final_night_*`). The Play checks are in `fix_intro_*`, `fix_sling_landing`, `fix_trailer_s10_*` and `fix_tut_step8_plot1/6`.

### NICE: skipped, still open

1. Studded outer faces + a FOOT-colour skirt from y -8 to 0 (outside / trailer views).
2. Lane rhythm: terracotta diamond inlays every 12 studs, or a darker "worn stone" lane fill.
3. A VineGrip pair on the front walls E1:3 / E13:3 (A/B only).
4. The orange runway-wall end faces: a DARK base band plus a sandstone cap line.

## Test-order fix (2026-10-22 ~01:20-01:45)

This is a test-only fix: `HubV2Tests` changed, and no game script was touched. The pre-fix copy is in `_Backup_HubMakeover.Before.TestFixBackup`.

- **T11.2 failed in a full run.** T10.5 leaves the player welded to their treadmill, so the walker couldn't move.
  - New `dismount()` (it drops the weld; TreadmillServer then cleans up by itself), used by every `put()`.
  - New `settle()` before T11.1 / T11.2: dismount, the T10.5 tier put back, standing still on the ground, out of every trigger zone so the windows close.
- **T11.1 was 15/1 on reruns.** The old `put()` teleported the welded character, which dragged the Treadmill_B1 model across the map (Validate 12). That can't happen any more.
- **T10.4b needed the client "Equip Best".** T10.4 now does it itself, through the save + `HatcheryDebug reload` (BaseHatchery's own loadBase / fitSlots path).
- T10.4b now puts back Rebirths / the save / the inventories it changed, so T10.1 "every base 40 x 40" holds on a rerun.

| Full hub suite (T2, T10, T11; 12 sections) | Result |
|---|---|
| Run 1, fresh TestFreshSave session | **110 / 0** |
| Run 2, new fresh TestFreshSave session | **110 / 0** |
| Bonus: run 3, same session as run 2 (the old 15/1 case) | **110 / 0** |
| Errors | 0 |

After every run, Treadmill_B1 is back on tier 1 at its layout pivot, with Rebirths 0.

## Owner round (2026-10-22 morning): grime, chest, tutorial, intro

### What the owner changed on the map (kept exactly as placed, never re-mirrored)
1. **Treadmill_B1 / B6** moved from the front corner (±107.7, -46) to the plaza side next to the plot: (-103.65, 0.65, -14.54) facing +X / (105.65, 0.65, -14.54) facing -X.
2. **UpgradeSign_B1 / B6** moved from (±116, -57) to (-109.91, 3.18, -4.89) / (113.91, 3.18, -4.89).
3. **The 4 spoke lanes lengthened at their gate end:** P2 +1, P5 +2, P3 +6, P4 +3 studs (edge lines resized to match).

The Layout (+ `tools/hub_layout.py`), the Ground builder (`OWNER_LANES`) and Validate now expect these. Validate: 0 fails; the layout tool: ALL PASS. The owner's left / right values aren't exact mirrors; they are kept as placed.

### A. Grime (only moss, cracks, drips, floor stains): `workspace.HalloweenDecor.Grime`, 118 carriers
- Wall-foot moss on all 41 bays, below the orange cornice; mirrored A / B pattern.
- 20 sun-facing runs tinted (the sun lesson).
- 18 wall cracks / drips (9 mirror pairs), all ≥ 3.5 from spiders / webs and clear of garlands, hands, bats and lanterns.
- 18 floor decals (9 mirror pairs), validated against every keep-clear zone.
- Builder: `HubV2Kit.Makeover.Grime`. Shots: `shots/grime_day_*` (11 fixed cameras + 4 close-ups), `shots/grime_night_*`.

### B. The chest has no collision
- All 28 `FreeGift.Chest` parts are CanCollide false (originals kept in `_MakeoverOrigCollide`).
- Play: you walk straight through it. The claim window, the FREE! sign and the pad ring still work.

### C. Tutorial
- Plots 1 and 6 re-run on PC: every arrow lands, and every target is reachable, including the owner's new treadmill spot (walk on from the back / sides / gate).
- Phone fix: while any window is open (menu windows or the walk-in Upgrade / Sell / Gift / Offline), the guide text leaves the screen, so the window keeps its FULL size (step 11 Rebirth window = the no-tutorial size). The window's own arrows stay visible, and the guide comes back on close.
- MenuController's step-11 "plain fit" is neutralised by the new `GuideHidesForWindows` attribute (kept as a fallback for an old TutorialClient). BrickUI.Hatch `guideClear` does the same.
- Phone scale was checked at the logic level, not on an emulated phone (no Studio UI clicking). Worth a look in Test > Device.
- Shots: `tut_step8/10/11_*`.

### D. Intro cutscene
- Shot 2 (the side dolly) used to start with the lens at the edge of the Top Time board and the front boards filling up to 22% of the frame. It is now `p + (10, 1.5, 7)`, FOV 55: 0% boards, lens ≥ 3.2 from any board, subject on the left third, slingshot right.
- The skid shot (6-11% boards) is now `(p.X + 13, 3.2, p.Z + 9)`, FOV 54: 0% boards.
- The arena backdrop behind WHEW (boards 4-10%, symmetric) is kept on purpose.
- No camera in walls, 0 errors. `INTRO_CAMS` updated in the layout tool + Layout.
- Frames: `shots/intro_t*` (each stage, WHEW 24.8, handover 27.5).

### Tests
- Full HubV2Tests: **110 / 0** (fresh TestFreshSave session, 0 server errors).
- Workspace 4,855 parts. Bats 12.
- Studio ends in Edit with TestFreshSave false.
- Backups: `_Backup_HubMakeover.Before.OwnerRound1022` (TutorialClient, MenuController, IntroCutscene, BrickUI.Hatch).

## Owner to do

1. Look at the hub in Studio.
2. **Save, Publish, Migrate** (servers still run the old hub).
3. Optional: decide on the NICE items above.
