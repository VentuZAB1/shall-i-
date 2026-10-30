# Wraith Hound - animation references (owner rule), 2026-10-27

**Clip review 3 (MUST 1), 2026-10-27: I re-ran the site search with the opens I had left.** animationreference.org
had 5/25 opens left. I searched the tag index (`/tags`, 3,765 tags) for dog, wolf, hound, canine, fox, cat, animal,
muybridge, quadruped, creature, walk, growl, snarl, crouch, claw, stalk, dig and badger. The tags I looked through were:
- `/tags/animals` (541) and `/tags/walk-cycle` (367);
- `/tags/wolfs-rain` (3), `/tags/wolf-children` (3) and `/tags/wanwa-the-doggy` (3);
- `/tags/sherlock-hound` (1), `/tags/dogdog` (3) and `/tags/blackfox` (2);
- `/tags/the-cat-returns` (3), `/tags/cartoon-animals` (13), `/tags/muybridge` (2) and `/tags/walking` (12).

`/tags/quadruped` returns a 404. **W0 below is a site clip**, opened in the site player (the counter went 5 → 4). The
player overlay hangs while the Browser pane is hidden, so I stepped its frames on the same source file (Sakugabooru
#174333, the mp4 the site player streams).

Clips are 24 fps; ours are 30 fps (frames = s x 30). Study only.

| # | Clip | Used for | Key poses and timing |
|---|---|---|---|
| **W0** | **animationreference.org, `/tags/wolfs-rain`: "Animals: Character Acting & Creature Animation (#30 - Wolfs Rain)"** (Yutaka Nakamura; source Sakugabooru #174333) | **walk timing + roar (snarl)**, the main reference | **Snarl, 0.0-5.25 s:** a dark wolf, head low and level, ears back, mouth open on the fangs. The mouth works open and closed in ~0.25-0.5 s beats and the snarl is held while it advances. Each slow stalk step takes ~0.75-1.0 s. **White wolf, 14.0-15.25 s:** the lips peel back and the mouth opens over ~0.5 s (15 f), then holds. **Walk, 10.5-13.75 s (back view):** a diagonal-pair walk with a foot fall every ~0.4-0.5 s, so a ~0.9-1.0 s cycle (27-30 f). The head stays level. |
| W1 | **Sheep Dog** (Disney, Pluto vs coyotes), Sakugabooru #143877 (Hugh Fraser / George Nicholas), 22-30 s | roar (snarl, secondary to W0), walk posture | The **lean coyote** is the closest canid. At 24.0-24.75 s it stalks low with the head forward and the ears up. In the snarl at 28.5-29.25 s the lips peel back and **the mouth opens over ~0.5 s (15 f)** while the head pushes forward a little; **the ears go back after the mouth opens** (~3-4 f late). It holds the snarl. |
| W2 | **The Pointer** (Disney 1939), Sakugabooru #258150 (Ollie Johnston / Lynn Karp), 8.0-10.8 s (also in the badger refs) | idle "scent drift" | The nose works in small lifts and dips every **0.4-0.6 s (12-18 f)** while the body stays still; the ears hang and lag the head. |
| W3 | `_review/ANIM_REFERENCES_1014.md` #6, **Monsters University** (crouch, then explode into the spread display in 5-7 f, hold) | act_smokecloak (the cloak spread) | The deimatic display: compress, a fast spread, a long hold. |
| W4 | `_review/ANIM_REFERENCES_1014.md` #4 (Dragon Walk Cycle: secondary parts lag ~1/4 cycle) and #8 (Avatar banshee: the tail streams with a small lagging bend; **#8 is a YouTube source in that file, not an animationreference.org clip**) | mane / tail overlap in every clip | Secondary masses **lag the body by 2-4 f** and **trail with a small bend**, with no big S-waves. |

## Mapping
- **idle (120 f loop), "scent drift"** (W2 + W4):
  - The head pitches -10 / +10 / -6 deg in 15-20 f moves (the nose lowers and lifts).
  - The ears flick back at f40 and forward at f80.
  - The mane rows sway +-4 deg with a 3 f lag per row; the tail drifts.
- **walk (36 f loop, r8; was 30 f)**: a lean trot-walk with diagonal pairs and long steps (stride 0.6), the head low and level (W0/W1 posture).
  - The feet follow my own soft path (`soft_trot`): they leave and land at zero speed, with a 0.045 lift.
  - W0's walk cycle is ~27-30 f and its slow stalk steps are 0.75-1.0 s each, so 36 f (1.2 s) sits between W0's walk and its stalk: a calmer, prowling trot.
  - It was lengthened to keep every knee and ankle step under 5.6 deg per frame (r4 clips NICE). 30 f is the fallback if the owner wants the brisker W0 cadence.
  - The body is carried 0.02 lower so the legs never lock straight.
  The mane rows lag the body by 4 f; the tail streams (W4).
- **roar (60 f), "mane flare"** (W1 + W3):
  - f0-14: the mane rows lift 18 deg (20 with the tremble) and the side wisps splay 25 deg, 2 f lag per row (a fast
    flare, W3); the ears go back.
  - f14-26: the chest pushes forward, the head pitches down 10 deg and the jaw opens 25 deg over ~12 f (W1: mouth
    first, ears follow). Re-checked against W0: the mouth opens in ~15 f there, so the jaw now opens f11-26 (15 f). Event `snarl` f26 (the jaw peak).
  - f26-44: hold with a 2 deg mane tremble.
  - f44-60: the mane falls back, the jaw closes, settle. No paw swipe (that is ShadePanther's).
- **act_smokecloak (100 f)** (W3 + W4):
  - f0-24: crouch flat (the legs bend, the body drops; r8: 24 f, was 18, so no knee step tops 5.6 deg); the feet stay planted.
  - f18-40: the mane lifts 14 deg and fans out wide (side wisps roll out 60 deg, 63 with the drift), 3 f lag per row.
    Event `cloak` f28.
  - f40-68: hold the fan, drifting +-6 deg over two cycles. Event `drift` f54.
  - f68-90: the mane folds back in (f68-84) and the hound rises (r8: the rise is 22 f, to f90).
  - f86-100: the mane settles to the exact rest pose.
