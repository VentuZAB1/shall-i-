APPROVE - 8.5/10 vs the Raiju and the refs (FINAL gate: model fixes + all 4 clips).
At 64 px it reads as a tank: a keeled dome, a saw rim and a hooked snapper beak. The signature is the clearest behaviour
act in the set. It is at or above the Raiju's level.

PHASE-1 MUST-FIXES: all 6 done.
1. Shell mouth: the cavity (x +-0.30, back wall y -0.24, roof z 0.88), the split MID, 2 cheek tiles and the hood at the
   top edge are in. The front view shows the head framed in a dark arch under the hood.
2. Head profile: skull top (0.50, 0.42), jowl cheeks, the jaw is SKIN with a 0.012 PLAS strip. It is a wedge now.
3. Brow (0.11, 0.05, 0.042): a ledge over the lime slit in close_side.
4. Moss: tufts scaled up, plus 2 in the back half. The back view carries 5 lime chunks.
5. SHELL_L (176, 158, 100): the ridge rows separate from the scutes.
6. Tail: SKIN_D rod with SHELL_L spikes.

CLIPS (checked _pose_tq_sheet, _pc_sheet and the code)
- idle DOZE: the chin sinks to the ground, the lids really close (pc f50), and one lid cracks open at f74 and shuts again.
  Unique and calm.
- roar STAND TALL & HISS: the legs straighten, the neck shoots out, a red gape with a jaw tremble, one snap. The
  0.045 rise + 4 deg tilt (builder deviation, the columns' reach) is accepted. It reads.
- act_hide (signature): it startles, the neck slides fully in, the scaled forelegs swing across the mouth and the
  plastron thuds down. It holds and rocks, then peeks out under the hood, looks L/R, snaps back in and emerges. Exactly
  the owner's "hiding inside its shell". I checked the evaluated mesh at f40: the retracted neck ends at y 0.693, inside
  the back shell wall plus the scute tiles. Nothing pokes out of the back.

OPTIONAL POLISH
1. From directly behind the tail still reads a little like a pale-runged ladder. Either use 3 larger spikes (0.09, 0.075,
   0.06) or colour the spikes SHELL instead of SHELL_L.
2. Head/Neck vs Spine is not in check_pairs (on purpose, for the retract). If the hide timing ever changes, re-check
   the back view at the hold frames.
