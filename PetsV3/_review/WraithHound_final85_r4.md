**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.**

# Wraith Hound - FINAL 8.5 GATE, round 4 (9+ polish check; model 01:47, FBX 01:48) - 2026-10-28

Both scores hold at 8.5, the same as round 3. The polish round made three edits. All three are verified in the code and the renders, and none is a regression. None of them moved the 64 px read, which is what kept round 3 at 8.5. Nothing blocks the ship bar. 9+ needs the items under "Still between this pet and 9+".

## What I looked at
- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round 3 `_review/WraithHound_final85_r3.md` (its TO 9+ list); `WraithHound/MODEL_NOTES.md` (Round 7) and `CLIP_NOTES.md`.
- Code: `pets/WraithHound.py` (01:47) diffed against `WraithHound/_scratch/WraithHound_pass85.py` (01:45, the round-3 state). The diff holds only the three polish edits: ASH_LAV, the `tipw` argument on the Mane2 side tips, and the eye slit, rim and pupil heights.
- Renders (01:47 set): `_model_sheet.png` (four views), `_close_sheet.png`, `close_front.png`, `close_side.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `crop_mane_front.png`, `model_front.png`, `_shares.json`.
- Pre-polish comparators: `WraithHound/_scratch/strip64_pass85.png`, `strip128_pass85.png` and `game_pass85.png` (all 01:45); `renders/_fan_front_back_r2.png` (01:41).
- Clip: `renders/_pose_tq_sheet.png` (01:41, the newest pose sheet), `_scratch/clipmetrics.json` and `fullcheck.json` (01:47), `_scratch/gate7.log` and `export.log`.
- My zooms and pixel counts (PIL) are in `C:\Users\ventu\AppData\Local\Temp\wh_r4\`. No file in the pet folder was touched. Icon 1 (the Wraith) was measured at 64 px and 128 px against the pass85 strip.
- Not used as evidence: `_scratch/lav/_lav_compare.png` (no labels). Every image I needed loaded.
- Staleness note: `_pose_tq_sheet.png` predates the 01:47 polish. Round 7 changed eye geometry, a tip width and a colour, not motion, and the 01:47 clip metrics match round 3, so the pose sheet still stands for the clip score.

## Builder claims, checked
| claim | result |
|---|---|
| Eye slit 0.022 (was 0.018) | Confirmed in `pets/WraithHound.py`. The rim went 0.020 to 0.024 and the pupil 0.0175 to 0.021, as the notes say. The socket stays 0.028. |
| Mane2 side tips tip width 1.0 | Confirmed: `tipw=(1.0 if bone == "Mane2" else None)`. The Mane2 centre tip stays 0.85; Mane1 and Mane3 stay soot. |
| ASH_LAV (158,148,198) | Confirmed in the code. |
| Game ASH_LAV 40.7 / SOOT 28.5 / INDIGO 5.9 | Confirmed in `_shares.json` and `gate7.log`. |
| Tris 6,820; all gates pass | Confirmed in `export.log`, `gate7.log` and `fullcheck.json`. |

## Round-3 TO 9+ items
1. **Icon-size eye: PARTIAL.** The geometry landed, but the 64 px read did not change. In the 64 px icon the eye box (strip x 16-30, y 24-36) holds 2 indigo pixels before and 3 after, so the eye is still one speck. At 128 px it goes from 8 to 11. Round 3 asked for an eye that reads "as a point of light" at 64 px; that is not met. The pupil is not visible in any close-up (front, side or three-quarter), so the pupil change has no visible effect. The hotter-colour option that round 3 offered was not tried.
2. **Icon-size accent (Option A): PARTIAL.** The Mane2 side tips are fatter. The 64 px plume zone goes from 52 to 58 indigo pixels, and 128 px goes from 193 to 205. An indigo-only mask at 64 px shows one blob plus one 3-4 px streak, so two blue elements, not the three points asked for. The blue stays on Mane2 only, which is correct.
3. **Palette test: LANDED to its stated condition, small effect.** ASH_LAV is (158,148,198). Game ASH_LAV is 40.7 %, against the 40 % floor (0.7-point margin). The game view still reads lavender (old against new in `cmp_game`). At icon size the Wraith's mean luminance goes from 99.8 to 97.9. It is still the second-lightest icon: the white-gold sphinx in slot 5 is 100.2, and the other four icons are 67 to 74.

## Regressions
None that must be fixed.
- Eye: in the front and side close-ups the blue slit sits inside the black socket, under the brow. No poke-through and no clipping.
- Mane2 tip widening: no intersection (`collision_free` true, `collisions` empty) and no floating parts in the front, side or game views.
- Watch, not a MUST: from the front, the fatter Mane2 side tips read as two chunky blue blocks flanking the crest (`model_front.png`). The same position is in `_fan_front_back_r2.png`, smaller. If the owner reads "wings from the front" again, the first revert is `tipw` back to 0.85 on Mane2.

## Clips: 8.5 PASS (unchanged)
- Limits from `clipmetrics.json` (01:47), idle / walk / roar / act: neck max 3.5 / 3.98 / 4.0 / 5.0 (limit 8); chest vs spine 0.6 / 2.92 / 1.5 / 1.5 (limit 5); head pitch-up 8.0 / 0 / 0 / 3.5 (limit 30). These match round 3. Quaternion flips are 0 in all clips.
- `fullcheck.json`: `collision_free` true, ground min 0.004 in all four clips, linear 0, loops closed, walk slide 0.
- `_pose_tq_sheet.png` (15 frames, 01:41): the poses read, the feet stay planted, the roar jaw and the cloak fan look right. No pose issue.

## Still between this pet and 9+ (measurable, model)
1. **Eye at 64 px.** The eye box has 3 indigo pixels and needs at least 6 (at 128 px, at least 16). Options: make the slit a hotter fill, for example (150,160,255), so it is brighter than the socket; and/or narrow the socket from 0.052 to 0.046 wide so more of the 64 px cell is blue.
2. **Accent at 64 px.** The mask shows 2 blue elements; 9+ needs 3 separate ones. The only route is to split the Mane2 side tips further apart (d0 x 0.40 to about 0.46, Mane2 only). That trades against round-4 NICE 3 (no front "wings"), so re-check the front crest after any change.
3. **Icon luminance.** The Wraith icon's mean Y must come down from 97.9 to about 90, so it is no longer the palest of the bright icons, while game ASH_LAV stays at or above 40 %.
4. **Close-up eye (NICE).** The pupil is not visible: either pull it 0.002 proud of the slit or drop the claim. The slit is about 1.9:1 (0.042 by 0.022) and reads as a blue window more than a narrow slit at close range. A narrower slit would look fiercer but costs the icon read, so this is an owner call.

## Still between this pet and 9+ (clips, NICE, not a brief limit)
- The walk's largest local per-frame step is 9.06 deg (Shin_FR f0 to f1), and the loop seam is 6.55 deg (Shin_FL f29 to f0). The armature-space max is 5.63 (Leg_BR f21). Target: a walk local step under 5.63, so the knee does not flick at contact. The act clip's local max is 6.76 (Shin_FL f6), the same kind of step; it is a NICE, not a limit breach.

## Pass / fail (round 4)
Model:

| check | result |
|---|---|
| Round-3 TO 9+ #1, eye reads at 64 px | PARTIAL (FAIL for 9+) |
| Round-3 TO 9+ #2, accent reads at 64 px | PARTIAL (FAIL for 9+) |
| Round-3 TO 9+ #3, palette test | PASS (small effect) |
| No regression (poke, intersect, collision) | PASS |
| Tris <= 15k (6,820) | PASS |
| Fierce face, studs, no glow | PASS |
| Front-view Mane2 side tips | WATCH |

Clips:

| check | result |
|---|---|
| Neck, chest, head pitch limits | PASS |
| Ground, collision_free, loops, linear 0 | PASS |
| Acts in place, ending at rest | PASS |
| Pose sheet (pre-polish, motion unchanged) | PASS |

**Verdict:** Model 8.5, PASS (thin margin, unchanged). Clips 8.5, PASS. No MUST items. A round 5 is only needed if the owner wants 9+ on the 64 px eye and accent (items 1 and 2 above).
