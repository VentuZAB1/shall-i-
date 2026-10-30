REVISE - 6/10 vs the references (round 1). The gorilla build and the face work. It still reads as grey stone crates with
orange stickers, not a lava golem: orange is only 1-5 % of every view, and the back is a blank slab.

MUST FIX (most important first):
1. No magma core shows (T4 = armour over core, as in ref_17). Let the core glow between the rock masses:
   - Pelvis (line 62): DARK -> MAGMA, density 0.62 -> 0.45. It shows as a molten waist in the front, side and back views.
   - Shins (line 141): BASALT -> MAGMA, density 0.45. Keep the TOPS knee plate (line 142), the thigh crack and the dark
     feet, so the legs read rock thigh / magma shin / stone foot, as on the Boar and in ref_17.
2. The back is what players see most, and it is a flat dark slab with one centred zigzag. That crack rejects plates down
   the whole middle, so the face is nearly bare. Give the back the "living volcano" signature:
   - A vent cone on the upper back: B.add((0, 0.36, 1.66), (0.22, 0.17, 0.18), BASALT, "Chest", top=(0.55, 0.55),
     density=D), with a flush MAGMA crater (0.11, 0.08, 0.012) on top and 2 MAGMA drip bars (w 0.06, 0.18 long) down
     its back face. The embers/smoke VFX emit from here. Check that the head-back roar (Head -18°) clears it.
   - Move the back fissure (lines 97-99) to x ≈ +0.25, starting at the vent base, so plates can fill the left half
     (target: >= 6 plates on the back face).
3. The magma heart reads as a lit 4-pane window in a signpost frame (the "TV" chest the bible bans). Make it a pit in the
   rock. Frame bars (line 84): TOPS -> BASALT, width 0.075 -> 0.09, thick 0.035 -> 0.06, offset 0.185 -> 0.20 (a rock lip).
   Replace the 4 equal MAGMA_Y squares (lines 76-78) with one MAGMA_Y diamond (0.075, 0.075, 0.016) in the centre plus
   2 MAGMA_Y 1x1 plates (0.03) at Rd @ (0.10, -0.05, 0) and Rd @ (-0.06, 0.10, 0). Orange diamond 0.13 -> 0.15.
4. The fists read as plated crates with 4 buttons on top. Fingers (line 136): half (0.065, 0.06, 0.075) -> (0.062, 0.06,
   0.15) at fc + (dx, -0.30, -0.02), so 4 BASALT fingers cover the full front face with gaps between them. Add a thumb:
   B.add(fc + Vector((-s*0.335, -0.14, 0.04)), (0.065, 0.10, 0.075), BASALT, "Hand_" + side, studs=[], role="limb").
   Lower the fist density from 0.62 to 0.40.
5. Re-render the pose sheet. _pose_tq_sheet.png (20:34) is older than this model (21:08), so these clips were not checked.

KEEP:
- The gorilla silhouette: huge shoulders, fists hanging to the ground, short pillar legs, head sunk between the shoulders.
- The face: heavy V brow shelf, ember eyes with light rims, an underbite with 4 square teeth, the orange mouth line.
- The spiked shoulder boulders with orange tips, and the light TOPS shoulders and fists against the darker BASALT body.
