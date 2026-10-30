# Permafrost Titan - model notes (MODEL GATE, 2026-10-27)

Glacier egg, SECRET 2.5 %. Plan: `_review/PermafrostTitan_plan.md` v2, hero = **option A, the GOLD CHEST BEZEL** (owner decision).
File: `pets/PermafrostTitan.py` (model + rig + check_pairs + joints; no clips yet).

## FINAL 8.5 ROUND 6 (2026-10-28, after `_review/PermafrostTitan_final85_r6.md`, model 8.4) - re-exported 09:17
Backups:
- the round-5 export: `_scratch/PermafrostTitan_exported_r5.py`
- this export: `_scratch/PermafrostTitan_exported_r6.py`
- **MD-A, stacked bands:** the chest/waist seam (Chest, z 1.165) goes JOINT_D -> **MAUVE**. Geometry and collisions are
  unchanged. From the front the chest and waist now read as one mass (`renders/_roar_front_sheet.png` f0, `_model_sheet`).
- **MD-B, fresh evidence from the current build:**
  - `_icons_strip_64` / `_128`, `_icons2_strip_64` / `_128` and `_close_sheet` are re-made (09:18). The crust plates
    show at 64 px.
  - Kit gold counter (`_tools/game_icon.py`): portrait **49**, game **27** (gate >= 25 / >= 20).
  - Stale sheets (`_clip_sheet_v1`, `_cv_kneel_*`, `_kneel_close_f40`, `_under_sheet`) moved to
    `_scratch/stale_r6_renders/`.
- **Step 1** (`_scratch/export_r6.txt`): collision_free **true**; tris 7,820; FBX `C:\cdimp\PermafrostTitan.fbx` 09:17.

## FINAL 8.5 ROUND 5 (2026-10-28, after `_review/PermafrostTitan_final85_r5.md`, model 8.4) - re-exported 08:24
Backups:
- before this round: `_scratch/PermafrostTitan_pre_r5.py`
- this export: `_scratch/PermafrostTitan_exported_r5.py`

The patch is `_scratch/fix_r5.py`.
- **MD1, head:** skull half-width **0.160 -> 0.172**; the head is now 0.344 BU wide.
  - The face X offsets are scaled by `HX = 1.075`: brow halves (0.070), eye hits (0.078), cheeks (0.148), jaw half-width
    (0.120), cavity (0.086), lip (0.088).
  - Head pitch is unchanged; collision-free.
- **MD2, crusts -> two solid plates:**
  - Upper pauldron: 3 broken blocks -> **2 plates**: (L 0.17, w 0.080) and (L 0.13, w 0.076).
  - Fist knuckles: 3 -> **2 plates** (L 0.12, w 0.076, laid more forward over the knuckles).
  - `ice_chunk` half-sizes are (w, 0.8 w, L / 2), so the smallest half-size of every new plate is >= 0.06.
  - The lower pauldron keeps its single chunk at the round-4 size. Enlarging it pushed tris 64 over the +200 cap.
  - Tris: **7,820** (+156 vs 7,664; cap +200). The bigger plates cut more faces where they sink into the
    pauldron / fist, so two big plates cost more than three small ones (`_scratch/tris_by_bone.py`).
- **MC4', mouth (model part):** cavity **(10, 10, 14)** + an upper lip on the skull (MAUVE, 0.012 proud of the cavity front, hidden inside the closed jaw).
  - `renders/_roar_jaw_close.png` f27 front: the cavity renders **(79, 81, 84), luma ~81** (round 4: 88). The lit
    slate brow is luma 135.
  - The kit shader's sheen floor (roughness 0.42) keeps a dark face near luma 75-85. It cannot reach < 60 here, so per
    the review this item needs the Studio check.
- **Step 1** (`_scratch/export_r5.txt`): collision_free **true**; tris 7,820; FBX `C:\cdimp\PermafrostTitan.fbx` 08:24.

## FINAL 8.5 ROUND 4 (2026-10-28, after `_review/PermafrostTitan_final85_r4.md`, model 8.3) - re-exported 05:11
Backup of the round-3 export: `_scratch/PermafrostTitan_exported_r3.py`; this export: `_scratch/PermafrostTitan_exported_r4.py`.
- **MM1, waist:** the waist block's bottom taper goes from 0.95 to **0.86**, so the waist narrows into the belt.
  - The belt seam is tucked to match: (0.262, 0.19) -> **(0.248, 0.178)** half-extents.
  - It now sits as a step between the waist base (0.225 x 0.163) and the hip top (0.27 x 0.21).
  - The hip plates (outer x 0.272, top z 1.005) stay flush below the seam (z 1.01-1.05).
  - `renders/_model_sheet.png` (05:05).
- **MC4, mouth:** the jaw cavity colour is now **(24, 26, 34)**, near-black and neutral; it was JOINT_D (52, 60, 84).
  - Measured in `renders/_roar_jaw_close.png`, front, f27: the cavity renders **(85, 88, 95)**.
  - The lit slate brow renders (133, 143, 170), so the cavity is about 38 % darker (luma 88 vs 143) and no longer blue.
  - The kit shader (roughness 0.42) lifts dark faces, so it reads as dark grey here; Studio's true colour will be darker.
- **Step 1** (`_scratch/export_r4.txt`):
  - collision_free **true**; ground_min_z 0 on idle / walk / roar and **-0.017** on the act (f20).
  - Linear 0; loops 0 / 0; slide 0.0; idle foot drift 0.
  - Tris **7,664**; Lua 32,186 bytes; stride 0.6452.
  - FBX `C:\cdimp\PermafrostTitan.fbx` (05:11).

## FINAL 8.5 ROUND 3 (2026-10-28, after `_review/PermafrostTitan_final85_r3.md`, model 8.0) - re-exported 04:21
Backup of the round-2 export: `_scratch/PermafrostTitan_exported_r2.py`.
- **M1, knee:** the shin starts exactly at the thigh's knee width (`SW, SD = TW * TT, TD * TT`, no +0.006 calf). The knee
  cap centre is at `-(SD - 0.012)`, so it sits 0.008 proud.
- **M2, belt:** the JOINT_D belt is now a seam, half-height **0.02** (was 0.04); width 0.262 and depth 0.19 are unchanged.
- **Gold at 64 px, measured with both tools on the same icons (`_scratch/gold_windows_r3.txt`):**

  | tool / window | portrait | game |
  |---|---|---|
  | kit counter (`_tools/game_icon.py`) | **52** | **27** |
  | `gold_cmp.py`, kit window H 29-58 | 54 | 27 |
  | `gold_cmp.py`, rendered window H 40-62, s >= 0.6, v >= 0.55 | **47** | **20** |
- **Shares (all figure pixels, %):**

  | view | MAUVE | PLUM | ICE_W | JOINT_D |
  |---|---|---|---|---|
  | side | 60.6 | 12.1 | 14.6 | 7.8 |
  | tq | 58.7 | 13.8 | 12.1 | 7.6 |
  | game | 57.0 | 16.7 | 15.2 | 7.1 |
  | back | 60.7 | 17.0 | 11.5 | 7.1 |
- **Tris 7,664.**
- **Renders (title bars carry the render time, 2026-10-28 04:20):** `_model_sheet.png` plus the icon strips,
  `gamelook_*` and `flat_*` re-made.

## FINAL 8.5 ROUND 2 (2026-10-28, after `_review/PermafrostTitan_final85_r2.md`, FIX model 7.5) - re-exported
Backup of the round-1 export: `_scratch/PermafrostTitan_exported_f85.py`.
- **MUST 1, one tapered tube per leg:**
  - Thigh 0.182 x 0.194, tapering to **0.66** at the knee.
  - The shin starts at the thigh's knee width (+0.006, a slight calf) and tapers to 0.84 at the ankle, so there is no
    step at the knee.
  - The plum thigh plate is now **0.020** thick (was 0.046). It rides 0.012 inside the thigh surface (0.008 proud) and
    stays on the flat part of the side.
  - The knee cap is 0.020 deep and sits on the shin front, so it is a bulge, not a block.
  - The knee joint is inside the tube.
  - The shin guard is 0.018 thick and rides the tapering shin front (0.008 proud).
  - **One** thin ankle band (+0.008 over the shin end); the foot's ankle joint sits inside it.
- **MUST 2, hips:**
  - The hip block is 0.27 wide (was 0.30), with a 0.78 base taper.
  - The thigh tops sit 0.02 further out.
  - The plum hip plates are thinner (0.034, was 0.058) and sit on the hip (x 0.238), not over the thigh tops.
  - `_model_sheet.png` front: the thighs now start as wide tops right under the hip block and taper down.
- **MUST 3, chest to pelvis:** the belt joint rnd 0.5 (was 0.4, width 0.262); the chest bottom taper 0.62 (was 0.66);
  the chest/waist gap rnd 0.5, width 0.26.
- **NICE 1:** the belly band is 0.16 x 0.012 x 0.030 (was 0.20 x 0.016 x 0.036).
- **Numbers:**
  - Tris **7,664**.
  - Gold at 64 px (kit counter): **portrait 52, game 27**.
  - Shares, all figure pixels:

    | view | MAUVE | PLUM | ICE_W |
    |---|---|---|---|
    | side | 60.6 | 12.0 | 14.6 |
    | tq | 58.3 | 13.9 | 12.1 |
    | game | 56.7 | 16.6 | 15.2 |
    | back | 60.3 | 16.9 | 11.4 |
- **Renders (all re-made):** `_model_sheet.png`, `_close_sheet.png`, `_under_sheet.png`, the icon strips,
  `gamelook_*.png`, `flat_*.png`.

## FINAL 8.5 (2026-10-28, after `_review/PermafrostTitan_final85.md`, FIX model 7) - re-exported
Backup of the exported round-5 file: `_scratch/PermafrostTitan_exported1.py`.
- **MUST 1, colour:** MAUVE **(164,116,200)**, PLUM **(98,66,130)** exactly as specified (ICE_W, GOLD and JOINT_D unchanged).
  - **The in-game test is NOT met:** the `gamelook_game` body (0.6x colour preview, figure pixels in the body hue band) reads
    mean **(93,81,127)**, median (87,77,121), dominant 8-level bucket **(80,64,112)** against the target **(100,80,130)**.
    The review measured about (72,64,104) at the old colour, so the lift is about +8 to +21 per channel.
  - Tested a further lift to (184,130,224): mean (102,87,140), dominant bucket (88,72,128). That is still under the bucket
    target, and the body turns pastel pink-lilac (`_scratch/mauve_cmp.png`, `gamelook_mauve164/184.png`,
    `icon_mauve164/184.png`). I kept the specified RGB. The dark read is the preview's lighting more than the RGB; the
    lead may want to judge it in Studio.
- **MUST 2, limbs:** every limb segment now tapers toward the joint below it.
  - Thigh 0.182 x 0.194 with the far end at **0.72**; shin 0.156 x 0.164 at **0.74**; shin guard (0.86, 1.0).
  - Upper arm 0.134 x 0.144 at **0.80**; forearm 0.140 x 0.148 at **0.82**; bracer 0.160 x 0.168 at 0.80.
  - Deltoid rnd **0.55** (was 0.45).
  - From the front the hip block still covers the thigh tops, so the taper reads most from the side and 3/4
    (`renders/_model_sheet.png`, `_kneel_views.png`).
- **MUST 3, jaw:** the MOUTH lip is on bone **`Jaw`** at the hinge seam (0, -0.399, 1.727). A JOINT_D cavity
  (0, -0.335, 1.707), half (0.086, 0.040, 0.018), sits on `Head` behind it. The roar jaw opens 24 deg (was 16).
  `renders/_roar_jaw_close.png` shows a dark slate mouth gap at f27, front and 3/4.
- **TO 9+:**
  - (1) Chest ring R_OUT **0.272** (0.265 gave 44 px). Portrait gold **51 px** at 64 (kit counter, H 29-58; brief
    counter 78; was 37). Game camera **27** (brief counter 31).
  - (2) Skull **(0.160, 0.160, 0.135)**, raised 0.02 (the crown cap, cheeks, brow, eyes and face plate move with it).
    The eye sockets and slits are **15 % wider** (`ice_eye(wx=1.15)`).
  - (3) A blunt, flat-topped ICE_W chunk on each pauldron tip, about 0.18 tall: the chunks end in a flat `top`
    (0.86, 0.80), no points.
  - (4) Knuckle shards 0.058 -> **0.035** (lengths 0.060 / 0.072 / 0.060 at `top` 0.80 x 0.72). From the front they
    read as ice knuckles, not teeth.
  - (5) A smooth ICE_W belly band (0, -0.176, 1.098), half (0.20, 0.016, 0.036), under the ribcage.
  - (6) VFX: skipped (the coordinator adds particles in Studio).
- **Numbers:**
  - Tris **7,672**; Lua 32,186 B.
  - Shares, all figure pixels (flat renders):

    | view | MAUVE | PLUM | ICE_W |
    |---|---|---|---|
    | game | 54.7 | 16.8 | 15.0 |
    | side | 60.0 | 11.2 | 14.6 |
    | tq | 56.5 | 14.4 | 12.2 |
    | back | 59.4 | 16.4 | 11.3 |
- **Renders (all re-made 2026-10-28):** `_model_sheet.png`, `_close_sheet.png`, `_under_sheet.png` (clean; the only nit
  is a few thigh-top studs showing through the hip block in the 500 px low-back close-up), `_icons_strip_64/128.png`,
  `_icons2_strip_64/128.png`, `gamelook_game.png` / `gamelook_tq.png`, `flat_*.png`.

## ROUND 5 (2026-10-27, review 4 NICE 4)
- Back echo ring outer diameter 0.27 -> **0.28 BU** (BR_OUT 0.140). Gold at 64 px (kit counter): portrait 37, **game 24**.
  ICE_W on flat_game **13.5 %** (all figure pixels), back view 9.8 %. Tris 7,552.

## ROUND 4 (2026-10-27, after `_review/PermafrostTitan_review3.md`, model approved; MUST 3 back pale)
- Upper shoulder caps **0.150 x 0.170 x 0.036** (rnd 0.30, the three chunks kept). This is a little over the asked
  0.140 x 0.160 x 0.035: that size measured 12.3 % on flat_game, too thin a margin given the review counts ~1 point under
  mine. The lower caps are 0.084 x 0.152 x 0.035. No spikes, no crown.
- **Pale share, stated method:** `renders/flat_game.png` (the kit's flat palette ID render of idle f0 from the game
  camera). Every figure pixel (background = max channel < 6 excluded) is assigned to the nearest palette colour
  (`_scratch/shares_all.py`; `_scratch/shares.py` also drops anti-aliased edge pixels).
  - **ICE_W game 13.5 %** (all pixels) / 13.3 % (edge-excluded). Target >= 12.
  - Same method on the other views: side 13.6, tq 10.5, back (`flat_back.png`, straight behind) 9.9.
- **Gold at 64 px (method: `_tools/game_icon.py`, the kit counter):** portrait 36, game camera **22** (gate 20). The brief
  counter reads 58 / 24. The bigger pale caps cost about 2 game-camera gold pixels.
- Tris 7,552 (unchanged), H 2.029.

## ROUND 3 (2026-10-27, after `_review/PermafrostTitan_review2.md`, APPROVED WITH FIXES 7/10) - shipped with the clips
- **MUST 1** back echo ring: outer 0.27 BU diameter (BR_OUT 0.135, BR_IN 0.088, band 0.047, depth 0.06, proud 0.030), ice
  disc r 0.066; a ring only (no settings, spikes or crown). Game-camera gold at 64: **24 px** (kit counter; target >= 20).
- **MUST 2** upper shoulder caps 0.130 x 0.150 x 0.033 (rnd 0.30, three chunks), lower caps 0.076 x 0.145 x 0.034, pauldron
  bottom 0.80: game (back) **ICE_W 11.5 %** (target >= 11). No spikes on the hump.
- NICE 1 shin guard depth 0.028; NICE 2 chest bottom taper 0.66; NICE 4 brows 30 deg. NICE 3 (Studio colour) and NICE 5
  (pet facing) need Studio - not possible from here.
- Evidence: `renders/model_back.png`, `renders/under_lowback.png`, `renders/gamelook_game.png`, `renders/_icons2_strip_64.png` / `_128.png`,
  `_scratch/game_icon.json`, `_scratch/shares_strict.json`. Clips: see `CLIP_NOTES.md`.

## ROUND 2 (2026-10-27, after `_review/PermafrostTitan_review1.md`, REVISE 6/10) - every MUST + NICE applied

Numbers now: **7,168 tris**; H_MODEL 2.029 BU, HEIGHT 10.0, PITCH 0.0455 (unchanged). Gold at 64 px: **portrait 36**
(kit counter; brief counter 55; r1 31), **game camera (behind) 16** (r1 0; review test >= 8). Head pose test
(`pose_try`: bow 12, lift -10, yaw +/-25, bow + yaw + jaw, chest bow + head bow): **0 collisions**, ground 0.0.

Strict value shares (background AND edge / speckle pixels excluded):

| colour | side | tq | game |
|---|---|---|---|
| MAUVE | 66.0 | 63.2 | 59.9 |
| PLUM | 12.3 | 14.8 | 19.0 |
| ICE_W | 10.2 | 8.7 | 10.4 |
| JOINT_D | 7.6 | 7.4 | 7.8 |
| GOLD + GOLD_D | 1.8 | 4.3 | 1.4 (r1 0) |
| BLACK | 2.2 | 1.6 | 1.6 |

| # | item | done |
|---|---|---|
| M1 | gold on the back | a **back echo bezel** on the hump's back face (centre z 1.69, tilted 8 deg up): 12 GOLD facets, outer dia **0.21 BU (~0.10 H, 44 % of the chest ring)**, band 0.035 radial, depth 0.06, GOLD_D lining, a small octagon ice disc inside; no settings, no crown, nothing pointed. On Chest; anchor `BACK` (model() info) for a glint VFX. Game-cam icon 16 gold px. Close-up `renders/close_back.png`. |
| M2 | brows | flat slate slabs: rnd 0.14 -> 0.06, half-length 0.084 -> 0.076, tilt 28 deg inner-down, dropped 0.005 onto the sockets. `close_brows.png`, `close_browtq.png`. |
| M3a | fists | the JOINT_D finger-gap band is gone; fist rnd 0.46, fingers rnd 0.55 (note: blockkit caps rounding at 0.45 x the smallest half-size, so 0.46 / 0.55 land at that cap). |
| M3b | pauldron | ice cap 0.148 x 0.165 x 0.036 -> **0.120 x 0.140 x 0.030**, rnd 0.30; pauldron body rnd 0.55 (capped) with a **bottom taper 0.80**; the three chunks kept. |
| M3c | feet | the foot is a **wedge**: a seg from heel to toes narrowing to 0.70 width at the toes, height 0.14 (half 0.07), rnd 0.45; three toe blocks kept. |
| M3d | knee caps | rnd 0.55 (capped), half-depth 0.05 -> 0.04. |
| N1 | colour | MAUVE (146,101,178): brightest channel 178 (passes 170). |
| N2 | gold margin | chest bezel R_OUT 0.225 -> 0.240: portrait 36 px. |
| N3 | core | the 0-deg square is gone: the core is now a flat **octagon ice disc** (radius 0.119, inside the gold-dark lining so the lining no longer cuts it into a star) + the 45-deg raised diamond + a small 45-deg top facet. |
| N4 | neck collar | JOINT_D neck knuckle half-height 0.090 -> 0.070, rnd 0.50. Head poses still 0 collisions. |
| N5 | ankle band | `A + (0,0,0.045)` -> `A + (0,0,0.015)`. |
| N7 | pet-facing | not verifiable from Blender (I do not touch Studio); the back ring now carries the gold from behind either way. |

Belly-up / from-below check: `PermafrostTitan/_scratch/view_under.py` (ground hidden) -> `renders/_under_sheet.png`
(belly, low front, low back): no floating, poking or open parts; soles are studded stone, toe claws black.

Deliverables: `renders/_model_sheet.png`, `_close_sheet.png` (back ring, brows front + 3/4, chest front / low / tq),
`close_low.png`, `_under_sheet.png`, `_icons_strip_64/128.png` and `_icons2_strip_64/128.png` (next to ThunderRex,
LavaGolem, CosmicLeviathan, GlacierYeti, BlizzardRoc), `flat_*.png`, `gamelook_*.png`; numbers in
`_scratch/shares_strict.json`, `_scratch/game_icon.json`, `_scratch/model_result.txt`.

---- (round 1 notes below, kept for history) ----

## Numbers (round 1)
- Tris: **7,000** (cap 15k).
- HEIGHT 10.0 studs = head top; H_MODEL 2.029 BU; stud PITCH 0.0455 (same world stud size as Raiju/Rex).
- Footprint 1.72 x 0.82 BU (8.5 x 4 studs at x1).
- Gold px in the 64 px portrait icon: **31** (kit counter; brief counter 50). Plan gate is >= 25. Game camera (behind): 0, see "Open items".

## What I built
- Upright, slightly forward-hunched stone giant: inverted-triangle studded ribcage, dark slate joint gaps (chest/waist, belt,
  neck, elbows, wrists, knees, ankles), plum armour plates (back slabs, back hump, forearm bracers, thigh plates, knee caps,
  shin guards, side hip plates, crown cap, thumbs).
- **Hero:** a 12-facet house-GOLD bezel ring set into the chest (outer dia 0.45 BU = 0.22H, band 0.075, depth 0.10, proud 0.045,
  tilted 10 deg up), GOLD_D inner lining, four low blunt gold settings on the diagonals; inside it a faceted ICE_W core
  (octagon disc -> raised diamond -> raised centre facet), smooth.
- Two rounded studded MAUVE pauldrons per shoulder, each capped with a glacier crust (an ICE_W slab + blunt flat-topped chunks).
- Long arms, flared forearms, boulder fists with curled fingers and three blunt ICE_W knuckle crusts.
- Pillar legs on blocky feet with 3 slate toe blocks (small black claws).
- Small bare head sunk between the pauldrons: slate brow ridge (two halves, 22 deg inner-down), deep-set wedge ICE_W slits in slate
  sockets with thin black reptile pupils (no glint), slate jaw seam with a flat closed mouth line, heavy square chin.
- No spikes anywhere (all ice chunks are blunt, flat-topped), no crown, no cyan, no glow.

## Palette (Blender RGB) and value shares (flat palette-ID renders, %)
| Name | RGB | side | tq | game | plan (side) |
|---|---|---|---|---|---|
| MAUVE | 136,94,166 | 65.3 | 62.8 | 58.7 | 48 |
| PLUM (added) | 86,56,112 | 11.8 | 14.8 | 20.5 | - |
| ICE_W | 226,240,250 | 11.3 | 9.4 | 11.6 | 12 |
| JOINT_D | 52,60,84 | 7.8 | 7.6 | 7.6 | 9 |
| GOLD | 255,196,50 | 1.2 | 3.3 | 0 | 4 |
| GOLD_D | 214,150,30 | 0.1 | 0.5 | 0 | 1 |
| BLACK | 14,14,22 | 2.4 | 1.6 | 1.6 | 2 |
MAUVE + PLUM (body family) = 77 % side. Gold is 1.2 % side because the bezel faces front (tq 3.8 %).

## Deviations from the plan (and why)
1. **Body colour deepened, same hue:** MAUVE (184,150,200) -> (136,94,166) (H 277, S 0.25 -> 0.43). In the 64/128 px strip next to
   Rex / LavaGolem / Leviathan / Turtle / Treant the plan value read as a pale pastel "toy" (every approved body is S 0.45-0.8
   or a dark neutral). In game (x0.6) it is about (82,56,100): dusky purple stone. Still H 277, out of the Glacier blue-violet
   cluster (212-250). In-game preview: `renders/gamelook_tq.png`, `gamelook_game.png`.
2. **Added PLUM armour plates** (same hue family, darker) for the 3-band blocking a secret needs (stone / plum armour / white ice +
   slate joints + gold hero). Without them the body was one flat colour.
3. **Extra blunt ice:** a glacier crust breaking out of the back hump (4 flat-topped chunks) and 2 small crusts on each forearm bracer,
   so the game camera (from behind) reads "ice giant". No points, no spike rows (Rex distinction kept).
4. **Proportions:** the plan's numbers are inconsistent (thigh 0.34H + shin 0.30H + foot 0.14H + shoulder line 0.82H leaves no
   torso). Used: hip 0.42H, knee 0.25H, shoulder joint 0.77H, pauldron tops ~0.93H, head top 1.0H; fists hang at 0.27-0.40H,
   just above the knees; head 0.145H wide.
5. **Bezel band** 0.037H radial (plan 0.03H) + the 4 gold settings, to clear the >= 25 gold px gate with margin.
6. Head group translated +0.035 up / 0.03 forward (HEAD_XF, pure translation) and a rounded slate neck knuckle centred on the throat
   pivot: tested poses head bow 12 (kneel), bow 14 + chest 3, bellow (head -10, jaw 10, arms out 8), look +15 / -25 yaw,
   roll 5 = **0 collisions** (pose_try).

## Rig (built, tested with pose_try)
Spine, Chest, Head (throat pivot), Jaw; Arm/Fore/Hand L/R (2-bone IK chains, elbows bend back); Leg/Shin/Foot L/R (IK, knee
pole forward). VFX anchor bones: `Core` (core pulse), `Hero` (bezel glint), `Pauldron_L/R` (frost drift, on the caps),
`Fist_L/R` (ice dust, at the knuckles), `Knee_R` (ice crack on the kneel).

## Evidence
- `renders/_model_sheet.png`, `renders/_close_sheet.png` (face + bezel), `renders/_icons_strip_64.png` / `_128.png`,
  `renders/_icons2_strip_64.png` / `_128.png` (portrait + game-camera icon + comparisons), `renders/gamelook_*.png`,
  `renders/flat_*.png`, `PermafrostTitan_icon.png`.
- Comparisons in the strips: ThunderRex, LavaGolem, CosmicLeviathan, SeaTurtleWarrior, Treant (Glacier siblings are not built yet).

## Open items for the reviewer / lead
- The bezel is on the chest, so the game camera (behind) shows no gold; from behind the read is the plum back slabs, the glacier
  crust on the hump and the pauldron ice. Pets turn to face the player when idle, and the Index/portrait shows the bezel.
- The Roc and Yeti (the pets it must outclass) are not built yet; I could only compare against the approved pets.
