# Convert the attachment points in <tree>_build.json (Blender coords) to Roblox axes relative to the FBX origin.
# Roblox (X, Y, Z) = (Blender X, Blender Z, -Blender Y).   python points_roblox.py
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))


def rb(p):
    return [round(p[0], 2), round(p[2], 2), round(-p[1], 2)]


for kind in ("dead", "haunted"):
    f = os.path.join(HERE, kind + "_build.json")
    if not os.path.exists(f):
        continue
    r = json.load(open(f))
    print("==", kind)
    for i, s in enumerate(r.get("spiders", [])):
        print("  spider %d: thread point %s  free drop %.1f  clear ring(1.2 stud) %.1f  branch r %.3f"
              % (i + 1, rb(s["point"]), s["free_drop"], s["clear_ring"], s["branch_radius"]))
    for i, w in enumerate(r.get("webs", [])):
        print("  web %d: hub %s  normal %s  radius %.2f  spokes %d" % (i + 1, rb(w["hub"]), rb(w["normal"]),
                                                                     w["radius"], w["spokes"]))
        print("         anchors (crotch, branch A, branch B):", [rb(a) for a in w["anchors"]])
    e = os.path.join(HERE, kind + "_export.json")
    if os.path.exists(e):
        x = json.load(open(e))
        lo, hi = x["bbox_blender"]
        print("  size Roblox X x Y x Z: %.2f x %.2f x %.2f" % (hi[0] - lo[0], hi[2] - lo[2], hi[1] - lo[1]))
        print("  bbox Roblox min", rb(lo), "max", rb(hi), "(Z swaps min/max sign)")
        print("  tris", x["tris"], "total", x["total_tris"])
