# Glacier Yeti - FINAL 8.5 GATE, ROUND 2 (2026-10-28, fresh reviewer) - FIX

**Model: 8.0/10 - FIX. Clips: 8.5/10 - PASS.**

The owner's ship bar is 8.5 as a floor. Model stays under it because two of the owner's named faults are still partly visible (profile/front fangs, pale fist strips). Clips meet every written limit and all round-1 clip MUSTs.

## What I looked at

Current files only (all stamped after the pet file `pets/GlacierYeti.py`, 2026-10-28 01:12):
- Model: `GlacierYeti/renders/_model_sheet.png` (tq, front, side, back, game, under; 03:24), `_close_sheet.png` (03:24), `_flat_sheet.png` (03:24; the flat_side/tq/game set is 01:13), `_icons_strip_64.png` / `_128.png` (01:13), `_crust_sheet.png` (03:24), `_final_mouth.png` (01:15), `_throat_check.png` (03:25), single frames `pclose_side_idle_00.png`, `pclose_side_roar_30.png`, `beat_f85_ws_tq_walk_000.png`, `beat_f85_ws_tq_act_skid_007.png`.
- Clip: `_beats_f85_ir_side.png`, `_beats_f85_ir_tq.png` (idle f0-100, roar f0-60), `_beats_f85_ws_side.png`, `_beats_f85_ws_tq.png` (walk f0-42, skid f7-100), `_xfade_sheet.png` (01:14), `_scratch/xfade.json`, `_scratch/verify.json`, `_scratch/export_result_f85.txt`.
- Comparisons: `Raiju/renders/_model_sheet.png`, `_ALL_FIERCE_progress.png` (both 2026-10-09; the Yeti is not in the lineup).
- Code, checked against the claims: `pets/GlacierYeti.py` L16-24 (palette), L123-128 (`slab()`, hard-coded PLATE_ICE), L150-165 (hump spines), L230 (fang spikes), L245 (fist plate centre z 0.092), `head()` (Neck share 0.34, pitch cap 7.5), `idle()` / `walk()` / `roar()` tables.
- Notes and rules: `GlacierYeti/MODEL_NOTES.md` and `CLIP_NOTES.md` (final-85 sections), `GlacierYeti_plan.md`, `GLACIER_CONCEPTS.md` (owner decisions), Obsidian `Creature Style.md` and `Model Review Checklist.md`.

Not used as evidence: `renders/_jaw_close.png` is from 17:53 (before M1 and M2), so I did not score from it.

Not done: no Studio, no video, no crops (PIL is not installed; I read full-size single frames instead). Idle and walk motion amplitude is judged from the numbers and the still sheets only. `blockkit` rnd-cap claim (M5) not re-checked in source; judged on the visual result.

---

## Round-1 MUSTs

### Model

| # | Item | Result | Evidence |
|---|---|---|---|
| M1 | Fangs: no white teeth in profile | **PARTIAL** | Colour dulled to IVORY (200,196,184) (L23) and the spike is shorter (0.07, L230). Still reads as a white tooth: `pclose_side_idle_00` shows a pale cone ahead of the lower lip; `pclose_side_roar_30` shows a pale point in the open mouth; `pclose_front_idle_00`, `_final_mouth` and `_close_sheet` show two bright white triangles at the mouth corners. Target not met. See MN1. |
| M2 | Roar mouth is a dark cavity, not a red bar | **PASS** | `pclose_side_roar_30` and `pclose_front_roar_30` show a dark maroon-brown cavity (MOUTH (40,8,14)), no red bar. Closed idle hides it (`pclose_front_idle_00`). |
| M3 | Fist plates are not white brackets | **PARTIAL** | Thinner (0.018) and sunk, but a pale strip still crosses each fist top in `model_front` (bottom of each arm), `model_tq`, `beat_f85_ws_tq_walk_000` and `beat_f85_ws_tq_act_skid_007`. Target ("no white bracket") not met. See MN2. |
| M4 | Crust reads as broken ice, not a card | **PASS** | `_crust_sheet.png` and `crust_cside`: pale cap, green seam, mid-ice lip (PLATE_ICE_D) in stepped pieces, navy below. Second tone is visible front and side. The cap top is still one flat near-white slab (see P1). |
| M5 | Limbs are not stacked boxes | **PASS** | Upper arm, forearm, thigh and shin are now superellipse lofts (L237-238, L280-281). `model_front` and `model_tq` show rounded limbs with a bicep and calf belly; no hard box corners. |
| M6 | Verification (model) | **PARTIAL** | Done: `under.png` (03:24, belly-up from the final file), `flat_side/tq/game` (01:13, from the 01:12 file), `model_game` (Blender game-style view). Lead's ruling: the Studio 5-stud game-camera render is checked later, not scored here. The Blender game view shows the body as a mid-value periwinkle close to the approved Raiju in value (`Raiju/renders/_model_sheet.png`); accepted. |

### Clips

| # | Item | Result | Evidence |
|---|---|---|---|
| C1 | Final idle and roar sheets | **PASS** | `_beats_f85_ir_side/tq.png` (03:25), rendered from the 01:12 file. Idle f0/30/45/60/75/100 and roar f0/12/17/22/28/45/52/60 all present. |
| C2 | Roar lift readable | **PASS** | Code: head -18 (f17), -24 (f22/f28/f45) (`roar()` P table). `verify.json`: neck 7.69 (pitch and yaw combined; pitch capped 7.5), head joint 18.79, neck + head 26.5 (limit 30), armature pitch-up 24.08, jaw 26 at f32. Roar f22 in `_beats_f85_ir_tq` shows the head clearly up and the jaw open. |
| C3 | Idle not too still | **PASS (numbers)** | Code: plates 9 at f35/f45, breath -3.5, hip yaw 5, head drop still 6 at f65/f75. `verify.json`: chest vs spine 3.79, head joint 4.41. The hip sway is the main visible motion; motion amplitude is not verifiable from stills. |
| C4 | Walk readable at 5 studs | **PASS** | Code: fist LIFT 0.10, body bob 0.050 (`walk()`). `verify.json`: walk slide 0.0, loops closed, ground_min_z 0.002. The diagonal steps and fist plants read in `_beats_f85_ws_tq`. |
| C5 | Idle to walk 0.2 s cross-fade, no pop | **PASS (offline)** | `xfade.json`: starts from idle f0, f40, f75 and a walk f24 stop. Ground min -0.004, no collisions. Largest blend step 5.19 deg vs the walk's own 5.85 deg. The sheet shows only idle f40 and walk f24; the other starts are numeric only. Live check in Studio is the lead's (ruled out of score). |

### Round-1 TO 9+ items (for the record)

- T1 Neck bone: **PASS.** `NECK_SHARE 0.34`, `NECK_MAX 7.5`; neck hinges in `joints()` (L332-340).
- T2 Hump frost spines: **PASS.** Three PLATE_ICE blades (L150-165). Visible as a crest in `model_side` and `model_back`; hidden from the front.
- T3 Body colour: **PASS.** POLAR_NAVY (96,106,186) (L16), NAVY_D (80,90,170) (L17). Brightest channel 186, above the 170 rule.
- T4 Crust seam: **PASS.** AURORA bar 0.055 (L260).
- T5 Walk chest yaw: **PASS, deviation accepted.** The Chest turns ±4.5 and the Spine turns with it (-1.5). Shoulder line ±6 in the world, chest vs spine 4.61 (limit 5). Better than the ±6 chest-only option, which would break the 5-degree limit.

---

## Runtime risk: head look-turn

The builder is right. `CreatureAnimator` adds look × 0.5 to both Neck and Head, so the head yaw from a look-turn is about 2x that of a head-only pet. Other pets with a Neck already do this, so it is not a model or clip MUST. The lead should check it at 5 studs in Studio and, if the head turns too far, cap the look share on the Neck for this pet.

---

## New MUSTs (model only, blocking 8.5)

**MN1. Fangs still read as white teeth (M1 partial).**
- `pets/GlacierYeti.py` L23: IVORY (200,196,184) becomes (150,146,140), a dim bone grey, not white.
- L230 (`B.spike((s * 0.112, -0.77, 1.335), ...)`): base y -0.77 becomes -0.745; length 0.07 becomes 0.05. The tip then stays inside the muzzle volume (front face y -0.795) in profile.
- Target: no pale point ahead of the lower lip in `pclose_side_idle_00` or `pclose_side_roar_30`. In `pclose_front_idle_00` the fangs show as dim grey points at the mouth corners, not white triangles.

**MN2. Fist knuckle plates still read as pale strips (M3 partial).**
- L245 (`c = Fv + Vector((gx, -0.075, 0.092))`): centre z 0.092 becomes 0.080, so the plate sinks under the tapered fist top.
- `slab()` (L123-128) hard-codes `PLATE_ICE` in `B.poly(pts, thick, PLATE_ICE, bone)`. Add a colour argument and pass `PLATE_ICE_D` (184,206,222) for the two fist plates, so they stop reading as white.
- Target: no white strip on the fists in `model_front`, `model_tq`, `beat_f85_ws_tq_walk_000` (f0 and f36) or `beat_f85_ws_tq_act_skid_007`.
- After MN1 and MN2, re-render from the new file (Blender only): `pclose_side_idle_00`, `pclose_side_roar_30`, `pclose_front_idle_00`, `model_front`, `model_tq`, the walk tq f0 and skid tq f7. Check `collision_free` and `ground_min_z` are unchanged (step 1).

---

## TO 9+ (polish, not blocking)

- **P1. Crust cap is still a flat card from the front and back.** `model_front`, `model_back`: the cap top is one near-white slab. Split the top into two plates with a 0.01 gap, or chamfer the outer edge, so it reads as broken ice.
- **P2. Accent is lost at 64 px.** `_icons_strip_64.png`: the AURORA green on the crust seams does not survive. Consider widening the seam from 0.055 to about 0.07, or a green tip on the hump spines.
- **P3. Idle motion at 5 studs.** Only a conditional item: if the 5-stud Studio view shows the idle as static, raise the head drop at f65/f75 from 6 to 9 deg (head joint would stay near 8, under the 30 rule).
- **P4. Look-turn cap.** The runtime item above, if the lead wants it fixed for this pet.

---

## Pass / fail checklist

### Model

| Check | Result |
|---|---|
| 64 px: hunched beast reads | PASS |
| 128 px: pale shoulders, dark head, accent rim | PASS |
| Face fierce (brow, slits, no glint, no smile) | PASS |
| Fangs: no white teeth in profile or front | PARTIAL (MN1) |
| Roar mouth is a dark cavity | PASS |
| Fists: no white brackets | PARTIAL (MN2) |
| Crust: second tone, not a flat card | PASS (P1 for 9+) |
| Limbs: not stacked boxes | PASS |
| Body colour: brightest channel 170+ | PASS (186) |
| Floating, poking, or visible from below (front, side, back, under) | PASS |
| Tris <= 15k | PASS (7,640 per the export) |
| Studs everywhere, details smooth | PASS |
| No glow, no Neon | PASS |
| Game-camera read (5 studs, FOV 70) in Studio | DEFERRED to lead (not scored) |

### Clips

| Check | Result |
|---|---|
| collision_free, ground_min_z >= -0.02, linear 0, loops closed, walk slide 0 | PASS (`export_result_f85.txt`, `verify.json`) |
| Chest vs spine <= 5 | PASS (max 4.61, walk) |
| Neck <= 8 | PASS (7.69 combined) |
| Head + neck pitch-up <= 30 | PASS (26.5 at f22) |
| No head shakes, no airborne spins | PASS |
| Acts in place, end at rest | PASS (roar 0.056, act 0.234 deg) |
| Walk diagonal (LH, RF, RH, LF) | PASS (per round-3/4 measurement) |
| Skid beats readable | PASS |
| Roar readable | PASS |
| Idle readable at 5 studs | PASS (numbers; motion not verifiable from stills) |
| Walk readable at 5 studs | PASS (numbers and stills) |
| Renders match the final file | PASS (sheets 03:25 from the 01:12 file) |
| Idle to walk cross-fade | PASS offline; live check is the lead's |

---

## Expected result

MN1 and MN2 alone should take the model to about 8.5. P1 and P2 are the path to 9. The clips should hold at 8.5 unless the Studio cross-fade or the 5-stud motion check fails.
