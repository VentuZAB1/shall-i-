APPROVE 8/10 - now a proper deep terror. One tapered bullet mantle runs into a pointed cone with swept arrowhead fins, a clean squid read
from every side. It has big blue warning rings, angry slit eyes under heavy brows and a beak maw down in the arm crown. act_wrap reads
as grab, crush, drag down, release. (Final gate, phase 2: model + all clips.)

Earlier must-fixes (fierce_verdict), all addressed:
1. Screen eyes: FIXED as specified. The eyes are sunk and slit-shaped (socket half z 0.058, iris 0.033) and slanted 18 deg, with the glint
   at the outer end and a lower-lid ridge. In the 512 px crop they still look a little like a visor, but they read as fierce slits at game
   distance.
2. Birdhouse mantle: FIXED. The walls taper from bot 0.95 to top 0.58 and the cone base matches the mantle top. No eave.
3. Drooping fins: FIXED. They are swept and lifted: an arrowhead from the front, swept blades in tq/back.
4. Hex nuts and bullet holes: FIXED. Layered rings of r 0.09-0.10 with BODY_D centres. The spots are gone, and there are 3 barnacle cones.
5. Cartoon nose: FIXED. The beak sits lower (z 0.38) between T1/T2, with 2 hooked mandibles.

Animation (my own renders of the exported blend from tq/side/front/top/low; ground_min = 0.03 (the hover) in every clip):
- idle HOVER WAVE: a slow bob while a wave travels round the arm ring, plus a fin ripple.
- roar KRAKEN RISE: it sinks, then rears up 0.24 with all 8 arms flared into a spiked crown (f20-42), tips writhing, and crashes back down.
  The strongest roar of this batch.
- act_wrap: an arm reaches up at f14. At f30-60 the 4 front arms close into a loop in front (the top view shows the ring round the "mast"),
  then 3 squeezes with fin flares. At f60-76 it drags down with the mantle tipping forward 15. At f84 the arms unfurl in a wide splash,
  then it returns to the hover. Behaviour-based, and the only constrict in the roster.

Optional polish (not blocking):
1. The coil reads more like a claw grab than a wrap. The plan's 60-80 deg curls are ~20-40 deg here. On the 4 front arms, raise the coil
   terms: b 8+10 -> 8+22, c 10+12 -> 10+26, d 12+14 -> 12+28. Re-check T1-T2/T2-T4/T1-T3.
2. The 3 squeezes are subtle (f36 vs f42 is nearly the same pose). On the squeeze keys (36/48/60), make Spine z +-0.04 -> +-0.07 and the
   d squeeze +15 -> +25, so each pulse pops at 30 studs.
