# Halloween STREET LAMP ("Pumpkin lantern post") - build PLAN (2026-10-13)

Builder plan for the plan reviewer. Binding brief: `StreetLamps\BRIEF.md` + `Halloween\AGENT_BRIEF.md`.
Nothing is built yet. After approval I build exactly this, unless the review changes it.

## 0. Ground rules I follow
- Headless Blender 5.2 only:
  `"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python lamp.py -- <step>`
  - Every run has a timeout and writes its log to `StreetLamps\log_<step>.txt`.
  - No Studio, no GUI Blender MCP, no downloads, no git.
- No Neon or emissive in any exported mesh or map.
  - The night render uses a review-only flame stand-in (emission), as the eggs did. It is never exported.
- `hkit.py` and `pumpkin.py` are imported read-only (`SKIN`, `grin`).
- Helpers from `PumpkinEggs\eggs.py`, `WebsSpiders\webs_spiders.py` and `DeadTrees\treekit.py` are copied into my own `StreetLamps\lampkit.py`, with their output paths pointed at my folder.
- Everything lives in `StreetLamps\`:
  - scripts: `lamp.py`, `lampkit.py`;
  - `.blend` files, `maps\`, `wip\`, logs, JSON reports, review PNGs, `NOTES.md`.
- The one FBX goes to `C:\cdimp\Halloween_StreetLamp.fbx`.
- 1 Blender m = 1 stud. +Z is up.
- **FBX origin = the ground contact point at the base centre (Z = 0).** All five objects keep this origin.
- **The arm, hook, lamp and pumpkin face all point to Blender -Y.**

## 1. The design in numbers

### Side elevation (Y-Z plane, X = 0; the arm reaches toward -Y)
```
 z
18.3            ,/\_bat_/\,             (wings spread in X-Z, looking -Y)
17.7        .---'==========-------._
16.7       /  @ volute       arm     \_C-hook   <- chain top on the hook cradle (y -3.55)
15.4     [##] collar 3   (web in      o  ring + 3 oval links
           |   the crook, Y-Z plane)  ^  spear-eye "spike" finial
14.8       |                        /^^^\  witch-hat cap, top ring
13.3       |                       |(o o)|  carved pumpkin inside 4 flat straps
12.5       |                        \_w_/  saucer, bottom collar
12.0       |                          v    drop finial = lowest point of the head
 8.0     [##] collar 2
           |  twisted section (4-lobe barley twist)
 6.3     [##] collar 1
           |  fluted pole (12 flutes)
 2.6     [==] base top collar
          / \  cast bell base, 4 gothic panels with web relief
 0.2    [_____] 3-step round plinth
 0.0    ^     ^ 4 claw feet on the diagonals
        y = 0 (pole axis) -----------------> -Y (arm, face)
```

### Height stack (targets, +/- 0.1)
| Element | Z (studs) | Size / notes |
|---|---|---|
| Claw feet (4, on the 45 deg diagonals) | 0 to 0.30 | Talon tips sunk at most 0.02 below Z = 0 |
| Plinth step 1 | 0.18 to 0.42 | r 0.95, round-over edges. It sits on the feet, so there is a small shadow gap under it. Underside closed. |
| Plinth step 2 | 0.42 to 0.62 | r 0.80, cove + bead |
| Plinth step 3 | 0.62 to 0.80 | r 0.68, torus bead |
| Bell base | 0.80 to 2.30 | Ogee profile, r 0.64 to 0.34. 4 recessed gothic-arch panels (front panel faces -Y), each with a raised cast spider-web relief. Bead borders. |
| Base top collar | 2.30 to 2.60 | r 0.38, 8 rivets |
| Lower fluted pole | 2.60 to 6.10 | r 0.25 to 0.24, 12 concave flutes |
| Collar 1 (knuckle) | 6.10 to 6.35 | r 0.32, bead rings, 8 rivets |
| Twisted section | 6.35 to 7.95 | 4-lobe twisted square bar, lobe r 0.27, pitch 1.0 stud per turn |
| Collar 2 | 7.95 to 8.20 | Same as collar 1 |
| Upper fluted pole | 8.20 to 15.10 | r 0.24 to 0.20 |
| Collar 3 (top) | 15.10 to 15.40 | The crook springs out of it, which hides the 24-to-12-side change. |
| Crook bend | 15.25 to 17.72 | Bar r 0.19 to 0.17. Vertical lead-in to z 16.5, then a quarter bend of radius 1.05. **Apex bar centre at (y -1.05, z 17.55).** |
| Arm | 17.55 to 17.08 | Bar r 0.16 to 0.11. Runs from y -1.05 to y -3.35, drooping gently. |
| C-hook (the crook's hook) | about 16.4 to 17.1 | Bar r 0.10 to 0.085. Curls down and back toward the pole and ends in a ball knob (r 0.075). Cradle bottom (bar centre) at **(y -3.55, z 16.62)**. Outermost point y -3.89. |
| Volute scroll in the bend | about 15.7 to 16.9 | Open C-scroll of flat bar, about 0.75 across, nested in the bend. Its coils touch the pole and the arm underside (forge-weld bands). |
| Bat ornament | 17.70 to 18.32 | On the crook apex, feet clasping the bar. Wingspan 1.70. |
| Chain | 16.70 to about 15.60 | 1 round ring hung over the hook cradle + 3 oval links (outer 0.36 x 0.24, wire r 0.045). Planes alternate. |
| Spear-eye finial + ball knob | 15.65 to 15.18 | A pointed-arch loop (reads as a spike). The bottom link threads through it. |
| Witch-hat cap | 14.80 to 15.18 | Concave flared cone, rim r 0.62 with a rolled bead and 4 rivets |
| Top ring | 14.80 | r 0.42. The 4 straps end here. |
| Pumpkin | 12.62 to about 14.15 (stem tip <= 14.48) | R 1.12, Rz 0.80, 8 ribs, flat bottom, centre z 13.34. **Width 2.24.** |
| Saucer (pumpkin seat) | 12.48 to 12.62 | r 0.45, rolled rim. This is the only contact with the pumpkin. |
| Bottom collar | 12.32 to 12.48 | r 0.22. The straps converge here. |
| Drop finial tip | **12.02** | Lowest point of the lamp head |

### Headline checks
- **Total height ≈ 18.3** (bat ears and wing tips). The iron alone reaches 17.72.
- **Arm reach:**
  - hanging axis at **y -3.55**;
  - outermost iron at y -3.89;
  - cage front at y about -5.05.
- **Lamp head bottom: 12.02** (drop finial tip). The cage collar is at 12.32 and the pumpkin bottom at 12.62.
- **Base footprint ≤ 2.55 x 2.55.**
  - The plinth is 1.90 across.
  - The toes fan ±18 deg from the diagonals, with tips at radius ≤ 1.38. That puts the largest X/Y coordinate at ≤ 1.26.
- **Lamp head:** the cage is 3.0 wide and about 3.6 tall with the finials. That is about 1/6 of the post height: classic crook-lamp proportions, with the pumpkin as the hero.
- **Strap layout:** 4 straps at 45 / 135 / 225 / 315 deg around the hanging axis.
  - The two front straps sit **±45 deg off the face**, so seen from the front the face shows between them at x = ±1.06.
  - The mouth half-width is 0.76.
- **Clearances:**
  - pumpkin skin to straps/rings ≥ 0.30 (straps 0.32-0.34 off the rib crests);
  - stem to cap ≥ 0.30;
  - cage to Post ≥ 0.40, apart from the ring sitting in the hook cradle (contact by design);
  - web to cage ≥ 0.30.
  - All are measured with BVH in the build step. Any violation stops the build.

## 2. Parts, triangle budgets, textures

| Object (MeshPart) | Contents | Target tris | Cap | Textures |
|---|---|---|---|---|
| `Post` | plinth, claw feet, bell base, fluted / twisted pole, collars, crook, arm, C-hook + knob, bend volute, bat | 6,220 | 6,500 | 1024: colour x AO, tangent normal, roughness |
| `Cage` | 4 straps, top ring, bottom collar, saucer, witch-hat cap, ball knob, spear-eye finial, drop finial, ring + 3 links | 2,880 | 3,000 | 512, same three maps |
| `Pumpkin` | carved shell (skin, knife walls, inner wall), stem, candle stub + wax puddle, wick | 3,000 | 3,300 | 1024, same three maps |
| `Web` | orb web strands in the crook (tube strands) | 1,060 | 1,150 | 512 colour + 512 roughness (procedural, planar) |
| `WebSilk` | 3 two-sided silk pieces | 280 | 300 | 512 RGBA colour (alpha = silk) |
| **Total** | | **13,440** | **14,000 (hard)** | |

- `lamp.py` raises an error if any part is over its cap, or the total is over 14,000.
- Each part is far below the 8,000 limit.

**Post breakdown**
- Column lathe: 24 sides x 59 rings + bottom fan = about 2,830.
- Crook + arm + hook + knob: 12 sides x about 55 adaptive rings = about 1,330.
- Bend volute: flat bar, 6-vertex section x 36 rings = about 430.
- 4 claw feet: leg 10 sides x 8 rings + 3 toes at about 36 each = about 1,070.
- Bat: about 560.

**Cage breakdown**
- Straps: 8-vertex rounded-rect section x 18 rings, 4 of them = 1,090.
- Rings and collar: 430.
- Cap: 260.
- Saucer: 110.
- Finials: 430.
- Chain: 552.

**Pumpkin breakdown**
- Skin: 48 x 18 (6 columns per rib, grooves on vertex columns) = 1,632.
- Inner wall: 20 x 10 = 360.
- Carve overhead: about 450.
- Stem: 180.
- Candle + puddle: 260.
- Wick: 60.

**Smoothness rules (anti low-poly)**
- **Ring spacing is adaptive:** at most 0.003 stud of chord sag, and at most 0.35 stud per segment.
  - On the 1.05-radius bend this works out to ≤ 9 deg per ring.
- **Side counts:**
  - pole and base: 24 sides (max deviation from a circle 0.008 at r 0.95);
  - crook, which is 12+ studs up: 12 sides;
  - feet legs at eye level: 10 sides.
- **Twisted section:** rings every 0.07 with *helical* vertex columns. The lobes follow the columns, so the chord sag stays ≤ 0.007.
- Every lo profile corner is a 2-ring bevel ≥ 0.03, so the lo is smooth-shaded with no hard edges inside a UV island.
- The exceptions are the pumpkin knife walls (flat + sharp, the eggs lesson) and the bat plate rims.
- The build reports the max chord sag and the max adjacent-ring angle per tube.

## 3. Palette (sRGB 0-255 -> linear 0-1 via `hkit.lin`)

### Iron
Painted wrought iron. Metallic 0: Roblox gets no metalness map from the FBX, and painted iron is a dielectric. The metal reads through colour + roughness instead.

| Material zone | sRGB | Linear | Roughness |
|---|---|---|---|
| Iron base, cool near-black (large-scale tonal noise ±10 %) | (40, 43, 50) | (0.021, 0.024, 0.032) | 0.62 ± 0.06 |
| Iron tone high (noise top) | (52, 55, 62) | (0.034, 0.038, 0.048) | 0.60 |
| Iron deep (grooves, flutes, under beads; before AO) | (24, 25, 30) | (0.009, 0.010, 0.013) | 0.72 |
| Edge wear, steel showing on beads / rivet heads / flute fillets / crests (≤ 60 % at the sharpest edges, broken by noise) | (96, 101, 112) | (0.117, 0.130, 0.162) | 0.38 |
| Rust dark (crevices only: plinth steps, collar coves, feet roots, rivet rings, hook cradle, bat joints) | (92, 50, 30) | (0.107, 0.032, 0.013) | 0.88 |
| Rust bright, sparse blooms inside the rust mask (≤ 15 % of it) + short run-down streaks under rivets | (150, 80, 40) | (0.305, 0.080, 0.021) | 0.90 |

- Rust stays a *hint*: at most about 8 % of the iron area.
- **Target albedo mean ≈ sRGB (44-52, 46-55, 52-62)**, cool, not pure black. The build reports a histogram and fails if the mean is < 36.

### Pumpkin
`pumpkin.SKIN`, the same as the giant head and egg A, so the set matches.

| Zone | sRGB | Linear |
|---|---|---|
| Skin crest | (246, 130, 20) | (0.922, 0.223, 0.007) |
| Skin light streak | (255, 178, 60) | (1.000, 0.445, 0.045) |
| Skin groove | (170, 58, 10) | (0.402, 0.042, 0.003) |
| Red tone / gold tone | (224, 92, 14) / (252, 158, 36) | (0.745, 0.107, 0.004) / (0.973, 0.342, 0.018) |
| Bottom / top (stem well) | (242, 162, 56) / (112, 98, 36) | (0.888, 0.361, 0.040) / (0.162, 0.122, 0.018) |
| Blemish | (176, 124, 62) | (0.434, 0.202, 0.048) |

- Skin roughness: 0.38 on crests, 0.60 in grooves, up to 0.90 on blemishes.

### Pumpkin interior, stem, candle, wick, web

| Zone | sRGB | Linear | Roughness |
|---|---|---|---|
| Flesh / cut walls A / B (fibrous noise) | (252, 218, 132) / (242, 176, 82) | (0.973, 0.701, 0.231) / (0.888, 0.434, 0.084) | 0.55 |
| Flesh pulp side / rind line at the outer knife edge (from "Depth") | (244, 156, 56) / (214, 104, 22) | (0.905, 0.333, 0.040) / (0.672, 0.138, 0.008) | 0.55 |
| Inner wall, scraped (A / B noise, spoon scrapes) | (252, 200, 112) / (228, 140, 48) | (0.973, 0.578, 0.162) / (0.776, 0.262, 0.030) | 0.72 |
| Stem base / mid / top (eggs "green") | (66, 86, 34) / (108, 100, 52) / (148, 126, 80) | (0.055, 0.093, 0.016) / (0.150, 0.127, 0.034) / (0.296, 0.209, 0.080) | 0.80 |
| Stem ridge high / low / dry cap | (196, 180, 124) / (48, 44, 22) / (206, 184, 130) | (0.552, 0.456, 0.202) / (0.030, 0.025, 0.008) / (0.617, 0.479, 0.223) | 0.80-0.85 |
| Candle wax (ivory) / drips | (236, 212, 162) / (240, 212, 146) | (0.839, 0.658, 0.361) / (0.871, 0.658, 0.287) | 0.46 / 0.30 |
| Wax pool (amber, glossy) / dust at the foot | (222, 180, 104) / (160, 144, 118) | (0.731, 0.456, 0.138) / (0.352, 0.279, 0.181) | 0.15 / 0.60 |
| Wick unburnt / charred / ash tip | (214, 204, 182) / (26, 23, 21) / (86, 78, 70) | (0.672, 0.604, 0.468) / (0.010, 0.009, 0.008) / (0.093, 0.076, 0.061) | 0.85 |
| Web strands base / dust (near the iron) / bright fibres | (228, 230, 236) / (184, 178, 168) / (250, 251, 255) | (0.776, 0.791, 0.839) / (0.479, 0.445, 0.392) / (0.956, 0.965, 1.000) | 0.38-0.72 |
| Web silk / silk dust / silk bright (RGBA, alpha = fibre + gauze) | (228, 224, 216) / (150, 138, 120) / (248, 247, 244) | (0.776, 0.745, 0.687) / (0.305, 0.254, 0.188) / (0.939, 0.930, 0.905) | 0.80 |

## 4. How each part is built
Every part has one generator per shape, with a `detail` switch.
- **Hi = the bake source:** dense, with all the micro detail.
- **Lo = the game mesh:** the *same* function at a coarse sampling, with the same seed and no micro detail. Nothing that has holes is decimated (the AGENT_BRIEF lesson).
- Shapes are lathes (profile x angular function), path tubes (parallel-transport frames) or param surfaces. So every lo vertex has an exact (u, v) parameter, which I use for the UVs.

### 4.1 Post
**Column**
- One lathe surface from the plinth underside to collar 3: profile points (z, r) from the height stack.
- The angular function depends on z:
  - **Pole zones: 12 flutes.**
    - Hi: concave flutes 0.018 deep with 0.02 fillets.
    - Lo: groove vertices on even columns, so the silhouette has a real slight scallop.
    - Flutes fade out over 0.08 near the collars.
  - **Twist zone: 4-lobe rounded-square section.** r = r0 (1 + 0.12 cos 4θ'), θ' = θ - 2π (z - 6.35) / 1.0. In the lo the vertex columns rotate with θ'.
  - **Bell base: 4 recessed gothic-arch panels** (hi displacement 0.02 deep, raised 0.012 bead border). Each holds a raised 6-spoke spider-web relief, 0.01 high.
- **Rivets:** hi-only domes (r 0.04) joined into the column's hi group.
  - 8 per collar, 8 on the base top collar, 4 on each plinth step.
- **Hammered forging:** fbm displacement 0.003 at about 25 per stud on every iron hi part.
- **Joint rule (DeadTrees lesson):** every joint is either hidden under a collar, or the joining tube starts ≥ 1.4 x its radius inside its parent. No tube end is exposed.

**Claw feet (4, on the 45 deg diagonals)**
- A cabriole leg comes out from under the bottom plinth's round-over (start buried 0.15 inside), swells into a knee (r 0.12) and runs to the ankle (r 0.075).
- The paw has 3 toes fanned ±18 deg. Each toe is a tapered tube (r 0.045 to 0.02) ending in a hooked talon that bites the ground.
- Hi: knuckle rings, a small leaf scroll relief on the knee top (a "scroll end"), talon ridges.

**Crook + arm + C-hook**
- One tube along a C2 spline:
  1. Collar 3 up to the bend.
  2. The quarter bend (radius 1.05), apex at (y -1.05, z 17.55).
  3. The drooping arm to y -3.35.
  4. The C-hook: out to y -3.89, down to the cradle at (-3.55, 16.62), and back up toward the pole.
  5. A ball knob at (-3.28, 16.78).
- The radius tapers 0.19 to 0.085. A small forged bead swell sits where the arm becomes the hook.
- UV seam along the outer (top/back) side of the curve, hidden from the front and from below.

**Bend volute**
- An open C-scroll of flat bar (0.10 x 0.045, 6-vertex rounded section) nested in the inside of the bend.
- Both ends curl into ~0.9-turn volutes. The outer coil touches the pole's -Y face and the arm underside.
- Hi: forge-weld bands (small wrapped collars) at the two contacts.
- This is the "scroll ends" ornament, and it is the web's upper-left anchor.

**Bat ornament** (fierce, never cute)
- **Body:** an ellipsoid (0.13 x 0.09 x 0.22) leaning forward.
- **Head:** looks down toward -Y, at the players. Tall pointed ears, a brow ridge, a snarl with 2 small fangs.
- **Feet:** two hooked feet clasp the crook bar.
- **Wings:** mantled, spread in the X-Z plane with a 20 deg dihedral up and a 15 deg forward sweep toward -Y, so 3/4 views see depth.
- **Each wing:**
  - a 0.045-thick plate with a rounded rim;
  - the leading edge is a thicker arm bone ending in a hooked thumb claw;
  - 3 finger ridges run to sharp tips with concave scallops between them;
  - the hi adds finger ridges and membrane wrinkles.
- **UVs:** planar projection for the front/back plate faces, a strip for the rim, param UVs for the body.
- **Style:** a jagged, sharp silhouette, so it reads as a heraldic vampire bat from 40 studs, matching the hub's fierce flock.

### 4.2 Cage
**Straps**
- 4 flat straps (0.14 x 0.055, rounded edges) run from the bottom collar out round the pumpkin and in to the top ring.
- Each strap's path in the r-z plane is the **offset of the pumpkin's outer profile** at that azimuth (rib crests included) by 0.33, blended into the collar and ring ends.
- Hi: a raised centre bead line, 2 rivets at each end, hammer texture.

**Other parts**
- Top ring and bottom collar: tori with bead detail.
- Saucer: a shallow dish with a rolled rim. The pumpkin's flat bottom rests on it.
- Witch-hat cap: a concave cone. Rim r 0.62 with a rolled bead and 4 rivets; tip into the ball knob.
- **Spear-eye "spike" finial:** a forged teardrop loop, a pointed arch 0.38 tall, wire r 0.035.
  - Its plane is X-Z, so the spike outline faces the front.
  - The bottom chain link threads through it. This is the physically sensible way to hang a cage from a spike finial.
- Drop finial: a lathe (ball + spike) under the bottom collar, tip at z 12.02.

**Chain** (each element interlocks with no intersection; checked)
- A round ring (centreline r 0.145, wire r 0.04, plane X-Z) hangs over the hook cradle, whose bar runs along Y there.
- Below it come 3 oval links in alternating planes: Y-Z, X-Z, Y-Z.
- Each link is a stadium path, 12 segments x 6 sides. The hi has true round wire + forge scale.

### 4.3 Pumpkin (eggs pipeline, copied)
**Field**
- `egg_field` with `P = dict(N=8, R=1.12, Rz=0.80, egg=0.0, depth=0.10, crest=0.45, lumps=0.025, micro=0.003, dtop=0.14, dtop_w=0.38, dbot=0.04, flat=0.9, flat_k=0.18, seed=505, phase=0.0)`.
- These are the giant head's proportions (Rz/R ≈ 0.71) and egg A's palette.
- Shell 0.15, `inner_params`, inner scrape 0.006.

**Sampling and stem**
- Hi: 256 x 192 skin, 160 x 112 inner.
- Lo: 48 x 18 skin (grooves on vertex columns), 20 x 10 inner.
- Stem: `gnarly_stem(L=0.34, r0=0.085, seed=17, "green")`, leaning slightly back (+Y), tip ≤ 14.48.

**Face** (designed in viewer coordinates, studs, relative to the pumpkin centre; set *below* the equator because players look up at it from 12-15 studs below)
- **Triangle eyes, slanted:**
  - the long top edge rises from the nose side to the outer corner (a scowl), with a sharp point at the bottom;
  - each about 0.52 wide x 0.38 tall, spanning x 0.12 to 0.64 (mirrored) and z -0.02 to 0.36;
  - the edges are slightly curved knife cuts (`quad_bezier` with a small bulge) so they look hand-cut.
- **Triangle nose:** apex up, about 0.22 wide, z -0.22 to -0.04.
- **Toothy grin:** `pumpkin.grin(W=0.76, top=(-0.30, 0.14), bot=(-0.56, 0.26), ...)`.
  - 2 square top teeth hang down, at x ±0.28 (w 0.17, tip 0.11, L 0.14).
  - 3 bottom teeth point up, at x -0.48 / 0 / 0.48 (w 0.15, tip 0.08, L 0.12).
  - Corners curl up 0.10; step 0.03, jitter 0.006.
- It reads as classic spooky-fun with attitude, like the head and the eggs, not cute.
- All values are first guesses. I tune them on fast previews (front at 25 studs, from below at 15 studs, 3/4) before the full bake.

**Carving** (the eggs lessons, applied as-is)
1. **`cutter_planar(outlines, R=1.12, Rz=0.80, egg=0)`:** radial knife walls (square to the skin) with *planar* caps, so the ear-clipped caps can't cut the island's own walls.
2. **The same cutter carves both the hi and the lo** (`carve2`, EXACT boolean, material TRANSFER). The lo is never a decimated carve, so the hole edges match the bake source.
3. **Solidify is not used.** Shell and cavity are two closed sampled surfaces, so the even-offset fold problem cannot happen.
4. **`repair_attrs()` on the hi after the boolean:** refills the Col / Rough / Depth values the EXACT boolean leaves at 0 on every new cut vertex. That black band was the eggs' dark serrated rim. The build logs fixed/left counts and fails if any are left.
5. **`knife()`:** cut walls flat-shaded, sharp edges between materials.
6. **Hole check:** `euler_holes` must equal 4 (2 eyes, nose, mouth) on both the hi and the lo, or the build stops.
7. The pumpkin is built facing +Y (the eggs' convention) and then **rotated 180 deg about Z** (a proper rotation, no mirroring) to face -Y. It is translated to (0, -3.55, 13.34). Hi, lo, cutter, stem and candle all get the same matrix before baking.

**Candle stub + wick**
- One melted church-candle stub from the eggs' `candle_field`. It is generated at egg-candle scale (R 0.44, H 1.05, 1 overflow notch, 4 drips) and scaled x0.34, so it ends up **r 0.15, h 0.36** with the drip proportions kept.
- It stands on the flat inner floor at the cavity centre (floor z ≈ 12.77), with a small wax puddle (r 0.24) round its foot.
- **Wick:** the eggs' curled `wick_pts` / `wick_mesh`, scaled x0.34 with the radius x1.5 (about 0.02), so it survives the bake.
  - Colours: unburnt at the base, charred, ash tip.
  - Wick tip ≈ floor + 0.41.

### 4.4 Web + WebSilk (in the crook)
**Web frame**
- Orb web in the **Y-Z plane at x ≈ 0**, bowing 0.12 toward +X. It faces ±X, so people walking along the path see it face-on and in profile with the crook. From the front it is edge-on, and the face and bat carry that view.
- Frame anchors, approximate (the build snaps them to the real iron surfaces):
  - pole -Y face (-0.22, 14.15) and (-0.21, 14.95);
  - bend volute outer coil (-0.6, 16.2);
  - arm underside (-1.15, 17.36), (-2.2, 17.15) and (-3.05, 16.95), the last one before the hook.
- **The lower edge is a free catenary frame thread** from (-3.05, 16.95) back to (-0.22, 14.15), sagging 0.3. It never touches the chain or cage, so a lamp-head sway (if the lead ever adds one) can't break the web.
- **Span ≈ 2.9 (Y) x 3.2 (Z).** This is a wide corner-quadrant web, not the narrow funnel the DeadTrees reviewer called a "ladder".

**Web build**
- `treekit.build_web` logic (copied): hub at about (-1.0, 16.25), **9 spokes** (r 0.045, 3-sided), **5 catch rings** (r 0.038, 3-sided, 2-segment catenaries sagging toward the hub).
- Frame r 0.055 (4-sided), plus short anchor ties to the iron.
- 2 broken spans with curled loose ends, and 2 loose threads hanging 0.5-0.9 from the lower frame. They stay at y ≥ -1.9 to keep clear of the cage.
- Strand thickness 0.076-0.11, within the AGENT_BRIEF read rule.
- **Colour:** a planar Y-Z projection onto a 512 map (`strand_maps` approach): silver-white, dusty toward the iron anchors. Plus a 512 roughness map linked straight to Roughness, so it embeds.

**WebSilk** (separate part, two-sided front + back faces, no DoubleSided needed)
1. A dense gauze mat around the volute / pole corner.
2. A hub patch, r 0.3.
3. A small tattered drape (about 0.8 x 0.6) hanging from the lower frame near the pole.
- **Texture:** a 512 RGBA atlas built like `silk_map` / `silk_texture`: fibre tangle + gauze film with torn holes + dust, frayed free edges.
- The silk gives the web a pale mass that survives at 40 studs against the sky.

## 5. UVs and bakes
**UVs**
- Explicit parameter UVs from the generators (u = around, v = arc length) for every lathe and tube.
- **Seams on hidden sides:**
  - column: back side (+Y);
  - crook: the outer/top side;
  - straps: the inner face;
  - feet: the underside.
- **Islands split at collars,** where the seam rings are hidden.
- **Texel priority:**
  - Post: base, feet and lower pole x1.25; bat x1.3; upper pole x1.0; crook / arm / volute x0.9.
  - Cage: chain and saucer x0.8.
  - Pumpkin: inner wall x0.55; candle x0.6 (eggs values).
- Packed with `pack_islands(shape_method="CONVEX", rotate=True, margin 0.006)`, so no island nests inside another island's holes (eggs lesson 4).
- **Expected density:** Post about 128 px/stud, Cage about 120, Pumpkin about 200.
- The pumpkin skin and inner wall use the eggs' `uv_layout`: ANGLE_BASED lunes cut along 3 rib grooves.

**Bakes**
- **`bake_groups` (copied from the eggs):** Cycles CPU, tangent normal, AO, diffuse colour, roughness. The coverage and hit masks, the fill of misses from the group's own hits, and the final margin dilation all come with it.
- **Every lo part only ray-matches its own hi part.**
  - Post groups: column, feet, crook+hook, volute, bat.
  - Cage groups: straps, rings + saucer + cap + finials, even links, odd links + ring.
  - Pumpkin groups: skin + stem, knife walls, inner wall, candle + puddle, wick.
  - This stops cross-talk where parts touch: feet / plinth, volute / pole, bat / bar, ring / hook, saucer / pumpkin.
- **AO sees every hi part in the scene** (all three parts are built in the same source file), so contact shadows are real. The lo copies are invisible to shadow and diffuse rays.
- **Cage extrusion / max ray** are small for the thin parts: chain 0.015 / 0.04, straps 0.02 / 0.06, Post 0.03-0.05 / 0.08-0.12, pumpkin as the eggs scaled x0.45. The hi and lo come from the same functions, so they lie within about 0.01 of each other.
- **AO is multiplied into the colour:**
  - Post: strength 0.55, distance 0.35;
  - Cage: 0.5 / 0.2;
  - Pumpkin: 0.5 / 0.22.
- **Iron colour + roughness on the hi.** Per-vertex `Col` / `Rough` come from analytic masks the generators already know:
  - flute grooves, profile coves, inside of bends → deep / rust;
  - beads, fillets, rivet heads, crests → wear;
  - plus fbm breakup.
  - On top, a Cycles **AO shader node** (bake-time) adds rust tint in true contact crevices, and Pointiness / AO-inside adds a little extra edge wear.
  - Fallback if the AO node makes the bake speckly: analytic masks only.
- **Anti-aliasing option:** if the 1024 Post maps alias (thin flutes and web relief), bake at 2048 and box-filter down to 1024, as the bat did.
- **PBR material:** `hkit.pbr_material`. The roughness map is linked straight in, so the FBX embeds it.
- **Opaque albedo alpha = 1.0** (safe in Roblox Overlay mode). Only `WebSilk` has real alpha.

## 6. Steps (`lamp.py`)
`fast` halves the hi density, uses 256 maps and 8 samples, and writes to `wip\`.

1. **`preview` (fast, before any bake):** geometry with flat palette colours.
   - Renders: front, side and 3/4 at 25 studs (eye height 5, vFOV 70), the head close-up, the head from below at 15 studs, and an ortho view next to a 2 x 1 x 5 player block.
   - What I check: proportions, silhouette, the face read and placement, strap vs face, web shape.
   - I iterate here first.
2. **`build`:** all hi and lo parts in `lamp_src.blend`.
   - Carve the pumpkin hi and lo + `repair_attrs` + hole check.
   - BVH clearance checks, triangle caps, chord-sag report, UVs.
   - Writes `build.json`.
3. **`bake post` / `bake cage` / `bake pumpkin`:** `bake_groups` per part, maps to `StreetLamps\maps\<Part>_albedo|normal|rough|ao.png`, then `pbr_material`.
   - Writes `bake_<part>.json` (miss fractions, texels).
4. **`web`:** strand colour + roughness maps and the silk RGBA atlas (procedural, no bake), with their materials.
5. **`export`:**
   - collect `Post`, `Cage`, `Pumpkin`, `Web`, `WebSilk` (origin = ground point, transforms applied);
   - assert min z ≥ -0.05, footprint ≤ 2.6, height and reach;
   - `hkit.export_fbx` to **`C:\cdimp\Halloween_StreetLamp.fbx`** (one FBX, 5 objects, textures embedded);
   - save `lamp.blend`; write `export.json` (per-object size, tris, texture, bbox centre, attachment points).
6. **`verify`:** re-import the FBX in a fresh scene.
   - Check: object names, tris, packed images with sizes, albedo alpha, the silk alpha range, scale 0.01, min z, the 4 holes, no stray loose parts.
   - Writes `verify.json`.
7. **`review`:** renders from the *re-imported FBX* (see section 8).
8. **Self-review** against the reviewer's checklist (section 9), fix, re-run. Then write `NOTES.md`.

Expected run times: build a few minutes; each 1024 bake about 5-15 minutes on CPU; review a few minutes. Long steps run in the background with logs and a timeout.

## 7. Attachment points (reported in NOTES, Blender object space = FBX origin, plus Roblox axes)
Each point is given two ways:
- Roblox via hkit axes: (X, Y, Z) = (Bx, Bz, -By).
- The importer-turned variant the lead has seen: (-Bx, Bz, By).

| Point | Approximate value (Blender x, y, z) | Use |
|---|---|---|
| Candle wick tip (end of the curl) + wick top (highest point) | about (0, -3.55, 13.18) | Flame flipbook (`vfx\CandleFlame_8x8.png`) centred at wick top + 0.05. Suggested flame size about 0.12 x 0.25. |
| Pumpkin cavity centre | about (0, -3.55, 13.40) | Glow particles |
| Cavity floor (inside, centre) | about (0, -3.55, 12.77) | Reference |
| **Suggested PointLight: LOW inside** | about (0, -3.55, 13.23), roughly floor + 0.45, just above the wick and below the eye line | Same reasoning as the eggs: a low light catches the upper walls of the holes that players below see. |
| **Chain top**: the ring's contact on the hook cradle | about (0, -3.55, 16.70) | The natural pivot if the lead ever sways the lamp head (Cage + Pumpkin) |
| Chain bottom: the finial eye | about (0, -3.55, 15.65) | Reference |
| Hanging axis | x 0, y -3.55 | Reference |
| Web hub + plane normal | hub about (0, -1.0, 16.25), normal ≈ ±X | For a spider |

- Exact values come from the build (JSON) and go into NOTES.
- **Suggested PointLight in Studio:** warm (255, 150, 60), Brightness about 2-3, Range 12-16, **Shadows = true**, so the light leaves only through the face (the eggs lesson). Flicker per the lead.

**Studio setup for NOTES**
- **Rendering:**
  - `WebSilk` needs `SurfaceAppearance.AlphaMode = Transparency` (required).
  - RenderFidelity Precise on Web / WebSilk / Cage.
  - CastShadow off on Web / WebSilk.
- **Collision:**
  - `Post` should not use Hull: its convex hull would fill the space under the arm and block players walking under it. Use PreciseConvexDecomposition, or CanCollide off plus a simple invisible cylinder collider.
  - Cage / Pumpkin / Web / WebSilk: CanCollide / CanTouch / CanQuery off.
- **Import:** keep the 5 parts in one Model, pivot = FBX origin ("Set Pivot to Scene Origin").

## 8. Review renders (EEVEE)
**Scene**
- `hkit.review_setup`: sky background, warm sun 4.0, plus a **green ground plane** (lawn (96, 168, 64)) and an orange 2 x 1 x 5 player block for scale.
- **Roblox matching:** backface culling ON, `WebSilk` alpha-blended, Web / WebSilk cast no shadows.
- Everything is rendered from the re-imported FBX.
- Cameras use vertical FOV 70 (copied `shoot_fov`) unless a lens is stated.

| File | Camera |
|---|---|
| `review_day_25.png` | 25 studs, eye height 5, vFOV 70, front 3/4 (from -Y, turned 35 deg toward -X), aimed at z about 9. The whole lamp is in frame. |
| `review_day_25_side.png` | 25 studs, eye 5, vFOV 70, from +X (path walker): crook profile + web face-on |
| `review_day_50.png` | 50 studs, eye 5, vFOV 70, front 3/4 |
| `review_close_head.png` | Lamp head close-up, about 7 studs, 50 mm, from slightly below at 3/4: cage, pumpkin face, chain, hook |
| `review_night_25.png` | **Night.** Dark-blue world (0.02, 0.028, 0.06), cool moon sun 0.35, exposure tuned. The pumpkin is lit from inside by a warm point light (1.0, 0.55, 0.2), about 20-40 W, radius 0.06, shadows on, at the suggested light position, plus a review-only flame stand-in on the wick (not exported). 25 studs, eye 5, front 3/4. |
| `review_night_close.png` | Night, lamp head close-up |

Extra shots in `wip\`:
- back at 25;
- head from below at 12 studs (what a player under it sees);
- base and feet at 5 studs, eye height;
- crook + web + bat at 8 studs;
- 40-stud front and side (the reviewer's Halloween-read distance);
- 3 lamps along an 8-wide path at 16-stud spacing, from 40 studs;
- ortho scale view.

## 9. Risks and how I avoid them
| # | Risk | Avoidance |
|---|---|---|
| 1 | Dark serrated rims around the carved holes | Eggs pipeline: same-cutter carve of a coarse lo (no decimation), planar-cap cutters, `repair_attrs` (fails if anything is left), flat + sharp knife walls, per-surface bake groups, CONVEX packing, 4-hole check on hi and lo. |
| 2 | Bake cross-talk / pale bands where iron parts touch | Per-part bake groups (each lo sees only its own hi). Joints hidden under collars or buried ≥ 1.4 x radius. No exposed tube starts. Close-up checks of every joint from below. |
| 3 | Low-poly look (faceted pole, crook, straps, pumpkin) | Adaptive rings (≤ 0.003 chord sag), 24 / 12 / 10 / 8 sides as listed, helical twist columns, groove-on-column ribs and flutes, smooth shading with bevelled profile corners, sag/angle report. |
| 4 | Iron reads as flat black plastic | Cool tint, tonal noise, edge wear on beads / rivets / fillets, roughness 0.38-0.9, baked forging + flutes + rivets in the normal map, albedo-mean check (fails < 36). |
| 5 | Too much rust turns it grim, not spooky-fun | Rust only in crevices, ≤ about 8 % of the area, warm and dark; checked at 25 studs. |
| 6 | Web reads as a ladder, or vanishes against the sky | Wide 2.9 x 3.2 corner web with the hub in the open area, 9 spokes + 5 rings, strands 0.076-0.11 thick, silk mass at the hub / corner / drape, checked at 25 and 40 studs side-on. |
| 7 | Face hidden by the straps, or unreadable from below / at night | 4 straps ±45 deg off the face; face set below the equator; light low inside; day check from below at 12-15 studs plus the night render. |
| 8 | Cage touches the pumpkin / web touches the cage / chain intersects | Strap paths are offset curves of the real pumpkin profile; BVH clearance checks fail the build; chain is placed analytically with alternating planes. |
| 9 | Bat looks cute or blobby | Sharp jagged wing silhouette, tall ears, fangs, head down toward the players; reviewed at 8, 25 and 40 studs; cute features (big round eyes, round head) avoided. |
| 10 | Budget creep | Per-part caps + hard 14,000 total in code; the breakdown above leaves about 560 of margin. |
| 11 | Pivot / axes / turned import | Origin = ground point for all 5 objects; min z ≥ -0.05 asserted; front = -Y stated; points given in Blender + both Roblox variants. |
| 12 | Textures not embedded / roughness dropped / alpha wrong | `hkit.export_fbx` + roughness linked straight in; `verify` re-imports and checks packed images, sizes, alpha. |
| 13 | Post Hull collision blocks the path under the arm | NOTES recommends PreciseConvexDecomposition or a cylinder collider. |
| 14 | Long or crashing bakes, memory | Hi densities sized per part (≈ 1.5 M tris total); one bake per run with a timeout and log; `fast` mode to iterate. |
| 15 | AO-node speckle in the baked iron colour | Enough bake samples + slight blur of the mask; fallback to analytic masks only. |
| 16 | 1024 aliasing on thin flutes / relief | Bake at 2048 and box-filter to 1024 if needed. |

## 10. Deliverables after approval
- `StreetLamps\lamp.py`, `lampkit.py`, `lamp_src.blend` (hi + lo + bake sources), `lamp.blend` (the 5 game objects).
- `maps\`, logs, `build.json` / `bake_*.json` / `export.json` / `verify.json`.
- `C:\cdimp\Halloween_StreetLamp.fbx`: `Post`, `Cage`, `Pumpkin`, `Web`, `WebSilk`, textures embedded.
- `NOTES.md`: per-object size / tris / texture, axes, attachment points, Studio setup.
- Review PNGs: the 6 listed in section 8, plus extras in `wip\`.

## 11. Open points for the plan reviewer
1. **Saucer contact.** The pumpkin rests on a small saucer (r 0.45) under its flat bottom. Everywhere else the cage keeps ≥ 0.30 off the skin. I read "0.3+ all round" as the straps and rings, since a pumpkin needs a seat. Is that OK?
2. **Bat plane.** The bat's wings are in the X-Z plane, so they are full-on from the face side. The web is in the Y-Z plane, full-on from the path. Each main view gets two Halloween reads. Is that preferred to turning the bat 45 deg?
3. **Height.** The total is about 18.3 including the bat. The iron alone is 17.7. If ≤ 18.0 is strict, I drop the chain to ring + 2 links (-0.27) and lower the crook by the same amount.
