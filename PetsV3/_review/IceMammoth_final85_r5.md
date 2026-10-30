# Ice Mammoth - FINAL 8.5 GATE, ROUND 5 (2026-10-28, fresh reviewer)

**Model: 8.6/10 - PASS. Clips: 8.4/10 - FIX.**

Lowest clip: **idle 8.4** and **walk 8.4**, both under the 8.5 floor. Roar 8.6, act 8.6. The model is unchanged from round 4 and still passes.

## What I looked at
- **Read:** `_review/GLACIER_REVIEWER_BRIEF.md`; `_review/IceMammoth_final85_r4.md`; `_review/PERCLIP_AUDIT_crusher_mammoth.md` (Mammoth part); `IceMammoth/CLIP_NOTES.md` (newest section, "Per-clip audit round 4"); `pets/IceMammoth.py` (idle, walk, roar, dust clip code, to confirm the stated amplitudes).
- **Numbers:** `IceMammoth/_scratch/verify.json` and `export_result_f85r4.txt` (both 05:57); the footfall JSON in `_scratch/footfalls.txt`.
- **Images (all loaded):**
  - `_beats_f85r4_iw_side.png` and `_beats_f85r4_iw_tq.png` (05:58, idle and walk, 390 px);
  - single frames `beat_f85r4_iw_side_idle_000/030/040` and `..._walk_000/010/020` (05:57, 390 px);
  - `pclose_side_roar_34.png` (05:57) and `_roar_mouth.png` (05:58);
  - `_beats_f85r3_act_side.png` and `_beats_f85r3_act_tq.png` (04:41);
  - `_model_sheet.png` and `_close_sheet.png` (04:41); `_icons_strip_64.png`.
- **Pixel diffs (read-only, System.Drawing via PowerShell; nothing written to the renders folder):**
  - idle f30 vs f40, head box (x 100-175, y 95-175): 1,214 px changed;
  - idle f36 vs f44, same box: 7 px (not a valid ear test; the ear bell is symmetric about f40);
  - idle f0 vs f20, full frame: 10,576 px changed;
  - walk f10 vs f20, full frame: 12,647 px changed (legs included);
  - walk f10 vs f20, body box (x 110-340, y 100-190): 2,802 px changed.
- **Freshness:** idle, walk and the roar-mouth close-ups are current (05:57-05:58). The model sheet, close sheet and act sheets are 04:41, before the 05:57 export. The only change since then is MOUTH_IN moved 0.01 back (interior, not visible at sheet scale). The act numbers (max swing 53.7, FX holds 0.0111) match round 4. I treated the 04:41 sheets as carried forward.
- **Limits:** no zoom tool and no PIL, so pixel-per-unit values are estimates. From the 390 px side frame, the 1.76 BU model height spans about 193 px, so about 110 px per BU. All BU-to-pixel figures below use that scale.
- **Note:** two images arrived mid-review with no text. They matched the act sheets I had already read, so I did not treat them as new evidence or instructions.

## MODEL: 8.6 / 10 - PASS
- **Reads:** the studded body, teal slit eyes in black sockets under dark brows (`_close_sheet`: one slit, no pupil, brows in BROW_D), the domed skull, the pale tusks with mint caps, the ridged trunk, and the dark cuffs. The pale underside shows in `under`. The aqua body is the only blue in `_icons_strip_64`, and it reads as the mammoth at 64 px.
- **Numbers:** tris_body 14,688 (cap 15k); `tris_glow` empty; HEIGHT 9.0.
- **Held back from 9:** the pale belly band still reads as a plate in `model_side`; the mid lock row repeats; the brows' outer ends read a little light in `close_front`.

## Per-clip table

| clip | score | one line why | evidence file |
|---|---|---|---|
| idle | **8.4** | The trunk swing now reads well: the tip moves 0.253 BU from f0 to f20, and the tip is clearly lower at f0 and raised at f20 at 390 px. The ear flap (f40) and the breath (3 deg) are still not readable as beats at 390 px. The trunk carries the whole clip. | `beat_f85r4_iw_side_idle_000/030/040.png`, `_beats_f85r4_iw_side.png`, `verify.json` |
| walk | **8.4** | Feet step in the true lateral order (BL f0, FL f10, BR f20, FR f30). The trunk swing is now visible (about 20 px of tip travel between f10 and f20 in the side frames; tip 0.214 BU). The body bob is still about 1 px (sink 0.012 BU), so the back line does not visibly move and the walk still reads stiff. | `beat_f85r4_iw_side_walk_010/020.png`, `_beats_f85r4_iw_side.png`, `footfalls.txt`, `verify.json` |
| roar | **8.6** | The trunk rising to the sky and the hold read clearly. The mouth is clearly open from the front, below and 3/4. From a pure side it is still a thin dark wedge under the cheek (26 px at 420 px), partly covered by the near tusk root. Unchanged except the 0.01 MOUTH_IN move, which left the side band the same size. | `_roar_mouth.png`, `pclose_side_roar_34.png`, `verify.json` |
| act (dust-over) | **8.6** | The scoops reach the snow (tip on the ground at f18-22, f64-68, f78-82; FX holds 0.0111, under 0.012). The flick passes over the head from f44 to f58 (FX z 1.730 at f56 vs dome top 1.76). The max swing is 53.7 (under 60). The name says "over the back", but the flick peaks at the crest and brow. | `_beats_f85r3_act_side.png`, `_beats_f85r3_act_tq.png` (04:41, numbers unchanged) |

**Lowest clip: idle 8.4 and walk 8.4. Clips = 8.4 (FIX).**

## Audit items (round 5)

**Idle**

| item | result | evidence |
|---|---|---|
| Ear flap at f40, 10 to 13 deg | PASS (applied); visibility PARTIAL | `pets/IceMammoth.py` idle `ears(...)` line uses 13 * bell(f, 40, 6). Head-box diff f30 vs f40 is 1,214 px, so a change exists, but it reads as fringe, not silhouette. |
| f40 ear flap visible in a side render at 390 px | **FAIL** | Single frames f30 and f40 look the same to the eye. The f36 vs f44 diff is 7 px, but the bell is symmetric about f40, so that comparison cannot show the peak. |
| Chest breath 2.0 to 3.0 deg (chest vs spine <= 5) | PASS on the numbers; visibility **FAIL** | `chest_vs_spine` idle 3.0 (verify.json). A 3 deg chest tilt is about 7 px at the bib at 390 px, but the chest and head move together and the change is not visible at sheet scale. |
| Trunk roll (3.2, 4.8, 5.6, 5.6) | PASS | Code line `rl = [a * pk.wave(...) for ... (3.2, 4.8, 5.6, 5.6)]`. |
| Trunk tip travel f0 to f20 >= 0.25 BU | PASS | CLIP_NOTES coordinates: (0.069, -1.439, 0.114) to (-0.142, -1.532, 0.219) = 0.253 BU. |
| Neck <= 8, chest vs spine <= 5, collision_free, loop closed, idle foot drift 0 | PASS | verify.json: neck 0.6, chest 3.0, `collisions_with_hinges` {}; `audit.idle.idle_foot_drift` 0.0. |

**Walk**

| item | result | evidence |
|---|---|---|
| Body roll +-1.5 to +-2.5 deg | PASS (code) | `-2.5 * pk.wave(...)` in `body(f)`. Visible only as a slight lean. |
| Spine pitch rock 0.4 to 0.7 deg | PASS (code); visibility PARTIAL | `0.7 * pk.wave(...)`. About 3 px at the rump at 390 px. |
| Sink 0.008 to 0.012, so the back line moves | PASS (code); **FAIL** on "visible back-line level change" | Body z is `-0.022 - 0.012*b` (b peaks at contacts f10 and f30). 0.012 BU is about 1.3 px at 390 px. Not visible in the frames. |
| Trunk side swing 3 to 6 deg per step | PASS | Code `(1.2, 1.6, 1.6, 1.6)` sums to 6.0. |
| Trunk fore-aft pendulum about 11 deg | PASS | Code `(2.3, 3.0, 3.0, 3.0)` sums to 11.3. Visible in the side frames. |
| Tip travel f10 to f20 >= 0.2 BU | PASS | CLIP_NOTES coordinates: (-1.616, 0.220) to (-1.425, 0.124) = 0.214 BU. |
| Stride 0.3194, slide 0.0, foot_z_var 0.0, loop closed | PASS | `stride` 0.3194; `audit.walk.slide` 0.0; `foot_z_var` 0.0; loop_pos and loop_rot 0.0. |
| Walk max adjacent swing <= 60; neck <= 8; chest vs spine <= 5 | PASS | verify.json: max swing 7.9 (Shin_FL); neck 0.8; chest 1.68. |

**Roar and act (not changed except MOUTH_IN)**

| item | result | evidence |
|---|---|---|
| Roar mouth open from the side (NICE: MOUTH_IN 0.01 back) | PARTIAL | `pclose_side_roar_34`: the dark band is still 26 px at 420 px, unchanged, and the near tusk root still covers the front edge. Front, below and 3/4 views are clearly open. |
| Roar jaw max <= 22, pitch-up <= 30, collision_free, ends at rest | PASS | jaw 22.0 (f34), pitch-up 16.0, `end_vs_rest` 0.0. |
| Act scoops reach contact; FX holds <= 0.012 | PASS | `_beats_f85r3_act_tq` (tip on the ground at f18-22, f64-68, f78-82); FX holds 0.0111; `ground_min_z` act -0.016. |
| Act flick passes over the head | PASS | `_beats_f85r3_act_side` f44-f58: the trunk arcs above the dome line; FX z 1.730 at f56 vs dome top 1.76. |
| Act max swing <= 60; head pitch-up <= 30; ends at rest | PASS | 53.7 (f76); 17.0; 0.0. |
| Act name "over the back" | PARTIAL (not scored) | The flick peaks at the crest and brow, not the back. |

**Global**

| item | result | evidence |
|---|---|---|
| ground_min_z >= -0.02, all clips | PASS | idle 0.018, walk 0.015, roar 0.018, act -0.016 (export json). |
| collision_free, all clips | PASS | `collisions` {}, `collision_free` true. |
| Idle, walk, roar, act loops and rest | PASS | Loops closed; roar and act end at rest. |
| Tris <= 15k; no glow; HEIGHT 9.0 | PASS | 14,688; `tris_glow` {}; height 9.0. |
| ANIM_REFS rule | OWNER DECISION | Not scored. |

## MUST (blocks 8.5; idle and walk only)

**Idle (8.4)**

1. **M1, ear reads from the side.** In `idle()`, change the ear term `13 * bell(f, 40, 6)` to `18 * bell(f, 40, 6)`. Measure in the headless probe: the free edge of Ear_L and Ear_R (the tip of each ear bone) must move at least 0.06 BU in the side plane between f30 and f40. Check: the f30 and f40 side frames at 390 px must show a change in the ear's outline, not only in the fringe (about 6 px at 110 px per BU). Keep neck <= 8, chest vs spine <= 5, and collision_free true.

2. **M2, breath reads.** In `idle()`, change the chest breath `rot=(3.0 * br, 0, 0)` to `4.5 * br` (still under the 5 deg chest limit). Change the Spine breath term `loc=(0, 0, -0.004 * br)` to `+0.03 * br`, so the back rises on each breath instead of sinking. Measure: the back top (dome) must rise at least 0.03 BU from the breath trough to the peak (headless probe, Spine z). Re-run collision_free, loop closed, idle foot drift 0.

**Walk (8.4)**

3. **M3, back line bobs.** In `walk()`'s `body(f)`, change the Spine loc `(0, 0, -0.022 - 0.012 * b)` to `(0, 0, -0.004 - 0.030 * b)`. This keeps the contact heights the same (the contacts at b = 1 stay at -0.034) and raises the mid-swing back by 0.018 BU. The back line then moves about 0.03 BU (about 3 px at 390 px). Keep the planted feet: foot_z_var 0.0, walk slide 0.0, `ground_min_z` >= -0.02. If any planted foot moves, cut the amplitude to 0.020 and re-check.

## TO 9+ (in order of impact)

**Model**
1. Belly pale band: break its top edge with 2 stud rows of WOOL_D (round 4 item).
2. Mid lock row: vary height by about +-0.02 BU, not just length, so the row has no rhythm.
3. Brows: darken the outer 30% of each brow slab to about (56, 72, 84) (the outer ends read light in `close_front`).
4. Body colour (80, 150, 176): lead ruling, not scored.

**Clips**
1. Roar tremble (+-3 deg): not verifiable from stills. Check at game speed in Studio.
2. Act name vs flick height: either rename the act "dust over the brow" or raise the f48-f56 Trunk1 and Trunk2 keys by about 3 deg so the tip clears the dome by at least 0.03 BU. Keep the one-frame swing under 60 (now 53.7 at f76).
3. Act one-frame swing 53.7 (f76): check for a snap in the game clip.
4. Re-render `_model_sheet`, `_close_sheet` and the act sheets at the 05:57 export. They predate the MOUTH_IN move.
5. M1 and M2 (ear and breath) need a game-distance check in Studio once they are in.

## Pass / fail checklist (round 5)

| check | result |
|---|---|
| **MODEL** | |
| Tris <= 15k | PASS (14,688) |
| HEIGHT 9.0 | PASS |
| Species reads at 64 px | PASS (`_icons_strip_64`) |
| Studded body, head, legs, trunk | PASS (`_model_sheet`) |
| Eyes: one slit in a black socket, no pupil | PASS (`_close_sheet`) |
| Pale underside visible | PASS (`under`) |
| No glow | PASS |
| **CLIPS** | |
| collision_free, all 4 clips | PASS |
| ground_min_z >= -0.02 | PASS |
| Loops closed, walk slide 0 | PASS |
| Roar and act end at rest | PASS |
| Neck <= 8, chest vs spine <= 5 | PASS |
| Head + neck pitch-up <= 30 | PASS (16.0, 17.0, 0.8, 0.47) |
| Jaw max <= 22 | PASS (22.0) |
| Max adjacent swing <= 60 | PASS (53.7) |
| Scoop holds FX <= 0.012 | PASS (0.0111) |
| Idle trunk tip travel >= 0.25 BU | PASS (0.253) |
| Walk trunk tip travel >= 0.2 BU | PASS (0.214) |
| Idle ear flap readable at 390 px | **FAIL** |
| Idle breath readable at 390 px | **FAIL** |
| Walk back line visibly moves | **FAIL** |
| Roar open mouth readable from the side | PARTIAL |
| Act flick passes over the head | PASS |
| Acts in place, no spins | PASS |

## Summary
- **Model: 8.6/10, PASS.** Unchanged from round 4; the MOUTH_IN move does not change the read.
- **Clips: 8.4/10, FIX.** Idle 8.4 and walk 8.4 are under the floor. Roar 8.6 and act 8.6 pass.
- **MUST:** M1 (ear 13 to 18 deg, free edge at least 0.06 BU), M2 (breath 4.5 deg plus a 0.03 BU Spine rise), M3 (walk Spine z to -0.004 - 0.030*b, keeping contacts and foot checks).
- **Unverified at phone scale:** the roar tremble and the ear and breath at true game distance.
