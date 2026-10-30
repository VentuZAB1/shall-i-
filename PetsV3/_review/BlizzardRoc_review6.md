# Blizzard Roc - model + clip gate review 6 (2026-10-28, fresh reviewer) - MODEL 8.5 PASS / CLIPS 8.6 FIX (documentation only)

**Model: 8.5/10 - PASS. Clips: 8.6/10 - FIX.**

- Model 8.5 is the floor, not a margin. The round-6 model change (outer tail fan) is verified. Nothing blocks it.
- Clips FIX is for one documentation MUST (MUST 1: `ANIM_REFS.md` and a code comment still describe the round-1 clips). The motion itself scores 8.6. Once MUST 1 is in, the clips pass on these same renders. No new renders are needed.

---------------------------------------------------------------------------------------------------------------------
## What I looked at

**Read (text):** `GLACIER_REVIEWER_BRIEF.md`, `BlizzardRoc_review5.md`, `BlizzardRoc_plan.md`, `BlizzardRoc/MODEL_NOTES.md`, `BlizzardRoc/CLIP_NOTES.md`, `BlizzardRoc/ANIM_REFS.md` (dated 00:50), `pets/BlizzardRoc.py` (takeoff L736-770, walk L593-632, tail L357-372, eye L155-167, idle L566-590, land L773-807, references L458-462). I diffed the code against the round-6 start snapshot (`_scratch/BlizzardRoc_r6start.py.txt`). The step-1 outputs (`_scratch/full_step1.txt`, `seam.txt`, `steps.txt`, `rest_delta.txt`) are dated 04:21, after the last code edit (`pets/BlizzardRoc.py` 04:21:10). The renders are dated 04:22-04:23, so the evidence is current.

**Images (newest set):**
- `_pose_tq_takeoff_sheet.png`, `_pose_front_takeoff_sheet.png`, `_pose_game_takeoff_sheet.png`: tiles are f10, 13, 15, 17, 19 (row 1) and f21, 23, 25, 28, 30 (row 2), matched by pixel comparison. The sheets carry no visible frame labels, although CLIP_NOTES says "frames labelled" (see N1).
- Individual frames `pose_{front,tq,game}_takeoff_{19,21,23,25,28,30}.png` and `pose_{front,tq,game}_fly_00.png`.
- `_pose_game_walk_sheet.png` and `pose_game_walk_00.png` (tail).
- `_model_sheet.png`, `model_game.png`, `model_front.png`, `model_tq.png`, `model_side.png`, `model_back.png`.
- `_icons_strip_64.png`, `_icons_strip_128.png`, `_icons2_strip_128.png`.
- Close-ups I made from these renders: model_game tail (4x), model_front head (6x), walk tail (4x), front f17/19/21 (2x), game f15/21 (2x), an f19-f28 strip.

**Checks run:**
- Decoded PNGs and compared takeoff f30 against fly f0 for all three cameras.
- Evaluated `wing3.stroke` for the takeoff-to-fly window (f21-f36).

**Not opened:** `_close_sheet.png` and `_eye_sheet.png`. They are dated 27 Oct, before the round-6 eye change, so there is no fresh head close-up. I did not open animationreference.org or check md5s (the reviewer does not open sites).

---------------------------------------------------------------------------------------------------------------------
## 1. Round-5 items

| # | item | result | evidence |
|---|---|---|---|
| MUST 1 | takeoff seam | **PASS** | Code `takeoff()` L760-763 runs f25-30 at `ph = 1 + (f-30)/30`. `pose_tq_takeoff_30.png`, `pose_front_takeoff_30.png` and `pose_game_takeoff_30.png` decode to exactly the same pixels as the matching `pose_*_fly_00.png` (max channel difference 0 over 300x300 px, all three cameras). `seam.txt`: 0.00 deg, 0.000 BU (limits 3 deg / 0.02 BU). The 30.6 deg wing snap and the 0.26-stud drop are gone. |
| MUST 2 | stretch the launch | **PASS** (numbers and read). The recovery after the launch is a new TO (TO C1). | Code L744-750: wing 36 (f13) to -8 (f17) to -36 (f21), so the downstroke takes 8 frames. Body z -0.075 (f14) to -0.01 (f18) to +0.07 (f22) = 0.145 BU = 0.65 studs over 8 frames (0.27 s). Pitch 17, 20, 24. Plant range(0,18) (f0-17), `lift_air_frames` from f18. Launch event 0.467 = f14. Front f15 to f19: wings drop from a V to horizontal. Game f21: both talons are off the ground and the body is raised. |
| MUST 3 | refs match the clips | **PARTIAL** | Done: #174482 and #256671 are not in `ANIM_REFS.md` (grep: no hits) and CLIP_NOTES says they were a mistake. The walk is H1 #260630. Not done: `ANIM_REFS.md` is still dated 00:50 and is out of step with the clip (walk "30 f / ~1.0 s", takeoff "airborne f16-19"). The code header (`pets/BlizzardRoc.py` L459-460) still credits #260711 for the takeoff and #260644 for head turns, although ANIM_REFS and CLIP_NOTES say both are supporting only and not on the site. See MUST 1. |
| MUST 4 | model evidence current | **PASS** | `_model_sheet`, `model_game`, `model_side`, the icon strips and the takeoff/walk sheets were all rendered at 04:22-04:23, after the last code edit. |
| TO 1 | knee bend in the coil | NOT DONE (lead ruling, not counted) | |
| TO 2 | walk weight | **PASS** | `n = 36` (L597). Lateral shift 0.01 BU over the stance (L612). `full_step1`: walk slide 0.0, foot_z_var 0.0, ground_min_z -0.015. The shift is small and reads only faintly. Accepted. |
| TO 3 | edge-on wings f16-19 | **PASS** | Twist +16 at f17 (24, L747) and f21 (22, L749). In the front crops, f17 shows feather steps and dark primaries, and f19-21 show stepped coverts on horizontal wings. They read as wings, not poles. f19-21 are still near-horizontal slabs (see TO C1). |
| TO 4 | tail from behind | **PARTIAL** | Outer pair at +-14, taper 0.58 (L365, L368). The rod read is gone from the game camera. But the fan is narrow (28 deg in total) and reads as one wedge with one violet band and a dark tip. The four violet tips are not separately visible. From the side (`model_side`) the tail is still a thin rod: the fan normal `(0, 0.34, 0.94)` is nearly vertical, so the feather plane is edge-on from the side. See TO M1. |
| TO 5 | smaller eye hot spot | **PASS** by code, evidence stale | FROST_H is now 0.010 x 0.002 (L164, was 0.014 x 0.003). At render scale the hot spot is not visible. No fresh close-up exists (see TO M4). |
| TO 6 | idle front f24 covert stagger | **NOT DONE** | Idle keys L583-584 shiver only the primary tips. The builder does not mention coverts. |
| TO 7 | runtime note | N/A to the clip | Land f0 = fly phase 0 (L779), so the runtime can trigger land at phase 0. Lead's item. |

**Round-6 claims from the builder:**
- Takeoff seam: verified (pixel-identical).
- Launch timing: verified in code and in the step-1 event values.
- Walk 1.2 s: verified in code.
- Tail +-14 and taper 0.58: verified in code, visible as a wedge from behind.
- Eye hot spot 0.010 x 0.002: verified in code, not visible in the renders.
- Tris 12,964 (`tris_body` in `full_step1`): verified.
- Ground margin: takeoff, land, roar and act_bow at -0.014, walk at -0.015, fly +0.377, collision_free true: verified.

---------------------------------------------------------------------------------------------------------------------
## 2. Scores

**Model 8.5 (PASS, floor).** Silhouette: a clear raptor-like bird. The studded skin, the CHAR mask, the hook beak and the violet crest read as fierce, not cute. The game-camera view shows wing primaries with violet tips and a narrow tail wedge. Held back by: a light grey back (47.5 % of the game view against a plan of dark back), the tail seen edge-on from the side, and bind-pose wings that read as poles from the front and 3/4 views.

**Clips 8.6 (motion, average of 7 clips).**

| clip | score | reason |
|---|---|---|
| idle | 9.0 | Unchanged. TO 6 (coverts) still open. |
| walk | 8.2 | 1.2 s, subtle weight shift, no slide. |
| fly | 8.5 | Unchanged. Clean stroke. |
| takeoff | 8.2 | Seam fixed (pixel-identical), 8-frame downstroke, 0.65-stud rise, feet off ground by f21. Held back by the post-launch recovery (TO C1) and a shallow coil (lead ruling). |
| land | 8.5 | Unchanged. |
| roar | 9.0 | Unchanged. |
| act_bow | 9.0 | Unchanged. |

---------------------------------------------------------------------------------------------------------------------
## 3. MUST list (blocks the clip gate)

**MUST 1 - documentation: the references must match the clips (no renders needed).**
- `BlizzardRoc/ANIM_REFS.md` L27: replace "walk (30 f loop): H1 wading walk: a ~1.0 s cycle" with "walk (36 f = 1.2 s loop): H1 wading walk (~1.0 s in the reference), slowed to 1.2 s on purpose (review 5 TO 9+), with a 0.01 BU lateral shift".
- `BlizzardRoc/ANIM_REFS.md` L32: replace "f16-19 airborne" with "first downstroke f13-21 (8 f); body rise f14-22; feet leave f18 (planted to f17); flight cycle f25-30".
- `BlizzardRoc/ANIM_REFS.md` header: "clip round 2" becomes "clip round 3 (review 5)".
- `pets/BlizzardRoc.py` L459-460: replace the reference list with "The Boy and the Heron (Sakugabooru #260630, animationreference.org item H1: takeoff, land, roar, act_bow, walk, idle); Bird Flight flapping tutorial (fly); #260711 and #260644 are supporting only, not on the site, and drive no clip."
- `ANIM_REFS.md` R1 and R4 rows: say "not used by any clip" (optional).
- Re-check: the four edits above. Nothing else needs re-review.

---------------------------------------------------------------------------------------------------------------------
## 4. TO 9+ list (after MUST 1; higher is better)

**Clips**

- **C1 - post-launch recovery (the biggest TO).** The f21 bottom (-36 deg) must join the fly-tempo phase at f25 (+20.5 deg). That is 56.5 deg in 4 frames (about 14 deg per frame), against about 4-9 deg per frame for the fly's own stroke. In the front sheet the wings go from horizontal at f23 to a V at f25, which reads as a quick lift.
  - Fix: lengthen the takeoff to **36 frames** and key the fly-tempo blend from f25 with `ph = 1 + (f - 36) / 30`, so f36 = fly f0 (the seam still holds exactly).
  - Computed with `wing3.stroke`: f21 -36 to f25 -19.5 (16.5 deg in 4 frames), then at most 7 deg per frame up to +36 at f36. The fly's own stroke peaks at 8.6 deg per frame (mean 4.9), so the recovery would sit inside the fly's own speed.
  - Launch event becomes 14/36 = 0.389. Re-run step 1 (collision_free, ground_min_z, step check) and the seam check.
- **C2 - coil legs (lead ruling, not counted).** Hips drop only about 3.7 %. Not re-raised.

**Model**

- **M1 - tail seen edge-on from the side.** The fan normal `(0, 0.34, 0.94)` (L362) makes the feather plane horizontal, so `model_side` shows a rod. Tilt the normal about 40 deg toward +-x so the side view shows a broad blade, then check that the game camera still shows a fan (not a rod).
- **M2 - bind-pose wings read as poles from the front and 3/4 views** (`model_front`, `model_tq`). Add a wing twist of about +16 deg to the bind pose (the same change as TO 3, applied to the hover pose).
- **M3 - light grey back.** The game-camera share is STORM_GREY 47.5 % and CHAR 19.2 % (MODEL_NOTES round 2), against a plan of a dark back. Darken the back shingles from (176,178,186) to about (158,160,170) or add one CHAR band across the mantle. Target: STORM at or below 40 % on the game camera.
- **M4 - fresh head close-up.** Render the head front and game views at 2x (the 27 Oct close sheets predate the eye change) and confirm the 0.010 hot spot reads as a slit, not a glint.

**Renders and notes**

- **N1 - frame labels.** The takeoff sheets have no visible frame labels (CLIP_NOTES says they do). Add the labels, or write the tile order into the notes. Tiles are 300 px: row 1 = f10 13 15 17 19, row 2 = f21 23 25 28 30.
- **N2 - idle f24 coverts** (round-5 TO 6): stagger the covert rows about 3-4 deg so the half-open wing does not read as flat plates.
- **N3 - stale code comments.** `pets/BlizzardRoc.py` L356 still says "FOUR plain feathers (no fan)", but the tail now fans +-14. The section header at L458 still says "clip round 1" (covered by MUST 1, item 4). Update both with the MUST 1 edit.

---------------------------------------------------------------------------------------------------------------------
## 5. Pass / fail

| # | check | result |
|---|---|---|
| 1 | step 1: collision_free, ground >= -0.02, audit linear 0, loops closed | PASS (-0.014 / -0.015, fly +0.377) |
| 2 | neck <= 8, chest vs spine <= 5 | PASS (Neck 7.5, Chest 4.0, `steps.txt`) |
| 3 | head + neck pitch-up <= 30 | PASS (26, CLIP_NOTES; not re-measured) |
| 4 | largest bone step <= 60 deg per frame | PASS (36.5 land, 32.6 roar, 30.3 takeoff) |
| 5 | events match frames | PASS (launch f14, touch f17, roar f20, snap f58, frostshed f24) |
| 6 | rest frames 0 deg | PASS (roar f60, act_bow f110, land f32; takeoff f30 = fly f0) |
| 7 | takeoff to fly seam | **PASS** (pixel-identical, all three cameras) |
| 8 | launch reads as weight | **PASS** (8-frame downstroke, 0.65-stud rise) |
| 9 | post-launch recovery | **TO C1** (56.5 deg in 4 frames) |
| 10 | refs cited and matching | **FAIL** (MUST 1: walk tempo, airborne frames, code header) |
| 11 | model evidence current | PASS (04:22-04:23 > code 04:21) |
| 12 | no glow; tris <= 15k | PASS (`tris_glow` {}, 12,964) |
| 13 | no head shakes, no airborne spin, acts in place, rest at end | PASS |
| 14 | idle, roar, act_bow, land read | PASS (TO N2 open on idle) |
| 15 | walk reads | PASS |
| 16 | fly reads | PASS |

---------------------------------------------------------------------------------------------------------------------
**Verdict.** Model 8.5, PASS (floor). Clips 8.6 motion, FIX for MUST 1 (documentation only). After MUST 1 the clips pass. The TO C1 recovery and TO M1-M3 are the next 9+ steps.
