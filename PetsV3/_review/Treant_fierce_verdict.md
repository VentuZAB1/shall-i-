REVISE - 6/10 vs the Raiju and the refs (fierce phase 1: MODEL only, the old clips are ignored).
The face is the best in this batch (amber slits in knot sockets, knot brow, splinter teeth, moss beard), and the crown names it
at 64 px. The body is still a standing golem (your note, confirmed): an upright box stack, a dark "backpack" burl,
square legs that narrow toward the ankle, slot-like dashes, and lightning-bolt cracks.

MUST-FIX
1. Hunch (the side view is a vertical stack, not "a hunched oak giant"). Chest block rot 18 -> ~28 and y -0.07 -> -0.12.
   HEAD_C (0, -0.20, 1.55) -> (0, -0.32, 1.46) with RH 6 -> 15 deg, so the face sits in front of and below the shoulder line
   (head top ~0.15 above the shoulder blocks). Raise the burl hump to z ~1.55 and grow it to (0.30, 0.18, 0.19) so it is the
   top of the back. Move the crown branches and the Head/Crown joints by the same offset (~-0.12 y, -0.09 z).
2. The burl reads as a backpack: a single BARK_D box with a hard outline. Make it BARK with 2 BARK_D knots (0.10 / 0.07)
   offset to one side, plus 2 smaller rounded burls (0.12, 0.09) beside it, so it reads as a growth.
3. Bark: the short flush black dashes read as slots or a barcode, and the back face is bare. Replace them with RAISED ridges
   (BARK_D, 0.035 wide, 0.03 proud, full trunk height ~0.85 -> 1.45, following the chest tilt): 3 on the front, 2 per side
   and 4 on the back, plus 1 per thigh front and per forearm. They also break the box outline in the back view.
4. Legs: shin bot=(1.18, 1.15) makes the KNEE end the widest, the opposite of a trunk. Thigh: add top=(0.82, 0.82). Shin:
   drop bot and add top=(1.40, 1.35), so it flares from ~0.15 at the knee to ~0.21 at the ankle and flows into the root base.
   Add one 0.04 BARK_D root buttress down the outer side of each shin into the outer root toe.
5. The sap cracks are zigzag BOLTS (the Raiju's motif). Make them splits: lateral jitter +-0.02 -> <= 0.006, one kink only,
   lens-tapered width (0.3 -> 1.0 -> 0.3 of 0.038), and a 0.03 x 0.06 sap drip under the chest crack.
6. The moss shoulder pads read as armour. Per shoulder, use a top slab (0.12, 0.13, 0.04) plus an overhang (0.09, 0.05, 0.07)
   hanging 0.08 down the outer side, rot z +-25 / +-10 so the 2 shoulders differ, with MOSS on top and LEAF_D under.

KEEP
- The whole face block: knot brow, amber slits with hot centres in FISSURE sockets, splinter teeth, moss beard.
- The crown of twisted branches with dark leaf clumps (the 64 px read). Optional: turn each clump 15-35 deg on z.
- The splayed root toes and the 3 twig talons per hand.
