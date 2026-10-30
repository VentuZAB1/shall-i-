APPROVE 8/10 - at the Raiju bar. The arched neck, the standing hot-pink flame crest, the long legs on big dark hooves and the
flame tail make a nightmare Friesian you can name at 64 px. The charcoal + hot-pink Void split from the dragon reads clearly.
act_rear is the most readable signature in this batch. (Final gate, phase 2: model + all clips.)

Earlier must-fixes (fierce_verdict), all addressed:
1. Train-car torso: FIXED. The waist is (0.142,0.20,0.135) at z 0.84, and the croup is rotated -15 with top (0.80,0.72). TAILP sits on the slope.
   Side and back now show a deliberate ribcage > waist < croup step instead of two equal boxes.
2. Jaw as a bridle strap: FIXED. The COAT jaw runs back into the jowl (Jaw joint moved) with a pale chin only at the front. The mouth line is
   half 0.07 at y -0.43, and the upper fangs at x +-0.076 now sit outside the jaw.
3. Spiky pink crowns at the fetlocks: FIXED. There are 3 flat flame blades per leg falling over the hoof (dirs as specified, tips >= 0.06).
4. Horn/brow visor: FIXED. h2 = h1 + (s*0.045,0.075,0.06) and the tip spike tilts up. From the side the horns stand clear above the poll.
5. Parallel neck locks: FIXED. They fan 34/52/70 deg with lengths 0.22/0.30/0.26.

Animation (tq key beats):
- idle HIP-SHOT FLEHMEN: the right hind rests on its toe, the tail swishes twice and the ears turn. At 72-100 the head lifts and the Lip curls -40.
  It reads as a calm, real horse, and nobody else has it.
- roar SQUEAL & BUCK: a jaw-open squeal (builder's head-up variant accepted), then the head drops and both hind legs kick high with the
  rump up 0.15. The buck frame (36) is a great silhouette.
- act_rear: gathers (12), rears ~52 deg on planted hind hooves (28-42), strikes in 3 alternating sine strikes per hoof while whinnying, then crashes
  down (66) and settles. The plan beats and timing are met, and the main mover arcs are far above 15 deg.

Optional polish (not blocking):
1. In close_tq the upper fang, the dark-red mouth line and the lower fang stack into a white-red-white "candy stick" at the mouth corner.
   Move the lower fangs 0.02 back (y -0.405 -> -0.385) so the two teeth don't line up into one striped bar.
2. From the side the croup is still a separate rounded block with the tail on its top-back corner. It is acceptable now, but the tail dock could
   start 0.02 lower (TAILP[0] z 0.90 -> 0.88) so it grows out of the slope rather than a ledge.
3. COAT (74,70,92) is the darkest body in the roster. Check one Studio screenshot: if the studs vanish into flat black at 30 studs, lift COAT
   ~10 % (do not touch the pink).
