# Glacier Yeti - FINAL 8.5 GATE, ROUND 3 (2026-10-28, fresh reviewer) - FIX

**Model: 8.2/10 - FIX. Clips: 8.5/10 - PASS.**

Summary: the two owner-named faults from round 2 are still visible in the newest renders. The fangs still render as near-white teeth and the fist tops still show a white strip. The split crust (P1) is a real improvement. The clips hold at the 8.5 floor. The idle head-drop change caused no regression.

## What I looked at

Newest set only: renders stamped 2026-10-28 03:56 to 03:58. The pet file `PetsV3/pets/GlacierYeti.py` is stamped 03:55, and the export is 03:59. All images opened without load errors.

- Model sheets (03:57): `renders/_model_sheet.png`, `renders/_close_sheet.png`.
- Model frames (03:56): `model_front.png`, `model_tq.png`, `model_side.png`, `model_back.png`, `model_game.png`, `under.png`, `renders/_final_mouth.png`, `renders/_crust_sheet.png`.
- Single frames: `pclose_front_idle_00.png`, `pclose_side_idle_00.png`, `pclose_side_roar_30.png`, `pclose_front_roar_30.png`, `beat_f85r2_ws_tq_walk_000.png`, `beat_f85r2_ws_tq_act_skid_007.png`.
- Strips (03:58): `_icons_strip_64.png`, `_icons_strip_128.png`, `flat_game.png`, `_flat_sheet.png`.
- Clip beat sheets (03:57): `_beats_f85r2_ir_tq.png`, `_beats_f85r2_ir_side.png`, `_beats_f85r2_ws_tq.png`, `_beats_f85r2_ws_side.png`.
- Numbers: `GlacierYeti/_scratch/verify.json`, the final-gate round 2 sections of `MODEL_NOTES.md` and `CLIP_NOTES.md`, and the palette and fang/fist code (lines 16-24, 230, 245-248).
- Pixel sampling: read-only sampling of the saved PNGs (System.Drawing). No edits, no Blender, no Studio. The values quoted below are those samples.

Caveat: these fang and fist-top readings come from the Blender preview renders. The brief makes these renders the judging evidence for this gate. The Studio 5-stud capture stays with the lead.

## Round-2 items

| Item | Result | Evidence |
|---|---|---|
| MN1 fangs: no white teeth (carried from round 2) | **FAIL** | `pclose_front_idle_00`: left fang tip (x 121-126, y 204-214) renders rgb (214,215,216), lum 215. Right fang (x 281-290, y 200-212) renders (203,204,203), with 81 px at lum 200 or more. Both read as white teeth, not dim grey. `pclose_side_idle_00`: the profile cone at the lower lip edge (x 176, y 208-216) renders (166,168,169), with a 229 highlight at (167,216). The tip still sits at the lip, not inside the muzzle. The builder's colour change (IVORY to (150,146,140)) did not produce a visible change in the render. |
| MN2 fist plates: no white strips (carried from round 2) | **FAIL** | `model_front`: the left fist top (box x 112-150, y 384-400) peaks at (251,255,255) at (146,391), with 142 px at lum 150 or more. The right fist top (box x 362-400) peaks at (237,255,255) at (371,390), with 119 px. The same white bar shows on `model_tq`, `beat_f85r2_ws_tq_walk_000` and `beat_f85r2_ws_tq_act_skid_007`. The fist plates are PLATE_ICE_D as the notes say (lines 245-248), but their top faces still render white. |
| M2 roar mouth is a dark cavity | PASS | `pclose_front_roar_30` and `pclose_side_roar_30` show a dark maroon cavity. Closed idle hides it. |
| M4 crust reads as broken ice | PASS | `_crust_sheet.png`: pale cap, green seam, mid-ice lip, navy below. |
| M5 limbs not stacked boxes | PASS | `model_front` and `model_tq`: rounded limbs with belly. |
| M6 verification set | PASS | Renders present for every view listed. The Studio game-camera check stays with the lead. |
| P1 crust reads as broken ice (front and back) | **PASS** | `crust_cfront` and `crust_cback`: the cap is two plates with a visible gap, and the outer plate is raised and tilted. Note: in profile (`model_side`, walk side f0-f42) the cap still reads as one flat white card. That is a 9+ item. |
| P2 accent survives at 64 px | **PARTIAL** | Seam is 0.070 (line 268). Green share in `flat_game.png` is 5.4% of non-black pixels, which agrees with the notes (5.2%). At 64 px the first icon holds 38 green-ish pixels out of 5,320 (about 0.7%), a faint trace. At 128 px it holds 158 of 19,040, clearly readable. |
| P3 idle head drop 9 deg | **PASS (numbers)** | Head local 6.35 at f76, neck 3.27 at f75. Head + neck is far under 30. In `_beats_f85r2_ir_tq` the head at f65 and f75 sits lower than at f0. The amplitude is modest at 5 studs, so the Studio check stays with the lead. |
| P4 look-turn doubling | Lead ruling | Not scored. |

Held from round 1 and round 2, all clip items:
- C1 to C5 hold.
- Chest vs spine: idle 3.79, walk 4.61, roar 4.08, act 4.39 (limit 5).
- Neck max roar 7.69 (limit 8).
- Head joint roar 18.79, pitch-up 24.08 (head + neck 26.5, limit 30).
- Ground min z 0.002 in all clips.
- `collisions_with_hinges` is empty.
- Loops closed. One-shots end at rest (0.056 and 0.234 deg).
- Walk diagonal sequence unchanged.

The fists are still white in the walk and skid frames, but that is a model item (MN2), not a clip item.

## Scores

**Model 8.2 (FIX).** P1 is fixed, the 128 px read is good, and the silhouette reads at 64 px. The two named faults (white fangs, white fist strips) are unchanged in the renders. The round-2 fixes for them did not land visually, so the model cannot move up to the 8.5 floor yet.

**Clips 8.5 (PASS).** No regression from the head-drop change. No new MUST. The live cross-fade and 5-stud checks in Studio are still open with the lead, and a failure there would take the clips below 8.5.

## MUSTs (blocking 8.5)

**MN1 (carried from round 2, still FAIL): fangs render as white teeth.**
- `pets/GlacierYeti.py` line 23: change IVORY from (150,146,140) to dark bone (72,70,68). Keep line 230 as it is (base y -0.745, length 0.05).
- Re-render from the new file. Pass when, in `pclose_front_idle_00.png`, every pixel in the fang tips at x 118-130, y 200-218 and x 280-292, y 198-214 has lum 170 or less. Currently the maximums are 215 and 207, with 81 px at 200 or more on the right fang.
- Pass when, in `pclose_side_idle_00.png`, the box x 160-192, y 200-226 has no pixel at lum 200 or more. Currently it has 5.
- If the builder believes the highlight is a preview-only specular, prove it in the Studio 5-stud capture before ship. For this gate, the render criterion stands.

**MN2 (carried from round 2, still FAIL): fist knuckle plates render white.**
- `pets/GlacierYeti.py` lines 245-248: the fist plates take the normal argument `(0, -0.45, 1)`. Change it to `(0, -1, 0.6)` so each plate faces forward-up and catches less top light. Change the plate colour from PLATE_ICE_D (184,206,222) to mid steel-ice (120,140,168).
- If that still fails, remove the top-face plates and keep the smooth BROW fist.
- Re-render. Pass when the maximum lum in the left fist box (x 112-150, y 384-400) and the right fist box (x 362-400, y 384-400) is 200 or less in `model_front.png`. Currently it is 254 and 250, with 142 and 119 px at 150 or more.
- Pass when no white top shows on the fists in `beat_f85r2_ws_tq_walk_000.png` or `beat_f85r2_ws_tq_act_skid_007.png`.

## TO 9+ (polish, not blocking)

- **P1b, profile crust.** In `model_side` and the walk side frames, the shoulder cap is a single flat white card. Chamfer the outer top edge by about 0.02 units, or split the top into a stepped third plate, so the profile breaks up like broken ice.
- **P2, 64 px accent.** The first 64 px icon has 38 green-ish pixels. Widen the crust front seam from 0.070 toward about 0.09, or give the rear hump blade an AURORA tip. Target 100 or more green-ish pixels in the first 64 px icon.
- **Idle at 5 studs.** The numbers pass. If the Studio 5-stud capture shows the idle as static, raise the f65 and f75 head drop from 9 to about 11 deg. Head joint stays well under 30.
- **Fang tip after MN1.** Confirm no tip shows ahead of the lower lip in profile after the colour change, so the fang does not read as a second white point.

## Pass/fail checklist

| Check | Result |
|---|---|
| 64 px: hunched beast reads | PASS |
| 128 px: pale shoulders, dark head, accent rim | PASS |
| Face fierce (brow, slits, no glint, no smile) | PASS |
| Fangs: no white teeth in profile or front | FAIL (MN1) |
| Roar mouth is a dark cavity | PASS |
| Fists: no white strip | FAIL (MN2) |
| Crust: second tone, broken ice from front and back | PASS (P1b for 9+) |
| Limbs: not stacked boxes | PASS |
| Body colour: brightest channel 170 or more | PASS (186) |
| Floating, poking, or visible from below | PASS |
| Accent at 64 px | PARTIAL (P2) |
| Clips: limits, ground, loops, rest, diagonal walk | PASS |
| Clips: idle and walk readable at 5 studs | PASS (numbers and stills; motion check in Studio) |
| Idle to walk cross-fade and 5-stud game camera | Lead, Studio (not scored) |
