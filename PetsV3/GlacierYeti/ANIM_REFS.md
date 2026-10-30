# Glacier Yeti - animation references (owner rule), 2026-10-27

## What I could open
- **animationreference.org:** it has no gorilla, ape or knuckle-walk tags. Its one heavy-animal tag has one clip, which I
  could not play (the Claude Browser pane is hidden; Chrome's renderer froze on the clip page). No clip credits spent.
- **Frame-by-frame plate I studied:** Muybridge, *Animal Locomotion* (1887) **Plate 747, "Baboon walking on all fours"**
  (16 photos; Wikimedia Commons USC scan). This is the closest plate to a quadrupedal primate gait.
- **Video refs reused** from `_review/ANIM_REFERENCES_1014.md` (all animationreference.org clips):
  - top table #4, "Dragon Walk Cycle" (C. Sophocleous): a diagonal-pair walk, a 45 f cycle, the head dipping on each front
    contact. It sets the walk timing; Muybridge 747 is the frame study.
  - top table #3, Sea Beasts heavy-head roar (the jaw lags the head lift);
  - Mantis section #5, combat "Attack" (the cocked tell, a 2-frame snap, a HARD STOP);
  - Mantis section #6, Monsters University (crouch and compress, then explode in 5-7 f);
  - Leviathan section #9, Children of the Sea (a heavy mass rises fast and settles 2-3x slower, no bounce).
- **Also reused:** `BrambleBadger/ANIM_REFS.md` ref B, "Pluto and the Gopher" (Sakugabooru #143881, studied by builder A). The
  drop is fast (0.5 s), the shoulders lead and the rump lags, the hold is low, and the rise is slower than the drop.

## Plate 747, "Baboon walking on all fours": what the frames show
| # | Observation | Frames |
|---|---|---|
| Q1 | **Diagonal sequence:** a hind foot lands, then the OPPOSITE hand. The order is LH, RF, RH, LF (the primate gait). | 1-16 |
| Q2 | **The planted arm is a straight column.** The hand reaches far forward on contact and the shoulder passes over it. | 5-8, 13-14 |
| Q3 | **The swinging arm** bends at the elbow and the hand trails low, just clearing the ground. The swing is short and quick, about 1/3 of the cycle. | 3-4, 9-12 |
| Q4 | **The back stays level** and the head stays level, looking forward. The shoulders roll with the arm in stance. | all |
| Q5 | **The hind foot lands near where the hand lifted off.** The step is long and the feet stay flat. | 6-7, 14-16 |

## How each clip uses them
- **walk (48 f loop): KNUCKLE WALK (Q1-Q5 + 1014 #4 Dragon Walk Cycle: diagonal pairs, head dip per front contact).**
  - Diagonal sequence: offsets Leg_L 0, Arm_L 0.25, Leg_R 0.5, Arm_R 0.75 are phase leads. Measured touch-downs:
    Leg_L f0, Arm_R f12, Leg_R f24, Arm_L f36 = LH, RF, RH, LF. Duty 0.62.
  - The torso drops 0.07 and pitches 9 deg forward (hunched), so the fists reach the snow. The arm IK plants them 0.10
    below their hang height, at the fist bottom ~0.02 (Q2).
  - The swinging fist lifts 0.07 with the elbow bent outward (Q3).
  - The torso bobs 0.02H per step (plan). The chest yaws ±5 deg with the arm in stance (Q4).
  - The head counter-pitches and counter-yaws, so the gaze stays level (Q4).
  - `stomp` at the Leg_L contact (`FX_SnowPuff`).
- **idle (120 f loop): "plate settle" (plan; Q4 for the stillness).**
  - Hip yaw ±5 deg, one slow cycle, and three slow breaths (chest 4.2 deg).
  - The shoulder crusts (`Plate_L/R` bones) lift 13 deg in 5 frames (f30-35), hold 10 frames (f35-45) and settle over 15 (f45-60). `settle1` is at f35 and `settle2` at f60 (`FX_AuroraDust`).
  - The head lowers 11 deg at f55-75 (no snow contact) and is back by f100. Feet planted, arms hang.
- **roar (60 f): "shoulder-heave bellow" (Mantis #6, top #3).**
  - f0-12: the shoulders pull back and the chest lifts and compresses (the #6 crouch, done upward).
  - f12-24: two heaves, the chest yawing +10 then -10 deg (shoulder forward, the arm swinging with it).
  - The head pitches up 15 deg from f10. The jaw opens late, f20-45 (#3), and the fangs show. `roar` at f24
    (`FX_BreathCloud` on `Mouth`).
  - f45-60: the jaw closes and the shoulders settle, slower than the heave (#9). No chest beat, no arms raised.
- **act_skid (100 f): "snow skid and brake" (Badger ref B, Mantis #5, Leviathan #9).**
  - f0-16: the drop (ref B, fast: the shoulders lead). The fists plant wide on the snow and the chest drops 0.06H.
  - f16-34: the arms sweep forward and back in wide arcs, like a sled; `skid1` f22 (`FX_SnowPuff` on `Chest`).
  - f34-52: the chest slides low while the feet stay put (root net 0); `skid2` f42.
  - f52-66: the fists dig in. A cocked lift (f52-56), then a 2-frame drive into the snow and a hard stop (Mantis #5);
    `brake` f58 (`FX_ShardBurst_L/R` on the hands).
  - f66-100: the push-up with a shoulder heave. It rises faster than it settles (#9), the plates settle, and it ends in
    exact rest.

## Central references (`_review/ANIM_REFERENCES_1027.md`), cited 2026-10-27
**Site tags searched:** `kaiju-no-8`, `wolfs-rain`, `creature`, `animals`, `muybridge` (no animal plates).

| ref | source | what I took | timing check |
|---|---|---|---|
| Muybridge Plate 747 "Baboon walking on all fours" | Wikimedia (USC scan) | Q1-Q5 above: the diagonal sequence and the straight-arm plant | Matches. The walk measures LH f0, RF f12, RH f24, LF f36 |
| ANIM_REFERENCES_1014 top #4 "Dragon Walk Cycle" (Sophocleous) | animationreference.org | Diagonal pairs and a head dip per front contact. The cycle is ~45 f; ours is 48 f | Matches |
| **Kaiju No. 8 #257646** (proro) | site `/tags/kaiju-no-8` = Sakugabooru #257646. I stepped it (canvas sheet, 0.17 s steps, 8.0-11.3 s, 23.976 fps) | 8.33 → 8.50 s: the heavy creature lands into a deep WIDE crouch, one hand planted, in ~4 frames (~5 f at 30). 8.8-10.0 s: it holds low for ~1.2 s with only a small weight shift. 10.5-11.0 s, close-up: the jaw opens over ~0.5 s (~15 f) with the head still | **Changed:** the skid drop now lands by f7 (was f10), and the fists plant at f7 (was f8). The low hold (f34-52) and the roar jaw onset (f12-28, 16 f) already match |
| **W0** Wolf's Rain #30 | site `/tags/wolfs-rain` = Sakugabooru #174333 | The snarl opens over ~20 f at 30 fps, then holds with the head level | The roar jaw opens f12-28 and holds 24-26 to f45: matches |

## Idle reference, per-clip round 4 (2026-10-28)
- **Tag page:** https://animationreference.org/tags/subtle (10 clips).
- **Clip:** the "Kung Fu Panda" card (20.3 s, 1920x1080; Po crouched on all fours by a river).
  - I stepped the card's own preview video in 0.5 s steps from 9.5 to 16.0 s, with paused frames laid out side by side in the page.
  - I did not open the clip overlay, so no clip open was spent on purpose. The guest counter read 2/25 on the first tag-page load and 1/25 after.
  - I also stepped the first "How To Train Your Dragon" card (9.3 s). It is a human reading by a candle, so it is not used.
- **What the frames show:** a heavy body at rest on its hands, breathing.
  - The head drops and the shoulder mass rises around it at 10.0-10.5, 11.5-12.0, 13.0-13.5 and 15.0-15.5 s. The back hump ends up above the head.
  - The head lifts and the shoulders settle at 11.0, 12.5 and 14.0 s.
  - The head-up beats are short (about 0.5 s). The low, hunched holds are longer (about 1 s). The shoulders move against the head, not with it.
- **How the idle uses it:**
  - The head drop is bigger (11 deg, f65-75) and holds longer (10 frames) than the rise back (f75-100 is slower, eased).
  - The shoulder crusts lift 13 deg once: rise 5 frames (f30-35), hold 10 (f35-45), settle 15 (f45-60). That is the shoulder mass rising and holding, read through the ice plates, with the ref's short rise and long hold.
  - The chest breath is 4.2 deg.
  - Not taken: the ref's head and shoulders move in counter-phase within one beat. Here the plate lifts (f30-50) and the head drop (f55-75) stay as separate beats, so each reads on its own at phone scale.

- Round 5 (lead ruling): a tag-page preview stepped with cited times counts as the animationreference.org reference, so no clip open was used. The idle's plate beat now holds 10 frames at the top (f35-45) and settles over 15 (f45-60). That matches the ref's long hunched holds and short up-beats.
