**Model: 8.3/10 - FIX. Clips: 8.5/10 - PASS.**

# Cinder Overlord - FINAL 8.5 GATE, ROUND 7 (fresh reviewer, 2026-10-28)

The coil and the crest widening are real improvements on the numbers: game-camera area 0.190 (pass), collision-free, gold 94 vs Phoenix 93. But the player's-eye read is still a long segmented worm with a small crown on top, and the rare-tier outclass is only won by one pixel on the counter. Clips hold at 8.5 after the body coil.

## 0. What I looked at, and the limits

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`. Round 6 `_review/CinderOverlord_final85_r6.md`.
- Builder notes `CinderOverlord/MODEL_NOTES.md` (FINAL 8.5 ROUND 6, exported 08:41), `CLIP_NOTES.md`, numbers `_scratch/gate_f85.json` (08:48).
- Freshness: FBX `C:\cdimp\CinderOverlord.fbx` 08:41; `renders/pose_tq_*` 08:41; sheets 08:43-08:46 (title bars read "final 8.5 round 6"). All current, so the clip re-check after the body coil is on the new model.
- Images opened, all loaded: `CinderOverlord_portrait_alt.png`; `renders/_icons_alt_strip_64.png` and `_128.png` (alt, kit, Phoenix, Ivonrath, Rex, Leviathan); `renders/_icons_strip_128.png` (Cinder, BlackDragon, Boar, Golem, Cerberus, Ivonrath, Phoenix, Rex, Leviathan); `renders/gamelook_game.png`; `CinderOverlord_icon_game.png`; `renders/_model_sheet.png`; `renders/close_front.png`; `renders/_close_sheet.png`; `renders/flat_game_stamped.png`; `renders/_pose_tq_sheet.png`; `renders/_cv_walk_game.png`, `_cv_walk_side.png`; `renders/_cv_roar_front.png`, `_cv_roar_side.png`; `renders/_molt_r6_front.png`, `_molt_r6_tq.png`.
- Limit: PIL is not available, so I could not zoom or re-count pixels. Gold and area numbers are the builder's gate file, checked by eye only.
- Hygiene: `renders/mr4_*_act_molt_*` (05:00, stale) are still in `renders/`, although MODEL_NOTES says the stale sheets were moved. Not scored.

## 1. Clip table (lowest clip = 8.5, so Y = 8.5 PASS)

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.5 | Head held level, neck breath is small; loop closes; no head shake. Breath amplitude is a Studio check (lead ruling). | `renders/_pose_tq_sheet.png` (idle 0 / 30 / 60 / 90) |
| walk | 8.5 | The head-to-tail S-wave reads in the side and game views after the coil; the head holds its line; no shake; no body poke through the ground. The worm-like read from the game camera is the MODEL silhouette (MUST 1), not a motion fault, so the clip is not docked for it. | `renders/_cv_walk_side.png` and `_cv_walk_game.png` (f0-40) |
| roar | 8.5 | Crown flare from f14, jaw opens clearly at f30 in the front and side views; closes by f58; no collision. | `renders/_cv_roar_front.png`, `_cv_roar_side.png` |
| act_molt | 8.5 | Blades lift one by one (fan visible f22-f40 from the front), reseat f84-100, and f110 matches f0. Outer blades 55.84 deg/peak in the gate. | `renders/_molt_r6_front.png`, `_molt_r6_tq.png`; `_scratch/gate_f85.json` `molt_blade_speed_deg_per_f` |

## 2. Round 6 items

| item | result | evidence |
|---|---|---|
| R6 MUST 1, game-camera worm read | **PARTIAL.** Metric passes (area 0.190 >= 0.18; fill width 0.53, waived by lead). Visual still fails: it reads as a segmented worm / centipede with a small crown, not a dragon. See MUST 1 below. | `renders/gamelook_game.png`, `CinderOverlord_icon_game.png`, first tile of `renders/_icons_strip_128.png` |
| R6 MUST 2, outclass Phoenix and Ivonrath | **PARTIAL.** Counter passes: kit-window gold Cinder 94 vs Phoenix 93 (a 1 px margin, within noise) and vs Ivonrath 25; area 0.373 vs 0.267 / 0.295. Visual outclass vs Phoenix is not shown: at 128 px the Phoenix reads louder, brighter and more dynamic. Ivonrath is clearly outclassed. | `renders/_icons_alt_strip_128.png` (Phoenix tile), `_icons_alt_strip_64.png`; gate `icons_64_128` |
| R6 TO 9+ 1, game gold >= 30 | **PASS.** Kit counter game gold 35 (was 25). | `_scratch/gate_f85.json` `gold_px_64.game` |
| R6 TO 9+ 2, T-a eyes | **PARTIAL.** The blue socket outer ends still meet or sit on the skull edge at eye height from the front. | `renders/close_front.png`, `renders/_close_sheet.png` (front panel) |
| R6 TO 9+ 3, T-b chin | **NOT DONE.** The chin is still a broad rounded bulb under the nose from the front, which reads as a bulbous muzzle. | `renders/close_front.png` (lower centre) |
| R6 TO 9+ 4, nostril pits | **NOT DONE.** Pits are still small black diamonds in the close-up; builder's size is 0.006 BU, below the 0.02 BU floor. | `renders/close_front.png` |
| R6 TO 9+ 5, breath | not scored (Studio check, lead ruling). | |
| R6 TO 9+ 6, stale evidence | **PARTIAL.** The pose, walk, roar and molt sheets are current (08:41-08:46). Stale `renders/mr4_*` (05:00) remain in `renders/`. | file times |
| R6 TO 9+ 7, pose-limit reading | not re-measured here. Builder reports neck 7.5 per bone (limit 8), spine 4.5 (limit 5), head net 2. Lead to confirm per-bone reading. | `CLIP_NOTES.md` |
| R6 TO 9+ 8, tier record | not checked (`GLACIER_CONCEPTS.md` lines 46 / 116 still say ultra-rare 0.5 %). | |
| Molt outer lift >= 55 deg | **PASS.** Crown_1 / Crown_5 max 55.84 deg. | gate json |
| Tris <= 15k | **PASS.** 10,268. | gate json |
| Collision-free, ground >= -0.02, linear 0, loops closed | **PASS.** `collision_free` true; ground -0.006 in all four clips; linear 0; loops 0 / 0. | gate json `step1` |
| Stride | **PASS.** 5.0089 BU / 48 f in the meta; the coil kept segment lengths. | gate json `export` |

## 3. Model score: 8.3 - FIX

**Holds:**
- The portrait and the crest read well at 128 px. The crown is the hero: gold on dark obsidian blades, with the molt fan visible in the portrait.
- Fierce face from the front: narrow blue slits under heavy brows, no glints, no smile, no googly eyes.
- Three bands read in the body: ember, obsidian rings and saddle, pale belly.
- Vents are slits, not legs, from the front and the 3/4 view (`_model_sheet.png`).
- Tris 10,268. Collision-free through the roar and molt with the thicker body. Studs cover the whole skin.

**Blocks 8.5:**
1. **The player's-eye silhouette still reads as a worm or centipede.** In `gamelook_game.png` and `CinderOverlord_icon_game.png` the body is a long, narrow tube with regular black ring bands. Six blue vent bars per side stand out from the flank like legs. The head is a small cap with a crown at the top of the tube. The coil fixed the S-curve but not the read, so the species still does not read instantly as a dragon at phone size.
2. **The rare-tier outclass is not shown visually against Phoenix.** The counter tie (94 vs 93) is one pixel. At 128 px the Phoenix's upright, bright and fierce pose is the louder read. The Cinder reads as a crowned serpent lying flat, which is less impressive than the Phoenix.

## 4. New MUSTs (block 8.5 on the model)

**MUST 1 (model): the game-camera read must be a dragon, not a centipede.** Evidence: `renders/gamelook_game.png`, `CinderOverlord_icon_game.png`.
- (a) **Vent bars at game distance.** Keep the vent pairs on Body1 and Body2 only (both sides). Delete the pairs on Body3, Body4 and Tail1 in the vent block of `pets/CinderOverlord.py` (the `Vent_*` anchors follow the removed pairs). The accent share in the game view must stay at or above 4 % (it is 6.5 % now).
- (b) **Head mass.** Scale the Head group by x1.15 about the throat (the `HEAD_XF` scale), and widen the crown mount by 0.04 BU on each side. Then measure the head + crown height on the game icon at 64 px; target >= 0.30 of the icon height (I could not measure it here, so the builder must).
- Pass: game-camera area stays >= 0.18; `collision_free` true in all four clips after the head scale; ground_min_z >= -0.02. Re-render `gamelook_game.png`, `CinderOverlord_icon_game.png` and `_cv_walk_game.png`. A fresh reviewer must then say the species reads as a dragon at 64 px.

**MUST 2 (model): the Cinder must clearly outclass the Phoenix on gold and on read.** Evidence: `renders/_icons_alt_strip_64.png` / `_128.png`.
- Kit-window gold at 64 px: raise the Cinder from 94 to >= 103 (+10 % over Phoenix's 93). Do this by raising the centre crown blade 0.34 -> 0.36 BU (it was collision-free at 0.34 in r3), and widening the centre and middle gold frames by +0.004 BU each (the r6 fallback). Re-run the molt collision check after the change.
- Portrait area at 64 px stays >= 0.36.
- Visual check: the 128 px strip must show the Cinder's head and crown rising above the Phoenix's head line in the portrait_alt frame, so it is the hero, not the louder read.
- Pass: gold >= 103 at 64 px, area >= 0.36, molt collision-free, and the visual check passes in a fresh reviewer's view.

## 5. TO 9+ (not blocking)

1. **T-b chin.** Flatten the chin bulb's front face by about 15 % so the front reads as a jaw, not a bulbous muzzle.
2. **Nostril pits.** Widen to >= 0.02 BU or drop them (FIERCE_GUIDE floor).
3. **T-a eyes.** Pull the blue socket and slit outer ends in by 0.01 BU so no blue sits outside the skull outline from the front.
4. **Walk, game camera.** After MUST 1a the vent bars will no longer swing like legs; re-check `_cv_walk_game.png` after the change.
5. **Stale renders.** Move `renders/mr4_*` out of `renders/` into `_scratch/`, and fix the CLIP_NOTES and MODEL_NOTES lines that say the stale sheets were moved.
6. **Pose-limit reading.** Lead to confirm per-bone (neck 7.5) is the intended reading; a total reading would be a molt fail.
7. **Tier record.** If mythic stands, update `GLACIER_CONCEPTS.md` lines 46 and 116 from ultra-rare 0.5 % to mythic.
8. **Breath.** Studio check, as ruled.

## 6. Pass / fail checklist

| # | check | result |
|---|---|---|
| 1 | Tris <= 15k (10,268) | PASS |
| 2 | Collision-free, ground >= -0.02, linear 0, loops closed | PASS |
| 3 | Gold kit portrait >= 25 (91 kit window) | PASS |
| 4 | Gold game camera >= 25 (35) | PASS |
| 5 | Lemon <= 10 px (0-2) | PASS |
| 6 | Species reads at 64 px from the player's eye (game icon) | **FAIL** (MUST 1) |
| 7 | Portrait silhouette at 64 px | PASS |
| 8 | Outclasses Thunder Rex and Cosmic Leviathan at 64 px | PASS |
| 9 | Outclasses Phoenix (counter: 94 vs 93) | PARTIAL, one pixel; visual not shown (MUST 2) |
| 10 | Outclasses Ivonrath | PASS (94 vs 25; area 0.373 vs 0.295) |
| 11 | Eyes fierce from the front | PARTIAL (T-a) |
| 12 | Nose and chin smooth | FAIL (T-b, not done) |
| 13 | Vents read as slits, not legs (front / 3/4) | PASS |
| 14 | Vents read as slits, not legs (game camera) | **FAIL** (MUST 1a) |
| 15 | Molt outer lift >= 55 deg (55.84) | PASS |
| 16 | No head shake; acts end in rest | PASS |
| 17 | Clips current after the body coil | PASS (08:41-08:46 renders) |
| 18 | Clip scores (idle / walk / roar / act_molt) | 8.5 / 8.5 / 8.5 / 8.5, PASS |
