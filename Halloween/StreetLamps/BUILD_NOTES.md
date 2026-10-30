# BUILD NOTES: what changed for each PLAN_REVIEW item (2026-10-14)

All numbers come from the final full-resolution run (`build.json`, `web.json`, `export.json`, `verify.json`, `calib.json`). Every review image is rendered from the **re-imported FBX** (`C:\cdimp\Halloween_StreetLamp.fbx`).

## MUST

### 1. A shepherd's crook, not an L-bracket: DONE
- **Change:** the plan's quarter bend + straight arm + small C-hook is gone.
  - The bar is now ONE continuous curve. It is built from a curvature-versus-turned-angle function: two quarter-ellipses (a1 = b1 = 1.8, b2 = 1.2) blended into an inward log spiral, then integrated, so the curvature is continuous (G2).
  - The second ellipse width (a2 = 2.461) is solved by bisection, so the ring's cradle lands exactly at y -3.55.
- **Shape:**

  | Check | Built | Target |
  |---|---|---|
  | Apex | y -1.873, bar centre z 17.58 | y -1.6 to -1.9, z ≤ 17.6 |
  | Largest bend radius | 3.93 | ≤ 4 |
  | Curl | 0.95 across, wraps 285°, ball knob r 0.088 | ≥ 0.9 across, ≥ 220° |
  | Cradle | y -3.55, z 15.872 | y about -3.55 |

  - The bar tapers 0.215 → 0.172 at the apex → 0.097 in the cradle → 0.086 at the knob, with a bead swell.
- **Volute:** kept in the upper inside corner as a log spiral (600°, r 0.80 → 0.12). Its centre and start radius are solved so the outer coil touches the bar near the pole.
- **Silhouette check:** a flat-black +X silhouette at 40 studs, `wip\pv_silhouette_side_40.png`. It reads as a shepherd's crook with a curl, bat, web and caged pumpkin.

### 2. The bat turned 90°: DONE
- The wings now lie in the Y-Z plane, spread along the arm:
  - 15° dihedral, 12° sweep toward +X;
  - jagged finger tips with concave scallops;
  - ridged membranes in the bake source.
- **Wingspan 2.06** (target 2.0-2.2).
- It perches across the bar at the apex: two feet side by side wrap over the bar. The game mesh and the bake source now share one foot path.
- The body faces +X; the head is turned 30° down toward the path. It has fangs and ears.
- Wings vs bar: 0.05 gap.
- See `wip\rv_crook_8.png` and `review_day_25_side_face.png`.

### 3. A bigger pumpkin and a bolder face: DONE

| Feature | Plan | Built | Target |
|---|---|---|---|
| Pumpkin radius | R 1.12 | **R 1.35, Rz 0.96**, width 2.73 (max radius 1.39) | R about 1.35 |
| Eyes | | **0.66** wide x 0.48 (slanted, scowling) | ≥ 0.65 |
| Nose | | **0.32** x 0.28 | ≥ 0.28 |
| Mouth width | | **1.91** | ≥ 1.8 |
| Mouth opening at the centre | | **0.50** | ≥ 0.45 |
| Top teeth | | 2, **0.26** at the root (0.22 at mid-height) | ≥ 0.22 |
| Bottom teeth | | 2, **0.24** at the root | ≥ 0.22 |
| Open gap, tooth tip to opposite lip | | 0.27 (top), 0.22 (bottom) | ≥ 0.2 |

- The straps were re-offset to match. Skin to cage is ≥ 0.327 (rule 0.30).
- Head bottom: the chain is a ring + 2 links. The pumpkin bottom is at 12.538, and the lowest point (drop finial) is at **12.061** (target ≥ 11.8).

### 4. The pumpkin turns in 90° steps: DONE
- The straps are the outward offset (0.36) of the pumpkin's max-radius envelope. That envelope is computed from the skin field over **all** azimuths, so it does not care how the pumpkin is turned.
- BVH clearance at all 4 angles:
  - skin to cage **0.3274** at 0°, 90°, 180° and 270°;
  - stem to cap **0.338** at each angle;
  - the stem lean scale is 0.35, so it stays inside the cap.
- The candle is centred; the wick tip is 0.03 off the axis.
- **NOTES:** the rotation recipe is in `NOTES.md`: a Luau function that turns about the Cage centre.
- **Renders:** `review_day_25_side_face.png` (+X camera, face turned to it) and `review_night_25_side_face.png`.
- **Advice to the lead:** turn each face along the path toward the plaza. This is in NOTES.

### 5. A web big enough to read: DONE

| Check | Built | Target |
|---|---|---|
| Span | **3.32 (Y) x 4.38 (Z)** | ≥ 3.3 x ≥ 4.0 |
| Lower pole anchor | z **13.30** | z about 13.3 |
| Spokes / catch rings | **11 / 7** | ≥ 10 / ≥ 7 |
| Strand thickness | 0.124 spokes and frame, 0.114 rings; even the 3-sided strands are ≥ 0.085 across their narrowest | ≥ 0.085 |
| Web tris | **1,284** | cap 1,500 |
| WebSilk tris | 284 | |

- The web fills the crook under the new arc.
- The pole anchors tuck 0.025 into the pole, so the silk looks wrapped on with no gap. The other end ties to chain link 1.
- Extras: a sagging catenary lower edge, loose threads, a hub blob, and a silk gauze and drape (alpha) on 3 islands.

### 6. A twist that reads: DONE
- Old twist: ±12 %. New twist: **±21 %**.
  - It is a true twisted square-bar profile, `cos(4θ)^0.75`, with pitch 1.0, between two riveted collars (z 6.40-7.90).
  - Bright edge wear runs along the helix crests, and rust sits in the grooves. It shows as light/dark spiral bands at 25 studs (`review_day_25.png`; close-up `wip\rv_twist_4.png`).

### 7. Lighting matches the game: DONE
- **(a) Night:** calibrated against `previews\night\A_Moonlit.jpg` with plain green and cream patches. The fit keeps its best iteration.

  | Patch | Measured | Target |
  |---|---|---|
  | Green | (96, 159, 92) | (93, 159, 88) |
  | Cream | (184, 177, 184) | (184, 177, 185) |

  - The sky the camera sees is dark blue with stars.
  - The moon sun carries 38 % of the light.
  - The scene stays clearly readable with true colours.
  - The darker variant exists only as an extra (`wip\rv_night_dark_variant_25.png`).
- **(b) Day:** every day shot has the inside point light ON. It is the warm `ff963c` PointLight analogue, with shadows, at the suggested PointLight point.
- **(c) Ground pool:** a downward SpotLight at the **ground-light attachment** (0, -3.55, 12.306), just under the bottom collar: 110°, warm, no shadows. The NOTES give Range 16.
  - It is visible as the warm pool on the path in `review_night_25.png`, `review_night_25_side_face.png` and `review_night_path_3lamps.png`.

### 8. Roughness fallback: DONE
- `verify` re-imports the FBX and confirms each part's images are packed and linked:
  - Post, Cage and Pumpkin: albedo, normal and roughness;
  - Web: albedo and roughness;
  - WebSilk: albedo with alpha.
- NOTES lists `maps\<Part>_rough.png` for setting `SurfaceAppearance.RoughnessMap` by hand.

## NICE

| # | Item | Status |
|---|---|---|
| 1 | Witch-hat cap | DONE, with a caveat: rim r 0.84, cone 0.41, plus a 0.34 spear tip bent **25°** toward the pole, about 0.74 tall in total. From below (the players' view) it still reads mostly as a lantern cap. |
| 2 | Spear-head finial | DONE: a flat spear-head 0.05 thick, pierced near its base. Link 2 hangs through the hole. |
| 3 | Chunkier lower pole | DONE: r 0.29 → 0.22, 12 flutes 0.03 deep (carried by the normal map). |
| 4 | Metalness PNGs | DONE: `maps\Post_metal.png` and `maps\Cage_metal.png`, baked from the bake source's edge-wear attribute (wear = 1, paint = 0). Not embedded; set by hand. |
| 5 | Web greyness | CHECKED: the strands (base 214, 216, 222) do not wash out against either sky. They read clearly on the night sky and the grey day sky, so no change was made. |
| 6 | 3 lamps at night | DONE: `review_night_path_3lamps.png` (plus the day version). The pumpkins are turned to look down the path. |
| 7 | Collider sizes | DONE in NOTES: a cylinder (16 x 0.6 x 0.6) on the pole axis, spanning 2-18, plus a base block 2.0 x 2.6 x 2.0. |

## Changes after my own review of the first (fast) build
- **Ground-pool spot:** it was invisible, so its strength was raised. The pool now reads on the path at night.
- **Straps:** they were faceted up close. They now use more samples along their length (max segment 0.36 → 0.22, sag 0.005 → 0.004).
- **Round parts:** the cap went from 20 to 28 sides, the top ring from 16 to 24, and the saucer from 16 to 20. The pumpkin game skin went from 48 x 16 to 48 x 18.
- **Budget savings to pay for that:**
  - candle 16 x 9 → 12 x 8;
  - wax puddle 12 → 8 sides;
  - web spoke and frame segments longer, and ring 4 in one segment;
  - two fewer base profile rings;
  - 4-sided toes.
- **Pumpkin shading:** the Skin and Inner shells now carry the smooth normals of the UNCUT shell. The boolean slivers round the face holes no longer bend the shading, and the normal map round the face is cleaner.
- **Night calibration:** it now keeps its best iteration (error 8 vs 9).
- **Bat bake:** the game mesh and bake source share one foot path, and the rays are longer. Misses went from 14 % to 11.6 %; see the known limitations in NOTES.

## Final numbers

| Object | Tris |
|---|---|
| Post | 5,716 (column 2,760, feet 848, crook 1,168, volute 468, bat 472) |
| Cage | 3,016 |
| Pumpkin | 3,610 |
| Web | 1,284 |
| WebSilk | 284 |
| **Total** | **13,910** (≤ 14,000; largest object 5,716 ≤ 8,000) |

- Height 18.546 (the lead's ruling allows up to about 18.6).
- Footprint 2.128 x 2.128.
- The iron reaches 4.175 from the pole axis.
- FBX: `C:\cdimp\Halloween_StreetLamp.fbx`, 5.9 MB, 5 meshes, textures embedded.

## Review images
- Top-level shots:
  - `review_day_25.png`, `review_day_25_side.png`, `review_day_25_side_face.png`, `review_day_50.png`, `review_day_path_3lamps.png`;
  - `review_night_25.png`, `review_night_25_side_face.png`, `review_night_close.png`, `review_night_path_3lamps.png`;
  - `review_close_head.png`.
- Detail shots in `wip\`:
  - `rv_crook_8`, `rv_twist_4`, `rv_base_5`, `rv_head_below12`;
  - `rv_day_40_front`, `rv_day_40_side`, `rv_day_25_back`;
  - `pv_silhouette_side_40`, `pv_silhouette_front34_40`.

---

# Round 2: what changed for each REVIEW.md item (2026-10-14)

The proofs are rendered from the **re-imported FBX** with the reviewer's own `review_check\rv.py`. `wip\rv2_measure.py` imports it read-only and only moves its light attachments to the round-2 positions. The renders and JSON are in `wip\rv2\`.

## MUST 1: the face reads in daylight. PASS
- **(a) Cavity colour:** the inner wall and the cavity ceiling are now pale warm yellow. The bake source is `mat_inner` (255, 232, 166) / (246, 212, 136); the baked colour-map mean of the cavity group is **sRGB (247, 220, 151)**.
- **(b) AO:** AO strength is now set per bake group.
  - cavity (LoInner): **0.08**, was 0.5;
  - knife walls: 0.15;
  - candle and wick: 0.3;
  - skin: 0.5.
- **(c) Rind band:** a dark rind band now frames every hole.
  - Each skin vertex of the bake source stores its distance to the nearest outer knife edge (`RimD`). The skin shader turns that distance into a crisp band: **(120, 45, 10)** at d < 0.028, fading out by 0.042.
  - The baked result: the darkest 2 % of skin texels average (97, 49, 16).
- **(d) Walls:** the knife walls are now a deeper flesh tone. Baked mean (211, 148, 70), below the fill.
  - Rendered, the walls are 0.36-0.38x the fill's luminance, so they no longer outshine it.
- **Measurement** (`wip\rv2\face_measure.json`):
  - day, 1920x1080, vFOV 70, inside light on (the reviewer's 40 W), pumpkin turned to the +X path camera;
  - each pixel is classed from a flat id render of the same camera, using the bake-group id map;
  - "fill" = cavity pixels seen through the holes, edge pixels dropped; "skin" = the skin 2-7 px outside every hole.

  | Distance | Fill sRGB | Adjacent skin sRGB | Ratio: luminance (linear Y) | Ratio: sRGB luma | Pass (≥ 1.4) |
  |---|---|---|---|---|---|
  | 25 studs | (200, 162, 133) | (163, 108, 65) | **1.98** | 1.44 | yes |
  | 40 studs | (200, 162, 133) | (161, 110, 72) | **1.93** | 1.42 | yes |

- **Crops:** `wip\rv2\z_F25_face.png` and `z_F40_face.png`. Eyes, nose and grin are solid pale shapes with dark frames; compare the reviewer's `z_E02_face.png`.
- **Also:** `D14_head8_side_faceturned.png` (day, 8 studs) and `N03_head8_side.png` (night).

## MUST 2: the web is no longer a ladder or comb. PASS
- **Spokes:** now 14, placed rather than random:
  - one to the top pole anchor by collar 3 and one to the z 13.3 anchor, **50°** apart;
  - one between those two;
  - the rest spread so that **every sector is 23.7-27.6°** (was up to about 40°).
- **Rings:** 7, spaced geometrically **x1.25 outward** (fractions 0.24 ... 0.92), so they sit closer near the hub.
  - Each ring's scale blends the spoke length with a reference, so the rings are rounder than the frame.
  - Where the frame comes close, the ring stops instead of bunching (21 chord ends dropped).
  - Every chord end gets an alternating +-2.8 % offset (+ a little noise). Chords over 0.6 long sag toward the hub. 2 chords are broken.
- **Proof** (`web.json`): measured on the chords themselves, the largest run of radially neighbouring spans in one sector within 4° of parallel is **1**. Round 1 had runs of 7.
- **Stubs:** the short stubs on the lower edge (the 2 short loose threads and the hanging broken-chord threads) are gone. Instead, **one long loose thread** (about 0.9) drapes from the lower edge and curls at its end.
- **Renders:** +X at 25 and 40 studs: `wip\rv2\D03_side25_default.png`, `D04_side40_default.png`, `D12_side25_faceturned.png`. Close: `D10_crook10.png`; clay: `C08_clay_crook12.png`.
- **Tris:** Web 1,110 (was 1,284), WebSilk 300.

## NICE
1. **Bell base:** DONE.
   - It is now a clean round ogee lathe with **32 sides** in the game mesh: convex shoulder, then an inflection, then a concave neck, with 3 more profile rings. The 4 raised ribs are gone.
   - The pole stays 24-sided, joined by a stitched band.
   - Gothic panels: the base island gets **1.6x** texel priority, and every part is now baked at 2x and box-filtered down. Normals are averaged and renormalised.
   - Tris paid for by keeping only the end rings on the straight pole runs.
   - See `wip\rv2\E03_base6_noshadow.png` and `D11_base6.png`.
2. **Witch hat:** DONE.
   - The cone is now **0.66** tall (was 0.41) with a concave flare into the brim, and the spear tip is bent **28°**.
   - The head hangs 0.26 lower, so the drop finial was shortened (0.275 -> 0.21). The **lowest point is 11.866** (≥ 11.8).
   - Stem clearance is still **0.338** at all 4 turns; skin to cage is 0.327.
   - See `C08_clay_crook12.png` and `D10_crook10.png`.
3. **Twist:** DONE. It now reads as iron, not copper.
   - Rust sits only along the deepest groove line. The crevice darkening in the grooves is reduced, and the twist albedo is lifted 20 % to offset the baked AO.
   - The crest wear is kept.
   - Measured on the FBX colour map (`twist_measure.json`): twist (47, 50, 56) vs plain pole (49, 51, 57).
     - sRGB mean ratio **0.97**, luminance ratio 0.95: within ±10 %.
     - The colour is neutral iron: R-B = -9.0 vs -7.9.
   - See `E01_base_3rdperson12.png`.
4. **Candle:** DONE. It is now amber wax with a dark soot ring round the wick, plus an amber puddle.
   - Measured by day at 25 studs: candle (167, 130, 96), darker than the fill. It no longer shows as a white chip.
   - The flame still shows through the mouth at night (`N03_head8_side.png`). The candle was not lowered.
5. **Straps and bottom collar:** DONE.
   - The strap sampling now also caps the real turning angle at 13° per segment, so the curls into the collar and the top ring have no kinks.
   - The bottom collar has **20** sides (was 16; the reviewer asked for ≥ 12). The drop finial has 14 (was 10).
   - See `D08_head8_34below.png`.
6. **Web material:** DONE.
   - Strands are one step greyer and silvery, base (205, 207, 214), dustier toward the iron (0.8 edge weight), with lower roughness (0.36).
   - Rings taper **0.085 -> 0.114** thick; spokes taper 0.088 -> 0.12. This holds the 0.085 floor for the 40-stud read.
   - The WebSilk hub patch grew from r 0.36 to **0.56**.
7. **Normal-map faults:** DONE.
   - **Flute fade:** the flutes now fade over 0.18 with a smootherstep in the bake source. The game pole is round and carries the flutes only in the normal map, so there is no sawtooth.
   - **Seams:** the column's UV seams moved to the lamp's back (+Y, away from the path), and the twist's seam into a groove. The column also has split normals at its real creases (416 edges).
   - **Remaining stripe:** the stripe on collar 2's lit edge in `C14` is an EEVEE shadow-terminator artefact, not a texture fault.
     - It sits at the light/shadow line and **vanishes with sun shadows off**: `wip\rv2\C14_nrm_mid_pole_noshadow.png`.
     - The hi bake source is clean there (`z_hi_c14.png`).
     - The normal map texels there are clean horizontal bands (`z_band_nrm.png`).
8. **WebSilk image:** CHECKED. The FBX embeds `WebSilk_albedo` **once**: the file holds 12 PNG streams for the 12 maps.
   - The Alpha socket is already fed from the same image node as Base Color.
   - The `.00x` copy appears only because Blender's FBX importer makes one image per texture link (colour and alpha).
   - Unlinking alpha would lose the silk's transparency in the FBX, so it stays. NOTES tells the lead to use the one ColorMap with AlphaMode Transparency.
9. **Market-deck note:** DONE in NOTES. At spots 7 and 8, turn each lamp so its arm reaches across the main line of sight.

## Round 2 numbers

| Object | Tris | Change |
|---|---|---|
| Post | 5,704 | was 5,716 |
| Cage | 3,184 | was 3,016 |
| Pumpkin | 3,500 | was 3,610: cavity shell 28 x 8, candle 10 sides |
| Web | 1,110 | |
| WebSilk | 300 | |
| **Total** | **13,798** | ≤ 14,000 |

- **Post breakdown:** column 3,064, feet 784, crook 1,000, volute 384, bat 472.
- **Savings that paid for the changes:**
  - crook sampling 0.0045 -> 0.0065 sag;
  - volute sampling;
  - chain wire 5 sides;
  - twist rings 20 -> 18;
  - feet legs;
  - only end rings on straight pole runs.
- **Sizes:** height 18.546; footprint 2.128; lowest head point 11.866; clearances at 4 turns 0.327 / 0.338.
- **Attachments:** the head is 0.26 lower (NOTES has the new table). The chain top and bat perch did not move.
- **Bake misses:**
  - bat 11.9 %;
  - cut walls 9.4 %;
  - chain 0 %, after longer rays for the ring and links;
  - everything else ≤ 1.1 %.
- **FBX:** `C:\cdimp\Halloween_StreetLamp.fbx`, 5.5 MB, 5 meshes. `verify` confirms every image is packed and linked.


---

# Round 3: the two optional polish items (2026-10-14)

Nothing else changed. The attachment points, sizes, bbox centres and clearances are identical to round 2, so the NOTES tables still hold; only the tri counts were updated.

1. **The strap corner at the bottom collar: SMOOTHED.**
   - The strap centreline is now relaxed around the sharpest turn of its under-loop: a weighted Laplacian over ±0.28 of arc, ends pinned. The centreline moves at most 0.016.
   - The sharpest turn per 0.01 of arc there drops from 6.3° (a radius of about 0.09) to 1.4° (about 0.4). The strap sampling still caps each segment at 13°.
   - The gap from the strap to the pumpkin envelope is unchanged (it was never closest there).
   - Before / after: `wip\rv2\z_r3_straps_before_after.png` (the reviewer's round-2 `C07` view on top, round 3 below).
2. **The twist ends at collars 1 and 2: CLEANED.**
   - The lobes now grow out of collar 1 and sink into collar 2 over a 0.22 smootherstep ramp (was a 0.06 step).
   - The game mesh has 2 more twist rings (18 → 20), spaced denser in the ramps (0.06) and 0.09 in the middle.
   - With sun shadows off, both junctions are clean: `wip\rv2\z_r3_c14_ns.png`.
   - With shadows on, the top junction still shows a jagged line: collar 2's cast-shadow edge on the twist, an EEVEE shadow-map artefact (`z_r3_c14_top.png`). The bottom junction is clean either way (`z_r3_c14_bot.png`).

**Re-verified** (re-import check, `verify.json` / `export.json` / `build.json`):

| Object | Tris (round 2) |
|---|---|
| Post | 5,800 (5,704) |
| Cage | 3,136 (3,184): the rounder loop needs fewer strap samples |
| Pumpkin | 3,500 |
| Web | 1,110 |
| WebSilk | 300 |
| **Total** | **13,846** (≤ 14,000) |

- Every image is packed and linked. The FBX holds 12 PNG streams. The shell still has 4 holes.
- Clearance at the 4 pumpkin turns: skin to cage 0.327 and stem to cap 0.338 at 0°, 90°, 180° and 270°. Lowest head point 11.866.
- Unchanged measurements:
  - day face fill/skin luminance 1.98x (25 studs) and 1.93x (40 studs);
  - twist vs pole albedo 1.00;
  - web largest parallel run 1.
- FBX: `C:\cdimp\Halloween_StreetLamp.fbx` (5.5 MB).
