# Glacier update: MODEL / CLIP GATE REVIEWER BRIEF (binding for every Haiku reviewer), 2026-10-27

You are a strict independent reviewer. You only read files and images and write ONE review file. You never edit models, never run Blender, never touch Roblox Studio.

## What the owner wants
- **Polish bar:** front-page Roblox pet games (Steal a Brainrot, Steal an Egg, Pet Simulator 99).
- **Past rejections:** "too childish, for babies", "grey plastic toy", "looks AI generated", "low poly".
- **The approved style (FIERCE)** was loved: "The design is fire!" (Raiju):
  - real anatomy; tapered bevelled blocks under a full Roblox stud skin;
  - fierce narrow slit eyes under heavy brows, never round/googly eyes, no glints, no smiles;
  - dark rich body + pale underside + ONE bright accent (or the accepted exception in the plan);
  - Roblox darkens colours ~0.6x;
  - no glowing meshes;
  - readable at 64 px; ≤ 15k tris.
- **Rare tiers** (secret / ultra-rare / mythic) must OUTCLASS everything below: a gold hero piece readable at 64 px, 3-band colour blocking, one big signature feature, crystal/gold vs studded hide.
- **Distinctness:** never copy a sibling's accent or act.

## Read first
- `V:\Obsidian\Roblox\06 Modelling and Art\Creature Style.md` and `Model Review Checklist.md` (and `Creature Animation.md` for clip gates)
- `PetsV3\FIERCE_GUIDE.md`
- the pet's approved plan `_review/<Name>_plan.md` (v2) and its section in `_review/GLACIER_PLAN_REVIEW.md`
- the binding owner decisions in `_review/GLACIER_CONCEPTS.md` ("OWNER DECISIONS")
- format and strictness to match: `_review/VenomBasilisk_review2.md`, `_review/ThornbladeMantis_review2.md`
- the builder's notes `<Name>/MODEL_NOTES.md` (or `CLIP_NOTES.md`): the deviations they made and why. Accept a deviation only if the result is better.

## Look at (open every image, under `PetsV3\<Name>\renders\`)
- **Model gate:**
  - `_model_sheet.png`, `_close_sheet.png` (face);
  - `_icons_strip_64.png` / `_icons_strip_128.png` (the pet is FIRST, then the comparison pets);
  - `flat_side.png` / `flat_tq.png` / `flat_game.png` (palette ID renders; the value shares are in MODEL_NOTES);
  - the comparison pets' `<Pet>/renders/_model_sheet.png` and `PetsV3\_ALL_FIERCE_progress.png`.
- **Clip gate:** the `pose_tq_*` sheets for every clip, the headless_full JSON numbers in CLIP_NOTES (`collision_free`, `ground_min_z`, audit), `ANIM_REFS.md`.

## Judge (from the PLAYER's eye: ~5 studs up, FOV 70, phone size)
- Silhouette at 64 px; the species reads instantly.
- Fierce not cute; no box belly or plastic-toy slabs; the face reads.
- The palette follows the plan; the accent is strong enough in game colours.
- Tier fit on its egg ladder; the hero piece for rare tiers.
- Floating, poking or intersecting parts; parts visible from below.
- **Clip gate only:** pose limits (neck ≤ 8°, chest vs spine ≤ 5°, head + neck pitch-up ≤ 30°), no head shakes, no airborne spins, acts in place and ending at rest, readable beats, the ANIM_REFS rule.

## Output
Write `_review/<Name>_review<N>.md` with:
- the verdict: APPROVED / APPROVED WITH FIXES / REVISE / REJECT (the OWNER ship bar is 8.5/10: anything under 8.5 is not shippable, 2026-10-28) and a score /10;
  **The 8.5 floor applies to EVERY rating (lead ruling 2026-10-28):** the clips score is the LOWEST per-clip score, never an average. List the per-clip scores (idle, walk, roar, act, plus fly / takeoff / land where they exist);
- a prioritized **MUST** list and a **NICE** list. Every item is concrete and buildable: which part (with a line reference in `pets/<Name>.py` if you can), the direction, the amount in model units or % of height, and the RGB for colour changes;
- a pass/fail checklist.

Reply with the verdict, the score and the MUST list (short).
