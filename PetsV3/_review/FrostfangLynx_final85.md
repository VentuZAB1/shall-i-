# Frostfang Lynx - FINAL 8.5 GATE (model + clips), 2026-10-28

## Verdict: FIX
- **Model: 7.5 / 10**
- **Clips: 7.0 / 10**
- Owner ship bar: 8.5 minimum, higher is better (2026-10-28). Both are under 8.5, so the pet is not shippable yet.
- Expected result after the MUST list: model about 8.5 (after M1-M3), clips about 8.5 (after M4-M5).

## What I looked at
- Brief `GLACIER_REVIEWER_BRIEF.md`, plan `FrostfangLynx_plan.md` (v2), reviews 1-4, `GLACIER_CONCEPTS.md` owner decisions.
- Obsidian `Creature Style.md`, `Model Review Checklist.md`; `FIERCE_GUIDE.md`.
- `FrostfangLynx/MODEL_NOTES.md`, `CLIP_NOTES.md`, `ANIM_REFS.md`, `FrostfangLynx_meta.json`, `renders/_shares.json`.
- Source `pets/FrostfangLynx.py` (line references below).
- Renders: `renders/_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `_pose_tq_sheet.png`, `_pclose_side_sheet.png`.
- Comparisons: `ShadePanther/renders/_model_sheet.png`, `Raiju/renders/_model_sheet.png`, `PetsV3/_ALL_FIERCE_progress.png`.
- Not checked by me: the flat palette PNGs (I used the builder's shares), the per-frame PNGs beyond the sheets, the Blender file, and the animationreference.org citation (accepted as recorded in review 4).

---------------------------------------------------------------------------------------------------------------------
## 1. Model score: 7.5 / 10

**Keep (these pass):**
- The species reads as a cat at 64 px: two tall ice-tipped ear tufts, a wedge head, a short bobtail. It is clearly not the ShadePanther or the Raiju.
- The face is fierce: narrow cyan slits in black sockets under heavy V brows, black nose, no glint, no smile (`_close_sheet.png`).
- Studded FIERCE skin is consistent. Tris about 6,532 (cap 15k).

**Why it is not higher (what the owner would notice):**
1. **Saddle reads as tiles.** The BACK_SHADE inlays on chest, waist and hips (`pets/FrostfangLynx.py` lines 124-127, `saddle()` lines 97-107) show as three separate dark grey pads with gaps along the back in `game_view.png`. That is the "plate" read the owner has rejected.
2. **White snow boots.** The paws are SNOW: the paw block (line 219, 0.076 x 0.088 x 0.042), the foot seg (line 217) and the shin socks (line 212). In the side and front panels of `_model_sheet.png` the lower legs read as white boots and make the legs look plush.
3. **The beard is a white fluffy collar.** The cheek ruffs and chest points (lines 169-181, 132-133) are a large SNOW mass (tq SNOW 23 %). From the front it is the one place the face leans cute.
4. **The accent is too weak for "Frostfang".** ICE is 2.2 % in the game view (plan 5 %). The ice shows only on ear tips, ruff tips and claws. The body is beige, and in the 64 px strip it has the lowest contrast of the four icons (Panther, Badger, Raiju are all bolder).
5. **Rosettes read as stuck-on discs.** The three-crescent blobs (`rosette()` lines 85-91, placement lines 223-252) read as flat dark spots from a 5-stud camera, in a dense leopard-like pattern.

## 2. Clip score: 7.0 / 10

**Passes:** `collision_free` true; linear 0 in all clips; idle and walk loops closed; `ground_min_z` -0.000; neck max 7.0 (limit 8); chest vs spine 2.1 (limit 5); head + neck pitch within 30; no head shake; acts in place and end at rest. The roar is the best beat: ruff flare, jaw opens to the frost fangs, reads as a threat in `pose_tq` roar_30.

**Weak:**
- **The signature act is almost invisible from the player's camera.** The crouch is `drop = 0.05 * H_U` (line 460 area, `clawflex()`). H_U = 1.18 units = 7.0 studs, so the drop is about 0.35 studs. The claw bones are 0.056 units (about 0.33 studs) long, 0.012 half-width, and open only -35 deg (line 475). In the `_pclose_side_sheet.png` act frames (12/36/50/62/95) the claws are small cyan marks, and the crouch looks almost like idle frame 0.
- **Idle has little motion at game distance.** Only the head yaw (+14 / -8 deg), an ear twitch at f70 and a tail-tip flick at f90. It reads as static.
- **Walk** is a clean but generic quad walk. Fine, not a signature.

---------------------------------------------------------------------------------------------------------------------
## 3. MUST list (to reach 8.5+ on both scores)

### M1 (model): one continuous dark saddle band, no tiles
- `pets/FrostfangLynx.py` lines 124-127: delete the three `saddle(B, blk, w, sd)` calls.
- Replace with one tapered BACK_SHADE band from the nape (line 136 scruff) over the chest, waist and hips to the tail root. Half-width about 0.045 units (0.27 studs), top at the torso top + 0.004, `rnd` 0.35, no gaps or seams.
- Pass: `game_view.png` shows one dark dorsal band with no tiles. Side view keeps the torso flush (no green gap, as in `crop_rump_side.png`).

### M2 (model): paws are warm with a thin white sole, not white boots
- Line 217 (foot seg) and line 219 (paw block): change SNOW to WARM_SILVER.
- Add one SNOW sole plate on the underside of each paw: about 0.012 thick, flush to the bottom, `role="detail"` (smooth).
- Keep the socks (line 212) and the claws as they are.
- Pass: front and side views show warm paws with a white sole line. SNOW share in the game view drops from about 10 % to about 7 %.

### M3 (model): frost accent to at least 3 % in the game view
- Line 154 (frost fangs): ICE_CLAW (214,244,255) becomes ICE (150,236,255).
- Lines 132-133 (chest-ruff points): add an ICE tip on the outer 45 % of each point, the same method as the cheek-ruff spikes (lines 178-181), `nostud=True`.
- Lines 139-142 (throat fur tufts): tips become ICE, `nostud=True`. Keep the tips rounded.
- Do NOT add ICE to the ear tufts (no horns).
- Pass: game-view ICE at 3 % or more (now 2.2 %). At 128 px the frost reads on chest and jaw, not as horns.

### M4 (clip): the claw flex must read at 5 studs
- `clawflex()`: crouch depth `drop = 0.05 * H_U` becomes `drop = 0.10 * H_U` (about 0.7 studs). Also Spine rot `3.5 * c` becomes `6.0 * c`, and Chest `1.5 * c` becomes `3.0 * c`.
- Line 222 (claw spikes): length 0.056 becomes 0.072; half-width 0.012 becomes 0.014.
- Lines 475-476: `Claw_FL` and `Claw_FR` open `-35.0` becomes `-55.0`. Keep the centre and outer splay (lines 477-480) and the knead.
- The `solve_leg(... toe=-12.0 * a)` call (line ~488): `toe=-12.0` becomes `toe=-20.0`. Heel stays at `0.008 * a`.
- Re-run the step-1 gate: `collision_free` true, `ground_min_z` >= -0.02, neck total <= 8 (the bigger crouch adds neck pitch), chest vs spine <= 5.
- Pass: `pclose_side_act_clawflex_50.png` shows four separate open claws and a clearly lower crouch than the idle frame from the same camera.

### M5 (clip): the idle has life at game distance
- Add a slow tail sway of about +/-8 deg over the 120 f loop, through the existing `bobtail(k, f, ..., sway=...)` argument (line 369). Add a breathing rise of about 0.01H on the Spine root (`loc z`).
- Keep the loop closed (frame 120 equals frame 0).
- Pass: `_pose_tq` idle 26 and idle 62 differ visibly in the tail and back, and the loop seam is 0.0.

**Re-send list:** `pets/FrostfangLynx.py` diff; `renders/game_view.png`; `_icons_strip_64.png` and `_icons_strip_128.png`; `_model_sheet.png` front and side panels; `pclose_side_act_clawflex_50.png` and `pose_tq_act_clawflex_50.png`; the new `fullcheck.json` (`collision_free` true, `ground_min_z` >= -0.02) and the per-clip angle numbers.

---------------------------------------------------------------------------------------------------------------------
## 4. TO 9+ list (the higher the better; not required for 8.5)
- **T1 Rosettes as rings (highest impact).** Change `rosette()` (lines 85-91) from three crescents to a ring of 5-6 small BACK_SHADE blobs around a WARM_SILVER centre, so each flank spot reads as a lynx rosette at 128 px. Remove one spot per flank block in the placement lines (223-252) to open the coat, so the cheetah-like density goes.
- **T2 Coat value (owner question, not a builder change).** WARM_SILVER (190,172,150) reads as beige in the game. A slightly deeper sand, about (170,156,138), would give the SNOW underside and the cyan more contrast. The plan says any palette change needs the owner's OK, so ask first with a game-view render of both.
- **T3 Stare beat.** In `clawflex()` the stare (YW line, head yaw 14 deg) is a turn. Ears flatten at -12 deg (TF) on f14-22 and the head holds at 18 deg, so the stare reads as a hunter's lock on the target, not a glance.

---------------------------------------------------------------------------------------------------------------------
## 5. Pass / fail checklist (8.5 gate)

**Model**

| # | item | result |
|---|---|---|
| 1 | 64 px: species reads at once | PASS (cat with ice tufts). Low colour contrast: see T2 |
| 2 | 128 px: no horn or goat read | PASS (ear tufts short, no chin tuft) |
| 3 | Face fierce: slit eyes, heavy brow, no glint, no smile | PASS |
| 4 | Palette follows plan v2 | PASS |
| 5 | Accent ICE at least 3 % in the game view | FAIL (2.2 %) - M3 |
| 6 | No floating, plate or tile parts | FAIL (saddle tiles read as plates) - M1 |
| 7 | Not cute: no white boots, no fluffy collar | FAIL (white paws and beard) - M2, M3 |
| 8 | Rosettes at least 20 % of the side view | PASS (20.8 %) but they read as stickers - T1 |
| 9 | Tris at most 15k | PASS (about 6,532) |
| 10 | Distinct from ShadePanther and Raiju | PASS |
| 11 | Stud skin, details smooth (eyes, claws, fangs) | PASS |

**Clips**

| # | item | result |
|---|---|---|
| 1 | `collision_free` true | PASS |
| 2 | Linear 0 in every clip | PASS |
| 3 | Loops closed (idle, walk) | PASS |
| 4 | `ground_min_z` >= -0.02 | PASS |
| 5 | Pose limits: neck <= 8, chest vs spine <= 5, head + neck pitch <= 30 | PASS |
| 6 | No head shake, no airborne frames | PASS |
| 7 | Acts in place, end at rest | PASS |
| 8 | Signature beat readable at game distance | FAIL (crouch 0.35 studs, claws 0.33 studs) - M4 |
| 9 | Idle has visible life at game distance | PARTIAL - M5 |
| 10 | Walk reads as a cat walk | PASS (generic) |
| 11 | ANIM_REFS rule (refs cited, timings used) | PASS as recorded in review 4 (not re-verified here) |

**Scores:** model 7.5 (M1-M3 lift it to about 8.5), clips 7.0 (M4-M5 lift it to about 8.5).
