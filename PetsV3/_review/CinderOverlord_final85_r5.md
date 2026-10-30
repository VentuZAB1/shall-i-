**Model: 8.4/10 - FIX. Clips: 8.5/10 - PASS.**

Model is under the 8.5 bar. Round 4 was model 8.2 / clips 8.4. Both round-4 model MUSTs (vents, neck) are now PASS, and the stale walk render (clip MUST 3) is closed. The model still has two new blockers, both about the gold hero, found on this pass.

# Cinder Overlord - FINAL 8.5 GATE, ROUND 5 (fresh reviewer, 2026-10-28)

## 0. What I looked at

- Brief: `_review/GLACIER_REVIEWER_BRIEF.md`. Round 4: `_review/CinderOverlord_final85_r4.md`.
- Builder notes: `CinderOverlord/MODEL_NOTES.md` (FINAL 8.5 ROUND 4, exported 05:00), `CLIP_NOTES.md`, `_scratch/export_r4.txt`, `_scratch/gold_windows_r4.txt`, `_scratch/game_icon_out.txt`, `_scratch/ang_r4.txt`, `_scratch/clipgate_r4.txt`.
- Owner rules: `_review/GLACIER_CONCEPTS.md` (OWNER DECISIONS; the Cinder row, line 46; "it beats the 1 % secrets too", line 29). Plan tier: `_review/CinderOverlord_plan.md`, section 0 and the palette table.
- Images (renders folder, newest set, title bars 05:00):
  - `close_front.png`, `_close_sheet.png`, `gamelook_game.png`, `flat_game_stamped.png`
  - `_cv_walk_game.png`, `_cv_walk_side.png`, `_molt_r4_front.png`, `_molt_r4_side.png`
  - `_model_sheet.png`, `_pose_tq_sheet.png`
  - `_icons_strip_64.png`, `_icons_strip_128.png`, `_icons2_strip_128.png`
- All images opened without error.
- **Freshness check (file times):** `_scratch/fix_r4.py` 04:56:17; `renders/_cv_walk_game.png` / `_cv_walk_side.png` / `close_front.png` / `gamelook_game.png` 05:00:44; `_scratch/export_r4.txt` 05:00:27; `C:\cdimp\CinderOverlord.fbx` 05:00:26. The renders postdate the last edit and the export.
- **Zoom limit:** PIL is not installed here, so I could not make the 3x crops that round 4 used. Neck and vent calls below are from the native 600 px renders. Treat them as judged, not zoom-verified.
- **Tier note:** the task brief calls Cinder "mythic". The binding plan and concepts file say **Ultra-rare, 0.5 %** (beaten only by the 0.1 % mythics), and the owner rule says it must beat the 1 % secrets. I scored it against the ultra-rare bar. If the owner means mythic, the bar is higher and this model would not pass.
- **Not re-scored (already ruled or accepted):** body is ember red (not the plan's plum #B684AC) and vents are cold blue (not ROSE #FF6096). Both come from earlier coordinator and lead rulings. Lead ruling this round: cold-blue vents are accepted.

## 1. Round-4 items

| Item | Result | Evidence |
|---|---|---|
| MUST 1 vents read as centipede legs | **PASS** | `gamelook_game.png` and `_cv_walk_game.png`: one deep-blue slash per segment side, six per side. No pale rung stripe. No pair reads as a leg pair. Walk f0-40 shows no vent pair breaking the silhouette. Caveat: the slashes still sit on the dark ring bands, see TO 9+ (worm read). |
| MUST 2 neck from above: one full band | **PASS** (native res) | `gamelook_game.png`: one full dark band under the head (Neck1) and one thin band below it (Neck2). The dorsal spikes read as spikes, not bands. |
| MUST 3 walk renders current | **PASS** | `_cv_walk_game.png` / `_cv_walk_side.png` 05:00:44, after the 04:56 edit and the 05:00 export. Title bars read 05:00. |
| T-a eyes at y -0.86 | **PARTIAL** | `close_front.png`: the blue slits sit under the brow shelves at the outer skull sides (about x 160-235 and 340-420 of 600), partly outside the skull outline. Moved 0.03 as asked, but from the front they still read side-set, not front-set. |
| T-b snout tip flatter | **PARTIAL** | `_close_sheet.png` side view: the tip is flatter. From the front, a round studded chin bulb sits under the nose (about y 490-540 of 622) and reads pig-like. Nostril pits are small dark squares, not eyes. |
| T-c molt blades lift 50 deg | **PASS** (modest) | `_molt_r4_front.png`: the outer blades visibly splay at f34-40 against f0. `_molt_r4_side.png`: the blades rise f22-34. Still small at 5 studs. |
| T-d idle breath | not scored | Studio check (lead ruling). |
| T-e vent pairs | **PASS** | Applied: one slit per pair, six per side. |

Other checks:
- Pose sheet (`_pose_tq_sheet.png`): idle, walk, roar and molt beats all show. No floating or intersecting parts seen.
- Molt side and front: the crest lifts one blade at a time and reseats. The roar opens the jaw clearly.
- Tris 10,228 (PASS, cap 15k). Collision-free true; ground -0.006; linear 0; loops 0 / 0 (`_scratch/export_r4.txt`).
- Gold windows (`_scratch/gold_windows_r4.txt`, `game_icon_out.txt`): portrait 36, game 28 on the kit counter. Both are above the 25-px rim gate on that window.

## 2. Scores

**Model 8.4/10 - FIX.**
- Holds: a clear fierce ember serpent with a readable gold crest at 64 px. The vents and neck from round 4 now pass. Eyes read as blue slits under heavy brows, with no glints. No stray parts.
- Blocks 8.5: (1) the gold hero is partly lemon, not the plan's gold; (2) the Cinder does not visibly outclass the 1 % secrets at icon size, which is a binding owner rule.

**Clips 8.5/10 - PASS.**
- Holds: the walk renders are current and show no vent-leg rungs in motion. The molt reads from front and side, and the roar is clear. Collision-free, ground -0.006, linear 0, loops closed. Neck max 7.5 deg per bone and spine 4.5 deg (builder numbers). Stride closed by the lead.
- Not blocking: T-d breath is a Studio check. Slither motion is judged from stills only.

## 3. New MUSTs (block 8.5)

**MUST 1 (model): the gold hero clips to lemon.** The crest's lit faces hit lemon (255,255,99), about H 60. The builder's r6 note counts 59 such pixels at 64 px in the kit portrait. The gold gate's window (H 29-58) does not count them, so 36 gold pixels understates the lemon and overstates amber gold. The plan's GOLD is #FFC432 (255,196,50), about H 42. In `close_front.png` the crest reads yellow, not amber.
- Fix: cap the crest's lit faces to the plan gold hue, H 42-50. Lower the gold material's emission or specular, or its base G channel, so no flat face goes above H 50. Recount with `game_icon.py` using window H 29-60 and report the histogram. Both portrait and game gold must stay at 25 or more.
- Pass: no more than 10 px at H 59-60 in the 64 px kit portrait. The crest reads amber in `close_front.png`.

**MUST 2 (model): the Cinder must outclass the 1 % secrets at icon size.** Owner rule (`GLACIER_CONCEPTS.md` line 29): "it beats the 1 % secrets too". In `_icons_strip_64.png` and `_icons_strip_128.png` the Cinder is a long, low, red-brown worm. It spans the frame width but fills only about half its height. Thunder Rex (blue) and Cosmic Leviathan (purple) read bigger and higher-contrast at both sizes. The gold crest is small against the dark slate. This is my visual judgement, not a pixel count.
- Fix: raise the icon's visual mass. The non-background bounding box of the 64 px portrait must fill at least 70 % of the frame height, up from about 50 %. Do this with the icon pose or camera (a higher camera, or a more upright S-curve in the icon pose), not by changing the body. Keep the whole body in frame. Recheck that the 64 px portrait still has 25 or more gold pixels.
- Pass: in `_icons_strip_64.png` the Cinder fills at least 70 % of the frame height and reads at least as strong as Thunder Rex at 64 px.

## 4. TO 9+ list (polish, not blocking)

- **T-a eyes still side-set.** In `close_front.png` the slits extend outside the skull outline. Shorten the outer ends of the slits, or move the sockets about 0.02 toward the midline, and judge from the front.
- **T-b chin bulb.** The studded lower-jaw bulb under the nose reads pig-like from the front. Shrink its stud coverage by about 15 %, or flatten its front face.
- **Worm read at player distance.** In `gamelook_game.png` and `_cv_walk_game.png` the body reads as a segmented worm: a dark ring band on almost every segment. Consider dropping every second band on Body2-4 and Tail1-3, as in the round-6 M1 approach. Judgement, not a brief rule.
- **Molt at distance.** The blade fan is modest at 5 studs. A 55 deg outer lift, with a collision re-test, would read more clearly. Keep the reseat slower than the rise.
- **Breath (T-d).** Confirm in Studio that the 4.5 deg per-bone breath reads from about 5 studs.

## 5. Pass / fail checklist

| # | Check | Result |
|---|---|---|
| 1 | Tris <= 15k (10,228) | PASS |
| 2 | Species reads at 64 px | PASS |
| 3 | Gold rim >= 25 px on the kit window (36 / 28) | PASS on count; **FAIL on hue** (MUST 1) |
| 4 | Gold is gold, not lemon | **FAIL** (MUST 1) |
| 5 | Outclasses the 1 % secrets at 64 px (owner rule) | **FAIL** (MUST 2, judged) |
| 6 | Neck from above reads as one full band plus one thin | PASS (native res) |
| 7 | Vents read as slits, not legs | PASS |
| 8 | Eyes read fierce from the front | PARTIAL (T-a) |
| 9 | Snout tip smooth | PARTIAL (T-b) |
| 10 | Body colour distinct at 128 px | PASS |
| 11 | Walk renders current | PASS |
| 12 | Molt legible from the front | PASS (small at distance) |
| 13 | Roar | PASS |
| 14 | Collision-free, ground, linear, loops | PASS (builder numbers) |
| 15 | Pose limits (neck, spine, head) | PASS (builder numbers) |
| 16 | Breath in motion (T-d) | not scored (Studio) |

## 6. Summary

- **Model 8.4/10 - FIX. Clips 8.5/10 - PASS.**
- Round-4 MUSTs pass: vents (1), neck (2), walk renders (3). Eyes and snout improved but remain partial (T-a, T-b).
- Model MUSTs: 1) gold lemon: cap the crest's lit faces to H 42-50, recount with window H 29-60; 2) outclass at 64 px: the Cinder's icon must fill at least 70 % of frame height.
- Clip MUSTs: none.
- The cold-blue vents, the ember body and the lead-closed walk speed are not counted against the score.
