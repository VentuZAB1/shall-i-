REVISE 7.5/10 - one small fix away from APPROVE. All 6 model must-fixes landed, and act_twirl is the best-staged signature of this batch.
The one problem: the trident never touches the ground. The idle's "taps" and the act_twirl's butt slam both stop in mid-air. (Final gate, phase 2.)

Earlier must-fixes (fierce_verdict), all addressed:
1. Waffle backpack: FIXED. 3 back keels + 1 per flank, continuous, ending in points at the serrated rim.
2. Cube head: FIXED. The skull is domed (half z 0.18, top 0.70/0.72), with the coral band fitted above the brows and scutes on the crown.
3. Small nose beak: FIXED. Root 0.18, with the hook (0.15 x 0.068) over the jaw tip. close_front shows the full coral slits.
4. Robot knee sockets: FIXED. The keel is aimed up the guard.   5. Shell hangs off: FIXED (dome y 0.25, flange 0.44 at y 0.19).
6. Toy finish: FIXED. SCALE inlays on the forearms, thighs, shins and neck, and the Trident is nostud (smooth bronze).

Must fix:
1. The trident butt floats ~0.15 above the floor. I measured min z of the Trident vertex group in the exported blend: 0.147 at idle f0, 0.141
   at the tap contacts f68/f80, and 0.146-0.163 at the slam f86-92. The feet sit at 0.000. That is ~0.6 stud at x1 and ~1.3 at x2.2, right
   where the spring VFX bursts, and the idle repeats it every 4 s. Cause: the guard pose (arm pitch -8 / elbow 12 + hold()) lifts the trident
   0.12 above its modelled butt (SHAFT[0] 0.03).
   Fix: slide the trident down through the fist by 0.145 along its shaft (a Trident location key, converted with the same R0^-1 @ Rh^-1
   step as the spin lift). Do this on every guard-pose key: all of idle (the 2 taps then lift off and land on the floor), roar f0/f60, and
   act_twirl f0-8 and f86-100.
   Target: Trident min z 0.00-0.01 at idle f0/68/80 and twirl f86-92, never below -0.005. Re-run step 1 + export; I'll approve on those numbers.

Animation (my own renders of the exported blend from tq/side/front; ground_min = 0.000 in every clip):
- idle SURFACE BREATH: the head lifts and gulps (jaw 26 at f22) and the chest swells, then 2 trident taps at 60-80. The band tails flutter.
- roar TRIDENT THRUST: a lunge step with the left foot and two thrusts at chest height, the trident levelled prongs-first, beak open 34-36.
- act_twirl: it raises the trident (0-12) and tips it flat (22). Then a 720 deg eased helicopter spin clear above the crown (22-60), with
  the left fist punching out on spin 2 (44-58). It catches the trident vertical and raises it high (66-80), drives it down in 6 frames
  with bent knees and a left stomp (80-86), then recovers proudly. Exactly the plan, except for the contact above.

Keep: the 1.15 H trident silhouette, the stacked plastron, and the coral war-band tails.
Optional polish: from behind (the view players follow), the dome's back is a flat square with thin bars, which reads a bit as a backpack.
Raise the keels to ~0.06 proud (plan: >= 0.03 H) and round the dome (top (0.62,0.66) -> (0.55,0.62), rnd 0.25 -> 0.35).
