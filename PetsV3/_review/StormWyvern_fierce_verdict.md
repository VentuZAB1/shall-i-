REVISE 7/10 - the strongest silhouette of this batch. The crest skull, spread bat wings with red-sprite zigzags and long blade tail read as a storm
wyvern at 64 px in every view, and the red slit eyes, brows and 4 fangs are properly fierce. What keeps it under Raiju level: a stick-thin torso
hanging between 3.3-unit wings, a flat box chest from the front, and back spines that read as rivets from behind.
(Phase 1 = model only. The rest pose shows the wings spread, as noted. The clips were not judged.)

Must fix:
1. Slim torso vs wings (your flag, confirmed in model_front/back): the wing arms grow out of a 0.45-wide body and nothing anchors them. Add a
   flight-muscle mass per side at the wing root on Chest: B.add((+-0.20,-0.08,1.13), (0.10,0.13,0.12), BODY, "Chest", rot=(30,0,0), top=(0.8,0.85),
   rnd=0.40). Widen the chest half x 0.225 -> 0.25 (the pelvis stays 0.185, a deliberate +35 % step). Head-Chest is a check pair, so watch the head-low
   gargoyle idle against the new masses in phase 2.
2. Box chest from the front: the pale keel and bands form a straight-sided "tie" on a rectangle. The plan wants a keel/V. Keel seg top=(0.70,0.8) ->
   (0.40,0.8) so it narrows to a point at the pelvis, and the 3 band half widths 0.122/0.11/0.09 -> 0.115/0.085/0.06.
3. Dorsal spines read as rivets in model_back (the view players follow): 0.10-0.12 long x 0.05 wide on a 1.79-tall pet is about half the Raiju's
   relative size. Spine lengths 0.10/0.11/0.12/0.12/0.11/0.09 -> 0.17/0.19/0.21/0.20/0.17/0.13 with width 0.05 -> 0.075, at the same 60-72 deg lay-back. Tail
   spines 0.10/0.08/0.06 -> 0.15/0.12/0.09, width +50 %. Result: one jagged ridge from the crest to the blade.
4. Crown from the front: the 2 white horns (dir s*0.35, 0.9, 0.45) stand up beside the white crest blade with its red tip, so model_front/close_front
   read a 3-prong crown or candle. Splay the horns: dir (s*0.65, 0.75, 0.25), length 0.16 -> 0.19, so they frame the skull as horns while the crest
   stays the single centre blade. Don't change the crest itself; it's the best thing in the side view.
5. Membrane zigzags float: the membrane surface is at 0.015 (poly th 0.03, centred), but the bars sit at lift 0.022 with thickness 0.008, leaving a 0.003 air gap
   that becomes a dark hairline at x2.2. Change zigzag lift 0.022 -> 0.019.

Keep:
- the side profile: long crested skull with the red crest tip, S-neck, raptor crouch on 3+1 talons, and the tail ending in the barbed red arrow blade
- the bat wings: dark finger bones, wrist knuckle + thumb claw, scalloped trailing edge, darker inner panel, 3 bold zigzags per wing (accent < 10 %)
- the palette: BODY (96,90,166) lands as deep indigo-violet in game with pale lavender belly bands; the red only on eyes, crest tip, blade and zigzags
