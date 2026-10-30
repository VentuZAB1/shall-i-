# Bramble Badger - animation references (owner rule), 2026-10-27

animationreference.org had 6/25 clip opens left today, and its tag pages have no dig, sniff or quadruped tags. So I
studied the **source clips on Sakugabooru** (the site's free source host). For each one I built a canvas contact sheet
of the post's own mp4 in the browser and stepped through it at 0.2-0.25 s. Clips run 24 fps; our clips are 30 fps
(frames = s x 30). The footage is study reference only: timing, spacing and poses.

**Tags tried on animationreference.org (clip review 3 follow-up):**
- `/tags/animals`, `/tags/walk-cycle`, `/tags/cartoon-animals`, `/tags/creature-animation`, `/tags/muybridge`;
- the site tag index searched for dig, badger, burrow, sniff, quadruped, growl and crouch. There is no dig, burrow
  or badger tag, and `/tags/quadruped` returns a 404.

D (the walk) is the site reference. The dig, sniff and hunker come from Sakugabooru, because the site has no such
clips.

| # | Clip | Used for | Key poses and timing |
|---|---|---|---|
| A | **The Pointer** (Disney 1939, Pluto), Sakugabooru #258150, Ollie Johnston / Lynn Karp, 8.0-10.8 s | idle "nose-down sniff", act beat 1 (sniff) | Pluto tracks with the **nose pressed to the ground, front end low, rump high**. The head never leaves the ground for long. The nose makes small lifts (~10-15 deg) and sideways sweeps every **0.4-0.6 s (12-18 f)**. It travels up the tree base 9.4-9.6 s and back down 9.8-10.0 s, then follows the ground sideways 10.2-10.8 s. The body stays still while the head works; the ears hang. |
| B | **Pluto and the Gopher** (Disney), Sakugabooru #143881, Hugh Fraser, 50.0-52.75 s | roar "hunker growl" | **Drop (0.5 s, 15 f)**: the shoulders sink first and the head pushes forward and low; the rump follows late. **Hold low (~1 s, 30 f)** with the head thrust forward and level, a small tremble. Then a **compress** (51.75-52.25 s), the whole body lowest, before the release. The rise is slower than the drop. |
| C | **Once Upon a Forest** (1993), Sakugabooru #282941, David Feiss, 9.2-12.0 s | act_burrow scoops + dirt timing | The digger dives in with **alternating forepaw strokes, ~0.2 s (6 f) per stroke**. The dirt flies back over the shoulders on each stroke (the VFX event frame = the paw's backward sweep, not the contact). The head stays low over the hole, and the rump rocks with each stroke. |
| D | `_review/ANIM_REFERENCES_1014.md` #4, **Dragon Walk Cycle** (C. Sophocleous) | walk "waddle-trot" | Diagonal pairs (FL with BR). The head dips on each front-foot contact (2 dips per cycle) with a small lag. A stocky body **rocks** side to side, a roll toward the planted front foot. |

## How each clip uses them
- **idle (120 f loop), "nose-down sniff"** (ref A), as built (round 4, 2026-10-28):
  - f0-20: head and neck pitch down to the ground (Neck 7.5 + Head 15.5 deg; neck max 7.87, within the 8 limit).
  - f22-80: three sniff sweeps: yaw +8 / -8 / +5 deg (peaks f36 / f52 / f68).
    - Between the sweeps the nose lifts **10 deg** (`-10*lf`, peaks f34 / f52 / f70), in ref A's 10-15 deg range.
    - The body follows each sweep with a **3.5 deg Spine roll** (`3.5*yw/8`). The shoulders lower 0.01.
  - **Ear twitch:** a 6 f triangle at each sniff peak (f33-36-39, f49-52-55, f65-68-71), plus one at f111-114-117 with the head back up (r5). Each one is 8 deg forward plus **28 deg outward**; the outward flick is what reads from the game camera behind the badger.
  - **Ear and tail flicks:** a 16 deg ear flick and a 14 deg tail flick at f40-52 and f96-108.
  - **Crest bristle:** f64-88, peak f70-78. The thorns lift **5 deg**, each on its own bone.
  - **Breathing all loop long:** 3 breaths per 120 f, peaks f10 / f50 / f90. The Spine rises ±0.023 (r6, about ±0.24 studs), and the Chest-carried mantle rides with it (no Chest breath pitch since r4). The head pitches `+3.35*b`, so the nose holds still.
  - f80-110: the head lifts back to rest, slower than the drop. f110-120: settle on rest. No head shake.
- **walk (30 f loop)** (ref D): diagonal pairs, short stride (0.075 half), soft feet (r6: the paws leave and land at zero speed, the lift eases in and out). The body is carried 0.010 lower and bobs 0.020, LOWEST at each touchdown (f0 / f15: weight acceptance), and rolls +-4 deg toward the planted front foot. The head dips 2 deg twice per cycle with a small lag. The stub tail flicks late (10 deg), and the crest ripples 2 deg.
- **roar (60 f), "hunker growl"** (ref B):
  - f0-15: drop. The root goes down **0.10H** (`drop = 0.10*H_U`, as 0.6 x shoulders + 0.4 x rump) and 0.012 forward.
    - The shoulders lead (f0-12), the rump lags 3 f (f3-15).
    - The thorns flatten back **22 deg** and the ears go back 28 deg (f0-12, held to f46).
  - f8-45: hold low. The neck pitches down 7 deg and the head up 4 deg, so the face stays level and forward (f0-22).
    - The jaw opens 1.5 -> 24 deg over f18-28 and holds to f42 (event `growl` f30).
    - A **2.5 deg** tremble runs f24-42 (period 4 f), on the jaw and 0.4x on the head. The tail tucks 8 deg.
  - f45-60: rise, slower than the drop; the jaw closes by f52 and the thorns come back by f56; exact rest at f60.
- **act_burrow (100 f, in place)** (refs A + C; clip review 3 M-2 and M-3; r6: each scoop lifts 0.035 (0.056H) so it
  reads at 2x, and touches down):
  - f0-8: a quick nose-tap on the spot. The head dips 7.7 deg (+3.6 deg neck) at f4 and eases back to a third of that at f8; then it settles low over the hole by f14. This is no longer the idle's long sniff.
  - f8-38: three scoops, L / R / L, each 10 f. The act opens with the paw. The events `dig1` f16, `dig2` f26 and `dig3`
    f36 fall on each backward sweep (ref C: the dirt flies on the sweep). The head stays low over the hole and the rump
    rocks with each stroke.
  - f41-59: hind kicks (BL f41-50, BR f50-59), `kick1` f44 and `kick2` f53. Each foot shoves back **0.070** and lifts **0.035** (r6) with the toe up (3 f),
    touches down at 0.058 (f+5), then steps home with a 0.012 lift (f+7 -> f+9).
  - f56-61: the head pops up. f60-68: a slow look right (+14 deg); f72-86: a slow look left (-14 deg, 14 f); f90-98: back
    to centre. This is no head shake: the world head yaw is at most 3.0 deg per frame. The thorns lift 3 deg and ripple 1.5 deg
    during the digging (f8-59).
  - f98-100: the exact rest pose.
