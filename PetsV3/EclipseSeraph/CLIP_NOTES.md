# Eclipse Seraph - clip notes (clip round 8 after review 10, builder D, 2026-10-28; PASSED review 11)

Code: `pets/EclipseSeraph.py` (from "animation (clip round 1)" down). References: `EclipseSeraph/ANIM_REFS.md` (The Boy
and the Heron #260711 / #260630, The Cat Returns #256671, banshee #8, Sea Beasts #3, Wolf's Rain W0, Bird Flight #5).
Rest pose on the ground = `DISPLAY_POSE` (the model-gate six-wing fan). Every act and land ends exactly in it.

## Review 10 fixes (clip round 8) - far upper wing height
- **(a) Roar:** `ROAR_W["A_L"]` up 30 -> **36** (twist 26, sweep -8 kept). No collision at 36. At 40 Wing_A_L cuts
  the Mane (6 hits, roar f13), so 40 is not an option.
- **(b) Takeoff:** `TOP["A_L"]` up 34 -> **31** and the f6 gather A_L up 34 -> **31**. TOP keeps twist 34; the gather
  key keeps its mixed twist 29.2.
- **Measured, the game camera** (`_scratch/rod_metric.py`; mane = share of camera-facing Mane verts that are
  visible, rest pose 0.67):

  | roar f30, far wing | blade width | mane visible | collisions |
  |---|---|---|---|
  | up 24, twist 30 | 6.4 | **0.83** | none |
  | up 30 (round 7) | 7.0 | 0.73 | none |
  | **up 36 (review 10, in file)** | **8.9** | **0.60** | none |
  | up 40 | 10.1 | 0.50 | Wing_A_L / Mane |

  - Raising the wing gives a wider fan, and its tips now sit above the head line. But it does NOT clear the mane:
    the wing root sits on the shoulders behind the mane, and from this high-behind camera the inner wing always lies
    over the mane's left half. The higher the wing, the more mane it hides.
  - The way to show more mane is to go lower: up 24 / twist 30 shows 0.83 (round 9 had 0.83, with the rod). That
    swap is one line (L433).
  - Side by side: `renders/_roar_far_wing_height_cmp.png`.
- **Takeoff halo**, hidden by area: f0-10 = 10 / 9 / 6 / 3 / 1 / 0 / 0 / 0 / 0 / 0 / 0 %, f11-12 0 %. The far wing
  passes below-left of the rim at f4-10 (`_rod_check_takeoff_3x.png`, f4 / 6 / 8 / 10).
  - Far blade width at takeoff f4-10 is 5.7-7.5 (it was 6.4-8.3 at up 34).
- **Far-wing blade width per frame** (reviewed file `_scratch/EclipseSeraph_r11final.py.txt`; raw output
  `_scratch/r10/rod_r11f.txt`):
  - What it measures: the ray-tested, camera-facing verts of Wing_A + WingTip_A on each side, projected to the game
    image. Width = the PCA minor std x1000 (the blade's visible width).
  - A rod measures 3-4. Round 9's far wing was 3.5 at takeoff f10 and 3.7 in the roar.

  | frame | far wing (A_L) | near wing (A_R) | mane visible |
  |---|---|---|---|
  | takeoff f4 | **5.7** | 11.0 | 0.77 |
  | takeoff f6 | **5.7** | 12.5 | 0.71 |
  | takeoff f8 | **5.8** | 14.0 | 0.68 |
  | takeoff f10 | **7.5** | 14.9 | 0.77 |
  | takeoff f13 | 12.6 | 7.6 | 0.77 |
  | roar f14 | **8.9** | 16.8 | 0.57 |
  | roar f30 | **8.9** | 16.8 | 0.60 |
  | roar f50 | **8.9** | 16.8 | 0.60 |
  | land f8 / f10 / f12 / f16 | 6.6 / 8.0 / 9.7 / 9.4 | 12.9 / 12.7 / 11.7 / 12.9 | 0.74 / 0.74 / 0.81 / 0.77 |
- **Pass checks (final file):**
  - roar f30 halo clearance: Mane 0.055 (the far wing 0.134);
  - step 1: collision_free true on all seven clips; linear 0; loops closed; walk slide 0.0004;
  - ground -0.003 / -0.004 / takeoff -0.013 / fly +0.160; tris 11,336;
  - largest step: takeoff 21.6, land 19.8, roar 9.0. Neck max 6.0, chest vs spine 2.5;
  - rest delta (vs own f0): roar / cascade / idle 0.00.
- **Evidence** (rendered 2026-10-28 09:53-09:54 from the final file):
  - **all 21 sheets:** `renders/_pose_<game|tq|front>_<idle|walk|fly|takeoff|land|roar|act_wingcascade>_sheet.png`,
    labelled with frame and time:
    - idle f0-120 every 20;
    - walk f0 / 7 / 13 / 20 / 27 / 33 / 40;
    - fly f0 / 4 / 7 / 10 / 14 / 18 / 24;
    - cascade f0 / 14 / 30 / 58 / 70 / 90 / 110;
    - roar, takeoff and land as in round 7;
  - `_rod_check_roar_3x.png` (f14 / 30 / 50), `_rod_check_takeoff_3x.png` (f4 / 6 / 8 / 10),
    `_rod_check_land_3x.png` (f7 / 8 / 10 / 12) and `_tiers_check_front_roar_3x.png`;
  - `_roar_far_wing_height_cmp.png`.
- Backups: `_scratch/EclipseSeraph_r11start.py.txt` (round 7) and `_scratch/EclipseSeraph_r11final.py.txt` (this).

## Review 9 fixes (clip round 7) - the viewer's-left upper wing (Wing_A_L) was still a rod
- **Why it stayed:** `key()` mirrors one twist onto both sides, and the game camera is off-axis (behind-right, high),
  so one twist value can't turn both upper wings face-on. Round 6's -18 fanned `Wing_A_R` (viewer's right) only.
  - Side check (`_scratch/side_check.py`): `Wing_A_L` is the viewer's LEFT wing in the game view. By distance it is
    slightly the nearer one (9.86 vs 10.22 BU), but it is the wing the review called "far". The labels use the
    review's word.
- **MUST 1, per-side keys:** a pose dict may now carry a side key, `"A_L"`. `wset()` keys the pair first, then the side
  key overrides that side only. `mix()` falls back to the pair key when one dict has no side key. `A_R` keeps the
  round-6 values (-18 twist, sweep back 8).

  | far-side twist (over the round-8 value), sweep as A_R | result |
  |---|---|
  | -30 (TOP -6 / ROAR_W -10) | Wing_A_L cut Wing_B_L and the Chest (takeoff, land, roar) |
  | **+6 (TOP 30 / ROAR_W 26)** | **first to fan**, collision-free |
  | +12 (my extra step) / +18 | Wing_A_L cut the Neck (roar, land; +18 also takeoff) |
  | +6 with sweep +8 forward / -8 back | forward cut the Neck; back hid more of the mane and the halo rim |

  - **Roar:** `ROAR_W["A_L"] = (30, -8, 26, 0)`, which is +6 as tested.
  - **Takeoff gather:** at up 40, +6 hid 11-14 % of the halo over takeoff f1-10 (over the 10 % bar). So the far gather
    is lower: `TOP["A_L"] = (34, -4, 34, -10)`. The lower wing leaves room for twist 34 (+10) without a neck cut, and
    the blade is wider than at 30 (6.4 -> 7.1 at f6, 7.1 -> 8.3 at f10).
  - The f6 key drops the far wing to that height early (`gather`: A_L (34, -0.8, 29.2, -9.2)), so f1 stays at 10 %.
- **Land f8 (and takeoff f11-14):** these frames sit between BRAKE (land f7) and LOW (land f12 / takeoff f13), not
  TOP, so they got their own far-side twist: `BRAKE["A_L"]` 26 -> **34**, `LOW["A_L"]` 24 -> **48**. With 36 / 54 the
  wing cut the Neck at land f8.
- **Rod metric** (`_scratch/rod_metric.py`, real clip frames, game camera): the visible, ray-tested verts of
  Wing_A + WingTip_A per side are projected to the image. "Minor" = the blade's visible width (PCA std, x1000). A rod
  measures about 3-4; the fanned A_R measures 12-17.

  | frame | r9 A_L | **r10 A_L** | A_R |
  |---|---|---|---|
  | roar f14 / 30 / 50 | 3.7 | **7.0** | 17.0 |
  | takeoff f6 | 4.1 | **6.4** | 12.5 |
  | takeoff f10 | 3.5 | **8.3** | 14.9 |
  | takeoff f13 | 4.3 | **12.6** | 7.6 |
  | land f6 / 8 / 10 / 12 | 4.7 / 3.4 / 3.2 / 3.3 | **6.3 / 6.6 / 8.0 / 9.7** | 12-13 |

  - Mane visible from the game camera (share of camera-facing Mane verts): roar f30 **0.73** (rest 0.67, r9 0.83),
    takeoff f10 0.74.
  - A lower roar far wing (up 24, twist 30) shows more mane (0.80) but a narrower blade (6.4). It is a one-line swap
    if you prefer it.
- **Front roar, three tiers:** in round 6 the middle pair (B 8) and the lower pair (C 14) merged into one band in the
  front view. `ROAR_W` B -> **(20, -6, 20, -10)** and C -> **(-4, 10, 2, -20)**: the middle pair rises and the lower
  pair drops below level, swept forward. The upper V is unchanged.
  - Evidence: `renders/_tiers_check_front_roar_3x.png` (f0 rest vs f30) and `_pose_front_roar_sheet.png`.
- **Untouched:** the fly stroke (fly f7 is unchanged, TO 9+ 3), DISPLAY_POSE, colours (on hold), and the model.
- **Pass checks (final file):**
  - **halo hidden** on the game camera, by area: takeoff f0-10 = 10 / 10 / 8 / 6 / 4 / 3 / 2 / 1 / 1 / 1 / **2 %**,
    f11-12 2 / 1 %;
  - **roar f30 halo clearance:** Mane **0.055** (>= 0.050);
  - **step 1:** collision_free true and 0 collisions on all seven clips; linear 0; loops closed; walk slide 0.0004;
    ground -0.003 / -0.004 / takeoff -0.013 (>= -0.015) / fly +0.160; tris 11,336;
  - **poses:** largest step: takeoff 21.6, land 19.8, roar 9.0 (was 12.3). Neck max 6.0 (roar), chest vs spine 2.5;
  - **rest delta** (end vs own f0): roar / cascade / idle 0.00.
- **Evidence** (all rendered 2026-10-28 09:38, the final file):
  - `renders/_rod_check_roar_3x.png` (game f14 / 30 / 50), `_rod_check_takeoff_3x.png` (f6 / 10) and
    `_rod_check_land_3x.png` (f7 / 8 / 10 / 12). Each is a 3x crop of the 300 px game render, (20,10,260,250) so the
    whole far wing is in frame, labelled "FAR upper wing (Wing_A_L, viewer's left)".
  - `renders/_pose_<game|tq|front>_<roar|takeoff|land>_sheet.png`, labelled with frame + time:
    - roar f0 / 8 / 14 / 22 / 26 / 30 / 40 / 50 / 58 / 64 / 66;
    - takeoff f0-14 (f0-10 every 2, then f10-14 every frame) and f16 / 20 / 24 / 28;
    - land f0 / 4 / 6 / 7 / 8 / 10 / 12 / 14 / 16 / 21 / 24 / 28.
- Backups: `_scratch/EclipseSeraph_r10start.py.txt` (round 9) and `_scratch/EclipseSeraph_r10final.py.txt` (this).

## Review 8 fixes (clip round 6) - roar + takeoff: the near upper wing read as a rod in the game view
- **MUST 1:** the upper pair (A) in the takeoff gather (TOP) and the roar hold (ROAR_W) now turn the feather plane
  18 deg and sweep 8 back:
  - TOP A (40, +4, 24, -10) -> **(40, -4, 6, -10)**;
  - ROAR_W A (30, 0, 20, 0) -> **(30, -8, 2, 0)**.

  | variant tried | result |
  |---|---|
  | +12 twist | Wing_A cut the Neck (takeoff, land, roar) |
  | -24 twist | Wing_A cut Wing_B (45-54 hits) |
  | -12 twist alone | still a rod at takeoff f10 |
  | -18 twist + 8 back (chosen) | the near upper wing shows a fan of separate feathers |

  - 3x game-camera crops: `renders/_rod_check_roar_3x.png` (roar f14 / 30 / 50) and `_rod_check_takeoff_3x.png`
    (takeoff f6 / 10).
  - The fly stroke (f24-28) and DISPLAY_POSE are untouched. TOP also feeds the land's first flare key, which is fine.
- **Pass checks:**
  - halo hidden on the game camera, by area: takeoff f0-10 = 10 / 10 / 9 / 8 / 6 / 5 / 4 / 4 / 4 / 3 / **2 %**
    (<= 10 %), f11-12 0 %;
  - front roar f14-50 shows the three tiers (`renders/_pose_front_roar_sheet.png`);
  - roar f30 halo-to-mane clearance **0.055** (>= 0.050);
  - all clips collision-free; ground -0.003 / -0.004 / takeoff -0.013 (>= -0.015) / fly +0.160;
  - linear 0, walk slide 0.0004, largest step 21.6, Neck 6.0, chest vs spine 2.5;
  - rest delta roar / land / cascade 0.00.
- All 21 sheets re-rendered with labels (`renders/_pose_<tq|game|front>_<clip>_sheet.png`).

## Review 7 (clip round 5): cheap 9+ items
- **Front fly:** the lower pair's stroke is 24 / -14 (was 22 / -6), a 38 deg beat; the front fly sheet shows it.
- **Halo at takeoff f10:** the gather top for the upper pair is now A (40, +4, 24, -10), was 44 / 4 / 24 / -12.
  Halo hidden on the game camera, by area: f0-10 7-10 % (was 10-18 %), f12-20 0 %.
- **Lion read:** see MODEL_NOTES round 8 (longer cheek ruff).
- **Step 1:** collision-free, linear 0, loops closed, walk slide 0.0004. Ground -0.003 / -0.004 / -0.013 / fly
  +0.160. Largest step 21.6 (takeoff Foot_FL). Neck 6.0, chest vs spine 2.5. Rest delta roar / land / cascade 0.00.
- All 21 sheets were re-rendered from the round-8 file with labels: `renders/_pose_<tq|game|front>_<clip>_sheet.png`.

## Review 6 (clip round 4): evidence re-rendered from the round-7 file
- All 21 clip sheets were re-rendered from the current file, with frame + time labels and a render-time footer:
  `renders/_pose_<tq|game|front>_<idle|walk|fly|takeoff|land|roar|act_wingcascade>_sheet.png`. Script:
  `BlizzardRoc/_scratch/clip_sheet.py`.
- New rest pose: lower pair C (-12, +70, 0, -45). Step 1 is collision-free on every clip. Ground -0.003 / -0.004 /
  -0.013 (takeoff) / fly +0.160. Linear 0. Walk slide 0.0004.
- Largest step: 21.6 deg (takeoff f15, Foot_FL); land 19.8 (WingTip_C, the wing folding back). Neck 6.0, chest vs
  spine 2.5.
- Rest delta: roar, land and cascade 0.00. Takeoff f28 = fly f0.
- Halo hidden on the game camera, by area (unchanged): f0-10 10-18 %, f12-20 0-6 %, f22 21 %; f24-28 are the fly's
  own stroke top (lead ruling).
- Roar sheets: the halo tilt 18 shows at f30 / f50.

## Review 5 fixes (clip round 3)
- **MUST 3, halo clear at the launch.** I measured how much of the halo is hidden, by area, on the game camera:
  `_scratch/halo_px.py` renders the gold of the full pose and of the halo alone, and `_scratch/halo_count.py` takes
  the ratio. The per-vertex ray test overstated it.

  | takeoff frame | 0 | 4 | 8 | 10 | 12-18 | 20 | 22 | 24 | 26 | 28 = fly f0 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | round 5 | 30 % | 31 % | 30 % | 30 % | 0 % (f12, f14); f16 34 % | 43 % | 42 % | 34 % | - | - |
  | **round 6** | **10 %** | 13 % | 17 % | 18 % | **0 %** | 6 % | 21 % | 36 % | 39 % | 42 % |

  - The upper pair sat behind the halo on the game camera, both at rest and at the stroke top. Changes:
    - rest A is now 40 / fwd +4 / tip -8;
    - the gather top A is 44 / +4 / -12 (TOP);
    - the second high beat (f17 TOP) is gone. After the launch downstroke, f16-28 run the flight cycle's upstroke at
      the FLY tempo and end exactly on fly f0 (same handoff as the Frostcrown and the Roc; no pop into the fly loop).
  - What is left at f22-28 is the fly clip's own stroke top (42 % at fly f0; review 5 accepted the fly). Clearing it
    needs a forward-swept stroke top. That cuts the mane at 14 hits (tested), so I left the approved fly stroke alone.
  - `renders/_pose_game_takeoff_sheet.png` = f10 / f13 / f17 / f24.
- **TO 9+ front cascade:** FAN C 20 -> **4, swept forward 14** (B 28 -> 30), so the lower pair is its own level tier
  in the hold. It LIFTS to 14 at f52 and settles level by f58, so the ripple still reads.
  `renders/_pose_front_act_wingcascade_sheet.png` (f52 / 58 / 64 / 70) shows three tiers per side.
- **TO 9+ front fly:** the lower pair's stroke is 22 / -6 (was 20 / 4), a 28 deg beat that reads from the front
  (`renders/_pose_front_fly_sheet.png`, f6 / 13 / 20).
- **TO 9+ roar tilt:** the halo tilt peak is 17 -> **18 deg**. At 20 the halo-to-mane gap fell to 0.039; at 18 it is
  0.055 (f30), over the 0.050 line.
- **New rest pose:** all clips start and end in the new `DISPLAY_POSE`.

## Review 4 fixes (the one bounded six-wing round) - SIX WINGS KEPT (no four-wing fallback)
- **Middle-pair root moved** back 0.10 onto the spine base (and up 0.04, out 0.02). Wing_B now rides the Spine, like
  the lower pair.
  - Static cut-through check (`_scratch/var6.py`, `pose_cands.py`): B rises **34 deg clean** (was 10). C rises 20
    clean with B at rest. The full fan A 54 / B 28 / C 20 is clean.
  - The fallback test (B >= 20 clean) passes.
- **Fly, no lock-step:** three strokes. Upper 46 -> 18; middle 28 -> 2, 4 f behind; lower 20 -> 4, 4 f behind the
  middle (8 f behind the upper). Tops at f0 / f4 / f8, bottoms at f13 / f17 / f21. All 28 frames are clean
  (`_scratch/path6.py`, then step 1).
- **Cascade, three tiers:** upper to 54 (f14-28), middle to **28** (f30-44, the arm now rises, not just the hand),
  lower to **20** (f44-58), each hand first. Hold f58-64.
- **Idle:** the wings breathe as a chain: upper, then middle +4 f, then lower +8 f.
- **Visible tiers** (please count on the sheets): game view, cascade f58 / f62 / f70 and fly f04 / f07 / f10 show
  three wing shapes per side (upper V, middle out, lower at the flank). In the front view the lower pair shows beside
  the flank at the cascade hold and the fly downstroke (f58-62, fly f07-f14).
- **NICE 1:** the launch LOW key sweeps the upper pair 2 deg less far forward (fwd -6; -8 cut the chest).
- **NICE 2:** land f4 has an in-between on the front legs (land max step 17.2, was 17.8 as a snap).
- **NICE 3:** the halo tilts 17 at the roar peak (head clearance stays 0.055 at rest; Halo vs Head / Neck / Mane is
  clean in every roar frame).
- **Rest frames:** roar f66, cascade f110 and land f28 are 0.00 deg from the ground rest pose (`rest_delta.py`).
  Takeoff ends in the flight cycle.

## Step 1 (`_tools/headless_full.py -- EclipseSeraph - 1` and `_tools/headless_clips.py`, every frame; round 3)
- collision_free **true** (six wings against each other, the body, the legs, the mane, the cheek ruff and the halo).
  Audit linear 0 on every clip. Loops are closed (idle / walk / fly: loop_pos 0, loop_rot 0). Walk slide 0.0004,
  foot_z_var 0.0026, idle_foot_drift 0.0, stride 0.484. Tris 11,336.
- ground_min_z: idle -0.003, walk -0.004, takeoff -0.013, land -0.003, roar -0.003, act_wingcascade -0.003,
  fly +0.160.
- Largest per-frame bone step (`BlizzardRoc/_scratch/step_check.py`): 21.6 deg (takeoff f15, Foot_FL, the leg tuck).
  Wings max 6.8 (cascade, Wing_C). Neck max 6.0 (roar). Chest vs Spine max 2.5. Head + neck pitch-up max 15.
- Rest delta (`FrostcrownDragon/_scratch/rest_delta.py`, last frame vs the ground rest pose): roar 0.00, cascade
  0.00, land 0.00. Takeoff f28 = fly f0 by construction (phase 1.0, same keys).

## Clips (30 fps)
| clip | frames | loop | events | what it does |
|---|---|---|---|---|
| idle | 120 | yes | `corona` f80 | HALO DRIFT: slow breath. The halo rolls +-5. The upper pair lifts 4 (f10-35) and settles. The middle and lower pairs follow 4 f behind, in phase. Quick head turns to +-8 yaw with long holds. Corona pulse at f80 (VFX). |
| walk | 40 | yes | - | Lateral-sequence lion walk (stride half 0.15, lift 0.08). Level back and head. The display fan is held (the upper pair 4 lower, with a 2 deg bob). The halo trails the head by 3 f. Tail sway. |
| fly | 28 | yes | - | THREE strokes in a chain: upper 46 -> 18, middle 28 -> 2 (4 f behind), lower 20 -> 4 (8 f behind). Body pitch 4 with a +-0.04 rise, head level, halo trailing the bob, tail streaming. Front paws tucked, hind legs trailing. |
| takeoff | 28 | no | `launch` f11 | Crouch (-0.07) while the six wings rise to the stroke top. LAUNCH on the first downstroke plus the hind-leg push. The tail lifts (+8) so the brush clears the floor in the crouch. The legs tuck; f16-28 run the flight upstroke at the fly tempo and end exactly on fly f0 (no second high beat). |
| land | 28 | no | `touch` f16 | Flare (the chest lifts, the upper pair brakes forward and opens), legs reach. TOUCH f16, absorb (-0.05), the wings settle into the display fan. |
| roar | 66 | no | `roar` f24 | HALO LIFT: the wings open to half first (f0-14, R2). The halo lifts 0.20 on its bone and tilts forward 16 (18 at the peak). The head rises 15 (Neck -6 / Head -9). The jaw opens and lags (f14-26). The mane's top arc flares 6. Hold with a jaw rumble (f26-50). Settle by f64. |
| act_wingcascade | 110 | no | `ripple1` f22, `ripple2` f40, `ripple3` f54 | SIGNATURE, SIX-WING CASCADE (in place). Crown bow (head down 6, halo sinks 0.02). Then each pair does a tip-to-root ripple (hand first, arm 6 f later): upper f14-28 (to 54), middle f30-44 (to 30, sweeping back as it rises), lower f44-58 (lifts to 14, settles LEVEL at 4, swept forward 14). All six hold the three-tier fan f58-64 (hands up: A tip -24, B tip -30, C tip -26). Reverse ripple f64-94 (lower pair first). Exact rest pose from f100. |

## Tested wing ranges (round 1, BEFORE the review-4 root move; kept for the record)
- A (upper): up <= 54 at fwd -4 (higher, or swept forward: the hand meets the halo / mane). Down >= ~18 at twist 24
  (lower: the root rows press into the shoulders).
- B (middle): up <= 10 (higher: the arm root cuts the chest top). Sweeping back to fwd -28 is clean, forward is not.
- C (lower): fwd >= -4 on the ground (further back: the root rows meet the swinging thigh). Twist >= 0.
- B and C move IN PHASE (C = B + 6). If C rises more than 15 above B, or B / C get different twist or tip dynamics,
  C's hand cuts B's arm. That is why the middle and lower pairs share one echo stroke, and why the cascade fan mostly
  comes from the hands (tip) rather than the arms.

## Decisions / deviations
- Plan: "the halo lifts 0.10H (0.22 BU) and tilts forward 25". I used 0.20 and 15 (17 at the peak since review 4). I kept it a step smaller because
  of the 0.054 head clearance (the rim already faces forward-up at 40), and did not test 25. The lift reads clearly
  in `_pose_front_roar_sheet.png`.
- Roar: the wings open to half BEFORE the head lift (the plan has them open at f30-50). With the head up 15 and the
  upper pair still raised to 44, the mane top cut the wing roots. Opening first is also R2's order (spread, then
  call).
- Cascade: "each feather row lags 2 frames" is done with the two wing bones per pair (hand first, arm 6 f later).
  There are no per-row bones. The fan is limited by the B arm range (above), so the hands carry it (tip -24 / -36).
- Model changes made for the clips are noted in `MODEL_NOTES.md` round 4 (the outer mane ring's low and side tufts
  are weighted to Neck, and DISPLAY_POSE C fwd is -4).

## Renders
`renders/_pose_tq_<clip>_sheet.png`, `_pose_game_<clip>_sheet.png`, `_pose_front_<clip>_sheet.png` for all seven
clips (frames labelled).
