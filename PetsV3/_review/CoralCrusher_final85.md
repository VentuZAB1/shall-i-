# Coral Crusher - FINAL GATE (8.5 bar), 2026-10-28 - FIX

**Model: 7.5/10. Clips: 7.5/10. Verdict: FIX.** Both are under the owner's 8.5 minimum (2026-10-28, "the higher the better").
The earlier 8s (`CoralCrusher_review3.md` model, `CoralCrusher_review4.md` clips) were judged against the old ship bar of 8.
This gate is stricter: the body colour, the missing pale underside, and the idle and act secondary motion are new findings
against the 8.5 bar. Clips are numerically clean; the gap is in quality and readability.

Estimated after the MUSTs below: model 8.5, clips 8.5. Not re-scored; that needs the next render round.

## What I looked at
- Brief: `_review/GLACIER_REVIEWER_BRIEF.md`; plan `_review/CoralCrusher_plan.md` (v2); owner decisions in
  `_review/GLACIER_CONCEPTS.md` (names two words, no new wave); plan review 2.8 in `_review/GLACIER_PLAN_REVIEW.md`
- Earlier reviews: `CoralCrusher_review1.md` (6/10), `review2.md` (7/10), `review3.md` (model approved, clips 8/10),
  `review4.md` (clips approved 8/10)
- `CoralCrusher/MODEL_NOTES.md`, `CLIP_NOTES.md`, `ANIM_REFS.md`, `CoralCrusher_meta.json`
- Rules: `V:\Obsidian\Roblox\06 Modelling and Art\Creature Style.md`, `Model Review Checklist.md`, `Creature Animation.md`;
  `PetsV3\FIERCE_GUIDE.md`
- Images (all opened): `renders/_model_sheet.png`, `_close_sheet.png`, `gamelook_game.png`, `flat_game.png`,
  `_under_sheet.png`, `_pose_tq_sheet.png`, `_wave_strip.png`, `_icons3_strip_64.png` / `_128.png`,
  `CoralCrusher_portrait_alt.png`; comparison: `_ALL_FIERCE_progress.png`, `_review/Raiju_model.png`
- Code: `pets/CoralCrusher.py` (palette L19-23, carapace and rim L152-170, cream lip L168-169, claws L240-290, idle L457,
  walk L480, roar L513, `act_semaphore` L538-580)
- Sibling acts: no other pet uses a claw wave; the act motif is unique.
- Not re-run: the headless gate. I used the numbers the notes report (collision_free true, ground_min_z -0.013,
  loops 0/0, slide 0.002). Not opened: the Sakugabooru posts.

---

## 1. MODEL: 7.5/10

**Passes**
- Species reads at game distance and at 64 px (`_icons3_strip_64` item 3, the game-camera icon): claws up, shell, legs.
- The claws are the hero. Rose spikes, black tips, and the asymmetry (crusher 1.20, cutter 0.98) read in `gamelook_game`.
- Fierce face: slate lids, one V brow, small slate mandibles with ivory tips (`_close_sheet` panels 3-4). No googly eyes.
- No box belly: domed loft, sloped shell, legs under the rim.
- Accent: rose spikes are the one bright accent and read as pink points at 64 px.
- Hard rules: studded body, smooth details, no glow, 11,900 tris (cap 15k), name two words.
- Shares reproduce from the flat renders (within about a point).

**Fails the 8.5 bar**
- **Body colour is mud.** The copper body is about 50 % of the side view (MODEL_NOTES, strict shares). In `gamelook_game`
  and `flat_game` it reads dusty tan-brown. In the lineup (`_ALL_FIERCE_progress.png`) Kraken is red, Raiju is saturated
  blue with yellow bolts, Kappa and the Turtle are teal. Coral is the dullest shape in that row. The owner's favourite
  (Raiju) is a saturated fire of colour, not a beige crab.
- **No pale underside.** Belly pale is 0.9 % side, 0.4 % tq, 0.8 % game (MODEL_NOTES). The FIERCE rule (dark body +
  lighter underside + one accent) is effectively unmet. The cream shows as a thin line under the rim at the front, and
  `gamelook_game` shows almost none. The plan asked for 8 %.
- **Legs read as sticks.** Six thin dark stilts with black tips (`_model_sheet` tq). Borderline spider-like at distance.
- **Claws read as mitts from the front.** The palms are smooth, rounded ovals. The gap between the fixed finger and the
  dactyl is narrow, so the pincer read is weaker than the silhouette.

### MODEL MUST (to reach 8.5)
**MM1 - Body colour: saturate the copper, deepen the seams (the biggest lift).**
- `pets/CoralCrusher.py` palette, L19-21:
  - BRONZE (200, 136, 88) -> **(214, 110, 70)** (rust copper; hue about 17 deg, brightest channel 214, so the Roblox
    0.6x rule holds at about (128, 66, 42) in game).
  - BRONZE_D (146, 96, 62) -> **(150, 74, 50)**.
  - SHELL_D (100, 66, 46) -> **(80, 46, 34)**, for the seams, legs and the brow plate. This keeps the dark-rich part of
    the rule.
- Check: `gamelook_game` reads rust copper, not tan. Put it in the 64 px strip beside Kappa and the Turtle. Watch it
  beside Hammerjaw (same Water egg, orange spikes): it must stay the crab's copper, not the shark's orange.
- Report the new shares in MODEL_NOTES. Keep BELLY_PALE and ROSE unchanged.

**MM2 - Show the pale underside in the game camera.**
- Rim band, `pets/CoralCrusher.py` L157-158 (SHELL_D ring, `hw + 0.016`): change it to **BELLY_PALE (240, 226, 200)**
  and add a thin SHELL_D seam (0.012) above it. This makes a two-tone armour edge, as real crabs have.
- If the six legs still cover the band from the side (the coxa and merus reach z 0.37, the rim sits at 0.36-0.41),
  also move the cream lip (L168, `zc - 0.050`) down to `zc - 0.10` and widen it to 0.040.
- Target: **BELLY_PALE at 4 % or more in `flat_side` and `flat_game`**, measured with the same sampler. Report the number.
- If the builder cannot reach it, the owner must sign off a no-pale deviation in writing. The vault rule and the
  FIERCE guide still say "lighter underside".

---

## 2. CLIPS: 7.5/10

**Passes (per the notes; not re-run)**
- collision_free true; ground_min_z -0.013; linear 0; loops 0/0; walk slide 0.002; idle foot drift 0.
- The wave reads: three arcs with holds, top-to-trough 36.7 / 42.1 / 36.7 deg, feet planted (`_wave_strip`, tq and game).
- The roar reads: short crouch, claws up in a V, three cocked-open clacks (`_pose_tq_sheet` roar f14-f38).
- The walk is a tripod scuttle at 45 deg (L1/R5/L3 vs R4/L2/R6), with claws held low.
- Acts end at exact rest (f110-120 for the act). No airborne spins, no head shakes.

**Fails the 8.5 bar**
- **The idle is a held threat pose most of the time.** CLIP_NOTES: the crusher lifts 20 deg at f12-28 and holds to f98,
  which is 70 of 120 frames. The pet's most-seen clip has no breathing (`_pose_tq_sheet` idle f28, f66, f70 all show the
  claw up). A pet that idles like a guard reads as aggressive all the time.
- **The act moves only one limb.** `act_semaphore` drives the claw, plus the cutter taps. The eyestalks and the shell do
  nothing through three weight-bearing beats. The wave reads as a mechanical arm, not an animal showing off.
- **The walk's timing has no site support.** ANIM_REFS S1 is the Ohmu *run*, and the notes say it does not support the
  30 f cycle. The timing rests on Wikimedia C1. The owner rule asks for animationreference.org clips for the timing.

### CLIP MUST (to reach 8.5)
**CM1 - Idle breathes (`idle(k)`, L457).**
- Keep the claw guard, but add a slow breath to the crusher lift: `claw(k, f, "R", lift=...)` at 20 deg +/- 3 deg, one
  35 f period (troughs f45 and f80, peak f62). Stay in the guard band, so the tap at f70 still reads.
- Body: `body(k, f, up=...)` at a 0.008 BU bob on the 120 f loop, closed. Feet stay IK-planted.
- Gate: loops 0/0, collision_free true, idle foot drift 0.

**CM2 - Act: secondary motion on the three beats (`act_semaphore`, L538-580).**
- Eyestalks track the crusher tip: `eyes(k, f, l=..., r=...)` with a yaw of about 12 deg, lagging the wave by 2 f. One
  smooth arc per beat, centred on `wave1` f30, `wave2` f53, `wave3` f76. Not an L/R alternating shake.
- Shell weight: `body(k, f, roll=...)` at +/- 2 deg on each peak, so the crusher side dips as it lifts.
- Keep the rest exact at f110-120. Re-check collision_free and foot drift 0.

**CM3 - Walk timing from a site clip (owner rule).**
- Pull one animationreference.org walk clip with a slow multi-leg or quadruped cycle (`/tags/walk-cycle`, 369 clips).
  Note the frames of one cycle in ANIM_REFS, and set the 30 f cycle from it (or change it and say so).
- Or log the owner's written ruling that Wikimedia C1 sets the walk timing. Either way, ANIM_REFS must not cite the Ohmu
  run as the timing source.

---

## 3. TO 9+ (highest impact, after the MUSTs)
1. **Legs thicker (model).** Widen the merus blocks about 20 % (the six-leg block from L294; leg proportions in LEGP L41-44). The six legs stop
   reading as stilts in the tq view.
2. **Pincer gape and molars (model).** Widen the pincer gap from 0.04H toward 0.06H and add two small slate molars on the
   dactyl's inner edge (`claw` section L240-290). From the front at 64 px the claw reads as a pincer, not a mitt.
3. **Accent on top of the shell (model).** Add two taller ROSE_D + ROSE coral clusters on the dome centre (the rear
   growth loop at L206). The game camera looks down, and the rose now sits only at the rim.
4. **Walk claw sway (clips).** Add a 4 deg sway to the crusher claw at half the cycle, out of phase with the legs. Then
   the claw is not a rigid block in the walk.

---

## 4. Pass / fail checklist

| # | check | result |
|---|---|---|
| 1 | Silhouette reads at 64 px and in game (game-camera icon) | PASS |
| 2 | Species reads at 5 studs (crab, not spider or bug) | PASS (legs borderline: TO 9+ 1) |
| 3 | Fierce face (brow, slits, ivory mandibles, no glint) | PASS |
| 4 | No box belly; belly line rises to the legs | PASS |
| 5 | Dark rich body (colour saturation vs lineup) | **FAIL** (MM1) |
| 6 | Pale underside shows (>= 4 % side and game) | **FAIL** (MM2) |
| 7 | ONE bright accent (rose) reads at 64 px and in game | PASS |
| 8 | Hard rules: studs on body, smooth details, no glow, <= 15k tris | PASS (11,900) |
| 9 | Floating, intersecting, see-through, inside-out parts | PASS (per review 2-3) |
| 10 | Palette shares reproduce from flat renders | PASS |
| 11 | Clips: collision_free, ground, loops, slide (as reported) | PASS (not re-run) |
| 12 | Pose limits (Spine analogue), no head shakes, no airborne spins | PASS (per review 4) |
| 13 | Idle reads alive (not a held threat pose for 2/3 of the loop) | **FAIL** (CM1) |
| 14 | Act has secondary motion on the beats | **FAIL** (CM2) |
| 15 | Acts in place, end exactly at rest | PASS |
| 16 | Animation-reference rule (site clip supports the timing) | **FAIL** for the walk (CM3); PASS for the wave (S2) |
| 17 | Name is two words; no gold claimed; medium tier fits its ladder | PASS |

**Model 7.5/10. Clips 7.5/10. FIX.** Send the next round with: the model sheet, close-ups, `flat_side` and `flat_game`
shares (MM1 and MM2), `gamelook_game`, the 64/128 px strips beside Kappa, the Turtle and Hammerjaw, the idle pose sheet
(f0-f120), the act wave strip with the eye and roll keys, and the ANIM_REFS walk line.
