# T11 `Tier11_x20` (x20, 1M/s): DIAMOND RAINBOW. PLAN (Phase A, no edits made)

## Concept
A "jewel-box" treadmill: an obsidian base with a diamond-white frame and a ROYGBIV rainbow belt. A grand rainbow ARCH
stands over the console. Its keystone carries an obsidian CROWN with a floating, spinning diamond and flapping
crystal-white wings. A crystal "tall console" holds a rainbow equalizer above the label screen, and two
crystal-capped rear PYLONS are joined by a low white spoiler.

## What I studied (captures, ids)
- `T11_A_bays1to6_front`, `T11_A_bay1to3_spawn`, `T11_A_bay6_hub34b`, `T11_A_bay6_runner`, `T11_A_bay6_side`,
  `T11_A_bay6_spawn`, `T11_A_bay6_rear34`, `T11_A_bay11_lineup`, `T11_A_bay11_runner`.
  - `T11_A_bay6_hub34` is NOT valid: it was taken in parallel and shows bay 5. Captures must run one at a time.
- **Tiers 1–6:** chassis only, no decor.
  - Each is one bold colour plus one dark colour.
  - Variant use (from T6): Studs on the big frame bars, Inlet on the belt strips, Weld on the accent blocks (feet,
    posts, grips, base plate), Universal on the screen face.
- **Bay 11 now:** a plain Tier6 copy.
  - Validator: `0 FAIL, 1 WARN` (the gold screen face is too bright).
  - The runner capture shows the mock "+1M" on the yellow face.
- **TreadmillClient hook facts that shape the plan:**
  - `halo` spins only around belt-vertical (Ry), so its X-tilt never changes.
  - `sparkle_` scales around its own centre.
  - `rune_` order = GetDescendants order. While running, the other runes dim 45 % and one white flash moves along at
    6 steps/s.
  - Wings roll around Z through `wing_root_*`, at up to ±0.28 rad.
  - `chevron_` wraps between z −3.8 and 3.4 and only moves while running.
- **Validator boxes:**
  - The HEAD warn box reaches all the way to z = −7.
  - The sign keep-out also applies for y −1..8.
  - Screen detection uses |rx| = 0.35 ± 0.1 at z < −6. None of my parts have that X-tilt.

## Palette (RGB, variant)
| Role | RGB | Material / variant | Notes |
|---|---|---|---|
| **W** Diamond white (main structure) | 242, 246, 255 | Plastic / Studs (bars) · Weld (facet pieces) | slightly cool pure white, not ice-blue (so it doesn't read as T8 Frost) |
| **C** Crystal (translucent) | 225, 238, 255, Transparency 0.35 | Plastic / Weld | the Weld X-pattern reads as gem facets |
| **O** Obsidian (dark frame) | 26, 24, 40 | Plastic / Studs · Weld (plinths, feet) · Inlet (grips) | deep blue-black velvet; makes the white and the rainbow pop |
| **M** Midnight label face | 30, 26, 64 | Plastic / Universal | luminance 0.12, opaque |
| **Rainbow** (one role, 7 hues) | R 255,58,58 · O 255,140,26 · Y 255,214,32 · G 46,204,96 · B 30,144,255 · I 88,86,232 · V 178,76,240 | Plastic / Inlet (belt) · Studs (arc) · Universal (EQ bars, gems) | always red on the runner's LEFT (−x) through violet on the RIGHT (+x) |
| **G** Gem glass (accent) | 240, 248, 255, Transparency 0.15, Reflectance 0.2 | Glass | only the halo diamond and 8 sparkle gems (9 parts, about 10 % of the model, under the 15 % limit) |

This gives three theme roles (W, C, Rainbow) plus the dark frame O, with M only on the label face. No Neon, no
SmoothPlastic, no Plastic without a variant.

## Chassis recolour map (26 parts; size, position and collision unchanged)
| Chassis part | Role |
|---|---|
| 7 belt strips (1.3×0.86×16.26), x = −3.89 / −2.59 / −1.30 / 0 / 1.30 / 2.59 / 3.89 | Rainbow **R / O / Y / G / B / I / V**, Inlet (a "rainbow road" for the runner) |
| Side frames ×2 (1.6×1.47×15.56, x ±4.91) | W Studs |
| Base plate (12.71×0.61×15.39) | O Studs (dark plinth rim) |
| Front console bar (14.27×2.16×1.73) | W Studs |
| Console posts ×2 (1.3×1.73×1.12) + centre post (4.19×1.73×0.69) | O Weld (dark recess between the white bars) |
| Upper console bar (9.08×1.47×1.73) | W Studs |
| Handles ×2 (1.3×1.47×2.59) + handle caps ×2 (rotated 1.3×1.47×0.61) | W Studs |
| Handle grips ×2 (1.21×1.21×1.64) | O Inlet |
| Screen bracket (2.16×2.85×0.99, tilted) | O Studs |
| Screen frame (6.48×3.46×0.86, tilted) | W Studs (white bezel) |
| **Screen face** (6.14×3.11×0.86, tilted, the label surface) | **M Midnight 30,26,64, Universal** (luminance 0.12, Transparency 0) |
| Front feet ×2 (1.25×1.21×4.58) | O Weld |

## Decor list (all in `Decor`: Anchored, CanCollide / CanTouch / CanQuery false)
Positions are belt space (x, y, z) at the part centre. Pairs are mirrored in x.
- Arch plane: z_a = −10.135.
- Arc: centre (0, 5.7), radius R = 6.55 (centre line), thickness 1.2.

### 1. Grand rainbow front arch (the T8 "arch" step, grown into the T11 grand front arch; its legs are the front pylons)
| Name | Size | Position | Role / variant | Purpose |
|---|---|---|---|---|
| ArchPlinth_L/R | 1.6×0.8×1.6 | (∓6.55, −0.2, −10.135) | O Weld | foot on the floor; back face flush with the console bar front (z −9.335) |
| ArchLeg_L/R | 1.2×4.9×1.3 | (∓6.55, 2.65, −10.135) | W Studs | diamond-white front pylons (y 0.2–5.1) |
| ArchCapital_L/R | 1.4×0.6×1.5 | (∓6.55, 5.4, −10.135) | O Studs | springline cap (y 5.1–5.7); holds lights L2/L3 |
| rune_1 (red) | 2.99×1.2×1.1 | (−6.386, 7.157, z_a), rotZ +77.14° | Rainbow Studs | arc voussoir 1 (runner's left) |
| rune_2 (orange) | 2.99×1.2×1.3 | (−5.121, 9.784, z_a), rotZ +51.43° | Rainbow Studs | voussoir 2 |
| rune_3 (yellow) | 2.99×1.2×1.1 | (−2.842, 11.602, z_a), rotZ +25.71° | Rainbow Studs | voussoir 3 |
| rune_4 (green, keystone) | 2.99×1.2×1.3 | (0, 12.25, z_a), rotZ 0 | Rainbow Studs | keystone; top at y 12.85 carries the crown |
| rune_5 (blue) | 2.99×1.2×1.1 | (2.842, 11.602, z_a), rotZ −25.71° | Rainbow Studs | voussoir 5 |
| rune_6 (indigo) | 2.99×1.2×1.3 | (5.121, 9.784, z_a), rotZ −51.43° | Rainbow Studs | voussoir 6 |
| rune_7 (violet) | 2.99×1.2×1.1 | (6.386, 7.157, z_a), rotZ −77.14° | Rainbow Studs | voussoir 7 (runner's right) |

- The voussoirs alternate 1.1 / 1.3 deep. Their corners overlap slightly at the outer joints, so the different
  depths stop z-fighting and give a real brick-arch joint look.
- Computed extents: x ≤ 7.30, inner apex y 11.65, outer apex y 12.85.
- The end voussoirs' inner bottom corners sink 0.12 into the opaque capitals. I'll tune the small outer-corner sliver
  in Phase B, by nudging y or widening the capital to 1.5.

### 2. Crown and spinning diamond (on the keystone)
| Name | Size | Position | Role / variant | Purpose |
|---|---|---|---|---|
| CrownBand | 3.0×0.8×1.6 | (0, 13.25, z_a) | O Studs | dark crown band (y 12.85–13.65) |
| CrownPoint ×4 | 0.5×0.9×0.5 | (±1.25, 14.1, z_a ± 0.55) | W Weld | crown points at the band corners (y 13.65–14.55) |
| sparkle_crown_1..4 | 0.4 cube, on its vertex (body diagonal vertical) | (±1.25, 14.9, z_a ± 0.55) | G Glass | twinkling gem tips (y 14.55–15.25) |
| **halo** | 1.1 cube, on its vertex | (0, 14.8, z_a) | G Glass + PointLight L1 | the floating, spinning DIAMOND |

- **halo height:** y 13.85–15.75 at rest. With the ±0.18 float it moves between 13.67 and 15.93: never touches the
  band and never goes above 16.
- **halo clearance:** its widest horizontal radius is 0.90. The nearest crown-point corner is 1.04 from the axis.
- **halo tilt:** rx is 35.26° or 45°. Spinning around Y never changes rx, so it can never be mistaken for the
  screen. Its area is tiny anyway.

### 3. Crown wings (the T10 "fins" step in diamond style, animated)
| Name | Size | Position | Role / variant | Purpose |
|---|---|---|---|---|
| wing_root_L/R | 0.4×0.8×0.8 | (∓1.7, 13.25, z_a) | W Studs | hinge blocks flush with the band ends; the flap pivot |
| wing_L/R | WedgePart, span 3.0 × height 1.5 × 0.25 thick | root edge at x ∓1.9, y ≈ 12.9–14.4, z_a; swept up 15° at rest, tip at x ≈ ∓4.8 | W Weld | crystal-white wings; flap by rolling around Z |

- At rest the wing tips reach y ≈ 15.0. The extra flap (3.0 × 0.276 = 0.83) takes them to at most 15.85, under 16.
- The wings stay above the arc: the arc's outer surface at x 4.8 is at y 11.1.
- **Why the wings are on the crown and not the sides:** side-mounted flapping fins would clip the side rails at full
  flap, or swing out past |x| 7.4. On the crown they flap freely, and the runner can see them.

### 4. Tall console with an equalizer screen (the T9 step)
| Name | Size | Position | Role / variant | Purpose |
|---|---|---|---|---|
| ConsoleTower_L/R | 0.6×4.195×1.0 | (∓3.6, 6.6025, −8.575) | C Weld | crystal towers next to the screen (x 3.3–3.9), standing on the upper console bar (y 4.505–8.7) |
| MarqueeBody | 7.8×1.3×1.0 | (0, 9.35, −8.575) | W Studs | top display bar on the towers (y 8.7–10.0), above the screen top (8.38) and inside the arch opening (the inner arc at x 3.9 is y 10.19) |
| MarqueeDisplay | 6.8×1.0×0.1 | (0, 9.35, −8.025) | O Universal | dark display on the runner side |
| screen_bar_1..7 | 0.55×0.8×0.15 | x = −2.7, −1.8, −0.9, 0, 0.9, 1.8, 2.7 · y 9.35 (8.95–9.75) · z −7.9 | Rainbow R→V, Universal | rainbow equalizer facing the runner (never on the label face) |
| screen_gem | 0.8×0.8×0.25, rotZ 45° (diamond outline) | (0, 9.35, −9.2) | Rainbow B 30,144,255, Universal | sapphire on the marquee's plaza side; pulses white while running |

### 5. Rails (the T7 step, low)
| Name | Size | Position | Role / variant | Purpose |
|---|---|---|---|---|
| RailPost ×6 | 0.8×1.225×0.8 | (±5.19, 1.4875, z = −4.0 / 1.6 / 7.2) | C Weld | crystal posts on the side frames (y 0.875–2.1) |
| RailBar_L/R | 0.8×0.5×12.35 | (±5.19, 2.35, 1.775) | W Studs | low white rail (y 2.1–2.6, z −4.4 to 7.95), butting into the rear pylons |
| sparkle_rail_L/R | 0.4 cube, on its vertex | (±5.19, 2.95, −4.0) | G Glass | gem glints at the rail fronts, in the runner's view |

### 6. Rear corner pylons and spoiler (the T11 pylons, plus the T10 "spoiler" step kept low)
| Name | Size | Position | Role / variant | Purpose |
|---|---|---|---|---|
| PylonBody_L/R | 1.0×6.0×1.2 | (±5.75, 2.4, 8.55) | W Studs | rear pylons (x 5.25–6.25, y −0.6–5.4, z 7.95–9.15), flush with the side-frame ends |
| PylonBand_L/R | 1.1×0.8×1.3 | (±5.75, 3.4, 8.55) | Rainbow: left R, right V; Inlet | rainbow-end collars that echo the belt edges |
| PylonCap_L/R | 0.9×1.2×1.0 | (±5.75, 6.0, 8.55) | C Weld | crystal tops (y 5.4–6.6) |
| sparkle_pylon_L/R | 0.7 cube, on its vertex | (±5.75, 7.2, 8.55) | G Glass | twinkling finial gems (y 6.6–7.8) |
| RearSpoiler | 10.4×0.5×1.0 | (0, 3.4, 8.55) | W Weld | low spoiler bar between the collars (y 3.15–3.65); below the runner corridor and out of the runner camera's view (55° below) |

### 7. Console emblem and belt life
| Name | Size | Position | Role / variant | Purpose |
|---|---|---|---|---|
| HoodSetting | 1.4×1.4×0.2, rotZ 45° | (0, 0.48, −9.435) | O Weld | dark diamond setting on the console front (plaza eye level) |
| hood_emblem | 1.0×1.0×0.3, rotZ 45° | (0, 0.48, −9.685) | Rainbow V, Universal | violet gem; pulses white while running |
| chevron_1..6 | 0.8×0.12×0.8, rotY 45° (diamond tiles) | (±2.59, 0.32, z = −2.6 / −0.2 / 2.2) | W Universal | white diamond tiles on the orange and indigo strips; slide along the belt while running |

## Animation hooks (all client-driven, all inside Decor)
| Hook | What it does here |
|---|---|
| `halo` | the crown diamond floats ±0.18 and spins (faster while running) |
| `wing_L` / `wing_R` + `wing_root_L/R` | the crown wings flap gently when idle and hard while running |
| `rune_1..7` | the rainbow arc. Idle: full spectrum. Running: a white flash sweeps red → violet (L→R as the runner sees it, 1.2 s per sweep) while the rest dim |
| `sparkle_` ×8 | crown tips ×4, pylon finials ×2, rail-front gems ×2 (twinkle 55–110 %, phase-offset) |
| `screen_bar_1..7` | rainbow equalizer bounces above the label while running |
| `screen_gem` | sapphire on the marquee front pulses toward white |
| `hood_emblem` | violet console gem pulses toward white |
| `chevron_1..6` | diamond tiles stream along the belt |

- Not used: `flame_`, `orb_*`, `led_side_` (forced cyan), `screen_bar` (single), `belt_slat_*`, `conv_*`, `egg`.
- `rune_1..7` are created in order, so the chase order is guaranteed.

### Lights (3, all Shadows = false)
| Id | Where | Colour | Brightness | Range |
|---|---|---|---|---|
| L1 PointLight | in `halo` | 255,250,240 | 2 | 12 |
| L2 PointLight | in ArchCapital_L | 255,150,170 (warm, red side) | 1.2 | 9 |
| L3 PointLight | in ArchCapital_R | 185,160,255 (cool, violet side) | 1.2 | 9 |

The capitals are 3.3+ studs from the screen edge and the label text uses LightInfluence 0, so the label stays
readable. If a capture shows the face lightened, I'll lower L2 and L3.

## Progression (why it is the king, and how it differs from tiers 1–10)
- **Silhouette:**
  - Tallest in the lineup: the crown diamond at y ≈ 15.8, against about 8.4 for T6.
  - Widest front: a 14.6-wide arch.
  - The only build with a round arch, a crown, a spinning gem and flapping wings all together.
- **Readable at 40–60 studs:** a rainbow arch on white legs, topped by a crown. Nothing else in the game looks like
  that.
- **Palette:**
  - Unlike T1–6, it isn't one colour: white + obsidian + the full spectrum.
  - Versus T8 Frost: neutral white, a dark obsidian base and a rainbow, instead of icy blue.
  - Versus T6: white instead of gold.
  - Versus T5 and T10: no red-dominant areas.
- **Family:**
  - Same brick chassis and Studs / Inlet / Weld / Universal mix.
  - The cumulative decor is all present:
    - rails (T7)
    - arch (T8, enlarged)
    - tall console with a screen (T9)
    - fins / spoiler (T10, as wings + a rear spoiler)
    - grand front arch, corner pylons and crown (T11)
- **Life:** more animation hooks than any other tier (8 families, about 40 animated parts) plus 3 lights. The owner
  sees the arc chaser, the equalizer, the wings, the sliding diamonds and the twinkling gems while running.

## Limits: how each is respected
| Limit | How |
|---|---|
| Functional parts, attributes | untouched; `Theme = "Diamond Rainbow"`, LabelHeight 10.6 kept |
| Chassis | only Color and MaterialVariant change (Transparency stays 0) |
| Envelope \|x\| ≤ 7.4 | widest parts are the plinths (7.35) and the end voussoirs (7.30). The wings swing to at most ≈ 4.9 |
| Envelope z −11.8 to 9.3 | plinths reach −10.935; pylon collars +9.2 |
| Envelope y ≤ 16 | halo 15.75 at rest (15.93 at the float peak); wings ≤ 15.85 at full flap |
| Envelope floor | lowest parts at −0.6 |
| Sign keep-out (\|x\| > 6.4, z 4 to 8.6) | nothing there. Pylon parts stay ≤ 6.35 (the collar is 6.3). Nothing else beyond 6.4 between z 4 and 8.6 (the only parts past 6.4 are the arch at z ≈ −10). The pylons sit behind the sign line (z ≥ 7.9) and are slim, to keep the sign visible |
| Runner Zone | only chevrons (y ≤ 0.38) are over the belt; rails at \|x\| ≥ 4.79; console parts at z ≤ −7.825 |
| Runner corridor and head box | empty: rails and spoiler are below 4.5; pylon caps and gems are at \|x\| ≥ 5.15; everything tall is at z ≤ −7.8. Expected validator result: no runner WARN |
| Label screen | face M lum 0.12, opaque. No new parts with \|rx\| 14–26° at z < −6: arc, gems and wings rotate about Z or Y only, and the halo has rx 35–45°. All new parts have area far below the bracket |
| Lights | 3, Shadows off |
| Banned | no Neon, ForceField, scripts, VFX, decals, meshes or unions; Wedge only for the wings |
| Accent ≤ 15 % | 9 Glass of ~92 visible |
| Craft | every piece rests on or butts flush against another (the halo floats on purpose). No coplanar overlaps (alternating depths on the arc, 0.05 collar overhang). Symmetric except the rainbow order |

## Estimated part count
| Group | Parts |
|---|---|
| Chassis | 26 |
| Arch | 13 |
| Crown + halo | 10 |
| Wings | 4 |
| Tall console | 12 |
| Rails | 10 |
| Rear pylons + spoiler | 9 |
| Emblem | 2 |
| Chevrons | 6 |
| **Total** | **≈ 92 visible parts** (66 decor) |

That leaves about 18 parts of headroom under the 110 aim for Phase B fixes (for example, arch joint fillers).

## Open points for the reviewer
- I treat the T8 "top arch" and the T11 "grand front arch" as ONE grand arch over the console. A second arch over the
  runner would hit the head box and crowd the owner's view.
- Fins are the flapping crown wings, plus the low rear spoiler.
  - Fallback 1: static crystal side fins at x ≈ 5.8–6.2 (+2 parts).
  - Fallback 2: drop the wings if the top reads busy.
- The rear pylons may hide a sliver of the upgrade sign from a far diagonal angle behind the base. They're 1.0 wide and
  outside the keep-out; I can shorten them to y ≈ 6 if needed.
