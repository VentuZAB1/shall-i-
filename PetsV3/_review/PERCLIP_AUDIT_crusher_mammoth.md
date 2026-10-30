# Per-clip audit: Coral Crusher and Ice Mammoth (Glacier, 2026-10-28)

Fresh auditor. Lead ruling applied: the 8.5 floor applies to EVERY clip, and the clips score is the LOWEST per-clip score.

Not counted (lead rulings): crab pale underside, crab walk timing, Mammoth colour (judged in Studio), VFX added in Studio, walk speed skating in game.

Files read: `_review/GLACIER_REVIEWER_BRIEF.md`; Crusher `_review/CoralCrusher_final85_r3/r4/r5.md` and `CoralCrusher/CLIP_NOTES.md`; Mammoth `_review/IceMammoth_final85_r3/r4.md` and `IceMammoth/CLIP_NOTES.md`.

Images: all opened, none failed to load. Base folders: `PetsV3\CoralCrusher\renders\` and `PetsV3\IceMammoth\renders\`.

---

## Coral Crusher

**Lowest clip: WALK 8.4 (under the 8.5 floor).**

| clip | score /10 | one line why | evidence file |
|---|---|---|---|
| idle | 8.6 | The guard lift is clear at f62 against f45 and f80, and the breath reads in the sheet. The eyestalk swivel and the f70 tap are not readable at phone size. | `_beats2x_idle.png` (04:40); `pose_tq_idle_45`, `_62`, `_80` (05:24) |
| walk | 8.4 | Leg alternation and claw sway show only in crops and close stills. Body motion from f0 to f27 in the game strip is small, so at phone size it reads as a static pose with legs moving. Walk timing not counted. | `pose_tq_walk_08` (05:24); `_walk_sway_strip.png` (03:47; walk keys unchanged since, per CLIP_NOTES) |
| roar | 8.7 | Both claws are up in a clack threat with the mandibles open. It reads from the tq and game views at f22 and the clacks at f22 / 30 / 38 are readable. | `pose_tq_roar_22`, `_14`, `_38` (05:24) |
| act (semaphore wave) | 8.8 | From the game camera the top (f30) and trough (f41) are clearly different, with three holds and exact rest at f110. The eye follow is a secondary read. | `_wave_strip.png` (04:44); `eyA_game_act_semaphore_41.png` (05:19); `pose_tq_act_semaphore_30` (05:24) |

Evidence freshness: all four Crusher clips have current 05:24 sheets, so none is marked stale.

**Fix to reach 8.5 on WALK (edit `pets/CoralCrusher.py`, walk block):**
- Raise the leg lift from 0.07 to 0.10 BU (about 40 %).
- Raise the carapace bob from 0.010 to 0.016 BU.
- Keep the claw sway at 6 deg, duty 0.55, stride 0.309, walk slide at or below 0.002, foot drift 0, `collision_free` true, loop closed.
- Check: re-render the game walk strip f0 to f9 and confirm the body and leg tips move visibly (at least 4 px in the 390 px frame) between the two contacts.

---

## Ice Mammoth

**Lowest clip: IDLE 8.3 (under the floor). WALK 8.4 is also under.**

Evidence freshness: the Mammoth idle and walk sheets are `_beats_f85r2_irw_*` (03:50), which is before the 04:42 export. The round-3 notes list no idle or walk key changes, so both are marked **evidence stale**. The roar body sheet is also 03:50 (jaw 20; now 22), but the mouth close-ups are current (04:40 and 04:41). The act sheets are current (04:40 and 04:41).

| clip | score /10 | one line why | evidence file |
|---|---|---|---|
| idle | 8.3 | The trunk swing shows in the side and tq sheets. The f40 ear flap and the 2.0 deg chest breath are not visible at sheet scale, so two of the three secondary beats do not read. Evidence stale. | `beat_f85r2_irw_side_idle_000` to `_100` and `_beats_f85r2_irw_side.png` (03:50); `_beats_f85r2_irw_tq.png` (03:50) |
| walk | 8.4 | Feet step in sequence and the stance changes frame to frame in side view. Body and trunk move little (trunk about 3 deg a step, body roll ±1.5 deg), so it reads as a stiff walk at phone size. Evidence stale. | `_beats_f85r2_irw_side.png` (walk f0 to f30, 03:50); `_beats_f85r2_irw_tq.png` (03:50) |
| roar | 8.6 | The trunk rises to the sky by f16 and holds f22 to f50, so the trumpet reads. From the front and below the dark mouth interior is clear. From the side the dark band is visible but partly covered by the tusk root. Body beats are stale (jaw 20). | `pclose_side_roar_34.png` (04:40); `_roar_mouth.png` (04:41); `_beats_f85r2_irw_side.png` roar f0 to f66 (03:50) |
| act (dust-over) | 8.6 | Scoops reach the snow (tip on the ground at f18 to f22, f64 to f68, f78 to f82). The flick arches over the head from f44 to f58 in side view. The flick peaks at the top of the head, not over the back the act name implies. | `_beats_f85r3_act_side.png`, `_beats_f85r3_act_tq.png` (04:41); `beat_f85r3_act_side_act_dustover_056.png` (04:40) |

**Fix to reach 8.5 on IDLE (edit `pets/IceMammoth.py`, idle block):**
- Ear flap at f40: 10 deg to 13 deg.
- Chest breath: 2.0 deg to 3.0 deg (still within the 5 deg limit).
- Trunk tip roll amplitudes: (2.7, 4.0, 4.7, 4.7) to (3.2, 4.8, 5.6, 5.6), which takes the tip from ±16 to about ±19 deg.
- Keep neck at or under 8 deg, chest vs spine at or under 5 deg, `collision_free` true, loop closed, idle foot drift 0.
- Check: the headless probe shows trunk tip travel between f0 and f20 of at least 0.25 BU, and the f40 ear flap is visible in a side render at 390 px.

**Fix to reach 8.5 on WALK (edit `pets/IceMammoth.py`, walk block):**
- Trunk swing per step: about 3 deg to about 6 deg.
- Body roll: ±1.5 deg to ±2.5 deg, keeping its phase on the planted side.
- Keep stride 0.319, walk slide 0.0, loop closed, `collision_free` true, neck at or under 8 deg, chest vs spine at or under 5 deg.
- Check: side render f10 against f20 shows trunk tip travel of at least 0.2 BU and a visible level change in the back line.

**Process MUST (both Mammoth idle and walk):** re-render the idle and walk beat sheets (side and tq, f0 to f100 / f0 to f30) at the 04:42 export state before the lead rules on them. The scores above may move once the stale evidence is replaced.

**Roar and act: pass at 8.6, no MUST.** NICE only: move `MOUTH_IN` about 0.01 further back so the side opening shows past the tusk root (roar); the act flick could reach the back line if the name is kept (optional).

---

## Pass / fail checklist (per clip)

| check | Crusher | Mammoth |
|---|---|---|
| Idle, every clip scores 8.5 or above | PASS on idle (8.6), FAIL on walk (8.4) | FAIL on idle (8.3), FAIL on walk (8.4) |
| Roar, every clip scores 8.5 or above | PASS (8.7) | PASS (8.6) |
| Act, every clip scores 8.5 or above | PASS (8.8) | PASS (8.6) |
| Current evidence for every clip | PASS (all 05:24 or 04:44) | FAIL on idle and walk (03:50, stale) |
| Numbers from the notes (collision, ground, loops, slide, limits) | PASS (per r5: collision_free true, ground -0.013, slide 0.002, rest exact f110 to f120) | PASS (per r4: collision_free true, neck max 3.0, chest vs spine max 2.0, pitch-up max 17, max swing 53.7) |

---

## Summary

- **Coral Crusher, per clip:** idle 8.6, walk 8.4, roar 8.7, act 8.8. Lowest: walk 8.4 (below the floor).
- **Ice Mammoth, per clip:** idle 8.3, walk 8.4, roar 8.6, act 8.6. Lowest: idle 8.3 (below the floor; walk also below).
- **Evidence:** all Crusher clips are current. Mammoth idle and walk are stale (03:50 sheets, before the 04:42 export) and need re-renders before a final ruling.
- **Result:** neither pet clears the per-clip floor on the evidence. The earlier "clips 8.5" (Crusher) and "clips 8.6" (Mammoth) were single scores, not per-clip.
