import io
T = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan"


def ins(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    io.open(path, "w", encoding="utf-8").write(s[:i] + text + s[i:])


MODEL = """## FINAL 8.5 ROUND 6 (2026-10-28, after `_review/PermafrostTitan_final85_r6.md`, model 8.4) - re-exported 09:17
Backups:
- the round-5 export: `_scratch/PermafrostTitan_exported_r5.py`
- this export: `_scratch/PermafrostTitan_exported_r6.py`
- **MD-A, stacked bands:** the chest/waist seam (Chest, z 1.165) goes JOINT_D -> **MAUVE**. Geometry and collisions are
  unchanged. From the front the chest and waist now read as one mass (`renders/_roar_front_sheet.png` f0, `_model_sheet`).
- **MD-B, fresh evidence from the current build:**
  - `_icons_strip_64` / `_128`, `_icons2_strip_64` / `_128` and `_close_sheet` are re-made (09:18). The crust plates
    show at 64 px.
  - Kit gold counter (`_tools/game_icon.py`): portrait **49**, game **27** (gate >= 25 / >= 20).
  - Stale sheets (`_clip_sheet_v1`, `_cv_kneel_*`, `_kneel_close_f40`, `_under_sheet`) moved to
    `_scratch/stale_r6_renders/`.
- **Step 1** (`_scratch/export_r6.txt`): collision_free **true**; tris 7,820; FBX `C:\\cdimp\\PermafrostTitan.fbx` 09:17.

"""

CLIP = """## FINAL 8.5 ROUND 6 (2026-10-28, after `_review/PermafrostTitan_final85_r6.md`: idle 8.0, walk 8.2, roar 8.1, act 7.9) - re-exported 09:17
- **ACT-1, kneel yaw (lead: up to 30 allowed):**
  - I tested 25 and 30 on the game camera (`_scratch/yaw_cmp_f40.png`, zoom `_scratch/yaw_cmp_zoom.png`; 18 / 25 / 30).
  - At 25 the shin still slants down toward the camera and half-reads as a step. At **30** the thigh comes straight down
    to the dark knee on the snow and the shin + foot lie flat to the side: a clear L. So **YAW_K = 30**.
  - Same pivot (the planted right ankle; right foot min z 0.0, no slide) and the same `leg_unyaw`.
  - Knee **-0.005 to -0.017** (f17-53); the act ends at rest (yaw 0 by f62).
  - Evidence: `renders/_kneel_2x_f40_f50.png` (game + tq), `_kneel_views.png`.
- **IDLE-1:** arm sway **5 -> 7**.
  - Fist cycle range **L 0.142, R 0.137** (>= 0.12 both). f0 -> f30: L 0.133, R 0.033.
  - Closest fist-to-thigh gap 0.067 / 0.066 (>= 0.04); no collision; idle foot drift 0.
- **WALK-1:** pelvis shift over the stance foot **0.022 -> 0.035** BU; chest roll **3.0 -> 3.5** deg.
  - Walk slide 0.0; closest fist-to-thigh gap 0.057; fist range 0.215.
- **ROAR-1, arm asymmetry: not a bug.**
  - At roar f27 the arm joints mirror exactly: Arm (+/-0.480, 0.116, 1.563), Fore (+/-0.787, 0.146, 1.239), Hand
    (+/-0.884, -0.168, 1.033), Fist (+/-0.878, -0.400, 1.052).
  - So the fists are at the same height and the out angles are equal. `arms_fk` converts the `-s * out` roll into armature
    axes through each bone's rest matrix, so the bone roll cannot skew it.
  - The tq camera's perspective (one arm toward the camera, one away) made it look uneven.
  - Front sheet f0 / f22 / f27 / f50: `renders/_roar_front_sheet.png` (symmetric).
- **MC4' mouth:** left for the Studio check (lead ruling: don't chase the kit luma).
- **Per clip:**

  | clip | chest vs spine (<= 5) | head max | ground | other |
  |---|---|---|---|---|
  | idle | 4.85 | 13.5 | 0.0 | foot drift 0; fist range 0.142 / 0.137 |
  | walk | **4.03** | 1.4 | 0.0 | slide 0.0 |
  | roar | 3.0 | 15.0 | 0.0 | arms symmetric |
  | act | 4.68 | 14.1 | -0.017 (f20) | yaw 30, ends at rest |

  Probes: `_scratch/ang_r6.txt`, `arm_r6.txt`, `clipgate_r6.txt`.
- **Step 1** (`_scratch/export_r6.txt`): collision_free **true**; linear 0; loops 0 / 0; tris 7,820.
- **Renders** (title bars 09:18, "final 8.5 round 6"):
  - `_kneel_2x_f40_f50` (game + tq), `_kneel_views`, `_beats2x_idle` / `_roar` / `_kneel`.
  - `_walk_sheet` (tq + game + side), `_roar_front_sheet` (front) + `_beats2x_roar` (tq), `_roar_jaw_close`.
  - `_model_sheet`, `_close_sheet`, the two `_icons_strip` and two `_icons2_strip` sizes, `_pose_tq_sheet`.

"""
ins(T + r"\MODEL_NOTES.md", "## FINAL 8.5 ROUND 5", MODEL)
ins(T + r"\CLIP_NOTES.md", "## FINAL 8.5 ROUND 5", CLIP)
print("ok")
