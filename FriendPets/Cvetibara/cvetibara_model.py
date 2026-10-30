# Cvetibara (Tsvetelina's pet) - celestial winged capybara for SLINGSHOT.
# Style target (research 2026-10-08, Steal an Egg "Winged Lamb"/"Red Panda"): chibi proportions, soft rounded
# forms, big glossy eyes, warm saturated colours, gold trim + glow on the celestial parts. NOT studded.
# Built procedurally: metaball body -> voxel remesh -> smooth -> decimate; parts placed on the body surface
# by ray casts. Colours = per-vertex "Col" attribute (baked to a texture at export).
# Facing: -Y (Blender front view). Ground: z = 0. Units: 1 BU ~ 1 stud before in-game scaling.
import bpy, bmesh, math, os
from mathutils import Vector, Matrix, Quaternion

OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\FriendPets\Cvetibara"
COLL = "Cvetibara"


def lin(c):
    """sRGB 0-255 -> linear 0-1 (FLOAT_COLOR attributes are linear)."""
    def f(x):
        x = x / 255.0
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return (f(c[0]), f(c[1]), f(c[2]), 1.0)


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(4))


def smooth(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ palette (sRGB)
FUR_TOP = lin((198, 128, 78))      # warm caramel-brown back (capybara)
FUR_SIDE = lin((226, 164, 106))
FUR_UNDER = lin((255, 232, 198))   # cream belly / chin
MUZZLE = lin((246, 212, 168))
PAW = lin((150, 92, 58))
BLUSH = lin((255, 150, 165))
NOSE = lin((84, 52, 46))
NOSE_DARK = lin((40, 24, 24))
EYE_TOP = lin((22, 16, 34))
EYE_LOW = lin((112, 82, 196))      # celestial lilac glint in the lower iris
WHITE = lin((255, 255, 255))
FEATHER_ROOT = lin((236, 226, 255))  # faint lilac at the feather roots
FEATHER = lin((255, 255, 255))
GOLD = lin((255, 200, 64))
GOLD_DEEP = lin((235, 150, 30))
PETAL_IN = lin((255, 120, 190))
PETAL_OUT = lin((206, 150, 255))
EAR_IN = lin((255, 168, 170))


# ------------------------------------------------------------------ scene helpers
def reset():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for block in (bpy.data.meshes, bpy.data.metaballs, bpy.data.materials, bpy.data.curves, bpy.data.armatures,
                  bpy.data.cameras, bpy.data.lights, bpy.data.actions):
        for d in list(block):
            if d.users == 0:
                block.remove(d)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)
    coll = bpy.data.collections.new(COLL)
    bpy.context.scene.collection.children.link(coll)
    return coll


def materials():
    def mat(name, glow):
        m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
        attr = nt.nodes.new("ShaderNodeVertexColor")
        attr.layer_name = "Col"
        nt.links.new(attr.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.55
        if glow:
            nt.links.new(attr.outputs["Color"], bsdf.inputs["Emission Color"])
            bsdf.inputs["Emission Strength"].default_value = 1.6
        nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
        return m
    return mat("PetToon", False), mat("PetGlow", True)


def new_obj(coll, name, bm, mat, smooth_shade=True):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth_shade:
        for p in me.polygons:
            p.use_smooth = True
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def color_layer(bm):
    return bm.verts.layers.float_color.get("Col") or bm.verts.layers.float_color.new("Col")


def blob(bm, layer, matrix, deform, color, useg=16, vseg=10):
    """A deformed UV sphere added to bm. deform(unit_co) -> local co; color(unit_co, local_co) -> rgba."""
    res = bmesh.ops.create_uvsphere(bm, u_segments=useg, v_segments=vseg, radius=1.0)
    for v in res["verts"]:
        u = v.co.copy()
        lc = deform(u)
        v.co = matrix @ lc
        v[layer] = color(u, lc)
    return res["verts"]


def tube(bm, layer, pts, r0, r1, color, sides=8):
    """A smooth closed tube along pts, radius r0 -> r1."""
    rings = []
    for i, p in enumerate(pts):
        t = i / (len(pts) - 1)
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        a = d.orthogonal().normalized()
        b = d.cross(a)
        r = r0 + (r1 - r0) * t
        ring = []
        for j in range(sides):
            ang = 2 * math.pi * j / sides
            v = bm.verts.new(p + (a * math.cos(ang) + b * math.sin(ang)) * r)
            v[layer] = color
            ring.append(v)
        rings.append(ring)
    for i in range(len(rings) - 1):
        for j in range(sides):
            bm.faces.new((rings[i][j], rings[i + 1][j], rings[i + 1][(j + 1) % sides], rings[i][(j + 1) % sides]))
    for ring, p in ((rings[0], pts[0]), (rings[-1], pts[-1])):
        c = bm.verts.new(p)
        c[layer] = color
        for j in range(sides):
            bm.faces.new((c, ring[(j + 1) % sides], ring[j]) if ring is rings[0] else (c, ring[j], ring[(j + 1) % sides]))


def frame(origin, x_axis, z_axis):
    """4x4 matrix with local X along x_axis and local Z as close as possible to z_axis."""
    x = x_axis.normalized()
    z = (z_axis - x * z_axis.dot(x)).normalized()
    y = z.cross(x)
    m = Matrix((x, y, z)).transposed().to_4x4()
    m.translation = origin
    return m


# ------------------------------------------------------------------ body (metaballs)
def build_body(coll, mat):
    mb = bpy.data.metaballs.new("BodyMB")
    mb.resolution = 0.03
    mb.render_resolution = 0.03
    mb.threshold = 0.6
    mbo = bpy.data.objects.new("BodyMB", mb)
    coll.objects.link(mbo)

    def el(kind, co, r, size=(1, 1, 1), stiff=2.0):
        e = mb.elements.new(type=kind)
        e.co = co
        e.radius = r
        e.stiffness = stiff
        if kind != "BALL":
            e.size_x, e.size_y, e.size_z = size
        return e

    # Calibrated 2026-10-08: one element alone -> surface half-size = 0.575 * radius * size (ELLIPSOID),
    # CUBE -> size + 0.575 * radius. Overlaps swell a little, so targets are ~8% under the wanted size.
    K = 0.575

    def ell(co, radii, stiff=2.0):  # ellipsoid with the given surface half-sizes
        el("ELLIPSOID", co, 1.0, tuple(r / K for r in radii), stiff)

    def box(co, half, round_r, stiff=2.0):  # rounded box with the given half-sizes and corner rounding
        rr = round_r / K
        el("CUBE", co, rr, tuple(max(0.0, h - round_r) for h in half), stiff)

    # barrel body + rump (capybara loaf: long, round, sits low on stubby legs)
    ell((0, 0.40, 0.86), (0.64, 0.94, 0.56))
    ell((0, 1.02, 0.84), (0.56, 0.42, 0.48))
    # long rounded-box capybara head (no neck), a big blunt rectangular snout and small cheeks
    box((0, -0.74, 1.56), (0.52, 0.70, 0.47), 0.34)
    box((0, -1.26, 1.42), (0.44, 0.34, 0.36), 0.28)
    ell((0.30, -1.02, 1.40), (0.20, 0.20, 0.18))
    ell((-0.30, -1.02, 1.40), (0.20, 0.20, 0.18))
    # short stubby legs that reach the ground (z = 0)
    for sx in (1, -1):
        ell((sx * 0.40, -0.16, 0.24), (0.18, 0.19, 0.25))
        ell((sx * 0.42, 1.06, 0.26), (0.20, 0.22, 0.27))
    bpy.context.view_layer.update()

    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(mbo.evaluated_get(dg))
    bpy.data.objects.remove(mbo, do_unlink=True)
    bpy.data.metaballs.remove(mb)
    body = bpy.data.objects.new("Body", me)
    coll.objects.link(body)

    # clean, even topology: voxel remesh -> smooth -> decimate
    me.remesh_voxel_size = 0.028
    with bpy.context.temp_override(object=body, active_object=body, selected_objects=[body]):
        bpy.ops.object.voxel_remesh()
    sm = body.modifiers.new("Smooth", "SMOOTH")
    sm.factor, sm.iterations = 0.6, 6
    dec = body.modifiers.new("Decimate", "DECIMATE")
    dec.ratio = 1.0
    dg = bpy.context.evaluated_depsgraph_get()
    tris = sum(len(p.vertices) - 2 for p in body.evaluated_get(dg).data.polygons)
    dec.ratio = min(1.0, 5200 / max(tris, 1))
    with bpy.context.temp_override(object=body, active_object=body, selected_objects=[body]):
        bpy.ops.object.modifier_apply(modifier="Smooth")
        bpy.ops.object.modifier_apply(modifier="Decimate")
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(mat)
    return body


def color_body(body, cheeks):
    me = body.data
    attr = me.color_attributes.get("Col") or me.color_attributes.new("Col", "FLOAT_COLOR", "POINT")
    me.color_attributes.active_color = attr
    normals = [v.normal for v in me.vertices]
    for i, v in enumerate(me.vertices):
        co, n = v.co, normals[i]
        c = mix(FUR_SIDE, FUR_TOP, smooth(0.0, 0.85, n.z))          # darker on top
        c = mix(c, FUR_UNDER, smooth(-0.05, -0.7, n.z) * 0.95)       # cream belly
        # light muzzle: a soft oval around the snout (no hard edges)
        dm = Vector(((co.x) / 0.50, (co.y + 1.40) / 0.45, (co.z - 1.40) / 0.40)).length
        c = mix(c, MUZZLE, smooth(1.0, 0.55, dm))
        c = mix(c, PAW, smooth(0.20, 0.03, co.z))                     # darker paw tips
        for ch in cheeks:                                             # soft blush
            d = (co - ch).length
            c = mix(c, BLUSH, smooth(0.20, 0.05, d) * 0.85)
        attr.data[i].color = c


def surface(body, origin, target):
    """First hit on the body along origin -> target (body has identity transform)."""
    d = (Vector(target) - Vector(origin)).normalized()
    ok, loc, nrm, _ = body.ray_cast(Vector(origin), d)
    if not ok:
        raise RuntimeError(f"no surface hit from {origin} to {target}")
    return loc, nrm


# ------------------------------------------------------------------ face
def build_face(coll, body, mat, mat_glow):
    bm = bmesh.new()
    L = color_layer(bm)
    eyes = []
    for sx in (1, -1):
        loc, n = surface(body, (sx * 0.62, -2.6, 1.86), (sx * 0.22, -0.7, 1.78))
        side = Vector((1, 0, 0)) - n * n.x
        m = frame(loc - n * 0.04, side, n)  # local X = screen right, local Z = out of the face
        # big glossy oval eye: tall, flat; dark top -> lilac bottom glint
        blob(bm, L, m, lambda u: Vector((u.x * 0.165, u.y * 0.20, u.z * 0.08)),
             lambda u, lc: mix(EYE_TOP, EYE_LOW, smooth(0.15, -0.95, u.y)), 16, 10)
        # two highlights (upper big, lower small), both on the upper-outer side
        hm = m @ Matrix.Translation((sx * 0.05, 0.08, 0.07))
        blob(bm, L, hm, lambda u: Vector((u.x * 0.06, u.y * 0.065, u.z * 0.025)), lambda u, lc: WHITE, 10, 6)
        hm2 = m @ Matrix.Translation((-sx * 0.055, -0.09, 0.065))
        blob(bm, L, hm2, lambda u: Vector((u.x * 0.028, u.y * 0.028, u.z * 0.015)), lambda u, lc: WHITE, 8, 5)
        eyes.append(loc)
    # wide capybara nose pad on the muzzle front, with two nostrils
    loc, n = surface(body, (0, -2.6, 1.66), (0, -1.0, 1.56))
    m = frame(loc - n * 0.03, Vector((1, 0, 0)), n)
    blob(bm, L, m, lambda u: Vector((u.x * 0.19, u.y * 0.09, u.z * 0.06)), lambda u, lc: NOSE, 16, 8)
    for sx in (1, -1):
        nm = m @ Matrix.Translation((sx * 0.08, 0.0, 0.045))
        blob(bm, L, nm, lambda u: Vector((u.x * 0.033, u.y * 0.026, u.z * 0.02)), lambda u, lc: NOSE_DARK, 8, 5)
    # small content smile under the nose ("w")
    z0 = loc.z - 0.13
    for k in range(15):
        t = k / 14.0
        x = (t - 0.5) * 0.22
        y = -abs(math.sin(t * math.pi * 2)) * 0.035
        p, pn = surface(body, (x, -2.6, z0 + y), (x * 0.5, -1.0, z0 + y))
        mm = frame(p - pn * 0.012, Vector((1, 0, 0)), pn)
        blob(bm, L, mm, lambda u: Vector((u.x * 0.022, u.y * 0.016, u.z * 0.012)), lambda u, lc: NOSE_DARK, 6, 4)
    face = new_obj(coll, "Face", bm, mat)
    return face, eyes


def build_ears(coll, body, mat):
    bm = bmesh.new()
    L = color_layer(bm)
    for sx in (1, -1):
        loc, n = surface(body, (sx * 0.95, -0.30, 2.40), (sx * 0.10, -0.55, 1.55))
        out = (n + Vector((sx * 0.35, 0.25, 0.4))).normalized()
        # local Z = forward (-Y), so the cup's inside (local +Z side) faces the front and is pink
        m = frame(loc + out * 0.05, Vector((sx, 0, 0.35)), Vector((0, -1, 0.1)))
        blob(bm, L, m @ Matrix.Translation((0, 0.07, 0)),
             lambda u: Vector((u.x * 0.15, u.y * 0.17 + 0.02, u.z * 0.07 - (u.x * u.x) * 0.035)),
             lambda u, lc: EAR_IN if (u.z > 0.25 and abs(u.x) < 0.7 and u.y > -0.55) else FUR_TOP, 12, 8)
    return new_obj(coll, "Ears", bm, mat)


# ------------------------------------------------------------------ wings
def feather(bm, L, m, length, width, thick, curl=0.12, root=FEATHER_ROOT, tip=GOLD, tip_from=0.62):
    def deform(u):
        t = (u.x + 1) * 0.5
        prof = math.sin(math.pi * min(t, 0.999) ** 0.8) ** 0.75
        z = u.z * thick * prof - curl * length * t * t
        return Vector((t * length, u.y * width * prof, z))

    def color(u, lc):
        t = (u.x + 1) * 0.5
        c = mix(root, FEATHER, smooth(0.0, 0.35, t))
        return mix(c, tip, smooth(tip_from, 0.98, t))
    blob(bm, L, m, deform, color, 10, 6)


def build_wings(coll, body, mat, mat_glow):
    wings, trims = [], []
    for side, sx in (("L", 1), ("R", -1)):
        bm = bmesh.new()
        L = color_layer(bm)
        tb = bmesh.new()
        TL = color_layer(tb)
        root, _ = surface(body, (sx * 0.9, 0.15, 1.85), (0, 0.15, 0.9))
        root = root + Vector((0, 0, -0.02))
        arm = Vector((sx * 1.0, 0.45, 0.80)).normalized()
        span = 1.2
        back_down = Vector((0, 0.55, -0.85))
        e2 = (back_down - arm * back_down.dot(arm)).normalized()
        nrm = arm.cross(e2) * sx   # wing plane normal (points up/out)

        def arm_point(u):
            return root + arm * span * u + Vector((0, 0, 0.16)) * math.sin(math.pi * u)

        def fdir(theta):
            th = math.radians(theta)
            return e2 * math.cos(th) + arm * math.sin(th)
        # primaries (long, fanning out at the tip)
        for k in range(5):
            u = 0.50 + 0.50 * k / 4
            th = 28 + 56 * k / 4
            feather(bm, L, frame(arm_point(u) - nrm * 0.03, fdir(th), nrm), 0.82 + 0.20 * k / 4, 0.15, 0.05, 0.10)
        # secondaries
        for k in range(6):
            u = 0.05 + 0.52 * k / 5
            th = 6 + 24 * k / 5
            feather(bm, L, frame(arm_point(u) - nrm * 0.01, fdir(th), nrm), 0.64, 0.15, 0.05, 0.10, tip_from=0.7)
        # coverts (short, rounded, on top)
        for k in range(7):
            u = 0.03 + 0.92 * k / 6
            th = 12 + 42 * k / 6
            feather(bm, L, frame(arm_point(u) + nrm * 0.03, fdir(th), nrm), 0.34, 0.14, 0.05, 0.05,
                    root=FEATHER_ROOT, tip=FEATHER, tip_from=0.99)
        # golden trim along the wing's leading edge (glows in game): one smooth tapered tube + a round tip
        tube(tb, TL, [arm_point(k / 16) for k in range(17)], 0.06, 0.035, GOLD)
        blob(tb, TL, Matrix.Translation(arm_point(1.0) + arm * 0.03), lambda c: c * 0.065, lambda c, lc: GOLD, 10, 6)
        wings.append(new_obj(coll, "Wing_" + side, bm, mat))
        trims.append(new_obj(coll, "Glow_WingTrim_" + side, tb, mat_glow))
    return wings, trims


# ------------------------------------------------------------------ celestial extras
def build_halo(coll, mat_glow, center, radius=0.30, tube=0.04, tilt=12):
    bm = bmesh.new()
    L = color_layer(bm)
    N, M = 40, 8
    rows = []
    for i in range(N):
        a = 2 * math.pi * i / N
        ring = []
        for j in range(M):
            b = 2 * math.pi * j / M
            r = radius + tube * math.cos(b)
            co = Vector((r * math.cos(a), r * math.sin(a), tube * math.sin(b)))
            v = bm.verts.new(co)
            v[L] = mix(GOLD, GOLD_DEEP, 0.5 - 0.5 * math.sin(b))
            ring.append(v)
        rows.append(ring)
    for i in range(N):
        for j in range(M):
            a, b = rows[i][j], rows[(i + 1) % N][j]
            c, d = rows[(i + 1) % N][(j + 1) % M], rows[i][(j + 1) % M]
            bm.faces.new((a, b, c, d))
    rot = Matrix.Rotation(math.radians(-tilt), 4, "X")
    bmesh.ops.transform(bm, matrix=Matrix.Translation(center) @ rot, verts=bm.verts)
    return new_obj(coll, "Glow_Halo", bm, mat_glow)


def star_points(r_out, r_in, n=5):
    pts = []
    for i in range(n * 2):
        a = math.pi / 2 + math.pi * i / n
        r = r_out if i % 2 == 0 else r_in
        pts.append(Vector((r * math.cos(a), r * math.sin(a), 0)))
    return pts


def add_star(bm, L, m, size, color):
    """A puffy 5-point star (front + back fans) - reads well small."""
    pts = star_points(size, size * 0.48)
    top = bm.verts.new(m @ Vector((0, 0, size * 0.28)))
    bot = bm.verts.new(m @ Vector((0, 0, -size * 0.10)))
    ring = [bm.verts.new(m @ p) for p in pts]
    for v in ring + [top, bot]:
        v[L] = color
    for i in range(len(ring)):
        a, b = ring[i], ring[(i + 1) % len(ring)]
        bm.faces.new((top, a, b))
        bm.faces.new((bot, b, a))


def build_constellation(coll, body, mat_glow):
    bm = bmesh.new()
    L = color_layer(bm)
    spots = [(0.14, 0.30, 0.12), (-0.22, 0.62, 0.10), (0.20, 0.94, 0.11), (-0.04, 1.22, 0.085)]
    for x, y, s in spots:
        loc, n = surface(body, (x, y, 3.0), (x, y, 0.0))
        m = frame(loc + n * 0.005, Vector((0, 1, 0)), n)
        add_star(bm, L, m, s, GOLD)
    return new_obj(coll, "Glow_Stars", bm, mat_glow, smooth_shade=False)


def build_flower(coll, body, mat, mat_glow):
    """Cveti's flower (tsvete = flower): a glowing star-lotus on the head, by the left ear."""
    loc, n = surface(body, (0.50, -0.95, 2.8), (0.18, -0.80, 1.6))
    up = (n + Vector((0.15, -0.1, 0.4))).normalized()
    base = frame(loc - up * 0.05, Vector((0, -1, 0)), up)
    bm = bmesh.new()
    L = color_layer(bm)
    for k in range(5):
        a = 2 * math.pi * k / 5
        d = Vector((math.cos(a), math.sin(a), 0.55)).normalized()
        m = base @ frame(Vector((0, 0, 0.02)), d, Vector((0, 0, 1)))

        def deform(u):
            t = (u.x + 1) * 0.5
            prof = math.sin(math.pi * min(t, 0.999) ** 0.7) ** 0.7
            return Vector((t * 0.36, u.y * 0.16 * prof, u.z * 0.04 * prof + 0.07 * t * t))
        blob(bm, L, m, deform, lambda u, lc: mix(PETAL_IN, PETAL_OUT, smooth(0.0, 1.0, (u.x + 1) * 0.5)), 12, 6)
    petals = new_obj(coll, "Flower", bm, mat)
    cb = bmesh.new()
    CL = color_layer(cb)
    blob(cb, CL, base @ Matrix.Translation((0, 0, 0.05)), lambda u: Vector((u.x * 0.085, u.y * 0.085, u.z * 0.06)),
         lambda u, lc: GOLD, 10, 6)
    centre = new_obj(coll, "Glow_FlowerCore", cb, mat_glow)
    return petals, centre


# ------------------------------------------------------------------ preview stage
def stage():
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x = sc.render.resolution_y = 900
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    w = sc.world or bpy.data.worlds.new("World")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.62, 0.74, 0.92, 1)
    bg.inputs["Strength"].default_value = 0.9
    st = bpy.data.collections.new("Stage")
    sc.collection.children.link(st)
    ground = bpy.data.meshes.new("Ground")
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, radius=6, segments=48)
    bm.to_mesh(ground)
    bm.free()
    gm = bpy.data.materials.new("GroundMat")
    gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.55, 0.78, 0.45, 1)
    ground.materials.append(gm)
    go = bpy.data.objects.new("Ground", ground)
    st.objects.link(go)

    def light(name, kind, loc, energy, rot=None, size=1.0, color=(1, 1, 1)):
        ld = bpy.data.lights.new(name, kind)
        ld.energy = energy
        ld.color = color
        if kind == "AREA":
            ld.size = size
        if kind == "SUN":
            ld.angle = math.radians(8)
        lo = bpy.data.objects.new(name, ld)
        lo.location = loc
        if rot:
            lo.rotation_euler = rot
        st.objects.link(lo)
        return lo
    light("Key", "SUN", (3, -4, 6), 3.2, (math.radians(50), 0, math.radians(35)), color=(1, 0.97, 0.92))
    light("Fill", "AREA", (-4, -3, 2.5), 350, (math.radians(70), 0, math.radians(-55)), 4, (0.85, 0.9, 1))
    light("Rim", "AREA", (0, 4.5, 3.5), 400, (math.radians(-55), 0, math.radians(180)), 3, (1, 0.95, 0.85))
    cam_d = bpy.data.cameras.new("Cam")
    cam_d.lens = 70
    cam = bpy.data.objects.new("Cam", cam_d)
    st.objects.link(cam)
    sc.camera = cam
    return cam


def aim(cam, loc, target=(0, -0.2, 1.25)):
    cam.location = loc
    d = Vector(target) - Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def build():
    coll = reset()
    mat, glow = materials()
    body = build_body(coll, mat)
    cheeks = []
    for sx in (1, -1):
        loc, _ = surface(body, (sx * 0.95, -1.45, 1.40), (sx * 0.1, -0.95, 1.42))
        cheeks.append(loc)
    color_body(body, cheeks)
    face, eyes = build_face(coll, body, mat, glow)
    ears = build_ears(coll, body, mat)
    wings, trims = build_wings(coll, body, mat, glow)
    halo = build_halo(coll, glow, Vector((0, -0.70, 2.40)))
    stars = build_constellation(coll, body, glow)
    flower, core = build_flower(coll, body, mat, glow)
    cam = stage()
    tris = 0
    for o in coll.objects:
        if o.type == "MESH":
            tris += sum(len(p.vertices) - 2 for p in o.data.polygons)
    return {"objects": [o.name for o in coll.objects], "tris": tris}


def shots(prefix, views=("threequarter", "side", "front", "back"), res=640):
    """Preview renders into renders/<prefix>_<view>.png"""
    sc = bpy.context.scene
    cam = sc.camera
    sc.render.resolution_x = sc.render.resolution_y = res
    spots = {"threequarter": (5.6, -7.6, 3.4), "side": (9.5, 0.2, 1.7), "front": (0, -9.8, 2.0),
             "back": (-5.0, 8.0, 4.2), "top": (0.01, 0.0, 11.0)}
    files = []
    for v in views:
        aim(cam, spots[v], (0, 0.05, 1.1))
        sc.render.filepath = os.path.join(OUT, "renders", prefix + "_" + v + ".png")
        bpy.ops.render.render(write_still=True)
        files.append(sc.render.filepath)
    return files


if __name__ == "__main__":
    print(build())
