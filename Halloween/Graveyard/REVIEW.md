# Graveyard review (independent reviewer, 2026-10-12)

> **Final status after round 2: all five assets PASS.** See "Round 2" at the end of this file. Round 1 is kept below
> as history.

# Round 1

## Scope and method
I reviewed the five FBX files in `C:\cdimp\`. Each one was imported fresh in headless Blender 5.2.2 (factory startup).
I did not change any of the builder's files. The `Grave_C.blend` file was opened read-only once, for the hi/lo comparison,
and was not saved. My scripts, logs, JSON results and renders are in `Halloween\Graveyard\review\`.

### Technical checks
- `inspect.py`: triangle counts, dimensions, pivot, images.
- `texcheck.py`: alpha, value ranges, UV coverage and stretch.
- `stretch.py`: where the stretched faces are.
- `grasscheck.py`: blade segment counts and bend angles.
- `hicompare.py` and `streakfaces.py`: the Grave_C fracture.

### Render setup (`render.py`)
- Eevee with AgX, using `hkit.review_setup`: sky-blue world, warm sun at 4.0, sky fill.
- A green grass ground plane. Backface culling is on for every imported material.
- 1920x1080 frames:
  - "true view" shots at the Roblox default vertical FOV of 70, from 25 and 45 studs, at eye height 5;
  - tele crops from the same camera positions.
- Close-ups at 5.5-7.5 studs, mid shots at 12 studs, a back-lit variant, and a soil-bed scene (40 studs, plus a
  high third-person view).
- Orthographic front and side views next to a 2 x 1 x 5 stud reference block with 1-stud ticks. A black line marks
  Z = 0 and a red line marks Z = -0.3.

## Verdicts

| Asset | Verdict | Blocking items |
|---|---|---|
| `Halloween_Grave_A.fbx` | **PASS** | none |
| `Halloween_Grave_B.fbx` | **PASS** | none |
| `Halloween_Grave_C.fbx` | **FIX** | 1 |
| `Halloween_DeadGrass_A.fbx` | **FIX** | 2 |
| `Halloween_DeadGrass_B.fbx` | **FIX** | 2 |

Overall this is a strong set. All three graves give an instant Halloween read at 45 studs, at true player-view pixel
size (`crop_45fov70_truepixels.png`): "RIP", the cross and the skull and crossbones all read. The carving is real
geometry with a clean bake: no dark rims, no black patches, and no UV stretch on any stone or mound (max anisotropy
2.5 on 0 % of the area). Budgets, textures, pivot and orientation are all correct.

The two FIX items are local. Neither needs a rebuild.

## Technical results (measured on the imported FBX)

| Asset | Tris (budget) | Textures | Size, Blender X x Y x Z (studs) | Lowest Z | Pivot | Front |
|---|---|---|---|---|---|---|
| Grave_A | 3,279 (4,000) OK | albedo / normal / rough, 512, packed | 4.78 x 3.47 x 4.24 | about -0.2 | ground centre (0.00, 0.00) | -Y, "RIP" reads correctly |
| Grave_B | 3,150 (4,000) OK | 3 x 512, packed | 3.91 x 2.81 x 4.45 | about -0.2 | (0.00, 0.00) | -Y |
| Grave_C | 3,308 (4,000) OK | 3 x 512, packed | 4.75 x 3.91 x 3.93 | about -0.2 | (0.00, 0.00) | -Y, leans back to +Y |
| DeadGrass_A | 2,464 (2,500) OK | 3 x 512, packed | 4.07 x 4.26 x 3.15 | about -0.15 | (0.00, 0.00) | n/a |
| DeadGrass_B | 2,268 (2,500) OK | 3 x 512, packed | 2.96 x 3.19 x 2.65 | about -0.15 | (0.00, 0.00) | n/a |

Details:
- **Import scale:** every FBX imports at object scale 0.01 with raw coordinates in studs. This matches a known-good kit
  asset (`Halloween_PumpkinEgg_Plain1.fbx`).
- **Pivot:** no vertex is below Z = -0.3 on any asset.
- **Albedo alpha:** 1.0 everywhere. This matters because Roblox's default `AlphaMode` (Overlay) would otherwise let the
  part colour show through.
- **Normal maps:** tangent space, OpenGL, mean (127, 128, 251).
- **Roughness:** about 0.85 (matte stone and straw).
- **Stone sizes match the brief:** about 3.07 x 1.16 x 4.04, 2.62 x 1.0 x 4.21 and 3.45 x 1.62 x 3.69 (with the lean).
- **Graves fit the Rock footprint** (6 x 4 x 6) with the soil mound included. They are about 0.8 of a 5-stud
  character's height (`scale_front_ortho.png`).
- **DeadGrass_A** matches its target of about 4 x 3 x 4.
- **DeadGrass_B** is 2.96 x 3.19 in plan, against a target of about 2.5. See the optional polish section.

## FIX list

1. **Grave_C: the broken top-right corner's fracture surface reads as smeared ripples, not as a break.**
   - **What is wrong:** seen from the right three-quarter at 7-12 studs, the fracture face shows parallel, wavy,
     horizontal streaks. A row of small dark "teeth" runs along its top edge.
     - It looks like smeared paint or stacked layers, not a rough rock break. This is the asset's signature feature,
       and it is visible to anyone walking past the bed.
     - **This is not a bake or UV fault.** The stone UVs have no stretch, and the hi-poly `Grave_C_hi` shows the same
       ripples (`compare_GraveC_corner_hi.png` vs `_lo.png`).
     - The cause is the procedural fracture displacement itself, which is stretched or anisotropic along one axis.
   - **Where:** the fracture faces of the top-right broken corner, on the side and top. Evidence:
     - `crop_mid12_GraveC_corner.png` and `crop_C34_rightside.png`;
     - `debug_GraveC_normal_r34.png`, where the streaks are in the normal map.
   - **Suggested change:**
     - Re-sculpt the fracture with isotropic, chunky conchoidal or stepped breaks, for example cellular (Voronoi) cut
       planes at about 0.15-0.3 stud plus fine isotropic noise. Do not use stretched noise.
     - Tint the break a little lighter and fresher (less lichen and moss) than the weathered faces, so the broken corner
       also reads as a break from 25-40 studs.
     - While you are there, widen the narrow vertical chip on the right side face, at about mid-height
       (`crop_C34_rightside.png`, lower half). It renders as a hard dark slot with a white sliver. Make it a broader,
       shallower chip.
     - Then re-bake and re-export. Nothing else on Grave_C needs to change.

2. **DeadGrass_A and DeadGrass_B: the blade arcs are faceted.**
   - **What is wrong:** each blade strip has only 5-7 faces. The bend between neighbouring segments is 13 degrees at the
     median and 21-26 degrees at the 90th percentile (`grasscheck.json`).
     - The long arching and flopped outer blades show 2-3 straight runs with visible corners: obvious at 5-6 studs
       (`close_DeadGrass_A_front.png`, `close_DeadGrass_A_34.png`) and still noticeable at 12 studs
       (`crop_mid12_grassA.png`).
     - Players walk right past the beds, and about 45 tufts will be placed. A polyline arc is the classic low-poly tell
       the owner has rejected before.
   - **Where:** mostly the outer, flopped and arching blades. The upright core blades are fine.
   - **Suggested change:** re-allocate the same 2,500-triangle budget instead of raising it:
     - give the long arching and flopped blades 8-10 segments, with each bend at about 7 degrees or less;
     - give the short upright core blades 3-4 segments;
     - drop about 20 % of the core blades that are hidden inside the tuft.
     - Keep the deliberate kinks and snaps (about 14 %) as a single sharp fold, so they still read as intentional
       breaks.
     - Rough maths: about 45 outer blades x 34 tris + about 65 core blades x 14 tris is about 2,440.
     - Optionally, give the grave-base blade clumps the same treatment. They are small, so this is not blocking.

## Optional polish (non-blocking)
- **Grave_A / Grave_C, epitaph lines:**
  - The worn epitaphs are rows of evenly spaced dashes, so they read a bit like Morse code at 7-25 studs. Fewer,
    irregular, letter-like blobs with gaps would read more as eroded text.
  - The Grave_C skull and crossbones could be about 1.2-1.3x larger (push the epitaph down) for a stronger read at 40+
    studs. It reads now, but it is small (`crop_45fov70_truepixels.png`).
- **Soil mound vs the bed:**
  - The mound is a lighter, orange-brown soil (mid about (128, 92, 60)) with a clear oval edge.
    - On a darker bed or on green, it shows as a "pad" under each stone, seen from the high third-person view
      (`bed_20studs_high.png`, `crop_bed_mounds.png`).
    - It still reads plausibly as fresh grave dirt.
  - **Lead:** compare it with the real bed soil in Studio. If it clashes, the builder can blend the outer 30 % of the
    mound albedo toward the bed's colour and value.
- **Dead grass colour and texture:**
  - **Blight spots:** the dark-brown spots are dense (3-6 on many blades). Below 12 studs the tuft reads as a spotted,
    diseased houseplant. Put spots on about 1 blade in 4.
  - **Pink cast:** the pinkish-tan and lilac-grey ("faded") variants tint the tuft slightly pink at mid range. Shift
    them toward straw and ash-grey.
  - **Vein streaks:** these wobble like wood grain up close. Straighter, finer streaks would read as grass.
  - **Blade shape:** the blades are wide and stiff with pointed tips, which reads closer to a dried flax or yucca than to
    soft dead grass. Slightly narrower outer blades with more droop would help, within the read limit of at least
    0.08-0.12 stud.
- **DeadGrass_B footprint:**
  - It is 2.96 x 3.19 against about 2.5 x 2.5.
  - Pull the flopped blades in a little, or the lead scales it by about 0.85 in Studio (the notes already allow
    0.75-1.3).
- **Close-range nitpicks, not visible from 20 studs:**
  - Grave_A has a small vertical gouge on the back, upper right (`crop_Aback_gouge.png`).
  - Grave_B has a chip lump at the back of the crossing (`crop_Bback_crossing.png`), and its arm ends are slightly
    faceted at a 7-stud three-quarter view.
  - All stones look soft below about 6 studs at 512 px. That is expected for the budget.
- **Stone colour:**
  - Under the blue sky fill, the stones read pale and cool. The albedo is a warm neutral (mean (116, 110, 93)).
  - A slightly deeper value (about -8 %) would make them read richer against the bright hub. This is a matter of taste;
    the stones are not muddy or plastic now.

## Criteria summary
- **Halloween read from 40 studs:**
  - Graves: excellent.
  - Grass: reads as dry, dead grass against the green; it is a support prop.
- **Silhouette and detail:**
  - Graves: chunky, rounded, no faceting at play distance.
  - Grass: arc faceting (FIX 2).
- **Bake faults:** none on the stones or mounds. No black patches, no dark rims around the carvings, no seams that show
  at range. The Grave_C fracture is a sculpt issue (FIX 1).
- **Colour:** good. The stones are a warm grey with moss accents; the mound and straw are warm. Neither plastic nor
  muddy.
- **Carving readability:** excellent. "RIP" and the skull read at 45 studs at real pixel size, and still read in a
  back-lit view (`lineup_25studs_backlit_tele.png`).
- **Grass blades:** they read as a dead-grass tuft at 25-45 studs, not as spiky noise and not as flat cards. Up close
  they are faceted and a little strappy.
- **Scale, pivot and budgets:** all OK. DeadGrass_B is slightly wide (optional).

## Render paths (`C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\Graveyard\review\`)

### Play-distance views
- `lineup_25studs_fov70.png`
- `lineup_45studs_fov70.png`
- `crop_25fov70_truepixels.png`
- `crop_45fov70_truepixels.png`
- `lineup_25studs_tele.png`
- `lineup_45studs_tele.png`
- `graves_25studs_tele.png`
- `graves_45studs_tele.png`
- `lineup_25studs_backlit_tele.png`
- `graves_40studs_backlit_tele.png`

### Bed scene
- `bed_40studs_fov70.png`
- `bed_40studs_tele.png`
- `bed_20studs_high.png`
- `crop_bed_mounds.png`

### Close-ups
- `close_<Asset>_front.png`, `_34.png`, `_back.png`, for all five assets.
- `mid12_Grave_B_34.png`
- `mid12_Grave_C_34.png`
- `mid12_DeadGrass_A_34.png`
- `mid12_DeadGrass_B_34.png`

### Scale and pivot
- `scale_front_ortho.png`
- `side_ortho_Grave_A.png`
- `side_ortho_Grave_B.png`
- `side_ortho_Grave_C.png`

### Evidence for FIX 1
- `crop_mid12_GraveC_corner.png`
- `crop_C34_rightside.png`
- `crop_Cback_fracture.png`
- `compare_GraveC_corner_hi.png`
- `compare_GraveC_corner_lo.png`
- `debug_GraveC_normal_r34.png`
- `debug_GraveC_albedo_r34.png`

### Evidence for FIX 2
- `close_DeadGrass_A_front.png`
- `crop_mid12_grassA.png`
- `grasscheck.json`

### Data
- `inspect.json`
- `texcheck.json`
- `stretch.json`
- `grasscheck.json`
- `uvcov_*.png`

# Round 2 (re-check of Grave_C, DeadGrass_A and DeadGrass_B)

## Scope and method
- **Not re-reviewed:** Grave_A and Grave_B. They are unchanged (FBX time stamps 10:28) and keep their round-1 PASS.
- **Re-checked:** the re-exported files in `C:\cdimp\`:
  - `Halloween_Grave_C.fbx` (11:31);
  - `Halloween_DeadGrass_A.fbx` (11:42);
  - `Halloween_DeadGrass_B.fbx` (11:43).
- **Method:** the same checks as round 1 (`inspect`, `texcheck`, `stretch`, `grasscheck`) and the same renders
  (`render.py`): eye height 5 at 25 and 45 studs (FOV 70 and tele), back-lit, 12-stud three-quarter views, close-ups,
  the soil bed, and the orthographic scale views.
- **Output:** everything is in `Halloween\Graveyard\review\round2\`.

## Technical results (imported FBX)

| Asset | Tris (budget) | Textures | Size, Blender X x Y x Z | Lowest Z | Pivot |
|---|---|---|---|---|---|
| Grave_C | 3,314 (4,000) OK | albedo / normal / rough, 512, all packed | 4.8 x 3.9 x 3.9 (unchanged) | about -0.2 | ground centre (0.00, 0.00) |
| DeadGrass_A | 2,478 (2,500) OK | 3 x 512, packed | 4.1 x 3.6 x 3.2 | about -0.15 | (0.00, 0.00) |
| DeadGrass_B | 2,234 (2,500) OK | 3 x 512, packed | 2.85 x 2.93 x 2.65 | about -0.15 | (0.00, 0.00) |

- **Import:** scale 0.01 on every file, so raw units are studs. No rotation.
- **Pivot:** no vertex below Z = -0.3.
- **Albedo alpha:** 1.0 everywhere.
- **Orientation:** the Grave_C carving still faces -Y.
- **Grave_C UVs:** the stone and mound still have 0 % stretched area.

### Blade bends (`grasscheck.json`)

| Asset | Median bend | 90th percentile | Adjacent faces bent over 20° |
|---|---|---|---|
| DeadGrass_A | 4.7° (was 12.9°) | 6.7° (was 20.8°) | 3 % (was 12 %) |
| DeadGrass_B | 4.4° (was 13.1°) | 6.3° (was 25.5°) | 4 % (was 18 %) |

- Long blades now have 8-10 faces and core blades 3-5.
- The blades whose maximum bend is over 30° (13-14 %) are the deliberate snaps.
- These numbers match the builder's report.

## Round-1 FIX items

1. **Grave_C fracture: RESOLVED.**
   - The broken corner is now a stepped, chunky, faceted break in lighter, fresher stone with very little moss.
   - It reads as broken rock from the right three-quarter at 7 and 12 studs (`crop_C34_rightside_r2.png`,
     `crop_mid12_GraveC_corner_r2.png`) and in the bed scene (`bed_20studs_high.png`).
   - The parallel ripples and the row of dark "teeth" are gone.
   - The silhouette of the corner is now a jagged stepped outline.
   - The old dark slot on the right side face is now a wide, shallow scoop. A faint thin crease remains along its inner
     edge, visible only within about 8 studs (optional polish).
2. **Grass faceting: RESOLVED on both tufts.**
   - The arching and flopped blades are smooth curves in the close-ups and at 12 studs (`close_DeadGrass_A_front.png`,
     `close_DeadGrass_A_34.png`, `close_DeadGrass_B_front.png`, `mid12_DeadGrass_*_34.png`).
   - The deliberate snaps still read as single sharp folds.
   - The colours are now straw / olive / ash with fewer spots. The tufts read as dry dead grass at 25-45 studs and in
     the bed (`bed_40studs_tele.png`, `crop_45fov70_truepixels_r2.png`).

## Final verdicts

| Asset | Round 1 | **Final** |
|---|---|---|
| Halloween_Grave_A | PASS | **PASS** (unchanged, not re-reviewed) |
| Halloween_Grave_B | PASS | **PASS** (unchanged, not re-reviewed) |
| Halloween_Grave_C | FIX | **PASS** |
| Halloween_DeadGrass_A | FIX | **PASS** |
| Halloween_DeadGrass_B | FIX | **PASS** |

## Optional polish (round 2, non-blocking)

### Pale "ash" blades (the most visible)
- **What:** the new ash-grey colour is near-white, and under the sky fill it renders pale blue-white.
- **Where it shows most (DeadGrass_A):**
  - A snapped, square-ended upright blade sits front and centre in the tuft. At 25 studs on plain grass it reads like a
    small white stake (`crop_25tele_grassA_r2.png`). It is also visible as a white line in `scale_front_ortho.png`.
  - A second pale blade sits just behind it.
- **DeadGrass_B:** it has a few pale blue-grey blades, but none looks like a stake.
- **In the soil bed at 40 studs** the effect is barely noticeable, which is why this is not blocking.
- **Fix if you touch the grass again:**
  - lower the ash variant's value to about 0.55-0.6 and warm it slightly (about (165, 158, 140) sRGB);
  - don't use it on snapped, short upright blades, or move that blade off the front.

### Snapped ground shards
- The small snapped pieces on the ground at the tuft base (`close_DeadGrass_B_front.png`, `mid12_DeadGrass_B_34.png`)
  read as loose triangular chips at close range.
- Fix: tuck them partly under the blades, or drop one or two.

### Grave_C
- A faint dark crease remains along one edge of the right-side scoop.
- The back still has the round-1 shallow chip with a thin centre line (`crop_Cback_fracture_r2.png`). Only visible
  within about 8 studs.

### Carried over from round 1, still open
- **Epitaph dashes:** they read like Morse code; same note as round 1.
- **Skull size:** the Grave_C skull could be a little larger.
- **Mound colour:** check the mound colour against the real bed soil in Studio. The builder deliberately left it, to
  keep the three graves matching.
- **DeadGrass_B footprint:** 2.85 x 2.93 against about 2.5. Scale it about 0.88 in Studio if an exact fit matters.

## Round 2 render paths (`C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\Graveyard\review\round2\`)

### Eye-height views
- `lineup_25studs_fov70.png`
- `lineup_45studs_fov70.png`
- `crop_45fov70_truepixels_r2.png`
- `lineup_25studs_tele.png`
- `lineup_45studs_tele.png`
- `graves_25studs_tele.png`
- `graves_45studs_tele.png`
- `lineup_25studs_backlit_tele.png`
- `graves_40studs_backlit_tele.png`

### 12 studs
- `mid12_Grave_C_34.png`
- `mid12_DeadGrass_A_34.png`
- `mid12_DeadGrass_B_34.png`

### Close-ups
- `close_Grave_C_front.png`, `close_Grave_C_34.png`, `close_Grave_C_back.png`
- `close_DeadGrass_A_front.png`, `close_DeadGrass_A_34.png`, `close_DeadGrass_A_back.png`
- `close_DeadGrass_B_front.png`, `close_DeadGrass_B_34.png`, `close_DeadGrass_B_back.png`

### Crops
- `crop_C34_rightside_r2.png`
- `crop_mid12_GraveC_corner_r2.png`
- `crop_Cback_fracture_r2.png`
- `crop_25tele_grassA_r2.png`
- `crop_25tele_grassB_r2.png`
- `crop_bed40_r2.png`

### Bed and scale
- `bed_40studs_fov70.png`
- `bed_40studs_tele.png`
- `bed_20studs_high.png`
- `scale_front_ortho.png`
- `side_ortho_Grave_C.png`

### Data
- `inspect.json`
- `texcheck.json`
- `stretch.json`
- `grasscheck.json`
