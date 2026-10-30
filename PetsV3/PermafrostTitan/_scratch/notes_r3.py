import io
T = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan"


def ins(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    io.open(path, "w", encoding="utf-8").write(s[:i] + text + s[i:])


MODEL = """## FINAL 8.5 ROUND 3 (2026-10-28, after `_review/PermafrostTitan_final85_r3.md`, model 8.0) - re-exported 04:21
Backup of the round-2 export: `_scratch/PermafrostTitan_exported_r2.py`.
- **M1, knee:** the shin starts exactly at the thigh's knee width (`SW, SD = TW * TT, TD * TT`, no +0.006 calf). The knee
  cap centre is at `-(SD - 0.012)`, so it sits 0.008 proud.
- **M2, belt:** the JOINT_D belt is now a seam, half-height **0.02** (was 0.04); width 0.262 and depth 0.19 are unchanged.
- **Gold at 64 px, measured with both tools on the same icons (`_scratch/gold_windows_r3.txt`):**

  | tool / window | portrait | game |
  |---|---|---|
  | kit counter (`_tools/game_icon.py`) | **52** | **27** |
  | `gold_cmp.py`, kit window H 29-58 | 54 | 27 |
  | `gold_cmp.py`, rendered window H 40-62, s >= 0.6, v >= 0.55 | **47** | **20** |
- **Shares (all figure pixels, %):**

  | view | MAUVE | PLUM | ICE_W | JOINT_D |
  |---|---|---|---|---|
  | side | 60.6 | 12.1 | 14.6 | 7.8 |
  | tq | 58.7 | 13.8 | 12.1 | 7.6 |
  | game | 57.0 | 16.7 | 15.2 | 7.1 |
  | back | 60.7 | 17.0 | 11.5 | 7.1 |
- **Tris 7,664.**
- **Renders (title bars carry the render time, 2026-10-28 04:20):** `_model_sheet.png` plus the icon strips,
  `gamelook_*` and `flat_*` re-made.

"""

CLIP = """## FINAL 8.5 ROUND 3 (2026-10-28, after `_review/PermafrostTitan_final85_r3.md`, clips 7.5) - re-exported 04:21
- **M3, left fist on the thigh: partly met.**
  - The review's values (out 6, fwd 22, bend 60) lift the fist to z 1.04, above the chest line (z 0.83), and 0.45 from
    the thigh.
  - I swept the pose with `_scratch/fist_probe.py` (fist-to-thigh surface distance) and `collide_where`
    (forearm-to-thigh). Every pose that brings the fist within ~0.05 of the thigh also cuts the thick forearm/bracer
    into the thigh top (Fore_L|Leg_L, 22-92 tri pairs).
  - The closest collision-free hold is **(out -11, fwd 14, bend 14)** at f30-46: the fist is **0.094** from the thigh
    surface, fist centre z 0.51, below the chest line. The f18 approach is (-4, 12, 24). The arm comes off the thigh
    f46-53 (4, 8, 24), before the f50-58 lean, and f62 (5, 4, 14) is kept.
  - In `renders/_kneel_2x_f40_f50.png` (tq) the fist rests in front of the thigh top.
  - The comment in the code now matches what is built.
- **M4, game-camera L-shape: both levers used.**
  - The Spine roll in the hold is **9** (was 7). The Head counter-roll is -5.5 (was -3.5), so the head stays level; the
    Chest stays -3.5, so chest vs spine is unchanged.
  - The kneeling foot's back sole sits **+0.02** higher in the hold (the ankle target 0.135 -> 0.155, f15-52).
  - The thinner knee cap needed the pelvis drop at **0.318** (was 0.312) to keep the knee on the snow. Ground probe:
    the LEFT knee is the lowest part from f18 to f52, at **-0.003 to -0.014** (the f20 settle).
  - `renders/_kneel_2x_f40_f50.png` (game f40 / f50 at 2x): the thigh drops from the hip, the shin lies back, the sole
    shows.
- **M5, idle shoulders.** The arms swing **±2.5 deg fwd/back with opposite signs** on the hip-yaw sine (the left arm
  back when the hips turn left).
  - I put it on the forward/back swing, not the vertical-axis slot: a hanging arm turned about the vertical only spins
    about its own length, so neither the fist nor the pauldron moves.
  - Chest vs spine is unchanged by it (the Arm bones).
- **Polish:**
  - Walk arm swing **5.5 deg** (was 4).
  - Idle breath pitch **1.8** (was 2.0); the head counter-pitch is 1.8.
  - Knee settle **0.005** (was 0.008).
- **Chest vs spine, measured (`ang_probe` on the Chest bone):**

  | clip | chest vs spine | head |
  |---|---|---|
  | idle | **4.85** | 2.3 |
  | walk | 2.5 | |
  | roar | 3.0 | 15 |
  | act | 4.68 | 14.1 |

  The idle is 4.85 because the yaw counter (4.5) stacks on the 1.8 breath, not the review's estimate of 4.6.
- **Step 1** (`_scratch/export_r3.txt`):
  - collision_free **true**. ground_min_z 0.000 for idle / walk / roar and **-0.014** for the act at f20.
  - Linear 0; loops 0 / 0; walk slide 0.0; idle foot drift 0. Tris 7,664. Events are unchanged; the anchor is `Knee_L`.
- **Fresh render set (title bars: rendered 2026-10-28 04:20):**
  - `_kneel_2x_f40_f50.png` (tq + game at f40 / f50, 700 px).
  - `_beats2x_idle.png`, `_beats2x_roar.png`, `_beats2x_kneel.png`.
  - `_walk_sheet.png` (tq + side, f0-42).
  - `_roar_jaw_close.png` (front + tq at f0 / f27; the dark mouth gap shows at f27).
  - `_kneel_views.png`, `_model_sheet.png`, and `_pose_tq_sheet.png` (24 beats).

"""
ins(T + r"\MODEL_NOTES.md", "## FINAL 8.5 ROUND 2", MODEL)
ins(T + r"\CLIP_NOTES.md", "## FINAL 8.5 ROUND 2", CLIP)
print("ok")
