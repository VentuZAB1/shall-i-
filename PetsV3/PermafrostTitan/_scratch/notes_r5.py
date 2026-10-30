import io
T = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan"


def ins(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    io.open(path, "w", encoding="utf-8").write(s[:i] + text + s[i:])


MODEL = """## FINAL 8.5 ROUND 5 (2026-10-28, after `_review/PermafrostTitan_final85_r5.md`, model 8.4) - re-exported 08:24
Backups:
- before this round: `_scratch/PermafrostTitan_pre_r5.py`
- this export: `_scratch/PermafrostTitan_exported_r5.py`

The patch is `_scratch/fix_r5.py`.
- **MD1, head:** skull half-width **0.160 -> 0.172**; the head is now 0.344 BU wide.
  - The face X offsets are scaled by `HX = 1.075`: brow halves (0.070), eye hits (0.078), cheeks (0.148), jaw half-width
    (0.120), cavity (0.086), lip (0.088).
  - Head pitch is unchanged; collision-free.
- **MD2, crusts -> two solid plates:**
  - Upper pauldron: 3 broken blocks -> **2 plates**: (L 0.17, w 0.080) and (L 0.13, w 0.076).
  - Fist knuckles: 3 -> **2 plates** (L 0.12, w 0.076, laid more forward over the knuckles).
  - `ice_chunk` half-sizes are (w, 0.8 w, L / 2), so the smallest half-size of every new plate is >= 0.06.
  - The lower pauldron keeps its single chunk at the round-4 size. Enlarging it pushed tris 64 over the +200 cap.
  - Tris: **7,820** (+156 vs 7,664; cap +200). The bigger plates cut more faces where they sink into the
    pauldron / fist, so two big plates cost more than three small ones (`_scratch/tris_by_bone.py`).
- **MC4', mouth (model part):** cavity **(10, 10, 14)** + an upper lip on the skull (MAUVE, 0.012 proud of the cavity front, hidden inside the closed jaw).
  - `renders/_roar_jaw_close.png` f27 front: the cavity renders **(79, 81, 84), luma ~81** (round 4: 88). The lit
    slate brow is luma 135.
  - The kit shader's sheen floor (roughness 0.42) keeps a dark face near luma 75-85. It cannot reach < 60 here, so per
    the review this item needs the Studio check.
- **Step 1** (`_scratch/export_r5.txt`): collision_free **true**; tris 7,820; FBX `C:\\cdimp\\PermafrostTitan.fbx` 08:24.

"""

CLIP = """## FINAL 8.5 ROUND 5 (2026-10-28, after `_review/PermafrostTitan_final85_r5.md`, clips 7.7: idle 7.6, walk 7.6, roar 8.0, act 7.5) - re-exported 08:24
Rulings applied: the fist on the knee is fine visually (the 0.03 centre test is dropped; the surface gap 0.092 stays
the logged number); no neck rule (no Neck bone; head + neck <= 30).
- **MC1', kneel from the game camera (lead ruling: body yaw, NOT another ankle tweak):**
  - The WHOLE body yaws **18 deg** toward the L side.
  - Timing: ease in f12-18, hold f18-52, ease out by f62. The act ends at exact rest.
  - Pivot: a vertical axis through the planted right ankle, so the right foot does not slide and keeps its heading.
  - Both foot targets rotate with the body, so the left knee stays pinned: lowest point **-0.005 to -0.017** through
    f17-53, the same as round 4.
  - Why it is on the Spine and not the Root bone: the kit exporter never exports Root (petkit `sample()` holds Root at
    identity), so the Spine - the top exported bone that carries the hips, legs and chest - carries the yaw. The Spine
    location gets the pivot term `(P - O) - Rz(P - O)`.
  - A fix that was needed: the kit leg IK aims each bone by the shortest arc, which is not yaw-equivariant. Under the
    yaw the thigh and shin twisted about their own axes and the knee cap dipped to -0.03.
    - `leg_unyaw()` re-aims the thigh and shin as Rz(psi) @ (the un-yawed shortest arc) and re-keys the foot. The joint
      positions are identical; the twist is gone.
  - Game camera: `renders/_kneel_2x_f40_f50.png` (game + tq). Crop: `_scratch/zoom_game_kneel_r5.png` (left round 4,
    right round 5).
    - The thigh now drops to the snow and the shin and foot run off to the side, not straight at the camera.
- **MC2', idle:** arm sway +/-5 kept, plus a forearm bend **+/-4** on Fore_L / Fore_R in opposite phase to the arm sway
  (the breath flex is kept).
  - Fist travel f0 -> f30: **L 0.105** BU; R 0.023 (the right fist peaks at other frames - its cycle range is 0.087).
  - Closest fist-to-thigh gap in the idle: 0.068 (L) / 0.066 (R); no collision.
  - Probe: `_scratch/arm_probe.py` -> `arm_r5.txt`.
- **MC3', walk:** shoulder swing 9 kept; the forearm bend in opposite phase goes **+/-2 -> +/-6**.
  - Fist range over the cycle: **0.206** BU per side.
  - Closest fist-to-thigh gap: **0.060** (>= 0.03); walk slide 0.0.
- **MC4', mouth:** see MODEL_NOTES (cavity (10, 10, 14) + a 0.012 lip; kit luma ~81, so the Studio check is needed).
- **9+ beats:**
  - Idle: one slow heavy LOOK (ANIM_REFS K8c: a slow head turn, weight by stillness). Head yaw 0 -> 12 deg over
    f44-60, hold to f84, back by f100. It is a single turn, not a shake. Head max 13.5 deg.
  - Walk: a per-step shoulder roll; the chest roll goes 1.5 -> 3.0 deg, one rock per step side.
- **Per clip:**

  | clip | chest vs spine (<= 5) | head max | ground | other |
  |---|---|---|---|---|
  | idle | 4.85 (f30) | 13.5 | 0.0 | foot drift 0; loop 0 / 0 |
  | walk | **3.61** (f12) | 1.4 | 0.0 | slide 0.0; loop 0 / 0 |
  | roar | 3.0 | 15.0 | 0.0 | - |
  | act | 4.68 (f57) | 14.1 | **-0.017** (f20) | ends at rest |

  Probe: `_scratch/ang_all.py` -> `ang_r5.txt`.
- **Step 1** (`_scratch/export_r5.txt`):
  - collision_free **true**; linear 0 on all clips; events unchanged.
  - FBX 08:24.
- **Renders** (title bar 08:22, "final 8.5 round 5"):
  - `_kneel_2x_f40_f50` (tq + game), `_beats2x_idle` / `_roar` / `_kneel`.
  - `_walk_sheet` (tq + **game** + side), `_roar_jaw_close`, `_kneel_views`, `_model_sheet`.
  - `_pose_tq_sheet` (08:24).

"""
ins(T + r"\MODEL_NOTES.md", "## FINAL 8.5 ROUND 4", MODEL)
ins(T + r"\CLIP_NOTES.md", "## FINAL 8.5 ROUND 4", CLIP)
print("ok")
