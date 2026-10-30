# SLINGSHOT treadmills x12–x20: builder brief (2026-10-12)

## What the owner asked
- "Make more treadmills models, similiar to current ones, make 5 more, so they can upgrade more and see bigger
  differences."
- "use subagents, with reviewers and approved plans, so we can get this ON POINT PERFECT."

## Approved design (the owner approved it; do not change names, rates or themes)
| Tier | Model name | TierName | Speed/s | Theme (owner-approved) | Decor step (cumulative) |
|---|---|---|---|---|---|
| 7 | `Tier7_x12` | x12 | 600K | **Emerald** | side rails |
| 8 | `Tier8_x14` | x14 | 700K | **Frost** (ice + glass accents) | + top arch |
| 9 | `Tier9_x16` | x16 | 800K | **Galaxy** (purple) | + tall console with a screen |
| 10 | `Tier10_x18` | x18 | 900K | **Inferno** (crimson + molten) | + side fins / spoiler |
| 11 | `Tier11_x20` | x20 | 1M | **Diamond Rainbow** | + arch + pylons + crown |

- **Prices:** $2T / $8T / $25T / $75T / $200T, money only. The orchestrator wires them into ShopConfig; you build the
  models only.
- **Bigger differences:** every tier must look clearly MORE impressive than the one before (silhouette, height, richer
  palette, more animated life), while still reading as the same family as tiers 1–6.
- **Hard limits win over the decor list.** When a step in the decor list clashes with a limit, keep the idea and move
  it. Examples: an arch over the runner's camera goes over the console at the front; side rails by the upgrade sign
  stay low and inside |x| ≤ 6.4.

## Where everything is
- **Roblox Studio MCP**, `studio_id = 7d424377-a99d-4b9c-aeaa-17ba7c0f40b2`, `execute_luau` with
  `datamodel_type = "Edit"` only.
  - NEVER start Play (`start_stop_play`).
  - NEVER edit scripts, `Workspace.Map`, `HalloweenDecor`, `ReplicatedStorage`, other tiers' templates, or other bays.
- **Your template (the source of truth):** `game.ServerStorage.Assets.Treadmills.Tier<N>_x<M>`.
  - It starts as a clean copy of `Tier6_x10`: the 26-part chassis, the 5 functional parts, and an empty Model `Decor`.
- **The lab:** `workspace._TreadmillLab.Bays.Bay<N>` holds a copy of every tier 1–11, side by side.
  - It also has a scale dummy (R15) standing on the belt and two copies of the hub upgrade sign.
  - Never edit the lab copy. Edit the template, then call `T.refresh(N)`.
- **Tools:** `local T = require(game.ServerStorage._TreadLabTools)`
  - `T.refresh(N)`: re-clones your template into its bay, puts a mock "+600K / sec" label on the screen face, and
    returns `T.validate(N)`.
  - `T.validate(N)`: the automatic check. Report lines are FAIL / WARN / ok.
  - `T.cams(N)`: camera presets (`spawn`, `hub34`, `eye`, `side`, `runner`, `rear34`, `close`, `lineup`).
  - `T.reset(N)`: start over from the Tier6 chassis.
- **Captures:** use the `screen_capture` tool with the `camera_position` / `look_at_position` from `T.cams(N)`.
  - **Captures must take turns.** Five agents share ONE Studio camera, and parallel captures came back swapped (a
    "bay 6" image showed bay 5).
  - Run `require(game.ServerStorage._TreadLabTools).lock("T<N>")` in `execute_luau` before capturing. It waits up to
    about 25 s and returns `true`; call it again if it returns false.
  - Then make your captures, ONE AT A TIME (never two `screen_capture` calls in the same message).
  - Then ALWAYS run `T.unlock("T<N>")`. Don't hold the lock while you think or build.
  - Use a unique `capture_id`, e.g. `T9_hub34_v2`.
  - The `side` preset now sits in the gap between bays. There's also a new `sideHi` preset.
  - If a capture comes back plain white, Studio got minimized. Say so in your message and stop capturing; don't try
    to fix it.
- **Lab layout:** bays 1–11 run along +X from x = 490, 22 studs apart, at z = −100, floor top y = 0.
  - Every treadmill's front (console) faces −Z.
  - Seen from the front, higher tiers are to the LEFT.
- **Study tiers 1–6 in bays 1–6 before planning.**
- **Your folder:** `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Treadmills\T<N>_<Theme>\` (PLAN.md,
  BUILD_NOTES.md).

## Coordinates (belt space)
Positions are relative to the template's Belt: `m.Belt.CFrame * CFrame.new(x, y, z)`.
- **Origin:** the belt centre, 0.6 above the floor, so floor level is y = −0.6.
- **Axes:**
  - −Z = front (the console).
  - +X = the runner's right.
  - +Y = up.
- **The runner** (the owner) is welded standing on the belt at z ≈ −1, facing −Z.
  - Their camera sits behind them, at about (0, 9, 12.5).
- **Chassis (Tier6_x10):**
  - 7 belt strips (1.3 × 0.9 × 16.3) at x = 0, ±1.3, ±2.6, ±3.9.
  - Side frames 1.6 × 1.5 × 15.6 at x ±4.9.
  - Base plate 12.7 × 0.6 × 15.4.
  - Front console bar 14.3 × 2.2 × 1.7 at z −8.5.
  - Upper console bar 9.1 × 1.5 × 1.7 at (0, 3.8, −8.2), with handles at x ±5.2.
  - Tilted screen pair at z ≈ −9: a 6.5 × 3.5 frame and a 6.1 × 3.1 face, plus a 2.2 × 2.9 bracket under it.
  - Two front side feet at x ±6.3, z −6.4.

## Style: "similar to current ones"
- **Brick-built, LEGO-like:**
  - Use Part blocks, like tiers 1–6.
  - Wedge, CornerWedge, Cylinder and Ball parts are fine where they read as real brick pieces.
  - Material Plastic with a MaterialVariant from `Studs`, `Inlet`, `Universal`, `Weld`. See how tiers 1–6 mix them.
  - The validator warns on SmoothPlastic and on Plastic without a variant.
- **Chassis:** the 26 Tier6 chassis parts are FIXED in size and position. You choose each one's Color and
  MaterialVariant. They keep their collision.
- **Decor:** every new part goes inside the Model `Decor`, with:
  - `Anchored = true`
  - `CanCollide = false`, `CanTouch = false`, `CanQuery = false`
- **Craft:**
  - Flush, aligned bricks with clean sizes.
  - No z-fighting (coplanar faces overlapping).
  - No floating bits, no random gaps.
  - Nothing clipping awkwardly through the chassis.
  - Symmetric where a real build would be.
- **Colour:**
  - A bold, saturated, readable palette: 2–4 theme colours plus a dark frame colour.
  - The silhouette must read at 40–60 studs.
  - Each tier must be instantly distinct from tiers 1–6:
    - T1 is cyan/blue, T2 orange, T3 pink, T4 matte grass-green, T5 red/black, T6 gold/black.
    - **Emerald** must read as a jewel-green gem build (not T4's grass green).
    - **Inferno** must read molten orange / crimson with lava (not T5's plain red).
- **Accents:**
  - Glass, Foil, Ice, DiamondPlate, Metal etc. may make up at most 15 % of the visible parts.
  - Translucent bricks (Plastic + variant, Transparency 0.2–0.45) are good for ice and crystal.
- **Banned (owner rules):**
  - Neon and ForceField.
  - Scripts, ParticleEmitter, Beam, Trail, Fire, Smoke, Sparkles. All VFX must come from the VFX Studio plugin, and
    this job is part-built only.
  - Decals and Textures. No new asset uploads.
  - MeshParts and Unions.
- **Lights:** at most 3 PointLight / SpotLight / SurfaceLight per model, with Shadows off.
- **Theme attribute:** set `m:SetAttribute("Theme", "<Theme>")`.

## Hard limits (`T.validate` checks these; finish with 0 FAIL)
- **Functional parts:** Conveyor, Belt (PrimaryPart), Zone, Blocker and FrontStop stay EXACTLY as they are.
- **Attributes:**
  - Name, Tier, TierName and SpeedPerSecond as in the table above.
  - Keep `LabelHeight` = 10.6.
- **Envelope:** every visible part fits inside |x| ≤ 7.4, −11.8 ≤ z ≤ 9.3, y ≤ 16, and stays above the floor.
  - At the hub, a path lamp stands at x ≈ 7.7–9.1, z ≈ −6.8.
  - The base and its fence start beyond z ≈ +14.
- **Upgrade-sign keep-out:** nothing at |x| > 6.4 for 4 ≤ z ≤ 8.6.
  - The upgrade sign stands there, on −X at bases 1–2 and on +X at base 3. The lab shows both copies.
  - Players walk up to the sign to buy, so don't hide it.
- **Runner Zone:** nothing inside |x| ≤ 3.1, 0.6 ≤ y ≤ 6.6, |z| ≤ 7.1. That's where the runner stands.
- **Runner camera** (WARN; justify it with the `runner` capture):
  - Keep the corridor behind the runner clear: |x| ≤ 5, y ≥ 4.5, z ≥ 1.5.
  - Keep the space over their head clear.
  - The owner looks at their treadmill this way for hours.
- **Label screen:**
  - The "+600K 👟 / sec" label is a SurfaceGui on the screen FACE. The client picks the smaller of the two
    20°-tilted panels at z < −6. The label faces the runner.
  - Keep that face dark or deep-coloured (luminance ≤ 0.45) so the yellow text reads.
  - Keep it opaque (Transparency ≤ 0.2).
  - Do NOT add other ~20°-tilted parts at z < −6 bigger than the bracket; the client could put the label on them.
- **Size:** at most 110 visible parts (the validator FAILs at 140).

## Hub context
- Each base has its own treadmill in front of it, with the console toward the central plaza.
- Players spawn about 24 studs in front of the middle treadmill and walk past all three.
- Bases 1 and 3 are turned ±45°, so the models are seen from many angles.
- A buy shoots a sparkle burst and swaps the model in place.

## Animation hooks: free motion by part NAME
`TreadmillClient` animates these parts on every client. They move a bit when idle and a lot while the owner runs.
- Keep them Anchored, inside `Decor`.
- The client moves them with CFrame relative to the Belt every frame.

| Name | What the client does |
|---|---|
| `flame_<anything>` | height flickers up from its bottom (fire tongues, lava spurts) |
| `sparkle_<anything>` | size twinkles 55–110 % (star / gem glints) |
| `rune_<number>` | while running, each flashes white in turn (light chasers); the others dim a bit |
| `halo` (one part) | floats ±0.18 studs and spins around its own vertical axis (crown ring, rotating gem) |
| `wing_L`, `wing_R` (+ optional pivot parts `wing_root_L/_R`) | flap around Z, harder while running (fins, wings) |
| `screen_gem`, `hood_emblem`, `skull_eyes`, `belt_cracks` (one part each) | colour pulses toward white while running |
| `screen_bar_<n>` | equalizer bars bounce in height while running (never on the label face) |
| `screen_bar` (one part) | a charge-up bar fills from one side while running |
| `chevron_<n>` | slides along the belt between z −3.8 and 3.4 and loops (belt arrows) |
| `orb_core`, `orb_ring_a/_b`, `orb_shard_0..2` | floating orb, spinning rings, orbiting shards (the old "Cursed" tier) |
| `led_side_<n>` | forced to CYAN (and blink white while running): only if cyan is wanted |
| AVOID: `belt_slat_*`, `conv_*`, `egg`, `eye_iris`, `skull_jaw` | belt internals and old special cases |

Name every other part plainly, by role (`RailPost`, `ArchBar` ...). Higher tiers should have more of this life.

## Process
**Phase A, PLAN (no Studio edits; only reads, `T.validate`, `T.cams` and captures).**
1. Study this brief, bays 1–6 and your bay.
2. Write `PLAN.md` in your folder:
   - **Concept:** one line.
   - **Palette:** exact RGB per role, plus the MaterialVariant per role.
   - **Chassis recolour map:** which chassis part gets which role.
   - **Decor list:** one line per piece or symmetric pair: name, size, belt-space position, colour role, variant,
     purpose.
   - **Animation hooks and lights.**
   - **Progression:** how it clearly beats the previous tier and differs from tiers 1–6.
   - **Limits:** how every hard limit is respected.
   - **Estimated part count.**
3. Then STOP and return a short summary. A plan reviewer approves plans before anything is built.

**Phase B, BUILD (only after an "approved" message).**
- Build it exactly as approved. Small improvements you find on the way are fine; list them.
- Run `T.refresh(N)` after each step and capture all the presets: `spawn`, `hub34`, `eye`, `side`, `runner`,
  `rear34`, `close`, `lineup`. Look at every capture critically.
- Iterate until there are 0 FAIL, every WARN is justified, and it looks great.
- Write `BUILD_NOTES.md`: what you built, the final validator output, the capture ids, and anything unsure.
- Return a summary.

**Phase C, FIX.** An independent visual reviewer writes `REVIEW.md` in your folder. Fix every point, re-validate,
recapture, and append to `BUILD_NOTES.md`.

**Stay in your lane.** Touch only your own template and your own bay refresh. When the brief blocks you, say so in
your message instead of working around it.
