# Blizzard Roc - animation references (owner rule: references before keying), current to clip round 6 (review 8 walk; rounds 3-6 = reviews 5-8; passed review 9), 2026-10-28

Method (lead ruling, review 4): animationreference.org TAG page -> the site item -> step the frames of that same item
on its Sakugabooru source with canvas contact sheets (seek + draw; times in seconds; our clips run at 30 fps, so
frames = s x 30). I mapped each item to its post by the preview md5 on the tag page and Sakugabooru's
`post.json?tags=md5:`. **This used no site opens** (the counter stayed at 3/25).

**Round 1's R1 (#260711) and R4 (#260644) are NOT on the site.** I scanned every page of `/tags/flying` (326 clips),
`/tags/the-boy-and-the-heron` (10), `/tags/animals` (541), `/tags/character-acting` (3,651) and `/tags/walk-cycle`
(370), plus 60 pages of `/tags/creature`; neither post is listed. I had found them by searching Sakugabooru
directly. They are now supporting references only, and the site item H1 below carries their beats: its own takeoff
replaces R1, and its wading walk replaces R4.

| # | site tag page -> site item title | Sakugabooru post | used for | frames read |
|---|---|---|---|---|
| H1 | `/tags/flying` (page 2), also `/tags/the-boy-and-the-heron` and `/tags/animals` -> "Akihiko Yamashita: Character Acting & Creature Animation (BD - Animals)" | #260630 (*The Boy and the Heron*) | takeoff, land, roar, act_bow, walk, idle | **TAKEOFF 97.0-99.0 s** (replaces R1): 97.0 wings half-open at the sides; 97.5 the wings rise high (the gather); **98.0 push**, the legs leave as the downstroke starts; 98.5 the bottom of the downstroke; 99.0 airborne, wings spread, legs dangling. **LAND 12.6-17.0 s**: 12.6-13.0 glide head-on, wings spread, legs hanging; 13.4-13.8 the legs reach forward and the wings rise high behind (brake); **touch ~14.1 s**; 14.2-16.6 the landing runs out as the wings come down to half; 16.2-17.0 the body sinks low and the wings fold. **THREAT DISPLAY 29.6-34.0 s** (R2): the wings rise and spread around the body, the head stays still and eyes locked, and the beak opens only after the spread (~1.5 s later). **HUNCHED DROOP 44.0-51.6 s** (R3): 45.3 the head and neck lower and the body hunches; 46.5-49.1 the wings hang half-open and drooped with small shudders; 50.4-51.6 the bird rises and the wings lift. **WADING WALK 17.85-20.85 s** (replaces R4): a step every ~0.5 s (cycle ~1.0 s). The HEAD stays at one height and angle while the body moves under it (gyro head). |
| E1 | `/tags/flying` (page 4) -> "Flying: Character Acting & Creature Animation (BD - Takeshi Honda)" | #236985 (*Tales from Earthsea*) | takeoff support | 13.6-14.8 s: a winged creature breaks from the sea (14.0). The wings open full with the forelegs reaching ~0.4 s later (14.4), then it passes over, legs trailing (14.8). |
| R5 | ANIM_REFERENCES_1014 #5 (site study), "Bird Flight Animation Tutorial - Flapping" | - | fly, takeoff, land | The arm leads and the hand trails 2-3 f. Primaries spread on the downstroke and the outer wing half-folds on the upstroke. The body rises on the downstroke, and the tail fans and lifts to brake. |
| (R1) | supporting only (not on the site) - **not used by any clip** | #260711 | (H1 carries the takeoff) | 4.0-9.0 s: run, wings off the body and raised behind, launch at 6.7 s into a high V, then the first deep downstroke. |
| (R4) | supporting only (not on the site) - **not used by any clip** | #260644 | (H1 carries the head holds) | 59.5-62.0 s: a quick head turn (~0.8 s) and then a HOLD. Not a sweep, never a shake. |

## How each reference maps to the clips (30 fps)
- **idle "frost shed" (120 f loop):** head turns as quick 8 f moves plus long holds (H1's still, locked head),
  yaw +-10. Wings FOLD -> LIFT1 -> BREATH (f10-40) with tip shivers. Event `frostshed` f24. Tail lowers 6 (f60-84).
  One talon re-grip per foot. **The net foot drift at the loop end is 0** (loop_pos 0); the 0.052 audit value is the
  peak height during a re-grip.
- **walk (36 f loop = 1.2 s):** H1 wading walk 17.85-20.85 s. **Head-thrust check (review 8 W3), stepped on
  2026-10-28:** I stepped the #260630 source at 1/24 s from 17.85 to 20.85 s and tracked the heron's head (the
  front-most white pixel of its top 14 rows, 886 x 480 frame).
  - The drawings change every 3 frames (0.125 s).
  - 17.85-19.1 s: the head advances smoothly, 13-17 px every drawing (x 32 -> 179).
  - 19.1-20.27 s: it decelerates (185, 193, 202, 207, 212, 216, 220, 221, 224, 228) and stops at 20.27 s
    (x 228-229 to 20.85 s).
  - The head height sinks smoothly (y 257 -> 277), with no per-step oscillation.
  - **There is no hold-then-thrust in this clip**, so the thrust is not cited and is dropped. The head GLIDES at one
    height while the body moves under it (gyro head), as round 2 read it.
  - The clip is slowed to 1.2 s on purpose (the reference cycle is ~1.0 s): a heavier bird. The body rolls +-5 and
    shifts 0.05 BU over the stance leg (review 8 W1). Wings folded.
- **fly (30 f loop):** R5 stroke, plus H1 / E1 for legs trailing after the takeoff.
- **takeoff (36 f):** H1 97.0-99.0. f0-10 the body COILS: hips down 0.075 and the body pitched forward 17 with the
  chest 4 (the gather), while the wings open FOLD -> LIFT1-4 -> the stroke top. **HOLD the coil f10-14** with the wings
  high (H1 97.5). **`launch` f14 (14 / 36 = 0.389)** = the push (H1 98.0). The **first downstroke runs f13-21** (36 ->
  -8 -> -36, 8 frames; H1 98.0-98.5). The **body rises f14-22** (z -0.075 -> -0.01 -> +0.07, 0.65 studs). The **feet
  are planted to f17 and leave at f18** (H1 98.0-98.5: the legs leave as the downstroke starts), then the legs tuck
  (f20 / f23). **f25-36 run the flight cycle** at the fly tempo (phase 0.633 -> 1.0), so the takeoff ends exactly on
  fly f0 (H1 99.0: airborne, wings spread, legs dangling).
- **land (32 f):** H1 12.6-17.0. f0 glide. f6-15 flare upright with the wings braking forward and the legs reaching
  (H1 13.4-13.8). **`touch` f17** (H1 ~14.1). f17-19 absorb DEEP into the same coil (hips -0.08, pitch 16, chest 4)
  and HOLD f19-22 (H1 16.2-16.6). f24-32 rise while the wings fold through LIFT4 -> FOLD (H1 17.0).
- **roar "snap-open" (60 f):** H1 29.6-34.0. The wings snap to FULL SPAN (f14-20), and the beak opens AFTER the
  spread (f20-24). Hold with the head still. The head is raised ~13 deg in world (the call pose).
- **act_bow "courtship bow" (110 f):** H1 44.0-51.6. Chest and head lower; two bobs with the wings DROOPED half-open
  and shuddering; rise, wings lift and SNAP closed (`snap` f58); two tail flicks; rest.
