APPROVE 8.5/10 - at or above the Raiju. Wedge head + upturned tusks + two-tone crest + magma gaps make a great 64 px boar
silhouette, and the wallow is the funniest, most readable signature in the Magma tier. (Final gate, phase 2: model + all clips.)

Earlier must-fixes (fierce_verdict), all addressed:
1. Accent budget: FIXED. There is now a 4th shell over the waist and the shells come lower. Measured orange is 7.1 % side / 6.6 % back /
   6.0 % front (target 6-9 %).
2. Box belly: FIXED. Waist 0.15 @ z 0.74, hips 0.16 @ z 0.70, tuck to (0,0.28,0.62), so the underline now rises toward the stifle.
3. Wedge from behind: FIXED. Hips are 0.18, hind legs at x 0.115 and the rump shell sits 0.02 lower, so the back view steps down from the withers.
4. Eye hidden by the tusk: FIXED. The tip spike is now 0.07 aimed (s*0.05,0.45,0.9), and close_side shows the whole orange slit.
5. Pig snout: FIXED. The nostrils are small slits rotated 20 deg.

Animation (checked in my own side/front renders of the exported blend; every clip has ground_min >= 0.000):
- idle ROOT & SNORT: two scoops with the snout, a snort with a head lift + body jolt + crest rise, ear flicks. Unique.
- roar CREST & CHAMP: 4 jaw clacks with the head low, then the squeal with the head up, ears pinned. Reads well.
- act_wallow: kneel, flop, on its back (roll 158) with four legs bicycling + back wriggle, roll back, spring up, snort.
  Behaviour-based and the only roll-on-the-back motif in the roster.
- The crest flare done as rise + slide (builder's note) is an acceptable variant for a one-bone crest.

Optional polish (not blocking):
1. On its back (f30-50) the boar balances on the crest tips. Measured: the Mane tips touch the ground, the rib shell is 0.03-0.07
   above it and the Spine/rump half floats 0.18 above it (visible from the side). During f18-60, key Mane pitch about +25 deg (lays
   the spikes back) and Spine pitch +6-8 deg, then re-run the ground fix so the shells rest in the "mud".
2. The crest flare is modest (0.045 rise + 6 deg; the root is buried 0.06 so it can't rise much more). In the roar, pin the ears
   back already at f8 (not only at f38) so the clack phase reads as a threat too. The coordinator's ember VFX on the crest will carry the rest.
