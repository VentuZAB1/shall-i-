import io, json, time
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher"
S = D + r"\_scratch"


def hr(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r3.txt")
eye = json.loads(open(S + r"\eye_r3.txt").read().split("EYE_RESULT", 1)[1])
sh = json.load(open(S + r"\shares_all_r3.json"))
g = json.load(open(S + r"\gate_f85.json"))
g.update({"written": time.strftime("%Y-%m-%d %H:%M"), "round": "9+ round (_review/CoralCrusher_final85_r3.md, PASS 8.5 / 8.5)",
          "step1": {k: ex[k] for k in ("collision_free", "ground_min_z", "audit", "clips", "events")},
          "tris": ex["tris_body"], "act_eye_tracking_and_roll": eye, "shares_all_pct": sh})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)
R = lambda f: eye[str(f)]
TXT = """## 9+ ROUND (2026-10-28, after `_review/CoralCrusher_final85_r3.md`: model 8.5 + clips 8.5 PASS) - EXPORTED 04:39
Backup of the r2 export: `_scratch/CoralCrusher_exported_r2.py`.
- **Eyes:**
  - Left yaw **-16 x track** (was -12). Right **30 x track** (was 4 base + 20 x track).
  - The right eye already points within ~3 deg of the tip at the tops, so more yaw there would overshoot. Its static
    4 deg glance is folded into the tracking, which raises the swing at the troughs.
  - Tip-angle swing (`_scratch/eye_probe.py`, `eye_r3.txt`):

    | eye | troughs (f41 / 64) | tops (f30 / 53 / 76) | swing |
    |---|---|---|---|
    | right | %.1f | %.1f | **%.1f deg** |
    | left | %.1f | %.1f | **%.1f deg** |

    Rest at f0 / f110 is exact (%.1f / %.1f).
- **Shell roll +/-4** (was 3): -6 at the tops, +2 at the troughs. The crusher-side shoulder sits %.4f at the tops and
  +%.4f at the troughs, a swing of **%.3f BU** (target >= 0.08).
- **Idle guard breath +/-6** (was 5), on the same 35 f arc; the f70 tap stays.
- **Act trough, lower:**
  - Merus trough **2** (was 16) and palm (wrist) trough **+2** (was -40); the top is unchanged (merus 40, wrist -6).
  - collision_free stays true. The full gate was re-run at merus 12, 8 and 2, then with the wrist change.
  - World angles at f41: merus 22.6 deg and carpus 19.2 deg above horizontal; the palm-to-tip is **46.5 deg** (was
    71.5). The tip drops **0.36 BU** from top to trough (was 0.18).
- **N1, model:** the two dome rose clusters taper - wider ROSE_D base (0.060 x scale, was 0.045) and pointed ROSE spikes
  (top 0.22, base 0.030 x scale). `renders/close_domeclusters.png`.
- **Step 1** (`_scratch/export_r3.txt`):
  - collision_free **true**; ground_min_z -0.013 in every clip.
  - Linear 0; idle and walk loops 0 / 0; idle foot drift 0; walk slide 0.002.
  - Tris **12,452**. Events are unchanged.
- **Renders (title bar = render time, 2026-10-28 04:40):**
  - `_act_eyes_roll.png` - game + front cameras, f0 / f30 / f41 / f53, from the current file.
  - `_model_sheet.png`, `_beats2x_idle.png` (idle f0 / 20 / 45 / 62 / 80 / 110), `_pose_tq_sheet.png`, `_wave_strip.png`.
  - `close_domeclusters.png`, `_icons3_strip_128.png`, `gamelook_game.png`.
- **Export:** `C:\\cdimp\\CoralCrusher.fbx` (04:39). `CoralCrusher_portrait_alt.png` is re-made from the game camera
  (04:40).

""" % (R(41)["Eye_R"], R(30)["Eye_R"], R(41)["Eye_R"] - R(30)["Eye_R"], R(41)["Eye_L"], R(30)["Eye_L"],
       R(41)["Eye_L"] - R(30)["Eye_L"], R(110)["Eye_L"], R(110)["Eye_R"], R(30)["shoulder_zR_minus_zL"],
       R(41)["shoulder_zR_minus_zL"], R(41)["shoulder_zR_minus_zL"] - R(30)["shoulder_zR_minus_zL"])
p = D + r"\CLIP_NOTES.md"
s = io.open(p, encoding="utf-8").read()
i = s.index("## FINAL 8.5 ROUND 2")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
a = io.open(D + r"\ANIM_REFS.md", encoding="utf-8").read()
a = a.replace("breathes there (final 8.5 r2: +/-5 deg over", "breathes there (9+ round: +/-6 deg over")
a = a.replace("(Final 8.5 r2: the eyestalks track the crusher - L 12 deg, R 20 deg - 2 f behind the wave, and the shell rolls -2 +/- 3 deg",
              "(9+ round: the eyestalks track the crusher - L 16 deg, R 30 deg - 2 f behind the wave, the shell rolls -2 +/- 4 deg, the trough drops to merus 2 / palm +2")
io.open(D + r"\ANIM_REFS.md", "w", encoding="utf-8").write(a)
print("ok")
