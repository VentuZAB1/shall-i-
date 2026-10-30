# Halloween HUB GRIME (cracks, moss, damp) - binding brief for the builder + reviewer agents (2026-10-13)

**Read `Halloween\AGENT_BRIEF.md` first: its rules apply.**
- Headless Blender 5.2 and/or Python (numpy / PIL) only.
- No Studio, no GUI Blender MCP.
- No downloads: everything procedural.
- `hkit.py` is read-only.
- Work in your own folder `Halloween\HubGrime\`.

## The owner's request (their words)
"Also in the hub make the ground/walls little be mushy, with cracks etc too feel halloween vibe yk?"

Interpretation the lead gave the owner:
- mossy, grimy, weathered;
- cracks in the ground and walls;
- moss creeping up from the bottom of the walls;
- dark damp stains;
- a few slime drips.

All of it goes ON TOP of the existing studded surfaces, so the stud style stays. The owner will see a test patch
before it is rolled out everywhere.

## What the surfaces are (Roblox, you don't touch Studio)
- **Floor:**
  - green studded plastic, RGB (128,170,96), a huge flat area (160 x 170 studs + side pieces);
  - a cream plaza circle (r 25) and cream paths (8 studs wide), RGB (222,205,170), studded;
  - brown path edges (150,118,88).
- **Walls:**
  - blue studded plastic (96,132,170), 24 studs tall (the front diagonals 48), 6 thick;
  - a darker blue top trim (69,95,132) at 22.9-24.5.
  - The walls already carry Halloween garlands (3.5 below the top), cobweb models and vines, so keep wall decals mostly
    in the lower half and in bays between them.
- **Studs:** classic Roblox studs, 1 per stud, Plastic material. Decals sit on a thin transparent carrier part 0.03-0.05
  above the surface. Transparent pixels show the studs, and opaque pixels hide them. A decal stretches to the carrier's
  face size: you give each texture its intended size in studs, and the lead sizes the carrier.
- The lighting is warm, sunny and a little hazy. There is also a NIGHT mode (dark blue, colours kept). Decals are lit
  like the surface.

## Style bar
- Stylized-realistic, matching the HQ Halloween props (`Halloween\review_head_front.png`,
  `Halloween\Graveyard\` renders, the TP trees). A spooky-fun "abandoned Halloween town square", NOT photographic
  grunge, NOT noisy dirt everywhere, NOT a flat cartoon either.
- Crisp, readable shapes from 20-60 studs:
  - **cracks** with a dark core, a slightly lighter chipped rim (a fake bevel highlight on one side, light from above),
    small branching, a few chipped fragments, and a bit of moss/dead grass growing in some cracks;
  - **moss** as soft clumpy cushions (olive / deep green with yellow-green tips, a little darker underneath);
  - **damp stains** as low-opacity dark watermarks;
  - **slime** as a stylized glossy lime-green with highlights. It is the playful accent; use it sparingly.
- Colours must read on BOTH the green floor and the blue walls. Prefer darks that are tinted (deep brown-green), not
  pure black or grey.

## Texture set (PNG RGBA, straight alpha, ≤ 1024 px per side, power-of-two not required; names fixed)
Into `Halloween\HubGrime\decals\`:

| Name | Use | Intended size (studs) |
|---|---|---|
| `G_Crack_A`, `G_Crack_B`, `G_Crack_C` | floor cracks (different shapes: long branching, star burst, split with chunks) | 8-14 |
| `G_Moss_A`, `G_Moss_B` | mossy damp patches on the floor | 6-10 |
| `G_Stain_A`, `G_Stain_B` | dark damp / mud stains, soft edges | 8-12 |
| `G_Slime_A` | a small slime puddle (accent) | 4-6 |
| `W_Crack_A`, `W_Crack_B`, `W_Crack_C` | wall cracks (vertical / diagonal, one from the floor up) | 6-12 tall |
| `W_MossBase_A`, `W_MossBase_B` | moss + damp creeping up from the wall base, **seamless left-right** so strips can be chained, fading upwards | 24 wide x 5-7 tall |
| `W_Drip_A`, `W_Drip_B` | dark damp streaks / slime drips running down from the top trim | 3-5 wide x 8-12 tall |

## Deliverables
1. `PLAN.md` FIRST, then STOP and wait for approval. It covers:
   - the technique (Blender procedural shaders baked to images, or numpy);
   - the palette (RGB);
   - per texture: the shape idea, size, pixel size and alpha strategy;
   - how you'll preview them on a studded mock surface.
2. After approval:
   - the PNGs;
   - the generator script(s) (re-runnable);
   - `NOTES.md`, with per texture: the intended size in studs, the pixel size, where it goes, and a suggested count +
     spacing for the whole hub (for example "floor: 1 crack per ~250 st², avoid within 6 studs of the spawn (0,-22)";
     "MossBase along every wall bottom with gaps");
   - **preview renders** of a studded mock:
     - a 40 x 24 green studded floor patch and a 40 x 24 blue studded wall section (studs modelled or a stud normal
       texture, sunny key light), carrying a realistic mix of the decals;
     - seen from 25 studs at player eye height (5 studs up, 70° FOV) and from 60 studs;
     - plus a night version (dark blue ambient).

## Review
An independent visual reviewer writes `REVIEW.md`: **PASS** or **FIX** with a numbered list. Its checks:
- the Halloween read;
- not noisy / not photo-grunge / not flat;
- edges clean (no halo, no white or black fringes from premultiplied alpha);
- the MossBase strips are seamless;
- the textures read on both the green and the blue;
- scale vs studs;
- whether the files exist with alpha.

The builder fixes every item (the NICE items too). At most 2 rounds.
