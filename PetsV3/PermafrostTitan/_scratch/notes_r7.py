import io
T = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan"


def ins(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    io.open(path, "w", encoding="utf-8").write(s[:i] + text + s[i:])


CLIP = """## FINAL 8.5 ROUND 7 (2026-10-28, after `_review/PermafrostTitan_final85_r7.md`: model 8.6, idle / walk / roar 8.5 PASS, act 8.1) - re-exported 09:41
Backups:
- the round-6 export: `_scratch/PermafrostTitan_exported_r6.py`
- this export: `_scratch/PermafrostTitan_exported_r7.py`

Idle, walk and roar are untouched.
- **MUST 1 (act), the standing foot:** `STAND_OUT = 0.10`.
  - The right foot steps 0.10 further out (body frame, away from the kneel side) during the yaw ease-in. It lifts 0.05
    at f15.
  - It is planted for the whole hold: Foot_R stays at (-0.377, -0.330, 0.165) at f18, f30 and f52; min z 0.0, no slide.
  - It steps back f52-62 (lift 0.05 at f57). The 30 deg yaw and the act's exact rest are unchanged.
- **The knee option (0.06 outward) was tried and dropped** (`KNEE_OUT = 0`):
  - it lifted the kneeling knee OFF the snow (lowest point over the hold 0.0);
  - it put the left forearm into the thigh (Fore_L | Leg_L, f21-30).
- **Result - the pass is NOT reached; the standing leg stays hidden.** Measured on the fixed game camera at f40
  (`_scratch/leg_px.py`: projected px boxes + the share of each bone's verts not covered by other parts):

  | stand-out | Shin_R visible | Foot_R visible | Shin_L visible |
  |---|---|---|---|
  | 0.10 | 0.00 | 0.03 | 0.49 |
  | 0.25 (test) | 0.00 | 0.04 | 0.49 |

  - The standing shin projects ABOVE the kneeling leg on screen (y 370-480 vs 550-650 of 700 px), i.e. under and in
    front of the torso, which hides it from the high camera behind.
  - After the 30 deg yaw a body-lateral step moves only ~58 %% into the image's horizontal (0.10 BU = ~15 px). The
    torso + left arm cover x ~180-540, so the shin would need ~1 BU of sideways step to clear it.
  - Tested stand-outs: 0.10, 0.18, 0.25 (`_scratch/standout_cmp.png`) - no visible change.
  - What could work (lead call):
    - (a) A kneel whose standing leg goes out to the SIDE rather than forward (a different K1 step from the reference;
      the foot ~0.3 lateral, ~0.1 forward).
    - (b) Accept the read from behind as the kneeling leg's L alone (thigh down to the knee on the snow, shin flat).
    - (c) A Studio-side snow puff at `Knee_L` (`icecrack`) to sell the contact.
- **Gate** (`_scratch/export_r7.txt`):
  - collision_free **true**; knee **-0.005 to -0.017** over f18-52; ground -0.017 (f20); linear 0; loops 0 / 0.
  - Idle / walk / roar numbers unchanged (round 6).
- **Renders** (title bars 09:41-09:43, "final 8.5 round 7"):
  - `_kneel_2x_f30_f40_f50` (game + tq), `_kneel_2x_f40_f50`, `_kneel_views`, `_beats2x_kneel`.
  - Also re-made with the full set: `_beats2x_idle` / `_roar`, `_walk_sheet`, `_roar_front_sheet`, `_roar_jaw_close`,
    `_model_sheet`, `_close_sheet`, the icon strips, `_pose_tq_sheet`.

"""
ins(T + r"\CLIP_NOTES.md", "## FINAL 8.5 ROUND 6", CLIP)
print("ok")
