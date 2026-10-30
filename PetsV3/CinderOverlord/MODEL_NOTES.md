# Cinder Overlord - model notes (MODEL GATE, 2026-10-27)

Magma / Fire egg, **MYTHIC** (secret + mythic in the economy plan, 0.5 %; must beat Phoenix, Ivonrath AND the 1 % secrets
Thunder Rex + Cosmic Leviathan).
Plan: `_review/CinderOverlord_plan.md` v2. File: `pets/CinderOverlord.py` (model + rig + check_pairs + joints; no clips yet).

## FINAL 8.5 ROUND 14 (2026-10-28, after `_review/CinderOverlord_final85_r14.md`: model 8.4, clips 8.5 APPROVED) - micro-fix - EXPORTED 14:53
Backups:
- the round-13 export: `_scratch/CinderOverlord_exported_r13.py`
- this export: `_scratch/CinderOverlord_exported_r14.py`

Nothing else changed.
1. **Hood rim:** the rim `B.seg` in `cobra_hood()` goes from OBS_D to **PALE_S** (222, 194, 158); its size is unchanged.
   - From the game camera the hood is now a red fan with a light edge, separate from the dark frill above:
     `renders/gamelook_game.png`, `_icon_game_64_128.png` (a light-edged fan at 128, a light band under the dark head at
     64), `_hood_back_2x_idle_f0_f20.png`.
   - The fallback (lowering the hood top 0.03) was not needed.
   - Geometry is unchanged, so every hood clearance is as round 13 (min 0.051 (idle f96)).
2. **Crown vs Head:** each blade socket is seated in the crown mount. That is a hinge: in the strict run no
   Crown_i|Head crossing falls outside its own hinge zone.
   - Clearance of each blade above the mount (every vertex more than 0.07 above its hinge) to the Head group, all
     frames of all four clips:
     - Crown_1 0.181 (act_molt f110);
     - Crown_2 0.166 (act_molt f26);
     - **Crown_3 0.053 (roar f44)**;
     - Crown_4 0.166 (act_molt f32);
     - Crown_5 0.181 (act_molt f110).
     - All are **>= 0.02**.
   - Crown neighbours >= 0.0357. Frill / cheek spikes to the crown >= 0.135.
3. **Shipping portrait:** **`CinderOverlord_portrait_raw.png`** (kit portrait, idle f0; the kit export writes it with the
   FBX) and its icon **`CinderOverlord_icon.png`**: gold **117** (the gate counter), area **0.378** (Thunder Rex 0.372).
   - The alt (`CinderOverlord_portrait_alt.png`, molt f40) is NOT shipped: area 0.369. Three reframes reached
     0.362 / 0.366 / 0.370, never 0.372.
   - It stays a reference render; `_icons_alt_strip_*` labels it "not shipped".
- **Kept as round 13:**
  - kit gate **collision_free true** (85 pairs); strict run only the two shoulder seats (<= 0.0277);
  - ground -0.006; loops 0 / 0; stride **5.0089**; HEIGHT 11.72; tris **13580**;
  - head + crown 0.320; game area **0.212**; paws 0.388 / 0.164;
  - game gaps idle 50.7-65.8, walk 61.8-63.0, roar 47.5-62.2, molt 52.5-62.2 px.
- **Renders** (title bars 14:53-14:55, "final 8.5 round 14"): the round-13 list.
  - `_molt_r13_*` and `mr13_*` moved to `_scratch/stale_r14_renders/`.

## FINAL 8.5 ROUND 13 (2026-10-28, after `_review/CinderOverlord_final85_r13.md`: model 8.3, clips 8.3 (act_molt)) - the reviewer's 5 fixes only - EXPORTED 14:41
Owner decision: one more SMALL round, the reviewer's 5 fixes and nothing else.

Backups:
- the round-12 export: `_scratch/CinderOverlord_exported_r12.py`
- this export: `_scratch/CinderOverlord_exported_r13.py`

The patch is `_scratch/fix_r13.py`, plus the crown and molt constants below.
1. **Hood colour:** the hood back plate goes from OBS_D to **PLUM_OBS** (ember) and the ribs to **PALE_S**. The obsidian
   rim and the sulfur-blue eye spots stay.
   - From the game camera the hood is now a red fan with a dark edge and pale ribs, separate from the dark frill and
     crown (`renders/gamelook_game.png`, `_icon_game_64_128.png`, `_hood_back_2x_idle_f0_f20.png`). Geometry is
     unchanged.
2. **Nose lump:** the hide test (`_scratch/nose_hide_r13.png`) shows two parts.
   - Under the nostrils: the muzzle's blunt oval front. That is the skull tip station plus the snout pad tube and its
     cap ring, seen end-on.
   - Under the mouth line: the jaw's round chin cap.
   - Fix (before / after in `_scratch/nose_r13_before_after.png`):
     - the muzzle tapers to a point: tip 0.044 x 0.022 -> **0.026 x 0.018**; 0.96 station width 0.060 -> **0.046**;
     - the muzzle slopes down to the tip (dz -0.026 / -0.034 / -0.036 -> **-0.040 / -0.062 / -0.068**);
     - the snout cap ring x0.80 / x0.60 -> **x0.55**;
     - the nostrils move to x 0.034 on the narrower tip;
     - the chin: jaw 0.85 station 0.078 / 0.032 -> **0.070 / 0.026**, tip 0.034 / 0.016 -> **0.024 / 0.012**, cap
       x0.80 -> **x0.60 / x0.55**.
   - Visible half-height under the nostril line: the tip is 0.018 (<= 0.03).
   - From the front the snout is now a wedge to a pointed nose (`renders/close_front.png`). The fangs and the roar
     mouth are unchanged (`_cv_roar_side.png`).
3. **Crown / area - deviation, measured:** the centre blade 0.40 -> 0.44 made the figure TALLER. The icon is
   bbox-normalised, so the kit area FELL to **0.354** (0.44 / 0.23 / 0.18) and 0.360 (0.44 / 0.27 / 0.22).
   - Trials, kit portrait at 64 px:

     | centre / middle / outer | gold | area |
     |---|---|---|
     | 0.40 / 0.23 / 0.18 (r12) | 113 | 0.365 |
     | 0.44 / 0.23 / 0.18 (review) | 110 | 0.354 |
     | 0.44 / 0.27 / 0.22 | 122 | 0.360 |
     | 0.40 / 0.27 / 0.22 | 118 | 0.370 |
     | **0.40 / 0.30 / 0.25** | **117** | **0.378** |
     | 0.42 / 0.30 / 0.26 | 124 | 0.371 |
   - Chosen: the centre stays **0.40**, the four side blades grow **0.23 / 0.18 -> 0.30 / 0.25**. They fill the top
     corners without adding height: kit area **0.378** (Thunder Rex 0.372), gold **117**.
   - Crown neighbours >= **0.0357** in all four clips: 1|2 0.039 (roar f21), 2|3 0.036 (act_molt f21), 3|4 0.036 (act_molt f110), 4|5 0.037 (act_molt f26).
4. **Molt hold - deviation, measured:** the review's head 20.5 -> 14 alone made the game-camera gap WORSE, **31.8 px**
   (r12 34.8). Nose-up tips the back of the head down toward the camera behind.
   - So I also used the review's fallback and lowered the neck arch. `MOLT_ARCH` -22.5 -> **-9** (3 deg per neck bone)
     and `MOLT_HEAD` 20.5 -> **9**, so the head stays level.
   - Game-camera head gap at every molt beat: **52.5-62.2 px** (>= 50; r12 34.8-62.4).
   - NEW `renders/_molt_game.png` (game camera, f0 / 22 / 34 / 40 / 56 / 84 / 100): the blades lift and fan above a
     clear head.
5. **Gate file:** every old gold field (`gold_px_64`, the old `gold_method` text with the 91, `kit_counter_64`) is
   deleted from `gate_f85.json`. `gold_gate` is the only gold number (**117**, floor 103), and `area_gate` is new
   (**0.378** >= 0.372).
- **Kept:**
  - kit gate **collision_free true** (85 pairs); strict run only the two shoulder seats (<= 0.0277);
  - hood clearance >= 0.051;
  - ground -0.006; loops 0 / 0; stride **5.0089**; HEIGHT 11.72; tris **13580**;
  - head + crown 0.320; game area **0.212**; paws past the outline 0.388 / 0.164;
  - game gap idle 50.7-65.8, walk 61.8-63.0, roar 47.5-62.2 px.
- **Renders** (title bars 14:41-14:43, "final 8.5 round 13"): the round-12 list plus `_molt_game.png`.
  - `_molt_r12_*` and `mr12_*` moved to `_scratch/stale_r13_renders/`.

## FINAL 8.5 ROUND 12 (2026-10-28, after `_review/CinderOverlord_final85_r12.md`: model 8.2, clips 8.5 APPROVED) - COBRA HOOD - EXPORTED 14:21
Owner decision (binding, via the lead): **cobra hood**. This is the last round before the owner decides again.

Backups:
- the round-11 export: `_scratch/CinderOverlord_exported_r11.py`
- this export: `_scratch/CinderOverlord_exported_r12.py`

The patch is `_scratch/fix_r12.py` plus the hood constants (`HOOD_*`) and `cobra_hood()` in the file.
- **MUST 1, cobra hood: thin studded plates, NOT a neck-radius scale.** Per side there are two panels:
  - The lower panel sits on **Neck2** (z 1.08-1.30), the upper on **Neck3** (z 1.26-1.64). Each is a thin lofted
    shell, 0.026 thick, so the idle sway, roar and molt carry the hood with the neck.
  - The panels sit 0.07 behind the neck axis and cup forward at the rim (0.10), so from behind they read as a fan.
  - Front face: ember (the body colour), smooth.
  - Back: an **obsidian studded back plate**, inset 0.025 from the rim.
  - **Rim:** obsidian, along the whole outer outline.
  - **Ribs:** three ember ribs per side on the dark back.
  - **Eye spot:** one **sulfur-blue** spot per side with a white-hot centre (cobra hood marking).
  - **Width:** the widest point is |x| **0.64** at z 1.38-1.44, just under the head. That is 0.43 past the neck side
    (0.21) and 0.27 past the skull side (0.37), so the hood is clearly wider than the skull. It narrows into the neck
    above (under the jaw) and below (z 1.08).
    - This is wider than the lead's "~0.12 per side", for the brief's own target (T / fan, wider than the skull).
      `HOOD_W` 1.45 is one constant; 1.22 gives |x| 0.55.
  - The upper panel's top shoulders stay under the lowest cheek spikes.
  - Hood 2x close-up from fixed cameras (back and game direction, idle f0 / f20, the hood swaying with the neck):
    `renders/_hood_back_2x_idle_f0_f20.png`.
  - The r11 radius-scale trial stays rejected (`_scratch/r11_hood_trial_rejected.png`).
- **Hood clearance, proxy-free, every frame of all four clips** (min, clip and frame):

  | hood vs | min BU | at |
  |---|---|---|
  | skull / head parts | 0.051 | idle f96 |
  | jaw | 0.078 | roar f32 |
  | frill + cheek spikes | 0.089 | idle f34 |
  | crown blade 1 | 0.466 | idle f36 |
  | crown blade 2 | 0.462 | idle f36 |
  | crown blade 3 (centre) | 0.490 | idle f102 |
  | crown blade 4 | 0.462 | idle f96 |
  | crown blade 5 | 0.466 | idle f96 |
  | left paw | 0.485 | roar f44 |
  | right paw | 0.485 | roar f44 |
  | left upper arm | 0.325 | idle f29 |
  | right upper arm | 0.325 | idle f89 |
  | Neck1 (below) | 0.154 | act_molt f85 |
  | chest | 0.380 | act_molt f18 |

  - All are **>= 0.02** (hood minimum 0.051 (idle f96)).
- **MUST 2, snout:** skull stations 0.82 / 0.96 half-height 0.082 / 0.040 -> **0.066 / 0.028** (widths kept). The tip
  (0.022) and the cap ring (x0.60) are unchanged. The nostrils re-seat by `surf_hit`.
  - `close_front.png` shows a lower, tapered snout front. The fangs are unchanged, and the roar mouth is unchanged
    (Jaw|Neck2 0.077 (roar f30)).
- **MUST 3, one gold number:** the gate counter is `_tools/game_icon.py` `gold_px_portrait_64` on the kit portrait icon
  (`CinderOverlord_icon.png`, idle f0) = **113** (>= 103, PASS). `gold_hist.py`'s kit window on the same icon gives
  the same 113.
  - The "91" the reviewer saw was a stale round-5-9 field (`gold_px_64` / the old `gold_method` text). It is moved to
    `history_pre_r12` and marked "not gates".
  - Reference only: portrait_alt 112, game icon 53. No extra gold was needed.
- **Kept:**
  - head + crown **0.320** of the figure height;
  - game area **0.208**;
  - paws past the outline 0.406 / 0.145;
  - crown neighbours >= 0.031;
  - shoulder seats <= **0.0277** (strict run: only those two entries);
  - Neck2|Spine and Body4|Body2 depth 0;
  - kit gate **collision_free true** (85 pairs, + Head / Jaw vs Neck2);
  - ground -0.006; loops 0 / 0; linear 0;
  - stride **5.0089** (walk keys unchanged); HEIGHT 11.72; tris **13580**.
- **Numbers (kit window H 29-58):**

  | icon | gold 64 | area 64 | gold 128 | area 128 |
  |---|---|---|---|---|
  | **Cinder kit portrait (GATE)** | 113 | 0.365 | 432 | 0.365 |
  | Cinder portrait_alt | 112 | 0.355 | 467 | 0.357 |
  | Cinder game camera | 53 | 0.208 | 195 | 0.205 |
  | InfernoPhoenix | 93 | 0.267 | 357 | 0.267 |
  | ThunderRex | 13 | 0.372 | 65 | 0.374 |
- **Renders** (title bars 14:21-14:24, "final 8.5 round 12"): the round-11 list plus `_hood_back_2x_idle_f0_f20.png`.
  - `gamelook_game` / `_tq`, `_icon_game_64_128`, `_icons2_strip_64` / `_128`, `_cv_idle_game` / `_front`.
  - `CinderOverlord_portrait_alt.png` + `_icon_alt`, `_icons_alt_strip_64` / `_128`, `_icons_strip_64` / `_128`.
  - `close_front`, `_close_sheet`, `_model_sheet`, `_pose_tq_sheet`, `_molt_r12_front` / `_tq`, `_cv_roar_front` /
    `_side`, `_cv_walk_game` / `_side`.
  - The `mr11_*` / `_molt_r11_*` files moved to `_scratch/stale_r12_renders/`.
- **Honest read:**
  - From the game camera the dark hood with its two blue spots now shows as a wide band under the crown and frill: a
    T / fan top on the neck.
  - At 64 px the hood and frill merge into one dark crowned block over the red coil.
  - The 3/4 and front views read as a hooded cobra-dragon.

## FINAL 8.5 ROUND 11 (2026-10-28, after `_review/CinderOverlord_final85_r11.md`: model 8.3, clips 8.5) - RAISED COBRA STANCE - EXPORTED 13:51
Owner decision (binding, via the lead): **raised cobra stance**.

Backups:
- the round-10 export: `_scratch/CinderOverlord_exported_r10.py`
- this export: `_scratch/CinderOverlord_exported_r11.py`

The patches are `_scratch/fix_r11.py` (stance, nose, crown x), `fix_r11c.py` (idle) and `fix_r11d.py` (seats), plus the
constants named below.
- **MUST 1, raised cobra stance:**
  - `FRONT[4]` z 1.16 -> **1.28**, `FRONT[5]` z 1.42 -> **1.60** (`HEAD_LIFT` 0.18). The neck's top half is 0.12-0.18
    taller; Neck2 / Neck3 are longer.
  - The head group rides up 0.18 through the `HEAD_XF` offset (-0.08 -> **+0.10**). Its pivot stays the build-space
    throat (`THROAT` 1.50, where the head is modelled), so the Head joint lands on the raised FRONT[5].
    - This gives the same world result as the review's "pivot 1.68 + jaw pivot / Jaw joint +0.18", with no head, jaw
      or crown coordinate re-typed.
  - **Deviation:** `HEAD_XF` scale 1.45 -> **1.60** (review: about 1.54). At 1.54 the taller figure made the kit-portrait
    gold **102** (< 103); at 1.60 it is 114, and head + crown is **0.320** of the figure height on the game camera.
  - **Lead decision needed: `HEIGHT` 10.5 -> 11.72 studs** (= 10.5 x 2.829 / 2.534 BU). Only the head is taller.
    Studs per BU stay as approved, so the body size, the stud pitch (0.0541) and the stride in studs are unchanged. With
    10.5 kept, the whole pet, body and slither stride included, would shrink 10 % in game. One-line revert.
  - **Game camera, idle f0:** the gap between the head group's lowest pixel and the body's highest pixel is **61.7 px**
    (r10 **42.2**), out of about 440 px of figure. The head and crown stand clear above the coil, with the neck as a
    stem between them.
  - **Hood trial (rejected):** I tried a cobra hood (the neck's side radius x2.1 under the head). From behind it read as a
    bulging barrel neck, not a hood, so it is not in the file (`_scratch/r11_hood_trial_rejected.png`).
- **Clips for the stance** (details in CLIP_NOTES round 11):
  - **Idle redone** as a COBRA SWAY. The r10 idle leaned the neck back 13.5 deg per breath, which dropped the head toward
    the game camera. The neck now stands upright and sways side to side; the head is held level.
  - **Walk keys unchanged.** The raised neck carries the head through the cycle at full height (gap 62.0-63.3 px, head
    pitch +/-0.6 deg), so there was nothing to redo.
  - Roar and act_molt re-checked.
- **MUST 2, flat nose cap:**
  - The skull's nose station 1.0 goes from half-height 0.032 to **0.022** (width 0.044 kept).
  - The cap ring's height factor goes from 0.80 to **0.60** (its width stays 0.80).
  - The nostril pits sit on the flatter top (`surf_hit` re-seats them).
  - From the front, the tip is now a low flat wedge with the narrow chin under it (`renders/close_front.png`, re-aimed
    0,-1.05,2.10 / 2.9 for the raised, larger head).
- **MUST 3a, crown gaps:** Crown_2 / Crown_4 x 0.150 -> **0.168**, Crown_1 / Crown_5 0.300 -> **0.310** (`CR_X1`,
  `CR_X2`). Neighbours, minimum over all four clips:
  - 1|2 0.031 (roar f21);
  - 2|3 0.031 (idle f26);
  - 3|4 0.031 (idle f26);
  - 4|5 0.031 (roar f21).
  - All are **>= 0.02**.
- **MUST 3b, seats changed (not only documented):**
  - **Shoulder:** the ball moves out onto the neck side, (+/-0.17, -0.71) -> (+/-**0.251**, **-0.765**), z 0.77.
    - Seat depth in Neck1: **0.0264** at rest, **0.0277** max over all clips (walk:10). The limit is 0.035; r10 was about 0.10.
  - **Chest / Neck2 caps:** the chest's end cap and Neck2's start cap (inside Neck1) go from 0.5 x r to **0.30 x r**.
    Neck2|Spine: no crossing, depth 0.
  - **Body2 / Body4 caps:** Body2's end cap and Body4's start cap (inside the Body3 bend) go from 0.45 / 0.55 x r to
    **0.30 / 0.35 x r**. Body4|Body2: no crossing in any clip, depth 0.
  - Arm|Neck2 is now 0.053 (idle f32), and Arm|Spine has depth 0.
  - **Strict run (A2): not collision-free as a count.** Its only entries are the two shoulder seats (Arm_L|Neck1 and
    Arm_R|Neck1, 4-8 triangle pairs re-shuffling around the root ring). `gate_f85.json` says this.
  - **Kit gate (A, joint-aware): collision_free true**, 83 pairs, every frame of all four clips.
- **NICE 1 / 2:**
  - The claw fan is wider (`PAW_GX` 0.042 -> 0.050).
  - The frill is longer (0.22 / 0.17 -> 0.26 / 0.21). It clears the crown by 0.135 (roar f44).
- **Paws past the body outline** on the game camera: near **0.387**, far **0.164** BU.
- **Clearances (proxy-free, every frame of all four clips):**
  - paws: Neck1 0.148 (walk f12), Spine 0.160 (walk f11), Jaw 0.580 (roar f32);
  - skull: Neck2 0.197 (act_molt f84);
  - jaw: Neck2 0.077 (roar f30).
- **Numbers (kit window H 29-58):**

  | icon | gold 64 | area 64 | gold 128 | area 128 |
  |---|---|---|---|---|
  | **Cinder portrait_alt** | 112 | 0.344 | 467 | 0.346 |
  | Cinder kit portrait | 114 | 0.350 | 428 | 0.350 |
  | Cinder game camera | 52 | 0.195 | 195 | 0.193 |
  | InfernoPhoenix | 93 | 0.267 | 357 | 0.267 |
  | Ivonrath | 25 | 0.295 | 112 | 0.295 |
  - Kit counter: portrait 114, game 52. Gold >= 103: PASS (portrait_alt **112**, kit portrait **114**).
  - Game area **0.195** (>= 0.18).
- **Step 1** (`_scratch/export_r11.txt`):
  - collision_free **true**; ground **-0.006**; linear 0; loops 0 / 0.
  - Tris **11460**. Stride **5.0089**: the rear body and the walk keys are unchanged, and `walk()` returns the stride from
    the segment lengths.
  - FBX `C:\cdimp\CinderOverlord.fbx` 13:51.
- **Renders** (title bars 13:47-13:55, "final 8.5 round 11"):
  - Game camera: `gamelook_game` / `_tq`, `_icon_game_64_128`, `_icons2_strip_64` / `_128`, and the NEW
    `_cv_idle_game` / `_cv_idle_front` (the cobra sway).
  - Portrait: `CinderOverlord_portrait_alt.png` + `_icon_alt`; `_icons_alt_strip_64` / `_128`.
  - Sheets: `close_front`, `_close_sheet`, `_model_sheet`, `_pose_tq_sheet`, `_molt_r11_front` / `_tq`,
    `_cv_roar_front` / `_side`, `_cv_walk_game` / `_side`.
  - The `mr10_*` / `_molt_r10_*` files moved to `_scratch/stale_r11_renders/`.
- **Honest read:** from behind and above, the game icon is now a crowned, maned head held clearly above the coil on a
  taller neck. It is still a vertical figure, though (the body runs away from the camera), so "dragon, not worm" at
  64 px stays the reviewer's call.

## FINAL 8.5 ROUND 10 (2026-10-28, after `_review/CinderOverlord_final85_r10.md`: model 8.3, clips 8.5) - EXPORTED 13:14
Backups:
- the round-9 export: `_scratch/CinderOverlord_exported_r9.py`
- this export: `_scratch/CinderOverlord_exported_r10.py`

The patch is `_scratch/fix_r10.py`, plus the follow-ups below. Items 3 / 2 / 1 of the round, in the lead's order.
- **MUST 3, collision proof** (details in CLIP_NOTES round 10):
  - **The proxies are exclusion zones, not sensors.** In `blockkit.overlap_report`, a crossing whose points ALL lie
    within r of any `joints()` segment counts as a hinge sliver and is IGNORED. So the review's extra proxies (paw r
    0.07, skull side r 0.12) would hide crossings at the paws and the skull sides, not check them.
    - Injection test: the left paw pushed 0.16 / 0.22 BU into the neck gives 51 / 89 crossings with no proxies, and
      **0** with the pet's joints or with the review's extra proxies. The cause is the Neck1 hinge sphere (r 0.34),
      which covers that spot.
    - So no exclusion proxy was added at the paws or the skull.
  - **Instead, three checks:**
    - (a) The kit gate now runs **83 pairs** (was 64). New: paws and arms vs Spine / Body1 / Neck2; Head and Jaw vs
      Neck1; all five crown blades vs the Head group (skull, cheek spikes, frill). Result: **collision_free true** in
      all four clips, every frame.
    - (b) Proxy-free **minimum surface clearance**, every frame of all four clips:
      - paws: Neck1 0.148 (walk f12), Spine 0.158 (walk f12), Neck2 0.265 (roar f44), Jaw 0.440 (roar f32), Head 0.591 (act_molt f18);
      - skull: Neck1 0.374 (act_molt f18), Neck2 0.134 (act_molt f84), arms 0.465 (act_molt f18);
      - jaw: Neck2 0.026 (roar f30, jaw open);
      - frill + cheek spikes: crown blades 0.123 (roar f26), Neck2 / Neck3 0.284 (walk f44).
      - All are **>= 0.02**.
    - (c) A run with only each pair's own hinge proxy. This found the centre crown blade's gold side frames grazing
      the neighbour sockets (molt f22). Fixed: the frames start 0.033 above the blade foot (inside the mount, not
      visible). Crown 2|3 is now 0.003 (act_molt f16).
      - What (c) still shows:
        - Seated contacts that exist at rest and stay in place (crossing box moves <= 0.035): the shoulder roots in
          Neck1 / Neck2 (their Neck2 / Spine crossings are 60-81 % buried inside Neck1), and the Spine / Neck2
          junction at the neck base.
        - One motion-only contact: the overlap ends of Body2 and Body4 meet on the inner side of the Body3 bend
          (walk f19 / f26, molt f82; partly buried in Body3). It is unchanged since the round-6 coil, and the kit
          treats it as a joint sliver. `_scratch/b3_bend.png`: f19 / f26 look the same as f12, which has none.
      - None of these involve the paws, the skull, the jaw or the frill.
  - The kit's Crown_3 proxy is now a hinge segment along its 0.2-wide socket (was a point). That gate saw the
    seated socket as "new" crossings once Crown_3 vs Head was checked. Every Crown_3 x Head crossing, rest and all
    clips, lies inside the mount block (x +/-0.102, y -0.628..-0.536, z 1.809..1.871).
- **MUST 2, jaw taper:**
  - The jaw tip goes from 0.046 / 0.020 to **0.034 / 0.016** (under the nose tip's 0.044). The 0.85 station goes from
    0.098 to **0.078** (rh 0.032 kept).
  - The lower fangs move in from x 0.075 to 0.064, so they stay on the narrower rim.
  - Front ray-cast (`_scratch/face_id.py`, close_front aim: same target, direction and distance): the jaw's
    visible width is now 0.267 BU at most (was 0.284). Going down, the face outline only narrows
    (0.40 -> 0.38 -> 0.37 -> 0.25 -> 0.23).
  - Caveat: the round red snout cap with its two nostrils is unchanged (not in the list). If the reviewer still reads a
    nose bulb, the next lever is that cap.
- **MUST 1a, paws:**
  - Paw box (0.052, 0.046, 0.042) -> **(0.070, 0.062, 0.056)**. Claws 0.075 / 0.015 -> **0.110 / 0.020**, spaced 0.042.
  - The arm segments are a touch thicker. The hand moves to x +/-**0.39**, the elbow to +/-**0.42**.
  - On the `gamelook_game` camera (`_scratch/paw_px.py`), past the body outline:
    - near paw (L) **0.378 BU**;
    - far paw (R) **0.107 BU**.
    - Both are >= 0.10.
- **MUST 1b, skull frill:** one swept-back obsidian pair per side on the rear skull, above the cheek spikes.
  - Built with the same `B.spike(..., OBS_D, "Head", top=(0.12, 0.35))` call. At build scale (`FRILL` in the file):
    - base (0.150, -0.470, 1.790), dir (0.80, 0.56, 0.28), L 0.22, w 0.050;
    - base (0.165, -0.465, 1.715), dir (0.86, 0.50, 0.04), L 0.17, w 0.045.
    - That is about 35 deg swept back from the side.
  - In world units the tips reach |x| **0.538** against the skull side's 0.334, so **+0.20 BU** past the skull (top
    view).
  - They clear the crown blades by 0.123 (roar f26).
  - Read: a dark spiked mane around the head, in the portrait icons and from the game camera.
- **Keeps:**
  - HEAD_XF 1.45; head + crown **0.306** of the figure height on the game camera; stride **5.0089**.
  - Gold >= 103: PASS (portrait_alt **127**; kit counter portrait 104 / game 45). The frill and paws widen the figure,
    so the icon scales down a little (r9: 135 / 110 / 47).
- **Numbers (kit window H 29-58):**

  | icon | gold 64 | area 64 | gold 128 | area 128 |
  |---|---|---|---|---|
  | **Cinder portrait_alt** | 127 | 0.376 | 483 | 0.375 |
  | Cinder kit portrait | 104 | 0.377 | 427 | 0.375 |
  | Cinder game camera | 45 | 0.197 | 181 | 0.197 |
  | InfernoPhoenix | 93 | 0.267 | 357 | 0.267 |
  | Ivonrath | 25 | 0.295 | 112 | 0.295 |
  - Game-camera area **0.197** (>= 0.18).
- **Step 1** (`_scratch/export_r10.txt`):
  - collision_free **true**; ground -0.006; linear 0; loops 0 / 0.
  - Tris **11396**; stride **5.0089**.
  - FBX `C:\cdimp\CinderOverlord.fbx` 13:14.
- **Renders** (title bars 13:15-13:19, "final 8.5 round 10"):
  - Game camera: `gamelook_game` / `_tq`, `_icon_game_64_128`, `_icons2_strip_64` / `_128`.
  - Portrait: `CinderOverlord_portrait_alt.png` + `_icon_alt`; `_icons_alt_strip_64` / `_128`.
  - Sheets: `close_front`, `_close_sheet`, `_model_sheet`, `_molt_r10_front` / `_tq`, `_cv_roar_front` / `_side`,
    `_cv_walk_game` / `_side`, `_pose_tq_sheet`.
  - The `mr9_*` / `_molt_r9_*` files moved to `_scratch/stale_r10_renders/`.
- **Not done (TO 9+):** the tail-tip crop in the walk tile, a standing Index pose, a flank accent, and
  `_review/GLACIER_CONCEPTS.md` lines 46 / 116. That last file is outside the files this builder may edit.

## FINAL 8.5 ROUND 9 (2026-10-28, after `_review/CinderOverlord_final85_r9.md`: model 8.4, clips 8.5 PASS) - EXPORTED 10:00
Backups:
- the round-8 export: `_scratch/CinderOverlord_exported_r8.py`
- this export: `_scratch/CinderOverlord_exported_r9.py`

The patch is `_scratch/fix_r9.py`, plus the muzzle taper.
- **MUST 1a, forearms out:** the elbow goes to x +/-**0.40** and the hand to +/-**0.36** (same y, z), in the model, the rig
  fallback and the `joints()` list.
  - The forearm now stands ~0.12 outside the chest outline at z 0.65.
  - From the game camera the near-side (left) claw shows as a braced arm beside the neck, in the idle and through the
    walk (`renders/gamelook_game.png`, `_cv_walk_game.png`).
  - The far-side claw stays behind the neck from that camera.
  - The slither and the paddles are unchanged and collision-free.
- **MUST 1b, broader skull:** Head + Jaw + Mouth parts go **x1.15 in x only** about the throat line (x = 0); the
  Crown_1..5 blades are untouched, so the sockets keep their spacing.
  - blockkit's `HEAD_XF` is uniform only, so this is a pet-side `_xscale()` run just before `B.build()`. Boxes keep
    their rotation and each local half-size grows by its scaled axis length; tubes / polys map their points.
  - HEAD_XF stays 1.45. Head + crown on the game camera: **0.306 of the figure height** (0.264 of the icon).
- **MUST 1c:** the Tail4 ring is dropped - only the Spine-base and Body1 rings remain (two bands on the back).
- **MUST 2, front face:**
  - As asked: the jaw station at 0.85 goes rh 0.040 -> **0.032**, and the jaw's front sits **0.02 further back** (the
    loft end -0.48 -> -0.46).
  - That alone still left a round nose pad above the chin, so the muzzle also tapers to a narrower tip:
    - skull stations 0.82 / 0.96 / 1.0: 0.118 / 0.070 / 0.055 wide -> 0.112 / 0.060 / 0.044;
    - the jaw tip 0.056 x 0.022 -> 0.046 x 0.020;
    - both nose caps sit flatter (x0.80 rings).
  - The nostril pits on top are unchanged.
  - From the front the nose is now a narrow muzzle tip with the chin tucked behind it, not two stacked round bulbs
    (`renders/close_front.png`, `_close_sheet.png`).
- **Numbers (kit window H 29-58):**

  | icon | gold 64 | area 64 | gold 128 | area 128 |
  |---|---|---|---|---|
  | **Cinder portrait_alt** | 135 | 0.378 | 536 | 0.378 |
  | Cinder kit portrait | 110 | 0.370 | 449 | 0.367 |
  | Cinder game camera | 47 | 0.192 | 187 | 0.193 |
  | InfernoPhoenix | 93 | 0.267 | 357 | 0.267 |
  | Ivonrath | 25 | 0.295 | 112 | 0.295 |
  - Kit counter: portrait 110, game 47. Gold >= 103: PASS (portrait_alt **135**).
  - Game-camera area **0.192** (>= 0.18).
- **Step 1** (`_scratch/export_r9.txt`):
  - collision_free **true** in all four clips (forearms out, wider skull; molt and roar included).
  - Ground -0.006; linear 0; loops 0 / 0.
  - Tris **11,348**; stride **5.0089**.
  - FBX `C:\cdimp\CinderOverlord.fbx` 10:00.
- **Renders** (title bars 10:00-10:01, "final 8.5 round 9"):
  - Game camera: `gamelook_game` / `_tq`, a game icon at 64 and 128 (`renders/_icon_game_64_128.png`), and the two
    `_icons2_strip` sizes.
  - Portrait: `CinderOverlord_portrait_alt.png` + `_icon_alt`; `_icons_alt_strip_64` / `_128` (with Phoenix and Ivonrath).
  - Sheets: `close_front`, `_close_sheet`, `_model_sheet`, `_molt_r9_front` / `_tq`, `_cv_roar_front` / `_side`,
    `_cv_walk_game` / `_side`, `_pose_tq_sheet`.
  - The `mr8_*` / `_molt_r8_*` files moved to `_scratch/stale_r9_renders/`.

## FINAL 8.5 ROUND 8 (2026-10-28, after `_review/CinderOverlord_final85_r8.md`: model 8.4, clips 8.5 PASS) - EXPORTED 09:32
Backups:
- the round-7 export: `_scratch/CinderOverlord_exported_r7.py`
- this export: `_scratch/CinderOverlord_exported_r8.py`

The patch is `_scratch/fix_r8.py`, plus the vent snap / crack edits.
- **1, head + crown:**
  - `HEAD_XF` 1.38 -> **1.45** (the lead's cap) and the centre blade 0.36 -> **0.40**.
  - Head + crown on the game camera (`_scratch/head_share.py`, idle f0): **0.302 of the figure height, 0.260 of the
    icon height**.
  - The icon frame is 1.16 x the larger side, so the whole figure tops out at 0.86 of the icon. The 0.30-of-icon target
    is NOT reached at 1.45 + 0.40; per the lead I did not go bigger.
  - Molt and roar are collision-free with the bigger head.
- **2, bands:** the Body4 ring is dropped (skip set 2-7). The rear rings are now on the Spine base, Body1 and Tail4;
  from behind the back shows two bands.
- **3, vents:** the six slits (Spine, Body1, Body2 x 2 sides) are **30 % shorter** and **flush**.
  - New `vent_flush()`: each slit is 5 short overlapping bars that follow the curved flank.
  - Their points are ray-cast onto the REAL skin, because the loft is a superellipse and `surf_pt`'s ellipse sat ~0.01
    inside it: the first flush try was buried.
  - The top sits 0.001 proud of the skin, with a 0.002 core line.
  - Width x0.65, so they read as jagged glowing cracks, not plates or limbs; nothing sticks past the outline from the
    game camera (`renders/gamelook_game.png`).
- **4, dorsal spikes +25 %** (body Spine..Tail1 and neck Neck1..3, length and base width). Collision-free with the crest
  in the molt and the roar.
- **5, hygiene:**
  - MODEL_NOTES line 3 now says MYTHIC.
  - `crown_*.png` and the `mr7_*` / `_molt_r7_*` frames moved to `_scratch/stale_r8_renders/`.
  - 9+ chin: the jaw tip goes 0.063 x 0.026 -> 0.056 x 0.022, the 0.85 station rh 0.044 -> 0.040, and the cap ring
    sits at 1.006 (was 1.012).
- **Portrait_alt camera:** a little higher, dir (1, -1.36, **0.80**) (kit 0.62).
  - Reason: the taller crest pushed the molt portrait area down to 0.348, under the round-7 >= 0.36 bar. At 0.80 it is
    0.373; still the molt peak f40, still three-quarter front.
- **Numbers (same counter, icon3 recipe, kit window H 29-58):**

  | icon | gold 64 | area 64 | fill h | gold 128 | area 128 |
  |---|---|---|---|---|---|
  | **Cinder portrait_alt (molt f40, z 0.80)** | 136 | 0.373 | 0.91 | 537 | 0.373 |
  | Cinder kit portrait | 114 | 0.360 | 0.91 | 464 | 0.360 |
  | Cinder game camera | 47 | 0.188 | 0.91 | 186 | 0.188 |
  | InfernoPhoenix | 93 | 0.267 | 0.91 | 357 | 0.267 |
  | Ivonrath | 25 | 0.295 | 0.67 | 112 | 0.295 |
  - Kit counter (`game_icon.py`): portrait 114, game 47.
  - **Gold >= 103: PASS** - portrait_alt **136** (Phoenix 93; at 128 px 537 vs 357, and vs 436 on its widened window).
  - **Area:** portrait_alt **0.373** (>= 0.36); game camera **0.188** (>= 0.18).
- **Step 1** (`_scratch/export_r8.txt`):
  - collision_free **true** in all four clips; ground -0.006; linear 0; loops 0 / 0.
  - Tris **11,384** (the curved vents); stride **5.0089** (unchanged).
  - FBX `C:\cdimp\CinderOverlord.fbx` 09:32.
- **Renders** (title bars 09:33-09:35, "final 8.5 round 8"):
  - Portrait: `CinderOverlord_portrait_alt.png` + `_icon_alt`.
  - Strips: `_icons_alt_strip_64` / `_128` (with Phoenix and Ivonrath), the two `_icons_strip` and two `_icons2_strip` sizes.
  - Sheets: `gamelook_game` / `_tq`, `close_front`, `_close_sheet`, `_model_sheet`, `_molt_r8_front` / `_tq`,
    `_cv_roar_front` / `_side`, `_cv_walk_game` / `_side`, `_pose_tq_sheet`.

## FINAL 8.5 ROUND 7 (2026-10-28, after `_review/CinderOverlord_final85_r7.md`: model 8.3, clips 8.5 PASS) - EXPORTED 09:08
Backups:
- the round-6 export: `_scratch/CinderOverlord_exported_r6b.py`
- this export: `_scratch/CinderOverlord_exported_r7.py`

The patch is `_scratch/fix_r7.py` (+ the nostril line and the inward gold).
- **MUST 1a, vents:** the slits on Body3, Body4 and Tail1 are gone. The vents stay on the Spine, Body1 and Body2 (the
  front of the body near the head).
  - The `Vent_4..6` bones go with them; only `Vent_1..3` remain.
  - The plan's FX_VentSmoke_4..6 therefore have no anchor (VFX is not built yet).
- **MUST 1b, head:** the head group goes **x1.15** (`HEAD_XF` 1.20 -> 1.38, about the throat). The crown mount is
  0.04 wider each side (ends 0.22 -> 0.26).
  - Head + crown height on the game icon (`_scratch/head_share.py`): **0.244** of the icon height (0.283 of the figure).
    The review's target is >= 0.30 (not reached).
- **MUST 2, gold:**
  - The centre blade goes 0.34 -> **0.36**.
  - The centre and middle gold frames get **+0.004**. It went INWARD: outward, Crown_2|3 and Crown_3|4 touched even in
    the idle. The frames now sit at `gin` 0.25 x gw + 0.004.
- **Numbers (same counter, icon3 recipe):**

  | icon | gold 64 (H 29-58) | gold 64 (H 29-60) | area 64 | fill h | gold 128 (H 29-58) | gold 128 (H 29-60) | area 128 |
  |---|---|---|---|---|---|---|---|
  | **Cinder portrait_alt (molt f40)** | 113 | 114 | 0.364 | 0.91 | 466 | 466 | 0.363 |
  | Cinder kit portrait | 108 | 111 | 0.373 | 0.91 | 427 | 429 | 0.374 |
  | Cinder game camera | 45 | 45 | 0.190 | 0.89 | 167 | 167 | 0.190 |
  | InfernoPhoenix | 93 | 109 | 0.267 | 0.91 | 357 | 436 | 0.267 |
  | Ivonrath | 25 | 25 | 0.295 | 0.67 | 112 | 111 | 0.295 |
  - Kit counter (`game_icon.py`): portrait 108, game 45.
  - **Gold >= 103: PASS** - portrait_alt 113 at 64 px (+21 % over the Phoenix's 93). At 128 px it is 466, which also
    beats the Phoenix's widened-window 436.
  - **Area:** portrait_alt 0.364 (>= 0.36); game camera **0.190** (>= 0.18).
  - **Head line:** in `renders/_icons_alt_strip_128.png` the Cinder's crown reaches the top of its tile, above the
    Phoenix's crest line.
- **9+:**
  - Eyes: the slit outer ends come in another 0.01 (socket 0.115 -> 0.110, slit 0.100 -> 0.095; the inner ends stay).
  - Chin: the jaw tip station is ~15 % flatter / narrower (0.074 x 0.030 -> 0.063 x 0.026) and the cap ring sits
    closer (1.024 -> 1.012).
  - Nostrils: 0.012 x 0.018 -> **0.018 x 0.024**, which is 0.025 x 0.033 BU as shown (x1.38 head).
- **Step 1** (`_scratch/export_r7.txt`):
  - collision_free **true** in all four clips (the bigger head in the roar / molt included); ground -0.006; linear 0;
    loops 0 / 0.
  - Tris **10,188**; stride **5.0089** (unchanged).
  - FBX `C:\cdimp\CinderOverlord.fbx` 09:08.
- **Renders** (title bars 09:09-09:11, "final 8.5 round 7"):
  - Portrait: `CinderOverlord_portrait_alt.png` (molt f40) + `_icon_alt`.
  - Strips: `_icons_alt_strip_64` / `_128` (with Phoenix and Ivonrath), the two `_icons_strip` and two `_icons2_strip` sizes.
  - Close-ups (re-framed for the bigger head): `close_front`, `_close_sheet`.
  - Sheets: `gamelook_game` / `_tq`, `_model_sheet`, `_pose_tq_sheet`, `_cv_walk_game` / `_side`, `_cv_roar_front` /
    `_side`, `_molt_r7_front` / `_tq`.
  - The `mr4_*` / `mr6_*` frames and `_molt_r6_*` moved to `_scratch/stale_r7_renders/`.

## FINAL 8.5 ROUND 6 (2026-10-28, after `_review/CinderOverlord_final85_r6.md`: model 8.4, clips 8.5 on every clip) - EXPORTED 08:41
Backups:
- the round-5 export: `_scratch/CinderOverlord_exported_r5.py`
- this export: `_scratch/CinderOverlord_exported_r6b.py`
- **MUST 1, the game-camera worm read:**
  - (a) Ring skip set `(3, 5, 7)` -> **`(2, 3, 5, 6, 7)`**. The rings stay on the Spine base, Body1, Body4 and Tail4,
    i.e. 3 dark bands on the rear 8 segments. The Neck1 ring and the dorsal saddle are kept.
  - (b) **RAD[1..4] +10 %** (0.339 / 0.308 / 0.277 / 0.220). The Body4 -> Tail1 taper (0.220 -> 0.168) reads fine in
    `_model_sheet`.
  - Measured with (a) + (b) alone: game-camera area **0.166**, fill width **0.50** - NOT enough; thickness hardly moves it.
    Extra test: tail +30 %, neck +15 % -> area 0.175, width 0.50.
  - (c) So I added **COIL = 1.5**: each body segment's heading away from the mean is x1.5. The S coils sideways and
    reads as a coiled serpent rather than a straight worm.
    - Every segment keeps its round-5 3D length, so the slither **stride stays 5.0089** (a plain RAD +10 % would have
      made it 5.0186).
    - Non-adjacent body points stay >= 0.08 apart; collision-free.
  - Result (game icon, 64 px): area **0.190** (pass >= 0.18). Fill width **0.53** (FAIL vs >= 0.60).
    - Why the width won't move: the game camera sits behind and 24 deg to the side, so the body's run toward the
      camera also adds width. Coiling swaps that run for sideways S, and the two nearly cancel (coil 1.4 / 1.6 gave
      0.53 / 0.55).
    - Getting >= 0.60 needs the rear body to trail at an angle to the travel line, and then the slither would look like
      it crabs sideways. **Lead decision needed.**
  - Game-camera gold went up to 35 (kit counter) from 25.
- **MUST 2, outclass (same counter, icon3 recipe):**

  | icon | gold 64 (H 29-58) | gold 64 (H 29-60) | area 64 | fill h | fill w | gold 128 (H 29-58) | gold 128 (H 29-60) | area 128 |
  |---|---|---|---|---|---|---|---|---|
  | **Cinder portrait_alt (molt f40)** | 94 | 94 | 0.373 | 0.89 | 0.75 | 390 | 391 | 0.372 |
  | Cinder kit portrait (idle f0) | 91 | 92 | 0.382 | 0.91 | 0.78 | 355 | 356 | 0.383 |
  | Cinder game camera | 35 | 35 | 0.190 | 0.89 | 0.53 | 129 | 128 | 0.191 |
  | InfernoPhoenix | 93 | 109 | 0.267 | 0.91 | 0.80 | 357 | 436 | 0.267 |
  | Ivonrath | 25 | 25 | 0.295 | 0.67 | 0.91 | 112 | 111 | 0.295 |
  | ThunderRex | 13 | 14 | 0.372 | 0.91 | 0.91 | 65 | 71 | 0.374 |
  | CosmicLeviathan | 20 | 31 | 0.208 | 0.56 | 0.91 | 89 | 132 | 0.208 |
  - Before the fix, the Cinder's portrait_alt gold was 88 / 349 (64 / 128) vs the Phoenix's 93 / 357, so it failed on
    gold. The opaque area already beat both.
  - Fix, crest only: the gold frames widen **+25 % INWARD**. The new `plate_crown(gin=)` moves the frame centre in
    and grows its half-width by the same amount, so the outer edge and the blade-to-blade clearance stay put.
    - A plain x1.25 width made Crown_2|3 and Crown_3|4 touch in the roar and the molt, so it was dropped.
    - +45 % inward gave only +2 px more and covered the blue inner V, so it was dropped too.
  - Result:
    - The Cinder portrait_alt is >= Phoenix and Ivonrath on gold (94 vs 93 / 25 at 64; 390 vs 357 / 112 at 128) and
      on area (0.373 vs 0.267 / 0.295).
    - Fill height: Cinder 0.89, Phoenix 0.91, Ivonrath **0.67**. Ivonrath is below the 0.70 bar on its own icon; that is
      not the Cinder's.
    - Caveat: the 64 px gold margin over the Phoenix is 1 px on the kit window. On the widened window the Phoenix
      counts 109 / 436 because 14 / 68 of its px are lemon flame (H 59-61); the Cinder has 0 lemon.
- **Step 1** (`_scratch/export_r6.txt`):
  - collision_free **true** (all four clips, incl. the molt with the thicker body); ground -0.006; linear 0; loops 0 / 0.
  - Tris **10,268** (fewer rings); stride **5.0089**.
  - FBX `C:\cdimp\CinderOverlord.fbx` 08:41.
- **Re-made from the final file** (title bars 08:43 / 08:46, "final 8.5 round 6"):
  - The `CinderOverlord_portrait_alt.png` (molt f40) render is from 08:42; `CinderOverlord_icon_alt.png` was made from it.
  - Strips: `_icons_alt_strip_64` / `_128` = [alt, kit, Phoenix, Ivonrath, Rex, Leviathan], the two `_icons_strip` and
    two `_icons2_strip` sizes.
  - Sheets: `_pose_tq_sheet`, `_cv_walk_game` / `_side`, `_cv_roar_front` / `_side`, `_molt_r6_front` / `_tq`,
    `close_front`, `_close_sheet`, `gamelook_game` / `_tq`, `_model_sheet`, `flat_game_stamped`.
  - Stale sheets (`_molt_r4_*`, `_cv_molt_front`, `_clip_sheet_v1`) moved to `_scratch/stale_r6b_renders/`.

## FINAL 8.5 ROUND 5 (2026-10-28, after `_review/CinderOverlord_final85_r5.md`: model 8.4, clips 8.5 PASS) - EXPORTED 06:09
Backups:
- the round-4 export: `_scratch/CinderOverlord_exported_r4.py`
- this export: `_scratch/CinderOverlord_exported_r5.py`

The 9+ patch is `_scratch/fix_r5.py`; the nose / chin caps were added after it (see 9+ below).
- **MUST 1, gold to amber:** crest-only `GOLD` (255, 196, 50) -> **(250, 160, 35)**.
  - Chosen from a 4-colour sweep on the kit portrait (`_scratch/gold_sweep_crest.png`, `gs_c0..c3`):

    | colour | kit H 29-58 | lemon H 59-61 | look |
    |---|---|---|---|
    | c0 (255, 196, 50), the old gold | 36 | 24 | lemon |
    | c1 (255, 172, 40) | 64 | 8 | still yellow-leaning |
    | **c2 (250, 160, 35)** | **80** | **1** | amber gold |
    | c3 (240, 150, 30) | 77 | 0 | turning orange |
  - c0 measured with my tool = 36, the same as the kit counter's round-4 number, so the tool matches the kit.
  - Why the hue moved: the lit faces had clipped G to 255 (lemon). With c2 they land at H 42-52.
    The shaded faces sit at H 30-38, which is still gold, not orange (`renders/close_front.png`).
  - GOLD_D is unused (no change).
- **Gold at 64 px** (`_scratch/gold_hist.py`, s > .5, v > .45; data `_scratch/gold_r5.json`):

  | icon | kit window H 29-58 | widened H 29-60 | lemon H 59-61 | fill height | opaque area |
  |---|---|---|---|---|---|
  | kit portrait (idle f0) | 81 | 83 | 2 | 0.91 | 0.383 |
  | game camera | 25 | 25 | 0 | 0.91 | 0.163 |
  | **portrait_alt (molt f40)** | 91 | 91 | 0 | 0.89 | 0.374 |
  | ThunderRex | 13 | 14 | 1 | 0.91 | 0.372 |
  | CosmicLeviathan | 20 | 31 | 8 | 0.56 | 0.208 |
  - Kit counter (`_tools/game_icon.py`): portrait **81**, game **25** - the same as above.
  - The game icon is AT the 25 floor (it was 28). Hue is not what limits it:
    - c2, (252, 168, 40) and (255, 176, 44) all give 25 there (`_scratch/g2_*`).
    - From behind only ~25 px of the crest frames show.
- **MUST 2, icon presence (lead ruling: pose + framing, not the model):**
  - `CinderOverlord_portrait_alt.png` (06:10) is the kit portrait camera (tq, transparent 512) at the **molt peak
    f40**: crest fanned 90 deg, neck arched, head level-high. The icon crops to the bounding box (icon3 recipe).
  - Icon: `CinderOverlord_icon_alt.png`.
  - Strips: `renders/_icons_alt_strip_64.png` / `_128.png`, laid out as [alt, kit idle f0, Thunder Rex, Cosmic Leviathan].
  - Numbers:
    - Height fill **0.89** (pass >= 0.70); gold 91 / 91, lemon 0.
    - Thunder Rex: fill 0.91, area 0.372. Cosmic Leviathan: fill 0.56, area 0.208.
  - Note: the current kit icon already measured fill 0.906 and area 0.383. The 'about 50 %' in the review matches the
    Cosmic Leviathan (0.56), not the Cinder.
  - Closer / lower cameras were tried (`_scratch/pp_m4-m9`, `pp_r1-r3`). They cut the body at the frame edge or gave a
    narrower, weaker silhouette, so the kit distance was kept.
- **9+ (cheap):**
  - T-a eyes: socket and slit outer ends come in 0.02; the inner ends stay.
  - T-b snout: the "pig snout" was the skull's studs showing on the flat snout front. Now:
    - a smaller stud-free cap ring 0.012 ahead of the snout tip;
    - the jaw tip a touch flatter (rh 0.034 -> 0.030), with a stud-free chin cover and the same kind of cap.
    - From the front: a smooth nose and chin, the two nostril pits on top (`renders/close_front.png`, `_close_sheet.png`).
- **Step 1** (`_scratch/export_r5.txt`):
  - collision_free **true**; ground -0.006 everywhere; linear 0; loops 0 / 0.
  - Tris **10,468** (+240 for the caps / chin cover); stride **5.0089 BU / 48 f**.
  - FBX `C:\cdimp\CinderOverlord.fbx` 06:09.
- **Renders** (title bar 06:12, "final 8.5 round 5"):
  - `close_front`, `_close_sheet`, `gamelook_game` / `_tq`, `_model_sheet`, `flat_game_stamped`.
  - The two `_icons_strip` and two `_icons2_strip` sizes, plus `_icons_alt_strip_64` / `_128` (06:10).

## FINAL 8.5 ROUND 4 (2026-10-28, after `_review/CinderOverlord_final85_r4.md` + coordinator) - EXPORTED 05:00
Backup of the round-3 export: `_scratch/CinderOverlord_exported_r3.py`.
- **1, vents:**
  - The vent core bar is now ROSE (the deep blue), not LAVA. The white cores read as ladder rungs.
  - In the walk from the game camera the blue slits still read as legs, so per T-e I dropped one slit of each pair. The
    pairs sit side by side along the body, not upper / lower, so each segment side keeps ONE slit at the pair centre
    (where the `Vent_*` anchor already is).
  - Now 6 slits per side instead of 12; no colour added. `renders/_cv_walk_game.png`.
- **2, neck:** the Neck3 ring is dropped and Neck2 is a thin band (0.70-0.80). From above: one full band (Neck1) and one
  thin band (Neck2); the Neck3 dorsal spike reads as a spike, not a band, so it stays. `renders/gamelook_game.png`.
- **3, walk renders:** `_cv_walk_game.png` / `_cv_walk_side.png` are re-made from the current file (05:00).
- **T-a, eyes:** the eye point moves to y -0.86 (was -0.83, originally -0.80); the brows follow.
- **T-b, snout:** the skull's tip stations are 10 % flatter (rh 0.048 -> 0.043 and 0.040 -> 0.036); the smooth cover and
  the nostrils follow.
- **T-c, molt:** the outer blades lift **50 deg** (was 45). Still collision-free.
  - Front fan spread: f0 48.0, f22 69.4, f34 / f40 **90.0** deg (was 85.0).
  - Rise vs fall peak (deg/f): outer 8.29 vs 6.62, middle 7.88 vs 6.35, centre 5.18 vs 3.17 - every fall stays slower.
- **Gold at 64 px:**

  | tool | portrait | game |
  |---|---|---|
  | kit counter (`game_icon.py`) | **36** | **28** |
  | `gold_cmp` kit window | 38 | 29 |
  | rendered window (H 40-62) | **35** | 9 |
- **Shares (all figure pixels, %):**

  | view | body | obsidian | pale | blue | gold |
  |---|---|---|---|---|---|
  | game | 53.0 | 25.0 | 2.7 | 6.5 | 6.4 |
  | side | 55.1 | 18.1 | 12.4 | 6.3 | 2.8 |
  | tq | 44.7 | 23.2 | 12.9 | 5.1 | 8.3 |
  | back | 52.7 | 23.7 | 4.6 | 6.2 | 6.5 |
- **Step 1** (`_scratch/export_r4.txt`):
  - collision_free **true**; ground_min_z -0.006 everywhere; linear 0; loops 0 / 0.
  - Tris **10,228**. Export stride **5.0089 BU / 48 f**.
- **Renders (title bar = 2026-10-28 05:00):** `close_front`, `_close_sheet`, `gamelook_game`, `flat_game_stamped` (plain
  `flat_game` kept for the sampler), the four icon strips, `_model_sheet`, `_molt_r4_front` / `_side`,
  `_cv_walk_game` / `_side`, `_pose_tq_sheet`.

## FINAL 8.5 ROUND 3 (2026-10-28, after `_review/CinderOverlord_final85_r3.md` + coordinator) - EXPORTED 04:25
Backup of the round-2 export: `_scratch/CinderOverlord_exported_r2.py`.
- **MUST 1, forehead:** the obsidian skull cap ends at the eye line (stations 0.66 / 0.78 removed); the brows are
  unchanged. `renders/close_front.png` shows a red forehead band between the brows and the cap edge, with the nasal
  ridge down its middle.
- **MUST 2, neck:** only Neck1 keeps a full ring; Neck2 and Neck3 are narrow bands (0.62-0.80). From above there is one
  full band plus two thin ones (`renders/gamelook_game.png`).
- **MUST 3, nostrils:** pits are **0.006 x 0.004 x 0.009** at y -1.07 (the snout tip); they no longer read as a second
  pair of eyes.
- **T1, vents flush:** the slits are placed with `off=0.000` and the blue bar is **0.006** deep. The white-hot core
  line is 0.004 deep, 0.004 proud of the blue, so it does not stick out.
  - From the game camera the vents still read as blue-and-white bars - their colour carries the read - but nothing
    stands off the body any more.
- **T2, centre blade 0.32 -> 0.34:** the molt is still collision-free.
  - Front fan spread f0 / 22 / 34 / 40 is 48.0 / 66.9 / 85.0 / 85.0 deg, unchanged.
  - The model is now **2.276 BU** tall (was 2.254). HEIGHT stays 10.5 studs, so the in-game body is ~1 % smaller; the
    stud pitch is 0.0486.
- **T3, eyes:** 0.03 toward the nose (the brows follow).
- **Gold at 64 px, both windows:**

  | window | portrait | game |
  |---|---|---|
  | kit counter | **35** | **28** |
  | rendered (H 40-62, s >= 0.6, v >= 0.55) | **35** | 8 |
- **Shares (all figure pixels, %):**

  | view | body | obsidian | pale | blue | gold |
  |---|---|---|---|---|---|
  | game | 47.3 | 25.4 | 3.1 | 7.2 | 6.3 |
  | side | 49.8 | 18.1 | 12.5 | 7.3 | 2.7 |
  | tq | 41.5 | 23.1 | 13.1 | 5.6 | 8.3 |
  | back | 47.2 | 24.2 | 4.9 | 7.1 | 6.4 |
- **Step 1** (`_scratch/export_r3.txt`): collision_free **true**; ground_min_z -0.006 in every clip; linear 0; loops 0 / 0.
  Tris **10,616**.
- **Walk stride (for the import check):** the export metadata carries **5.0089 BU per 48 f**.
- **Renders (title bar = render time, 2026-10-28 04:26):**
  - `close_front.png`, `_close_sheet.png`, `gamelook_game.png`, `_model_sheet.png`.
  - `_icons_strip_64/128.png`, `_icons2_strip_64/128.png`.
  - `_molt_r4_front.png`, `_pose_tq_sheet.png`.
  - `flat_game_stamped.png` - `flat_game.png` itself is left unstamped for the share sampler.

## FINAL 8.5 ROUND 2 (2026-10-28, after `_review/CinderOverlord_final85_r2.md` + coordinator) - EXPORTED
Backup of the round-1 export: `_scratch/CinderOverlord_exported_f85.py`. Gate file: `_scratch/gate_f85.json` (still the only one).
- **Brightness (coordinator):** the body is **(176,72,54)** (was 166,66,50), the same ember hue (H 8.9 vs 8.3). In
  `renders/_icons_strip_128.png` it stays red-ember: no drift toward Ivonrath's purple or the Phoenix's orange.
- **R2-M1, neck:** rings stay on Neck1 and Neck3; Neck2 has a narrow band (0.62-0.80); the ring on the chest curve is
  dropped. From above the neck now shows three bands, one of them thin (was four). `renders/gamelook_game.png`.
- **R2-M2, brows:** half-length **0.070**, roll **10 deg** (as asked).
  - At those numbers the outer ends still reached the crown mount from the front. The brow plane faces outward and
    forward, so its outer end sits further back and rises on screen.
  - I also moved the brows 0.012 toward the nose (BROW_IN 0.030) and dropped them **0.016** (BROW_DZ 0.040, was 0.056).
  - `renders/close_front.png` (and `_scratch/brow_zoom.png`): short dark blocks over the eyes, with red skull between
    them and the crown mount. The forward points are unchanged.
- **R2-M3, vents:** the blue slits are **15 % longer**. They sit 4 deg further up the flank (32 / 148) so the lower ends
  stay clear of the pale scutes.
- **R2-M4, gold, both windows at 64 px:**

  | window | portrait | game |
  |---|---|---|
  | kit counter (H 29-58, s > 0.5, v > 0.45) | **33** | 21 |
  | rendered (H 40-62, s >= 0.6, v >= 0.55) | **30** | 10 |

  Both portrait windows are >= 25, so no gold change was needed.
- **TO 9+:**
  - (a) A smooth stud-free cover over the snout tip (the skull loft f 0.74-1.0, +0.004); the nasal ridge and nostrils
    sit on it.
  - (b) Tail4 is 45 % shorter (the tip pulled in, the curl 0.13), so the walk stride is now **5.01 BU** per 48 f (was 5.19).
- **Shares (all figure pixels, %):**

  | view | body | obsidian | pale | blue | gold |
  |---|---|---|---|---|---|
  | game | 45.4 | 25.5 | 2.8 | 9.4 | 6.1 |
  | side | 48.5 | 18.2 | 12.3 | 8.6 | 2.6 |
  | tq | 40.2 | 23.6 | 12.9 | 6.6 | 7.9 |
  | back | 44.7 | 24.5 | 4.6 | 9.5 | 6.2 |
- **Tris 10,688.**

## FINAL 8.5 (2026-10-28, after `_review/CinderOverlord_final85.md`, FIX model 7) - EXPORTED
The single gate file is `_scratch/gate_f85.json`. `gate_r6.json` and `gold_windows_r6.txt` are renamed `STALE_f85_*`.
Backup of the r6 export: `_scratch/CinderOverlord_exported_r6.py`. Colours are unchanged (rulings A/B, body not lifted).
- **M1, mass, not a worm:**
  - `RAD` = 0.297 / 0.308 / 0.280 / 0.252 / 0.200 (+12 %); `FRAD` +5 % (0.282 ... 0.189). The chest base sits on the
    thicker body (FRONT[0] z 0.254 -> 0.285).
  - The Body3, Tail1 and Tail3 rings are dropped, so every second ring is gone from Body2 to Tail4. The Spine, Body1
    and neck rings stay.
  - The rest are narrowed: body bands 0.62-0.80 (was 0.55-0.84), tail bands 0.66-0.76 (was 0.62-0.79).
  - The vents, dorsal spikes and scutes follow the radii. The vents move 4 deg up the flank (28 / 152, was 24 / 156),
    so the wider scutes (T1) do not cover their lower ends.
- **M2, head:**
  - The jaw-muscle bulges are cut to 60 % (0.035 x 0.069 x 0.053) and tucked under a new flat, tapered OBS_D cheek
    plate on each side. The plate is laid on the skull surface via `surf_hit`, from the jaw hinge to under the eye,
    and tapers to 55 % at the front.
  - **Head studs:** the stud skin is one object-space box projection with one global pitch (`bk.stud_skin`, pitch
    0.0482). The head studs therefore already have the same size as Body1's. The "bubble" look came from the tile
    stretching over the round jaw bulges; those are now covered by the flat plate (`renders/_close_sheet.png`, side).
- **M3, eyes:** socket 0.125 x 0.010 x 0.036, slit 0.110 x 0.010 x 0.020 (+30 %, deep blue). The pupil grows with the
  slit (0.0065 x 0.020, 0.003 proud). No glint, no round eye; the slits stay angled and set under the brow.
  - In the 64 px portrait icon the near eye reads as a clear blue slit. The far eye is behind the skull in this
    front-left 3/4 camera, so only one slit can show (`_scratch/icons_64x4.png`, 4x nearest-neighbour).
- **M4, clean crown:**
  - The mount ends are 0.22 (was 0.30) and dropped 0.02 behind the blades; the two side blocks are removed.
  - The "dark arms over the brows" in the r6 `close_front` were mostly the BROWS: their outer ends rose to the crown
    line from the front. The brows are now shorter and less rolled (half-length 0.090, was 0.108; roll 16, was 22),
    and kept toward the nose so the forward point is unchanged.
  - From the front no dark arm reaches the crown now (`renders/close_front.png`).
- **M5, gold - ONE method (kit counter, `_tools/game_icon.py`, H 29-58, s > 0.5, v > 0.45):**
  - **portrait 32, game 24** at 64 px (r6: 26 / 20).
  - Added: a rounded gold tip nib on the centre blade (top 29 % of the blade, above the blue V) and a smaller one on
    blades 2 / 4 (top 22 %). The centre frames are deeper (half-depth t/2 + 0.022, was + 0.009); blades 2 / 4 are
    t/2 + 0.017. The frame widths are unchanged (wider frames touched in the molt).
  - Finding: in the kit portrait the lit flat gold faces clip to lemon (255,255,99) = H 60, outside the window (59
    such pixels at 64 px). A flat cap therefore added no counted pixels; the counted gold comes from the less-lit side
    faces, hence the deeper frames.
- **T1:** the pale scutes on Body1-4 wrap 8 deg further up each flank (180-360, was 188-352). Pale share: side 12.5 %,
  tq 12.9 %. From the top-down game camera it is still only 2.7 %, because the body lies on its belly.
- **T2:** Tail1-3 radii 0.168 / 0.135 / 0.103 (+25 %); Tail4 0.072 (was 0.060) to keep the taper smooth; tip 0.042.
- **T4:** blades 1 / 5 keep 0.020 frames, no nib and normal depth. The centre carries the most gold, then 2 / 4.
- **Shares (all figure pixels, flat renders, %):**

  | view | body | obsidian | pale | blue accent | gold |
  |---|---|---|---|---|---|
  | game | 45.0 | 28.6 | 2.7 | 7.8 | 6.1 |
  | side | 47.6 | 20.5 | 12.5 | 7.1 | 2.8 |
  | tq | 40.0 | 24.7 | 12.9 | 6.1 | 8.1 |
  | back | 43.8 | 27.2 | 4.7 | 8.2 | 6.3 |

  Body >= 40 and obsidian <= 40 in every view.
- **Tris 10,588.** Height 2.254 BU (10.5 studs).
- **Renders (2026-10-28):** `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64/128.png`,
  `_icons2_strip_64/128.png`, `gamelook_game.png` / `gamelook_tq.png`, `flat_*.png`.

## ROUND 6 (2026-10-27, lead rulings after `_review/CinderOverlord_review5.md`) - FINAL, EXPORTED
- **Ruling A, blue that copies no one:** the r5 accent (40,160,255) was 2.8 deg from Kraken's RING / EYE (40,150,255).
  - **Accent** (vent slits, eye slits, tail spike, crown inner lines) is now **(20, 92, 250)**: H 223, S 0.92, luma 88.
    The ruling said "about (24,104,255)", but that sits 2 deg / RGB 28 from ThunderRex DEEP (34,110,230). So I went a touch
    darker: 14 luma below Rex DEEP, and well below Kraken RING (luma ~126) and Leviathan AZURE (~143).
  - **Cores** (vent cores, tail tip, crown centre gem) are now near-white **(226, 240, 255)** (S 0.11): white-hot inside a
    deep blue rim. At that saturation they cannot hue-copy anyone.
  - Check: `_scratch/blue_cmp.png` puts the Cinder at 128 / 64 px next to Kraken, ThunderRex, CosmicLeviathan,
    InfernoPhoenix and Ivonrath. At 64 px the Cinder reads as an ember serpent with deep-blue / white vents and a gold
    crown. Kraken (red squid) and ThunderRex (blue armoured rex) are clearly separate.
- **Ruling B:** the cold-blue vent read is accepted; no warm centre.
- **Shares margin:** the obsidian rings are trimmed (body band 0.52-0.86 -> 0.55-0.84, tail 0.60-0.80 -> 0.62-0.79); the
  belly and crown are untouched. Game view: **body 41.9 %** (was 40.4), obsidian 33.6 %.
- **Gold (kit counter):** **portrait 26 (gate 25), game camera 20.**
  - The darker accent next to the gold cost one pixel, so the centre / middle gold frames widened 0.036 / 0.028 ->
    0.038 / 0.028.
  - 0.040 / 0.030 made the blade frames touch in the roar and molt. A 0.335 centre blade cut the portrait count to 24,
    because the taller pet frames smaller. Both were reverted.
- **ONE gate file: `_scratch/gate_r6.json`.** gate_r5 / r4 / 18:13 are all renamed `STALE_*`.
- **Re-rendered from the final model:** `renders/_model_sheet.png`, `close_front.png` (+ `_close_sheet.png`),
  `_icons_strip_64/128.png`, `_icons2_strip_64/128.png`, `gamelook_*.png`, `_molt_r4_front/side/tq.png`.
- **Step 1:** collision_free true, ground_min_z -0.006 in every clip, linear 0, loops 0 / 0. Tris 10,852, H 2.254 (meta height 10.5).
- **EXPORTED** `C:\cdimp\CinderOverlord.fbx` (+ `CinderOverlord.lua`, `_meta.json`, `_bu.json`, `_portrait_raw.png`, `_rigged.blend`).

## ROUND 5 (2026-10-27, after `_review/CinderOverlord_review4.md`, model REVISE 7/10)
- **MUST 1 + 2, accent and cores: SULFUR-BLUE (option S).** Comparison: `_scratch/accent_cmp.png`. It shows r4 A2 / W / S
  at 128 and 64 px next to InfernoPhoenix, Ivonrath and ThunderRex.
  - The ember body (166, 66, 50), the ash belly, the obsidian saddle and the gold crown are kept in both options.
  - **W, white-hot, rejected:**
    - Its core (255, 236, 160) is an exact copy of LavaGolem MAGMA_HOT, and within 1-2 deg of Ivonrath FLAME_HOT and
      BlackDragon EYE_HOT.
    - Its accent (255, 192, 32), H 43, sits on the house GOLD (H 43), Ivonrath FLAME (H 41) and Phoenix FLAME (H 47).
    - At 128 px the yellow vents read like the Phoenix's flame tips and merge with the crown. With the accent kept off
      the crown, the vents still read as the Phoenix's colours.
  - **S, sulfur-blue, picked:**
    - Accent / vent and eye slits / tail spike / crown inner lines **(40, 160, 255)**, H 207. Hot cores / tail tip /
      crown centre gem **(140, 220, 255)**, H 198.
    - Every Fire-egg colour sits at H 341-49 (Phoenix, Ivonrath, Cerberus, MoltenBoar, LavaGolem) or H 247-268
      (BlackDragon). The nearest is BlackDragon INK at H 247: 40 deg from the accent and 49 deg from the core. So both
      clear the 15 deg rule by a wide margin.
    - Blue is the complement of the orange body, so the hot points pop at 64 px. Blue sulfur flames are a real, rarer
      kind of volcanic fire, so the hot tone now belongs to the Cinder alone and reads as a higher tier than the
      Phoenix's orange.
    - Outside the Fire egg (disclosure): the core is 5 deg from ThunderRex CYAN (H 193), and the accent 10-13 deg from
      ThunderRex DEEP (H 217) / Leviathan AZURE (H 219). Different egg, different body colour and silhouette.
  - The crown's inner edge lines got their own variable `CROWN_IN`, set to the same blue. In the close-up
    (`renders/close_front.png`) the blue lines sit inside the gold frames without merging.
- **MUST 3, gold:**
  - The window the review specified (H 38-48, s >= 0.6, blends excluded) gives **7 px** on the portrait (1 with the
    no-blend neighbour rule). The same window gives ThunderRex 1 / 0, CosmicLeviathan 5 / 2 and InfernoPhoenix 8 / 0
    (`_scratch/gold_windows_r5.txt`). Rendered gold highlights sit at H 48-60, so that window cannot gate any pet.
  - The **kit counter (H 29-58) now reads 27 on the portrait and 19 on the game camera.** All 27 portrait pixels lie at
    H 38-58 (13 at 38-48, 14 at 48-58). **None** fall in the H 29-38 band where the r4 ember blends inflated the count:
    the crown's inner lines are blue now, so no gold-ember blend exists.
  - The crown blades grew ~6 % taller (centre 0.30 -> 0.32, middle 0.215 -> 0.23, outer 0.17 -> 0.18, same widths;
    wider blades touched in the molt) and the centre / middle gold widened to 0.036 / 0.028. That moved the kit count
    25 -> 27 (gate 25).
- **The ONE gate file is now `_scratch/gate_r5.json`** (`gate_r4.json` renamed `STALE_r4_gate_r4.json`):
  - gold (kit) portrait **27**, game 19;
  - game view: body **40.4 %**, obsidian **35.1 %**, sulfur accent 6.8, blue cores 3.5, gold 5.1 + 0.9;
  - side: body 47.7, obsidian 23.4, warm pale 10.8; tq: body 39.7, obsidian 26.8, pale 12.2.
  - The game body share fell from 42.4 because the taller crown and the blue points take more of the frame. It still
    passes >= 40.
- **MUST 4, renders**, all re-made from the current model (22:53): `renders/_model_sheet.png`, `close_front.png` (+
  `_close_sheet.png`), `_icons_strip_64/128.png`, `_icons2_strip_64/128.png`, `_molt_r4_front/side/tq.png`,
  `gamelook_*.png`.
- **Step 1 (`_scratch/clipgate_r5.txt`):** collision_free **true**, ground_min_z -0.006 in every clip, linear 0, loops
  0 / 0. Tris 10,852, H 2.254.

## ROUND 4 (2026-10-27, after `_review/CinderOverlord_review3.md`, REVISE 7/10)
- **MUST 5 + lead hue ruling (2026-10-27): EMBER.** The wine body (160, 87, 102) read as a pink worm, so the hue moved to
  fire. Comparison: `_scratch/hue_cmp.png`. It shows rows r4-now / A / B / A2 / B2 at 128 and 64 px next to Ivonrath,
  InfernoPhoenix and ThunderRex. The brief's "Fire-egg Rex" is ThunderRex, the only Rex built.
  - A = ember body (166, 66, 50); B = oxblood (160, 50, 56). Both have the warm ash belly (222, 194, 158).
  - With the old ROSE accent (255, 96, 150), **A and B still showed pink at 64 px**: the vent slits, eye slits and crown
    inner edges. So I added A2 / B2 with the accent turned to a hot ember (255, 84, 48).
  - **Pick: A2.**
    - It reads FIRE at 64 px: an ember / cinder body with hot orange-red slits around the lava cores.
    - It has no pink left anywhere.
    - It is clearly apart from Ivonrath's crimson: A2 leans orange, while B / B2 sit right on Ivonrath's red.
  - **Applied:** PLUM_OBS **(166, 66, 50)**, PALE_S **(222, 194, 158)**, ROSE (the accent) **(255, 84, 48)**.
  - **Kept:** OBS_D (62, 50, 64) saddle and rings, LAVA cores, GOLD / GOLD_D crown.
  - The rig has one body tone (PLUM_OBS), so there was no separate shadow tone to shift.
- **MUST 4, one set of numbers:** `_scratch/gate_r4.json` is the ONLY gate-number file. It was re-written after the ember run.
  The 18:13 files were renamed `_scratch/STALE_1813_*`; gate_clip_out.txt was an even older round-2 run (tris 11,124, gold
  25 / 19). From gate_r4.json:
  - **Gold at 64 px** (kit counter `_tools/game_icon.py`): **portrait 35, game 20.**
    - The portrait rose from 27 because the crown's inner edges are now ember, not rose. The counter's hue window
      (29-58 deg) catches the gold / ember edge blend: 32 of the 35 pixels are in the crown rows, 3 on the body.
  - **Shares**, flat_game.png, every figure pixel to the nearest palette colour: **body PLUM_OBS 42.4 %, obsidian OBS_D
    34.1 %** (targets >= 40 / <= 40); ember accent 6.8, lava 2.8.
  - Side: body 48.9, obsidian 22.5, warm pale **10.3**. Tq: body 41.4, obsidian 25.8, pale **11.6** (the pale band keeps its
    share).
- **Step 1 after the hue change** (`_scratch/clipgate_r4.txt`): collision_free true, ground_min_z -0.006, linear 0, loops 0 / 0.
- Model unchanged otherwise: tris 10,852, H 2.232. Renders: `renders/_model_sheet.png`, `_icons_strip_64.png` /
  `_128.png`, `_icons2_strip_*`, `gamelook_*.png`.

## ROUND 3 (2026-10-27, after `_review/CinderOverlord_review2.md`, REVISE 6/10) - every MUST + NICE 1/3 applied
- **MUST 1** obsidian cap arc 65-115 deg (was 55), rose slits 0.018 proud + pupils 0.023: the eyes read from the front.
- **MUST 2** V muzzle: the last skull stations (0.96: 0.070 x 0.048) and (1.0: 0.055 x 0.040).
- **MUST 3** dorsal saddle 9 deg (body) / 8 deg (tail), neck saddle dropped: **game PLUM_OBS 43.2 % / OBS_D 37.8 %**.
- **MUST 4** RAD[1..3] 0.275 / 0.250 / 0.225 (round 2: 0.250 / 0.230 / 0.205).
- **MUST 5** vent hot cores w x 0.50 in LAVA (255,128,24); the crown centre gem is LAVA; ROSE_H retired.
- NICE 1 outer-blade gold 0.020; NICE 3 the centre blade gold on its sides too (0.034) and 0.30 tall. Gold at 64:
  portrait 27 px, game 20. NICE 2 (Ivonrath hue) unchanged - S 0.44 kept; the 128 px strip is in the evidence.
- Evidence: `renders/model_front.png`, `renders/_icons_strip_64.png` / `_128.png`, `renders/gamelook_*.png`,
  `_scratch/shares_strict.json`, `_scratch/game_icon.json`. Clips: see `CLIP_NOTES.md`.

## ROUND 2 (2026-10-27, after `_review/CinderOverlord_review1.md`, REVISE 5/10) - every MUST + NICE applied

Numbers now: **11,124 tris**; H_MODEL 2.210 BU (the crown blades grew 12 %), HEIGHT 10.5 studs (unchanged), stud pitch
0.0472. Gold at 64 px: **portrait 28** (kit counter; brief counter 50), **game camera 19** (r1 16). Gate >= 25: PASS.
Crown + neck pose test (`pose_try`, 8 poses: alternating lifts A/B, all blades 35 deg up, all 35 deg forward, neck bow +
blades, look yaw, look-up + blades): **0 collisions in every pose**, ground_min_z -0.006 (Tail3, at rest).
Sheet: `renders/_pose_crown_sheet.png` (rest / all up / all forward / bow / look-up).

Strict value shares (`PermafrostTitan/_scratch/shares.py`: background AND anti-aliased edge / speckle pixels excluded):

| colour | side | tq | game | plan / review target |
|---|---|---|---|---|
| PLUM_OBS (body) | 45.9 | 39.6 | 28.0 | 44 |
| OBS_D (obsidian) | 30.0 | 31.6 | 53.5 | 16 (review: "deeper obsidian-dominant" fallback, see M1) |
| PALE_S | 7.7 (+ IVORY-matched shade 1.9) | 9.5 (+2.0) | **0.6** | 10 / game >= 4 (see M7) |
| ROSE + ROSE_H | 6.6 | 5.6 | 7.0 | ~6 (review ruling) |
| LAVA | 1.7 | 1.1 | 1.1 | < 2 |
| GOLD + GOLD_D | 2.2 | 6.5 | 5.4 | 3 |

| # | item | done |
|---|---|---|
| M1 | body off the Leviathan magenta | PLUM_OBS first set to the review's (150,84,110); the 64 px portrait **still read pink**, so per the review's own fallback ("deeper obsidian-dominant, not lighter") it went to **(144,80,96)** (H 345 oxblood, S 0.44, luma 101 >= 95; 45 deg off the Leviathan's H 300) AND an **obsidian dorsal saddle** (OBS_D band over the top of every body/tail segment and the back of the neck, rings drop from it down the flanks) + an **obsidian skull cap** brow-to-crown. Game view is now dark obsidian back + wine flanks + lava vents. |
| M2 | crown not a tiara | gold only on the two upper edges of every blade + the two sides of the centre blade (outer side frames on blades 1/2/4/5 gone). To hold the >= 25 px gate the remaining gold edges are wider (half 0.016 -> 0.025) and the blades 12 % taller (0.17 / 0.215 / 0.28); rose inner lines moved in (0.66) so the wider gold does not cover them. |
| M3 | Fire read | `LAVA = (255,128,24)`: the hot core line of all 24 vent slits + the tail ember tip. ROSE_H stays only on the centre crown gem. |
| M4 | rose ~6 % | slits `w = 0.060*sc + 0.014`, `L = 0.22*sc + 0.04` exactly as ruled; the pair spacing now scales with the slit width (gap ~0.25 w) so the doubled slits stay two slits; raised to 24 deg on the flank (clear of the wider pale band). No stripes. Rose 6.6 % side / 7.0 % game. |
| M5 | head not a brick | the literal numbers (front half-size 0.115, rnd 0.50) would not have changed the read: blockkit caps rounding at 0.45 x the smallest half-size, so the box only got smaller. The skull is now a **lofted wedge** (8 superellipse stations, n 2.8): widest at the cheeks (0.40 wide), tapering + dropping to a **squared muzzle** (side view = a crocodile / dragon wedge). Jaw lofted too (tapers with the snout), jaw-muscle boxes -> smooth ellipsoid bulges, the boxy OBS_D cheek plates removed, nostrils sit on top of the muzzle (no pig-snout read from the front). Close-ups: `renders/_close_sheet.png`. |
| M6 | bulk | `RAD[0..4] = 0.265, 0.250, 0.230, 0.205, 0.180` (+15 %), tail radii unchanged; the rearing neck thickened with it (`FRAD` +~10 %: 0.268 ... 0.180) and the forearms moved out/forward with the thicker chest. Vents, rings, scutes, spikes follow the radii. |
| M7 | pale underside in game | arc widened to **188-352 deg** on Spine..Body4 (200-340 on Tail1), `PALE_S = (245,236,240)`. Side 7.7 %, tq 9.5 %, **game 0.6 %**. The game camera sits behind and ~38 deg above a serpent lying on its belly: geometrically it only sees the lower flank down to ~-27 deg on the side facing it and nothing below the equator on the other side. Reaching 4 % in game would need the pale band at/above the equator on both flanks (a pale lateral stripe, which would also run into the vents = candy stripes). I stopped at 188-352 and ask the reviewer to judge the 3-band read from `gamelook_game.png` (dark back / wine flanks / lava vents / gold crown) instead of a game pale share. |
| M8 | BlackDragon in the strips | BlackDragon is first after the Cinder in `_icons_strip_64/128.png` and `_icons2_strip_64/128.png` (then Boar, Golem, Cerberus, Ivonrath, Phoenix, Rex, Leviathan). |
| N1 | tail rings | Tail1-4 ring band 0.60-0.80 (body keeps 0.52-0.86). |
| N2 | beams | nasal ridge now a thin 0.02-wide OBS_D ridge on the muzzle tip only; the crown mount is two tapered halves (0.068 high at the centre -> 0.04 at the ends), side blocks smaller. |
| N3 | brow points | each brow has an OBS_D forward point at its inner-front end (angry V). |
| N4 | eye slits | rose slit 0.074 -> 0.085, socket 0.088 -> 0.098. |
| N5 | molt check | done above: 35 deg lifts at the fatter body = 0 collisions. |

Deliverables: `renders/_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64/128.png`, `_icons2_strip_64/128.png`,
`flat_side/tq/game.png`, `gamelook_game.png`, `gamelook_tq.png`, `_pose_crown_sheet.png`; numbers in
`_scratch/shares_strict.json`, `_scratch/game_icon.json`, `_scratch/model_result.txt`.

---- (round 1 notes below, kept for history) ----

## Numbers (round 1)
- Tris: **10,896** (cap 15k).
- HEIGHT 10.5 studs = crown tip of the rearing head; H_MODEL 2.177 BU (measured); stud pitch 0.0465.
- Footprint 3.56 x 0.93 BU (17 x 4.5 studs at x1): the rear third lies on the ground in a lateral S.
- Gold px in the 64 px portrait icon: **39** (brief counter 52); game camera 16. Plan gate >= 25.

## What I built
- Cobra posture: chest on the ground, the front rising in an S (Spine curve -> Neck1..3) to a level wedge head; the rear (Body1-4,
  Tail1-4) lies in a lateral S down to a thin tail with a rose / rose-hot ember spike.
- Smooth lofted body segments (superellipse tubes, studded), **banded-krait obsidian rings** wrapping the back and flanks (one per
  segment), stacked pale ventral scute plates (the rising throat shows a scute "ladder"), small obsidian dorsal spikes on the rings
  shrinking to the tail, **6 pairs of rose lava vents** (double slanted slits with rose-hot centres) on the flanks.
- Two small clawed forearms held at the chest (3 black claws each).
- Head (built at 1.0, shown x1.2 about the throat): wedge skull, obsidian nasal ridge, heavy jaw (6 deg open) with pale underside,
  dark mouth, 2 long upper ivory fangs + 2 lower, **wedge rose slit eyes** (thin black pupils, no glint) under heavy obsidian V
  brows, 3 swept obsidian cheek spikes per side, nostril pits on top of the snout.
- **Hero crown:** an obsidian crown mount (the plan's "crown base", studded) carrying **five smooth obsidian blades** (0.25 / 0.19
  / 0.15 BU = 0.115H / 0.087H / 0.069H), each framed in house GOLD along its four upper / side edges, rose inner edge lines, a
  rose-hot tip on the centre blade. The blades stand side by side with no overlap (tops fanned 0 / 12 / 24 deg), each on its own
  bone `Crown_1..5`, so the molt act can lift them one by one: **lift tests (alternating, all at 35 deg, + neck bow) = 0 collisions**.

## Palette and value shares (flat renders, %)
| Name | RGB | side | tq | game | plan (side) |
|---|---|---|---|---|---|
| PLUM_OBS | 160,90,136 | 56.6 | 47.0 | 51.7 | 44 |
| OBS_D | 62,50,64 | 24.7 | 26.6 | 32.7 | 16 |
| PALE_S | 226,210,214 | 6.4 | 10.6 | 0.7 | 10 |
| ROSE | 255,96,150 | 3.6 | 3.4 | 3.7 | 8 |
| ROSE_H | 255,190,214 | 1.6 | 1.1 | 1.3 | 2 |
| GOLD | 255,196,50 | 2.3 | 5.8 | 4.4 | 3 |
| GOLD_D | 214,150,30 | 0.4 | 1.1 | 1.2 | - |
| BLACK | 14,14,22 | 3.7 | 3.5 | 3.5 | 3 |
| IVORY / MOUTH | | 0.3 / 0.3 | 0.3 / 0.6 | 0 / 0.7 | 1 / 1 |

## Deviations from the plan (and why)
1. **Colours:** PLUM_OBS (182,132,172) -> (160,90,136) (H 318, S 0.44): the plan value read candy-pink next to the dark Fire pets
   in the strip; H 318 also keeps it away from the Cosmic Leviathan's H 300 magenta hide. OBS_D (96,84,96) -> (62,50,64) so the
   obsidian reads as obsidian. In game the body is about (96,54,82), a dark plum.
2. **Obsidian as rings** (wrapping back + flanks) rather than plates on the top only: the per-segment top plates read as a
   caterpillar; rings give the banded serpent read and the 3-band blocking.
3. **Gold frames on all four upper / side edges** of each blade (plan: a thin band on the top edge only): the top edges alone gave
   well under 25 gold px at 64 px.
4. **Crown mount + spacing:** the plates were first fanned and overlapping; every per-plate lift collided, so they now stand on
   an obsidian mount side by side.
5. **Head x1.2** (HEAD_XF scale about the throat) and **cheek spikes** (not in the plan): the first head read small on the long
   neck ("goose").
6. **Vents** are double slits (single slits did not read). ROSE is 3.4-3.7 % (+ROSE_H) vs plan 8 %: the vents are flush slits;
   reaching 8 % would need wider lava stripes, which I held back to keep the obsidian / plum read. Easy to raise if wanted.
7. Forearms sit on Neck1 (held at the chest, z 0.58-0.76) so they read as arms, not front feet.

## Rig
Spine (chest base on the ground) -> Body1..4 -> Tail1..4 (+ `Tail_Tip` anchor at the ember), Neck1..3 -> Head (throat pivot) ->
Jaw (+ `Mouth` anchor), `Crown_1..5` (own bones), Arm_L/R -> Claw_L/R (the hands), `Vent_1..6` anchors (at the left vent of each
pair, on its segment bone; mirror x for the right vent). MOTION "Walk" (the walk clip will be the slither), RIG "serpent".
VFX anchors: Crown_1..5 (ember sparks), Vent_1..6 (smoke), Mouth (ember puff), Tail_Tip (ember), Claw_L/R (paddle sparks).

## Evidence
`renders/_model_sheet.png`, `renders/_close_sheet.png` (head + crown), `renders/_icons_strip_64.png` / `_128.png`,
`renders/_icons2_strip_64.png` / `_128.png` (portrait + game-camera icon + MoltenBoar, LavaGolem, Cerberus, Ivonrath,
InfernoPhoenix, ThunderRex, CosmicLeviathan), `renders/gamelook_*.png`.
