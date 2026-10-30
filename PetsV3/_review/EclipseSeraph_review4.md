# Eclipse Seraph - model gate round 4 + CLIP GATE review 4 (2026-10-27) - REVISE

**Score: 7/10 overall for a 0.1 % MYTHIC** (ship at 8+).
- **Model: 8/10.** Round-3 colour and gold targets are met on my counter. Two small items remain: the game-camera red is 1 px short, and the wings and body are one colour mass.
- **Clips: 6/10.** The six-wing read FAILS in motion. In the cascade and the flight, only two wing pairs read. The owner's four-wing question is open (section 3).

**Six-wing clip gate: FAIL as built.** The step-1 build gate (tris, not a blob) still passes, but the signature cascade and the flight do not read as six wings from the front or the game camera. Decision needed from the owner (section 3).

Keep: the halo at 40 degrees with the 0.066 lip, the corona band at 0.10, the body and mane colours, the red slit eyes, the lilac face, the walk, the takeoff crouch, the roar wing order and jaw timing, and the land flare.

---

## 1. Model: round 3 MUSTs re-checked (my counter; builder's in brackets)

| 64 px item | round 3 (mine) | round 4 (mine) | target | status |
|---|---|---|---|---|
| mean saturation, portrait | 0.32 | **0.39** [0.39 icon, 0.370 strip] | >= 0.36 | PASS (Leviathan 0.35 [0.351]) |
| saturated share (sat > 0.35) | 35 % | **74 %** | >= 40 % | PASS (Leviathan 41 %) |
| near-white (lum > 200) | 27 % | **21 %** [16.8 icon] | <= 25 % | PASS |
| dark (lum < 90) | 20 % | **26 %** [22.7 raw] | >= 22 % | PASS (Leviathan 35 %, Solar Lion 22 %) |
| gold px, portrait | 90 | **103** (9.8 %) [70 / 108] | >= 20 | PASS (Leviathan 20, Frostcrown 100) |
| gold px, game camera | 18 | **22** (3.3 %) [27 / 25] | >= 20 | PASS, thin margin |
| red px, portrait | 20 | **32** (3.0 %) [49] | >= 10 | PASS |
| red px, game camera | 12 | **9** (1.4 %) [14] | >= 10 (I want 12) | **FAIL by 1 px on my counter** |

- **Halo clearance:** head 0.055, mane 0.080 (BU). Both at or above 0.050. PASS.
- **Tris:** 11,264 (builder). PASS, under 15k.
- **Brush size:** the builder enlarged the block to (0.11, 0.12, 0.10), added a sixth up-back tuft and lengthened the tufts. The game-camera red nonetheless fell from 12 px to 9 px on my counter, so the brush is not reading better from behind. Needs a fix (MUST 2).

**Lion read at 64 px:** moderate. At 128 px the dark ruff, white muzzle and red eyes read as a lion-angel. At 64 px it is a lilac winged cat with a dark ruff. Acceptable for a mythic with a gold halo; not as strong as the Solar Lion's gold-spiked ruff.

**Outclass check (64 px, my counter):**
- **Cosmic Leviathan (1 %):** PASS on chroma (0.39 against 0.35), gold (103 against 20), and red accent. FAIL on dark mass (26 against 35 %); the Leviathan's dark is body, not a hero piece.
- **Solar Lion (common, 54.9 %):** close on chroma (0.39 against 0.42). Gold is lower (103 against 267 px), but the Seraph's gold is one hero piece, not a mane. Distinct and premium enough; not a clear win on punch.
- **Frostcrown (0.1 %):** chroma and gold level (0.39 against 0.43; 103 against 100 px). Dark is higher on the Frostcrown (29 against 26 %). Two mythics that read as different families (lilac and steel blue).

**NEW MODEL ISSUE: the wings and the body are one colour mass.**
- BODY_MID (196,112,234), luminance 151; WING_LILAC (204,120,242), luminance 159. A difference of 8 luminance, with the same hue (281).
- In the flat render (game view) WING_LILAC is 30.7 % and BODY_MID 26.5 %, and they read as one purple body in the strips. The pairs are distinguishable only by shape and dark tips.
- This is a direct cause of the six-wing failure in section 3. Fix in MUST 1.

---

## 2. Clip gate (clip round 1, `CLIP_NOTES.md`, `_scratch/full_step1.txt`, `steps.txt`)

**Measured by the builder's scripts (checked):**
- collision_free true; `collisions {}`; audit linear 0 on all seven clips.
- Loops closed: idle, walk and fly loop_pos 0, loop_rot 0.
- Walk slide 0.0004; foot_z_var 0.0026; idle_foot_drift 0.0; stride 0.484.
- ground_min_z: idle -0.003, walk -0.004, takeoff -0.010, land -0.003, roar -0.003, cascade -0.003, fly +0.160. Rule: >= -0.02. PASS.
- Event times are normalised fractions of each clip (for example idle corona 0.667 = 80 / 120). They match the frame numbers in the brief. PASS.
- Pose limits (`step_check.py` measures each bone's local rotation from rest): Neck max 6.0 (limit 8). Chest vs Spine 2.5 (limit 5). Head plus neck pitch-up 15 (limit 30; the roar's Neck -6 plus Head -9 gives 15, consistent). PASS.
- Per-frame bone step: largest 17.8 deg (land f4, Foot_FL). Limit ~60 deg. PASS. Snap note in NICE 2.
- Cascade rest: f100 renders identical to f00 (same images). Exact rest pose. PASS.

**Visual check (the pose sheets, tq / game / front):**

| clip | read | result |
|---|---|---|
| idle | Halo drifts, head turns with holds, no shake. Wings breathe a few degrees. | PASS |
| walk | Level head and back, wings held in the display fan, legs step, no slide. | PASS |
| takeoff | Crouch, tail lifts, all wings rise, the launch on f11-13 reads. At f13 the upper-left wing sweeps across the halo's left edge for a frame or two. | PASS, with NICE 1 |
| land | Flare, wings brake forward then settle into the fan by f21. | PASS |
| roar | Wings open first (f08-14), halo lifts visibly (f14-26), jaw opens after the head (f26-40), mane flares, settles by f58. Reads as a roar call. | PASS |
| fly | Upper pair flaps clearly. Middle and lower pairs move in lock-step; the lower pair is not visible in the front or game views. | **FAIL for six wings** |
| act_wingcascade | Upper pair fans; middle pair changes about 10 deg; lower pair never visible; the ripple across three pairs does not read. | **FAIL for six wings and for the signature** |

**ANIM_REFS rule (owner: 1-3 clips from animationreference.org per animation, cited):**
- The references are real and well mapped (a clean table), but they are not for this pet. The clips are reused from the Blizzard Roc work (The Boy and the Heron, Sakugabooru), The Cat Returns, Avatar and Sea Beasts from earlier sessions, and a Sakugabooru wolf clip.
- The signature (the wing ripple) has no cited clip at all. The notes say the tags "lion roar", "bird wing fan" and "angel wings" had no usable entries on animationreference.org, but do not list the tags tried or the results. The precedent (Spider search, `ANIM_REFERENCES_1014.md`) logs the search.
- Result: **PARTIAL.** Required for round 4: cite at least one fresh animationreference.org clip each for the cascade and the fly, with frame times, or log the tags searched and the results.

---

## 3. The key question: does the cascade or the flight still read as six wings?

**No, not as built.**
- In every frame of the cascade and the fly (front and game views), the lower pair is hidden behind the body. The viewer sees two pairs: the raised upper V and the middle pair spread at shoulder height.
- The middle pair changes by about 10 degrees; its arm root cuts the chest above that (the builder's own note). So the cascade's three-tier ripple has nowhere to show. The visible motion is the upper pair fanning and the hands twitching.
- The middle and lower pairs share one stroke (C = B + 6 frames). Together with the 8-luminance colour merge (section 1), they read as one wing mass.
- The six-wing read holds only in the static display pose, and even there the lower pair needs the reader's effort.

**Deviations (ruled):**
1. **Roar: wings open before the head lifts. ACCEPT.** This is the reference's order (wings spread, then the call). The roar sheets show it clearly.
2. **Halo lift 0.20 (plan 0.22) and tilt 15 (plan 25). ACCEPT.** The lift is visible in the front roar sheet, and the 25-degree tilt would clip the head (clearance is only 0.055).
3. **Middle pair rises only about 10 deg before its root cuts the chest, so the fan comes from the hands. NOT ACCEPTED** as the six-wing solution. It is the cause of the cascade failure. Fix in MUST 3.
4. **Middle and lower pairs flap in step (C = B + 6). NOT ACCEPTED** for the six-wing read. They need separate motion (MUST 3).

**Decision for the owner (the owner's rule: four wings only if the gate fails):**
- **(A) One bounded six-wing fix round (my recommendation).** Apply MUSTs 1 and 3. If the game-camera cascade hold and the fly extremes then show all three pairs, the six-wing gate passes. If the lower pair is still invisible, go to (B).
- **(B) Four-wing fallback.** Drop the lower pair, re-plan the cascade as two pairs, and keep the colours and the gold. This needs the owner's OK before it is built.

I am not recommending (B) yet: the fix is a value split plus a root move, not a redesign. But the owner decides.

---

## 4. MUST (round 5)

**MUST 1 - Separate the wings from the body in value (model; fixes the six-wing read in every view).**
- `WING_LILAC` (line 22): (204,120,242) to **(214,150,246)**. Luminance 159 to about 180 (a gap of about 29 over the body's 151). Hue stays 280. Saturation falls from 0.50 to 0.39 on the feathers.
- Check after the change: mean saturation must stay at or above 0.36 on the 64 px portrait (the estimate is about 0.36, so check, do not assume). If it drops below, raise BLOOD's share (MUST 2) or the corona band.
- Keep the upper pair's hand coverts as the WING_IN highlight (line 171).

**MUST 2 - Game-camera red at least 12 px on my counter (now 9).**
- The brush is the red for the back. Keep the block (0.11, 0.12, 0.10) but move it so it sits clear of the body from the high rear camera: lower it by about 0.03 BU and push it back about 0.03 BU, so the tufts are not hidden by the haunch. Alternatively lengthen the up-back tuft.
- Target: at least 12 red px in the 64 px game-camera icon on my counter. Re-measure.

**MUST 3 - Six wings in motion (the signature).**
- **Middle pair root:** move the B shoulder root back from the chest front onto the spine base (Wing_B root, about y -0.20 to -0.05), so the B arm can rise above 10 deg without cutting the chest. Re-run the cut-through check (`_scratch/path6.py`).
- **Lower pair in the in-place acts:** the cascade is in place and the hind legs stand, so the walk clash (C fwd >= -4) does not apply in the cascade hold. Let C rise 16 to 20 deg at the tip in the hold (f58-64) and in the fly extremes, so its tips show past the flank in the front and game views.
- **Break the lock-step:** give C a different amplitude or a 4-frame lag from B in the fly (for example B flaps 10 deg and C 14 deg, C lagging 4 frames), so the two read as separate pairs.
- **Target:** in the game-camera cascade and the fly, all three pairs visible as distinct shapes in at least 3 frames each (I will count on the strip).

**MUST 4 - Cite the references (owner rule).**
- Before the cascade and the fly are approved: at least one fresh clip from animationreference.org for each, with frame times and key poses. Or, if none fits, log the tags searched and the results (precedent: the spider search).

## 5. NICE
1. **Takeoff f13:** the upper-left wing sweeps across the halo's left edge for a frame or two. Reduce the upper pair's forward sweep at the launch by about 4 deg (`DISPLAY_POSE` fwd), or hold it one frame later.
2. **Land f4:** the 17.8-deg foot step is under the limit, but it is a snap at the flare. Add one in-between frame (about 0.3 deg out) on Foot_FL.
3. **Halo at the roar:** the tilt to 15 reads, but a 2-degree extra tilt at the roar peak would help the face-on read (only if the clearance holds at 0.05).
4. **Gold margin:** game-camera gold is 22 on my count and 25 to 27 on the builder's. Keep it above 20 after MUST 1 and 2.

---

## 6. Pass / fail checklist

**Model (round 4)**

| item | result |
|---|---|
| Saturation at least 0.36 (and beats the Leviathan) | PASS (0.39 vs 0.35) |
| Saturated share at least 40 % | PASS (74 %) |
| Near-white at most 25 % | PASS (21 %) |
| Dark mass at least 22 % | PASS (26 %) |
| Gold at least 20 px, portrait and game | PASS (103); PASS, thin (22) |
| Red at least 10 px, game camera | FAIL, 1 px short on my counter (9; builder 14) |
| Red at least 10 px, portrait | PASS (32) |
| Halo clearance at least 0.050 | PASS (head 0.055, mane 0.080) |
| Tris at most 15k | PASS (11,264) |
| Wings separate from body in value | FAIL (luminance gap 8) |
| Lion read at 64 px | PARTIAL (moderate; strong at 128 px) |
| Outclasses Cosmic Leviathan at 64 px | PARTIAL (wins chroma, gold, red; loses dark mass) |
| Outclasses Solar Lion at 64 px | PARTIAL (close on chroma; less gold mass, one hero piece) |
| No violet anywhere; accents BLOOD and GOLD | PASS |

**Clip gate (clip round 1)**

| item | result |
|---|---|
| collision_free, audit linear 0 | PASS |
| Loops closed (idle, walk, fly) | PASS |
| Walk slide about 0 | PASS (0.0004) |
| ground_min_z at least -0.02 in every clip | PASS (min -0.010) |
| Neck at most 8 deg | PASS (6.0) |
| Chest vs Spine at most 5 deg | PASS (2.5) |
| Head plus neck pitch-up at most 30 deg | PASS (15, builder's, consistent with the roar) |
| Per-frame bone step at most about 60 deg | PASS (17.8) |
| No head shakes | PASS |
| No airborne spins | PASS |
| Acts in place, ending at rest | PASS (cascade f100 = f00) |
| Readable beats: idle, walk, takeoff, land, roar | PASS |
| Readable beats: cascade ripple | FAIL |
| Six wings read in flight (fly) | FAIL |
| Six wings read in the signature (cascade) | FAIL |
| ANIM_REFS rule (animationreference.org, cited per animation) | PARTIAL |

---

## 7. Next round: send with
- `_icons_strip_64.png` (7 cells) and `_icons2_strip_64.png` / `_128.png` (4 cells), with raw and strip counts.
- `flat_game.png` with the value shares.
- Game-camera and front pose sheets for the **cascade** and the **fly**, at every frame in the table, with the three pairs marked.
- The new animationreference.org citations (or the tags searched, with results).
- The `step_check` and `path6` output after MUST 3.

**Bottom line:** REVISE. The model is close: colours, gold, dark mass and red (1 px short) all pass on my counter, and the wings need a value split. The clips are clean on every limit, but the six-wing read fails in the cascade and the flight. Run one bounded six-wing fix round (MUSTs 1 to 4). If the lower pair still does not show from the game camera, the four-wing fallback is the owner's decision.
