APPROVE 8/10 - at the Raiju bar. It is now a true lung: a thin S-body (~13 D) with clam-belly scutes, a violet flame mane down the spine,
gold stag antlers, barbel whiskers trailing back, a fierce camel head with an open fanged jaw, and the pearl. The ink + gold + violet
Void palette is clearly separate from the Stallion. (Final gate, phase 2: model + all clips.)

Earlier must-fixes (fierce_verdict), all addressed:
1. Sausage body: FIXED. D is 0.28 (RAD follows) and the neck rings are 0.135. The S is deepened (CP[3] 1.08, CP[5] 0.58, CP[9] 1.08) and the hind hip
   is at x 0.075. The head now outweighs the tube and the body reads serpentine in side and tq.
2. Whiskers crossing the face: FIXED. They run back along the jaw line and droop beside the neck on the specified path. The front view keeps
   two gold arcs, and in tq/side they read as barbels under the cheek, not a rod through the mouth.
3. Sugar-cube pearl: FIXED. Three 0.11 PEARL blocks (rotated) make a round faceted ball with an 8-bar GOLD equator band. It reads as a round
   white pearl tied to the gold accent at play distance.

Builder deviation accepted: act_pearlchase is restaged as one airborne whirl (frame 48: the body twisted into a rising coil, the head up
after the pearl). It still reads as "chases the pearl around", and the snatch with the front claw (64) is clear.

Animation (tq key beats):
- idle PEARL NUDGE: the pearl drifts out, the head turns to it and nudges it back, with a lazy wave down the body. Unique and charming without being cute.
- roar S-COIL STRIKE: pulls back into a tall S with the head high (18), then strikes forward with the jaw wide and the tongue out (30). Clear.
- act_pearlchase: the pearl darts off (06), the front body rears after it (34), the airborne whirl (48), the claw catch (64), and it settles with the pearl back
  at the cheek (82). Each beat reads.
- fly / takeoff / land: wingless vertical swimming waves with the head level.

Optional polish (not blocking):
1. The whiskers are rigid on the Head bone. In the whirl (48) they hang straight down like a gold rod, and in the head-low idle nudge the tips reach
   the front-foot level. If a later pass adds 2 whisker bones per side (Whisker_L1/L2, child of Head), let them trail 15-25 deg behind the
   head motion. Until then, check one head-low frame in Studio that the tips don't sink into the floor.
2. Close up, the pearl's bevelled cubes read slightly like a cotton ball. Optional: lift PEARL to pure (246,244,255) and set the band
   0.01 more proud so the ring silhouette is crisper.
