# Halloween street lamp: "Pumpkin lantern post" (round 3, 2026-10-14)

Script: `lamp.py` (helper kit `lampkit.py`). Run with
`blender.exe -b --factory-startup --python lamp.py -- <step>`. Add `fast` before the step for a low-res test.
The steps, in order: `preview | build | bake post | bake cage | bake pumpkin | web | export | verify | calib | review`.
Re-run `build` before re-baking: a bake replaces the per-group bake materials on the game mesh.

The proof renders and measurements built on the reviewer's `review_check\rv.py` are made by
`wip\rv2_measure.py -- face | twist | close | checks | night | c14ns`. Their output is in `wip\rv2\`.

Files:
- `lamp.blend`: the 5 game objects only.
- `lamp_src.blend`: the game objects plus the hidden bake sources (`Hi_*`) and the boolean `Cutter`.
- `maps\`: every texture as a PNG.
- `*.json`: the numbers below (`build`, `bake_*`, `web`, `export`, `verify`, `calib`).
- FBX: **`C:\cdimp\Halloween_StreetLamp.fbx`** (5.5 MB). It holds 5 mesh objects and embeds 12 PNG maps, each once.

## Coordinates and axes
- 1 Blender unit = 1 stud. +Z is up.
- **All 5 objects share ONE origin**: the centre of the pole foot on the ground, at (0, 0, 0). They are NOT centred on their own bboxes. The feet bottom is at z = -0.01.
- In Roblox each MeshPart's Position is its own bbox centre. The importer keeps the parts' relative placement, so use the offsets below, measured from `Cage.Position` (or `Post.Position`).
- Directions:
  - The arm reaches toward Blender **-Y**.
  - The pumpkin face looks along the arm, away from the pole: Blender **-Y**.
  - The bat faces Blender **+X**.
  - The web lies in the Y-Z plane and bows about 0.1 toward +X.
- FBX settings (hkit `FBX_ARGS`): axis_forward -Z, axis_up Y, global_scale 0.01, apply_unit_scale. A Blender re-import gives object scale 0.01.
- Roblox conversion:
  - The lead noted the importer turns models 180°, so **Roblox = (-x, z, y)** (Blender +Y → Roblox +Z, +X → -X). The face then looks toward Roblox **-Z**.
  - The plain hkit mapping (x, z, -y) is listed too, in case a later import does not turn the model.

## Objects

| Object | Size x / y / z, Blender (studs) | Roblox size X / Y / Z | bbox centre (Blender) | Tris | Embedded textures |
|---|---|---|---|---|---|
| Post (pole, ogee base + 4 claw feet, twist, crook, volute, bat) | 2.128 / 5.240 / 18.556 | 2.128 / 18.556 / 5.240 | (0.000, -1.556, 9.268) | 5,800 | 1024: colour, normal, roughness |
| Cage (straps, top ring, witch hat + spear, saucer, collar, drop finial, ring + 2 links) | 2.579 / 2.579 / 4.182 | 2.579 / 4.182 / 2.579 | (0.000, -3.550, 13.957) | 3,136 | 512: colour, normal, roughness |
| Pumpkin (carved shell, stem, candle, wick, wax puddle) | 2.726 / 2.744 / 1.901 | 2.726 / 1.901 / 2.744 | (-0.013, -3.550, 13.229) | 3,500 | 1024: colour, normal, roughness |
| Web (orb web strands) | 0.234 / 3.321 / 4.507 | 0.234 / 4.507 / 3.321 | (0.057, -1.817, 15.154) | 1,110 | 512: colour, roughness |
| WebSilk (gauze, drape, hub patch; alpha) | 0.079 / 2.052 / 3.042 | 0.079 / 3.042 / 2.052 | (0.068, -1.257, 14.588) | 300 | 512: colour with alpha |
| **Total** | height 18.546 above the ground; footprint 2.128 x 2.128; the iron reaches 4.176 from the pole axis; lowest head point 11.866 | | | **13,846** | |

- Budgets: ≤ 14,000 total, ≤ 8,000 per object. Both met; the largest object is 5,800.
- Texel density in px/stud:
  - Post 119;
  - Cage 97;
  - Pumpkin 141.
  - The base island has 1.6x priority on top of that. Every part is baked at 2x and box-filtered down.
- The colour maps already include baked AO. The Pumpkin's cavity and cut walls use only 0.08 / 0.15 AO, so the holes stay bright.
- No emissive or Neon anywhere. The glow comes only from the lights below.

## Attachment points (Blender object space; all in studs)
Round 2 made the witch-hat cone taller, so the whole head (cap, pumpkin, cage) hangs **0.26 lower** than in round 1. The chain top and bat perch did not move.

The Cage bbox centre lies exactly on the hanging axis. Offsets are given from `Cage.Position`, using the lead's turned mapping (-dx, dz, dy).

| Point | Blender (x, y, z) | Roblox (-x, z, y), turned | Roblox (x, z, -y), hkit | Offset from Cage.Position (turned) |
|---|---|---|---|---|
| Wick tip (end of the curl) | (0.017, -3.516, 12.795) | (-0.017, 12.795, -3.516) | (0.017, 12.795, 3.516) | (-0.017, -1.162, 0.034) |
| Wick top (highest point) | (0.011, -3.528, 12.800) | (-0.011, 12.800, -3.528) | (0.011, 12.800, 3.528) | (-0.011, -1.157, 0.022) |
| Flame centre (wick top + 0.05) | (0.011, -3.528, 12.850) | (-0.011, 12.850, -3.528) | (0.011, 12.850, 3.528) | (-0.011, -1.107, 0.022) |
| **Suggested inside PointLight** | (0.011, -3.528, 12.860) | (-0.011, 12.860, -3.528) | (0.011, 12.860, 3.528) | (-0.011, -1.097, 0.022) |
| **Cavity centre** | (0.000, -3.550, 13.081) | (0.000, 13.081, -3.550) | (0.000, 13.081, 3.550) | (0, -0.876, 0) |
| Cavity floor (inside, centre) | (0.000, -3.550, 12.408) | (0.000, 12.408, -3.550) | (0.000, 12.408, 3.550) | (0, -1.549, 0) |
| **Ground-light point** (just under the bottom collar) | (0.000, -3.550, 12.046) | (0.000, 12.046, -3.550) | (0.000, 12.046, 3.550) | (0, -1.911, 0) |
| **Chain top** (ring, top of its inner circle in the crook cradle) | (0.000, -3.550, 15.969) | (0.000, 15.969, -3.550) | (0.000, 15.969, 3.550) | (0, 2.012, 0) |
| **Pumpkin rotation pivot** (pumpkin centre on the hanging axis) | (0.000, -3.550, 13.099) | (0.000, 13.099, -3.550) | (0.000, 13.099, 3.550) | (0, -0.858, 0) |
| Bat perch (top of the bar at the apex) | (0.000, -1.873, 17.752) | (0.000, 17.752, -1.873) | (0.000, 17.752, 1.873) | (0, 3.795, 1.677) |

- The hanging axis is the vertical line through (0, -3.55) in Blender: Roblox X = 0, Z = -3.55 from the pole axis (turned mapping).
- The pole axis is the vertical line through the origin. From `Post.Position`, the pole axis is 1.556 studs away from the arm, on the side opposite it.
- The ground is 9.278 below `Post.Position`.

## Lights (Studio)
- **Inside PointLight**, the same as the eggs (`LEAD_INTEGRATION.md`):
  - Range 11, Brightness 1.2, Color `ff963c`, Shadows true, attribute `Flicker` = 1.2;
  - place it in an Attachment at the suggested PointLight point;
  - parent it to the Pumpkin so it turns with it. It is only 0.025 off the axis, so the Cage works too.
  - The day face read was proven with this light on (see BUILD_NOTES, Round 2, MUST 1). If the face still looks soft in Studio by day, raise the daytime Brightness (reviewer's note).
- **Candle flame**:
  - the eggs' Flame ParticleEmitter (Grid8x8 flipbook, attribute `Prime`) in an Attachment at the flame centre;
  - the flame is about 0.12 wide and 0.25 tall at this candle size, so start at Size ≈ 0.25 and tune.
  - The wick is about 0.05 thick. The candle is amber wax, 0.40 tall, with a soot ring round the wick.
  - The flame shows through the mouth at night (`wip\rv2\N03_head8_side.png`).
- **Ground-pool SpotLight** at the ground-light point:
  - Face = Bottom (straight down), Angle 110, Range 16, warm colour (`ffb068` in the review; `ff963c` also works), Brightness about 1-1.5, Shadows **false**;
  - parent it to the Cage.
  - Reason: the closed pumpkin sends almost no light onto the path. This spot makes the warm pool shown in `review_night_25.png` and `review_night_path_3lamps.png`.
- The Glow ParticleEmitter from the eggs can sit at the cavity centre if wanted. Keep its Size small (about 2.5): the pumpkin is only 2.7 wide.

## Turning the pumpkin (90° steps, no clipping)
- The cage, ribs and straps repeat every 90°.
- The clearance check ran at all 4 angles:
  - skin to cage ≥ **0.327** at 0°, 90°, 180° and 270°;
  - stem to cap ≥ **0.338** at each angle (rule ≥ 0.30);
  - the candle and wick stay centred.
- Turn about the **Cage centre**, not about `Pumpkin.Position`. The pumpkin's bbox centre is 0.013 off the axis because of the stem lean and the face.

```lua
-- quarterTurns: +1 = 90 deg counter-clockwise seen from above, -1 = clockwise, 2 = half turn.
local function turnPumpkin(lamp: Model, quarterTurns: number)
	local cage = lamp:FindFirstChild("Cage") :: BasePart
	local pumpkin = lamp:FindFirstChild("Pumpkin") :: BasePart
	local pivot = cage.Position            -- the Cage bbox centre lies ON the hanging axis
	local up = Vector3.yAxis               -- lamps stand upright; use lamp:GetPivot().UpVector if tilted
	local turn = CFrame.new(pivot) * CFrame.fromAxisAngle(up, quarterTurns * math.pi / 2) * CFrame.new(-pivot)
	pumpkin.CFrame = turn * pumpkin.CFrame -- Attachments / lights parented to the Pumpkin follow it
end
```

- The face starts looking along the arm: Roblox -Z of the model as imported (the turned mapping). From there:
  - `+1` turns it toward the model's -X;
  - `-1` turns it toward +X.
- **Advice:** on the 6 path spots the arms reach ACROSS the path. Turn each face ALONG the path, toward the plaza, so walkers see it.
  - `review_day_25_side_face.png` and `review_night_25_side_face.png` show it turned toward the side camera.
  - The 3-lamp shots show a row of faces looking down the path.
- **Market-deck spots 7 and 8 (reviewer's note):** seen from the front (-Y), the lamp's silhouette is a lollipop: pole + round head, no crook. Turn each of these lamps so its arm reaches ACROSS the main line of sight, as on the paths, so players see the crook side-on.

## Studio setup
- Every part:
  - CanCollide / CanTouch / CanQuery false, CollisionFidelity Box, RenderFidelity **Precise**;
  - Anchored.
  - Never use Hull on the Post: the crook would make a giant hull.
- **WebSilk**:
  - SurfaceAppearance AlphaMode = **Transparency**. The alpha is in the colour map, `maps\WebSilk_albedo.png`.
  - The FBX embeds that PNG once (12 PNG streams for 12 maps).
  - Blender's own FBX importer shows it as two image datablocks, because colour and alpha are 2 texture links to the same image. Use the one ColorMap.
- **Web and WebSilk**: CastShadow = false. Thin strands make noisy shadows.
- The Pumpkin, Cage and Post can keep CastShadow on.
- **Do not sway the Cage.** The web is tied to chain link 1 (web to link 0.016) and would tear away.
- **Colliders** (optional, if the lamp must block players), as invisible anchored parts, Transparency 1, CanCollide true:
  - **Pole**: Cylinder Size (16, 0.6, 0.6), Orientation (0, 0, 90) so it stands upright. Its centre is on the pole axis, 10.0 above the ground (it spans 2 → 18).
  - **Base**: Block Size (2.0, 2.6, 2.0), centred on the pole axis 1.3 above the ground. The base bell is r 0.97; the claw feet reach to 1.06 on the diagonals.
  - The arm and lantern sit at 11.8+ studs and need no collider.
- **Roughness-map fallback**:
  - `verify` confirms that every part has its roughness image packed and linked in the FBX.
  - If the import drops it, as it did for the Spider, set `SurfaceAppearance.RoughnessMap` by hand from `maps\Post_rough.png`, `maps\Cage_rough.png`, `maps\Pumpkin_rough.png` or `maps\Web_rough.png`.
- **Metalness** (not embedded; optional, set by hand):
  - `SurfaceAppearance.MetalnessMap` = `maps\Post_metal.png` and `maps\Cage_metal.png`;
  - worn iron edges = 1, paint = 0, so the worn edges glint like iron.
  - Leave it empty on the other parts.
- Normal maps are tangent-space, OpenGL (Y+), MikkTSpace: what Roblox expects.
- Two parts carry custom normals; keep the file normals on import:
  - the Pumpkin shell carries custom (smooth) normals;
  - the Post column has split normals at its real creases (collar chamfers, base neck, plinth steps).

## Textures in `maps\`
| Part | Size | Files |
|---|---|---|
| Post | 1024 | `Post_albedo`, `Post_normal`, `Post_rough`, `Post_metal`, `Post_ao` |
| Cage | 512 | `Cage_albedo`, `Cage_normal`, `Cage_rough`, `Cage_metal`, `Cage_ao` |
| Pumpkin | 1024 | `Pumpkin_albedo`, `Pumpkin_normal`, `Pumpkin_rough`, `Pumpkin_ao` |
| Web | 512 | `Web_albedo`, `Web_rough` |
| WebSilk | 512 | `WebSilk_albedo` (RGBA) |

`*_ao.png` is for reference only: it is already multiplied into the albedo. `wip\<Part>_ids.png` holds the bake-group id maps used for the measurements.

## The model in short
- **Post:**
  - a cast-iron fluted pole, r 0.29 tapering to 0.22, with 12 flutes 0.03 deep (in the normal map; the flute ends fade smoothly into the collars);
  - a twisted square-bar section with ±21 % twist: the lobes grow smoothly out of collar 1 and sink into collar 2 (0.22 ramps); iron-dark with bright wear on the helix crests and rust only along the deepest groove line;
  - a clean round **ogee bell** (32 sides) with crisp recessed gothic panels and a raised spider-web relief, on 4 claw feet;
  - a continuous **shepherd's crook**:
    - apex at y -1.873, z 17.58; largest bend radius 3.93;
    - ends in a curl 0.95 across that wraps 285°, with a ball knob;
    - the ring hangs in its cradle at y -3.55;
  - a log-spiral volute in the upper inside corner;
  - a cast-iron **bat** perched across the bar: wings along the arm, span 2.06, 15° dihedral, jagged fingers, fangs, head turned 30° down toward +X.
- **Cage:**
  - 4 straps offset 0.36 from the pumpkin's max-radius envelope (computed over every azimuth, so it holds at every turn); the under-loop rounds smoothly into the bottom collar;
  - a top ring;
  - a **witch hat**: brim r 0.84, a 0.66 tall cone with a concave flare, then a flat spear-head finial 0.34 tall, pierced near its base for the link, tip bent 28° toward the pole;
  - a saucer seat, a 20-sided bottom collar and a shorter 14-sided drop finial (lowest point 11.866);
  - chain: ring + 2 links.
- **Pumpkin:**
  - R 1.35, Rz 0.96 (2.73 wide), 8 ribs, gnarly stem;
  - a bold scowling face:
    - eyes 0.66 wide;
    - nose 0.32;
    - grin 1.91 wide, open 0.50 at the centre;
    - 2 + 2 teeth 0.24-0.26 wide at the root;
  - every hole has a dark rind band (about sRGB 120, 45, 10; 0.03-0.04 wide) on the skin side of the knife edge;
  - the cavity is pale warm yellow (baked mean sRGB 247, 220, 151);
  - the knife walls are a deeper flesh tone (211, 148, 70), so the holes read as solid lit shapes by day;
  - the face holes go all the way through (4 holes in the bake source and the game mesh);
  - an amber candle (166, 117, 57) with a soot ring and a curled wick.
- **Web:**
  - 14 tapering spokes (0.088 → 0.12 thick); every sector is 23.7-27.6° wide;
  - 2 spokes are anchored on the pole 50° apart, one by collar 3 and one at z 13.3;
  - 7 catch rings spaced x1.25 outward (closer near the hub), tapering 0.085 → 0.114 thick:
    - every chord end is offset so no two neighbouring spans in a sector are parallel (largest parallel run: 1);
    - where the frame comes close, a ring stops instead of bunching;
    - 2 chords are broken;
  - strands silvery grey (205, 207, 214), dustier toward the iron;
  - span 3.32 (Y) x 4.51 (Z);
  - one long loose thread drapes from the lower edge and curls at its end;
  - silk: corner gauze, a drape, and a larger hub patch (r 0.56).

## Known limitations
- **Bat bake**: 11.9 % of the bat's texels found no high-poly surface. The game wings use a coarser outline than the scalloped bake source. The misses are filled from neighbours; no visible fault at 8-10 studs (`wip\rv2\D10_crook10.png`).
- **Cut walls**: 9.4 % of the cut-wall texels are filled the same way. They read as plain flesh.
- **EEVEE review artefacts**: with sun shadows on, the review renders show fine diagonal stripes in two places:
  - on collar 2's lit edge (`C14`);
  - stair-steps on the base (the reviewer's `D11` note).
  - These are EEVEE shadow-terminator artefacts, not texture faults. With the sun's shadows off, the same view is clean: `wip\rv2\C14_nrm_mid_pole_noshadow.png` and the reviewer's `E03`.
- **Web**: the web is still an orb web, so the outer chords of one sector are roughly concentric. The alternating chord offsets stop them from reading as parallel rungs.
- **Face read margin**: the daylight fill/skin ratio passes on luminance (1.93-1.98x). On plain sRGB luma it passes with less margin (1.42-1.44x).
- **Budget**: the total is 13,846 tris, so there are 154 tris of headroom.
- **Lighting match**: the review day sun is an approximation. Only the night was calibrated to `previews\night\A_Moonlit.jpg`:
  - green measured (96, 159, 92), target (93, 159, 88);
  - cream measured (184, 177, 184), target (184, 177, 185).
- **Review flame**: the flame in the night renders is a review-only emission stand-in on the wick. It is not in the FBX.
- **UV unwrap warning**: Blender warns that the pumpkin unwrap "failed to solve 2 of 14 islands". Those islands keep their Smart-UV projection; a check found no collapsed or zero-area UV island.
