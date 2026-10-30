# Tier10_x18 INFERNO: plan (Phase A, 2026-10-12)

Template `ServerStorage.Assets.Treadmills.Tier10_x18`, lab `workspace._TreadmillLab.Bays.Bay10` (belt centre 688, 0.6, -100).
Attributes stay: Name `Tier10_x18`, Tier 10, TierName `x18`, SpeedPerSecond 900000, LabelHeight 10.6. New: `Theme = "Inferno"`.
Baseline `T.validate(10)`: 0 FAIL, 1 WARN (gold label face, lum 0.78). The plan fixes it with a basalt face.

## 1. Concept
A volcano-forged hot-rod. A basalt **lava gate** with a flame crown and a crimson **volcano console** at the front.
**Lava-channel rails** with chasing ember runes and flexing crimson **tail fins** on the sides. A low **rear spoiler**
with flame stacks and exhausts. The belt is a molten river: yellow core, orange, crimson, then a black crust.

## 2. Palette (4 colours, all Plastic + MaterialVariant)
| Role | RGB | Variants (where) | Share (approx.) |
|---|---|---|---|
| BASALT (dark frame, warm near-black) | (30, 22, 24) | Studs (structure), Inlet (outer belt strips), Universal (label face) | ~40 % |
| CRIMSON (armour) | (196, 20, 40) | Studs (armour, fins, rails, spoiler), Weld (legs, feet) | ~30 % |
| LAVA (molten orange) | (255, 100, 0) | Inlet (veins, runes, seams, flames, strips), Weld (base plate, grips, bracket, console core) | ~22 % |
| MAGMA (white-hot yellow) | (255, 184, 28) | Universal (flame cores, emblem, gem), Inlet (centre belt strip, embers) | ~8 % |

- Why it isn't T5: T5 is flat pure red (151,0,0)/(181,0,0) on neutral black (17/45) with no decor.
- Inferno uses a warm basalt, a blue-leaning crimson and large molten orange/yellow areas (belt river, flames, veins).
- Its silhouette is about 1.5x taller and has a lot of motion.
- Accent materials: only the 2 exhaust pipes (Metal, BASALT colour). That is 2 of about 100, well under the 15 % cap.
- No Neon, ForceField, Glass, MeshParts, Unions, decals or effects objects.

## 3. Chassis recolour map (26 parts, colour and variant only; size, position, name and collision untouched)
| Chassis part (belt space) | Role | Variant |
|---|---|---|
| Side frames 1.6x1.47x15.56 @ x +-4.91 | BASALT | Studs |
| Belt strip x = 0 | MAGMA | Inlet |
| Belt strips x = +-1.3 | LAVA | Inlet |
| Belt strips x = +-2.59 | CRIMSON | Inlet |
| Belt strips x = +-3.89 | BASALT | Inlet |
| Base plate 12.71x0.61x15.39 (shows as a thin rim outside the frames) | LAVA ("lava seeping out") | Weld |
| Front console bar 14.27x2.16x1.73 | BASALT | Studs |
| Console legs 1.3x1.73x1.12 (x2) | CRIMSON | Weld |
| Console centre 4.19x1.73x0.69 | LAVA | Weld |
| Upper console bar 9.08x1.47x1.73 | BASALT | Studs |
| Handle boxes 1.3x1.47x2.59 (x2) | CRIMSON | Studs |
| Handle grips 1.21x1.21x1.64 (x2) | LAVA | Weld |
| Handle caps 1.3x1.47x0.61 (x2) | BASALT | Studs |
| Screen bracket 2.16x2.85x0.99 (20 deg) | LAVA (glowing stem under the screen) | Weld |
| Screen frame 6.48x3.46 (19 deg) | CRIMSON (bezel) | Studs |
| **Screen face 6.14x3.11 (20 deg, label)** | **BASALT, lum 0.09, opaque** | Universal |
| Front feet 1.25x1.21x4.58 (x2) | CRIMSON | Weld |

## 4. Decor list (all inside Model `Decor`: Anchored, CanCollide/CanTouch/CanQuery false)
- Coordinates are belt space, centre (x, y, z); size is X x Y x Z.
- "+-" means a mirrored L/R pair: the `_L` part sits at -x.
- Sub-models inside Decor: Gate, Volcano, Rails, Fins, Spoiler.
- Wedges are oriented with 90/180-degree turns only, never a ~20-degree X tilt.

### 4a. Lava gate: the arch, with a flame crown (front, z -11.6 .. -9.3)
| # | Name | Size | Centre | Colour / variant | Purpose |
|---|---|---|---|---|---|
| 2 | GatePillar_L/R | 1.4 x 8.4 x 2.0 | (+-6.435, 3.6, -10.335) | BASALT Studs | Basalt columns from the floor to y 7.8, outer face flush with the console bar end (x 7.135) |
| 2 | PillarCap_L/R | 1.4 x 1.4 x 2.0 | (+-6.435, 8.5, -10.335) | CRIMSON Studs | Crimson capital band under the lintel |
| 2 | LavaVeinLow_L/R | 0.4 x 3.0 x 0.2 | (+-6.235, 3.7, -11.435) | LAVA Inlet | Lava crack on the pillar front, lower half |
| 2 | LavaVeinHigh_L/R | 0.4 x 2.8 x 0.2 | (+-6.635, 6.4, -11.435) | LAVA Inlet | Upper half, offset 0.4 outward and overlapping 0.2, so the crack zig-zags |
| 2 | sparkle_vein_L/R | 0.4 x 0.4 x 0.4 | (+-6.435, 5.1, -11.435) | MAGMA Inlet | Ember glint on the crack joint (half embedded) |
| 2 | ArchCorbel_L/R (Wedge) | 1.4 x 1.4 x 2.0 | (+-5.035, 8.5, -10.335) | CRIMSON Studs | Full faces against the pillar and the lintel; the slope faces down and inward, giving a pointed gate opening |
| 1 | Lintel | 14.27 x 1.2 x 2.0 | (0, 9.8, -10.335) | BASALT Studs | Arch beam (same width as the console bar); 0.65 above the screen top |
| 2 | sparkle_lintel_L/R | 0.4 cube | (+-3.8, 9.8, -11.335) | MAGMA Inlet | Embers on the lintel front |
| 1 | screen_gem | 1.0 x 1.0 x 0.3, 45 deg about Z | (0, 9.8, -9.185) | MAGMA Universal | Diamond on the lintel's **runner-facing** face, right above the label |
| 1 | CraterRim | 4.0 x 0.6 x 1.6 | (0, 10.7, -10.335) | CRIMSON Studs | Crater the crown erupts from |
| 1 | flame_crown_C | 1.1 x 1.7 x 1.1, 45 deg about Y | (0, 11.85, -10.335) | LAVA Inlet | Centre tongue, base y 11.0 |
| 1 | flame_core_C | 0.5 x 2.0 x 0.5, 45 deg about Y | (0, 12.0, -10.335) | MAGMA Universal | Hot core inside it; its yellow tip flickers out above the orange |
| 2 | flame_crown_L/R | 0.8 x 1.3 x 0.8, 45 deg about Y | (+-1.3, 11.65, -10.335) | LAVA Inlet | Side tongues |
| 2 | flame_core_L/R | 0.4 x 1.6 x 0.4, 45 deg about Y | (+-1.3, 11.8, -10.335) | MAGMA Universal | Their cores |
| 2 | Brazier_L/R | 1.2 x 0.5 x 1.2 | (+-6.435, 10.65, -10.335) | CRIMSON Studs | Torch bowls on the lintel ends |
| 2 | flame_torch_L/R | 0.8 x 1.1 x 0.8, 45 deg about Y | (+-6.435, 11.45, -10.335) | LAVA Inlet | Corner torches (base y 10.9) |
| 2 | flame_torchcore_L/R | 0.4 x 1.4 x 0.4, 45 deg about Y | (+-6.435, 11.6, -10.335) | MAGMA Universal | Torch cores |

### 4b. Volcano console: the tall console (front, between the pillars)
| # | Name | Size | Centre | Colour / variant | Purpose |
|---|---|---|---|---|---|
| 1 | VolcanoBase | 11.47 x 2.16 x 2.0 | (0, 0.48, -10.335) | BASALT Studs | Front plinth; top flush with the console bar (1.56); one dark band with the pillar feet |
| 1 | VolcanoStep | 8.0 x 2.945 x 2.06 | (0, 3.0325, -10.105) | CRIMSON Studs | Crimson cone body; back flush with the upper console bar (-9.075), top flush (4.505). Clears the tilted bracket by 0.013 (OBB-checked) |
| 2 | VolcanoSlope_L/R (Wedge) | 1.735 x 2.945 x 2.06 | (+-4.8675, 3.0325, -10.105) | CRIMSON Studs | High side against the step, sloping down outward to the pillar, so the front reads as a volcano trapezoid |
| 1 | belt_cracks | 13.6 x 0.35 x 0.2 | (0, 0.475, -11.435) | LAVA Inlet | Lava seam across the whole dark front band |
| 1 | EmblemPlate | 2.0 x 2.0 x 0.15, 45 deg about Z | (0, 3.03, -11.21) | BASALT Studs | Dark diamond outline |
| 1 | hood_emblem | 1.4 x 1.4 x 0.3, 45 deg about Z | (0, 3.03, -11.435) | MAGMA Universal | Magma diamond badge on the volcano |

### 4c. Lava-channel rails, the Emerald step (on the side-frame tops, |x| 4.9..5.95)
| # | Name | Size | Centre | Colour / variant | Purpose |
|---|---|---|---|---|---|
| 6 | RailPost (3 per side) | 0.8 x 1.6 x 0.8 | (+-5.3, 1.675, z = -4.8 / 1.4 / 7.5) | BASALT Studs | Posts standing on the side frames |
| 2 | RailBeam_L/R | 0.8 x 0.6 x 13.23 | (+-5.3, 2.775, 1.335) | CRIMSON Studs | Rail from the handle grips (z -5.28) to the frame end (7.95), top y 3.075 |
| 10 | rune_1..rune_10 | 0.25 x 0.36 x 1.2 | (+-5.825, 2.775, z = -4.3 / -1.7 / 0.9 / 3.5 / 6.1) | LAVA Inlet | Ember chase lights on the beam's outer face. Created L,R,L,R... front to back, so the chase runs toward the back on both rails like the belt |

### 4d. Side fins: the new x18 step (`wing_` hooks)
| # | Name | Size | Centre | Colour / variant | Purpose |
|---|---|---|---|---|---|
| 2 | wing_root_L/R (FinSocket) | 0.8 x 0.4 x 6.78 | (+-5.3, 3.275, -1.89) | BASALT Studs | Socket on the rail (z -5.28..1.5); the flap pivot |
| 2 | wing_L/R: FinLowerWedge (Wedge) | 0.4 x 2.4 x 3.18 | (+-5.3, 4.675, -3.69) | CRIMSON Studs | Swept leading edge, rising toward the back; the tip touches the handle grip's back face |
| 2 | wing_L/R: FinBody | 0.4 x 2.4 x 3.2 | (+-5.3, 4.675, -0.5) | CRIMSON Studs | Fin body |
| 2 | wing_L/R: FinTipWedge (Wedge) | 0.4 x 2.4 x 3.2 | (+-5.3, 7.075, -0.5) | LAVA Inlet | Glowing upper fin, rising to the tip at top-rear (y 8.275, z 1.1) |
| 2 | wing_L/R: FinSpar | 0.4 x 4.8 x 0.4 | (+-5.3, 5.875, 1.3) | BASALT Studs | Dark trailing-edge spar, ends at z 1.5 |

The fin is a classic swept tail fin: a slanted leading edge (36 deg) and a vertical trailing spar.
- All 4 pieces on a side share the name `wing_L` (or `wing_R`), so the client rotates them as one rigid fin about `wing_root_*`.
- The client's code supports several parts with the same wing name. Flagging it here for the reviewer.

### 4e. Rear spoiler and exhausts (new x18 step)
| # | Name | Size | Centre | Colour / variant | Purpose |
|---|---|---|---|---|---|
| 2 | SpoilerPlate_L/R | 0.6 x 5.0 x 2.3 | (+-6.01, 1.9, 8.1) | CRIMSON Studs | End plates from the floor to y 4.4, against the side-frame outer face; x <= 6.31 (sign keep-out OK) |
| 1 | SpoilerWing | 11.42 x 0.5 x 1.25 | (0, 3.85, 8.625) | BASALT Studs | Wing between the plates, y 3.6..4.1, z 8.0..9.25 |
| 1 | skull_eyes (SpoilerLip) | 11.42 x 0.3 x 0.3 | (0, 4.25, 9.1) | LAVA Inlet | Gurney-flap tail light, top y 4.4 (< 4.5 corridor) |
| 2 | flame_spoiler_L/R | 0.5 x 1.2 x 0.5, 45 deg about Y | (+-6.01, 5.0, 8.1) | LAVA Inlet | Flame stacks on the plate tops (outside the |x| <= 5 corridor) |
| 2 | ExhaustPipe_L/R (Cylinder, axis along Z) | 0.8 long x 0.6 dia | (+-3.6, -0.17, 8.01) | BASALT **Metal** (accent) | Pipes out of the rear of the outer belt strips |
| 2 | flame_exhaust_L/R | 0.4 x 0.4 x 0.4, local Y turned to +Z | (+-3.6, -0.17, 8.61) | MAGMA Inlet | Backfire flames; they grow backward, max z 8.99 |

- The spoiler wing starts at z 8.0, so a player exiting (teleported to z 7.5) doesn't spawn inside it.
- From the runner camera only the top edge of the wing and lip shows, at the very bottom of the frame.

## 5. Animation hooks and lights
**40 animated parts.** Every one rests on a surface or is half embedded, and every hook was checked at its maximum motion.

| Hook | Parts | Effect |
|---|---|---|
| `flame_*` | **14** | Always flickering, stronger while running: crown 3 tongues + 3 cores, torches 2 + 2, spoiler stacks 2, exhausts 2 |
| `rune_1..10` | 10 | Ember chase down both rails while running |
| `sparkle_*` | 4 | Ember glints on the pillar cracks and the lintel |
| `wing_L` / `wing_R` | 4 + 4, with `wing_root_L/R` | Fins flex: +-3.4 deg idle, +-16 deg while running |
| Pulse to white-hot while running | 4 | `belt_cracks` (front seam), `hood_emblem` (volcano badge), `screen_gem` (above the label, in the owner's view), `skull_eyes` (spoiler lip) |

- Flames are rotated 45 deg about Y only, so they still grow up from their base and look 3D from every side.
- Each core sits inside its tongue and flickers on its own phase.
- Nothing animated sits on a wing; sparkles and flames don't follow wing motion.
- Lights (3, all Shadows = false):
  - `GateGlow`: PointLight in CraterRim, (255,120,30), Brightness 2, Range 16. Lights the gate, screen and runner.
  - `VolcanoGlow`: PointLight in VolcanoStep, (255,90,20), Brightness 1.5, Range 12. Lights the plaza side.
  - `SpoilerGlow`: PointLight in SpoilerWing, (255,90,20), Brightness 1.5, Range 10. Lights the rear belt and exhausts.

## 6. Progression
**Height ladder (static top / top with running flicker):**
- T6: 8.5.
- x18 gate: 10.4.
- x18 crown: 12.7 / 13.48 (tongue), 13.0 / 13.92 (core).
- Fins: 8.3.

**Over x16 Galaxy:**
- x18 keeps the same rails + arch + tall console, as one heavier "lava gate" plus a stepped volcano console.
- It adds the two new pieces: flexing tail fins and a rear spoiler with stacks and exhausts.
- It adds a 5-tongue flame crown plus 2 torches above the label.
- About 40 animated parts, with motion on every side: gate and belt seam from the plaza, fins and runes from the sides,
  spoiler and exhausts from the base side.
- Coordination note: for a clear step, Galaxy should stay at or below ~11.5 static top.

**Below x20 Diamond:**
- No pylons, no crown or halo, no rainbow.
- Static top 13.0 leaves 13 to 16 for x20's crown; x20 should top out at 14 or more.
- About 100 parts here, so x20 still has room up to 110.

**Distinct from tiers 1-6:**
- T5 is plain red/black with no decor.
- T2 is a light peach/orange; here the orange always sits in basalt and crimson, never tan.
- T6's gold appears only as small magma cores, sparks and one centre strip.

## 7. Hard limits: how each is met
All of this was verified with a pure-math Luau run against the validator's own boxes. No instances were created.

- **Functional parts:** Conveyor, Belt, Zone, Blocker and FrontStop are not touched.
- **Chassis:** the 26 chassis parts get only Color and MaterialVariant changes.
- **Envelope:** min x -7.135, max x 7.135; min z -11.635; max z 9.25; min y -0.6.
  - Max y is 13.0 static and 13.92 at peak flicker, both under 16.
- **Upgrade-sign keep-out:** inside 4 <= z <= 8.6, the widest parts are the spoiler plates (x 6.31) and the stack flames (x 6.364). Both are under 6.4.
- **Runner Zone:** nothing at |x| <= 3.1 with y >= 0.6. The rails start at x 4.9; the exhausts sit at |z| > 7.1.
- **Runner camera corridor:** 0 parts, static or animated.
  - The spoiler and lip top out at y 4.4.
  - The fins are at x >= 5.1 and end at z 1.5. Even fully flexed inward they stay at z < 1.5.
- **Over-head box:** 0 parts. The gate is at z <= -9.335; the fins are at |x| >= 5.1.
- **Label screen:** the face is BASALT (lum 0.09, opaque). No new part has a ~20 deg X tilt; the only rotations are 45 deg about Y or Z and 90-degree wedge turns. The math check flagged 0 parts.
- **Interpenetration:** nothing clips the chassis.
  - VolcanoStep clears the bracket by 0.013 and the lintel clears the screen frame by 0.65 (exact OBB test).
  - Contacts are face-to-face. Proud details (veins, runes, emblem, seam) stick out 0.2 to 0.3, so no faces are coplanar.
- **Bans:** no Neon, ForceField, scripts, ParticleEmitter, Beam, Trail, Fire, Smoke, Sparkles, Decal, Texture, MeshPart or Union.
- **Lights and accents:** 3 lights with Shadows off; 2 accent parts.

## 8. Estimated part count
| Group | Parts |
|---|---|
| Chassis | 26 |
| Gate + volcano | 36 |
| Rails | 18 |
| Fins | 10 |
| Spoiler + exhausts | 10 |
| **Total visible** | **100** (decor 74, aim <= 110) |

Animated: 40. Accents: 2. Lights: 3.

## 9. Phase B build order and notes
1. Recolour the chassis and set `Theme`.
2. Build in this order: Volcano, Gate, Crown, Rails + runes (in chase order), Fins (wedge orientation checked on capture),
   Spoiler + exhausts, lights.
3. After each step: `T.refresh(10)` and all 8 presets.
4. Check the rune and flame order with GetDescendants on the refreshed bay.

The `side` preset puts the camera 4 studs inside Bay 9, next to its dummy.
- I'll keep the official preset.
- I'll also capture a clean profile from (676.5, 6.6, -101), looking at (688, 4.6, -101), between the bays.

Captures studied in Phase A:
- `T10A_lab_bays1to6_front`
- `T10A_T6_hub34`, `T10A_T5_hub34_b`, `T10A_T6_runner`, `T10A_T6_rear34`
- `T10A_T1T2_rear34`, `T10A_T3T4_rear34`
- `T10A_bay10_spawn`, `T10A_bay10_side`, `T10A_bay10_side_clear`, `T10A_bay10_runner`, `T10A_bay10_lineup`, `T10A_bay10_close`
