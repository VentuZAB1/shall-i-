APPROVE 8/10 - at the Raiju's level. It's a long, low, real leopard with a deep chest + strong tuck, a small fierce head (heavy brows,
violet slit eyes with cat pupils, long fangs), big clawed paws, a dark topline, readable ghost rosettes and a thick crystal-tipped
tail. The portrait reads as a proper void predator now. (Final gate, phase 2: model + all clips.)

Earlier must-fixes (fierce_verdict), all addressed:
1. Crystals / pink: DONE AS SPECIFIED. The base moved back and out, they point back-out, the colours are now plan violet (170,80,255)/(206,160,255)
   and the tip share is 0.25. In tq/portrait they read as shoulder crystals. In the front view they still flank the head at ear height (polish 1).
2. Soft face: FIXED. The whisker pads are FUR and flat and the ear inners are FUR. close_front now reads as a snarling cat, not a cartoon mouth.
3. One-tone body: FIXED. There is a FUR_D topline saddle, dark tail end, dark paws/brows/ears, and PALE only on the underside strip.
4. Coin slot: FIXED. The saddle now lies on the top surfaces from the withers to the rump.
5. Specky rosettes: FIXED. There are 5 bigger broken rings per side (r 0.050-0.054, bars 0.034, darker GHOST), readable at distance.
6. Thin tail: FIXED. Tail segments are now 0.044-0.064, so it reads as a leopard tail, not a rope.

Animation (checked side/front renders of the exported blend; ground_min 0.002 in every clip):
- idle BIG-CAT STRETCH: play-bow with the front paws sliding forward and the rump high, then it watches left with the tail tip twitching. Unique.
- roar SNARL & SWIPE: crouch, ears flat, lip curl (jaw 26), then the right forepaw rears up and swipes across the face. Reads clearly.
- act_pounce: low stalk with paws creeping, hind-end wiggle, then a launch into a flat airborne leap (0.30 off the ground, front paws reaching,
  ~0.52 SH travel). It lands, pins, bites and hops home. A textbook ambush, and the only pounce in the roster.

Optional polish (not blocking):
1. The shoulder crystal tips reach z ~0.96, level with the ear tips, so from the front they read as pink side tufts. Lay them further
   back: direction (s*0.6,0.55,0.75) -> (s*0.55,0.85,0.40) and main shard 0.22 -> 0.19, so the tips stay below the ear line from the front.
2. The play-bow is mild (Spine pitch 9, chest sinks only 0.03). Deepen it: Spine pitch 9 -> 15, z -0.03 -> -0.07, front reach
   -0.16 -> -0.22, so the elbows nearly touch the ground and the stretch reads at 30 studs.
