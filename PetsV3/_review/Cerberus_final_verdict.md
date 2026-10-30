APPROVE 8.5/10 - above the Raiju for silhouette. The 3-head fan with personality ears, red slit eyes under heavy brows, spiked
collars, Rottweiler rust points and the serpent tail make an instantly readable hellhound (the f_70 vibe), and the act is a
genuinely funny behaviour. (Final gate, phase 2: model + all clips.)

Earlier must-fixes (fierce_verdict), all addressed:
1. Floating chest V: FIXED. The bars are seated on the tapered rib front ((+-0.10,-0.497,0.82) -> (+-0.03,-0.446,0.60), normal tilted), and
   model_side has no rust plank under the necks any more.
2. Serpent head as a 4th head: FIXED enough. The tail tip swings to +x with the snake yawed 35 deg out, so it no longer sits between the
   alpha's ears. From the front it now peeks out between the centre and left heads (see polish 1).
3. Spindly legs: FIXED. Front upper arm 0.092, shins 0.080, socks 0.074, paws (0.086,0.10) with claws spread +-0.052, front stance
   x 0.19. They now carry the head fan from the front.

Animation (checked front/side renders of the exported blend; every clip has ground_min >= 0.000):
- idle SIBLING SQUABBLE: the right veteran darts in and nips the CENTRE's ear (builder's variant: it can't reach the left head past the
  centre, which is accepted). The centre flinches, and the left hothead pants and then whips round snarling. Reads as squabbling siblings.
- roar THREE-HEAD FAN SNARL: heads drop, then fan out (L/R ~30 deg, C up ~16) with trembling open jaws, paws spread, serpent rears.
- act_triplesnap: all heads track the fly, C snaps up (36 deg), L lunges and snaps, R lunges and snaps, then all three clamp DOWN
  together, chew, and finish smug. Each beat is clear from the front. Unique in the roster.

Optional polish (not blocking):
1. From the front the snake head still overlaps the left head's ear tips. Push TAILP[3] x 0.23 -> 0.30 and the snake yaw 35 -> 45 deg
   so it clearly peeks out beside the fan.
2. The roar fan is about +-30 deg against the plan's +-40. If the Neck pairs stay collision-free, raise the neck yaw 20 -> 25 for a wider,
   more dramatic fan.
