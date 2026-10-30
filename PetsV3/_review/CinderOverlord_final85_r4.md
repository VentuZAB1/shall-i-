**Model: 8.2/10 - FIX. Clips: 8.4/10 - FIX.**

Both are under the owner's 8.5 bar. Round 3 was model 8.0 / clips 8.0. The model gained for the forehead and the nostrils. The clip score is held back by a stale walk render and the Studio-only idle check. MUST 4 (walk speed) is closed by the lead and is not scored here.

# Cinder Overlord - FINAL 8.5 GATE, ROUND 4 (fresh reviewer, 2026-10-28)

## 0. What I looked at

- Brief: `_review/GLACIER_REVIEWER_BRIEF.md`. Round 3: `_review/CinderOverlord_final85_r3.md`.
- Builder notes: `CinderOverlord/MODEL_NOTES.md` (ROUND 3 section, 04:25), `CLIP_NOTES.md` (FINAL 8.5 ROUND 2 and the round-3 numbers), `_scratch/gate_f85.json` (the one gate file, 04:27), `_scratch/gold_windows_r3.txt`, `_scratch/export_r3.txt`, `_scratch/clipgate_r3.txt`, `_scratch/fix_r3.py`.
- Source checked for exact lines in `pets/CinderOverlord.py`: 195-196 (vent bar and core), 285-288 (neck rings), 298-299 (neck spikes), 338 (skull cap stations), 376 (eye point), 400 (centre blade 0.34). Palette: `LAVA = (226,240,255)` (line 29, the vent core), `ROSE = (20,92,250)` (line 25, the vent slit).
- Images (newest set, 04:24-04:26): `renders/close_front.png`, `renders/_close_sheet.png`, `renders/gamelook_game.png`, `renders/flat_game_stamped.png`, `renders/_model_sheet.png`, `renders/_icons_strip_64.png`, `renders/_icons_strip_128.png`, `renders/_icons2_strip_128.png`, `renders/_molt_r4_front.png`, `renders/_pose_tq_sheet.png`.
- Zoom crops (made in a scratch folder outside the project, not in the renders): the forehead of `close_front.png` (2.5x), the head and neck of `gamelook_game.png` (3x), and the flank vents of `gamelook_game.png` (2.6x).
- **Stale, not current:** `renders/_cv_walk_game.png` is dated 03:42. The model changed at 04:25 (vent geometry and core colour), so the walk game view does not show the current vents. I judged it only for the clip's motion, and I flag it under the clip MUST.
- Not opened: `_cv_walk_side.png`, `_molt_r4_side.png`, `_molt_r4_tq.png`, `_cv_roar_*.png`. The roar and molt are judged from `_molt_r4_front.png` and the pose sheet only.
- Not re-counted: the gold pixels. The window log (`gold_windows_r3.txt`) gives portrait 35 / game 28 on the kit counter, which matches the builder's numbers.

## 1. Round-3 items

| Item | Result | Evidence |
|---|---|---|
| MUST 1 forehead: red skull between the brows and the cap | **PASS** (marginal) | `close_front.png` and the 2.5x crop. The dark studded plate ends at the brow line. In the centre, red skull shows between the two brow blocks, from the plate's lower edge down to the brow line, about one brow block thick. The dark nasal ridge splits that red band down its middle. Code: the cap stations stop at 0.54 (line 338). |
| MUST 2 neck from above: at most one full dark band | **PARTIAL** | `gamelook_game.png` (3x crop): three dark bands still read down the neck, one per neck segment. Code: Neck1 has a full ring 0.50-0.84 (line 286); Neck2 and Neck3 have narrow rings 0.62-0.80 (lines 287-288). The obsidian neck spikes at t 0.67 (lines 298-299) sit on those bands and carry the dark mass down, so the narrow bands still read as rings from above. |
| MUST 3 nostrils read as eyes | **PASS** | `close_front.png`: two small dark pits on the snout top, about 40 px below the eye line. They are not in the eye line between the brows. The eyes are the blue slits at the skull sides. |
| T1 vents: do they still read as centipede legs? | **FAIL** (still reads as legs) | `gamelook_game.png` (2.6x crop): stacked pairs of blue-and-pale bars sit along the flank. The outer ends break the body silhouette on the near side. The pale core stripe (`LAVA`, line 196) reads as a rung. The flush geometry works (line 195, 311, 314), but the colour carries the read. The stale `_cv_walk_game.png` f0-40 shows the same rung pairs. See MUST 1. |
| T2 centre blade 0.34 | **PASS** | Line 400. The centre blade is taller in `close_front.png`, and the hero still reads in both icon strips. |
| T3 eyes 0.03 toward the nose | **PARTIAL** | Line 376. The move is applied, but the blue eye slits still sit on the outer skull edges and read as side-set from the front (`close_front.png`). Not a blocker. |
| T4 idle breath in motion | **UNVERIFIED** | Studio check. Cannot be judged from stills. Not a fail. |
| MUST 4 walk speed (lead-closed) | not scored | Per the lead ruling. |

Other checks:
- Tris 10,616 (PASS, cap 15k).
- Species at 64 px (PASS): in `_icons_strip_64.png` the Cinder is first and reads as a red serpent with a gold crest. At 128 px the body colour stays ember-red, separate from the Phoenix and Ivonrath.
- Gold (recorded, not re-counted): portrait 35 and game 28 on the kit counter, both above the 25 gate (PASS).
- Molt legible from the front: PASS, but small. In `_molt_r4_front.png` the outer blades visibly fan at f34-40 against f0. At 5 studs the change is modest.
- Pose sheet: idle, walk, roar and molt beats are all current and readable. No floating or intersecting parts are visible in any view.
- Model has no stray parts, and the snout tip is smooth.

## 2. Scores

**Model 8.2/10 - FIX.**
- Holds: a clear fierce serpent silhouette; the gold five-blade crest as the hero (taller centre blade, readable at 64 and 128 px); a palette that follows the plan; the forehead red band and the nostril fix now work; no stray parts.
- Blocks 8.5: (1) the vents still read as centipede legs from the game camera (the pale core is the cause); (2) the neck still reads as three bands from above.

**Clips 8.4/10 - FIX.**
- Holds: the molt reads from the front and the blades lift one by one; the roar is clear; the reseat is slower than the rise; idle and walk loops close; collision-free with ground min -0.006; linear 0; neck and chest limits met on the builder's numbers; the walk stride is closed by the lead.
- Blocks 8.5: the walk game render predates the current model, so I cannot confirm the walk reads without vent-leg rungs in motion. The idle breath in motion (T4) is still a Studio check.

## 3. New MUSTs (block 8.5)

**MUST 1 (model): vent cores read as rungs, so the vents read as legs.** `pets/CinderOverlord.py` line 196: the vent core bar is coloured `LAVA` (226,240,255). Change that one argument to `ROSE` (20,92,250), so the core is the same deep blue as the slit. Leave `LAVA` on the tail tip and the crown gem, which use it elsewhere. Do not change the geometry.
- Pass: in `gamelook_game.png` each flank vent reads as a single deep-blue slit with no pale rung stripe, and no pair reads as a leg pair.

**MUST 2 (model): neck still reads as three bands from above.** `pets/CinderOverlord.py` line 287 `elif i in (3, 4):` and line 288. Remove the Neck3 ring, so the band runs only on Neck2 (`elif i == 3:`), at 0.70-0.80 instead of 0.62-0.80. Leave Neck1's full ring (line 286) alone.
- Pass: in `gamelook_game.png` the neck shows one full dark band and one thin line, not three bands. Check the neck spikes too (lines 298-299, the `i in (2, 3, 4)` loop): drop the spike on Neck3 (`i == 4`) if it still reads as a band.

**MUST 3 (clips): the walk game render predates the model.** `renders/_cv_walk_game.png` and `renders/_cv_walk_side.png` are from 03:42, before the 04:25 export. Re-render the walk f0-40 from the game camera and the side camera from the current export (`C:\cdimp\CinderOverlord.fbx`), and record the render time in `CLIP_NOTES.md`.
- Pass: the re-rendered walk at 5 studs shows no vent pair breaking the silhouette in any frame of f0-40. This check also covers MUST 1 in motion.

## 4. TO 9+ list (polish, not blocking)

- **T-a eyes read as side-set.** `pets/CinderOverlord.py` line 376: move the eye point another 0.03 toward the nose (`-0.83` to `-0.86`), or shorten the eye slit (`0.110` to `0.090`), so the slits read as front-facing from 5 studs. Judge in `close_front.png`.
- **T-b snout tip reads a little pig-like from the front.** The rounded, studded nose bulb in `close_front.png` is the cause. Option: flatten the front of the snout tip by about 10 % and keep the nostril pits on it.
- **T-c molt fan at game distance.** The outer blades fan 85 deg at f34-40, but the change is small at 5 studs. Option: outer lift 45 to 50 deg (builder notes, round 3 CLIP_NOTES), then re-run the collision test. Keep the reseat slower than the rise.
- **T-d idle breath (T4).** Confirm in Studio that the 4.5 deg per neck-bone breath reads from about 5 studs.
- **T-e vent pairs.** If MUST 1 alone does not clear the legs read in the walk render, the next step is to drop the lower vent of each pair, not to add colour.

## 5. Pass / fail checklist

| # | Check | Result |
|---|---|---|
| 1 | Tris <= 15k (10,616) | PASS |
| 2 | Species reads at 64 px | PASS |
| 3 | Gold hero, portrait >= 25 (35, recorded) | PASS |
| 4 | Brows do not read as horns | PASS |
| 5 | Red skull between brows and cap | PASS (marginal) |
| 6 | Neck from above reads as one column | FAIL (MUST 2) |
| 7 | Face: eyes read, no beady centre marks | PASS (nostrils fixed; eyes side-set, T-a) |
| 8 | Vents read as slits, not legs | FAIL (MUST 1) |
| 9 | Snout tip smooth | PASS |
| 10 | Body colour distinct at 128 px | PASS |
| 11 | Clip: molt legible from the front | PASS (small at distance) |
| 12 | Clip: roar | PASS |
| 13 | Clip: reseat slower than rise | PASS (builder numbers) |
| 14 | Clip: renders current | FAIL (MUST 3, walk game 03:42) |
| 15 | Clip: reference disclosure (C2) | PASS (round 3) |
| 16 | Clip: neck, spine and head limits, loops, ground, collision | PASS (builder numbers) |
| 17 | Clip: walk speed (lead-closed) | not scored |
| 18 | Clip: idle breath in motion | UNVERIFIED (Studio, T-d) |

## 6. Summary

- **Model 8.2/10 - FIX. Clips 8.4/10 - FIX.**
- Model MUSTs: 1) vent core `LAVA` to `ROSE` at line 196; 2) Neck3 ring off, Neck2 band 0.70-0.80 (line 287), drop the Neck3 spike if it still reads as a band.
- Clip MUST: 3) re-render walk game and side from the current export (`_cv_walk_game.png` is 03:42).
- Round-3 items that now pass: forehead red band (MUST 1), nostril pits (MUST 3), centre blade 0.34 (T2).
- Round-3 items still open: neck from above (MUST 2 partial), vents as legs (T1 fail, now MUST 1), eyes side-set (T3 partial, T-a).
