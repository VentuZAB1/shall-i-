# Glacier Yeti - FINAL 8.5 GATE (2026-10-28) - FIX

**Model: 7.5 / 10. Clips: 7.5 / 10. Verdict: FIX (both under the 8.5 floor).**
The owner's bar is 8.5 as a floor. Higher is better (2026-10-28 clarification). Nothing under 8.5 ships.

Round-2 model (7) and the clip round (8) were the last reviews. This pet has moved a long way since review 1 (5/10). The silhouette, the face and the clip numbers are good. The last visible faults are the same kinds the owner has rejected before: white teeth in profile, a red bar for a mouth, and flat white cards on the shoulders.

## What I looked at

Final files (stamped 2026-10-28 00:02-00:03 or later):
- `GlacierYeti/renders/_model_sheet.png` (front, side, back, tq)
- `renders/model_side.png`, `renders/model_back.png`
- `renders/pclose_front_idle_00.png`, `pclose_front_roar_30.png`, `pclose_side_idle_00.png`, `pclose_side_roar_30.png`
- `renders/_final_mouth.png`
- `renders/_beats_walk_final_1028_0003_side.png`, `_tq.png` (f0, f12, f24, f36)
- `renders/_beats_skid_final_1028_0003_side.png`, `_tq.png` (f7 to f100, 12 frames each)

Stale (pre-final, read for context only):
- `renders/_icons_strip_64.png`, `_icons_strip_128.png` (17:31, the icons are unchanged in shape but predate the mouth and fang changes)
- `renders/flat_game.png` (17:30; the value shares come from `MODEL_NOTES.md`)
- `renders/_beats_rw_*` and `_beats_act_*` (17:55; no final roar or idle sheet exists)
- `renders/_close_sheet.png`, `_chest_sheet.png`, `under.png` (1027; not re-checked from the final file)

Comparisons: `_ALL_FIERCE_progress.png` (lineup), `Raiju/renders/_model_sheet.png` (the approved calibration pet). IceMammoth and LavaGolem were judged from the lineup and the strips, not their own sheets.

Notes and code: `_review/GlacierYeti_plan.md` (v2), `GlacierYeti_review1` to `review4`, `GlacierYeti/MODEL_NOTES.md`, `CLIP_NOTES.md` (round 4), `ANIM_REFS.md`, `_review/GLACIER_CONCEPTS.md` (owner decisions), `FIERCE_GUIDE.md`, `pets/GlacierYeti.py` (473 lines, read in full), and the Obsidian notes "Creature Style", "Model Review Checklist" and "Creature Animation".

Not done: no Blender, no Studio, no re-run of the headless JSON. Clip numbers come from `CLIP_NOTES.md` round 4 and review 4, which I cross-checked against the code. The game-camera (5 studs, FOV 70) view is still missing.

---

## Model score: 7.5 / 10

**What works**
- The hunch reads as a hunched ape or yeti at 64 px and 128 px. The pale shoulders and the dark head carry it.
- The face is fierce. The heavy brow V sits over narrow plate-grey slits in black sockets, with no glint, no round eye and no smile (`pclose_front_idle_00`).
- Studs cover the body, and the details (plates, claws, fangs, slits) stay smooth.
- Tris are 6,048 (CLIP_NOTES round 3), well under the 15k cap.
- The side and back views show no floating or poking parts. The belly line rises from the chest to the hind legs (`model_side.png`).
- The walk and skid frames show one clear silhouette per beat.

**What holds it at 7.5**
- **Fangs in profile.** The two IVORY fangs point up and forward from the lower jaw, and their tips sit in front of the snout face. In `pclose_side_idle_00` and `pclose_side_roar_30` they read as two white teeth. In the front view they are big white triangles at the mouth corners. The owner has rejected this read before (review 2 MUST 2, the crust icicle).
- **The open mouth is a red bar.** In `pclose_front_roar_30` the MOUTH block sits between the fangs as a flat red-brown slab. It does not read as a mouth.
- **Shoulder crusts read as white cards.** Each crust is a single flat PLATE_ICE cap. From the front (`model_front`, model sheet) they look like flat tiles.
- **Fist plates read as white brackets.** In the tq walk and skid frames the knuckle plates show as white bracket shapes on each dark fist.
- **Limbs are still stacked boxes.** The upper arm, forearm, thigh and shin keep hard block corners (rnd 0.50). From the front they read as sleeves and blocks, not muscle.
- **The accent is thin.** AURORA is 3 to 4 % and shows only on the crust rims. That is per the plan, so it is not a MUST, but it is the reason the 64 px strip shows little green.
- **The body colour is untested in game.** POLAR_NAVY (108,116,196) reads lilac-periwinkle in the Blender preview. The game-camera view (about 5 studs, FOV 70) has not been rendered.

## Clip score: 7.5 / 10

**What works**
- The numbers are clean (from `CLIP_NOTES` round 4 and review 4): collision-free at step 1, ground_min_z 0.002, linear 0, loops closed, walk slide 0.
- Chest vs spine max 4.39 (limit 5).
- Head joint plus neck max 22.55 (limit 30).
- No head shakes. No airborne spins. Acts play in place and end at rest (residual 0.06 and 0.23 degrees).
- The walk is the diagonal gait, verified in review 4 from the offsets and the baked data: LH f0, RF f12, RH f24, LF f36. Settled, not reopened.
- The skid reads as a skid and a brake in the final sheets. The drop (f7), the sled sweeps (f16 to f28), the dig and the open-mouth gasp (f58), and the push-up and rise (f74 to f100) all show clearly.

**What holds it at 7.5**
- **Neck limit (written as neck ≤ 8) is not met.** The Yeti has no Neck bone. The head joint peaks at 22.6 in the roar and 16.0 in the skid. The lead ruled Option B (head plus neck ≤ 30), and review 4 accepted it. I have not reopened the ruling, but it stays a known fail against the written checklist. TO 9+ item T1 is the clean fix.
- **Idle and walk are too small to read at 5 studs.** Plate lift is about 5.5 degrees (key 6). Chest breath is 2.4 degrees. The walk's body bob is 0.033 units, about 0.2 studs. The swinging fist lifts 0.07 units, about 0.4 studs. A phone player will see a near-still idle and a plod.
- **The roar has no final sheet.** `_beats_rw_*` is from 17:55, before the final JSON (21:57) and the mouth fix (00:03). Only `pclose_*_roar_30` and `_final_mouth.png` are current. The roar is judged from those frames. Review 4 MUST 1 is still open.
- **The idle has no final sheet either.** Only `pclose_*_idle_00` is current.
- **Idle to walk cross-fade** (0.2 s, CreatureAnimator) is not verified in the runtime (review 4 NICE 4).

---

## MUST for 8.5 (model)

M1. **Fangs (white teeth in profile).** `pets/GlacierYeti.py` L178-179, the IVORY spikes.
- Change the base y from -0.818 to -0.77.
- Change the length from 0.10 to 0.07.
- Result: the tip lands at about y -0.78, behind the snout face (y -0.795).
- Colour IVORY (238,234,220) becomes (200,196,184).
- Target: no white point ahead of the muzzle in `pclose_side_idle_00` and `pclose_side_roar_30`. In the front view the fangs show as short points only.

M2. **Roar mouth reads as a red bar.** L174 (the lip inlay, MOUTH, size 0.105 x 0.040 x 0.006) and L177 (the mouth block, MOUTH, size 0.082 x 0.062 x 0.042, bevel 0.012).
- Change both colours from MOUTH (86,18,30) to (40,8,14).
- On L177 change the bevel from 0.012 to 0.030 and the z half-size from 0.042 to 0.036.
- Target: the open roar reads as a dark cavity. The closed idle stays hidden.

M3. **Fist plates read as white brackets.** L195-198, the two knuckle plates per fist.
- Change the slab thickness (the 0.032 argument in L198) to 0.018.
- Change the plate centre z in L196 from 0.100 to 0.092, so the plates sink into the top edge.
- Target: no white bracket on the fist in `_beats_walk_final_1028_0003_tq` (f0, f36) and the skid tq f7.

M4. **Shoulder crusts read as flat white cards.** L201, the `shell(...)` cap (PLATE_ICE).
- Add a 0.03-tall lip under the cap's lower edge: a block at `cap.world((0, -cap.h.y - 0.01, -cap.h.z + 0.03))`, half size (cap.h.x x 0.9, 0.03, 0.03), colour PLATE_ICE_D (184,206,222), on bone `pl`, `nostud=True`, rnd 0.3.
- Result: three bands (light top, mid lip, navy body), so the crust reads as broken ice, not a card.
- Target: the crust shows a visible second tone from the front and the side (`model_front`, `pclose_front_idle_00`).

M5. **Limbs read as stacked boxes.** Raise the rnd to 0.66 on: the upper arm (L186, currently rnd 0.50), the forearm (L187, 0.50), the thigh (L222-223, 0.50), the shin (L224, 0.50) and the calf bulge (L226, 0.50).
- Target: no hard box corners on the arms and legs in the front and tq views.

M6. **Verification (model).** Before the next review:
- Studio game-camera render at about 5 studs, FOV 70, phone size, with the final palette. It judges the body colour (navy, not lilac) and the crust read. Shift POLAR_NAVY to (96,106,186) (TO 9+ T3) if it still reads lilac.
- Belly-up render from the final file. `under.png` is from 1027.
- Re-render `flat_side`, `flat_tq`, `flat_game` from the final file. The value shares in `MODEL_NOTES` are from 1027.

## MUST for 8.5 (clips)

C1. **Final idle and roar sheets.** Render tq and side pose sheets from the 21:57-or-later files. Idle at f0, f30, f45, f60, f75, f100. Roar at f0, f12, f17, f22, f28, f45, f52, f60. The 17:55 `_beats_rw_*` sheets are stale. Review 4 MUST 1 is still open.

C2. **Roar lift is too small to read.** `pets/GlacierYeti.py` L399-400, the roar P table.
- Change the head pitch hp from -20 to -24 at f22, f28 and f45. Also change -15 to -18 at f17.
- Expected head joint peak about 26.5 (limit 30). The jaw stays at 26.

C3. **Idle is too still.**
- L343 (PL): change the plate keys from 6.0 to 9.0 at f35 and f45.
- L347: change the chest breath from -2.4 * br to -3.5 * br.
- L346: change the hip yaw from 4.0 to 5.0.
- Check chest vs spine stays ≤ 5.

C4. **Walk is too small at 5 studs.**
- L362: change LIFT from 0.07 to 0.10.
- L368: change the body bob from `-0.033 * b` to `-0.050 * b`.
- Re-run step 1. Check collision-free, ground ≥ -0.02, walk slide 0 and the loop.

C5. **Verification (clips).** Check the idle to walk 0.2 s cross-fade in the Studio runtime (review 4 NICE 4). Confirm no pop.

---

## TO 9+ (the owner's "higher is better")

T1. **Add a Neck bone (Option A).** Insert `Neck` between Chest and Head in `rig()` (L239-242). Split the roar lift: Neck about 8, Head about 14. This clears the written neck ≤ 8 limit and the head plus neck ≤ 30 rule. Re-check the neck-sleeve hinge in `joints()` (L275-277).

T2. **A 64 px signature.** The Yeti has no feature the eye keeps at 64 px, and the Raiju has its dorsal spines. Add three short PLATE_ICE frost spikes on the hump ridge (hump at L113). Positions: x = 0, y about -0.10, 0.00 and +0.12, z about 1.57. Length 0.10 to 0.12, pointing back and up, `nostud=True`, not AURORA. The flat-topped plate read keeps them clear of Thunder Rex's crystal ridge. Check the side view for clearance.

T3. **Body colour, if needed.** If the game-camera render (M6) still reads lilac, change POLAR_NAVY (L16) from (108,116,196) to (96,106,186). The brightest channel stays 186, above the 170 rule.

T4. **Crust seam weight.** Widen the crust rim seam (L211, AURORA bar 0.040) to 0.055 so the green reads at 64 px. Keep the seam on the rim only.

T5. **Walk and idle weight shift.** In the walk, chest yaw (L369) from ±4 to ±6 so the arm drive reads from 5 studs. Hip sway in the idle (L346) is covered by C3.

---

## Pass / fail checklist

### Model

| Check | Result |
|---|---|
| 64 px: a hunched ape/yeti reads | PASS |
| 128 px: pale shoulders, dark head and accent rim read | PASS |
| Face fierce: slits under heavy brow, no round eye, no glint, no smile | PASS |
| No white teeth or grin in profile (fangs) | FAIL (M1) |
| Roar mouth reads as a cavity, not a red bar | FAIL (M2) |
| Fists read as fists (no white brackets) | PARTIAL (M3) |
| Shoulder crusts read as broken ice, not flat cards | PARTIAL (M4) |
| Limbs read as anatomy, not stacked boxes | PARTIAL (M5) |
| No box belly; belly line rises in side view | PASS |
| Dark body + ONE accent (plates and AURORA seams, the accepted exception) | PASS |
| Body colour rule: brightest channel 170 or more | PASS (196) |
| Studs everywhere, details smooth | PASS |
| No glow, no Neon | PASS |
| Tris ≤ 15k | PASS (6,048) |
| Floating, poking or intersecting parts (front, side, back) | PASS |
| Parts visible from below | NOT CHECKED on the final file (M6) |
| Game-camera read (5 studs, FOV 70) | NOT CHECKED (M6) |
| Tier fit: Big, below Roc, Titan and Absolute Zero, heavier than the Mammoth | PASS |
| Distinctness: no sibling copy | PASS (navy family shared with Raiju/ThunderBull, accepted cross-egg) |

### Clips

| Check | Result |
|---|---|
| Collision-free, ground ≥ -0.02, linear 0, loops closed, walk slide 0 | PASS (per CLIP_NOTES round 4 and review 4) |
| Chest vs spine ≤ 5 | PASS (max 4.39) |
| Head + neck pitch-up ≤ 30 | PASS (max 22.55) |
| Neck ≤ 8 (written rule; Head joint is the neck) | FAIL as written (lead ruling Option B stands; T1 is the clean fix) |
| No head shakes | PASS |
| No airborne spins | PASS |
| Acts in place (root net 0) | PASS |
| Acts end at rest | PASS (≤ 0.23 degrees) |
| Walk is the diagonal gait (LH, RF, RH, LF) | PASS (settled) |
| Skid beats readable in final sheets | PASS |
| Roar readable | PARTIAL (no final roar sheet; C1, C2) |
| Idle readable at 5 studs | FAIL-ish (plates 5.5 degrees, breath 2.4; C3) |
| Walk readable at 5 studs | PARTIAL (small motion; C4) |
| ANIM_REFS rule: 1-3 animationreference.org clips, cited | PASS (per review 4) |
| Renders match final files | PARTIAL (walk, skid and face final; idle and roar sheets missing; C1) |
| Idle to walk cross-fade | NOT CHECKED in runtime (C5) |

## Expected result

Fixing M1 to M5 should take the model to about 8.5. The clip MUSTs C1 to C4 should take the clips to about 8.5. M6 and C5 are the verification passes. T1 to T5 are the path to 9 and above. Re-review both gates after the next round.
