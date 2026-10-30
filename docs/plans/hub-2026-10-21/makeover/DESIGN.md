# SLINGSHOT hub makeover: design (Stage A, 2026-10-21 night)

**Status (2026-10-22): BUILT.** Approved and built in Stage B, tested in Stage C. See `FINAL.md`. The build differs from this design in the places below. Each change has a ruling in `progress.md`.
- Walls: coping top **22.4** (panel 20.8, pillars 25.2, towers 30.2), not 25.6.
- Paving: **tone C**, warm mid-tan (172,144,108); lanes (188,162,124); edges (136,106,76).
- Garlands: **12**, not 39. Alternating bays, mirror-symmetric, one feature per bay.
- Hands: scaled 0.9 about their grip.
- Bats: 3 flocks of 4, each on its own clean panel.
- Wall pumpkins: **5** clusters on the floor: the alley end (0,164), the junctions (±88,-55) and the corridor ends (±209,6).
- 4 big spiders: on the 4 corner webs.
- Lanterns: cage at y 13.7 (arm at 16). The corridor-end pair hangs on the E2/E12 pilaster legs at z 9.95.

**Original status:** design only, waiting for review. In Studio I only took screenshots and cleared the editor Selection (the owner had `Map.Bounds` selected, and its gizmo showed in the captures).

**Files:**
- Plan picture: `plan_annotated.png`. It is drawn over the real top-down capture; north (top) is the runway, -Z.
- Numbers: `plan.json`, made by `tools/makeover_plan.py` (`python makeover_plan.py`).
- Before shots: `shots/before_*.jpg`.
- Ledger: `progress.md`.

## Rule #1 (owner, 2026-10-21, overrides everything looser)

> "Very important is to be GOOD/BEAUTIFUL, but NOT DECORATION WITH TREES / BUSHES AND SEATS, they are useless, now we
> use small decorations such as on walls and on the ground etc."

- **No trees, bushes, flowers, shrubs or benches anywhere in the hub.**
  - This includes the backdrop-island tree.
  - All of them move to `ServerStorage._Backup_HubMakeover.Before`.
- **Beauty comes only from:**
  - the walls themselves: pillars, coping, base band, two tones, studs
  - small decor ON the walls: garlands, the pumpkin hands, a few bats, lanterns, corner webs
  - small decor ON the ground: paving, lanes, the medallion ring, kerbs, pumpkin clusters at the wall foot
- **Also from the owner:**
  - "Decoration can ruin everything."
  - Big walls on all sides, with the pumpkin hands on them.
  - Fix the example placements and their rotations.

## 0. What I found (before)

- **Walls:** the hub edge is a 4-stud kerb wall, so the world just stops at the sky (`before_02_front`, `before_09_hero`).
- **Clutter:** 117 parts of bushes and trees, 6 gate flower beds, a planted alley strip, 4 benches, 8 lamp posts, and 12 Halloween garden spots with dead trees. They are spread over the plaza and the plot gaps (`before_01_top`, `before_06_gate1`, `before_11_corridor`).
- **Owner's examples:**
  - The stalls are toed in about 12°, and so are their decks.
  - The FREE! zone and sign are still at (0,56), 36 studs behind the chest (`before_10_alley`).
  - The spawn point is inside the chest.
- **"Pumpkin hands":** I read this as the **VineGrip**, not the garlands. `Halloween/Vines/NOTES.md` describes it as "giant pumpkin-vine 'fingers' gripping the back wall".
  - The old hub had `VineGrip_L` / `VineGrip_R` on its back wall, under the giant head. They are in `_Backup_Hub.Before.HalloweenDecor.Vines`.
  - The garlands go up as well, so both readings are covered.
  - **Reviewer:** please confirm this reading.

## 1. Snapped placements (pass 1)

Each pair is an exact mirror, uses whole studs, and has rotations in 45° steps. "Front" means the side the players use.

| Item | Now (owner example) | New | How I found its front |
|---|---|---|---|
| **UpgradeStall** | pivot (-69.8,1.0,-51.0), rotY -167.6 | Plinth centre (-70, 0.95, -54), rotY 180, so the counter faces +Z (the plaza) | The pivot LookVector (0.21,0,0.98) equals the counter's; the Emblem (stall icon) sits on that side, and the ring is 5.63 in front of the plinth, centred. The sign is double-sided (SurfaceGui Front + Back). |
| **SellStall** | (69.8,0.9,-50.3), rotY 167.5 | (70, 0.95, -54), rotY 180 | Same check: its ring is 4.50 in front. **Ruling:** move the Sell PadRing + SellZone 1.13 forward to 5.63 so both stalls are exact mirrors. |
| Upgrade / Sell rings | (-68.6,-45.5) / (68.8,-45.9) | (-70, -48.37) / (70, -48.37) | Each zone stays on its own ring. |
| **LeftMarket / RightMarket** decks (24×24) | rotY ∓77.6 (crooked) | Centre (∓70, 0.3, -47.6), rotY 0 | Square to the front wall. The back trim edge is flush with the wall line z -60, and the deck is centred on the orange runway-wall end (x ±60..80). |
| **RichestBoard** (blue) | (-22.7, 10.2, 1.5), rotY -135 | (-26, *keep y*, 3), rotY -135 | The screen is the SurfaceGui Face Front on `Cube.056`; its LookVector is the model LookVector. Checked in the captures: from the chest you read the screens (`before_03_chest`), and the back is a blank panel (`before_08b_board_back`). |
| **TimeBoard** (green) | (25.2, 10.2, 3.7), rotY 135 | (26, y, 3), rotY 135 | Same. |
| **SpeedBoard** (blue) | (-23.5, 10.2, 37.1), rotY -45 | (-26, y, 37), rotY -45 | Same. |
| **HeaviestBoard** (green) | (23.9, 10.2, 36.1), rotY 45 | (26, y, 37), rotY 45 | Same. |
| **Chest** | (0.2, 1.8, 19.9), rotY 0 | (0, 1.8, 20), rotY 0 | The front faces -Z, toward the slingshot. The Lock and Keyhole parts are on the z-min side. |
| **PadRing** | (-0.53, 0.39, 20.36), rotY -115 | (0, 0.39, 20), rotY 0 | It is a ring, so its rotation does not matter. |
| **FreeGiftZone** + FREE! sign + sparkles | (0, 0.6, 56) | (0, 0.95, 20) | This is exactly what `FreeGiftServer` does at run time (pad Fill + 0.6). The sign sits 6.8 above the chest, 2.4 over the lid. |
| **Spawn** | (0, -0.4, 20), inside the chest | (0, -0.4, 52), rotY 0 (faces -Z) | It is open floor behind the back board gap, on the spine lane. It only matters for a player's first frame (`BaseManager.spawnAtBase` moves them to their gate), for MapGuard's fallback and for players without a plot. |

**Leaderboards**
- **The arena is kept.** The 4 boards stand at the diagonals around the chest, all facing it, as the owner placed them.
- They sit on a 52×34 rectangle, 1-3 studs from the owner's spots, with the owner's 45° steps.
- **Double-sided:** every board gets a back screen so the walking lines outside the ring also read a board.
  - The back screen is a model `<Board>_Back` in `Leaderboards` that holds a clone of the screen part `Cube.056` and its SurfaceGui.
  - It is flipped 180° and sits flush on the board's blank back panel (I'll find the panel by raycast).
  - It carries the same `Leaderboard` attribute.
  - `ServerScriptService.Leaderboards` draws every model with that attribute, and `LeaderboardScroll` scans the folder children, so **no script change** is needed.
  - Cost: 4 parts and 4 SurfaceGuis.
- **The front pair moves 1-3 studs wider, to x ±26,** so the IntroCutscene side-dolly camera keeps 3.8+ studs from the TimeBoard.
  - That camera runs x 18→13.5, z 2→-24 and always looks away toward -X-Z.
  - The owner's example was a similar 3.5.

## 2. Big walls on all sides (pass 2)

The walls follow the unchanged floor outline: 13 edges and 14 vertices (`plan.json` → edges). They are built **outside** the floor edge.

**Nothing intrudes into the walkable floor below y 24**, except the pillar faces, which stand 0.1 in.
- This matters because plots 1/6 have a side on the E1/E13 line itself.
- The `Map.Bounds` columns (2..6 outside the edge) end up inside the wall body.
- `Map.Bounds` and `MapGuard` are unchanged.

**Wall section** (d = distance outward from the floor edge):

| Part | d | y | Colour | Notes |
|---|---|---|---|---|
| Base band (wainscot) | 0 .. 6.6 | 0 .. 3.6 | DARK (58,84,130) | Flush with the floor edge; the "base trim". |
| Panel | 0.8 .. 6.8 | 3.6 .. 24 | BODY (96,132,170) | Recessed 0.8, Plastic, **studs on the inner face**. Same blue family as the old big walls the owner asked for. |
| Coping | 0.4 .. 7.4 | 24 .. 25.6 | CAP (232,222,196) | Warm cream, ties in with the paving; it draws a clean line against the sky. |
| Pillar | 4 wide, -0.1 .. 6.6 | 0 .. 27.2 | DARK | Stands 0.9 proud of the panels and rises 1.6 above the coping. |
| Pillar cap | 5 wide, -0.5 .. 7.2 | 27.2 .. 28.4 | CAP | |
| Pillar foot | 5 wide, -0.1 .. 6.6 | 0 .. 2 | FOOT (46,66,104) | |
| Runway-junction towers | at (±81,-60) | rise to 32 | | Step from the 25.6 hub wall up toward the 40-tall orange runway wall. They frame the runway mouth, which stays fully open (x -59..59). |

**Corners**
- **Inside (room) corners:** an L of two pilaster pieces.
- **Outside (reflex) corners**, at (±183,12) and (±73,78): one 4×4 block that wraps the corner.
- **E1/E13:** run to x ±80 so they close against the runway wall (today there is a 1-stud gap at x ±80..81).

**Parts, collision and lighting**
- About 165 parts, all anchored, CanCollide on.
- **CastShadow off.** This follows the owner's "fewer shadows" pick (`_HadShadow`). The darker base band and the ground apron give the contact line.
- There are no WallCaps: 25.6 is far above the about 7-stud jump.

**Rhythm:** 42 pillars, one at every vertex plus even bays per edge. The left side is listed below; E8–E13 mirror E6–E1.

| Edge | Length | Bays × width | Where |
|---|---|---|---|
| E1 / E13 | 134 | 5 × 26.8 | Front, beside the runway mouth (plot 1/6 side + the plaza's front corners) |
| E2 / E12 | 72 | 3 × 24 | Behind plots 1/6 |
| E3 / E11 | 32 | 1 × 32 | Corridor end between plots 1-2 / 5-6 |
| E4 / E10 | 66 | 2 × 33 | Behind plots 2/5 |
| E5 / E9 | 110 | 4 × 27.5 | Beside plots 2/5 |
| E6 / E8 | 93 | 3 × 31 | Beside plots 3/4 |
| E7 | 146 | 5 × 29.2 | Back wall, under the giant pumpkin |

## 3. Wall decor (pass 4)

Seasonal items go in `HalloweenDecor.WallDecor`; anything permanent is called out in the list. Everything is anchored with CanCollide, CanQuery and CanTouch off.

- **Pumpkin HANDS:** the 2 VineGrip models (cloned from the backup), in E7 bays 2 and 4 at x ±29.2.
  - They flank the alley-end bay, right under the head (head x -54..54, front bulge at z 175 above y 50).
  - They grip the coping's inner edge (y 25.6), as their frame expects.
  - If the leaves clip the pillar caps, I scale them to 0.9.
- **Garlands:** one in **every bay except the 2 hand bays**, 39 in total. Each hooks onto the **front faces of its two pillars**.
  - Scale = (span/2 − 0.4)/13, so 0.89 (24-wide bays) to 1.24 (33-wide bays).
  - The hooks hang at y 21, and every garland in the hub hangs at the same height.
- **Bats:** 12 flat wall bats in 3 loose flocks of 4 (the static posed meshes; no Animator).
  - E7 alley-end bay, E1 bay 1 and E13 bay 5 (the plaza's front corners).
- **Lanterns:** the 8 night-boost lamps, on 8 pillars, in symmetric pairs. Details are in §5.
- **Corner webs:** 4 webs with 4 spiders, at the inside corners (±183,78) and (±73,171), near the top.
  - The other 16 spiders go to the backup.

## 4. Ground (pass 3)

- **Paving:** the 3 Ground tiles change from glaring cream (222,205,170) to **warm sandstone (212,190,152)**, still studded. I'll take an A/B shot before choosing the final tone.
- **Two-tone lanes:** light paving (230,214,180) with a 0.8 edge line (176,146,110), flat at top y 0.06.
  - **Spine** (x 0, 14 wide): pad front z -38 → medallion, then medallion → the back wall at the alley end. It carries the main axis: runway → slingshot → chest → alley → hands → head.
  - **Front avenue** (z -30, 10 wide): from gate 1 to gate 6. It runs along the stall decks and stays clear of the boards (21+), the treadmills (0.6+) and the pad.
  - **4 spokes** (8 wide): from the medallion's side and back gaps to the gate aprons of plots 2/5 and 3/4. They keep 2.3+ studs from every board corner.
- **Gate aprons:** 6 aprons, 16×10, in front of each plot gate. Each one holds the spawn spot (8 out from the gate).
- **Wall apron:** a 3-wide band (186,158,120) along every wall foot. Behind plots it fills exactly the 3-stud strip up to the slot.
- **Plot kerbs:** a raised kerb (156,128,96), 1.2 wide and 0.25 tall (walkable), around each 60×90 slot.
  - Only on the plaza-facing sides: not on sides within 3.5 studs of a wall.
  - The front kerb leaves a 14-wide gap at the gate.
  - The kerbs are hub parts under `Map.Hub.Decor.Ground`, **not inside Base/Plot**. `Plot.Look` stays untouched and skin-ready, and the rebirth fences are untouched.
- **Medallion:** the same 5 discs at (0,20), recoloured. The outer band is terracotta (150,96,64) at r 25.9, and the boards stand just outside it (28.9).
- **Pumpkin-egg clusters:** 5 of the 6 live clusters move to the wall foot.
  - One centred at the alley end (0,164), between the hands and under the head.
  - Two beside the junction towers at (±90,-56), clear of the decks and the plot 1/6 treadmills.
  - Two at the corridor ends (±209,6).
  - Cluster #6 goes to the backup.

## 5. Lamps (pass 6)

- **The 8 lamps become wall lanterns:**
  - the permanent `Cage` and `Bulb` with their lights
  - a 2-part dark-iron bracket
  - the Halloween `StreetLamp` pumpkin inside the cage
- **Where:** at about y 14 on the pillars at
  - the alley end (±14.6,171)
  - the reflex corners (±73,78), on a 45° bracket into the nook
  - the junction towers (±81,-60), by the stalls
  - the corridor-end corners (±215,12)
- **Night boost:** the boost keys on the lights' `NightBrightness` / `NightRange` attributes inside `HalloweenDecor`, wherever they are. So `HalloweenClient` needs **no change**.
- **Moved to the backup:** the 18.6-tall posts and the lamp webs.

## 6. What leaves the hub (pass 5)

Everything listed is moved, not deleted, to `ServerStorage._Backup_HubMakeover.Before.Removed`. Each item is saved with:
- an `_From` attribute holding its original parent path
- an `_Tags` attribute, and its tags stripped
- its scripts disabled

| Removed | Notes |
|---|---|
| `Map.Hub.Decor` Trees | 6 |
| `Map.Hub.Decor` Benches | 4 |
| `Map.Hub.Decor` Garden | 12 clusters |
| `Map.Hub.Decor` GateBeds | 6 |
| `Map.Hub.Decor` AlleyBed | Soil strip + 11 plants |
| `Map.Hub.Decor` Backdrop | Floating island + GiantTree; it would sit inside the new back wall anyway |
| `Map.Hub.Decor` Lamps posts | 8 |
| `Map.Hub.EdgeWalls` | Replaced by the new walls |
| `HalloweenDecor.Garden` | Dead / TP / haunted trees, bushes, graves, dead grass |
| `HalloweenDecor.Spiders` | 16 of the 20 |
| `HalloweenDecor.StreetLamps` webs | 16 parts |
| PumpkinEggs cluster #6 | |

**Stays:** the Plaza medallion, MarketCorners, the stalls, the boards, the FreeGift, the treadmills, the signs, the plots, the GiantPumpkin, the slingshot, LaunchPlatform and the runway.

**Net parts:** about -60 (≈ +450 / -510), so the hub stays well under the 11,000 budget (8,477 at 6×R4).
- Hub parts outside the plots today: 760 → about 650.
- `HalloweenDecor` today: 189 → about 180.

## 7. Risks and how each is covered

| Risk | Detail | How it is covered |
|---|---|---|
| **Tutorial** | It finds `UpgradeZone`, the own `Plot.Floor`, `Treadmill_B<id>.Belt` and the slingshot at run time; there are no hub coordinates in TutorialClient. | Stage C re-runs the step 8/9/10 target checks on plots 1 and 6. |
| **Intro** | Its stage is hard-coded around (−16..18, −40..5). | Flat lanes only there. The front boards are the only tall things nearby (3.8+ studs, never in frame). Stage C: IntroDebugT freezes at 0.5 / 2.0 / 2.8 / 3.5 / gate / outro (lens → puppet clear), and the FINISH takeover stands. |
| **Stall rings on walking lines** | With the owner's front-corner stalls, the Upgrade/Sell rings sit on the gate-edge → plot 1/2 (and 5/6) fan lines, so a walk-through briefly opens the window (it closes at 8 studs). No corner spot avoids this. | **Ruling:** keep the owner's spot. The validator rule becomes "the ring is fully on its deck" for the stalls. |
| **MapGuard** | | Stage C: jump at every edge (no climb), teleport 2 studs outside each edge (put back), nobody stuck between pillars and fences at R5. The pillars stand only 0.1 into the floor; the strip behind a plot is ≥ 2.9. |
| **Launch path** | Nothing new in LAUNCH_ZONE except the flat lane. The walls are at \|x\| ≥ 81. | Stage C: launch from the pad and check the flight. |
| **Trailer S10** | The glide's line of sight to the pumpkin crosses the back wall at y 40-48 (wall top 25.6). | Stage C: rerun the "lens → pumpkin clear" sample. |
| **Leaderboards** | 8 models with attributes. | Stage C: 8 screens draw Row01. |
| **Tooling** | `HubV2Kit.Layout` / `hub_layout.py` still hold the pre-owner positions, and `Validate` checks 9/11/15/19/21 assume the old edge walls and the density rule. | Pass 1 updates the layout tool → Lua → Layout. Validate: new wall check, back screens allowed, stall-ring rule, density → anti-clutter ("nothing taller than 1.5 freestanding on the open plaza except the functional models"). HubV2Tests gets the new Stage C checks. |
| **Hand edits** | | Tests check rules, not decor spots. |

## 8. Build passes (Stage B), each followed by the fixed cameras

1. Snap and rotate the placements; fix the zone and spawn; add the back screens; update the layout tool and Validate.
2. Walls.
3. Ground.
4. Wall decor.
5. Clear the clutter.
6. Lamps.

**Fixed cameras (position → look at):**

| Cam | Position | Look at |
|---|---|---|
| C1 top | (0,210,56.5) | (0,0,55) |
| C2 runway | (0,55,-150) | (0,0,45) |
| C3 chest | (0,6,-4) | (0,4,30) |
| C4 Upgrade | (-48,9,-24) | (-70,5,-50) |
| C5 Sell | (48,9,-24) | (70,5,-50) |
| C6 gate 1 | (-88,9,-14) | (-124,4,-32) |
| C7 gate 3 | (-22,9,46) | (-42,4,82) |
| C8 boards | (0,30,-30) | (0,6,22) |
| C9 hero | (-170,110,-150) | (0,0,40) |
| C10 alley | (0,8,40) | (0,16,171) |
| C11 corridor | (-62,12,-8) | (-215,8,8) |

**Night:** from a Play client using the Settings Day/Night switch.

**Stage C:** all listed tests, with TestFreshSave set true before and false after every Play session.

## 9. Revert

- **Before each pass I save:**
  - every model I move, with its CFrame, as a `CFrameValue` under `_Backup_HubMakeover.Before.CFrames`, named by full path
  - every script I change, disabled, under `.Scripts`
  - every removed item under `.Removed`, with `_From` / `_Tags`
- **New parts** carry the attribute `_Makeover = true`.
- **One-step revert:** `require(game.ServerStorage["_Backup_HubMakeover.Before"].Revert:Clone())()` in Edit. It:
  1. destroys every `_Makeover` instance
  2. moves each `Removed` item back to `_From` and re-adds its tags
  3. restores every CFrame, including the old EdgeWalls
  4. puts the original scripts back
- The revert is rehearsed once at the end of Stage B.
