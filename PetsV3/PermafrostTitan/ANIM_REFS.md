# Permafrost Titan - animation references (owner rule), 2026-10-27

## Search log (animationreference.org first)
- **animationreference.org** (counter 4/25 -> 3/25 during my session, shared with the other three builders): browsed the
  free tag pages `/tags` (no golem / giant / titan / kneel tag; "giant" = anime titles only), `/tags/walk-cycle`,
  `/tags/body-mechanics` (79 clips, titles are only film names), `/tags/creature`, `/tags/dragon` (Dragon Ball beams).
  The free curated **locomotion guide** (`/resources/locomotion-animation-reference`) lists **Muybridge, Animal
  Locomotion I, Plate 27 "Man walking and carrying a 75 lb stone on head"** - the exact heavy-load walk I need. It is a
  still sequence hosted on Wikimedia, so it cost **no clip credit**. I spent no clip credits (none of the paid clips
  matched by title; I left the last ones to the other builders).
- **Sakugabooru:** tag search `snake*`, no general tags for my animals; nothing for a kneel either.
- **Fallback, frame-by-frame plates (brief: "Muybridge plates"):** Muybridge 1887 **Plate 356 "Man kneeling, firing
  and rising"** (Wikimedia Commons, rbm-QP301M8-1887-356), three camera rows (front 8 frames, side 7, rear-3/4 6).
- **Reused** from `_review/ANIM_REFERENCES_1014.md`: #3 *Sea Beasts* heavy-head roar (the jaw lags the head lift),
  #9 *Children of the Sea* (a heavy mass rises fast and settles 2-3x slower, no bounce).

## A. Plate 27 - heavy-load walk (12 frames studied as a contact sheet)
| # | observation | frames |
|---|---|---|
| W1 | **Wide stance at contact**; the front foot lands almost flat (very little heel strike), the rear leg still straight. | 1, 6-7, 12 |
| W2 | **Down right after contact**: the support knee flexes and the body sinks; the load stays level. | 2-3, 8-9 |
| W3 | **Passing is low**: the swing foot just clears the ground (no high knee). | 3-4, 9-10 |
| W4 | **Torso stays vertical**, no twist; the weight rolls over the stance foot (small lateral shift). | all |
| W5 | **Arms do not swing** (they hold the load): for a giant with massive arms, a tiny swing (plan: 4 deg). | all |

## B. Plate 356 - kneel and rise
| # | observation | frames (row) |
|---|---|---|
| K1 | **The front foot steps forward first**, then the body drops straight down; the rear knee lands under / behind the hips, the rear toes tuck under. | front 2-3, side 1 |
| K2 | **The kneel hold**: front shin vertical, front thigh about level, torso upright, the rear shin lies back on the ground. | front 3-6, side 2-5, rear 1-4 |
| K3 | **The rise starts with a FORWARD lean** (about 15-20 deg) to load the front foot, then the front leg drives up; the rear leg follows through. | side 6-7, rear 5-6, front 7-8 |
| K4 | Descent and rise take about the same number of frames; the hold is the long part. | all rows |

## C. Kaiju No. 8 - heavy creature weight (lead's site cuts, added 2026-10-27 after the clip gate)
**Added after the keys were set** (the walk, roar and kneel were keyed on A / B and the 1014 refs). The lead's ruling then
applied one change from this section: the K8a kneel settle (f18-23).
Found on the site's free tag page `/tags/kaiju-no-8` (6 clips; no clip credit spent). I stepped the frames on the
Sakugabooru source posts (the same mp4 the site player streams) as canvas contact sheets in the browser. Nothing was
downloaded. Anime frames are at 23.976 fps; the 30-fps equivalent is x1.25.
- **#257646** (Sakugabooru tags `proro`, `kaiju no. 8`, `3d background`, `cgi`, `creatures`, `fighting`; Source #07). It is
  a CGI fight cut, not the Yuya Takahashi cut the lead's note names.
- **#254909** (tags `yuya takahashi`, `artist unknown`, `kaiju no. 8`, `character acting`, `creatures`; Source #01,
  CAD/AD Tetsuya Nishio). This is the site's "Kaiju No. 8: Character Acting & Creature Animation (#01 ... Yuya Takahashi)".

| # | observation | time / frames (24 fps) |
|---|---|---|
| K8a | **Landing into a hold.** Close-up: the feet and hand hit the street with a dust burst. Wide shot: the kaiju sits in a low three-point crouch, settles ~3 frames, then holds visually still for ~1.5 s (36 frames = ~45 f at 30 fps). Only the dust moves. | #257646 8.25-8.45 s (f198-203) impact; f204-207 settle; f207-243 hold (8.6-10.1 s) |
| K8b | **Tuck, lift, lock.** The head is bowed (horns forward, eyes down) and held ~4 frames. It lifts to level in ~4-5 frames (= ~6 f at 30 fps), the eyes lock on the camera, and then it holds still for ~0.9 s. The glowing lines carry the hold. | #257646 f243-247 tuck, f247-251 lift, f251-272 hold (10.14-11.34 s) |
| K8c | **Weight by stillness.** After the transformation the kaiju looks at its raised fist almost motionless for ~5 s (only small fist turns). The head turns from profile to the camera slowly, over ~3.3 s. No snaps: the size reads through slow, minimal motion and the glow. | #254909 15.8-21.3 s (fist), 24.6-28.0 s (head turn) |

**Fit:** these cuts fit the roar hold and the kneel hold. They do not show a rise: #257646 cuts out of the crouch, so K3
(Plate 356) stays the source for the rise itself.
- **roar:** K8b matches the beat order: tuck f0-10, lift f10-22, a still hold f22-50 (28 f = 0.93 s, K8b ~0.9 s), with
  the core pulses carrying the hold (K8c). My lift takes 12 f, which is slower than K8b's ~6 f. I kept the slower lift
  for the giant's mass (#9). If the reviewer wants more snap, the lift can go to f10-17 without other changes.
- **act_kneelrise:** K8a backs a still kneel hold (f18-50 = 1.07 s; only a 0.006 BU breath and the core pulses). The
  landing currently eases in (smoothstep into f18). An optional polish from K8a is a 3-frame settle after the knee lands
  (overshoot ~0.01 down at f20, back by f23). It is not applied yet: the clips under review stay unchanged.
- **idle:** K8c supports the low-motion idle (hip yaw +/-3 deg, 1-deg breaths, the head level).

## How each clip uses them
- **walk (48 f loop): heavy stride (W1-W5).** Contacts at f0 / f24 with a flat foot (toe 0), duty 0.62 (long stance =
  heavy); the pelvis drops 0.035 BU 4-6 f after each contact (W2) and rises at passing; the swing foot lifts only 0.07
  (W3); the pelvis shifts 0.025 over the stance foot (W4); arms swing 4 deg (plan, W5); the chest counter-yaws 2 deg;
  the head stays level.
- **idle (120 f loop): weight shift** (plan; final-8.5 numbers): hip yaw +/-4 deg over one cycle, breathing (chest 2 deg,
  body sink 0.015), the shoulders (pauldrons are on the Arm bones) settle 2 deg at f30 and f70, a slow +/-8 deg fist
  flex (60 f), `core1` f40 / `core2` f100. No head tilt.
- **roar (66 f): core bellow (#3 + #9; final-8.5 numbers).** f0-10 anticipation: the head tucks 4 deg and the chest
  compresses; f10-22 the body pushes forward (Spine -4, Chest -7 world), the head lifts 15 deg, the arms go out 22 deg
  (24 at f34), `core1` f22 (+ `glint` f22 on the Hero bezel, `icedust` f24 on the fists); the jaw opens LATE (24 deg at
  f27, #3); hold f22-50 with `core2` f34; f50-66 a slower settle back to rest (#9).
- **act_kneelrise (100 f): K1-K4 + K8a + #9.** (Final 8.5 round 2: MIRRORED - the left knee goes down and the
  right foot steps forward; read left / right swapped below.) f0-9 the left foot steps forward 0.30 and 0.04 out (round 4); f6-18 the body drops
  0.272 and rolls 7 deg toward the kneeling side (round 4, the chest and head counter-roll), the knee settles 0.008 at f20-23 (K8a)
  and the right knee lands (`icecrack` f18 on `Knee_R`), the right toes tuck, the head bows 12 deg, the fists come to
  rest just above the thighs; f18-50 the kneel hold with `core1` f30 / `core2` f44 (fists never touch the ground);
  the right foot turns 10 deg out in the hold and the elbows bend 30 (final 8.5);
  f50-58 the forward lean (K3, spine 10 deg + chest 4) then the front leg drives up (f58-76); f70-79 the left foot steps back;
  f84-100 exact rest pose.
