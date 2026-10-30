# Permafrost Titan - clip notes (CLIP GATE, 2026-10-27)

References: `ANIM_REFS.md` (Muybridge Plate 27 heavy-load walk via the animationreference.org locomotion guide,
Muybridge Plate 356 kneel and rise, refs #3 / #9).
Gate run: `headless_full ... 1` (step 1) -> `_scratch/clipgate.txt`. Sheets: `renders/_pose_tq_sheet.png` (24 beats),
`renders/_cv_kneel_side.png` + `_cv_kneel_front.png` (the act from fixed side / front cameras).

## FINAL 8.5 ROUND 11 - THIGH READ (2026-10-28, after `_review/PermafrostTitan_final85_r10.md`: act 8.4) - EXPORTED 14:23
Backups:
- this export: `_scratch/PermafrostTitan_exported_r11.py`, `_scratch/r11_export_files/`
- the round-10 export: `_scratch/PermafrostTitan_exported_r10.py`, `_scratch/r10_export_files/` (FBX 14:02, lua, json)

Only the left-arm table of `act_kneelrise` changed. Idle / walk / roar clip data are identical to round 10 **and**
round 8 (json compare), and so are the events and the model. Yaw stays 30; the leg, the knee and the timing are
unchanged.
- **Where the thigh was hidden** (`_scratch/thigh_probe.py`: fixed game camera after a depsgraph update, 350 px grid,
  f40): Leg_L is covered by Shin_L 1,905 px, the hanging **upper arm (Arm_L) 1,450 px**, and the Spine 1,176 px. The
  upper arm was the lever, not the fist or forearm.
- **Lever A, knee pole** (act-only pole override, eased f12-18 / f52-62; `_scratch/r11_pole.txt`): **rejected.**
  - Every 20 deg of pole rotation moves the knee 6-8 cm. Outward (+x): +0.078 (20 deg), +0.129 (40 deg); inward:
    -0.066 (-20 deg).
  - The best thigh it reached (0.679 at +20 deg) still missed 0.70, with the knee off the snow.
  - The ankle offset (`KNEE_OUT` 0-0.30, `r11_ko.txt`) does the same: the knee leaves the band at once (0.12 -> +0.054).
- **Lever B, left arm with the thigh metric** (`r11_arm.txt` 60 holds: out -11..+9, fwd 4..34, bend 14..45;
  `r11_arm2.txt` fine sweep fwd 26..32, bend 0 / 14):
  - Within fwd <= 14 (the review's range) the best is 0.692 (out +9).
  - Clearing the thigh needs the upper arm forward: fwd >= 30 gives Leg_L >= 0.75 screen and >= 0.60 vert.
  - **Chosen hold (4, 32, 0)**: a straight arm 32 deg forward, so both fists brace forward over the raised right knee
    (side view: `_scratch/r11/_arm_cmp_f40.png`). f18 key (1, 24, 12) reaches forward on the landing; the f53 key
    (4, 28, 10) stays forward so the thigh is still clear at f50.
  - Fist 0.326 off the thigh (>= 0.05), fist centre z 0.52 (< 0.80), no arm-leg overlap f8-64.
  - NICE 1 (fist resting 0.05-0.08 on the thigh) conflicts with MUST 1: any fist on the thigh puts the upper arm over it
    from this camera.
- **Thigh / shin from the game camera** (screen share / vert share; r8 = `kneel_pix_r8.json` + `kneel_vis_r8.json`,
  r10 = `thigh_probe_base` + `kneel_vis_r10b.json`, r11 = `thigh_probe_r11_f*.json` + `kneel_vis_r11.json`):

  | part, frame | r8 | r10 | r11 |
  |---|---|---|---|
  | Leg_L thigh f40 | 0.591 / 0.487 | 0.636 / 0.487 | **0.759 / 0.637** |
  | Leg_L thigh f50 | 0.580 / 0.487 | 0.630 / 0.487 | **0.761 / 0.600** |
  | Shin_L f40 | 0.585 / 0.478 | 0.638 / 0.618 | **0.638 / 0.618** |
  | Shin_L f50 | 0.578 / 0.478 | 0.639 / 0.610 | **0.639 / 0.610** |
  | Foot_L f40 | 0.706 / 0.500 | 0.773 / 0.487 | **0.773 / 0.487** |

- **NOT met: background between the shin and the thigh.**
  - Measured as background px inside the on-screen hip-knee-ankle triangle: **0 px** at r10 and r11 (yaw 30).
  - The same 0 px after every leg variant tried (pole, knee-out, ankle).
  - Yaw 45 / 60 with this arm gives only 24 / 47 px (`r11_yaw_armfwd.txt`), and the arm covers the thigh again
    (Arm_L 1,450 / 5,072 px).
  - From the high camera behind, the shin rises back toward the camera and always projects over the thigh. The chunky
    blocks are wider than the L's opening, so no background shows inside it (3x crop `_kneel_3x_game_f30_f40_f50.png`).
- **Gates** (export run `_scratch/export_r11.txt`, `kneel_vis_r11.json`, `knee_frames_r11.json`):
  - Knee f18-52 **-0.0030 to -0.0001**; touch-down **f18** (`icecrack`); xy drift after touch-down 0.010.
  - Toes -0.0172; act ground -0.017; rest 0.0 from f84.
  - collision_free **true**; no arm-leg overlap on either side.
  - Linear 0; loops 0 / 0; walk slide 0.0; standing foot drift 0.0.
  - Chest 4.68 (f57); head 14.11 (f20); tris 7,820; events unchanged.
- **Evidence** (title bars "final 8.5 round 11", rendered 14:23-14:24):
  - `renders/_kneel_2x_f30_f40_f50.png`, `_kneel_2x_f40_f50.png`.
  - `_kneel_3x_game_f30_f40_f50.png` (new: 3x lower-body crop from the game camera).
  - `_kneel_close_f30_f40_f50.png`, `_beats2x_kneel.png`, `_kneel_game_strip_f0_f64.png`, `_kneel_views.png`,
    `_pose_tq_sheet.png`.

## FINAL 8.5 ROUND 10 - TOES TUCKED 40 (2026-10-28, lead ruling 10-28) - EXPORTED 14:02
Backups:
- this export: `_scratch/PermafrostTitan_exported_r10.py`
- the round-8 export: `_scratch/PermafrostTitan_exported_r8.py`, `_scratch/r8_export_files/` (FBX 09:53, lua, json)

Only `act_kneelrise` changed. The idle / walk / roar clip data is **identical** to round 8 (the exported json
compared clip by clip), and so are the events and the model. Yaw stays **30** and the timing is unchanged.
- **What changed (act only):**
  - The kneeling foot tucks its toes **40 deg** (was 16). Its ankle hold is **(0, 0.34, 0.18)** (was 0.365 / 0.101).
  - The pelvis drop is **0.380** (was 0.348).
  - Contact fixes:
    - the f15 ankle key is **(0, 0.34, 0.21)** (was 0.32 / 0.13), so the toes never dig in on the way down;
    - the f58 rise key keeps the r8 absolute hip height **-0.338**, so the knee pushes off inside the band instead of
      digging to -0.04.
- **Search** (`_scratch/r10b_search.txt` 72 rows, `r10b_search2.txt` 24 rows):
  - Toes 38-44, ankle up 0.17-0.20 and back 0.32-0.36, drop 0.355-0.385.
  - The rule was shin >= 60 % on the fixed camera, then the lowest knee.
  - Toes 40 / back 0.34 / drop 0.38 is the lowest knee that stays >= 60 % at f30, f40 **and** f50. Back 0.33 / drop 0.38
    sits 1.4 mm lower but drops to 59.6 % at f50.
- **Visibility on the game camera** (the `arm_search.py` method with the camera fixed -> `arm_search_r10b_fixedcam.txt`;
  screen share -> `kneel_pix_r10b.json`):

  | f40 (f50) | r8 vert | r10 vert | r8 screen | r10 screen |
  |---|---|---|---|---|
  | shin | 47.8 (47.8) | **61.8 (61.0)**; f30 62.5 | 58.5 (57.8) | **63.8 (63.9)** |
  | foot | 50.0 (49.4) | 48.7 (46.3) | 70.6 (70.4) | **77.3 (76.8)** |
  | thigh | 48.7 | 48.7 | 59.1 (58.0) | **63.6 (63.0)** |

- **Knee height per frame** (the lowest Shin_L point within 0.14 of the Knee_L joint; `knee_frames_r8.json` /
  `knee_frames_r10b.json`):

  | f | 14 | 15 | 16 | 17 | 18 | 20 | 25 | 30 | 34 | 40 | 45 | 50 | 52 | 54 | 56 | 57 | 58 | 59 | 60 | 62 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | r8 | +.0707 | +.0269 | +.0025 | -.0072 | -.0117 | -.0161 | -.0112 | -.0079 | -.0062 | -.0080 | -.0104 | -.0117 | -.0089 | -.0067 | -.0078 | -.0095 | -.0096 | -.0042 | +.0097 | +.0574 |
  | r10 | +.0334 | +.0109 | +.0047 | +.0017 | **-.0008** | -.0011 | -.0008 | -.0004 | -.0001 | -.0004 | -.0007 | -.0008 | -.0030 | -.0105 | -.0136 | -.0140 | -.0126 | -.0061 | +.0083 | +.0574 |

  - Hold f18-52: **-0.0030 to -0.0001**. The knee touches the snow the whole hold and never rises above it (the lead
    allowed up to +0.010).
  - **Touch-down f18 = the `icecrack` event (0.18)** - this is the frame for the snow-puff VFX at `Knee_L` (r8: f17).
  - The knee comes down with no bounce. The Knee_L joint drifts 0.010 in xy after touch-down (r8: 0.037).
  - On the rise (f54-59) the knee pushes into the snow (-0.014 lowest), then lifts at f60.
- **Gates** (export run `_scratch/export_r10.txt`, `kneel_vis_r10b.json`):
  - collision_free **true**; no arm-leg overlap on either side (f8-64).
  - Act ground **-0.017** (left toes, f18-53); f84-100 rest 0.0. Idle / walk / roar ground 0.0.
  - Linear 0; idle / walk loops 0 / 0; walk slide 0.0; idle foot drift 0.0.
  - Standing foot Foot_R drift **0.0**, min z 0.0.
  - Chest vs spine **4.68** (f57); Head **14.11** (f20; no neck bone).
  - Tris 7,820; lua 32,186 bytes; events unchanged.
- **Evidence** (renders, title bars "final 8.5 round 10", rendered 14:02):
  - `renders/_kneel_2x_f30_f40_f50.png` (game + tq, 700 px), `_kneel_2x_f40_f50.png`.
  - `_kneel_close_f30_f40_f50.png` (game + tq at half distance, aimed at the knee).
  - `_beats2x_kneel.png` (f0 / 9 / 18 / 20 / 40 / 50 / 58 / 70 / 84).
  - `_kneel_game_strip_f0_f64.png` (every 4 frames, with times at 30 fps).
  - `_kneel_views.png` (front / tq / back / game at f18 / 40 / 58).
  - `_pose_tq_sheet.png`.

## ROUND 10 - SIDE-ON KNEEL (2026-10-28, Builder A; brief: yaw 60-75, shin >= 60 % at game f40) - NOT PASSED, NO EXPORT
The pet file is back to the round-8 export (byte-identical to `_scratch/PermafrostTitan_exported_r8.py`). The FBX in
`C:\cdimp` is still the 09:53 one. The test file with every switch is in `_scratch/PermafrostTitan_r10_attempt.py`.
- **Bug in the r9 metric:** `arm_search.py` read the camera's `matrix_world` right after `pk.aim` without a depsgraph
  update. So the camera was the stale one at the world ORIGIN (0, 0, 0), not the game camera at (1.60, 3.50, 4.04)
  (`_scratch/cam_check.py`). The r9 "shin 28.7 %" was seen from the floor.
  - Fixed in `arm_search.py` / `arm_search10.py`; the old copy is `arm_search_r9_buggy.py`.
  - **Corrected "before"** (round-8 export, real game camera, `arm_search_r10_fixedcam_r8.txt`): shin **47.8 %** (f40
    and f50), foot **50.0 / 49.4 %**.
  - The corrected full 36-hold grid (`arm_search_r10_fullgrid.txt`): shin 38.2-47.8 %, foot 50 % for every hold. So
    the exported hold is already the best.
- **Yaw test** (whole body about the planted right ankle, eased f8-18 / f52-64; `kneel_vis_y*.json`,
  `kneel_pix_y*.json`). Shin / foot / thigh visibility at game f40, vert share (arm_search method) / screen-area share:

  | yaw | shin | foot | thigh (screen) |
  |---|---|---|---|
  | 30 (r8) | 47.8 / 58.5 | 50.0 / 70.6 | 59.1 |
  | 45 | 46.3 / 58.7 | 48.7 / 65.6 | 48.3 |
  | 60 | 42.6 / 58.5 | 48.1 / 59.8 | 25.3 |
  | 75 | 39.0 / 54.3 | 46.9 / 52.3 | 3.8 |

  - More yaw does NOT show more shin. From 45 up, the left arm and fist come between the camera and the thigh (at 75
    they hide 96 % of it).
  - The yaw itself was clean at every value:
    - knee -0.0062 to -0.0161 over f18-52, lands f17;
    - Foot_R drift 0 and min z 0;
    - no arm-leg overlap;
    - Chest 4.68, Head 21.0 (with a 15 deg head counter-turn; limit 30).
- **Why:** 36 % of the shin's verts are buried inside the knee and foot blocks in this kneel (22 % at rest;
  `kneel_cap_*.json`).
  - Even the best of 24 camera azimuths at the game elevation sees only **53.7 %** of the shin.
  - So 60 % is out of reach by yaw alone, at any angle.
- **Pose levers tried** (`tuck_grid_y45.txt`, `tuck_grid2.txt`; all collision-free):
  - **Toes tucked 40 deg, ankle +0.18:** shin 64.0 % / 63.9 % at yaw 30, 58.8 % / 64.7 % at yaw 45. But the knee lifts
    to **+0.010 (off the snow)**.
  - **Every setting that puts the knee back in the band** (deeper drop 0.37-0.39, pelvis shift, ankle fwd / back, toes
    28-36) brings the shin back to <= 53 % (vert).
  - The best knee-valid one at yaw 45 (toes 32, drop 0.37): 43.4 % vert / 61.2 % screen, but the thigh falls to 51.8 %.
    It is not better than r8.
  - **Flat top-of-foot kneel (toes 150-180):** the foot is fully visible, but shin 35-41 % and the knee sinks
    to -0.02 / -0.03.
  - **Left-arm holds:** no effect on the shin (corrected grid above).
- **Result:** no setting meets yaw >= 45 + shin >= 60 % + knee on the snow together, so nothing was exported.
  - Knee lands **f17** (round-8 export, unchanged; `icecrack` at 0.18 = f18) - for the snow-puff VFX at `Knee_L`.
  - Gates on the restored file (`fullcheck`): collision_free true, act ground -0.016 (f20), loops 0 / 0, slide 0,
    linear 0, tris 7,820; Chest 4.68 (f57), Head 14.11 (f20).
  - Evidence: `_scratch/r10/_r10_side_on_tests_f40.png` (all 7 variants, game + 2x, 13:44); `_scratch/r10/_cmp_yaw.png`.

## FINAL 8.5 ROUND 9 (2026-10-28, after `_review/PermafrostTitan_final85_r9.md`: act 8.2) - NO CHANGE, NO RE-EXPORT (lead: stop and report)
- **MUST 1, left-arm search:** a full grid of out -11 / -6 / -1 / +4, fwd -6 / 4 / 14, bend 0 / 15 / 30 = 36 holds.
  - Each was measured on the fixed game camera at f40 (`_scratch/arm_search.py` -> `arm_search_r9.txt`). The Arm_L /
    Fore_L / Hand_L fcurves are muted and set by hand; every other bone keeps its exported pose.
  - **21 of 36 holds pass** the arm rules (0 overlap of Fore_L / Fist_L / Hand_L with Leg_L, fist gap >= 0.05).
  - **None changes what the camera sees:** the kneeling shin is **28.7 %** visible and the foot **46.3 %** in all 36
    (and at f50: 28.7 / 45.6 %), the same as the exported hold (out -6, fwd 14, bend 14).
  - **The occluders are the leg itself, not the arm.** Of the hidden shin verts, 44 sit behind the thigh (Leg_L) and 53
    behind the foot (Foot_L). Of the hidden foot verts, 75 sit behind the shin and 11 behind the thigh. Zero arm parts
    occlude.
  - From the camera behind, the thigh, shin and foot line up along the view, so the shin self-occludes.
  - Per the lead, no further arm or leg change. **The round-8 export (09:53) stands.**
- **Re-logged (round-8 file, `_scratch/ang_r9.txt`):**

  | clip | chest vs spine | head max |
  |---|---|---|
  | idle | 4.85 (f30) | 13.5 |
  | walk | 4.03 (f36) | 1.4 |
  | roar | 3.0 (f10) | 15.0 |
  | act | **4.68** (f57) | **14.1** (f20) |

  The act values match round 6, because the round-7 / round-8 changes (feet, knee, left arm) do not touch the Chest
  or the Head.

## FINAL 8.5 ROUND 8 (2026-10-28, after `_review/PermafrostTitan_final85_r8.md`: model 8.6, idle / walk / roar 8.5, act 8.2) - re-exported 09:53
Backups:
- the round-7 export: `_scratch/PermafrostTitan_exported_r7.py`
- this export: `_scratch/PermafrostTitan_exported_r8.py`

Only the act changed. The hidden standing leg is not counted (lead ruling).
- **MUST 1, re-solved:**
  - `KNEE_OUT` **0.06**: the kneeling ankle target goes 0.06 out (body frame) for the hold, eased f12-18 / f52-62.
  - The pelvis drop goes **0.326 -> 0.348**, so the knee stays on the snow: **-0.006 to -0.016** over f18-52.
  - The left arm's hold goes from out -11 to **-6** (f18 key -4 -> -1), so it clears the wider thigh.
    - No Fore_L | Leg_L contact anywhere (collision_free true).
    - The fist sits 0.126 above the thigh surface; fist centre z 0.49, under the chest line 0.80 (`fist_probe`).
  - No knee settle was added.
  - The act ends at exact rest (f84-100 ground 0.0).
- **The kneeling shin on the game camera** (`_scratch/shin_px.py`, knee -> ankle on the fixed game camera at 700 px):

  | ankle offset | shin on screen | angle to the view line (90 = side-on) |
  |---|---|---|
  | 0 (round 7) | 75.8 px | 53.7 deg |
  | **0.06 (this export)** | **79.1 px (f40), 79.0 (f50)** | **56.7 deg** |
  | 0.08 (the fallback, measured) | 80.6 px | 58.1 deg |
  | -0.08 (inward, measured) | 71.7 px | 50.4 deg |

  - Outward is the right direction, but the gain is small (+4 %). The fallback would add only +1.5 px and lift the knee
    more, so it was not used.
  - From behind, the camera still sees the shin about 33 deg off its side-on angle - a limit of the kneel / yaw geometry.
- **Gate** (`_scratch/export_r8.txt`):
  - collision_free **true**; act ground **-0.016** (f20); linear 0; loops 0 / 0; tris 7,820.
  - Idle / walk / roar keys are unchanged.
- **Renders** (title bars 09:53-09:54, "final 8.5 round 8"):
  - `_kneel_2x_f30_f40_f50` (game + tq), `_kneel_2x_f40_f50`, `_kneel_views`, `_beats2x_kneel`.
  - The full sheet set and the icon strips.

## FINAL 8.5 ROUND 7 (2026-10-28, after `_review/PermafrostTitan_final85_r7.md`: model 8.6, idle / walk / roar 8.5 PASS, act 8.1) - re-exported 09:41
Backups:
- the round-6 export: `_scratch/PermafrostTitan_exported_r6.py`
- this export: `_scratch/PermafrostTitan_exported_r7.py`

Idle, walk and roar are untouched.
- **MUST 1 (act), the standing foot:** `STAND_OUT = 0.10`.
  - The right foot steps 0.10 further out (body frame, away from the kneel side) during the yaw ease-in. It lifts 0.05
    at f15.
  - It is planted for the whole hold: Foot_R stays at (-0.377, -0.330, 0.165) at f18, f30 and f52; min z 0.0, no slide.
  - It steps back f52-62 (lift 0.05 at f57). The 30 deg yaw and the act's exact rest are unchanged.
- **The knee option (0.06 outward) was tried and dropped** (`KNEE_OUT = 0`):
  - it lifted the kneeling knee OFF the snow (lowest point over the hold 0.0);
  - it put the left forearm into the thigh (Fore_L | Leg_L, f21-30).
- **Result - the pass is NOT reached; the standing leg stays hidden.** Measured on the fixed game camera at f40
  (`_scratch/leg_px.py`: projected px boxes + the share of each bone's verts not covered by other parts):

  | stand-out | Shin_R visible | Foot_R visible | Shin_L visible |
  |---|---|---|---|
  | 0.10 | 0.00 | 0.03 | 0.49 |
  | 0.25 (test) | 0.00 | 0.04 | 0.49 |

  - The standing shin projects ABOVE the kneeling leg on screen (y 370-480 vs 550-650 of 700 px), i.e. under and in
    front of the torso, which hides it from the high camera behind.
  - After the 30 deg yaw a body-lateral step moves only ~58 %% into the image's horizontal (0.10 BU = ~15 px). The
    torso + left arm cover x ~180-540, so the shin would need ~1 BU of sideways step to clear it.
  - Tested stand-outs: 0.10, 0.18, 0.25 (`_scratch/standout_cmp.png`) - no visible change.
  - What could work (lead call):
    - (a) A kneel whose standing leg goes out to the SIDE rather than forward (a different K1 step from the reference;
      the foot ~0.3 lateral, ~0.1 forward).
    - (b) Accept the read from behind as the kneeling leg's L alone (thigh down to the knee on the snow, shin flat).
    - (c) A Studio-side snow puff at `Knee_L` (`icecrack`) to sell the contact.
- **Gate** (`_scratch/export_r7.txt`):
  - collision_free **true**; knee **-0.005 to -0.017** over f18-52; ground -0.017 (f20); linear 0; loops 0 / 0.
  - Idle / walk / roar numbers unchanged (round 6).
- **Renders** (title bars 09:41-09:43, "final 8.5 round 7"):
  - `_kneel_2x_f30_f40_f50` (game + tq), `_kneel_2x_f40_f50`, `_kneel_views`, `_beats2x_kneel`.
  - Also re-made with the full set: `_beats2x_idle` / `_roar`, `_walk_sheet`, `_roar_front_sheet`, `_roar_jaw_close`,
    `_model_sheet`, `_close_sheet`, the icon strips, `_pose_tq_sheet`.

## FINAL 8.5 ROUND 6 (2026-10-28, after `_review/PermafrostTitan_final85_r6.md`: idle 8.0, walk 8.2, roar 8.1, act 7.9) - re-exported 09:17
- **ACT-1, kneel yaw (lead: up to 30 allowed):**
  - I tested 25 and 30 on the game camera (`_scratch/yaw_cmp_f40.png`, zoom `_scratch/yaw_cmp_zoom.png`; 18 / 25 / 30).
  - At 25 the shin still slants down toward the camera and half-reads as a step. At **30** the thigh comes straight down
    to the dark knee on the snow and the shin + foot lie flat to the side: a clear L. So **YAW_K = 30**.
  - Same pivot (the planted right ankle; right foot min z 0.0, no slide) and the same `leg_unyaw`.
  - Knee **-0.005 to -0.017** (f17-53); the act ends at rest (yaw 0 by f62).
  - Evidence: `renders/_kneel_2x_f40_f50.png` (game + tq), `_kneel_views.png`.
- **IDLE-1:** arm sway **5 -> 7**.
  - Fist cycle range **L 0.142, R 0.137** (>= 0.12 both). f0 -> f30: L 0.133, R 0.033.
  - Closest fist-to-thigh gap 0.067 / 0.066 (>= 0.04); no collision; idle foot drift 0.
- **WALK-1:** pelvis shift over the stance foot **0.022 -> 0.035** BU; chest roll **3.0 -> 3.5** deg.
  - Walk slide 0.0; closest fist-to-thigh gap 0.057; fist range 0.215.
- **ROAR-1, arm asymmetry: not a bug.**
  - At roar f27 the arm joints mirror exactly: Arm (+/-0.480, 0.116, 1.563), Fore (+/-0.787, 0.146, 1.239), Hand
    (+/-0.884, -0.168, 1.033), Fist (+/-0.878, -0.400, 1.052).
  - So the fists are at the same height and the out angles are equal. `arms_fk` converts the `-s * out` roll into armature
    axes through each bone's rest matrix, so the bone roll cannot skew it.
  - The tq camera's perspective (one arm toward the camera, one away) made it look uneven.
  - Front sheet f0 / f22 / f27 / f50: `renders/_roar_front_sheet.png` (symmetric).
- **MC4' mouth:** left for the Studio check (lead ruling: don't chase the kit luma).
- **Per clip:**

  | clip | chest vs spine (<= 5) | head max | ground | other |
  |---|---|---|---|---|
  | idle | 4.85 | 13.5 | 0.0 | foot drift 0; fist range 0.142 / 0.137 |
  | walk | **4.03** | 1.4 | 0.0 | slide 0.0 |
  | roar | 3.0 | 15.0 | 0.0 | arms symmetric |
  | act | 4.68 | 14.1 | -0.017 (f20) | yaw 30, ends at rest |

  Probes: `_scratch/ang_r6.txt`, `arm_r6.txt`, `clipgate_r6.txt`.
- **Step 1** (`_scratch/export_r6.txt`): collision_free **true**; linear 0; loops 0 / 0; tris 7,820.
- **Renders** (title bars 09:18, "final 8.5 round 6"):
  - `_kneel_2x_f40_f50` (game + tq), `_kneel_views`, `_beats2x_idle` / `_roar` / `_kneel`.
  - `_walk_sheet` (tq + game + side), `_roar_front_sheet` (front) + `_beats2x_roar` (tq), `_roar_jaw_close`.
  - `_model_sheet`, `_close_sheet`, the two `_icons_strip` and two `_icons2_strip` sizes, `_pose_tq_sheet`.

## FINAL 8.5 ROUND 5 (2026-10-28, after `_review/PermafrostTitan_final85_r5.md`, clips 7.7: idle 7.6, walk 7.6, roar 8.0, act 7.5) - re-exported 08:24
Rulings applied: the fist on the knee is fine visually (the 0.03 centre test is dropped; the surface gap 0.092 stays
the logged number); no neck rule (no Neck bone; head + neck <= 30).
- **MC1', kneel from the game camera (lead ruling: body yaw, NOT another ankle tweak):**
  - The WHOLE body yaws **18 deg** toward the L side.
  - Timing: ease in f12-18, hold f18-52, ease out by f62. The act ends at exact rest.
  - Pivot: a vertical axis through the planted right ankle, so the right foot does not slide and keeps its heading.
  - Both foot targets rotate with the body, so the left knee stays pinned: lowest point **-0.005 to -0.017** through
    f17-53, the same as round 4.
  - Why it is on the Spine and not the Root bone: the kit exporter never exports Root (petkit `sample()` holds Root at
    identity), so the Spine - the top exported bone that carries the hips, legs and chest - carries the yaw. The Spine
    location gets the pivot term `(P - O) - Rz(P - O)`.
  - A fix that was needed: the kit leg IK aims each bone by the shortest arc, which is not yaw-equivariant. Under the
    yaw the thigh and shin twisted about their own axes and the knee cap dipped to -0.03.
    - `leg_unyaw()` re-aims the thigh and shin as Rz(psi) @ (the un-yawed shortest arc) and re-keys the foot. The joint
      positions are identical; the twist is gone.
  - Game camera: `renders/_kneel_2x_f40_f50.png` (game + tq). Crop: `_scratch/zoom_game_kneel_r5.png` (left round 4,
    right round 5).
    - The thigh now drops to the snow and the shin and foot run off to the side, not straight at the camera.
- **MC2', idle:** arm sway +/-5 kept, plus a forearm bend **+/-4** on Fore_L / Fore_R in opposite phase to the arm sway
  (the breath flex is kept).
  - Fist travel f0 -> f30: **L 0.105** BU; R 0.023 (the right fist peaks at other frames - its cycle range is 0.087).
  - Closest fist-to-thigh gap in the idle: 0.068 (L) / 0.066 (R); no collision.
  - Probe: `_scratch/arm_probe.py` -> `arm_r5.txt`.
- **MC3', walk:** shoulder swing 9 kept; the forearm bend in opposite phase goes **+/-2 -> +/-6**.
  - Fist range over the cycle: **0.206** BU per side.
  - Closest fist-to-thigh gap: **0.060** (>= 0.03); walk slide 0.0.
- **MC4', mouth:** see MODEL_NOTES (cavity (10, 10, 14) + a 0.012 lip; kit luma ~81, so the Studio check is needed).
- **9+ beats:**
  - Idle: one slow heavy LOOK (ANIM_REFS K8c: a slow head turn, weight by stillness). Head yaw 0 -> 12 deg over
    f44-60, hold to f84, back by f100. It is a single turn, not a shake. Head max 13.5 deg.
  - Walk: a per-step shoulder roll; the chest roll goes 1.5 -> 3.0 deg, one rock per step side.
- **Per clip:**

  | clip | chest vs spine (<= 5) | head max | ground | other |
  |---|---|---|---|---|
  | idle | 4.85 (f30) | 13.5 | 0.0 | foot drift 0; loop 0 / 0 |
  | walk | **3.61** (f12) | 1.4 | 0.0 | slide 0.0; loop 0 / 0 |
  | roar | 3.0 | 15.0 | 0.0 | - |
  | act | 4.68 (f57) | 14.1 | **-0.017** (f20) | ends at rest |

  Probe: `_scratch/ang_all.py` -> `ang_r5.txt`.
- **Step 1** (`_scratch/export_r5.txt`):
  - collision_free **true**; linear 0 on all clips; events unchanged.
  - FBX 08:24.
- **Renders** (title bar 08:22, "final 8.5 round 5"):
  - `_kneel_2x_f40_f50` (tq + game), `_beats2x_idle` / `_roar` / `_kneel`.
  - `_walk_sheet` (tq + **game** + side), `_roar_jaw_close`, `_kneel_views`, `_model_sheet`.
  - `_pose_tq_sheet` (08:24).

## FINAL 8.5 ROUND 4 (2026-10-28, after `_review/PermafrostTitan_final85_r4.md`, clips 7.7) - re-exported 05:11
Coordinator ruling: the neck limit applies only to Neck bones. The Titan has none, so it is held to head + neck <= 30.
Measured head peaks: roar 15, act 14.1.
- **MC1, kneeling shin:**
  - The left ankle hold moves from aL + (0, 0.34, 0.155) to **aL + (0, 0.365, 0.101)** (f18-52).
    The f15 key is (0, 0.32, 0.13) and the f62 key is (0, 0.24, 0.10).
  - The toe curl TL goes from 26 to 16 for the flatter shin.
  - The knee stays pinned (DROP 0.326) and touches down at **-0.005 to -0.017** through f18-52.
  - Shin_L at f40 (`_scratch/joints_r4_f40.txt`): knee (0.266, 0.065, 0.140), ankle (0.250, 0.385, 0.266).
    The shin rises **21.5 deg** above horizontal; with the round-3 ankle target it was 31.4, so it leans back **9.9 deg**.
    The thigh is 9.0 deg off vertical.
  - From the game camera (`renders/_kneel_2x_f40_f50.png`, zoom `_scratch/zoom_game_kneel_r4.png`) the vertical
    thigh and the foot block coming back toward the camera form the L.
- **MC2, idle arm sway:** +/-2.5 -> **+/-5** (`sway = 5.0 * sn(f, n)`, the shoulders turn with the hips).
  - The closest the left fist gets to the thigh in the idle is **0.068**.
  - Chest vs spine stays at 4.85 (limit 5). `renders/_beats2x_idle.png`.
- **MC3, walk arm swing:** 5.5 -> **9**. The closest the left fist gets to the thigh in the walk is **0.065**. `renders/_walk_sheet.png`.
- **Fist re-measure (the kneel's left fist, f30-46):** probe `_scratch/fist_probe.py`, output `_scratch/fist_r4.txt`.
  - What it measures: the BVH surface distance from every vertex weighted to Hand_L / Fist_L to the nearest Leg_L
    face. It is a true surface-to-surface gap, not a vertex-to-vertex distance.
  - Nearest surface gap fist-to-thigh: **0.092** (f30, f40, f46).
  - Fist centre to the nearest thigh surface: **0.372**.
  - Fist centre height **z 0.502**, well under the chest line (z 0.824).
  - The 0.019 / 0.294 in `_scratch/fist_r3.txt` came from the REJECTED round-3 trial pose (-17, 6, 21): out 6 / fwd 21 put
    the forearm into the thigh (Fore_L | Leg_L).
    The kept pose (-11, 14, 14) is collision-free.
  - The ~0.09 floor comes from the forearm and bracer thickness: closing the gap further puts the forearm into the thigh first.
- **Chest vs spine (max, deg):** idle 4.85, walk 2.5, roar 3.0, act 4.68 - all <= 5.
- **Step 1** (`_scratch/export_r4.txt`):
  - collision_free **true**; ground 0 / 0 / 0 / **-0.017** (act f20); linear 0; loops 0 / 0; slide 0.0.
  - Events: idle frost1 / core1 / frost2 / core2; roar core1 / glint / icedust / core2; act icecrack / core1 / core2.
- **Renders** (title bar = 2026-10-28 05:05, "final 8.5 round 4"):
  - `_kneel_2x_f40_f50` (tq + game), `_beats2x_idle` / `_roar` / `_kneel`, `_walk_sheet`, `_roar_jaw_close`.
  - `_kneel_views`, `_model_sheet`, and `_pose_tq_sheet` (05:11).

## FINAL 8.5 ROUND 3 (2026-10-28, after `_review/PermafrostTitan_final85_r3.md`, clips 7.5) - re-exported 04:21
- **M3, left fist on the thigh: partly met.**
  - The review's values (out 6, fwd 22, bend 60) lift the fist to z 1.04, above the chest line (z 0.83), and 0.45 from
    the thigh.
  - I swept the pose with `_scratch/fist_probe.py` (fist-to-thigh surface distance) and `collide_where`
    (forearm-to-thigh). Every pose that brings the fist within ~0.05 of the thigh also cuts the thick forearm/bracer
    into the thigh top (Fore_L|Leg_L, 22-92 tri pairs).
  - The closest collision-free hold is **(out -11, fwd 14, bend 14)** at f30-46: the fist is **0.094** from the thigh
    surface, fist centre z 0.51, below the chest line. The f18 approach is (-4, 12, 24). The arm comes off the thigh
    f46-53 (4, 8, 24), before the f50-58 lean, and f62 (5, 4, 14) is kept.
  - In `renders/_kneel_2x_f40_f50.png` (tq) the fist rests in front of the thigh top.
  - The comment in the code now matches what is built.
- **M4, game-camera L-shape: both levers used.**
  - The Spine roll in the hold is **9** (was 7). The Head counter-roll is -5.5 (was -3.5), so the head stays level; the
    Chest stays -3.5, so chest vs spine is unchanged.
  - The kneeling foot's back sole sits **+0.02** higher in the hold (the ankle target 0.135 -> 0.155, f15-52).
  - The thinner knee cap needed the pelvis drop at **0.318** (was 0.312) to keep the knee on the snow. Ground probe:
    the LEFT knee is the lowest part from f18 to f52, at **-0.003 to -0.014** (the f20 settle).
  - `renders/_kneel_2x_f40_f50.png` (game f40 / f50 at 2x): the thigh drops from the hip, the shin lies back, the sole
    shows.
- **M5, idle shoulders.** The arms swing **±2.5 deg fwd/back with opposite signs** on the hip-yaw sine (the left arm
  back when the hips turn left).
  - I put it on the forward/back swing, not the vertical-axis slot: a hanging arm turned about the vertical only spins
    about its own length, so neither the fist nor the pauldron moves.
  - Chest vs spine is unchanged by it (the Arm bones).
- **Polish:**
  - Walk arm swing **5.5 deg** (was 4).
  - Idle breath pitch **1.8** (was 2.0); the head counter-pitch is 1.8.
  - Knee settle **0.005** (was 0.008).
- **Chest vs spine, measured (`ang_probe` on the Chest bone):**

  | clip | chest vs spine | head |
  |---|---|---|
  | idle | **4.85** | 2.3 |
  | walk | 2.5 | |
  | roar | 3.0 | 15 |
  | act | 4.68 | 14.1 |

  The idle is 4.85 because the yaw counter (4.5) stacks on the 1.8 breath, not the review's estimate of 4.6.
- **Step 1** (`_scratch/export_r3.txt`):
  - collision_free **true**. ground_min_z 0.000 for idle / walk / roar and **-0.014** for the act at f20.
  - Linear 0; loops 0 / 0; walk slide 0.0; idle foot drift 0. Tris 7,664. Events are unchanged; the anchor is `Knee_L`.
- **Fresh render set (title bars: rendered 2026-10-28 04:20):**
  - `_kneel_2x_f40_f50.png` (tq + game at f40 / f50, 700 px).
  - `_beats2x_idle.png`, `_beats2x_roar.png`, `_beats2x_kneel.png`.
  - `_walk_sheet.png` (tq + side, f0-42).
  - `_roar_jaw_close.png` (front + tq at f0 / f27; the dark mouth gap shows at f27).
  - `_kneel_views.png`, `_model_sheet.png`, and `_pose_tq_sheet.png` (24 beats).

## FINAL 8.5 ROUND 2 (2026-10-28, after `_review/PermafrostTitan_final85_r2.md`, FIX clips 7) - re-exported
- **MUST 4, the kneel is MIRRORED - it now kneels on the LEFT knee (the camera side):**
  - Same timing. The RIGHT foot steps forward 0.30 and 0.04 out.
  - The LEFT foot tucks and turns 10 deg out in the hold.
  - The Spine rolls +7 toward the left; the Chest and Head counter-roll -3.5. The f6 weight shift goes onto the left foot.
  - **The VFX anchor is renamed `Knee_L`** (`icecrack` f18), on `Shin_L` at the knee front. `Knee_R` no longer exists.
  - The slimmer knee cap and shin lifted the knee 0.03-0.04 off the snow, so the pelvis drop is **0.312** (was 0.272).
    Ground probe (`_scratch/ground_probe.py`): the LEFT knee (Shin_L) is the lowest part from f18 to f52, at -0.003 to
    -0.009 in the hold and **-0.018** at the f20 settle (limit -0.02).
  - **Asymmetric hold:** with the 0.31 drop the hanging fists reached the snow and the left fist covered the kneeling
    knee from the front and the 3/4. The RIGHT fist now rests forward on the raised right knee (fwd 20, bend 32). The
    LEFT elbow bends 48 so its fist sits on the thigh above the knee (out 12, fwd 8).
  - Evidence:
    - `renders/_kneel_close_f40.png`: the tq and game cameras at f40, plus close-ups aimed at `Knee_L` - the left knee
      cap is flat on the snow (3/4) and the left shin lies on the snow with the sole up (game).
    - `_kneel_views.png`: front / tq / back / game at f18 / 40 / 58.
    - `_beats2x_kneel.png`.
- **MUST 5, idle:** hip yaw **+/-6 deg** (was 4).
  - The Chest counter-yaws **-0.75 x yaw** (4.5 deg) and the Head -0.25 x yaw, so the head stays facing forward.
  - The review's -0.8 would make chest vs spine 5.2 deg at f30, where the 2 deg breath pitch stacks on it; -0.75 keeps
    it at **4.92**.
  - The fist flex stays at 8 deg. `renders/_beats2x_idle.png`.
- **Chest vs spine (measured, `CinderOverlord/_scratch/ang_probe.py` on the Chest bone):** idle 4.92, roar 3.0,
  act 4.68 (limit 5). Head max: roar 15, act 13.5.
- **Step 1** (`_scratch/export_r2.txt`):
  - collision_free **true**. ground_min_z 0.000 for idle / walk / roar; -0.018 for the act at f20 (the knee settle).
  - Linear 0. Idle and walk loops 0 / 0. Walk slide 0.0. Idle foot drift 0.
  - Tris 7,664. Events are unchanged.
- **Renders:** `_pose_tq_sheet.png` (24 beats), `_beats2x_idle/roar/kneel.png`, `_kneel_views.png` and
  `_kneel_close_f40.png`.
- **Export:** `C:\cdimp\PermafrostTitan.fbx` (2026-10-28 03:29).

## FINAL 8.5 (2026-10-28, after `_review/PermafrostTitan_final85.md`, FIX clips 6.5) - re-exported
- **MUST 3 (jaw):** see `MODEL_NOTES.md`. The lip rides `Jaw`, and a dark cavity sits behind it on `Head`. The roar jaw opens
  **24 deg** at f27 (12 at f22, 22 at f34, 20 at f50). `renders/_roar_jaw_close.png` shows the mouth gap.
- **MUST 4 (roar):**
  - The arms go out **22 deg** at f22 / f27 / f50 and **24** at f34; 10 at f58; -2 at f10 (anticipation kept). The
    elbows bend 0.6 x the out angle.
  - Head **-15**; Spine **-4**; Chest -3 local, which is **-7 in world** (chest vs spine **3 deg**). Head up in world =
    4 + 3 + 15 = **22 deg** (limit 30).
  - The largest step is the arms from -2 (f10) to 22 (f22): 2 deg per frame.
  - `renders/_beats2x_roar.png`: f0 vs f22 / f34 / f50 shows the arms clearly out, the forward push and the open mouth.
- **MUST 5 (idle):**
  - Chest breath **2 deg**; the body sinks **0.015** at the breath peak; hip yaw **+/-4 deg**.
  - The Head counter-pitches the breath (+2) and counter-yaws, so it stays level.
  - New: a slow **+/-8 deg fist flex** on `Hand_L` / `Hand_R`, 60-frame period, the left fist a quarter cycle ahead.
  - The feet stay planted. `renders/_beats2x_idle.png` (f0 / f30 / f60 / f90 at 2x) shows the fists and the torso change.
- **MUST 6 (kneel):**
  - `Foot_R` turns **10 deg outward** (yaw) from f18 to f50, eases back by f72, and is applied after the leg IK, so the
    knee stays on the snow (ground -0.009 at f20, unchanged).
  - The elbow bend in the hold is **30** (was 26), so the fists sit on the thighs.
  - **Disclosure on the 3/4 test:** the kit's tq camera sits on the pet's front-left, so the kneeling (right) leg is on
    the far side. At f40 the right knee cap shows on the snow behind the standing shin (`_scratch/knee40.png`, a posed
    close-up aimed at `Knee_R`), but the right sole faces back and stays hidden from the front 3/4.
  - The sole and the flat shin read clearly from the back and the game camera (`renders/_kneel_views.png` back / game
    f40). A clearer 3/4 read would mean mirroring the act (kneel on the left knee, on the camera side) and moving the
    `Knee_R` anchor; I did not do that without a ruling.
  - Fixed-camera act renders re-made: `renders/_cv_kneel_side.png`, `_cv_kneel_front.png`, `_cv_kneel_tq.png`
    (`cv_tq_act_kneelrise_40.png`), `kv_*_act_kneelrise_18/40/58.png`.
- **Step 1** (`_scratch/clipgate_f85.txt`, and the export run `_scratch/export_f85.txt`):
  - collision_free **true**. ground_min_z 0.000 for idle / walk / roar; **-0.009** for the act at f20.
  - Linear 0. Idle and walk loops 0 / 0. Walk slide 0.0, foot_z_var 0.0. Stride 0.645.
- **Clips and events are unchanged:**

  | clip | frames | loop |
  |---|---|---|
  | idle | 120 | yes |
  | walk | 48 | yes |
  | roar | 66 | no |
  | act_kneelrise | 100 | no |

  Events are as in the table below.
- **Renders re-made:** `_pose_tq_sheet.png` (24 beats), `_beats2x_idle/roar/kneel.png`, `_kneel_views.png`, the `_cv_kneel_*`
  sheets and `_roar_jaw_close.png`.
- **Export:** `C:\cdimp\PermafrostTitan.fbx` (2026-10-28 01:03, 1,067,868 B). The portrait raw is re-made.

## ROUND 5 (2026-10-27, after `_review/PermafrostTitan_review4.md`, APPROVED 8/10): NICE pass, then EXPORT
- Back echo ring outer diameter **0.28 BU** (BR_OUT 0.135 -> 0.140, inner 0.088 kept). Game-camera gold at 64 px **24**
  (was 22; gate 20). Portrait 37. Pale on flat_game stays **13.5 %** (all figure pixels; strict 13.3).
- The kneel-settle line is no longer labelled "MUST 2".
- ANIM_REFS section C now says it was added after the keys were set.
- **Reference contact sheets in `renders/refs/`: skipped.** Saving the K8 frames would mean writing Sakugabooru video
  frames to disk (a download of third-party media). I studied them in the browser only; the frame numbers in ANIM_REFS C
  let anyone re-check them on posts #257646 / #254909.
- Step 1 (`_scratch/clipgate_r5.txt`): collision_free **true**, ground_min_z 0.000 (idle / walk / roar) and -0.009 (act f20),
  linear 0, loops 0 / 0, walk slide 0.0. Model sheet `renders/_model_sheet.png` checked.

## ROUND 4 (2026-10-27, after `_review/PermafrostTitan_review3.md`, APPROVED WITH FIXES 7/10)
- **MUST 1, the kneel reads from the front, the 3/4 and behind:**
  - The Spine rolls **-7 deg** toward the kneeling (right) side, f8-18 in, held to f50, out by f76.
  - The Chest counter-rolls +3.5 and the Head +3.5. Chest vs spine stays at **4.0 deg** in the hold and 4.7 at the
    f58 lean (<= 5); the head stays level.
  - The left foot steps **0.30 forward and 0.04 out** (was 0.22 forward), so the standing leg separates from the
    kneeling one in the front view.
  - The roll lowers the right hip, so the pelvis drop went from 0.30 to **0.272** to keep the knee ON the snow.
  - Knee heights at f30 (`Leg_*` tails = the knees): left **0.498**, right **0.196**. The right knee is 0.30 BU lower
    (target >= 0.10).
  - Renders at f18 / f40 / f58 from the front, tq, back and game camera: `renders/_kneel_views.png`.
- **Kneel settle (lead ruling, ref K8a):** after the knee lands at f18 the body dips 0.008 more at f20 and is back by
  f23. The roar keeps its slower lift.
- **MUST 3, the back pale:** see `MODEL_NOTES.md` ROUND 4. ICE_W on `flat_game.png` = **13.5 %** (all figure pixels).
- **NICE:**
  - (1) ANIM_REFS now says spine 10 deg + chest 4 deg for the lean.
  - (2) The rig has **no Neck bone**: the head pivots at the throat, so the head + neck limits (up <= 30, down <= 20)
    apply to the Head bone and the neck <= 8 rule does not apply.
  - (3) The roar arms peak at **9 deg** at f34 (8 at f22 / f50); the text is corrected.
  - (5) The kneel and roar beats are rendered at 2x: `renders/_beats2x_kneel.png`, `_beats2x_roar.png`.
  - (7) The elbows bend 4 deg more in the hold (f30-50), so the fists read as resting over the thighs.
- **Gate (step 1, `_scratch/clipgate_r4.txt`):** collision_free **true**. ground_min_z 0.000 for idle / walk / roar and
  **-0.009** for the act at f20 (the settle; the right knee cap on the snow). Linear 0, loops 0 / 0, walk slide 0.0.

## Numbers (step 1)
- **collision_free: true.** ground_min_z: idle / walk / roar 0.000; act_kneelrise **-0.005 at f18** = the right knee cap
  and the tucked toes resting ON the snow during the kneel (`_scratch/ground_probe.py`: knee -0.003, toes -0.005).
- Audit: linear 0; idle loop 0 / 0, idle_foot_drift 0; walk loop 0 / 0, **slide 0.0, foot_z_var 0.0**. Stride 0.645 BU.
  Tris 7,552. Lua 31 KB.
- Pose limits (from the key tables): chest vs spine <= 4.7 deg (the f58 lean = the Spine 10 deg + the Chest 4 deg; roar 3.5); spine + chest + head pitch-up
  max 15 deg (roar); no head shake; the fastest limb move is the right thigh into the kneel over 12 frames (f6-18).

## Clips
| clip | frames | loop | events (frame) | what it does |
|---|---|---|---|---|
| idle | 120 | yes | `frost1` 30, `core1` 40, `frost2` 70, `core2` 100 | WEIGHT SHIFT: hip yaw +/-3 deg (one cycle), two slow breaths (chest 1 deg, the body sinks 0.005), the shoulders (pauldrons ride the Arm bones) settle out 2 deg at f30 and f70; the head stays level and forward (counter-yaw). Feet planted. |
| walk | 48 | yes | - | HEAVY LOAD WALK (Plate 27): flat-foot contacts (toe peel max 10 deg), duty 0.62, the body sinks 0.035 five frames after each contact and rises at passing, low swing (lift 0.07), the pelvis rolls 0.022 over the stance foot, chest counter-yaw 2 deg, arms swing 4 deg. |
| roar | 66 | no | `core1` 22, `glint` 22, `icedust` 24, `core2` 34 | CORE BELLOW: f0-10 lean in + head tuck 4 deg (anticipation); f10-22 the head lifts 10 deg, the arms go out 8 deg (9 at f34), the core pulses; the jaw opens late (peak f27, ref #3); hold to f50; a slower settle to f66 (ref #9). |
| act_kneelrise | 100 | no | `icecrack` 18, `core1` 30, `core2` 44 | KNEEL AND RISE (Plate 356): f0-9 the left foot steps forward 0.30 and 0.04 out (round 4); f6-18 the body drops 0.272 and rolls 7 deg toward the kneeling side, the right knee lands on the snow (ice crack) and settles 0.008 (f20-23), the right toes tuck under, the head bows 12 deg, the arms come forward with the fists over the thighs (never on the ground); hold to f50 with two core pulses; f50-58 the forward lean (K3: the Spine carries 10 deg, the Chest 4); f58-76 the front leg drives up and the right foot comes through; f70-79 the left foot steps back; exact rest from f84. |

## VFX anchor bones (plan section 8)
`Core` (FX_CorePulse on `core1/2`), `Pauldron_L` / `Pauldron_R` (FX_FrostDrift on `frost1/2`), `Fist_L` / `Fist_R`
(FX_IceDust on `icedust`), `Knee_L` (FX_IceCrack on `icecrack`; was `Knee_R` before final 8.5 round 2), `Hero` (FX_HeroGlint on `glint`). The back echo ring
centre is reported by model() as `BACK` (0, 0.368, 1.691) on Chest if the lead wants a second glint anchor (no bone
added, to keep the rig as reviewed).

## Signature act in one line
The giant drops to its left knee on the snow, bows with its ice core pulsing, then leans forward and rises.

## Round-3 model fixes (review 2) shipped with these clips
- **M1** back echo ring 0.27 BU outer diameter (band 0.047), same construction, no settings / spikes: **game-camera
  gold 24 px** at 64 (kit counter; brief counter 27; review asked >= 20 by its count, which read 14 when mine read 16,
  so I kept a margin).
- **M2** upper shoulder caps 0.130 x 0.150 x 0.033 (rnd 0.30, three chunks kept) + the lower caps 0.076 x 0.145 x
  0.034: **back (game) pale ICE_W 11.5 %** (target >= 11).
- NICE: shin guard depth 0.028, chest bottom taper 0.66, brows 30 deg.
- Shares (strict) side / tq / game: MAUVE 64.4 / 63.0 / 58.9, PLUM 12.1 / 14.3 / 18.0, ICE_W 11.7 / 9.2 / 11.5,
  GOLD+GOLD_D 1.9 / 4.3 / 2.2. Portrait gold 37 px.

## References added after the clip gate
- Kaiju No. 8 cuts (Sakugabooru #257646, #254909) are in `ANIM_REFS.md` section C (K8a-c). They fit the roar hold and the kneel
  hold; the rise itself stays on Plate 356 K3. Two optional polishes (a quicker roar lift, a 3-frame kneel settle) are listed there,
  not applied: the clips under review are unchanged.
