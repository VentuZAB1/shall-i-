**Model: 8.4/10 - FIX. Clips: 8.5/10 - PASS.**

# Cinder Overlord - FINAL 8.5 GATE, ROUND 6 (fresh reviewer, 2026-10-28)

Both round-5 MUSTs are closed on their own numbers. The model still fails on the player's-eye silhouette, which round 5 had as a 9+ note and which I now rule blocking, and on the rare-tier outclass rule, which no gate has measured against Phoenix or Ivonrath. Clips are unchanged since round 5 and hold at 8.5.

## 0. What I looked at, and the limits

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`. Round 5 `_review/CinderOverlord_final85_r5.md`.
- Builder notes `CinderOverlord/MODEL_NOTES.md` (FINAL 8.5 ROUND 5, exported 06:09), `CLIP_NOTES.md`, `ANIM_REFS.md` (refs present and cited). Code `pets/CinderOverlord.py` (lines 15-57 constants, 258-340 body, rings, vents, crown).
- Rules: `_review/GLACIER_CONCEPTS.md` (owner decisions line 29; table line 46; Area 4 line 67), `FIERCE_GUIDE.md`, Obsidian `06 Modelling and Art/Creature Style.md`, `Model Review Checklist.md`, `Creature Animation.md`.
- Images, all loaded: `CinderOverlord_portrait_alt.png`, `CinderOverlord_icon_alt.png`, `CinderOverlord_icon_game.png`, `renders/_icons_alt_strip_64.png` / `_128.png`, `_icons_strip_64.png` / `_128.png`, `_icons2_strip_64.png` / `_128.png`, `renders/close_front.png`, `_close_sheet.png`, `close_side.png`, `gamelook_game.png`, `_model_sheet.png`, `_scratch/gold_sweep_crest.png`. Clip frames: `pose_tq_idle_00` / `_30`, `pose_tq_walk_00` / `_36`, `pose_tq_roar_30`, `pose_tq_act_molt_22` / `_40` / `_84` (all 06:08-06:09). Older sheets for reference only: `_pose_tq_sheet.png`, `_cv_walk_game.png`, `_cv_walk_side.png`, `_molt_r4_front.png`.
- Numbers: `_scratch/gate_f85.json` (06:13, the single gate file: tris 10,468, collision_free true, stride 5.0089 BU / 48 f, gold, shares, molt speeds), `_scratch/gold_r5.json`, `_scratch/game_icon_out.txt`.
- **Limit:** PIL is not installed here, so I could not zoom or re-count pixels. Gold and fill numbers are the builder's, checked against the images by eye only. Blade angles are the gate's `max` field, read as degrees.
- **Freshness:** `renders/pose_tq_*` (06:08-06:09) are current. `_pose_tq_sheet.png` (05:00, round-4 title bar, before the gold change) and `_cv_walk_*` / `_molt_r4_*` (05:00) are stale, yet CLIP_NOTES names `_pose_tq_sheet.png` as the current sheet. Not scored; see TO 9+.
- **Tier:** scored against the mythic bar, per the lead's ruling that the Cinder IS the Fire mythic. `GLACIER_CONCEPTS.md` line 46 and the pet table line 116 still say "Ultra-rare 0.5 %". I did not edit them.

## 1. Clip table (lowest clip = 8.5, so Y = 8.5 PASS)

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.5 | Head held level, neck 4.5 deg per bone, no shake, loop closes (rest frames idle_00 and idle_60 are the same file size, 100,898 B). The breath is almost invisible at 300 px: idle_00 and idle_30 look the same. Lead ruled breath is a Studio check, so not counted. Vent smoke and tail flick are VFX / small, not in the gate. | `renders/pose_tq_idle_00.png`, `pose_tq_idle_30.png` (06:08) |
| walk | 8.5 | Head to tail S-wave reads in the 3/4 frames; the crest and head hold their line; no shake. Stride 5.0089 BU / 48 f (speed not gated, lead ruling). Judged from stills only. The worm-like body read from the game camera (MUST 1) shows in the walk too; re-check after the MUST 1 fix. | `renders/pose_tq_walk_00.png`, `pose_tq_walk_36.png` (06:09) |
| roar | 8.5 | Crown flare and the jaw opening are clear in the 3/4 frame at the roar event (f30; flare event f20). No collision; the roar frames from the game camera are not in the evidence set. | `renders/pose_tq_roar_30.png` (06:09) |
| act_molt | 8.5 | The signature reads: the blades lift one at a time (lift1 f22, lift2 f48, shed f56) and reseat; rest frames f0 and f110 match (same file size). Outer blades report a max of 55.8 (the r5 9+ ask was 55). At 300 px the fan is moderate, clearer in the front sheet (stale). Nothing blocks. | `renders/pose_tq_act_molt_22.png`, `_40.png`, `_84.png` (06:08) |

## 2. Round-5 items

| item | result | evidence |
|---|---|---|
| R5 MUST 1, gold clipped to lemon | **PASS** (metric). Visual: the lit tops read gold-yellow, the flanks amber; I judge it gold. | Kit portrait lemon (H 59-61) 2 px (was ~59); game 0; portrait_alt 0. Gold px: kit 81, game 25, portrait_alt 91 (`gate_f85.json`). `renders/_close_sheet.png` |
| R5 MUST 2, presence at icon size (pose / framing) | **PASS vs Thunder Rex and Cosmic Leviathan.** Not shown vs Phoenix / Ivonrath (see MUST 2). | portrait_alt fill 0.891 (>= 0.70). Area 0.374 vs Rex 0.372 and Leviathan 0.208. Gold 91 vs Rex 13-14 and Leviathan 20-31. `renders/_icons_alt_strip_64.png`, `_128.png` |
| R5 9+ nose / chin caps (T-b) | **PARTIAL.** The nose is smooth. The chin is still a rounded smooth bulb under the nose, which reads as a bulbous muzzle from the front. | `renders/_close_sheet.png` (front panel, lower centre). The nostril pits are 0.006 x 0.004 x 0.009 BU (`pets/CinderOverlord.py` nostril block), below the FIERCE_GUIDE 0.02 BU floor. |
| T-a eyes (open since r4) | **PARTIAL.** From the front the blue socket outer ends still sit outside the skull outline at eye height (about 20-25 px of 600 beyond the cheek edge). The brows read as visor wedges. | `renders/_close_sheet.png` front panel; `close_front.png` |
| R5 TO 9+ worm read | **FAIL**, not done. Now MUST 1 (game-camera read). | `renders/gamelook_game.png`, `CinderOverlord_icon_game.png`, game tile in `_icons2_strip_128.png` |
| R5 TO 9+ molt outer lift to 55 deg | **PASS** (gate max 55.8 outer, 40.0 centre) | `_scratch/gate_f85.json` `molt_blade_speed_deg_per_f` |
| R5 T-d breath | not scored (Studio check, lead ruling) | |

## 3. Model score: 8.4 - FIX

**Holds:**
- The crest is the strongest hero in the strip: 91 gold px on the molt portrait, 0 lemon. Kit portrait 81.
- Portrait fill 0.891 and area 0.374 match Thunder Rex (0.906 / 0.372) and beat Cosmic Leviathan (0.562 / 0.208).
- Fierce face from the front: narrow blue slits under heavy brows, no glints, no smile, no googly eyes.
- Three bands read: ember body, obsidian saddle and rings, pale belly.
- Vents are one slit per side per segment, not legs. Body colour luma about 101 (guide requires >= 95).
- Tris 10,468 (cap 15k). Collision-free, ground -0.006, linear 0, loops closed. Studs cover the whole skin.

**Blocks 8.5:**
1. **The player's-eye silhouette is a thin segmented worm.** The game-camera icon has area 0.163 (portrait 0.383) and fill width 0.50. Its flanks carry dark ring bands on most segments. It reads as a centipede or worm, not a fierce dragon. The brief judges the species from the player's eye, so this is blocking (MUST 1).
2. **The rare-tier outclass rule is not shown against Phoenix or Ivonrath.** The brief says rare tiers must outclass everything below. Phoenix (2 %) and Ivonrath (4 %) are below the Cinder. Only Rex and Leviathan were measured. At 128 px the Phoenix tile is an orange-yellow flame mass that looks at least as loud as the Cinder's dark-red body (MUST 2).

## 4. New MUSTs (block 8.5)

**MUST 1 (model): the game-camera silhouette must read as a dragon, not a worm.**
- Evidence: `CinderOverlord_icon_game.png` and the game tile in `_icons2_strip_64/128.png` (06:10-06:12). Game-camera area 0.163, fill width 0.50 (`gate_f85.json`).
- Fix, both in `pets/CinderOverlord.py`:
  - (a) Line 265, the ring skip set `(3, 5, 7)` becomes `(2, 3, 5, 6, 7)`. Rings then stay only on Body1, Body4 and Tail4 (3 of the 8 body and tail segments, down from 5). Keep the Neck1 ring and the dorsal saddle.
  - (b) Line 49, `RAD[1..4]` +10 %: 0.308 -> 0.339, 0.280 -> 0.308, 0.252 -> 0.277, 0.200 -> 0.220. Vents, scutes and rings follow RAD. Check the Body4 -> Tail1 taper (0.220 -> 0.168) by eye.
- Pass: on the same counter, game-camera area >= 0.18 and fill width >= 0.60. Step 1 still `collision_free: true` and `ground_min_z >= -0.02` in all four clips. Re-render `gamelook_game.png`, the game icon and the walk frames. No more than 3 dark ring bands on the rear 8 segments.

**MUST 2 (model): measure the outclass of Phoenix and Ivonrath, and fix it if it fails.**
- Evidence: the Cinder's tile against the InfernoPhoenix and Ivonrath tiles in `_icons_strip_64.png` / `_128.png` (06:12). Phoenix is louder than the Cinder by eye. No gate has the numbers.
- Measure: run the same icon recipe (icon3, 64 px) and the same gold counter (`_tools/game_icon.py`, H 29-58) on the InfernoPhoenix and Ivonrath tiles. Record gold px, opaque area and fill height.
- Pass: Cinder gold px >= each, and Cinder opaque area >= each. Fill height >= 0.70 for all.
- If it fails: raise the centre crown blade 0.32 -> 0.34 (it was collision-free in the r3 molt test) and widen the centre and middle gold frames by +0.004. Re-run the molt collision check and the gold count.

## 5. TO 9+ (not blocking)

1. **Game-camera gold margin.** 25 px equals the gate floor, so there is zero margin. Aim for >= 30: the middle-blade gold frame width 0.028 -> 0.032, then re-check the molt.
2. **T-a eyes.** Pull the blue socket and slit outer ends in by 0.01 BU, so no blue sits outside the skull outline from the front.
3. **T-b chin.** Flatten the chin bulb's front face about 15 % so the front reads as a jaw, not a bulbous muzzle.
4. **Nostril pits** are 0.006 BU, below the 0.02 BU speck floor (FIERCE_GUIDE). Widen them to >= 0.02 BU or drop them.
5. **Breath.** Idle breath is nearly invisible at 5 studs. A 5-6 deg per-bone neck breath would help, after the Studio check.
6. **Stale evidence.** Re-render `renders/_pose_tq_sheet.png`, `_cv_walk_game.png` / `_side.png` and `_molt_r4_front` / `_side` / `_tq` from the current model. Fix the CLIP_NOTES line that calls the 05:00 sheet current.
7. **Pose-limit reading.** The gate reads "neck <= 8 deg" per bone, as in r4. The molt neck arch is 22.5 deg over three bones. Lead to confirm per-bone is the intended reading. If it is a total, the molt fails.
8. **Tier record.** If mythic stands, update `GLACIER_CONCEPTS.md` line 46 and line 116 from ultra-rare 0.5 % to mythic.

## 6. Pass / fail checklist

| # | check | result |
|---|---|---|
| 1 | Tris <= 15k (10,468) | PASS |
| 2 | Collision-free, ground >= -0.02, linear 0, loops closed | PASS |
| 3 | Gold kit portrait >= 25 (81) | PASS |
| 4 | Gold game camera >= 25 (25) | PASS, zero margin |
| 5 | Gold is gold, lemon <= 10 px (2) | PASS |
| 6 | Species reads at 64 px from the player's eye (game icon) | **FAIL** (MUST 1) |
| 7 | Portrait silhouette at 64 px | PASS |
| 8 | Outclasses Thunder Rex and Cosmic Leviathan at 64 px | PASS |
| 9 | Outclasses Phoenix and Ivonrath (rare-tier rule) | **NOT SHOWN** (MUST 2) |
| 10 | Eyes fierce from the front | PARTIAL (T-a) |
| 11 | Nose and chin smooth | PARTIAL (T-b) |
| 12 | Vents read as slits, not legs | PASS |
| 13 | Molt outer lift >= 55 deg | PASS |
| 14 | Pose limits: neck <= 8 per bone (7.5), spine <= 5 (4.5), head pitch net <= 30 | PASS (builder numbers, per-bone reading) |
| 15 | No head shake; acts end in rest | PASS (rest frames match) |
| 16 | Current clip renders | PARTIAL (`pose_tq_*` current; the sheets are stale) |

## 7. Not re-scored (accepted rulings)

- Ember body (176, 72, 54) instead of plan plum #B684AC; sulfur-blue accent instead of rose #FF6096.
- Cold-blue vents; top-down belly; walk speed (distance-driven animator); breath (Studio check); VFX (added in Studio).
