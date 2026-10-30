# StreetLamps PLAN review (plan reviewer, 2026-10-13)

**Verdict: APPROVED WITH CHANGES.**

The plan is strong and buildable. The pipeline lessons are applied correctly: the same cutter carves hi and lo, planar caps, `repair_attrs`, the 4-hole check, per-part bake groups, CONVEX packing, and a re-import verify. The changes below are about the read at 25-40 studs from where players actually stand.

Per `LEAD_INTEGRATION.md`, the arms reach ACROSS the paths. So players walking a path mostly see the lamp's side (Blender ±X), and a -Y face is nearly edge-on to them.

Lead rulings:
- (1) The saucer seat is OK.
- (3) ~18.3 total is OK. Up to 18.6 is acceptable after the changes below.
- (2) The bat: see MUST 2.

## REQUIRED (MUST)
1. **The arm must read as a curled shepherd's crook, not an L-bracket.**
   - Replace "quarter bend r 1.05 + a 2.3-stud near-straight arm + a small C-hook" with one continuous sweep. From collar 3 the bar arcs over (a half-ellipse; apex at y ≈ -1.6 to -1.9, bar centre z ≤ 17.6) and comes down into the hook.
   - No stretch of the bar may have a curvature radius over ~4 studs.
   - The end curls back toward the pole into a hook/scroll ≥ 0.9 stud across that wraps ≥ 220°, ending in the ball knob. The ring hangs in its cradle at y ≈ -3.55.
   - Keep the volute in the upper inside corner.
   - Check it in `preview` with a flat-black silhouette from +X at 40 studs.
2. **Bat ruling: turn it 90°.**
   - The wings spread along the arm (Y-Z plane), and the bat perches ACROSS the bar (feet side by side, a natural perch). The body faces +X, with the head turned ~30° down toward the path.
   - Path walkers then see the full silhouette against the sky. From the front it becomes a narrow upright figure, which is fine.
   - Wingspan 2.0-2.2 (1.7 is ~33 px at 40 studs).
   - Keep the dihedral, the jagged fingers and the fangs.
3. **Bigger pumpkin, bolder face.** At 40 studs in 1080p the scale is ~19 px/stud.
   - Pumpkin: R 1.12 → ≈ 1.35 (width ≈ 2.7, Rz ≈ 0.96). Re-offset the straps and keep the 0.30 rule.
   - Eyes ≥ 0.65 wide. Nose ≥ 0.28.
   - Mouth ≥ 1.8 wide and ≥ 0.45 open at the centre.
   - 2 top teeth + 2-3 bottom teeth, each ≥ 0.22 wide, leaving ≥ 0.2 open between each tip and the opposite edge.
   - Why: the planned grin is 0.26 tall with 0.12-0.14 teeth. That leaves 0.09-0.14 slivers, a 2-px zigzag at 40 studs (the DeadTrees "mouth slivers" lesson).
   - Keep the head bottom ≥ 11.8: use a ring + 2 links, or lift the crook.
4. **The Pumpkin must turn in 90° steps about the hanging axis without clipping.** This is almost free, because the cage and ribs repeat every 90°.
   - The stem lean must stay inside the cap clearance at all 4 angles. Run the BVH clearance check at all 4.
   - Keep the candle centred.
   - NOTES: the rotation recipe.
   - Add `review_day_25_side_face.png`: camera at +X, pumpkin turned to face it.
   - Advice to the lead: on path spots, turn the face ALONG the path toward the plaza.
5. **A web big enough to read.** The DeadTrees lesson: webs 3.4-3.8 studs across failed at 40 studs.
   - Fill the crook under the new arc: span ≥ 3.3 (Y) x ≥ 4.0 (Z), with the lower pole anchor down to z ≈ 13.3.
   - ≥ 10 spokes and ≥ 7 catch rings (or a true spiral), so it can't read as a fan or a ladder.
   - Every strand ≥ 0.085 thick. The planned 0.076 rings are under the brief's 0.08 floor.
   - Raise the Web cap to ≤ 1,500 tris. Hold the 14,000 total: straight pole runs need only end rings, drop a chain link, feet ≤ 900.
6. **A twist that reads.** ±12 % (±0.03 stud) on a 0.27 bar is ~1 px at 25 studs.
   - Use ≥ ±20 % (a true twisted square-bar profile).
   - Put edge wear along the helix crests, so the twist shows as light/dark spiral bands at 25 studs.
7. **Review lighting must match the game.**
   - (a) Night: the in-game night is a bright moonlit blue. Calibrate so a plain green plane and a cream patch match `previews\night\A_Moonlit.jpg`: green ≈ (93,159,88), cream ≈ (184,177,185). The planned (0.02,0.028,0.06) world oversells the glow. Keep a darker version only as an extra.
   - (b) Day: the inside PointLight is ON in daytime too (Range 11, Brightness 1.2, ff963c, shadows). Light the day shots with an equivalent light.
   - (c) Add a **ground-pool light** attachment just under the bottom collar: a downward SpotLight, ~110°, Range ~16, warm, no shadows. The closed pumpkin sends almost no light onto the path, and a street lamp that doesn't light its street looks fake. Show it in `review_night_25.png`.
8. **NOTES: roughness fallback.**
   - `verify` confirms a roughness image is packed for every part.
   - NOTES lists `maps\<Part>_rough.png` and says to set `SurfaceAppearance.RoughnessMap` by hand if the import drops it (it did for the Spider).

## Recommended (NICE)
1. A witch-hat cap that reads as one: rim r ≈ 0.85, height ≈ 0.7, tip bent 20-30° back. The planned cap is 0.38 tall and is lost at 40 studs.
2. Make the top finial a flat spear-head pierced near its base for the link, not a wire loop. It reads as the brief's "spike finial" and still hangs correctly.
3. A slightly chunkier lower pole (r 0.29 tapering to 0.22) for the stylized world. Flutes 0.03 deep, so they show in the normal map at 15-25 studs.
4. Per-part metalness PNGs (edge wear = 1, paint = 0) for a hand-set `MetalnessMap`. The worn edges then glint like iron, not grey paint.
5. Check the web against the bright sky in the side renders. If the silver-white washes out, take the strand base one step greyer (≈ 205,205,210) and let the silk carry the pale mass.
6. Also shoot the 3-lamps-on-a-path view at night. The rhythm of glowing faces down a path is the selling shot for the owner.
7. NOTES: ready collider sizes (cylinder r 0.3 x 16 + a base box), so the Post never needs a hull.
