import io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan"


def insert_before(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    s = s[:i] + text + s[i:]
    io.open(path, "w", encoding="utf-8").write(s)


MODEL = """## FINAL 8.5 (2026-10-28, after `_review/PermafrostTitan_final85.md`, FIX model 7) - re-exported
Backup of the exported round-5 file: `_scratch/PermafrostTitan_exported1.py`.
- **MUST 1, colour:** MAUVE **(164,116,200)**, PLUM **(98,66,130)** exactly as specified (ICE_W, GOLD and JOINT_D unchanged).
  - **The in-game test is NOT met:** the `gamelook_game` body (0.6x colour preview, figure pixels in the body hue band) reads
    mean **(93,81,127)**, median (87,77,121), dominant 8-level bucket **(80,64,112)** against the target **(100,80,130)**.
    The review measured about (72,64,104) at the old colour, so the lift is about +8 to +21 per channel.
  - Tested a further lift to (184,130,224): mean (102,87,140), dominant bucket (88,72,128). That is still under the bucket
    target, and the body turns pastel pink-lilac (`_scratch/mauve_cmp.png`, `gamelook_mauve164/184.png`,
    `icon_mauve164/184.png`). I kept the specified RGB. The dark read is the preview's lighting more than the RGB; the
    lead may want to judge it in Studio.
- **MUST 2, limbs:** every limb segment now tapers toward the joint below it.
  - Thigh 0.182 x 0.194 with the far end at **0.72**; shin 0.156 x 0.164 at **0.74**; shin guard (0.86, 1.0).
  - Upper arm 0.134 x 0.144 at **0.80**; forearm 0.140 x 0.148 at **0.82**; bracer 0.160 x 0.168 at 0.80.
  - Deltoid rnd **0.55** (was 0.45).
  - From the front the hip block still covers the thigh tops, so the taper reads most from the side and 3/4
    (`renders/_model_sheet.png`, `_kneel_views.png`).
- **MUST 3, jaw:** the MOUTH lip is on bone **`Jaw`** at the hinge seam (0, -0.399, 1.727). A JOINT_D cavity
  (0, -0.335, 1.707), half (0.086, 0.040, 0.018), sits on `Head` behind it. The roar jaw opens 24 deg (was 16).
  `renders/_roar_jaw_close.png` shows a dark slate mouth gap at f27, front and 3/4.
- **TO 9+:**
  - (1) Chest ring R_OUT **0.272** (0.265 gave 44 px). Portrait gold **51 px** at 64 (kit counter, H 29-58; brief
    counter 78; was 37). Game camera **27** (brief counter 31).
  - (2) Skull **(0.160, 0.160, 0.135)**, raised 0.02 (the crown cap, cheeks, brow, eyes and face plate move with it).
    The eye sockets and slits are **15 % wider** (`ice_eye(wx=1.15)`).
  - (3) A blunt, flat-topped ICE_W chunk on each pauldron tip, about 0.18 tall: the chunks end in a flat `top`
    (0.86, 0.80), no points.
  - (4) Knuckle shards 0.058 -> **0.035** (lengths 0.060 / 0.072 / 0.060 at `top` 0.80 x 0.72). From the front they
    read as ice knuckles, not teeth.
  - (5) A smooth ICE_W belly band (0, -0.176, 1.098), half (0.20, 0.016, 0.036), under the ribcage.
  - (6) VFX: skipped (the coordinator adds particles in Studio).
- **Numbers:**
  - Tris **7,672**; Lua 32,186 B.
  - Shares, all figure pixels (flat renders):

    | view | MAUVE | PLUM | ICE_W |
    |---|---|---|---|
    | game | 54.7 | 16.8 | 15.0 |
    | side | 60.0 | 11.2 | 14.6 |
    | tq | 56.5 | 14.4 | 12.2 |
    | back | 59.4 | 16.4 | 11.3 |
- **Renders (all re-made 2026-10-28):** `_model_sheet.png`, `_close_sheet.png`, `_under_sheet.png` (clean; the only nit
  is a few thigh-top studs showing through the hip block in the 500 px low-back close-up), `_icons_strip_64/128.png`,
  `_icons2_strip_64/128.png`, `gamelook_game.png` / `gamelook_tq.png`, `flat_*.png`.

"""

CLIP = """## FINAL 8.5 (2026-10-28, after `_review/PermafrostTitan_final85.md`, FIX clips 6.5) - re-exported
- **MUST 3 (jaw):** see `MODEL_NOTES.md`. The lip rides `Jaw`, and a dark cavity sits behind it on `Head`. The roar jaw opens
  **24 deg** at f27 (12 at f22, 22 at f34, 20 at f50). `renders/_roar_jaw_close.png` shows the mouth gap.
- **MUST 4 (roar):**
  - The arms go out **22 deg** at f22 / f27 / f50 and **24** at f34; 10 at f58; -2 at f10 (anticipation kept). The
    elbows bend 0.6 x the out angle.
  - Head **-15**; Spine **-4**; Chest -3 local, which is **-7 in world** (chest vs spine **3 deg**). Head up in world =
    4 + 3 + 15 = **22 deg** (limit 30).
  - The largest step is the arms from -2 (f10) to 22 (f22): 2 deg per frame.
  - `renders/_beats2x_roar.png`: f0 vs f22 / f34 / f50 shows the arms clearly out, the forward push and the open mouth.
- **MUST 5 (idle):**
  - Chest breath **2 deg**; the body sinks **0.015** at the breath peak; hip yaw **+/-4 deg**.
  - The Head counter-pitches the breath (+2) and counter-yaws, so it stays level.
  - New: a slow **+/-8 deg fist flex** on `Hand_L` / `Hand_R`, 60-frame period, the left fist a quarter cycle ahead.
  - The feet stay planted. `renders/_beats2x_idle.png` (f0 / f30 / f60 / f90 at 2x) shows the fists and the torso change.
- **MUST 6 (kneel):**
  - `Foot_R` turns **10 deg outward** (yaw) from f18 to f50, eases back by f72, and is applied after the leg IK, so the
    knee stays on the snow (ground -0.009 at f20, unchanged).
  - The elbow bend in the hold is **30** (was 26), so the fists sit on the thighs.
  - **Disclosure on the 3/4 test:** the kit's tq camera sits on the pet's front-left, so the kneeling (right) leg is on
    the far side. At f40 the right knee cap shows on the snow behind the standing shin (`_scratch/knee40.png`, a posed
    close-up aimed at `Knee_R`), but the right sole faces back and stays hidden from the front 3/4.
  - The sole and the flat shin read clearly from the back and the game camera (`renders/_kneel_views.png` back / game
    f40). A clearer 3/4 read would mean mirroring the act (kneel on the left knee, on the camera side) and moving the
    `Knee_R` anchor; I did not do that without a ruling.
  - Fixed-camera act renders re-made: `renders/_cv_kneel_side.png`, `_cv_kneel_front.png`, `_cv_kneel_tq.png`
    (`cv_tq_act_kneelrise_40.png`), `kv_*_act_kneelrise_18/40/58.png`.
- **Step 1** (`_scratch/clipgate_f85.txt`, and the export run `_scratch/export_f85.txt`):
  - collision_free **true**. ground_min_z 0.000 for idle / walk / roar; **-0.009** for the act at f20.
  - Linear 0. Idle and walk loops 0 / 0. Walk slide 0.0, foot_z_var 0.0. Stride 0.645.
- **Clips and events are unchanged:**

  | clip | frames | loop |
  |---|---|---|
  | idle | 120 | yes |
  | walk | 48 | yes |
  | roar | 66 | no |
  | act_kneelrise | 100 | no |

  Events are as in the table below.
- **Renders re-made:** `_pose_tq_sheet.png` (24 beats), `_beats2x_idle/roar/kneel.png`, `_kneel_views.png`, the `_cv_kneel_*`
  sheets and `_roar_jaw_close.png`.
- **Export:** `C:\\cdimp\\PermafrostTitan.fbx` (2026-10-28 01:03, 1,067,868 B). The portrait raw is re-made.

"""

insert_before(D + r"\MODEL_NOTES.md", "## ROUND 5 (2026-10-27, review 4 NICE 4)", MODEL)
insert_before(D + r"\CLIP_NOTES.md", "## ROUND 5 (2026-10-27, after", CLIP)

p = D + r"\ANIM_REFS.md"
s = io.open(p, encoding="utf-8").read()
old_i = """- **idle (120 f loop): weight shift** (plan): hip yaw +/-3 deg over one cycle, slow breathing (chest 1 deg), the
  shoulders (pauldrons are on the Arm bones) settle 2 deg at f30 and f70, `core1` f40 / `core2` f100. No head tilt."""
new_i = """- **idle (120 f loop): weight shift** (plan; final-8.5 numbers): hip yaw +/-4 deg over one cycle, breathing (chest 2 deg,
  body sink 0.015), the shoulders (pauldrons are on the Arm bones) settle 2 deg at f30 and f70, a slow +/-8 deg fist
  flex (60 f), `core1` f40 / `core2` f100. No head tilt."""
old_r = """- **roar (66 f): core bellow (#3 + #9).** f0-10 anticipation: the head tucks 4 deg and the chest compresses; f10-22 the
  head lifts 10 deg, the arms go out 8 deg (9 at f34), `core1` f22 (+ `glint` f22 on the Hero bezel, `icedust` f24 on the fists);
  the jaw opens LATE (f20-26, #3); hold f22-50 with `core2` f34; f50-66 a slower settle back to rest (#9)."""
new_r = """- **roar (66 f): core bellow (#3 + #9; final-8.5 numbers).** f0-10 anticipation: the head tucks 4 deg and the chest
  compresses; f10-22 the body pushes forward (Spine -4, Chest -7 world), the head lifts 15 deg, the arms go out 22 deg
  (24 at f34), `core1` f22 (+ `glint` f22 on the Hero bezel, `icedust` f24 on the fists); the jaw opens LATE (24 deg at
  f27, #3); hold f22-50 with `core2` f34; f50-66 a slower settle back to rest (#9)."""
old_k = "  f50-58 the forward lean (K3, spine 10 deg + chest 4) then the front leg drives up (f58-76); f70-79 the left foot steps back;"
new_k = ("  the right foot turns 10 deg out in the hold and the elbows bend 30 (final 8.5);\n"
         "  f50-58 the forward lean (K3, spine 10 deg + chest 4) then the front leg drives up (f58-76); f70-79 the left foot steps back;")
assert s.count(old_i) == 1 and s.count(old_r) == 1 and s.count(old_k) == 1, (s.count(old_i), s.count(old_r), s.count(old_k))
s = s.replace(old_i, new_i).replace(old_r, new_r).replace(old_k, new_k)
io.open(p, "w", encoding="utf-8").write(s)
print("notes ok")
