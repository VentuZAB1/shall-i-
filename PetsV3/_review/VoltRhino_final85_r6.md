# Volt Rhino - FINAL 8.5 GATE, ROUND 6 (2026-10-28) - PASS

**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.** (Clips = the lowest clip, idle 8.5.)

No new MUSTs block the ship. All three round 5 MUSTs are closed with evidence. The TO 9+ list below is still open.

---------------------------------------------------------------------------------------------------------------------
## What I looked at
- Brief (`GLACIER_REVIEWER_BRIEF.md`), round 5 verdict (`VoltRhino_final85_r5.md`), `CLIP_NOTES.md` (Final gate round 5), `ANIM_REFS.md` (walk row and the W0 / elephants rows), `_scratch/verify.json`, `verify_out.txt`, `export_result_f85r5.txt`, `feet_taps_f85r5.txt`, `r_*.txt` probe logs.
- Source `PetsV3/pets/VoltRhino.py`, grep only: line 29 (JAW_MAX 14), line 317 (`top=(0.45, 0.76)`), line 323 (nose ring), line 344 (eye socket), line 383 (horn zig 0.013), line 543 (snort 8 deg), lines 590-614 (roar pump), line 645 (tap1 yaw 0).
- Images (all loaded, folder `VoltRhino\renders\`): `_beats_f85r5_wr_side.png` and `_beats_f85r5_wr_tq.png` (walk + roar, 08:32); `_under_act_r5.png` (act f42 / f54 from below, ground hidden); `_chin_sheet.png`; `closeb_cbelow.png`; `closeb_cside2.png`; `under.png`; `beat_f85r5_wr_side_roar_000.png`; `_beats_f85r4_ir_side.png` (newest idle sheet, 06:11, since idle was not changed in round 5); `_beats_f85r4_wa_side.png` (newest act sheet, 06:11); `_model_sheet.png` (06:10); `_close_sheet.png` (06:10); `_icons_strip_64.png` and `_icons_strip_128.png` (08:31).
- Pixel counts (stdout only, nothing written): reddish = R > G+25 and R > B+20, same test as round 5.

---------------------------------------------------------------------------------------------------------------------
## 1. Model score: 8.5/10 - PASS
What works:
- The rhino reads at 128 px and at 64 px: dark studded back, pale belly, ivory horn with lime zig, lime bolts.
- The face close-up (`_close_sheet.png`) shows a dark slit eye with a lime inlay under a dark brow, with no glints and no smile. It is fierce, not cute.
- `under.png`: the pale band on the head underside is body colour (sampled RGB 172,188,209 against body 171,186,207), not background. No see-through gap.
- Tris 14,532, glow {}, collision_free true, export collisions {}.

What keeps it at 8.5, not higher:
- Eye at 64 px (round 4 T1, still open). BLACK socket half-size is still 0.074 (line 344).
- The Volt is still the lightest body in the Thunder row at 64 px (T2, owner call). Horn zig still 0.013 (line 383).
- Nose cap is still a flat dark disc; the front ring is at y -1.727 (T3, line 323).
- The model sheet dates from 06:10. The only geometry change since then is the mouth interior front (line 317), and the closed-jaw counts below cover it.

---------------------------------------------------------------------------------------------------------------------
## 2. Clip scores (clip score = lowest clip)

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.5 | Unchanged since round 4. Stamp lift at f38 reads, flick f90, horn tilt is one slow cycle. Snort is still faint (T5). Numbers: chest vs spine 0.72, neck 2.06, pitch-up 7.47, max swing 15.1 (tail flick). Evidence is the 06:09 round 4 sheet. | `_beats_f85r4_ir_side.png`, `verify.json` |
| walk | 8.6 | MUST 3 closed (site reference now cited). Lateral sequence, duty 0.70 by builder measure, slide 0, loop closed, chest vs spine 2.09, neck 2.48. Motion unchanged from round 5. The walk reads as a heavy, level, low-headed walk. | `_beats_f85r5_wr_side.png` (walk f0-35), `_beats_f85r5_wr_tq.png`, `ANIM_REFS.md` walk row |
| roar | 8.6 | MUST 1 closed: the open mouth now reads as a dark red wedge under the snout at f20 / f28 / f36 in both views (33 px side, 51 px top-quarter; 0 px at f0). It is still a thin sliver of about 12 x 5 px at 360 px. The neck pump is still 5 deg and reads small (T6). Neck is 7.8, at the limit of 8. | `_beats_f85r5_wr_side.png`, `_beats_f85r5_wr_tq.png`, `beat_f85r5_wr_side_roar_028.png`, `_chin_sheet.png` |
| act_horntap | 8.6 | MUST 2 closed: from below at f42 and f54 (under and underside) the pale brisket is unbroken and no head skin shows; horn tip 0.0076 / 0.0035 on the snow; soles 0.000; snap max 16.8 per frame (was 26.7). Taps 1 and 3 still look alike (T8). The act side sheet is the 06:09 round 4 render; its pose is unchanged. | `_under_act_r5.png`, `verify.json`, `feet_taps_f85r5.txt` |

Clips score = lowest = **idle 8.5 - PASS**.

Limits (all within the brief): neck idle 2.06 / walk 2.48 / roar 7.8 / act 6.0 (limit 8). Chest vs spine 0.72 / 2.09 / 1.0 / 3.8 (limit 5). Head pitch-up 7.47 / 0 / 16 / 16 (limit 30). Roar and act end at rest (0.0 vs start and vs bind). Ground min z idle 0.0, walk -0.002, roar 0.0, act -0.008. Loops closed, walk slide 0, idle foot drift 0. Snap is a strike return, not a head shake.

---------------------------------------------------------------------------------------------------------------------
## 3. Round 5 items

| item | result | evidence |
|---|---|---|
| MUST 1 roar mouth reads at phone scale | **PASS** | Source line 317 is `top=(0.45, 0.76)`, not the asked (0.45, 0.60). The builder measured 23 px at 0.60, so the deviation is accepted because the acceptance is pixel-based. Counts (mine): side f20 / f28 / f36 = 33 px (need 25); top-quarter = 51 px (need 40); f0 = 0 px in both. Closed-jaw checks = 0 px: `closeb_cbelow.png`, `under.png`, side f0. JAW_MAX 14 kept (line 29). |
| MUST 2 act clearance from below | **PASS** | `_under_act_r5.png` (f42 and f54, under and underside): the pale brisket is unbroken, no head or cheek surface through the chest front, horn tip on the snow. Raw overlap is still hidden by the throat hinge (`verify.json` collisions_raw_no_hinges: Head|Chest 80, Jaw|Chest 28), and the brief asks for the raw counts to be reported, which they are. |
| MUST 3 walk reference from animationreference.org | **PASS** | `ANIM_REFS.md` walk row cites `/tags/elephants`, card "Video by projectarcheology", stepped from the tag page's preview at 10.0-11.4 s in 0.2 s steps, with no clip open. Other tag pages are listed. This meets the lead ruling that a stepped tag-page preview with cited times counts. The 40 f cycle and duty 0.70 fit the cited timing. |
| Round 5 limits, end at rest, ground | PASS | `verify.json`, `export_result_f85r5.txt` |
| Feet and horn tip at the taps | PASS | `feet_taps_f85r5.txt`: soles 0.000 at f30 / f42 / f54; Horn_Tip z 0.008 / 0.008 / 0.004 |
| Tris, glow, collisions | PASS | 14,532; glow {}; collision_free true |
| T1 eye socket at 64 px | NOT ADDRESSED | line 344 still `(0.011, 0.074, 0.156)` |
| T2 Volt legibility at 64 px (owner call) | NOT ADDRESSED | line 383 horn zig still 0.013 |
| T3 nose cap edge | NOT ADDRESSED | line 323 still y -1.727 |
| T5 snort 8 deg | NOT ADDRESSED | line 543 still `8.0 * sn`; faint in the 360 px idle frames |
| T6 roar pump 5 deg | NOT ADDRESSED | lines 590 / 614 unchanged; neck still 7.8 of 8, so the pump must come from the chest |
| T8 act taps 1 and 3 alike | NOT ADDRESSED | line 645 tap1 yaw is still 0; Horn_Tip x is -0.0 at f30, f42 and f54 |
| Optional act snap spread | PASS (round 4) | max 16.8 per frame (was 26.7) |

---------------------------------------------------------------------------------------------------------------------
## 4. New MUSTs

None. Nothing in round 6 blocks 8.5 on the model or on any clip.

Check before ship (verification, not a score change): the mouth front was deepened at 08:20, after the act hold and idle snort frames were last rendered (06:09). Re-render side view at the final save: act f62, f70, f86 and idle f72, at 360 px. Acceptance: no maroon or pale speck under the snout beyond the roar wedge. If one appears, use `top=(0.40, 0.56)` (round 5 fallback) and re-run the closed-jaw count (f0 = 0 px).

---------------------------------------------------------------------------------------------------------------------
## 5. TO 9+ (ordered by impact; higher is better)

1. **Roar opening depth (roar, the signature beat):** line 317 `top=(0.45, 0.76)` to `top=(0.45, 0.84)`. Acceptance: side f28 at least 40 reddish px (now 33), top-quarter f28 at least 60 (now 51), f0 still 0 px in both, `closeb_cbelow` and `under.png` still 0 px.
2. **T6 roar pump (roar):** add +1.5 deg chest pitch on the bellow keys f20, f28, f36 (lines ~612-614). Acceptance: chest vs spine at most 5 (now 1.0), neck max stays 7.8 or less, pitch-up stays 16.
3. **T8 act taps (act):** give tap1 a 3 deg head yaw (line 645 tap1 row, yaw 0 to 3). Acceptance: Horn_Tip x at tap1 differs from tap3 by at least 0.04 (both are about 0.0 now); re-run `probe_feet` and keep the soles at 0.000.
4. **T1 eye socket at 64 px (model):** BLACK y half-size 0.074 to 0.080 (line 344). Acceptance: at 1:1 in `_icons_strip_64.png`, at least 2 dark px touch the upper-left long side of the lime.
5. **T5 snort (idle):** head toss 8 to 10 deg (line 543, `8.0 * sn` to `10.0 * sn`). Acceptance: idle head pitch-up stays at 30 or less (about 9.5 expected).
6. **T2 horn zig (model, owner call):** line 383 thickness 0.013 to 0.017. Judge against ThunderBull in the 64 px strip.
7. **T3 nose cap (model):** front nose ring line 323, y -1.727 to -1.723.

---------------------------------------------------------------------------------------------------------------------
## 6. Pass / fail checklist (round 6)

| item | result |
|---|---|
| Model 8.5 floor | PASS (8.5) |
| idle clip | PASS (8.5) |
| walk clip | PASS (8.6) |
| roar clip | PASS (8.6) |
| act_horntap clip | PASS (8.6) |
| MUST 1 roar mouth (33 / 51 px, f0 = 0, closed = 0) | PASS |
| MUST 2 act from below (brisket unbroken) | PASS |
| MUST 3 walk reference (elephants tag, cited times) | PASS |
| Limits, end at rest, ground, feet at taps | PASS |
| Tris 14,532, glow {}, collision_free | PASS |
| TO 9+ T1, T2, T3, T5, T6, T8 | OPEN (not blocking) |
