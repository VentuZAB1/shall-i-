APPROVE 8/10 - at the Raiju's level. A low-headed bison with a real hump, a cape and ivory horns that reads at 64 px. The face is now a
bison (a nose pad and slit eyes under heavy brows), and act_charge is a clear, weighty bull behaviour. (Final gate, phase 2: model + all clips.)

Earlier must-fixes (fierce_verdict), all addressed:
1. Grazing head: FIXED. With HEAD_P -42 and HEAD_O (0,-0.92,0.63), model_side and close_side show the eye, the brow and the whole muzzle
   profile, with the nose ~45 deg down.
2. Cow face: FIXED. One dark nose pad with 2 slanted slits, and the muzzle tapers (bot 0.74,0.80). close_front reads as a bison.
3. Loose shards: FIXED. The short beard is rooted on the throat and continues the neck line. The brisket hem is 2 laid-back locks per side.
4. Box-on-box back: FIXED as specified. The hump is longer (half y 0.28), and the mane blends in and ends at mid-ribcage. A small flat cap still
   shows on the hump (polish 1).
5. Pencil horns: FIXED. nostud on the segs and spikes gives smooth ivory with dark tips.

Animation (my own renders of the exported _rigged.blend from tq/side/right side/front; ground_min = 0.000 in every clip):
- idle CUD & FLIES: the jaw grinds (yaw +-6) and the tail swats the left flank at f45 and the right at f90. Ear flicks, then a slow glare held at
  68-86. Unique.
- roar BROADSIDE BELLOW: it steps round 35 deg to show its flank with the tail raised stiff and the head low. The jaw opens 26 deg, the flanks
  pump twice, and it steps back.
- act_charge: the right fore-hoof reaches forward and drags back twice (f4-30, clear from its right side). It rocks back with the tail stiff
  (f36-40), lunges 0.15 (f48-52) and hooks the horns up and to its right (f57-62, head pitch -12, ~24 deg total yaw, roll 22). A snort at
  f76. Matches the plan, and it is the only hoof-scrape in the roster.

Optional polish (not blocking):
1. The hump block's narrow top (top=(0.34,0.42)) still reads as a flat cap in model_tq/back. Change it to (0.50,0.56) for one rounded mound.
2. The scrape and the rock-back are small for a 30-stud read. Hoof lift 0.09 -> 0.13; at f36-40, Spine y 0.07 -> 0.10 and pitch -4 -> -7.
3. At f36-52 the tail reads stiff but level. About 15 deg more tail pitch would sell "tail up" before the charge.
