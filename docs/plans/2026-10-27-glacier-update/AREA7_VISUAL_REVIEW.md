# AREA 7 VISUAL REVIEW: Frostfall Glacier (S1, closed)

Reviewer: visual reviewer, 2026-10-27. Read-only: renders, build notes, plan, owner rules. Studio not touched.
Renders: `s1_renders/g1..g7` and `_sheet.png`. The renderer is flat raycast with a fixed sun: no lighting, textures, studs, particles, eggs or UI. Judged here: layout, colour blocking, value contrast, prop placement, readability.

## Verdict: FIX
## Score: 6/10

Clean, distinct from Celestial, rules respected, nothing misaligned. But it is still a blockout: walls and floor are too close in value, the trench edge disappears at eye height, the props are too sparse to make a place, the egg is unverified, and Glacier is visible from Lv25 launch arcs, which the build notes say does not happen.

## What works
- Reads as a different zone from Celestial at a glance: pale icy blue against magenta walls and sand (g1 vs g5).
- The closed end holds: g5 shows Celestial's end wall exactly as before.
- Egg lanes are clear: nothing in |x| < 46 in g1, g2 or the top view (g7).
- VIP door frames sit flush in the walls (g3, g4). No floating or misaligned parts seen in the seven frames.
- Decor restraint follows the owner rules: no trees, bushes, seats, signs or lights.
- The trench shows as a clear dark navy band from above (g7).

## Per frame
- g1 entrance: pale slab floor, walls merge with floor at the far end; props are specks. Weakest frame.
- g2 trench: the trench is a faint seam at eye height; the rims match the floor.
- g3 right wall: VIP frames and crystal/boulder pairs read well; the grey boulder looks like a ball.
- g4 VIP: frame is clean. The foreground floor is grey-blue, not pale. Probably the renderer's shadow from the left wall; confirm in Studio that the hideout floor is not covered.
- g5 Celestial end: unchanged. Good.
- g6 arc over end: Glacier is visible past the magenta wall; the pale floor sits against the pale sky haze and reads more like a white void than ice (see M4).
- g7 top: layout reads well; the far end wall is a light band and merges with the floor.

## MUST
**M1. Walls and floor are too close in value.** Walls (165,210,240) on floor (210,240,252) is the lowest contrast of any area. In g1 and g3 the walls and floor read as one pale mass, and the far wall nearly vanishes into the sky.
- Recolour every Glacier wall part (`Area7_Glacier.Walls`: WallL_1, WallL_2, WallR and its door pieces, EndWall) to **112,168,216 (#70A8D8)**, Plastic, studs kept.
- Sills (185,222,245) to 150,196,228.
- VipHideout Back and Roof (120,190,235) to 96,150,200.
- Keep the floor (210,240,252) and the gold VIP trim unchanged.
- In the S2 lineup, check that Water (Area 2: walls 35,80,205, floor 110,195,255) still reads as a different area.

**M2. Trench rims vanish at eye height.** RimA and RimB (150,230,255) on floor (210,240,252) are nearly the same value. At eye height (g2) the gap is a faint seam, and the player can't see the drop.
- Set RimA and RimB to **40,140,215 (#288CD7)** and height 0.3 to 0.6. Keep position, CanCollide off.
- Keep TrenchBottom (25,55,100).

**M3. Too empty and too small to make a place.** 19 props (13 big, 6 small) plus 6 snow patches over about 400 studs. In g1 and g2 the floor between the entrance and the trench is a bare pale slab. The crystals are 8.5 to 10 studs but read as specks from 100+ studs away. World Building asks for about 16 small props per side per zone, 6 to 12 studs tall, hugging walls. Glacier has about 9 to 10 per side.
- Add **6 small ice-crystal clusters mounted on the wall faces**. Small decor on walls is allowed by the rules, so this adds frost identity without touching the lanes.
- Size: 3 to 4 studs tall, Glacier (120,205,255) points on snow (238,246,252) bases. Box fidelity, CastShadow off, CanCollide/CanQuery/CanTouch off, Anchored.
- Position: base at y 14 to 22, on the inner wall face (x = +59.5 right, x = -59.5 left). Keep at least 12 studs in z from every VIP door span.
- Candidate z bands (check each with the validator):
  - Right wall: z -2575, -2700, -2810.
  - Left wall: z -2510, -2745, -2850. The left wall is the VIP hideout face (VipSafe/filler at x -60), so keep to these bands.
- Do not add anything at |x| < 46 or on the floor in the lanes.

**M4. Owner decision: Glacier is visible from Lv25 launch arcs (g6).** The build notes say "nothing changes for players". That is not true from the arc: at Lv25 (apex about y 598) the pale floor and walls show past Celestial's magenta end wall. The pale floor against the sky haze reads as a white void, not an ice field.
- Recommended: hide it until S2 by parenting `Area7_Glacier` to ServerStorage. The step is reversible (parent it back).
- Confirm that the S2 opener in `S2_OPEN_CHECKLIST.md` moves the folder back to `workspace.Map.Runway`. If it does not, add that step.
- If the owner prefers a teaser, say so and accept the white-void look. Owner decides, not this review.

**M5. Gate before S2: render the GlacierEgg.** No egg is in any render, so "will eggs stand out?" is unanswered. On paper the body (sapphire 30,70,160) on the floor (210,240,252) is a strong dark-on-pale contrast. The ice-cyan band (120,220,255) is pale, so it reads only against the dark body, not the floor.
- Render the egg at real scale on FloorA at x 0 and x ±40, at eye height and top-down, with the sizing shell.
- Check that the two Frost speckles (Neon, copied from Celestial's Star parts) read as frost, not glow.

## NICE
- **N1. Boulders read as grey balls** (g1 right, g3 centre). Tint the frozen boulders to about 200,222,236 and sink 1 stud into the floor so they sit down. Or swap one of the two rock meshes.
- **N2. Snow patches** (g1, g3) read as white strips against the pale floor. Acceptable as they are; they may merge with the floor under real lighting.
- **N3. Glacier material on wall caps only** (not on floors) for a frost sheen. Walls are not walked on, so the friction rule does not apply. Keep only if it looks right in a Studio render.
- **N4. Banner length.** "Frostfall Glacier" (20 characters with the emoji) cannot be judged from these renders. Check the phone emulator in S2. The plan's fallback is "Glacier" alone.

## Owner rules check
- Decor sides only, sparse: pass. M3 adds 6 small wall props and stays inside the rule.
- No trees, bushes, seats, signs or lights: pass.
- Lanes |x| < 46 clear: pass.
- Small VFX only, no global lighting change: not judged here (no particles or lighting in renders). Nothing in the build notes suggests a lighting edit.
- Polish bar (front-page games): not yet. It is a blockout; M1 to M3 are the main gap.

## Not judged (renderer limits)
Lighting and shadows, studs, materials, the egg, particles, the banner, the phone UI and real camera framing. The renderer's fixed sun leaves the left side in shadow, so M1 is judged on the lit right wall and the floor.
