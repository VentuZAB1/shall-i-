# Cinder Overlord - FINAL 8.5 GATE, ROUND 3 (fresh reviewer, 2026-10-28)

**Model: 8.0/10 - FIX. Clips: 8.0/10 - FIX.**

Both are under the owner's 8.5 bar (PASS only at 8.5+). Model moved from 7.5 to 8.0. Clips held at 8.0; the open items are the Studio walk-speed check (C3) and the idle breath in motion.

## 0. What I looked at

- Brief: `_review/GLACIER_REVIEWER_BRIEF.md`. Round 2: `_review/CinderOverlord_final85_r2.md` (model 7.5, clips 8).
- Builder notes: `CinderOverlord/MODEL_NOTES.md` (FINAL 8.5 ROUND 2 section), `CLIP_NOTES.md` (FINAL 8.5 ROUND 2), `ANIM_REFS.md` (section D), `_scratch/gate_f85.json` (the only gate file).
- Source checked for exact numbers: `pets/CinderOverlord.py` (03:39), lines 188-195 (vent bar), 285-288 (neck rings), 311/314 (vent offset), 338-346 (skull cap), 354-355 (nostril pits), 373-400 (eyes, brows, crown mount).
- Renders, all from the newest set (03:39-03:43 on 2026-10-28; FBX `C:\cdimp\CinderOverlord.fbx` 03:42):
  - `_model_sheet.png`, `_close_sheet.png`, `close_front.png`
  - `gamelook_game.png`, `gamelook_tq.png`, `flat_game.png`, `flat_side.png`, `model_back.png`
  - `_icons_strip_64.png`, `_icons_strip_128.png`, `_icons2_strip_128.png`
  - `_pose_tq_sheet.png` (26 beats), `_molt_r4_front.png` (14 beats), `_cv_walk_game.png` (f0-40), `_cv_roar_front.png` (f0-58)
- Not opened: `_molt_r4_side/tq.png`, `_cv_walk_side.png`, `_cv_molt_front.png`, `_icons2_strip_64.png`. All images loaded.
- Not verified by me: the gold pixel counts. PIL is not installed here, so I could not re-count. I used the builder's recorded numbers in `gate_f85.json` (kit 33 / 21, rendered 30 / 10). Idle breath in motion and walk speed in Studio cannot be judged from stills.

## 1. Round-2 items

| Item | Result | Evidence |
|---|---|---|
| R2-M1 neck bands (game view) | PARTIAL | The letter is met: full rings on Neck1 and Neck3, Neck2 narrowed to 0.62-0.80, chest ring gone (code lines 285-288). But `gamelook_game.png` and `flat_game.png` still show two full-width dark bands on the neck plus one thin band, and the neck still reads as a segmented column from above. See MUST 2. |
| R2-M2 brows | PARTIAL | The brows now pass the horn test: they are short, low blocks over the eyes and their outer ends do not reach the crown (`close_front.png`). The forehead does not: the obsidian skull cap (code lines 338-346, stations to 0.78, running to the snout) is a dark plate from the crown base down to the nostril line. In `close_front.png` (x 240-360, y 215-345) there is no red skull between the brows and the crown in the centre. Red shows only on the flanks. See MUST 1. |
| R2-M3 vents (+15 % long, 4 deg up, clear of pale) | PASS | Code: `vl *= 1.15`, angles 32 / 148 (was 28 / 152). `_model_sheet.png` (bottom-left) and `flat_side.png` show the slits above the cream belly. In `_icons_strip_128.png` the blue flank bars read clearly next to the Phoenix. |
| R2-M4 gold, both portrait windows >= 25 | PASS (recorded) | `gate_f85.json`: kit counter 33, rendered window 30 (both >= 25). Game view 21 / 10 is not required. Not re-counted by me (see section 0). |
| T-a snout stud dots | PASS | The snout tube is `nostud=True`. The snout tip in `close_front.png` and `_close_sheet.png` (side) is smooth. Studs remain on the lower jaw and chin, which is acceptable. |
| T-b tail length | PASS | Tail4 shortened; stride 5.009 BU per 48 f in `gate_f85.json`. The tip reads tapered in `gamelook_tq.png`. |
| T-c idle breath (from 5 studs) | UNVERIFIED | 4.5 deg per neck bone (limit 8); idle loop 0 / 0 and collision-free in `gate_f85.json`. Motion cannot be judged from stills. Not a fail. |
| Body colour (176,72,54) at 128 px | PASS | In `_icons_strip_128.png` Cinder stays ember-red. It does not drift to Ivonrath's purple-crimson or to the Phoenix's orange, and the silhouettes separate it further. |
| Molt legible from the front (clip C1) | PASS | `_molt_r4_front.png`: the outer blades visibly fan at f34-40 against f0. Small at game distance, but readable in the sheet. |
| Roar (clip) | PASS | `_cv_roar_front.png`: neck gathers, crown flares, jaw opens at f30 and f44. |
| Reference disclosure (C2) | PASS | `ANIM_REFS.md` section D names Haku (*Spirited Away*, Sakugabooru #225387), gives tags and frame ranges, and states plainly that he is a flying dragon. The Wikimedia snake study (S1, S2) is cited with times and frames. The animationreference.org search is logged. |
| Walk speed in Studio (C3) | OPEN | Not a lead-exempt item. Still needs a Studio follow test. See MUST 4. |

## 2. Scores

**Model 8.0/10 - FIX.**
- Holds: a clear, fierce serpent silhouette; the gold five-blade crest as the hero (readable at 64 and 128 px); a palette that follows the plan; cold-blue vents and belly accepted by ruling; the crest on a black mount with blue tips; no stray or floating parts in the views.
- Blocks 8.5: the dark forehead plate (MUST 1), the neck still banded from above (MUST 2), and the two central nostril pits, which read as small beady eyes between the brows (MUST 3).

**Clips 8.0/10 - FIX.**
- Holds: the molt reads from the front, the roar is clear, the reseat is slower than the rise (7.47 vs 5.80 deg/f outer, 5.18 vs 3.17 centre), the idle and walk loops close (0 / 0), collision-free with ground min -0.006, linear 0, neck and chest limits met on the builder's numbers, and the renders are current.
- Blocks 8.5: C3 (walk speed in Studio) is still open. The recorded stride is 5.009 BU per 48 f (1.6 s at 30 fps). At 4.70 studs/BU (10.5 studs / 2.232 BU) that is about 23.6 studs per 1.6 s, or about 14.7 studs/s. Nobody has checked that against the pet's real follow speed.

## 3. MUST list (blocks 8.5)

**MUST 1. Forehead plate (R2-M2 unfinished).** `pets/CinderOverlord.py` line 338: the skull-cap stations are `(0.03, 0.08, 0.18, 0.30, 0.42, 0.54, 0.66, 0.78)`. Remove `0.66` and `0.78`, so the cap ends at station `0.54` (the eye line, about y -0.80) and not at the nostril line. Keep the brow blocks as they are.
- Pass: in `close_front.png`, a red band of skull at least as tall as one brow block shows between the two brow blocks and the cap's lower edge, and the dark area stops at the brow line.

**MUST 2. Neck from above (R2-M1 unfinished).** `pets/CinderOverlord.py` lines 285-288. Change `if i in (2, 4):` to `if i == 2:` (only Neck1 keeps a full ring), and change `elif i == 3:` to `elif i in (3, 4):` so Neck3 takes the narrow 0.62-0.80 band.
- Pass: `gamelook_game.png` and `flat_game.png` show at most one full-width dark band on the neck. The narrow bands stay visible but no longer read as rings.

**MUST 3. Nostril pits read as eyes.** `pets/CinderOverlord.py` lines 354-355: the pits are `surf_hit(... (s * 0.042, -1.035, 2.4) ...)` with size `(0.010, 0.005, 0.016)`. Shrink to `(0.006, 0.004, 0.009)` and move the start point forward to `y = -1.07`, toward the snout tip.
- Pass: in `close_front.png` the two blue slits at the skull sides are the only eyes. The centre pits are small and sit on the snout top. No dark squares sit in the eye line between the brows.

**MUST 4 (clips, C3). Walk speed in Studio.** Run the pet at its real follow speed in Studio and check the 48-frame slither does not skate. Write the measured speed beside the stride (5.009 BU per 48 f, about 14.7 studs/s by the numbers above) in `CLIP_NOTES.md`.
- Pass: no visible skating in the Studio follow test, and the number is written down. If it skates, match the travel to the measured speed. Do not add a new clip.

## 4. TO 9+ list (polish, not blocking)

- **T1 vent "legs" from the game camera.** The six pairs of blue bars stand off the flank, and with the dark rings they read as a centipede's legs in `gamelook_game.png` and `_cv_walk_game.png`. The vent bar sits at depth 0.012 (line 195) and the vent loop uses `off=0.004` (lines 311 and 314). Try `off=0.000` and a bar depth of 0.006, so the blue sits flush. Judge in `gamelook_game.png`. This is the first thing to check in Studio.
- **T2 mythic mass at 128 px.** In `_icons_strip_128.png` the Cinder reads with the same visual weight as Ivonrath and smaller than Golem, Boar and Rex. The crest carries the hero read. Option: centre blade 0.32 to 0.34 (re-run the molt collision test first).
- **T3 eyes set on the skull sides.** The blue eye slits sit at the outer edges of the skull (`ep` at x +/-0.6, lines 373-376). From the front they read as side-set eyes. Option: move them about 0.03 toward the nose.
- **T4 idle breath in motion.** Confirm the 4.5 deg per neck bone breath reads from about 5 studs in Studio.

## 5. Pass / fail checklist

| # | Check | Result |
|---|---|---|
| 1 | Tris <= 15k (10,688) | PASS |
| 2 | Species reads at 64 px | PASS |
| 3 | Gold hero, both portrait windows >= 25 | PASS (recorded, not re-counted) |
| 4 | Brows do not read as horns | PASS |
| 5 | Red skull between brows and crown | FAIL (MUST 1) |
| 6 | Neck from above reads as one column | PARTIAL (MUST 2) |
| 7 | Face: eyes read, no beady centre marks | FAIL (MUST 3) |
| 8 | Vents clear of the pale belly, 15 % longer | PASS |
| 9 | Snout tip smooth, no stud dots | PASS |
| 10 | Body colour distinct at 128 px | PASS |
| 11 | Clip: molt legible from the front | PASS |
| 12 | Clip: roar | PASS |
| 13 | Clip: reseat slower than rise | PASS |
| 14 | Clip: renders current | PASS |
| 15 | Clip: reference disclosure (C2) | PASS |
| 16 | Clip: neck, spine and head limits, loops, ground, collision | PASS (builder numbers, not re-run) |
| 17 | Clip: walk speed in Studio (C3) | OPEN (MUST 4) |

## 6. Summary

- Model 8.0/10 - FIX. Clips 8.0/10 - FIX.
- MUSTs (model): 1) cut the skull cap at station 0.54 so red skull shows between brows and crown; 2) narrow the Neck3 ring to 0.62-0.80; 3) shrink and move the nostril pits to the snout tip.
- MUST (clips): 4) record the Studio walk speed against the 5.009 BU / 48 f stride.
- Round-2 items that passed: vents, gold (recorded), snout tip, tail length, body colour, reference disclosure, molt and roar.
- The 9+ list is four polish items, led by the blue vent bars that read as legs from the game camera.
