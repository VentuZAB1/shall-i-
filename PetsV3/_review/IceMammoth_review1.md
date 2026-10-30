# Ice Mammoth - model gate review 1 (2026-10-27) - REVISE (model)

**Score: 6/10 for a MEDIUM 26 %.** Ship at about 8/10. The build is a solid start: the species reads, the trunk and tusks read,
the stud skin is correct and the mesh is clean. Two of the owner's rules are broken in ways that show in game (the accent and
the colour), and the pale underside and the spiky crest work against the dome silhouette. All four MUST fixes are mesh and
colour edits. **Bone names and the joint tree do not change**, so clip authoring can start on the current rig, but the clip
gate waits for the round-2 model sheet.

## Direct answers to the two checks
1. **Does the MINT accent still exist visibly?** No. It exists only in close-ups. Measured on the flat game-camera render:
   13 mint pixels out of 37,631 object pixels (0.03 %). In the 64 px icon there is no readable mint. The few cyan specks in
   the icon sit on lit body or tusk edges. Of the six pets in the strip, the Mammoth is the only one with no accent you can
   see at 64 px (ThunderBull cyan bars, MoltenBoar orange lines, Mossback green spots, Bramble Badger amber crest all read).
2. **Is the 170 rule broken in a way that will look muddy in game?** Yes, and the rule is not the main problem.
   - CHAR_TEAL (112,152,162) has a brightest channel of 162, 8 under the guide. Its Blender luminance (141) passes the
     luminance clause, so this alone is minor.
   - The real problem is the in-game darkening. At the ~0.6x Roblox factor, the body becomes about (67,91,97): a dull grey-slate
     with saturation 0.31. WOOL_D (64,84,96) becomes about (38,50,58), which is near-black. WOOL_D covers 49.8 % of the
     game-camera silhouette. That is a murky grey mass, and it is the owner's "grey plastic" complaint.
   - The builder's darkening was right in direction (the plan's pastel body looked "baby blue" in the lit icons, and the owner
     has rejected babyish pets). The overshoot went to grey, not to rich.

## What I looked at
- `pets/IceMammoth.py` (full read: palette L17-24, head L154-186, tusks L187-210, trunk L211-223, body and wool L243-278,
  neck, legs L282-299, tail, rig L313-340)
- `IceMammoth/MODEL_NOTES.md`, `_review/IceMammoth_plan.md`, `GLACIER_PLAN_REVIEW.md` 2.2, `GLACIER_CONCEPTS.md` (OWNER
  DECISIONS), `FIERCE_GUIDE.md`, the Obsidian Creature Style, Model Review Checklist and Creature Animation notes
- Renders: `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png` and `_128.png` (upscaled 4-5x), `flat_side/tq/game.png`,
  `model_game.png`, `IceMammoth_icon.png`
- `_scratch/trunk_proto_sheet.png` and `trunk_proto_64.png`
- Comparison: `GlacierYeti/renders/_model_sheet.png`, `FrostfangLynx/renders/_model_sheet.png` and its 64/128 strips,
  `_ALL_FIERCE_progress.png` (lineup)
- Pixel counts on the flat renders (background excluded, nearest palette colour) to check the builder's shares

## Measured value shares (object pixels, flat palette IDs)
| view | CHAR_TEAL | WOOL_D | TUSK_ICE | DARK | BELLY_PALE | MINT |
|---|---|---|---|---|---|---|
| side | 54.8 | 30.6 | 4.2 | 3.2 | 0.7 | 0.12 |
| tq | 56.3 | 25.3 | 6.6 | 5.4 | 0.3 | 0.44 |
| game | 41.2 | 49.8 | 1.5 | 2.6 | 0.09 | **0.03** |

The builder's side numbers (56.7 / 31.9 / 4.3 / 3.7 / 1.2 / 0.2) match within about 2 points. The numbers are honest.
Plan targets were 42 / 18 / 6 / 6 / 10 / 4. Belly and accent are the two that collapsed.

## Colour in game (estimate: flat x 0.6, the Roblox rule; not a game screenshot)
| colour | Blender RGB (brightest, S) | in game ~ | note |
|---|---|---|---|
| plan CHAR | (150,184,188) (188, 0.20) | (90,110,113) | the plan's game target |
| builder CHAR | (112,152,162) (162, 0.31) | (67,91,97) | grey-slate, 20 luma under target |
| **proposed CHAR** | **(96,168,184) (184, 0.48)** | (58,101,110) | rich dark teal, not grey |
| builder WOOL_D | (64,84,96) (96, 0.33) | (38,50,58) | near-black across half the silhouette |
| **proposed WOOL_D** | **(80,110,124) (124, 0.35)** | (48,66,74) | same game darkness as Raiju's FUR (~48,61,109) |

Proposed CHAR/WOOL Blender luminance is 148 / 103, a clear value step for the wool to read against the body.

---------------------------------------------------------------------------------------------------------------------
## MUST (in priority order)

**M1. Make the MINT accent a real accent (the explicit check fails).**
- Target: MINT at least 1.5 % of side-view object pixels and at least 0.8 % in the game-camera view. That is about 30 px in the
  64 px icon, a cyan flash you can see. Today: 0.12 % side, 0.03 % game.
- Tusk cracks (`pets/IceMammoth.py` L196-210): the bars are 0.022 long x 0.007 thick, so they read as small L-brackets (see the
  close sheet). Make them 0.035 long x 0.012 thick, and use 3 per tusk at t = 0.55, 0.70, 0.85 on the outer third. Keep them
  flush.
- Add a MINT ice cap on each tusk tip: the last 0.10 units of the tube, a second short tube or a `B.seg` in MINT with
  `nostud=True`. A cyan tip against the white tusk is the strongest 64 px accent you can get on this pet.
- Eye slits (L173-175): the MINT slit (0.058 x 0.008) grows to about 0.075 x 0.016, and the socket stays DARK.
- Do not add a glow. Solid MINT only.

**M2. Fix the body colours (the 170 check and the muddy read).**
- `CHAR_TEAL` (L17): (112,152,162) becomes **(96,168,184)**. Brightest 184 (passes 170), saturation 0.48, hue 190. Keep
  it saturated so it does not go pastel. Re-check the 64 px strip after the change so it does not read as "baby blue".
- `WOOL_D` (L18): (64,84,96) becomes **(80,110,124)**. Dark, but not near-black in game, so it reads as a slate-teal mane.
- Keep the brows and the head cap on WOOL_D. Keep the tusks TUSK_ICE and the tip DARK.
- Re-render the flat game and side views and report the new game shares. Target: the CHAR share in game above 40 %, and the
  WOOL share in game below 45 %.

**M3. Restore a visible pale underside (the belly rule is broken: 0.7 % side, 0.09 % game).**
- Cause: the wool lock rows hang too low. Row 3 (L260, L = 0.30) and row 2 (L = 0.29) reach about z 0.4-0.5 by my estimate from
  the code (flank surface near z 0.8, minus L). The barrel underside is about z 0.6, so the skirt covers the belly band
  (L243-244, BELLY_PALE). The plan's limit was 0.35H, which is z 0.64.
- Fix: shorten rows 2 and 3 so the tips stop at about z 0.64 (row 3 L 0.30 to about 0.16, row 2 L 0.29 to about 0.20).
  The pale band then shows as a strip of about 0.05-0.08 units under the body.
- Target: BELLY_PALE at least 3 % side and at least 1 % game. Check the side view at belly height.
- This is also what makes the lock rows read as blocks, not tassels (see NICE 2).

**M4. Replace the spikes with wool clumps so the silhouette is a dome.**
- Head cap (L161-165): four spikes with `top=(0.2, 0.4)`, L 0.13-0.15. Change to rounded wool blocks: `top=(0.6, 0.6)`, L 0.08,
  width 0.07. They must not poke out past the dome.
- Spine tufts (L249-258): seven pointed spikes (`top=(0.25, 0.35)`, L 0.12-0.18, width 0.085) read as a stegosaur or hedgehog
  ridge on the flank. Change to `top=(0.7, 0.7)`, L 0.10-0.12, same width, so they read as laid-back wool clumps.
- Check: at 64 px the top of the silhouette should be a dome with a soft ridge, not a row of points.
- Head height (about 0.9H with the head group scaled 1.12) is accepted, see NICE 3.

**M5. Deliverables for round 2 (the builder did not send these).**
- The game-camera flat share after M1-M3, and a flat side and tq.
- An underside render (camera below the body, looking up). Parts visible from below were not checkable in this round.
- The 64 and 128 px icon strip with ThunderBull, MoltenBoar, Mossback, Bramble Badger and the Yeti, so the accent can be judged
  against them.
- The trunk icon at 64 px (see NICE 4), and the same model sheet and close sheet.

---------------------------------------------------------------------------------------------------------------------
## NICE (do them if they are cheap)

1. **Tusk socket rings (L193, DARK)** read as black bracelets around the trunk root in the close sheet. Use WOOL_D or CHAR_TEAL
   so the tusk root reads as a socket. Keep DARK for the toenails and the trunk tip.
2. **Tusk colour:** TUSK_ICE (238,246,250) reads glossy white plastic in close-up. Ice-ivory is better: (226,240,246). The
   smooth tube itself is accepted (see deviations below).
3. **Head:** the 1.12 scale makes the head front boxy (close sheet). Round the skull front: the `rnd` on the head block (L155,
   0.42) goes to 0.55. The 1.12 scale is accepted as a deviation: a mammoth's crown is close to its shoulder height, so the
   plan's "head top 0.62H" looks wrong for this animal.
4. **Trunk at 64 px:** the trunk reads at 128 px and in flat_tq, but it merges with the body between the front legs at 64 px.
   Lower `TRUNK_TIP` (L32) from z 0.37 to about 0.28 so the tip sits below the knee line and adds a silhouette beat. Keep the
   finger tip DARK.
5. **Wool skirt (side view)** reads as fringe or tassels. M3 fixes most of it. Also give the row-2 locks a more even length.
6. **The dorsal dome** (L246-247, WOOL_D band) reads as one flat dark slab from the game camera. Break it with two transverse
   CHAR_TEAL stud-ridge seams (0.018 wide), similar to the Venom Basilisk FIX 6.
7. **Brow shelves (L167-170)** look like separate visors in the front close-up. Push them 0.01 into the skull. Keep the V shape.
8. **Ring bands:** the trunk ridges (accordion bands, L132-148) read a little caterpillar in close-up. Soften the step ratio
   (0.90) to 0.94, or drop to 2 bands per segment.

---------------------------------------------------------------------------------------------------------------------
## Deviations from the plan: accept or reject
- **Tusks as smooth tubes (not 3 blocks): ACCEPT.** Blocks kinked; the smooth curve is better. Keep the cracks and the cap (M1).
- **Head scale 1.12 and head top about 0.9H (plan 0.62H): ACCEPT.** See NICE 3. The spikes are the problem, not the height (M4).
- **Body colours darker (M2): REJECT as built, ACCEPT the direction.** Grey, not rich.
- **WOOL_D 32 % side (plan 18 %): ACCEPT** as the dark mane, but only with the new WOOL colour (M2) and the lock rows shortened (M3).
- **BELLY_PALE 1.2 % (plan 10 %): REJECT.** The rule is "dark body + pale underside". Fix with M3.
- **MINT 0.2 % (plan 4 %): REJECT.** Fix with M1.
- **Toenails as blunt DARK blocks, not B.spike claws: ACCEPT** for an elephant foot. Do not add claws.
- **Trunk as 4 accordion segments with a pale inner strip: ACCEPT** (the trunk prototype gate passes at 128 px; see NICE 4 and 8).

## Tier and lineup
- Medium 26 %. The Mammoth is 9.0 tall, the same as the Yeti (14 %) and the Roc (7.4 %). The rarer pets sit at the same height,
  so the Yeti's and Roc's extra presence has to come from silhouette. Do not add height. An 8.5 Mammoth is possible if the
  round-2 lineup shows the Yeti losing its place. Not a MUST.
- Distinctness: the teal body (H 190) is apart from the Yeti navy (H 234) and the Lynx sand. The mint (H 161) is 29 degrees from the
  Lynx ICE accent, which was the plan's ruling. Keep the mint on the tusks and eyes only, so the Lynx and Mammoth do not share an
  accent location.

## Pass / fail checklist
| check | result | note |
|---|---|---|
| Tris <= 15k | PASS | 11,216 (builder number; not re-counted) |
| HEIGHT 9.0 | PASS | builder number; not re-measured |
| Stud skin on body, head, legs, trunk; details smooth | PASS | close sheet |
| No glow, no Neon in renders | PASS | |
| Eyes: narrow slits, no glint, no smile, not googly | PASS | small; see M1 |
| Brow shelf reads fierce | PASS | V shape, inner end low |
| Trunk reads at 128 px | PASS | visible in the 5x zoom |
| Trunk reads at 64 px | BORDERLINE | merges with body between legs (NICE 4) |
| Tusks read at 64 px | PASS | white curves |
| MINT accent readable at 64 px | **FAIL** | 0.03 % game; M1 |
| Body brightest channel >= 170 | **FAIL** | 162 (M2) |
| Body does not read muddy in game | **FAIL** | grey-slate 67,91,97; M2 |
| Near-black only for small details | **FAIL** | WOOL_D near-black in game (M2) |
| Pale underside visible | **FAIL** | 0.09 % game; M3 |
| Dome silhouette (no spiky crest) | **FAIL** | head and spine spikes; M4 |
| Floating / poking / intersecting parts (renders) | PASS with note | brows (NICE 7), socket rings (NICE 1) |
| Parts visible from below | NOT CHECKED | no underside render (M5) |
| Builder shares match the render | PASS | within about 2 points |
| Clip gate | NOT APPLICABLE | model round only; pose sheets and `collision_free` come with the clip round |

## Not done in this review
- No Blender run and no game run. In-game colours are the 0.6x estimate.
- The underside view was not rendered, so the "visible from below" check is open (M5).
- Clip gate not run.
