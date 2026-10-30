**Model: 8.5/10 - PASS. Clips: 8.7/10 - PASS.**

# Wraith Hound - FINAL 8.5 GATE, round 5 (9+ check on the r8 build) - 2026-10-28

Model holds at 8.5. The round-8 polish landed the icon luminance and the knee-step clip fixes, and the eye count reproduces. The accent split was skipped on purpose, so 9+ is not reached on the model. The close-up eye lost its black socket frame, which is a minor regression with a cheap fix (below). Clips close every NICE item from round 4 and have no breaches.

## What I looked at
- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round 4 `_review/WraithHound_final85_r4.md` ("Still between this pet and 9+"); builder `WraithHound/MODEL_NOTES.md` and `CLIP_NOTES.md` (Round 8 sections).
- Live pet file `PetsV3/pets/WraithHound.py` (saved 05:21) is identical to `WraithHound/_scratch/WraithHound_r8.py` (05:25).
- Renders: the 05:23 set (`renders/_icons_strip_64.png`, `_icons_strip_128.png`, `close_front.png`, `close_side.png`, `_model_sheet.png`), `_scratch/_game_cmp_r8.png`, `renders/_pose_tq_sheet_r8.png` (05:24), and `renders/pclose_tq_walk_00/09/18/27.png`. All opened and loaded.
- Logs and metrics: `_scratch/export.log` (05:25), `fc_r8.txt` and `fullcheck.json` (05:23), `clipmetrics.json` (05:17), `ANIM_REFS.md` (05:28).
- My own measurements (PIL is not installed here, so I used a numpy PNG reader; scripts and zooms are in `C:\Users\ventu\AppData\Local\Temp\wh_r5\`). Eye boxes, indigo components, mean Y, nearest-palette shares on the flat renders, 8x and 16x zooms. I did not run Blender or Studio and edited no files.
- Comparator caveat: `_scratch/strip64_pass85.png` and `strip128_pass85.png` are the state BEFORE round 7 (ASH_LAV 170,160,206; rim 0.020), not the round-7 state. My before/after deltas therefore span round 7 and round 8. The builder's round-7 numbers are quoted where they differ.
- Timing caveat: the swing metrics come from 05:17, and the pet file was last saved at 05:21. The notes say only the Mane2 tip width changed after that, and the 05:23 full check and 05:25 export audit agree (walk 36 f, collision-free, ground 0.004, loops closed).

## Round-4 9+ items
1. **Eye at 64 px: LANDED on the agreed mask.** The loose mask (b-r > 70 and b > 120) gives 7 px at 64 (target 6; pass85 2, round 7 3) and 21 px at 128 (target 16; pass85 9, round 7 13). I reproduced the builder's numbers exactly. Caveat: the saturated core (b-r > 100 and b-g > 100) is only 3 px at 64 (pass85 0) and 13 at 128 (pass85 1). The rest of the 7 are blue-grey anti-alias halo. At 8x (`z64_old_vs_new_8x.png`) the eye reads as a point of blue; at 1x it is still a faint speck.
2. **Accent at 64 px: NOT DONE.** The builder skipped the Mane2 split on purpose (front-wing risk). The plume still has two separate blue elements at 64 px: a 54 px centre tip and a 3+2 px diagonal side streak. The third blue element is the eye (6 px). Side-tip width is back at 0.85, so the 128 px count is unchanged at 22 px.
3. **Icon luminance: LANDED.** Wraith cell mean Y is 83.3 (pass85 92.4). The white-gold sphinx (slot 5) is 92.8, so the Wraith is now below it; before it was level. Creature-only: Wraith 112.7, sphinx 139.9, spider 105.7, so the Wraith is still second-lightest but no longer level with the sphinx. Game shares by nearest palette: ASH_LAV 41.34 % (floor 40) and INDIGO 5.24 % (floor 5), both matching the notes.
4. **Close-up eye (NICE): PARTIAL.** The pupil claim is dropped, which is the item's allowed option. The slit is still 0.046 x 0.025 (1.84:1, was 1.9:1), so at close range it reads as a blue panel, not a narrow slit (`close_front` 3x crop). The black socket frame has almost gone (regression R1). The pupil block is still in the code (pet file lines 175-176) but never renders.
5. **Front crest, Mane2 side tips (round-4 WATCH): LANDED.** In the `close_front` crest crop the side tips are small and mostly hidden behind the ears. No chunky blue blocks.
6. **Clip knee steps (round-4 NICE): LANDED.** See the clips section.

## Regressions
- **R1 (minor, close-up only, must fix): the black socket frame is almost gone.** Pet file line 169 has the socket at `(0.050, 0.008, 0.030)` and the rim at `(0.049, 0.006, 0.027)` (line 171). Black now shows about 0.0005 per side in X (round 7 about 0.0025). In the close-ups the blue sits flush with only a thin dark edge. **Exact fix:** change line 169 from `(0.050, 0.008, 0.030)` to `(0.054, 0.008, 0.030)`. Leave the rim, the slit and Z unchanged. Then re-run the full check (`collision_free` must stay true, and check that the socket does not poke past the brow at line 177). Re-count the 64 px eye: it must stay at 6 or more (black adds no blue to the loose mask).
- No other regressions. No collisions and no floating or intersecting parts (`collisions` is empty, `collision_free` true). Walk and act limits are unchanged. The ASH_LAV change still reads as the Wraith, deeper and more violet (the owner's call per the lead).

## Still between this pet and 9+
1. **Accent (round-4 item 2), NOT DONE.** Split the Mane2 side tips so the plume shows three separate blue elements at 64 px. Direction: d0 x 0.40 to 0.46 on the Mane2 `_L` and `_R` side wisps only (pet file line 93-94, the `wisp(...)` call with `tipcol=INDIGO`). Re-check `close_front` for front wings, and re-count the 64 px plume (three separate blue elements) and the eye (at least 6 px). This is the change that trades against round-4 NICE 3 (no front wings).
2. **Close-up eye slit (round-4 item 4), owner call.** The slit is 1.84:1 and reads as a window. A narrower slit (ratio of about 2.5:1 or more) costs the 64 px count, so both targets may not hold together. The owner decides which wins.
3. **Pupil code.** Either delete the pupil block (pet file lines 175-176) or make it visible, so the code matches the notes. No score effect.
4. **Watch (owner's call, no fix asked).** Game shares pass only on the nearest-palette rule. On a tight 12-RGB test, ASH_LAV is 39.8 % (floor 40) and INDIGO 4.89 % (floor 5). The darker lavender is the owner's call.

## Clips: 8.7 PASS
- Knee steps (round-4 NICE): walk local max **5.49** (Foot_FR f7; was 9.06), act local max **5.54** (Shin_FL f84; was 6.76). Both under 5.63. Walk armature max 4.71 (was 5.63). Walk loop seam max 2.92 over all bones (`end.f35_vs_f0`; was 6.55). LANDED.
- Limits: walk neck 4.0 and act 5.0 (limit 8); chest vs spine walk 2.92 and act 1.5 (limit 5); head pitch-up idle 8.0 and act 3.5 (limit 30). PASS.
- Quaternion flips 0, linear 0, loops closed, walk slide 0, ground min 0.004 in all clips, `collision_free` true. PASS.
- Acts in place and end at rest: act f100 vs f0 = 0.0, roar f60 vs f0 = 0.0. Event frames unchanged. PASS.
- `ANIM_REFS.md` cites W0 for the walk and records the 36 f (1.2 s) choice, with 30 f as the fallback. The lead ruled the tempo is not a fault. PASS.
- Pose sheet `pclose_tq_walk_00/09/18/27`: planted feet and a readable diagonal lift at 0.045. PASS.
- Why 8.7 and not 9: the clip 9+ list from round 4 is closed, so I scored up. I held 0.3 back because the new feet and 1.2 s gait can only be judged from stills here, and the act's cloak-fan mane (non-limb, `Mane1_L` f25) peaks at 6.38 deg per frame. That is unchanged from round 4 (6.6) and is not a breach of any rule.

## Pass / fail (round 5)
| check | result |
|---|---|
| R4 #1 eye at 64 px (7 / 21 on the agreed mask) | LANDED (saturated core 3 px) |
| R4 #2 accent, three separate plume elements | NOT DONE (two; split skipped on purpose) |
| R4 #3 icon luminance below sphinx, game lavender at or above 40 | LANDED (83.3 vs 92.8; 41.34 %) |
| R4 close-up eye (pupil claim or narrow slit) | PARTIAL (claim dropped; slit still a window) |
| R4 front Mane2 blocks (WATCH) | LANDED |
| Regression: poke, intersect, collision | PASS (none) |
| Regression: close-up socket frame | FAIL, minor (R1, fix given) |
| Tris <= 15k (6,820) | PASS |
| Clip knee steps and seam | PASS (all under 5.63) |
| Clip limits, loops, ground, flips, ends at rest | PASS |

**Verdict:** Model 8.5, PASS (holds; 9+ not reached: accent not done, close-up eye partial). Clips 8.7, PASS. Must-fix before the next pass: R1 (socket width). Nothing blocks the 8.5 ship bar.
