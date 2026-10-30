import io, json, os, time
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher"
S = D + r"\_scratch"


def hr(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_f85.txt")
sa = json.load(open(S + r"\shares_all_f85.json"))
st = json.load(open(S + r"\shares_strict_f85.json"))
eye = json.loads(open(S + r"\eye_f85.txt").read().split("EYE_RESULT", 1)[1])
gate = {"written": time.strftime("%Y-%m-%d %H:%M"),
        "round": "final 8.5 (_review/CoralCrusher_final85.md)",
        "export": r"C:\cdimp\CoralCrusher.fbx",
        "step1": {k: ex[k] for k in ("collision_free", "ground_min_z", "audit", "clips", "events")},
        "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"],
        "shares_all_pct": sa, "shares_strict_pct": st, "act_eye_tracking_and_roll": eye}
json.dump(gate, open(S + r"\gate_f85.json", "w"), indent=1)


def ins(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    io.open(path, "w", encoding="utf-8").write(s[:i] + text + s[i:])


def rep(path, a, b):
    s = io.open(path, encoding="utf-8").read()
    assert s.count(a) == 1, (path, s.count(a), a[:70])
    io.open(path, "w", encoding="utf-8").write(s.replace(a, b))


def row(v):
    x = sa[v]
    return "  | %s | %.1f | %.1f | %.1f | %.1f | %.1f |" % (v, x["BRONZE"], x["BRONZE_D"], x["SHELL_D"], x["BELLY_PALE"],
                                                         x["ROSE"] + x["ROSE_D"])


MODEL = """## FINAL 8.5 (2026-10-28, after `_review/CoralCrusher_final85.md`, FIX model 7.5) - EXPORTED
Single gate file: `_scratch/gate_f85.json`. Backup of the r5 export: `_scratch/CoralCrusher_exported_r5.py`.
- **MM1, rust copper:** BRONZE **(214,110,70)**, BRONZE_D **(150,74,50)**, SHELL_D **(80,46,34)**, exactly as specified.
  BELLY_PALE and ROSE are unchanged.
  - `renders/gamelook_game.png` (0.6x) reads a rust red-brown, not tan.
  - In `renders/_icons3_strip_128.png` (kit portrait, ALT, game icon, Kappa, Turtle, Kraken, Hammerjaw, Orca) the crab is
    a solid copper-orange. Hammerjaw stays navy with orange stripes and the Kraken red, so the copper reads as the
    crab's own colour.
- **MM2, pale edge:**
  - The rim band is now **BELLY_PALE**: 0.030 proud, 0.080 tall, deepening toward the rear to 0.065 proud and 0.170
    tall. A thin SHELL_D seam sits above it, inside the band edge, so from above the cream top shows past it.
  - The cream lip is lower (zc - 0.10) and wider (+0.040, rear +0.070).
  - **The 4 %% target is NOT met:** BELLY_PALE is **side %.1f %%, game %.1f %%** (tq %.1f, back %.1f), all figure
    pixels. Strict counts: side %.1f, game %.1f.
  - From the side camera (45 deg base yaw) the crusher claw, the margin spines and the leg plates cover the rim. From the
    game camera only the rear edge shows; it now reads as a cream two-tone edge (`renders/model_tq.png`,
    `_under_sheet.png`).
  - Doubling the share would need a pale skirt around the whole shell or cream on the claws (rejected in review 2).
    **This needs the owner's written no-pale sign-off, as the review says.**
- **TO 9+ 1:** merus 0.084 x 0.110 (+20 %%), coxa 0.080, top plate and spike raised with it.
- **TO 9+ 2:** the finger roots sit 0.097 c off the palm axis (was 0.085), giving a gape of about 0.06 H on the crusher.
  The four molars are bigger (0.030 x 0.026 x 0.022 c) on the inner edges of both fingers (they already existed but
  were small). Evidence: `renders/close_crushertq.png`, `close_crusherin.png`.
- **TO 9+ 3:** two taller ROSE_D + ROSE coral clusters on the dome centre (scale 1.30 / 1.20) at (0.075, 0.075) and
  (-0.085, 0.02).
- **Shares (all figure pixels, flat renders, %%):**

  | view | BRONZE | BRONZE_D | SHELL_D | pale | rose |
  |---|---|---|---|---|---|
%s
%s
%s
%s
- **Tris 12,644** (cap 15k). Lua 58,671 B.
- **Renders (2026-10-28):** `_model_sheet.png`, `_close_sheet.png` (crusher front / in / tq, face front / high),
  `_under_sheet.png`, `_icons_strip_*`, `_icons2_strip_*`, `_icons3_strip_*`, `gamelook_*.png`, `flat_*.png`.
- **Index portrait:** `CoralCrusher_portrait_alt.png` is re-made (= the game-camera render of idle f0, as ruled).

""" % (sa["side"]["BELLY_PALE"], sa["game"]["BELLY_PALE"], sa["tq"]["BELLY_PALE"], sa["back"]["BELLY_PALE"],
       st["side"]["BELLY_PALE"], st["game"]["BELLY_PALE"], row("game"), row("side"), row("tq"), row("back"))

CLIP = """## FINAL 8.5 (2026-10-28, after `_review/CoralCrusher_final85.md`, FIX clips 7.5) - EXPORTED
- **CM1, the idle breathes:**
  - The crusher guard breathes **20 +/- 3 deg** over one 35 f arc: troughs f45 / f80, peak f62, back to 20 by f98.
    The tap at f70 still reads.
  - The body bob is **0.008** (was 0.004), two breaths per loop, and the loop is closed.
  - Evidence: `renders/_pose_tq_sheet.png`, row 1 = idle f0 / 20 / 45 / 62 / 70 / 80 / 98 / 110.
- **CM2, secondary motion on the wave:**
  - The eyestalks track the crusher, 2 f behind the wave: a 0-1 track curve with tops held f28-36 / f51-59 / f74-82
    and troughs f41 / f64. Yaw **12 deg** toward the crusher on both eyes; the eye bones are mirrored, so L is - and
    R is +. The right eye also keeps a 4 deg base glance.
  - Probe (`_scratch/eye_probe.py`, horizontal angle from each stalk to the crusher tip) - both eyes point closer to the
    tip at the tops:

    | eye | tops (f30 / 53 / 76) | troughs (f41 / 64) |
    |---|---|---|
    | left | 57.9 | 71.4 |
    | right | 15.8 | 20.7 |
  - The r5 static `r=-8` actually turned the right eye AWAY from the crusher; it is now +4.
  - **Shell weight:** the roll is -2 +/- 2 deg with the beat (-4 at the tops, 0 at the troughs). The crusher shoulder
    sits 0.042 lower than the cutter's at each top and level at the troughs.
  - Evidence: `renders/_wave_strip.png` (tq + game, f18-82 every 2 f).
- **CM3:** the lead ruling is written into `ANIM_REFS.md`: the Wikimedia crab footage (C1) sets the walk timing; the
  site Ohmu (S1) backs only the leg alternation and the level shell.
- **TO 9+ 4, walk:** the crusher sways **4 deg** (spread) twice per 30 f cycle, phase-shifted between the tripod contacts.
  The cutter keeps its lift wave only.
- **Step 1** (`_scratch/export_f85.txt`):
  - collision_free **true**; ground_min_z -0.013 in every clip (the r5 value, the toe tips).
  - Linear 0; idle and walk loops 0 / 0; idle foot drift 0; **walk slide 0.002**, foot_z_var 0.001.
  - Clips and events are unchanged (act `wave1` 30, `wave2` 53, `wave3` 76, `tap1` 90, `tap2` 96).
- **Export:** `C:\\cdimp\\CoralCrusher.fbx` (2026-10-28 01:48, 1,223,484 B). The Index portrait is
  `CoralCrusher_portrait_alt.png`, re-made from the game camera.

"""

ins(D + r"\MODEL_NOTES.md", "## ROUND 3 (2026-10-27, after", MODEL)
ins(D + r"\CLIP_NOTES.md", "## ROUND 5 (2026-10-27, after", CLIP)

A = D + r"\ANIM_REFS.md"
ins(A, "## C1 - rock crab walk (4.6-7.0 s) (Wikimedia study notes)",
    """## LEAD RULING (final 8.5 review, CM3): what sets the walk timing
**The walk timing (the 30 f cycle, duty 0.55, the small quick steps) comes from the Wikimedia crab footage C1** (rock
crabs, 4.6-7.0 s: R1 low level shell, R2 diagonal body, R4 small quick alternating groups). The site clip S1 (the
Ohmu RUN) is NOT the timing source. It backs only the alternating leg groups and the level shell (O2), as noted in
review 4. animationreference.org has no crab, insect or multi-leg walk to take a crab timing from.

""")
rep(A, """- **idle (120 f loop): claw guard (#7).** The crusher lifts 20 deg to guard and holds; the eyestalks""",
    """- **idle (120 f loop): claw guard (#7).** The crusher lifts 20 deg to guard and breathes there (final 8.5: +/-3 deg over
  one 35 f arc, troughs f45 / f80, peak f62; the body bobs 0.008); the eyestalks""")
rep(A, """bob 0.010 (R1), claws held 10 deg LOWER than rest and folded (R3, review 2 N5), eyes lag 2 f (plan).""",
    """bob 0.010 (R1), claws held 10 deg LOWER than rest and folded (R3, review 2 N5), eyes lag 2 f (plan); the crusher
  sways 4 deg twice per cycle between the tripod contacts (final 8.5). Timing: C1 (lead ruling above).""")
print("notes + gate ok")
