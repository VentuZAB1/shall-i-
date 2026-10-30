# Cinder Overlord - animation references (owner rule), 2026-10-27

## Search log (animationreference.org first)
- **animationreference.org** (counter 4/25 -> 3/25 during my session, shared with the other builders): the tag list
  `/tags` has **no snake, serpent, naga or coil tag**; `/tags/dragon` (219) is Dragon Ball beams; `/tags/creature`
  titles are generic. No clip credits spent.
- **Round 4 (review 3 MUST 1), the site clip:** I read the free tag pages `/tags/creature-animation` (2,414 clips),
  `/tags/animals` (540), `/tags/creature`, `/tags/dragon` (217), `/tags/sea-beasts` (3), `/tags/walk-cycle` (369) and
  `/tags/body-mechanics` (76) from their page data (title, tags, Sakugabooru post). I searched them for snake, serpent, eel,
  worm, naga, orochi, Shenron, Haku and eastern dragon. The only serpentine body on the site is **Haku, the white dragon in
  *Spirited Away***: `/tags/creature-animation` -> Sakugabooru **#225387**. `Kanada Dragon` is an effects style, not a dragon.
  The `/tags/dragon` clips are Dragon Ball / Kanada beams, and the `body-mechanics` clips are site-hosted only (they cost
  opens). I stepped the frames on the Sakugabooru post (the same mp4 the site player streams) as canvas contact sheets.
  **No site opens were spent**, nothing was downloaded. The Wikimedia snake clips (S1, S2) stay as study notes.
- **Sakugabooru:** tag search `snake*` returns no tags.
- **Fallback, real footage (Wikimedia Commons, studied as frame contact sheets in the browser):**
  - **S1** `Snake on a beach.webm` (104 s), a slithering snake on sand, **53.0-56.6 s** sampled every 0.2 s.
  - **S2** `Snake-cobra.gif` (150 frames, 5 s), a reared king cobra facing the camera, every 10th frame.
- **Reused** from `_review/ANIM_REFERENCES_1014.md`: #3 *Sea Beasts* heavy-head roar (head drop/tuck, lift, the jaw
  opens ~0.4 s AFTER the lift starts), #6 *Monsters University* (compress, then the display spreads in 5-7 f),
  #9 *Children of the Sea* (a heavy mass rises fast, settles 2-3x slower, no bounce).

## D - SITE: Haku the river dragon (*Spirited Away*), Sakugabooru #225387
Tags `spirited_away`, `takeshi_inamura`, `yoshihiro_osugi`, `creatures`, `flying`, `cgi`, `3d_background`; 47 s,
23.997 fps. Haku is a long-bodied eastern dragon, the closest thing on the site to a serpent body.

| # | observation | frames (24 fps) |
|---|---|---|
| D1 | **The bend travels head -> tail.** Low over the ground, the head and neck stay on a straight, level line. A big arch forms just behind the forelegs and runs back along the body, leaving the front straight again. The bend takes ~16-20 frames (~0.7-0.8 s) to pass along the visible body. | f146-f186 (arch forms f154, peaks mid-body f162, gone to the rear by f178) |
| D2 | **Gliding side view:** smaller humps keep running from the neck to the tail while the head holds its line. The amplitude is smallest at the neck and largest mid-body to the rear. | f636-f680 (sampled every 4 f) |
| D3 | **The head holds still while the body moves.** In the riding close-up the head stays level, the gaze locked forward, and the motion is in the body and mane behind it. No head bob or shake. | f696-f760 |

**Disclosure (review 4):** Haku is a **flying eastern dragon, not a ground snake**. His bends are mostly vertical (in the
air), while the Cinder's slither bends sideways on the ground. What I took **from Haku**: the bend running head -> tail,
the head held on a level line while the body moves (D1-D3), and the amplitude growing from the neck back. What came
**from the Wikimedia snake study** (S1, S2): the bend being LATERAL and staying put on the ground while the body slides
through it (U1), the ~1.5-2 s pace (U4), the reared cobra neck with the level gaze (C1), and the tail flick as the only
fast move (C2).

**Use:** D1 + D2 back the slither: the wave runs head -> tail with a lag per bone, the amplitude grows to mid-body (U2),
and the reared neck counter-yaws so the head stays on its line. This also backs the lead's ruling on the head -> tail
direction. D3 backs the idle: the breaths and sway live in the neck and body while the head counter-pitches and
counter-yaws to stay level (C1). The slow, minimal-motion idle also matches the site's *Kaiju No. 8* K8c (#254909,
cited in the Titan's ANIM_REFS): weight reads through stillness.

## S1 - lateral undulation (sand) (Wikimedia study notes)
| # | observation | time |
|---|---|---|
| U1 | The bends **form near the head and travel back along the body** while the body slides forward through them; each bend stays almost fixed on the ground. | 53.0-56.6 |
| U2 | The **amplitude grows from the neck to the mid-body**; the tail tip trails in the same track. | all |
| U3 | The head stays on a smooth line and only yaws into each new bend (about +/-10 deg). | 54.6-56.0 |
| U4 | A slow slither forms a new bend about every 1.5-2 s. | all |

## S2 - reared cobra (Wikimedia study notes)
| # | observation | frames |
|---|---|---|
| C1 | The reared neck **sways slowly** a few % of the head width left / right and up / down; the head stays LEVEL with the gaze locked. | 0-150 |
| C2 | Tongue flicks are the only quick motion (f30, f50, f100); everything else is slow. | 30, 50, 100 |

## How each clip uses them
- **slither = the "walk" clip (48 f loop, D1-D2 + U1-U4).** A yaw wave on Spine -> Body1-4 -> Tail1-4 that travels from the
  front to the tail (each bone lags the one in front by 3 f), amplitude growing to mid-body then easing to the tip (U2);
  the reared neck carries a small counter-sway so the head stays on its line (U3, C1); the forearms paddle 6 deg (plan).
  NOTE: the plan text says "from the tail to the head"; real lateral undulation (U1) runs head -> tail, and a
  tail -> head wave reads as swimming backwards, so the wave runs head -> tail.
- **idle (120 f loop): ember breathing (D3 + C1, C2).** Slow breathing: the neck rises 9 deg and sinks back (each neck bone
  3 deg, final 8.5), a small sway with the head level (C1), `smoke1` f30 / `smoke2` f90 for the vent smoke; one quick tail
  flick 8 deg at f80 (C2 timing: the only fast move), `flick` f80.
- **roar (66 f): crown flare (#3 + #6).** f0-14 the neck gathers (pitch-up 12 deg total, head held level); f14-26 the
  five crown blades tilt out and up 15 deg with a 2-frame lag each, `flare` f20; f26-44 the jaw opens late (#3), the
  forearms spread, `roar` f30; f44-66 the jaw closes and the blades settle back slower (#9).
- **act_molt (110 f): the crown sheds (#9 + U1).** f0-18 the neck arches 22.5 deg pitch-up in total (7.5 per bone,
  round 4), head level. f12-34 the blades lift one by one (3-frame lag): the four outer blades 45 deg, the centre 35 (final 8.5); blade 1 is
  fully up at `lift1` f22. f40-62 the centre
  blade lifts furthest and holds while the outer blades drop back, `lift2` f48, `shed` f56. f62-86 a ripple runs tail -> head
  along the body (plan; 6 deg per body / tail bone, the Spine 4.5). f84-110 the blades reseat in reverse order, slower than
  they rose (#9): the centre blade takes 16 f (f84-100), the outer blades end at f108 (final 8.5). Exact rest.
