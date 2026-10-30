REVISE - 7/10 vs the references (round 1). The front and tq views are a great boar, but the side view (seen most) breaks up.

MUST FIX (most important first):
1. The head sits apart from the body on a short neck: side and back views show a notch above and below it. The neck (line
   96) spans z 0.62-1.12, the head 0.55-1.25 (after HEAD_FWD) and the chest shell 0.80-1.34, so the wedge reads as a box
   on a stick. Neck -> B.add((0, -0.74, 0.93), (0.40, 0.18, 0.31), ROCK, "Neck", top=(0.92, 0.92), studs=[]) (z 0.62-1.24,
   buried 0.12 in the head and 0.10 in the shell). If the roar or rooting clips, cut HEAD_FWD 0.10 -> 0.06. Re-run collision_free.
2. The tusks cross the far eye in the tq hero view and most pose frames, and from the side they stand upright like rhino
   horns. Splay them out into crescents (lines 112-114): b0 x ±0.27 -> ±0.30; b1 (s*0.41, -1.60, 0.86) -> (s*0.50, -1.58,
   0.80); spike dir (s*0.12, 0.10, 1) -> (s*0.55, 0.20, 1), length 0.30 -> 0.26. The tips land near x ±0.62, outside the
   head (half-width 0.47), so they frame the face instead of covering it.
3. Too little magma: orange is 11 % of the tq view and 16-19 % of the side and back views (bible 30-40 %). Each flank has
   1 zigzag (3 segments, no branch, ending 0.06 above the core seam), and it reads as a Raiju bolt sticker.
   - Thighs (line 141): ROCK -> MAGMA, density 0.45, plus an outer rock knee pad B.add((X0 + s*(th[0] + 0.02), y, 0.56),
     (0.03, th[1]*0.92, 0.15), ROCK, leg, studs=["+x" if s > 0 else "-x"], role="limb"). The front, back and inner legs
     then glow under armour, as in ref_17.
   - crack() on armc: 5 points + 1 branch, e.g. ((-0.30, 0.20), (-0.20, 0.09), (-0.27, -0.02), (-0.14, -0.10), (-0.18,
     -0.21)), branch=(2, (-0.05, 0.02)), w 0.075 -> 0.062 (0.48 cell). Add a shorter crack on each hips-shell flank (armh)
     and one on the forehead, from between the brows up to the crest.
4. Each head flank shows a 3x3 bar code of upright plates ("i!!" in the side view; LESSONS 7 says no letters). On the head
   block (line 98) set pmix=(0.70, 0.15, 0.15), prelief=1.5 and density 0.50, for 4-6 chunky square rock slabs.
5. In the front view the crest shows as one grey-and-orange candle on top of the head (LESSONS 6). Make it rise to the
   withers: (y, L, w) rows -> (-0.50, 0.24, 0.12), (-0.36, 0.34, 0.15), (-0.21, 0.46, 0.18), (-0.06, 0.40, 0.16),
   (0.08, 0.30, 0.13). Widen spike2's base hx from w*0.55 to w*0.75 so it reads as a ridge.

KEEP:
- The face: fierce eyes with light rims in dark rock sockets, 22° ROCK_T brows, the big pig-snout pad with dark nostrils, orange-lined ears.
- The wedge: head 1.04 TW, a chest shell 25 % wider than the hips shell, short legs on dark split hooves.
- The orange belly band and shins, the two-tone laid-back crest, the flat flame tail.
