# Frostfang Lynx - clip gate sign-off check, review 4 (2026-10-27)

## Verdict: SIGN-OFF
**Score: 8/10** for the clip gate (7/10 at review 3). No MUST remains. The NICE items below can ship as they are.

## Timestamps (renders and clips are newer than the last source edit)
- `pets/FrostfangLynx.py`: 17:26:46 (last edit).
- `renders/crop_front_throat.png`, `crop_tq_throat.png`, `low_below.png`: 17:43:03-17:43:06. **After** the source edit.
- `FrostfangLynx.json` / `.lua`: 17:42:56. After the source edit.
- `_scratch/fullcheck.json`: 17:42:47. `_scratch/clipmetrics.json`: 17:42:51.

## M1 (throat): PASS
- The throat is now a narrow studded strip (half-width 0.045) with four SNOW fur tufts (line 141-143). It is no longer a plate.
- Front (`crop_front_throat.png`): the strip reads as fur with tufts, not a slab.
- Side/tq (`crop_tq_throat.png`): the strip is slim, and the tufts break its outline.
- Below (`low_below.png`): no flat plate under the chin. Pass.
- NICE: the tuft tips are sharp (top 0.15-0.45). At tq close-up they read as a second row of white teeth under the jaw. Round them (top about 0.35-0.6) if you touch the code again.

## M2 (claws): PASS
- Each front claw has its own bone now (`Claw_FL1-4`, `Claw_FR1-4`, under `Claw_FL` / `Claw_FR`). The rest pose is unchanged (`claw_zoom.png` panel 1: four distinct claws).
- Open (`claw_zoom.png` panels 2-3, `claw_paw3.png`): the claws spread into a fan of separate cyan wedges across the toe, not one plank. Pass.
- My decode of the tracks: each parent claw bone opens 39 deg max; the centre children add about +6 deg and the outer children about -8 deg, with a yaw fan of +/-6 deg (centre) and +/-18 deg (outer). The notes say 41 deg centre and 27 deg outer. The totals are a few degrees different, but the order (centre opens more, outers splay wider) and the visible result match. Not a blocker.

## Idle frame 0: PASS
- Ear_L, Ear_R, Head, Neck, Tail3 are exactly 0.0 deg at frame 0 (decode). The ear offset is gone.
- Jaw is 1.0 deg open at frame 0 and at the end of the act (f96). Harmless, but the act claims "exact rest". NICE: zero the Jaw in the rest frames.

## Pose limits and loops (my decode matches `clipmetrics.json`)

| clip | neck max | chest vs spine | head pitch-up | quat flips | loop seam | result |
|---|---|---|---|---|---|---|
| idle | 5.6 | 0.6 | 0.4 | 0 | 0.8 deg (Shin) | PASS |
| walk | 2.0 | 2.7 | 0.6 | 0 | 10.9 deg (Foot_FR), a normal frame step | PASS |
| roar | 4.0 | 2.0 | 0.0 | 0 | n/a (no loop) | PASS |
| act_clawflex | 7.0 | 2.1 | 1.6 | 0 | n/a | PASS |

- Limits: neck <= 8, chest vs spine <= 5, head+neck pitch-up <= 30. All pass.
- Per-frame swing: `clipmetrics.json` reports the largest single-limb step as 7.8 deg (walk, Shin_FL) and 11.7 deg (act, Claw_FR2). My decode of the raw bone-local quaternions gives 12.4 deg (walk, Shin_FR frame 6) and 8.4 deg (act, Claw_FR). The two metrics measure different things (world limb vs local bone). Both are far below the ~60 deg limit. NICE: write the metric definition into `clipmetrics.json` so the numbers can be compared.

## Refs (ANIM_REFS): ACCEPTED
- L0 (animationreference.org, `/tags/the-cat-returns`, Sakugabooru #256671) is added. It covers the walk (a steady head and a cat walk cycle) and the act crouch. This meets the owner rule for the walk and the crouch. I accept the citation as written (I could not open the site from here).
- NICE: the Mapping section still says "8 f apart" and "35 deg" for the claw flex. The build uses a 12 f lag and the new fan angles. Update those two lines.

## Remaining NICE (none blocks ship)
1. Round the throat tuft tips (M1 NICE).
2. Zero the Jaw in the idle frame 0 and the act end frame (1 deg).
3. Update the ANIM_REFS mapping lines for the 12 f lag and the new claw angles.
4. Add the swing-metric definition to `clipmetrics.json`.

Verdict: **SIGN-OFF, 8/10.** The model and the clips are ready for the owner's look.
