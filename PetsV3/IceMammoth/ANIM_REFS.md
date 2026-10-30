# Ice Mammoth - animation references (owner rule), 2026-10-27

## What I could open
- **animationreference.org:** the only elephant tag (`/tags/elephants`) has ONE clip ("Video by projectarcheology"). There are no rhino,
  mammoth or trunk tags. I could not play it: the Claude Browser pane is hidden (every click / script times out), and in
  Chrome the clip page froze the renderer (screenshot, click and script all timed out). No credits were spent on a clip I
  could watch. Sakugabooru's `elephant` tag search returns no posts.
- **So the walk uses a frame-by-frame plate I could actually study:** Muybridge, *Animal Locomotion* (1887) **Plate 733,
  "Elephant walking"** (24 photos in a 4x6 grid; Wikimedia Commons `File:Elephant_walking.jpg`). I read it frame by frame.
- **Roar and act timing** reuse the video studies in `_review/ANIM_REFERENCES_1014.md` (#3 Sea Beasts heavy-head roar, #5 combat
  "Attack" snap, #9 Children of the Sea humpback mass timing), plus Richard Williams' heavy-walk notes (*The Animator's Survival
  Kit*: on a heavy walk the body sinks right after contact, the feet lift less and stay down longer).

## Plate 733, "Elephant walking": what the frames show
| # | Observation | Frames |
|---|---|---|
| P1 | **Lateral sequence.** A hind foot lands, then the fore foot on the SAME side lifts a few frames later. The order is LH, LF, RH, RF. | swings at frames 1-2 (hind), 6-8 (fore), 10-12 (hind), 17-20 (fore), 23-24 (hind) |
| P2 | **High duty.** Each foot is in the air for only about 4-5 of the 24 frames. Three feet are on the ground almost all the time. It is never a trot. | whole plate |
| P3 | **Fore swing.** The wrist folds sharply and the sole flips up and BACK, with clearance only about 1/5 of the leg length. The leg plants as a straight column and the foot lands flat. | 6, 7, 8, 17, 18 |
| P4 | **Hind swing.** At toe-off the hind leg trails straight back with the sole showing. It then swings forward with only a small knee bend, low to the ground. | 1, 2, 11, 12, 23 |
| P5 | **The back stays level.** There is almost no bob. The barrel rolls slightly away from the lifted leg. | all |
| P6 | **Head and trunk.** The head is steady. The trunk hangs nearly vertical with the tip curled forward, and swings a little forward and back with the stride. | all |
| P7 | **Tail.** The tail swings loose and lifts off the rump for a few frames, lagging the hips. | 3-6 vs 9-12 |

## The video refs reused (from `_review/ANIM_REFERENCES_1014.md`)
- **Top table #3, Sea Beasts heavy-head roar:**
  - Anticipation: the head DROPS and tucks first (~0.86 s).
  - Then it lifts. The jaw opens about 0.4 s (12 f) AFTER the lift starts, so the jaw lags the head.
  - A slow settle follows.
- **Leviathan section #9, Children of the Sea humpback:**
  - A heavy mass rises fast (about 2 s), hangs a beat, then subsides 2-3x slower, with no bounce.
  - Overshoot only on the light tip (the fluke), never on the body.
- **Mantis section #5, combat "Attack":** the tell is a cocked hold (3-4 f), then a 2-frame snap and a hard stop with a short drift.

## How each clip uses them
- **walk (40 f loop): heavy lateral-sequence walk (P1-P7, Williams).**
  - Own offsets BL 0, FL 0.75, BR 0.5, FR 0.25. Measured touch-downs: BL f0, FL f10, BR f20, FR f30, the hind leading the
    fore on the same side (P1). `cm.quad_walk(gait="walk")` measured as a DIAGONAL sequence, so it is not used.
  - Duty 0.72 (P2; the plate is ~0.8, eased so the feet read in game).
  - Fore knees fold back (P3). The lift is now 0.15 (round 6: was 0.07, about 1/5 of the leg as in P3). That is higher than the plate, so the pads clear the snow from the game camera. The sole stays nearly flat (5 deg toe) instead of the plate's flip-back.
  - Body: the basis is a 0.010 sink after each contact (Williams) with the back level (P5). **The code exaggerates both on purpose for phone-scale readability (lead rounds 4-5):** the body sinks 0.030 per step (highest at the hind touch-downs f0 / f20, lowest at the fore touch-downs f10 / f30), rolls ±2.5 deg toward the planted side and rocks 0.7 deg in pitch. So the back is NOT level as in P5.
  - Head nearly still: ±1 deg (P6).
  - Trunk: a forward/back pendulum in step with the fore legs, about 11 deg summed per step (round 4: was 3, also bigger than P6's "a little"), plus a 6 deg side swing, the tip lagging 2-3 f.
  - The tail swings, lagging the hips by 1/4 cycle (P7).
- **idle (120 f loop): "trunk swing" (plan; P6 for the hanging trunk).**
  - The trunk swings side to side as a lagged chain (tip ±12 deg), two cycles; each bone lags the one above it.
  - Three slow breaths: the chest pitches 4.5 deg and the back rises 0.03. The phase is set so the lungs are empty at the f80 exhale.
  - Exhale at f80 (`exhale` event, `FX_BreathCloud`): the head lifts 8 deg and the neck 4 deg (the dome rises 0.077 BU), the trunk tip lifts and the ears flick out. There is also an ear flap at f40 (18 deg out + 16 deg lift).
  - The tusks never move; the feet stay planted.
- **roar (66 f): "trumpet" (ref #3 + #9).**
  - f0-8 anticipation: the head tucks 4 deg and the trunk curls in.
  - f8-22 the head lifts to -15 deg (pitch up). The trunk rises fast (#9) and curls up in front of the face to about 70 deg
    (bone pitch summed down the chain).
  - The jaw (mouth) opens from f20, after the head lift (#3 jaw lag).
  - `trumpet` event at f26, then a hold f26-50 with a ±2 deg trunk tremble and a 1-deg head tremble. The tail lifts.
  - f50-66 the trunk lowers more slowly than it rose (#9): ease-out, no bounce. Exact rest at f66.
- **act_dustover (100 f): "dust over the back" (plan; refs #5 for the flick, #9 for the heavy settle).**
  - f0-22: the head dips 6 deg and the trunk swings down and back toward the forefeet. The tip curls in to scoop, staying
    above the ground (ground_min_z >= -0.02).
  - f22-48: the trunk lifts and curls up in front of the head, which pitches up to at most -18 deg. A cocked hold at
    f44-48 is the tell (#5).
  - f48-56: the snap. The trunk whips up and back over the brow in 2 in-between frames (no adjacent-frame jump over 60 deg).
    `dust1` at f56 (`FX_FrostPuff` on `Back` + `FX_SnowSpray` on `Trunk_Tip`).
  - f56-64: follow-through drift, then down.
  - f64-92: two smaller scoop + flick beats, `dust2` f74 and `dust3` f86 (70 % and 55 % of the first).
  - f92-100: the trunk returns, slower than it rose (#9). One tail flick. Exact rest pose.
  - The legs stay planted throughout; no shake, no spin.

## Central references (`_review/ANIM_REFERENCES_1027.md`), cited 2026-10-27
**Site tags searched:** `elephants`, `animals`, `muybridge` (2 clips: Plate 27 man carrying a stone, Plate 444 kiss; no
animal plates) and `wolfs-rain`.

| ref | source | what I took | timing check |
|---|---|---|---|
| Site `/tags/elephants` | "Video by projectarcheology", the only elephant clip on animationreference.org (tags animals, body-mechanics; real footage, 13.4 s) | Round 4: searched, not used (the player froze). **Final85 round (2026-10-28): readable.** The tag page embeds the card's own preview video, so it was stepped there with no clip open: adult elephant 10.6-13.2 s (contact sheets in `VoltRhino/renders/ref_idle_elephant_*.jpg`). 10.6-12.0 s: standing, ears held out, the trunk swings slowly through a wide arc toward the calf; 12.0-12.6 s: the body leans, then one foreleg lifts low and plants | Used for the final85 idle (C1): the trunk swing is wider (tip +-12 -> +-16 deg) and stays a slow pendulum; the ears flap out at f40 as well as f82; the breath is larger (chest 0.5 -> 1.2 deg) |
| Muybridge Plate 733 "Elephant walking" | Wikimedia scan (the site's Muybridge set has no animal plates) | The walk (P1-P7 above): lateral sequence, high duty, low fore swing with the wrist folding | Matches. The walk measures BL f0, FL f10, BR f20, FR f30 (lateral), duty 0.72 |
| **W0** Wolf's Rain #30, Yutaka Nakamura | site `/tags/wolfs-rain` = Sakugabooru #174333. I stepped it myself (canvas sheet, 0.167 s steps, 12.9-17.6 s) | The black wolf's snarl (15.9-16.6 s): the mouth opens gradually over ~0.66 s (~16 f at 24 fps = ~20 f at 30 fps), then HOLDS wide for ~1 s with the head level and still. The white wolf (13.9-15.7 s) holds a bared snarl for 1.8 s with only a small tremble. | **Changed:** the trumpet jaw now opens over f16-34 (18 f; was f16-26), then holds 13-14 deg to f50 with the head still (the trunk tremble stays) |

The trumpet's trunk rise is unchanged: ref #9's mass timing (a fast rise, a 2-3x slower fall) still fits. I found no
elephant-trumpet footage on the site.
