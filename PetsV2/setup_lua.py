# python setup_lua.py <Pet> [light]  -> prints studio_setup.lua with CFG filled from <Pet>_meta.json
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
n = sys.argv[1]
m = json.load(open(os.path.join(here, n, n + "_meta.json")))
cfg = '{name = "%s", display = "%s", height = %s, motion = "%s", rig = "%s", stride = %.5f, walk_len = %.4f, glow = {%s}, light = %s}' % (
    m["name"], m["display"], m["height"], m["motion"], m["rig"], m["stride"] or 0, m["walk_len"] or 1,
    ", ".join('"%s"' % g for g in m["glow"]), sys.argv[2] if len(sys.argv) > 2 else "1.2")
print(open(os.path.join(here, "studio_setup.lua"), encoding="utf-8").read().replace("__CFG__", cfg))
