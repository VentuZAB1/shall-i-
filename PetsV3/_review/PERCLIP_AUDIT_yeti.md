# Glacier Yeti - PER-CLIP AUDIT (lowest clip score rule), 2026-10-28, fresh auditor

Owner floor 8.5 applies to EVERY clip. Clips score = lowest per-clip score.
Base for evidence files: `PetsV3\GlacierYeti\renders\` (numbers in `PetsV3\GlacierYeti\_scratch\verify.json`).

**Lowest clip score: 8.1 (idle). FAILS the 8.5 floor. Walk 8.6, roar 8.6, act_skid 8.6.**

## Table

| clip | score /10 | why (one line) | evidence file |
|---|---|---|---|
| idle (120 f loop) | **8.1** | Head dip f65-75 reads, but the body is nearly static at phone scale: plate settle max adjacent-frame swing only 3.2 deg, breath 3.5 deg. No animationreference.org clip is cited for the idle (ANIM_REFS gives only Muybridge Q4 for "stillness"). | `_beats_f85r2_ir_tq.png`, `_beats_f85r2_ir_side.png`, `beat_f85r2_ir_side_idle_000.png` vs `beat_f85r2_ir_side_idle_075.png` (03:57; motion valid, model look is pre-05:22) |
| walk (48 f loop) | **8.6** | Diagonal knuckle walk reads (measured LH f0, RF f12, RH f24, LF f36), fists plant, hunched; slide 0, loop closed. Chest vs spine 4.61 is 92 % of its limit. Cites Dragon Walk Cycle + Muybridge 747. | `_beats_f85r3_ws_tq.png`, `_beats_f85r3_ws_side.png` (05:25; walk keys unchanged since round 1, motion valid) |
| roar (60 f) | **8.6** | Shoulder heave, head lift and late jaw open (26 deg at f32) all read; no head shake, settles to rest. Neck 7.69 is 96 % of the <=8 limit, so the margin is thin. | `_beats_f85r2_ir_tq.png`, `_beats_f85r2_ir_side.png`, `beat_f85r2_ir_tq_roar_022.png`, `beat_f85r2_ir_side_roar_022.png` (03:57); `pclose_side_roar_30.png`, `pclose_front_roar_30.png` (05:21, mouth cavity) |
| act_skid (100 f, signature) | **8.6** | Drop, sled sweep, hard brake at f58, push-up and gasp, exact rest (0.234 deg). Max swing 9.4 deg, head joint 10.56, neck 5.44, all under limits. The f16-34 sled sweep reads softly at phone size. | `_beats_f85r3_ws_tq.png`, `_beats_f85r3_ws_side.png` (05:25); `beat_f85r3_ws_tq_act_skid_058.png`, `beat_f85r3_ws_side_act_skid_058.png` (05:21-22) |

## Fix to reach 8.5 for IDLE (all keys measurable; re-run `headless_full` step 1)

1. **Plate settle:** Plate_L and Plate_R keys at f35 and f45 from 9 deg to **13 deg**. Predicted max adjacent-frame swing 3.2 x 13/9 = about 4.6 deg (target >= 4.0). Must stay collision-free vs Head, Neck, Arm_L, Arm_R, Chest.
2. **Head drop:** f65 and f75 from 9 deg to **11 deg** (the round-3 suggestion). Predicted Head joint local about 7.7 deg (6.35 x 11/9; target >= 7.5 at f75). Neck about 4.0 (limit 8). Head pitch-up is unaffected (2.92). Head|Chest raw crossings are absorbed by the sleeve hinge (slide up to 0.05); if step 1 shows any collision, drop back to 10.
3. **Chest breath:** 3.5 deg to **4.2 deg**. Predicted chest vs spine about 4.5 (today 3.79; must stay <= 5). Hip yaw stays at 5 so idle foot drift stays 0.
4. **Reference (ANIM_REFS rule):** add one animationreference.org clip for the idle (a heavy creature settle or breath), cite the frames used, and map the f35-75 settle and head dip to it. This is documentation, but the rule requires it.

Gate for the next review: idle max adjacent-frame swing >= 4.0 deg; Head local at f75 >= 7.5 deg; chest vs spine <= 5; neck <= 8; head + neck pitch-up <= 30; `collision_free` true; ground_min_z >= -0.02; idle loop closed (end vs start 0). Re-render the idle beat sheet at f0 / 30 / 45 / 65 / 75 / 100 (side and tq) for the visual check.

Not part of the 8.1 score: the roar neck margin (7.69 vs 8) is a risk, not a fail. Do not add head motion to the roar.

## Not scored (per lead rulings)
- 5-stud readability and the live idle-to-walk cross-fade: Studio checks, lead's job.
- Look-turn doubling (`look * 0.5` on Neck and Head): capped in Studio.
- `renders\_xfade_sheet.png` (01:14) was opened, but it predates the round-2 idle keys, so it is not used for any score.

## Sheet provenance
- idle and roar: `_beats_f85r2_ir_*` (03:57). Motion valid. The fangs and fist plates are pre-05:22, so the look is stale, not the motion.
- walk and act_skid: `_beats_f85r3_ws_*` (05:22-05:25). These supersede `_beats_f85r2_ws_*`, which were not needed.
- close-ups (fangs, mouth): `pclose_*` (05:21), current model.
- Images that failed to load: none.
