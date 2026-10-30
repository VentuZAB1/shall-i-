# SLINGSHOT - "UFO Invasion" weather event models (Mothership + Saucer), built procedurally in Blender.
# Run inside the Blender GUI through MCP:
#   import runpy; U = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Weather\UFO\build_ufo.py")
#   U["build_all"]()          # (re)build both models + palette + stage, save ufo_models.blend
#   U["render_all"]()         # 3 renders per model + UFO_lineup.png
#   U["export_all"]()         # Mothership.fbx, Saucer.fbx (palette embedded)
#   U["report"]()             # tri counts / sizes / pivots
#
# Units: 1 Blender metre = 1 Roblox stud (the FBX is exported with global_scale 0.01 - see export_model()).
# Colours: one 64x64 palette PNG (16 px cells); every face's UVs sit on the centre of its colour cell; Closest.
# No emissive materials anywhere (owner rule): light pods are plain light-green geometry.
import bpy, bmesh, math, os
from mathutils import Vector, Matrix

OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Weather\UFO"
BLEND = os.path.join(OUT, "ufo_models.blend")

PALETTE = [  # index: (name, sRGB hex). Cell i -> column i % 4, row i // 4 (row 0 = bottom of the PNG = UV v 0..0.25)
    ("SILVER",   "C9D1DA"),   # 0  light hull panels
    ("STEEL",    "98A3AF"),   # 1  light gunmetal
    ("GUNMETAL", "5B646F"),   # 2  underside
    ("DEEP",     "3A414A"),   # 3  darker gunmetal (underside panels, grooves)
    ("GREEN",    "78FF5A"),   # 4  UFO green (light pods, accents)
    ("DKGREEN",  "2E8A2A"),   # 5  dark green contrast
    ("GLASS",    "1E5B55"),   # 6  dark tinted teal-green "glass" (opaque)
    ("GLASS_HI", "4E9E8F"),   # 7  lighter teal (cartoon glass highlight)
    ("BAY",      "171B20"),   # 8  belly bay interior
    ("WHITE",    "EEF2F6"),   # 9  bright trim
    ("MIDGREEN", "4CC23A"),   # 10 mid green
    ("TRIM",     "262B31"),   # 11 near-black trim / seams
]
CI = {n: i for i, (n, _) in enumerate(PALETTE)}


def cell_uv(i):
    return ((i % 4) * 16 + 8) / 64.0, ((i // 4) * 16 + 8) / 64.0


# ------------------------------------------------------------------ palette + material
def make_palette():
    path = os.path.join(OUT, "ufo_palette.png")
    for im in list(bpy.data.images):
        if im.name.startswith("ufo_palette"):
            bpy.data.images.remove(im)
    img = bpy.data.images.new("ufo_palette_tmp", 64, 64, alpha=False)
    px = [0.0] * (64 * 64 * 4)
    for y in range(64):
        for x in range(64):
            i = (y // 16) * 4 + x // 16
            h = PALETTE[i][1] if i < len(PALETTE) else PALETTE[0][1]
            o = (y * 64 + x) * 4
            px[o:o + 4] = [int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0, 1.0]
    img.pixels[:] = px
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    bpy.data.images.remove(img)
    img = bpy.data.images.load(path, check_existing=False)
    img.name = "ufo_palette.png"
    return img


def palette_material(img):
    m = bpy.data.materials.get("UFO_Palette") or bpy.data.materials.new("UFO_Palette")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.38
    bsdf.inputs["Metallic"].default_value = 0.0
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    out.location, bsdf.location, tex.location = (300, 0), (0, 0), (-350, 0)
    m.use_backface_culling = True        # preview like Roblox (MeshParts cull back faces)
    return m


def flat_material(name, hexs, rough=0.6):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    c = tuple(int(hexs[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    lin = tuple((v / 12.92) if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)
    b.inputs["Base Color"].default_value = (*lin, 1.0)
    b.inputs["Roughness"].default_value = rough
    m.diffuse_color = (*lin, 1.0)
    return m


# ------------------------------------------------------------------ mesh builder
class MB:
    def __init__(self):
        self.bm = bmesh.new()
        self.pal = self.bm.faces.layers.int.new("pal")

    def v(self, co):
        return self.bm.verts.new(co)

    def f(self, vs, c):
        fa = self.bm.faces.new(vs)
        fa[self.pal] = CI[c]
        return fa

    def recolor(self, faces, c):
        for fa in faces:
            fa[self.pal] = CI[c]


def colour_of(spec, j, i):
    if isinstance(spec, str):
        return spec
    if callable(spec):
        return spec(j, i)
    a, b, period = spec[:3]
    off = spec[3] if len(spec) > 3 else 0
    return a if ((j + off) // period) % 2 == 0 else b


def lathe(mb, prof, segs, phase=0.0, flip=False):
    """Revolve a (r, z, colour-of-next-segment) profile about Z. A profile running top-centre -> outward -> down ->
    inward gives outward-facing normals; use flip=True for profiles that start at the bottom centre and go up
    (Roblox culls back faces, so winding matters). Returns {(profile_index, segment): face}."""
    angs = [phase + 2 * math.pi * j / segs for j in range(segs)]
    rings = []
    for (r, z, _) in prof:
        if r < 1e-6:
            rings.append([mb.v((0.0, 0.0, z))])
        else:
            rings.append([mb.v((r * math.cos(a), r * math.sin(a), z)) for a in angs])
    faces = {}
    for i in range(len(prof) - 1):
        A, B = rings[i], rings[i + 1]
        spec = prof[i][2]
        for j in range(segs):
            j2 = (j + 1) % segs
            c = colour_of(spec, j, i)
            if len(A) == 1:
                vs = [A[0], B[j], B[j2]]
            elif len(B) == 1:
                vs = [A[j], B[0], A[j2]]
            else:
                vs = [A[j], B[j], B[j2], A[j2]]
            fa = mb.f(vs[::-1] if flip else vs, c)
            faces[(i, j)] = fa
    return faces


def basis(n, t):
    n = Vector(n).normalized()
    t = Vector(t)
    t = (t - n * t.dot(n)).normalized()
    b = n.cross(t)
    return n, t, b


def dome(mb, c, n, t, rt, rb, rn, useg, vseg, col, base_col=None, col_fn=None, base=True):
    """Half ellipsoid on the t-b plane at c, bulging along n. Closed with a base cap unless base=False."""
    n, t, b = basis(n, t)
    c = Vector(c)
    rings = []
    for k in range(vseg):
        phi = (math.pi / 2) * k / vseg
        rings.append([mb.v(c + t * (rt * math.cos(phi) * math.cos(th)) + b * (rb * math.cos(phi) * math.sin(th))
                           + n * (rn * math.sin(phi)))
                      for th in [2 * math.pi * j / useg for j in range(useg)]])
    apex = mb.v(c + n * rn)
    out = []
    for k in range(vseg):
        A = rings[k]
        for j in range(useg):
            j2 = (j + 1) % useg
            cc = col_fn(j, k) if col_fn else col
            if k < vseg - 1:
                B = rings[k + 1]
                out.append(mb.f([A[j], A[j2], B[j2], B[j]], cc))
            else:
                out.append(mb.f([A[j], A[j2], apex], cc))
    if base:
        mb.f(list(reversed(rings[0])), base_col or col)
    return out


def cyl(mb, c, n, t, rt, rb, h0, h1, segs, side, cap=None, cap_in=None, cap_frac=0.6, chamfer=0.0, inset_depth=0.0,
        base=True, cham_col=None):
    """Elliptic cylinder along n from h0 to h1 (top chamfer optional). Top cap: plain `cap`, or a ring + inner disc
    (`cap_in`, radius cap_frac, pushed by inset_depth along n)."""
    n, t, b = basis(n, t)
    c = Vector(c)
    ths = [2 * math.pi * j / segs for j in range(segs)]

    def ring(h, s=1.0):
        return [mb.v(c + t * (rt * s * math.cos(th)) + b * (rb * s * math.sin(th)) + n * h) for th in ths]

    def band(A, B, col):
        for j in range(segs):
            j2 = (j + 1) % segs
            mb.f([A[j], A[j2], B[j2], B[j]], col)

    R0 = ring(h0)
    R1 = ring(h1 - chamfer)
    band(R0, R1, side)
    top = R1
    if chamfer > 0:
        R2 = ring(h1, 1.0 - chamfer / max(rt, rb))
        band(R1, R2, cham_col or side)
        top = R2
    capc = cap or side
    if cap_in:
        s0 = 1.0 - chamfer / max(rt, rb)
        Ri = ring(h1, cap_frac)
        band(top, Ri, capc)
        if inset_depth:
            Rj = ring(h1 + inset_depth, cap_frac)
            band(Ri, Rj, capc)
            Ri = Rj
        mb.f(Ri, cap_in)
    else:
        mb.f(top, capc)
    if base:
        mb.f(list(reversed(R0)), side)


def box(mb, c, x, y, hx, hy, hz, col, bevel=0.0):
    """Box centred at c with local axes x, y (z = x cross y), half sizes hx, hy, hz; optional edge bevel."""
    x = Vector(x).normalized()
    y = Vector(y)
    y = (y - x * y.dot(x)).normalized()
    z = x.cross(y)
    M = Matrix.Translation(Vector(c)) @ Matrix((
        (x.x * hx * 2, y.x * hy * 2, z.x * hz * 2, 0),
        (x.y * hx * 2, y.y * hy * 2, z.y * hz * 2, 0),
        (x.z * hx * 2, y.z * hy * 2, z.z * hz * 2, 0),
        (0, 0, 0, 1)))
    res = bmesh.ops.create_cube(mb.bm, size=1.0, matrix=M)
    vs = res["verts"]
    fs = list({f for v in vs for f in v.link_faces})
    mb.recolor(fs, col)
    if bevel > 0:
        es = list({e for v in vs for e in v.link_edges})
        r = bmesh.ops.bevel(mb.bm, geom=vs + es, offset=bevel, segments=1, affect="EDGES", profile=0.5)
        mb.recolor(r["faces"], col)
    return fs


# ------------------------------------------------------------------ helpers: scenes / collections
def ensure_scene(name):
    sc = bpy.data.scenes.get(name) or bpy.data.scenes.new(name)
    return sc


def ensure_coll(sc, name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
    if c.name not in sc.collection.children:
        sc.collection.children.link(c)
    return c


def clear_coll(c):
    for o in list(c.objects):
        d = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if d is not None and d.users == 0:
            if isinstance(d, bpy.types.Mesh):
                bpy.data.meshes.remove(d)
            elif isinstance(d, bpy.types.Curve):
                bpy.data.curves.remove(d)
            elif isinstance(d, bpy.types.Camera):
                bpy.data.cameras.remove(d)
            elif isinstance(d, bpy.types.Light):
                bpy.data.lights.remove(d)


def to_object(mb, name, coll, mat, origin, shift, sharp_deg=31.0):
    """bmesh -> object. Geometry is in nominal model space; `origin` (nominal) becomes the object origin;
    `shift` recentres the whole model so its bounding-box centre is the world origin."""
    bm = mb.bm
    uvl = bm.loops.layers.uv.new("UVMap")
    for fa in bm.faces:
        u, v = cell_uv(fa[mb.pal])
        for l in fa.loops:
            l[uvl].uv = (u, v)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.translate(bm, verts=bm.verts, vec=-Vector(origin))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(sharp_deg))
    ob = bpy.data.objects.new(name, me)
    ob.location = Vector(origin) + shift
    coll.objects.link(ob)
    return ob


def empty(name, coll, loc, size=2.0):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = "SINGLE_ARROW"
    e.empty_display_size = size
    e.rotation_euler = (math.pi, 0, 0)       # arrow points DOWN = beam direction (-Z blender / -Y roblox)
    e.location = loc
    coll.objects.link(e)
    return e


def model_bounds(mbs):
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for mb in mbs:
        for v in mb.bm.verts:
            for k in range(3):
                lo[k] = min(lo[k], v.co[k])
                hi[k] = max(hi[k], v.co[k])
    return lo, hi


def ring_pods(mb, n_pods, rc, zc, nr, nz, rt, rb, rn, phase, lens="GREEN", socket="DKGREEN", useg=14, vseg=5):
    """Light pods on a rim chamfer whose outward normal (in the r-z plane) is (nr, nz)."""
    for k in range(n_pods):
        a = phase + 2 * math.pi * k / n_pods
        ca, sa = math.cos(a), math.sin(a)
        c = Vector((rc * ca, rc * sa, zc))
        nrm = Vector((nr * ca, nr * sa, nz)).normalized()
        tan = Vector((-sa, ca, 0.0))
        # socket (dark-green bezel) - starts inside the hull, protrudes a little
        cyl(mb, c - nrm * (rn * 0.6), nrm, tan, rt * 1.18, rb * 1.3, 0.0, rn * 0.85, useg, socket, cap=socket,
            chamfer=rn * 0.22)
        dome(mb, c + nrm * (rn * 0.2), nrm, tan, rt, rb, rn, useg, vseg, lens)


# ------------------------------------------------------------------ MOTHERSHIP (~120 studs wide)
MS_SEGS = 72


def half_disc_door(dm, sx, R, gap, zt, zb, steps, npts=36):
    """Closed half-disc door (sx=-1 left / +1 right of the seam at x=0). Bottom face is built as concentric
    half-rings, analytically offset inward (no bmesh inset spikes).
    steps: [(arc_inset, seam_inset, dz, colour-of-band), ...]; dz moves the ring down (-Z) relative to the previous
    ring; colour may be (a, b, period) for radial stripes."""
    cx = sx * gap

    def dring(d, ds, z):
        rho = R - d
        beta = math.asin(min(ds / rho, 0.999))
        a0 = (math.pi / 2 + beta) if sx < 0 else (-math.pi / 2 + beta)
        span = math.pi - 2 * beta
        return [dm.v((cx + rho * math.cos(a0 + span * k / npts), rho * math.sin(a0 + span * k / npts), z))
                for k in range(npts + 1)]

    top = dring(0.0, 0.0, zt)
    bot = dring(0.0, 0.0, zb)
    n = len(top)
    dm.f(top, "GUNMETAL")
    for k in range(n):
        k2 = (k + 1) % n
        dm.f([bot[k], bot[k2], top[k2], top[k]], "STEEL" if k < n - 1 else "TRIM")
    A = bot
    d_acc, ds_acc, z_acc = 0.0, 0.0, zb
    for (dd, dds, dz, col) in steps:
        d_acc += dd
        ds_acc += dds
        z_acc -= dz
        B = dring(d_acc, ds_acc, z_acc)
        for k in range(n):
            k2 = (k + 1) % n
            c = col if isinstance(col, str) else (col[0] if k == n - 1 else colour_of(col, k, 0))
            dm.f([A[k], B[k], B[k2], A[k2]], c)
        A = B
    return A


def build_mothership(coll, mat):
    S = MS_SEGS
    pieces = {}
    TOP = 10.5           # hull top plateau (bridge foot)
    UND0 = (55.6, -4.6)  # underside slope start (outer)
    UND1 = (34.0, -9.2)  # underside slope end (belly collar)
    FRAME_Z = -11.1      # belly frame bottom plane (= lowest point of the hull)
    BAY_R, BAY_TOP = 18.8, -3.0

    # ---- Hull
    hull = MB()
    prof = [
        (0.0, TOP, "STEEL"),
        (20.4, TOP, "DKGREEN"),                    # 1 green ring around the bridge foot
        (22.2, TOP, "SILVER"),                     # 2 bevel
        (22.8, TOP - 0.3, ("SILVER", "STEEL", 9, 4)),  # 3 tier-2 slope, 8 big panels
        (36.4, 7.6, "SILVER"),                     # 4 bevel
        (37.0, 7.2, "STEEL"),                      # 5 riser (window slots)
        (37.3, 5.4, "TRIM"),                       # 6 groove
        (37.9, 5.15, "GREEN"),                     # 7 green terrace stripe
        (40.6, 5.15, "STEEL"),                     # 8 bevel
        (41.2, 4.9, ("SILVER", "STEEL", 6, 3)),     # 9 tier-1 slope, 12 panels (+ radial light strips)
        (55.0, 2.9, "SILVER"),                     # 10
        (57.6, 2.5, "STEEL"),                      # 11 rounded rim shoulder
        (59.4, 1.9, "STEEL"),                      # 12
        (60.0, 1.2, "STEEL"),                      # 13 rim band
        (60.0, 0.6, "TRIM"),                       # 14 rim groove
        (59.4, 0.35, "DKGREEN"),                   # 15
        (59.4, -0.35, "TRIM"),                     # 16
        (60.0, -0.6, "STEEL"),                     # 17
        (60.0, -1.3, "STEEL"),                     # 18 bevel
        (59.6, -1.7, "GUNMETAL"),                  # 19 pod chamfer (LightRing sits here)
        (56.2, -4.3, "DEEP"),                      # 20
        (UND0[0], UND0[1], ("GUNMETAL", "DEEP", 9, 4)),  # 21 underside slope, 8 panels
        (UND1[0], UND1[1], "STEEL"),               # 22 belly collar
        (33.2, -9.6, "STEEL"),                     # 23
        (32.6, -10.7, "STEEL"),                    # 24
        (31.8, FRAME_Z, "DKGREEN"),                # 25 belly frame ring (flat, faces down)
        (27.6, FRAME_Z, ("GREEN", "TRIM", 3)),      # 26 green hazard stripes around the doors
        (23.4, FRAME_Z, "STEEL"),                  # 27
        (19.4, FRAME_Z, "STEEL"),                  # 28 bevel into the opening
        (BAY_R, FRAME_Z + 0.4, "BAY"),             # 29 opening wall (bay)
        (BAY_R, BAY_TOP, "BAY"),                   # 30 bay ceiling
        (0.0, BAY_TOP, None),
    ]
    hf = lathe(hull, prof, S)
    # window slots on the tier-2 riser (segment index = profile point index of its upper end)
    wins = [hf[(5, j)] for j in range(S) if j % 2 == 0]
    r = bmesh.ops.inset_individual(hull.bm, faces=wins, thickness=0.42, depth=-0.25, use_even_offset=True)
    hull.recolor(r["faces"], "DEEP")
    hull.recolor(wins, "GLASS")
    # radial green light strips on tier 1 (one per big panel)
    strips = [hf[(9, j)] for j in range(S) if j % 6 == 2]
    r = bmesh.ops.inset_individual(hull.bm, faces=strips, thickness=1.15, depth=-0.18, use_even_offset=True)
    hull.recolor(r["faces"], "DKGREEN")
    hull.recolor(strips, "GREEN")

    def z_at(rr):
        return UND0[1] + (UND0[0] - rr) / (UND0[0] - UND1[0]) * (UND1[1] - UND0[1])

    ud = (Vector(UND1) - Vector(UND0)).normalized()      # inward-down along the underside
    un = Vector((-ud.y, ud.x))
    if un.y > 0:
        un = -un                                          # surface normal (down / outward)
    # underside girders (8, on the panel seams) + thrusters (8, on the panel centres)
    for k in range(8):
        a = 2 * math.pi * k / 8
        ca, sa = math.cos(a), math.sin(a)
        r0, r1 = UND1[0] + 0.6, UND0[0] - 0.8
        rm = (r0 + r1) / 2
        pm = Vector((rm, z_at(rm))) + un * 0.25
        c = Vector((pm.x * ca, pm.x * sa, pm.y))
        xax = Vector((ud.x * ca, ud.x * sa, ud.y))
        box(hull, c, xax, (-sa, ca, 0), (r1 - r0) / 2 / abs(ud.x), 0.85, 0.55, "STEEL", bevel=0.22)
        a2 = a + math.pi / 8
        rr = 45.0
        c = Vector((rr * math.cos(a2), rr * math.sin(a2), z_at(rr) + 0.8))
        tdir = (math.cos(a2), math.sin(a2), 0)
        cyl(hull, c, (0, 0, -1), tdir, 3.4, 3.4, 0.0, 2.0, 20, "STEEL", cap="STEEL", cap_in="DKGREEN",
            cap_frac=0.72, chamfer=0.35)
        dome(hull, c + Vector((0, 0, -2.0)), (0, 0, -1), tdir, 3.4 * 0.56, 3.4 * 0.56, 0.5, 20, 4, "GREEN")
    # bay ceiling detail: launch clamps (4) + centre hatch, so an open bay doesn't read as an empty hole
    for k in range(4):
        a = 2 * math.pi * (k + 0.5) / 4
        c = Vector((11.0 * math.cos(a), 11.0 * math.sin(a), BAY_TOP))
        cyl(hull, c, (0, 0, -1), (1, 0, 0), 3.0, 3.0, -0.2, 0.9, 16, "GUNMETAL", cap="GUNMETAL", cap_in="DKGREEN",
            cap_frac=0.55, chamfer=0.2)
    cyl(hull, Vector((0, 0, BAY_TOP)), (0, 0, -1), (1, 0, 0), 4.2, 4.2, -0.2, 0.5, 24, "GUNMETAL", cap="DKGREEN",
        cap_in="GREEN", cap_frac=0.6)
    pieces["Hull"] = (hull, None)   # origin = model centre

    # ---- Bridge (command deck + glass dome)
    br = MB()
    B0 = TOP - 0.6
    dome_r, dome_z0, dome_h = 15.4, B0 + 4.8, 7.8
    prof = [
        (0.0, B0, "STEEL"),
        (19.3, B0, "SILVER"),
        (19.3, B0 + 1.3, "SILVER"),
        (18.9, B0 + 1.75, "STEEL"),      # 3 sloped window wall
        (17.7, B0 + 4.2, "SILVER"),
        (17.1, B0 + 4.8, "TRIM"),
        (dome_r + 0.4, dome_z0, "GLASS"),
    ]
    nd = 9
    cap_r = 2.8
    for k in range(nd + 1):
        phi = math.acos(cap_r / dome_r) * k / nd
        prof.append((dome_r * math.cos(phi), dome_z0 + dome_h * math.sin(phi), "GLASS"))
    ztop = prof[-1][1]
    prof[-1] = (prof[-1][0], prof[-1][1], "SILVER")
    prof += [(cap_r - 0.2, ztop + 0.45, "SILVER"), (cap_r - 0.6, ztop + 0.8, "SILVER"), (0.0, ztop + 0.8, None)]
    i_dome0 = 6
    i_dome1 = 6 + nd + 1

    def bridge_col(j, i):
        base = prof[i][2] if isinstance(prof[i][2], str) else "STEEL"
        if i_dome0 <= i < i_dome1:
            if j % 9 == 0:
                return "SILVER"                       # 8 dome ribs
            if 3 <= i - i_dome0 <= 6 and 46 <= j <= 50:
                return "GLASS_HI"                     # cartoon glass highlight streak
            return "GLASS"
        return base

    bf = lathe(br, [(r_, z_, bridge_col) for (r_, z_, _) in prof], S, flip=True)
    wins = [bf[(3, j)] for j in range(S) if j % 3 != 0]
    r = bmesh.ops.inset_individual(br.bm, faces=wins, thickness=0.32, depth=-0.22, use_even_offset=True)
    br.recolor(r["faces"], "DEEP")
    br.recolor(wins, "GLASS")
    pieces["Bridge"] = (br, None)   # origin = model centre
    bridge_top = ztop + 0.8

    # ---- Antenna
    an = MB()
    z0 = bridge_top - 0.3
    cyl(an, (0, 0, z0), (0, 0, 1), (1, 0, 0), 1.3, 1.3, 0.0, 1.0, 16, "STEEL", cap="STEEL", chamfer=0.3)
    cyl(an, (0, 0, z0), (0, 0, 1), (1, 0, 0), 0.42, 0.42, 0.9, 6.8, 12, "SILVER", cap="SILVER")
    cyl(an, (0, 0, z0 + 3.4), (0, 0, 1), (1, 0, 0), 1.5, 1.5, 0.0, 0.5, 16, "DKGREEN", cap="DKGREEN", chamfer=0.15)
    tip = Vector((0, 0, z0 + 7.6))
    dome(an, tip, (0, 0, 1), (1, 0, 0), 1.0, 1.0, 1.0, 14, 5, "GREEN", base=False)    # two open halves weld
    dome(an, tip, (0, 0, -1), (1, 0, 0), 1.0, 1.0, 1.0, 14, 5, "GREEN", base=False)   # into one closed sphere
    pieces["Antenna"] = (an, None)   # origin = model centre

    # ---- LightRing (24 pods on the rim chamfer). Spins about the vertical axis.
    lr = MB()
    p0, p1 = Vector((59.6, -1.7)), Vector((56.2, -4.3))
    mid = (p0 + p1) / 2
    d = (p1 - p0).normalized()
    nrm2 = Vector((-d.y, d.x))
    if nrm2.x < 0:
        nrm2 = -nrm2
    ring_pods(lr, 24, mid.x, mid.y, nrm2.x, nrm2.y, 3.0, 1.4, 1.1, phase=math.pi / 24, useg=18, vseg=5)
    pieces["LightRing"] = (lr, (0, 0, mid.y))

    # ---- Belly doors (closed). Hinge line = tangent at the door's outermost point, on its TOP face, parallel to Y;
    #      rotate about local Y to swing open downward.
    door_r, gap = BAY_R - 0.25, 0.12
    zt, zb = FRAME_Z + 1.0, FRAME_Z + 0.3
    # outer steel frame -> recessed dark-green band -> steel iris (radial stripes) -> raised green half-lens.
    # Seam-side insets are small so the two green halves read as ONE split circle from below.
    steps = [(0.7, 0.35, 0.0, "STEEL"), (0.25, 0.12, -0.2, "TRIM"), (1.6, 0.25, 0.0, "DKGREEN"),
             (0.25, 0.1, 0.2, "STEEL"), (6.6, 0.3, 0.0, ("STEEL", "GUNMETAL", 3)), (0.35, 0.12, 0.22, "DKGREEN")]
    for side, sx in (("BellyDoorL", -1), ("BellyDoorR", 1)):
        dm = MB()
        inner = half_disc_door(dm, sx, door_r, gap, zt, zb, steps)
        dm.f(list(reversed(inner)), "GREEN")
        pieces[side] = (dm, (sx * (door_r + gap), 0.0, zt))

    # ---- recentre on the bounding-box centre of the whole model
    lo, hi = model_bounds([p[0] for p in pieces.values()])
    center = (lo + hi) / 2
    shift = -center
    objs = {}
    for name, (mb, origin) in pieces.items():
        org = center if origin is None else Vector(origin)
        objs[name] = to_object(mb, "MS_" + name, coll, mat, org, shift)
    objs["BeamOrigin"] = empty("MS_BeamOrigin", coll, Vector((0, 0, FRAME_Z)) + shift, 6.0)
    return objs, (hi - lo), shift


# ------------------------------------------------------------------ SAUCER (~16 studs wide)
SC_SEGS = 48
SC_BAY_R = 3.25        # belly opening radius (diameter 6.5 = ~40% of the 16-stud saucer)
SC_FRAME_Z = -2.15     # frame bottom plane (lowest point of the saucer)
SC_BAY_TOP = -0.4      # bay ceiling (emitter lens hangs from here)
SC_COLLAR_R = 4.45


def build_saucer(coll, mat):
    S = SC_SEGS
    pieces = {}
    hull = MB()
    prof = [
        (0.0, 1.7, "STEEL"),
        (3.5, 1.7, "STEEL"),                   # (under the dome)
        (3.5, 2.15, "DKGREEN"),                # dome collar: dark-green top ring
        (3.95, 2.15, "STEEL"),
        (4.25, 1.95, "STEEL"),                 # collar outer wall
        (4.45, 1.55, ("SILVER", "STEEL", 6, 3)),  # upper slope, 8 panels
        (6.8, 0.8, "SILVER"),
        (7.55, 0.5, "STEEL"),
        (7.95, 0.22, "TRIM"),
        (8.0, 0.08, "GREEN"),                  # thin green rim line
        (8.0, -0.1, "STEEL"),
        (7.95, -0.2, "GUNMETAL"),              # pod chamfer (RimLights)
        (6.85, -1.15, "DEEP"),
        (6.65, -1.25, ("GUNMETAL", "DEEP", 6, 3)),  # underside, 8 panels
        (SC_COLLAR_R, -1.6, "STEEL"),          # belly collar (frames the opening, reads from below)
        (4.25, -1.75, "STEEL"),
        (4.05, -2.05, "STEEL"),
        (3.9, SC_FRAME_Z, "DKGREEN"),          # flat frame ring around the doors (lowest plane of the ship)
        (3.55, SC_FRAME_Z, "STEEL"),           # bevel into the opening
        (SC_BAY_R, SC_FRAME_Z + 0.2, "BAY"),   # opening wall (dark bay)
        (SC_BAY_R, -0.7, "DKGREEN"),           # dark-green band under the ceiling
        (SC_BAY_R, SC_BAY_TOP, "BAY"),         # bay ceiling
        (0.0, SC_BAY_TOP, None),
    ]
    lathe(hull, prof, S)
    # beam emitter on the bay ceiling: steel mount -> dark-green ring -> green lens bulging down
    cyl(hull, Vector((0, 0, SC_BAY_TOP)), (0, 0, -1), (1, 0, 0), 1.75, 1.75, -0.1, 0.18, 32, "STEEL", cap="STEEL",
        cap_in="DKGREEN", cap_frac=0.82, chamfer=0.05)
    dome(hull, Vector((0, 0, SC_BAY_TOP - 0.18)), (0, 0, -1), (1, 0, 0), 1.3, 1.3, 0.32, 32, 5, "GREEN")
    pieces["Hull"] = (hull, None)   # origin = model centre

    dm = MB()
    dr, dz0, dh = 3.55, 1.55, 2.55
    nd = 9
    dprof = [(0.0, dz0 - 0.05, "GLASS"), (dr, dz0 - 0.05, "GLASS")]
    for k in range(nd + 1):
        phi = (math.pi / 2) * k / nd
        rr = dr * math.cos(phi)
        dprof.append((rr if rr > 1e-4 else 0.0, dz0 + dh * math.sin(phi), "GLASS"))

    def dome_col(j, i):
        if 4 <= i <= 7 and 30 <= j <= 32:
            return "GLASS_HI"
        return "GLASS"

    lathe(dm, [(r_, z_, dome_col) for (r_, z_, _) in dprof], S, flip=True)
    pieces["Dome"] = (dm, None)   # origin = model centre

    rl = MB()
    p0, p1 = Vector((7.95, -0.2)), Vector((6.85, -1.15))
    mid = (p0 + p1) / 2
    d = (p1 - p0).normalized()
    nrm2 = Vector((-d.y, d.x))
    if nrm2.x < 0:
        nrm2 = -nrm2
    ring_pods(rl, 12, mid.x, mid.y, nrm2.x, nrm2.y, 0.85, 0.42, 0.34, phase=math.pi / 12, useg=16, vseg=5)
    pieces["RimLights"] = (rl, (0, 0, mid.y))

    # ---- belly doors (closed), same mechanism as the mothership: half discs split along Y, hinge = outer edge of
    #      the TOP face (origin), hinge axis = Blender Y (= Roblox Z). L opens with +Y rotation, R with -Y.
    door_r, gap = SC_BAY_R - 0.08, 0.05
    zb = SC_FRAME_Z + 0.1
    zt = zb + 0.3
    steps = [(0.22, 0.08, 0.0, "STEEL"), (0.08, 0.03, -0.06, "TRIM"), (0.35, 0.05, 0.0, "DKGREEN"),
             (0.08, 0.03, 0.06, "STEEL"), (0.9, 0.06, 0.0, ("STEEL", "GUNMETAL", 3)), (0.1, 0.03, 0.06, "DKGREEN")]
    for side, sx in (("BellyDoorL", -1), ("BellyDoorR", 1)):
        dmd = MB()
        inner = half_disc_door(dmd, sx, door_r, gap, zt, zb, steps)
        dmd.f(list(reversed(inner)), "GREEN")
        pieces[side] = (dmd, (sx * (door_r + gap), 0.0, zt))

    lo, hi = model_bounds([p[0] for p in pieces.values()])
    center = (lo + hi) / 2
    shift = -center
    objs = {}
    for name, (mb, origin) in pieces.items():
        org = center if origin is None else Vector(origin)
        objs[name] = to_object(mb, "SC_" + name, coll, mat, org, shift)
    objs["BeamOrigin"] = empty("SC_BeamOrigin", coll, Vector((0, 0, SC_FRAME_Z)) + shift, 1.5)
    STATE["saucer_lens"] = Vector((0, 0, SC_BAY_TOP - 0.18 - 0.32)) + shift
    return objs, (hi - lo), shift


# ------------------------------------------------------------------ stage (world, lights, cameras)
SKY_TOP = (0x86, 0xBE, 0xEC)
SKY_BOT = (0xD6, 0xEA, 0xF8)


def stage_world():
    w = bpy.data.worlds.get("UFO_World") or bpy.data.worlds.new("UFO_World")
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.62, 0.68, 0.76, 1.0)
    bg.inputs["Strength"].default_value = 0.75
    return w


def stage_lights():
    c = bpy.data.collections.get("UFO_Lights")
    if c is None:
        c = bpy.data.collections.new("UFO_Lights")
    clear_coll(c)

    def sun(name, rot, energy, ang, col=(1, 1, 1)):
        ld = bpy.data.lights.new(name, "SUN")
        ld.energy = energy
        ld.angle = math.radians(ang)
        ld.color = col
        o = bpy.data.objects.new(name, ld)
        o.rotation_euler = [math.radians(a) for a in rot]
        c.objects.link(o)

    sun("Key", (38, 0, 30), 2.4, 12, (1.0, 0.98, 0.95))
    sun("Fill", (180 + 25, 0, -140), 1.1, 30, (0.85, 0.92, 1.0))   # from below
    sun("Rim", (65, 0, 200), 1.3, 20)
    return c


def stage_scene(sc, world, lights, res=(1600, 1000)):
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    try:
        sc.eevee.taa_render_samples = 48
    except Exception:
        pass
    sc.world = world
    if lights.name not in sc.collection.children:
        sc.collection.children.link(lights)
    cam = sc.objects.get(sc.name + "_Cam")
    if cam is None:
        cd = bpy.data.cameras.new(sc.name + "_Cam")
        cam = bpy.data.objects.new(sc.name + "_Cam", cd)
        sc.collection.objects.link(cam)
    sc.camera = cam
    return cam


def aim(cam, loc, target, lens=50.0):
    cam.location = Vector(loc)
    d = Vector(target) - Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.clip_start = 0.1
    cam.data.clip_end = 5000


def composite_sky(src, dst):
    import numpy as np
    im = bpy.data.images.load(src, check_existing=False)
    w, h = im.size
    a = np.empty(w * h * 4, dtype=np.float32)
    im.pixels.foreach_get(a)
    a = a.reshape(h, w, 4)
    t = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None, None]       # row 0 = bottom
    top = np.array(SKY_TOP, np.float32) / 255.0
    bot = np.array(SKY_BOT, np.float32) / 255.0
    sky = bot[None, None, :] * (1 - t) + top[None, None, :] * t
    al = a[:, :, 3:4]
    rgb = a[:, :, :3] * al + sky * (1 - al)
    outp = np.concatenate([rgb, np.ones((h, w, 1), np.float32)], axis=2)
    o = bpy.data.images.new("sky_tmp", w, h, alpha=False)
    o.pixels.foreach_set(outp.ravel())
    o.filepath_raw = dst
    o.file_format = "PNG"
    o.save()
    bpy.data.images.remove(o)
    bpy.data.images.remove(im)
    try:
        os.remove(src)
    except OSError:
        pass


def render_to(sc, path):
    tmp = path[:-4] + "_rgba_tmp.png"
    sc.render.filepath = tmp
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    win = bpy.context.window
    prev = win.scene
    win.scene = sc
    try:
        bpy.ops.render.render(write_still=True, scene=sc.name)
    finally:
        win.scene = prev
    composite_sky(tmp, path)
    return path


# ------------------------------------------------------------------ build / render / export / report
STATE = {}


def setup_new_file():
    """One-time: turn whatever file is open into a clean ufo_models.blend WITHOUT touching the file on disk
    (everything is removed in memory, then saved under the new path)."""
    if bpy.data.filepath == BLEND:
        return "already " + BLEND
    keep = bpy.data.scenes.new("Mothership")
    bpy.context.window.scene = keep
    for sc in list(bpy.data.scenes):
        if sc != keep:
            bpy.data.scenes.remove(sc)
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.armatures, bpy.data.actions, bpy.data.materials,
                 bpy.data.cameras, bpy.data.lights, bpy.data.curves, bpy.data.worlds, bpy.data.node_groups,
                 bpy.data.texts, bpy.data.collections):
        for d in list(coll):
            try:
                coll.remove(d)
            except Exception:
                pass
    for im in list(bpy.data.images):
        if im.type == "IMAGE":
            bpy.data.images.remove(im)
    bpy.data.orphans_purge(do_recursive=True)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return "saved " + BLEND


def build_all(save=True):
    img = make_palette()
    mat = palette_material(img)
    world = stage_world()
    lights = stage_lights()
    out = {}
    for model, builder in (("Mothership", build_mothership), ("Saucer", build_saucer)):
        sc = ensure_scene(model)
        coll = ensure_coll(sc, model)
        clear_coll(coll)
        objs, size, shift = builder(coll, mat)
        stage_scene(sc, world, lights)
        STATE[model] = {"size": size, "shift": shift}
        out[model] = {"size": [round(v, 2) for v in size], "objects": list(objs.keys())}
    build_lineup(world, lights)
    for me in list(bpy.data.meshes):
        if me.users == 0:
            bpy.data.meshes.remove(me)
    if save:
        bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return out


def rebuild_saucer(save=True):
    """Rebuild ONLY the Saucer (+ lineup). The Mothership objects / Mothership.fbx are left as they are."""
    img = bpy.data.images.get("ufo_palette.png") or make_palette()
    mat = bpy.data.materials.get("UFO_Palette") or palette_material(img)
    world = stage_world()
    lights = bpy.data.collections.get("UFO_Lights") or stage_lights()
    sc = ensure_scene("Saucer")
    coll = ensure_coll(sc, "Saucer")
    clear_coll(coll)
    objs, size, shift = build_saucer(coll, mat)
    stage_scene(sc, world, lights)
    STATE["Saucer"] = {"size": size, "shift": shift}
    build_lineup(world, lights)
    for me in list(bpy.data.meshes):
        if me.users == 0:
            bpy.data.meshes.remove(me)
    if save:
        bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return {"size": [round(v, 2) for v in size], "objects": list(objs.keys())}


def size_of(model):
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for o in bpy.data.collections[model].objects:
        if o.type != "MESH":
            continue
        for v in o.data.vertices:
            p = o.location + v.co
            for k in range(3):
                lo[k] = min(lo[k], p[k])
                hi[k] = max(hi[k], p[k])
    return lo, hi


def build_lineup(world, lights):
    sc = ensure_scene("Lineup")
    coll = ensure_coll(sc, "Lineup_Stage")
    clear_coll(coll)
    bpy.context.view_layer.update()
    lo_m, hi_m = size_of("Mothership")
    lo_s, hi_s = size_of("Saucer")
    mx = 0.0
    sx = hi_m.x + 14.0 - lo_s.x
    hx = sx + hi_s.x + 9.0
    for name, x, lo in (("Mothership", mx, lo_m), ("Saucer", sx, lo_s)):
        inst = bpy.data.objects.new("Inst_" + name, None)
        inst.instance_type = "COLLECTION"
        inst.instance_collection = bpy.data.collections[name]
        inst.location = (x, 0.0, -lo.z)
        coll.objects.link(inst)
    # human reference: 5-stud capsule
    mb = MB()
    rad = 0.85
    cyl(mb, (hx, 0, rad), (0, 0, 1), (1, 0, 0), rad, rad, 0.0, 5.0 - 2 * rad, 16, "SILVER", base=False)
    dome(mb, (hx, 0, 5.0 - rad), (0, 0, 1), (1, 0, 0), rad, rad, rad, 16, 6, "SILVER")
    dome(mb, (hx, 0, rad), (0, 0, -1), (1, 0, 0), rad, rad, rad, 16, 6, "SILVER")
    hm = flat_material("HumanRef_Orange", "FF8A2A", 0.5)
    o = to_object(mb, "HumanRef_5studs", coll, hm, (hx, 0, 0), Vector((0, 0, 0)))
    o.data.materials[0] = hm
    # ground: a floating display slab, so the sky-blue background stays visible
    gm = flat_material("Ground_Grey", "B4BEC8", 0.95)
    x0, x1 = -90.0, hx + 40.0
    gb = MB()
    box(gb, ((x0 + x1) / 2, 15.0, -0.8), (1, 0, 0), (0, 1, 0), (x1 - x0) / 2, 72.0, 0.8, "STEEL", bevel=0.3)
    g = to_object(gb, "Ground", coll, gm, (0, 0, 0), Vector((0, 0, 0)))
    g.data.materials[0] = gm
    # labels
    lm = flat_material("Label_Dark", "1E2A36", 0.8)
    hm_ = hi_m.z - lo_m.z
    hs_ = hi_s.z - lo_s.z
    for txt, x, z, sz in (("MOTHERSHIP  120 studs", mx, hm_ + 3.0, 5.0), ("SAUCER  16", sx, hs_ + 2.0, 2.6),
                          ("PLAYER  5", hx, 6.2, 1.8)):
        cu = bpy.data.curves.new("lbl_" + txt.split()[0], "FONT")
        cu.body = txt
        cu.align_x = "CENTER"
        cu.size = sz
        cu.extrude = 0.05
        to = bpy.data.objects.new("Label_" + txt.split()[0], cu)
        to.data.materials.append(lm)
        to.location = (x, 0.0, z)
        to.rotation_euler = (math.pi / 2, 0, 0)
        coll.objects.link(to)
    stage_scene(sc, world, lights, res=(2400, 1000))
    STATE["lineup"] = {"mx": mx, "sx": sx, "hx": hx}
    return sc


def render_all(models=("Mothership", "Saucer"), lineup=True):
    files = []
    for model, R in (("Mothership", 60.0), ("Saucer", 8.0)):
        if model not in models:
            continue
        sc = bpy.data.scenes[model]
        cam = sc.camera
        lo, hi = size_of(model)
        ctr = (lo + hi) / 2
        k = R / 60.0
        # front (level)
        aim(cam, ctr + Vector((0, -205 * k, 6 * k)), ctr, 50)
        files.append(render_to(sc, os.path.join(OUT, model + "_front.png")))
        # 3/4 from below (how players see it)
        az, el, dist = math.radians(-35), math.radians(-17), 215 * k
        loc = ctr + Vector((math.sin(-az) * math.cos(el) * dist, -math.cos(az) * math.cos(el) * dist, math.sin(el) * dist))
        aim(cam, loc, ctr, 50)
        files.append(render_to(sc, os.path.join(OUT, model + "_threequarter_below.png")))
        # underside
        cam.location = ctr + Vector((0, 0, -300 * k))
        cam.rotation_euler = (math.pi, 0, 0)
        cam.data.lens = 50
        files.append(render_to(sc, os.path.join(OUT, model + "_underside.png")))
        pre = "MS_" if model == "Mothership" else "SC_"
        if bpy.data.objects.get(pre + "BellyDoorL"):
            # belly doors swung open 85 deg about their hinge (local Y) - checks the pivots
            dl, dr = bpy.data.objects[pre + "BellyDoorL"], bpy.data.objects[pre + "BellyDoorR"]
            dl.rotation_euler.y, dr.rotation_euler.y = math.radians(85), math.radians(-85)
            if model == "Mothership":
                az, el, dist, look = math.radians(-30), math.radians(-24), 200 * k, Vector((0, 0, -8))
            else:
                az, el, dist, look = math.radians(-28), math.radians(-34), 300 * k, Vector((0, 0, -1.4))
            loc = ctr + Vector((math.sin(-az) * math.cos(el) * dist, -math.cos(az) * math.cos(el) * dist,
                                math.sin(el) * dist))
            aim(cam, loc, ctr + look, 50)
            try:
                files.append(render_to(sc, os.path.join(OUT, model + "_doors_open.png")))
            finally:
                dl.rotation_euler.y, dr.rotation_euler.y = 0.0, 0.0
    if not lineup:
        bpy.ops.wm.save_as_mainfile(filepath=BLEND)
        return files
    sc = bpy.data.scenes["Lineup"]
    L = STATE.get("lineup")
    if L is None:
        bpy.context.view_layer.update()
        lo_m, hi_m = size_of("Mothership")
        L = {"mx": 0.0, "hx": 110.0}
    lo_m, hi_m = size_of("Mothership")
    cx = (-62 + L["hx"] + 4) / 2
    width = (L["hx"] + 4) - (-62)
    el = math.radians(6.0)                      # orthographic = exact size comparison
    tgt = Vector((cx, 0, 20))
    aim(sc.camera, tgt + Vector((0, -math.cos(el), math.sin(el))) * 400, tgt, 50)
    sc.camera.data.type = "ORTHO"
    sc.camera.data.ortho_scale = width * 1.1
    files.append(render_to(sc, os.path.join(OUT, "UFO_lineup.png")))
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return files


FBX_ARGS = dict(use_selection=True, global_scale=0.01, apply_unit_scale=True, apply_scale_options="FBX_SCALE_NONE",
                axis_forward="-Z", axis_up="Y", object_types={"MESH", "EMPTY"}, use_mesh_modifiers=True,
                mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False, path_mode="COPY",
                embed_textures=True)


def export_model(model):
    prefix = "MS_" if model == "Mothership" else "SC_"
    sc = bpy.data.scenes[model]
    objs = list(bpy.data.collections[model].objects)
    win = bpy.context.window
    prev = win.scene
    win.scene = sc
    vl = sc.view_layers[0]
    names = {}
    path = os.path.join(OUT, model + ".fbx")
    try:
        for o in objs:
            bare = o.name[len(prefix):] if o.name.startswith(prefix) else o.name
            names[o] = (o.name, o.data.name if o.data else None)
            o.name = bare
            if o.data:
                o.data.name = bare
        with bpy.context.temp_override(window=win, scene=sc, view_layer=vl):
            for o in vl.objects:
                o.select_set(o in objs, view_layer=vl)
            vl.objects.active = objs[0]
            bpy.ops.export_scene.fbx(filepath=path, **FBX_ARGS)
    finally:
        for o, (on, dn) in names.items():
            o.name = on
            if o.data and dn:
                o.data.name = dn
        win.scene = prev
    return {"fbx": path, "kb": round(os.path.getsize(path) / 1024, 1)}


def export_all():
    return [export_model("Mothership"), export_model("Saucer")]


def report():
    rep = {}
    for model in ("Mothership", "Saucer"):
        lo, hi = size_of(model)
        d = {"size_studs": [round(v, 2) for v in (hi - lo)], "bbox_center": [round(v, 3) for v in (lo + hi) / 2],
             "objects": {}}
        tot = 0
        for o in sorted(bpy.data.collections[model].objects, key=lambda x: x.name):
            if o.type == "MESH":
                tris = sum(len(p.vertices) - 2 for p in o.data.polygons)
                tot += tris
                ws = [o.location + v.co for v in o.data.vertices]
                blo = Vector([min(p[k] for p in ws) for k in range(3)])
                bhi = Vector([max(p[k] for p in ws) for k in range(3)])
                d["objects"][o.name] = {"tris": tris, "origin": [round(v, 3) for v in o.location],
                                        "size": [round(v, 2) for v in (bhi - blo)],
                                        "bbox_center": [round(v, 3) for v in (blo + bhi) / 2]}
            else:
                d["objects"][o.name] = {"empty": True, "origin": [round(v, 3) for v in o.location]}
        d["tris_total"] = tot
        rep[model] = d
    return rep


def check_normals():
    """Roblox culls back faces: every closed island must have a positive signed volume (= normals point out)."""
    res = {}
    for m in ("Mothership", "Saucer"):
        for o in bpy.data.collections[m].objects:
            if o.type != "MESH":
                continue
            bm = bmesh.new()
            bm.from_mesh(o.data)
            seen, bad, n_isl = set(), [], 0
            for f in bm.faces:
                if f.index in seen:
                    continue
                stack, isl = [f], []
                seen.add(f.index)
                while stack:
                    g = stack.pop()
                    isl.append(g)
                    for e in g.edges:
                        for h in e.link_faces:
                            if h.index not in seen:
                                seen.add(h.index)
                                stack.append(h)
                vol = 0.0
                for g in isl:
                    vs = [l.vert.co for l in g.loops]
                    for i in range(1, len(vs) - 1):
                        vol += vs[0].dot(vs[i].cross(vs[i + 1])) / 6.0
                n_isl += 1
                if vol <= 0:
                    bad.append(round(vol, 3))
            res[o.name] = {"islands": n_isl, "inside_out": len(bad),
                           "non_manifold_edges": sum(1 for e in bm.edges if not e.is_manifold)}
            bm.free()
    return res
