import io
T = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan"


def ins(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    io.open(path, "w", encoding="utf-8").write(s[:i] + text + s[i:])


MODEL = """## FINAL 8.5 ROUND 4 (2026-10-28, after `_review/PermafrostTitan_final85_r4.md`, model 8.3) - re-exported 05:11
Backup of the round-3 export: `_scratch/PermafrostTitan_exported_r3.py`; this export: `_scratch/PermafrostTitan_exported_r4.py`.
- **MM1, waist:** the waist block's bottom taper goes from 0.95 to **0.86**, so the waist narrows into the belt.
  - The belt seam is tucked to match: (0.262, 0.19) -> **(0.248, 0.178)** half-extents.
  - It now sits as a step between the waist base (0.225 x 0.163) and the hip top (0.27 x 0.21).
  - The hip plates (outer x 0.272, top z 1.005) stay flush below the seam (z 1.01-1.05).
  - `renders/_model_sheet.png` (05:05).
- **MC4, mouth:** the jaw cavity colour is now **(24, 26, 34)**, near-black and neutral; it was JOINT_D (52, 60, 84).
  - Measured in `renders/_roar_jaw_close.png`, front, f27: the cavity renders **(85, 88, 95)**.
  - The lit slate brow renders (133, 143, 170), so the cavity is about 38 % darker (luma 88 vs 143) and no longer blue.
  - The kit shader (roughness 0.42) lifts dark faces, so it reads as dark grey here; Studio's true colour will be darker.
- **Step 1** (`_scratch/export_r4.txt`):
  - collision_free **true**; ground_min_z 0 on idle / walk / roar and **-0.017** on the act (f20).
  - Linear 0; loops 0 / 0; slide 0.0; idle foot drift 0.
  - Tris **7,664**; Lua 32,186 bytes; stride 0.6452.
  - FBX `C:\\cdimp\\PermafrostTitan.fbx` (05:11).

"""

CLIP = """## FINAL 8.5 ROUND 4 (2026-10-28, after `_review/PermafrostTitan_final85_r4.md`, clips 7.7) - re-exported 05:11
Coordinator ruling: the neck limit applies only to Neck bones. The Titan has none, so it is held to head + neck <= 30.
Measured head peaks: roar 15, act 14.1.
- **MC1, kneeling shin:**
  - The left ankle hold moves from aL + (0, 0.34, 0.155) to **aL + (0, 0.365, 0.101)** (f18-52).
    The f15 key is (0, 0.32, 0.13) and the f62 key is (0, 0.24, 0.10).
  - The toe curl TL goes from 26 to 16 for the flatter shin.
  - The knee stays pinned (DROP 0.326) and touches down at **-0.005 to -0.017** through f18-52.
  - Shin_L at f40 (`_scratch/joints_r4_f40.txt`): knee (0.266, 0.065, 0.140), ankle (0.250, 0.385, 0.266).
    The shin rises **21.5 deg** above horizontal; with the round-3 ankle target it was 31.4, so it leans back **9.9 deg**.
    The thigh is 9.0 deg off vertical.
  - From the game camera (`renders/_kneel_2x_f40_f50.png`, zoom `_scratch/zoom_game_kneel_r4.png`) the vertical
    thigh and the foot block coming back toward the camera form the L.
- **MC2, idle arm sway:** +/-2.5 -> **+/-5** (`sway = 5.0 * sn(f, n)`, the shoulders turn with the hips).
  - The closest the left fist gets to the thigh in the idle is **0.068**.
  - Chest vs spine stays at 4.85 (limit 5). `renders/_beats2x_idle.png`.
- **MC3, walk arm swing:** 5.5 -> **9**. The closest the left fist gets to the thigh in the walk is **0.065**. `renders/_walk_sheet.png`.
- **Fist re-measure (the kneel's left fist, f30-46):** probe `_scratch/fist_probe.py`, output `_scratch/fist_r4.txt`.
  - What it measures: the BVH surface distance from every vertex weighted to Hand_L / Fist_L to the nearest Leg_L
    face. It is a true surface-to-surface gap, not a vertex-to-vertex distance.
  - Nearest surface gap fist-to-thigh: **0.092** (f30, f40, f46).
  - Fist centre to the nearest thigh surface: **0.372**.
  - Fist centre height **z 0.502**, well under the chest line (z 0.824).
  - The 0.019 / 0.294 in `_scratch/fist_r3.txt` came from the REJECTED round-3 trial pose (-17, 6, 21): out 6 / fwd 21 put
    the forearm into the thigh (Fore_L | Leg_L).
    The kept pose (-11, 14, 14) is collision-free.
  - The ~0.09 floor comes from the forearm and bracer thickness: closing the gap further puts the forearm into the thigh first.
- **Chest vs spine (max, deg):** idle 4.85, walk 2.5, roar 3.0, act 4.68 - all <= 5.
- **Step 1** (`_scratch/export_r4.txt`):
  - collision_free **true**; ground 0 / 0 / 0 / **-0.017** (act f20); linear 0; loops 0 / 0; slide 0.0.
  - Events: idle frost1 / core1 / frost2 / core2; roar core1 / glint / icedust / core2; act icecrack / core1 / core2.
- **Renders** (title bar = 2026-10-28 05:05, "final 8.5 round 4"):
  - `_kneel_2x_f40_f50` (tq + game), `_beats2x_idle` / `_roar` / `_kneel`, `_walk_sheet`, `_roar_jaw_close`.
  - `_kneel_views`, `_model_sheet`, and `_pose_tq_sheet` (05:11).

"""

ins(T + r"\MODEL_NOTES.md", "## FINAL 8.5 ROUND 3", MODEL)
ins(T + r"\CLIP_NOTES.md", "## FINAL 8.5 ROUND 3", CLIP)
print("ok")
