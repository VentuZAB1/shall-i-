REVISE - 7/10 vs the Raiju and the refs (fierce phase 1: MODEL only, the old clips are ignored).
A big step up from the fawn: a real red-deer body, a rising belly line, a fierce narrow head, a rack that names it at 64 px.
Under 8 because of the rack's side profile, the drapes and the neck ends. Chestnut is fine (warm tan-brown in game).

MUST-FIX
1. Rack profile: the beam rises almost straight up (BEAM y -0.80 -> -0.66) while 6 of the 7 tines point FORWARD, so the side
   view is a comb or fish skeleton. Sweep the beam back: BEAM y -> (-0.80, -0.72, -0.60, -0.50, -0.47), same x and z. Raise
   the tines: bez (s.22,-1,.40) -> (s.25,-1,.80); trez (s.12,-1,.50) -> (s.30,-.8,1); crown-forward (s.10,-.85,.75) ->
   (s.15,-.55,1); crown-side (s.75,.55,.65) -> (s.60,.50,.95). Only the brow tine stays near horizontal over the face, and
   the crown becomes a cup. A swept rack also reaches the flank more naturally in act_scratch. Re-check Head vs Chest/Spine.
2. Moss drapes: each one is 3 parallel round rods, which read as green fingers or test tubes up close (LESSONS item 5). Per
   drape, clump 0.045 -> 0.06 (wraps the beam) + 2 FLAT pointed leaf blades 0.045 wide x 0.010 thick instead of the rods,
   broad face normal (s0.7, -0.7, 0) so front and side both see them, lengths L and 0.6 L, splayed +-25 deg.
3. Neck2's flat end cap sticks out behind the skull as a square collar (close_side). Change Neck2 ext1 0.03 -> 0 and
   top=(0.86, 0.82) -> (0.72, 0.66) so it tapers into the braincase. Add 2 MANE tufts at the nape (0.10 long, laid back
   60 deg) over the joint.
4. Throat locks: the lowest ones hang across the upper foreleg like a dark blade stuck in the shoulder (side view). Lengths
   at t (0.10, 0.32, 0.55, 0.78): (0.20, 0.24, 0.24, 0.20) -> (0.12, 0.18, 0.22, 0.20); nothing below z 0.70.
5. HEIGHT 9 -> 11. The rack makes the model 2.19 BU tall, so at 9 the withers sit at ~4 studs, a fawn next to the Raiju's
   ~5.3. At 11 the withers come to ~4.9-5.2 studs, level with the wolf (a royal stag should never look smaller-bodied), and
   the rack tips reach 11 studs. The extra height is thin antler, so x2.2 (~24 studs) still reads light. Rescale PITCH to
   0.042 x (H_model / 11) / (1.498 / 8) = ~0.045. Don't go to 12 (26 studs at x2.2).
6. Back view (seen most) is flat chestnut + white rump: BACK saddle 0.13 half-width + a 0.06-wide BACK stripe up the neck
   top to the nape, so the brief's dark back / chestnut flank / pale belly zones read.

KEEP
- The V rack with emerald drapes as the 64 px signature (the front view is excellent).
- The head: long narrow face, black nose, pale lip, emerald slits under heavy angled brows.
- The rising belly line with its pale strip, the pale rump patch, and the thin jointed legs with split hooves.
