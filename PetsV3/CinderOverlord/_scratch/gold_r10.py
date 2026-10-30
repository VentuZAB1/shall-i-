# python CinderOverlord/_scratch/gold_r10.py -> _scratch/gold_r10.json (+ CinderOverlord_icon_alt.png)
# The Cinder's three icons (portrait_alt molt f40, kit portrait idle f0, game camera) through the icon3 recipe at 64 and
# 128 px: kit gold counter, silhouette fill and area. The comparison pets are unchanged since round 9 (their numbers are
# copied from gold_r9.json; their folders are not touched).
import runpy, json, os, shutil
S = os.path.dirname(os.path.abspath(__file__))
D = os.path.dirname(S)
G = runpy.run_path(os.path.join(S, "gold_hist.py"))
shutil.copy(os.path.join(D, "CinderOverlord_portrait_alt.png"), os.path.join(S, "palt_r10_raw.png"))
src = {"portrait_alt": os.path.join(S, "palt_r10_raw.png"), "kit_portrait": os.path.join(D, "CinderOverlord_portrait_raw.png"),
       "game": os.path.join(D, "CinderOverlord_game_raw.png")}
out = {}
for k, p in src.items():
    ic = G["icon"](p)
    if k == "portrait_alt":
        ic.save(os.path.join(D, "CinderOverlord_icon_alt.png"))
    out[k] = {"64": G["stats"](ic, 64), "128": G["stats"](ic, 128)}
old = json.load(open(os.path.join(S, "gold_r9.json")))
for k in ("InfernoPhoenix", "Ivonrath", "ThunderRex", "CosmicLeviathan"):
    out[k] = old[k]
json.dump(out, open(os.path.join(S, "gold_r10.json"), "w"), indent=1)
print("GOLD10", {k: (v["64"]["kit_29-58"], v["64"]["area"], v["64"]["fill_h"], v["64"]["fill_w"]) for k, v in out.items()})
