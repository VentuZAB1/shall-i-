# Volt Rhino - FINAL 8.5 GATE, ROUND 5 (2026-10-28) - FIX

**Model: 8.5/10 - PASS. Clips: 8.4/10 - FIX.**

The clips score is the lowest clip, the roar (8.4). The cause is the open-mouth beat: round 4 tapered the mouth interior (T4), which fixed the squared wedge but made the opening too small to read at phone scale (13 reddish px in a 360 px side frame). Three MUSTs block the ship. The model holds at 8.5 with no regression.

## What I looked at
- Brief; round-4 verdict; `MODEL_NOTES.md` (final gate round 4 polish); `CLIP_NOTES.md` (round 4); `ANIM_REFS.md`; `_scratch/verify.json`, `verify_out.txt`, `export_result_f85r4.txt` (06:10); `_scratch/feet_taps_f85r4.txt` (probe 06:11 on the 06:08:57 save); the r_* logs.
- `pets/VoltRhino.py`: read lines 300-350 (MOUTH, JAW interior, nose cap, eye); grep for JAW_MAX / MOUTH / ROAR_P / TAP_P.
- Images (folder `...\PetsV3\VoltRhino\renders\` unless noted): `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `..\VoltRhino_icon.png`, `_evidence_r4.png`, `pclose_side_roar_28.png`, `pclose_below_roar_28.png`, the newest beat sheets `_beats_f85r4_ir_side.png`, `_beats_f85r4_ir_tq.png`, `_beats_f85r4_wa_side.png`, `_beats_f85r4_wa_tq.png` (06:09-06:11), and `...\PetsV3\_ALL_FIERCE_progress.png`. Every image loaded.
- Pixel counts (read-only, stdout only, nothing written): the 64 px Volt eye as an ASCII map of the icon cell, and reddish mouth pixels in the 360 px roar frames.
- Not opened: `flat_side/tq/game.png` and the comparison pets' own model sheets. Palette shares are taken from MODEL_NOTES (IRON_D 43.4 % side, gate 25 %).

---------------------------------------------------------------------------------------------------------------------
## 1. Model score: 8.5/10 - PASS

What works:
- The silhouette reads at 128 px and at 64 px: a dark-backed rhino, an ivory horn with a lime zig, the studded hide and the pale belly.
- Palette follows the plan. In game, IRON_D is about 65 % of the visible body (MODEL_NOTES), so the back reads dark.
- Tris 14,532 (under 15k), glow {}, collision_free true, feet on the ground.
- The eye frame is wider than round 4 (BLACK 0.011 / 0.074 / 0.156). The black now shows on the lower-right side.

What keeps it at 8.5 and not higher:
- Eye at 64 px (T1, partial). The Volt cell has 6 lime pixels at (31,37), (31,38), (32,38), (30,39), (31,39), (30,40). Nine dark-ish pixels touch them: three under lum 60 and six at lum 60-95. Most are on the lower-right side and the top end. The upper-left long side is mid-grey. MODEL_NOTES says 7 lime and 8 dark. I count 6 and 9.
- Head is still a round tube capped by a dark nose plate (T3, not addressed). The side view reads a little like a sausage.
- At 64 px the Volt is the lightest body in the Thunder row (T2, owner call). Next to the dark Thunder pets in `_ALL_FIERCE_progress.png` (ThunderBull, MoltenBoar, ShadePanther) its body sits in the light grey-blue range. The lime is thin.

---------------------------------------------------------------------------------------------------------------------
## 2. Clip scores (clip score = lowest clip)

| clip | score | result | why | evidence |
|---|---|---|---|---|
| idle | 8.5 | PASS | Stamp reads at 360 px: the front-left leg is clearly up at f38 (sole 11 px higher than f30), others planted (idle_foot_drift 0). Flick at f90 (Tail3 15.1 deg). Snort 8 deg (head pitch-up 7.47 at f71) is present but faint on the 360 px frame (T5). Yaw is one slow cycle, not a shake. | `_beats_f85r4_ir_side.png` (f30/38/46), `verify.json` |
| walk | 8.6 | FIX (MUST 3, rule only) | Lateral touch-downs BL f0, FL f10, BR f20, FR f30 (measured). Duty 0.70, loop closed, slide 0, ground -0.002, chest vs spine 2.09. Motion is clean. The reference row is not from animationreference.org (MUST 3). | `_beats_f85r4_wa_side.png`, `verify.json`, `ANIM_REFS.md` |
| roar | 8.4 | FIX (MUST 1) | Open jaw is the signature beat and it reads as a sliver: 0 reddish px at f0, 13 px (7 x 2 px) at f20, f28 and f36 in the 360 px side frame, 27 px in the top-quarter frame. Head lift (pitch-up 16) reads well. The 5 deg neck pump reads small (T6). Neck max 7.8 (limit 8). | `beat_f85r4_ir_side_roar_028.png`, `beat_f85r4_ir_tq_roar_028.png`, `pclose_side_roar_28.png`, `pclose_below_roar_28.png` |
| act_horntap | 8.5 | FIX (MUST 2, verification) | Motion is solid: tips at f30/f42/f54 (Horn_Tip z 0.008 / 0.008 / 0.004), soles 0.000, snap over f57-64 with max 16.8 deg per frame on Head (was 26.7), chest 3.8 (limit 5), pitch-up 16. Taps 1 and 3 still look alike at phone scale (T8). Raw Head|Chest overlap for 80 frames is hidden by the throat hinge, and no view from below was rendered (MUST 2). | `_evidence_r4.png`, `_beats_f85r4_wa_side.png`, `_beats_f85r4_wa_tq.png`, `verify.json`, `feet_taps_f85r4.txt` |

Lead rulings not counted: VFX in Studio; walk speed (distance-driven animator).

---------------------------------------------------------------------------------------------------------------------
## 3. Round-4 items

| item | result | evidence |
|---|---|---|
| Ship check: act f30 / f42 / f54 re-rendered from the final save | PASS | `_evidence_r4.png` (06:10, side/front/tq) |
| Ship check: roar f28 side and below re-rendered | PASS | `pclose_side_roar_28.png`, `pclose_below_roar_28.png` (06:10) |
| Ship check: f54 snout vs brisket | PASS (visual) | `_evidence_r4` f54 side and tq: a clear gap in front of the foreleg. Builder: snout 0.048 above snow, tip 0.004. No under view (MUST 2). |
| Feet and horn tip at the taps | PASS | `feet_taps_f85r4.txt`: soles 0.000 at f30/42/54; Horn_Tip 0.008 / 0.008 / 0.004 |
| Limits (neck, chest, pitch-up, end at rest, ground) | PASS | `verify.json`: neck 2.06 / 2.48 / 7.8 / 6.0 (limit 8); chest 0.72 / 2.09 / 1.0 / 3.8 (limit 5); pitch-up 7.47 idle, 16 roar, 16 act (limit 30); one-shots end at rest 0.0; ground act -0.008 |
| Tris, glow, collisions | PASS | tris 14,532; glow {}; collision_free true (hinge-exempt, see MUST 2) |
| T1 eye socket at 64 px | PARTIAL | 6 lime px; 9 dark-ish px, mostly lower-right; upper-left side mid-grey (section 1) |
| T2 Volt legibility at 64 px (owner call) | NOT ADDRESSED | horn zig still 0.013 |
| T3 nose cap edge | NOT ADDRESSED | no change in MODEL_NOTES; no `closeb_cside2` re-render |
| T4 mouth taper | PARTIAL | shape fixed (line 316 `top=(0.30, 0.50)`, front 0.03 x 0.025). The visible opening fell to 13 px (MUST 1). |
| T5 snort 8 deg | PARTIAL | numbers right (f71-72, settles f76); still faint on a 360 px frame |
| T6 roar pump 5 deg | PARTIAL | neck pump 5 deg (base -2.8, pulse -7.8); reads small; neck is at 7.8 of 8 |
| T7 act snap spread | PASS | spread over f57-64; max 16.8 deg per frame (Head f60), was 26.7 (FX_BoltTrail) |
| T8 act taps 1 and 3 | NOT ADDRESSED | no tap-1 yaw in round-4 notes; f30 and f54 in `_beats_f85r4_wa_side.png` still alike |

---------------------------------------------------------------------------------------------------------------------
## 4. New MUSTs (blocking 8.5 on the clips)

**MUST 1 (roar, blocks the clip score): the open mouth must read at phone scale.**
- Measured: reddish px (R > G+25, R > B+20) in the 360 px side frames: 0 at f0, 13 at f20 / f28 / f36 (bbox x 81-87, y 175-176). Top-quarter f28: 27 px.
- Cause: round-4 T4 cut the mouth interior front from 0.07 x 0.0375 to 0.03 x 0.025 (`pets/VoltRhino.py` line 316, `top=(0.30, 0.50)`). The shape is right, but the visible opening is now too small.
- Fix: on line 316 change `top=(0.30, 0.50)` to `top=(0.45, 0.60)` (front end 0.045 x 0.030). Keep the throat end, the lip line (line 312) and `JAW_MAX = 14.0`.
- Acceptance (360 px renders, re-counted with the same test): side roar f28 at least 25 reddish px; top-quarter roar f28 at least 40; f0 still 0 in side and top-quarter; no maroon or pale speck below the snout in `closeb_cbelow` or `under.png`. If the closed-jaw check fails, use `top=(0.40, 0.56)` instead.

**MUST 2 (act, verification that can block): clearance from below at the taps.**
- `verify.json` raw counts with no hinge exemption: act Head|Chest 80 frames and Jaw|Chest 31 frames; roar 59; idle 51; walk 28. The 0.26 throat hinge hides them. The f30/f42/f54 checks are side, front and top-quarter only. None is from below.
- Fix: render act f42 and f54 from below the chin (camera under the throat, looking up) on the final save.
- Acceptance: no head, cheek or jaw surface visible through the brisket or the chest front in either frame. Report the raw counts for the final save.
- If skin shows: on the strike holds (f30-31, f42-43, f54-55), lift the Neck base by 0.015, then re-tune the Head pitch on the same keys until Horn_Tip z stays within 0.000-0.010. Re-run `probe_feet`.

**MUST 3 (walk, ANIM_REFS rule): the walk reference must come from animationreference.org.**
- The owner rule (memory: "before ANY animation, pull 1-3 clips from animationreference.org, note frames, cite in plan"). The walk row in `ANIM_REFS.md` cites Sakugabooru #144564 from a `walk_cycle animals` search. The only `/tags/walk-cycle` check was page 1 of 370 clips.
- Fix: either (a) open one quadruped walk on animationreference.org, step it, and add its URL and frame numbers to the walk row; or (b) write a no-fit row like the idle's, listing every walk-cycle page checked and the search terms.
- Acceptance: the walk row names an animationreference.org URL, or it documents a no-fit covering each page checked.
- Passing as-is: idle (`/tags/elephants`, a tag-page preview frame), roar (`/tags/wolfs-rain`), act (1014 site refs #5, #6, #9 plus the Muybridge plate). These are cited with frames.

---------------------------------------------------------------------------------------------------------------------
## 5. TO 9+ (ordered by impact; higher is better)

- **T1 (eye, 64 px):** widen BLACK's y half-size from 0.074 to 0.080 (`pets/VoltRhino.py` eye loop, line ~344) so the upper-left long side gets 2 or more dark px. Accept at 1:1 in `_icons_strip_64` when there are 6+ lime px and dark px touch both long sides.
- **T2 (Volt at 64 px, owner call):** the horn zig (line ~383) from 0.013 to 0.017 thick. Judge against ThunderBull in the strip. A FLANK darkening (126, 134, 150) toward (110, 118, 136) is an option if the owner wants the body darker, but it is a palette change.
- **T3 (nose cap):** pull the front-most nose ring (y -1.727, z 0.826, lines ~319-330) back by 0.004 to y -1.723, so the front edge in `closeb_cside2` stays below (230, 240, 250).
- **T5 (snort):** take the head toss from 8 to 10 deg. Pitch-up stays about 9.5, well under 30.
- **T6 (roar pump):** the neck is at 7.8 of 8, so the lever is the chest. Add +1.5 deg chest pitch on the bellow keys (f20, f28, f36). Chest vs spine is 1.0 now, limit 5.
- **T8 (act taps):** give tap 1 a 3 deg head yaw, as round 3 suggested, so the three strikes differ.
- **Optional (act snap):** Head peaks at 16.8 deg per frame at f60. Spread the snap over f56-66 to bring the peak to about 12.

---------------------------------------------------------------------------------------------------------------------
## 6. Pass / fail checklist (round 5)

| Item | Result | Evidence |
|---|---|---|
| Model score 8.5 floor | PASS (8.5) | model sheets, icon, strips, `export_result_f85r4.txt` |
| idle clip | PASS (8.5) | `_beats_f85r4_ir_side.png`, `verify.json` |
| walk clip | FIX (8.6, MUST 3) | `_beats_f85r4_wa_side.png`, `ANIM_REFS.md` |
| roar clip | FIX (8.4, MUST 1) | `beat_f85r4_ir_side_roar_028.png`, `beat_f85r4_ir_tq_roar_028.png` |
| act_horntap clip | FIX (8.5, MUST 2) | `_evidence_r4.png`, `verify.json` |
| Limits, end at rest, ground | PASS | `verify.json`, `export_result_f85r4.txt` |
| Feet and tips at taps | PASS | `feet_taps_f85r4.txt` |
| Tris, glow | PASS | 14,532; glow {} |
| Round-4 ship check (act, roar) | PASS | `_evidence_r4.png`, `pclose_*_roar_28.png` |
| Act raw collisions verified from below | NOT DONE | MUST 2 |
