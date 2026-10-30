# Inferno Phoenix v1 - builder report for the MODEL GATE (2026-10-14)

Spec: `pets/InfernoPhoenix.py` (model + rig + check_pairs + joints + FOLD/LIFT constants + a v0 idle STUB that only
holds the fold, so headless_pack measures at idle f0). Clips come after this gate (brief section 7).
Backup of the first build: `_tools/rex_versions/InfernoPhoenix_v1a.py`.

## Numbers
- tris **11,604** (budget 12k); size 2.97 x 2.47 x 2.07 (bind)
- H_MODEL: C crest anchor **2.034** (block top 2.040) at bind AND idle f0; the crest is the model top in both
- lowest at rest: talons -0.026 (bind), **-0.012 at idle f0** (FOOT_LIFT 0.014)
- idle f0 `collision_free: true` (all check_pairs + joints)

## Checklist evidence (brief section 9)
| item | evidence | builder verdict |
|---|---|---|
| 1 side silhouette | `_model_sheet_600.png`, `_fold_sheet_600.png` | built to 4.1/4.2 numbers; neck kept at the brief's hw 0.15/0.13 |
| 2 front | `_fold_sheet_600.png` front, `_flat_sheet.png` | PALE tongue now reads as ONE upward flame (see deviation D4) |
| 3 game camera | `_fold_sheet_600.png` game | cape changed (D5) |
| 4 icon strip (12 cmps) | `_icons_strip_64.png`, `_icons_strip_128.png` | |
| 5 A/B | `_AB_Thunderbird_64/128.png`, `_AB_Ivonrath_64/128.png` | |
| 6 shares | `_shares.txt` (table below) | misses listed below |
| 7 face close (700 px, bind) | `_face_close.png` (front / side / tq) | |
| 8 crest | 5 plumes, 4 stepped blocks, +11 deg back-curl each | lengths D2 |
| 9 wings + fold | fold_search table below; tongues same-sign per wing | FOLD D1 |
| 10 streamers | vane 0.376 x 0.10 = **3.8 : 1**, diamond section, collinear tongue; shafts hw 0.045 | roots D6 |
| 12 hard rules | no Neon/glow; 11.6k tris; HEIGHT 10; PITCH formula; no os.environ | |
| 13 rig limits | `_limits_sheet.png` (6 poses x tq/side/game) - **0 hits all 6**; `path_test` **0 hits all 10 paths** | D7-D9 |

### fold_search (FOLD_TAIL = C vane start 1.12, 0.135) - top 5 meeting ALL acceptance numbers
| up, fwd, twist, tip | hits | w90 | wing min z | wingtip -> vane | tip (y, z) |
|---|---|---|---|---|---|
| **86, 6, -80, 10 (chosen)** | 0 | **0.349** | **0.332** | **0.392** | 1.216, 0.515 |
| 86, 10, -80, 10 | 0 | 0.401 | 0.332 | 0.390 | 1.206, 0.515 |
| 83, 6, -80, 10 | 0 | 0.395 | 0.356 | 0.421 | 1.223, 0.543 |
| 83, 10, -80, 10 | 0 | 0.454 | 0.356 | 0.417 | 1.208, 0.543 |
| 86, 6, -84, 0 | 0 | 0.376 | 0.323 | 0.442 | 1.267, 0.552 |
The brief grid (twist -90) only gave min z 0.21-0.29; twist -80 + tip +10 gives both min z >= 0.30 and tip->vane <= 0.45.
Primaries end above the streamers (tip z 0.515 over the vane z 0.135-0.20).

### path_test (bezier keys, every frame, wing pairs + Chest/Spine): **0 hits on all 10**
1 fold->open (f0 F, 3 L1, 6 L2, 8 L3, 9 L4, 10 OPEN 30,0,0,0) · 2 flight bottom (-40,-2,0,8)->BRAKE (24,16,-10,-4)
->L4..L1->F (land timing) · 3 raised-V loop with 2 beats · 4 BREATH loop · 5 2-frame takeoff to LAUNCH (-34,8,6,4) ·
6 stoop 1-frame OPEN->L4..L1->F->L1..L3->V · 7 F<->L1 · 8 V->L3..L1->F · 9 the act path (section 7.7 frames: ... PYRE
(-60,-22,10,-6) f26-50 ... BOT (-38,8,6,4) x2 ... BRAKE ... F f92) · 10 the roar path (F, L1 f5, L2 f10, BREATH f16-46,
L1 f52, F f56).

### Limit poses (`_limits_sheet.png`; step 1, all check_pairs + joints; ground poses with feet planted)
| pose | keys | hits | lowest |
|---|---|---|---|
| L1 FOLD | 86,6,-80,10 | 0 | -0.012 |
| L2 look-back 44 | Neck 8 / Neck2 12 / Head 24 yaw | 0 | -0.012 |
| L3 pyre bow | wings PYRE, **Spine z -0.05** (D7) / pitch +9, Neck 12, Neck2 12, Head 20, Crest -10, X1 -4 X2 -4 X3 -2 | 0 | -0.012 |
| L4 roar train peak | wings BREATH, Spine -4, Crest +14, X1 +56 / X2 +24 / X3 -14 | 0 | -0.012 |
| L5 streamer drop | the act's RISING frame: z +0.46, pitch -4, wings OPEN, X1 -24 / X2 -6 / X3 +4, legs (50, roll -15, -30, 66) (D8) | 0 | +0.096 (vane) |
| L6 fly downstroke bottom | wings (-40,-2,0,8), Spine +45, Neck -8 Neck2 -8 Head -28, Crest -6, wave extreme X1 -27 X2 -9 X3 -13, fan L -8 / R +8, legs **THI 60 roll -18** SHI -40 FOO 70 (D9) | 0 | (air) |
(The wave's other extreme X1 -17 / X2 +9 / X3 +13 is also 0 hits with these legs.)

## Shares (flat palette-ID, idle f0) vs the section 3 targets
| view | BASALT+D | EMBER | PALE | FIRE | GOLD | BLACK+MOUTH (anti-alias edges) |
|---|---|---|---|---|---|---|
| side | 44.2 (32-42) **+2** | 23.9 (16-24) ok | **1.7 (5-10)** | 22.5 (14-22) +0.5 | 3.0 ok | 4.7 |
| tq | 35.4 (26-36) ok | **33.4 (20-28)** | 5.8 (6-12) -0.2 | 14.7 ok | 4.7 ok | 6.0 |
| game | 48.0 (38-48) ok | 23.2 (14-22) +1.2 | 1.3 (<=3) ok | 19.3 ok | 2.5 ok | 5.8 |
| front | 24.3 (18-30) ok | 40.2 (28-40) +0.2 | 12.0 (12-22) ok | 8.7 ok | 4.9 ok | 9.9 |
BASALT alone <= 35.2 everywhere (<= 40 ok); top role <= 40.2 (<= 45 ok).
- **Side PALE is structural:** the tongue lies on the forward-facing keel/breast, so the side camera sees it edge-on. I
  tried PALE cheeks (hidden by the cranium/face blocks: +0.1) and a PALE belly row on the lower body (hidden by the flank
  skirt: +0.1); both gave nothing, cheeks reverted, the belly row kept (harmless).
- **tq EMBER 33** is the neck column + breast side seen in 3/4. Fixable only by wrapping the BASALT cape further round
  the neck sides or a bigger tongue; I stopped here for your call.

## Deviations from the brief (please approve or overrule)
- **D1 FOLD = (86, 6, -80, 10)** (table above).
- **D2 crest lengths:** C 0.44 -> **0.52**, inner 0.37 -> **0.40** (outer 0.29). The brief's tip estimate (2.07) left out
  the 3 x 11 deg back-curl; at 0.44 the C tip was 1.982. 0.52 puts the anchor at 2.034, the model top in both poses.
- **D3 streamer vanes** narrowed to 3.8 : 1 (were ~1.85 : 1 in my first build; read as bird toes).
- **D4 the PALE tongue moved onto the KEEL front** (the keel bulge is the most forward mass and completely hid the
  chest-face shingles: front PALE was 1.0 %). Keel rows 1 / 2 / 3 / 4 PALE from the tip down (keel rebuilt bottom->top so
  face_shingles works on it), chest-face rows 3-4 + the centre column PALE (the broad base), and a 2-block PALE tip up
  the throat (Neck front, t 0.40-1.10, narrowing to a point) so it reads as ONE flame rising from the belly to the chin.
- **D5 cape / arm bar (EMBER shares, your section 3 fallback "raise BASALT on the neck back"):** the Neck2 cape is
  BASALT (the hood runs down the nape); the Neck cape is BASALT with its lowest row EMBER + the LAVA hem (a burning collar);
  the wing arm bar is EMBER only on its inner 22 % (a small shoulder ember), BASALT outward. Before: EMBER 26 / 39 / 27 /
  51 (side / tq / game / front).
- **D6 streamer roots x-separated:** L/R knuckles x 0.075 -> **0.095**, L/R start (0.10, 0.39, 0.51), all root shafts
  hw 0.05 -> **0.045** (= the 0.09 minimum). At 0.075 the C and L shafts overlapped in x near the roots, so ANY X1 pitch cut
  them (1-4 hits in the roar/pyre/drop poses). Each chain only pitches about its own knuckle, so x-separated roots can
  never cross. Knuckles clear by 0.005.
- **D7 pyre crouch:** with the feet planted, Spine z -0.13 drives the trouser tops deep into the lower body (Shin|Spine
  50/45 hits); -0.10 = 13/14, -0.08 = 5/6, **-0.05 = 0**. Proposal: the act's pyre uses z -0.05, pitch +9 and lets the
  wings + bow carry the "sinking". Also: streamers on the ground at rest only go to about X1 -5 (X1 -8 puts the vane at
  -0.053), so the pyre streamers use X1 -4 / X2 -4 / X3 -2.
- **D8 rising-frame legs:** the act's (50, -30, 66) swings the feet into the hanging side streamers (21/19 hits); a -15
  roll spread fixes it (also clean: thigh 30 / 20 with -10 / -6).
- **D9 fly tuck:** THI 76 (Thunderbird) swings the balled feet into the side streamer roots (40+ hits) and raises the
  talons above the tail line at the +45 body pitch; THI 60 with roll -18 is clean and reads tucked.

## Files (all in `InfernoPhoenix/renders/`)
`_model_sheet_600.png` (bind: tq / front / back / side / game) · `_model_tq_600.png` · `_fold_sheet_600.png` (idle f0) ·
`_face_close.png` (700 px front / side / tq, bind) · `_icons_strip_64.png` / `_128.png` (Phoenix + 12) ·
`_AB_Thunderbird_64/128.png` · `_AB_Ivonrath_64/128.png` · `_flat_sheet.png` · `_shares.txt` · `_limits_sheet.png`.
Tool changes: `_tools/pose_try.py` now takes `WINGS:up,fwd,twist,tip` tokens, `plant=1` (spec plant_frames) and reports
`lowz` per candidate; `_tools/fold_search.py` takes `FOLD_ALL=1` (dumps every row) and reports `minzy`.
