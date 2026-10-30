# Animation references — new pets, 2026-10-14

Source: animationreference.org. Frames sampled by seeking; times are in seconds.
Our clips run at 30 fps, so convert with frames = s × 30.

| # | Clip | Use for | Key observations |
|---|------|---------|------------------|
| 1 | *The Old Man and the Sea* (A. Petrov), Sakugabooru cut #17124, 30.5-37 s | Hammerjaw swim + Slam, Orca swim | Sharks circle on long glides with the body nearly straight. Each tail beat is ~0.9 s. Lead-in: 2 strong strokes, then a glide. In the strike (33.6→34.2 s, ~18 f) the head yaws INTO the target and the tail swings the OPPOSITE way, making a C-curve. Head travel ≈ 1/5 of tail-tip travel. Pectorals stay spread and rigid: no flapping. |
| 2 | *Children of the Sea* cut #111777 | idle-hover timing | Background fish hover with tiny, fast tail flicks and a slow drifting bob. The body barely moves; only the tail third works. |
| 3 | *Sea Beasts* (Netflix), 0-3 s | Orca roar, Basilisk roar | Heavy-head roar. Anticipation: the head drops and the chin tucks (0.86 s). The head then lifts (1.29 s) and the jaw opens fully ~0.4 s AFTER the head lift starts (1.71 s); the jaw lags the head. A slow settle follows. |
| 4 | *Dragon Walk Cycle* (C. Sophocleous), 0.3-2.7 s | Basilisk walk | Diagonal pairs (FL with BR). Cycle ≈ 1.5 s (45 f). The head dips on each front-foot contact (2 dips per cycle) with a small lag. The tail wave travels base→tip about ¼ cycle late, and the tip curls up on the trailing beat. Folded wings/frill ride with the shoulders and do not flap. |
| 5 | *Bird Flight Animation Tutorial — Flapping* (diagram short) | Thunderbird fly / takeoff / land | The leading edge (arm) leads and the tips trail (overlap of ~2-3 f). Primaries spread on the upstroke and the wing half-folds on the upstroke. The body rises on the downstroke. Glide = flat with a tiny bob. Bounding = flaps, then folded wings. The tail fans out for braking and turning, which is the landing flare. |

## How each rule maps to our clips

- **Hammerjaw swim (loop 48 f)**
  - Tail1→Tail4 yaw wave with a phase lag of 0.12 cycle per bone.
  - Amplitude grows toward the tip: 4 / 8 / 14 / 20°.
  - Head counter-yaw ≈ 1/5 of the tail tip (≤ 4°).
  - Fins rigid: only ±3° roll drift.
- **Hammerjaw Slam (act, ~42 f)**
  - Wind-up, f0-12: the tail swings out to one side.
  - Strike, f12-20 (8 f): the head yaws into the target and the tail snaps the other way (C-curve). The hammer pitches down on the impact frame.
  - Hold, f20-26, then a 16 f settle.
- **Orca swim (loop 48 f)**
  - Same wave as Hammerjaw but in PITCH (the flukes beat up and down).
  - Head counter-pitch ≤ 3°.
- **Orca roar**
  - Head drop/tuck, 8 f.
  - Head lift, f8-18.
  - Jaw opens late, peaking at f20.
  - Hold, then settle (ref 3).
- **Basilisk walk (loop 45 f)**
  - Diagonal pairs.
  - Spine lateral S (lizard); the head dips on each front contact.
  - The tail wave lags ¼ cycle.
- **Basilisk roar**
  - Uses ref 3 timing.
  - The frill flares on the head-lift frame, with the jaw lag.
- **Thunderbird fly (loop 24 f)**
  - Downstroke 10 f, upstroke 14 f.
  - The arm leads the tips by 2 f.
  - The body rises on the downstroke.
  - The tail fans 10° wider on turns and landing.

## Thornblade Mantis (2026-10-14 night) - animationreference.org, free "Combat study" page previews (24 fps)
| # | clip | used for | key poses / frames |
|---|---|---|---|
| 5 | **"Attack"** (combat study set, 9.8 s; the opening arm strike) | act_thornstrike STRIKE 1 / 2 | f0-5: settle. f6-11: the body coils and the head dips (anticipation). f12-14: the hand is COCKED close to the body and held (a 3 f tell). f14 to f16: the SNAP, 2 frames with a smear at f15 and full extension at f16. f16-21: follow-through, the arm held extended with a small drift and settle (5 f). In our brief this becomes the 4 f tell (f20-24 hold), the 2 f snap (f25 open, f27 closed) and a hard stop. |
| 6 | **Monsters University** (combat study set, 3 s; the Oozma Kappa "scare" pop) | roar = deimatic display | f0-5: everyone CROUCHES and compresses. f5-10/12: they EXPLODE up into the big spread pose (arms up and wide), 5-7 f from crouch to full spread. Then they hold. Our mapping: crouch f0-10, rear f10-20, the fan / arms spread f14-26 with `display` at f24, then the hold. |
| 7 | **How to Train Your Dragon** (combat study set, 8.6 s; a cautious forest approach) | idle peering / lock-on | A slow step, a pause and a look, repeated. The body freezes while the head scans, and weight shifts only between pauses. Our mapping: lock-on peering = Spine x sway 0.025 over 5 f each way with the head LOCKED (the predator head-lock). |
Also used: #3 Sea Beasts heavy-head roar (the jaw lags the head lift). Clip credits left today: 18/25. The previews on the study page do not cost credits.

## Cosmic Leviathan + Inferno Phoenix flight (2026-10-14 late night) - animationreference.org /tags/dragon
| # | clip | used for | key poses / timing |
|---|---|---|---|
| 8 | **"Avatar"**, the banshee (ikran) flight (YouTube dULrAcg3R-Y, studied at 103.0-105.0 s in 0.4 s steps) | Leviathan swim "Manta Flight", Phoenix fly | One full wing stroke takes about 0.8-0.9 s (≈ 24-27 f at 30 fps). Big amplitude: the upstroke ends in a high V (about 45° above level) and the downstroke ends about 25° below level. The body barely bobs and the head stays level (gyro). The long tail streams nearly STRAIGHT behind, with only a small lagging bend (no big S-wave in steady flight). Banking rolls the whole body (103.0 s: a banked dive with the wings in a high V). The two riders' banshees are out of phase, so stroke speed varies about ±15 %. |

Mapping:
- **Leviathan swim (36 f loop):**
  - wing-fin stroke +28 / -20 about the fan hinge (fin_rot), downstroke 15 f / upstroke 21 f
  - FinTip lags 2-3 f (ref 5)
  - the body counter-bobs ±0.02 (it rises on the downstroke)
  - head stabilised within ±2°
  - Tail1-4 carry only a small pitch wave (lag 0.1 cycle per bone, 2 / 3 / 4 / 5°) and the fluke a 6° beat; NOT a big serpent S (ref 8)
- **Phoenix fly:** the same stroke timing (refs 5 + 8). The streamers stream straight with a small lagging wave, as the banshee's tail does.
Clip credits left today: 16/25.
| 9 | **Children of the Sea**, CGI humpback (Sakugabooru #111889, free post page; canvas contact sheet 60-73 s at 1 s) | Leviathan act_sounding "rise & ignite" + "resurface", roar "gather" | The heavy-mass timing. The head lunges up out of the water to near-vertical in about 2 s (62→64 s, ≈ 60 f), hangs a beat, then the body subsides SLOWLY over about 5 s (67→73 s), with water sheeting off. The fall is 2-3x slower than the rise, with no bounce. Mapping: ignite rise f0-14 is fast, the slip f70-82 eases out, the resurface f82-102 is slow; any settle is a long ease with no overshoot on the body (overshoot only on the fluke tip). No fluke-up sounding dive is in this cut. |

## Abyss Weaver + Inferno Phoenix clip references (2026-10-14 day 2, before animating)
**Spider search (owner rule: references before animating).** animationreference.org has NO spider / insect /
multi-leg locomotion: `/tags` (3,732 tags) has no spider, insect, bug or crawl tag; `/tags/creature` (20 clips) is all
dragons; `/tags/creature-animation` titles are generic. Sakugabooru, the source host: no `spider` or `insect` general
tags; the CGI-spider anime "Kumo desu ga, Nani ka?" posts #238075 (NCOP) and #153903 (ED montage) checked by contact
sheet: no spider locomotion. No clip credits were spent (16/25 left).

**So the Weaver uses:**
- **walk "SCUTTLE":** the brief's metachronal tetrapod (real spider biomechanics: back-to-front waves inside each
  tetrapod, duty 0.58, >= 4 feet down, solved numerically by the plan reviewer), plus ref **#4** for the creature
  weight (a body dip per contact, secondary parts lagging 2 f: the abdomen lag).
- **idle "STILL HUNTER":** ref **#7** (step, freeze, scan): long holds, single-leg taps, the whole body turns to a sound.
- **roar "FANG FLARE":** ref **#6** (crouch f0-10, explode into the display in 5-7 f, hold).
- **act "RIFT WEAVE" cast:** ref **#5** (the cocked hold as the tell, then a 2-frame snap + hard stop): the abdomen
  whip-down f74-80 with the in-between at f77.

**The Phoenix uses:**
- fly / takeoff / land: refs **#5** (bird flapping) + **#8** (banshee stroke ~0.85 s, the tail streams straight)
- roar: ref **#3** (the jaw lags the head lift)
- act_rebirth: ref **#9** (heavy rise fast, fall 2-3x slower)
- walk "STALKING STRUT": ref **#4** + the Thunderbird walk recipe
- Phoenix "NEW" refs the brief asked for if available: a large bird taking off from standing, a heavy creature slump,
  a peacock / turkey tail-raise display. `/tags/flying` (325) titles are generic tag combos (no bird / takeoff
  titles); `/tags/creature` (20) is all dragons. "Tyrant Dragon Animation - MAYA 2023" (YouTube d8EYJW3-Njg) only
  played a pre-roll ad in the headless study. Not found, so the Phoenix stays on #3 / #5 / #6 / #7 / #8 / #9 (all
  logged above): the takeoff + rise from #5 + #8 (the body rises on the downstroke, ~0.85 s strokes), the pyre slump
  from #9 (a heavy mass settles 2-3x slower than it rose, no bounce), the train rise from #6 (crouch, then the spread
  in 5-7 f), the look-back hold from #7.
