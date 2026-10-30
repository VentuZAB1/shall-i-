REVISE 7.5/10 - the closest of this batch to the Raiju. The 3-head fan with personality ears, red slit eyes under heavy brows, spiked
collars, Rottweiler rust and the serpent tail give a great 64 px silhouette (the f_70 vibe). Fix these 3 and it's an APPROVE; after that only the side
and front views need re-checking.
(Phase 1 = model only. The old clips were not judged.)

Must fix:
1. Floating chest V: both rust bars hang 0.07-0.09 in front of the tapered ribcage. In model_side they show as a rust plank
   dangling under the necks. Because of bot=(0.66,0.56), the rib front is at y -0.491 at z 0.82 and at y -0.440 at z 0.60. Set
   p0 = (+-0.10, -0.497, 0.82), p1 = (+-0.03, -0.446, 0.60) and normal (0,-1,-0.23) (LESSONS item 2). The top end can tuck under the yoke.
2. Serpent head sits between the alpha's ears: in the front view the snake head is exactly between the centre head's ears and reads as a
   4th head or a hat. Swing the tail tip to +x: TAILP[2] (0,0.97,1.06) -> (0.06,0.97,1.04), TAILP[3] (0,1.05,1.24) ->
   (0.16,1.03,1.18), and yaw the snake head's direction ~25 deg outward. From the front it then peeks out beside the head fan, and in the side view it still
   rises above the back.
3. Mastiff legs: under the ~1.0-wide head fan the legs look spindly from the front (the plan says "thick"). Changes:
   front upper arm 0.078 -> 0.092, all shins 0.066 -> 0.080, rust socks 0.060 -> 0.074, paws (0.074,0.09) -> (0.086,0.10) with
   claws spread to +-0.052, front stance x 0.175 -> 0.19. The hind thigh can stay.

Keep:
- the ear personalities (pinned / upright alpha / torn veteran) and the centre head's 10 % size + height lead
- RUST (166,94,62): the browner choice was right, it lands as a proper Rottweiler tan in game; keep the chest-V/socks/brow-dot pattern
- the collars with steel spikes, and the serpent head with its fangs + red eyes (unique silhouette in the roster)
