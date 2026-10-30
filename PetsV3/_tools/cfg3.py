# python _tools/cfg3.py A B C -> Luau table literal of PetSetup3 configs (meta + bu json of each pet), one line
import sys, os, json
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = []
for n in sys.argv[1:]:
    m = json.load(open(os.path.join(here, n, n + "_meta.json"), encoding="utf-8"))
    bu = json.load(open(os.path.join(here, n, n + "_bu.json"), encoding="utf-8"))["height"]
    out.append('{name="%s",display="%s",height=%s,bu_height=%.4f,motion="%s",rig="%s",stride=%.5f,walk_len=%.4f}'
               % (m["name"], m["display"], m["height"], bu, m["motion"], m["rig"], m["stride"] or 0, m["walk_len"] or 1))
sys.stdout.buffer.write(("{" + ",".join(out) + "}").encode("utf-8"))
