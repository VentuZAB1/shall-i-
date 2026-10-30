# Glacier Yeti - FINAL 8.5 GATE, ROUND 5 (2026-10-28, fresh reviewer) - FIX (clips)

**Model: 8.5/10 - PASS. Clips: 8.4/10 - FIX.**

Summary: the model still clears the floor. The shoulder caps are darker, the fangs and fists pass, and the silhouette holds at 64 and 128 px. The idle is much better than round 4 (the head drop and the cap tilt now show in the renders). It still fails 8.5 because the plate beat is a sharp triangle with no hold, and the cited animationreference.org reference was a card preview, not an opened clip. Walk, roar and act_skid are unchanged in motion and pass at 8.6. The lowest clip, idle, sets the score.

## What I looked at

- **Method:** PIL 12.3 and numpy 2.5 (Python 3.12 install). Every number below is measured on the renders. Scratch scripts are in `C:\Users\ventu\AppData\Local\Temp\yeti_r5\`. Nothing was edited except this file.
- **Read:** the brief, `GlacierYeti_final85_r4.md`, `PERCLIP_AUDIT_yeti.md`, `CLIP_NOTES.md` (round 4 and per-clip round 4), `MODEL_NOTES.md` (per-clip round 4, model 9+), `ANIM_REFS.md` (idle reference section), `_scratch/verify.json` (06:14), `_scratch/full_step1.txt` (06:14), `_scratch/export_result_f85r4.txt` (06:22), `renders/_beats_f85r4_idle.json`, the idle keyframe code in `PetsV3/pets/GlacierYeti.py` (`idle()`, `head()`, `plates()`, lines 393-431), and the owner rule `feedback-animation-references.md`.
- **Images opened (all load):** `_beats_f85r4_idle_side.png`, `_beats_f85r4_idle_tq.png`, `_beats_f85r4_idle_game.png` (06:23), `_model_sheet.png` (06:23), `_crust_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png` (06:23), `_beats_f85r3_ws_tq.png` / `_side.png` (walk and act_skid, 05:25), `_beats_f85r2_ir_tq.png` / `_side.png` (roar, 03:57). Zoom strips I made from the idle frames: cap crops (f0-f70) and head crops (f0-f100).
- **Not used:** the newest walk and skid sheets (`_beats_walk_final_1028_0003_*`, `_beats_skid_final_1028_0003_*`, 00:03). These are pre-cap-change, but the walk and skid motion has not changed since round 2, so they agree with the round-3 sheets.

## Per-clip scores (clips = LOWEST = idle)

| clip | score /10 | why (one line) | evidence file |
|---|---|---|---|
| idle (120 f loop) | **8.4 - FIX** | Head drop reads (about 10 px at 360 px, back by f100) and the cap tilts at f35/f45. The plate beat is a 5-frame rise, 5-frame fall triangle with no hold at 13 deg. That reads as a twitch, not a heavy settle. The cited reference is a card preview, not an opened clip. | `renders/_beats_f85r4_idle_side.png`, `_tq.png`, `_game.png`; `renders/beat_f85r4_idle_tq_idle_035.png` / `_045.png` vs `_000.png`; `_scratch/verify.json` |
| walk (48 f loop) | 8.6 - PASS | Diagonal knuckle walk (LH f0, RF f12, RH f24, LF f36), fists plant on the snow, hunched, head level. Slide 0, loop closed, chest vs spine 4.61 (92 % of limit). Motion unchanged since round 2. | `renders/_beats_f85r3_ws_tq.png`, `_beats_f85r3_ws_side.png`; `renders/_beats_walk_final_1028_0003_tq.png` |
| roar (60 f) | 8.6 - PASS | Shoulder heave, head lift, late jaw open (26 deg at f32), settles to rest. Neck 7.69 is 96 % of the 8 limit, so the margin is thin (risk, not a fail). | `renders/_beats_f85r2_ir_tq.png`, `_beats_f85r2_ir_side.png`; `renders/_final_mouth.png` |
| act_skid (100 f) | 8.6 - PASS | Drop, sled sweep, hard brake at f58, push-up, exact rest (0.234 deg). Max swing 9.4 (Arm_R f78), neck 5.44, head joint 10.56. | `renders/_beats_f85r3_ws_tq.png`, `_beats_f85r3_ws_side.png`; `renders/_beats_skid_final_1028_0003_side.png` |

**Clips score = 8.4 (idle, the lowest). FIX.**

## Per-clip audit items (round 5)

| Item | Result | Evidence |
|---|---|---|
| Idle loop closed, end vs start 0 | PASS | `verify.json` idle end_vs_start 0.0 |
| Idle foot drift 0, collision_free, ground 0.002 | PASS | `full_step1.txt`: collision_free true, ground_min_z 0.002 all clips |
| Idle max adjacent-frame swing >= 4.0 | PASS | 4.6 deg (FX_AuroraDust_L f48). Fix target met. |
| Idle head local at f75 >= 7.5 | PASS | 7.65 at f75 (`verify.json`); neck 3.94 |
| Idle chest vs spine <= 5 | PASS | 4.45 at f80 (89 % of limit) |
| Idle neck <= 8, head+neck pitch-up <= 30 | PASS | neck 3.94; pitch-up 3.62 |
| Idle head drop visible at phone scale | PASS | side-view top of the navy silhouette moves 75 -> 85 px (f0 -> f60-70) and back to 75 by f120 (measured, 360 px tiles). `head_side.png` shows the head lower at f60-f70. |
| Idle plate settle reads as a heavy settle | **FAIL** | Keys (`pets/GlacierYeti.py` line 415): `PL = [(0,0),(30,0),(35,13),(40,0.8),(45,13),(50,0),(120,0)]`. Each lift is a 5-frame rise and a 5-frame fall. There is no hold at 13 deg, and the fall is as fast as the rise. The cited reference (Kung Fu Panda card) has short head-up beats of about 0.5 s and longer holds. The Leviathan rule in `ANIM_REFS.md` (settle 2-3x slower than the rise) is not met on the plates. `cap_nearR_tq.png`: the tilt is visible at f35 and f45 but is a few px at 360 px. |
| Idle reference per owner rule (open 1-3 clips, step frame by frame) | **FAIL** (strict) | `ANIM_REFS.md` "Idle reference, per-clip round 4": the frames come from the card's own preview video, and the builder says the clip was not opened. The rule (`feedback-animation-references.md`) says open 1-3 clips and step them. 25 opens per day are available. The citation is real, but the rule is not met as written. |
| Walk / roar / act numbers unchanged | PASS | walk slide 0, chest vs spine 4.61; roar neck 7.69, pitch-up 24.08, end at rest 0.056; act end at rest 0.234 |
| Raw Head|Chest and Neck|Chest crossings (idle 32 / 68 frames before hinges) | NOTE (risk) | `verify.json` `collisions_raw_no_hinges`. Hinges clear them to 0 with slides up to 0.05, so the rig relies on sleeve hinges. Visible crops show no poke. Not a score item. |
| Pose limits: neck <= 8, chest vs spine <= 5, pitch-up <= 30, no head shakes, no airborne spins | PASS | all clips in `verify.json` |

## Model audit items (round 5)

| Check | Result | Evidence |
|---|---|---|
| 64 px: species reads, hunched beast | PASS | `_icons_strip_64.png` (Yeti first) |
| 128 px: pale shoulders, dark head, accent rim | PASS | `_icons_strip_128.png` |
| Face fierce (brow V, slits, no glint, no smile) | PASS | `close_front.png`, `close_tq.png` |
| Fangs: no white teeth | PASS (by eye) | `close_front.png`: small tan points at the mouth corners. Round-4 pixel check (154-155) is not re-measured. |
| Fists: no white strip | PASS (by eye) | `model_front.png`: fist plates are grey-blue |
| Roar mouth is a dark cavity | PASS | `_final_mouth.png` (round 4) |
| Crust reads as broken ice front and back | PASS | `_crust_sheet.png` (cap, mint seam, mid-ice lip, navy) |
| Cap-top clip (9+ item): lit cap-top median <= 235, under 10 % of cap pixels at 250+ | PARTIAL (9+) | Builder numbers (cap-masked): 14 % (tq), 6 % (side), 2 % (game) at lum >= 250; tq median 237. My unmasked pale-pixel count is not comparable (it includes sky and ground), so I use the builder's cap-masked figures. Tq is still above the target. |
| Profile cap is one flat card (9+ item P1b) | OPEN (9+) | `model_side.png`: the cap top is still a single flat slab |
| 64 px accent (9+ item P2, target 100 green px) | PARTIAL (9+) | First 64 px tile: about 44-61 green-ish px depending on threshold (approximate). Below 100. |
| Limbs not stacked boxes; studs consistent | PASS | `model_tq.png`, `under.png` |
| Floating, poking or visible from below | PASS | `under.png`, `model_back.png` |
| Accent strong enough in game colours | PASS | `_beats_f85r4_idle_game.png` (mint seam and crust read) |
| Body colour brightest channel 170+ | PASS | POLAR_NAVY (96,106,186) per `MODEL_NOTES.md` |

## MUST (blocks 8.5 on a clip)

**M1 (idle, the plate beat).** In `pets/GlacierYeti.py` `idle()`, replace the plate keys with a single held settle:
- `PL = [(0,0), (30,0), (35,13), (45,13), (60,0), (120,0)]`.
- The rise stays 5 frames (f30 to f35, so the max adjacent-frame swing stays at about 4.6 deg, above the 4.0 gate).
- The hold is 10 frames at 13 deg (f35 to f45).
- The fall is 15 frames (f45 to f60), which is 3x the rise.
- Remove the second lift (f40 / f45) and the dip to 0.8.
- Keep the head drop at f55-75 as a separate beat. Re-run `headless_full` step 1. Gates: collision_free true; idle max adjacent-frame swing >= 4.0; head local at f75 >= 7.5; chest vs spine <= 5; loop closed; foot drift 0.
- If the builder keeps two lifts instead, each lift needs a hold of at least 6 frames at 13 deg, and each fall needs at least 8 frames.

**M2 (idle, the reference rule).** Open at least one clip from animationreference.org for the idle (a heavy creature settle or a breath, for example the Kung Fu Panda clip itself, not the card preview). Step it frame by frame. Put the clip title, tag, the frame numbers used, and the hold length into `ANIM_REFS.md`, and show how M1's hold and fall map to them. Keep the card preview as a secondary note. This is documentation, but the owner rule requires it, and the current cited timing (short head-up beats, longer holds) does not match the triangle keys.

Both M1 and M2 are required for idle to reach 8.5. Once M1 and M2 pass, idle should move to about 8.6 (the model and the other clips are already at or above the floor).

## TO 9+ (not blocking)

1. **Cap top faces:** lower CAP_ICE (182,200,214) by a further 10 % on the top faces only, to about (164,180,193). Target: tq cap-top median lum 235 or less, and under 10 % of cap pixels at 250+. Keep the mint seam and the lip. Re-check the 128 px pale read.
2. **Profile cap (P1b):** chamfer the outer top edge 0.02 units, or split the top into a stepped third plate, so the side silhouette breaks up like broken ice (`model_side.png`).
3. **64 px accent (P2):** widen the crust front seam from 0.070 toward about 0.09, or add an AURORA tip to the rear hump blade. Target 100 or more green-ish px in the first 64 px tile.
4. **Roar neck margin:** neck 7.69 against a limit of 8 (96 %). Lower the roar neck share by about 1 deg, or spread it into the Chest, to get margin for Studio.
5. **Sheets:** re-render the walk and act sheets from the 06:13 file (the current walk and act sheets predate the cap change). Documentation only.
6. **Idle plate motion:** a second, smaller settle (about 6 deg) after the hold would add life, but only after M1 and M2 pass.

## Checklist

| Check | Result |
|---|---|
| Model 8.5 floor (every item) | PASS (8.5, at the floor; 9+ items open) |
| Idle 8.5 floor | FAIL (8.4): plate triangle + reference rule |
| Walk 8.5 floor | PASS (8.6) |
| Roar 8.5 floor | PASS (8.6; neck margin 4 %) |
| Act_skid 8.5 floor | PASS (8.6) |
| Lead rulings (look-turn doubling, 5-stud check, cross-fade, VFX, walk skate) | Not scored |
