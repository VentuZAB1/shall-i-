# Wraith Hound - FINAL 8.5 GATE, round 2 (model + clips, export 01:17) - 2026-10-28

**Model 8.0/10. FIX (2 MUSTs, both small). Clips 8.5/10. PASS (at the bar).**

Round 1 scored the model 7.5 and the clips 8.0. Every round-1 MUST was applied and the code matches the claims. The ghost read is now the biggest gain: the lavender body is the largest single colour in game view (41.1 %), and the pet reads as pale smoke rather than a dark crest. The clip fixes landed too: the roar hold is a smooth 10-frame wave, the roar side flare is 12 degrees, and the cloak fan lifts 6 degrees. Two model issues are left, and both are small: the indigo accent is too thin to read at 64 px, and the eyes are still too small to read there.

## What I looked at
- Notes and data: `WraithHound/MODEL_NOTES.md` (round 5), `CLIP_NOTES.md`, `_scratch/gate5.log`, `_scratch/fullcheck.json`, `_scratch/clipmetrics.json`, `WraithHound.json` (roar Jaw track, normalised), `pets/WraithHound.py` (current lines).
- Renders (all 01:15-01:16): `_model_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `crop_mane_side.png`, `crop_mane_front.png`, `_fan_front_back_f85.png`, `_tail_f85.png`, `crop_tail_side.png`, `_close_sheet.png`, `model_front.png`, `low_below.png`, `pclose_front_roar_30.png`, `pclose_side_act_smokecloak_47.png`, `_pose_tq_sheet.png`.
- Not re-checked: the comparison sheets (Raiju, ShadePanther, NightmareStallion, BlackDragon) were judged from the round-1 read and the 128 px strip.
- No Blender, no Studio.

## Round-1 items, checked
| item | result |
|---|---|
| Ghost: mane roots mid-slate (WISP_ROOT, L21, L71) | **done.** Game: ASH_LAV 41.1 (largest colour), SOOT 27.1, WISP_ROOT 17.0. The body reads lavender in `game_view.png`. |
| Ghost: tail lavender down to a soot tip; the tip-overlap line fixed | **done.** Tail1-3 lavender (L216 `i < 3`), Tail4 soot, overlap ext 0.015. `_tail_f85.png` and `crop_tail_side.png` show a clean lavender-to-soot transition with no dark line. |
| Plume: only Mane2's centre tip indigo, longer | **done.** L84-85: Mane2 tail 0.44 · sc, Mane1 and Mane3 centre tips SOOT. `crop_mane_side.png` shows one long indigo leader and a swept line of side tips. |
| Eyes: slit taller, rim taller | **done** (L166-168: rim 0.020, slit 0.018, pupil 0.0175). Better in `_close_sheet.png`. **Not enough at 64 px** (see MUST 2). |
| Chest plate lavender (no white bib) | **done** for the plate (L140, ASH_LAV, 0.075). The throat strip (L144, MIST) still reads as a white bib from the front (`model_front.png`). That is the TO 9+ #2 design (MIST kept on the throat), so NICE only. |
| Roar jaw: smooth 10-frame wave, no flutter | **done.** Jaw f26-44: min 22.55 (f27-28, f37-38), max 24.45 (f32-33, f42-43), period 10 frames, +-1 deg (L399 `/ 10`). Ramp f12 to f26 and close by f53 are unchanged. |
| Roar side flare 12 degrees (was 25) | **done** (L408). In `pclose_front_roar_30.png` the side wisps sit as a low crest, not batwing horns. |
| Cloak fan lift 6 degrees (was 14) | **done** (L435). In `_fan_front_back_f85.png` the fan widens sideways. From directly behind it still radiates (TO 9+ clip #1). |
| Gates | **pass.** fullcheck: collision_free true, collisions {}, linear 0, ground min 0.004 in every clip, loops closed, tris 6,820, glow {}. |

## Measured
**Shares (`_scratch/gate5.log`, builder's count):**

| view | ASH_LAV | MIST | SOOT | WISP_ROOT | INDIGO |
|---|---|---|---|---|---|
| side | 47.0 | 7.0 | 23.8 | 14.2 | 3.1 |
| game | **41.1** | 5.1 | 27.1 | 17.0 | **5.2** |

Caution, for the notes: WISP_ROOT is mid-slate. At Roblox's ~0.6x darkening it lands near (77,74,100), which is a dark tone in game. The dark family (SOOT + WISP_ROOT) is 44.1 % in game. The ghost read still holds because the lavender body is the largest single colour, but the notes should give the family total as well as the separate numbers.

**Limits (`clipmetrics.json`, 01:17 export):** neck max 3.5 / 4.0 / 4.0 / 5.0 (idle / walk / roar / act; limit 8). Chest vs spine 0.6 / 2.92 / 1.5 / 1.5 (limit 5). Head + neck pitch-up 8.0 idle, 3.5 act (limit 30). Head yaw 0 in idle, roar and act; 0.98 in walk. No quaternion flips. Last frame = first frame in idle, roar and act. Walk loop closed. **Every limit passes.**

**Accent at icon size:** INDIGO 5.2 % in game is only just above the 5 % floor. In `_icons_strip_64.png` the blue points almost disappear, and at 128 px they show only on the crest. The accent is the weakest part of the design at icon size.

---------------------------------------------------------------------------------------------------------------------
## MODEL: 8.0/10

**What now works:** the body reads as a pale lilac ghost hound, not a dark wolf. The lavender-to-soot tail is clean. The crest reads as one swept mane with a single long indigo leader. The face is fierce in close-up, with heavy soot brows, slit eyes, a black nose, and ivory fangs. Studs cover every surface, there is no glow, and the build is 6,820 tris.

**Why it stops at 8.0:**
1. **The accent is too thin at 64 px.** The blue tips are the only bright colour, and they fade into the mid-slate crest at icon size.
2. **The eyes do not read at 64 px.** In `_icons_strip_64.png` the eyes are not visible, so the face reads only in close-up.
3. **The saddle is still a flat dark plank in game view** (`game_view.png`). It is the top band on each torso block, and its top surface is flat and dark from the withers to the hips.
4. **The throat is a white bib from the front** (`model_front.png`).
5. **The crest still stacks in three rows** of blades in `crop_mane_side.png`, with the side tips at three heights. It reads as a swept crest, not yet one plume.

### MODEL MUST (to reach 8.5)
**M1 - the indigo tips carry the accent at 64 px (`pets/WraithHound.py` L76-77, the `wisp()` tip segment).** The indigo tip is `B.seg(j, q, w * 0.70 * 0.62, d * 0.70 * 0.62, tipcol, ...)`. Change the `0.62` factor to `(0.85 if tipcol == INDIGO else 0.62)`. The indigo points become about 40 % fatter and read as blue points, not hairlines. Expect game INDIGO from 5.2 % to about 6.5 %. Check: `_icons_strip_64.png` shows blue points on the crest, and `flat_game` reads INDIGO 6 % or more.

**M2 - the eyes read at 64 px as dark pools (`pets/WraithHound.py` L165, the socket).** The socket is `B.add(c, (0.052, 0.008, 0.020), BLACK, ...)`. Change the height `0.020` to `0.028`. Under the heavy brow, the eye becomes a dark pool with the indigo slit inside it, which reads as a fierce eye at icon size. The socket's width stays at 0.052, so nothing pokes out of the head. The slit (L168) and the rim (L166) do not change. Check: `_icons_strip_64.png` and `_close_sheet.png` (no pokes through the brow or the skin).

### MODEL TO 9+
1. **Round the saddle so it is not a plank** (`pets/WraithHound.py` L127-129). Add `rnd_t=0.45` to each `upper()` call (the default is 0.30). The top band rounds off in `game_view.png` and reads as fur, not a board.
2. **Thin the crest to one line.** After M1 restores the accent, set the side tips of Mane1 and Mane3 to SOOT: in `mane_row` L84-85, pass `tipcol=(INDIGO if bone == "Mane2" else SOOT)` to the side-wisp call. Keep game INDIGO at 5 % or more, and check that `crop_mane_side.png` reads as one leader plus one line.
3. **Throat bib (NICE-level, but it is the last white block from the front).** Make the top half of the throat seg (L144, `B.seg((0, -0.54, 0.71), (0, -0.78, 0.90), 0.075, 0.060, MIST, ...)`) ASH_LAV, and keep MIST on the lower half. This is the TO 9+ #2 design, extended to the throat.

### MODEL NICE
- The roar docstring (L387) still says the side wisps splay 25 degrees. It is 12 now. Fix the comment, and write the values into MODEL_NOTES.
- Write the family total (SOOT + WISP_ROOT = 44.1 % game) into MODEL_NOTES next to the separate numbers.

---------------------------------------------------------------------------------------------------------------------
## CLIPS: 8.5/10 (PASS at the bar)

**What works:** every pose limit passes with margin. The roar hold is a smooth 10-frame wave. The jaw ramp is smooth, opens by f26 on the `snarl` event, and closes by f53. The roar side flare is a low crest, not wings. The cloak fan widens sideways and reads as a swept crest from the side (`pclose_side_act_smokecloak_47.png`) and from the 3/4 view in `_pose_tq_sheet.png`. The idle sniff, the trot walk, and the snarl all read. Every round-1 clip MUST is applied.

**What still holds it back, but not below the bar:**
1. **Behind, the fan radiates like a hedgehog ring** (`_fan_front_back_f85.png`, bottom middle). Every row lifts by the same 6 degrees, so the rows stack up into a ring.
2. **The cloak's smoke read depends on VFX,** which is not in this gate. The FX anchors are in the rig. Without the smoke VFX the act is a crest fan.

### CLIP MUST
None. Every clip item from round 1 is applied, and the clip gate passes at 8.5.

### CLIP TO 9+
1. **Stagger the rows in the cloak fan** (`pets/WraithHound.py` L435). Change `[6.0 * a for a in fan]` to `[6.0 * fan[0], 4.0 * fan[1], 2.0 * fan[2]]`. Each row lifts less than the row in front of it, so the fan streams back rather than ringing. Re-render the act f47 from behind.
2. **Check the smoke VFX in Studio** on the `cloak` event (f28). Same as the model TO 9+ #3 from round 1; it is not a model edit.

---------------------------------------------------------------------------------------------------------------------
## Pass / fail checklist (round 2)

**Model**

| check | result |
|---|---|
| 64 px: species reads (canid, wedge head, ears, tail) | PASS |
| 64 px: ghost reads (pale body, dark crest) | PASS (improved) |
| 128 px: one plume, not stacked spines | PASS on the leader, partial on the side tips (TO 9+ #2) |
| Fierce face in close-up | PASS |
| Face reads at 64 px | **FAIL** (M2) |
| Accent reads at 64 px | **FAIL** (M1) |
| Studs, smooth details, no glow | PASS |
| Tris <= 15k (6,820) | PASS |
| Dark body + pale underside + one accent (in game) | PASS (ASH_LAV 41.1 is the largest colour; SOOT 27.1) |
| Accent distinct from Raiju and the Void violets | PASS |
| No box belly, no plastic slabs (side, front, below) | PASS (throat bib: NICE, TO 9+ #3) |
| Floating or poking parts | PASS |
| Height ties the Stallion (9.0) | PASS |

**Clips**

| check | result |
|---|---|
| Neck <= 8 deg | PASS (5.0 max) |
| Chest vs spine <= 5 deg | PASS (2.92 max) |
| Head + neck pitch-up <= 30 deg | PASS (8.0 max) |
| No head shakes | PASS |
| No airborne spins | PASS |
| Acts in place, ending at rest | PASS |
| Ground >= -0.02, collision_free, linear 0, loops closed | PASS |
| Roar jaw: smooth open and close, no flutter | PASS |
| Roar: mane flare, not batwing horns | PASS |
| Cloak: a swept fan, not a porcupine spike | PASS from the side and 3/4; from behind partial (TO 9+ #1) |
| Anim-reference rule | PASS (accepted in review 4) |

---------------------------------------------------------------------------------------------------------------------
**Send-back for round 3:** apply M1 and M2 (two lines in `pets/WraithHound.py`, L76-77 and L165). Re-export, then re-render `_icons_strip_64.png`, `_icons_strip_128.png`, `flat_game.png` (check INDIGO), `_close_sheet.png` (check the sockets), and `_pose_tq_sheet.png`. No clip re-check is needed unless the export changes a bone.
