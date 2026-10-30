# Glacier Yeti - FINAL 8.5 GATE, ROUND 6 (2026-10-28, fresh reviewer) - PASS

**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.**

Summary: both round-5 idle items are met. The plate beat now rises 5 f, holds 10 f at 13 deg and settles over 15 f, and M2 is accepted under the lead ruling. The model is unchanged since round 4 (geometry and palette), so it keeps its 8.5. The idle sits at the floor, not above it: the plate moves only about 3 px in a 360 px tile, the hold is 0.33 s against the cited reference's ~1 s, and the swing gate is met at exactly 4.0 with no margin. None of this blocks 8.5, so there are no MUSTs. The 9+ list is below.

## What I looked at

- **Read:** `GLACIER_REVIEWER_BRIEF.md`, `GlacierYeti_final85_r5.md`, `CLIP_NOTES.md` (through "Final gate round 5"), `ANIM_REFS.md`, `GLACIER_PLAN_REVIEW.md` (2.3 and 5), `GLACIER_CONCEPTS.md` (palette), `GlacierYeti_plan.md` (idle, palette).
- **Source:** `PetsV3/pets/GlacierYeti.py` `idle()` lines 412-429 (PL keys at line 418). Diffed against `GlacierYeti/_scratch/GlacierYeti_f85r4.py` ignoring CR endings: the only changes are the idle plate keys, the idle events and the idle docstring. Walk, roar, act, model and rig code are unchanged.
- **Numbers:** `GlacierYeti/_scratch/verify.json` (08:33), `GlacierYeti/_scratch/export_result_f85r5.txt` (08:33). Animation fps = 30 (header of `GlacierYeti.lua`).
- **Images opened (all loaded):**
  - `GlacierYeti/renders/_beats_f85r5_idle_side.png`, `_beats_f85r5_idle_tq.png`, `_beats_f85r5_idle_game.png`;
  - my zoom of the plate region from `beat_f85r5_idle_side_idle_*.png` (f0-f65; the set has no f33 or f75 files, so the zoom skipped them);
  - `_beats_f85_ws_tq.png` (walk and act, 03:24, from pets file 01:12, the current walk and act);
  - `_beats_f85r2_ir_tq.png`, `_beats_f85r2_ir_side.png` (roar, 03:57);
  - `_model_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `_close_sheet.png` (06:22 renders; geometry unchanged since).
- **My measurements** (scratch files in `C:\Users\ventu\AppData\Local\Temp\yeti_r6\`; nothing in the project was edited):
  - Mint seam centroid, side tile (px): f0 145.6, f20 146.5, f30 146.3, f35 143.1, f40 142.9, f45 142.8, f50 144.0, f55 145.2, f60 145.7. The seam is partly shaded during the hold (pixel count 800 to 720), so this is a rough measure, but the shape is clear.
  - Head top, side tile (px): f0 78, f30 81, f45 79, f55 82, f65 85, f80 81, f100 82, f120 78.
  - Body median colour, idle f0: game (88,103,177), tq (109,124,210), side (91,105,182).
- **Not available:** the Kung Fu Panda stepped frames are not in `renders/` or `_review/`. I accept M2 under the lead ruling but could not check the cited times myself.

## Per-clip scores (clips = LOWEST = idle)

| clip | score /10 | why (one line) | evidence file |
|---|---|---|---|
| idle (120 f, 30 fps, loop) | **8.5 - PASS (floor, no margin)** | M1 and M2 met: the plate now rises 5 f, holds 10 f at 13 deg (flat to 0.35 px) and falls 15 f. But the plate moves only about 3 px in a 360 px tile, the hold is 0.33 s, and the swing gate is met at exactly 4.0. | `renders/_beats_f85r5_idle_side.png`, `_beats_f85r5_idle_tq.png`, `_beats_f85r5_idle_game.png`; `renders/beat_f85r5_idle_side_idle_035.png` / `_045.png`; `_scratch/verify.json`; `_scratch/export_result_f85r5.txt` |
| walk (48 f, loop) | 8.6 - PASS | Knuckle walk, diagonal LH f0 / RF f12 / RH f24 / LF f36. Fists plant on the snow, head level. Keys unchanged this round; slide 0; chest vs spine 4.61. | `renders/_beats_f85_ws_tq.png` (03:24, pets file 01:12) |
| roar (60 f) | 8.6 - PASS | Shoulder heave, head lift, jaw open 26 deg at f32, back at rest (0.056). Neck 7.69 is 96 % of the 8 limit: thin margin, not a fail. | `renders/_beats_f85r2_ir_tq.png`, `renders/_beats_f85r2_ir_side.png` (03:57, current keys) |
| act_skid (100 f) | 8.6 - PASS | Drop, sled sweep, brake at f58, push-up, exact rest (0.234). Max swing 9.4 (Arm_R f78); neck 5.44; head joint 10.56. | `renders/_beats_f85_ws_tq.png` (act f7-f100, current); `_scratch/verify.json` |

**Clips score = 8.5 (idle, the lowest). PASS.**

## Round-5 items

| Item | Result | Evidence |
|---|---|---|
| **M1** idle plate beat: 5 f rise, 10 f hold at 13 deg, 15 f settle; events moved | **PASS** | Source line 418: `PL = [(0,0),(30,0),(35,13),(45,13),(60,0),(120,0)]`. Mint seam: rise 3.2 px over f30-35, drift 0.35 px over the f35-45 hold, fall 3.0 px over f45-60 (the fall is 3x the rise, as the Leviathan rule asks). Events `settle1` 0.292 (f35) and `settle2` 0.5 (f60) in the export. Amplitude is small (see 9+ item 1). |
| M1 gates: collision_free, ground, loop, foot drift, swing, head local, chest vs spine, neck, pitch-up | **PASS** (swing at the gate) | Export: collision_free true; ground 0.002 in all clips; linear 0; `idle_foot_drift` 0.0. verify.json: idle end_vs_start 0.0; max swing **4.0** (FX_AuroraDust_R f33, gate >= 4.0, no margin); head local 7.65 at f75; chest vs spine 4.45 at f80; neck 3.94; pitch-up 3.62. |
| **M2** reference, owner rule | **PASS** by lead ruling; documentation **PARTIAL** | `ANIM_REFS.md` "Idle reference, per-clip round 4": tag page `/tags/subtle`, Kung Fu Panda card, 0.5 s steps 9.5-16.0 s, key poses. Accepted under the ruling. The file still contradicts itself (lines 39 and 78, see documentation fixes). The mapping matches in ratio only (line 75 vs 82). |
| Walk / roar / act numbers unchanged | **PASS** | Source diff: no walk, roar or act edits. verify.json: walk chest vs spine 4.61, walk slide 0.0; roar neck 7.69, pitch-up 24.08, end at rest 0.056; act end at rest 0.234, act neck 5.44, head joint 10.56. |
| Idle head drop visible at phone scale | **PASS** | Head top moves 78 px (f0) to 85 px (f65) and back to 78 (f120): about 7 px in a 360 px tile by my threshold (the round-5 note said 10 px; keys are unchanged). |
| Pose limits: neck <= 8, chest vs spine <= 5, pitch-up <= 30; no head shakes, no airborne spins | **PASS** | verify.json, all clips. |
| Raw Head|Chest and Neck|Chest crossings before hinges (idle 32 / 68 f) | NOTE (risk) | verify.json `collisions_raw_no_hinges`; `collisions_with_hinges` is empty. Not scored (see 9+ item 8). |
| Model 64 px: species reads | **PASS** | `renders/_icons_strip_64.png` (Yeti first): hunched beast, pale shoulders, dark head. |
| Model 128 px: pale shoulders, dark head, accent rim | **PASS** | `renders/_icons_strip_128.png`. |
| Face fierce (brow V, slits, no glint, no smile) | **PASS** | `renders/_close_sheet.png` (06:22; geometry unchanged). |
| Fangs and fists: no white strip | **PASS** (by eye) | `renders/_close_sheet.png`, `renders/_model_sheet.png`. |
| Crust reads as broken ice, front and back | **PASS** | `renders/_model_sheet.png` (model_back, model_game). |
| Floating, poking, visible from below | **PASS** (by eye) | `renders/_model_sheet.png` (under, back). |
| Cap-top clip (9+ P1a) | PARTIAL (9+, carried) | Builder's numbers: 14 % of cap pixels at lum >= 250 (tq); target under 10 %. Not re-measured. |
| Profile cap is one flat card (9+ P1b) | OPEN (9+, carried) | `renders/_model_sheet.png` model_side: one flat slab. |
| 64 px accent (9+ P2) | PARTIAL (9+, carried) | Builder's count 44-61 green px in the first 64 px tile; target 100. Not re-measured. |

## New MUSTs

**None.** Nothing blocks 8.5 on the model or on any clip. The idle clears the floor on M1, M2 and every gate.

## Documentation fixes (required to close the reference record; not scored)

1. `ANIM_REFS.md` line 39 (idle, "How each clip uses them") still describes the round-1 keys: "lift 4 deg and settle twice, f30-40 and f40-50 (`settle` f50)". Replace with: "lift 13 deg f30-35, hold f35-45, settle f45-60 (settle1 f35, settle2 f60)".
2. `ANIM_REFS.md` line 78: "The shoulder crusts lift 13 deg twice (f35, f45)" contradicts the keys. Replace with the same single lift, hold and fall.
3. `ANIM_REFS.md` lines 75 and 82: the ratio matches (cited up-beat about 0.5 s to hold about 1 s, which is 5 f to 10 f in ours), but the absolute hold does not (ours is 10 f = 0.33 s at 30 fps; cited about 1 s). Write both in seconds so the mapping is not read as a time match.
4. `CLIP_NOTES.md` "Final gate round 5" and the round-5 review cite the 00:03 walk and act sheets (`_beats_walk_final_1028_0003_*`, `_beats_skid_final_1028_0003_*`). Those predate the final85 round (01:12): walk C4 (fist lift 0.07 to 0.10, body bob 0.033 to 0.050) and the T1 Neck bone on all clips. The round-5 statement that walk motion has been unchanged since round 2 is therefore not accurate for the sheets. Point the walk and act evidence at `renders/_beats_f85_ws_tq.png` (03:24, pets file 01:12) and re-render those sheets from the current file (round-5 9+ item 5).

## TO 9+ (not blocking)

1. **Make the plate beat visible (the biggest gap).** The crust moves about 3 px in a 360 px tile. In `pets/GlacierYeti.py` line 418, raise the hold from 13 to 18 deg: `PL = [(0,0),(30,0),(35,18),(45,18),(60,0),(120,0)]`. Keep the hold at f35-45 and the fall at f45-60. Expect about 4-5 px of motion and a max swing near 5.5, clear of the 4.0 gate. Re-run step 1: collision_free true (Plate_L/R vs Head and Jaw are already in `check_pairs`), loop closed, foot drift 0.
2. **Match the cited hold in seconds.** Hold f35-50 (15 f = 0.5 s), fall f50-65, and move `settle2` to f65 (0.542). Keep the head drop at f55-75. Same gates as item 1.
3. **Body colour.** The in-game median (88,103,177) is brighter than the plan's in-game navy (72,77,120). Darken POLAR_NAVY (96,106,186) to about (84,92,164) and NAVY_D (80,90,170) to about (70,78,146). Re-render the game view and the 64 px strip. This does not block: the brightest-channel rule (170 or more) passes, and the palette was accepted at 8.5 in rounds 4 and 5.
4. **Cap top faces (carried).** Lower CAP_ICE (182,200,214) to about (164,180,193) on the top faces only. Target: tq cap-top lum 235 or less, and under 10 % of cap pixels at 250 or more (now 14 %).
5. **Profile cap (carried P1b).** Chamfer the outer top edge by 0.02 units, or split the top into a stepped third plate, so the side silhouette breaks up.
6. **64 px accent (carried P2).** Widen the crust front seam from 0.070 to about 0.09, or add an AURORA tip to the rear hump. Target 100 or more green px in the first 64 px tile (now 44-61).
7. **Roar neck margin (carried).** Neck 7.69 against 8 (96 %) at roar f22. Move about 1 deg of the roar neck share into the Chest.
8. **Throat check before ship (risk).** The raw Neck|Chest crossings (68 f in idle) are hidden only by the sleeve hinges. Check one Studio close-up of the throat at idle f60-75 and roar f22.

## Checklist

| Check | Result |
|---|---|
| Model 8.5 floor (every item) | PASS (8.5; geometry and palette unchanged since 06:13; 9+ items open) |
| Idle 8.5 floor | PASS (8.5): M1 and M2 met; at the floor, no margin |
| Walk 8.5 floor | PASS (8.6) |
| Roar 8.5 floor | PASS (8.6; neck margin 4 %) |
| Act_skid 8.5 floor | PASS (8.6) |
| Lead rulings (look-turn doubling, 5-stud check, cross-fade, VFX, walk skate) | Not scored |
