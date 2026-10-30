# Volt Rhino - animation references (owner rule), 2026-10-27

## What I could open
- **animationreference.org:** no rhino, bison or heavy-ungulate tags; the one heavy-animal tag (`elephants`) has one clip, and I
  could not play it (the Claude Browser pane is hidden, and Chrome's renderer froze on the clip page). No clip credits spent.
- **Frame-by-frame plates I studied (Wikimedia Commons scans):**
  - Muybridge, *Animal Locomotion* (1887), **"Walking bison"** (24 photos, Zeno scan "Gehendes Bison (0.65 Sekunden)"). A heavy,
    shoulder-humped horned ungulate: the closest plate to a rhino.
  - Muybridge **Plate 733, "Elephant walking"** (24 photos): the heavy-walker duty factor (see `IceMammoth/ANIM_REFS.md`).
- **Video refs reused** from `_review/ANIM_REFERENCES_1014.md`:
  - top table #3, Sea Beasts heavy-head roar;
  - Mantis section #5, combat "Attack" (the cocked tell, then a 2-frame snap and a hard stop);
  - Mantis section #6, Monsters University (crouch, then explode to the display in 5-7 f, then hold);
  - Leviathan section #9, Children of the Sea (a heavy mass rises fast and settles 2-3x slower).

## Walking bison plate: what the frames show
| # | Observation |
|---|---|
| B1 | **Lateral sequence:** a hind hoof lands, then the fore on the same side lifts. There are 3 hooves down most of the time. |
| B2 | **Head carried LOW**, the muzzle below the brisket line. It dips a little on each front contact (2 dips a cycle). |
| B3 | **Fore swing:** the knee folds back so the cannon tucks up under the chest. Clearance is about 1/4 of the leg, and the hoof flips back. |
| B4 | **Hind swing:** a low arc with a hock flex. The hoof trails and only just clears the ground. |
| B5 | **The back line stays level** and the hump rides steady. The barrel rolls slightly toward the planted side. |
| B6 | **Tail:** hangs, with a small lagging swing. |

## How each clip uses them
- **walk (40 f loop, lateral sequence, B1-B6 + plate 733):**
  - Own lateral offsets (BL 0, FL 0.75, BR 0.5, FR 0.25), duty 0.70. Measured touch-downs: BL f0, FL f10, BR f20,
    FR f30 (B1).
  - Front knees fold back (B3); lift 0.08 front-heavy.
  - The body sinks 0.02H on each contact (plan: rocks 0.02H per step) and rolls ±2 deg (B5).
  - The head dips 1.5 deg on each front contact, lagging 2 f (B2).
  - The tail lags 1/4 cycle (B6).
- **idle (120 f loop): "horn tilt" (plan; B5 weight shift).**
  - The weight shifts left, then right.
  - f30-46: one foreleg (FL) lifts 0.03 and sets down (`FX_DustTap` event `stamp` f46).
  - The head yaws ±6 deg slowly, so the horn tilts side to side (a slow look, not a shake: one cycle).
  - Tail flick at f90 (`flick`). Ears twitch.
- **roar (60 f): "bellow" (ref #3, plan limits).**
  - f0-6: the head drops and tucks 4 deg (anticipation).
  - f6-16: the head lifts to -12 deg, plus the neck -4 = 16 up; the snout stays forward.
  - The jaw opens late, from f14 (the jaw lags the head).
  - Three bellow pulses (jaw +5 deg, chest pump) at f20 / f28 / f36: `bellow1-3` on `Mouth` (`FX_BellowRing`).
  - f40-60: the head lowers more slowly than it rose (#9); the jaw closes. Legs planted.
- **act_horntap (100 f): "lightning taps" (refs #5, #6, #9).**
  - Geometry note: the horn curves UP from the nose, so the horn tip can only reach the ground before the snout when the face
    points steeply down (~70 deg total). The rhino lowers its forequarters a little (chest +4, neck +8) and drives the head
    down at the throat, horn forward, snout clear of the snow. It is like a bull dropping its horns.
  - f0-22: lower (eased).
  - Three taps (#5): a 3 f cocked lift (the tip rises 0.05), then a 2 f strike to the ground: `tap1` f30, `tap2` f42,
    `tap3` f54 (`FX_BoltTrail` on `Horn_Tip`).
  - f56-62: the snap up (#6): from face-down to horn-to-the-sky in 6 frames, with in-betweens so no bone swings more than
    60 deg in one frame. The head ends -12 / neck -4 (16 up).
  - f62-86: hold with a small settle; the lightning inlays flash, `charge` f70 (`FX_ChargeGlow` on `Horn_Base`, shoulder
    `FX_BoltSpark_L/R`).
  - f86-100: back to rest, slower than the snap (#9). The legs stay planted.

## Central references (`_review/ANIM_REFERENCES_1027.md`), cited 2026-10-27
**Site tags searched:** `elephants`, `animals`, `muybridge` (no animal plates), `wolfs-rain`, `kaiju-no-8`.

| ref | source | what I took | timing check |
|---|---|---|---|
| Muybridge "Walking bison" | Wikimedia (Zeno scan) | The walk (B1-B6 above) | Matches. The walk measures BL f0, FL f10, BR f20, FR f30 (lateral), duty 0.70 |
| **W0** Wolf's Rain #30, Yutaka Nakamura | site `/tags/wolfs-rain` = Sakugabooru #174333 (I stepped it) | The snarl opens over ~0.66 s (~20 f at 30 fps), then the mouth HOLDS with the head level | **Changed:** the bellow jaw now starts opening at f10 (2 deg) → f16 (7) → first pulse f20 (14). It never closes between the pulses (9-14 deg, the W0 hold), and the head stays level. The plan pins bellow1 at f20 and ref #3 wants the jaw to lag the head lift, so the onset is 10 f, not W0's 20 f |
| Head-down charge: Muybridge **Plate 700 "Buffalo galloping"** | Wikimedia `Muybridge_Buffalo_sequence.jpg`, 16 photos | Frames 9-16: at each forelimb strike the shoulders SINK, the fore knees flex and the head drives down to a near-vertical face (chin tucked, horns forward), about 1 photo after the forefoot lands. It is a charge posture, not a graze. | Matches the braced taps: chest -0.06, front knees +30 deg, face ~70 deg down, the brace on the strike frame. No change |

## Per-animation references (round 4, 2026-10-28), the final list
**W0, one figure:** Sakugabooru #174333 (Wolf's Rain #30, Yutaka Nakamura; site `/tags/wolfs-rain`), 23.976 fps. The black
wolf's snarl:
- the mouth starts opening at source **f381** (15.91 s), is wide at **f397** (16.57 s), and holds to the cut at **f421**
  (17.58 s);
- the onset is **16 frames at 24 fps = 20 frames at 30 fps**, and the hold is ≥ 24 frames at 24 fps = 30 frames at 30 fps.

The bellow: start **f10**, mid **f16** (7 deg), first pulse **f20** (14 deg) = a 10 f onset. It is half of W0 because the plan
pins bellow1 at f20 and ref #3 wants the jaw to start after the head lift (f6). Between the pulses the jaw stays open
9-14 deg = W0's hold.

| animation | site search | clip / source | frames (24 fps → 30 fps) | what I took |
|---|---|---|---|---|
| walk | `/tags/walk-cycle`: 370 clips, page 1 has no quadruped walk in the titles. Sakugabooru `walk_cycle animals` search → **#144564** *The Jungle Book* (1967), Colonel Hathi's elephant march (tags `walk_cycle`, `animals`) | #144564, stepped 1.0-2.5 s at 3-frame steps | One front foot lifts at **f27**, plants by **f33-36**; the other front lifts at **f42-45**; the first front lifts again at **f57**. **Stride ≈ 30 f at 24 fps = 37.5 f at 30 fps**; each foot is up ~7-9 of 30 f → **duty ≈ 0.70-0.75** | The heavy-walk timing: our 40 f cycle and duty 0.70 sit inside it. The cartoon march's high knee lift is NOT taken (lift 0.08) |
| walk | (Wikimedia fallback) Muybridge "Walking bison", 24 photos, numbered left to right, 4 rows of 6 | photos 1-24 | **Hind swings** (hock flexed, hoof trailing): photos **1-2, 7-8, 13-14, 19-20**. **Fore swings** (knee folded, cannon tucked under the chest): photos **3-5, 9-11, 15-17, 21-23**. Each fore leaves ~2 photos after the hind on the same side → **lateral sequence BL, FL, BR, FR**. A stride is ~12 photos and each hoof is up ~3 of 12 → **duty ≈ 0.75** | The touch-down order (ours: BL f0, FL f10, BR f20, FR f30); the low head that dips on each fore contact; the tucked fore swing |
| idle (final85 C1, 2026-10-28) | `/tags/elephants`: 1 clip, "Video by projectarcheology" (tags animals, body-mechanics; real footage, 720x1280, 13.4 s). Stepped from the tag page's own preview video (`.../videos/6240985f-...mp4`), so no clip open was used. **No-fit for the other tags:** `/tags/animals` (533 clips) and `/tags/creature-animation` (2,415) were cross-checked by thumbnail md5 against Sakugabooru's `animals western` posts with heavy animals (Ice Age, Snow Bear, Mickey's Elephant, Ferdinand the Bull, Moose Hunt): none of them is on the site; the rest are anime with no heavy-quadruped idle in the titles | the adult elephant, 10.6-13.2 s (contact sheets `renders/ref_idle_elephant_1060-1320.jpg`, `_1130-1290.jpg`, `_overview.jpg`) | **10.6-12.0 s**: standing, ears held out, the trunk swings slowly toward the calf. **12.0-12.3 s**: the body leans onto the other legs. **12.3-12.6 s** (~9 f at 30 fps): the near foreleg lifts low and plants. Head and trunk keep moving while the body is still | The weight shift now moves OFF the lifting foreleg (phase 0 -> 0.433: the shift peaks on the right at f38, mid-lift of FL; before, the body leaned onto the lifting leg). The low lift (0.032) and the 16 f stamp stay (a deliberate stamp, slower than the step). The head yaw, ear twitches and tail flick keep the still body alive; the snort (T3) adds one more beat |
| walk (final85 r5 MUST 3, 2026-10-28) | **Site clip:** `/tags/elephants`, card "Video by projectarcheology" (the only clip on the tag; real footage, 720x1280, 13.4 s). Stepped from the tag page's embedded preview video (`.../videos/6240985f-d28b-4b4f-abe4-a3402910862c.mp4`), with paused frames side by side in the page; no clip overlay opened (guest counter 1/25 before and after). Tag pages also checked for a heavy quadruped walk: `/tags/walk-cycle`, `/tags/animals`, `/tags/creature-animation`, `/tags/subtle`; nothing better on the site | the adult elephant walking toward the camera (3/4 front), **10.0-11.4 s in 0.2 s steps** (0.0-1.4 s checked first: the adult only stands there while the camera pans) | **10.0 s**: the viewer-right foreleg trails, lifting. **10.2**: it swings forward, LOW (the foot barely clears the grass), and the body leans onto the planted viewer-left fore. **10.4**: it plants. **10.6**: the viewer-left fore lifts. **10.8**: it swings low while the trunk swings the other way. **11.0**: it plants. Each fore swing is ~0.4 s and a fore lifts every ~0.6 s, so one foot's cycle is ~1.2 s and duty is about 0.67. The head dips a little as each fore lands | **Fits:** 40 f (1.33 s) cycle, duty 0.70, low swing lift 0.08 and the roll toward the planted side (Spine roll, phase 0.25) match. The trunk counter-swing has no rhino part, so the head yaws instead (1.5 deg, phase 0.3). The Jungle Book march stays as a timing cross-check only |
| roar | `/tags/wolfs-rain` | W0 #174333 (above) | onset 16 f at 24 fps = 20 f at 30 fps; hold ≥ 30 f | The jaw stays open through the bellow pulses with a level head |
| act | `/tags/kaiju-no-8`: **6 clips** (#09 "Morphing", #07 CGI = #257646, #01 Yuya Takahashi "Character Acting", #11 CGI, #01 "Beams", #01 CGI). I stepped #257646 (8.0-11.3 s): a biped landing into a crouch, no head-down charge. The other five titles are morphing, beams or CGI fights, with no quadruped charging horn-first. **Not used.** | (Wikimedia fallback) Muybridge **Plate 700 "Buffalo galloping"** | photos 9-16: at each forelimb strike the shoulders sink, the fore knees flex and the face drives down near-vertical about 1 photo after the forefoot lands | The braced tap: chest -0.06, front knees +29.8 deg, face ~70 deg down, the brace on the strike frame |
