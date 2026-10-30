# Volt Rhino - model gate review 2 (2026-10-27) - APPROVED WITH FIXES (model)

**Score: 7.5/10 for a 6 % High** (ship bar about 8). Round 1 was 6/10. The body now reads as steel, not grey plastic. The
belly is a real pale band, the horn is one smooth tube, the ears are fierce, and the lime is greener and clearer. Four
small defects are left, and one of them (the horn rings) brings back the segment-step fault from round 1. None of the fixes
changes a bone, a joint or a bone name.

**Verdict: APPROVED WITH FIXES.** Same route as VenomBasilisk review 2: **the clips can start now.** The MUST fixes below must
be in the mesh before export. Send one updated `_close_sheet` (brow, horn rings), `flat_side` and the StormWyvern strip with
the first clip pose sheet. No new full model round.

## What I looked at
- `pets/VoltRhino.py` (348 lines; line references below); `VoltRhino/MODEL_NOTES.md` "Round 2" section
- `_review/VoltRhino_review1.md` (the M1-M8 list), `_review/GLACIER_REVIEWER_BRIEF.md`
- Renders: `_model_sheet`, `_close_sheet`, `_horn_sheet`, `under.png`, `model_game.png` (600 px), `model_side`, `model_front`,
  `model_back`, `flat_side`, `flat_game`, `flat_tq`, `_icons_strip_64`, `_icons_strip_128`
- Combined strip: `VoltRhino/_scratch/_all_strips_r2.png`

## 1. Round-1 MUST status

| Item | Status | Evidence |
|---|---|---|
| M1 palette: IRON (156,164,178), IRON_D (92,100,116) | DONE | `flat_side`, `_model_sheet`: steel flanks, darkest back in `flat_game` |
| M2 fold rims as wedges | PARTIAL | Wedges are on. From the game camera the back still shows three dark arcs (`model_game`), which read as bands. NICE |
| M3 armour edges sloped | PARTIAL | Shield, saddle and rump now slope (L82-84). A light flank panel under the saddle still has straight edges (MUST 4) |
| M4 pale underside 8 % | DONE | 8.1 % side. Pale belly band, pointed ends, pale throat and jaw. Visible in `flat_side` and `under.png` |
| M5 ears: dark flaps, black inner | DONE | `_close_sheet` panel 1: reads as fierce ear flaps, no headphone cups |
| M6 horn: one smooth tube, no segment steps | PARTIAL | Smooth tube and root collar work. The two growth rings protrude as steps (MUST 1) |
| M7 VOLT 3.6 % side / 3.2 % game, eyes 22 deg | DONE | Rump bolt reads in `model_side`; slits read as fierce in `_close_sheet` |
| M8 nasal ridge and brow | PARTIAL | Nasal ridge DONE (grow 0.012). Brow still reads as a dark pipe (MUST 2) |

## 2. MUST (prioritised, all in `pets/VoltRhino.py`; none changes a bone)

### MUST 1. Horn growth rings: flush them or drop them (L250-254)
- The two growth rings are `(0.47, 0.51, 0.008)` and `(0.66, 0.70, 0.008)`, a proud 0.008 model units. In `_horn_sheet`
  panels 2-3 they read as stacked steps with white outer edges: a telescope or a traffic cone, not growth lines.
- Change both ring offsets to **0.003** or less, or colour them as flush bands. Keep the root collar (0.014 at L252) as it is.
- Check in `horn_side` that the silhouette has no step along the upper horn.

### MUST 2. Brow: stop it reading as a pipe (L236-239)
- The brow block `(0.040, 0.026, 0.096)` sits on the skull as a separate dark capsule. In `_close_sheet` panel 2 it reads as a
  stuck-on bar above the lime slit.
- Sink it into the skull: move `bc` in by 0.010 along `-n`, so only about two-thirds of it is visible. Or give it a flatter
  wedge (depth 0.018, bevel 0.008) so it reads as a brow overhang.
- The eye socket and the lime slit stay where they are.

### MUST 3. Legs: one fold band per leg, not stacked rings (L287-291)
- Each front leg carries the elbow fold (L287-289) and the shin gaiter (L290-291): two dark bands on the front legs.
  The rear legs carry two as well. In `under.png` and `model_side` the legs read as stacked tiers or robot rings.
- Keep the elbow/knee fold on each leg. **Remove the front shin gaiter** (L290-291), or make it flush (proud 0.003).
- Make the elbow fold a tapered wedge, not a full ring, so it matches the back folds.

### MUST 4. Flank panel under the saddle: no straight-edged window (L83, L186-187)
- In `flat_side` there is a lighter rectangle on the mid-flank (about x 250-305, y 150-190 of the 400 px frame). Its top is the
  saddle's lower edge (f 0.34 -> 0.22) and its bottom is the PALE top at -0.24. Both edges are straight, so the panel reads as
  a window.
- Direction: lower the saddle's rear edge from f 0.22 to about **0.06** (L83), so the dark saddle runs down the flank and the
  light panel shrinks to a point. Alternatively, raise the PALE band top under the saddle (y 0.0 to 0.40) to meet it.
- Check `flat_side` after the change: the light area should be the belly, not a panel on the flank.

### MUST 5. Deliverable: StormWyvern is missing from the strips
- The brief names StormWyvern as a comparator. The round-2 strips (`_icons_strip_64`, `_icons_strip_128`,
  `_all_strips_r2.png`) show Volt, ThunderBull, Raiju, Thunderbird and ThunderRex only.
- Add StormWyvern to both strips, next to the rhino, at 64 and 128 px. The Wyvern is the 14 % Thunder pet the rhino must beat
  on look (plan section 2).

## 3. NICE (do these too)
- **Horn zig reads as a pasted ribbon.** The lime sits proud (the `hw + 0.004` offset, L264-270 area) and looks like a flat
  sticker in `horn_side`. Sink the zig by half its thickness so only about 0.006 shows. Keep the 0.060 width.
- **Horn from the game camera.** In `model_game` the horn is a thin pale spike and its lime is faint. Carry the zig over the
  top of the horn, or add a short lime tip band, so the hero reads from above and behind.
- **Back arcs.** Taper the rump plate's rear edge to a point (`ARMOUR` L84, f -0.02 -> 0.06) so the back reads as a shield and
  two folds, not three rings.
- **Horn share.** HORN_IVORY + HORN_SHADE is 3.4 % side against the plan's 6 %. Accept: the horn is slimmer and the 64 px read
  is fine. Do not thicken it to hit the number.

## 4. Pass / fail checklist

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Tris at or under 15k | PASS | 12,452 |
| 2 | Silhouette at 64 and 128 px; species reads | PASS | Rhino + horn, the only steel-grey body in the strip |
| 3 | Hero (lime horn) at 64 px | PASS | Horn and lime read in `_icons_strip_64` |
| 4 | Fierce, not cute | PASS | Lime slits under dark brows, dark back, dark ear flaps. Brow fix (MUST 2) lifts it |
| 5 | Not a grey plastic toy | PASS with fixes | Steel reads at 128 px; leg tiers and horn rings still toy-like (MUST 1, 3) |
| 6 | Dark back + pale underside + ONE accent | PASS | Back 45.8 % side (darkest in game), underside 8.1 %, lime the one accent |
| 7 | Palette shares | PASS | IRON_D 45.8 % (gate 25); PALE 8.1 % (8-10); VOLT 3.6 % side, 3.2 % game (3.5-4.5 side) |
| 8 | Accent strong in game colours | PASS | Horn zig, shoulder bolts, rump bolt, eye slits. NICE: horn from behind |
| 9 | Distinct from siblings | PASS | Only neutral body in the egg; lime 26 deg from Thunderbird BOLT (accepted) |
| 10 | Stud skin off horn, inlays, toenails, eyes | PASS | `nostud` on horn, zigs, toenails, slits |
| 11 | No glow, no Neon | PASS | Colour only |
| 12 | Floating, poking, intersecting | PARTIAL | Brow pipe (MUST 2), horn ring steps (MUST 1). Horn root collar seats cleanly on the nose |
| 13 | Visible from below | PASS with notes | `under.png`: pale belly and throat clean, no gaps. Leg tiers (MUST 3) |
| 14 | Deliverables | PARTIAL | StormWyvern missing from the strips (MUST 5) |

## 5. Next steps
1. Lead: apply MUST 1-4 in `pets/VoltRhino.py`. Keep the bone names. Check the tris stay under 15k.
2. Lead: the clip stage may start now. Fixes must be in the mesh before the FINAL export (step 1 and export).
3. Send to the reviewer after the fixes: `_close_sheet` (brow and horn rings), `_horn_sheet`, `flat_side`, `_icons_strip_64`
   and `_icons_strip_128` with StormWyvern, plus the first clip pose sheet.
4. Clip gate notes (carry forward): the horn tip sits 1.23 from the throat pivot, 25 deg above horizontal (MODEL_NOTES). The
   horn tap needs a front-leg crouch and a spine pitch. Head pitch-up at most 16 deg for the roar (review 1 MUST 2). Report
   the neck, chest and head numbers from the headless run.
