REVISE - 7.5/10 vs the references (round 1). Very close. The front is the best view in this batch (3 real personalities,
clean Rottweiler points). The back and side views, which players see most, are near-black boxes. 3 small fixes, then APPROVE.

MUST FIX (most important first):
1. The flame tail reads as an orange horn or antenna between the centre head's ears. It shows in the front view, in all
   3 face crops and in most pose frames (LESSONS 6). Its top is at z 1.86 (TAILP[3] z 1.54 + 0.32), the centre head's top
   is at 1.75, and the front camera lifts objects this far back by about 0.15 more. Lower the tail and sweep it back:
   TAILP = [(0, 0.66, 1.04), (0, 0.88, 1.10), (0, 1.06, 1.19), (0, 1.20, 1.28)]. Flame seg end: tip + (0, 0.26, 0.20).
   Inner FLAME_Y end: tip + (0, 0.21, 0.16). Tail3 joint tail: (0, 0.1, 0.3) -> (0, 0.2, 0.15).
   Target: flame top <= z 1.50, and no orange above the centre head in model_front.png. Check that the roar still reads.
2. CHAR (44,40,54) has V 21 %, below the bible's floor for dark pets (item 6: V >= 28 %). In the side and back views the
   plates and AO vanish and the body is one black blob (about half of the back view). CHAR -> (60, 54, 74).
   Keep NOSE (20,18,28) so the noses and claw nubs still pop. The contrast with TAN stays large.
3. The back view has almost no colour (7 % tan versus 29 % in front). Add the real Rottweiler tan under the tail: a flush
   upward-pointing wedge on the hips' back face, B.add((0, 0.684, 0.72), (0.15, 0.006, 0.13), TAN, "Spine",
   top=(0.25, 1), studs=[], role="limb"). Its y follows the 0.95 bottom taper at that height, and it sits below the tail
   root (z 1.04). Optional: a flush 0.10 x 0.12 tan patch on the +y face of each hind shin, above the sock.

KEEP:
- The three personalities: goof (bold eyes looking off, tongue out, one flopped ear), alpha (bigger and higher, fierce,
  24° tan brows, fangs), grump (half lids, frown, pinned ears). Do not even them out.
- The tan points: muzzles, brow dots, cheek marks, the chest V, socks, and tan paws with dark claw nubs.
- The red spiked collars on thick necks, the chest/hips step (21 %), and the flat two-tone flame shape.
