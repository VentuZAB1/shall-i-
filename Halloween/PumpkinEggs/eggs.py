# SLINGSHOT Halloween hub - PUMPKIN EGGS + CANDLES (decoration only), 2026-10-12.
#   PumpkinEgg_A / _B / _C : carved, hollow jack-o'-lantern EGGS (the game is about eggs); lit inside in Studio
#                            A = slanted angry eyes + fanged grin, B = sinister slit eyes + zigzag mouth,
#                            C = crazed eyes (one big jagged, one small squint) + wide toothy grin
#   PumpkinEgg_Plain1 / 2  : uncarved egg pumpkins for clusters (deep red-orange; pale "ghost" cream, green-grey grooves)
#   Candles                : 3 melted church candles on a wax puddle
# Headless (one asset per run, each in a fresh file):
#   blender.exe -b --factory-startup --python eggs.py -- egg A | egg B | egg C | plain P1 | plain P2 | candles | review
#   add "fast" before the step for a quick low-res test.
# Pipeline (as pumpkin.py build_head): a dense procedural FIELD is the bake source; the game mesh is a COARSE sampling of
# the SAME field (same seed; the rib grooves fall on vertex columns so the coarse silhouette keeps them), carved with the
# SAME cutter (cutter_planar: radial knife walls square to the skin, planar caps); knife edges sharp. After the boolean,
# repair_attrs() refills the colour attributes the EXACT boolean leaves at 0 on every new cut vertex (that black band was
# the dark serrated rim around the holes). Bakes run per surface group (skin+stem+tendril / cut walls / inner) so a skin
# texel can never take a ray hit from a cut wall; UV islands packed CONVEX so nothing nests inside the face holes.
import sys, os, json, time
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import *  # noqa: F401,F403
from pumpkin import SKIN, grin  # read-only helpers from the worked example
from mathutils import Matrix

OUT = os.path.join(HERE, "PumpkinEggs")
MAPS = os.path.join(OUT, "maps")
WIP = os.path.join(OUT, "wip")
T0 = time.time()
CFG = {"fast": False}


def log(*a):
    print("[eggs %6.1fs]" % (time.time() - T0), *a, flush=True)


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def smax(a, b, k):
    h = max(k - abs(a - b), 0.0) / k
    return max(a, b) + h * h * k * 0.25


def pal(**kw):
    return {k: lin(v) for k, v in kw.items()}


def bl(v):
    """Blender object-space point, rounded (relative to the bounding-box centre = the MeshPart pivot)."""
    return [round(float(v[0]), 3), round(float(v[1]), 3), round(float(v[2]), 3)]


def rb(v):
    """Blender (x, y, z) -> Roblox (X, Y, Z): Blender +Z = Roblox +Y, Blender +Y = Roblox -Z."""
    return [round(float(v[0]), 3), round(float(v[2]), 3), round(-float(v[1]), 3)]


# ------------------------------------------------------------------ palettes
PAL = {
    "A": dict(SKIN),
    "B": pal(crest=(232, 108, 16), light=(255, 156, 46), groove=(146, 44, 8), top=(98, 84, 30),
             bottom=(236, 142, 46), blemish=(158, 108, 54), red=(206, 70, 12), gold=(246, 142, 30)),
    "C": pal(crest=(250, 146, 28), light=(255, 192, 76), groove=(176, 66, 12), top=(116, 102, 40),
             bottom=(246, 172, 62), blemish=(178, 128, 64), red=(230, 102, 18), gold=(255, 172, 46)),
    "P1": pal(crest=(206, 66, 16), light=(236, 108, 36), groove=(112, 26, 8), top=(88, 62, 26),
              bottom=(214, 96, 34), blemish=(146, 84, 46), red=(180, 42, 12), gold=(226, 96, 22)),
    "P2": pal(crest=(234, 214, 172), light=(246, 232, 200), groove=(170, 164, 122), top=(136, 136, 96),
              bottom=(228, 206, 164), blemish=(180, 162, 122), red=(226, 202, 160), gold=(242, 226, 188)),
}
STEMS = {
    "green": dict(base=(66, 86, 34), mid=(108, 100, 52), top=(148, 126, 80), hi=(196, 180, 124), lo=(48, 44, 22),
                  cap=(206, 184, 130)),
    "dark": dict(base=(52, 68, 28), mid=(86, 82, 40), top=(124, 104, 64), hi=(170, 156, 104), lo=(36, 32, 16),
                 cap=(190, 164, 112)),
    "pale": dict(base=(110, 122, 82), mid=(144, 140, 100), top=(170, 158, 120), hi=(214, 206, 170), lo=(78, 78, 54),
                 cap=(214, 200, 160)),
}


# ------------------------------------------------------------------ the pumpkin-egg field
def egg_field(P, pl):
    """Surface point / colour / roughness for a unit direction d. pumpkin.pumpkin_sculpt + egg factor, a flattened
    bottom (it stands on the ground), a fixed rib phase, palette, optional groove streaks and inner scrape marks.
    Same P -> same shape at any sampling resolution."""
    rng = random.Random(P["seed"])
    off = Vector((rng.uniform(-50, 50), rng.uniform(-50, 50), rng.uniform(-50, 50)))
    off2 = Vector((rng.uniform(-50, 50), rng.uniform(-50, 50), rng.uniform(-50, 50)))
    N = P["N"]
    ribvar = [rng.uniform(-1, 1) for _ in range(N)]
    phase = rng.uniform(0, 1)
    phase = P.get("phase", phase)
    R, Rz, eg = P["R"], P["Rz"], P.get("egg", 0.0)
    zb = -P.get("flat", 9.0) * Rz
    fk = P.get("flat_k", 0.2) * Rz
    micro, scrape = P.get("micro", 0.0), P.get("scrape", 0.0)
    streak, samt = P.get("streak"), P.get("streak_amt", 0.0)
    radd = P.get("rough_add", 0.0)

    def f(d):
        th = math.acos(max(-1.0, min(1.0, d.z)))
        ph = math.atan2(d.y, d.x)
        s = math.sin(th)
        u = N * ph / (2 * math.pi) + phase
        k = math.floor(u + 0.5)
        fr = u - k                                   # -0.5 .. 0.5 across a rib (grooves at +-0.5)
        kk = int(k) % N
        rv = ribvar[kk]
        bulge = max(0.0, math.cos(math.pi * fr)) ** P["crest"]
        depth = P["depth"] * (s ** 0.7) * (1 + 0.3 * rv)
        m = 1.0 - depth * (1.0 - bulge)
        m *= 1.0 + 0.03 * rv * s
        m *= 1.0 + P["lumps"] * fbm(d * 1.4 + off, 3)
        if micro:
            stri = noise.noise(Vector((fr * 10.0 + kk * 3.7, th * 2.4, 1.7)))
            m *= 1.0 + micro * (0.9 * stri * s + 0.6 * fbm(d * 24.0 + off2, 3))
        if scrape:                                   # spoon scrapes running down the inner wall
            q = Vector((math.cos(ph) * 2.2 * N, math.sin(ph) * 2.2 * N, th * 1.3)) + off2
            m *= 1.0 + scrape * (noise.noise(q) + 0.5 * noise.noise(q * 2.7))
        w = 1 - eg * d.z                             # egg: narrower top
        x, y = d.x * m * R * w, d.y * m * R * w
        z = d.z * Rz * (1 + 0.45 * (m - 1))
        z -= P["dtop"] * Rz * math.exp(-(th / P["dtop_w"]) ** 2)    # the stem well
        if zb > -Rz:
            z = smax(z, zb, fk)                      # the weight-flattened bottom it stands on
        z += P["dbot"] * Rz * math.exp(-((math.pi - th) / 0.5) ** 2)
        col = mix(pl["groove"], pl["crest"], bulge ** 0.55)
        sk = noise.noise(Vector((fr * 16.0 + kk * 5.1, th * 3.3, 9.1)))
        col = mix(col, pl["light"], 0.42 * smoothstep(0.1, 0.6, sk) * bulge)
        tone = fbm(d * 1.1 + off2, 2)
        col = mix(col, pl["red"] if tone < 0 else pl["gold"], min(1.0, abs(tone) * 0.9))
        col = mix(col, pl["bottom"], 0.45 * smoothstep(2.3, 3.0, th))
        col = mix(col, pl["top"], 0.85 * math.exp(-(th / (P["dtop_w"] * 0.85)) ** 2))
        if streak:                                   # ghost pumpkin: green-grey streaks down the grooves
            sn = 0.5 + 0.5 * noise.noise(Vector((fr * 5.0 + kk * 2.3, th * 4.0, 3.3)) + off)
            col = mix(col, streak, samt * (1 - bulge) ** 1.2 * smoothstep(0.3, 0.7, sn) * s)
        bl = smoothstep(0.55, 0.75, fbm(d * 9.0 + off2 * 0.7, 3)) * P.get("blemish", 1.0)
        col = mix(col, pl["blemish"], 0.3 * bl)
        r = 0.38 + 0.22 * (1 - bulge) + 0.32 * bl + radd
        return Vector((x, y, z)), col, (r, r, r)
    return f


def inner_params(P, t):
    """The cavity wall: the same ribs (same seed and phase, softened) pulled in by the wall thickness t, its own stem
    well (same depth -> the top is t thick) and a flat floor t above the outer bottom."""
    R, Rz = P["R"], P["Rz"]
    Ri, Rzi = R - t, Rz - t
    zb = -P["flat"] * Rz
    return dict(P, R=Ri, Rz=Rzi, depth=P["depth"] * 0.55, lumps=P["lumps"] * 0.8, micro=0.0,
                dtop=P["dtop"] * Rz / Rzi, flat=(-zb - t) / Rzi, dbot=0.0)


def grooves_az(N, phase, useg):
    out = []
    for j in range(useg):
        u = N * j / useg + phase
        if abs((u - math.floor(u)) - 0.5) < 1e-6:
            out.append(round(360.0 * j / useg, 4))
    return out


def pick_seams(N, phase, usegs, wants):
    common = set(grooves_az(N, phase, usegs[0]))
    for u in usegs[1:]:
        common &= set(grooves_az(N, phase, u))
    common = sorted(common)
    assert common, "no groove sits on a vertex column"
    return [min(common, key=lambda a: abs((a - w + 180) % 360 - 180)) for w in wants]


# ------------------------------------------------------------------ mesh helpers
def sphere_surface(field, useg, vseg, flip=False):
    """Own UV-sphere sampling (vertex column j at azimuth 2 pi j / useg) -> (V, F, C, Rr)."""
    V, C, Rr = [], [], []

    def add(d):
        p, c, r = field(d)
        V.append(p)
        C.append(c)
        Rr.append(r)
        return len(V) - 1

    top = add(Vector((0.0, 0.0, 1.0)))
    rings = []
    for i in range(1, vseg):
        th = math.pi * i / vseg
        ring = []
        for j in range(useg):
            ph = 2 * math.pi * j / useg
            ring.append(add(Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)))))
        rings.append(ring)
    bot = add(Vector((0.0, 0.0, -1.0)))
    F = []
    for j in range(useg):
        F.append((top, rings[0][j], rings[0][(j + 1) % useg]))
    for a, b in zip(rings[:-1], rings[1:]):
        for j in range(useg):
            jn = (j + 1) % useg
            F.append((a[j], b[j], b[jn], a[jn]))
    for j in range(useg):
        F.append((bot, rings[-1][(j + 1) % useg], rings[-1][j]))
    if flip:
        F = [tuple(reversed(f)) for f in F]
    return V, F, C, Rr


def make_obj(name, V, F, C=None, Rr=None, mats=(), fmat=None, recalc=False, smooth=True, extra=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in V], [], [tuple(f) for f in F])
    me.update()
    if C:
        set_colors(me, "Col", C)
    if Rr:
        set_colors(me, "Rough", Rr)
    for nm, vals in (extra or {}).items():
        set_colors(me, nm, vals)
    for m in mats:
        me.materials.append(m)
    if fmat is not None:
        me.polygons.foreach_set("material_index", fmat)
    ob = link(bpy.data.objects.new(name, me))
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
    if smooth:
        me.shade_smooth()
    return ob


def build_mesh(name, parts, mats):
    """parts: [(V, F, C, Rr, material index, depth value)] -> one object. 'Depth' = 1 on the skin, 0 on the cavity
    wall: the boolean interpolates it onto the cut walls, the flesh shader draws the rind line from it."""
    V, F, C, Rr, fm, D = [], [], [], [], [], []
    for pv, pf, pc, pr, mi, dep in parts:
        o = len(V)
        V += pv
        C += pc
        Rr += pr
        D += [(dep, dep, dep)] * len(pv)
        F += [tuple(i + o for i in f) for f in pf]
        fm += [mi] * len(pf)
    return make_obj(name, V, F, C, Rr, mats=mats, fmat=fm, extra={"Depth": D})


def knife(ob, wall=2):
    """Knife edges sharp: cut walls flat, edges between different surfaces split."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    for f in bm.faces:
        f.smooth = f.material_index != wall
    for e in bm.edges:
        lf = e.link_faces
        if len(lf) == 2 and lf[0].material_index != lf[1].material_index:
            e.smooth = False
    bm.to_mesh(ob.data)
    bm.free()


def repair_attrs(ob, wall=2, names=("Col", "Rough", "Depth")):
    """The EXACT boolean does NOT interpolate point colour attributes onto the new cut vertices: they come out
    (0, 0, 0, 0). On the bake source that is a black, glossy band along every knife edge = the dark serrated rims
    around the holes. Refill each such vertex from its valid neighbours on the same surface (edges of skin / cavity
    faces only, never across a cut wall), ring by ring."""
    me = ob.data
    arrs = {}
    for nm in names:
        a = me.color_attributes.get(nm)
        if a is not None:
            arr = np.empty(len(a.data) * 4, np.float32)
            a.data.foreach_get("color", arr)
            arrs[nm] = arr.reshape(-1, 4)
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


def carve2(ob, cut):
    b = ob.modifiers.new("Carve", "BOOLEAN")
    b.operation = "DIFFERENCE"
    b.solver = "EXACT"
    b.object = cut
    b.material_mode = "TRANSFER"
    apply_mods(ob)
    knife(ob)
    return ob


def euler_holes(ob, shells=2):
    """Two closed shells joined by k tunnels (the carved holes): chi = 2*shells - 2k."""
    me = ob.data
    chi = len(me.vertices) - len(me.edges) + len(me.polygons)
    return (2 * shells - chi) / 2.0


def triangulate(ob):
    t = ob.modifiers.new("Tri", "TRIANGULATE")
    t.quad_method = "BEAUTY"
    t.ngon_method = "BEAUTY"
    apply_mods(ob)


def join(objs, name):
    for o in bpy.context.scene.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = objs[0]
    ob.name = name
    ob.data.name = name
    return ob


def split_copy(ob, name, keep):
    """A copy of ob with only the faces where keep(face, material names) is true (UVs, flags kept)."""
    names = [m.name if m else "" for m in ob.data.materials]
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    dead = [f for f in bm.faces if not keep(f, names)]
    bmesh.ops.delete(bm, geom=dead, context="FACES")
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in ob.data.materials:
        me.materials.append(m)
    o = link(bpy.data.objects.new(name, me))
    o.matrix_world = ob.matrix_world.copy()
    return o


def bbox(ob):
    vs = np.empty(len(ob.data.vertices) * 3, np.float32)
    ob.data.vertices.foreach_get("co", vs)
    vs = vs.reshape(-1, 3)
    return vs.min(0), vs.max(0)


def recentre(lo, others):
    mn, mx = bbox(lo)
    c = Vector(((mn + mx) / 2).tolist())
    lo.data.transform(Matrix.Translation(-c))
    lo.data.update()
    for o in others:
        o.location -= c
    return c, Vector((mx - mn).tolist())


def strip_colors(ob):
    for a in list(ob.data.color_attributes):
        ob.data.color_attributes.remove(a)


def tube(pts, radii, nside, cols, rough):
    """Closed tube along a polyline (parallel-transport frames, capped ends)."""
    n = len(pts)
    T = [(pts[min(n - 1, i + 1)] - pts[max(0, i - 1)]).normalized() for i in range(n)]
    ref = Vector((0, 0, 1)) if abs(T[0].z) < 0.9 else Vector((1, 0, 0))
    Nn = T[0].cross(ref).normalized()
    V, F, C, Rr, rings = [], [], [], [], []
    for i in range(n):
        Nn = (Nn - T[i] * Nn.dot(T[i])).normalized()
        B = T[i].cross(Nn)
        ring = []
        for j in range(nside):
            a = 2 * math.pi * j / nside
            V.append(pts[i] + (Nn * math.cos(a) + B * math.sin(a)) * radii[i])
            C.append(cols[i])
            Rr.append((rough, rough, rough))
            ring.append(len(V) - 1)
        rings.append(ring)
    for i in range(n - 1):
        for j in range(nside):
            jn = (j + 1) % nside
            F.append((rings[i][j], rings[i][jn], rings[i + 1][jn], rings[i + 1][j]))
    V.append(pts[0] - T[0] * radii[0] * 0.5)
    C.append(cols[0])
    Rr.append((rough,) * 3)
    s0 = len(V) - 1
    V.append(pts[-1] + T[-1] * radii[-1] * 0.8)
    C.append(cols[-1])
    Rr.append((rough,) * 3)
    s1 = len(V) - 1
    for j in range(nside):
        jn = (j + 1) % nside
        F.append((rings[0][jn], rings[0][j], s0))
        F.append((rings[-1][j], rings[-1][jn], s1))
    return V, F, C, Rr


# ------------------------------------------------------------------ stem + tendril
def gnarly_stem(L, r0, seed, base, sp, detail):
    """pumpkin.stem_sculpt made gnarly: a bent, twisted, knotted stem, 5 deep spiralling ridges, a flared foot that
    melts into the ribs, a dry broken top. detail=False -> the coarse game version of the same stem."""
    sp = {k: lin(v) for k, v in sp.items()}
    rng = random.Random(seed)
    off = Vector((rng.uniform(-40, 40), rng.uniform(-40, 40), rng.uniform(-40, 40)))
    az = rng.uniform(0, 2 * math.pi)
    lean = rng.uniform(0.30, 0.45)
    wob = rng.uniform(0.05, 0.09)
    tw = rng.uniform(0.8, 1.6)
    knots = [(rng.uniform(0.3, 0.72), rng.uniform(0.08, 0.14), rng.uniform(0, 6.283)) for _ in range(2)]
    ld = Vector((math.cos(az), math.sin(az), 0.0))
    sd = Vector((-math.sin(az), math.cos(az), 0.0))
    base = Vector(base)

    def path(t):
        return (base + ld * (lean * L * t * t) + sd * (wob * L * math.sin(2.4 * math.pi * t))
                + Vector((0.0, 0.0, L * t * (1 - 0.12 * t))))

    if detail:
        ts, m = [i / 110 for i in range(111)], 56
    else:
        ts, m = [0.0, 0.05, 0.11, 0.19, 0.3, 0.42, 0.55, 0.68, 0.8, 0.9, 0.97, 1.0], 10
    V, C, Rr, F, rings = [], [], [], [], []
    for t in ts:
        c = path(t)
        T = (path(min(1.0, t + 0.01)) - path(max(0.0, t - 0.01))).normalized()
        Nn = Vector((0, 1, 0)).cross(T).normalized()
        B = T.cross(Nn)
        r = (r0 * (1 + 0.95 * math.exp(-(t / 0.11) ** 2)) * (1 - 0.25 * t)
             * (1 + 0.1 * math.exp(-((t - 0.97) / 0.04) ** 2)))
        amp = 0.2 + 0.2 * math.exp(-(t / 0.12) ** 2)
        bc = mix(sp["base"], sp["mid"], smoothstep(0.05, 0.6, t))
        bc = mix(bc, sp["top"], smoothstep(0.55, 1.0, t))
        ring = []
        for j in range(m):
            a = 2 * math.pi * j / m
            kn = 1.0 + sum(ka * math.exp(-((t - tk) / 0.05) ** 2) * (0.55 + 0.45 * math.cos(a - pa))
                           for tk, ka, pa in knots)
            ridge = (0.5 + 0.5 * math.cos(5 * a + tw * t * 2.2 + 0.4 * math.sin(8 * t))) ** 0.6
            grain = noise.noise(Vector((math.cos(a) * 3, math.sin(a) * 3, t * 30)) + off) if detail else 0.0
            rr = r * kn * (1 - amp + amp * ridge) * (1 + 0.035 * grain)
            V.append(c + (Nn * math.cos(a) + B * math.sin(a)) * rr)
            col = mix(bc, mix(bc, sp["hi"], 0.5), 0.45 * ridge)
            col = mix(col, sp["lo"], 0.35 * (1 - ridge) + 0.2 * max(0.0, grain))
            if detail:
                spk = smoothstep(0.3, 0.6, noise.noise(Vector((math.cos(a) * 6, math.sin(a) * 6, t * 40)) + off * 1.3))
                col = mix(col, sp["lo"], 0.5 * spk)
            C.append(col)
            Rr.append((0.8, 0.8, 0.8))
            ring.append(len(V) - 1)
        rings.append(ring)
    for i in range(len(rings) - 1):
        for j in range(m):
            jn = (j + 1) % m
            F.append((rings[i][j], rings[i][jn], rings[i + 1][jn], rings[i + 1][j]))
    T1 = (path(1.0) - path(0.98)).normalized()
    V.append(path(1.0) - T1 * r0 * 0.3)          # the dry broken end, a little sunken
    C.append(sp["cap"])
    Rr.append((0.85, 0.85, 0.85))
    vt = len(V) - 1
    for j in range(m):
        F.append((rings[-1][j], rings[-1][(j + 1) % m], vt))
    V.append(path(0.0) - Vector((0, 0, r0 * 0.6)))
    C.append(sp["base"])
    Rr.append((0.8, 0.8, 0.8))
    vb = len(V) - 1
    for j in range(m):
        F.append((rings[0][(j + 1) % m], rings[0][j], vb))
    return V, F, C, Rr


def tendril_pts(field, P, tdef, n1, n2):
    """A vine tendril: born under the stem foot, runs down the shoulder on the skin, then lifts off in a corkscrew."""
    R, Rz = P["R"], P["Rz"]

    def surf(th, az, lift):
        d = Vector((math.sin(th) * math.cos(az), math.sin(th) * math.sin(az), math.cos(th)))
        p = field(d)[0]
        nrm = Vector((p.x / R ** 2, p.y / R ** 2, p.z / Rz ** 2)).normalized()
        return p + nrm * lift, nrm

    a0, sgn = math.radians(tdef[0]), tdef[1]
    pts = []
    nE = None
    for i in range(n1):
        t = i / (n1 - 1)
        p, nE = surf(0.13 + 0.80 * t, a0 + sgn * (0.30 * t + 0.06 * math.sin(3.5 * t)), 0.05 + 0.02 * math.sin(math.pi * t))
        pts.append(p)
    E = pts[-1]
    Td = (pts[-1] - pts[-2]).normalized()
    A = (Td * 0.35 + nE * 0.95).normalized()
    B2 = (Td - A * Td.dot(A)).normalized()
    B1 = B2.cross(A).normalized()
    rho0, turns, pitch = 0.24, 2.5, 0.12
    Cc = E - B1 * rho0
    for i in range(1, n2 + 1):
        t = i / n2
        phi = 2 * math.pi * turns * t
        rho = rho0 * (1 - 0.6 * t)
        pts.append(Cc + (B1 * math.cos(phi) + B2 * math.sin(phi)) * rho + A * (pitch * phi / (2 * math.pi)))
    return pts


def tendril_mesh(pts, nside):
    n = len(pts)
    radii = [0.062 - 0.028 * (i / (n - 1)) for i in range(n)]
    cols = [mix(lin((84, 108, 40)), lin((146, 156, 74)), (i / (n - 1)) ** 1.5) for i in range(n)]
    return tube(pts, radii, nside, cols, 0.55)


# ------------------------------------------------------------------ faces (viewer coords: x = viewer's right, z up)
def chain(*segs):
    out = []
    for s in segs:
        out += s[:-1]
    return out


def mirror(pts):
    return [(-x, z) for x, z in reversed(pts)]


def clean(pts, eps=2e-3):
    out = []
    for p in pts:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > eps:
            out.append(p)
    while len(out) > 3 and abs(out[0][0] - out[-1][0]) + abs(out[0][1] - out[-1][1]) <= eps:
        out.pop()
    return out


def lens(a, b, up, down, n):
    """A sharp-ended lens (slit eye) from a to b; up/down = how far the control points bulge each side."""
    mx, mz = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dz = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dz)
    px, pz = -dz / L, dx / L
    return chain(quad_bezier(a, (mx + px * up, mz + pz * up), b, n), quad_bezier(b, (mx - px * down, mz - pz * down), a, n))


def face_A():
    """Slanted angry eyes (scowling top edge, sharp inner corner) + triangle nose + fanged grin."""
    eye = chain(quad_bezier((0.20, 0.50), (0.95, 0.86), (1.58, 1.48), 12),
                quad_bezier((1.58, 1.48), (1.70, 0.95), (1.34, 0.62), 6),
                quad_bezier((1.34, 0.62), (0.80, 0.20), (0.20, 0.50), 10))
    nose = chain(quad_bezier((0.0, 0.30), (-0.05, 0.0), (-0.25, -0.26), 6),
                 quad_bezier((-0.25, -0.26), (0.0, -0.17), (0.25, -0.26), 5),
                 quad_bezier((0.25, -0.26), (0.05, 0.0), (0.0, 0.30), 6))
    mouth = grin(1.70, (-0.72, 0.45), (-1.95, 1.15),
                 top_teeth=[(-1.15, 0.30, 0.05, 0.30), (-0.48, 0.40, 0.04, 0.72), (0.48, 0.40, 0.04, 0.72),
                            (1.15, 0.30, 0.05, 0.30)],
                 bot_teeth=[(-0.88, 0.30, 0.05, 0.36), (0.0, 0.34, 0.05, 0.42), (0.88, 0.30, 0.05, 0.36)],
                 corner_up=0.25, step=0.06, jit=0.012, seed=3)
    return {"EyeR": eye, "EyeL": mirror(eye), "Nose": nose, "Mouth": mouth}


def zigzag_mouth(W, base, curve, n, amp, th, seed):
    """A jagged lightning-bolt mouth: a band following a zigzag centre line that curls up at the corners."""
    rng = random.Random(seed)
    xs = [-W + 2 * W * i / n for i in range(n + 1)]
    cl = []
    for i, x in enumerate(xs):
        q = x / W
        a = amp * (0.7 + 0.3 * math.cos(math.pi * q)) * (1 + rng.uniform(-0.15, 0.15))
        cl.append(base + curve * q * q + (a if i % 2 == 0 else -a))
    thick = [th * (1 - 0.45 * (x / W) ** 2) for x in xs]
    top = [(x + rng.uniform(-0.015, 0.015), z + t / 2) for x, z, t in zip(xs, cl, thick)]
    bot = [(x + rng.uniform(-0.015, 0.015), z - t / 2) for x, z, t in zip(xs, cl, thick)]
    rc, lc = (W + 0.20, base + curve + 0.16), (-W - 0.20, base + curve + 0.16)
    return [rc] + top[::-1] + [lc] + bot


def face_B():
    """Narrow sinister slit eyes slanted down to a dagger nose, a zigzag jagged mouth."""
    eye = lens((0.24, 0.58), (1.74, 1.16), 0.30, 0.22, 14)
    nose = chain(quad_bezier((-0.20, 0.10), (0.0, 0.02), (0.20, 0.10), 4),
                 quad_bezier((0.20, 0.10), (0.05, -0.12), (0.0, -0.38), 5),
                 quad_bezier((0.0, -0.38), (-0.05, -0.12), (-0.20, 0.10), 5))
    mouth = zigzag_mouth(W=1.85, base=-1.25, curve=0.50, n=10, amp=0.22, th=0.42, seed=5)
    return {"EyeR": eye, "EyeL": mirror(eye), "Nose": nose, "Mouth": mouth}


def face_C():
    """Crazed: one big lopsided staring eye (viewer's left) with a hard brow cut slanting down to the nose, one small
    squint (viewer's right), a crooked nose, a wide grin packed with sharp shark teeth."""
    rng = random.Random(9)
    cx, cz, rx, rz = -0.95, 0.80, 0.62, 0.62
    a0, a1 = (-0.36, 1.00), (-1.66, 1.50)              # the brow line (inner end low = angry)
    slope = (a1[1] - a0[1]) / (a1[0] - a0[0])
    big = []
    n = 30
    for k in range(n):
        a = 2 * math.pi * k / n
        r = 1.0 + 0.07 * math.sin(2 * a + 0.6) + 0.04 * math.sin(5 * a + 1.3) + rng.uniform(-0.02, 0.02)
        x, z = cx + math.cos(a) * rx * r, cz + math.sin(a) * rz * r
        big.append((x, min(z, a0[1] + slope * (x - a0[0]))))
    small = lens((0.50, 0.86), (1.32, 1.30), 0.22, 0.12, 10)
    nose = chain(quad_bezier((0.06, 0.22), (-0.10, 0.0), (-0.24, -0.24), 4),
                 quad_bezier((-0.24, -0.24), (0.0, -0.25), (0.22, -0.30), 4),
                 quad_bezier((0.22, -0.30), (0.12, -0.04), (0.06, 0.22), 4))
    mouth = grin(1.95, (-0.66, 0.66), (-2.0, 1.45),
                 top_teeth=[(x, 0.34, 0.03, 0.36) for x in (-1.33, -0.81, -0.27, 0.27, 0.81, 1.33)],
                 bot_teeth=[(x, 0.32, 0.03, 0.34) for x in (-1.07, -0.54, 0.0, 0.54, 1.07)],
                 corner_up=0.35, step=0.06, jit=0.014, seed=7)
    return {"EyeBig": big, "EyeSmall": small, "Nose": nose, "Mouth": mouth}


def cutter_planar(name, outlines, R, Rz, flesh, egg=0.0):
    """pumpkin.cutter_radial with PLANAR caps. The walls are the same (rays from the centre through the outline on
    the egg front -> knife walls square to the skin), but each cap is the central projection of the outline onto a
    plane y = const (inside the cavity / in front of the skin). cutter_radial scales the outline onto a curved
    surface, so the ear-clipped cap of a long concave outline (B's zigzag mouth) is far from planar: its chord
    triangles cut through the island's own walls and the EXACT boolean wiped most of the shell."""
    bm = bmesh.new()
    for pts in outlines.values():
        P = []
        for vx, vz in pts:
            x, z = -vx, vz
            w = 1 - egg * max(-1.0, min(1.0, z / Rz))
            q = 1 - (x / (R * w)) ** 2 - (z / Rz) ** 2
            P.append(Vector((x, R * w * math.sqrt(max(0.02, q)), z)))
        yi, yo = 0.5 * min(p.y for p in P), 1.35 * max(p.y for p in P)
        b = bmesh.new()
        inner = [b.verts.new(p * (yi / p.y)) for p in P]
        outer = [b.verts.new(p * (yo / p.y)) for p in P]
        n = len(P)
        b.faces.new(inner)
        b.faces.new(list(reversed(outer)))
        for i in range(n):
            j = (i + 1) % n
            b.faces.new((inner[i], outer[i], outer[j], inner[j]))
        bmesh.ops.triangulate(b, faces=b.faces, quad_method="BEAUTY", ngon_method="EAR_CLIP")
        bmesh.ops.recalc_face_normals(b, faces=b.faces)
        if b.calc_volume(signed=True) < 0:
            bmesh.ops.reverse_faces(b, faces=b.faces)
        tmp = bpy.data.meshes.new("_island")
        b.to_mesh(tmp)
        b.free()
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    ob = obj_from_bm(bm, name, smooth=False)
    ob.data.materials.append(flesh)
    return ob


# ------------------------------------------------------------------ materials for the sculpt
def mat_inner():
    return mat_noise("Inner", lin((252, 200, 112)), lin((228, 140, 48)), scale=(9.0, 9.0, 1.4), nscale=1.0,
                     detail=6, rough=0.72, lo=0.3, hi=0.72, bump=0.35)


def mat_flesh():
    """Cut walls: pale fibrous flesh, a thin deep-orange rind line along the outer knife edge (from 'Depth')."""
    m = mat_noise("Flesh", lin((252, 218, 132)), lin((242, 176, 82)), scale=(14.0, 14.0, 14.0), nscale=1.0,
                  detail=5, rough=0.55, lo=0.32, hi=0.7, bump=0.15)
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    base = bsdf.inputs["Base Color"].links[0].from_socket
    at = nt.nodes.new("ShaderNodeVertexColor")
    at.layer_name = "Depth"
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(at.outputs["Color"], sep.inputs["Color"])
    rind = nt.nodes.new("ShaderNodeMapRange")
    rind.inputs["From Min"].default_value = 0.80
    rind.inputs["From Max"].default_value = 0.93
    rind.interpolation_type = "SMOOTHSTEP"
    nt.links.new(sep.outputs["Red"], rind.inputs["Value"])
    deep = nt.nodes.new("ShaderNodeMapRange")              # the pulp side of the wall is a little more orange
    deep.inputs["From Min"].default_value = 0.25
    deep.inputs["From Max"].default_value = 0.0
    nt.links.new(sep.outputs["Red"], deep.inputs["Value"])
    def sk(socks, ident):
        return [s for s in socks if s.identifier == ident][0]

    m1 = nt.nodes.new("ShaderNodeMix")
    m1.data_type = "RGBA"
    nt.links.new(deep.outputs["Result"], sk(m1.inputs, "Factor_Float"))
    nt.links.new(base, sk(m1.inputs, "A_Color"))
    sk(m1.inputs, "B_Color").default_value = (*lin((244, 156, 56)), 1)
    m2 = nt.nodes.new("ShaderNodeMix")
    m2.data_type = "RGBA"
    nt.links.new(rind.outputs["Result"], sk(m2.inputs, "Factor_Float"))
    nt.links.new(sk(m1.outputs, "Result_Color"), sk(m2.inputs, "A_Color"))
    sk(m2.inputs, "B_Color").default_value = (*lin((214, 104, 22)), 1)
    nt.links.new(sk(m2.outputs, "Result_Color"), bsdf.inputs["Base Color"])
    return m


# ------------------------------------------------------------------ UVs
def uv_layout(ob, seam_az, abf_mats, shrink, angle=55):
    """Smart UV for everything, then the skin / cavity wall re-unwrapped ANGLE_BASED as lunes cut along rib grooves
    (seam_az, degrees; the vertices of a groove column keep their azimuth through the boolean), islands scaled to
    equal texel density, `shrink` islands made smaller (cavity wall), packed."""
    me = ob.data
    names = [m.name for m in me.materials]
    abf_idx = {i for i, n in enumerate(names) if n in abf_mats}
    bm = bmesh.new()
    bm.from_mesh(me)

    def on(v, s):
        x, y = v.co.x, v.co.y
        if x * x + y * y < 1e-10:
            return True
        a = math.degrees(math.atan2(y, x))
        return abs((a - s + 180) % 360 - 180) < 0.05

    nseam = 0
    for e in bm.edges:
        mats = {f.material_index for f in e.link_faces}
        e.seam = False
        if len(mats) > 1:
            e.seam = True
        elif mats and mats <= abf_idx:
            for s in seam_az:
                if on(e.verts[0], s) and on(e.verts[1], s):
                    e.seam = True
                    nseam += 1
                    break
    bm.to_mesh(me)
    bm.free()
    sc = bpy.context.scene
    sc.tool_settings.use_uv_select_sync = True
    only(ob)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(angle), island_margin=0.004)
    bpy.ops.object.mode_set(mode="OBJECT")
    log("  uv smart done")
    if abf_idx:
        for p in me.polygons:
            p.select = p.material_index in abf_idx
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.uv.unwrap(method="ANGLE_BASED", margin=0.004)
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.average_islands_scale()
    bpy.ops.object.mode_set(mode="OBJECT")
    if shrink:
        uv = me.uv_layers.active.data
        for p in me.polygons:
            k = shrink.get(names[p.material_index])
            if k:
                for li in p.loop_indices:
                    uv[li].uv = uv[li].uv * k
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    # CONVEX: never nest a small island inside another island's holes (the face holes of the front lune) - filtering
    # then bled the stem's dark texels into the skin right at the knife edge
    log("  uv unwrap+average done, packing")
    bpy.ops.uv.pack_islands(rotate=True, rotate_method="CARDINAL", margin_method="FRACTION", margin=0.006,
                            shape_method="CONVEX")
    bpy.ops.object.mode_set(mode="OBJECT")
    return nseam


# ------------------------------------------------------------------ bakes (per surface group)
def bake_groups(groups, size, prefix, ao_strength, ao_dist):
    """groups: [(lo part, [hi parts], cage, maxray)]; the lo parts share one UV layout. Each lo part only matches
    rays against ITS OWN hi parts. Coverage (EMIT of the lo itself) and hit masks (EMIT of white hi) are baked with
    margin 0; covered texels that missed get values grown from their own group's hits; the margin is dilated at the
    end. AO sees the whole scene (every hi part renders; the lo parts are invisible to shadow/diffuse rays)."""
    sc = bpy.context.scene
    sc.world.light_settings.distance = ao_dist
    shp = (size, size, 4)
    acc = {k: np.zeros(shp, np.float32) for k in ("albedo", "normal", "rough", "ao")}
    owned = np.zeros((size, size), bool)
    zero = np.zeros(size * size * 4, np.float32)
    t_lin = bpy.data.images.new(prefix + "_tmpL", size, size, alpha=False)
    t_lin.colorspace_settings.name = "Non-Color"
    t_rgb = bpy.data.images.new(prefix + "_tmpC", size, size, alpha=False)
    bmat = bpy.data.materials.new(prefix + "_bake")
    bmat.use_nodes = True
    tex = bmat.node_tree.nodes.new("ShaderNodeTexImage")
    bmat.node_tree.nodes.active = tex
    cmat = bpy.data.materials.new(prefix + "_cov")
    cmat.use_nodes = True
    nt = cmat.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1, 1, 1, 1)
    em.inputs["Strength"].default_value = 1.0
    nt.links.new(em.outputs["Emission"], nt.nodes["Material Output"].inputs["Surface"])
    ctex = nt.nodes.new("ShaderNodeTexImage")
    ctex.image = t_lin
    nt.nodes.active = ctex

    def bake(node, img, kind, s2a, cage=0.0, maxray=0.0, **kw):
        node.image = img
        img.pixels.foreach_set(zero)
        bpy.ops.object.bake(type=kind, use_selected_to_active=s2a, cage_extrusion=cage, max_ray_distance=maxray,
                            margin=0, use_clear=False, **kw)
        a = np.empty(size * size * 4, np.float32)
        img.pixels.foreach_get(a)
        return a.reshape(shp)

    def emit_white(his, on, saved):
        if on:
            for h in his:
                for m in h.data.materials:
                    if m and m.use_nodes:
                        for n in m.node_tree.nodes:
                            if n.type == "BSDF_PRINCIPLED":
                                ls = [l for l in m.node_tree.links if l.to_socket == n.inputs["Emission Color"]]
                                saved.append((m, n, tuple(n.inputs["Emission Color"].default_value),
                                              n.inputs["Emission Strength"].default_value,
                                              [(l.from_socket, l.to_socket) for l in ls]))
                                for l in ls:
                                    m.node_tree.links.remove(l)
                                n.inputs["Emission Color"].default_value = (1, 1, 1, 1)
                                n.inputs["Emission Strength"].default_value = 1.0
        else:
            for m, n, col, st, ls in saved:
                n.inputs["Emission Color"].default_value = col
                n.inputs["Emission Strength"].default_value = st
                for a, b in ls:
                    m.node_tree.links.new(a, b)
            saved.clear()

    stats = {}
    for lo, his, cage, maxray in groups:
        for attr in ("visible_shadow", "visible_diffuse", "visible_glossy", "visible_transmission"):
            setattr(lo, attr, False)
    for lo, his, cage, maxray in groups:
        for o in sc.objects:
            o.select_set(False)
        lo.select_set(True)
        bpy.context.view_layer.objects.active = lo
        lo.data.materials.clear()
        lo.data.materials.append(cmat)
        cov = bake(ctex, t_lin, "EMIT", False)[..., 0] > 0.5
        lo.data.materials.clear()
        lo.data.materials.append(bmat)
        for h in his:
            h.hide_render = False
            h.select_set(True)
        out = {"normal": bake(tex, t_lin, "NORMAL", True, cage, maxray, normal_space="TANGENT"),
               "ao": bake(tex, t_lin, "AO", True, cage, maxray),
               "albedo": bake(tex, t_rgb, "DIFFUSE", True, cage, maxray, pass_filter={"COLOR"}),
               "rough": bake(tex, t_lin, "ROUGHNESS", True, cage, maxray)}
        saved = []
        emit_white(his, True, saved)
        hit = bake(tex, t_lin, "EMIT", True, cage, maxray)[..., 0] > 0.5
        emit_white(his, False, saved)
        hit &= cov
        if CFG.get("debug"):
            np.savez_compressed(os.path.join(WIP, "dbg_%s.npz" % lo.name), cov=cov, hit=hit, albedo=out["albedo"],
                                rough=out["rough"], ao=out["ao"])
        for k, arr in out.items():
            filled = fill_misses(arr, hit, iters=6)
            acc[k][cov] = filled[cov]
        owned |= cov
        stats[lo.name] = {"texels": int(cov.sum()), "miss": round(float(1 - hit.sum() / max(1, cov.sum())), 4)}
        log("  baked", lo.name, stats[lo.name])
    for k in acc:
        acc[k] = fill_misses(acc[k], owned, iters=10)
    if CFG.get("debug"):
        np.savez_compressed(os.path.join(WIP, "dbg_final_%s.npz" % prefix), owned=owned,
                            **{k: v for k, v in acc.items()})
    acc["albedo"][..., :3] *= (1 - ao_strength) + ao_strength * acc["ao"][..., :1]
    imgs = {}
    for k, cs in (("albedo", "sRGB"), ("normal", "Non-Color"), ("rough", "Non-Color"), ("ao", "Non-Color")):
        acc[k][..., 3] = 1.0
        img = bpy.data.images.new(prefix + "_" + k, size, size, alpha=False)
        img.colorspace_settings.name = cs
        img.pixels.foreach_set(acc[k].ravel())
        save_png(img, os.path.join(MAPS, f"{prefix}_{k}.png"))
        imgs[k] = img
    for i in (t_lin, t_rgb):
        bpy.data.images.remove(i)
    imgs["stats"] = stats
    return imgs


# ------------------------------------------------------------------ the carved eggs
EGGS = {
    "A": dict(P=dict(N=8, R=2.55, Rz=3.35, egg=0.17, depth=0.085, crest=0.45, lumps=0.025, micro=0.003, dtop=0.08,
                     dtop_w=0.30, dbot=0.03, flat=0.92, flat_k=0.18, seed=101, phase=0.0),
              useg=(384, 48), vseg=(256, 36), iuseg=(192, 32), ivseg=(128, 24), shell=0.28, face=face_A, pal="A",
              stem=dict(L=0.95, r0=0.19, seed=17, sp="green"), tendril=(8, -1)),
    "B": dict(P=dict(N=9, R=2.6, Rz=3.5, egg=0.18, depth=0.08, crest=0.5, lumps=0.028, micro=0.003, dtop=0.07,
                     dtop_w=0.28, dbot=0.03, flat=0.92, flat_k=0.18, seed=202, phase=0.75),
              useg=(360, 72), vseg=(256, 32), iuseg=(180, 36), ivseg=(128, 24), shell=0.30, face=face_B, pal="B",
              stem=dict(L=1.05, r0=0.2, seed=29, sp="dark"), tendril=(166, 1)),
    "C": dict(P=dict(N=8, R=2.65, Rz=3.3, egg=0.15, depth=0.09, crest=0.42, lumps=0.03, micro=0.003, dtop=0.085,
                     dtop_w=0.32, dbot=0.03, flat=0.91, flat_k=0.18, seed=303, phase=0.0),
              useg=(384, 48), vseg=(256, 36), iuseg=(192, 32), ivseg=(128, 24), shell=0.27, face=face_C, pal="C",
              stem=dict(L=0.85, r0=0.2, seed=41, sp="green"), tendril=(12, -1)),
}
TRI_LIMIT_EGG = 9000


def build_egg(key):
    E = EGGS[key]
    P = E["P"]
    name = "PumpkinEgg_" + key
    fast = CFG["fast"]
    hs = 2 if fast else 1
    size = 256 if fast else 1024
    fresh(samples=8 if fast else 24)
    pl = PAL[E["pal"]]
    skin, inner_m, flesh = mat_vc("Skin"), mat_inner(), mat_flesh()
    stem_m, tend_m = mat_vc("StemMat"), mat_vc("TendrilMat")
    Pi = inner_params(P, E["shell"])
    outl = {k: clean(v) for k, v in E["face"]().items()}
    cut = cutter_planar("Cutter", outl, P["R"], P["Rz"], flesh, egg=P["egg"])
    hi = build_mesh("Shell_hi", [
        sphere_surface(egg_field(P, pl), E["useg"][0] // hs, E["vseg"][0] // hs) + (0, 1.0),
        sphere_surface(egg_field(dict(Pi, scrape=0.006), pl), E["iuseg"][0] // hs, E["ivseg"][0] // hs, flip=True)
        + (1, 0.0)], [skin, inner_m])
    log(name, "hi sculpt", len(hi.data.polygons))
    carve2(hi, cut)
    log(name, "repaired cut-vertex attributes (fixed, left):", repair_attrs(hi))
    f_lo = egg_field(dict(P, micro=0.0), pl)
    lo = build_mesh(name, [sphere_surface(f_lo, E["useg"][1], E["vseg"][1]) + (0, 1.0),
                           sphere_surface(egg_field(Pi, pl), E["iuseg"][1], E["ivseg"][1], flip=True) + (1, 0.0)],
                    [skin, inner_m])
    carve2(lo, cut)
    holes = {"hi": euler_holes(hi), "lo": euler_holes(lo), "cut": len(outl)}
    log(name, "carved", len(hi.data.polygons), "hi faces; holes", holes)
    if not (holes["hi"] == holes["lo"] == len(outl)):
        raise RuntimeError("a hole did not open: %s" % holes)
    top = f_lo(Vector((0.0, 0.0, 1.0)))[0]
    base = (0.0, 0.0, top.z - 0.06)
    S = E["stem"]
    stem_hi = make_obj("Stem_hi", *gnarly_stem(S["L"], S["r0"], S["seed"], base, STEMS[S["sp"]], True),
                       mats=[stem_m], recalc=True)
    stem_lo = make_obj("Stem_lo", *gnarly_stem(S["L"], S["r0"], S["seed"], base, STEMS[S["sp"]], False),
                       mats=[stem_m], recalc=True)
    tend_hi = make_obj("Tendril_hi", *tendril_mesh(tendril_pts(f_lo, P, E["tendril"], 70, 150), 12),
                       mats=[tend_m], recalc=True)
    tend_lo = make_obj("Tendril_lo", *tendril_mesh(tendril_pts(f_lo, P, E["tendril"], 8, 22), 5),
                       mats=[tend_m], recalc=True)
    lo = join([lo, stem_lo, tend_lo], name)
    triangulate(lo)
    strip_colors(lo)
    for a in list(lo.data.attributes):
        if a.name == "Depth":
            lo.data.attributes.remove(a)
    tris = len(lo.data.polygons)
    log(name, "game mesh tris", tris)
    if tris > TRI_LIMIT_EGG:
        raise RuntimeError("%s has %d tris > %d" % (name, tris, TRI_LIMIT_EGG))
    seams = pick_seams(P["N"], P["phase"], [E["useg"][1], E["iuseg"][1]], [25.0, 155.0, 270.0])
    nseam = uv_layout(lo, seams, {"Skin", "Inner"}, {"Inner": 0.55})
    log(name, "uv seams at", seams, "edges", nseam)
    # per-group bake
    hk = {"Skin": "HiSkin", "Flesh": "HiWall", "Inner": "HiInner"}
    hp = {v: split_copy(hi, v, (lambda nm_: lambda f, nm: nm[f.material_index] == nm_)(k)) for k, v in hk.items()}
    lp = {"LoSkin": split_copy(lo, "LoSkin", lambda f, nm: nm[f.material_index] in ("Skin", "StemMat", "TendrilMat")),
          "LoWall": split_copy(lo, "LoWall", lambda f, nm: nm[f.material_index] == "Flesh"),
          "LoInner": split_copy(lo, "LoInner", lambda f, nm: nm[f.material_index] == "Inner")}
    for o in (hi, lo, cut):
        o.hide_render = True
    imgs = bake_groups([(lp["LoSkin"], [hp["HiSkin"], stem_hi, tend_hi], 0.07, 0.16),
                        (lp["LoWall"], [hp["HiWall"]], 0.05, 0.12),
                        (lp["LoInner"], [hp["HiInner"]], 0.07, 0.16)], size, name, ao_strength=0.5, ao_dist=0.45)
    for o in list(hp.values()) + list(lp.values()):
        bpy.data.objects.remove(o)
    lo.hide_render = False
    pbr_material(lo, name + "_PBR", imgs)
    for o in (hi, stem_hi, tend_hi, cut):
        o.hide_render = True
        o.hide_viewport = True
    fi = egg_field(Pi, pl)
    itop, ibot = fi(Vector((0, 0, 1)))[0].z, fi(Vector((0, 0, -1)))[0].z
    cav, flo = Vector((0, 0, (itop + ibot) / 2)), Vector((0, 0, ibot))
    c, dims = recentre(lo, [hi, stem_hi, tend_hi, cut])
    rep = dict(name=name, tris=tris, texture=size, size_blender_xyz=bl(dims), bottom_offset_z=-round(dims.z / 2, 3),
               cavity_centre=bl(cav - c), cavity_floor=bl(flo - c), shell=E["shell"], holes=holes,
               bake=imgs["stats"], blender_shift=[round(v, 4) for v in -c])
    finish(name, [lo], rep, "egg_" + key)
    return rep


def finish(name, objs, rep, blend):
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, blend + ("_fast" if CFG["fast"] else "") + ".blend"))
    if not CFG["fast"]:
        rep["export"] = export_fbx(objs, os.path.join(CDIMP, "Halloween_" + name + ".fbx"))
    with open(os.path.join(OUT, name + ".json"), "w") as fh:
        json.dump(rep, fh, indent=1)
    log(name, "done", json.dumps(rep))


# ------------------------------------------------------------------ the plain eggs
PLAINS = {
    "P1": dict(name="PumpkinEgg_Plain1",
               P=dict(N=10, R=1.5, Rz=1.92, egg=0.16, depth=0.095, crest=0.5, lumps=0.03, micro=0.003, dtop=0.10,
                      dtop_w=0.34, dbot=0.03, flat=0.9, flat_k=0.2, seed=404, phase=0.5),
               useg=(400, 60), vseg=(240, 34), pal="P1", stem=dict(L=0.62, r0=0.13, seed=53, sp="dark")),
    "P2": dict(name="PumpkinEgg_Plain2",
               P=dict(N=9, R=1.38, Rz=1.74, egg=0.18, depth=0.075, crest=0.55, lumps=0.03, micro=0.0025, dtop=0.09,
                      dtop_w=0.32, dbot=0.03, flat=0.9, flat_k=0.2, seed=505, phase=0.5,
                      streak=lin((104, 128, 86)), streak_amt=0.55, rough_add=0.08),
               useg=(360, 54), vseg=(240, 34), pal="P2", stem=dict(L=0.58, r0=0.12, seed=67, sp="pale")),
}
TRI_LIMIT_PLAIN = 5000


def build_plain(key):
    E = PLAINS[key]
    P = E["P"]
    name = E["name"]
    fast = CFG["fast"]
    hs = 2 if fast else 1
    size = 256 if fast else 512
    fresh(samples=8 if fast else 48)
    pl = PAL[E["pal"]]
    skin, stem_m = mat_vc("Skin"), mat_vc("StemMat")
    hi = build_mesh("Egg_hi", [sphere_surface(egg_field(P, pl), E["useg"][0] // hs, E["vseg"][0] // hs) + (0, 1.0)],
                    [skin])
    f_lo = egg_field(dict(P, micro=0.0), pl)
    lo = build_mesh(name, [sphere_surface(f_lo, E["useg"][1], E["vseg"][1]) + (0, 1.0)], [skin])
    top = f_lo(Vector((0.0, 0.0, 1.0)))[0]
    base = (0.0, 0.0, top.z - 0.04)
    S = E["stem"]
    stem_hi = make_obj("Stem_hi", *gnarly_stem(S["L"], S["r0"], S["seed"], base, STEMS[S["sp"]], True),
                       mats=[stem_m], recalc=True)
    stem_lo = make_obj("Stem_lo", *gnarly_stem(S["L"], S["r0"], S["seed"], base, STEMS[S["sp"]], False),
                       mats=[stem_m], recalc=True)
    lo = join([lo, stem_lo], name)
    triangulate(lo)
    strip_colors(lo)
    for a in list(lo.data.attributes):
        if a.name == "Depth":
            lo.data.attributes.remove(a)
    tris = len(lo.data.polygons)
    log(name, "game mesh tris", tris)
    if tris > TRI_LIMIT_PLAIN:
        raise RuntimeError("%s has %d tris > %d" % (name, tris, TRI_LIMIT_PLAIN))
    N = P["N"]
    seams = pick_seams(N, P["phase"], [E["useg"][1]], [90.0 - 180.0 / N * 3, 90.0 + 180.0 / N * 3, 270.0])
    uv_layout(lo, seams, {"Skin"}, {})
    lo.hide_render = True
    bake_lo = split_copy(lo, "LoAll", lambda f, nm: True)
    imgs = bake_groups([(bake_lo, [hi, stem_hi], 0.06, 0.14)], size, name, ao_strength=0.5, ao_dist=0.3)
    bpy.data.objects.remove(bake_lo)
    lo.hide_render = False
    pbr_material(lo, name + "_PBR", imgs)
    for o in (hi, stem_hi):
        o.hide_render = True
        o.hide_viewport = True
    c, dims = recentre(lo, [hi, stem_hi])
    rep = dict(name=name, tris=tris, texture=size, size_blender_xyz=bl(dims), bottom_offset_z=-round(dims.z / 2, 3),
               bake=imgs["stats"], blender_shift=[round(v, 4) for v in -c])
    finish(name, [lo], rep, "plain_" + key)
    return rep


# ------------------------------------------------------------------ the candles
CANDLES = [
    dict(pos=(0.10, 0.72), H=1.20, R=0.47, seed=11, wax=(236, 212, 162), notches=[(1.35, 0.11, 0.30)], extra=5),
    dict(pos=(0.74, -0.22), H=1.80, R=0.53, seed=22, wax=(222, 198, 154), notches=[(5.75, 0.16, 0.26), (2.2, 0.07, 0.2)],
         extra=6),
    dict(pos=(-0.42, -0.30), H=2.40, R=0.58, seed=33, wax=(240, 220, 174), notches=[(3.85, 0.23, 0.36), (0.9, 0.09, 0.22)],
         extra=7),
]
S1, S2, S3, S4 = 0.60, 0.78, 0.86, 0.90
LIP = 0.045


def candle_field(K):
    """A melted pillar candle as f(theta, s): s runs up the side (0..S1), over the rounded lip (..S2), down the inside
    wall (..S3), across the meniscus (..S4) and the wax pool to the wick (1). Rim notches where wax overflowed, drips
    running down from them (raised wax ridges ending in a teardrop bulb), a sagging soft top, a dusty foot."""
    rng = random.Random(K["seed"])
    H, R = K["H"], K["R"]
    cx, cy = K["pos"]
    off = Vector((rng.uniform(-30, 30), rng.uniform(-30, 30), rng.uniform(-30, 30)))
    lr = LIP
    slant, ths = rng.uniform(0.015, 0.04), rng.uniform(0, 2 * math.pi)
    notches = K["notches"]

    def rim(th):
        v = H - slant + slant * math.cos(th - ths)
        v += 0.03 * noise.noise(Vector((math.cos(th) * 1.8, math.sin(th) * 1.8, 0.5)) + off)
        v += 0.012 * noise.noise(Vector((math.cos(th) * 7, math.sin(th) * 7, 2.5)) + off)
        for tn, dn, wn in notches:
            v -= dn * math.exp(-(wrap(th - tn) / wn) ** 2)
        return v

    zf = min(rim(2 * math.pi * i / 720) for i in range(720)) - lr - 0.012
    drips = []
    for tn, dn, wn in notches:
        zs = rim(tn) - lr
        drips.append((tn + rng.uniform(-0.04, 0.04), zs, zs - rng.uniform(0.0, 0.06), rng.uniform(0.10, 0.13),
                      rng.uniform(0.05, 0.065)))
        t2 = tn + rng.choice((-1, 1)) * rng.uniform(0.2, 0.32)
        zs2 = rim(t2) - lr
        drips.append((t2, zs2, rng.uniform(0.25, 0.6) * zs2, rng.uniform(0.06, 0.08), rng.uniform(0.03, 0.04)))
    for _ in range(K["extra"]):
        t2 = rng.uniform(0, 2 * math.pi)
        zs2 = rim(t2) - lr
        drips.append((t2, zs2, rng.uniform(0.12, 0.5) * zs2, rng.uniform(0.05, 0.08), rng.uniform(0.028, 0.04)))

    def drip(th, z):
        best, tint = 0.0, 0.0
        for t0, zs, L, w0, k0 in drips:
            x = wrap(th - t0) * R
            if abs(x) > 2.0 * w0 or z > zs + 0.03:
                continue
            ze = zs - L
            if z >= ze:
                u = (zs - z) / max(L, 1e-3)
                bul = math.exp(-((z - ze) / (w0 * 0.9)) ** 2)
                w = w0 * (1 - 0.35 * u) * (1 + 0.35 * bul)
                k = k0 * (0.6 + 0.4 * u) * (1 + 0.4 * bul) * smoothstep(zs + 0.03, zs - 0.02, z)
                q = 1 - (x / w) ** 2
            else:
                w = w0 * 0.65 * 1.35
                k = k0 * 1.4
                q = 1 - (math.sqrt(x * x + 1.3 * (ze - z) ** 2) / w) ** 2
            if q > 0:
                v = k * q ** 0.55
                best = max(best, v)
                tint = max(tint, min(1.0, v / (k0 * 0.5)))
        return best, tint

    def side_r(th, z, h):
        r = R * (1 + 0.010 * noise.noise(Vector((math.cos(th) * 2.0, math.sin(th) * 2.0, z * 1.6)) + off))
        r += 0.028 * math.exp(-max(z, 0.0) / 0.09)              # wax built up at the foot
        r += 0.010 * math.exp(-max(0.0, h - z) / 0.07)          # the soft top sags out a little
        dv, tint = drip(th, z)
        return r + dv, tint

    wax = lin(K["wax"])
    amber, dust = lin((222, 180, 104)), lin((160, 144, 118))
    drip_c, soot = lin((240, 212, 146)), lin((66, 60, 54))

    def f(th, s):
        h = rim(th)
        ct, st = math.cos(th), math.sin(th)
        rt, _ = side_r(th, h - lr, h)
        rc = rt - lr
        tint, zone = 0.0, 0
        if s <= S1:
            z = (h - lr) * s / S1
            r, tint = side_r(th, z, h)
        elif s <= S2:
            a = math.pi * (s - S1) / (S2 - S1)
            r, z, zone = rc + lr * math.cos(a), h - lr + lr * math.sin(a), 1
        elif s <= S3:
            q = (s - S2) / (S3 - S2)
            r, z, zone = rc - lr - 0.03 * q, (h - lr) + (zf + 0.022 - (h - lr)) * q, 2
        elif s <= S4:
            q = (s - S3) / (S4 - S3)
            r, z, zone = rc - lr - 0.03 - 0.055 * q, zf + 0.022 * (1 - q) ** 2, 3
        else:
            q = (s - S4) / (1 - S4)
            r, z, zone = (rc - lr - 0.085) * (1 - q), zf - 0.006 * q * q, 3
        p = Vector((cx + r * ct, cy + r * st, z))
        n1 = noise.noise(Vector((ct * 3, st * 3, z * 4)) + off)
        n2 = noise.noise(Vector((ct * 9, st * 9, z * 14)) + off * 0.7)
        col = mix(wax, dust, 0.35 * math.exp(-max(z, 0.0) / 0.22))
        col = tuple(cc * (0.965 + 0.035 * n1 + 0.02 * n2) for cc in col)
        rough = 0.46
        if zone == 0:
            col = mix(col, mix(wax, drip_c, 0.5), 0.3 * smoothstep(h - 0.3, h - lr, z))
            col = mix(col, drip_c, 0.75 * tint)
            rough = 0.46 - 0.2 * tint
        elif zone == 1:
            col, rough = mix(col, drip_c, 0.3), 0.36
        elif zone == 2:
            col, rough = mix(wax, amber, 0.3), 0.32
        else:
            col, rough = mix(wax, amber, 0.62 + 0.08 * n1), 0.15
            col = mix(col, soot, 0.6 * math.exp(-(r / 0.075) ** 2))
        return p, col, (rough, rough, rough)

    return f, zf


def grid_surface(field, thetas, ss, pole_s=None):
    """Rows field(theta, s), open at the first row, closed by a pole vertex at pole_s. Winding: outward."""
    V, C, Rr, F, rows = [], [], [], [], []
    m = len(thetas)
    for s in ss:
        row = []
        for th in thetas:
            p, c, r = field(th, s)
            V.append(p)
            C.append(c)
            Rr.append(r)
            row.append(len(V) - 1)
        rows.append(row)
    for a, b in zip(rows[:-1], rows[1:]):
        for j in range(m):
            jn = (j + 1) % m
            F.append((a[j], a[jn], b[jn], b[j]))
    if pole_s is not None:
        p, c, r = field(0.0, pole_s)
        V.append(p)
        C.append(c)
        Rr.append(r)
        pv = len(V) - 1
        for j in range(m):
            F.append((rows[-1][j], rows[-1][(j + 1) % m], pv))
    return V, F, C, Rr


def puddle_field(cands, seed):
    """The melted wax puddle under the cluster: a lobed outline with wax tongues, a rounded edge, mounds of wax
    built up around each candle foot, dust caught at the edge."""
    rng = random.Random(seed)
    off = Vector((rng.uniform(-30, 30), rng.uniform(-30, 30), rng.uniform(-30, 30)))
    cx = sum(K["pos"][0] for K in cands) / len(cands)
    cy = sum(K["pos"][1] for K in cands) / len(cands)
    tongues = [(rng.uniform(0, 2 * math.pi), rng.uniform(0.22, 0.45), rng.uniform(0.14, 0.26)) for _ in range(4)]
    e = 0.07
    SE = 0.12
    wax = mix(lin((234, 210, 160)), lin((222, 182, 112)), 0.3)
    dust = lin((146, 130, 104))

    def Rp(th):
        v = 1.48 + 0.15 * fbm(Vector((math.cos(th) * 1.3, math.sin(th) * 1.3, 0.3)) + off, 3)
        for tt, tl, tw in tongues:
            v += tl * math.exp(-(wrap(th - tt) / tw) ** 2)
        return v

    def top(x, y):
        z = 0.06 + 0.012 * noise.noise(Vector((x * 2.5, y * 2.5, 0.7)) + off)
        for K in cands:
            d = math.hypot(x - K["pos"][0], y - K["pos"][1]) - K["R"]
            z += 0.09 * math.exp(-(max(d, 0.0) / 0.17) ** 2)
        return z

    def f(th, s):
        rp = Rp(th)
        ct, st = math.cos(th), math.sin(th)
        if s <= SE:
            a = (s / SE) * math.pi / 2
            r = rp - e + e * math.cos(a)
            z = top(cx + (rp - e) * ct, cy + (rp - e) * st) * math.sin(a)
        else:
            q = (s - SE) / (1 - SE)
            r = (rp - e) * (1 - q)
            z = top(cx + r * ct, cy + r * st)
        x, y = cx + r * ct, cy + r * st
        n1 = noise.noise(Vector((x * 3, y * 3, 1.9)) + off)
        col = tuple(cc * (0.96 + 0.05 * n1) for cc in wax)
        col = mix(col, dust, 0.45 * smoothstep(rp - 0.25, rp, r) + 0.15 * smoothstep(0.3, 0.7, n1))
        rough = 0.3 + 0.2 * smoothstep(rp - 0.25, rp, r)
        return Vector((x, y, z)), col, (rough, rough, rough)

    return f, (cx, cy)


def wick_pts(K, zf, n):
    rng = random.Random(K["seed"] + 7)
    cx, cy = K["pos"]
    phi = rng.uniform(0, 2 * math.pi)
    P0 = Vector((cx, cy, zf - 0.03))
    P1 = Vector((cx, cy, zf + 0.25))
    P2 = Vector((cx + 0.10 * math.cos(phi), cy + 0.10 * math.sin(phi), zf + 0.18))
    return [P0 * (1 - t) ** 2 + P1 * 2 * (1 - t) * t + P2 * t * t for t in (i / (n - 1) for i in range(n))]


def wick_mesh(pts, nside):
    n = len(pts)
    radii, cols = [], []
    for i in range(n):
        t = i / (n - 1)
        radii.append((0.04 - 0.008 * t) * (1 + 0.35 * math.exp(-((1 - t) / 0.08) ** 2)))
        c = mix(lin((214, 204, 182)), lin((26, 23, 21)), smoothstep(0.1, 0.2, t))
        cols.append(mix(c, lin((86, 78, 70)), smoothstep(0.82, 1.0, t)))
    return tube(pts, radii, nside, cols, 0.85)


def build_candles():
    name = "Candles"
    fast = CFG["fast"]
    size = 256 if fast else 512
    fresh(samples=8 if fast else 48)
    mats = [mat_vc("Wax%d" % (i + 1)) for i in range(3)] + [mat_vc("Puddle"), mat_vc("Wick")]
    hs = 2 if fast else 1
    th_hi = [2 * math.pi * j / (256 // hs) for j in range(256 // hs)]
    th_lo = [2 * math.pi * j / 28 for j in range(28)]
    s_hi = [i / (240 // hs) for i in range(240 // hs)]
    s_lo = [0.0, 0.15, 0.30, 0.45, 0.60, 0.66, 0.72, 0.78, 0.86, 0.90, 0.95]
    his, los, tips, tops = [], [], [], []
    wick_hi, wick_lo = [], []
    for i, K in enumerate(CANDLES):
        f, zf = candle_field(K)
        his.append(make_obj("Candle%d_hi" % (i + 1), *grid_surface(f, th_hi, s_hi, 1.0), mats=[mats[i]]))
        los.append(make_obj("Candle%d_lo" % (i + 1), *grid_surface(f, th_lo, s_lo, 1.0), mats=[mats[i]]))
        wp = wick_pts(K, zf, 40)
        tips.append(wp[-1].copy())
        tops.append(max(wp, key=lambda p: p.z).copy())
        wick_hi.append(make_obj("Wick%d_hi" % (i + 1), *wick_mesh(wp, 12), mats=[mats[4]], recalc=True))
        wick_lo.append(make_obj("Wick%d_lo" % (i + 1), *wick_mesh(wick_pts(K, zf, 7), 6), mats=[mats[4]],
                                recalc=True))
    pf, pc = puddle_field(CANDLES, 77)
    pth_hi = [2 * math.pi * j / (360 // hs) for j in range(360 // hs)]
    pth_lo = [2 * math.pi * j / 40 for j in range(40)]
    ps_hi = [i / (64 // hs) for i in range(64 // hs)]
    ps_lo = [0.0, 0.06, 0.12, 0.45, 0.75]
    pud_hi = make_obj("Puddle_hi", *grid_surface(pf, pth_hi, ps_hi, 1.0), mats=[mats[3]])
    pud_lo = make_obj("Puddle_lo", *grid_surface(pf, pth_lo, ps_lo, 1.0), mats=[mats[3]])
    wk_hi = join(wick_hi, "Wicks_hi")
    lo = join(los + [pud_lo] + wick_lo, name)
    triangulate(lo)
    strip_colors(lo)
    tris = len(lo.data.polygons)
    log(name, "game mesh tris", tris)
    if tris > 3000:
        raise RuntimeError("Candles has %d tris > 3000" % tris)
    uv_layout(lo, [], set(), {}, angle=60)
    lo.hide_render = True
    groups = []
    for i in range(3):
        nm = "Wax%d" % (i + 1)
        groups.append((split_copy(lo, "Lo" + nm, (lambda n_: lambda f_, nm_: nm_[f_.material_index] == n_)(nm)),
                       [his[i]], 0.09, 0.2))
    groups.append((split_copy(lo, "LoPuddle", lambda f_, nm_: nm_[f_.material_index] == "Puddle"), [pud_hi], 0.12,
                   0.26))
    groups.append((split_copy(lo, "LoWick", lambda f_, nm_: nm_[f_.material_index] == "Wick"), [wk_hi], 0.03, 0.08))
    imgs = bake_groups(groups, size, name, ao_strength=0.5, ao_dist=0.25)
    for g in groups:
        bpy.data.objects.remove(g[0])
    lo.hide_render = False
    pbr_material(lo, name + "_PBR", imgs)
    for o in his + [pud_hi, wk_hi]:
        o.hide_render = True
        o.hide_viewport = True
    c, dims = recentre(lo, his + [pud_hi, wk_hi])
    rep = dict(name=name, tris=tris, texture=size, size_blender_xyz=bl(dims), bottom_offset_z=-round(dims.z / 2, 3),
               wick_tips=[bl(t - c) for t in tips], wick_tops=[bl(t - c) for t in tops],
               candle_heights=[K["H"] for K in CANDLES], bake=imgs["stats"], blender_shift=[round(v, 4) for v in -c])
    finish(name, [lo], rep, "candles")
    return rep


# ------------------------------------------------------------------ review
ASSETS = [("egg_A", "PumpkinEgg_A"), ("egg_B", "PumpkinEgg_B"), ("egg_C", "PumpkinEgg_C"),
          ("plain_P1", "PumpkinEgg_Plain1"), ("plain_P2", "PumpkinEgg_Plain2"), ("candles", "Candles")]


def load_asset(blend, name):
    path = os.path.join(OUT, blend + ("_fast" if CFG["fast"] else "") + ".blend")
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [name]
    ob = dst.objects[0]
    link(ob)
    with open(os.path.join(OUT, name + ".json")) as fh:
        rep = json.load(fh)
    return ob, rep


def flame(name, loc, w, h, strength=30.0):
    """Review-only stand-in for the Studio flame particles (NOT exported)."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=12, radius=1.0)
    for v in bm.verts:
        x, y, z = v.co
        k = 1 - 0.55 * max(0.0, z)
        v.co = Vector((x * w * k, y * w * k, (z + 0.35 * (1 - z * z)) * h))
    ob = obj_from_bm(bm, name)
    ob.location = loc
    em = bpy.data.materials.new(name + "_m")
    em.use_nodes = True
    nt = em.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (1.0, 0.62, 0.22, 1)
    e.inputs["Strength"].default_value = strength
    nt.links.new(e.outputs["Emission"], nt.nodes["Material Output"].inputs["Surface"])
    ob.data.materials.append(em)
    ob.visible_shadow = False
    return ob


def point(name, loc, energy, col=(1.0, 0.55, 0.2), radius=0.12):
    ld = bpy.data.lights.new(name, "POINT")
    ld.energy, ld.color, ld.shadow_soft_size = energy, col, radius
    ob = link(bpy.data.objects.new(name, ld))
    ob.location = loc
    return ob


def from_rb(v):
    return Vector((v[0], -v[2], v[1]))


def review():
    sc = fresh(samples=16)
    review_setup(res=(1600, 1000))
    sun = [o for o in sc.objects if o.type == "LIGHT"][0]
    gm = mat_noise("Ground", lin((92, 86, 80)), lin((64, 60, 58)), scale=(1, 1, 1), nscale=0.7, detail=6,
                   rough=0.85, lo=0.3, hi=0.7, bump=0.2)
    bpy.ops.mesh.primitive_plane_add(size=80)
    gr = bpy.context.active_object
    gr.data.materials.append(gm)
    layout = {"PumpkinEgg_A": ((0.0, 0.0), 0), "PumpkinEgg_B": ((6.6, -1.6), 18), "PumpkinEgg_C": ((-6.6, -1.2), -16),
              "PumpkinEgg_Plain1": ((3.6, 2.2), 30), "PumpkinEgg_Plain2": ((-3.4, 2.7), -40),
              "Candles": ((-1.7, 3.9), 0)}
    obs, reps = {}, {}
    for blend, name in ASSETS:
        ob, rep = load_asset(blend, name)
        (x, y), rz = layout[name]
        ob.location = (x, y, -rep["bottom_offset_z"])
        ob.rotation_euler = (0, 0, math.radians(rz))
        obs[name], reps[name] = ob, rep
    bpy.context.view_layer.update()
    shots = []
    out = WIP if CFG["fast"] else OUT

    def P(name, rv):
        return obs[name].matrix_world @ Vector(rv)

    tgt = Vector((0, 0.8, 2.6))
    shots.append(shoot(os.path.join(out, "review_day_25studs.png"), tgt, (0.0, 1.0, 0.30), 25.0, lens=50))
    shots.append(shoot(os.path.join(WIP, "review_day_34.png"), tgt, (-0.7, 1.0, 0.45), 25.0, lens=50))
    shots.append(shoot(os.path.join(WIP, "review_back.png"), tgt, (0.3, -1.0, 0.35), 25.0, lens=50))
    for k in ("A", "B", "C"):
        nm = "PumpkinEgg_" + k
        c = obs[nm].location + Vector((0, 0, -0.3))
        d = (math.sin(obs[nm].rotation_euler.z) * -1 + 0.2, math.cos(obs[nm].rotation_euler.z), 0.12)
        shots.append(shoot(os.path.join(WIP, "close_%s.png" % k), c, d, 10.0, lens=50))
    cc = obs["Candles"].location
    shots.append(shoot(os.path.join(WIP, "close_candles.png"), cc + Vector((0, 0, -0.1)), (0.5, 1.0, 0.5), 7.0,
                       lens=50))
    shots.append(shoot(os.path.join(WIP, "close_plain.png"), Vector((0.1, 2.45, 1.7)), (0.0, 1.0, 0.25), 13.0,
                       lens=50))
    # night: dim moonlit world, a warm light + flame stand-in inside every carved egg and on every wick
    w = sc.world.node_tree.nodes["Background"]
    w.inputs["Color"].default_value = (0.02, 0.028, 0.06, 1)
    w.inputs["Strength"].default_value = 1.0
    sun.data.energy, sun.data.color = 0.35, (0.6, 0.7, 1.0)
    for k in ("A", "B", "C"):
        nm = "PumpkinEgg_" + k
        cav, flo = P(nm, reps[nm]["cavity_centre"]), P(nm, reps[nm]["cavity_floor"])
        point("L" + k, flo + Vector((0, 0, 0.95)), 160.0, radius=0.25)
        flame("F" + k, flo + Vector((0, 0, 0.75)), 0.22, 0.55, 25.0)
    for i, tip in enumerate(reps["Candles"]["wick_tops"]):
        p = P("Candles", tip)
        point("LC%d" % i, p + Vector((0, 0, 0.18)), 6.0, radius=0.05)
        flame("FC%d" % i, p + Vector((0, 0, 0.12)), 0.055, 0.16, 25.0)
    sc.view_settings.exposure = 0.6
    shots.append(shoot(os.path.join(out, "review_night_lit.png"), tgt, (0.0, 1.0, 0.30), 25.0, lens=50))
    nm = "PumpkinEgg_A"
    shots.append(shoot(os.path.join(out, "review_close_A_lit.png"), obs[nm].location + Vector((0, 0, -0.3)),
                       (0.2, 1.0, 0.12), 10.0, lens=50))
    for k in ("B", "C"):
        nm = "PumpkinEgg_" + k
        c = obs[nm].location + Vector((0, 0, -0.3))
        d = (math.sin(obs[nm].rotation_euler.z) * -1 + 0.2, math.cos(obs[nm].rotation_euler.z), 0.12)
        shots.append(shoot(os.path.join(WIP, "close_%s_lit.png" % k), c, d, 10.0, lens=50))
    shots.append(shoot(os.path.join(WIP, "close_candles_lit.png"), cc + Vector((0, 0, -0.1)), (0.5, 1.0, 0.5), 7.0,
                       lens=50))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(WIP, "review.blend"))
    return shots


def preview(blend, name, tag):
    """Quick look at one asset: front at 25 studs, a close-up, a close-up lit from inside (WIP folder)."""
    sc = fresh(samples=16)
    review_setup(res=(1200, 900))
    sun = [o for o in sc.objects if o.type == "LIGHT"][0]
    bpy.ops.mesh.primitive_plane_add(size=60)
    bpy.context.active_object.data.materials.append(mat_flat("G", lin((80, 76, 72)), rough=0.9))
    ob, rep = load_asset(blend, name)
    ob.location = (0, 0, -rep["bottom_offset_z"])
    bpy.context.view_layer.update()
    h = rep["size_blender_xyz"][2]
    c = Vector((0, 0, h / 2))
    out = []
    out.append(shoot(os.path.join(WIP, tag + "_25.png"), c, (0.0, 1.0, 0.3), 25.0, lens=50))
    near = max(h * 1.25, 6.0)
    out.append(shoot(os.path.join(WIP, tag + "_close.png"), c + Vector((0, 0, -0.2)), (0.25, 1.0, 0.1), near, lens=50))
    out.append(shoot(os.path.join(WIP, tag + "_34.png"), c, (-0.9, 0.6, 0.45), max(h * 1.6, 7.0), lens=50))
    out.append(shoot(os.path.join(WIP, tag + "_back.png"), c, (0.3, -1.0, 0.35), max(h * 1.6, 7.0), lens=50))
    if "cavity_centre" in rep or "wick_tops" in rep:
        w = sc.world.node_tree.nodes["Background"]
        w.inputs["Color"].default_value = (0.02, 0.028, 0.06, 1)
        sun.data.energy, sun.data.color = 0.35, (0.6, 0.7, 1.0)
        if "cavity_centre" in rep:
            cav, flo = ob.matrix_world @ Vector(rep["cavity_centre"]), ob.matrix_world @ Vector(rep["cavity_floor"])
            point("L", flo + Vector((0, 0, 0.95)), 160.0, radius=0.25)
            flame("F", flo + Vector((0, 0, 0.75)), 0.22, 0.55, 25.0)
        else:
            for i, tip in enumerate(rep["wick_tops"]):
                p = ob.matrix_world @ Vector(tip)
                point("LC%d" % i, p + Vector((0, 0, 0.18)), 6.0, radius=0.05)
                flame("FC%d" % i, p + Vector((0, 0, 0.12)), 0.055, 0.16, 25.0)
        sc.view_settings.exposure = 0.6
        out.append(shoot(os.path.join(WIP, tag + "_lit.png"), c + Vector((0, 0, -0.2)), (0.25, 1.0, 0.1), near,
                         lens=50))
    return out


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if "fast" in argv:
        CFG["fast"] = True
        argv.remove("fast")
    if "debug" in argv:
        CFG["debug"] = True
        argv.remove("debug")
    rep = {}
    i = 0
    while i < len(argv):
        step = argv[i]
        if step == "egg":
            rep["egg_" + argv[i + 1]] = build_egg(argv[i + 1])
            i += 2
        elif step == "plain":
            rep["plain_" + argv[i + 1]] = build_plain(argv[i + 1])
            i += 2
        elif step == "candles":
            rep["candles"] = build_candles()
            i += 1
        elif step == "preview":
            rep["preview"] = preview(argv[i + 1], argv[i + 2], argv[i + 3])
            i += 4
        elif step == "review":
            rep["review"] = review()
            i += 1
        else:
            raise SystemExit("unknown step " + step)
    print("EGGS_REPORT " + json.dumps(rep, default=str))
