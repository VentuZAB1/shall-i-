# HubGrime PLAN review (plan reviewer, 2026-10-13)

**Verdict: APPROVED WITH CHANGES.**

This is an excellent plan. numpy painting is the right tool for colour + alpha decals. These parts are all exactly right:
- the stud logic (opaque = on the surface, glaze = in it);
- straight alpha with push-pull bleed;
- the periodic MossBase with a shared seam band;
- the frequency budget and the 1/8 thumbnail test;
- calibration to the real screenshots, and before/after pairs.

The changes cover Roblox sampling and sorting traps that the Blender preview would hide, plus two taste risks.

Lead rulings:
- (1) The hub walls are blue (96,132,170). Orange stays only as a swatch-sheet robustness check.
- (2) Drips go mostly on walls without garlands, ≤ 1 per 3 back-wall bays. Confirmed.
- (3) MossBase as a tiled Texture on a carrier: confirmed. The files must also work as plain Decals.

## REQUIRED (MUST)
1. **No visible edge may carry content (texture wrap).** A Roblox `Texture` wraps in U and V. Decals whose content touches an edge can also show a hairline on the opposite edge.
   - Rule: every edge that must meet geometry gets a **hidden overlap band**: the content runs ≥ 0.25 stud past the contact line, then a ≥ 4 px transparent margin. This applies to the MossBase bottom, the W_Crack_C bottom and the W_Drip top.
   - NOTES tells the lead to sink that band 0.25 below the floor top (MossBase, W_Crack_C), or up behind the trim (W_Drip; the trim sticks out 0.3).
   - Only the MossBase left/right edges carry content to the edge (U tiling).
   - Previews: set the image extension to REPEAT, as Roblox does. Add a 2x2 wrapped tile + naive-mip strip to `fringe.png`. `checks.json` verifies the margins.
2. **MossBase run ends.** A run cropped in open wall cuts through cushions with a hard vertical edge, which looks like a sticker.
   - Add two small end caps, `W_MossBase_EndL` / `W_MossBase_EndR` (≈ 6 x 6 studs, 256 x 256). The inner edge is the shared seam band; outward, the moss fades out by density. Flag the 2 extra names to the lead.
   - NOTES: every run ends exactly on a seam (Decal chaining, or a Texture length + OffsetStudsU chosen for it). Cap both ends unless the end sits against a pillar, corner or prop.
3. **Overlaps must not depend on draw order.** Roblox sorts transparent surfaces per part, so the order of two overlapping decals on different carriers can flip with the camera. Eevee's DITHERED mode hides that.
   - Render the mocks with BLENDED (per-object sort), and capture every overlapping pair in both orders.
   - Design: W_Crack_C's foot carries its own moss in the MossBase palette, so crack-over-moss and moss-over-crack both look right.
   - NOTES rule: overlaps only as "stain under anything" (low-alpha darkening is order-safe); never a crack over moss. `Decal.ZIndex` only orders decals on the same carrier face.
4. **Moss quality gate.** The metaball cushions must not read as green bubbles, blobs or camo paint.
   - Break the whole surface into micro-clumps, with lit-tip stipple on the light side, like the Graveyard moss in `review_close_Grave_A.png`.
   - The contour is tufted and irregular. No uniform dark stroke: "2 px outline" means a crisp alpha edge only.
   - Gate after the moss family: a 6-stud close-up and a 25-stud crop, side by side with the Graveyard moss.
   - If it reads as blobs, switch to the planned Blender displaced-moss render BEFORE making MossBase.
5. **The bevel light must not become a pale outline.** In-game the green is already ≈ (176,221,160), so a continuous pale rim reads as a sticker halo.
   - W5/W6 on green and blue: one side only, broken (≤ 50 % of the crack length), ≤ 0.1 stud wide, alpha ≤ 0.3 on the floor.
   - Check it in `floor_close6_day` and in the 25-stud crops on green and blue.
6. **Housekeeping.**
   - The set is **15** textures (8 G_ + 7 W_), not 14. Fix the counts, and run every check on all 15 plus the end caps.
   - Apply the alpha-0 floor (step 3) AFTER the dither (step 7), so the dither can't re-create invisible fog over the carrier.

## Recommended (NICE)
1. Make `wall_eye25_night_candle` a warm light pool on a floor cluster: the new street lamps will light grime at the path edges.
2. Half-resolution (960 x 540) copies of the 25-stud renders, as a phone check for moiré and noise.
3. Keep the moss halos (W1) at ≤ 0.3 alpha and irregular, so moss on blue doesn't sit in a dirty ring.
4. Cracks on cream: also suggest Decal.Transparency 0.1-0.15 (ΔE 73 there), not only for stains.
5. Also write the owner test patch as a small JSON (texture, carrier size, CFrame relative to the bay), so the lead places it exactly.
6. MossBase is 42.7 px/stud. Add a 4-stud shot from the third-person camera to `wall_close8_day`, and keep every painted feature ≥ 3 texels.
