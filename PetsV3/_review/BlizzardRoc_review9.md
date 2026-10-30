# Blizzard Roc - model + clip gate review 9 (2026-10-28, fresh reviewer, final gate)

**Model: 8.7/10 - PASS. Clips: 8.5/10 - PASS.** (Clips = the lowest per-clip score. Walk 8.5 and land 8.5 tie at the floor.)

- Walk moves from 8.3 to 8.5. W1 meets its measured target, W2 is waived by the lead ruling, and W3 is done in the code docstring and the ANIM_REFS walk row.
- The walk is at the floor, not comfortable. Its weight is thin (see section 2).
- Model and the other six clips are unchanged since round 8. The code diff from r8final to r9final is the walk lines only (L600-629), so their round-8 scores carry.

---------------------------------------------------------------------------------------------------------------------
## What I looked at

**Read (text):** `GLACIER_REVIEWER_BRIEF.md`; `BlizzardRoc_review8.md`; `BlizzardRoc/CLIP_NOTES.md`; `BlizzardRoc/ANIM_REFS.md`; `pets/BlizzardRoc.py` L596-650; `BlizzardRoc/_scratch/full_step1.txt`; `_scratch/crest_range.py`.

**Currency:** `pets/BlizzardRoc.py` is byte-identical to `_scratch/BlizzardRoc_r9final.py.txt` (cmp). The code was last written 06:42. The walk renders are 08:16 and `full_step1.txt` is 08:17, so both are newer than the geometry. I did not re-run headless or Blender; the step-1 numbers come from `full_step1.txt`.

**Images (renders\\):** `_pose_front_walk_sheet.png`, `_pose_tq_walk_sheet.png`, `_pose_game_walk_sheet.png`, `_model_sheet.png`. I also made 2x crops of f0 / 6 / 12 / 18 for tq, game and front (in the Windows Temp folder, not the project).

**My measurements** (300 px tiles, `renders/pose_<view>_walk_NN.png`, scratch script in Temp; they match the builder's crest numbers):
- Crest centroid (FROST_V pixels in the top 45 % of the tile), f0-36 every 3 f.
- Pale body centroid (v > 0.92, s < 0.12, rows 30-60 %).
- Dark-pixel foot extent (bottom 30 % of the tile, tq).

---------------------------------------------------------------------------------------------------------------------
## 1. Scores

| clip | score | why (one line) | evidence |
|---|---|---|---|
| idle | 9.0 | Unchanged since round 8 (walk-only code diff). | `renders/_pose_game_idle_sheet.png`, `_pose_tq_idle_sheet.png` |
| **walk** | **8.5 (PASS, floor)** | Sway now reads in front (crest 29.3 px, target 24). Stride and stance are clean (no slide, collision-free). Head held level, so it reads as a stalk. Weight is thin: contact dip about 2 px and lateral shift about 4 px; roll carries all the sway. | `renders/_pose_front_walk_sheet.png`, `_pose_tq_walk_sheet.png`, `_pose_game_walk_sheet.png`; `pets/BlizzardRoc.py` L599-629; `ANIM_REFS.md` L27-37 |
| fly | 8.6 | Unchanged since round 8. | `renders/_pose_tq_fly_sheet.png`, `_pose_game_fly_sheet.png` |
| takeoff | 8.7 | Unchanged since round 8. | `renders/_pose_tq_takeoff_sheet.png`, `_pose_game_takeoff_sheet.png` |
| land | 8.5 | Unchanged since round 8. Lowest non-walk clip, at the floor. | `renders/_pose_tq_land_sheet.png`, `_pose_game_land_sheet.png` |
| roar | 9.0 | Unchanged since round 8. | `renders/_pose_tq_roar_sheet.png` |
| act_bow | 9.0 | Unchanged since round 8. | `renders/_pose_tq_act_bow_sheet.png` |

**Clips score = 8.5 (walk and land, tied at the floor).**

**Model: 8.7 (carried).** The geometry is unchanged since round 8. I re-checked `_model_sheet.png` and it matches the round-8 read. M2 (bind-pose wings read as poles) is still a lead ruling and is not counted.

---------------------------------------------------------------------------------------------------------------------
## 2. Walk evidence

**Measured** (front / game / tq, 300 px tiles, f0-36):

| measure | front | game | tq | reading |
|---|---|---|---|---|
| crest x range | **29.3 px** | 23.2 px | - | W1 target (front >= 24): met. Roll carries it. |
| crest y range | 5.0 px | 6.7 px | - | Head/crest is steady. W2 bob waived. |
| pale body centroid x range (lateral shift) | 3.8 px | 4.3 px | 1.9 px | 0.05 BU is about 4 px. It is not the sway source. |
| tq dark-pixel foot span (bottom 30 %) | - | - | 27 px at f0 (feet together), 57-59 px at f18-27 | Stride reads from the side. |

**Code (`pets/BlizzardRoc.py`):** pitch sp = 1.2 (L616), yaw sy = 2 (L617), roll sr = 5 (L618), lateral shift 0.05 BU (L620), contact dip -0.02 BU (L611 and L613), neck chain -0.2 / -0.2 / -0.35 with no thrust term (L622-623). The docstring (L600-604) matches the code: roll +-5, shift 0.05, yaw +-2, head glides, no bob.

**Why 8.5 and not higher:**
- (+) The sway reads in the front sheet. The crest travels about 29 px and the body rocks each step.
- (+) Stepping reads from the tq camera (feet separate from 27 to 58 px). No slide, collision-free, loop closed.
- (+) The head stays level in world (the neck chain cancels about 75 % of the body roll). It reads as a composed stalk.
- (+) Docstring, ANIM_REFS walk row and code agree (W3).
- (-) Weight is thin. The contact dip is 0.02 BU (about 2 px, not visible) and the lateral shift is about 4 px, so only the roll carries the weight feel.
- (-) From the game camera the legs are pale-grey shafts under the wing. The stride is weak there. My dark-pixel count missed them, so I give no number. I judged it by eye on the 2x crop.
- (-) Roll of 5 is at the edge. At phone size the rock reads as deliberate. It is not far from a waddle. The builder reads it as heavy; I accept that for the floor score, but it is the first thing to check if the owner calls it a waddle.

---------------------------------------------------------------------------------------------------------------------
## 3. New MUSTs

**None block the 8.5 floor.** The model and all seven clips pass on their current scores. Walk W1 is met on its measured target. W2 is waived by the lead ruling. W3 is done in code and in the walk row.

---------------------------------------------------------------------------------------------------------------------
## 4. TO 9+ (not blocking, not counted)

1. **Weight (walk).** Deepen the contact dip: `dip()` L611 and L613, `-0.02` -> `-0.04` BU (about 4 px). Measure: the lowest point of the pale body in the front tile moves at least 4 px over the cycle. Re-run step 1: ground >= -0.02, `collisions` {}.
2. **Shift (walk).** If the front pale-body centroid is still under 6 px after item 1, raise L620 from `0.05` to `0.08` BU. Measure: front pale-body centroid x range >= 6 px. Re-run step 1 (collisions {}, chest vs spine within limit).
3. **Game-camera stride (walk).** Lengthen the stance step by 10-15 % (the stride argument of `cm.biped_walk`, L638, currently 0.15) or raise the passing-foot lift. Judge by eye on the 2x game crop; the legs are pale, so the dark-pixel method does not work for this. Re-run step 1: walk slide 0.0.
4. **Model accent at 64 px.** Carried from round 8 (the violet is only on three tips). Still open, not counted.
5. **Roll 4 vs 5.** Do not change it now. Only drop roll to 4 (and raise the shift to 0.07 BU) if the owner calls the walk a waddle.

---------------------------------------------------------------------------------------------------------------------
## 5. Carry-over doc items (not MUSTs; do them in the same edit)

- `BlizzardRoc/ANIM_REFS.md` L1 still reads "clip round 3 (review 5) + round 4 (review 6)". Round-8 W3 asked for "clip round 5 (review 7)". Set it to clip round 6 (review 8).
- `BlizzardRoc/CLIP_NOTES.md` L34-41 still describes the dropped head bob (+-5 thrust) and the 0.02 shift under the review-8 heading. It contradicts L7-17 and the code. Delete it or mark it superseded.

---------------------------------------------------------------------------------------------------------------------
## 6. Pass / fail checklist

| # | check | result |
|---|---|---|
| 1 | Code is current: pets file == r9final (cmp); renders 08:16 and step 1 08:17 are newer than the code (06:42) | PASS |
| 2 | Step 1: collision_free true, collisions {}, audit linear 0, loops closed (walk loop_pos 0, loop_rot 0) | PASS (`full_step1.txt`) |
| 3 | Ground >= -0.02 (walk -0.015 at f33; fly +0.377) | PASS |
| 4 | Walk slide 0.0, foot_z_var 0.0 | PASS |
| 5 | Neck <= 8, chest vs spine <= 5 (walk: neck local about 1.1, chest local 0.0 per CLIP_NOTES; not re-run) | PASS |
| 6 | W1 sway: front crest x range >= 24 px | PASS (29.3 px) |
| 7 | W1 shift 0.05 BU in code | PASS (L620) |
| 8 | W2 head bob | WAIVED (lead ruling); head held level |
| 9 | W3 walk row and docstring match code | PASS (ANIM_REFS header stale: carry-over) |
| 10 | Other clips unchanged (diff r8final -> r9final = walk lines only) | PASS |
| 11 | Tris 12,940, no glow | PASS (`full_step1.txt`) |
| 12 | No head shakes, no airborne spin, no hop; walk acts in place, loops | PASS |
| 13 | Walk reads as a stalk (front, tq) | PASS (floor; game-camera stride weak, TO 9+ item 3) |
| 14 | Model unchanged and clean | PASS (8.7 carried) |

---------------------------------------------------------------------------------------------------------------------
**Verdict.** Model **8.7, PASS** (carried). Clips **8.5, PASS** (walk 8.5 and land 8.5 tied; idle 9.0, fly 8.6, takeoff 8.7, roar 9.0, act_bow 9.0). No blocking MUST. Two doc carry-overs (section 5) should land with the next edit.
