APPROVE 8.5/10 - above the Raiju for the front read. From the front and tq it IS the Lion-and-Sun emblem: a fierce tawny face (heavy
brows, gold slit eyes, gold brow sun, long fangs) inside a black-brown ring, then studded bronze rays with gold tips. The king's sit
idle and the sun-wheel act are unique in the roster. (Final gate, phase 2: model + all clips.)

Earlier must-fixes (fierce_verdict), all addressed:
1. Edge-on plank + mohawk in the side view: FIXED enough. The rays tilt back into a shallow cone (TILT 22/10/0) and the wheel sits in the mane
   (RC y -0.72), with the Ray joints re-aimed along ray_dir. From the side the side rays now show as blades in the mane. The top 3 rays are still thin
   gold sticks from pure side-on, but that is inherent to flat rays and acceptable.
2. Black mane hidden: FIXED. All 14 face-ring tufts are MANE (MANE_I only on the cheek ruff) and R0 is 0.31. model_front shows tawny face ->
   dark ring -> bronze -> gold.
3. Smooth rays: FIXED. The ray blades are role="limb", and the renders show studs on every ray.
4. Box rump: FIXED. The hips are rotated -14 with top (0.84,0.78) and TAILP[0] at (0,0.66,0.83), so the croup slopes into the tail.

Animation (tq key beats):
- idle KING'S SIT: it sits on its haunches with the chest high (Spine -15, -0.225), holds long looks left and right, sweeps the tail on the ground, then stands. Reads as royal.
- roar LION ROAR: the head drops as the jaw opens, rises to a level roar (jaw 36) with the flanks pumping, then 3 jaw-pop grunts and a tail lash. Matches the plan.
- act_sunburst: puffs up, gathers the rays, they SHOOT out and the wheel turns 360, with the right forepaw up and the head at 3/4 (40-60), then
  snaps back and huffs. The builder's lower-rays-into-the-mane deviation is accepted (it keeps the rays out of the legs).

Optional polish (not blocking):
1. act_sunburst 32-60: out = 0.12 pushes the ray roots (0.31 -> 0.43) past the mane edge. The rays then float as a detached ring with
   sky between them and the mane, which reads half like "parts flew off". Cap out at 0.06 (oscillation +-0.01) so every ray stays rooted
   in the mane while it spins. The flat = 1.0 rotate-out already gives the burst.
2. The emblem paw (frame 50) reads as a forward reach at knee height rather than the heraldic raised paw. Lift it to chest height:
   Leg_FR -62 -> -75 and curl the wrist down (Foot_FR 55 -> 75).
