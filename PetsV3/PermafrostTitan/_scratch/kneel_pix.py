# blender -b --factory-startup --python PermafrostTitan/_scratch/kneel_pix.py -- <tag> [frames=40,50] [res=350]
# r10: SCREEN-AREA visibility on the fixed game camera (pk.camera_for(k, "game") at f0, as arm_search.py):
# for every pixel of a res x res grid a ray is cast through the camera frame;
#   alone_px(bone)   = pixels whose ray hits that bone's own faces (the bone's whole projected area)
#   visible_px(bone) = pixels whose FIRST hit on the full mesh belongs to that bone
#   share = visible / alone (what fraction of the part's on-screen area the player sees)
# Also reports the vert-ray share used by arm_search.py (vis_*), for comparison.
import sys, runpy, json, os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
tag = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
frames = [int(v) for v in opts.get("frames", "40,50").split(",")]
RES = int(opts.get("res", "350"))
view = opts.get("view", "game")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk = R3["pk"]
R3["full"]("PermafrostTitan", save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = 700
k.set_action("act_kneelrise")
sc.frame_set(0)
loc, tgt = pk.camera_for(k, view)
pk.aim(sc.camera, loc, tgt)
bpy.context.view_layer.update()
camo = sc.camera
cam = camo.matrix_world.to_translation()
fr = [camo.matrix_world @ v for v in camo.data.view_frame(scene=sc)]   # tr, br, bl, tl (world)
tr, br, bl, tl = fr
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
BONES = ("Leg_L", "Shin_L", "Foot_L")
out = {"tag": tag, "res": RES}
for f in frames:
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    W = [mw @ v.co for v in me.vertices]
    polys = [list(p.vertices) for p in me.polygons]
    ev.to_mesh_clear()
    pown = []
    for pl in polys:
        c = {}
        for i in pl:
            c[own[i]] = c.get(own[i], 0) + 1
        pown.append(max(c, key=c.get))
    full = BVHTree.FromPolygons(W, polys)
    alone = {b: BVHTree.FromPolygons(W, [pl for pl, o in zip(polys, pown) if o == b]) for b in BONES}
    cnt_alone = {b: 0 for b in BONES}
    cnt_vis = {b: 0 for b in BONES}
    occ = {b: {} for b in BONES}
    for j in range(RES):
        v = (j + 0.5) / RES
        left = tl.lerp(bl, v)
        right = tr.lerp(br, v)
        for i in range(RES):
            u = (i + 0.5) / RES
            p = left.lerp(right, u)
            d = (p - cam).normalized()
            hit = full.ray_cast(cam, d, 50.0)
            first = pown[hit[2]] if hit[0] is not None else None
            for b in BONES:
                h = alone[b].ray_cast(cam, d, 50.0)
                if h[0] is not None:
                    cnt_alone[b] += 1
                    if first == b:
                        cnt_vis[b] += 1
                    elif first is not None:
                        occ[b][first] = occ[b].get(first, 0) + 1
    scale = (700.0 / RES) ** 2          # report in px of the 700 px game render
    out[f] = {b: {"alone_px": round(cnt_alone[b] * scale), "visible_px": round(cnt_vis[b] * scale),
                  "share": round(cnt_vis[b] / max(1, cnt_alone[b]), 3),
                  "occluders": dict(sorted(occ[b].items(), key=lambda x: -x[1])[:3])} for b in BONES}
print("KNEELPIX " + json.dumps(out))
open(os.path.join(k.dir, "_scratch", "kneel_pix_%s.json" % tag), "w").write(json.dumps(out, indent=1))
