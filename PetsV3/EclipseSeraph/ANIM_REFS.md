# Eclipse Seraph - animation references (owner rule: references before keying), clip round 2, 2026-10-28

Method (lead ruling): animationreference.org TAG page -> the site item -> step the frames of that same item on its
Sakugabooru source with canvas contact sheets (seek + draw; times in seconds; our clips run at 30 fps, so frames =
s x 30). I mapped each item to its post by the preview md5 on the tag page and Sakugabooru's `post.json?tags=md5:`.
**This used no site opens** (the counter stayed at 3/25).

**Multi-pair wing search, logged** (as in the spider precedent). I looked for a four- or six-winged flyer to set the
lag between the pairs. I searched `/tags/wings` (12 clips: Pokemon, a few birds), `/tags/angel` (15: mostly the
"Angelkade" FX tag), `/tags/butterfly` (7: particle FX), `/tags/bird-flight` (1: the flapping tutorial),
`/tags/flying` (all 326) and `/tags/dragon` (219). None has a multi-pair wing flyer. The 4 f lag between the pairs
therefore comes from the plan. Its timing rules (the arm leads, the tip trails, the strokes chain) come from the site
bird references below.

| # | site tag page -> site item title | Sakugabooru post | used for | frames read |
|---|---|---|---|---|
| H1 | `/tags/flying` (page 2), also `/tags/the-boy-and-the-heron` and `/tags/animals` -> "Akihiko Yamashita: Character Acting & Creature Animation (BD - Animals)" | #260630 (*The Boy and the Heron*) | **cascade**, **fly**, takeoff, land, roar | **THREAT DISPLAY 29.6-34.0 s** (cascade + roar): the wings rise and spread around the body (29.6 -> 31.0 s, ~1.4 s = 42 f), then HOLD (31.8-33.3 s) with the head level and still. The beak opens only after the spread. **TAKEOFF WINGBEAT 97.0-99.0 s** (fly + takeoff): 97.5 the wings high (top), 98.0-98.5 the downstroke (~0.5 s), 99.0 spread again. Gather to spread is ~1.0-1.2 s per heavy beat at lift-off. **LANDING 12.6-17.0 s** (land): 12.6 glide, wings spread wide; 13.4-13.8 the legs reach and the wings rise to brake; touch ~14.1 s; 14.2-16.6 the wings come down to half; 17.0 folded. |
| R5 | `/tags/bird-flight` -> "Bird Flight Animation Tutorial - Flapping" | - | fly, cascade ripple | The arm leads and the hand trails by 2-3 f; the outer wing half-folds on the upstroke. **Cascade:** the plan asks for a tip-to-root ripple, so the hand rises first and the arm follows 6 f later (R5 reversed). |
| E1 | `/tags/flying` (page 4) -> "Flying: Character Acting & Creature Animation (BD - Takeshi Honda)" | #236985 (*Tales from Earthsea*) | takeoff, land flare | 13.6-14.8 s: the creature breaks from the water. The wings open full with the forelegs reaching ~0.4 s later (14.4), then it passes over, legs trailing. 36.8-38.8 s: an upright hover with the wings spread wide and the forelegs reaching (the brake pose). |
| C1 | `/tags/walk-cycle` (page 4), also `/tags/the-cat-returns` -> "Animals: Character Acting & Creature Animation (BD - Crowd)" | #256671 (*The Cat Returns*) | walk | 16.79-17.71 s, side view: near hind ~17.0, near fore ~17.2, far hind ~17.4, far fore ~17.6. That is a LATERAL-SEQUENCE walk with a ~0.8 s cycle, head and back level, tail carried. |
| W0 | `/tags/wolfs-rain` -> "Animals: Character Acting & Creature Animation (#30 - Wolfs Rain)" | #174333 | roar hold | The mouth opens over ~15 f, then holds with the head still. |
| D3 / D5 | ANIM_REFERENCES_1014 #8 (banshee flight) / #3 (Sea Beasts roar), site studies | - | fly timing / roar | One stroke ~0.8-0.9 s, the head stays level, the tail streams. The jaw opens ~12 f after the head lift starts. |

## How each reference maps to the clips (30 fps)
- **fly (28 f loop):** D3 cruise timing (28 f) plus H1's wingbeat shape and R5's arm-leads rule. **Three separate
  strokes:**
  - upper pair 46 -> 18;
  - middle pair 28 -> 2, **4 f behind** the upper;
  - lower pair 20 -> 4, **4 f behind** the middle (8 f behind the upper).
  The three pairs reach their tops at f0 / f4 / f8 and their bottoms at f13 / f17 / f21, so a wave runs from the front
  pair to the back pair on every beat (no lock-step).
- **act_wingcascade (110 f, signature):** H1 29.6-34.0 (the wings spread around the body over ~1.4 s, then a still hold
  with a locked head). Each pair does a tip-to-root ripple (R5 reversed: hand first, arm 6 f later):
  - upper pair f14-28 to 54 (`ripple1` f22);
  - middle pair f30-44 to **28** (`ripple2` f40);
  - lower pair f44-58 to **20** (`ripple3` f54).
  All three tiers HOLD f58-64 (H1 31.8-33.3: the head still). The reverse ripple runs f64-94 (lower first).
- **takeoff / land:** H1 + E1 as above. Crouch, `launch` f11, legs tuck; flare, `touch` f16, absorb, fold back to the
  display fan.
- **walk:** C1 lateral sequence, level head (`cm.quad_walk(..., gait="walk")`).
- **roar:** H1 order (spread first, then the call), D5 jaw lag, W0 hold. The halo lifts 0.20 and tilts 17 at the peak.
- **idle:** H1 stillness. The wings breathe as a chain: upper, then middle 4 f later, then lower 4 f after that.
