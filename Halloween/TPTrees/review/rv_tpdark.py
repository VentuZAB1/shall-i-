# Reviewer diagnostic: where is the darker TP albedo? (per strip-side island, up/down facing, hanging vs draped)
# blender.exe -b --factory-startup --python rv_tpdark.py -- <fbx> <canopy_bottom_z>
import bpy, sys, json
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
FBX, ZC = argv[0], float(argv[1])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=FBX)
o = bpy.data.objects["TP"]
me = o.data
me.calc_loop_triangles()
V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", V); V = V.reshape(-1, 3)
TV = np.empty(len(me.loop_triangles) * 3, dtype=np.int64); me.loop_triangles.foreach_get("vertices", TV); TV = TV.reshape(-1, 3)
TL = np.empty(len(me.loop_triangles) * 3, dtype=np.int64); me.loop_triangles.foreach_get("loops", TL); TL = TL.reshape(-1, 3)
UV = np.empty(len(me.loops) * 2); me.uv_layers.active.data.foreach_get("uv", UV); UV = UV.reshape(-1, 2)
img = None
for n in me.materials[0].node_tree.nodes:
    if n.type == "TEX_IMAGE" and any(l.to_socket.name == "Base Color" for l in me.materials[0].node_tree.links if l.from_node == n):
        img = n.image
w, h = img.size
I = np.empty(w * h * 4, dtype=np.float32); img.pixels.foreach_get(I); I = I.reshape(h, w, 4)
a, b, c = V[TV[:, 0]], V[TV[:, 1]], V[TV[:, 2]]
cr = np.cross(b - a, c - a)
area = 0.5 * np.linalg.norm(cr, axis=1)
nrm = cr / np.maximum(np.linalg.norm(cr, axis=1)[:, None], 1e-9)
# luma per triangle: average of 7 barycentric samples
ws = [(1/3, 1/3, 1/3), (0.6, 0.2, 0.2), (0.2, 0.6, 0.2), (0.2, 0.2, 0.6), (0.45, 0.45, 0.1), (0.1, 0.45, 0.45), (0.45, 0.1, 0.45)]
L = np.zeros(len(TV))
for w0, w1, w2 in ws:
    uv = UV[TL[:, 0]] * w0 + UV[TL[:, 1]] * w1 + UV[TL[:, 2]] * w2
    x = np.clip((uv[:, 0] % 1) * w, 0, w - 1).astype(int); y = np.clip((uv[:, 1] % 1) * h, 0, h - 1).astype(int)
    p = I[y, x, :3]
    L += 0.2126 * p[:, 0] + 0.7152 * p[:, 1] + 0.0722 * p[:, 2]
L /= len(ws)
cz = (a[:, 2] + b[:, 2] + c[:, 2]) / 3
# island id per vertex
n = len(V); par = list(range(n))
def find(x):
    while par[x] != x:
        par[x] = par[par[x]]; x = par[x]
    return x
E = np.empty(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", E)
for e0, e1 in E.reshape(-1, 2):
    r0, r1 = find(int(e0)), find(int(e1))
    if r0 != r1: par[r0] = r1
isl = np.array([find(int(t[0])) for t in TV])
dark = L < 0.65
out = {}
out["area_total"] = round(float(area.sum()), 2)
out["dark_area_frac(luma<0.65)"] = round(float(area[dark].sum() / area.sum()), 3)
hang = cz < ZC
out["hanging_area_frac"] = round(float(area[hang].sum() / area.sum()), 3)
out["dark_frac_in_hanging"] = round(float(area[dark & hang].sum() / max(area[hang].sum(), 1e-9)), 3)
out["dark_frac_in_draped"] = round(float(area[dark & ~hang].sum() / max(area[~hang].sum(), 1e-9)), 3)
out["dark_frac_downfacing(nz<-0.3)"] = round(float(area[dark & (nrm[:, 2] < -0.3)].sum() / max(area[nrm[:, 2] < -0.3].sum(), 1e-9)), 3)
out["dark_frac_upfacing(nz>0.3)"] = round(float(area[dark & (nrm[:, 2] > 0.3)].sum() / max(area[nrm[:, 2] > 0.3].sum(), 1e-9)), 3)
rows = []
for r in np.unique(isl):
    m = isl == r
    rows.append(dict(isl=int(r), tris=int(m.sum()), area=round(float(area[m].sum()), 2),
                     mean_luma=round(float((L[m] * area[m]).sum() / area[m].sum()), 3),
                     dark_frac=round(float(area[m & dark].sum() / area[m].sum()), 3),
                     mean_nz=round(float((nrm[m, 2] * area[m]).sum() / area[m].sum()), 2),
                     zmin=round(float(cz[m].min()), 2), zmax=round(float(cz[m].max()), 2),
                     centre=[round(float(x), 2) for x in V[np.unique(TV[m])].mean(0)]))
rows.sort(key=lambda d: -d["area"])
out["islands"] = rows
print("RV_TPDARK " + json.dumps(out, indent=0))
