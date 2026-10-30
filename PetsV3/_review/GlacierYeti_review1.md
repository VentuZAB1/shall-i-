# Glacier Yeti - model gate review 1 (2026-10-27) - REVISE (model)

**Score: 5/10 for a 14 % big tier.** Ship at 8/10 or better.

The silhouette is right and the species reads as a hunched ape. But it is still a blocky robot ape. The arms are tubes, the knees and feet are boxes, the two fists read as robot faces, the white muzzle with two fangs reads as a grin (the same failure as the chest V), and the single accent (AURORA) does not show at all. The builder's own doubt is confirmed: the torso front is a plain navy barrel and the limbs are blocky. None of the fixes needs a bone, joint or clip change, so the fixes can go into the mesh now.

## What I looked at

- Code: `pets/GlacierYeti.py` (palette L16-22, torso table L34-40, Spine/Chest tubes L110-111, hump ice sheets L115-128, head and face L131-160, arms, fists and knuckle plates L165-187, legs and feet L202-209).
- Builder and plan: `GlacierYeti/MODEL_NOTES.md`, `_review/GlacierYeti_plan.md` (v2), section 2.3 of `_review/GLACIER_PLAN_REVIEW.md`, `_review/GLACIER_CONCEPTS.md` (owner decisions), `FIERCE_GUIDE.md`, the Creature Style / Model Review Checklist notes.
- Yeti renders: `_model_sheet.png`, `_close_sheet.png` (front, side, tq), `_icons_strip_64.png`, `_icons_strip_128.png`, `model_front.png`, `model_side.png`, `model_back.png`, `model_game.png`, `close_front.png`, `flat_side.png`, `flat_game.png`.
- Comparisons: Raiju `_model_sheet.png` (calibration), IceMammoth `_model_sheet.png`, LavaGolem `_model_sheet.png`, `_ALL_FIERCE_progress.png`. Kappa, SeaTurtleWarrior, Treant and BrambleBadger were judged from the 64 and 128 px icon strips only (their own sheets were not opened this round). `flat_tq.png` was not opened (the value shares come from MODEL_NOTES).

Measured facts: 5,076 tris (cap 15k). HEIGHT 9.0 studs. Side value shares: POLAR_NAVY 61.0, PLATE_ICE 18.6, BROW 15.0, BLACK 3.0, AURORA 1.1, SNOW 0.8, IVORY 0.5 (sums to 100). Tris, height and shares match the notes.

## What works

- **Silhouette and species.** The hunch, the pale shoulder crusts and the dark head read as an ape or yeti at 64 px and at 128 px. It is clearly not the Mammoth (teal, tusks, back spikes), the Badger or the Turtle.
- **Upper face is fierce.** The heavy brow V over narrow slit eyes is not round, has no glints and no smile. Keep it.
- **Body colour passes the rule.** POLAR_NAVY (108,116,196) has a brightest channel of 196, above the 170 rule. It reads periwinkle in the Blender preview, which is expected before Roblox darkens it. Re-check it in the Studio game view at the clip gate.
- **Hard rules pass.** Studs cover the body, plates and claws are smooth, nothing glows, and the tris are well under the cap.
- **Accepted deviations** (each is better than the plan):
  - No snow chest V. Correct, but the muzzle has the same problem (MUST 5).
  - BROW on the fists and feet gives value contrast, like Raiju's dark paws.
  - Elbow at 0.50H gives ape proportions.
  - POLAR_NAVY is darker than the plan's value, same hue.
  - No pale underside. The plates carry the pale, but that is only acceptable if the one accent works (MUST 6).

## Answer to the builder's doubt

It is still a blocky ape. The navy chest is a bean with no pectoral or belly form. The arms are sleeves. The feet are cubes. The fists read as robot faces. The muzzle reads as a grin. The build is in the same family as LavaGolem (box sleeves, box fists, knuckle walk), and the tapering in MUST 2 and 3 is what separates the two.

---

## MUST (in priority order)

1. **Fists read as robot faces (front view, both fists).** A pale horizontal slit with a cyan dot sits on each dark fist. Cause: three knuckle plates across the fist front, with an AURORA seam on the middle one (L173-178).
   - Move the three plates to the top edge of the fist: plate centre z +0.055 becomes +0.105 (same x, y). Keep the fist front smooth BROW.
   - Drop the seam on the middle plate (`seam_edges` for i == 1).
   - Test: the front view shows no pale slit on either fist.

2. **Arms are straight tubes, and the forearm is wider than the upper arm** (L167-168). Upper arm radius 0.145 to 0.15; forearm 0.165 to 0.17.
   - Upper arm: 0.17 at the shoulder down to 0.14 at the elbow, rnd about 0.5 (bicep bulge).
   - Forearm: 0.15 at the elbow down to 0.10 at the wrist (top about 0.70). The wrist should be about 0.65-0.70 of the elbow width.
   - Fist radius 0.13 stays.

3. **Legs are box knees and calves are tubes; the feet are boxes** (L202-209).
   - Thigh (L202) is 0.17 at the hip and 0.19 at the knee, so it is widest at the knee. Change to 0.19 at the hip and 0.15 at the knee, rnd about 0.5.
   - Shin (L204) is 0.13 to 0.14, widest at the ankle. Change to 0.14 at the knee and 0.10 at the ankle, with a calf bulge.
   - Foot (L205) is a BROW box 0.13 x 0.18 x 0.06. Make it a wedge tapered toward the toe, with three rounded toe blocks (about 0.04 radius) and the black claws kept.
   - Test: the foot outline from above is a wedge, not a rectangle.

4. **Chest front is one plain navy barrel** (torso table L34-40, tubes L110-111). Add form in navy (no colour change).
   - Two pectoral masses at about (±0.13, -0.24, 1.13), half size about 0.12 x 0.09 x 0.10, rnd about 0.5, studded.
   - One abdominal mass at about (0, -0.12, 0.98), half size about 0.14 x 0.06 x 0.08, rnd about 0.5.
   - Expect about +1 to 2k tris, still well under 10k.

5. **The white muzzle and fangs read as a grin with teeth, or a bib** (muzzle L134 SNOW; fangs L157-160 IVORY, 0.14 long). The same failure as the chest V.
   - Muzzle SNOW (232,240,248) becomes POLAR_NAVY (108,116,196). Keep the BLACK nose.
   - Fangs IVORY shorten from 0.14 to 0.10 (L160), keep the colour.
   - A dark snout with two short fangs reads fierce. SNOW share goes to 0, which the notes already accept.

6. **The one accent does not show.** AURORA is 1.1 % of the side view and no green is visible at 64 px or in the close-ups. The seams are too thin (0.012H).
   - Widen the seam inlays to about 0.02H.
   - Run one seam the full length of each shoulder crust's lower edge (crust code L180-187), not short pieces.
   - Keep the hump sheet seams (L115-128).
   - Target: AURORA at least 3 % of the side view, and green visible in the 64 px strip. Colour stays AURORA (120,240,160).

7. **A pale slab peeks above the skull** (`close_front.png`, top centre, above the brow). It reads as a white cap. The most likely source is the hump ice sheets (L115-128), especially the z 1.30 sheet. Hide that sheet and re-render to confirm.
   - If confirmed: lower the z 1.30 sheet by 0.05 (or tilt it back to 20 degrees) so its top does not rise above the skull top.

## NICE (do these too)

- **Brow V (L139):** narrow each wing (half width 0.114 to about 0.095) so the V does not read as a visor across the whole skull.
- **Skull (L132):** widen from 0.205 to about 0.22. The head is about 45 % of the shoulder crust width and looks like a bump under the hump.
- **Belly and lower legs:** one step darker, for example (92,100,178), so the mass shades instead of reading as one flat print. Keep the stud pitch.
- **Shoulder crust spikes (L180-187):** trim to two spikes per crust. At 128 px the third icicle makes the shoulder look horned rather than slabbed.
- **Distinctness from LavaGolem:** MUST 2 and 3 (tapered arms, rounder fists, tapered legs) should separate them. Keep the skid act (not a chest beat or a pound) as the Yeti's own motif.

## Pass / fail checklist (model gate)

| Check | Result |
|---|---|
| 64 px silhouette: species reads as hunched ape/yeti | PASS |
| 128 px strip: pale shoulders and dark head read | PASS |
| 128 px strip: accent reads | FAIL (MUST 6) |
| Upper face fierce: slits under a heavy brow, no round eyes, no glint, no smile | PASS |
| Muzzle and fangs fierce, not a grin | FAIL (MUST 5) |
| Real anatomy, tapered limbs | FAIL (MUST 2, 3) |
| Fists and feet are not boxes or faces | FAIL (MUST 1, 3) |
| No box belly; belly line rises in side view | PASS in side view, PARTIAL in front (MUST 4) |
| Not cute, not a plastic slab | PARTIAL (boxy limbs) |
| Dark body + ONE accent (no pale underside, accepted) | PARTIAL (accent FAIL, MUST 6) |
| Body colour rule: brightest channel 170 or more | PASS (196) |
| Studs everywhere, details smooth | PASS |
| No glow, no Neon | PASS |
| Tris 15k or under | PASS (5,076) |
| Floating, poking or intersecting parts (visible parts) | PARTIAL (slab above skull, MUST 7) |
| Parts visible from below | NOT CHECKED (no underside render supplied) |
| Tier fit: big, below Roc, Titan and Absolute Zero, above Mammoth on presence | PASS on ranking, PARTIAL on finish |
| Distinctness: no sibling copy | PARTIAL (LavaGolem build family; colour and plates separate it) |
| Clip gate | not judged this round |

## Next round (send all at once)

- `_model_sheet.png`, `_close_sheet.png` (front, side, tq).
- `_icons_strip_64.png` and `_icons_strip_128.png` next to IceMammoth, BrambleBadger, LavaGolem, Kappa, SeaTurtleWarrior and Treant.
- Flat palette shares (side, tq, game) for the new values.
- A low-angle front view and a belly-up view (for the "visible from below" check).
- The clip gate only starts after the model is at 8/10 or better.
