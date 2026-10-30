# Hub makeover: visual review (2026-10-22, read-only reviewer)

## Verdict: FIX THEN SHIP

The makeover is a big step up from `before_*`. The clutter is gone, the hub is enclosed, the placements are square, and the mirror-symmetric "one feature per bay" discipline is right.

From most player views, though, the hub still reads plain. The owner has called that "basic" before. Three things cause it:
- **Toy blue walls.** The pillars render as crushed pure royal blue, (1,48,145) to (18,68,165), with HSL S 0.80 to 0.99.
- **A cream coping that renders cyan-grey,** (205,220,220). The warm cap line is lost against the sky.
- **Dead colour fields.**
  - 20 of the 41 bays carry nothing on the panel.
  - A washed pale-mint slot bed fills every plot's surroundings.

All the fixes below are cheap: recolours, one trim part per edge, small finials, and a nudge. None of them touches Lighting, and none adds trees, bushes or seats.

Measured render colours: each value is a 1×1 LANCZOS average of a crop. The crops are listed under M1.

| Thing | Built colour | Renders as |
|---|---|---|
| Panel | (96,132,170) | (60,137,205) close (R08); (26,101,185) far (R03) |
| Pillar | (58,84,130) | (18,68,165) close; (1,48,145) far |
| Coping / caps | (232,222,196) | (205,220,220): hue 180°, cyan-grey |
| Paving | (172,144,108) | (216,196,162) |
| Lane | (188,162,124) | (218,198,166), the same as the paving |
| SlotBed | (150,172,112) | (201,218,174): pale mint, L 0.77 |
| Plot grass | (80,165,62) | (104,222,97) |

---

## MUST (before the owner looks)

### M1. Retune the wall palette: warm the caps, uncrush the pillars

**Problem:** see `review/R08_garland_close`, `R03_plot2_from_plaza`, `R10_backwall_thirdperson`, `after_10_alley` and `final_night_C10_alley`.
- The wall faces pick up the cyan sky light. So the dark blue renders as crushed toy royal blue: the red channel drops to 1-18.
- The cream coping turns cyan-grey, which leaves the whole perimeter as one cold blue mass against a blue sky and sea.
- Keep the **blue hue**, which the owner chose.

**Fix:** recolour by part name, everywhere under `Map.Hub.Walls`. Also update the colour constants in `HubV2Kit.Makeover.Walls`, so a rebuild keeps the new palette.

| Part names | Now | Start value |
|---|---|---|
| `Coping`, `PillarCap`, `CornerCap`, `TowerCap` | (232,222,196) | **(242,206,146)**, warm sandstone |
| `Pillar`, `CornerPillar`, `Tower`, `Base` | (58,84,130) | **(78,84,124)** |
| `PillarFoot`, `CornerFoot`, `TowerFoot` | (46,66,104) | **(56,58,92)** |
| `Panel` | (96,132,170) | **(108,128,164)** |

**Measure:** use the same cameras and crops as this review. The captures are 1519×753.

- **R08 camera** (-121,14,-46) → look (-121,15,-60). Crops:
  - panel (400,500,600,650)
  - pillar (200,300,300,600)
  - coping (400,125,1100,165)
- **R03 camera** (-66,14,34) → look (-170,8,56). Crops:
  - panel (700,330,800,400)
  - pillar (815,320,830,390)

```
python -c "from PIL import Image;import colorsys,sys;im=Image.open(sys.argv[1]).convert('RGB');c=im.crop(tuple(map(int,sys.argv[2:6]))).resize((1,1),Image.LANCZOS).getpixel((0,0));h,l,s=colorsys.rgb_to_hls(*[x/255 for x in c]);print(c,'H%.0f S%.2f L%.2f'%(h*360,s,l))" shot.jpg x0 y0 x1 y1
```

**Targets:**

| Part | Target |
|---|---|
| Coping | hue 25-50°, S ≥ 0.20 (warm, not cyan) |
| Pillar | R ≥ 30 and S ≤ 0.70, at both cameras; at least 0.10 L darker than the panel |
| Panel | hue 205-225°, S ≤ 0.50, L 0.48-0.58 |

**Iterate at most 3 times:**
- If the pillar is still crushed (R < 30), add +10 to its R and G.
- If the panel reads grey (S < 0.30), move it halfway back to the old value.
- Save the before/after pair as `review/M1_*`.

### M2. Add an orange cornice band under the coping on every edge

**Problem:** see `R03`, `R04_avenue_eye`, `R06_corridor_eye` and `R13_plaza_side_eye`.
- Long runs are identical studded slabs.
- Nothing on the hub walls repeats the orange of the runway walls or the pumpkins, so the junction is a clash of two primaries.

**Fix:** one Part named `Cornice` per edge, in `Map.Hub.Walls.E<i>`.

| Property | Value |
|---|---|
| Length | The edge length (the pillars cover the ends) |
| Height | y 20.0-20.8, directly under the coping. Follow the +0.02 coping lift on even edges. |
| Depth | d 0.45-0.80: 0.35 proud of the panel face, 0.05 behind the coping lip |
| Colour | (214,112,44), Plastic, smooth |
| Flags | Anchored; CanCollide, CanQuery, CanTouch and CastShadow all false; `_Makeover` |

**Follow-ups:**
- Lower the 4 corner webs and their 4 spiders by 1.0 (web y 14.4 → 13.4), so the web tops clear the band.
- The garland hooks (top about 18.9) and the lanterns (arm 16) are already clear.
- If it renders brown rather than orange in R08/R03, raise it to (236,128,52).

### M3. Pumpkin finials on the pillar caps (skyline and theme)

**Problem:** see `after_02_runway`, `R03`, `R13` and `p2_C9_hero`.
- The skyline is a flat line of slab caps.
- The pumpkin theme lives only on the back wall.

**Fix:** finials are part of the wall architecture, at one fixed rhythm: one finial per pillar, **38 in total**.

**Template:** clone `HalloweenDecor.StreetLamps.StreetLamp_1.Pumpkin`.
- Keep the SurfaceAppearance.
- Delete the PointLight, the emitters and the attachments.
- Scale it uniformly to 3.6 wide (about ×1.33 → 3.6 × 2.5 × 3.6).
- Anchored; no collide, query, touch or shadow; `_Makeover`.
- Parent: `HalloweenDecor.WallDecor.Finials`.

**Spots:** the bottom of each finial sits on its cap top (PillarCap top 25.2, TowerCap 30.2), and the carved face points into the hub.
- **24 mid pillars:** every mid pillar (28) EXCEPT E7 x ±14.6 and ±43.8. The VineGrip leaves cover those 4 (hand bbox x ±14.1..±45.9, up to y 29.3).
- **8 room corners:** one finial each, at vertex + 3.3·(n_a + n_b), with n = the outward normals of the two edges. Use the higher CornerCap. It faces along the inward bisector.
- **4 reflex corner blocks:** facing the inward bisector, into the plaza.
- **2 junction towers:** facing +Z.

**Gate:**
- A/B-capture C2, C10, C11, R03 and R13 with and without the finials.
- If the skyline reads busy, keep the corners and towers and only every other mid pillar per edge, mirror-symmetric.
- Do not add more of anything else on the caps.

### M4. Recolour the plot SlotBeds from pale mint to a muted lawn

**Problem:** see `R02_plot1_from_gate`, `R03`, `R06`, `R15_alley_corner_web_garland` and `after_10_alley`. The 60×90 slot bed around every R0 plot is the largest colour field in the hub. It renders as washed-out mint (201,218,174) and reads unfinished.

**Fix:** the colour is set at run time, so a recolour in Edit alone would be overwritten in Play.
- `ServerScriptService.BaseBuilder` line 16: `slotBed = Color3.fromRGB(150, 172, 112)` → **`Color3.fromRGB(100, 148, 66)`**.
- Recolour the 6 live `Bases.Base<i>.Plot.Look.SlotBed` parts the same way, so Edit matches Play.
- Back up the script under `_Backup_HubMakeover.Before.Scripts` and add it to Revert.

**Target:** R06 crop (100,520,500,600) renders hue 85-100°, S ≥ 0.30 and L ≤ 0.62. The owned plot grass must stay clearly brighter.

### M5. The junction bat flocks clip into the towers

**Problem:** see `R07_junction_bats_close` and `final_night_junction`.
- `Bat_E1_1` is centred at x -88 and is 7.2 wide, so it reaches x -84.4. That is inside the tower (x -80..-86) at the tower face plane. Its wing tip is cut off.
- E13 has the mirrored clip.

**Fix:** the clear bay is x -86 .. -105.8 (centre -95.9).
- Scale the 4 bat x-offsets about the flock centre (-94.2) by 0.8.
- Move the flock centre to **x ∓95.9**. The span becomes about -88.0..-103.7, at least 2 studs clear of the tower and the pillar.
- Mirror the change for E13.

---

## SHOULD

1. **Gate-corner ground details (12).**
   - **What:** at each gate, a cluster of a `Halloween_Candles` at scale 0.6 (≤ 1.44 tall) plus a `PumpkinEgg_Plain1` at scale 0.38 (≤ 1.5 tall, so it stays legal under Validate 21).
   - **Where:** P + D·2.0 ± L·8.6, with P = the gate point, D = the plaza-facing direction and L = the lateral axis. That is just outside the 14-wide kerb gap, beside the apron corners.
     - Gate 1: (-120,-38.6) and (-120,-21.4).
     - Gate 2: (-88,33.4) and (-88,50.6).
     - Gate 3: (-48.6,76) and (-31.4,76).
     - Gates 4-6 mirror these.
   - **Lights:** set the candles' PointLight `Enabled=false` and keep the flames.
   - **Why:** it marks every plot entrance and gives night sparkle where players actually walk (`R03`, `R12_plaza_mid_high`).
2. **Make the junction towers read as gate pylons.**
   - **Problem:** the tower (6 wide, top 30.2) is a thin blue sliver against the 40-tall orange runway wall (`R14_tower_sell_thirdperson`, `R05_junction_thirdperson`, `p2_tower`).
   - **Fix:** raise `Tower` to a top of 40.0 (size y 38.8 → 40, keeping the foot) and `TowerCap` to 40-41.4, so it reaches the orange wall top.
   - Keep the lantern at 13.7 and put the M3 finial on the new cap.
3. **Night warmth on the long runs.**
   - **Problem:** at night the side walls stay bright blue with no warm light. Only the back centre bay glows (`final_night_C10_alley`, `final_night_C2_runway`).
   - **Fix:** after M1-M3, give the finials on E1/E13 bays 2-5, E2/E12, E4/E10 and E5/E9 (about 14) a PointLight:
     - Range 10, day Brightness 0.3, Shadows false, Color (255,150,60)
     - attributes NightBrightness 1.6 and NightRange 14 (HalloweenClient boosts them like the lanterns; no script change)
   - Re-shoot the night views from a Play client (TestFreshSave true before, false after).

## NICE

1. **Outer faces** (`R11_outer_face`, `after_09_hero`): a flat unstudded slab, with the hub looking thin from the air and in the trailer.
   - Set the outward face of every `Panel` to Studs.
   - Add a FOOT-colour skirt on the outer face from y -8 to 0, so the walls look grounded.
2. **Lane rhythm** (`R04`, `R12`, `R13`): the lanes render identical to the paving; only the edge lines read.
   - Add 2×2 terracotta (150,96,64) diamond inlays on the lane centrelines every 12 studs (about 49 parts).
   - They are flat, 0.05 thick, at top y 0.07, with no collide, query or touch.
   - Or darken the lane fill to (160,132,98), a "worn stone" path with no glare.
3. **Hands on the front walls:** one more VineGrip pair on E1:3 / E13:3. Those bays are bare and sit in the main "facing the slingshot" view (`R01_spawn_thirdperson`). A/B it only, because it is a big piece.
4. **Orange runway-wall end faces** (x ±60..80, z -60, 40 tall): the most dominant raw block in the spawn view (`R01`).
   - Add a DARK base band (0-3.6) and a sandstone cap line at y 38.4-40 on the hub-facing face.

---

## What's good (keep it)

- **The back wall is the best view in the hub.** The giant head, the 2 hands, the bat bay between the 2 lanterns and the alley-end pumpkins all sit on the spine axis (`R10`, `p6_lantern_back`). It confirms ruling 1: VineGrip = the "pumpkin hands".
- **Garlands:** alternating (12) is the right density. Every garland bay is correct, and the web + garland pair at the alley corners reads balanced (`R15`).
- **The junction corner at night is lovely** (`final_night_junction`).
- **Lanterns, webs and spiders** are well scaled and seated.
- **Spawn view:** the medallion, the chest, the FREE! sign and the 4-board arena read cleanly (`R01`).
- **Nothing floats:** every pumpkin piece has its bottom at y 0.00, and the garland hooks sit 0.9 in front of the pillar faces.
- **Symmetry:** the only asymmetry is intended. The corner clusters use pumpkin A on one side and B on the other; they are 430 studs apart and never seen together.
- **Paving tone C** is calm, with no glare.

## Review captures (`makeover/review/`)

| File | What it shows |
|---|---|
| R01_spawn_thirdperson | Spawn view, third person |
| R02_plot1_from_gate | Plot 1 from its gate |
| R03_plot2_from_plaza | Plot 2 from the plaza |
| R04_avenue_eye | Front avenue at eye height |
| R05_junction_thirdperson | Runway junction, third person |
| R06_corridor_eye | Corridor at eye height |
| R07_junction_bats_close | Junction bats, close-up |
| R08_garland_close | A garland, close-up |
| R09_alley_mouth_lantern | Alley-mouth lantern |
| R10_backwall_thirdperson | Back wall, third person |
| R11_outer_face | A wall's outer face |
| R12_plaza_mid_high | Plaza from a mid height |
| R13_plaza_side_eye | Plaza side at eye height |
| R14_tower_sell_thirdperson | Junction tower by the Sell stall |
| R15_alley_corner_web_garland | Alley corner with the web and garland |

All were taken in Edit with the camera restored. No DataModel writes.
