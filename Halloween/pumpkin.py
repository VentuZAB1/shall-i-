# SLINGSHOT Halloween - carved pumpkins: the GIANT jack-o'-lantern head behind the back wall + the pumpkin eggs.
# Headless:  blender.exe -b --factory-startup --python pumpkin.py -- head | render | export
# A pumpkin = UV-sphere sculpt (ribs that converge on a stem well, fat/thin ribs, lumps, striations, colour streaks,
# blemishes) -> solidify inward (hollow, inner wall = material 1) -> EXACT boolean with the face cutters (cut walls =
# material 2 "flesh") -> game mesh -> bakes. The face looks along Blender +Y (= Roblox -Z, toward the hub).
import sys, os
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import *  # noqa
import json
import numpy as np

SKIN = dict(crest=lin((246, 130, 20)), light=lin((255, 178, 60)), groove=lin((170, 58, 10)),
            top=lin((112, 98, 36)), bottom=lin((242, 162, 56)), blemish=lin((176, 124, 62)),
            red=lin((224, 92, 14)), gold=lin((252, 158, 36)))


def pumpkin_sculpt(name, P):
    rng = random.Random(P["seed"])
    off = Vector((rng.uniform(-50, 50), rng.uniform(-50, 50), rng.uniform(-50, 50)))
    off2 = Vector((rng.uniform(-50, 50), rng.uniform(-50, 50), rng.uniform(-50, 50)))
    N = P["N"]
    ribvar = [rng.uniform(-1, 1) for _ in range(N)]
    phase = rng.uniform(0, 1)
    R, Rz, eg = P["R"], P["Rz"], P.get("egg", 0.0)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=P["useg"], v_segments=P["vseg"], radius=1.0)
    cols, rough = [], []
    for v in bm.verts:
        d = v.co.normalized()
        th = math.acos(max(-1.0, min(1.0, d.z)))
        ph = math.atan2(d.y, d.x)
        s = math.sin(th)
        u = N * ph / (2 * math.pi) + phase
        k = math.floor(u + 0.5)
        f = u - k                                   # -0.5 .. 0.5 across a rib (grooves at +-0.5)
        kk = int(k) % N
        rv = ribvar[kk]
        bulge = max(0.0, math.cos(math.pi * f)) ** P["crest"]
        depth = P["depth"] * (s ** 0.7) * (1 + 0.3 * rv)
        m = 1.0 - depth * (1.0 - bulge)
        m *= 1.0 + 0.03 * rv * s                    # fat and thin ribs
        m *= 1.0 + P["lumps"] * fbm(d * 1.4 + off, 3)
        stri = noise.noise(Vector((f * 10.0 + kk * 3.7, th * 2.4, 1.7)))
        m *= 1.0 + P["micro"] * (0.9 * stri * s + 0.6 * fbm(d * 24.0 + off2, 3))
        w = 1 - eg * d.z                            # egg: narrower top
        x, y = d.x * m * R * w, d.y * m * R * w
        z = d.z * Rz * (1 + 0.45 * (m - 1))
        z -= P["dtop"] * Rz * math.exp(-(th / P["dtop_w"]) ** 2)   # the stem well
        z += P["dbot"] * Rz * math.exp(-((math.pi - th) / 0.5) ** 2)
        v.co = Vector((x, y, z))
        col = mix(SKIN["groove"], SKIN["crest"], bulge ** 0.55)
        sk = noise.noise(Vector((f * 16.0 + kk * 5.1, th * 3.3, 9.1)))
        col = mix(col, SKIN["light"], 0.42 * smoothstep(0.1, 0.6, sk) * bulge)
        tone = fbm(d * 1.1 + off2, 2)
        col = mix(col, SKIN["red"] if tone < 0 else SKIN["gold"], min(1.0, abs(tone) * 0.9))
        col = mix(col, SKIN["bottom"], 0.45 * smoothstep(2.3, 3.0, th))
        col = mix(col, SKIN["top"], 0.85 * math.exp(-(th / (P["dtop_w"] * 0.85)) ** 2))
        bl = smoothstep(0.55, 0.75, fbm(d * 9.0 + off2 * 0.7, 3)) * P.get("blemish", 1.0)  # rare small scuffs
        col = mix(col, SKIN["blemish"], 0.3 * bl)
        r = 0.38 + 0.22 * (1 - bulge) + 0.32 * bl
        cols.append(col)
        rough.append((r, r, r))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    set_colors(me, "Col", cols)
    set_colors(me, "Rough", rough)
    for p in me.polygons:
        p.use_smooth = True
    return link(bpy.data.objects.new(name, me))


def lip(W, yfun, teeth, direction, sign, step, jit, rng):
    """One lip of a grin, walked left->right (direction 1) or right->left (-1). Teeth = (centre, width, tip width,
    length); sign -1 = teeth hang down (top lip), +1 = point up (bottom lip)."""
    pts = []
    n = int(round(2 * W / step))
    for i in range(n + 1):
        x = -W + i * step if direction > 0 else W - i * step
        if not any(abs(x - c) < w / 2 for c, w, tw, L in teeth):
            pts.append((x, yfun(x) + rng.uniform(-jit, jit)))
        for c, w, tw, L in teeth:
            e_in = c - w / 2 if direction > 0 else c + w / 2
            if (direction > 0 and x <= e_in < x + step) or (direction < 0 and x >= e_in > x - step):
                e_out = c + w / 2 if direction > 0 else c - w / 2
                t_in = c - tw / 2 if direction > 0 else c + tw / 2
                t_out = c + tw / 2 if direction > 0 else c - tw / 2
                pts += [(e_in, yfun(e_in)), (t_in, yfun(e_in) + sign * L), (t_out, yfun(e_out) + sign * L),
                        (e_out, yfun(e_out))]
    return pts


def grin(W, top, bot, top_teeth, bot_teeth, corner_up, step, jit, seed):
    """top/bot = (centre y, rise at the corners). Returns the mouth outline (viewer coords)."""
    rng = random.Random(seed)
    ytop = lambda x: top[0] + top[1] * (x / W) ** 2
    ybot = lambda x: bot[0] + bot[1] * (x / W) ** 2
    cy = (top[0] + top[1] + bot[0] + bot[1]) / 2
    pts = [(W + 0.06 * W, cy + corner_up)]
    pts += lip(W * 0.985, ytop, top_teeth, -1, -1, step, jit, rng)
    pts.append((-W - 0.06 * W, cy + corner_up))
    pts += lip(W * 0.985, ybot, bot_teeth, 1, 1, step, jit, rng)
    return pts


# The giant head's face, designed in studs for R 55 / Rz 40 (viewer coords: x to the viewer's right, z up).
def giant_face():
    eye = quad_bezier((6, 13), (19, 21.5), (32, 24), 12)[:-1] + quad_bezier((32, 24), (25, -3), (6, 13), 16)[:-1]
    nose = (quad_bezier((0, 3.5), (-2.4, -1.6), (-6.8, -8), 8)[:-1] + quad_bezier((-6.8, -8), (0, -10.2), (6.8, -8), 8)[:-1]
            + quad_bezier((6.8, -8), (2.4, -1.6), (0, 3.5), 8)[:-1])
    # a wide grin with interleaved fangs (top 4 hang down, bottom 3 point up), slightly uneven like a knife cut
    mouth = grin(37, (-15.0, 8.0), (-34.5, 23.0),
                 top_teeth=[(-24.0, 7.2, 1.1, 8.6), (-8.5, 7.8, 1.2, 9.6), (8.0, 7.6, 1.1, 9.2), (23.5, 7.0, 1.0, 8.0)],
                 bot_teeth=[(-16.0, 7.0, 1.0, 7.6), (0.0, 7.4, 1.1, 8.4), (16.5, 7.0, 1.0, 7.4)],
                 corner_up=5.5, step=1.0, jit=0.25, seed=11)
    return {"EyeR": eye, "EyeL": [(-x, z) for x, z in eye], "Nose": nose, "Mouth": mouth}


def cutter(name, outlines, y0, y1, flesh):
    """Extrude each outline (viewer coords, studs) along +Y from y0 to y1. Viewer's right = world -X."""
    bm = bmesh.new()
    for pts in outlines.values():
        vs = [bm.verts.new((-x, y0, z)) for x, z in pts]
        f = bm.faces.new(vs)
        ext = bmesh.ops.extrude_face_region(bm, geom=[f])
        moved = [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=(0, y1 - y0, 0), verts=moved)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.triangulate(bm, faces=bm.faces, quad_method="BEAUTY", ngon_method="EAR_CLIP")
    ob = obj_from_bm(bm, name, smooth=False)
    ob.data.materials.append(flesh)
    return ob


def cutter_radial(name, outlines, R, Rz, flesh, inner_k=0.3, outer_k=1.7, egg=0.0):
    """Like a real knife: each outline (viewer coords, studs, on the front of an R/Rz ellipsoid) is cut along rays
    from the centre, so the cut walls stand square to the skin (a Y-extruded cutter shows wide flesh bands where the
    surface curves away, e.g. at the mouth corners)."""
    bm = bmesh.new()
    for pts in outlines.values():
        b = bmesh.new()
        inner, outer = [], []
        for vx, vz in pts:
            x, z = -vx, vz
            w = 1 - egg * max(-1.0, min(1.0, z / Rz))
            q = 1 - (x / (R * w)) ** 2 - (z / Rz) ** 2
            y = R * w * math.sqrt(max(0.02, q))
            p = Vector((x, y, z))
            inner.append(b.verts.new(p * inner_k))
            outer.append(b.verts.new(p * outer_k))
        n = len(pts)
        b.faces.new(inner)
        b.faces.new(list(reversed(outer)))
        for i in range(n):
            j = (i + 1) % n
            b.faces.new((inner[i], outer[i], outer[j], inner[j]))
        bmesh.ops.triangulate(b, faces=b.faces, quad_method="BEAUTY", ngon_method="EAR_CLIP")
        bmesh.ops.recalc_face_normals(b, faces=b.faces)
        if b.calc_volume(signed=True) < 0:  # recalc can leave a thin cone inside-out (the nose did): flip it
            bmesh.ops.reverse_faces(b, faces=b.faces)
        tmp = bpy.data.meshes.new("_island")
        b.to_mesh(tmp)
        b.free()
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    ob = obj_from_bm(bm, name, smooth=False)
    ob.data.materials.append(flesh)
    return ob


def repair_attrs(ob, wall=2, names=("Col", "Rough")):
    """(From the PumpkinEggs builder, 2026-10-12.) The EXACT boolean does NOT interpolate point colour attributes onto
    the new cut vertices: they come out (0,0,0,0) -> a black glossy band along every knife edge on the bake source =
    the dark serrated rims around the holes. Refill each from its valid neighbours on the same surface (never across a
    cut wall), ring by ring."""
    me = ob.data
    arrs = {}
    for nm in names:
        a = me.color_attributes.get(nm)
        if a is not None:
            arr = np.empty(len(a.data) * 4, np.float32)
            a.data.foreach_get("color", arr)
            arrs[nm] = arr.reshape(-1, 4)
    if "Col" not in arrs:
        return 0, 0
    valid = arrs["Col"][:, 3] > 0.5
    nbad = int((~valid).sum())
    if nbad:
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.verts.ensure_lookup_table()
        nb = {}
        for i in np.nonzero(~valid)[0]:
            v = bm.verts[int(i)]
            nb[int(i)] = [e.other_vert(v).index for e in v.link_edges
                          if any(f.material_index != wall for f in e.link_faces)]
        bm.free()
        for _ in range(12):
            todo = [i for i in nb if not valid[i]]
            if not todo:
                break
            done = []
            for i in todo:
                good = [j for j in nb[i] if valid[j]]
                if good:
                    for arr in arrs.values():
                        arr[i] = arr[good].mean(0)
                    done.append(i)
            for i in done:
                valid[i] = True
        for nm, arr in arrs.items():
            arr[:, 3] = 1.0
            me.color_attributes[nm].data.foreach_set("color", arr.ravel())
    return nbad, int((~valid).sum())


def carve(hi, thickness, cut, skin, inner):
    hi.data.materials.clear()
    hi.data.materials.append(skin)
    hi.data.materials.append(inner)
    sol = hi.modifiers.new("Shell", "SOLIDIFY")
    sol.thickness = thickness
    sol.offset = -1
    sol.use_even_offset = False  # even offset folds the inner shell on the fine skin detail -> boolean drops it
    sol.material_offset = 1
    apply_mods(hi)
    if cut:
        b = hi.modifiers.new("Carve", "BOOLEAN")
        b.operation = "DIFFERENCE"
        b.solver = "EXACT"
        b.object = cut
        b.material_mode = "TRANSFER"
        apply_mods(hi)
        repair_attrs(hi)
        # the knife edge is SHARP: cut walls flat, edges between skin/inner and cut walls split. Smooth shading across
        # it baked a sawtooth band of tilted normals around every hole.
        bm = bmesh.new()
        bm.from_mesh(hi.data)
        for f in bm.faces:
            f.smooth = f.material_index != 2
        for e in bm.edges:
            lf = e.link_faces
            if len(lf) == 2 and lf[0].material_index != lf[1].material_index:
                e.smooth = False
        bm.to_mesh(hi.data)
        bm.free()
    return hi


def stem_sculpt(name, L, r0, seed):
    rng = random.Random(seed)
    off = Vector((rng.uniform(-40, 40), rng.uniform(-40, 40), rng.uniform(-40, 40)))
    n, m = 150, 72
    lean = rng.uniform(0.26, 0.32)
    path = lambda t: Vector((lean * L * t * t, 0.10 * L * math.sin(math.pi * t) * 0.6, L * t * (1 - 0.1 * t)))
    bm = bmesh.new()
    rings, cols = [], []
    for i in range(n + 1):
        t = i / n
        c = path(t)
        T = (path(min(1, t + 0.01)) - path(max(0, t - 0.01))).normalized()
        Nn = Vector((0, 1, 0)).cross(T).normalized()
        B = T.cross(Nn)
        r = r0 * (1 + 0.9 * math.exp(-(t / 0.1) ** 2)) * (1 - 0.28 * t) * (1 + 0.07 * math.exp(-((t - 0.97) / 0.04) ** 2))
        amp = 0.16 + 0.2 * math.exp(-(t / 0.12) ** 2)
        ring = []
        for j in range(m):
            a = 2 * math.pi * j / m
            ridge = (0.5 + 0.5 * math.cos(6 * a + 2.6 * t + 0.35 * math.sin(9 * t))) ** 0.6
            grain = noise.noise(Vector((math.cos(a) * 3, math.sin(a) * 3, t * 26)) + off)
            rr = r * (1 - amp + amp * ridge) * (1 + 0.025 * grain)
            p = c + (Nn * math.cos(a) + B * math.sin(a)) * rr
            ring.append(bm.verts.new(p))
            base = mix(lin((84, 98, 42)), lin((128, 116, 62)), smoothstep(0.05, 0.6, t))
            base = mix(base, lin((158, 134, 84)), smoothstep(0.55, 1.0, t))
            col = mix(base, mix(base, lin((210, 190, 130)), 0.5), 0.45 * ridge)
            col = mix(col, lin((60, 52, 26)), 0.35 * (1 - ridge) + 0.2 * max(0.0, grain))
            cols.append(col)
        rings.append(ring)
    for i in range(n):
        for j in range(m):
            a, b = rings[i][j], rings[i][(j + 1) % m]
            c2, d2 = rings[i + 1][(j + 1) % m], rings[i + 1][j]
            bm.faces.new((a, b, c2, d2))
    top_c = path(1.0) - (path(1.0) - path(0.98)).normalized() * r0 * 0.25
    vt = bm.verts.new(top_c)
    cols.append(lin((206, 184, 128)))
    for j in range(m):
        bm.faces.new((rings[n][j], rings[n][(j + 1) % m], vt))
    vb = bm.verts.new(path(0.0) - Vector((0, 0, r0 * 0.5)))
    cols.append(lin((84, 98, 42)))
    for j in range(m):
        bm.faces.new((rings[0][(j + 1) % m], rings[0][j], vb))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    set_colors(me, "Col", cols)
    set_colors(me, "Rough", [(0.78, 0.78, 0.78)] * len(cols))
    for p in me.polygons:
        p.use_smooth = True
    return link(bpy.data.objects.new(name, me))


def pupil(name, W, H, T, loc):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=28, radius=1.0)
    for v in bm.verts:
        x, y, z = v.co
        pinch = max(0.0, 1 - z * z) ** 0.55
        v.co = Vector((x * W / 2 * pinch, y * T / 2, z * H / 2))
    ob = obj_from_bm(bm, name)
    ob.location = loc
    return ob


def inner_materials():
    flesh = mat_noise("Flesh", lin((252, 222, 152)), lin((246, 196, 112)), scale=(1.6, 1.6, 0.25), nscale=0.9,
                      detail=3, rough=0.55, lo=0.3, hi=0.7)
    inner = mat_noise("Inner", lin((255, 204, 100)), lin((238, 152, 54)), scale=(1.2, 1.2, 0.2), nscale=0.5,
                      detail=4, rough=0.7, lo=0.3, hi=0.7, bump=0.25)
    return flesh, inner


# ------------------------------------------------------------------ the giant head
HEAD = dict(R=55.0, Rz=40.0, N=10, depth=0.085, crest=0.45, lumps=0.025, micro=0.003, dtop=0.16, dtop_w=0.38,
            dbot=0.06, seed=31, useg=320, vseg=200)
HEAD_SHELL = 2.6
BLEND_HEAD = os.path.join(HERE, "head.blend")


def eye_centre(R, Rz):
    return (19.0, 15.0)  # viewer coords (studs) - the middle of each eye socket


def build_head():
    sc = fresh(samples=16)
    t0 = __import__("time").time()
    skin = mat_vc("Skin")
    flesh, inner = inner_materials()
    hi = pumpkin_sculpt("Head_hi", HEAD)
    cut = cutter_radial("Cutter", giant_face(), HEAD["R"], HEAD["Rz"], flesh, inner_k=0.75, outer_k=1.3)
    carve(hi, HEAD_SHELL, cut, skin, inner)
    lowP = dict(HEAD, useg=128, vseg=84, micro=0.0)
    lo = pumpkin_sculpt("HeadAll", lowP)
    carve(lo, HEAD_SHELL, cut, skin, inner)
    tri = lo.modifiers.new("Tri", "TRIANGULATE")
    apply_mods(lo)
    for a in list(lo.data.color_attributes):
        lo.data.color_attributes.remove(a)
    cut.hide_render = True
    cut.hide_viewport = True
    t1 = __import__("time").time()
    stem_hi = stem_sculpt("Stem_hi", 17.0, 4.4, 5)
    stem_hi.location = (0.0, -1.0, HEAD["Rz"] * (1 - HEAD["dtop"]) - 3.0)
    stem_hi.data.materials.append(mat_vc("StemMat"))
    # game meshes
    R = HEAD["R"]
    parts = split_faces(lo, {
        "HeadInner": lambda f: f.material_index == 1,
        "HeadFront": lambda f: f.material_index == 2 or f.calc_center_median().y > -0.22 * R,
        "HeadBack": lambda f: True,
    })
    for nm, ob in parts.items():
        if len(ob.data.polygons) > 19800:
            dec = ob.modifiers.new("D", "DECIMATE")
            dec.ratio = 19500 / len(ob.data.polygons)
            apply_mods(ob)
    stem_lo = decimate_copy(stem_hi, "Stem", 2600)
    ex, ez = eye_centre(R, HEAD["Rz"])
    # behind each eye hole: front surface y ~ 47 there; the pupil sits 6 studs deeper (inside the glow)
    pupR = pupil("PupilR", 3.8, 13.0, 1.8, (-ex, 40.0, ez))   # viewer's right eye = world -X
    pupL = pupil("PupilL", 3.8, 13.0, 1.8, (ex, 40.0, ez))
    rep = {"carve_s": round(t1 - t0, 1), "hi_tris": len(hi.data.polygons)}
    sizes = {"HeadFront": 1024, "HeadBack": 512, "HeadInner": 1024}
    for nm, ob in parts.items():
        smart_uv(ob)
        imgs = bake_set(ob, [hi], sizes[nm], nm, cage=0.25, maxray=1.2,
                        ao_strength=0.2 if nm == "HeadInner" else 0.55, ao_dist=6.0)
        pbr_material(ob, nm + "_PBR", imgs)
        rep[nm] = len(ob.data.polygons)
    smart_uv(stem_lo)
    imgs = bake_set(stem_lo, [stem_hi], 512, "Stem", cage=0.08, maxray=0.4, ao_strength=0.5, ao_dist=2.0)
    pbr_material(stem_lo, "Stem_PBR", imgs)
    rep["Stem"] = len(stem_lo.data.polygons)
    for o in (hi, stem_hi):
        o.hide_render = True
        o.hide_viewport = True
    pm = mat_flat("PupilMat", lin((18, 6, 6)), rough=0.2)
    for p in (pupR, pupL):
        p.data.materials.append(pm)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_HEAD)
    rep["total_s"] = round(__import__("time").time() - t0, 1)
    return rep


def render_head():
    bpy.ops.wm.open_mainfile(filepath=BLEND_HEAD)
    sc = review_setup()
    R = HEAD["R"]
    # a stand-in for the in-game fire (particles) so the carving can be judged: a bright core + a point light
    core = link(bpy.data.objects.new("FireCore", bpy.data.meshes.new("fc")))
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=R * 0.62)
    bm.to_mesh(core.data)
    bm.free()
    em = bpy.data.materials.new("Fire")
    em.use_nodes = True
    nt = em.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (1.0, 0.45, 0.08, 1)
    e.inputs["Strength"].default_value = 6.0
    nt.links.new(e.outputs["Emission"], nt.nodes["Material Output"].inputs["Surface"])
    core.data.materials.append(em)
    out = []
    tgt = (0, 0, 4)
    out.append(shoot(os.path.join(HERE, "review_head_front.png"), tgt, (0, 1, 0.12), R * 4.2, lens=50))
    out.append(shoot(os.path.join(HERE, "review_head_34.png"), tgt, (0.75, 1, 0.35), R * 4.0, lens=50))
    out.append(shoot(os.path.join(HERE, "review_head_close.png"), (-14, 40, 10), (-0.2, 1, 0.15), R * 1.1, lens=50))
    out.append(shoot(os.path.join(HERE, "review_head_back.png"), tgt, (-0.4, -1, 0.5), R * 4.0, lens=50))
    return out


def export_head():
    bpy.ops.wm.open_mainfile(filepath=BLEND_HEAD)
    objs = [bpy.data.objects[n] for n in ("HeadFront", "HeadBack", "HeadInner", "Stem", "PupilR", "PupilL")]
    return export_fbx(objs, os.path.join(CDIMP, "HalloweenHead.fbx"))


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["head"]
    rep = {}
    for step in argv:
        if step == "head":
            rep["head"] = build_head()
        elif step == "render":
            rep["render"] = render_head()
        elif step == "export":
            rep["export"] = export_head()
    print("HW_REPORT " + json.dumps(rep))
