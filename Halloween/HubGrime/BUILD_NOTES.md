# HUB GRIME: build notes (builder, 2026-10-13; rounds 2-5 + polish on 2026-10-14)

This covers what I built and what I changed for every `PLAN_REVIEW.md` item, both MUST and NICE. It also lists where I
deviated from `PLAN.md`, how it was verified, and the known limitations. **The visual review (`REVIEW.md`, FIX) is
answered in the "Round 2" section at the end**; where round 2 replaced something described earlier, that section wins.

## Deliverables
- **`decals\`:** 17 RGBA straight-alpha PNGs (15 briefed + the 2 approved MossBase end caps).
- **`gen\`:** the re-runnable generator. Only system Python (numpy, PIL) and headless Blender 5.2.

| Script | What it does |
|---|---|
| `make_specs.py` | the single source of truth: sizes, carriers, contact bands, content edges (shared with Blender) |
| `grime_lib.py` | the numpy kit: noise, crack geometry and SDF raster, moss v5, slime, stains, compositing, export + checks |
| `rec_cracks.py` | the 6 crack recipes |
| `rec_stains.py` | round 2: the 2 stain recipes (watermark, mud skid, elongated drops) |
| `make_decals.py` | all 17 textures; writes `checks.json` |
| `make_sheets.py` | the overview, 1:1 swatches, thumbnails, fringe/wrap sheets, MossBase seam chain + metrics, hidden-band check, floating-moss check, W_Crack_C 1/8 gate, moss gate, order pairs |
| `make_studs.py` | the 1-stud stud tile (normal + AO), as Roblox draws `SurfaceType.Studs` (flat) |
| `mock_preview.py` | the Blender mocks, carriers, calibrated day/night, all cameras |
| `render_previews.py` | runs Blender, then applies the haze veil once (`post_veil.py`) |
| `make_test_patch.py` | writes `test_patch.json` from the PNGs' content extents; refuses a patch that breaks the spacing rules |
| `calib_fit.py` | round 4: fits the mock lighting + wall/pillar/floor albedo to the live-game screenshots -> `calib_round4.json` |
| `quickview.py`, `sample_calib.py` | dev helpers |

- **`NOTES.md`:**
  - per texture: carrier size, pixels, surface, hidden band, count and spacing;
  - placement rules;
  - the TEST-PATCH recipe;
  - `test_patch.json` (exact carriers + a Luau builder snippet).
- **`renders\` (40 frames since round 2):**
  - day and night at 25 and 60 studs (eye height 5, vertical FOV 70);
  - before/after pairs;
  - third-person views;
  - top-down ortho;
  - close-ups at 6 / 8 / 4 studs;
  - an oblique wall view;
  - true-pixel crops;
  - half-res phone checks;
  - a night lamp pool;
  - the 4 overlap pairs in both draw orders;
  - round 2: the wall mock IS the test-patch bay (pillars, `test_patch.json`), plus `wall_tp_day/night` (default
    third-person camera) and `wall_foot_top_ortho` (floor moss meets the wall foot).
- **`sheets\`:** `overview_floor/wall`, `swatch_<name>` (1:1 on green, blue, cream, orange), `thumbs`,
  `fringe_floor/wall`, `mossbase_seams` (+ 1:1 crops), `moss_gate`, `order_pairs`, `gate_W_Crack_C_vs_A` (round 2).
- **`checks.json`:** all per-file checks, plus `mossbase_seams`, `hidden_bands` and (round 2) `floating_moss`.
  **Everything passes.**

## Review items

### MUST 1: no visible edge carries content (texture wrap)
- **Margins.** Every edge has a ≥ 4 px alpha-0 margin, except the MossBase left/right edges and each end cap's inner
  edge. `checks.json` → `edges_with_content` ⊆ `edges_allowed`, and `edge_rule_ok` is true on all 17.
- **Hidden bands.** Contact edges carry content at full strength for ≥ 0.25 stud past the contact line, then a 1-4 px
  ramp, then the 4 px margin.
  - The generator uses a per-edge ramp (`contact_ramps`). A plain 10 px fade would have eaten the band, and the first
    check caught that.
  - The bands:

| Texture | Band | Contact line |
|---|---|---|
| MossBase A/B/EndL/EndR | 0.375 at the bottom (12 px band + 4 px margin at 42.7 px/stud) | |
| W_Crack_C | 0.375 at the bottom (24 + 4 px) | |
| W_Drip_A/B | 0.35 at the top (24 + 4 px) | trim bottom |

  - `checks.json["hidden_bands"]`: every texture is ok (margin alpha 0; continuation ratio ≥ 0.93 over the first
    0.25 stud).
  - The W_Drip_A moss tufts were moved up so they grow out from under the trim through the band.
  - Placement (sink 0.375 / raise 0.35) is in NOTES section 2.
- **Previews.** Every decal image node uses `extension = REPEAT`, as Roblox does.
- **Fringe sheets.** `fringe_*.png` now starts each row with a **2x2 wrapped tile** at mip 1 over magenta, followed by
  the naive straight-alpha mip strip (mip 1-3 over black, white and magenta). No wrap lines appear. The band visible
  in the W_Drip_B 2x2 tile is that texture's own top goo band, which in game is hidden behind the trim.

### MUST 2: MossBase run ends
- **New files:** `W_MossBase_EndL` and `W_MossBase_EndR`, 6 x 6.375 studs, 256 x 272 px.
- **Inner edge.** The inner edge is the shared seam band. The caps are rendered on a 9-stud window that includes 3
  studs of seam context, then cropped, so blurs near the join match the strips exactly.
- **Outer end.** Outward, the moss thins by density and size, the damp band height fades to 0, and the outer edge has
  the 4 px margin.
- **Seam metrics (`checks.json["mossbase_seams"]`):**

| Comparison | Max difference (/255) |
|---|---|
| A vs B band identity | 0.09 |
| caps vs strips | 2.0 (dither only) |

  - All 8 pairings (A|A, A|B, B|A, B|B, EndL|A, EndL|B, A|EndR, B|EndR) have identical seam statistics, inside the
    strips' own neighbour-difference range, so `seamless_ok` is true.
  - Visual: `sheets\mossbase_seams.png` (an EndL|A|A|B|B|A|B|EndR chain on a blue wall, seams ticked) and
    `mossbase_seams_crops_1to1.png`.
- **Rules.** The run-end rules (end on a seam; cap free ends; pillar, corner or prop ends need no cap) and the
  pillar-to-pillar Texture option are in NOTES.

### MUST 3: overlaps must not depend on draw order
- **Render mode.** The previews use **BLENDED** (per-object sort) with no depth prepass. I first had "show backface"
  off, which made Eevee write a per-object depth prepass, so one decal clipped the other. That was found in the first
  order test and fixed: `use_transparency_overlap = True`, i.e. pure sorted blending, as in Roblox.
- **Both orders rendered.** Forced by moving the bottom decal's origin far behind along the view ray (geometry
  unchanged):
  - `order_floor_moss_over_stain` / `order_floor_stain_over_moss`;
  - `order_floor_crack_over_stain` / `order_floor_stain_over_crack`;
  - `order_wall_moss_over_crack` / `order_wall_crack_over_moss`;
  - all side by side in `sheets\order_pairs.png`.
  - Both orders look right in every pair. A stain on top just reads as damp moss or a muddier crack.
- **Design.** W_Crack_C's foot carries its own moss in the MossBase palette, and it sits on a documented low-moss slot
  (A: 6.7-10.3, B: 12.2-15.8 studs). Crack-over-moss and moss-over-crack both read as "a crack emerging from moss".
- **NOTES rule:**
  - only a stain may sit under other decals;
  - W_Crack_C only on a slot;
  - never a crack over moss;
  - **nothing overlapping slime.** A mud stain drawn over the slime made it look dirty, so slime is no-overlap. The
    mock was changed to follow this.
  - `ZIndex` only orders decals on the same face.

### MUST 4: moss quality gate (no bubbles, blobs or camo)
The moss went through 6 renderer versions, all judged at 1:1 and at play distance:

| Version | What it looked like |
|---|---|
| v1 | sphere micro-clumps with round tip dots read as **green grapes / bubbles** (rejected) |
| v2 | summed clump field + fur noise read as a kitchen **sponge** (pitted) |
| v4 | cellular creases read as **reptile scales / cracked mud** |
| v5 | soft lumps, colour-only speckle: closer, but the forms were flat (**camo** risk) |
| v6 | final (below) |

The final renderer (`grime_lib.moss_render`):
- **Contour:** soft clump kernels summed, plus fine periodic fur noise, give an irregular **tufted contour** with a
  crisp 1 px alpha edge and **no dark stroke**.
- **Form:** each cushion's dome plus **soft sub-lumps** (lit from above, shaded underneath); cavity only between
  lumps.
- **Surface:** blotchy **yellow-green tip stipple concentrated on the lit side** over an olive body. This is the
  graveyard moss language.
- **Palette:** deepened after the lit previews (it read as "lettuce" in the bright hub). M1-M5 are now
  (34,50,24) / (66,86,34) / (96,116,44) / (146,166,60) / (182,194,86).

**Gate:** `sheets\moss_gate.png` puts the Graveyard moss reference next to G_Moss_A and W_MossBase_A at **6 studs**
(`renders\moss_close6_floor/wall`) and the **25-stud true-pixel** crops. Verdict: it reads as soft clumpy moss
cushions in the same family as the graveyard moss. **The Blender displaced-moss fallback was not needed.** The
MossBase moss was finished after this gate.

### MUST 5: the bevel light must not become a pale outline
- The W5 light lip is **one side only** (the lower / away-from-light lip).
- It is **broken** by a 1D noise gate along the crack to ≤ 50 % of the length, is ≤ 0.07 stud wide, and is skipped on
  hairlines.
- Alpha is 0.25-0.26 on the floor and 0.24 on walls (lowered from 0.30 after the first wall renders).
- **W6 was dropped:** chip faces are now a shallow **recess** glaze (W4) with a crisp dark edge on one side and a thin
  broken light edge on the other, instead of a pale patch.
- Checked in `floor_close6_crack.png` and in the 25-stud crops on green and blue: no sticker halo.

### MUST 6: housekeeping
- The counts are now **15 + 2 caps = 17 everywhere**. Every check runs on all 17.
- **Export order** (`grime_lib.export`):
  1. TPDF dither (±0.5 LSB);
  2. the alpha floor (< 2/255 → 0), applied **after** the dither;
  3. confidence-weighted push-pull colour bleed;
  4. texels with alpha < 15/255 eased toward the bleed colour (see Known limitations).

### NICE 1: warm light pool on a floor cluster
`renders\floor_night_lamp.png`: a Moonlit night, with a warm spot lamp on a pole over the G_Moss_A + G_Stain_A cluster
and cracks around it.

### NICE 2: phone check
`floor_eye25_day_half.png` and `wall_eye25_day_half.png` are rendered at 960 x 540, not downscaled, so the mip
selection is real. No moiré or sparkle.

### NICE 3: moss halos ≤ 0.3 and irregular
The halo is clamped at 0.3 and modulated by noise (`moss_render`). The separate rising damp in MossBase is a designed
damp band, not a halo.

### NICE 4: cracks on cream
NOTES now says Decal.Transparency 0.10-0.15 for cracks on cream (and 0.25-0.35 for stains). The preview's G_Crack_B
on the path uses 0.12.

### NICE 5: test patch as JSON
`test_patch.json` gives every carrier's texture, kind (Decal/Texture), face, size, position, yaw and properties, plus a
Luau builder snippet. Its assumptions are listed in it: wall face z 104, bay between the pillars at 13.3 / 39.8, pillars
about 3 wide. Verify these in Studio.

### NICE 6: MossBase at 42.7 px/stud
- `wall_tp4_day.png` is a third-person shot 4 studs from the wall.
- Every painted MossBase feature is ≥ 3 texels:
  - moss noise cell 0.14 stud (6 texels);
  - micro-clumps r ≥ 0.075 (≥ 3.2 px);
  - the min stipple size is held.

## Other changes vs PLAN.md (found in the lit previews)
- **Floor cracks bolder.** Typical half-width 0.10 (0.2 stud wide), open sections up to 0.22. At eye height they
  thinned to hairlines. Crack geometry was rebuilt as **straight runs with sharp kinks** (walk-to-target plus a light
  micro-jag) after the first midpoint-displacement version read as wiggly worms or a spider.
- **Glazes raised to read under the bright hazy hub light.** In the calibrated renders, 0.25-alpha stains were
  invisible:

| Glaze | New alpha |
|---|---|
| damp stain interior | 0.40 |
| mud | 0.50-0.66 |
| rising damp at the floor | 0.56, fading upward |
| drip streaks | 0.5 → 0.28 |

  - All glazes now have soft feathered edges, low-frequency mottling and a **broken** tide line, because the first
    versions read as flat cut-out stickers, including a "cardboard mountain" damp band.
- **Damp and mud colours.** W1 is now a deeper, more saturated brown-green (38,50,22), so wet plastic reads as damp,
  not as a cast shadow. G_Stain_B became real mud: warm (86,60,34), more opaque, with lighter dried-crust patches,
  crust cracks and a dark wet rim, so it can't be mistaken for the dummy's shadow.
- **Slime.** The painted gloss threshold was tightened; the old one flooded the whole flat top, so the slime looked
  pastel. The body now maps to the saturated lime S2, with crisp lit-side highlights.
- **Lighting calibration.**
  - **Tone mapping:** AgX was too pale and desaturated next to the game, so the previews use Khronos PBR Neutral.
  - **Ambient vs sky:** ambient and the visible sky are split with Is-Camera-Ray, so the night can have a dark starry
    sky and still be readable.
  - **Haze:** a uniform Roblox-like veil is applied in post. Eevee's world volume rendered black.
  - **Night:** gets the Moonlit preset's saturation boost.
  - **Result:** day and night within about 15 levels of the in-game screenshots. Numbers are in NOTES section 5.
- **Fringe check redefined.** The plan's "naive vs correct mips ≤ 8/255" is now measured on **edge blocks** (blocks
  that mix alpha-0 and visible texels, where halos live).
  - The gate is p99 ≤ 8/255 at mips 1-2, and mip 3 must be no worse than black fill.
  - Black-fill and white-fill errors are listed for comparison: our fill beats both everywhere, while white fill
    reaches 20-38/255.
  - See Known limitations for the remaining intrinsic mixing.

## Known limitations
1. **Floor decals at eye height.**
   - From 25+ studs at eye height 5, floor decals are foreshortened about 5x.
   - Cracks, moss and slime stay readable. Stains are deliberately subtle (`floor_eye25_day.png`); they read best from
     the default third-person camera (`floor_tp_day.png`).
   - NOTES suggests scaling floor decals up to +15 % in large open areas.
2. **Mip 3 mixing.**
   - At mip 3, the one-sided light lip next to the opaque crack core mixes in straight-alpha mips. It is real
     low-alpha highlight, not bleed: up to about 9/255 p99, always ≤ the black-fill reference.
   - It was not visible in the naive-vs-correct comparison.
   - Texels below 15/255 alpha carry a colour eased toward the neighbourhood, which changes the visible composite by
     ≤ about 3/255.
3. **End-cap joins.**
   - A cap's inner edge wraps to its own transparent outer edge, so a half-texel (0.012 stud) at the join can blend.
   - It was not visible in the previews.
   - If a hairline ever shows in Studio at a cap join, overlap the cap 0.03 stud onto the strip.
4. **MossBase softness.** At 42.7 px/stud (24 studs on the 1024 cap), MossBase is slightly soft closer than about
   4 studs.
5. **The mock is a stand-in.** Eevee approximates Roblox. The studs are a normal/AO tile. The garland and the 5-stud
   dummy are placeholders. The haze is a uniform veil. The Roblox U direction on the wall Front face (u = 0 at the
   viewer's left) is assumed; NOTES and the test patch tell the lead how to spot and fix it (slide W_Crack_C to the
   low-moss stretch).
6. **Test patch positions.** Round 2 uses the lead's measured Studio facts; they are still listed under `verify` in
   `test_patch.json` so the lead can confirm them before building.


## Round 2: visual review (`REVIEW.md`, FIX) item by item

Every MUST and NICE item is applied. After the changes I regenerated all 17 PNGs, re-ran every check and sheet,
re-rendered all 40 previews and re-laid the test patch.

- **Checks** (`checks.json`):
  - all 17 files: the edge rule, fringe (max 3.59/255 on the edge blocks), size and multiple-of-4 rules pass;
  - `mossbase_seams.seamless_ok` = True;
  - `hidden_bands` all ok (W_Crack_C continuation 0.955, W_Drip_B 1.0);
  - `floating_moss`: **0 floating blobs in all 9 wall textures**.

### MUST 1: W_Crack_C read as a dead tree
- **Redrawn from scratch** (`rec_cracks.w_crack_c`). It has no trunk, no root flare, no upward Y-fork and no bush.
- **Base:** a broken triangular **notch recess** at the floor line, painted as a hole (D1 floor, D2 wall in the light,
  a thin broken W5 lip). It replaces the old taper.
- **Crack:** an **angular zigzag** from the notch apex through 7 alternating kinks. The segments swing 15-27° either
  side of vertical, so each kink turns about 30-50°.
  - The width pulses: two open sections, hairline tips.
  - The core edges carry the NICE 1 micro-jag.
- **Branches:** 4 branches that leave at **shallow or downward** angles and end in hairlines.
- **Moss:** only **inside the notch** (clipped to the notch shape) and on **2 ledges** (25 % and 52 % up), plus one
  grass sprig. The old round moss bush is gone.
- **Damp:** a soft rising-damp glaze under the notch.
- **Kept:** the 0.375 hidden band (continuation 0.955) and the A low-slot fit. MossBase_A's moss is ≤ 1.1 stud tall over
  6.7-10.3 studs, and the notch sits in it.
- **Gate:** `sheets\gate_W_Crack_C_vs_A.png` puts W_Crack_C next to W_Crack_A at 1/8 and 1/4, on blue and cream. Both
  read as cracks; W_Crack_C reads as "a crack from a broken corner". Also see `thumbs.png`, `wall_eye25_day.png`,
  `wall_close8_day.png` and `order_wall_*`.

### MUST 2: stains read as cast shadows / G_Stain_B as a slug
All new recipes in `gen\rec_stains.py`.
- **(a) Hue, not just value.** Two saturated wet-ground families replace the grey-brown glaze:
  - `G_Stain_A`: deep **olive** SO1 (52,74,20) / SO2 (26,44,8);
  - `G_Stain_B`: warm **umber** SU1 (104,64,22) / SU2 (52,30,10).
  - Next to the dummy's grey-blue shadow (`floor_close6_crack.png`, `floor_tp_day.png`) they read as wet ground, not
    as shade.
- **(b) Watermark structure (G_Stain_A):**
  - a crisp 1 px outer edge;
  - a **lighter, mottled interior** (α 0.26, minus 25 % toward the dried middle);
  - a **crisp darker rim band** (α 0.6, 0.15 stud);
  - **2 broken inner rings** at 0.55 and 1.25 stud in.
  - At 5x foreshortening it stays a ring, not a blob (`floor_eye25_day.png`, `order_wallfoot_*`).
- **(c) G_Stain_B is now a mud skid, not a capsule:**
  - an irregular 4-lobe **splash head**;
  - 7 overlapping **scuff lanes** of different lengths that taper in the drag direction and break into gaps;
  - a noise-broken edge;
  - the rim only on the wide parts (no outlined "tentacles"), a ring on the head;
  - 12 **elongated splatter** drops thrown ahead and to the sides.
  - An intermediate version read as a jellyfish (head + outlined tentacles). It was reworked into broad broken lanes
    before sign-off.

### MUST 3: free-floating wall moss
- **Clumps (MossBase A/B and the caps):** the free clumps and stipples above the mass were cut.
  - What is left: a few **attached satellites**, 0.1-0.4 stud from the top clumps (A 5, B 3, caps 1).
  - Size falls off with distance.
- **Tongues:** the creeping tongues are rebuilt as **connected plumes**.
  - A broad foot, ragged flanks and a blunt lumpy top, 2.3-2.7 studs tall.
  - They are made of overlapping cushions, with no stalk. An intermediate version climbed as thin diagonal "arms" and
    was redone.
- **Shared seam set:** regenerated as the base run only (no spores), so nothing floats and nothing repeats every 24
  studs.
- **W_Crack_C:** its moss is now only in the notch and on 2 ledges.
- **New automatic check:** `checks.json["floating_moss"]` (`make_sheets.floating_moss`).
  - Moss = α > 0.75 and green-lit.
  - Anchors = the mass touching the contact line + the dark crack cores.
  - A blob of ≥ 3 px more than 0.5 stud from every anchor counts as floating.
  - **Result: 0 floating in all 9 wall textures.** Attached satellites: W_Crack_A 4, W_Crack_B 3, W_Crack_C 3, W_MossBase_A 8, W_MossBase_B 3, W_MossBase_EndL 1, W_MossBase_EndR 0, W_Drip_A 0, W_Drip_B 1.
  - The reviewer counted about 20 floating clumps in W_MossBase_A alone in round 1.

### MUST 4: W_Drip_B goo band was a hard rectangle
- The band height now follows a smooth envelope that **thins to nothing at the left end** (x 0.35 → 1.25 stud) and
  **ends in a rounded ooze lobe** at the right (x 3.45).
- The wavy lower edge is kept.
- The hidden part behind the trim is limited to x 0.3-3.82, so no square corner shows below the trim.
- Hidden-band continuation 1.0. See `overview_wall.png` and the `fringe_wall.png` 2x2 tile.

### MUST 5: chips rendered as glass shards
- `grime_lib.paint_recess` was rewritten.
  - A **dark W4 recessed fill** (α about 0.42, slightly deeper on the shaded wall).
  - A thin, noise-**broken light edge only on the lit inner wall** (the wall that faces the light).
  - **No rim on the shadow side** and no pale fill.
- **Chips are placed on the crack:** every spall chip now overlaps its crack core (its centre is offset by
  0.6 x half-width + 0.35 x depth). Chips that did not touch a core were dropped.
- The loose "pebble" chips (`paint_pebble`) are no longer used anywhere.
- **Crater (G_Crack_B):** it showed the studs through a pale tinted floor, which read as a lens. It now has an
  **opaque rubble floor** (α 0.84, D1/W9 mottle, a few W8 crumbs), the light-side wall's shadow across the floor, and a
  striated inner wall band. See `floor_close6_slime.png` (on cream).

### MUST 6: re-laid test patch (`test_patch.json` + NOTES section 4)
- **(a) Off Base2.** The patch is now in the bay between the pillars at x 39.8 and 66.4, using the lead's Studio facts:
  - faces x 41.05 / 65.15, clear width 24.1, centre 53.1 (the lead's note said 52.6; the true midpoint is 53.1);
  - the patch spans x 41.05-65.15, clear of Base2 and Base3 with their +4 margins (checked by the script).
- **Recomputed x:**
  - W_Crack_C = left face − 8.5 = **56.65** (on the A low-moss slot);
  - W_Crack_B = right face + 6 = **47.05**, y 4-14;
  - MossBase_A = one Texture carrier, face to face, 24.1 wide.
- **(b) Drip vs crack.** W_Drip_A is now by the **left** pillar (x 61.04): its visible content starts 2 studs from the
  pillar face. The script measures the min distance between the visible content of every wall pair from the PNG alpha
  (in world space, hidden bands excluded) and refuses a patch with any pair < 2 studs.
  - Result: MossBase_Bay | Crack_Diag 2.39, MossBase_Bay | Drip_Damp 10.81, Crack_FloorUp | Crack_Diag 6.13, Crack_FloorUp | Drip_Damp 5.05, Crack_Diag | Drip_Damp 13.29.
  - MossBase to W_Crack_C is exempt by design.
- **(c) Floor moss reaches the wall.**
  - Moss_UnderCrack (`G_Moss_A`, under W_Crack_C) and Moss_WallFoot (`G_Moss_B`, near the right pillar) are pushed in
    until their moss ends **≤ 0.4 stud** from the wall foot.
  - A Top-face decal's image-top direction (+Z or −Z) is unverified, so they are placed to satisfy this in **either**
    orientation; the surplus slides under the wall, which hides it.
  - Rotation 0, because a yaw would lift one corner off the foot.
  - Proof: `wall_foot_top_ortho.png` and `wall_close8_day.png`; the pillar bases are clear.
- **Mock = patch.** The Blender wall mock now reads `test_patch.json` (mock x = −(X − 53.1), mock y = Z − 104, a proper
  rotation, no mirror) and has the 2.5 x 1.7 pillars. Every wall render shows the exact patch layout; the side
  sections are catalog-only.

### NICE 1: crack line quality
- **Wedge roots:** `branch(..., root=)` widens a branch's first quarter into a wedge. G_Crack_B's crater rays use
  root 0.7, so they are no longer spider legs.
- **Micro-jag:** an angular Worley-cell jitter (cell 0.09 stud, ±1.2 px) on the core edges of every crack, faded out
  on hairlines.
  - A fBm version looked hairy and was replaced.
- **Crater:** about **1.8 studs** (radius 0.9, 11-sided), with a **visible D2 inner wall** on the lit side, D1 in shade,
  0.24 stud wide.

### NICE 2: the damp band drew a mountain range
- **Tide line:** broken irregularly by two incommensurate noise gates (it has to stay periodic over 24 studs for the
  seam), so there are no periodic dashes.
- **W_MossBase_B wicks:** narrow, ragged fingers (exponential falloff plus noise) instead of mountain peaks.
- **Caps:** the damp now fades by noise (`t = (x + 5) / 3.2 + 0.35 * noise`), not along a straight 45° ramp.
- Evidence: `fringe_wall.png` (white row) and `overview_wall.png`.

### NICE 3: G_Slime_A read as a stamped icon
Now an **asymmetric splat**:
- an uneven 6-lobe pool;
- ONE broad run-off tongue toward the upper right, ending in a blunt lobe (an intermediate thin horn was blunted);
- 5 elongated droplets thrown the same way;
- a **darker thick-pool core** (`slime_paint(thick_core=1.0)`);
- a contact ring (α 0.46) that shows on cream.

See `floor_close6_slime.png` and `swatch_G_Slime_A.png`.

### NICE 4: round drops
- Both stains' drops are **irregular elongated** ellipses, warped by noise, each with a small trailing lobe and only a
  faint darker end. No round rivets, and no rims of their own.

### NICE 5: G_Crack_C read as a ladder
- The **rail gap varies** (0.7-1.35 stud).
- The **cross cracks are angled** (offset −0.5 to +0.45 stud) and fewer: 3 full and 1 half.
- **Chunk 4 visibly tilts** (W4 0.46 on the low side, W5 0.3 on the raised lit edge).
- Chunk 2 is missing, with moss and grass in the hole.

### NICE 6: test_patch.json
- `verify` lists:
  - floor top y 0;
  - wall face z 104.00;
  - trim bottom y 22.9;
  - the pillar depth (centres z 103.1, proud from 104 to 102.3, 2.5 wide);
  - the pillar faces.
- `after_building` says to **delete the GrimeTestPatch ModuleScript**. The Luau snippet now ends with
  `workspace.GrimeTestPatch:Destroy()`.
- It also says to **show the owner the default third-person view** as well as eye height
  (`renders\wall_tp_day.png`, `wall_tp_night.png`).

### Round 2 known limitations (in addition to the list above)
- **Floor decal orientation.** The orientation of a Top-face Decal's image in Roblox is unverified. The wall-foot moss
  is placed to work either way; the other floor decals don't depend on it.
- **Stains stay a quiet layer.** They are now clearly wet ground rather than shadow, but from 25+ studs at eye height
  they are still faint by design. Judge them from the third-person view.


## Round 3: polish after the round-2 PASS (`REVIEW.md` "Round 2" NICE 1-3 + the lead's notes)

Every open polish item is applied. Everything that passed is kept: the edge rule, bleed bands, hidden bands, seams and
the `test_patch.json` layout (re-generated from the new PNGs, same positions and clearances: MossBase_Bay | Crack_Diag 2.39, MossBase_Bay | Drip_Damp 10.81, Crack_FloorUp | Crack_Diag 6.13, Crack_FloorUp | Drip_Damp 5.05, Crack_Diag | Drip_Damp 13.29).
All 17 PNGs were regenerated, and all checks, sheets and 40 renders were re-run. Results:
- all 17 files pass the edge, fringe, size and multiple-of-4 rules (edge-block fringe max 2.08/255);
- `mossbase_seams.seamless_ok` = True;
- every hidden band is ok (W_Crack_C 1.0, W_Drip_B 1.0);
- `floating_moss`: 0 in all 9 wall textures.

### N1: glassy chips and lips
- **Separate chip polygons dropped** on W_Crack_A, W_Crack_B (the chip and the pocket beside its open section),
  W_Crack_C, G_Crack_A and G_Crack_C. Only the open-section bevels of the cracks themselves remain.
  - The random draws for the old chips are still made, so every crack line keeps exactly its reviewed shape.
- **G_Crack_C tilt:** the tilted chunk is now one bounded by drawn cross cracks on both sides (the old one had an
  undrawn straight edge, which is what made it read as a pane).
  - It gets a **darker W4 tint** that deepens toward the sunken rail.
  - The tint is feathered inside the cracks, so no straight polygon edge shows.
  - No W5 at all.
- **Lips gate-broken:** `paint_cracks` now multiplies the along-crack gate (on 45 % of the length, down from 50 %) by a
  second 2D noise gate at another scale.
  - Every lip is on well under half its length, with irregular gaps.
  - The continuous white lip on G_Crack_A's open section is gone.
- **Ticks removed:**
  - The G_Crack_B crater-top tick came from a rim "pocket" polygon. Both pockets are gone.
  - The crater rim's pale lip is gone too. It also drove the far-mip mixing: G_Crack_B's mip-3 edge p99 is now
    3.94/255 against a black-fill reference of 8.54.
  - The W_Crack_C notch has no rim light any more (`paint_polys_hole(..., rim_light=0)`).

### N2: G_Crack_B read as a spider on cream
Rebuilt (`rec_cracks.g_crack_b`):
- **Pit:** an angular, slightly long pit (8-sided, irregular, 1.9 x 1.55 studs).
- **Long rays:** TWO long, bold rays (3.5 and 3.05 studs) roughly across each other. Each is a straight run with 2 sharp
  kinks.
- **Short rays:** five SHORT thin stubs (0.45-0.85 stud, less than half the width of the long rays) at uneven angles.
- **No knee bends.** The mid-ray side branches are gone.
- **Ring pieces:** straight concentric ring chords that slightly cross the rays they join, so they read as a
  spider-web fracture and not as leg joints. Two are bold and two thin.
- See `renders\floor_close6_slime.png` (on the cream path) and `sheets\swatch_G_Crack_B.png`.

### N3: leftovers
- **MossBase damp (A and B):**
  - B's rising-damp wicks are rounded (Gaussian) bumps instead of exponential cusps, so there are no flame spikes.
  - The ragged-top noise only acts where the damp is tall.
  - Tide-line pieces now survive only on flat stretches (a slope gate) and in longer runs (a lower-frequency break
    gate), at alpha 0.18. The curved "eyebrow" ticks are gone.
  - B's second, inner tide line was removed.
  - The seam band is untouched: every change is a function of the shared profile there, and `seamless_ok` stays true.
- **EndL / EndR:**
  - The cap damp fades along a smooth sine ramp with a gentle low-frequency wobble (no pointed peaks).
  - The satellite on both caps (EndL's "dark pill") is removed.
- **W_Crack_C:**
  - The damp behind the notch is a soft elliptical fan whose density falls off with distance. There is no outline, so
    no "mountain" peaks.
  - The grass sprig that read as a pink worm is removed.
- **G_Stain_A:**
  - The rim is broken in 3 places (soft gaps around the outline).
  - Its width varies by ±45 % around the outline.
  - The lower-right lobe became a long flat run-off and the upper-left lobe is squashed, so it is no longer a
    cloud/teddy-head silhouette.
- **W_Drip_B:** the left end of the goo band is now a rounded quarter-ellipse with a small sagging lobe, not a straight
  bevel.

### Lead's note: MossBase A mounds lower and flatter
- The big cushions in A are flatter (squash 1.25 x 0.66, radii 1.5-2.1) and the two plumes are lower (tops 1.55 / 1.3).
- The tallest moss in A is now about 1.9 studs (it was 2.9). The W_Crack_C slot stays low (≤ 0.75).
- Seams are unchanged. In `wall_eye25_day.png` the mounds now sit low along the wall foot.
- B is unchanged; its 2.6-stud wick plume still gives a taller option if the owner wants one.


## Round 4: owner feedback on the live-game test patch ("mushier first")

The owner kept the cracks and asked for thicker, taller, greener moss and darker, wetter damp. The live-game
screenshots (`ingame_round3\`) showed three problems:
1. The back wall is in shade in the game, so MossBase rendered as a thin dark fringe.
2. G_Stain_A read as a cast shadow next to the pumpkins.
3. The floor moss was hard to see.

**Untouched:** all six crack textures and both drips are **byte-identical** to round 3 (md5 checked before/after).
`W_Crack_C` included.

### 1. The mock is re-calibrated against the live game
- **New fitter `gen\calib_fit.py`.** It renders the plain bay from the live-game third-person framing
  (`calib4_day/night`) and samples 4 surfaces at projected world points:
  - the shaded wall;
  - the shaded floor at the wall foot;
  - the sunlit floor;
  - the pillar front.
- **How it fits.** It inverts the veil (and the night saturation boost), then fits per channel in linear light:
  - the sky colour from the shaded floor;
  - the sun strength from the sunlit floor (the sun keeps a warm-white colour, so sunlit decals keep true hues; the
    floor albedo absorbs the rest);
  - the wall and pillar albedo from their shade values;
  - at night the moon colour is free (the Moonlit grading).
  - Result in `gen\calib_round4.json`, which `mock_preview.py` loads.
- **Geometry.** The sun now stands **behind the back wall** (direction (0.25, 0.42, 0.87), about 60° up), as in the
  game. The wall face and the floor at its foot only get sky light; the wall's shadow reaches about 12 studs onto the
  floor.
- **Fit error (render minus game, sRGB levels):**

| Surface | Day | Night |
|---|---|---|
| wall | [0, 0, -1] | [15, 11, -27] |
| shaded floor | [0, 0, 0] | [1, -1, 0] |
| sunlit floor | [0, 0, 0] | [0, 0, 0] |
| pillar | [0, 0, 0] | [0, 0, -11] |

  - Day matches within 1 level.
  - The night wall stays about 15-27 levels less saturated blue than the game, so the mock night is conservative.
- **Other mock changes:**
  - The studs are now the game's rounded squares (`make_studs.py`), with slightly lighter tops.
  - The day haze veil is lowered from 14 % to 6 %.
  - New shots in the live-game framing at 1520 x 752: `game_tp_day`, `game_close_day`, `game_tp_night` and
    `game_tp_day_before`.
- **Validation.** `sheets\ingame_vs_mock.png` shows, per row:
  - the game screenshot;
  - the re-calibrated mock with the **same round-3 decals** (`renders\calibcheck_r3_*`, from the archived set in
    `decals_round3\`), where MossBase reproduces the game's thin dark fringe;
  - the round-4 decals in the same light.

### 2. W_MossBase_A/B + end caps: mushier
- **New moss palette.** MM1-MM5: (32,62,16) / (64,112,24) / (104,160,34) / (166,214,52) / (222,248,104).
  - The tips are lit-side lime and cover more (`tip_lo` 0.42, `tip_amt` 1.0, value 0.97, dome 1.25).
  - In the wall's cyan-blue shade it now renders clearly green, not near-black. Cracks keep the old palette through a
    `pal` switch in `moss_render` (default None = bit-identical).
- **Mass.**
  - The base run is thick and continuous (base cushions R 0.9-1.45).
  - Broad mounds: A about 3.2-4 studs, B about 3 studs.
  - Blunt plumes climbing to about **5.0 studs** in places (A at u 14, B at u 6).
  - Median moss height: A 2.7 studs, B 1.85.
  - The mounds are wide domes on the mass, not trees on stalks.
- **Low-moss slots for floor-up cracks kept:** A 6.7-10.3 is ≤ 1.05 stud over 7-10 (edges ≤ 1.22); B 12.2-15.8 is
  ≤ 1.15. Big neighbours are capped so they don't spill into a slot.
- **Seam band.** The shared seam set got a medium mound centred on every join (about 1.8 studs), so there is no dip
  every 24 studs. The caps fade from it to nothing over about 4 studs.
- **Damp.**
  - A taller, darker wet band (WD1 (20,36,12), alpha up to 0.74 at the floor) above the moss: A about 3.4, B about 3.0
    with rounded wicks, soft-capped at 4.35 so its fade ends inside the tile.
  - A subtle **wet sheen**: faint pale streaks running down the band (SH, alpha ≤ 0.11).
  - The broken tide line is kept on flat stretches.
- **Checks:**
  - `mossbase_seams.seamless_ok` = True (A|B seam max 0.2131/255 against the strips'
    own neighbour p99 0.1922);
  - hidden bands ok (continuation 1.0);
  - **0 floating moss**;
  - edges and fringe ok.

### 3. G_Moss_A/B: bigger cushions, brighter tips
- The cushions are about 1.3x fatter (G_Moss_A main cushion R 1.15 → 1.5; G_Moss_B along the joint R up to about
  1.2), with the same mushy palette and tips.
- The carrier sizes are unchanged, so the test-patch floor positions are unchanged.

### 4. Stains: wetter and darker, but clearly not shadows
- **G_Stain_A:**
  - a deeper green-olive tint (SW1 (40,72,22) / SW2 (18,36,8));
  - a darker wet interior (alpha 0.40);
  - a clearly **defined tide edge** (alpha 0.74, 0.13 stud, only 2 short breaks);
  - inner rings;
  - **36 glossy wet flecks** (elongated sky reflections, 0.1-0.28 stud, all roughly one way, never on the rim);
  - a faint sheen patch and a thin broken **sky-reflection line** inside the far rim.
  - A cast shadow has none of these: it is grey-blue, untextured and has no highlights.
- **G_Stain_B:** a wetter, darker umber (SU3/SU4, alpha 0.54), a darker rim and 26 gloss flecks.
- Fringe: G_Stain_A's edge blocks are p99 7.68/255 at mip 3 (the black-fill reference is
  15.36).

### 5. G_Slime_A: 20 % bigger
- The carrier is now **6 x 6** (same 512 px art, drawn in 5-stud space, so 85 px/stud).
- The optional plaza-rim slime still clears the star crack by ≥ 2.35 studs in all 4 possible Top-face orientations.

### 6. Test patch
- The layout is the same.
- Only `Crack_Diag` (W_Crack_B) moves: up from y 4-14 to **y 5.75-15.75**. The moss is taller now, and
  `make_test_patch.py` lifts it in 0.25 steps until it is ≥ 2 studs clear of the moss.
- Clearances: MossBase_Bay | Crack_Diag 2.13, MossBase_Bay | Drip_Damp 9.26, Crack_FloorUp | Crack_Diag 6.11, Crack_FloorUp | Drip_Damp 5.05, Crack_Diag | Drip_Damp 12.52.
- The floor moss still reaches the wall foot (≤ 0.4 stud).

### Round 4 results
- All 17 files pass the edge, fringe (max 5.41/255), size and multiple-of-4 rules.
- Seams, hidden bands and floating moss are all ok.
- 44 preview frames were re-rendered with the new calibration, plus the calibration frames.

### Round 4 notes / limitations
- **W_Crack_C notch moss.** W_Crack_C was frozen with the cracks, so its small notch moss keeps the darker round-3
  palette. It sits in MossBase's low slot next to the brighter round-4 moss. If the owner notices, only that moss can
  be retinted to the new palette, with the crack untouched.
- **The look from 25 studs.** MossBase now reads as a thick overgrown mossy hedge along the wall foot. If the owner
  wants it lower in places, use B on more bays (median 1.85 vs A's 2.7).
- **Frame differences.** The mock can't reproduce the game's dynamic shadows from props, the candle light pools or the
  vines. The comparison frames have no pumpkins.


## Round 5: review of round 4 (FIX, 2 MUST + NICE)

The direction stays. The brightness, the thick continuous base and the dark wet band are kept; only the silhouettes
and the chroma are trimmed.

**Changed PNGs (md5 against round 4):** G_Moss_A, G_Moss_B, G_Stain_A, W_Crack_C, W_MossBase_A, W_MossBase_B, W_MossBase_EndL, W_MossBase_EndR.

**Unchanged:** G_Crack_A, G_Crack_B, G_Crack_C, W_Crack_A, W_Crack_B, W_Drip_A, W_Drip_B, G_Stain_B, G_Slime_A.

### MUST 1: no hedge of round bushes
- **Thick mat:** a continuous 1-2 stud moss mat (base cushions R 0.85-1.35).
- **Broad masses, capped:** two per tile at uneven spacing (A at u 3.7 and 15.2, B at u 9.6 and 20.0), about 2.3-2.6
  studs tall, much wider than tall (squash 1.55 x 1.2).
- **Round crowns replaced by ragged climbing tongues** (2 per tile, irregular spacing: A at u 13.7 and 20.7, B at
  u 5.9 and 17.5):
  - a modest foot;
  - a column that narrows toward the top, wanders sideways and has ragged flanks;
  - a broken, lumpy top (2 small tufts touching the tip);
  - tops about 3.1-4.0 studs, so the moss reaches at most 4.45 (A) / 4.57 (B).
- **Macro dome shading flattened:** the moss look's dome went from 1.25 to 0.55, with cavity darkening 0.22 and the
  per-clump lumps kept (`lump_k` 0.95).
  - An intermediate setting (dome 0.4, `lump_k` 1.25) read as cobblestones and was backed off.
  - The floor cushions (G_Moss_A/B) keep their round-4 volume: domes are right on the floor; only their colour
    changed.
- **Seam mound lowered:** about 1.2 studs now (was about 1.8), so the chain doesn't pulse every 24 studs.
- **Results:**
  - median moss height A 2.37 / B 2.19 studs (A was 2.7);
  - W_Crack_C slots kept: A ≤ 1.08 over 7-10, B ≤ 0.77;
  - `sheets\mossbase_seams.png` shows no even "bush every N studs" rhythm;
  - `wall_oblique20_day` reads as a moss mat with tongues, not a row of cut-out bushes.

### MUST 2: no neon
- **Body moved toward olive** with the value kept:
  - MM1 (56,68,40), MM2 (84,106,50), MM3 (122,150,62);
  - tips MM4 (166,194,80), sparks MM5 (204,226,120).
- **Lime only on a minority of lit tips:** `tip_amt` 0.58, `tip_lo` 0.5.
- **Dying patches:** olive / yellow-brown (MD1 (66,62,26) → MD2 (146,134,62)), from a low-frequency periodic field.
  - In MossBase they are kept out of the shared seam band (that was the only cause of a cap-seam mismatch).
- G_Moss_A/B take the same colours.
- **Gate** (new `checks.json["moss_chroma"]`: the wall-moss pixels in `game_tp_day/night`, the same pixel mask as the
  reviewer's measurement):

| | Day | Night | Gate (day / night) |
|---|---|---|---|
| moss median saturation | 0.591 | 0.718 | 0.68 / 0.75 |
| slime drip median saturation | 0.798 | 0.904 | |

  - **PASS.** The slime is still the most saturated green.
  - The moss median value is 0.482 day / 0.416 night, with a mean
    of [80, 141, 81] in day shade: it is clearly green, not dark, on the shaded wall.
- **The night needed a calibration fix as well as the palette change.**
  - The same metric on the owner's own round-3 screenshots gives 0.58 day / 0.67 night, while the round-4 mock gave
    0.65 / 0.82 for the very same decals. The mock night over-saturated green moss by about 0.15.
  - `calib_fit.py` now also fits the night sky colour on the wall moss (round-3 decals, `calib4m_*` frames) next to
    the floor (weighted x2) and the wall.
  - The night errors are now spread instead of loaded on the moss: shaded floor [-5, -8, 20], wall
    [8, 3, 0], round-3 moss [0, 9, -20]. The mock moss is still a little greener than the game,
    so the gate is conservative.
  - The day fit is unchanged and within 0-1 level; the day moss renders darker than in game, which is also
    conservative.

### NICE
1. **W_Crack_C notch + 2 ledge tufts** now use the final MossBase look (palette, tips, dying patches).
   - Only the moss colour pass changed. The halo and shadow glazes keep their round-3 colours.
   - Checked pixel by pixel against round 4: alpha is identical everywhere.
   - Every changed texel with alpha ≥ 15/255 lies in the three moss rows (the notch and the two ledges).
   - The only other changes are alpha < 6 % edge texels whose stored colour follows the colour bleed: ≤ 6 levels after
     compositing.
2. **G_Stain_A:** 36 white flecks → 14 long faint streaks (0.22-0.48 stud long, ≤ 0.07 wide, alpha 0.26-0.42). The
   rim reflection line is kept. G_Stain_B is untouched.
3. **EndL/EndR damp fade:** the cap damp now wobbles along its whole fade (three proportional noise octaves outside the
   shared seam band). There is no straight diagonal and no dome, and no pointed peaks either, because the wobble
   scales with the local damp height.
4. **Re-checked:** `mossbase_seams.png` (irregular), `wall_oblique20_day` (no cut-out bushes).

### Checks
- All 17 files pass the edge, fringe (max 5.41/255), size and multiple-of-4 rules.
- `seamless_ok` = True (band identity: caps 3.0 / 2.0, A vs B 0.05).
- Hidden bands are ok, with 0 floating moss.
- 44 previews plus the `calibcheck_r3_*` frames were re-rendered in the re-fitted light; `sheets\ingame_vs_mock.png`
  was rebuilt (its right column is now the round-5 decals).

### Test patch
- The layout is the same.
- `Crack_Diag` sits at y 5.25-15.25. The script lifts it only as far as needed; the moss is lower now, so it moved
  down 0.5 from round 4.
- Clearances: MossBase_Bay | Crack_Diag 2.11, MossBase_Bay | Drip_Damp 9.26, Crack_FloorUp | Crack_Diag 6.15, Crack_FloorUp | Drip_Damp 5.05, Crack_Diag | Drip_Damp 12.72.


## Round 5 polish: review round 5 NICE 1-4 (owner approved the rollout)

Texture-only changes. The following are unchanged:
- the palette and saturation (the moss chroma gate stays at day 0.591 / night
  0.719, against the slime's 0.798 / 0.904);
- the seamless A/B/cap joins, the hidden bands, the base mat (the same base-run code), and the transparent margins;
- the W_Crack_C low-moss slots (A 6.7-10.3: ≤ 1.08 stud; B 12.2-15.8: ≤ 0.77);
- file names and sizes.

NICE 5 (the per-bay `OffsetStudsU` variation) is placement, so the lead is doing it.

**Changed PNGs (md5 against round 5):** G_Moss_A, G_Moss_B, W_Crack_C, W_MossBase_A, W_MossBase_B, W_MossBase_EndL, W_MossBase_EndR.

- **W_Crack_C** changed only in its moss colours (the new dying-patch settings); its crack is untouched.
- **G_Moss_A/B** changed only through the dying-patch settings.

### NICE 1: tongue tips and lean
- The column now stops 0.45 stud below the top and ends in **three lumps across the tip**. The middle lump is highest
  and the two side lumps are lower and smaller, so the top is neither a spire point nor a flat block.
- The two tongues of each tile **lean in opposite directions**: A at u 13.7 right / u 20.7 left, B at u 5.9 left /
  u 17.5 right. Runs of alternating A/B therefore never repeat the same fin direction.

### NICE 2: no box-hedge masses
- New `mb_mass`: one or two tall centre cushions, plus **lower shoulder cushions that reach the full foot width**, so
  the sides fall at about 45-55°.
- The top line is broken by 1-2 lumps.
- The old box masses were partly clipped by the seam-band filter (that made their vertical side). The new masses sit
  fully inside the unique zone:
  - A at u 4.4 (half-width 2.3) and u 15.5 (3.8);
  - B at u 9.2 (3.0) and u 19.4 (2.5).
- **Heights:**
  - median moss height A 1.97 / B 1.84 (round 5: 2.37 / 2.19); rounded shoulders hold less moss than box sides;
  - max 4.2 / 4.1;
  - the mat underneath is unchanged (10th percentile 0.79 / 0.70).

### NICE 3: end caps
- **The last stud now wobbles.** The cap's outer damp boundary is a z-dependent edge: it slants inward with height and
  wobbles ±0.4 stud by two noise octaves. It is held constant through the hidden band, so the band stays intact
  (continuation EndL 1.0, EndR 0.959).
- Two small damp lumps sit near the end.
- **No comb streaks:**
  - the fine ragged-top octaves are damped to 40 % in the caps;
  - the 8x wobble octave is gone;
  - the top fade is softer (t 0.70 → 1.32 instead of 0.85 → 1.22);
  - the wet-sheen streaks are at 40 %.
  - All of this applies **outside** the shared seam band only, so the joins are unchanged.

### NICE 4: dying patches
- Fewer, larger and softer:
  - noise cell 1.7 instead of 0.85;
  - threshold 0.40 → 0.85 instead of 0.38 → 0.62;
  - blend 0.6 instead of 0.8.
- More yellow-olive: MD1 (88,92,38) → MD2 (172,170,78) instead of the orange-brown (66,62,26) → (146,134,62).
- They are weighted onto the lit mound tops and the moss edges. No orange freckles in `wall_close8_day`.
- The patches are kept out of the shared seam band, as before.
- This is the shared moss look, so G_Moss_A/B and W_Crack_C's notch/ledge moss follow.

### Checks (all re-run)
- **Seams:** `seamless_ok` = True.
  - Band identity: caps 3.0 / 2.0, A vs B 0.05.
  - Join deltas: A|B 0.2139, EndL|A 0.2159, A|EndR 0.2126, against the strips' own
    neighbour p99.9 of 0.3476.
- **Edges:** every free edge keeps its ≥ 4 px alpha-0 margin (`edge_rule_ok` on all 17), and the fringe max is
  5.41/255.
- **Hidden bands:** all ok. **Floating moss:** 0.
- **Previews:** 44 frames re-rendered, and the sheets were rebuilt (`mossbase_seams.png`, `ingame_vs_mock.png`, etc.).
- **Test patch:** unchanged (Crack_Diag y 5.25-15.25). Clearances: MossBase_Bay | Crack_Diag 2.13, MossBase_Bay | Drip_Damp 9.26, Crack_FloorUp | Crack_Diag 6.15, Crack_FloorUp | Drip_Damp 5.05, Crack_Diag | Drip_Damp 12.72.

## Final nits (polish review "Round 5 polish": 2 optional nits)

**Changed PNGs:** `W_MossBase_A`, `W_MossBase_EndR`. The other 15 are byte-identical (md5 checked before and after a
full regeneration). Names and sizes are unchanged.

### 1. W_MossBase_A's first mass (u about 2-6)
- **Where the flank came from.** The old mass's left shoulder and the first base-run cushion were clipped by the
  seam-band filter at u about 2.0, which left a near-vertical flank about 1.9 studs tall.
- **Rebuilt with its own random stream.** The original random draws are still consumed and the result is discarded,
  so the rest of A (the second mass, the tongues, the mat) is unchanged.
  - The mass is at u 4.6, half-width 2.0, with round top lumps at different heights instead of the flat slab.
  - A slope filter removes any moss above a line of about 49° on its left flank.
- **Gap filled.** A low filler cushion fills the mat gap between the shared seam moss (ends at about u 1.56) and the
  unique zone. It sits at u ≥ 1.62, outside the 1.125-stud identity band; its halo reaches about 1.3.
- **Joins unchanged.** All 8 pairings keep identical join deltas, and A vs B band identity is 0.07/255.
- **W_Crack_C slot unchanged:** u 7-10 ≤ 1.08 stud (u 6.7-10.3 ≤ 1.17, as before). Median moss height 1.93.

### 2. W_MossBase_EndR fade streaks
- EndR's damp height is now smoothed along x (Gaussian, sigma 0.25 stud), blended in only outside the shared seam
  band. The faint vertical streaks are gone and the seam band is unchanged.
- **Results:**
  - EndR vs A band identity 2.0/255;
  - hidden band intact (continuation 0.959);
  - the wobbly slanted outer end is kept.
- **EndL is untouched.**

### Checks
- Every check was re-run and passes: edges and margins on all 17, fringe max 5.41/255, `seamless_ok` true, hidden
  bands ok, 0 floating moss.
- Moss chroma: 0.59 day / 0.72 night against the slime's 0.80 / 0.90.
- The test patch is unchanged.
- 44 previews were re-rendered and the sheets rebuilt.
