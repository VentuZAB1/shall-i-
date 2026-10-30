APPROVE - 8/10 vs the Raiju and the refs (FINAL gate: model fixes + all 4 clips).
The best face in the Grass tier now sits on a body that reads as a hunched old oak, not a golem box. At 64 px it shows
the crown of 5 leaf clumps, long talon arms and root feet.

PHASE-1 MUST-FIXES: all 6 done.
1. Hunch: UPPER pitch 34, the head is pushed forward/down (HEAD_C y -0.40, RH 16 deg) under the hump, and the crown moved
   with it.
2. Burl: a BARK hump with 2 BARK_D knots plus 2 side burls. It reads as a growth, not a backpack.
3. Bark: raised BARK_D ridges (3 front, 2 per side, 4 back, plus thighs and forearms). The back view is no longer bare.
4. Legs: the shin flares to the ankle (top 1.40/1.35) and has a root buttress on each.
5. Sap cracks: lens-shaped splits with one kink and a drip under the chest crack. No more bolts.
6. Moss shoulders: a top slab plus an overhang, rotated differently on each side.

CLIPS (checked _pose_tq_sheet and the code)
- idle WIND SWAY: the body sways, the arms lag, a gust swings them at f65 and a back-stretch at f100. Unique.
- roar TIMBER LEAN: it creaks back, then tips forward from the ankles with the crown whipping, then hauls back. The
  25 deg lean (builder deviation) is accepted. roar_30 is the most dramatic frame in the batch.
- act_takeroot (signature): it plants wide and the roots grip (builder deviation: grip instead of sinking, accepted).
  The arms rise into a branch V, the head tilts up, and the frozen tree holds 40-62 with only the crown swaying. The head
  snaps forward, then 2 yanks free the left foot and then the right. It clearly says "becomes a tree, tears itself free".

OPTIONAL POLISH
1. Arms coming down (f72-90): they lower through the FRONT, so at ~f80-88 both arms point straight at the viewer like a
   zombie (takeroot_86). Lower them through the sides instead, like drooping branches: f80 pitch -70 roll 60, f88
   pitch -20 roll 35, then rest.
2. The tree hold is 22 f (0.73 s). If the clip can grow to 106 f, hold 40-68 so the "it's just a tree" beat lands.
