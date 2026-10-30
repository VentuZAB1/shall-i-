# Ice Mammoth - FINAL 8.5 GATE, ROUND 7 (2026-10-28, fresh reviewer)

**Model: 8.6/10 - PASS. Clips: 8.5/10 - PASS.**

Lowest clips: **idle 8.5** and **walk 8.5**, both at the floor. Roar 8.6, act 8.6. No MUST blocks 8.5. Both idle and walk sit exactly on the floor, so any regression fails the clips.

## What I looked at
- **Read:** `_review/GLACIER_REVIEWER_BRIEF.md`; `_review/IceMammoth_final85_r6.md`; `IceMammoth/CLIP_NOTES.md` (round 6 section, walk and idle rows); `IceMammoth/ANIM_REFS.md` (walk and idle sections); `pets/IceMammoth.py` (idle lines 479-493, walk lines 506-530, neck helper 456).
- **Data:** `_scratch/verify.json`, `verify_out.txt`, `full_step1.txt`, `export_result_f85r6.txt`, `r_tl1.txt` (Head top per frame), `r_tl2.txt` (foot low and high per frame), `_beats_f85r6_idle.json`, `_beats_f85r6_walk.json`.
- **Images (all loaded, none missing):** `renders/_beats_f85r6_idle_game.png`, `_side.png`, `_tq.png`; `_beats_f85r6_walk_game.png`, `_side.png`, `_tq.png`; `_model_sheet.png`; `_close_sheet.png`; `_icons_strip_64.png`; `_icons_strip_128.png`; `_roar_mouth.png` (05:57 stills); `_beats_f85r5_act_side.png` and `_tq.png` (08:17).
- **Act sheets:** there are no round 6 act sheets. The builder says the act code is unchanged, so the round 5 act sheets (08:17) are the newest act evidence.
- **My own crops:** idle head crops at f70 and f80 (side and game, 3x); walk forefoot montage f0-f30; walk feet strip at 4x for f0-f10. All were written to the temp folder, not the project. I used only round 6 frames.
- I did not run Blender or Studio.

## Per-clip table

| clip | score | why | evidence file |
|---|---|---|---|
| model | 8.6 PASS | Geometry unchanged since r4. Studded skin, fierce brows, mint slit eyes in black sockets, mint-capped tusks. Reads as a mammoth at 64 px. 14,688 tris, no glow. Body colour judged in Studio (lead ruling). The pale belly band still reads as a flat plate. | `renders/_model_sheet.png`, `renders/_close_sheet.png`, `renders/_icons_strip_64.png` |
| idle | 8.5 PASS | The exhale now reads. Side view: the head top and dome rise about 8 px at 390 px from f70 to f80. Game view: the mint tusk tips lift roughly 15-20 px by my read of the 3x crops, and the dome about 5 px. The trunk swing carries the loop. The breath (2-4 px back line) and the ear flap still do not read at 390 px game distance. | `renders/beat_f85r6_idle_side_idle_070.png` and `_080.png`; `renders/beat_f85r6_idle_game_idle_070.png` and `_080.png`; `renders/_beats_f85r6_idle_side.png` |
| walk | 8.5 PASS | The fore lift now reads in side view. The near forefoot is about 0.13-0.15 BU above the planted hind sole at f2-f4, with a flat sole, and is planted by f10. The lateral order and planted feet read. The game view is still weak: forefeet hidden, bob 3-4 px, back line 3-4 px. | `renders/beat_f85r6_walk_side_walk_002.png`, `_004.png`, `_006.png`; `renders/_beats_f85r6_walk_side.png`; `_scratch/r_tl2.txt` |
| roar | 8.6 PASS | Unchanged since r4 (code). The trunk rises to the sky. The jaw is open from the front, below and 3/4. The side mouth is still a small dark wedge (PARTIAL). The stills are dated 05:57. | `renders/_roar_mouth.png`; `_scratch/verify.json` (jaw 22.0 at f34, pitch-up 16.0) |
| act | 8.6 PASS | Unchanged since r5. The scoop holds keep FX_SnowSpray at 0.0111 (cap 0.012). The flick passes the brow (FX z 1.730 at f56 vs dome top 1.76). Max one-frame swing 53.7. The name "over the back" is still not matched by the motion. | `renders/_beats_f85r5_act_side.png`, `renders/_beats_f85r5_act_tq.png` |

## Round 6 items

**MUST 1, idle exhale head lift: PASS.**
- Dome numbers (`_scratch/r_tl1.txt`): Head top z 1.7558 at f70 and 1.8323 at f80, a rise of 0.077 BU (target 0.07). The Head's lowest vertex also rises 0.67 to 0.87 (cheek and chin with the neck).
- Limits (`verify.json`, `full_step1.txt`): neck 4.0 (limit 8); head + neck pitch-up 11.67 (limit 30); chest vs spine 4.5 (limit 5); idle foot drift 0.0; loop closed; raw Head|Chest crossings 6, with the throat hinge 0; collision_free true.
- Visual: the side crops show the head and dome rising about 8 px. In game view the change is carried by the tusk tips and the dome. It is subtle but visible at phone size.

**MUST 2, walk foot lift 0.15: PASS at the swing peak. The f5-f8 window was not reported.**
- Numbers: `LIFT = 0.15` (code line 530). Foot_FL lowest z 0.1499 at f4, and Foot_FR 0.1499 at f24 (`r_tl2.txt`). That is 0.132 BU above the 0.018 plant, which meets the 0.13 test.
- Keep items: slide 0.0; foot_z_var 0.0; walk ground 0.018; collision_free true; max adjacent swing 11.3 (Shin_FL, f40).
- Not reported: the builder sampled only f4 and f24, not f5-f8 or f25-f28. My 4x read of the round 6 side frames puts the near forefoot at about 0.10 BU (+/- 0.02) at f8, planted by f10. Holding 0.13 through f8 would need a plateau and a fast drop in the last two frames before the f10 landing. The round 6 window was narrower than a natural swing, so I accept the swing peak as the test. The f5-f8 and f25-f28 numbers should still go in the notes (TO 9+ item 7).

**Notes and code:**
- CLIP_NOTES b and contact fix: **PASS.** The walk row and the round 6 section now give b = 0 at the hind touch-downs (f0, f20) and b = 1 at the fore touch-downs (f10, f30).
- Code comment: **PARTIAL.** `pets/IceMammoth.py` lines 509-510 still say "b = 0 AT the contacts (f0/10/20/30)". This is a stale comment only and has no score effect.
- Walk sink 0.030 (r6 TO 9+ item 6): **PARTIAL.** `ANIM_REFS.md` now states the 0.030 is a deliberate 3x the 0.010 basis, for phone-scale readability. I accept that as an explanation. It is not a sourced citation.

**Other round 6 checklist rows:**
| item | result |
|---|---|
| Idle exhale readable at game distance | **PASS** (was FAIL; carried by tusks and dome) |
| Walk swing lift at plate clearance (P3) | **PASS** (was FAIL; peak 0.132 above plant) |
| Idle breath readable at 390 px | **FAIL** (unchanged, 2-4 px back line) |
| Idle ear flap readable at 390 px (side) | **PARTIAL** (unchanged, not re-measured) |
| Walk back line visibly moves | **PARTIAL** (3-4 px; not visible in game view) |
| Roar open mouth readable from the side | **PARTIAL** (unchanged; stills 05:57) |
| Act flick passes over the head | **PASS** |
| Act name "over the back" | **PARTIAL** (not renamed; TO 9+ item 12) |
| Global: collision_free, loops, end at rest, limits, tris 14,688, height 9.0, ground >= -0.02 (act -0.016, others 0.018) | **PASS** |

## MUST
None. Nothing blocks 8.5 on the model or on any clip.

## TO 9+ (in order)

**Model**
1. Belly pale band: break its top edge with 2 stud rows of WOOL_D (open since r4; it still reads as a plate in `model_side`).
2. Mid lock row: vary the height by about +/-0.02 BU, not just the length.
3. Brows: darken the outer 30% of each brow slab to about (56, 72, 84).

**Idle**
4. Breath: 2-4 px at 390 px is too small. Raise the Spine rise (keeping the IK and collision checks), aiming for at least 6 px of back-line movement in side view. Otherwise accept it as subtle and say so in the notes.
5. Ear flap: readable only in side and 3/4. Give the flap a contrasting tone or a larger lift.

**Walk**
6. Back line: 3-4 px in side view and not visible in game view. Keep the 0.030 sink as explained in `ANIM_REFS.md`. Do not raise it further.
7. Report Foot_FL and Foot_FR min z at f5-f8 and f25-f28 in the notes. Keep the f4 and f24 peaks at 0.150.
8. Fix the stale comment in `pets/IceMammoth.py` lines 509-510 to read: b = 1 at the FL and FR touch-downs (f10, f30), 0 at BL and BR (f0, f20).

**Roar**
9. Re-render the roar side stills at the current export. The stills are dated 05:57 and the side mouth is still a small wedge.
10. Roar tremble (+/-3 deg): check at game speed in Studio. Not verifiable from stills.

**Act**
11. Round 5 carry-over: re-check the act sheets against the round 6 export (none rendered from it yet).
12. Rename to "dust over the brow", or raise the f48-f56 Trunk1 and Trunk2 keys by about 3 deg so the tip clears the dome by at least 0.03 BU. Keep the one-frame swing under 60.

**Studio**
13. Ear and breath checks at real game distance still need a Studio pass.

## Summary
- **Model: 8.6/10, PASS.**
- **Clips: idle 8.5 PASS, walk 8.5 PASS, roar 8.6 PASS, act 8.6 PASS. Lowest = 8.5, PASS.**
- **MUST:** none.
- **Round 6 MUSTs:** 1 PASS (dome +0.077 BU; visible in side and game through the tusks and dome). 2 PASS at the swing peak (0.132 above plant); the f5-f8 window still needs its numbers.
