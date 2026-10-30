# Bramble Badger - clip gate review 4 (2026-10-27) - SIGN-OFF (clips)

**Score: 8/10** for a 40 % starter. This meets the ship bar.

Review 3 asked for three edits, the evidence, and the reference notes. All of them are in, and the numbers check out.
No remaining MUST.

## Review 3 items - status

| Item | Status | Evidence |
|---|---|---|
| M-1 Roar hunker 0.10H, thorns -22, ears -28 | MET | `renders/_roar_vs_idle_side.png` (fixed side camera, idle f0 / roar f12 / f30 / f59). The body sits visibly lower at f12 and f30, the thorns lie flatter, and it returns to rest at f59. |
| M-2 Act opens with a paw, not the idle sniff | MET | 8 f nose-tap, no yaw, first scoop at f8. `pclose_side_act_burrow_04` shows a short tap, not the long sniff. Events dig1 16 / dig2 26 / dig3 36 / kick1 44 / kick2 53 match the code. |
| M-3 Look-around no longer a shake | MET | Reversal spread over 14 f. Max head yaw rate 2.99 deg per frame (act, `clipmetrics.json` `head_yaw_rate_max`). |
| M-4 Evidence and numbers | MET | Below. |
| N-1 Kick toe clear of the floor | MET | Toe up 7 deg. Lowest point -0.002 in every clip (`fullcheck.json`). |
| N-2 Kick lift at most 0.05H | MET | Lift 0.028. |
| N-3 Kick reads at game distance | MET | Shove 0.06. `pclose_side_act_burrow_44` shows the rear feet pushed back. |
| N-4 Side walk frame | MET | `pclose_side_walk_08`: no leg intersections. |

## M-4 evidence (`_scratch/clipmetrics.json`, `_scratch/clipmetrics.py`)

| Check | Result | Limit | Status |
|---|---|---|---|
| Quaternion sign flips | 0 (keys and sampled), all four clips | 0 | PASS |
| Max per-frame limb swing | 12.95 deg (act, Shin_FL f10) | 60 | PASS |
| Neck | idle 7.87, act 6.0, roar 7.0, walk 3.47 | 8 | PASS |
| Chest vs spine | walk 2.92, roar 1.5, act 1.25, idle 1.0 | 5 | PASS (notes now agree) |
| Head pitch-up (world) | act 6.25, others 0.0-0.2 | 30 | PASS |
| Head yaw per frame | act 2.99, idle 1.61, walk 1.06, roar 0.0 | (no shake) | PASS |
| Act end (f99, f100) vs f0 | 0.0 deg, 0.0 units | rest | PASS (exact) |
| Roar end (f59) vs f0 | 0.21 deg, 0.0003 units | rest | PASS (within 0.5 deg) |
| Idle loop (f120 vs f0) | 0.0 deg; f119 0.63 deg on Tail1 | closed | PASS |
| Walk loop (f30 vs f0) | 0.0 deg | closed | PASS |

Two small notes, neither a fail:
- The head pitch-up max is 6.25 in the JSON. The message said "up to 8.0". The JSON value is the one to quote.
- The roar's end is 0.21 deg off frame 0, not exactly zero. It is inside a 0.5 deg tolerance.

## Full check (`_scratch/fullcheck.json`)

- `collision_free`: true, `collisions`: {}.
- `ground_min_z`: idle -0.002, walk -0.002, roar -0.002, act_burrow -0.002. All pass the -0.02 limit.
- Audit: linear 0 in every clip. Loops closed. Walk slide 0.0, foot_z_var 0.0.
- Tris: 4,956 (cap 15k).

## References

`ANIM_REFS.md` lists the animationreference.org tags tried, with no dig, burrow, badger or quadruped tag. The site's
walk clip (D) is cited. The other three are Sakugabooru studies, the same route as the 2026-10-14 spider precedent.
**PASS.**

## Minor, for the next pass (not blocking)

- The kicks are small at game distance. They pass, but a stronger shove would help. Optional.

## Sign-off

The Bramble Badger clip gate is passed. The model and the clips are cleared for the Studio import. Keep the pose-sheet
set with the pet's build record.
