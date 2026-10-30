REVISE 7.5/10 - the front and tq views read as the Lion-and-Sun emblem from across the map (the best 64 px front read of this batch). The face is properly
fierce and the body is a real lion with a rising belly line. Two things keep it under the Raiju bar. From the side (the view players get while it follows
them) the sun is an edge-on plank with a gold mohawk on top. From the front the "black mane" barely shows, so the face is ringed orange-on-orange.
(Phase 1 = model only; the clips were not judged. Colours are fine per the Studio calibration.)

Must fix:
1. Side view: all 12 rays lie in one plane (y -0.80), so model_side / close_side show a thin vertical plank with gold nubs, and the top ray stands up as
   a gold mohawk. Make the sun a shallow cone that opens backwards: tilt rays i 0-3 and 9-11 22 deg back (+y) about their own tangent axis
   (cos a, 0, -sin a), rays i 4 and 8 10 deg, and keep i 5-7 flat (they pass in front of the front legs). Move the wheel into the mane: RC
   (0,-0.80,1.02) -> (0,-0.72,1.04). Re-aim the Ray joints and tails along the tilted directions. From the side the upper rays then show as broad
   blades fanning back over the mane; from the front they shrink by only ~6 %. (act_sunburst can flatten the tilt while the wheel turns.)
2. The black mane is hidden from the front and tq. The 14 face-ring tufts alternate MANE_I (148,80,40) with MANE, and the ray roots start right at the
   bulk edge (R0 0.25 = the bulk half-width), so the face is framed by rust plus bronze orange. Make all 14 face-ring tufts MANE (keep MANE_I on the
   cheek ruff only) and set R0 0.25 -> 0.31 (long rays 0.40 -> 0.36 to keep the disc size). Target in model_front: tawny face -> a >= 0.08-wide
   near-black ring -> bronze rays -> gold tips.
3. Studs: the ray blades are role="detail", so the new StudMask leaves the 12 biggest shapes on the pet smooth. Give the bronze RAY blocks
   role="limb" (bevel 0.008 unchanged); the gold tips can stay smooth.
4. Box rump (side + back views): the hips block ends in a near-vertical rear wall with a hard top corner, and the tail leaves from that corner. Hips rot
   (-8,0,0) -> (-14,0,0), top=(0.84,0.90) -> (0.84,0.78), TAILP[0] (0,0.64,0.86) -> (0,0.66,0.83), so the croup slopes ~15 deg into the tail.

Keep:
- the face: heavy brows over gold eyes with slit pupils, the gold sun mark on the brow, the dark nose and long fangs (fierce, not cute)
- the 12-ray emblem with gold outer tips (iconic at 64 px), plus the dark mane bulk, chest bib and dorsal mane
- the heavy forequarters, the big clawed paws, the deep chest with its rising pale belly strip, and the long tail with a dark tuft
