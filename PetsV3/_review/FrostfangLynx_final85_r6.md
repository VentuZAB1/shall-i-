**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.**

# Frostfang Lynx - FINAL 8.5 GATE, round 6 (walk-only change) - 2026-10-28

Clip score is the floor of the four clips (owner rule): idle 8.5, walk 8.5, roar 8.5, act 8.5, so 8.5.

## Per-clip scores
| Clip | Score | Basis |
|---|---|---|
| Idle | 8.5 | Carried from round 5. Source and metrics unchanged (see below). |
| Walk | 8.5 | Re-scored. Knee step fixed, tail sway still passes. The lift check at game camera is the one open item (below). |
| Roar | 8.5 | Carried from round 5. Unchanged. |
| Act | 8.5 | Carried from round 5. Unchanged. |
| Model | 8.5 | Carried from round 5. No model lines changed. |

## What I looked at
- Brief, `GLACIER_REVIEWER_BRIEF.md`; round 5 review; `CLIP_NOTES.md` r6 section; `ANIM_REFS.md` (L0).
- Renders: `renders/_walk_sheet_r6.png` (f0-f27 every 3 f, game / side / tq rows), `renders/_walk_tail_r6.png` (1x and 2x, f8 vs f23), `renders/_walk_tail_r4.png` (round-5 comparison).
- An unlabeled full-size image came with the request (3600x1106). Its size matches `_walk_sheet_r6.png`, so I treated it as that sheet. I did not score from it separately.
- Source diff: `FrostfangLynx/_scratch/FrostfangLynx_f85r4.py` (the round-5 source) vs `FrostfangLynx_f85r6.py`. The live `pets/FrostfangLynx.py` is byte-identical to the r6 snapshot.
- Numbers: `_scratch/fullcheck.json` and `fc_r6.txt` (09:04), `_scratch/clipmetrics.json` (09:04).

## Nothing outside the walk changed
The diff touches only the walk: the walk docstring, new helpers `soft_lift` / `soft_target` / `soft_walk` (placed between `idle` and `walk`), and the walk body (n 24 to 30, bob phase and amplitude, lift 0.050 to 0.030, `cm.quad_walk` to `soft_walk`).
- `idle`, `roar`, `clawflex`, `rig`, `model`, `anim`, and the ear, ruff and bobtail helpers are unchanged.
- Idle, roar and act metrics match round 5 exactly: neck 5.63 / 4.0 / 7.36; chest vs spine 1.44 / 2.0 / 3.35; act local max 12.03.

## Walk verdict: 8.5, PASS
| Check | Round 5 | Round 6 | Result |
|---|---|---|---|
| Largest walk leg step, local | 12.45 (Shin_FR f6) | 5.49 (Shin_BR f5), bar 5.63 | PASS |
| Largest walk limb step, world | 7.8 | 5.57 | PASS |
| Tail sway, 1x / 2x | 26.9 / 55.5 px | 25.8 / 51.1 px (bar 15 / 30) | PASS |
| Loop seam, pos / rot | 0.0 / 0.0 | 0.0 / 0.0 | PASS |
| Slide / foot z variance | 0.0 / 0.0 | 0.0 / 0.0 | PASS |
| collision_free / ground min | true / -0.0 | true / -0.0 | PASS |
| Quaternion flips | 0 | 0 | PASS |
| Neck / chest vs spine | ~2 / 2.68 | 2.0 / 2.68 | PASS |
| Stride | 0.355 per 0.8 s | 0.393 per 1.0 s | PASS (lead ruling: speed follows distance travelled) |

- **Lift (0.030) and stalking vs shuffling:** the paws leave the floor through the 13-frame swing. The front paws curl under and land flat, and lift-off and touchdown have zero speed, so there is no knee flick. At sheet scale this reads as a deliberate cat step, not a shuffle. The panels are about 200 px, and I could not measure paw clearance in pixels at game camera. This is the one open check (NICE 1).
- **Tail counter-sway:** still reads. In the 1x game frames the black tip moves from the left of the rump (f8) to the right (f23). The sway is about 4% smaller than round 5 because the cycle is longer. It is still well above the bar.
- **Head nod:** the notes give peaks at f8.5 / f23.5, one frame after the front touchdowns. I did not re-measure it.
- **Revert?** No. The walk did not get worse on any gate, and the knee step and limb step are both smaller. Revert only if the game-camera check in NICE 1 shows shuffling.

## MUST
None. Nothing blocks 8.5.

## NICE (not counted)
1. Game-camera check of the 0.030 lift: a 1x pair at the paw apexes (about f15 and f22) in Studio. If it reads as shuffling, revert to the round-5 walk: `n = 24`, `cm.quad_walk` with lift 0.050, and the r4 body bob. Note that `LYNX_SOFT=0` is not a clean revert, because it keeps the 30 f cycle.
2. Remove the `LYNX_SOFT` env test switch from `pets/FrostfangLynx.py` before the final export.
3. The round-5 TO 9+ list still stands (head-nod vs the steady-head reference, fangs on TEETH, underside SNOW band, claw width). None is required for 8.5.

## Checklist
- Model 8.5: PASS
- Idle 8.5: PASS (unchanged)
- Walk 8.5: PASS
- Roar 8.5: PASS (unchanged)
- Act 8.5: PASS (unchanged)
- Walk gates (loop, slide, collision, ground, flips, leg step, tail): PASS
- Only walk lines changed: PASS
