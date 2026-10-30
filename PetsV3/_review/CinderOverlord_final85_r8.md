**Model: 8.4/10 - FIX. Clips: 8.5/10 - PASS.**

# Cinder Overlord - FINAL 8.5 GATE, ROUND 8 (fresh reviewer, 2026-10-28)

Round 7 changes are real: the rear vents are gone, the head is bigger, gold is 113 against the Phoenix's 93 at 64 px, and the clips still hold. But from the game camera the Cinder is still a banded serpent tube with a crown on top, and the head + crown share is 0.244 against the 0.30 target from round 7. Model stays FIX at 8.4. Clips hold at 8.5 after the head scale.

## 0. What I looked at, and the limits

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`. Round 7 `_review/CinderOverlord_final85_r7.md`.
- Builder notes `CinderOverlord/MODEL_NOTES.md` (FINAL 8.5 ROUND 7, export 09:08), `CLIP_NOTES.md` (round 7 header), `_scratch/gate_f85.json` (09:12), and the headless run in `_scratch/export_r7.txt`.
- Freshness: FBX `C:\cdimp\CinderOverlord.fbx` 09:08; `renders/pose_tq_*` 09:08; sheets and icons 09:09-09:11; title bars read "final 8.5 round 7". All current, so the clip re-check is on the new head.
- Images opened and loaded: `renders/gamelook_game.png`, `CinderOverlord_icon_game.png`, `renders/_icons_alt_strip_64.png` and `_128.png`, `CinderOverlord_portrait_alt.png`, `renders/close_front.png`, `renders/_close_sheet.png`, `renders/_model_sheet.png`, `renders/_icons_strip_128.png`, `renders/_icons2_strip_128.png`, `renders/_pose_tq_sheet.png`, `renders/_molt_r7_front.png` and `_tq.png`, `renders/_cv_roar_front.png` and `_side.png`, `renders/_cv_walk_game.png` and `_side.png`.
- Limits: PIL is not available, so I could not zoom or re-count pixels. Gold, area and share numbers are the builder's gate file, checked by eye only. I did not run Blender (reviewer rule), so the collision and ground results are from the builder's headless log, not my own run.

## 1. Clip table (lowest clip = 8.5, so Y = 8.5 PASS)

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.5 | Head held near level through the 0 / 30 / 60 / 90 beats; crown breath is small; no head shake. The bigger head does not sag or drift. Breath amplitude is a Studio check (lead ruling). Loop 0 / 0 in the gate. | `renders/_pose_tq_sheet.png` (idle row), `_scratch/gate_f85.json` `audit.idle` |
| walk | 8.5 | The S-wave runs head to tail in the side view and holds its line; the head does not shake; no body poke through the ground. The walk game tile is clean: the blue vent bars stay put and do not swing. The tail runs off the bottom of the tile at f0 and f40 in the fixed game camera (see TO 9+ 4). | `renders/_cv_walk_side.png`, `renders/_cv_walk_game.png` |
| roar | 8.5 | Crown flare from f14; jaw opens clearly at f30 in the front and side views, with the mouth visible; closes by f58. The enlarged head shows no contact with the crown or the neck. | `renders/_cv_roar_front.png`, `renders/_cv_roar_side.png` |
| act_molt | 8.5 | Blades lift one by one, the fan is visible at f22-f40 from the front, reseat f84-f100, and f110 matches f0. Outer blades peak at 55.84 deg (gate). No visible contact with the bigger head or crown. | `renders/_molt_r7_front.png`, `renders/_molt_r7_tq.png`, `_scratch/gate_f85.json` `molt_blade_speed_deg_per_f` |

Headless run (`_scratch/export_r7.txt`): `collision_free` true in all four clips, `ground_min_z` -0.006 in all four, linear 0, idle and walk loops 0 / 0, stride 5.0089 per 48 f, tris 10,188.

## 2. Round 7 items

| item | result | evidence |
|---|---|---|
| R7 MUST 1a, vents off Body3, Body4, Tail1 | **PARTIAL.** The rear pairs are gone (the bone list ends at Vent_1..3). From the game camera the three remaining pairs still stick off the flank like blue stubs, which still reads as legs (see MUST 1c). | `_scratch/export_r7.txt` bones; `renders/gamelook_game.png`; `renders/_cv_walk_game.png` |
| R7 MUST 1b, head x1.15, crown mount +0.04, head + crown >= 0.30 of icon height | **PARTIAL.** The change is made (HEAD_XF 1.38, mount ends 0.26). The measured share is **0.244** of the icon height (0.283 of the figure), below the 0.30 target. The builder reports it as not reached. | `_scratch/gate_f85.json` `game_icon_head_share`; `MODEL_NOTES.md` round 7 |
| R7 MUST 1, pass tests | Area 0.190 (>= 0.18) **PASS**. Collision-free, ground -0.006 **PASS**. Re-rendered **PASS**. A fresh reviewer says it reads as a dragon at 64 px: **FAIL**. The game silhouette is still a long even tube with regular dark bands and a crown on top, and reads as a serpent or worm more than a dragon. | `renders/gamelook_game.png`, `CinderOverlord_icon_game.png`, `renders/_icons2_strip_128.png` (tile 2) |
| R7 MUST 2, gold >= 103 at 64 px | **PASS.** Portrait_alt 113 (kit window H 29-58) against Phoenix 93 and Ivonrath 25. A 21 % margin, not the one-pixel tie from round 7. | `_scratch/gate_f85.json` `icons_64_128` |
| R7 MUST 2, area >= 0.36 | **PASS.** 0.364 against Phoenix 0.267 and Ivonrath 0.295. | same |
| R7 MUST 2, head and crown above the Phoenix head line at 128 px | **PASS** on the stated test. The Cinder's crown reaches the top of its tile, about 25 px above the Phoenix's crest (by eye). | `renders/_icons_alt_strip_128.png` |
| R7 MUST 2, "hero, not the louder read" | **PARTIAL** (my judgment). The Cinder has the bigger, brighter gold. The Phoenix's upright, flame-tipped stance still reads as the busier figure, and the Cinder lies in a coil. | `renders/_icons_alt_strip_128.png` |
| R7 MUST 2, molt collision-free | **PASS** per gate. No visible contact in the molt frames. | `_scratch/gate_f85.json` `collision_free`; `renders/_molt_r7_front.png` |
| R7 TO 9+ 1, chin flatter by about 15 % | **NOT VISIBLY DONE.** The numbers changed, but from the front the chin is still a rounded bulb under the snout. | `renders/close_front.png` (lower centre), `renders/_close_sheet.png` |
| R7 TO 9+ 2, eye socket outer ends in 0.01 | **PARTIAL.** From the front, the left blue socket still appears to reach the skull outline at eye height. I could not measure it. | `renders/close_front.png`, `renders/_close_sheet.png` |
| R7 TO 9+ 3, nostrils >= 0.02 BU | **PASS.** Black diamonds read clearly in the close-up. Builder size 0.025 x 0.033 BU. | `renders/close_front.png`; MODEL_NOTES round 7 |
| R7 TO 9+ 4, walk game re-check after the vent cut | **PARTIAL.** The bars no longer swing, but they still read as legs from the game camera (MUST 1c). | `renders/_cv_walk_game.png` |
| R7 TO 9+ 5, stale renders | **PARTIAL.** `mr4_*`, `mr6_*` and `_molt_r4_*` are out of `renders/` now. `renders/crown_back.png` and `crown_front.png` (01:21) are still there. | `renders/` listing |
| R7 TO 9+ 6, pose-limit reading | Not re-measured here (lead to confirm the per-bone reading). | `CLIP_NOTES.md` |
| R7 TO 9+ 7, tier record | **PARTIAL.** `GLACIER_CONCEPTS.md` line 46 now says MYTHIC, but line 116 still says "ultra-rare", and line 46's swatches are the old plum and rose palette. `MODEL_NOTES.md` line 3 still says ULTRA-RARE 0.5 %. | `_review/GLACIER_CONCEPTS.md` lines 46, 116 |
| R7 TO 9+ 8, breath | Studio check (lead ruling). Not scored. | |
| Tris <= 15k | **PASS.** 10,188. | `_scratch/gate_f85.json` `tris` |
| Stride | **PASS.** 5.0089 per 48 f. | `_scratch/export_r7.txt` |
| Molt outer lift >= 55 deg | **PASS** per gate (55.84). Not re-measured. | `_scratch/gate_f85.json` |

## 3. Model score: 8.4 - FIX

**Holds:**
- Gold wins the counter and the area against Phoenix and Ivonrath at 64 and 128 px. The crown is the hero in the portrait.
- The front face reads fierce: narrow blue slits under heavy brows, no glints, no smile, no googly eyes. The nostril pits are now visible.
- Vents are slits, not legs, from the front and the 3/4 view (`renders/_model_sheet.png`). Ember, obsidian rings and pale belly still read as three bands.
- Tris 10,188; collision-free through the roar and the molt with the bigger head. Studs cover the whole skin.
- The head is bigger on the game icon than in round 7, and the rear vents are gone.

**Blocks 8.5:**
1. The game-camera read is still a serpent or worm tube, not a dragon. The head + crown share is 0.244, short of the round 7 target of 0.30. The visible blue flank bars still read as legs. (MUST 1.)

Note: the round 7 MUST 2 pass tests are all met on the stated test. The "louder read" point is a judgment and stays a 9+ item.

## 4. New MUSTs (block 8.5 on the model)

**MUST 1 (model): the game-camera read must be a dragon, not a serpent tube, and the head + crown share must reach the round 7 target.**
Evidence: `renders/gamelook_game.png` and `CinderOverlord_icon_game.png` (one even-width body with three or four dark bands and a crown on top); `renders/_icons2_strip_128.png` tile 2; `_scratch/gate_f85.json` `game_icon_head_share` 0.244.
- (a) **Head + crown height.** Raise the head + crown share on the kit game icon from 0.244 to **>= 0.30** of the icon height (`CinderOverlord/_scratch/head_share.py`, game view). Method: `HEAD_XF` 1.38 -> **1.50** about the throat, and the centre crown blade 0.36 -> **0.40 BU** (its gold frame keeps the +0.004 inward rule). If still below 0.30, go to `HEAD_XF` 1.55 at most. Re-run the molt and roar collision checks: the taller crown and the bigger head are the new risk.
- (b) **Body bands from the game camera.** Drop one dark ring on the mid-body (the ring between the Body1 and Body4 rings that shows on the back in `gamelook_game.png`), so the back shows two bands between the neck and the tail, not three or four. Game obsidian share must not rise above 25.0 % (now 25.0). Game body share stays >= 40 % (now 53.0).
- (c) **Blue flank bars.** From the game camera the blue slits still stick off the flank like legs (`gamelook_game.png`, and the walk game at f0-f16). Shorten all six blue vent slits (Vent_1..3, both sides) by **30 %** in length. No slit tip may stand outside the body outline from the game camera.
- **Pass:** game area >= 0.18 (now 0.190); collision-free in all four clips after the head and crown change; ground_min_z >= -0.02. Re-render `gamelook_game.png`, `CinderOverlord_icon_game.png`, `_cv_walk_game.png` and the 64 / 128 strips. A fresh reviewer must then say "dragon, not worm" at 64 px.

## 5. TO 9+ (not blocking)

1. **Chin.** From the front (`renders/close_front.png`, lower centre), flatten the front face of the chin cap about 15 % more, or narrow the cap ring, so the front reads as a jaw, not a bulb. The round 7 numbers did not change the read.
2. **Eye sockets.** Pull the left and right blue socket outer ends in another 0.01 BU, or sink them under the brow, so no blue sits on the skull outline from the front.
3. **Index card pose.** The portrait is a low lying coil; the Phoenix stands upright. Fill height is already 0.91, so the gap is pose. The molt neck limit (7.5 deg per bone) caps any lift, so the 9+ route is the head + crown height from MUST 1a.
4. **Walk game framing.** The tail runs off the bottom of `renders/_cv_walk_game.png` at f0 and f40. Check in Studio that the follow camera does not crop it.
5. **Hygiene.** Move `renders/crown_back.png` and `crown_front.png` (01:21, stale) to `_scratch/`. `MODEL_NOTES.md` line 3 still says ULTRA-RARE 0.5 %. `_review/GLACIER_CONCEPTS.md` line 116 still says "ultra-rare", and line 46's swatches still list the old plum and rose palette.
6. **Pose-limit reading.** Lead to confirm the per-bone reading (neck 7.5 per bone, limit 8).
7. **Breath.** Studio check, as ruled.
8. **Rare-tier comparison.** Thunder Rex and Cosmic Leviathan pass on the counter (13 and 20 px). Visually at 64 px both are brighter, flashier figures than the Cinder's red coil. Not re-scored here; worth a look in the same round.
