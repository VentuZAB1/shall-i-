# Cinder Overlord - round 4 review (2026-10-27): MODEL REVISE 7/10, CLIPS APPROVED WITH FIXES 8/10

**Model verdict: REVISE, 7/10** (round 3 was 7/10). Target to ship: 8/10 or better.
**Clip verdict: APPROVED WITH FIXES, 8/10.** The measured clip numbers pass the gate. The fixes are a re-render of the molt sheets and disclosure of the reference source.

The body is no longer pink, and the pet reads as fire at 128 px. The colour fix moved it into the same red family as Ivonrath and Phoenix, though, and the new accent and hot-core colours are copies of Phoenix. The gold count is also inflated, and the molt renders are stale.

## 0. What I looked at

- Coordinator's round-4 message: the five round-3 MUSTs and the ember ruling.
- `CinderOverlord/CLIP_NOTES.md`, `MODEL_NOTES.md` (round 4), `ANIM_REFS.md` (section D, Haku), and `_scratch/gate_r4.json`, `_scratch/shares_all.json`, `_scratch/hue_cmp.py`, `_scratch/clipgate_r4.txt`.
- The clip data, recomputed from `CinderOverlord/CinderOverlord.json` (quaternions per frame; the 22:37 export).
- Source colours in `pets/CinderOverlord.py` (lines 18-26, dated 22:37), and the sibling palettes of Ivonrath, InfernoPhoenix, MoltenBoar, LavaGolem, Cerberus, ThunderRex, CosmicLeviathan, BlackDragon. Hue distances computed from the RGB values.
- Renders: `_scratch/hue_cmp.png`, `renders/_model_sheet.png`, `renders/_icons_strip_64.png` / `_128.png` (both 22:37), `_molt_r4_front|side|tq.png` (22:33), `close_front.png` (18:13).

Not verified:
- I cannot view the Haku footage (the brief limits me to files and images I have been given), so I accept the frame observations in `ANIM_REFS.md` section D as the builder recorded them.
- I did not re-measure the gold count from pixels.
- The collision result and the ground minimum are the builder's headless numbers.

## 1. Round-3 MUSTs

| # | Round-3 MUST | Round-4 result | Verdict |
|---|---|---|---|
| 1 | Animation refs for idle and walk, from animationreference.org | Haku, *Spirited Away*, via the site tag `/tags/creature-animation` -> Sakugabooru #225387; tags tried and clips rejected are logged; frames D1-D3 recorded. | **PASS**, with a disclosure: the frames were stepped on the Sakugabooru post, not the site overlay. The memory rule says to tell the owner when that happens (NICE 1). |
| 2 | Spine (chest) yaw <= 5 deg in the molt | Spine max **4.5 deg** (signed y -4.5 to +4.5). Neck bones **7.5** each (<= 8). | **PASS** (recomputed) |
| 3 | Centre-blade reseat slower than its rise | Crown_3 rise peak **5.18 deg/f**, reseat peak **4.62 deg/f** (f84-95). Outer blades: Crown_1 reseat 0.99, Crown_5 2.74 deg/f. No overshoot; final angle 0.00. | **PASS** (recomputed) |
| 4 | One numbers file; 18:13 files retired | `gate_r4.json` is the stated single file; the 18:13 files are renamed `STALE_1813_*`. **But** the gold count method is inflated (MUST 3) and two inputs are stale (MUST 4). | **PARTIAL** |
| 5 | Colour: remove the pink, keep the lead's ember ruling judged | No pink in the body now; the game-view shares are 42.4 / 34.1 (body / obsidian, target >= 40 / <= 40). The accent and hot cores **copy Phoenix** and the body sits **7.5 deg from Ivonrath** (MUST 1 and 2). | **FAIL on distinctness**, PASS on the fire read |

## 2. Clip gate (recomputed from the JSON)

| Check | Value | Limit | Result |
|---|---|---|---|
| Sign flips (all clips) | 0 | 0 | PASS |
| Rest at end (roar, molt) | 0.00 deg | exact | PASS |
| Idle loop (first vs last) | 0.000 deg | closed | PASS |
| Walk loop (first vs last) | 0.76 deg (one frame of motion) | closed | PASS |
| Neck bones (each), molt | 7.5 | <= 8 | PASS (0.5 margin) |
| Head + neck world pitch, molt | signed sum 0.0 to 2.0 (head counter-pitch -20.5) | <= 30 | PASS |
| Spine, molt | 4.5 | <= 5 | PASS |
| Walk wave order | Spine f12 ... Tail4 f36, head to tail | head to tail | PASS (unchanged) |
| Centre-blade reseat vs rise | 4.62 vs 5.18 deg/f | reseat slower | PASS |
| Joint step per frame | max 6.3 deg (not re-checked for round 4; within 60) | <= 60 | PASS |
| Collision, ground, linear | builder's headless: collision_free true, ground -0.006, linear 0 | 0 / >= -0.02 | PASS (not re-run) |

The lift is now 3-frame staggered (NICE 3 from round 3). The reseat sits just under the rise (4.62 against 5.18): correct, but the margin is small.

## 3. Colour: the lead's ember ruling

### What the numbers say

Hue is in degrees; the distance is the smaller angle between hues.

| Colour | RGB | Hue | Sat | Lum | Closest sibling | Distance |
|---|---|---|---|---|---|---|
| Cinder body PLUM_OBS | (166,66,50) | 8.3 | 0.70 | 94 | Ivonrath RED (198,42,40), H 0.8 | **7.5 deg** |
| Cinder body vs Phoenix EMBER (232,78,32) | | | | | InfernoPhoenix EMBER, H 13.8 | 5.5 deg |
| Cinder accent ROSE (255,84,48) | | 10.4 | 0.81 | 131 | InfernoPhoenix EMBER (232,78,32), H 13.8 | **3.4 deg** |
| Cinder accent vs Cerberus RED (255,50,40) | | | | | Cerberus.RED, H 2.8 | 7.6 deg |
| Cinder LAVA (255,128,24) | | 27.0 | 0.91 | 154 | InfernoPhoenix LAVA (255,128,24) | **identical** |
| Cinder PALE_S (222,194,158) | | 33.7 | 0.29 | 198 | Ivonrath BELLY (232,140,90), H 21.1 | 12.6 deg, sat 0.29 vs 0.61 |
| Cinder GOLD (255,196,50) | | 42.7 | 0.80 | | house gold (every rare pet) | shared on purpose |

Ivonrath's crimson and Phoenix's ember are both in the 0-14 degree band, and so is the whole Fire egg's accent set (Cerberus RED H 3, MoltenBoar MAGMA H 23, LavaGolem MAGMA H 37). The egg has no free hue near red-orange. So the Cinder cannot be distinct from both by hue alone. It has to separate by value, saturation, silhouette and the accent's place in the pet.

### What the picture says

- `hue_cmp.png` (A2 row, 128 px): the Cinder reads as a red-brown serpent with a gold crown. Ivonrath reads as a bright crimson winged wyrm. The silhouettes are clearly different. The bodies are close, but A2 is browner and darker than Ivonrath, so the two separate at 128 px.
- At 64 px (`_icons_strip_64.png`): the Cinder is a red serpent with a gold crown, and it is the same size as the Ivonrath icon. The two are readable as different pets, but the colour family is shared.
- The Phoenix is a bright flame bird at 128 px. The Cinder's accent is the Phoenix's own neck colour, so the two pets share their hot tone.

### Rulings

**(a) The ember hue is accepted in principle.** It is clearly not pink, and it reads fire. The builder's pick, A2, is the right direction.

**(b) The accent (255,84,48) is REJECTED** as a copy of InfernoPhoenix EMBER (3.4 deg). The rule is "never copy a sibling's accent".

**(c) The LAVA hot cores (255,128,24) are REJECTED** as an exact copy of InfernoPhoenix LAVA. The hot cores and the tail tip need a colour the Phoenix does not use, or a value shift from it.

**(d) Ivonrath: distinct by silhouette, value and saturation, not by hue.** Accept, and do not lift the body value further (that would bring back the pink and push it toward Ivonrath's bright crimson).

**(e) Pink check: PASS** at 128 px. No pink on the body or the vents in the current icon strip.

## 4. Gate numbers

- **Gold at 64 px: 35 on the portrait is inflated.** The builder says 32 of the 35 pixels sit in the crown rows, and the counter's hue window (29 to 58 degrees) catches the blend between the gold (H 43) and the new ember edges (H 10). Anti-aliased blends are not gold. The count went from 27 to 35 when only the ember edges changed, which is the sign of a counter artefact. The honest gold count is unknown until it is re-measured with a tight window (MUST 3).
- **Shares, flat_game:** body 42.4, obsidian 34.1, ember accent 6.8, lava 2.8. The method is the nearest palette colour (every figure pixel). This is consistent with `shares_all.json`. Pass.
- **Side and tq:** body 48.9 / 41.4, obsidian 22.5 / 25.8, warm pale 10.3 / 11.6. Pass (the pale band keeps its share).

## 5. Stale renders (blocks the judgement of the molt and the face)

- `renders/_molt_r4_front.png`, `_molt_r4_side.png`, `_molt_r4_tq.png` are dated **22:33**, four minutes before the palette file (**22:37**). They still show the pink body, the pink vents and the pink crown edges. The molt cannot be judged in the current colour from them, so this round's molt judgement is provisional.
- `renders/close_front.png` is dated **18:13**. It predates the round-3 face fixes and the ember accent, so the face cannot be judged in the current palette.

## 6. Fierce, Fire, outclass

- **Fierce or cute:** fierce. The ember body, the dark saddle, the fangs and the claws all read predator. No cute read survives at 64 or 128 px.
- **Reads as FIRE:** yes. The ember body, the lava cores and the gold crown read as volcanic at 128 px. This is the main improvement this round.
- **Distinct from Ivonrath:** partial. Silhouette and value separate them; colour family is shared (7.5 deg). Accept with the rule in section 3(d).
- **Outclasses the Fire egg and the 1 % secrets at 64 / 128 px:** not yet.
  - The Phoenix is a brighter, more striking flame bird at 128 px.
  - ThunderRex is a bright blue, heavier silhouette.
  - The Cinder is now an even match for Ivonrath on impact, and it has the gold crown as its hero.
  - The Cinder's two hot-tone colours are the Phoenix's, so it loses the warm-tone contest it should win. Fixing MUST 1 and MUST 2 is the lever: an accent the Phoenix does not use will make the Cinder's hot points read as its own.

## 7. MUST list (prioritized)

**MUST 1 - The accent copies InfernoPhoenix EMBER (3.4 deg).**
- `pets/CinderOverlord.py` line 25: `ROSE = (255, 84, 48)` is 3.4 degrees from the Phoenix neck colour (232,78,32).
- Pick a new accent at least 15 degrees from every Fire-egg colour (Phoenix EMBER H 14, Ivonrath RED H 1, Cerberus RED H 3, MoltenBoar MAGMA H 23, LavaGolem MAGMA H 37) and at least 20 degrees from the Phoenix's warm tones. It must read hot at 64 px and must not read pink (hue 330 to 350 failed).
- Check it in a `hue_cmp`-style strip against Phoenix, Ivonrath and ThunderRex at 64 and 128 px before the lead signs it off. Since the egg has no free hue near red-orange, a value or saturation contrast (a lighter hot cream on the slits, or a deeper ember) is acceptable if the hue cannot be separated.

**MUST 2 - LAVA hot cores are an exact copy of InfernoPhoenix LAVA (255,128,24).**
- Line 26: `LAVA = (255, 128, 24)`. Change it to a distinct warm tone (for example a hot amber, a few degrees off the Phoenix's), and re-check the 64 px icon for the orange read, since the lava cores are the Fire signal at 64 px.
- Do this together with MUST 1; the two colours must not collide.

**MUST 3 - Re-measure the gold count with a tight window.**
- The 35 is a counter artefact of the blend pixels (section 4). Re-run `_tools/game_icon.py` with gold H 38-48, saturation >= 0.6, and blend pixels excluded. Report the portrait and game counts from that run.
- Gate: >= 25 on the portrait. If the tight count is below 25, add gold on the centre blade's sides (the crown is the hero).

**MUST 4 - Re-render the stale renders before the owner sees them.**
- Re-render `_molt_r4_front|side|tq` (the full molt beats, 0 to 110) from the current 22:37 model.
- Re-render the face close-up (`close_front` and `close_side`), since the eyes and brows now sit against the ember accent.
- Re-run `_model_sheet.png` and the 64 / 128 icon strips after MUST 1 and MUST 2 land.

## 8. NICE list

1. **Disclose the reference source.** The Haku frames were stepped on the Sakugabooru post. The memory rule for this site says to say so when the site overlay is not used. State it to the owner with the clip title and the tag.
2. **Body hue against Ivonrath.** Keep the body's saturation at or below 0.70 and its luminance at or below 94 (do not lift it), so the Cinder stays darker and duller than Ivonrath's crimson.
3. **Crown centre blade.** The centre blade's gold sides were kept at 0.034; if the crown needs to outshine the Phoenix at 128 px, lengthen the centre blade (0.30 to about 0.32) rather than adding colour.
4. **Molt reseat margin.** Crown_3 reseats at 4.62 deg/f against a 5.18 rise. That passes, but a 10 % margin would give a safer gate (about 4.5 deg/f).
5. **Walk speed.** Still open from round 3: confirm in Studio that the in-game speed matches the 5.19 BU stride, so the slither does not skate.

## 9. Pass / fail checklist (round 4)

| # | Check | Result |
|---|---|---|
| 1 | Tris <= 15k | PASS (10,852) |
| 2 | Height 10.5, tallest of the Fire egg and the secrets | PASS |
| 3 | Collision free, ground >= -0.02, loops closed, linear 0 | PASS (builder's numbers) |
| 4 | Neck bones <= 8 deg | PASS (7.5) |
| 5 | Head + neck world pitch <= 30 deg | PASS (0-2) |
| 6 | Chest (Spine) <= 5 deg | PASS (4.5) |
| 7 | No sign flips, no head shake, no spin | PASS |
| 8 | Acts end at rest | PASS |
| 9 | Centre-blade reseat slower than rise | PASS (4.62 vs 5.18) |
| 10 | Animation refs for idle and walk (site clip) | PASS, with disclosure (NICE 1) |
| 11 | Animation refs for roar and molt | PASS (#3, #6, #9) |
| 12 | No pink on the body or vents (icon) | PASS |
| 13 | Reads as Fire | PASS |
| 14 | Gold >= 25 px at 64 px | **UNVERIFIED** (35 is an inflated count; MUST 3) |
| 15 | Accent distinct from every Fire-egg sibling | **FAIL** (3.4 deg from Phoenix EMBER) |
| 16 | Hot cores distinct from every sibling | **FAIL** (identical to Phoenix LAVA) |
| 17 | Body distinct from Ivonrath | PARTIAL (7.5 deg hue; separated by value and silhouette) |
| 18 | Fierce, not cute | PASS |
| 19 | Game shares: body >= 40 %, obsidian <= 40 % | PASS (42.4 / 34.1) |
| 20 | Molt judged in the current palette | **FAIL** (renders stale at 22:33) |
| 21 | Face judged in the current palette | **FAIL** (close-up dated 18:13) |
| 22 | Outclasses Phoenix, Ivonrath, Rex, Leviathan at 64/128 px | **FAIL** (not yet; the warm-tone contest is lost to the Phoenix) |

## 10. Next round

Send with the fixes applied:
- the new accent and LAVA colours, with a `hue_cmp` strip against Phoenix, Ivonrath and ThunderRex at 64 and 128 px (MUST 1 and 2);
- the re-measured gold count and its method (MUST 3);
- fresh molt renders from the current 22:37 model, and a fresh face close-up (MUST 4);
- the disclosure note for the Haku source (NICE 1).

The clip gate is approved with fixes: once MUST 4 lands, the molt renders are judged in the current palette and the clip goes to the owner. The model goes to the owner at 8/10, after MUST 1-4.
