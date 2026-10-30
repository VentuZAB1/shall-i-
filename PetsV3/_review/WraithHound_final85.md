# Wraith Hound - FINAL 8.5 GATE (model + clips, as exported) - 2026-10-28

**Model 7.5/10. Clips 8.0/10. Verdict: FIX.** Both are under the owner's 8.5 ship bar. Higher is better, so a TO 9+ list follows the MUST list.

Technically this is clean: 6,820 tris, no glow, studs on every surface, all pose limits pass with margin, and the roar jaw fix is in the export. The two things the plan was built on still fail from the player's eye, though. The ghost is lost in the game view (about half the pet is soot), and the mane still reads as stacked spines with three stair-stepped indigo points, not one streaming plume. The cloak act reads as a porcupine fan. The 8.5 given in review 4 was a combined score taken before this gate's bar and before a close look at the game-view shares and the act. This review scores model and clips separately, as asked.

## What I looked at
- Rules: vault `Creature Style.md`, `Model Review Checklist.md`, `Creature Animation.md`; `FIERCE_GUIDE.md`; `GLACIER_CONCEPTS.md` (Wraith line and the rarity table); `_review/WraithHound_plan.md` (v2); `WraithHound_review1-4.md`.
- Builder notes and data: `WraithHound/MODEL_NOTES.md`, `CLIP_NOTES.md`, `ANIM_REFS.md`, `renders/_shares.json`, `_scratch/fullcheck.json`, `_scratch/export.log`, `WraithHound.json`.
- Renders: `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `model_side.png`, `game_view.png`, `crop_mane_side.png`, `crop_mane_front.png`, `low_below.png`, `flat_side.png`, `flat_game.png`, `_pose_tq_sheet.png`, `_fan_front_back_r3.png`, `pclose_front_roar_30.png`, `pclose_side_act_smokecloak_47.png`.
- Comparisons: `Raiju/renders/_model_sheet.png`, `ShadePanther/renders/_model_sheet.png`, `PetsV3/_ALL_FIERCE_progress.png` (the lineup).
- Own read-only checks: the roar `Jaw` track from `WraithHound.json` (quaternions normalised, angle per frame); `pets/WraithHound.py` line numbers. No Blender, no Studio.

## Measured
**Shares (`_shares.json`, builder's count):**

| view | ASH_LAV | MIST | SOOT | INDIGO | plan / gate |
|---|---|---|---|---|---|
| side | 44.4 | 8.3 | 38.7 | 3.5 | SOOT <= 38 (review 2 gate) |
| game | 36.2 | 5.1 | **47.7** | 6.1 | body should read lavender in game |

The game view is the player's view. In `game_view.png` the saddle and the mane form one dark top from the withers to the tail root, and the pale part is only the flanks and legs. Nobody has gated the game share until now.

**Roar jaw (`WraithHound.json`, normalised, degrees from rest):** frames 0-11 at rest. The jaw opens from f12 (0.3), through f20 (15.2), to a peak of 23.5 at f26, which is the `snarl` event frame. It closes from f44 and is back at rest by f53. The ramp is smooth, with at most 2.4 degrees per frame. **The review-4 fix is in the export, and it passes.** The hold from f26 to f44 is not smooth, though: the jaw alternates 22.5 / 23.5 / 24.5 with a 4-frame period (7.5 Hz). That is the code's `tr` term (`pets/WraithHound.py` L392, `sin(2*pi*f/4)`) fed into the jaw (L397, `0.5 * tr`) and the mane (L400, `+-tr`).

**Limits (unchanged from `fullcheck.json` and the review-3 table; only the jaw moved since):** neck max 5.0 (<= 8), chest vs spine 2.9 (<= 5), head + neck pitch-up 8.0 (<= 30), head yaw 0 (1.5 in walk), no Spine/Root spin, Spine X = 0 in every clip, last frame = first frame, ground_min_z 0.004 (>= -0.02), collision_free true, linear 0, walk slide 0. The `fullcheck.json` (21:58) and `export.log` (21:59) are from the same run as the jaw fix.

---------------------------------------------------------------------------------------------------------------------
## MODEL: 7.5/10

**What works (keep):** a lean, long-legged canid that reads at 64 px (wedge head, pinned tall ears, long tail); studs on the whole surface and smooth details; fierce close-up face (heavy soot brows, slit eyes, black nose, ivory fangs, no glint, no smile); 6,820 tris; no glow; height 9.0 ties the Stallion; the lavender-ash hide is clearly not Raiju's royal blue.

**Why it stays under 8.5 (player's eye, 5 studs up):**
1. **The ghost is lost in game.** Game SOOT 47.7 % against a plan of 26 %. The top of the pet reads dark, and the pale body is only the flanks and legs.
2. **The crest reads as spines, not one plume.** Each of the three rows has its own indigo centre point (`mane_row` L79, default `INDIGO`), so there are three stair-stepped blue points in `crop_mane_side.png` and at 128 px. It is a Raiju-style dorsal fin row, not smoke.
3. **The accent is weak at icon size.** INDIGO is 6.1 % in game and the eye slits are 1-2 px at 64 px. At icon size the only accent is the crest points.
4. **The face does not carry at 64 px.** The eyes vanish in `_icons_strip_64.png`. The fierce read is close-up only.
5. **The white chest plate reads as a bib** from the front (`_close_sheet.png`, `crop_mane_front.png`). It is a NICE, not a MUST.

**Against the owner's favourites:** Raiju (the approved "design is fire") has a navy body with yellow bolts, so the 3-band block is high contrast. The Wraith is a pastel lilac with a dark top, so it is the washed-out pet in the lineup, and the Void-egg dark pets outclass it at phone size.

### MODEL MUST (to reach 8.5)
**M1 - game-view soot to 40 % or less (`pets/WraithHound.py` L70-71, L210).** The mane roots and middles are SOOT on every wisp. Set the root and middle segments of the centre, back and side wisps to a mid-slate, `WISP_ROOT = (128, 124, 166)` (#807CA6), so the mane reads as smoke rising from a lavender back. Keep SOOT on the tip segments and on the outer-low wisps (L87). At L210 change `ASH_LAV if i < 2 else SOOT` to `ASH_LAV if i < 3 else SOOT`, so the tail is a pale plume with a soot tuft at Tail4 only. Re-measure `flat_game` and `flat_side`: target game SOOT <= 40 %, game ASH_LAV >= 40 %. Record the root colour in MODEL_NOTES as a deviation from the plan (a soot mane), with the reason.

**M2 - one plume, one accent line (`mane_row` L79 and L84).**
- L79 (centre wisp): pass `tipcol=(INDIGO if bone == "Mane2" else SOOT)`, so only the tallest row keeps its indigo centre point.
- L79 (tail length): `0.36 * sc` becomes `(0.44 if bone == "Mane2" else 0.36) * sc`, so the tallest tip streams further back.
- Keep the indigo side tips (L84) for now.
- Check `crop_mane_side.png` and the 128 px strip. The blue points should read as one leading point and one line of side tips, not three stacked points.

**M3 - eyes readable at 64 px (`pets/WraithHound.py` L160-162).** The socket (L159) keeps its size so nothing pokes out of the head. Make the slit taller: L162 `(0.042, 0.006, 0.012)` becomes `(0.042, 0.006, 0.018)`. Make the rim taller: L160 `(0.047, 0.006, 0.014)` becomes `(0.047, 0.006, 0.020)`. Keep the tilt. Check the 64 px strip.

### MODEL TO 9+ (highest impact, after the MUSTs)
1. **Side tips to one line.** If the side tips of Mane1 and Mane3 still stair-step after M2, set `tipcol=(INDIGO if bone == "Mane2" else SOOT)` on the side wisps (L84). Watch the accent share: it must stay at 5 % or more in game.
2. **Lavender chest front.** Change the chest plate (L134) from `MIST` to `ASH_LAV`, and keep MIST on the throat (L138) and the belly strip (L132). That removes the white bib and gives the front a lavender read.
3. **Smoke, not spines, on the cloak.** This is a VFX check, not a model edit: the smoke wisp VFX on `FX_SmokeWisp_1-3` must be built (Blender-made, per the VFX rule) and checked in Studio at the `cloak` event (f28). A fan without smoke reads as a porcupine. With the smoke it reads as the ghost.

### MODEL NICE
- The lower chest plate and the belly strip are still flat slabs from below (`low_below.png`). Narrow the plate (L134) from 0.090 to about 0.075, and check the under view again.
- Put the new numbers (game SOOT, the plume tips, the eye sizes) into MODEL_NOTES.

---------------------------------------------------------------------------------------------------------------------
## CLIPS: 8.0/10

**What works:** every pose limit passes with margin. The loops close, the acts stay in place and end on the rest pose, and the feet stay planted (ground min 0.004). The roar jaw fix (f12 to f26, smooth, closes by f53, `snarl` on f26) is correct in the export. The walk knees are smooth (the review-4 fix). The idle sniff, the trot walk and the snarl all read, and the anim-reference rule holds (W0 site clip, with the Sakugabooru copy of the same file, accepted in review 4).

**Why it stays under 8.5:**
1. **A 4-frame jaw and mane flutter in the roar hold (f26-44).** The jaw alternates 22.5 / 23.5 / 24.5, and the mane rows move +-2 degrees on the same 4-frame cycle. That is a shiver, not a tremble.
2. **The roar's side wisps flare like batwing horns beside the ears** from the front (`pclose_front_roar_30.png`). The 25-degree roll at L401 is the cause.
3. **The cloak act reads as a porcupine crest, not a cloak.** At f47 (`pclose_side_act_smokecloak_47.png`, `_fan_front_back_r3.png`) the fan lifts up as well as out, so it stands up like spines. The 14-degree centre lift at L428 is the cause.

### CLIP MUST (to reach 8.5)
**C1 - kill the 4-frame flutter (`pets/WraithHound.py` L392).** Change `math.sin(2 * math.pi * f / 4)` to `math.sin(2 * math.pi * f / 10)`. That gives a 3 Hz tremble, +-1 degree on the jaw (L397) and +-2 degrees on the mane (L400). Check the Jaw track between f26 and f44: no 4-frame pattern. The amplitudes stay as they are.

**C2 - roar side wisps, not batwing wings (`pets/WraithHound.py` L401).** `[25.0 * m for m in mf]` becomes `[12.0 * m for m in mf]`. The roar keeps its lift (L400, 18 degrees) and the head drop. The act's 60-degree roll (L428) is not touched.

**C3 - the cloak fans sideways, not up (`pets/WraithHound.py` L428).** The centre lift `[14.0 * a for a in fan]` becomes `[6.0 * a for a in fan]`. Keep the 60-degree roll, the 3-frame row lag and the two drift cycles. Re-render the act f47 front and side. The fan should widen, not stand up.

### CLIP NICE
- Re-check the roar mane's last residual (`Mane3_R`, 0.49 degrees at f59, from review 4) so the roar ends exactly on frame 0.
- The crouch forelegs swing 41 degrees (review 3, NICE 4). It reads as a stalk, so it passes. Leave it.

---------------------------------------------------------------------------------------------------------------------
## Pass / fail checklist (final gate)

**Model**

| check | result |
|---|---|
| 64 px: species reads (canid, wedge head, ears, tail) | PASS |
| 64 px: ghost reads (pale body, dark topline) | **FAIL** (M1) |
| 128 px: one plume, not stacked spines | **FAIL** (M2) |
| Fierce face in close-up (brows, slit eyes, fangs, no glint, no smile) | PASS |
| Face reads at 64 px | **FAIL** (M3) |
| Studs on the whole surface, details smooth, no glow | PASS |
| Tris <= 15k (6,820) | PASS |
| Dark body + pale underside + one accent (in game) | **FAIL** (game SOOT 47.7 %, M1) |
| Accent distinct from Raiju and the Void violets | PASS (lighter than Raiju; 28-35 degrees from the violets) |
| No box belly, no plastic slabs (side and front) | PASS (from below: PARTIAL, NICE) |
| Floating or poking parts | PASS |
| Height ties the Stallion (9.0) | PASS |

**Clips**

| check | result |
|---|---|
| Neck <= 8 deg | PASS (5.0) |
| Chest vs spine <= 5 deg | PASS (2.9) |
| Head + neck pitch-up <= 30 deg | PASS (8.0) |
| No head shakes | PASS |
| No airborne spins | PASS |
| Acts in place, ending at rest | PASS |
| Ground >= -0.02, collision_free, linear 0, loops closed | PASS |
| Roar jaw opens over f11-26 (review-4 MUST) | PASS (f12 to f26, smooth) |
| Roar hold: no 4-frame flutter | **FAIL** (C1) |
| Roar reads as a mane flare, not batwing horns | **FAIL** (C2) |
| Cloak reads as a cloak, not a porcupine fan | **FAIL** (C3) |
| Idle and walk read | PASS |
| Anim-reference rule | PASS (accepted in review 4) |

---------------------------------------------------------------------------------------------------------------------
**Send-back:** apply M1-M3 and C1-C3 (the code lines are above), then re-render `flat_game`, `flat_side`, `_icons_strip_64`, `_icons_strip_128`, `crop_mane_side`, `pclose_front_roar_30` and the act f47 front and side. Re-run `fullcheck.json` and the Jaw track check (no 4-frame pattern). The smoke VFX (TO 9+ item 3) is checked in Studio, not in this gate.
