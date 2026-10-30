# Halloween STREET LAMPS - binding brief for the builder + reviewer agents (2026-10-13)

**Read `Halloween\AGENT_BRIEF.md` first. Every rule there applies:**
- headless Blender 5.2 only; no Studio, no GUI Blender MCP;
- no Neon or emissive;
- no downloads;
- the kit `hkit.py` and `pumpkin.py` / `PumpkinEggs\eggs.py` are read-only (copy helpers into your own script);
- work in your own folder `Halloween\StreetLamps\`;
- FBX to `C:\cdimp\`;
- the quality bar, triangle limits, Roblox axes, NOTES.md plus review renders.

## The owner's request (their words)
"Let's make a new street lights, and remove those small ugly ones, make them tall this time, and not lowpoly, and make
them halloween themed."

The owner then picked from three styles: **"Pumpkin lantern post"**. It is ONE design, used at 8 spots.

## Approved design (what the owner said yes to)
- **Height about 18 studs** (a player is about 5; the hub walls are 24).
- A **black wrought-iron post**:
  - an ornate stepped base with small claw feet;
  - a fluted pole with a twisted section;
  - a curled **shepherd's-crook arm** at the top with a small **iron bat ornament** (wings spread) on the arm or the crook.
- **Lamp:** hanging from the arm tip on a **short chain** (3-5 links) is an **iron cage**:
  - 4-6 curved bars and a top cap with a spike finial;
  - inside it, a **carved jack-o'-lantern** with triangle eyes and a toothy grin.
  - The face is cut all the way through; reuse the pumpkin-egg carving approach in `PumpkinEggs\eggs.py`.
  - The face looks along the arm direction (outwards from the post), so players walking the path see it.
- A **cobweb** in the crook of the arm. Use real strands plus a separate silk part with an RGBA texture, as in
  `WebsSpiders\NOTES.md`.
- **Not low poly:**
  - smooth curves (no faceting on the pole, crook, cage bars or pumpkin);
  - real iron detail: rivets, collars, scroll ends;
  - baked normal + AO + colour + roughness.
- **Iron:** near-black with a cool tint (not pure black), slight edge wear and a hint of rust in the crevices.
- **Pumpkin:** rich orange, with ribs.
- Stylized-realistic HQ, matching the giant head (`Halloween\review_head_front.png`) and the pumpkin eggs
  (`PumpkinEggs\review_day_25studs.png`). A spooky-fun Halloween street, not grim horror, and never cute.

## What it replaces (context only, you don't touch Studio)
The current lamps are about 10-stud black boxes with a Neon yellow box. There are 8 of them:
- 6 along the hub's cream plaza paths;
- 2 at the wooden market deck.

The hub is a bright, saturated, sunny Roblox simulator: a green studded floor, blue studded walls 24 tall, and Halloween
decor everywhere (a giant jack-o'-lantern head, garlands, webs, TP trees). Players also have a NIGHT setting (dark
blue starry sky, map colours kept), so the lamps must look great both in sunny day and at night lit from inside.

## Lighting (the lead sets it up in Studio; you only model)
- The lead adds, inside the pumpkin, a warm PointLight (Flicker attribute) and a small flame flipbook on a candle you
  model. The flipbook is the existing `Halloween\vfx\CandleFlame_8x8.png`.
- So model a **short candle stub** on the pumpkin's inner floor and give its wick tip in NOTES.
- No emissive. The glow is the Studio light.
- The cage sits 0.3+ stud away from the pumpkin skin all round, so light and shadow read.
- Like the eggs, the inner wall is a scraped flesh colour.

## Budgets
- **One lamp ≤ 14,000 triangles in total, all parts.** It repeats 8 times in the hub.
- Split it into named objects (each becomes a MeshParts):
  - `Post` (base + pole + crook + bat);
  - `Cage` (cage + chain + cap);
  - `Pumpkin` (carved pumpkin + stem + candle);
  - `Web` (strands);
  - `WebSilk` (RGBA silk).
- Each object ≤ 8,000 triangles.
- Textures: `Post` 1024; `Cage` 512; `Pumpkin` 1024; `Web`/`WebSilk` 512.
- The FBX embeds them (`hkit.export_fbx`).
- The output is **ONE FBX** at `C:\cdimp\Halloween_StreetLamp.fbx` that holds all the objects.

## Pivot / orientation
- **FBX origin = the ground contact point** at the centre of the base (Z = 0). Nothing goes below Z = 0 by more than
  0.05.
- **The arm reaches towards Blender -Y.** The pumpkin face also looks towards -Y. Remember the importer maps Blender +Y
  to Roblox +Z, so the lead will turn it as needed. Just be consistent and state it in NOTES.
- The hanging cage + pumpkin bottom is about 12-13 studs above the ground, so players walk under it without hitting
  it. The arm reaches about 3-4 studs out from the pole axis.
- The footprint of the base is ≤ 2.6 x 2.6 studs (it stands at the edge of 8-stud-wide paths).

## Deliverables
- `PLAN.md` (**FIRST, then STOP and wait for approval**):
  - a palette with linear-ish RGB per material;
  - a part list with sizes in studs and a triangle budget per part;
  - the build steps;
  - how you'll carve the face and cut the web;
  - the review camera list.
- After approval:
  - build script(s) + `.blend` in your folder;
  - the FBX;
  - `NOTES.md` with:
    - per-object size, tris and texture size;
    - the axes;
    - **attachment points in Blender object space**: candle wick tip, pumpkin cavity centre, a suggested PointLight
      position (low inside, as the eggs NOTES explain), and the chain top;
    - any Studio setup (which parts need SurfaceAppearance AlphaMode Transparency).
- Review renders on `review_setup` (sky background, green ground plane, sunny key):
  - from 25 studs at player eye height (5 studs up, 70° FOV);
  - from 50 studs;
  - a close-up of the lamp head;
  - a **night render**: dark blue ambient, the pumpkin lit from inside by a warm point light at your suggested
    position.

## Review process
1. A plan reviewer approves the plan.
2. The builder builds and self-reviews.
3. An independent visual reviewer writes `REVIEW.md`: **PASS** or **FIX** with a numbered list. Its checks:
   - the Halloween read from 40 studs;
   - not low poly / no faceting;
   - bake faults (dark rims, seams, stretched UVs);
   - iron that isn't flat black;
   - the pumpkin face read in day AND night;
   - the web reads;
   - proportions (tall, elegant, readable silhouette);
   - pivot at the ground;
   - budgets;
   - embedded textures.
4. The builder fixes every FIX item (and the NICE items too, the owner wants perfect). At most 2 rounds.
