**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.**

# Coral Crusher - FINAL GATE round 5 (9+ eye round check), 2026-10-28

Both scores hold at the 8.5 floor. The eye change is a real, measured improvement and nothing regressed. The eyes are still only a secondary read at phone size, so 9+ is not reached yet. Nothing blocks ship at 8.5.

## What I looked at
All six images opened; none failed to load.
- `renders/_eyes_r4_game1x.png` (file 05:26, title stamp 05:19): full 390 px game frame at f30 / 41 / 53 / 62 / 66, plus the eye box x4.
- `renders/_eyes_r4_game_cmp.png` (eye box before vs after at f30 / 41 / 66).
- `renders/_eyes_r4_face.png` (before vs after, front and high 3/4; title stamp 05:22).
- `renders/_model_sheet.png` (05:25): tq, front, side, back.
- `renders/_pose_tq_sheet.png` (05:24): all 26 beats.
- `CoralCrusher_portrait_alt.png`: dated **04:44, before the eye round**. The face is out of frame, so it does not show the eye change and I did not score the eyes from it.

Numbers (read from files, not re-run):
- `_scratch/eyepx_before.txt` / `eyepx_after.txt` (390 px, f30 to f41, own motion). Cen L 4.3 to 5.5, cen R 5.8 to 7.2, tip L 5.5 to 6.6, tip R 6.2 to 7.4 px. Total tip travel L 10.8 to 12.4, R 6.4 to 7.2. These match the builder's notes exactly. `vis` = 1.0 for both eyes at all nine probed frames (f30 to f76).
- `_scratch/export_eyes_r4.txt`: collision_free true, ground_min_z -0.013 in all four clips, linear 0, loops 0 / 0, walk slide 0.002, tris 12,452.
- Provenance: `pets/CoralCrusher.py` (saved 05:22) is identical to `_scratch/CoralCrusher_exported_eyes_r4.py`. Diffed against the 9+ backup, the only change is the eye block (`ES, EB = 1.25, 1.20` and its uses). The probe ran 05:17 and the crops are stamped 05:19. I found no other eye-geometry edit after the probe.

## The eye change: BETTER (small, measured)
- **Measured:** own motion is up about 25 to 30 % on both eyes at both troughs (f41 and f66). Left total tip travel 10.8 to 12.4 px. Both eyes are at or above the 4 px bar at both troughs.
- **Face (before vs after):** the bulbs, lids and socket are bigger and stand a little taller over the front rim. The slate lids stay angled and heavy, the socket stays black, and the rose slit stays narrow. From front and high 3/4 the eyes still read as angry slits, not round or googly. No glints, no smile. **It stays fierce.**
- **Claw clearance:** in the eye box x4 at f41 and f62, the crusher's lower edge passes above the right stalk and does not cover it. The ray-cast `vis` = 1.0 agrees.
- **Honest limit:** on the full 1x frame the eyes are still small dark marks. Their travel is roughly half an eye's width in the 4x crop, so it is readable when you look for it. At a glance on a phone it is still secondary. The round-4 "1-3 px" was an estimate, and the true "before" was already 4 to 6 px. So the round raised the number, but it did not change how the pet reads at a glance.

## Regressions
**None found.**
- Model sheet and pose sheet: claws, shell, legs, rose spikes and palette are unchanged. Nothing new intersects.
- Collision and ground gates pass.
- Not counted, as the brief says: pale underside (2.2 % game) and walk timing, both pending owner sign-off.

## What is still between this pet and 9+
1. **Eye read at phone size (the one 9+ point).** The change is correct and measurable, but a 9+ read needs the stalks to hold up in the 1x frame. A further bulb and lid step (about 10 to 15 % on the bulb and lid) is one option for the lead to weigh. It is a suggestion, not a must.
2. **Rose fin (round 4, NICE, still open).** The flat front-left spike in `renders/close_domeclusters.png` was not touched this round. Replace it with a cone like the others.
3. **Housekeeping, not a score item.** Re-make `CoralCrusher_portrait_alt.png` from the 05:24 file before it is uploaded. The eyes are out of frame there, so this does not affect the score.

**Model 8.5 PASS. Clips 8.5 PASS.** The eye round is better and still fierce, with no regression. I am not scoring 9 because the eyes are still only a secondary read at phone size and the round-4 rose fin is still open.
