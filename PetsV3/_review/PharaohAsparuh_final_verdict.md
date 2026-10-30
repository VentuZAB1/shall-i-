REVISE - 7.5/10 vs the Raiju and the refs (FINAL gate: model fixes + all clips). Up from 6/10.
From the front and tq he is excellent and clearly Asparuh: a cream Persian, a stern closed mouth with 2 fangs,
turquoise kohl slit eyes under heavy brows, the nemes with a clean flat striped flap, the uraeus, the usekh and a 5-lock
ruff. All 5 phase-1 must-fixes are done: the haunches are FUR and rounded, the mouth is closed, the chest has been
cleaned up (no drops, 5 locks, lappets seated), the flaps are single panels, and the tail is a fat plume. The clips are
good too.
Two cheap problems remain, both in the views players see most (side/back while lying, and the walk while following):
the new fluff tufts render as smooth faceted crystal shards and loose white chips, and the walking tail is a flagpole.
Model + walk-key fixes only; nothing else changes.

MUST FIX
1. Delete the 4 PALE flank tufts (spikes at y -0.17 / 0.01, z 0.17). They lie at ground level beside the belly, and
   in side/back/tq they read as loose white chips or paper, not fur.
2. The 6 haunch-edge tufts and the 2 Tail2 tufts are unstudded B.spike pyramids. From behind they read as broken
   crystal (the "rubble" look is back). Replace each haunch's 3 with 2 flat FUR locks built like a crest blade:
   B.add half (0.024, 0.055, 0.09), top=(0.5, 0.15), studs on, laid back 65 deg and 15 deg outward. Root them
   0.04 deep in the haunch's back-upper surface at (s*0.25, 0.63, 0.34) and (s*0.27, 0.66, 0.22). Use 1 lock of
   the same kind on top of Tail2. If they still read as shards, delete them: the rounded haunch (rnd 0.50) already
   breaks the box.
3. Walk tail: tail_up holds Tail2 vertical with the 0.70-long rigid Tail3 on top, so the tail rises about 2 head-heights
   (out of frame in pose_tq_walk_00/14). A Persian carries the plume lower. dt[0] -> (0.10+0.3 sin, 0.80, 0.60),
   dt[1] -> (0.6 sin, 0.64, 0.77), dt[2] -> (0.8 sin, 0.90, 0.42 + 0.15*curl). That makes a rising S-plume behind
   him with the tip at about the nemes top (z ~1.36 in the walk). Re-run check_pairs for Tail vs Leg_B.

KEEP
- The face and costume read (eyes, kohl, brows, stern fanged mouth, nemes + uraeus + usekh, gold anklets).
- act_knead: paws lift 0.15 L-R-L-R-L-R with the toe splay and shoulder roll, then the slow blink at f73-79. Unique.
- roar YAWN-SNARL: the head goes back with the jaw wide and lids shut (f22-28), then a forward snarl with the ears
  flat (f33-44). Clear, and Pharaoh is the only pet with a yawn.
