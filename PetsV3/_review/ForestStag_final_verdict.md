REVISE - 7.5/10 vs the Raiju and the refs (FINAL gate: model fixes + all 4 clips). Model 8/10; the signature's strokes don't read.
The model is now a real royal stag and all 6 phase-1 must-fixes are done. The beam sweeps back (BEAM y -0.80 -> -0.47)
with raised bez/trez and a crown cup. The drapes are flat sheets with a pointed fringe. Neck2 is tapered (0.72, 0.66) with
nape tufts. The throat locks are shortened and clipped at z 0.70. HEIGHT is 11 with PITCH 0.0445. There is a BACK saddle and a neck stripe.
Idle (sniff, ear swivel, freeze, nibble) and roar (neck level forward, 3 bouts, rack lowered at the viewer) are good.

MUST-FIX (1 item; the owner named this act himself: "Deer scratches its tummy using its head")
1. act_scratch: the 4 strokes are invisible. I measured points on the Head bone in the baked clip
   (ForestStag_rigged.blend). Between a contact key and its rake key (22->27, 32->37, 42->47, 52->57) the contact tines
   (brow/bez/trez) move only 0.025-0.030 BU. That is 0.13-0.15 studs at x1. The long rub (62->68) moves 0.04 BU. pc frames
   024/030/046 are near-identical, so in game this reads as "turns its head to its side and freezes for 2 s", not as a
   scratch. The cause is that the rake key only changes Neck yaw by -6 deg. Near the neck base that moves the head
   mostly AWAY from the flank, and only by a few cm.
   Fix: keep the searched contact pose (base) as it is. Search a second "rake-end" pose the same way (_posesearch.py).
   In that pose the contact tines sit 0.12-0.18 BU further BACK and DOWN along the flank/shoulder and stay >= 0.02 off
   the body. Starting point: Neck y1 base-14, Neck2 y2 base-10, Head hd base+12 (nose further down, so the tines drag).
   Then animate each stroke as contact -> rake-end in 6 f (drag, ease-in) -> back to contact in 4 f, and use 1.3 x that
   travel for the long rub at 62-72. Target: each stroke moves the contact tines >= 0.12 BU (>= 0.6 studs at x1). Add
   a 3 deg Chest roll toward the head on each drag so the shoulder leans into the rack. Re-run step-1 collisions
   (Head vs Chest/Spine/Leg_FL/Shin_FL).

KEEP
- The swept royal rack with the emerald drapes. At 64 px it is the strongest silhouette in the Grass tier.
- The neck curl itself (Neck 73 + Neck2 28 + head roll 84) with Leg_BL lifted to open the flank. The pose is right;
  it just needs to move.
- The rut roar: the neck goes level forward and the rack is lowered at the viewer. The scent-the-wind idle with independent ears.
