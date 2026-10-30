# blender -b --factory-startup --python PermafrostTitan/_scratch/thigh_probe.py -- <tag> [res=250] [f=40]
# r11 probe (fixed game camera = pk.camera_for(k, "game") at f0, read AFTER a depsgraph update):
#   pix   : screen share (visible / alone px, 700 px units) of Leg_L / Shin_L / Foot_L + top occluders (px)
#   vert  : vertex share (arm_search method) of Leg_L / Shin_L / Foot_L
#   arm   : Fore_L/Fist_L/Hand_L/Arm_L vs Leg_L/Shin_L face overlap at f, fist+hand gap to the Leg_L surface, fist centre z
#   knee  : lowest Shin_L vert near the Knee_L joint per frame f16-54 -> band f18-52, first frame <= 0; toes = Foot_L min
import sys, runpy, json, os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
tag = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
RES, F = int(opts.get("res", "250")), int(opts.get("f", "40"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk = R3["pk"]
R3["full"]("PermafrostTitan", save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = 700
k.set_action("act_kneelrise")
sc.frame_set(0)
loc, tgt = pk.camera_for(k, "game")
pk.aim(sc.camera, loc, tgt)
bpy.context.view_layer.update()
camo = sc.camera
cam = camo.matrix_world.to_translation()
tr, br, bl, tl = [camo.matrix_world @ v for v in camo.data.view_frame(scene=sc)]
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]


def mesh():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    W = [ev.matrix_world @ v.co for v in me.vertices]
    polys = [list(p.vertices) for p in me.polygons]
    ev.to_mesh_clear()
    pown = []
    for pl in polys:
        c = {}
        for i in pl:
            c[own[i]] = c.get(own[i], 0) + 1
        pown.append(max(c, key=c.get))
    return W, polys, pown


out = {"tag": tag, "f": F}
sc.frame_set(F)
W, polys, pown = mesh()
full = BVHTree.FromPolygons(W, polys)
B = ("Leg_L", "Shin_L", "Foot_L")
alone = {b: BVHTree.FromPolygons(W, [pl for pl, o in zip(polys, pown) if o == b]) for b in B}
ca, cv, oc = {b: 0 for b in B}, {b: 0 for b in B}, {b: {} for b in B}
for j in range(RES):
    left, right = tl.lerp(bl, (j + 0.5) / RES), tr.lerp(br, (j + 0.5) / RES)
    for i in range(RES):
        d = (left.lerp(right, (i + 0.5) / RES) - cam).normalized()
        h = full.ray_cast(cam, d, 50.0)
        first = pown[h[2]] if h[0] is not None else None
        for b in B:
            if alone[b].ray_cast(cam, d, 50.0)[0] is not None:
                ca[b] += 1
                if first == b:
                    cv[b] += 1
                elif first is not None:
                    oc[b][first] = oc[b].get(first, 0) + 1
sc_ = (700.0 / RES) ** 2
# the inside of the L: H' K' A' (hip, knee, ankle joints) on screen; background px inside that triangle = the gap
from bpy_extras.object_utils import world_to_camera_view
J = {b: k.arm.matrix_world @ k.arm.pose.bones[b].head for b in ("Leg_L", "Shin_L", "Foot_L")}
P2 = {b: world_to_camera_view(sc, camo, J[b]).to_2d() for b in J}
def _inside(p, a, b, c):
    def s_(p1, p2, p3):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
    d1, d2, d3 = s_(p, a, b), s_(p, b, c), s_(p, c, a)
    return not ((d1 < 0 or d2 < 0 or d3 < 0) and (d1 > 0 or d2 > 0 or d3 > 0))
gap = tri = 0
for j in range(RES):
    left, right = tl.lerp(bl, (j + 0.5) / RES), tr.lerp(br, (j + 0.5) / RES)
    for i in range(RES):
        uv = Vector(((i + 0.5) / RES, 1 - (j + 0.5) / RES))
        if _inside(uv, P2["Leg_L"], P2["Shin_L"], P2["Foot_L"]):
            tri += 1
            d = (left.lerp(right, (i + 0.5) / RES) - cam).normalized()
            if full.ray_cast(cam, d, 50.0)[0] is None:
                gap += 1
v1, v2 = (P2["Leg_L"] - P2["Shin_L"]), (P2["Foot_L"] - P2["Shin_L"])
import math
out["L"] = {"gap_px": round(gap * (700.0 / RES) ** 2), "tri_px": round(tri * (700.0 / RES) ** 2),
            "knee_angle_2d": round(math.degrees(v1.angle(v2)), 1) if v1.length and v2.length else None}
out["pix"] = {b: [round(cv[b] / max(1, ca[b]), 3), round(cv[b] * sc_)] for b in B}
out["occ"] = {b: {o: round(n * sc_) for o, n in sorted(oc[b].items(), key=lambda x: -x[1])[:3]} for b in B}
vert = {}
for b in B:
    ids = [i for i in range(len(W)) if own[i] == b]
    n = 0
    for i in ids:
        d = W[i] - cam
        h = full.ray_cast(cam, d.normalized(), d.length + 0.01)
        if h[0] is None or h[3] >= d.length - 0.004 or pown[h[2]] == b:
            n += 1
    vert[b] = round(n / max(1, len(ids)), 3)
out["vert"] = vert
legp = [pl for pl, o in zip(polys, pown) if o in ("Leg_L", "Shin_L")]
armp = [pl for pl, o in zip(polys, pown) if o in ("Fore_L", "Fist_L", "Hand_L", "Arm_L")]
bl_ = BVHTree.FromPolygons(W, [pl for pl, o in zip(polys, pown) if o == "Leg_L"])
fist = [W[i] for i in range(len(W)) if own[i] in ("Hand_L", "Fist_L")]
out["arm"] = {"overlap": len(BVHTree.FromPolygons(W, legp).overlap(BVHTree.FromPolygons(W, armp))),
              "gap": round(min(bl_.find_nearest(p)[3] for p in fist), 3),
              "fist_z": round((sum(fist, Vector()) / len(fist)).z, 3)}
kn, toes, land = [], [], None
kids = None
for f in range(16, 55):
    sc.frame_set(f)
    W, polys, pown = mesh()
    kj = k.arm.matrix_world @ k.arm.pose.bones["Knee_L"].head
    if kids is None:
        kids = [i for i in range(len(W)) if own[i] == "Shin_L" and (W[i] - kj).length < 0.14]
    z = min(W[i].z for i in kids)
    if 18 <= f <= 52:
        kn.append(z)
    if land is None and z <= 0:
        land = f
    toes.append(min(W[i].z for i in range(len(W)) if own[i] == "Foot_L"))
out["knee"] = {"band": [round(min(kn), 4), round(max(kn), 4)], "land": land, "toes": round(min(toes), 4)}
print("THIGH " + json.dumps(out))
open(os.path.join(k.dir, "_scratch", "thigh_probe_%s.json" % tag), "w").write(json.dumps(out, indent=1))
