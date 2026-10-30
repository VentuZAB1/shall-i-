PASS

# Round 2 re-review: PASS (independent reviewer, 2026-10-14)

I imported the re-exported `C:\cdimp\Halloween_StreetLamp.fbx` fresh and re-rendered every round-1 view with my own `rv.py`. The light points were moved to the new NOTES positions (the head hangs 0.26 lower). All renders, crops (`z_*`), `stats.json` and `clearance.json` are in `review_check\round2\`.

## Round-1 items, verified myself
- **MUST 1, face in daylight: FIXED.**
  - At true 1080p, 40 studs (`z_E02_face`) and at 25 studs (`z_D12_head`, `z_D01_head`), the eyes, nose and grin read as solid pale shapes with dark rind frames. They are no longer outlines.
  - The face still reads with the inside light OFF (`D15`).
  - At night it glows clearly (`z_E05_face`, `N03`, `N05`).
- **MUST 2, web ladder and comb: FIXED.**
  - It is now an even radial orb web, with no parallel-rung runs at 10, 25 or 40 studs (`D10`, `C08`, `z_D12_head`).
  - The comb stubs are replaced by one draping thread.
  - The strands are now silvery grey.
- **NICE items:**
  - 1, the base: now a clean round ogee bell with crisp web-relief panels (`E03`, `C13`).
  - 2, the hat: reads as a witch hat side-on and in silhouette (`D10`, `z_S01`).
  - 3, the twist: iron-toned in daylight (`E01`).
  - 4, the candle: amber, no white chip.
  - 5, the straps: much smoother (`D08`).
  - 6, the web material: done.
  - 7, the normal map: the flute fade is clean (`C14`).
  - 8, WebSilk: one embedded image is accepted. The `.00x` copy is only the Blender importer's.
  - 9, market-deck note: in NOTES.
- **Budgets and pivot:**
  - 13,798 tris, with Post (5,704) the largest object.
  - Pivot at the ground, min z -0.01; height 18.55; footprint 2.13.
  - All textures are packed at the briefed sizes.
- **New problems: none.**
  - The only contacts are by design: the web tie to chain link 1, the ring in the hook cradle, the pumpkin on its saucer, and the web anchors on the iron.
  - The new hat and spear don't touch the web (`clearance.json`).
  - The lowest point is 11.866, which still clears walking players.

**Owner-facing impression:** this is a tall, elegant, clearly Halloween cast-iron crook lamp: crook curl, bat, web, witch-hat cage and a carved face that reads by day and glows by night. It sits at the quality of the giant head and the pumpkin eggs, and I see nothing an owner would call low-poly or cheap at gameplay distance.

## MUST
None.

## NICE (optional polish, not blocking)
1. At 8 studs or closer, each strap still has one slight corner where its under-loop turns into the bottom collar (`z_C07_straps`). Add 2 rings there if any budget is left.
2. At 4 studs or closer, the twisted lobes end slightly ragged where they meet collars 1 and 2 (`C14`).
3. Notes for the lead (Studio, not the model):
   - **Jumping under the lamp:** with the default JumpHeight 7.2, a player jumping directly under the hanging axis reaches about 12.2-12.4. Their head briefly passes through the drop finial (11.87) and grazes the pumpkin bottom (12.28). This is harmless with CanCollide off.
   - **Ground light on the pole:** at night the 110° ground SpotLight also warms the lower pole and the twist (`N05`). Narrow it to about 90° if the iron should stay cool.

---

# Round 1 (superseded): verdict FIX

I imported `C:\cdimp\Halloween_StreetLamp.fbx` fresh in headless Blender 5.2 and rendered it at stud scale. Day shots have the inside light on; night uses the builder's calibrated Moonlit values. All renders and `stats.json` are in `review_check\` (script: `rv.py`).

## What passes
- **Halloween read and silhouette:** strong side-on from the path at 25 and 40 studs (`D03`, `S01`). The lamp is tall and elegant, the shepherd's crook and its curl read clearly, the bat reads against the sky, and the caged pumpkin hangs correctly.
- **Night:** the face glows clearly at 25 and 40 studs (`N05`, `E05`).
- **Faceting:** none visible at 12-40 studs on the pole, crook, pumpkin or cage.
- **Pumpkin bake:** clean. No dark rims or black patches, and all 4 holes are clean (albedo-only check: `C01`, `C02`).
- **Iron:** cool near-black, not flat black. Albedo mean is (46, 47, 53), with real edge wear and rust.
- **Pivot and proportions:**
  - The pivot is at the ground (min z -0.01) and all 5 objects share the origin.
  - Height is 18.55 and the footprint 2.13.
  - The head bottom is at 12.06, so a 5-stud player clears it easily.
- **Budgets:** 13,910 tris in total, with Post (5,716) the largest object.
- **Textures:** sizes match the brief and all are packed. Texel density is about 119 px/stud on the Post, 109 on the Cage and 149 on the Pumpkin.
- **Expected staging, not a fault:** the dark stair-step patches on the base in `D11` and `wip\rv_base_5` are EEVEE shadow-terminator artefacts. They disappear with sun shadows off (`E03`).

## MUST (blocking)
1. **The face does not read in daylight; it looks drawn on.**
   - **Evidence:**
     - At true 1080p, 40 studs, face turned to the camera and inside light on (`E02`, crop `z_E02_face.png`): the holes fill with the same orange as the skin.
     - Only the pale knife walls show, as thin khaki outlines, so the eyes and nose almost vanish. `z_D12_head` at 25 studs shows the same.
     - The cause: under the `ff963c` light (and the baked AO), the inner flesh (234, 169, 85) renders the same hue as the skin and only slightly brighter. The pale cut walls then outshine the fill.
   - **Fix (texture only, 0 tris):**
     - (a) Make the inner wall and the cavity ceiling (what players see through the holes from below) a pale warm yellow, about sRGB (250, 215, 140).
     - (b) Cut the AO strength of the inner bake group from 0.5 to 0.2 or less.
     - (c) Bake a dark rind band, 0.03-0.04 wide, on the skin side of every outer knife edge, about (120, 45, 10). Each hole then gets a dark frame instead of a pale outline.
     - (d) Keep the cut walls no brighter than the new fill.
   - **Accept when:** day renders at 25 and 40 studs, 1920x1080, vFOV 70, face turned to the camera, show:
     - the eyes, nose and grin as solid shapes;
     - a hole fill at least 1.4x the luminance of the skin next to it.
   - **For the lead:** if the face is still soft in Studio, raise the daytime inside PointLight Brightness.
2. **The web reads as a ladder and a comb**, which PLAN_REVIEW MUST 5 forbids.
   - **Evidence:** `D10`, `C08` (clay), `z_D12_head`, `z_E02_face`.
     - The sectors between the hub and the pole are about 40° wide.
     - So 6-7 straight catch-ring spans there run parallel, like rungs.
     - The lower catenary carries 5 short vertical stubs, like a comb.
   - **Fix (tri-neutral):**
     - Split every sector wider than about 30° with an extra spoke (about 2 spokes). Fan the pole anchors at least 35° apart (one near the volute or collar 3, one at the z 13.3 anchor).
     - Space the rings geometrically, closer near the hub (about x1.25 per ring).
     - Replace the 5 stubs with 1-2 longer loose threads (0.5-0.9) that drape and curl. The deleted stubs pay for the new spokes.
   - **Accept when:** the +X renders at 25 and 40 studs show no group of 4 or more parallel spans.

## NICE (the owner wants perfect; do these too)
1. **Soft, lumpy bell base at 6 studs or closer** (`E03`, `C13`, `D11`): it looks like a sack, and the gothic panels are smudged.
   - Make the bell a clean round ogee lathe: 32 sides in the lo, plus 2-3 profile rings at the ogee.
   - Make the panels crisp normal-map detail: bake at 2048 and box-filter to 1024, or give the base island about 1.6x texel priority.
   - Pay the tris by keeping only the end rings on straight pole runs.
2. **The witch-hat cap reads as a flat coolie or pagoda lampshade from the side** (`D10`, `C12`).
   - Raise the cone to about 0.65-0.7, with a concave flare and the spear tip bent 25-30°.
   - Keep the lowest point at 11.8 or higher (shorten the drop finial if needed) and the stem clearance at 0.30 or more.
3. **The twist reads as copper or bronze at 12-25 studs** (`E01`, `D03`, `N05`). That is more than "a hint of rust".
   - Keep the rust in the grooves only, and keep the bright wear on the crests.
   - Target a twist albedo mean within ±10% of the pole's iron.
4. **In daylight the candle top shows as a white chip or tooth in the mouth** (`D07`, `D14`, `E04`).
   - Use amber wax with a soot ring round the wick, or set the candle about 0.08 lower.
   - Keep the flame visible through the mouth at night.
5. **The straps kink where they curl under into the bottom collar, and the bottom collar is an octagon** (at 8 studs or closer: `D07`, `D08`, `C11`).
   - Add 2-3 rings at those bends and give the collar 12 sides (about +120 tris; pay from NICE 1).
6. **At 8-12 studs the web looks like uniform white PVC tubing** (`D08`, `D10`).
   - Take the strands one step greyer and silvery, about (205, 207, 214), dusty near the iron.
   - Taper the rings to 0.085-0.09 near the hub.
   - Let a larger WebSilk hub patch carry the pale mass.
7. **Normal-map faults at about 4-6 studs** (`C14`):
   - a sawtooth fade where the lower flutes meet collar 2;
   - a smear on collar 2's top edge.
   - Ramp the flute fade smoothly in the bake source and check the seams of the collar islands.
8. **The WebSilk colour map is embedded twice** (`.001` to Base Color, `.003` to Alpha). Feed the Alpha from the same image node, so the FBX carries one image.
9. **Lead note:** the front (-Y) silhouette is a lollipop (`S02`). At the 2 market-deck spots, turn each lamp so its arm reaches across the main line of sight, as on the paths.
