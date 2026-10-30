# Blizzard Roc - model + clip gate review 8 (2026-10-28, fresh reviewer, final gate)

**Model: 8.7/10 - PASS. Clips: 8.3/10 - FIX.** (Clips = the lowest per-clip score, the walk.)

- Model passes: the round-7 model items (M3b back, M4b eye) are done and checked on the pixels.
- Clips fail on the walk alone: 8.3. The walk's weight shift is about 0.09 studs, too small to see at phone size, its head bob does not show from the player's camera, and ANIM_REFS still describes the old walk.
- Every other clip is 8.5 or higher. The fly stroke, which round 7 could not verify, now reads.
- Three walk MUSTs (W1 to W3). Each is a few lines of code or doc.

---------------------------------------------------------------------------------------------------------------------
## What I looked at

**Read (text):** `GLACIER_REVIEWER_BRIEF.md`; `BlizzardRoc_review7.md`; `BlizzardRoc/MODEL_NOTES.md` (round 8); `BlizzardRoc/CLIP_NOTES.md` (round 7 + 8 sections); `BlizzardRoc/ANIM_REFS.md`; `pets/BlizzardRoc.py` L599-647 (walk), L617-629 (body + head bob), L618 and L620 (roll, shift), L600 (docstring).

**Currency:** `pets/BlizzardRoc.py` is byte-identical to `_scratch/BlizzardRoc_r8final.py.txt` (cmp). It was last written 06:12. The renders are 06:13-06:14, so they are newer than the geometry. Step-1 outputs (`_scratch/full_step1.txt`, `steps.txt`, `seam.txt`, `rest_delta.txt`) are dated 06:12. I did not re-run headless; I used those outputs.

**Round-8 code diff** (`BlizzardRoc_r7final` vs `r8final`): wing arm bar and wrist CHAR; Chest middle shingle row and Spine lower row CHAR; the FROST_H eye hot spot removed; walk head bob (L622-629); walk lateral shift 0.01 -> 0.02 (L620).

**Images (renders\\):** `_model_sheet.png`, `model_game.png`, `_head2x_sheet.png`, `head2x_front.png` (eye zoom), `_icons_strip_64.png` / `_128.png`, `flat_game.png` / `flat_tq.png` / `flat_side.png` (value shares recomputed), `_pose_{game,tq,front}_walk_sheet.png`, `_pose_{tq,game,front}_fly_sheet.png`, `_pose_{tq,game}_takeoff_sheet.png`, `_pose_{tq,game}_land_sheet.png`, `_pose_{game,tq}_idle_sheet.png`, `_pose_tq_roar_sheet.png`, `_pose_tq_act_bow_sheet.png`.

**My measurements:**
- Value shares on `flat_*.png`: nearest-palette count on the non-background pixels.
- Walk head bob: crest-tip (violet) centroid and top per frame, on `pose_{tq,game,front}_walk_NN.png` (300 px, every 3 f).
- A 2x head montage of the tq walk frames and an eye zoom. Scratch crops were written only to the Windows Temp folder, not to the project.

---------------------------------------------------------------------------------------------------------------------
## 1. Scores

| clip | score | why (one line) | evidence |
|---|---|---|---|
| idle | 9.0 | Unchanged apart from the tail. Frost shed, head turns and talon re-grips read; no regression. | `_pose_game_idle_sheet.png`, `_pose_tq_idle_sheet.png` |
| **walk** | **8.3 (FIX)** | Roll sway reads (about 16 px). The 0.02 BU shift is about 0.09 studs, about 2 px at 300 px, so it does not read. The head bob shows in tq as a 7-8 px weave, but not from the game camera. ANIM_REFS still describes the old walk. | `_pose_front_walk_sheet.png`, `_pose_tq_walk_sheet.png`, `_pose_game_walk_sheet.png`; code L599-647; `ANIM_REFS.md` L27-29 |
| fly | 8.6 | The stroke now reads in all three cameras: f0 high V, f10-15 near-horizontal, f20 low, f25 rising, f30 = f0. Mid-stroke front frames (f10, f15) are flat planks. | `_pose_tq_fly_sheet.png`, `_pose_game_fly_sheet.png`, `_pose_front_fly_sheet.png` |
| takeoff | 8.7 | Coil, launch, downstroke and the rise read; takeoff f36 = fly f0 exactly (0.00 deg). The coil is still shallow (lead ruling). | `_pose_tq_takeoff_sheet.png`, `_pose_game_takeoff_sheet.png`, `_scratch/seam.txt` |
| land | 8.5 | Flare, brake, touch, hold and fold all read; no change. Lowest of the non-walk clips. | `_pose_tq_land_sheet.png`, `_pose_game_land_sheet.png` |
| roar | 9.0 | Snap-open with the beak after the spread; the crest flares; no change beyond the tail. | `_pose_tq_roar_sheet.png` |
| act_bow | 9.0 | Bow, drooped wings and the snap-closed read; rest at the end (0.00). | `_pose_tq_act_bow_sheet.png` |

**Clips score = 8.3 (walk, the lowest).**

**Model: 8.7 (+0.1 over round 7).** The mantle band and the eye fix are real and visible. See section 3.

---------------------------------------------------------------------------------------------------------------------
## 2. Round-7 items

- **M3b back (STORM + MANTLE <= 40 %, CHAR >= 20 %): PASS.** Game camera, nearest palette on `flat_game.png`: STORM 22.3 + MANTLE 14.2 = **36.5 %** (builder 36.7); CHAR **29.6 %** (builder 29.8). The dark band across the chest and spine reads in `model_game.png`. Also the wing arm bar and wrist are dark, so the folded-wing leading edge reads as a stripe.
- **M4b eye (pale FROST_H bar removed): PASS.** `head2x_front.png` zoom: violet FROST_V slit under a dark lid, black slit pupil, no pale dash. Code L164-166 removes the bar.
- **Walk 8.2 (0.02 BU shift + head bob): PARTIAL, still 8.3.** The shift is in code (L620) and the bob is in code (L622-629), with the step-1 values intact (see section 3). Neither reads from the game camera.
- **Fly evidence (f0-30 every 5 f, tq and game): PASS.** The sheets exist in tq, game and front, and the stroke is visible. It was unverified in round 7.
- **Mantle / wing leading-edge stripe, per the brief: PASS.** The game-camera greys are under 40 %, CHAR is over 20 %, and the stripe reads without a visible seam.
- **Eye hot spot, per the brief: PASS** (as M4b).
- **Largest per-frame steps (`steps.txt`): PASS, matches the builder.** idle 9.0, walk 6.3, fly 8.7, takeoff 30.6 (Foot_L f19), land 36.5 (FX_SnowPuff_LandR f8, an effects bone, not visible), roar 32.6 (Wing_L f17), act_bow 26.6 (WingTip_L f58).
- **Takeoff-to-fly handoff: PASS.** `seam.txt`: takeoff vs fly f0 = **0.00 deg / 0.000 BU**.
- **Tris: PASS.** 12,940 (`full_step1.txt`, `tris_body`), no glow.
- **Step 1 (ANIM_REFS / clip gate): PASS.** `collision_free` true, `collisions` {}, audit linear 0, loops closed, walk slide 0.0, `foot_z_var` 0.0, ground -0.014 / -0.015 (fly +0.377).

---------------------------------------------------------------------------------------------------------------------
## 3. Evidence for the walk (why it is 8.3)

**Weight shift (W1).** The code moves the spine sideways by `0.02 * wave` (L620). 1 BU = 4.5 studs (9.0 studs = 1.996 BU), so 0.02 BU = **0.09 studs**. In a 300 px front tile the bird is about 185 px tall (about 20 px per stud), so the shift is about **2 px**. That is not readable at phone size. The sway that does show comes from the roll `sr = 3 * wave` (L618): the front-tile crest tip moves between x 165 (f6) and x 149 (f27), a range of about 16 px. That range is the roll and yaw, not the lateral shift.

**Head bob (W2).** The head holds for f0-12 of each step and thrusts over f12-18 (L624-627). Measured:
- Front tile, crest-top y: 62-70 px across the cycle (peaks f12 and f30, low at f0 / f18 / f36), a range of about 8 px.
- TQ tile: a 7-8 px vertical weave. In the 2x head montage (temp) the head reads as an up-and-down weave rather than a clean hold-then-jab, and the hold is not clean (the crest drifts 12 px in x during f0-12, partly body yaw and roll).
- Game tile: crest-top y 68-74 (about 6 px) and crest x 128-139 (about 11 px, the body roll). The bob is not visible from the player's camera. The builder says the same in CLIP_NOTES.

**Neck and step checks (pass):** walk neck local max 4.9 (limit 8). Largest walk step 6.3 deg (Leg_R f9). Walk slide 0.0. Ground -0.015. `collision_free` true.

**Reference (W3).** `ANIM_REFS.md` L27-29 still reads "the gyro head, which holds height and angle" and "a 0.01 BU lateral shift", and its header says round 3 and 4. The clip now has 0.02 BU and a thrust that the entry does not mention. The H1 row (L16) also says "the head stays at one height and angle". Either the thrust is in H1 (then cite its timestamps) or it is not (then the thrust is a deviation). The code docstring (L600) says roll +-4 and the code uses 3. The CLIP_NOTES clips table says +-3. I could not check H1 frames myself.

**Score reasoning.** The walk has a clean stance, no slide, and a correct period. The 2x head and the weight shift are both too small to read at the player's camera. That is the 8.2 to 8.3 gap. Fixing W1 and W2 should lift the walk above 8.5. W3 is required for the ANIM_REFS rule.

---------------------------------------------------------------------------------------------------------------------
## 4. New MUSTs (only what blocks 8.5 on the clips)

Only the walk blocks. The model and the other six clips pass.

**W1. Visible weight sway (walk).**
- `pets/BlizzardRoc.py` L618: `sr = 3 * pk.wave(f, n, 0.05)` -> `sr = 5 * pk.wave(f, n, 0.05)`.
- L620: `loc=(0.02 * pk.wave(...), 0, dip(f))` -> `loc=(0.05 * pk.wave(...), 0, dip(f))`.
- L600 docstring: keep the roll and shift numbers in step with the code.
- Measure: `_pose_front_walk_sheet.png`, crest-tip x range over f0-36 >= **24 px** in a 300 px tile (now about 16 px).
- Step 1 must hold: `collision_free` true, `collisions` {}, walk slide 0.0, ground >= -0.02, neck <= 8. If a collision appears, use `sr = 4` and the shift 0.04 instead.

**W2. Head thrust readable at the game camera (walk).**
- `pets/BlizzardRoc.py` L624: `hb = 5.0 - 10.0 * t / 12.0` -> `hb = 7.5 - 15.0 * t / 12.0`.
- L627: `hb = -5.0 + 10.0 * u * u * (3 - 2 * u)` -> `hb = -7.5 + 15.0 * u * u * (3 - 2 * u)`.
- Expected neck local max about 7.4 (limit 8). The Neck + Neck2 + Head pitch sum stays -0.75 x sp, so the head stays level and the pitch-up limit is not at risk.
- Measure: front tile crest-top y range over f0-36 >= **12 px** (now 8); game tile crest-top y range >= **9 px** (now 6). Re-run step 1 with W1 and W2 applied together: the neck local max (all axes) must stay <= 8.
- **Do this only after W3's frame check.** If H1 shows no head thrust, delete the thrust (set `hb` to 0 apart from the gyro) rather than enlarging it.

**W3. ANIM_REFS and comments match the clip (walk; ANIM_REFS rule).**
- `ANIM_REFS.md` L1: header -> "clip round 5 (review 7)".
- `ANIM_REFS.md` L27-29 (walk row): state the current shift (0.02 BU, or the W1 value), the roll and yaw, and the head behaviour. For the head, either cite the H1 17.85-20.85 s sub-times where the head thrusts (frames f12-18 of each step, about 0.6 s apart), or say the head is gyro-held and remove the thrust (see W2).
- `pets/BlizzardRoc.py` L600 docstring: roll "+-3" (the code value), or raise the code to 4 and keep the docstring.
- Measure: every walk number in ANIM_REFS maps to one code line.

---------------------------------------------------------------------------------------------------------------------
## 5. TO 9+ (not blocking)

- **Model accent at 64 px.** The violet accent is three tips (crest, tail, primary tips); the 64 px icon reads mostly white with a dark wing. Consider one FROST_V bar on the lower secondary coverts so the icon carries the accent. Keep it to one accent (the palette rule).
- **Model, bind-pose wings** still read as poles from the front and 3/4 (M2, lead ruling, not counted).
- **Fly, mid-stroke frames** (f10, f15 front) read as flat planks. A small wing twist on the two mid-stroke keys would show feather surface (not counted: it changes an approved clip, so it needs a re-check of every key).
- **Takeoff coil** (lead ruling, not counted).

---------------------------------------------------------------------------------------------------------------------
## 6. Pass / fail checklist

| # | check | result |
|---|---|---|
| 1 | step 1: collision_free, ground >= -0.02, audit linear 0, loops closed | PASS (-0.014 / -0.015; fly +0.377; `collisions` {}) |
| 2 | neck <= 8, chest vs spine <= 5 | PASS (7.5 / 4.0; walk neck 4.9) |
| 3 | head + neck pitch-up <= 30 | PASS (26 from CLIP_NOTES, not re-run) |
| 4 | largest bone step <= 60 per frame | PASS (36.5 FX bone, 32.6 roar, 30.6 takeoff, 26.6 act_bow) |
| 5 | events match frames | PASS (launch 0.389 = f14; touch 0.531 = f17; roar 0.333 = f20; snap 0.527 = f58; frostshed 0.2 = f24) |
| 6 | rest frames 0 deg | PASS (idle, roar, act_bow, land 0.00 vs rest) |
| 7 | takeoff to fly seam | PASS (0.00 deg / 0.000 BU) |
| 8 | launch reads as weight | PASS (unchanged from round 7) |
| 9 | post-launch recovery at fly tempo | PASS (unchanged; takeoff f25-36 at the fly tempo) |
| 10 | refs cited and matching | **FAIL** (walk row stale; W3) |
| 11 | model evidence current | PASS (r8final = live; renders 06:13-06:14 > geometry 06:12) |
| 12 | no glow; tris <= 15k | PASS (12,940) |
| 13 | no head shakes, no airborne spin, acts in place, rest at end | PASS (the walk bob is a held-then-thrust neck move, not a shake) |
| 14 | idle, roar, act_bow, land read | PASS |
| 15 | walk reads | **FAIL** (8.3; W1 and W2) |
| 16 | fly reads | PASS (stroke f0-30 visible in three cameras) |
| 17 | M3b back, M4b eye | PASS (36.5 / 29.6 %; no pale eye bar) |

---------------------------------------------------------------------------------------------------------------------
**Verdict.** Model **8.7, PASS**. Clips **8.3, FIX** (the walk; idle 9.0, fly 8.6, takeoff 8.7, land 8.5, roar 9.0, act_bow 9.0). The model work landed. Fix W1 to W3 and resubmit the walk only (step 1, the front and tq walk sheets, and ANIM_REFS).
