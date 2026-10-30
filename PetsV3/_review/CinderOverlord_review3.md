# Cinder Overlord - MODEL round 3 + CLIP GATE review (2026-10-27) - REVISE

**Verdict: REVISE.**
- **Model: 7/10** (review 2 was 6/10). Target to ship: 8/10 or better.
- **Clip gate: NOT PASSED.** Blocked by the animation-reference rule (idle and walk), a 6-degree Spine yaw against the 5-degree chest limit, and a centre-blade reseat that is faster than its rise. Fix those and it can go to the owner.

Round 3 is a real step. The eyes read from the front again, the lava cores show, the body is no longer the magenta family, and the game view reads volcanic. It still does not outclass the Fire egg or the 1 % secrets: it is the dimmest serpent in the lineup at 128 px, and its mass is still thin next to Rex and Leviathan.

## 0. What I looked at

- Coordinator's round-3 message and `CinderOverlord/MODEL_NOTES.md`, `CLIP_NOTES.md`, `ANIM_REFS.md`.
- Clip data read directly from `CinderOverlord/CinderOverlord.json` (per-frame quaternions and molt position keys). I computed the joint limits myself, not only from the builder's notes.
- `CinderOverlord/_scratch/clipgate.txt`, `clipgate_events.txt`, `shares_strict.json`, `gate_clip_out.txt`, `game_icon.json`, `model_result.txt`.
- Renders: `model_front.png`, `close_front.png`, `_icons2_strip_64.png`, `_icons_strip_128.png`, `flat_game.png`, `gamelook_game.png`, `_pose_tq_sheet.png` (22 beats), `_cv_acts_side.png`, `_cv_walk.png`, `_cv_molt_front.png`.
- Owner rule and clip rules: `Creature Animation.md`, the animation-reference memory note, and `_review/ANIM_REFERENCES_1014.md` (where the roar and molt references came from).
- Heights of the comparison pets from `pets/*.py`.

I did not run Blender or Studio. The collision result, the ground minimum of -0.006 and the tri count are the builder's headless numbers; I accepted them without re-running.

## 1. Clip gate (measured from `CinderOverlord.json`)

| Check | Measured | Limit | Result |
|---|---|---|---|
| collision_free | true (builder, headless) | 0 | PASS (not re-run) |
| ground_min_z | -0.006 in all clips | >= -0.02 | PASS (builder's number) |
| Loops closed | idle first = last exact; walk wrap step 1.3 deg, as a normal frame | closed | PASS |
| Rest at end | act_molt and roar last frame 0.00 deg from rest | exact rest | PASS |
| Neck bones (each) | idle 2.1, walk 1.1, roar 4.0, molt 8.0 | <= 8 deg | PASS (molt is exactly at the limit, no margin) |
| Head + neck world pitch (signed sum) | idle 2, walk 0.6, roar 4, molt 2 (head counter-pitches -22) | <= 30 deg | PASS |
| **Chest vs spine** (Spine = chest base) | molt Spine yaw **-6 to +6 deg**; walk +/-3 deg; idle 0 | <= 5 deg | **FAIL** in molt (MUST 2) |
| Head shake | Head yaw: idle +/-1.2 (one slow sway, C1), walk +/-0.5, roar and molt 0; no fast oscillation | none | PASS |
| Airborne spin / root travel | no `pos` key on the root in any clip; stays in place | none | PASS |
| Quaternion sign flips | 0 in all four clips | none | PASS |
| Max joint step per frame | molt 6.3 (Crown_3), roar 6.3 (Jaw), idle 5.0 (tail flick) | <= 60 deg | PASS |
| Walk wave order | peaks Spine f12, Body1 f14, Body2 f18, Body3 f20, Body4 f24, Tail1 f26, Tail2 f30, Tail3 f32, Tail4 f36: head to tail, 2-4 f lag | head to tail, 3 f lag | PASS (matches the builder's claim) |
| Walk amplitude | 3 / 6 / 9 / 10 / 10 / 9 / 8 / 7 / 6 deg | as written | PASS |
| Event frames | idle 30/80/90; walk 12/36; roar 20/30; molt 22/48/56 | as written | PASS |
| Molt centre blade reseat vs rise | rise peak **5.2 deg/f**; reseat peak **6.3 deg/f** (Crown_3, f80-104) | reseat slower than rise (ref #9) | **FAIL** (MUST 3) |
| Molt outer blades reseat | Crown_1 / Crown_5 reseat ~1-2.7 deg/f, no overshoot | slower than rise | PASS |
| Molt neck arch | 8 deg per neck bone over three bones (24 total), head level | <= 8 per bone | PASS |

Crown blade position keys: the five crown bones carry a small position offset in the molt (0.025 to 0.05 stored units, `ps` 0.0526). That is the "lift off the socket" motion. At render scale I could not see whether the blade bases stay on the mount; check it on the close molt frames (NICE 4).

### Animation references (owner rule)

`Creature Animation.md` and the owner's memory rule both say: before keyframing, pull 1-3 clips from animationreference.org, cite the frames, and put them in the plan.

- **Roar and molt: PASS.** They cite #3 (Sea Beasts, heavy-head roar), #6 (Monsters University, crouch then explode) and #9 (Children of the Sea, heavy rise, slower fall). These are on animationreference.org in `_review/ANIM_REFERENCES_1014.md`.
- **Idle and walk: FAIL.** `ANIM_REFS.md` cites Wikimedia Commons footage (a snake on sand, a king cobra gif). That is not animationreference.org, and the owner has not approved it as a substitute.
- **The search was incomplete.** `ANIM_REFS.md` lists the tags tried as `/tags`, `/tags/dragon` (Dragon Ball beams) and `/tags/creature` (generic titles). It did not try `/tags/creature-animation` (about 2.4k clips, the creature tag per the site note), `/tags/animals` (532), `/tags/body-mechanics` (76) or `/tags/walk-cycle` (367). Those are the tags that could hold a slither or a breath.

## 2. Model (round-2 MUSTs, checked)

| Item | Result | Note |
|---|---|---|
| M1 cap 65 deg, rose slits raised | PASS | The pink slits show beside the brows in `close_front.png` and `model_front.png`. The two black marks lower on the face are nostrils, not eyes. |
| M2 V muzzle | PARTIAL | The muzzle is narrower, but from the front it is still a rounded block with the jaw merging into it. Not a clear V. (NICE 2) |
| M3 dorsal saddle, game shares | PASS on the body, check the numbers (MUST 4) | `flat_game.png` and `gamelook_game.png` show the wine body is now the main colour, with the dark rings and lava vents on it. The two share files disagree (see MUST 4). |
| M4 RAD[1..3] | PASS | Body is thicker in the game view. The lower body still reads thinner than Rex or Leviathan (MUST 5). |
| M5 lava cores + lava crown gem | PASS | Orange vent cores show on the flanks in `flat_game.png` and at the tail tip; the crown centre gem is warm. |
| NICE 1 / 3 | PASS | Outer gold 0.020; the centre blade gold kept. |
| Gold at 64 px | **CONFLICT** (MUST 4) | `game_icon.json` says 27; `gate_clip_out.txt` says 25 (the gate minimum). |
| Tris | 10,852 | PASS (<= 15k). Matches `model_result.txt`. |
| Height | 10.5 | Tallest of the Fire egg (Phoenix 10.0, Cerberus 8.5, Ivonrath 7.5, MoltenBoar 6.6, LavaGolem 7.0) and of the secrets (Rex 10.0, Leviathan 10.0). |

## 3. Questions from the coordinator

**Does it read as Fire?** Yes, now. The wine body, the dark saddle, the lava cores and the lava tail tip read volcanic in the game view and at 128 px. The orange is small at 64 px, but the tail tip and the crown gem carry the warm note there. The distinctness from the Leviathan holds (no magenta).

**Does it outclass the Fire egg and the 1 % secrets?** No.
- At 128 px (`_icons_strip_128.png`) the Cinder is the dimmest serpent in the strip. The Phoenix (bright ember flame), Ivonrath (bright red winged wyrm), Rex (bright blue with cyan crystals) and Leviathan (magenta with gold crown and fins) all read more striking.
- It is the tallest of the Fire egg and matches the secrets on height, so height is not the gap. The gap is contrast and mass: a dark, thin tube against a dark slate background recedes.
- Distinctness now passes against the Leviathan and the Ivonrath (the saturation gap is enough).

**Fierce or cute?** Fierce. No pink, a dark back, a wedge skull, fangs and a visible pink eye pair from the front. The concern from round 2 about a blank face is resolved.

**Segmented worm?** From above (`gamelook_game.png`), the dark rings on the thin tube read as a segmented larva. That is a design question for the owner (NICE 1).

**Most impressive pet of the Fire egg?** No. The Phoenix and Ivonrath are more striking at icon size. The Cinder is the top of the egg by odds, so it has to be the most imposing. It is not yet.

## 4. MUST list (prioritized)

**MUST 1 - Animation references for idle and walk (blocks the clip gate).**
- Re-search animationreference.org with the tags `/tags/creature-animation`, `/tags/animals`, `/tags/body-mechanics` and `/tags/walk-cycle`. Look for a slither, a coil, a sway, a tail flick or a reared sway.
- Pull 1-3 clips for idle and walk, step through them, note the key poses and frames, cite the clip titles, tags and frames in `ANIM_REFS.md` and the plan (`_review/CinderOverlord_plan.md` section 10 still says "TBD").
- If none fits, the owner must approve the Wikimedia fallback in chat before the idle and walk are accepted. The fallback is not allowed by the rule as written.
- The roar and molt references already comply; keep them.

**MUST 2 - Spine yaw over the chest limit in the molt (blocks the clip gate).**
- The Spine (the chest base) reaches 6 deg in `act_molt`. The limit is 5 deg. Reduce the Spine's molt ripple key to 5 deg (the Body1-4 and tail ripple can stay at 5.5-6, since the chest limit only applies to the Spine).
- Report the chest number in `CLIP_NOTES.md` next to the neck number, so the gate can see both.

**MUST 3 - Centre blade reseats faster than it rises (blocks the clip gate).**
- Crown_3 rises at 5.2 deg/f and reseats at 6.3 deg/f (f80-104). The reference (#9) and the clip note both say the reseat is slower.
- Stretch the centre blade's reseat keys so its peak is at or below the rise (about 4.5 deg/f): spread f80-104 to f80-110, or ease the reseat curve. Keep the outer blades as they are (they already reseat at about 1 deg/f).

**MUST 4 - Reconcile the gate numbers (blocks the model pass).**
- The two result files disagree, both dated 18:13:
  - gold at 64 px: 25 in `gate_clip_out.txt` vs 27 in `game_icon.json` (the coordinator quotes 27); the gate minimum is 25, so 25 passes with no margin.
  - game shares: PLUM_OBS 40.6 / OBS_D 40.7 in `gate_clip_out.txt` vs 43.2 / 37.8 in `shares_strict.json`. Obsidian at 40.7 fails the target of 40 or less.
- Re-run one share script on the current `flat_game.png`, `flat_side.png`, `flat_tq.png` and the 64 px icon, write one file, and quote only that file.

**MUST 5 - Outclass: the dimmest serpent in the lineup (blocks the model pass).**
- The Cinder's wine body (144,80,96) is the lowest-contrast main colour in the Fire egg and the strip. Its brightest channel is 144, so at 128 px it sits in the dark slate background.
- Lift the body's brightest channel at the same hue to about 160, for example (160,88,104) (H ~347, S ~0.45, luminance ~111). Keep OBS_D (62,50,64) for the saddle and rings, so the obsidian share does not go up.
- Re-test the 64 px icon for pink. If it turns pink, stop at 150, which is still lighter than now.

## 5. NICE list

1. **Segmented-worm read in the game view.** The dark rings across the tube read as a centipede or larva from above (`gamelook_game.png`). Option: keep the full ring band on the back and neck, but drop the flank rings to about 60 % of their width on Body1-4. Owner to judge; accept if the banded read is wanted.
2. **V muzzle from the front.** Still rounded. Narrow the front station a little more, or give the jaw a forward point, so the front silhouette reads as a wedge.
3. **Molt readability at game distance.** The lift reads in side view and the crest reads from the front at f28-50 (`_cv_molt_front.png`). At 5 studs the one-by-one lift is subtle; a slightly longer lift (lag 3 f instead of 2 f) would make the sequence legible.
4. **Blade bases.** Check the close molt frames for the blade bases staying on the crown mount, since the crown bones carry position keys.
5. **Walk in place.** The walk has no root travel (the body stays in place and the game moves the pet). Confirm in Studio that the in-game speed matches the 5.19 BU stride, so the slither does not skate or outrun its wave.
6. **Neck at the limit.** The molt neck bones hit 8.0 deg exactly. Give them 0.5 deg of margin (7.5 deg) so a rounding error cannot fail the gate.

## 6. Pass / fail checklist (round 3)

| # | Check | Result |
|---|---|---|
| 1 | Tris <= 15k | PASS (10,852) |
| 2 | Collision free, ground >= -0.02, loops closed, linear 0 | PASS (builder's numbers; loops re-checked) |
| 3 | Neck bones <= 8 deg | PASS (at the limit) |
| 4 | Head + neck pitch-up <= 30 deg | PASS (2-4 deg world) |
| 5 | Chest vs Spine <= 5 deg | **FAIL** (molt 6 deg) |
| 6 | No head shake | PASS |
| 7 | No airborne spin | PASS |
| 8 | Quaternion signs continuous | PASS (0 flips) |
| 9 | Joint steps <= 60 deg/frame | PASS (max 6.3) |
| 10 | Acts in place, end at rest | PASS |
| 11 | Walk wave head to tail | PASS |
| 12 | Molt readable beats | PASS in side and front; subtle at game distance (NICE 3) |
| 13 | Reseat slower than rise (ref #9) | **FAIL** (centre blade) |
| 14 | Animation references: roar, molt | PASS (animationreference.org) |
| 15 | Animation references: idle, walk | **FAIL** (Wikimedia, not animationreference.org) |
| 16 | Fire identity reads | PASS (volcanic at 128 px and in game) |
| 17 | Distinct from CosmicLeviathan / Ivonrath | PASS |
| 18 | Face reads from the front (eyes) | PASS |
| 19 | Outclasses Phoenix, Ivonrath, Rex, Leviathan | **FAIL** (dimmest serpent at 128 px) |
| 20 | Gold >= 25 px at 64 px | **CONFLICT** (25 vs 27; re-measure) |
| 21 | Shares: body main colour, obsidian <= 40 % (game) | **CONFLICT** (43.2 / 37.8 vs 40.6 / 40.7) |

## 7. Next round

Send with the fixes applied:
- the animationreference.org reference table for idle and walk (MUST 1), or the owner's written OK for the fallback;
- `CLIP_NOTES.md` with the chest (Spine) number and the centre-blade reseat speed after the fix (MUST 2 and 3);
- one reconciled share file and gold count (MUST 4);
- the 64 px and 128 px icon strips with the lifted body (MUST 5), `gamelook_game.png`, and `_cv_molt_front.png` at game distance.

The clip gate goes to the owner after MUST 1-3 pass; the model goes to the owner at 8/10 after MUST 4-5.
