# Eclipse Seraph - model + clip gate review 5 (2026-10-28) - REVISE

**Scores (ship bar now 8.5 minimum, higher is better):**
- **Model: 8/10.** Blocked by the Index card and by the punch against Solar Lion.
- **Clips: 8.5/10.** At the bar.
- **Pet overall: 8/10.** Not shippable until the model reaches 8.5.

**Six-wing verdict: PASS in motion, no fallback to four wings.** The game and tq views show three tiers per side in both the cascade hold and the fly. The front view is weaker, and the static Index icon hides the lower pair (section 2). Fix that (model MUST 1). A front-only weakness would not fail the gate, but the Index card is player-facing, so here it does matter.

**Near-white (your question): accept, no pull-back.** The rise to 28 % on my 64 px count (22.9 % icon, 34.4 % raw) comes from the lighter lilac wings, not from white. The wings read lilac in the strip and the Index icon, and the pegasus white is gone. Guard it at 30 % or below on my count.

---

## 1. Model (my counter, 64 px; builder's in brackets)

| item | round 4 | round 5 | target | result |
|---|---|---|---|---|
| mean saturation, 7-cell portrait | 0.39 | **0.37** [0.37 icon, 0.352 strip] | >= 0.36 | PASS (Leviathan 0.35, Frostcrown 0.42, Solar Lion 0.42) |
| saturated share (sat > 0.35) | 74 % | **55 %** | >= 40 % | PASS (Leviathan 41 %, Solar Lion 68 %) |
| near-white (lum > 200) | 21 % | **28 %** [22.9 icon, 34.4 raw] | <= 25 % raw; accepted (section 0) | ACCEPTED, guard at 30 % |
| dark (lum < 90) | 26 % | **25 %** [23.1 raw] | >= 22 % | PASS (Leviathan 35 %, Solar Lion 22 %) |
| gold px, portrait | 103 | **108** (10.1 %) [26 game] | >= 20 | PASS |
| gold px, game camera (4-cell 64) | 22 | **20** (3.0 %) [26 strict / brief] | >= 20 | PASS, thin margin |
| red px, portrait | 32 | **36** (3.4 %) | >= 10 | PASS |
| red px, game camera | 9 | **13** (2.0 %) [~17] | >= 12 | PASS |
| halo clearance, head / mane | 0.055 / 0.080 | **0.055 / 0.080** | >= 0.050 | PASS |
| tris | 11,264 | **11,288** | <= 15k | PASS |

Flat game view (round 5 palette): WING_LILAC 31.6 %, BODY_MID 25.4 %, OBSID 16.8 %, GOLD 4.6 %, BLOOD 2.6 %, MOON_IVORY 4.9 %. The wing and body split is now real. Luminance is about 180 for the feathers and 151 for the body.

**The Index icon (`EclipseSeraph_icon.png`, 512 px): this is the card the player sees.** It shows two raised upper blades and one middle wing, with the lower pair hidden behind the flank. It reads as three or four wings, not six. The 64 px portrait has the same problem.

**Lion read at 64 px:** moderate. At 128 px the dark ruff, white muzzle and red eyes read as a lion-angel. At 64 px it is a lilac winged creature with a dark ruff. Acceptable; not yet strong.

**Outclass check (64 px):**
- **Cosmic Leviathan (1 %): PASS on colour, FAIL on dark.** Chroma 0.37 against 0.35, saturated share 55 % against 41 %, gold 108 against 20, red present. Dark is 25 % against the Leviathan's 35 %.
- **Solar Lion (common, 54.9 %): FAIL on punch.** Chroma 0.37 against 0.42, saturated share 55 % against 68 %, gold 108 against 267. The Solar Lion's gold is a mane, not a hero piece, so the Seraph's gold is the rarer signal. But at a glance the Solar Lion still reads more vivid, and a mythic must not look weaker than the common in its own egg.
- **Frostcrown (0.1 %): level on chroma (0.37 against 0.42), behind on punch.** Two mythics that read as different families.

---

## 2. Clip gate (round 2 clips, `CLIP_NOTES.md`, `full_step1.txt`, `steps.txt`, `rest_delta.txt`)

**Measured (checked against the logs):**
- collision_free true; `collisions {}`; audit linear 0 on all seven clips.
- Loops closed (idle, walk, fly); walk slide 0.0004; stride 0.484.
- ground_min_z: idle -0.003, walk -0.004, takeoff -0.010, land -0.003, roar -0.003, cascade -0.003, fly +0.160. Rule -0.02. PASS.
- Pose limits: Neck 6.0 (limit 8), Chest vs Spine 2.5 (limit 5), head plus neck 15 (limit 30, builder's figure, consistent with the roar). PASS.
- Largest per-frame step: 17.2 deg (land f5, Foot_FR, was 17.8). Limit about 60. PASS.
- Rest: cascade, roar and land end at 0.0 deg from the ground rest pose. Takeoff ends in the flight cycle, as intended.

**Six-wing read, by view (the question you asked):**

| view | cascade hold f58-70 | fly f07-f14 | verdict |
|---|---|---|---|
| game (high behind) | three distinct tiers per side; the middle pair rises clearly at f36-44 and the lower pair spreads level at f52-62 | upper, middle and lower are separate shapes; the lower sits low at the flank | **PASS** |
| tq (three-quarter high) | upper V, middle out, lower near the ground at f44-78 | upper, middle and lower are separate at f10-f18 | **PASS** |
| front | the lower pair is a small row at flank height; the middle pair moves | two rows per side plus a small third | **PARTIAL** |
| Index icon (512 px, three-quarter front) | lower pair hidden | lower pair hidden | **FAIL** |

**Why the six-wing gate passes and no fallback is needed:** the gate that matters is what the player sees in motion. The game and tq views now show three tiers per side in both the cascade and the fly, which was the round 4 failure. The four-wing fallback is not triggered. The front and Index views are a model problem (MUST 1), not a clip problem.

**Other clip findings:**
- **Takeoff launch, f11-14 (NICE in round 4, still visible):** the upper pair's left wing crosses the lower-left edge of the halo for about 2-3 frames in the game view. It is brief, but it hides the hero at the launch. Fix in clip MUST 1.
- **Cascade ripple:** the middle pair rises clearly (f36-44, to 28) and the lower pair follows (to 20). The ripple reads as a sequence, not a flicker. Amplitude on the lower pair is modest.
- **Roar:** the halo lift at 17 is visible in the front view (f14-26). The jaw opens after the head. Reads as a call.
- **Land:** the in-between on the front legs is in; the flare and touch read.

**ANIM_REFS rule (owner's rule: 1-3 clips from animationreference.org per animation, cited):** PASS. The references now trace each item from the animationreference.org tag page to its item title, then to the Sakugabooru source frames (The Boy and the Heron, the takeoff wingbeat, the landing, the threat display). The multi-pair wing search is logged in the spider style (`/tags/wings`, `/tags/angel`, `/tags/butterfly`, `/tags/bird-flight`, `/tags/flying`, `/tags/dragon`). None has a multi-pair flyer, and the 4-frame lag is taken from the plan. This is the honest version of the rule.

---

## 3. MUST to reach 8.5 (round 6)

**Model**

**MUST 1 - Six wings on the Index card and at rest.**
- The lower pair must read as its own shape in the 512 px Index icon and in the 64 px portrait. It is hidden at the current rest pose.
- Lever: raise the lower pair's rest angle in `DISPLAY_POSE` (line 389 area, `"C": (10.0, -10.0, 0.0, -6.0)`) from up 10 to about 16, and sweep its tip out about 6 deg. The walk clash was at fwd -10 (thigh), and fwd is now -4, so the walk should still clear. Re-run the cut-through check and the walk.
- Target: on the Index icon, three separate wing shapes per side (upper, middle, lower), with the lower one clear of the flank silhouette. A reviewer counts six.

**MUST 2 - Punch against Solar Lion at 64 px.**
- Target on my 7-cell portrait: mean saturation at least 0.40 and saturated share at least 60 % (now 0.37 and 55 %).
- Lever A: widen the BLOOD corona band from 0.10 to 0.12 (`cor_o - 0.10` in the halo tube, `HALO` block). That adds red to the portrait and to the saturated share.
- Lever B, only if A is not enough: the wings' hue stays at 280; raise BODY_MID saturation by at most one step (196,112,234 to 200,108,238) and check the violet distance (the Shade Panther accent is hue 271).
- Guard: dark stays at 22 % or more, and near-white at 30 % or less, after both levers.

**Clips**

**MUST 3 - Keep the halo clear at the launch.**
- The upper pair's forward sweep at the launch (f11-14) must not cross the halo face. Hold the sweep back 2 frames, or lower the A tip about 4 deg for the launch frames, so the halo is unoccluded in the game view from f0 to f24.
- Re-check `pose_game_takeoff` f10 / f13 / f17.

## 4. TO 9+ (after the 8.5 bar)
1. **Lion read at 64 px:** strengthen the ruff so it reads at the icon without the 128 px zoom (a fuller dark mane frame on the cheeks).
2. **Front cascade:** make the lower pair a clear tier in the front hold (now a small row).
3. **Hero gold on the portrait:** widen the face-on gold so the portrait gold reaches about 130 px without losing dark mass.
4. **Front fly:** the lower pair's downstroke should show from the front, not only in the game view.
5. **Roar tilt:** a few more degrees of face-on tilt at the roar peak, if the head clearance allows (currently 0.055).

---

## 5. Pass / fail checklist (round 5)

**Model**

| item | result |
|---|---|
| Saturation at least 0.36 (beats Leviathan) | PASS (0.37 against 0.35) |
| Saturated share at least 40 % | PASS (55 %) |
| Near-white (accepted per section 0; guard 30 %) | ACCEPTED (28 %) |
| Dark mass at least 22 % | PASS (25 %) |
| Gold at least 20 px, portrait and game | PASS (108; 20) |
| Red at least 12 px, game camera | PASS (13) |
| Halo clearance at least 0.050 | PASS (0.055 / 0.080) |
| Tris at most 15k | PASS (11,288) |
| Six wings on the Index card | FAIL (lower pair hidden) |
| Lion read at 64 px | PARTIAL (moderate) |
| Outclasses Cosmic Leviathan at 64 px | PARTIAL (colour and gold yes; dark no) |
| Outclasses Solar Lion at 64 px | FAIL (punch) |

**Clips**

| item | result |
|---|---|
| collision_free, audit linear 0 | PASS |
| Loops closed; walk slide about 0 | PASS |
| ground_min_z at least -0.02 | PASS (min -0.010) |
| Neck at most 8 deg; chest vs spine at most 5 deg; head plus neck at most 30 deg | PASS (6.0; 2.5; 15) |
| Per-frame step at most about 60 deg | PASS (17.2) |
| No head shakes; no airborne spins | PASS |
| Acts in place; cascade, roar and land end at rest | PASS |
| Six wings in motion, game view | PASS |
| Six wings in motion, tq view | PASS |
| Six wings, front view | PARTIAL |
| Halo unoccluded at the launch | FAIL (wing crosses for 2-3 frames) |
| ANIM_REFS rule | PASS |

---

## 6. Next round: send with
- `EclipseSeraph_icon.png` (512 px Index card) and `_icons2_strip_64` / `_128` (portrait and game-camera cells).
- `_icons_strip_64` (7 cells) with the raw and strip counts.
- `_pose_game_takeoff_sheet.png` (f10, f13, f17) and `_pose_game_act_wingcascade_sheet.png` (f58-70).
- The step-check and rest-check output, and the cut-through check after MUST 1.

**Bottom line:** REVISE. The six-wing read in motion now passes in the game and tq views, and the clips are at the bar. The model is held back by the hidden lower pair on the Index card and by a punch gap against the Solar Lion at 64 px. Both are small, codeable changes. The owner's fallback to four wings is not triggered.
