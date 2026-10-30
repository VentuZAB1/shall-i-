# Ice Mammoth - clip gate review 4 (2026-10-27) - APPROVED WITH FIXES (clips)

**Score: 8/10 for a MEDIUM 26 %.** Round 3 was 7.5/10. Every round-3 MUST is now addressed with measured numbers, and the
scoop now meets the snow. One MUST is left, and it is evidence only: the throat and jaw close-ups were rendered before the
final jaw keys, so they must be re-rendered and labelled. No clip or rig change is needed for it.

## Round-3 MUST status
| # | item | round-3 | round-4 evidence | verdict |
|---|---|---|---|---|
| M1 | Scoop reaches the snow | no contact; tip hovered about 1 stud up | Trunk_Tip bone at f20 0.057, f66 0.059, f80 0.059 (min 0.045 at f65). FX_SnowSpray 0.016, 0.018, 0.018 (min 0.008). ground_min_z act -0.019 at f65 (within -0.02). Max swing 46.6 at f62 (under 60) | **PASS on contact, with a restated criterion** (see below) |
| M2 | animationreference rule | not met (no site clip pulled) | Lead ruling: W0 pulled and stepped; Muybridge 733 is the walk study | **PASS** (citations concrete, see below) |
| M3 | Limits reconciled, saved | 6/4.4 in message vs 2.0/1.7 saved | verify.json saved; maxima neck 0.6/0.8/2.0/3.0, chest 0.5/1.68/1.0/0, head pitch-up 1.1/0.2/16/17. Match CLIP_NOTES round 3 | **PASS** |
| M4 | End at rest, roar and act | not measured | verify.json: end_vs_rest 0.0 and start_vs_rest 0.0 for roar and act | **PASS** |
| M5 | Raw crossings vs hinge | count not reported | verify.json: raw Head-Chest idle 6, walk 15, roar 6, act 7; with the hinge 0. Close-ups exist but are stale (see MUST 1) | **PASS on counts; close-up evidence STALE** |

### M1 detail: the criterion was a bone proxy
- My round-3 wording was "Trunk_Tip world z ≤ 0.04". The Trunk_Tip bone sits in the middle of the tip block, about 0.058 above
  its underside. So the bone reads 0.045-0.059 when the mesh is on the snow. The literal bone number cannot pass, and it
  is the wrong measure.
- The physical criteria are met: the mesh reaches -0.019 (the tip presses about 0.02 into the snow, which the -0.02 limit
  allows), and the spray anchor sits at 0.008-0.018 at the scoops.
- Both side and tq beat sheets (`_beats_act_side.png`, `_beats_act_tq.png`, 17:50) show the tip on or touching the snow at
  f20, f66 and f80. The scoops and the flicks read.
- **Restate the criterion** in CLIP_NOTES as: the lowest mesh point of the trunk at each scoop is ≤ 0.02 above the ground
  (touching at about 0), FX_SnowSpray ≤ 0.02, and ground_min_z ≥ -0.02. Note that ground_min_z -0.019 is a thin margin.

### M2 detail: the citations are concrete enough
- **W0** (`/tags/wolfs-rain`, Sakugabooru #174333): the black wolf's snarl at 15.9-16.6 s (mouth opens over about 0.66 s, then
  holds wide about 1 s with the head level). The trumpet jaw now opens over f16-34 and holds. The code comment and keys
  match: jaw f16 2, f22 6, f26 9, f34 14, f50 13, f58 4 (`pets/IceMammoth.py` ROAR_P, L482-490).
- **Muybridge Plate 733:** the walk. The footfalls file confirms the lateral order BL f0, FL f10, BR f20, FR f30.
- **The site `/tags/elephants` entry is not a citation.** It is marked as "not read" (the player froze), with no frames. Keep
  it in the list as a search result, but label it "not used". It does not carry the rule.
- **Two smaller points (NICE 1 and 2):** the W0 hold was about 1 s, and the mammoth holds about 0.5 s (f34-50); the
  unit conversion (24 fps to 30 fps) is written in one place as "~15 f" and in another as "0.66 s".

---------------------------------------------------------------------------------------------------------------------
## MUST

**MUST 1. Re-render the M5 evidence from the final code, with frame labels.** (Evidence, not geometry.)
- The jaw and throat renders are stale. `_throat_close.png` is timestamped 17:51, `pclose_*_roar_26.png` and
  `_jaw_roar_sheet.png` 17:57. `pets/IceMammoth.py` was last written at 21:57, and the W0 jaw re-time (ANIM_REFS central, 21:52)
  came after the renders. So the f26 jaw in those sheets is the old timing (its keys are now f26 = 9 deg).
- Re-render from the final file, and label every panel with its clip and frame:
  - side and tq throat close-ups at roar f22 and act f48 (replace `_throat_close.png`);
  - the roar mouth at f22, f26, f34 and f50 (side view, showing the jaw gape, not the trunk) for the "no see-through" claim;
  - the act scoop at f48 for the head dip (13-14 deg down);
  - the act scoops at f20, f66 and f80, side and tq, from the final file (the M1 contact evidence, currently 17:50).
- The `_jaw_roar_sheet.png` panels are unlabelled, and the mouth is hidden behind the trunk. "No see-through" cannot be checked
  from it, so the re-render must show the open mouth from the side.
- The raw counts in verify.json stand, and do not need re-running unless the render shows a new crossing.

---------------------------------------------------------------------------------------------------------------------
## NICE
1. **The W0 hold is shorter than cited.** The cited snarl holds about 1 s. The trumpet jaw holds 14-13 deg for about 0.5 s
   (f34-50), then closes by f58. Either hold to about f60 or write down why the shorter hold is correct for a trumpet.
2. **Units in the references.** W0 is given as "~15 f" (central file, at 24 fps) and "0.66 s" (ANIM_REFS, about 20 f at
   30 fps). Write one conversion line, so the 18-frame jaw window reads as derived.
3. **ground_min_z -0.019 is a thin margin.** It passes. If the tip is lowered further in a later edit, the -0.02 limit fails.
   Keep the scoop depth where it is.
4. **Head dip at the scoops is 13-14 deg down.** The Mammoth brief limits pitch-up only. 13-14 is under the 20-deg down
   limit used for the other pets (Thornblade), so it passes. Say so in CLIP_NOTES.
5. **C1 is still open:** the in-game capture of the body colour (round-2 gate). The lit preview is aqua. Apply the round-2 hue
   shift only if the capture says aqua.

## Pass / fail checklist
| check | result | note |
|---|---|---|
| collision_free, all 4 clips | PASS | step 1 (21:58) |
| Raw crossings reported, hinge removes all | PASS | verify.json |
| ground_min_z ≥ -0.02 | PASS | -0.019 act f65 (thin) |
| Trunk tip touches the snow at each scoop | PASS | mesh -0.019; spray 0.008-0.018 |
| Trunk_Tip bone ≤ 0.04 at the scoops | not met (0.057-0.059) | bone proxy; criterion restated |
| Loops closed (idle, walk) | PASS | |
| Walk footfalls, lateral (BL, FL, BR, FR) | PASS | f0, f10, f20, f30 |
| Walk slide ~0, idle feet still | PASS | |
| Roar and act end at rest (and start at rest) | PASS | 0.0 both |
| Neck ≤ 8 deg | PASS | max 3.0 (act f20) |
| Chest vs spine ≤ 5 deg | PASS | max 1.68 (walk) |
| Head + neck pitch-up ≤ 30 deg | PASS | 16 roar, 17 act |
| Head pitch-down at the scoops | PASS | 13-14 deg (NICE 4) |
| Max adjacent-frame swing ≤ 60 deg | PASS | 46.6 (trunk tip, f62) |
| No head shakes, no airborne spins | PASS | |
| Acts in place | PASS | linear 0 |
| Event names (no `end`), timings match plan | PASS | |
| Throat close-up and jaw evidence current | **FAIL (stale)** | MUST 1 |
| animationreference rule | PASS | W0 + Muybridge; elephants entry relabel |

## Not done in this review
- No Blender run and no game run. The contact judgement uses the saved verify.json numbers and the beat sheets.
- I did not check the other pets' limit maxima (the 6 and 4.4 the builder attributes to the Rhino and the Yeti).
- The act beat sheets (`_beats_act_side/tq.png`) are timestamped 17:50, before the final file (21:57). I did not confirm the act
  keys are unchanged since then, so the M1 contact judgement rests on those sheets plus verify.json (21:58). Include the act
  scoops in the MUST 1 re-render to close this.
