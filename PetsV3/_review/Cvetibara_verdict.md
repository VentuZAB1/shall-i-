REVISE - 7/10 vs the references (round 1). The front and 3/4 views are adorable and keep the V2 charm. The side and back
views, which players see most, read as a plain caramel brick under two rakes.

MUST FIX (most important first):
1. The wings read as rakes or combs. The 7 primaries (feather_wing, lines 125-135) fan about 13 deg apart and taper to
   30 % width (0.057 at the tip), so the tips stand about 0.12 apart and each gold tip reads as a separate yellow tooth
   (back and top views). Changes:
   - Use 9 primaries (fan step about 10 deg), width 0.19 -> 0.22, top (1, 0.30) -> (1, 0.55), so neighbouring tips touch.
   - Gold tip = the outer 30 % of the SAME feather: width = that feather's width at 70 % (about 0.15), top=(1, 0.80),
     thick FT + 0.002, and no overshoot past the tip (drop "+ d * 0.006").
   Target: from behind, a white wing with a scalloped gold edge, as in V2. Re-run collision_free for the wings after.
2. There is no light zone outside the front: the side view is about 95 % caramel, but V2 had a cream underside.
   Add a flush SNOUT belly band on both torso flanks (+x/-x faces), z 0.29-0.45, y -0.42..0.62. It must follow the bottom
   taper (lesson 2: x = 0.45*(0.92 + 0.08*t) + 0.006) and join the belly plate (line 147) and the chest bib (line 146).
   Optional, same recipe: a cream lower-cheek band on the head sides (z 0.76-0.90) that carries the snout colour back.
3. Plate mazes. Head and torso density 0.66 (lines 143, 152) packs the plates into Tetris clusters: a "7" on the head
   side and dice on the flank. Use the SECRET fill: head 0.45, torso 0.50. Set bk.STYLE["mix"] = (0.75, 0.25, 0.0)
   inside model() and restore it after B.build(). Target: 6-10 separate plates per head side.
4. Nostrils (lines 158-160): in the 512 px crop, the two 25-deg slanted dark bars on the nose read as a second pair of
   closed eyes. Make them 2 small upright dots, half (0.016, 0.006, 0.014), rot 0, at x +-0.055 (bible: "small round
   nostrils").

KEEP:
- The face: big square lilac-glint eyes with 2 highlights, the big dark nose with sheen, the "w" mouth and the blunt
  cream snout. It is the cutest face of the set.
- The loaf body with the huge head and the tiny dark paws with 3 cream claw nubs.
- The hero set: the gold block halo, the pink star-lotus and the 4 gold stars on the back.
