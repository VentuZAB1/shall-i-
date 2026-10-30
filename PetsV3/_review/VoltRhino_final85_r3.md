# Volt Rhino - FINAL 8.5 GATE, ROUND 3 (2026-10-28) - FIX

**Model: 8.3/10 - FIX. Clips: 8.4/10 - FIX.**

Both are under the 8.5 floor. Round 3 fixed the back seam (MM1), the flank palette (T-a), the brow nub (T-b), the thigh tris (T-f), the rebound (T-d) and the icon timing (MM4). What still blocks 8.5: the chin is still a flat pale plank with a white sliver at the snout tip (MM2 not met), the eye slit does not resolve at 64 px (MM3 not met), and the idle stamp is still not a readable beat at phone scale (MC1 not met).

## What I looked at
- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round 2 `_review/VoltRhino_final85_r2.md`; builder notes `VoltRhino/MODEL_NOTES.md` and `CLIP_NOTES.md` (both "Final gate round 2" sections), `ANIM_REFS.md`, `_scratch/verify.json` (04:07), `_scratch/export_result_f85r2.txt` (04:09), `_scratch/feet_taps_f85r2.txt` (04:02).
- Code, read only: `pets/VoltRhino.py` (last saved 04:06:07): FLANK (line 21), FLANK tubes (233-234), fold wedges (245), Jaw chin seg (286), pale strip loop (292-299), MOUTH block (about 300-301), eyes (320), brow nub spike (364), thigh lofts `seg=12` (373, 376), snort (515-516), idle FL lift (530), act rebound keys (616-624), rump tuple (137).
- Renders, all from the final set (titles read 04:06 for the .py; files 04:07 to 04:09; icon 04:09:13 is newer than `VoltRhino_portrait_raw.png` 04:09:11):
  - `_model_sheet.png` (tq, front, side, back, game, under), `_close_sheet.png`, `_chin_sheet.png` (closeb_cbelow, closeb_cside2, pclose_side_roar_28, pclose_below_roar_28), `under.png`, `_flat_sheet.png`.
  - `_icons_strip_64.png`, `_icons_strip_128.png`, `VoltRhino_icon.png`.
  - `_idle_stamp.png` plus full-size `beat_f85_ir_side_idle_030.png`, `_038.png`, `_046.png`.
  - `_beats_f85_ir_side.png` and `_tq.png` (idle and roar), `_beats_f85_wa_side.png` and `_tq.png` (walk and act).
- Limits: no PIL or ImageMagick, and reviewers read files only, so I could not crop, zoom or count pixels. The 64 px judgement is from the displayed strip. Pixel estimates for the foot lift are my visual estimates in the 360 px frames. I did not open animationreference.org; the citation is judged from `ANIM_REFS.md`. The palette shares are the builder's numbers, checked by eye against `_flat_sheet.png`.

---------------------------------------------------------------------------------------------------------------------
## 1. Model score: 8.3/10 - FIX
- Gains over round 2 (8.1): the back reads as one armour step (MM1), the flanks sit a step darker than the legs and head (T-a), the brow nub is a short spike (T-b). The silhouette still reads at 128 px next to the other Thunder pets.
- Still open: the chin reads as a light plank from below and at the open jaw (MM2); the eye slit does not show at 64 px (MM3). Both are direct misses on the round-2 goals.

## 2. Clip score: 8.4/10 - FIX
- Gains over round 2 (8.2): the strike rebound is 6 degrees with the spine recoil (T-d), and the roar pump is 3 degrees with the head + neck held at 15 (T-e). Numbers are clean: neck max idle 2.06 / walk 2.48 / roar 6.5 / act 6.0 (limit 8); chest vs spine 0.72 / 2.09 / 1.0 / 3.8 (limit 5); head pitch-up roar 16.0, act 16.0 (limit 30); one-shots end at rest 0.0; ground_min_z idle 0.000, walk -0.002, roar 0.000, act -0.008; collision_free true; loops closed; walk slide 0; idle foot drift 0.
- Still open: the idle stamp (MC1). The lift is 0.060 (line 530), but the frames do not show it at phone scale. The idle is the first clip a player sees, so this stays a blocker.

---------------------------------------------------------------------------------------------------------------------
## 3. Round 2 items

### Round 2 MUST

**MM1. Back: one junction line, not two: PASS.**
- Line 137 is now `(0.40, 0.93, "Spine", 0.06, 0.06, 0.032)`, so the rump starts where the saddle ends.
- `model_game`, `model_back`, `model_side` and `flat_side` show one saddle-to-rump step across the middle. There is no second overlapping band.

**MM2. Chin: a thin strip, no flat face, no white tip: PARTIAL (goal not met).**
- Improved: the pale underside is narrower than in round 2, and the throat strip now runs on from it.
- Not met:
  - the separate chin seg is still on the Jaw (line 286, `B.seg((0,-1.00,0.825),(0,-1.65,0.762), 0.080, 0.026, PALE, "Jaw", ...)`);
  - `under.png` shows a light, hard-edged rectangle on the underside of the head;
  - `closeb_cbelow` shows the strip with squared ends;
  - `closeb_cside2` shows a thin white sliver along the front edge of the snout;
  - `pclose_below_roar_28` shows the open jaw as a flat, angular pale plank, and the throat strip reads as a pale collar.

**MM3. Eye slit longer, and it reads at 64 px: PARTIAL.**
- PASS in close-ups: `close_side` and `close_tq` show a clear lime bar in a black socket under the brow, longer than round 2 (VOLT 0.110, BLACK 0.118 at line 320).
- FAIL at 64 px: the eye does not resolve as a line in `_icons_strip_64.png` for me. At most a faint mark in `_icons_strip_128.png`. At this scale the slit is about 1 px.

**MM4. Process: icon, strips, feet at taps: PARTIAL.**
- PASS on the icon: `VoltRhino_icon.png` 04:09:13 is newer than `VoltRhino_portrait_raw.png` 04:09:11, and both strips are 04:09:13.
- PASS on the horn tip: `verify.json` Horn_Tip on the holds 0.0078 / 0.0079 (tap1 and tap2 hold), 0.0076 / 0.0079, 0.0035 / 0.0035 (tap3), all under 0.010.
- PARTIAL on the feet: `_scratch/feet_taps_f85r2.txt` is 04:02:52, about 3 minutes before the final `pets/VoltRhino.py` save at 04:06:07. The only current evidence is step 1 `ground_min_z` act -0.008, which is good but does not log the soles at f30, f42 and f54.

**MC1. Idle foot stamp readable at phone scale: FAIL.**
- The number changed: line 530 is `0.060 * math.sin(math.pi * u) ** 0.8` (from 0.032). The window f30 to f46 and the stamp at f46 (0.383) are unchanged.
- The render does not show it: `beat_f85_ir_side_idle_030` against `_038` (peak) and `_046`. At 360 px the front-left sole is only a few pixels higher at f38 than at f30, and f46 looks the same as f30. The lift is about 0.06 units, which is about 0.32 studs; at this frame scale that is roughly 5 px.
- Other feet planted: PASS (idle_foot_drift 0).

**C1 (idle reference), C3 (act strikes), limits, end at rest, no glow, tris: PASS.**
- C1: `ANIM_REFS.md` cites `/tags/elephants` with the no-fit notes; the weight shift moves off the lifting foreleg.
- C3: holds 2 frames at f30-31, f42-43, f54-55; rebounds at f33, f45, f57 (line 616-624); tap 3 deeper by 2.5 degrees with the cheek clear.
- Tris 14,248 (`export_result_f85r2.txt` tris_body); glow list empty.

### Round 2 TO 9+

- **T-a (flanks):** PASS. `FLANK = (126,134,150)` (line 21) on the Chest and Spine tubes only (lines 233-234); legs and head stay IRON. `flat_side` shows the flanks a step darker. The builder gives IRON_D 41.6 % side, above the 25 % gate.
- **T-b (brow nub):** PASS. Line 364 `B.spike((0,-1.22,1.11),(0,-0.40,1.0), 0.12, 0.050, HORN_IVORY, ...)`: the 0.12 is the length (the call takes a direction and a length).
- **T-c (idle snort 4 degrees):** PASS on the code (lines 515-516 `4.0 * sn`). Not readable at phone scale in the idle f70 and f72 frames. Moved to TO 9+.
- **T-d (act rebound 6 degrees + 1.5 recoil):** PASS. Lines 616, 620, 624 (`HT - 6.0`, `-1.5` spine). The head lifts off the snow at f33, f45 and f57 in the act sheets, though it is still thin at phone scale.
- **T-e (roar pump 3 degrees):** PASS on the numbers (neck roar max 6.5; head + neck 15; pitch-up 16.0). Still small on screen.
- **T-f (thigh lofts 12 segments):** PASS. Lines 373 and 376 `seg=12`; tris 14,248.

---------------------------------------------------------------------------------------------------------------------
## 4. New MUSTs (only what blocks 8.5)

**MUST 1 (model): chin plank and white snout tip. Lines 286 and 292 of `pets/VoltRhino.py`.**
- Delete line 286 (the separate Jaw chin seg). It is the flat plank in `pclose_below_roar_28`.
- In the strip loop on line 292, change `(-1.06, -1.22, -1.38, -1.52, -1.64)` to `(-1.06, -1.22, -1.38, -1.52)`. The pale then stops about 0.1 short of the snout tip, so the white sliver in `closeb_cside2` goes.
- Acceptance: `under.png` and `closeb_cbelow` show no light plane with a straight hard edge on the head. `closeb_cside2` shows no white at the snout front. `pclose_below_roar_28` still shows a dark mouth interior when the jaw opens (the MOUTH block stays; keep the Jaw bone).

**MUST 2 (model): eye slit visible at 64 px. Line 320.**
- VOLT half-size `(0.009, 0.026, 0.110)` becomes `(0.009, 0.036, 0.110)`.
- BLACK socket `(0.011, 0.040, 0.118)` becomes `(0.011, 0.048, 0.118)`.
- Height to length of the lime slit goes from about 0.24 to about 0.33, so it stays a slit and not a bar.
- Acceptance: the lime line shows in `_icons_strip_64.png` (Volt first) at 1:1 and in `close_side`. Re-render the 64 and 128 strips and the icon from the new portrait (the MM4 rule).

**MUST 3 (clip): idle foot stamp readable. Line 530 of `pets/VoltRhino.py`.**
- `0.060 * math.sin(math.pi * u) ** 0.8` becomes `0.120 * math.sin(math.pi * u) ** 0.8`. That is about 0.65 studs at this scale (1 unit = 5.41 studs).
- Keep the f30 to f46 window and the stamp event at f46 (0.383).
- Optional, if a lift alone reads as a hop: add a 0.02 units body dip over the same window on the Root or Chest.
- Acceptance: in `beat_f85_ir_side_idle_038` (360 px) the front-left sole is at least 10 px above its f30 position. FR, BL and BR stay planted (idle_foot_drift 0). Re-run step 1: `ground_min_z` idle at or above -0.02, `collision_free` true.

Process note (score-neutral, but MM4 stays PARTIAL until it is done): after MUSTs 1 to 3, re-run `probe_feet.py` on the final file and save a new log, so the soles at f30, f42 and f54 come from a save newer than the last `pets/VoltRhino.py` change.

---------------------------------------------------------------------------------------------------------------------
## 5. TO 9+ (higher is better; these are the highest-impact extras)

- **T1 (snort, lines 515-516):** 4 degrees is not readable at phone scale. Make it 6 degrees on the head and 4 on the jaw.
- **T2 (roar pump, neck and head keys around lines 560-562):** 3 degrees is still small on screen. Try a neck pump of 5 degrees with the head tipping back 5 degrees, so head + neck stays 15 and pitch-up stays 16.
- **T3 (pale throat collar, line 281):** the pale throat band reads as a bib-like ring around the neck when the head is up (`pclose_below_roar_28`). Consider fading its rear end to IRON.
- **T4 (act taps 1 and 3):** they still look alike at phone scale. A 2 to 3 degree yaw difference on tap 1 would separate them.

---------------------------------------------------------------------------------------------------------------------
## 6. Pass / fail checklist (round 3)

| Item | Result | Evidence |
|---|---|---|
| MM1 one back step | PASS | line 137; `model_game`, `model_back`, `flat_side` |
| MM2 chin: strip, no flat face, no white tip | PARTIAL | line 286 still a chin seg; `under.png`, `closeb_cbelow`, `closeb_cside2`, `pclose_below_roar_28` (MUST 1) |
| MM3 eye longer | PASS | `close_side`, `close_tq`; line 320 |
| MM3 eye reads at 64 px | FAIL | `_icons_strip_64.png` (MUST 2) |
| MM4 icon from final portrait | PASS | icon 04:09:13 > portrait 04:09:11 |
| MM4 feet at taps re-logged | PARTIAL | `feet_taps_f85r2.txt` 04:02:52 predates the 04:06:07 save (process note) |
| MM4 horn tip values | PASS | `verify.json` 0.0078 / 0.0079 / 0.0035 |
| MC1 idle stamp readable | FAIL | `beat_f85_ir_side_idle_030` / `_038` / `_046` (MUST 3) |
| MC1 other feet planted | PASS | idle_foot_drift 0 |
| T-a flanks | PASS | line 21, 233-234; `flat_side` |
| T-b brow nub 0.12 | PASS | line 364 |
| T-c snort 4 degrees | PASS (code) | lines 515-516; not visible at phone scale (T1) |
| T-d rebound 6 degrees | PASS | lines 616-624 |
| T-e roar pump 3 degrees | PASS (numbers) | verify.json neck 6.5, pitch-up 16.0 |
| T-f thigh 12 segments, tris | PASS | lines 373, 376; tris 14,248 |
| C1 idle reference | PASS | `ANIM_REFS.md` |
| C3 holds and rebounds | PASS | `verify.json` holds; `_beats_f85_wa_*` |
| Limits (neck, chest, pitch-up, end at rest) | PASS | `verify.json` |
| Collisions, ground | PASS | step 1 collision_free true; ground min -0.008 |
| Tris at or under 15k | PASS | 14,248 |
| No glow | PASS | glow [] |
