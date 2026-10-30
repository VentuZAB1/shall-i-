import io, json, time
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher"
S = D + r"\_scratch"


def hr(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r2.txt")
eye = json.loads(open(S + r"\eye_r2.txt").read().split("EYE_RESULT", 1)[1])
g = json.load(open(S + r"\gate_f85.json"))
g.update({"written": time.strftime("%Y-%m-%d %H:%M"), "round": "final 8.5 round 2 (_review/CoralCrusher_final85_r2.md)",
          "step1": {k: ex[k] for k in ("collision_free", "ground_min_z", "audit", "clips", "events")},
          "act_eye_tracking_and_roll": eye})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)

CLIP = """## FINAL 8.5 ROUND 2 (2026-10-28, after `_review/CoralCrusher_final85_r2.md`, model 8.5 PASS, clips 8.0) - EXPORTED
- **CM-R2-1, idle:** the crusher guard breathes **+/-5 deg** (was 3) over the same 35 f arc (troughs f45 / f80, peak f62).
- **CM-R2-2, act:**
  - The right eye's tracking yaw is **20 x track** (was 12); the left stays -12. The eye bones are mirrored, so L is
    - and R is +, re-checked with the probe.
  - Horizontal angle from each stalk to the crusher tip (`_scratch/eye_probe.py`, `eye_r2.txt`):

    | eye | troughs (f41 / 64) | tops (f30 / 53 / 76) | f36 | tracking |
    |---|---|---|---|---|
    | right | %.1f | %.1f | %.1f | **%.1f deg** |
    | left | %.1f | %.1f | – | **%.1f deg** |

    Both eyes are >= 10 deg.
  - **Shell roll +/-3 deg** with the beat (was 2): -5 at the tops, +1 at the troughs. The crusher shoulder sits
    %.3f lower than the cutter's at the tops and %.3f higher at the troughs.
- **CM-R2-3, walk sway:**
  - At 4 deg the crusher did not visibly move in the game-camera preview (`renders/_walk_sway_strip.png`, every 3 f).
    It is now **6 deg** (spread, twice per 30 f cycle, between the tripod contacts).
  - `renders/_walk_sway_claw.png` (a crusher crop of the same frames with a fixed reference line) shows the tip moving.
  - **Walk slide stays 0.002** (foot_z_var 0.001).
- **Step 1** (`_scratch/export_r2.txt`):
  - collision_free **true**; ground_min_z -0.013 in every clip.
  - Linear 0; idle and walk loops 0 / 0; idle foot drift 0.
  - Tris 12,644. Clips and events are unchanged.
- **Renders:** `_pose_tq_sheet.png` (26 beats incl. idle f0-110) and `_wave_strip.png` (re-made); the walk strips above.
- **Export:** `C:\\cdimp\\CoralCrusher.fbx` (2026-10-28 03:48). `CoralCrusher_portrait_alt.png` re-made from the game
  camera.

""" % (eye["41"]["Eye_R"], eye["30"]["Eye_R"], eye["36"]["Eye_R"], eye["41"]["Eye_R"] - eye["30"]["Eye_R"],
       eye["41"]["Eye_L"], eye["30"]["Eye_L"], eye["41"]["Eye_L"] - eye["30"]["Eye_L"],
       -eye["30"]["shoulder_zR_minus_zL"], eye["41"]["shoulder_zR_minus_zL"])
p = D + r"\CLIP_NOTES.md"
s = io.open(p, encoding="utf-8").read()
i = s.index("## FINAL 8.5 (2026-10-28")
io.open(p, "w", encoding="utf-8").write(s[:i] + CLIP + s[i:])
a = io.open(D + r"\ANIM_REFS.md", encoding="utf-8").read()
a = a.replace("breathes there (final 8.5: +/-3 deg over", "breathes there (final 8.5 r2: +/-5 deg over")
a = a.replace("the crusher\n  sways 4 deg twice per cycle", "the crusher\n  sways 6 deg twice per cycle")
a = a.replace("(Final 8.5: the eyestalks track the crusher 12 deg, 2 f behind the wave, and the shell rolls -2 +/- 2 deg",
              "(Final 8.5 r2: the eyestalks track the crusher - L 12 deg, R 20 deg - 2 f behind the wave, and the shell rolls -2 +/- 3 deg")
io.open(D + r"\ANIM_REFS.md", "w", encoding="utf-8").write(a)
print("crab notes ok")
