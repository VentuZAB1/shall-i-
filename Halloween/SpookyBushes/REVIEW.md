# SpookyBushes: independent review (2026-10-12)

Reviewer: an independent agent, not the builder. Every check was made on the FBX files in `C:\cdimp\`, imported fresh in
headless Blender 5.2 (factory startup). Nothing of the builder's was modified.

## FINAL VERDICTS (round 2, FBX re-export of 12:40)
| Asset | Round 1 | **Round 2 (final)** |
|---|---|---|
| `Halloween_Bush_Thorn.fbx` | FIX (3 items) | **PASS**: all 3 FIX items resolved; optional polish below |
| `Halloween_Bush_Autumn.fbx` | PASS | **PASS**: still passes after the polish changes |
| `Halloween_Bramble.fbx` | PASS | **PASS**: still passes after the polish changes |

No blocking issues remain. The three assets are ready for the lead to import (see the Roblox setup in `NOTES.md`,
especially `AlphaMode = Transparency` on `WebSilk`).

## Round 2 (re-review of the 12:40 re-export)
I used the same method as round 1 (below), with the same eye-height cameras. This time each asset was shot from 4 sides:
front, right side, back and left side (yaw 0 / 90 / 180 / 270), at 25 and 40 studs. I also rendered close-ups, clay
and silhouette passes, and two new eye-height web shots. The round-1 renders stay in `renders\` for comparison.

### Round 2 technical checks (all pass)
| Check | Thorn | Autumn | Bramble |
|---|---|---|---|
| Triangles (budget) | Bush 8,759 + Web 576 + WebSilk 336 = **9,671** (10,000) | Bush 8,088 + Gourds 1,520 = **9,608** (10,000) | **4,515** (5,000) |
| Embedded textures | yes: Bush 1024 x3; Web 128; **WebSilk 1024 RGBA** (alpha 0 to 1, mean 0.10) | yes: 1024 x3 + 512 x3 | yes: 512 x3 |
| Size, Roblox X x Y x Z (footprint) | 6.35 x 5.94 x 6.09 (about 6 x 5.5 x 6; see polish 4) | 6.19 x 5.21 x 6.07 | 3.88 x 3.06 x 3.85 |
| Pivot (base centre, Z = 0) | yes, lowest point -0.13 | yes, -0.18 | yes, -0.16 |
| UV stretch (area with anisotropy > 2) | Bush 1.6%, WebSilk 0% | 0% | 2% |
| Texel density (median px/stud) | Bush **51** (was 70), WebSilk 192 | 71 | 76 |
| Spider point (2.570, 3.790, 1.733) | 0.017 under the cane; the drop to the ground is clear | - | - |
| Bake faults | none: no black patches, rims or seams | none | none |

### Halloween_Bush_Thorn: **PASS**
- **FIX 1 (cobweb read): resolved.**
  - The front orb web (11 radials plus a spiral) hangs near-vertical facing -Y. It reads as a cobweb at once at 25
    and 45 studs from eye height (`lineup_25.png`, `lineup_45.png`, `Thorn_25_front_truepx.png`), even at true
    pixel size.
  - The left web reads from the left side (`Thorn_40_sideL_truepx.png`, `Thorn_web_left_eye.png`).
  - The style is graphic, like a Halloween decoration, which suits the "playful decorated yard" brief.
- **FIX 2 (strands): resolved.**
  - The vertical rod and the tip-to-tip clothesline loops are gone.
  - The anchor threads run irregularly to thorns and leaves, and the silvery colour no longer glares in sun
    (`Thorn_40_zoom150.png`, `Thorn_40_zoom150_sideL.png`).
- **FIX 3 (body): resolved.**
  - There are 5 lobes with dark gaps, and the foliage now fills the footprint (about 4.5 tall).
  - Outline leaves run all the way down to the soil, and the crown is uneven, with one pale dead cane.
  - The side canes root into the soil (`Thorn_40_zoom150_back.png`, `Thorn_sil_0.png`, `Thorn_clay_200.png`).
  - It now reads as a dark, thorny bramble from every side, not as a boulder.
- **Berries:** mostly black or purple now; the one red cluster is fine.

Optional polish (Thorn, round 2):
1. **Edge-on webs look like flat white blades.**
   - What's wrong: both silk sheets are flat cards framed by thick frame tubes. Seen edge-on, the front web shows
     as a solid white "ruler" or racket hanging off a cane (`Thorn_40_zoom150_sideL.png` right edge,
     `Thorn_25_sideR_truepx.png` upper left, `Thorn_web_left_eye.png` right).
   - Change: give each card a slight billow (bend it 10-20 degrees across its width, or sag the bottom edge) and
     taper the frame thread toward the free corners, so the edge-on view breaks up.
2. **Half of the silk texture is empty.** `BushThornSilk_albedo` is 1024 x 1024, but both webs sit in its left
   half; the right half is blank. Either pack the webs into a 512 x 1024 map (half the memory) or scale the islands
   up to fill it (sharper threads).
3. **The body texture is softer close up.** Bush texel density fell from about 70 to about 51 px/stud because the
   lobed body has more surface. Within about 10 studs the baked leaves look softer, and a few lobe tops show
   polygon corners (`Thorn_close_back34.png` top lobes, `Thorn_web_left_eye.png` right lobe). This is fine at
   game distance. If you touch the atlas again, shrink the wood and berry islands to give the body more texels.
4. **The size is slightly over the brief:** 6.35 x 5.94 x 6.09 against about 6 x 5.5 x 6. It still fits the
   original Bush slot (5-6 x 6 x 5-6). The lead can scale it to 0.95 if a bed is tight, as NOTES says.

### Halloween_Bush_Autumn: **PASS**
- **Back of the bush:** the new hanging leaves screen most of the three bare stems from the back
  (`Autumn_40_zoom150_back.png`). From the left side the stems still show a little (`Autumn_40_zoom150_sideL.png`).
  That's acceptable for a bush, so no action is needed.
- **Gourd warts:** they are darker and now read as warts or spots rather than mould (`Autumn_close_low.png`).
- **Unchanged and still good:** the autumn read, the colour, the clumpy silhouette, the bake and the budget
  (`Autumn_40_zoom150.png`, `Autumn_40_front_truepx.png`).

### Halloween_Bramble: **PASS**
- The bark is slightly warmer and the twig tips vary a little more. At game distance it reads as before, as a dry
  dead tangle with hanging leaves (`Bramble_25_front_truepx.png`, `Bramble_40_zoom150_back.png`).
- Round-1 polish note, still optional: up close (`Bramble_close_front34.png`) most twig ends are still short
  pencil-point cones and the bends are faceted.

### Round 2 renders and data (`...\SpookyBushes\review\`)
- **Lineups:**
  - `renders_r2\lineup_25.png`
  - `renders_r2\lineup_45.png`
  - `renders_r2\lineup_25_back.png`
- **True pixel size, 4 sides:** `renders_r2\{Thorn,Autumn,Bramble}_{25,40}_{front,sideR,back,sideL}_truepx.png`
- **40 studs at eye height, long lens:** `renders_r2\{asset}_40_zoom150{,_sideR,_back,_sideL}.png`
- **Close-ups:** `renders_r2\{asset}_close_{front34,back34,low}.png`
- **Webs:**
  - `renders_r2\Thorn_web_front_eye.png`
  - `renders_r2\Thorn_web_left_eye.png`
  - `renders_r2\Thorn_web_top.png`
  - `renders_r2\Thorn_web_side.png`
  - `renders_r2\Thorn_web_nosilk.png`
- **Clay and silhouettes:** `renders_r2\{asset}_{clay,sil}_{0,90,200}.png`
- **Data:**
  - `inspect_report_r2.json`
  - `uv_report_r2.json`
  - `tex_r2\` (maps re-saved from the FBX)
  - Logs: `log_*_r2.txt`
- **Scripts:** the round-1 scripts. Round-2 runs set `REVIEW_TAG=_r2`, and `spider_check.py` takes
  `SPIDER_ROBLOX=x,y,z`.

---

# Round 1 (original findings, kept for history)

| Asset | Round 1 verdict |
|---|---|
| `Halloween_Bush_Thorn.fbx` | FIX (3 items) |
| `Halloween_Bush_Autumn.fbx` | PASS (optional polish only) |
| `Halloween_Bramble.fbx` | PASS (optional polish only) |

## How it was checked
- **Import:** each FBX imported on its own. The objects come in at scale 0.01 because hkit exports with
  global_scale 0.01, so x100 = studs. That matches the hkit convention and the builder's numbers.
- **Scene:** hkit `review_setup` sky and warm sun (Eevee, AgX), a green grass plane, a soil disc under each asset (the
  hub beds are soil), and a 2 x 1 x 5-stud grey reference block (a Roblox character).
- **Roblox look:** backface culling ON on every material. WebSilk uses its albedo alpha with alpha hashed (dithered),
  matching `AlphaMode = Transparency`. Normal and roughness maps forced to Non-Color.
- **Player views:** camera at **eye height 5 studs**, 25 / 40 / 45 studs away, **70 degree vertical FOV** on a
  1920x1080 frame. The `*_truepx.png` crops show the asset at the exact pixel size a player sees. The `*_zoom150.png`
  shots use the same 40-stud eye-height viewpoint through a long lens, to show what those pixels contain.
- **Extra passes:** close-ups (front 3/4, back 3/4, low), Workbench clay (raw game mesh) and black silhouettes from
  3 sides each.
- **Data checks:**
  - UV stretch and texel density per triangle (`uv_report.json`);
  - embedded maps re-saved from the FBX (`review\tex\`);
  - the Thorn spider point checked by raycast (`spider_check.py`).

## Technical checks (all pass)
| Check | Thorn | Autumn | Bramble |
|---|---|---|---|
| Triangles (budget) | Bush 8,528 + Web 558 + WebSilk 572 = **9,658** (10,000) | Bush 8,232 + Gourds 1,520 = **9,752** (10,000) | **4,515** (5,000) |
| Embedded textures | yes: Bush 1024 x3; Web 128; **WebSilk 512 RGBA** (alpha 0 to 1, mean 0.20, 83% of texels under 0.5) | yes: Bush 1024 x3, Gourds 512 x3 | yes: 512 x3 |
| Material wiring on import | albedo, normal (via Normal Map), roughness and silk alpha all linked | same | same |
| Size, Roblox X x Y x Z (footprint) | 6.3 x 5.7 x 5.9 (6 x 5.5 x 6) | 6.0 x 5.2 x 6.2 (6 x 5 x 6) | 3.9 x 3.1 x 3.9 (4 x 3 x 4) |
| Pivot (origin at base centre, Z = 0) | yes, lowest point about -0.06 | yes, about -0.18 | yes, about -0.16 |
| UV stretch (area with anisotropy > 2) | Bush 0.1%, WebSilk 13% (fine for a silk sheet) | 0% | 0% |
| Texel density (median px/stud) | 70 | 72 (gourds 154) | 76 |
| Spider point (1.525, 3.740, 2.641) | 0.014 under the cane; the drop to the ground is clear | - | - |

The atlases have no black patches, no dark rims and no visible seams. The AO is tinted, not grey. The fill-colour
dilation at the island edges is normal.

## Halloween_Bush_Thorn: **FIX**

The canes, thorns, berries and leaf bake are good work. But the two things the brief asks this bush to carry, **a
cobweb and a thorny bramble shape**, do not read where players actually see it: at eye height, 25-40 studs away. The
builder's review camera sits about 10-15 studs up and looks down onto the web cap
(`review_thorn_back34.png`, `review_lineup_50.png`). That angle shows the web far more than any player will see it.

1. **The cobweb does not read from player eye height.**
   - **What's wrong:** `WebSilk` lies almost flat over the top of the mound. From 5 studs up it is seen edge-on, as a
     thin white strip along the top (`Thorn_40_front_truepx.png`, `Thorn_40_zoom150.png`, `lineup_45.png`). Where it
     does show (`Thorn_web_top.png`), the silk albedo is a random fibre tangle with three starburst hubs. It has no
     radial or spiral structure, so it reads as frost or white hair, not as a cobweb.
   - **Change:**
     - Re-drape the sheet so a good part of it, about 3 x 2.5 studs, hangs **down the front (Blender -Y) and one
       side**, within about 30 degrees of vertical, slung between two or three canes and the foliage.
     - Give it the recognisable orb-web read used by the hub's webs (`WebsSpiders\NOTES.md`, the torn web): about
       8-12 radial threads plus a sagging spiral. Make it strand geometry (0.075 or thicker, budget allowing), or
       paint strong threads into the silk albedo (threads alpha about 0.9, film about 0.15).
   - **Acceptance:** in the 40-stud true-pixel crop, a viewer names it "cobweb" without being told.

2. **The `Web` strands read as white plastic tubing or a clothesline, not silk.**
   - **What's wrong:** the 7 strands are uniform round tubes in pure bright white (albedo mean about 0.85). They hang
     in neat matching catenaries from one cane tip to the next, which outlines the cane crown like a fence or
     gazebo frame. One strand drops **straight down like a rod** at the front-right cane (`Thorn_40_zoom150.png`,
     right of centre; `Thorn_clay_0.png`; `Thorn_web_side.png`).
   - **Change:**
     - Re-route the strands as the web's frame and anchor threads: from the web's edge out to cane tips, thorns and
       leaves, at irregular angles and lengths. No tip-to-tip loops.
     - Make the sag uneven and remove the vertical rod.
     - Tone the colour down to a silvery off-white (about 205-215 grey with a faint cool tint, roughness about 0.6)
       so the strands stop glowing in full sun. Keep them 0.075 or thicker so they survive at 30-60 studs.

3. **The body reads as a smooth leaf-wallpapered boulder, not a clumpy thorn bush.**
   - **What's wrong:**
     - At eye height, the lower two-thirds of the outline is one smooth ovoid curve, with polygon facets showing
       along the rim (`Thorn_40_zoom150.png` lower left, `Thorn_sil_0.png`, `Thorn_sil_90.png`,
       `Thorn_close_low.png`).
     - The 100 protruding leaves sit mostly on the upper half, and several are hidden under the web.
     - The thorny canes are only a tidy, symmetrical crown on top (`Thorn_sil_0.png` looks like a cage), so the mass
       itself has no bramble character.
     - The foliage mound is only about 3.8 studs tall in a 5.7-stud asset, so the bush looks lower and smaller
       than the original Bush it replaces.
     - Next to the Autumn bush, whose lobes read clearly (`Autumn_40_zoom150.png`), the Thorn looks unfinished.
   - **Change:**
     - (a) Split the mound into **3-5 distinct lobes with dark gaps** between them, like the Autumn clump layout.
       Raise the foliage to about 4.5 studs.
     - (b) Move protruding leaves to the **silhouette rim, especially the lower half and around the base**, so the
       outline is ragged all the way down. To pay for it, drop the leaves hidden under the silk. Use fewer
       segments on leaves away from the outline (for example 32 down to about 20 triangles), and trim the
       body-shell decimation if needed.
     - (c) Have **3-5 thorny canes come out of the sides** of the mound and arc down into the soil, with 1-2 low
       thorny runners along the ground. Make the top crown less symmetrical (vary height and lean; one broken or
       dead cane).
   - **Acceptance:** `Thorn_sil_0.png` and `Thorn_sil_90.png` show a broken, clumpy outline, and the thorns read
     as a tangle through the bush, not a frame on top.

Optional polish (Thorn):
- The brief asks for "a few black berries". The red, unripe drupelets are the most saturated thing on the bush and
  read as bright red dots at 25 studs (`Thorn_25_front_truepx.png`). Make most clusters black or deep purple and keep
  at most 1-2 red.
- In close views, the baked leaves smear slightly where the shell turns away from the viewer, and the leaf
  serration shows pixel steps (`Thorn_close_front34.png`). This is not a UV fault (the stretch stats are clean); it
  is the price of 70 px/stud. It is only visible within about 10 studs.

## Halloween_Bush_Autumn: **PASS**
- **Halloween read:** reads as an autumn bush instantly at 25-45 studs. It has rich orange, red and amber colour with
  darker gaps, nothing muddy or plastic, and the shaded side goes deep crimson. The two gourds show as orange and
  yellow shapes at the base at 40 studs (`Autumn_40_front_truepx.png`).
- **Silhouette:** clearly clumpy: 4-5 lobes with real protruding leaves on the outline (`Autumn_sil_90.png`,
  `Autumn_clay_0.png`). Not a sphere, and no faceting on the curves at game distance.
- **Leaves:** a real leaf read, both baked and geometric.
- **Technical:** the bake is clean, budgets, scale and pivot are fine, and the warm AO tint works.

Optional polish (Autumn):
- From the back and sides, the canopy sits about 0.6-0.8 stud up on three bare dark stems with an open gap under
  it, which reads a little like a creature on legs (`Autumn_40_zoom150_back.png`, `Autumn_close_low.png`). Hang a
  few leaf sprays or drooping leaves down to about 0.2-0.3 above the soil on the back and sides.
- The pumpkin and goblin-gourd warts are pale flat blotches in the albedo and normal maps, with smooth silhouettes.
  Close up they read as mould spots rather than warts (`Autumn_close_low.png`). Give a few warts real bumps, or
  darken and shrink the blotches so they read as raised warts.
- The gourds sit only on the front (-Y). That's fine as long as the lead faces the front toward the path.

## Halloween_Bramble: **PASS**
- **Read:** at 25-40 studs it reads as a dry, dead, tangled shrub. The few hanging dead leaves give it colour, and the
  silhouette is open and twiggy (`Bramble_40_zoom150.png`, `Bramble_25_front_truepx.png`). It suits the footprint as
  filler.
- **Technical:** 4,515 triangles, a 512 texture set, a clean bake, correct size and pivot.

Optional polish (Bramble):
- Nearly every twig ends in the same short sharpened-pencil cone, and the 3-6 sided twigs show faceted bends at
  close range (`Bramble_close_front34.png`, top centre curl). Vary the tip lengths and taper them over a longer run.
  If budget allows, move about 10% of the triangles from the smallest inner twigs to extra segments on the most
  visible curved twigs.
- The bark reads cool lavender-grey in sun. A slightly warmer grey-brown (dry wood) would sit better next to the
  soil beds. This is a matter of taste, not a fault.

## Renders and data (all in `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\SpookyBushes\review\`)
- **Lineups (player eye height, 70 degree FOV, full 1920x1080 frame):**
  - `renders\lineup_25.png`
  - `renders\lineup_45.png`
  - `renders\lineup_25_back.png`
- **True pixel size at 25 and 40 studs, front and back-left:** `renders\{Thorn,Autumn,Bramble}_{25,40}_{front,backL}_truepx.png`
- **40-stud eye-height viewpoint, long lens:** `renders\{Thorn,Autumn,Bramble}_40_zoom150.png` and `..._40_zoom150_back.png`
- **Close-ups:** `renders\{Thorn,Autumn,Bramble}_close_{front34,back34,low}.png`
- **Web:**
  - `renders\Thorn_web_top.png`
  - `renders\Thorn_web_side.png`
  - `renders\Thorn_web_nosilk.png`
- **Raw game mesh (clay) and silhouettes:** `renders\{asset}_clay_{0,90,200}.png`, `renders\{asset}_sil_{0,90,200}.png`
- **Data:**
  - `inspect_report.json` (triangles, textures, material links, bounds)
  - `uv_report.json` (stretch and texel density)
  - `tex\` (maps re-saved from the FBX)
- **Scripts:**
  - `inspect.py`
  - `render.py` (modes: lineup, player, zoom, close, web, clay, sil)
  - `uvtex.py`
  - `spider_check.py`
