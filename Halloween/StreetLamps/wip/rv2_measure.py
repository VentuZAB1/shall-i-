# Round-2 proof renders + measurements, built on the reviewer's review_check\rv.py (imported read-only; only its
# attachment constants are updated to the round-2 positions from export.json).
# Usage: blender -b --factory-startup --python wip\rv2_measure.py -- face|web|twist
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector

ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\StreetLamps"
sys.path.insert(0, os.path.join(ROOT, "review_check"))
import rv  # noqa: E402

OUT = os.path.join(ROOT, "wip", "rv2")
os.makedirs(OUT, exist_ok=True)
rv.OUT = OUT
E = json.load(open(os.path.join(ROOT, "export.json")))
A = E["attach"]
rv.PL = Vector(A["suggested_pointlight"])
rv.FLAME = Vector(A["flame_centre"])
rv.GROUNDL = Vector(A["ground_light"])
rv.HEAD = Vector((0.0, rv.HANG_Y, A["pumpkin_pivot"][2] + 0.09))
CLS = {1: "skin", 2: "wall", 3: "inner", 4: "wax", 5: "wick"}


def log(*a):
    print("[rv2]", *a, flush=True)


def read_png(p):
    im = bpy.data.images.load(p, check_existing=False)
    w, h = im.size
    a = np.empty(w * h * 4, np.float32)
    im.pixels.foreach_get(a)
    bpy.data.images.remove(im)
    return a.reshape(h, w, 4)[::-1]          # top row first


def class_render(name, cam_loc, tgt, res):
    """Same camera, flat emission ids: Pumpkin from wip\\Pumpkin_ids.png (R = (group + 1) / 16), all else black."""
    sc = bpy.context.scene
    saved = {}
    blk = bpy.data.materials.new("IdBlack")
    blk.use_nodes = True
    nt = blk.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (0, 0, 0, 1)
    o_ = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], o_.inputs[0])
    idm = bpy.data.materials.new("IdPumpkin")
    idm.use_nodes = True
    nt = idm.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = bpy.data.images.load(os.path.join(ROOT, "wip", "Pumpkin_ids.png"))
    t.image.colorspace_settings.name = "Non-Color"
    t.interpolation = "Closest"
    e = nt.nodes.new("ShaderNodeEmission")
    o_ = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(t.outputs["Color"], e.inputs["Color"])
    nt.links.new(e.outputs[0], o_.inputs[0])
    for o in sc.objects:
        if o.type == "MESH":
            saved[o.name] = list(o.data.materials)
            o.data.materials.clear()
            o.data.materials.append(idm if o.name.startswith("Pumpkin") else blk)
        if o.type == "LIGHT":
            o.hide_render = True
    w = sc.world
    wsave = []
    for n in w.node_tree.nodes:
        if n.type == "BACKGROUND":
            wsave.append((n, n.inputs["Strength"].default_value))
            n.inputs["Strength"].default_value = 0.0
    vt = sc.view_settings.view_transform
    sc.view_settings.view_transform = "Standard"
    sc.render.filter_size = 0.0
    p = rv.shot(name + "_ids", cam_loc, tgt, res=res)
    sc.render.filter_size = 1.5
    sc.view_settings.view_transform = vt
    for n, v in wsave:
        n.inputs["Strength"].default_value = v
    for o in sc.objects:
        if o.type == "MESH" and o.name in saved:
            o.data.materials.clear()
            for m in saved[o.name]:
                o.data.materials.append(m)
        if o.type == "LIGHT":
            o.hide_render = False
    return p


def srgb_to_lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def classes(ids_rgba):
    """Pixel class from the sRGB-encoded id value (k / 16 linear)."""
    v = ids_rgba[..., 0]
    lin = srgb_to_lin(v)
    k = np.rint(lin * 16).astype(int)
    ok = np.abs(lin * 16 - k) < 0.25
    return np.where(ok, k, 0)


def shift_or(m, r):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def erode(m, r):
    return ~shift_or(~m, r)


def measure(beauty, ids, dist):
    B = read_png(beauty)[..., :3]
    C = classes(read_png(ids))
    lin = srgb_to_lin(B)
    Y = 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]
    luma = 0.2126 * B[..., 0] + 0.7152 * B[..., 1] + 0.0722 * B[..., 2]
    hole = (C == 3) | (C == 4) | (C == 5)
    fill = erode(C == 3, 1)                                  # cavity seen through the holes, edges dropped
    wall = erode(C == 2, 1)
    cut = shift_or(hole | (C == 2), 1)
    ring = shift_or(cut, 7) & ~shift_or(cut, 2) & (C == 1)   # skin 2..7 px outside every hole
    res = dict(dist=dist, px_fill=int(fill.sum()), px_wall=int(wall.sum()), px_skin_ring=int(ring.sum()))
    for nm, m in (("fill", fill), ("wall", wall), ("skin_adjacent", ring), ("candle", erode(C == 4, 0))):
        if m.sum():
            res[nm + "_srgb"] = [round(float(x) * 255, 1) for x in B[m].mean(0)]
            res[nm + "_Y"] = round(float(Y[m].mean()), 4)
            res[nm + "_luma"] = round(float(luma[m].mean()) * 255, 1)
    if fill.sum() and ring.sum():
        res["ratio_Y"] = round(res["fill_Y"] / res["skin_adjacent_Y"], 3)
        res["ratio_luma"] = round(res["fill_luma"] / res["skin_adjacent_luma"], 3)
    if wall.sum() and fill.sum():
        res["wall_vs_fill_Y"] = round(res["wall_Y"] / res["fill_Y"], 3)
    return res


def step_face():
    sc, objs = rv.scene(False, res=(1920, 1080))
    rv.blockman(3.0, -6.0)
    rv.turn_pumpkin(objs, 1)
    out = []
    for dist in (25, 40):
        cam = rv.eye((1, 0), dist)
        b = rv.shot("F_day_side%d_faceturned_1080" % dist, cam, rv.AIM, res=(1920, 1080))
        ids = class_render("F_day_side%d_faceturned_1080" % dist, cam, rv.AIM, (1920, 1080))
        m = measure(b, ids, dist)
        m["pass_ratio_1.4"] = bool(m.get("ratio_Y", 0) >= 1.4 and m.get("ratio_luma", 0) >= 1.4)
        out.append(m)
        log(json.dumps(m))
    with open(os.path.join(OUT, "face_measure.json"), "w") as fh:
        json.dump(out, fh, indent=1)


def step_close():
    """Day / night close-ups and the reviewer's other day angles, with the round-2 attachments."""
    sc, objs = rv.scene(False)
    rv.blockman(3.0, -6.0)
    H = rv.HEAD
    rv.shot("D07_head8_front", H + Vector((0, -7.6, -2.4)), H, vfov=30, res=(1600, 1200))
    rv.shot("D08_head8_34below", H + Vector((5.0, -5.0, -3.6)), H, vfov=30, res=(1600, 1200))
    rv.shot("D10_crook10", Vector((10.0, -2.0, 13.5)), Vector((0, -1.9, 16.0)), vfov=35, res=(1600, 1200))
    rv.shot("D11_base6", Vector((-3.5, -5.0, 3.2)), Vector((0, 0, 1.2)), vfov=40, res=(1600, 1200))
    rv.shot("D03_side25_default", rv.eye((1, 0), 25), rv.AIM)
    rv.shot("D04_side40_default", rv.eye((1, 0), 40), rv.AIM)
    rv.shot("E01_base_3rdperson12", Vector((-7.0, -9.5, 7.5)), Vector((0, 0, 2.0)), vfov=70, res=(1920, 1080))
    rv.turn_pumpkin(objs, 1)
    rv.shot("D14_head8_side_faceturned", H + Vector((7.6, 0.0, -2.4)), H, vfov=30, res=(1600, 1200))
    rv.shot("D12_side25_faceturned", rv.eye((1, 0), 25), rv.AIM)
    for o in sc.objects:
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.use_shadow = False
    rv.shot("E03_base6_noshadow", Vector((-3.5, -5.0, 3.2)), Vector((0, 0, 1.2)), vfov=40, res=(1600, 1200))


def step_checks():
    sc, objs = rv.scene(False, res=(1600, 1200))
    for o in objs.values():
        o["orig_mat"] = o.data.materials[0]
    sc.view_settings.view_transform = "AgX"
    rv.set_mode(objs, "clay")
    rv.shot("C07_clay_head_34_8", rv.HEAD + Vector((5.0, -5.0, -3.6)), rv.HEAD, vfov=30)
    rv.shot("C08_clay_crook12", Vector((12.0, -2.0, 13.0)), Vector((0, -1.9, 16.0)), vfov=28)
    rv.shot("C10_clay_full25_side", rv.eye((1, 0), 25), rv.AIM)
    rv.set_mode(objs, "nrm")
    rv.shot("C11_nrm_head_front", rv.HEAD + Vector((0, -6.0, -1.0)), rv.HEAD, vfov=28)
    rv.shot("C13_nrm_base", Vector((-3.0, -4.2, 2.6)), Vector((0, 0, 1.2)), vfov=36)
    rv.shot("C14_nrm_mid_pole", Vector((-3.0, -3.5, 7.0)), Vector((0, 0, 7.5)), vfov=36)


def step_c14ns():
    """C14 again with the sun's shadows off: separates EEVEE shadow-terminator stripes from normal-map faults."""
    sc, objs = rv.scene(False, res=(1600, 1200))
    for o in objs.values():
        o["orig_mat"] = o.data.materials[0]
    sc.view_settings.view_transform = "AgX"
    rv.set_mode(objs, "nrm")
    for o in sc.objects:
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.use_shadow = False
    rv.shot("C14_nrm_mid_pole_noshadow", Vector((-3.0, -3.5, 7.0)), Vector((0, 0, 7.5)), vfov=36)


def step_night():
    sc, objs = rv.scene(True)
    rv.blockman(3.0, -6.0)
    rv.turn_pumpkin(objs, 1)
    rv.shot("N05_side25_faceturned", rv.eye((1, 0), 25), rv.AIM)
    rv.shot("N06_side40_faceturned", rv.eye((1, 0), 40), rv.AIM)
    rv.shot("N03_head8_side", rv.HEAD + Vector((7.6, 0.0, -2.4)), rv.HEAD, vfov=30, res=(1600, 1200))


def step_twist():
    """Albedo mean of the twist vs the plain pole iron, sampled from the re-imported FBX's Post colour map at the
    face-corner UVs (area weighted)."""
    rv.fresh(4)
    objs = rv.import_lamp()
    o = objs["Post"]
    me = o.data
    me.calc_loop_triangles()
    img = None
    for n in me.materials[0].node_tree.nodes:
        if n.type == "TEX_IMAGE" and any(l.to_socket.name == "Base Color" for l in n.outputs["Color"].links):
            img = n.image
    w, h = img.size
    px = np.empty(w * h * 4, np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)
    uv = np.empty(len(me.loops) * 2, np.float32)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    co = np.empty(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)                     # rv.import_lamp: the mesh is in studs (object scale reset to 1)
    sums = {"twist": [np.zeros(3), 0.0], "pole": [np.zeros(3), 0.0]}
    rng = np.random.default_rng(1)
    for t in me.loop_triangles:
        P = co[list(t.vertices)]
        cz = P[:, 2].mean()
        rad = np.linalg.norm(P[:, :2].mean(0))
        if rad > 0.45:
            continue
        if 6.50 < cz < 7.80:
            key = "twist"
        elif (2.9 < cz < 5.9) or (8.5 < cz < 15.0):
            key = "pole"
        else:
            continue
        U = uv[list(t.loops)]
        area = t.area
        for _ in range(4):
            a, b = rng.random(2)
            if a + b > 1:
                a, b = 1 - a, 1 - b
            q = U[0] + a * (U[1] - U[0]) + b * (U[2] - U[0])
            x, y = int(q[0] * w) % w, int(q[1] * h) % h
            sums[key][0] += px[y, x, :3] * area / 4
            sums[key][1] += area / 4
    res = {}
    for k, (s_, a_) in sums.items():
        m = s_ / max(a_, 1e-9)
        res[k + "_srgb"] = [round(float(c) * 255, 1) for c in m]
        lin = srgb_to_lin(m)
        res[k + "_Y"] = round(float(0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]), 5)
    res["twist_vs_pole_Y"] = round(res["twist_Y"] / res["pole_Y"], 3)
    res["twist_vs_pole_srgb_mean"] = round(float(np.mean(res["twist_srgb"])) / float(np.mean(res["pole_srgb"])), 3)
    res["chroma_twist_R_minus_B"] = round(res["twist_srgb"][0] - res["twist_srgb"][2], 1)
    res["chroma_pole_R_minus_B"] = round(res["pole_srgb"][0] - res["pole_srgb"][2], 1)
    log(json.dumps(res))
    with open(os.path.join(OUT, "twist_measure.json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    {"face": step_face, "close": step_close, "checks": step_checks, "night": step_night,
     "twist": step_twist, "c14ns": step_c14ns}[argv[0]]()
    log("done", argv[0])
