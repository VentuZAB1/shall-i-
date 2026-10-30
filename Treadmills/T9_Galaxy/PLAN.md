# Tier9_x16 GALAXY: PLAN (Phase A, 2026-10-12)

Template `ServerStorage.Assets.Treadmills.Tier9_x16`, bay `workspace._TreadmillLab.Bays.Bay9` (belt centre 666, 0.6, -100).
Theme attribute: `m:SetAttribute("Theme", "Galaxy")`. Name, Tier 9, TierName x16, SpeedPerSecond 800000 and LabelHeight 10.6 stay as they are.

## What I studied
- Tiers 1-6 (bays 1-6) are chassis-only (14 to 26 visible parts, no decor, no hooks, top at y 8.5). T5 and T6 share the
  26-part chassis; T6 is gold + black. None of tiers 1-6 is purple; the closest hue is T3's pastel pink (222,89,178).
- Bay 9 today = the T6 chassis copy. `T.validate(9)`: 0 FAIL, 1 WARN (the label face is gold, lum 0.78).
- From the hub (front, -Z) people see the front console bar, the pillars, the upper bar and the BACK of the tilted label
  frame. The label itself only faces the runner.
- In the runner camera the label sits dead centre above the dummy's head, with empty sky above it up to the top of the
  frame. That is where the new raised screen goes, so the owner sees it for hours.
- Captures (Phase A): `T9_A_study_tiers1to6`, `T9_A_study_T6_hub34`, `T9_A_study_T3_hub34`, `T9_A_runner_v1`,
  `T9_A_spawn_v1`, `T9_A_side_v1`, `T9_A_rear34_v1`, `T9_A_close_v1`, `T9_A_lineup_v1`, `T9_A_eye_v1`.
- I read `TreadmillClient` (findScreen and the fx loop) and `_TreadLabTools.validate` to get the exact hook behaviour and
  check boxes.

## Concept (one line)
**"Star Gate":** a violet portal arch over the console. It holds a tall second screen (a starfield on the hub side, an
equalizer on the runner side) and is crowned by a magenta ringed planet with three orbiting moons. Low violet handrails
with twinkling stars run down both sides.

## Palette
| Role | RGB | MaterialVariant | Used for |
|---|---|---|---|
| FRAME (deep-space indigo, the dark frame) | (30, 20, 62) | Studs (Inlet on belt strips) | side frames, console bars, handles, plinths, screen tower body, topper base, rail posts, corner wedges |
| VOID (darker frame shade, screens only) | (16, 10, 36) | Universal | label face (lum 0.05), both big-screen display plates |
| VIOLET (main theme) | (118, 56, 222) | Studs on big blocks / Inlet on belt + rails / Weld on small blocks | arch posts + lintel, label frame (bezel), belt edge strips, rail bars, pillars, feet, base plate, planet dish |
| MAGENTA (nebula energy accent) | (240, 50, 210) | Universal (runes, planet, gem, bars) / Weld (grips, stripe, caps) / Inlet (centre strip) | rune bands, planet, screen_gem, centre belt lane, grips, bracket, front stripe, rail caps |
| LAVENDER (stardust) | (196, 168, 255) | Universal | planet ring (Transparency 0.3), star rays, 2 equalizer bars, some stars, 1 moon |
| STARLIGHT (stars) | (255, 240, 178) | Universal | sparkle stars, 2 moons, centre equalizer bar |

That is 4 theme colours (violet, magenta, lavender, starlight) plus the dark frame (VOID is only a darker shade of it,
for screens). There are 0 accent materials: everything is Plastic + variant, and the only translucent brick is the ring.

## Chassis recolour map (26 parts: size and position untouched, collision kept)
| Chassis part (belt space) | Role | Variant |
|---|---|---|
| Side frames 1.6x1.47x15.56 at x +-4.91 (2) | FRAME | Studs |
| Belt strip x 0 | MAGENTA (centre "runway" lane) | Inlet |
| Belt strips x +-1.30 and +-2.59 (4) | FRAME | Inlet |
| Belt strips x +-3.89 (2) | VIOLET (edge lanes) | Inlet |
| Base plate 12.71x0.61x15.39 | VIOLET (rim line along both sides) | Weld |
| Front console bar 14.27x2.16x1.73 | FRAME | Studs |
| Console pillars 1.3x1.73x1.12 (2) + centre piece 4.19x1.73x0.69 | VIOLET | Weld |
| Upper console bar 9.08x1.47x1.73 | FRAME | Studs |
| Screen bracket 2.16x2.85x0.99 (tilted) | MAGENTA (accent spine on the frame back) | Studs |
| Label FACE 6.14x3.11x0.86 (tilted) | VOID (16,10,36), lum 0.05, opaque | Universal |
| Label FRAME 6.48x3.46x0.86 (tilted) | VIOLET (bezel; a big violet panel seen from the hub) | Studs |
| Handles 1.3x1.47x2.59 (2) + upright knobs 1.3x1.47x0.61 (2) | FRAME | Studs |
| Handle grips 1.21x1.21x1.64 (2) | MAGENTA | Weld |
| Front side feet 1.25x1.21x4.58 (2) | VIOLET | Weld |

Belt read from the runner: violet edge | dark | dark | MAGENTA centre | dark | dark | violet edge. That gives a dark
space runway with a glowing centre lane under the white arrow texture.

## Decor list (all in `Decor`: Anchored, CanCollide / CanTouch / CanQuery false)
Positions are belt space (centre of the part), x = runner's right, -z = front. Sizes are X x Y x Z. Every part is
axis-aligned or rotated only about Z / Y, so none is X-tilted. I checked with `ToOrientation`: rx = 0 for the ring, the
diamonds and the wedges.

### A. Star Gate arch (17 parts)
| Name | Size | Position (centre) | Colour | Variant | Purpose |
|---|---|---|---|---|---|
| ArchPlinth_L / _R | 1.5 x 0.5 x 1.93 | (-+6.4875, 1.81, -8.475) | FRAME | Studs | post base, sits on the front console bar ends (y 1.56-2.06) |
| ArchPost_L / _R | 1.295 x 9.34 x 1.73 | (-+6.4875, 6.73, -8.475) | VIOLET | Studs | posts x 5.84-7.135, y 2.06-11.40, z -9.34..-7.61; inner face flush with the handle ends (x 5.84) |
| ArchLintel | 14.27 x 1.3 x 1.73 | (0, 12.05, -8.475) | VIOLET | Studs | crossbar y 11.40-12.70, same width/depth as the front console bar |
| ArchCornerWedge_L / _R | Wedge 1.73(depth) x 1.3 x 1.3 | x -+(4.54..5.84), y 10.1-11.4, z -9.34..-7.61 | FRAME | Studs | arch corner braces: right angle in the post/lintel corner, slope facing down-inward (rotated about Y/Z only) |
| rune_1 .. rune_4 | 1.395 x 0.45 x 1.83 bands | (+6.4875, y, -8.475), y = 2.45, 5.65, 7.75, 9.85 | MAGENTA | Universal | bands wrapping the +X post, bottom to top (they clear the handle at 3.03-4.5, the knob top at 5.11 and the wedge at 10.1) |
| rune_5, rune_6 | 0.45 x 1.4 x 1.83 bands | (+3.9, 12.05, -8.475), then (-3.9, 12.05, -8.475) | MAGENTA | Universal | bands wrapping the lintel, either side of the screen |
| rune_7 .. rune_10 | 1.395 x 0.45 x 1.83 bands | (-6.4875, y, -8.475), y = 9.85, 7.75, 5.65, 2.45 | MAGENTA | Universal | -X post, top to bottom: the light runs up, across and down the gate |

### B. Tall console: raised screen tower (18 parts)
| Name | Size | Position | Colour | Variant | Purpose |
|---|---|---|---|---|---|
| ScreenTower | 6.48 x 4.15 x 1.3 | (0, 10.625, -9.99) | FRAME | Studs | the raised screen body, x +-3.24 (same width as the label frame), y 8.55-12.70, z -10.64..-9.34. Its back face is flush on the lintel's front face (y 11.4-12.7). It sits 0.02 above the label frame's top edge (8.53), so the two screens stack into one tall console |
| ScreenDisplayRunner | 5.88 x 2.25 x 0.2 | (0, 9.975, -9.29) | VOID | Universal | runner-side display, y 8.85-11.10 (below the lintel) |
| screen_bar_1 .. _5 | 0.7 x h x 0.2, h = 1.0 / 1.3 / 1.6 / 1.3 / 1.0 | x = -2.2, -1.1, 0, 1.1, 2.2; bottom y 9.05; z -9.14 | MAGENTA / LAVENDER / STARLIGHT / LAVENDER / MAGENTA | Universal | equalizer on the runner side |
| sparkle_scr_1, _2 | 0.4 cube, 45 deg about Z | (-+2.3, 10.8, -9.19) | STARLIGHT | Universal | stars above the outer bars |
| ScreenDisplayFront | 5.88 x 3.55 x 0.2 | (0, 10.625, -10.69) | VOID | Universal | hub-side starfield display, y 8.85-12.40 |
| screen_gem | 1.0 x 1.0 x 0.3, 45 deg about Z | (0, 10.7, -10.84) | MAGENTA | Universal | galaxy-core diamond in the middle of the starfield |
| StarRayH / StarRayV | 3.2 x 0.22 x 0.14 / 0.22 x 2.8 x 0.18 | (0, 10.7, -10.82) / (0, 10.7, -10.84) | LAVENDER | Universal | 4-point lens-flare star behind the gem (different depths: no coplanar overlap) |
| sparkle_scr_3 .. _7 | 0.5 / 0.35 / 0.4 / 0.3 / 0.3 cubes, 45 deg about Z | (-2.3, 11.8), (2.4, 11.95), (2.3, 9.3), (-2.4, 9.45), (1.2, 12.05); all at z -10.79 | STARLIGHT x3, LAVENDER x2 | Universal | starfield, centred on the display surface so they stay attached while shrinking |

### C. Planet topper (7 parts)
| Name | Size | Position | Colour | Variant | Purpose |
|---|---|---|---|---|---|
| TopperBase | 6.48 x 0.5 x 3.03 | (0, 12.95, -9.125) | FRAME | Studs | cap flush over the lintel and screen tops (z -10.64..-7.61, y 12.7-13.2) |
| PlanetDish | Cylinder 0.3 x 2.0 x 2.0, axis vertical | (0, 13.35, -9.125) | VIOLET | Weld | projector dish, top at y 13.5 |
| orb_core | Ball d 1.8 | (0, 14.75, -9.125) | MAGENTA | Universal | the planet: hovers 0.35 over the dish (static top 15.65) |
| orb_ring_a | Cylinder 0.14 x 3.6 x 3.6 | at the core, rotated 115 deg about Z | LAVENDER, Transparency 0.3 | Universal | Saturn ring tilted 25 deg left/right. It precesses as the client spins it about the vertical (rx stays 0) |
| orb_shard_0 | Ball d 0.5 | (2.3, 15.2, -9.125) | STARLIGHT | Universal | moon |
| orb_shard_1 | Ball d 0.5 | (-1.15, 14.45, -11.117) | STARLIGHT | Universal | moon (120 deg apart) |
| orb_shard_2 | Ball d 0.5 | (-1.15, 14.9, -7.133) | LAVENDER | Universal | moon |

Orbit check: the moons orbit at r 2.3 around the core, so their sweep is z -11.675..-6.575, |x| <= 2.55 and y >= 14.05,
all inside the envelope. They clear the ring rim (r 1.8) by 0.25 and the topper base by 0.85. With the client's float
(+-0.15) and pulse (+12 %), the planet stays at y 13.59-15.91 (the dish top is 13.5, the cap is 16). The ring's low point
is 13.78. orb_ring_b is NOT used: a tumbling ring would sweep through the dish.

### D. Side rails (16 parts)
| Name | Size | Position | Colour | Variant | Purpose |
|---|---|---|---|---|---|
| RailBar_L / _R | 0.9 x 0.65 x 12.87 | (-+5.185, 3.525, 1.165) | VIOLET | Inlet | handrails continuing back from the handle grips (flush on the grip's back face at z -5.27) to z 7.6; y 3.2-3.85 |
| RailPost x3 per side | 0.9 x 2.325 x 0.9 | (-+5.185, 2.0375, z), z = -2.0, 2.3, 6.6 | FRAME | Studs | standing on the side frames (top 0.875) |
| sparkle_rail_L1..3 / _R1..3 | 0.5 cube, 45 deg about Z | (-+5.185, 3.85, z) above each post | STARLIGHT | Universal | star studs on the rail top (top 4.20, 4.24 at max twinkle) |
| RailCap_L / _R | 1.0 x 0.75 x 0.45 | (-+5.185, 3.525, 7.4) | MAGENTA | Weld | rear end caps (z 7.175-7.625) |

### E. Front face (5 parts)
| Name | Size | Position | Colour | Variant | Purpose |
|---|---|---|---|---|---|
| FrontStripe | 10.2 x 0.35 x 0.2 | (0, 0.35, -9.39) | MAGENTA | Weld | nebula line on the front console bar (x +-5.1, between the plinths) |
| sparkle_front_1 .. _4 | 0.45 cube, 45 deg about Z | (x, 1.0, -9.34), x = -4.4, -1.5, 1.5, 4.4 | STARLIGHT | Universal | stars on the front console bar |

```
FRONT ELEVATION (seen from the hub, -Z)              y
                    o  (moons orbit)                 15.9
               ==( PLANET )==   <- tilted ring       14.75
                  [ dish ]                           13.5
          [=======TopperBase=======]                 13.2
 [M]=====[============LINTEL============]=====[M]    12.7 / 11.4   (M = rune bands)
 |P|\    [  * starfield  +gem+   *  ]    /|P|        11.4 .. 8.55  ScreenTower
 |M|     [ *        --+--       *   ]     |M|
 |P|        \___ label frame back __/     |P|        8.53 .. 4.98
 |M|  [========= upper console bar =======]|M|       4.5
 |P|        [pillar][centre][pillar]       |P|
[plinth]==== front console bar (stars) ===[plinth]   1.56
```

## Animation hooks (all handled by TreadmillClient; 38 animated parts)
- **10 x `rune_<n>`** on the arch. While running, a white flash runs up the +X post, across the lintel and down the -X
  post (6 steps/s, a 1.7 s loop) and the other bands dim. Idle: all solid magenta.
  - The client lights runes in **GetDescendants order**, so I'll create rune_1..rune_10 in sequence as direct children
    of `Decor`. After `T.refresh(9)` I'll check that order in the bay clone.
- **5 x `screen_bar_<n>`** equalizer on the runner-side display. They are bottom-anchored, never on the label face.
- **17 x `sparkle_*`** stars: 7 on the big screen, 6 on the rails, 4 on the front bar. Each one is centred on its
  surface, so it never detaches while it twinkles (55-110 %).
- **Planet system:** `orb_core` floats and pulses, `orb_ring_a` precesses and `orb_shard_0..2` are 3 orbiting moons.
- **`screen_gem`**: the galaxy core pulses toward white while running.
- Not used: flame_, wing_, halo (left to x18/x20), led_side_ (forced cyan), chevron_ / belt internals.

## Lights (3 max, all Shadows = false)
1. PointLight in `orb_core`, (255, 90, 225), Brightness 2, Range 10: a magenta glow on the gate top. It moves with the
   planet.
2. SurfaceLight on `ScreenDisplayFront`, Face = Front (-Z), (170, 120, 255), Brightness 1.5, Range 12, Angle 110: a
   violet wash toward the plaza.
3. PointLight in `ScreenDisplayRunner`, (200, 130, 255), Brightness 0.8, Range 7: a soft glow for the owner. I'll
   remove it in Phase B if the runner capture shows it lifting the label face.

## Progression
- **vs x14 Frost (rails + arch):** x16 keeps both and adds:
  - the tall console: a second, raised screen stacked on the label screen and mounted on the arch;
  - a planet + ring + 3 moons topper. The top goes from roughly arch height (about 12-13) to 15.65.
  - much more motion: rune chase, equalizer, planet system, 17 star twinkles and a pulsing gem.
- **vs x18 Inferno:** x18 adds fins / spoiler (wing_ hooks), flames and its own palette. I stop at 89 visible parts,
  which leaves headroom under the 110 aim, and I don't use the wing_, flame_ or halo hooks.
- **vs tiers 1-6:** none of them is purple, and none has decor or animation. Galaxy is dominated by dark indigo and
  violet; magenta is only for small "energy" accents, so it can't read as T3's pastel pink. The silhouette (gate +
  stacked screens + planet) is unique in the ladder so far.

## Limits: how each one is respected
- **Functional parts and chassis:** untouched; only colour and MaterialVariant change. Every new part goes in `Decor`.
- **Envelope (|x| <= 7.4, -11.8 <= z <= 9.3, y <= 16):**
  - max |x| is 7.2375 (plinths); rune bands reach 7.185;
  - min z is -11.675 (moon sweep); the static decor reaches -10.99 (the gem);
  - max y is 15.65 static and 15.91 at peak animation;
  - the lowest decor is the FrontStripe at y 0.175, above the floor.
  - The hub path lamp (x 7.7+) is clear by 0.46.
- **Upgrade-sign keep-out (|x| > 6.4, 4 <= z <= 8.6):** nothing there. Rails, posts and caps stay within |x| <= 5.685.
  The arch is only at z -9.44..-7.51.
- **Runner Zone (|x| <= 3.1, 0.6 <= y <= 6.6, |z| <= 7.1):** nothing. All decor with |x| <= 3.1 is at z <= -9.0 or
  y >= 8.55.
- **Runner camera corridor (|x| <= 5, y >= 4.5, z >= 1.5):** nothing. The rails top out at 4.24 even with a sparkle at
  110 %.
- **Over the head (|x| <= 3.5, 6.6-12, z -7..1.5):** nothing. The screen and lintel are at z <= -7.61, and the moons
  that pass z -6.9 are at y > 14.
- **Label screen:**
  - The face stays the label, VOID (16,10,36), lum 0.05, opaque.
  - No decor is X-tilted, so findScreen still sees only the 3 chassis tilted parts.
  - The raised screen is vertical, sits behind the face's top edge (z <= -9.34 versus the face top edge at -9.16) and
    starts 0.16 higher. Even from a high camera it can't cover the text.
  - The equalizer bars start at y 9.05, above the label top (8.39).
- **Banned items:** no Neon / ForceField / MeshPart / Union / Decal / Texture / script / particle; Plastic + variant
  only.
- **Lights:** 3, Shadows off.
- **Part count:** under 110 (see below).
- **Craft:**
  - Symmetric pairs, with flush seats: plinth on the bar, post on the plinth, lintel on the posts, screen on the lintel
    face, cap over both.
  - Decorative bands and stars overhang by 0.05 so no faces are coplanar, and the two star rays sit at different depths.
  - The planet hovers on purpose (it is animated) over a projector dish.

## Estimated part count
26 chassis + 63 decor = **89 visible parts**: arch 17, screen tower 18, topper 7, rails 16, front 5. That is under the
110 aim and the 140 hard cap. 0 accent-material parts, 3 lights.

## Phase B order (after approval)
1. Recolour the chassis and set Theme. Refresh and capture.
2. Arch with runes. Refresh, then check the `runner`, `close` and `hub34` captures.
3. Screen tower and displays. Refresh, then check `runner` for label legibility and `side` for the stack seam.
4. Topper and planet system, then lights.
5. Rails, then front stars.
6. Refresh, capture all 8 presets, check the rune order and the validator (0 FAIL; target 0 WARN). Then write
   BUILD_NOTES.md.

Known risks to check in Phase B:
- the 0.02 seam where the raised screen meets the label frame (side view);
- whether the planet is cut off at the top of the `runner` preset;
- whether the runner PointLight greys the label face.
