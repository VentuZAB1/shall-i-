# HUB GRIME: notes for the lead (round 5, 2026-10-14)

This set adds cracks, moss, damp, mud and slime decals for the Halloween hub. Everything sits on top of the existing
studded surfaces, so the stud style stays.

- **Files:** 17 PNGs in `HubGrime\decals\`. 15 are the briefed set; 2 are approved extras, `W_MossBase_EndL` and
  `W_MossBase_EndR`.
- **Format:** RGBA, straight alpha, ≤ 1024 px per side.
- **How to re-make them:**
  - `python gen\make_decals.py` (the decals);
  - `python gen\make_sheets.py` (the check sheets);
  - `python gen\render_previews.py` (the Blender previews);
  - `python gen\make_test_patch.py` (the test patch JSON).
- **Previews:** in `renders\`. Check sheets are in `sheets\`, and every automatic check is in `checks.json`.
- **Round 2** (visual review `REVIEW.md`): every MUST and NICE item is applied; `BUILD_NOTES.md` "Round 2" maps each
  item to its change. The test patch moved to the bay between the pillars at x 39.8 and 66.4 (section 4).
- **Round 3** (review PASS + polish): every open polish item is applied; see `BUILD_NOTES.md` "Round 3". The test
  patch layout is unchanged.
- **Round 4** (owner: "mushier first", after the live-game test patch): the previews are re-calibrated against the
  live-game screenshots (`ingame_round3\`), and MossBase A/B + caps, G_Moss_A/B, both stains and the slime are
  remade thicker, greener and wetter. **All crack and drip textures are byte-identical to round 3.** See
  `BUILD_NOTES.md` "Round 4" and `sheets\ingame_vs_mock.png`.
- **Round 5** (review of round 4: FIX): the wall moss is a thick mat with ragged climbing tongues instead of a hedge of
  round bushes, the moss green is shifted toward olive (no more neon), W_Crack_C's notch/ledge moss uses the final
  palette, G_Stain_A has fewer, longer, fainter gloss streaks, and the cap damp fades with a wobble again. **Changed
  PNGs: G_Moss_A, G_Moss_B, G_Stain_A, W_Crack_C, W_MossBase_A, W_MossBase_B, W_MossBase_EndL, W_MossBase_EndR.** See `BUILD_NOTES.md` "Round 5".
- **Round 5 polish** (review round 5 PASS, NICE 1-4, texture only): blunt lumpy tongue tops leaning opposite ways in each
  tile, rounded-shoulder masses with lumpy tops, wobbly cap ends without comb streaks, fewer/larger/softer yellow-olive
  dying patches. **Changed PNGs: G_Moss_A, G_Moss_B, W_Crack_C, W_MossBase_A, W_MossBase_B, W_MossBase_EndL, W_MossBase_EndR** (names and sizes unchanged). See `BUILD_NOTES.md`
  "Round 5 polish". Rollout tip from the review (placement): vary `OffsetStudsU` per back-wall bay by 6/12/18 studs,
  except bays that carry a W_Crack_C (offset 0 for the low-moss slot); keep 2-3 bays bare.

## 1. Per texture

**Carrier = the part the decal goes on.**
- **Size:** the carrier is exactly the "carrier (studs)" size; the decal stretches over the whole face.
- **Hidden band:** some textures have a hidden band on one edge. That part of the carrier goes **below the floor top**
  or **up behind the top trim**. Section 2 explains why.

| Texture | Carrier (studs, W x H) | Pixels | px/stud | Surface | Hidden band | Count for the whole hub | Spacing / where |
|---|---|---|---|---|---|---|---|
| `G_Crack_A` (long branching) | 14 x 7 | 1024 x 512 | 73 | floor | none | 5-6 | the cracks share 14-18 in total, about 1 per 250-300 st² of open green inside grime clusters; never the same shape twice within 30 studs |
| `G_Crack_B` (impact pit: 2 long cracks, short stubs, ring pieces) | 10 x 10 | 768 x 768 | 77 | floor | none | 4-5 | one of the 2-3 plaza-rim cracks; on cream use Decal.Transparency 0.12 |
| `G_Crack_C` (split band, uneven gap, one tilted chunk) | 12 x 8 | 960 x 640 | 80 | floor | none | 4-6 | open green, near garden props / graves |
| `G_Moss_A` (fat bright moss cushions on a damp patch) | 8 x 8 | 576 x 576 | 72 | floor | none | 5-6 | the moss shares 8-12 in total: wall feet (ties into MossBase), under trees, beside graves |
| `G_Moss_B` (fat moss along a joint) | 10 x 6 | 720 x 432 | 72 | floor | none | 3-6 | along wall feet (long axis parallel to the wall), path edges |
| `G_Stain_A` (wet green-olive puddle: dark wet interior, defined tide edge, a few long faint gloss streaks, a sky-reflection line) | 10 x 10 | 512 x 512 | 51 | floor | none | 5-7 | the stains share 10-14 in total: under drips, wall feet, under trees; may go UNDER moss and cracks |
| `G_Stain_B` (wet umber mud skid: splash head, tapering broken scuffs, splatter, gloss flecks) | 12 x 8 | 576 x 384 | 48 | floor | none | 5-7 | path edges (straddling the brown edge), around the pumpkin clusters; may go UNDER cracks and moss |
| `G_Slime_A` (asymmetric slime splat: one run-off lobe, droplets thrown one way) | **6 x 6** (round 4) | 512 x 512 | 85 | floor | none | 3-5 in the whole hub | an accent: clean cream / plaza edge, near 1-2 pumpkin clusters, under a slime drip; **never overlapping anything**; never two in one view from spawn |
| `W_Crack_A` (vertical) | 5 x 10 | 384 x 768 | 77 | wall | none | the wall cracks share 10-15 in total, about 1 per 1-2 bays | lower half, centred in a bay below the garland swag; round 4: keep its content **>= 2 studs above the moss** (MossBase now reaches 3-5 studs), so the bottom edge goes about 4.5-6 above the floor |
| `W_Crack_B` (diagonal with open sections) | 8 x 10 | 608 x 760 | 76 | wall | none | (shared, see W_Crack_A) | lower half, about y 5.25-15.25 over MossBase (2 studs clear of the moss) |
| `W_Crack_C` (zigzag crack rising from a broken notch at the floor) | 6 x 12.375 | 448 x 924 | 75 | wall | **bottom 0.375** | 4-6 | always on a MossBase run, centred on a low-moss slot (see below) |
| `W_MossBase_A` (thick 1-2 stud moss mat, 2 rounded-shoulder masses about 2.5 studs with lumpy tops, 2 ragged blunt-topped climbing tongues to about 4.2 leaning opposite ways, low slot for W_Crack_C) | 24 x 6.375 | 1024 x 272 | 42.7 | wall | **bottom 0.375** | along wall bottoms | runs of 1-3 strips (24-72 studs), gaps of 6-20 studs between runs |
| `W_MossBase_B` (thick moss mat, 2 rounded-shoulder masses, wet band with rounded rising-damp wicks, 2 blunt-topped climbing tongues to about 4.1 leaning opposite ways) | 24 x 6.375 | 1024 x 272 | 42.7 | wall | **bottom 0.375** | along wall bottoms | alternate with A |
| `W_MossBase_EndL` (left run end) | 6 x 6.375 | 256 x 272 | 42.7 | wall | **bottom 0.375** | 1 per free left end | its RIGHT edge joins a strip's left edge |
| `W_MossBase_EndR` (right run end) | 6 x 6.375 | 256 x 272 | 42.7 | wall | **bottom 0.375** | 1 per free right end | its LEFT edge joins a strip's right edge |
| `W_Drip_A` (damp streaks from the trim) | 4 x 11.35 | 320 x 908 | 80 | wall | **top 0.35** | the drips share 6-10 in total; about 2/3 of them A | under the top trim |
| `W_Drip_B` (slime drips from the trim) | 4 x 8.35 | 320 x 668 | 80 | wall | **top 0.35** | (shared, see W_Drip_A) | under the top trim |

**Total:** about 40 floor decals and about 30-45 wall carriers, with 17 unique textures (about 10 MB of GPU memory).

## 2. Placing carriers in Studio

### Every carrier
- It goes in `Workspace.HalloweenDecor.Grime`.
- Properties:
  - `Anchored = true`;
  - `CanCollide`, `CanTouch` and `CanQuery` all false (the owner's no-collision rule);
  - `CastShadow = false`;
  - `Transparency = 1`;
  - thickness 0.05.

### Floor decals
- Carrier `Size = (W, 0.05, H)`, with the top face 0.03-0.05 above the floor top.
- `Decal.Face = Top`.
- Any yaw.
- Uniform scale ±15 %. Don't stretch one axis by more than 10 %.

### Wall decals
- Carrier `Size = (W, H, 0.05)`, with the decal face 0.03-0.05 in front of the wall face.
- `Decal.Face` is the face that looks at the hub (`Front` for an unrotated part on the back wall).
- No rotation beyond ±10°: the light is painted from above.

### Layer offsets
Use these distances from the surface, so overlapping decals never z-fight:
- stain 0.03;
- crack 0.04;
- moss, slime and drip 0.05.

### Hidden bands (the textures wrap)
A Roblox `Texture` wraps, and a `Decal` can also show a hairline from the opposite edge. So:
- every edge that does NOT meet geometry has a ≥ 4 px fully transparent margin;
- every edge that DOES meet geometry has content running ≥ 0.25 stud past the contact line, then the 4 px margin.

You only have to put the contact line where the table says:

| Texture | Where the carrier goes |
|---|---|
| MossBase A/B/EndL/EndR, W_Crack_C | carrier bottom = **floor top − 0.375**. The band sinks into the floor part. |
| W_Drip_A/B | carrier top = **trim bottom + 0.35** (y 22.9 + 0.35 = 23.25 on the hub walls). The band sits behind the trim, which sticks out 0.3. |

### MossBase runs
- **Preferred: `Texture`.**
  - One carrier per run, with `StudsPerTileU = 24` and `StudsPerTileV = 6.375`.
  - The carrier is exactly 6.375 tall and any length.
  - It tiles seamlessly, and a shorter carrier simply crops the strip.
  - A and B can't alternate inside one Texture: use one Texture per run, A on some runs and B on others.
- **Or: plain Decals.** 24-wide carriers that abut exactly at multiples of 24.000. Every pairing (A|A, A|B, B|A, B|B)
  is seamless.
- **Run ends:**
  - A run must end **exactly on a seam**: a multiple of 24 from where the tiles start, with `OffsetStudsU = 0`.
  - Cap each free end with EndL / EndR.
  - No cap is needed where the end sits against a pillar, corner or prop.
  - In a back-wall bay, the simplest option is one Texture carrier from pillar face to pillar face: no caps, no cut.
- **Low-moss slots for W_Crack_C:** the stretches where the moss stays ≤ about 1.1 stud tall, measured from where the
  tile starts (u = 0 = the left end as seen from the hub):
  - A: 6.7-10.3 studs;
  - B: 12.2-15.8 studs.
  - Centre W_Crack_C on a slot. Its own moss foot then covers the strip there, whichever draws on top.

### No floating moss on walls
- Every moss blob in the wall textures is part of the base mass, within 0.5 stud of it, or sits on a crack ledge or in
  the W_Crack_C notch (`checks.json` -> `floating_moss`: 0 floating blobs in all 9 wall textures).
- Keep it that way in Studio: never put a separate floor-moss decal (G_Moss_A/B) on a wall, and never stack a second
  MossBase higher up the wall.

### Overlaps: order-safe only
Roblox sorts transparent parts per part, so the draw order of two overlapping decals can flip with the camera. The
previews show every allowed pair in both orders (`renders\order_*`, `sheets\order_pairs.png`). The rules:
- **Allowed:**
  - a stain (G_Stain_A/B, or the damp in MossBase) UNDER anything else;
  - W_Crack_C on a MossBase low-moss slot.
- **Not allowed:**
  - a crack over moss (anywhere else);
  - anything overlapping slime;
  - two cracks overlapping;
  - two moss decals overlapping.
- `Decal.ZIndex` only orders decals on the same face of the same carrier, so it does not help here.

### Cream paths and the plaza
Cream renders almost white in game, so dark glazes pop about twice as hard there.
- Stains on cream: `Decal.Transparency 0.25-0.35`.
- Cracks on cream: `Decal.Transparency 0.10-0.15`.
- At most 1 decal per about 30 studs of path, at the path edge (straddling the brown edge) rather than centred.

## 3. Where in the hub (density, exclusions)

Hub reference points:
- plaza centre (0, −33), r about 25;
- spawn (0, −22);
- back-wall pillars at x = ±13.3, 39.8, 66.4, 93, 119.5 (2.5 wide, 1.6 deep, centres z 103.1); inner face at
  z = 104.00; trim bottom y 22.9;
- base slots: Base1 x −140..−76 z 4..84, Base2 x −38..26 z 16..96, Base3 x 76..140;
- 12 pumpkin-egg clusters;
- garden props on the floor.

### How to place it
- **Clusters, not a sprinkle.** Use 12-16 floor grime clusters of 2-4 decals each: a crack plus moss plus a stain, or
  a stain plus slime (not touching). Put them where grime would collect: wall feet, under trees, beside graves, path
  edges, around the pumpkin clusters.
- **Keep it clean in between.** At least 60 % of any 40 x 40 area stays clean; decal coverage in an area stays under
  about 25-30 %.

### Exclusions
- Nothing within **8 studs of spawn** (0, −22).
- Keep the plaza centre clean (r ≤ 12 around (0, −33), the statue plinth). Put 2-3 cracks and 1 stain on the plaza rim
  (r 18-25), so the spawn view gets some grime.
- Nothing inside the base slots (+4 margin), on treadmill pads, on stall plinths, on VIP doors, on the tutorial arrow
  route or on leaderboards.
- **Never on the runway** (Map.Hub runway areas are out of scope).

### Walls
- **MossBase:** along every wall bottom, with gaps. On the back wall, one Texture carrier per bay, pillar face to
  pillar face, alternating A and B bays. Leave 2-3 bays bare along the hub so it doesn't look stamped.
- **Wall cracks:** about 1 per 1-2 bays, in the lower half, below the garland swag. Never behind a vine or a web.
- **Drips:** mostly on wall stretches without garlands (side walls, front diagonals, corners). On the back wall, at
  most **1 per 3 bays**, off-centre near a pillar where the rope is highest; slide it if a pennant covers it.
- **Wall-foot pairing:** floor moss (G_Moss_A/B) and stains at the wall foot, in front of MossBase runs, tie the wall
  and the floor together.

### Orange walls
Orange walls are the runway walls, out of scope. The set was still checked on orange (`sheets\overview_*.png`, bottom
row).

## 4. TEST PATCH for the owner (one back-wall bay + the floor in front of it)

The exact parts (size, CFrame, properties, plus a Luau snippet that builds them) are in **`test_patch.json`**, made by
`python gen\make_test_patch.py`. The script places every part from the PNGs' real content extents and refuses to
write the JSON if a rule below is broken. "Left" and "right" mean as seen **from the hub** looking +Z, where +X is on
the viewer's LEFT.

**Where:** the back-wall bay between the pillars at **x 39.8 and 66.4** (pillar faces x 41.05 and 65.15, clear width
24.1, centre **x 53.1**). The whole patch spans x 41.05-65.15, clear of Base2 (x -38..26) and Base3 (x 76..140) with
their +4 margins. (Round 1 sat on Base2: fixed.)

**Verify in Studio first** (also listed in the JSON's `verify`):
- floor top **y = 0**;
- back wall inner face **z = 104.00** (BackWall centre z 107, 6 thick);
- top trim bottom **y = 22.9**;
- pillar depth: centres **z 103.1**, 1.6 deep, so they stand proud of the wall from z 104 to 102.3 (2.5 wide);
- pillar faces **x 41.05 / 65.15**.

If the wall face or a pillar face is off, shift every wall part (and the wall-foot floor parts) by the same delta.

**Wall:**
1. `MossBase_Bay`: `W_MossBase_A` as a **Texture** (`StudsPerTileU 24`, `StudsPerTileV 6.375`) on ONE carrier from
   pillar face to pillar face, 24.1 x 6.375, centre x 53.1, bottom at y -0.375. No end caps (both ends meet pillars).
2. `Crack_FloorUp`: `W_Crack_C` at **x 56.65** = left face 65.15 - 8.5, on MossBase_A's low-moss slot, bottom at
   y -0.375.
3. `Crack_Diag`: `W_Crack_B` at **x 47.05** = right face 41.05 + 6, **y 5.25-15.25** (lifted from y 4-14 just
   enough to stay 2 studs clear of the moss; round 4 had 5.75), below the garland swag.
4. `Drip_Damp`: `W_Drip_A` by the **left** pillar at **x 61.04**: its visible content starts 2 studs from the pillar
   face; top at y 23.25, behind the trim.

Measured clearances between the visible content of the wall decals (all >= 2 studs, round 5): MossBase_Bay to Crack_Diag 2.11, MossBase_Bay to Drip_Damp 9.26, Crack_FloorUp to Crack_Diag 6.15, Crack_FloorUp to Drip_Damp 5.05, Crack_Diag to Drip_Damp 12.72. (W_Crack_C sits in the moss on purpose.) The drip does not run into a crack.

**Floor in front of the bay** (all rotation 0 at the wall foot):
- `Moss_UnderCrack`: `G_Moss_A` under the crack (x 56.65, z 101.42, height 0.05).
- `Moss_WallFoot`: `G_Moss_B` along the wall foot near the right pillar (x 46.65, z 101.85, height 0.05).
- Both reach the wall foot: their moss ends 0.4 stud short of the wall at most. Whether a Top-face decal's image top
  points at +Z or -Z is not verified, so they are placed to reach the foot in either orientation; the extra length
  slides under the wall, where the wall hides it.
- `Stain_WallFoot`: `G_Stain_A` (x 53.5, z 97.6, yaw 20, height 0.03); its back edge runs under the moss.
- `Crack_Long`: `G_Crack_A` (x 52.1, z 89.5, yaw -25), away from the wall foot.

**Optional plaza-rim spot:** `G_Crack_B` (Transparency 0.12, on cream) and `G_Slime_A`, not touching.

**After building:** **delete the `GrimeTestPatch` ModuleScript** (it only carries the JSON; the snippet's last line
does it).

**What to show the owner:**
- the **default third-person view** (character about 12 studs from the wall). From eye height the floor grime is very
  faint and the stains vanish beyond about 25 studs, so the third-person view is how players will actually see it
  (`renders\wall_tp_day.png` / `wall_tp_night.png`);
- the eye-height view from about 25 studs (`renders\wall_eye25_day.png`);
- day and night (DayNightClient);
- next to it, the same bay without decals (`renders\*_before.png`).

The wall mock in `renders\` is built from `test_patch.json` (mock x = -(X - 53.1), mock y = Z - 104), so the wall
previews show this exact layout. The side sections next to the bay are catalog-only.

## 5. Lighting and preview notes
- The decals don't change Lighting.
- **Round 4: the previews are calibrated to the LIVE GAME screenshots of the round-3 test patch** (`ingame_round3\`,
  fitted by `gen\calib_fit.py` into `gen\calib_round4.json`).
  - In the hub the sun stands **behind the back wall**, so the wall face and the floor at its foot only get the
    cyan-blue sky light; the mock now does the same (sun from behind, elevation about 60°, its shadow reaches about
    12 studs onto the floor like in game).
  - Fitted per channel on the shaded wall, the shaded floor at the wall foot, the sunlit floor and the pillar front.
    Render minus game, day: wall [0, 0, 0], shaded floor [0, 0, 0], sunlit floor
    [0, 0, 0], pillar [0, 0, 0] (sRGB levels).
  - Round 5: the Moonlit sky colour is fitted on THREE shaded materials at once (the floor, weighted x2, the wall and
    the round-3 wall moss decal as seen in the owner's night screenshot), because the floor alone let the mock night
    over-saturate green moss. Night render minus game: shaded floor [-5, -8, 20], sunlit floor
    [-2, -5, 14], wall [8, 3, 0], round-3 moss [0, 9, -20] (the mock stays a
    little greener than the game, i.e. conservative for the moss-chroma gate).
  - Mock surface colours from the fit: wall [140, 152, 203], pillar [78, 78, 148],
    floor green [146, 170, 116]; the studs are the game's rounded squares.
  - Check: the round-3 decals rendered in the re-calibrated mock look like the game (`sheets\ingame_vs_mock.png`,
    middle column): MossBase was a thin dark fringe, which is exactly the owner's complaint.
- A light uniform haze veil (6 %) is added in post (it was 14 %; the live game reads more saturated).
- Moss chroma gate (`checks.json` -> `moss_chroma`, wall moss in the live-game framing): median saturation
  0.591 day / 0.718 night (gate 0.68 / 0.75); the slime drip in the same frames is
  0.798 / 0.904, still the most saturated green.
- Read best from the default third-person camera (`renders\game_tp_day.png`, the live-game framing).
- At eye height, floor decals are strongly foreshortened: cracks stay readable; the stains are now dark, wet and glossy,
  but they are still the quieter layer.
