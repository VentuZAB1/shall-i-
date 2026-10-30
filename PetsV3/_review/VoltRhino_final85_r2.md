# Volt Rhino - FINAL 8.5 GATE, ROUND 2 (2026-10-28) - FIX

**Model: 8.1/10 - FIX. Clips: 8.2/10 - FIX.**

Both are under the 8.5 floor (owner, 2026-10-28). Round 2 closed most of round 1: the rear hoop is gone, the legs are round, the T1 ridge and T2 saddle bolts are in, the lateral walk, strike holds, rebound and pose limits are all clean. What still blocks 8.5: the back still has a double armour edge across the middle (saddle rear and rump front overlap), the pale chin still reads as a flat plate from below, the eye slit does not read at 64 px, the idle foot stamp is not visible at phone scale, and the icon was written before the final portrait.

## What I looked at
- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round 1 `_review/VoltRhino_final85.md`.
- Builder notes: `VoltRhino/MODEL_NOTES.md` and `CLIP_NOTES.md` (both "Final 8.5 gate round" sections), `ANIM_REFS.md` (central and final85 C1 rows).
- Numbers: `_scratch/export_result_f85.txt` (01:37), `_scratch/verify.json` (01:38), `_scratch/full_step1.txt` (23:59, older step-1 run), `_scratch/feet_taps.txt` (00:00, predates the f85 tap changes).
- Code, read only: `pets/VoltRhino.py` (01:35:38): ARMOUR (lines 134-136), fold_wedge (156), armour bands and fold (241-247), bolts (248-267), spike ridge (268-277), chin (285), lip and mouth (288-293), eyes (300-315), brow nub (352), legs (361-373), idle (487-518), act rebound keys (599-612).
- Renders (all from the 01:35 file):
  - Model: `renders/_model_sheet.png` (01:37, title carries the time), `_close_sheet.png` (01:37), `_chin_sheet.png` (01:37), `_flat_sheet.png` (01:37; contains flat_side, flat_tq, flat_game), `_icons_strip_64.png` and `_128.png` (01:36), `model_game.png` (01:37), `under.png` (01:36), `VoltRhino_icon.png` (01:36:58), `VoltRhino_portrait_raw.png` (01:37:47).
  - Pose sheets: `_beats_f85_ir_side.png` and `_tq.png` (idle + roar), `_beats_f85_wa_side.png` and `_tq.png` (walk + act).
  - Single frames: `beat_f85_ir_side_idle_030.png` and `_046.png`, `beat_f85_wa_side_act_horntap_033.png`, `_042.png`, `_054.png`, `beat_f85_wa_side_walk_000.png`, `beat_f85_wa_tq_act_horntap_030.png`.
  - Idle references: `renders/ref_idle_elephant_overview.jpg`, `_1060-1320.jpg`, `_1130-1290.jpg`.
  - Old, used only for comparison: `renders/final/pclose_below_roar_28.png` (23:59).
- Not used: older sheets (`_horn_sheet`, `_jaw_roar_sheet`, `_final_jaw_throat`, `beat_act_*` from 10-27).
- Limits: no PIL or ImageMagick on this machine, so I could not crop or zoom, and I did not count pixels. Judgements are from the full-size and displayed frames. The palette shares are the builder's numbers, checked by eye against `_flat_sheet.png`. I did not run Blender, and I could not open animationreference.org (reviewers read files only).

---------------------------------------------------------------------------------------------------------------------
## 1. Model score: 8.1/10 - FIX

**Good:** the species reads at 64 and 128 px next to the other Thunder pets. The ivory horn with the lime zig is the hero at icon size and in `model_game`. The back is the darkest mass (IRON_D 65.0 % of the game view by the builder's final85 count, and the back is visibly the darkest part in `model_game`). The belly is a clean pale band. The legs are now round columns on round pads with black toenails (`under.png`, `model_side`), so the stacked-box read is gone. T1 spikes sit on the spine (`model_side`, `model_tq`). T2 saddle bolts are visible from the game camera (`model_game`, `model_side`). Tris 14,572 (cap 15k). Glow list empty.

**Costs:**
- The back still has a double armour edge across the middle. `model_game` and `model_back` show a second dark band at about y 0.36 to 0.40: the saddle's rear edge (line 135, y1 0.40) and the rump plate's front edge (line 136, y0 0.36, lower edge dropping to -0.30 height) overlap. This is the hoop the owner objected to, now as a double line.
- The pale chin still reads as a plate: `under.png` shows a flat pale rectangle on the underside of the head, and `_chin_sheet.png` `closeb_cbelow` a flat pale wedge with a dark recess above it. A thin white edge sticks out at the snout tip (`closeb_cside2`).
- The lime eye slit reads in `_close_sheet` (close_side, close_tq) and in the 512 icon as a lime bar under the brow. It does not read in `_icons_strip_64.png` (I cannot resolve the eye there).
- The flanks (IRON 146,154,168, about 37 % of the side) still read as light grey-blue in `close_tq` and `close_front`. That is the plan's palette, but it is the weakest part of "dark rich body".
- The ivory brow nub (line 352, a 0.21-long spike) reads as a white stray tooth on the forehead in `close_tq` and in the 512 icon.

---------------------------------------------------------------------------------------------------------------------
## 2. Clip score: 8.2/10 - FIX

**Good:** the numbers are clean and the acts read. `verify.json`: neck max idle 2.06, walk 2.48, roar 5.5, act 6.0 (limit 8); chest vs spine 0.72, 2.09, 1.0, 3.8 (limit 5); head pitch-up roar 16.0, act 16.0 (limit 30); end vs rest 0.0 on the one-shots; step 1 collision_free true; ground_min_z idle 0.000, walk -0.002, roar 0.000, act -0.008; loops closed; walk slide 0; idle foot drift 0. The walk is the lateral sequence (BL f0, FL f10, BR f20, FR f30). The strikes hold and rebound (see C3). The roar head lift reads with the jaw open in `_beats_f85_ir_side` (roar f20 to f36).

**Costs:** the idle is the weak clip, and it is the first clip a player sees. At phone scale the foot stamp and the snort do not show (C2, T3). The roar pulses are small (N3). The act's strike rebound is 4 degrees (correct to the brief, but thin).

---------------------------------------------------------------------------------------------------------------------
## 3. Round 1 checks (every item in `VoltRhino_final85.md`)

### Round 1 MUST

**M1. Re-render from the final file, regenerate the portrait: PARTIAL.**
- PASS: every sheet was re-rendered from `VoltRhino.py` (01:35:38). The time is in the title bar (`_model_sheet`: "rendered 2026-10-28 01:37 | VoltRhino.py 2026-10-28 01:35"). `flat_side/tq/game`, both icon strips (Volt first, then ThunderBull, Raiju, Thunderbird, ThunderRex, StormWyvern), `model_game` and `under.png` are all newer than the file.
- GAP: `VoltRhino_icon.png` is 01:36:58, but the export's raw portrait `VoltRhino_portrait_raw.png` is 01:37:47. So the icon was not written from the final portrait by timestamp. The two images show the same 3/4 pose and the same parts (the icon adds a black outline and a crop), so this is a traceability gap, not a visible one.

**M2. Back: three seams down to two, no full ring: PARTIAL.**
- PASS: the rear fold at y 0.405 is gone (line 245 comment, no third hoop in `model_game`). The fold wedge is 0.014 (line 156).
- FAIL on the target: the back still shows a double band across the middle (saddle rear at y 0.40, rump front at y 0.36, overlapping by 0.04 with the rump front dropping to -0.30). `model_game` and `model_back` read it as a second hoop-like ring.

**M3. Chin: no white slab: PARTIAL.**
- PASS on the slab: the old `pclose_below_roar_28.png` (23:59) shows a big white plank under the jaw. The new `_chin_sheet` shows much less pale.
- PARTIAL: `under.png` still shows a flat pale rectangle on the underside of the head, `closeb_cbelow` still a flat wedge, and `closeb_cside2` a thin white edge at the snout tip. The chin is still a separate capsule (line 285).
- The MOUTH lip (line 288) is narrower; the red dots are gone in `_chin_sheet`.

**M4. Eyes read at 64 px: PARTIAL.**
- PASS in the close-ups: the lime slit is larger (VOLT half-size 0.009 x 0.026 x 0.092 and socket 0.011 x 0.040 x 0.100, line 308). `close_side` and `close_tq` show a clear lime bar on a black socket under the brow. The slit is still narrow (height/length about 0.28).
- FAIL at 64 px: I cannot see the eye in `_icons_strip_64.png`.

**M5. Legs: no stacked boxes: PASS.**
- `under.png`: round thighs and shins on round pads with black toenails, no stacked tiers. `model_side` and `beat_f85_wa_side_walk_000.png` show round columns with a hock flowing from the shin (lines 361-373).
- Step 1 is collision_free true and ground is clean.

### Round 1 NICE

- **N1 (IRON_D 76,84,102):** PASS (line 18). The back is the darkest part in `model_game`.
- **N2 (IRON 146,154,168):** PASS on the value (MODEL_NOTES). The flanks still read light grey-blue in the close-ups (see TO 9+).
- **N3 (roar pump):** PASS on the numbers. The neck max is 5.5 at bellow1 (verify.json). The pump is only 2 degrees, so it is small at phone scale (TO 9+).

### Round 1 clip MUSTs

**C1. Idle has an animationreference.org reference: PASS (citation accepted).**
- `ANIM_REFS.md` (final85 C1 row) and plan section 10 cite `/tags/elephants`, "Video by projectarcheology", 10.6 to 13.2 s, with the no-fit note for `/tags/animals` and `/tags/creature-animation`.
- The contact sheets (`ref_idle_elephant_1130-1290.jpg`, `_overview.jpg`) show an adult standing with a calf. At 12.0 to 12.3 s the body leans onto the other legs, and at 12.3 to 12.6 s the near foreleg lifts low and plants, as the builder says.
- The rig's weight shift now moves off the lifting leg (line 'sw = pk.wave(f, n, 0.433, 1)'). That matches the reference.
- Caveat: the citation comes from the tag page's preview video, not the clip page. I could not open the site to check it.

**C2. Idle renders are current: PARTIAL.**
- PASS on the renders: `_beats_f85_ir_side.png` and `_tq.png` at 01:36, from the 01:35 file. Frames f0, 30, 38, 46, 60, 70, 72, 90, 120 (plus roar frames). The three other feet stay planted (idle_foot_drift 0).
- FAIL on the stamp: `beat_f85_ir_side_idle_030.png` and `_046.png` look the same at 360 px. The left-fore lift is 0.032 units at its peak (line 518), which is about 0.17 studs at this scale (1 unit = 8.69 / 1.605 = 5.41 studs). The stamp is not a readable beat.

**C3. Act strikes read as strikes: PASS.**
- Holds (verify.json, `Horn_Tip` z on the hold frames): tap1 f30-31 0.0078 / 0.0078, tap2 f42-43 0.0076 / 0.0079, tap3 f54-55 0.0035 / 0.0035 (limit 0.010). Ground min -0.008 (limit -0.02). The feet stay on their rest points (per the builder; `feet_taps.txt` is from 00:00 and was not re-logged after the f85 change).
- Rebound: f33, f45 and f57 (line 604 to 612, head HT - 4.0 degrees). `beat_f85_wa_side_act_horntap_033.png` shows the head lifting off the snow after the strike.
- Tap 3 deeper by 2.5 degrees with the neck reaching 0.045 forward. Tap 2 drags the horn sideways in its hold. Visually taps 1 and 3 look alike at phone scale. That is within the brief.
- Limits: neck max 6.0, chest vs spine 3.8, pitch-up 16.0. All in bound.

### Round 1 clip NICE and TO 9+

- **N3 (roar pulses):** PASS on the numbers, small at phone scale (see above).
- **T3 (idle snort):** PARTIAL. The snort is at f70-73 (line 492), 2 degrees on the head and 2 degrees on the jaw (lines 503-504). It is not visible at phone scale in `_beats_f85_ir_side` idle f70 and f72.
- **T1 (back ridge, three spikes):** PASS. The spikes are visible on the spine in `model_side` and `model_tq` (lines 268-277). They are small and dark.
- **T2 (saddle volt bolts):** PASS. One bolt per side of the saddle, visible from the game camera in `model_game` (lines 261-267).

### Round 1 checklist (section 6 of round 1), items that changed

- #7 palette shares: PASS. Builder's shares: IRON_D 43.4 % side, 65 % game. The dark back covers the body in `_flat_sheet.png` and above 25 %.
- #14 renders match the final export: PASS for the sheets, PARTIAL for the icon (M1).
- #21 idle renders current: PASS (01:36), with the stamp caveat in C2.
- #22 animation refs: PASS on the idle row (C1).

---------------------------------------------------------------------------------------------------------------------
## 4. New MUSTs (only what blocks 8.5)

### Model

**MM1. Back: one junction line where the saddle meets the rump (not two).** Line 136, the rump tuple:
- Change `(0.36, 0.93, "Spine", -0.30, 0.06, 0.032)` to `(0.40, 0.93, "Spine", 0.06, 0.06, 0.032)`.
- The rump's front edge then starts where the saddle's rear edge ends (y 0.40, lower-edge fraction 0.06), so the back has one step there, not an overlapping pair with the rump's front dropping to fraction -0.30.
- Check: `model_game` and `model_side` show the shield edge and one saddle-to-rump step on the back, with no second band. The rump bolts (y 0.50 to 0.74) are unaffected.
- Re-run step 1 (collision_free true).

**MM2. Chin: a thin strip, not a flat plate.** Line 285, the chin segment:
- Radii `0.10, 0.040` to `0.080, 0.026`, and raise both end centres by 0.02 (z 0.785 to 0.805 at y -1.00, and 0.722 to 0.742 at y -1.65), so the top is buried in the head loft and only a 0.01 to 0.015 pale strip shows.
- Goal: no flat face in `under.png` or `closeb_cbelow`, and no white tip at the snout in `closeb_cside2`.
- If a flat face still shows after this, delete line 285 and use `Lh.band(B, Lh.s_at_y(-1.10), Lh.s_at_y(-1.62), PALE, "Jaw", zlo=-1.0, zhi=-0.55, grow=0.008, step=0.05)`, the same method as the throat band on line 280. Keep the Jaw bone so the mouth still opens.

**MM3. Eye slit reads at icon size: longer, not taller.** Line 308:
- VOLT half-size `(0.009, 0.026, 0.092)` to `(0.009, 0.026, 0.110)`.
- BLACK socket `(0.011, 0.040, 0.100)` to `(0.011, 0.040, 0.118)`.
- Height/length about 0.24 (still narrow, still fierce).
- Check: the lime line is visible in `_icons_strip_64.png` (Volt first) and in `_close_sheet` close_side.

**MM4. Process re-checks.** No geometry change.
- Regenerate `VoltRhino_icon.png` from the final `VoltRhino_portrait_raw.png` (01:37:47) after MM1 to MM3, and re-make `_icons_strip_64.png` and `_128.png`.
- Re-log the foot z at f30, f42 and f54 from the current file (the only foot log is `feet_taps.txt`, 00:00).

### Clips

**MC1. Idle foot stamp readable at phone scale.** In `idle()`, line 518:
- Raise the Leg_FL lift `0.032 * math.sin(math.pi * u) ** 0.8` to `0.060 * math.sin(math.pi * u) ** 0.8` (about 0.32 studs at this scale).
- Keep the f30 to f46 window and the stamp event at f46 (0.383).
- Check: `beat_f85_ir_side_idle_046.png` shows the front-left foot clearly off the snow against f30. FR, BL and BR stay planted (idle_foot_drift 0). Re-run step 1 (ground_min_z idle at or above -0.02).
- The reference's lift is also low (C1), so this keeps the timing and the reference's shape and only makes it readable.

---------------------------------------------------------------------------------------------------------------------
## 5. TO 9+ (higher is better; these are the highest-impact extras)

- **T-a (flanks, palette):** the flank IRON (146,154,168) reads light grey-blue in `close_tq` and `close_front`. Try IRON (126,134,150) on the flanks only (line 20 is shared by flanks, legs and head, so use a separate flank colour). Keep IRON_D at 25 % or more of the side view.
- **T-b (brow nub, line 352):** the ivory spike (0.21 long) reads as a stray tooth on the forehead. Shorten it to 0.12, or colour it IRON_D.
- **T-c (idle snort, line 503-504):** 2 degrees is invisible on the phone. Make it 4 degrees on the head and the jaw (`2.0 * sn` to `4.0 * sn`), with the existing f70 to f73 ease.
- **T-d (act rebound, lines 604, 608, 612):** the 4-degree rebound is thin at phone scale. Try 6 degrees, with a 1 to 2 degree spine recoil on the same frames.
- **T-e (roar pulses):** the neck pump is 2 degrees (N3). Try 3 degrees; keep the head at -2 and the snout forward.
- **T-f (tris headroom):** 14,572 leaves 428 spare. The thigh lofts (lines 361 and 364) start at H + 0.10, so their top part probably sits inside the barrel where it cannot be seen. Try 12 segments (default 20) on those thigh tubes to free some tris. I did not measure per-part counts, so the saving is an estimate.

---------------------------------------------------------------------------------------------------------------------
## 6. Pass / fail checklist (round 2)

| Item | Result | Evidence |
|---|---|---|
| M1 renders from final file + time in titles | PASS | `_model_sheet` title 01:37, `VoltRhino.py` 01:35 |
| M1 icon regenerated from final portrait | PARTIAL | icon 01:36:58, raw portrait 01:37:47 (MM4) |
| M2 rear fold gone, fold thinner | PASS | line 245, line 156 (0.014) |
| M2 one fold on back, no hoop | FAIL | saddle/rump double band, `model_game`, `model_back` (MM1) |
| M3 chin slab reduced | PASS | `pclose_below_roar_28` (old) vs `_chin_sheet` |
| M3 chin reads as a strip | PARTIAL | `under.png`, `closeb_cbelow`, `closeb_cside2` (MM2) |
| M4 eye slit larger | PASS | `_close_sheet` close_side, close_tq |
| M4 eye slit reads at 64 px | FAIL | `_icons_strip_64.png` (MM3) |
| M5 legs not stacked boxes | PASS | `under.png`, `model_side`, walk f0, step-1 collision_free |
| N1 IRON_D 76,84,102 | PASS | line 18 |
| N2 IRON 146,154,168 | PASS | MODEL_NOTES; stud highlights tamer |
| N3 roar neck pump | PASS (small) | verify.json neck max 5.5 |
| C1 idle animationreference cited | PASS | `ANIM_REFS.md` final85 C1; ref contact sheets |
| C2 idle renders current | PASS | `_beats_f85_ir_*` at 01:36 |
| C2 stamp visible at f46 | FAIL | `beat_f85_ir_side_idle_030` vs `_046` (MC1) |
| C2 other feet planted | PASS | idle_foot_drift 0 |
| C3 holds 2 frames, tip 0.010 or less | PASS | verify.json Horn_Tip 0.0035 to 0.0079 |
| C3 rebound 3 frames after | PASS | line 604-612, `beat_f85_wa_side_act_horntap_033` |
| C3 tap variety | PASS | tap3 +2.5 deg, tap2 drag |
| Limits (neck, chest, pitch-up) | PASS | verify.json |
| End at rest, no shakes, acts in place | PASS | end vs rest 0.0 |
| Events in fraction convention | PASS | stamp 0.383, bellow1 0.333, tap1 0.3 |
| Tris at or under 15k | PASS | 14,572 (export) |
| No glow | PASS | glow [] |
| T1 back ridge | PASS | lines 268-277, `model_side`, `model_tq` |
| T2 saddle bolts | PASS | lines 261-267, `model_game` |
| T3 snort visible | PARTIAL | 2 degrees, not visible at phone scale (T-c) |

---------------------------------------------------------------------------------------------------------------------
## 7. Next steps
1. Builder: MM1 to MM3 in `pets/VoltRhino.py` (line 136, line 285, line 308), then re-run step 1 and check `model_game`, `under.png`, `_close_sheet` and `_icons_strip_64`.
2. Builder: MC1 (line 518), re-run step 1 (collision_free and ground).
3. Builder: MM4 (icon from the 01:37:47 portrait, feet re-log at f30, f42, f54).
4. Send to the final reviewer, all at once: the updated `_model_sheet`, `_close_sheet`, `_chin_sheet`, `_icons_strip_64/128`, `model_game`, `under.png`, the idle f30 and f46 side frames, the act f33 and f42 frames.
5. Ship bar: model at or above 8.5 and clips at or above 8.5. TO 9+ if time allows.
