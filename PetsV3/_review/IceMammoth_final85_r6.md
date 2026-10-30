# Ice Mammoth - FINAL 8.5 GATE, ROUND 6 (2026-10-28, fresh reviewer)

**Model: 8.6/10 - PASS. Clips: 8.4/10 - FIX.**

Lowest clips: **idle 8.4** and **walk 8.4**, both under the 8.5 floor. Roar 8.6, act 8.6. The model is unchanged from round 5 and still passes.

## Scoring basis
The round 6 changes are real and match the code, but the brief judges from the player's eye (about 5 studs, FOV 70, 390 px). In the game-camera frames (`_beats_f85r5_iw_game.png`) the ear is not visible at all, and neither the breath nor the walk bob is visible. The idle and walk scores therefore stay where round 5 left them. The numbers pass; the beats do not read at game distance.

## What I looked at
- **Read:** `_review/GLACIER_REVIEWER_BRIEF.md`; `_review/IceMammoth_final85_r5.md`; `IceMammoth/CLIP_NOTES.md` (round 5 section); `IceMammoth/ANIM_REFS.md` (plate 733 P1-P7, idle and walk refs); `pets/IceMammoth.py` (idle, `ears()`, walk `body()`, walk `walk_cycle` call); `IceMammoth/_scratch/verify.json`, `export_result_f85r5.txt`, `full_step1.txt`, `footfalls.txt`.
- **Images (all loaded, none missing):** `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `_beats_f85r5_iw_side.png`, `_beats_f85r5_iw_tq.png`, `_beats_f85r5_iw_game.png`, `_beats_f85r5_act_side.png`, `_beats_f85r5_act_tq.png`, `_roar_mouth.png`, `pclose_side_roar_34.png`; single 390 px frames `beat_f85r5_iw_side_idle_030/040` and `beat_f85r5_iw_side_walk_010/020`; builder crop `_scratch/ear_r5.png`.
- **Freshness:** model, close and icon sheets 08:16-08:20 (after the 08:14 file). Idle, walk and act sheets 08:16-08:17. Roar stills are 05:57-05:58, older than the 08:14 export, but the roar code has not changed since then (see below), so they still describe the roar clip.
- **Pixel measurements (read-only, System.Drawing; nothing written to the renders folder):**

| measure | result | round 5 reference |
|---|---|---|
| Idle head box (100-175, 95-175), f30 vs f40 | 1,580 px changed | 1,214 px (on r4 renders) |
| Idle ear box (105-170, 100-140), f30 vs f40 | 731 px changed | not measured |
| Idle ear box, f36 vs f44 | 1 px (bell is symmetric about f40; not a test) | n/a |
| Idle full frame, f0 vs f20 | 14,568 px | 10,576 px (r4) |
| Walk body box (110-340, 100-190), f10 vs f20 | 3,075 px | 2,802 px (r4) |
| Back-line top y at x200 / x230 / x260, idle f0, 20, 40, 60, 80 | 116-118 / 119-126 / 128-132 (range 2 / 7 / 4 px) | builder: 2 / 7 / 3 |
| Back-line top y, walk f0-f30 step 5 | x200 range 3 px, x230 range 4 px, x260 range 3 px | builder: 4 / 5 / 3 |

- **Code checks (`pets/IceMammoth.py`):**
  - idle: Spine `loc z = 0.03*br` (line 478); Chest `4.5*br` (line 479); `ears(... 18*bell(f,40,6), 16*bell(f,40,6))` (line 489).
  - walk: Spine `z = -0.022 - 0.030*b` (line 504); `walk_cycle(k, n, legs, 0.115, 0.075, body, duty=0.72)`.
  - roar and act call `ears()` with flare only (lift defaults to 0), so their ears are unchanged. The Spine breath is idle only, and the walk body is walk only.
- **Discrepancy found:** `b = 0.5 - 0.5*cos(4*pi*f/40)` equals 1 at f10 and f30 (the FL and FR touch-downs) and 0 at f0 and f20 (BL and BR). CLIP_NOTES says "b = 0 AT the contacts (f0/10/20/30)", which is wrong. Effect: the fore contacts sit 0.018 deeper than in round 4 (IK holds them: slide 0.0, ground 0.015), and the hind contacts are unchanged. The walk back line is lowest at f10 and f30 (top y 124-125 at x200) and highest at f0 and f20 (121-122), which matches the code.

## Per-clip table

| clip | score | one line why | evidence file |
|---|---|---|---|
| model | **8.6 PASS** | Unchanged since r4. Studded body, black sockets with one mint slit each, fierce brows, pale tusks with mint caps, 14,688 tris. Reads at 64 px. | `renders/_model_sheet.png`, `renders/_close_sheet.png`, `renders/_icons_strip_64.png` |
| idle | **8.4 FIX** | The trunk swing carries the clip. The ear (731 px box change, about 9 px fringe edge) and the breath (back line 2-4 px at x200/x260) are measured but do not read in the game-camera frames. The exhale reads only through the trunk. | `renders/beat_f85r5_iw_side_idle_030.png` and `_040.png`, `renders/_beats_f85r5_iw_game.png`, `renders/_beats_f85r5_iw_side.png` |
| walk | **8.4 FIX** | Lateral order (BL f0, FL f10, BR f20, FR f30), planted feet, trunk pendulum and roll all read. The bob is now 3-4 px (round 4: about 1 px) but is not visible in the game view. Swing lift is 0.075 BU, about half of the plate's clearance (see MUST 2). | `renders/beat_f85r5_iw_side_walk_010.png` and `_020.png`, `renders/_beats_f85r5_iw_game.png`, `ANIM_REFS.md` (P3) |
| roar | **8.6 PASS** | Trunk rises clearly to the sky; jaw open from the front, below and 3/4. From the pure side the mouth is still a small dark wedge under the cheek (PARTIAL, unchanged). Jaw 22, pitch-up 16. | `renders/_roar_mouth.png`, `renders/pclose_side_roar_34.png`, `_scratch/verify.json` |
| act (dust-over) | **8.6 PASS** | Scoops reach the snow (FX holds 0.0111). The flick passes over the brow (FX z 1.730 at f56 vs dome top 1.76). Max swing 53.7. The name "over the back" is PARTIAL and not scored. | `renders/_beats_f85r5_act_side.png`, `renders/_beats_f85r5_act_tq.png` |

**Lowest clip: idle 8.4 and walk 8.4. Clips = 8.4 (FIX).**

## Round 5 items

**Idle**

| item | result | evidence |
|---|---|---|
| M1: ear 13 to 18 deg, plus lift; free edge at least 0.06 BU in the side plane (f30 to f40) | **PARTIAL** | Code applies 18 deg and 16 deg lift (line 489). The builder's probe gives 0.0619 BU (not re-run here). The ear box changes by 731 px and the fringe edge moves about 9 px. The ear is a small dark tab on grey wool and is not visible in the game view. |
| M1 visibility: ear outline changes in the 390 px side frames | **PARTIAL** | Side frames 030 vs 040 show a small change at the head top. Not readable at game distance. |
| M2: chest breath 4.5 deg, chest vs spine at most 5 | **PASS** | verify.json `chest_vs_spine` 4.5; code line 479. |
| M2: Spine rises 0.03 on each breath | **PASS** (numbers) | Code line 478; back line moves 2 / 7 / 4 px at x200 / x230 / x260. |
| M2 visibility: breath readable at 390 px | **FAIL** | The 2-4 px back-line change is not visible in the side or game frames. |
| Trunk roll and tip travel f0 to f20 (0.253 BU) | **PASS** | Code `rl` amplitudes; CLIP_NOTES coordinates (carried from r5). |
| Neck at most 8, collision_free, loop closed, idle foot drift 0 | **PASS** | verify.json neck 0.6, collisions_with_hinges {}; `audit.idle.idle_foot_drift` 0.0. |

**Walk**

| item | result | evidence |
|---|---|---|
| M3: Spine `-0.022 - 0.030*b`; contacts unchanged; slide 0; ground at least -0.02 | **PASS** (numbers) | Code line 504; step 1: slide 0.0, foot_z_var 0.0, ground walk 0.015, stride 0.3194. |
| M3 visibility: back line visibly moves | **PARTIAL** | 3 / 4 / 3 px at x200 / x230 / x260 (side, 390 px). Not visible in the game view. The plate (P5) says the back stays level, so a larger bob would contradict the reference. |
| M3 note accuracy | **FAIL (notes)** | CLIP_NOTES says b = 0 at all contacts. Wrong; see Discrepancy above. |
| Trunk tip travel f10 to f20 at least 0.2 BU | **PASS** | 0.206 BU (builder); my 390 px frames agree. |
| Body roll, spine rock, trunk side and fore-aft swing | **PASS** (code) | Lines 503 and the `pt` / `rl` lists. |
| Stride 0.3194, slide 0.0, foot_z_var 0.0, loop closed; max swing at most 60; neck at most 8; chest at most 5 | **PASS** | verify.json walk: max swing 7.7 (Shin_FL), neck 0.8, chest 1.68; footfalls.txt order BL, FL, BR, FR. |

**Roar and act (unchanged in round 6)**

| item | result | evidence |
|---|---|---|
| Roar mouth open from the side | **PARTIAL** | `pclose_side_roar_34.png`: the dark band is a small wedge under the cheek, partly covered by the tusk root. Front, below and 3/4 are clearly open. |
| Roar jaw at most 22, pitch-up at most 30, collision_free, ends at rest | **PASS** | jaw 22.0 (f34), pitch-up 16.0, `end_vs_rest` 0.0. |
| Act scoops reach the snow; FX holds at most 0.012 | **PASS** | `_beats_f85r5_act_tq.png`; holds 0.0111; ground_min_z -0.016. |
| Act flick passes over the head | **PASS** | `_beats_f85r5_act_side.png` f48-f58; FX z 1.730 at f56 vs dome 1.76. |
| Act max swing at most 60; pitch-up at most 30; ends at rest | **PASS** | 53.7 (f76); 17.0; 0.0. |

**Global**

| item | result |
|---|---|
| ground_min_z at least -0.02, all clips | **PASS** (idle 0.018, walk 0.015, roar 0.018, act -0.016) |
| collision_free, all clips | **PASS** (`collisions` {}, `collision_free` true) |
| Tris at most 15k; no glow; height 9.0 | **PASS** (14,688; `tris_glow` {}; 9.0) |

## MUST (blocks 8.5; idle and walk only)

**Idle (8.4)**

1. **Exhale head lift readable at game distance.** In `idle()`, change the Head term `-1.5 * ex` to `-8.0 * ex`, and add `neck_lift(hd)` (the helper roar and act use) to the Neck so the dome clears the shoulder hump. Measure in the headless probe: the Head bone's dome top rises at least 0.07 BU from f70 to f80 (side view, about 8 px at 390 px). Keep: Neck max at most 8; head pitch-up at most 30; Head|Chest raw crossings at most 6; collision_free true; idle foot drift 0; loop closed. Re-render the side frames at f70 and f80 and confirm the silhouette moves.

**Walk (8.4)**

2. **Swing lift to the plate's clearance.** In `walk()`, change the `walk_cycle` lift argument from `0.075` to `0.15`. The reference (`ANIM_REFS.md` P3) says the fore foot's clearance is "only about 1/5 of the leg length". The fore leg runs from Leg_FL hip z 1.00 to ankle z 0.21, which is 0.79 BU, so 1/5 is about 0.16 BU. The current 0.075 is about half that (the notes' "low lift of 0.07" misreads P3). Measure: Foot_FL and Foot_FR bone z rises at least 0.13 BU above planted height in f5-f8 and f25-f28. Keep: slide at most 0.002; foot_z_var at most 0.001; ground_min_z at least -0.02; collision_free true; max adjacent swing at most 60. If slide exceeds 0.002, use 0.12 and re-check.

## TO 9+ (in order of impact)

**Model**
1. Belly pale band: break its top edge with 2 stud rows of WOOL_D (open since round 4; it still reads as a plate in `model_side`).
2. Mid lock row: vary height by about plus or minus 0.02 BU, not just length.
3. Brows: darken the outer 30% of each brow slab to about (56, 72, 84) (the outer ends still read light in `close_front`).

**Idle**
4. Ear flap: readable only in side and 3/4 views. Give the flap a larger lift or a contrasting tone so the flick reads at 390 px in side view.
5. Breath: 2-4 px at 390 px. Either accept it as subtle (ANIM_REFS gives the breath as a 0.006 chest rise) or raise the Spine rise, with IK and collision checks. FX_BreathCloud is a Studio VFX matter and is not credited here.

**Walk**
6. The sink of 0.030 is three times the Williams basis in CLIP_NOTES (0.010), and P5 says "the back stays level". Either cite the source for 0.030 in `ANIM_REFS.md` or hold it at 0.010-0.020. Do not raise it further.
7. Correct CLIP_NOTES: b = 1 at the FL and FR touch-downs (f10, f30) and 0 at BL and BR (f0, f20). The fore touch-downs now bend the fore knees to hold the foot, which P3 does not show (straight column plant).

**Roar and act**
8. Roar side mouth: the dark wedge is small under the cheek and tusk root. Open it from the side (a larger jaw drop or a tusk-root offset) and re-render the side stills at the 08:14 export. The clip has not changed since 05:57.
9. Roar tremble (plus or minus 3 deg): check at game speed in Studio; not verifiable from stills.
10. Act: rename to "dust over the brow", or raise the f48-f56 Trunk1 and Trunk2 keys by about 3 deg so the tip clears the dome by at least 0.03 BU. Keep the one-frame swing under 60 (53.7 at f76). Check for a snap in game.
11. Round 5 carry-over: the M1 and M2 ear and breath checks at real game distance need a Studio check once in.

## Pass / fail checklist (round 6)

| check | result |
|---|---|
| **MODEL** | |
| Tris at most 15k | PASS (14,688) |
| HEIGHT 9.0 | PASS |
| Species reads at 64 px | PASS (`_icons_strip_64`) |
| Studded body, head, legs, trunk | PASS (`_model_sheet`) |
| Eyes: one slit in a black socket, no pupil | PASS (`_close_sheet`) |
| Pale underside visible | PASS (`under`) |
| No glow | PASS |
| **CLIPS** | |
| collision_free, all 4 clips | PASS |
| ground_min_z at least -0.02 | PASS |
| Loops closed, walk slide 0 | PASS |
| Roar and act end at rest | PASS |
| Neck at most 8, chest vs spine at most 5 | PASS |
| Head + neck pitch-up at most 30 | PASS (16.0, 17.0, 0.8, 0.47) |
| Jaw max at most 22 | PASS (22.0) |
| Max adjacent swing at most 60 | PASS (53.7) |
| Scoop holds FX at most 0.012 | PASS (0.0111) |
| Idle trunk tip travel at least 0.25 BU | PASS (0.253, carried) |
| Walk trunk tip travel at least 0.2 BU | PASS (0.206) |
| Idle ear flap readable at 390 px (side) | **PARTIAL** |
| Idle breath readable at 390 px | **FAIL** |
| Idle exhale readable at game distance | **FAIL** (trunk only) |
| Walk back line visibly moves | **PARTIAL** (3-4 px; not in game view) |
| Walk swing lift at plate clearance (P3) | **FAIL** (0.075 vs about 0.16) |
| Roar open mouth readable from the side | **PARTIAL** |
| Act flick passes over the head | PASS |
| Acts in place, no spins | PASS |

## Summary
- **Model: 8.6/10, PASS.** Unchanged from round 5.
- **Clips: 8.4/10, FIX.** Idle 8.4 and walk 8.4 are under the floor. Roar 8.6 and act 8.6 pass.
- **MUST:** (1) idle exhale head lift 0.02 to 8 deg with `neck_lift`, dome rise at least 0.07 BU f70 to f80; (2) walk `walk_cycle` lift 0.075 to 0.15, fore sole rise at least 0.13 BU, slide at most 0.002.
- **Notes for the builder:** the walk bob and breath are numerically correct but do not read at game distance; the CLIP_NOTES claim "b = 0 at all contacts" is wrong; the walk sink of 0.030 is three times the cited 0.010 basis and P5 says the back stays level.
