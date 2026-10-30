REVISE - 7/10 vs the Raiju (8) and the refs (model phase 1). A readable midnight dragon: the pearl horn crown, the
crescent-moon tail and the framed wings are strong, and the face is properly fierce. It loses to the Raiju on in-game
size, on a plain blue body with no big accent from behind, and on white specks where it needs real marks.
MUST FIX (most important first):
1. In-game size (builder's question): HEIGHT 7.5 -> 10.0. The rest-pose height is 1.998 (horn tips; withers only 1.07),
   so 7.5 gives 0.266 units/stud: withers 4.0 studs vs the Raiju's 5.6, 25 % smaller than the Griffin of the same egg
   and than Ivonrath (both 0.199 units/stud). At 10.0: 0.200 units/stud, withers 5.3 studs, span 16.8 studs (Ivonrath
   17.0), 22 studs at x2.2 incl. the thin horn tips (LavaGolem/Treant are 10 too); pitch auto-scales. Later: H_model/0.20.
2. No big accent on the body: from the back and side (what players see) the body, legs and tail are plain blue. Add one
   flush MOON crescent on the outer face of each hind thigh (Leg_B bone), like the Raiju's bolts: 4 B.bar pieces along
   an arc of r 0.11 round the thigh centre, opening toward the tail, width 0.05, 0.010 proud, end bars top=(1, 0.15),
   x computed on the tapered thigh face (lessons item 2). It echoes the tail moon and reads at 64 px.
3. Constellations read as confetti (9 loose 0.05-0.07 diamonds per wing face). Outer panel (W, f1, f2): ONE 4-point
   star (2 crossed MOON bars 0.13 x 0.032, ends top=(1, 0.2)) at the panel centre + 3 diamonds (half 0.034) in a
   straight line toward f1, 0.10 apart. Rear panel (W, f2, f3): 2 diamonds. Inner panel (S, W, f3): none. Both faces.
4. The S-neck is a vertical post in the side view (N1 -> N2 rises straight up). NECKP[1] (0, -0.78, 1.18) ->
   (0, -0.83, 1.15), NECKP[2] (0, -0.745, 1.49) -> (0, -0.71, 1.47): the lower neck bows forward, the upper neck leans
   back ~20 deg. Move every Head-bone part by (0, +0.035, -0.02) (pure translation); re-check roar/eclipse later.
5. Floating keel: the pale keel (0, -0.60, 0.79) stands in front of the tapered chest; a side ray test is see-through
   behind it at z 0.64-0.72 (y -0.58..-0.50) = the pale blade hanging under the neck. The chest front recedes from
   y -0.56 (z 1.05) to -0.43 (z 0.51), ~14 deg: lean the keel to match (bottom further back), centre y ~ -0.52,
   <= 0.012 proud; the scute bands follow.
6. From the front the 5 Orbit shards sit between the horn tips and blur the crown into a cluster of white spikes.
   Shard ring radius 0.30 -> 0.40 and ORBIT_C y 0.22 -> 0.30 (z unchanged, below the horn tips, so H stays 1.998).
KEEP:
- The crown: 2 big swept 3-segment pearl horns with moon tips + 2 side horns over heavy dark brows and pale slit eyes.
- The flat crescent-moon tail blade - the best signature shape of the four from behind.
- The dark-framed 2-tone membrane wings with the scalloped trailing edge and the pearl thumb claw.
