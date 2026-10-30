# SLINGSHOT Halloween hub - the flying BAT (flock of ~10-14 circling the giant jack-o'-lantern). 2026-10-12.
# Headless:  blender.exe -b --factory-startup --python bat.py -- preview | build | render | export
#   preview = sculpt only + quick EEVEE looks;  build = sculpt + game mesh + bakes + rig + clips (+ bat.blend);
#   render = review renders + flap strip from bat.blend;  export = C:\cdimp\Halloween_Bat.fbx from bat.blend.
#
# Fierce semi-realistic vampire / fruit-bat mix: dark brown-black fur with a rusty mantle, big pointed ears with inner
# ridges, a snarling open mouth with fangs, glossy dark eyes under a heavy brow, leathery plum-brown membrane wings
# (thin panels lighter, veins + elastin striations) on visible arm / forearm / finger bones, hooked thumb claws, hind
# legs trailing with claws, a narrow tail membrane.
# Pipeline (Halloween kit, hkit.py read-only): dense procedural sculpt (per-vertex Col + Rough, fur strands as a
# shader bump) -> game mesh = its own coarse version of the same shapes -> bakes (normal, colour x AO, roughness)
# -> ONE skinned MeshPart. Rig + clips reuse the PetsV2 creature pipeline (petkit.py read-only): Pet.key / sample /
# write_clips -> CreatureClips module "Bat".
# Axes: 1 Blender metre = 1 stud. The bat FLIES ALONG BLENDER +Y (nose = +Y) with +Z up, so the bat's
# anatomical LEFT is Blender -X (bones *_L) and its RIGHT is +X (*_R). Anatomy constants below are written for the +X
# side and mirrored. Studio's importer turns the model 180 deg (Blender +Y -> Roblox +Z, +X -> -X).
import sys, os, math, json, time

sys.dont_write_bytecode = True       # import the shared kits read-only (no __pycache__ writes in their folders)
HAL = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween"
PV2 = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV2"
for _p in (HAL, PV2):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import bpy
from mathutils import Vector, Matrix, Quaternion, noise
import numpy as np
import hkit as H
import petkit as pk

OUT = os.path.join(HAL, "Bats")
MAPS = os.path.join(OUT, "maps")
REN = os.path.join(OUT, "renders")
BLEND = os.path.join(OUT, "bat.blend")
FBX_PATH = r"C:\cdimp\Halloween_Bat.fbx"
for _d in (MAPS, REN):
    os.makedirs(_d, exist_ok=True)

lin = H.lin
smooth = H.smoothstep


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def shade(c, k):
    return tuple(x * k for x in c)


# ------------------------------------------------------------------ palette (linear) + roughness
FUR_D = lin((24, 17, 16))        # near-black brown (fur grooves)
FUR_M = lin((46, 32, 27))        # dark brown body fur
FUR_TIP = lin((78, 55, 42))      # lighter tips on the clump crests
MANTLE = lin((68, 40, 26))       # rusty mantle (neck / shoulders)
MANTLE_TIP = lin((124, 74, 42))
BELLY = lin((58, 42, 36))
SKIN = lin((50, 33, 36))         # bare muzzle / ear skin (dark plum-grey)
SKIN_IN = lin((96, 56, 60))      # inner ear
NOSE = lin((30, 20, 23))
LIP = lin((54, 22, 28))
GUM = lin((128, 36, 46))
MOUTH = lin((34, 7, 10))
TONGUE = lin((122, 46, 56))
FANG = lin((236, 228, 206))
FANG_ROOT = lin((190, 160, 128))
EYE = lin((10, 6, 6))
EYE_RIM = lin((46, 14, 10))
MEM = lin((44, 27, 29))          # membrane: dark plum-brown
MEM_THIN = lin((76, 44, 45))     # thin panels: a touch lighter
VEIN = lin((56, 20, 24))
BONE_C = lin((36, 26, 27))
KNUCKLE = lin((70, 54, 50))
CLAW = lin((20, 16, 15))
CLAW_TIP = lin((150, 138, 118))

R_FUR, R_SKIN, R_MEM, R_NOSE, R_WET, R_EYE, R_TOOTH, R_CLAW = 0.86, 0.60, 0.62, 0.36, 0.30, 0.05, 0.32, 0.36


# ------------------------------------------------------------------ anatomy (+X side = the bat's RIGHT; mirrored for the left)
BS = 1.2                              # body / head / ears / legs scale (the wings keep their 5-stud span)


def bs(*c):
    return Vector(c) * BS


S = bs(0.13, 0.16, 0.05)             # shoulder (inside the pectoral)
E = Vector((0.48, 0.05, 0.095))      # elbow
W = Vector((1.20, 0.30, 0.14))       # wrist
THUMB = [W, W + Vector((0.025, 0.055, 0.012)), W + Vector((0.035, 0.10, 0.016))]
DIG = {  # W -> knuckle -> tip (2 = leading edge ... 5 = innermost)
    2: [W, Vector((1.52, 0.36, 0.152)), Vector((1.80, 0.385, 0.145))],
    3: [W, Vector((1.88, 0.30, 0.142)), Vector((2.50, 0.16, 0.10))],
    4: [W, Vector((1.70, -0.10, 0.122)), Vector((2.06, -0.50, 0.085))],
    5: [W, Vector((1.30, -0.28, 0.112)), Vector((1.30, -0.74, 0.07))],
}
HIP = bs(0.07, -0.27, -0.035)
KNEE = bs(0.13, -0.35, -0.05)
ANKLE = bs(0.16, -0.45, -0.045)
FOOT = ANKLE + bs(0.004, -0.045, 0.002)
BODYLINE = [S, bs(0.12, 0.05, 0.03), bs(0.11, -0.10, 0.012), bs(0.09, -0.22, -0.02), HIP]
LEG = [HIP, KNEE, ANKLE, FOOT]
ARM = [S, E, W]
HEAD_J = bs(0.0, 0.31, 0.05)         # neck joint (Head bone head)
EAR_BASE = bs(0.066, 0.385, 0.148)
EAR_UP = Vector((0.40, -0.16, 1.0)).normalized()
EAR_FWD = Vector((0.45, 1.0, 0.10)).normalized()
EAR_LEN, EAR_W = 0.30 * BS, 0.074 * BS
TAIL_TIP = bs(0.0, -0.47, -0.055)

# head landmarks
MOUTH_C = bs(0.0, 0.548, -0.016)
MOUTH_R = bs(0.040, 0.075, 0.013)
SNOUT_TIP = bs(0.0, 0.646, 0.044)
EYE_C = bs(0.054, 0.503, 0.088)
EYE_R = 0.0225 * BS
SOCKET_R = bs(0.031, 0.020, 0.021)
SNARL = [bs(sx * 0.024, 0.585, 0.004) for sx in (1, -1)]
SNARL_R = bs(0.014, 0.026, 0.010)


def mirror(v, sx):
    return Vector((v.x * sx, v.y, v.z))


# ------------------------------------------------------------------ geometry helpers
class Curve:
    """Catmull-Rom through control points, arc-length parameterised: at(t), t in [0, 1]."""

    def __init__(self, ctrl, sub=24):
        P = [Vector(c) for c in ctrl]
        if len(P) == 2:
            dense = [P[0].lerp(P[1], i / sub) for i in range(sub + 1)]
        else:
            ext = [P[0] + (P[0] - P[1])] + P + [P[-1] + (P[-1] - P[-2])]
            dense = []
            for i in range(1, len(ext) - 2):
                p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
                for j in range(sub):
                    t = j / sub
                    dense.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                                        + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t))
            dense.append(P[-1].copy())
        self.d = dense
        self.L = [0.0]
        for a, b in zip(dense, dense[1:]):
            self.L.append(self.L[-1] + (b - a).length)
        self.total = self.L[-1]

    def at(self, t):
        if t <= 0:
            return self.d[0].copy()
        if t >= 1:
            return self.d[-1].copy()
        s = self.total * t
        lo, hi = 0, len(self.L) - 1
        while hi - lo > 1:
            m = (lo + hi) // 2
            if self.L[m] <= s:
                lo = m
            else:
                hi = m
        u = (s - self.L[lo]) / max(self.L[hi] - self.L[lo], 1e-12)
        return self.d[lo].lerp(self.d[hi], u)


def seg_dist(p, a, b):
    ab = b - a
    t = max(0.0, min(1.0, (p - a).dot(ab) / max(ab.length_squared, 1e-12)))
    return (p - (a + ab * t)).length


def poly_dist(p, pts):
    return min(seg_dist(p, a, b) for a, b in zip(pts, pts[1:]))


class MB:
    """Tiny mesh builder: verts + faces + per-vertex colour / roughness."""

    def __init__(self):
        self.v, self.f, self.col, self.rough, self.mask = [], [], [], [], []

    def vert(self, p, c=(0.5, 0.5, 0.5), r=0.5, m=(0.0, 0.0, 0.0)):
        self.v.append(Vector(p))
        self.col.append(tuple(c[:3]))
        self.rough.append(r)
        self.mask.append(tuple(m))
        return len(self.v) - 1

    def face(self, idx):
        if len(set(idx)) >= 3:
            self.f.append(tuple(idx))

    def mirrored(self):
        o = MB()
        o.v = [Vector((-x.x, x.y, x.z)) for x in self.v]
        o.col, o.rough, o.mask = list(self.col), list(self.rough), list(self.mask)
        o.f = [tuple(reversed(f)) for f in self.f]
        return o

    def obj(self, name, smooth_shade=True, mat=None, recalc=False):
        me = bpy.data.meshes.new(name)
        me.from_pydata([tuple(x) for x in self.v], [], self.f)
        me.validate()
        if recalc:      # closed parts: make every shell's normals point outward
            import bmesh
            bm = bmesh.new()
            bm.from_mesh(me)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
            bm.to_mesh(me)
            bm.free()
        H.set_colors(me, "Col", self.col)
        H.set_colors(me, "Rough", [(r, r, r) for r in self.rough])
        H.set_colors(me, "Mask", self.mask)
        for p in me.polygons:
            p.use_smooth = smooth_shade
        if mat:
            me.materials.append(mat)
        return H.link(bpy.data.objects.new(name, me))


def grid_faces(mb, idx, flip=False):
    for j in range(len(idx) - 1):
        for i in range(len(idx[0]) - 1):
            q = (idx[j][i], idx[j][i + 1], idx[j + 1][i + 1], idx[j + 1][i])
            mb.face(tuple(reversed(q)) if flip else q)


def tube(mb, pts, radius, color, rough, sides=8, cap=True):
    """Tube through pts. radius(t) or number; color(t, ang) or rgb; rough(t) or number."""
    pts = [Vector(p) for p in pts]
    n = len(pts)
    rings, prev = [], None
    for i, p in enumerate(pts):
        t = i / (n - 1)
        d = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        a = d.orthogonal().normalized() if prev is None else (prev - d * prev.dot(d)).normalized()
        prev = a
        b = d.cross(a)
        r = radius(t) if callable(radius) else radius
        ring = []
        for j in range(sides):
            ang = 2 * math.pi * j / sides
            c = color(t, ang) if callable(color) else color
            rr = rough(t) if callable(rough) else rough
            ring.append(mb.vert(p + (a * math.cos(ang) + b * math.sin(ang)) * max(r, 1e-4), c, rr))
        rings.append(ring)
    for i in range(n - 1):
        for j in range(sides):
            mb.face((rings[i][j], rings[i][(j + 1) % sides], rings[i + 1][(j + 1) % sides], rings[i + 1][j]))
    if cap:
        for idx, ring in ((0, rings[0]), (n - 1, rings[-1])):
            c = mb.vert(pts[idx], mb.col[ring[0]], mb.rough[ring[0]])
            for j in range(sides):
                if idx == 0:
                    mb.face((c, ring[(j + 1) % sides], ring[j]))
                else:
                    mb.face((c, ring[j], ring[(j + 1) % sides]))
    return rings


def ellipsoid(mb, center, radii, color, rough, x_axis=(1, 0, 0), z_axis=(0, 0, 1), useg=16, vseg=10, deform=None):
    """UV ellipsoid in frame(center, x_axis, z_axis). color(u) / rough(u) get the unit-sphere point."""
    m = pk.frame(center, x_axis, z_axis)
    rows = []
    for j in range(vseg + 1):
        th = math.pi * j / vseg
        row = []
        for i in range(useg if 0 < j < vseg else 1):
            ph = 2 * math.pi * i / useg
            u = Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)))
            lc = Vector((u.x * radii[0], u.y * radii[1], u.z * radii[2]))
            if deform:
                lc = deform(u, lc)
            c = color(u) if callable(color) else color
            rr = rough(u) if callable(rough) else rough
            row.append(mb.vert(m @ lc, c, rr))
        rows.append(row)
    for j in range(vseg):
        a, b = rows[j], rows[j + 1]
        for i in range(useg):
            i2 = (i + 1) % useg
            if len(a) == 1:
                mb.face((a[0], b[i], b[i2]))
            elif len(b) == 1:
                mb.face((a[i], b[0], a[i2]))
            else:
                mb.face((a[i], b[i], b[i2], a[i2]))


def claw(mb, base, direction, bend_axis, length, r, sides=6, n=6, bend=60.0):
    pts = pk.arc_points(base, direction, length, bend_axis, bend, n)
    tube(mb, pts, lambda t: r * (1 - t) ** 0.9 + 0.0012,
         lambda t, a: mix(CLAW, CLAW_TIP, smooth(0.6, 1.0, t)), lambda t: R_CLAW - 0.12 * t, sides)


# ------------------------------------------------------------------ the body (metaball sculpt)
def body_elements():
    """(co, radii, rot quat or None, negative) - pre-scale coordinates (x BS)."""
    q_jaw = Quaternion((1, 0, 0), math.radians(-14))
    q_sock = lambda sx: Quaternion((0, 1, 0), math.radians(-22 * sx)) @ Quaternion((0, 0, 1), math.radians(-28 * sx))
    q_brow = lambda sx: (Quaternion((0, 1, 0), math.radians(-20 * sx)) @ Quaternion((0, 0, 1), math.radians(-12 * sx))
                         @ Quaternion((1, 0, 0), math.radians(18)))
    E_ = [
        ((0, 0.11, 0.005), (0.160, 0.170, 0.135), None, False),      # deep chest
        ((0, -0.10, -0.005), (0.110, 0.165, 0.098), None, False),    # abdomen (narrower)
        ((0, -0.27, -0.02), (0.062, 0.085, 0.056), None, False),     # rump
        ((0, 0.28, 0.05), (0.100, 0.080, 0.094), None, False),       # neck
        ((0, 0.255, 0.078), (0.132, 0.085, 0.104), None, False),     # mantle ruff
        ((0, 0.395, 0.085), (0.100, 0.108, 0.090), None, False),     # cranium
        ((0, 0.500, 0.045), (0.058, 0.070, 0.048), None, False),     # muzzle base
        ((0, 0.585, 0.038), (0.029, 0.066, 0.029), None, False),     # muzzle front (fox-like taper)
        ((0, 0.553, 0.062), (0.025, 0.062, 0.021), None, False),     # nose bridge
        ((0, 0.505, -0.040), (0.034, 0.085, 0.018), q_jaw, False),   # lower jaw (dropped)
        ((0, 0.548, -0.016), (0.040, 0.075, 0.013), Quaternion((1, 0, 0), math.radians(-10)), True),  # mouth
    ]
    for sx in (1, -1):
        E_ += [
            ((sx * 0.100, 0.15, 0.025), (0.098, 0.105, 0.090), None, False),  # pectorals / shoulders
            ((sx * 0.050, 0.465, 0.040), (0.050, 0.060, 0.046), None, False),  # cheeks / jowls
            ((sx * 0.045, 0.503, 0.114), (0.044, 0.024, 0.016), q_brow(sx), False),  # heavy brow, low over the eye
            ((sx * 0.054, 0.508, 0.088), (0.031, 0.020, 0.021), q_sock(sx), True),   # eye socket (carved)
            ((sx * 0.024, 0.585, 0.004), (0.014, 0.026, 0.010), None, True),  # snarl: lip pulled up at the fang
        ]
    return [(tuple(c * BS for c in co), tuple(r * BS for r in radii), rot, neg) for co, radii, rot, neg in E_]


def metaball_mesh(name, res, voxel, smooth_iter):
    mb = bpy.data.metaballs.new(name + "_MB")
    mb.resolution = mb.render_resolution = res
    mb.threshold = 0.6
    mbo = H.link(bpy.data.objects.new(name + "_MB", mb))
    for co, radii, rot, neg in body_elements():
        x = mb.elements.new(type="ELLIPSOID")
        x.co, x.radius, x.stiffness = co, 1.0, 2.0
        x.size_x, x.size_y, x.size_z = radii[0] / pk.K, radii[1] / pk.K, radii[2] / pk.K
        if rot is not None:
            x.rotation = rot
        x.use_negative = neg
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(mbo.evaluated_get(dg))
    bpy.data.objects.remove(mbo, do_unlink=True)
    bpy.data.metaballs.remove(mb)
    ob = H.link(bpy.data.objects.new(name, me))
    rm = ob.modifiers.new("Remesh", "REMESH")
    rm.mode, rm.voxel_size = "VOXEL", voxel
    sm = ob.modifiers.new("Smooth", "SMOOTH")
    sm.factor, sm.iterations = 0.6, smooth_iter
    H.apply_mods(ob)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def ell_q(p, c, r):
    return Vector(((p.x - c.x) / r.x, (p.y - c.y) / r.y, (p.z - c.z) / r.z)).length


def body_paint(p, n):
    """-> base colour, tip colour, roughness, fur amplitude, skin factor"""
    muzzle = 1.0 - smooth(0.82, 1.05, ell_q(p, bs(0, 0.605, 0.030), bs(0.042, 0.075, 0.058)))
    mq = ell_q(p, MOUTH_C, MOUTH_R)
    lip = 1.0 - smooth(1.25, 1.8, mq)
    gum = 1.0 - smooth(1.02, 1.25, mq)
    for c_ in SNARL:     # the snarl notches show gum too
        gum = max(gum, 1.0 - smooth(0.9, 1.25, ell_q(p, c_, SNARL_R)))
    mantle = smooth(0.12 * BS, 0.20 * BS, p.y) * (1 - smooth(0.32 * BS, 0.39 * BS, p.y)) * smooth(-0.45, 0.1, n.z)
    belly = smooth(-0.30, -0.70, n.z) * (1 - smooth(0.25 * BS, 0.35 * BS, p.y))
    head = smooth(0.33 * BS, 0.40 * BS, p.y)
    sock = 0.0
    for sx in (1, -1):
        sock = max(sock, 1.0 - smooth(1.0, 1.7, ell_q(p, mirror(EYE_C, sx), SOCKET_R)))
    furrow = smooth(0.012 * BS, 0.0, abs(p.x)) * smooth(0.48 * BS, 0.50 * BS, p.y) * (1 - smooth(0.53 * BS, 0.55 * BS, p.y)) \
        * smooth(0.085 * BS, 0.10 * BS, p.z)
    base = mix(FUR_M, BELLY, belly)
    base = mix(base, MANTLE, mantle * 0.85)
    tipc = mix(FUR_TIP, MANTLE_TIP, mantle)
    base = mix(base, FUR_D, max(sock * 0.8, furrow * 0.7))
    tipc = mix(tipc, FUR_M, sock)
    amp = (0.0075 * (1 - head) + 0.0040 * head) * (1 + 0.7 * mantle) * (1 - 0.45 * belly)
    skin = max(muzzle, lip)
    amp *= (1 - skin)
    col, rough = base, R_FUR
    if skin > 0:
        sk = mix(SKIN, NOSE, smooth(0.625 * BS, 0.648 * BS, p.y))
        sk = mix(sk, LIP, lip)
        sk = mix(sk, GUM, gum)
        col = mix(col, sk, skin)
        rough = R_FUR + (R_WET - R_FUR) * gum + (R_SKIN - R_FUR) * max(0.0, skin - gum)
    return col, tipc, rough, amp, skin


def fur_displace(ob, hi=True, seed=3.1):
    """Combed fur clumps on the hi sculpt: smooth anisotropic noise stretched along the flow (-Y), 2 layers (no
    sub-vertex frequencies = no aliasing). Fine strands live in the shader bump. Colour + roughness per vertex."""
    me = ob.data
    off = Vector((seed * 13.1, seed * 7.7, seed * 3.3))
    co = [v.co.copy() for v in me.vertices]
    nr = [v.normal.copy() for v in me.vertices]
    cols, roughs, new = [], [], []
    for p, n in zip(co, nr):
        col, tipc, rough, amp, skin = body_paint(p, n)
        h1 = noise.noise(Vector((p.x * 20.0, p.y * 5.0, p.z * 20.0)) + off)
        h2 = noise.noise(Vector((p.x * 44.0, p.y * 10.0, p.z * 44.0)) + off * 1.7)
        hn = max(-1.0, min(1.0, (0.72 * h1 + 0.28 * h2) / 0.55))
        d = amp * hn
        if skin > 0.05 and p.z > 0.035 * BS and p.y > 0.52 * BS:   # snarl wrinkles across the top of the muzzle
            w = math.sin((p.y - 0.52 * BS) * 2 * math.pi / (0.022 * BS)) * smooth(0.5, 0.9, skin) \
                * smooth(0.035 * BS, 0.06 * BS, p.z)
            d += 0.0024 * w
            col = mix(col, shade(col, 0.55), max(0.0, -w) * 0.6)
        if amp > 0:
            col = mix(mix(col, FUR_D, 0.45 * smooth(-0.05, -0.85, hn)), tipc, 0.35 * smooth(0.3, 0.95, hn))
        new.append(p + n * d if hi else p)
        cols.append(col)
        roughs.append((rough, rough, rough))
    if hi:
        me.vertices.foreach_set("co", [c for v in new for c in v])
        me.update()
    for a in list(me.color_attributes):
        me.color_attributes.remove(a)
    H.set_colors(me, "Col", cols)
    H.set_colors(me, "Rough", roughs)
    return ob


# ------------------------------------------------------------------ face parts
def eye_parts(hi):
    mb = MB()
    seg = (20, 12) if hi else (14, 7)
    for sx in (1, -1):
        out = (mirror(EYE_C, sx) - bs(0, 0.43, 0.06)).normalized()
        out = (out + Vector((0, 0.35, 0))).normalized()
        c = mirror(EYE_C, sx) - out * EYE_R * 0.42
        side = Vector((0, 0, 1)).cross(out).normalized()
        # almond-shaped, deep-set; slanted (outer corner higher) for an angry look
        tilt = Quaternion(out, math.radians(-22 * sx))
        ellipsoid(mb, c, (EYE_R * 1.3, EYE_R * 0.72, EYE_R * 0.8),
                  lambda u: mix(EYE, EYE_RIM, smooth(0.35, 0.8, math.hypot(u.x, u.y)) * 0.85),
                  lambda u: R_EYE + 0.45 * smooth(0.45, 0.85, math.hypot(u.x, u.y)),     # wet centre, matte rim
                  x_axis=tilt @ side, z_axis=out, useg=seg[0], vseg=seg[1])
    return mb


def nose_parts(hi):
    """Small moist nose tip at the end of the fox-like muzzle; comma nostrils that open to the sides."""
    mb = MB()
    seg = (20, 10) if hi else (8, 4)
    fwd = Vector((0, 1, 0.25)).normalized()
    c = SNOUT_TIP - fwd * 0.004

    def col(u):
        k = 1.0 - 0.5 * smooth(0.25, 0.0, abs(u.x)) * smooth(0.1, -0.6, u.y) * smooth(0.0, 0.5, u.z)   # philtrum
        return shade(NOSE, k)
    ellipsoid(mb, c, (0.017 * BS, 0.0115 * BS, 0.010 * BS), col, R_NOSE, x_axis=(1, 0, 0), z_axis=fwd,
              useg=seg[0], vseg=seg[1],
              deform=lambda u, lc: Vector((lc.x * (1.0 + 0.25 * u.y), lc.y, lc.z * (1.0 - 0.25 * max(0.0, -u.y)))))
    for sx in (1, -1):
        b = c + Vector((sx * 0.011 * BS, 0.003 * BS, 0.002 * BS))
        d = Vector((sx * 0.9, 0.45, 0.15)).normalized()
        tube(mb, [b, b + d * 0.004 * BS, b + d * 0.0065 * BS], lambda t: 0.0058 * BS * (1 - 0.3 * t),
             lambda t, a: shade(NOSE, 1.0 - 0.85 * smooth(0.55, 1.0, t)), R_NOSE, 10 if hi else 5)
    return mb


def mouth_parts(hi):
    mb = MB()
    seg = (16, 10) if hi else (8, 4)
    ellipsoid(mb, MOUTH_C + bs(0, -0.026, -0.003), bs(0.030, 0.048, 0.012), MOUTH, 0.55, useg=seg[0], vseg=seg[1])
    ellipsoid(mb, MOUTH_C + bs(0, -0.014, -0.010), bs(0.021, 0.044, 0.0065), TONGUE, 0.42, useg=seg[0], vseg=seg[1])
    return mb


def teeth_parts(hi):
    mb = MB()
    sides = 8 if hi else 5
    n = 8 if hi else 3
    col = lambda t, a: mix(FANG_ROOT, FANG, smooth(0.0, 0.35, t))
    for sx in (1, -1):
        b = bs(sx * 0.023, 0.588, 0.006)      # upper canines: long, curving back
        pts = pk.arc_points(b, (sx * -0.06, 0.20, -1), 0.046 * BS, (1, 0, 0), -16, n)
        tube(mb, pts, lambda t: 0.0082 * BS * (1 - t) ** 0.9 + 0.0006, col, R_TOOTH, sides)
        b = bs(sx * 0.017, 0.572, -0.032)     # lower canines, inside the uppers
        pts = pk.arc_points(b, (sx * 0.04, 0.22, 1), 0.026 * BS, (1, 0, 0), 14, n)
        tube(mb, pts, lambda t: 0.0060 * BS * (1 - t) ** 0.9 + 0.0006, col, R_TOOTH, sides)
        if not hi:
            continue
        b = bs(sx * 0.008, 0.606, 0.004)      # small upper incisors
        pts = pk.arc_points(b, (0, 0.15, -1), 0.012 * BS, None, 0, max(3, n // 2))
        tube(mb, pts, lambda t: 0.0038 * BS * (1 - t) ** 0.6 + 0.0008, col, R_TOOTH, max(4, sides - 2))
    return mb


def ear_part(hi, sx):
    """Tall pointed bat ear: cupped thin shell, rolled outer rim, transverse ridges inside, furred back at the
    base, a small pointed tragus at the opening."""
    mb = MB()
    up = mirror(EAR_UP, sx)
    fw = mirror(EAR_FWD, sx)
    fw = (fw - up * fw.dot(up)).normalized()
    side = up.cross(fw).normalized()
    base = mirror(EAR_BASE, sx)
    NA, NH = (24, 44) if hi else (7, 10)

    def mid(a, h):
        w = EAR_W * ((1 - h) ** 0.72) * (1 + 0.28 * math.sin(math.pi * min(1.0, h * 1.5))) + 0.0015
        cup = 0.032 * BS * (1 - a * a) * (1 - h) ** 0.55
        roll = 0.010 * BS * smooth(0.72, 1.0, abs(a)) * (1 - h) ** 0.5     # rolled rim curls forward
        back = 0.055 * BS * h * h                                          # the tip leans back
        return base + side * (a * w) + up * (h * EAR_LEN) - fw * (cup + back) + fw * roll

    def thick(h):
        return 0.010 * BS * (1 - h) + 0.0035

    rows_f, rows_b = [], []
    for j in range(NH + 1):
        h = j / NH
        rf, rb = [], []
        for i in range(NA + 1):
            a = -1 + 2 * i / NA
            p = mid(a, h)
            ridge = 0.0
            if hi and abs(a) < 0.80 and 0.10 < h < 0.80:
                ridge = 0.0032 * BS * (0.5 + 0.5 * math.cos(h * 2 * math.pi * 7.5)) ** 4 * (1 - abs(a) / 0.80)
            pf = p + fw * (thick(h) * 0.5 + ridge)
            pb = p - fw * thick(h) * 0.5
            fur = smooth(0.30, 0.06, h)
            cin = mix(SKIN_IN, mix(SKIN_IN, SKIN, 0.6), smooth(0.45, 0.95, abs(a)) + 0.25 * h)
            if ridge > 0.0012:
                cin = mix(cin, shade(SKIN, 0.85), min(1.0, ridge / 0.003) * 0.6)
            cin = mix(cin, FUR_M, fur * 0.7)
            cb = mix(SKIN, FUR_M, fur)
            rf.append(mb.vert(pf, cin, R_SKIN))
            rb.append(mb.vert(pb, cb, R_SKIN + (R_FUR - R_SKIN) * fur))
        rows_f.append(rf)
        rows_b.append(rb)
    # winding: the front face looks along +fw
    def oriented(q, want):
        a, b, c = (mb.v[q[0]], mb.v[q[1]], mb.v[q[2]])
        return q if (b - a).cross(c - a).dot(want) >= 0 else tuple(reversed(q))
    for j in range(NH):
        for i in range(NA):
            mb.face(oriented((rows_f[j][i], rows_f[j][i + 1], rows_f[j + 1][i + 1], rows_f[j + 1][i]), fw))
            mb.face(oriented((rows_b[j][i], rows_b[j][i + 1], rows_b[j + 1][i + 1], rows_b[j + 1][i]), -fw))
    for j in range(NH):
        for i, sgn in ((0, -1), (NA, 1)):
            q = (rows_f[j][i], rows_f[j + 1][i], rows_b[j + 1][i], rows_b[j][i])
            mb.face(oriented(q, side * sgn))
    for i in range(NA):
        mb.face(oriented((rows_f[0][i], rows_f[0][i + 1], rows_b[0][i + 1], rows_b[0][i]), -up))
        mb.face(oriented((rows_f[NH][i], rows_f[NH][i + 1], rows_b[NH][i + 1], rows_b[NH][i]), up))
    return mb


# ------------------------------------------------------------------ wings
def edge_curve(a, b, pull_to, depth, n=40):
    """Scalloped membrane edge from a to b, pulled toward pull_to by depth * sin(pi t)."""
    a, b = Vector(a), Vector(b)
    pts = []
    for i in range(n + 1):
        t = i / n
        p = a.lerp(b, t)
        pts.append(p + (Vector(pull_to) - p).normalized() * depth * math.sin(math.pi * t))
    return Curve(pts, sub=2)


def wing_curves():
    C = {"arm": Curve(ARM),
         "le": Curve([S, Vector((0.42, 0.21, 0.105)), Vector((0.84, 0.28, 0.135)), W])}   # propatagium edge
    for k_, pts in DIG.items():
        C[k_] = Curve(pts)
    C["body"] = Curve(BODYLINE + [KNEE, ANKLE])
    C["e54"] = edge_curve(DIG[5][2], DIG[4][2], W, 0.20)
    C["e43"] = edge_curve(DIG[4][2], DIG[3][2], W, 0.17)
    C["e32"] = edge_curve(DIG[3][2], DIG[2][2], W, 0.025)
    C["e5a"] = edge_curve(ANKLE, DIG[5][2], E, 0.25)
    return C


def coons(top, bot, left, right, nu, nv, billow=0.0):
    P00, P10, P01, P11 = top(0), top(1), bot(0), bot(1)
    grid = []
    for j in range(nv + 1):
        v = j / nv
        row = []
        for i in range(nu + 1):
            u = i / nu
            p = ((1 - v) * top(u) + v * bot(u) + (1 - u) * left(v) + u * right(v)
                 - ((1 - u) * (1 - v) * P00 + u * (1 - v) * P10 + (1 - u) * v * P01 + u * v * P11))
            row.append(p + Vector((0, 0, billow * math.sin(math.pi * u) * math.sin(math.pi * v))))
        grid.append(row)
    return grid


def membrane_sheet(res):
    """Mid-surface of the left wing membrane: (points, faces). res = (radial, across hand, P2 span, P1 rows)."""
    C = wing_curves()
    R, A, U2, V1 = res
    Wf = lambda u: W.copy()
    Sf = lambda v: S.copy()
    patches = [
        coons(C["arm"].at, C["e5a"].at, C["body"].at, C[5].at, U2, R, billow=0.05),   # plagiopatagium
        coons(Wf, C["e54"].at, C[5].at, C[4].at, A, R, billow=0.035),                 # finger 5-4
        coons(Wf, C["e43"].at, C[4].at, C[3].at, A, R, billow=0.035),                 # finger 4-3
        coons(Wf, C["e32"].at, C[3].at, C[2].at, max(2, A // 2), R, billow=0.012),    # finger 3-2
        coons(C["le"].at, C["arm"].at, Sf, Wf, U2, V1, billow=0.0),                   # propatagium
    ]
    pts, quads = [], []
    for g in patches:
        idx = []
        for row in g:
            r_ = []
            for p in row:
                pts.append(p)
                r_.append(len(pts) - 1)
            idx.append(r_)
        for j in range(len(idx) - 1):
            for i in range(len(idx[0]) - 1):
                quads.append((idx[j][i], idx[j][i + 1], idx[j + 1][i + 1], idx[j + 1][i]))
    key, remap, upts = {}, [], []
    for p in pts:   # merge shared boundaries + degenerate corners
        k_ = (round(p.x, 5), round(p.y, 5), round(p.z, 5))
        if k_ not in key:
            key[k_] = len(upts)
            upts.append(p)
        remap.append(key[k_])
    out = []
    for q in quads:
        f = []
        for i in q:
            if remap[i] not in f:
                f.append(remap[i])
        if len(f) < 3:
            continue
        a, b, c = upts[f[0]], upts[f[1]], upts[f[2]]
        nrm = (b - a).cross(c - a)
        if len(f) == 4:
            nrm = nrm + (c - a).cross(upts[f[3]] - a)
        out.append(tuple(f) if nrm.z >= 0 else tuple(reversed(f)))
    return upts, out


def membrane_paint(p, hi):
    """Base colour + roughness + Mask(vein strength, thin factor) for a membrane point (mirrored to left-wing space).
    The veins and elastin striations themselves are drawn per pixel by mat_membrane (crisp lines in the bake)."""
    q = Vector((abs(p.x), p.y, p.z))
    d_arm, d_hand = poly_dist(q, ARM), min(poly_dist(q, DIG[k_]) for k_ in DIG)
    d_body, d_leg = poly_dist(q, BODYLINE), poly_dist(q, LEG)
    d_bone = min(d_arm, d_hand, d_leg)
    thin = smooth(0.03, 0.30, d_bone) * smooth(0.02, 0.22, d_body)
    col = mix(MEM, MEM_THIN, 0.62 * thin)
    fur = min(1.0, smooth(0.11, 0.03, d_body) + smooth(0.06, 0.025, d_arm) * smooth(0.45, 0.28, q.x) * 0.9)
    col = mix(col, FUR_M, fur * 0.85)
    rough = R_MEM + (R_FUR - R_MEM) * fur
    vein = smooth(0.015, 0.06, d_bone) * (0.55 + 0.45 * smooth(0.6, 1.3, q.x)) * (1 - fur)
    return col, rough, (vein, thin * (1 - fur), 0.0)


def membrane_part(hi, T=0.016):
    pts, faces = membrane_sheet((44, 22, 44, 8) if hi else (6, 6, 8, 2))
    vn = [Vector() for _ in pts]
    for f in faces:
        a, b, c = pts[f[0]], pts[f[1]], pts[f[2]]
        n = (b - a).cross(c - a)
        for i in f:
            vn[i] += n
    vn = [n.normalized() if n.length > 1e-12 else Vector((0, 0, 1)) for n in vn]
    mb = MB()
    top, bot = [], []
    for p, n in zip(pts, vn):
        col, rough, m = membrane_paint(p, hi)
        top.append(mb.vert(p + n * T * 0.5, col, rough, m))
        bot.append(mb.vert(p - n * T * 0.5, col, rough, m))
    for f in faces:
        mb.face(tuple(top[i] for i in f))
        mb.face(tuple(bot[i] for i in reversed(f)))
    cnt = {}
    for f in faces:
        for i in range(len(f)):
            e = tuple(sorted((f[i], f[(i + 1) % len(f)])))
            cnt[e] = cnt.get(e, 0) + 1
    for f in faces:      # rim along the open boundary
        for i in range(len(f)):
            a, b = f[i], f[(i + 1) % len(f)]
            if cnt[tuple(sorted((a, b)))] == 1:
                mb.face((top[b], top[a], bot[a], bot[b]))
    return mb


def wing_bones_part(hi):
    """Visible arm (furred humerus + thin forearm), elbow + wrist knobs, thumb + hooked claw, 4 finger bones."""
    mb = MB()
    sides = 12 if hi else 6
    arm = Curve(ARM)
    n = 28 if hi else 8
    te = (E - S).length / arm.total

    def arm_r(t):
        r = 0.040 * (1 - t / te) ** 0.9 + 0.021 if t < te else 0.019 - 0.006 * (t - te) / (1 - te)
        r += 0.006 * math.exp(-((t - te) / 0.05) ** 2)       # elbow
        r += 0.010 * math.exp(-((t - 1.0) / 0.045) ** 2)     # wrist knob
        return r

    def arm_c(t, a):
        fur = smooth(te + 0.05, te - 0.15, t)
        return mix(mix(BONE_C, KNUCKLE, 0.4 * math.exp(-((t - te) / 0.05) ** 2)), FUR_M, fur)
    tube(mb, [arm.at(i / (n - 1)) for i in range(n)], arm_r, arm_c,
         lambda t: R_SKIN + (R_FUR - R_SKIN) * smooth(te + 0.05, te - 0.15, t), sides)
    for k_, pts in DIG.items():
        c = Curve(pts)
        nn = 22 if hi else 5
        r0 = 0.016 if k_ in (3, 4) else 0.014
        tk = (pts[1] - pts[0]).length / c.total

        def fr(t, r0=r0, tk=tk):
            return r0 * (1 - t) ** 0.55 + 0.0035 + 0.005 * math.exp(-((t - tk) / 0.05) ** 2)

        def fc(t, a, tk=tk):
            return mix(BONE_C, KNUCKLE, 0.8 * math.exp(-((t - tk) / 0.06) ** 2) + 0.2 * smooth(0.85, 1.0, t))
        tube(mb, [c.at(i / (nn - 1)) for i in range(nn)], fr, fc, R_SKIN, 8 if hi else 4)
    tube(mb, THUMB, lambda t: 0.016 * (1 - t) + 0.010, BONE_C, R_SKIN, 8 if hi else 4)
    claw(mb, THUMB[-1], (0.25, 1.0, -0.15), (1, 0, 0), 0.058, 0.0105, sides=8 if hi else 4, n=7 if hi else 4, bend=-80)
    return mb


def leg_part(hi):
    mb = MB()
    sides = 10 if hi else 6
    c = Curve(LEG)
    n = 18 if hi else 5

    def lr(t):
        return 0.034 * BS * (1 - t) + 0.016 * BS * t + 0.004 * math.exp(-((t - 0.40) / 0.07) ** 2)

    tube(mb, [c.at(i / (n - 1)) for i in range(n)], lr, lambda t, a: mix(FUR_M, SKIN, smooth(0.30, 0.55, t)),
         lambda t: R_FUR + (R_SKIN - R_FUR) * smooth(0.30, 0.55, t), sides)
    ellipsoid(mb, FOOT + bs(0, -0.006, 0), bs(0.020, 0.028, 0.011), SKIN, R_SKIN, useg=12 if hi else 6,
              vseg=7 if hi else 3)
    for i in range(5):      # toes point back, claws hook DOWN (ventral)
        a = (i - 2) * 0.0085 * BS
        b = FOOT + bs(0, -0.026, 0.0) + Vector((a, 0, 0))
        claw(mb, b, (a * 2.5, -1.0, 0.15), (1, 0, 0), 0.036 * BS, 0.0055 * BS, sides=6 if hi else 3,
             n=6 if hi else 3, bend=95)
    return mb


def uro_part(hi):
    """Narrow tail membrane between the legs (left leg -> tail tip -> right leg)."""
    R_, U_ = (14, 20) if hi else (3, 6)
    legL = Curve([HIP, KNEE, ANKLE])
    legR = Curve([mirror(HIP, -1), mirror(KNEE, -1), mirror(ANKLE, -1)])
    top = Curve([HIP, bs(0, -0.33, -0.045), mirror(HIP, -1)])
    bot = Curve([ANKLE, bs(0.09, -0.475, -0.06), TAIL_TIP, bs(-0.09, -0.475, -0.06), mirror(ANKLE, -1)])
    g = coons(top.at, bot.at, legL.at, legR.at, U_, R_)
    mb = MB()
    T = 0.012
    it, ib = [], []
    for row in g:
        rt, rb = [], []
        for p in row:
            col, rough, m = membrane_paint(p, hi)
            rt.append(mb.vert(p + Vector((0, 0, T / 2)), col, rough, m))
            rb.append(mb.vert(p - Vector((0, 0, T / 2)), col, rough, m))
        it.append(rt)
        ib.append(rb)
    for j in range(len(g) - 1):
        for i in range(len(g[0]) - 1):
            q = [(j, i), (j, i + 1), (j + 1, i + 1), (j + 1, i)]
            ft = [it[a][b] for a, b in q]
            a_, b_, c_ = (mb.v[ft[0]], mb.v[ft[1]], mb.v[ft[2]])
            up_ok = (b_ - a_).cross(c_ - a_).z >= 0
            mb.face(tuple(ft) if up_ok else tuple(reversed(ft)))
            fb = [ib[a][b] for a, b in q]
            mb.face(tuple(reversed(fb)) if up_ok else tuple(fb))
    J = len(g) - 1
    for i in range(len(g[0]) - 1):     # trailing rim
        mb.face((it[J][i], it[J][i + 1], ib[J][i + 1], ib[J][i]))
    return mb


# ------------------------------------------------------------------ materials (sculpt)
def sk(coll, name, typ="RGBA"):
    for s in coll:
        if s.name == name and s.type == typ:
            return s
    return coll[name]



def mat_sculpt(name, fur_bump=0.0, strand_scale=(110.0, 22.0, 110.0)):
    m = H.mat_vc(name)
    if fur_bump <= 0:
        return m
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = strand_scale
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.0
    nz.inputs["Detail"].default_value = 3.0
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = fur_bump
    bp.inputs["Distance"].default_value = 0.002
    nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], bsdf.inputs["Normal"])
    vc = [n for n in nt.nodes if n.type == "VERTEX_COLOR" and n.layer_name == "Col"][0]
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    rng = nt.nodes.new("ShaderNodeMapRange")
    rng.inputs["From Min"].default_value = 0.3
    rng.inputs["From Max"].default_value = 0.7
    rng.inputs["To Min"].default_value = 0.80
    rng.inputs["To Max"].default_value = 1.16
    nt.links.new(nz.outputs["Fac"], rng.inputs["Value"])
    nt.links.new(vc.outputs["Color"], sk(mul.inputs, "A"))
    nt.links.new(rng.outputs["Result"], sk(mul.inputs, "B"))
    nt.links.new(sk(mul.outputs, "Result"), bsdf.inputs["Base Color"])
    return m


def mat_membrane(name):
    m = H.mat_vc(name)
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    N, L = nt.nodes.new, nt.links.new

    def math(op, a, b=None, c=None):
        n = N("ShaderNodeMath")
        n.operation = op
        for i, x in enumerate((a, b, c)):
            if x is None:
                continue
            if isinstance(x, (int, float)):
                n.inputs[i].default_value = x
            else:
                L(x, n.inputs[i])
        return n.outputs[0]

    def vmath(op, a, b=None, scale=None):
        n = N("ShaderNodeVectorMath")
        n.operation = op
        L(a, n.inputs[0])
        if b is not None:
            if isinstance(b, (tuple, list)):
                n.inputs[1].default_value = b
            else:
                L(b, n.inputs[1])
        if scale is not None:
            n.inputs["Scale"].default_value = scale
        return n.outputs["Value"] if op in ("DISTANCE", "LENGTH", "DOT_PRODUCT") else n.outputs["Vector"]

    def noise(vec, scale, detail):
        n = N("ShaderNodeTexNoise")
        n.inputs["Scale"].default_value = scale
        n.inputs["Detail"].default_value = detail
        L(vec, n.inputs["Vector"])
        return n

    def ramp(x, a, b, c, d):
        n = N("ShaderNodeMapRange")
        n.clamp = True
        L(x, n.inputs["Value"])
        n.inputs["From Min"].default_value, n.inputs["From Max"].default_value = a, b
        n.inputs["To Min"].default_value, n.inputs["To Max"].default_value = c, d
        return n.outputs["Result"]

    tc = N("ShaderNodeTexCoord")
    sep = N("ShaderNodeSeparateXYZ")
    L(tc.outputs["Object"], sep.inputs[0])
    ax = math("ABSOLUTE", sep.outputs["X"])
    q2 = N("ShaderNodeCombineXYZ")
    L(ax, q2.inputs["X"])
    L(sep.outputs["Y"], q2.inputs["Y"])
    q2.inputs["Z"].default_value = 0.4
    q3 = N("ShaderNodeCombineXYZ")
    L(ax, q3.inputs["X"])
    L(sep.outputs["Y"], q3.inputs["Y"])
    L(sep.outputs["Z"], q3.inputs["Z"])
    # veins = iso-lines of ANISOTROPIC noise: radial around the wrist on the hand panels (angle stretched),
    # body -> trailing edge on the inner arm panel (x stretched) -> long branching lines, not closed cells
    sel = ramp(ax, W.x - 0.10, W.x - 0.02, 0.0, 1.0)
    dx = math("SUBTRACT", ax, W.x)
    dy = math("SUBTRACT", sep.outputs["Y"], W.y)
    ang = math("ARCTAN2", dy, dx)
    dv = N("ShaderNodeCombineXYZ")
    L(dx, dv.inputs["X"])
    L(dy, dv.inputs["Y"])
    rad = vmath("LENGTH", dv.outputs[0])
    hv = N("ShaderNodeCombineXYZ")
    L(math("MULTIPLY", ang, 3.4), hv.inputs["X"])
    L(math("MULTIPLY", rad, 1.3), hv.inputs["Y"])
    hv.inputs["Z"].default_value = 0.7
    av = N("ShaderNodeCombineXYZ")
    L(math("MULTIPLY", ax, 8.5), av.inputs["X"])
    L(math("MULTIPLY", sep.outputs["Y"], 1.8), av.inputs["Y"])
    av.inputs["Z"].default_value = 1.9
    def vein_lines(vec):
        warp = vmath("SUBTRACT", noise(vmath("SCALE", vec, scale=0.8), 1.0, 1.0).outputs["Color"], (0.5, 0.5, 0.5))
        out = None
        for sc_, w_, wt, wk in ((1.0, 0.020, 1.0, 0.45), (2.4, 0.014, 0.5, 0.8)):
            v_in = vmath("ADD", vmath("SCALE", vec, scale=sc_), vmath("SCALE", warp, scale=wk))
            fac = noise(v_in, 1.0, 1.5).outputs["Fac"]
            line = math("MULTIPLY", ramp(math("ABSOLUTE", math("SUBTRACT", fac, 0.5)), 0.0, w_, 1.0, 0.0), wt)
            out = line if out is None else math("MAXIMUM", out, line)
        return out
    va, vh = vein_lines(av.outputs[0]), vein_lines(hv.outputs[0])
    veins = math("ADD", math("MULTIPLY", va, math("SUBTRACT", 1.0, sel)), math("MULTIPLY", vh, sel))
    mask = N("ShaderNodeVertexColor")
    mask.layer_name = "Mask"
    msep = N("ShaderNodeSeparateColor")
    L(mask.outputs["Color"], msep.inputs["Color"])
    veins = math("MULTIPLY", veins, msep.outputs["Red"])
    rings = math("COSINE", math("MULTIPLY", vmath("DISTANCE", q3.outputs[0], tuple(W)), 2 * 3.14159265 / 0.038))
    bands = math("COSINE", math("ADD", math("MULTIPLY", ax, 2 * 3.14159265 / 0.042),
                                  math("MULTIPLY", math("SINE", math("MULTIPLY", sep.outputs["Y"], 9.0)), 0.6)))
    st = math("ADD", math("MULTIPLY", rings, sel), math("MULTIPLY", bands, math("SUBTRACT", 1.0, sel)))
    st = math("POWER", math("MULTIPLY_ADD", st, 0.5, 0.5), 6.0)
    st = math("MULTIPLY", st, msep.outputs["Green"])
    vc = [n for n in nt.nodes if n.type == "VERTEX_COLOR" and n.layer_name == "Col"][0]
    mixv = N("ShaderNodeMix")
    mixv.data_type = "RGBA"
    L(math("MULTIPLY", veins, 0.72), mixv.inputs["Factor"])
    L(vc.outputs["Color"], sk(mixv.inputs, "A"))
    sk(mixv.inputs, "B").default_value = (*VEIN, 1.0)
    dark = N("ShaderNodeMix")
    dark.data_type = "RGBA"
    dark.blend_type = "MULTIPLY"
    L(math("MULTIPLY", st, 0.5), dark.inputs["Factor"])
    L(sk(mixv.outputs, "Result"), sk(dark.inputs, "A"))
    sk(dark.inputs, "B").default_value = (0.8, 0.8, 0.8, 1.0)
    L(sk(dark.outputs, "Result"), bsdf.inputs["Base Color"])
    bp = N("ShaderNodeBump")
    bp.inputs["Strength"].default_value = 0.55
    bp.inputs["Distance"].default_value = 0.0015
    L(math("ADD", math("MULTIPLY", veins, 0.7), math("MULTIPLY", st, 0.3)), bp.inputs["Height"])
    L(bp.outputs["Normal"], bsdf.inputs["Normal"])
    return m


# ------------------------------------------------------------------ the sculpt (hi)
def build_hi():
    fur = mat_sculpt("FurHi", fur_bump=0.30)
    plain = mat_sculpt("PlainHi")
    memm = mat_membrane("MembraneHi")
    body = metaball_mesh("Body_hi", 0.007 * BS, 0.0055 * BS, 4)
    fur_displace(body, hi=True)
    body.data.materials.append(fur)
    objs = [body]
    for nm, mb in (("Eyes_hi", eye_parts(True)), ("Nose_hi", nose_parts(True)), ("Mouth_hi", mouth_parts(True)),
                   ("Teeth_hi", teeth_parts(True))):
        objs.append(mb.obj(nm, mat=plain, recalc=True))
    for sx, sd in ((-1, "L"), (1, "R")):
        objs.append(ear_part(True, sx).obj("Ear%s_hi" % sd, mat=fur, recalc=True))
    mem, wb, leg = membrane_part(True), wing_bones_part(True), leg_part(True)
    objs += [mem.obj("WingR_hi", mat=memm), mem.mirrored().obj("WingL_hi", mat=memm),
             wb.obj("WingBonesR_hi", mat=fur, recalc=True), wb.mirrored().obj("WingBonesL_hi", mat=fur, recalc=True),
             leg.obj("LegR_hi", mat=fur, recalc=True), leg.mirrored().obj("LegL_hi", mat=fur, recalc=True),
             uro_part(True).obj("Uro_hi", mat=memm)]
    return objs


# ------------------------------------------------------------------ the game mesh (lo): pieces + weights + UVs
BONES_LR = ("Ear", "Wing", "WingTip", "Leg")


def norm_w(w, keep=4):
    items = sorted(((b, x) for b, x in w.items() if x > 0.004), key=lambda t: -t[1])[:keep]
    s = sum(x for _, x in items) or 1.0
    return {b: x / s for b, x in items}


def w_limb(p):
    """IDW over the wing / leg skeleton for membrane, arm, finger, leg and tail-membrane vertices."""
    sd = "L" if p.x < 0 else "R"     # the bat faces +Y: its anatomical LEFT is -X
    q = Vector((abs(p.x), p.y, p.z))
    d = {"Wing_" + sd: poly_dist(q, ARM),
         "WingTip_" + sd: min([poly_dist(q, DIG[k_]) for k_ in DIG] + [poly_dist(q, THUMB)]),
         "Body": poly_dist(q, BODYLINE),
         "Leg_" + sd: poly_dist(q, LEG)}
    return norm_w({b: 1.0 / (x + 0.03) ** 3 for b, x in d.items()})


def w_uro(p):
    d = {"Body": min(seg_dist(p, bs(0, -0.27, -0.03), TAIL_TIP), poly_dist(p, [HIP, bs(0, -0.33, -0.045), mirror(HIP, -1)])),
         "Leg_R": poly_dist(p, LEG), "Leg_L": poly_dist(p, [mirror(x, -1) for x in LEG])}
    return norm_w({b: 1.0 / (x + 0.03) ** 3 for b, x in d.items()})


def w_body(p):
    wh = smooth(0.26 * BS, 0.36 * BS, p.y)
    w = {"Head": wh}
    rest = 1.0 - wh
    for sx, sd in ((-1, "L"), (1, "R")):
        ws = 0.5 * smooth(0.14, 0.05, (p - mirror(S, sx)).length) * rest
        wl = 0.45 * smooth(0.09, 0.03, (p - mirror(HIP, sx)).length) * rest
        w["Wing_" + sd] = ws
        w["Leg_" + sd] = wl
    w["Body"] = max(0.0, 1.0 - sum(w.values()))
    return norm_w(w)


def w_ear(p):
    sd = "L" if p.x < 0 else "R"     # the bat faces +Y: its anatomical LEFT is -X
    sx = -1 if sd == "L" else 1
    h = (p - mirror(EAR_BASE, sx)).dot(mirror(EAR_UP, sx)) / EAR_LEN
    we = smooth(0.04, 0.30, h)
    return norm_w({"Ear_" + sd: we, "Head": 1 - we})


def set_weights(ob, fn):
    groups = {}
    for v in ob.data.vertices:
        for b, x in fn(v.co).items():
            if b not in groups:
                groups[b] = ob.vertex_groups.get(b) or ob.vertex_groups.new(name=b)
            groups[b].add([v.index], x, "REPLACE")


def triangulate(ob):
    ob.modifiers.new("Tri", "TRIANGULATE")
    H.apply_mods(ob)


def join(objs, name):
    objs = [o for o in objs if o is not None]
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    with bpy.context.temp_override(active_object=objs[0], selected_editable_objects=objs, selected_objects=objs):
        bpy.ops.object.join()
    objs[0].name = objs[0].data.name = name
    return objs[0]


def tag_part(ob, value):
    a = ob.data.attributes.get("part") or ob.data.attributes.new("part", "INT", "FACE")
    a.data.foreach_set("value", [value] * len(ob.data.polygons))


def coverage(ob, size):
    """UV coverage mask of ob (EMIT bake of white, with bake margin) -> bool array [size, size]."""
    img = bpy.data.images.new("cov_" + ob.name, size, size, alpha=False)
    img.colorspace_settings.name = "Non-Color"
    m = bpy.data.materials.new("cov_" + ob.name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1, 1, 1, 1)
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.nodes.active = tex
    ob.data.materials.clear()
    ob.data.materials.append(m)
    H.only(ob)
    bpy.ops.object.bake(type="EMIT", use_selected_to_active=False, margin=6)
    return np.array(img.pixels[:], dtype=np.float32).reshape(size, size, 4)[..., 0] > 0.5


def rebake_bones(lo, hi, imgs, size):
    """The thin finger / forearm tubes sit inside the membrane: some of their bake rays hit the membrane (jagged
    streaks). Re-bake just those faces against just the hi bones and paste them into the maps."""
    import bmesh
    bl = H.link(bpy.data.objects.new("BonesBake", lo.data.copy()))
    bm = bmesh.new()
    bm.from_mesh(bl.data)
    lay = bm.faces.layers.int.get("part")
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f[lay] != 1], context="FACES")
    bm.to_mesh(bl.data)
    bm.free()
    src_hi = [o for o in hi if o.name.startswith("WingBones")]
    tmp = os.path.join(MAPS, "_tmp")
    ib = H.bake_set(bl, src_hi, size, "BatBones", cage=0.022, maxray=0.05, ao_strength=0.55, ao_dist=0.15, outdir=tmp)
    mask = coverage(bl, size)
    for key in ("albedo", "normal", "rough", "ao"):
        a = np.array(imgs[key].pixels[:], dtype=np.float32).reshape(size, size, 4)
        b = np.array(ib[key].pixels[:], dtype=np.float32).reshape(size, size, 4)
        a[mask] = b[mask]
        imgs[key].pixels[:] = a.ravel()
    bpy.data.objects.remove(bl)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    return int(mask.sum())


SS, TEX = 2048, 1024      # bake supersampled, ship 1024


def downsample(imgs, n, m):
    """Box-filter the SS bakes down to the shipped size (anti-aliases thin ridges); normals renormalised."""
    k = n // m
    out = {}
    for key, cs in (("albedo", "sRGB"), ("normal", "Non-Color"), ("rough", "Non-Color"), ("ao", "Non-Color")):
        a = np.array(imgs[key].pixels[:], dtype=np.float32).reshape(m, k, m, k, 4).mean(axis=(1, 3))
        if key == "normal":
            v = a[..., :3] * 2 - 1
            v /= np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-6)
            a[..., :3] = v * 0.5 + 0.5
        a[..., 3] = 1.0
        img = bpy.data.images.new("Bat_" + key, m, m, alpha=False)
        img.colorspace_settings.name = cs
        img.pixels[:] = a.ravel()
        H.save_png(img, os.path.join(MAPS, "Bat_%s.png" % key))
        out[key] = img
    return out


def uv_place(ob, scale, offset):
    uv = ob.data.uv_layers.active.data
    for l in uv:
        l.uv = (l.uv[0] * scale + offset[0], l.uv[1] * scale + offset[1])


def build_lo():
    # body: its own coarse version of the same metaball shape (no fur), decimated
    body = metaball_mesh("BodyLo", 0.010 * BS, 0.0075 * BS, 3)
    dec = body.modifiers.new("Dec", "DECIMATE")
    dec.ratio = min(1.0, 2000 / max(1, len(body.data.polygons) * 2))
    H.apply_mods(body)
    triangulate(body)
    for a in list(body.data.color_attributes):
        body.data.color_attributes.remove(a)
    set_weights(body, w_body)
    pieces_b = []
    for nm, mb, fn in (("EyesLo", eye_parts(False), lambda p: {"Head": 1.0}),
                       ("NoseLo", nose_parts(False), lambda p: {"Head": 1.0}),
                       ("MouthLo", mouth_parts(False), lambda p: {"Head": 1.0}),
                       ("TeethLo", teeth_parts(False), lambda p: {"Head": 1.0}),
                       ("EarLLo", ear_part(False, 1), w_ear), ("EarRLo", ear_part(False, -1), w_ear),
                       ("WingBonesLLo", wing_bones_part(False), w_limb),
                       ("WingBonesRLo", wing_bones_part(False).mirrored(), w_limb),
                       ("LegLLo", leg_part(False), w_limb), ("LegRLo", leg_part(False).mirrored(), w_limb),
                       ("UroLo", uro_part(False), w_uro)):
        o = mb.obj(nm, recalc=nm not in ("UroLo",))
        triangulate(o)
        set_weights(o, fn)
        tag_part(o, 1 if nm.startswith("WingBones") else 0)
        pieces_b.append(o)
    memL = membrane_part(False).obj("MemLLo")
    memR = membrane_part(False).mirrored().obj("MemRLo")
    for o in (memL, memR):
        triangulate(o)
        set_weights(o, w_limb)
        tag_part(o, 0)
    tag_part(body, 0)
    # --- UV atlas: membrane (L/R + top/bottom share one planar island) in v 0..0.5; body square (0, .5)-(.5, 1);
    #     all the other pieces in the square (.5, .5)-(1, 1). Texel density ~380-430 px/stud at 1024.
    xs = [abs(v.co.x) for v in memL.data.vertices]
    ys = [v.co.y for v in memL.data.vertices]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    s = min(0.98 / (x1 - x0), 0.48 / (y1 - y0))
    for o in (memL, memR):
        uvl = o.data.uv_layers.new(name="UVMap")
        for poly in o.data.polygons:
            for li in poly.loop_indices:
                co = o.data.vertices[o.data.loops[li].vertex_index].co
                uvl.data[li].uv = (0.01 + (abs(co.x) - x0) * s, 0.01 + (co.y - y0) * s)
    H.smart_uv(body, angle=66, margin=0.012)
    uv_place(body, 0.5, (0.0, 0.5))
    misc = join(pieces_b, "MiscLo")
    H.smart_uv(misc, angle=66, margin=0.012)
    uv_place(misc, 0.5, (0.5, 0.5))
    for o in (body, misc, memL, memR):
        o.data.uv_layers.active.name = "UVMap"
        for a in list(o.data.color_attributes):
            o.data.color_attributes.remove(a)
    lo = join([body, misc, memL, memR], "Bat")
    for p in lo.data.polygons:
        p.use_smooth = True
    return lo


# ------------------------------------------------------------------ rig
BONES = None


def bone_specs():
    sp = [("Root", Vector((0, 0, 0)), Vector((0, 0, 0.2)), None),
          ("Body", bs(0, -0.02, 0.0), bs(0, 0.26, 0.04), "Root"),
          ("Head", HEAD_J, HEAD_J + bs(0, 0.22, 0.0), "Body")]
    for sx, sd in ((-1, "L"), (1, "R")):
        sp += [("Ear_" + sd, mirror(EAR_BASE, sx), mirror(EAR_BASE, sx) + mirror(EAR_UP, sx) * EAR_LEN * 0.8, "Head"),
               ("Wing_" + sd, mirror(S, sx), mirror(W, sx), "Body"),
               ("WingTip_" + sd, mirror(W, sx), mirror(W + (DIG[3][2] - W).normalized() * 0.45, sx), "Wing_" + sd),
               ("Leg_" + sd, mirror(HIP, sx), mirror(ANKLE, sx), "Body")]
    return sp


def build_rig(lo):
    ad = bpy.data.armatures.new("BatRig")
    arm = H.link(bpy.data.objects.new("Armature", ad))
    H.only(arm)
    bpy.ops.object.mode_set(mode="EDIT")
    for name, h, t, par in bone_specs():
        e = ad.edit_bones.new(name)
        e.head, e.tail, e.roll = h, t, 0.0
        if par:
            e.parent = ad.edit_bones[par]
    bpy.ops.object.mode_set(mode="OBJECT")
    for pb in arm.pose.bones:
        pb.rotation_mode = "QUATERNION"
    lo.parent = arm
    mod = lo.modifiers.new("Armature", "ARMATURE")
    mod.object = arm
    return arm


# ------------------------------------------------------------------ animation (PetsV2 clip pipeline)
class BatRig(pk.Pet):
    """petkit.Pet context bound to an existing armature (no scene reset, files go to Halloween/Bats)."""

    def __init__(self, arm):
        self.name = self.display = "Bat"
        self.dir = OUT
        self.parts, self.glow, self.body_bones = [], [], []
        self.J = {b.name: b.head_local.copy() for b in arm.data.bones}
        self.P = {b.name: b.parent.name for b in arm.data.bones if b.parent}
        self.tail = {}
        self.clips, self.events = {}, {}
        self.meta = {"motion": "Fly", "rig": "bat"}
        self.arm = arm
        self.coll = bpy.context.scene.collection
        self.glowobjs = {}


def keyq(k, bone, f, Q, loc=None):
    pb = k.arm.pose.bones[bone]
    R0 = k.arm.data.bones[bone].matrix_local.to_quaternion()
    pb.rotation_quaternion = R0.inverted() @ Q @ R0
    pb.keyframe_insert("rotation_quaternion", frame=f, group=bone)
    if loc is not None:
        pb.location = R0.inverted() @ Vector(loc)
        pb.keyframe_insert("location", frame=f, group=bone)


def Rx(d):
    return Quaternion((1, 0, 0), math.radians(d))


def Ry(d):
    return Quaternion((0, 1, 0), math.radians(d))


def Rz(d):
    return Quaternion((0, 0, 1), math.radians(d))


def wings(k, f, up, fwd, twist, tip_up, tip_fwd, asym=0.0, tip_twist=0.0):
    """Armature axes, bat flies +Y. up + = wing raised; fwd + = swept forward (toward +Y); twist + = leading edge
    down (pronation). Order: twist about the wing's long axis, then raise, then sweep. Hand relative to the arm."""
    for sd, sx in (("L", -1), ("R", 1)):
        a = 1.0 + asym * sx
        keyq(k, "Wing_" + sd, f, Rz(sx * fwd) @ Ry(-sx * up * a) @ Rx(-twist))
        keyq(k, "WingTip_" + sd, f, Rz(sx * tip_fwd) @ Ry(-sx * tip_up) @ Rx(-tip_twist))


def periodic(keys, n, f):
    """Periodic Catmull-Rom (non-uniform knots) through [(frame, value)] over a loop of n frames."""
    ks = sorted(keys)
    m = len(ks)
    T = [k_[0] for k_ in ks]
    V = [k_[1] for k_ in ks]

    def tv(i):
        q, r = divmod(i, m)
        return T[r] + q * n, V[r]

    f = f % n
    i = max(j for j in range(m) if T[j] <= f) if f >= T[0] else -1
    t0, v0 = tv(i)
    t1, v1 = tv(i + 1)
    tm, vm = tv(i - 1)
    tp, vp = tv(i + 2)
    m0 = (v1 - vm) / (t1 - tm)
    m1 = (vp - v0) / (tp - t0)
    h = t1 - t0
    s = (f - t0) / h
    h00, h10, h01, h11 = 2 * s ** 3 - 3 * s ** 2 + 1, s ** 3 - 2 * s ** 2 + s, -2 * s ** 3 + 3 * s ** 2, s ** 3 - s ** 2
    return h00 * v0 + h10 * h * m0 + h01 * v1 + h11 * h * m1


FLY_N = 12   # 0.40 s per wingbeat at 30 fps (reference: one beat = 10 drawings at 24 fps = 0.42 s)
# reference-driven key poses (Batman TAS #01 Man-Bat flight, Sakugabooru 69115; see NOTES.md)
#        frame:  up,  fwd, twist, tip_up, tip_fwd
FLY_KEYS = {0: (58, 2, -4, 22, -14),       # TOP: wings high, hand tips up + back (ref f93 / f103)
            2: (14, 12, 12, 4, 6),         # MID-DOWN: max span, swept forward, pronated - the power pose (f95 / f130)
            4: (-34, 8, 10, -16, 4),       # LATE DOWN: wings below the body, tips curling (f97)
            5: (-46, 2, 4, -26, -6),       # BOTTOM: folded under the body (f99 / f107 / f132)
            7: (-26, -12, -14, -40, -44),  # EARLY UP: the wrist leads, hand folded back + down (f101 / f134)
            9: (16, -12, -14, -24, -46),   # MID UP: wrist high, hand still folded (f91 / f136)
            11: (46, -4, -8, 6, -30)}      # unfolding into the top


def warp_phase(f, n=FLY_N, peak=5.5):
    """Time warp so a cosine peaks at the bottom of the stroke: 0..peak -> 0..0.5, peak..n -> 0.5..1."""
    f = f % n
    return 0.5 * f / peak if f <= peak else 0.5 + 0.5 * (f - peak) / (n - peak)


def fly(k):
    n = FLY_N
    k.new_action("fly", n, True)
    ch = [[(fr, v[i]) for fr, v in FLY_KEYS.items()] for i in range(5)]
    for f in range(n + 1):
        vals = [periodic(c, n, f) for c in ch]
        wings(k, f, *vals)
        g = warp_phase(f)
        z = -0.034 * math.cos(2 * math.pi * g)                     # body lowest at the top of the stroke
        pitch = 6.0 + 2.5 * math.cos(2 * math.pi * (g - 0.40))     # nose lifts a little on the power stroke
        k.key("Body", f, rot=(pitch, 0, 0), loc=(0, 0, z))
        g2 = warp_phase(f - 1)                                      # head + ears lag one frame
        k.key("Head", f, rot=(-(pitch - 6.0) * 0.8 - 5.0 - 1.5 * math.cos(2 * math.pi * (g2 - 0.40)), 0, 0))
        for sd, sx in (("L", -1), ("R", 1)):
            ear = 10.0 + 6.0 * math.cos(2 * math.pi * (g2 - 0.55))
            k.key("Ear_" + sd, f, rot=(ear, 0, -sx * 3.0 * math.sin(2 * math.pi * g2)))
            leg = 4.0 + 6.0 * math.sin(2 * math.pi * (f / n - 0.30))
            k.key("Leg_" + sd, f, rot=(leg, sx * 2.0 * math.sin(2 * math.pi * f / n), 0))
    k.finish()


GLIDE_N = 72   # 2.4 s, every channel an integer number of cycles -> seamless


def glide(k):
    n = GLIDE_N
    k.new_action("glide", n, True)
    TAU = 2 * math.pi
    for f in range(n + 1):
        t = f / n
        up = 7.0 + 3.0 * math.sin(TAU * t)
        asym = 0.25 * math.sin(TAU * t + 1.2)                       # small roll-control trims, L vs R
        wings(k, f, up, 4.0 + 2.0 * math.sin(TAU * 2 * t + 1.0), 2.0 + 2.0 * math.sin(TAU * t + 0.5),
              5.0 + 3.0 * math.sin(TAU * 2 * t + 0.7), -3.0 + 2.5 * math.sin(TAU * t + 1.9), asym=asym * 0.4,
              tip_twist=1.5 * math.sin(TAU * 2 * t + 2.2))
        roll = 4.0 * math.sin(TAU * t + 1.2)                        # banks into the trims
        k.key("Body", f, rot=(4.0 + 1.5 * math.sin(TAU * 2 * t), 0, roll), loc=(0, 0, 0.02 * math.sin(TAU * t + 0.3)))
        k.key("Head", f, rot=(-4.0 + 2.0 * math.sin(TAU * 2 * t + 0.8), 12.0 * math.sin(TAU * t + 0.6), -roll * 0.6))
        for sd, sx in (("L", -1), ("R", 1)):
            tw = 4.0 * math.sin(TAU * 3 * t + (0.0 if sx > 0 else 1.7)) * smooth(0.0, 0.3, math.sin(TAU * t) ** 2)
            k.key("Ear_" + sd, f, rot=(8.0 + tw, 0, -sx * 2.0 * math.sin(TAU * t)))
            k.key("Leg_" + sd, f, rot=(3.0 + 3.0 * math.sin(TAU * 2 * t + sx), sx * 1.5 * math.sin(TAU * t), 0))
    k.finish()


def animate(arm):
    k = BatRig(arm)
    fly(k)
    glide(k)
    rep = pk.audit(k)
    data = pk.sample(k)
    size = pk.write_clips(k, data, None)
    k.set_action("fly")
    return k, {"audit": rep, "lua_bytes": size, "clips": {c: [n, round(n / pk.FPS, 3)] for c, (n, lp) in k.clips.items()},
               "ref": {"bone": "Head", "dist": round((k.J["Head"] - k.J["Root"]).length, 5)}}


# ------------------------------------------------------------------ build / export / render
def preview():
    H.fresh(samples=16)
    t0 = time.time()
    objs = build_hi()
    tris = {o.name: sum(len(p.vertices) - 2 for p in o.data.polygons) for o in objs}
    H.review_setup(res=(1100, 800))
    out = [H.shoot(os.path.join(REN, "pv_top34.png"), (1.0, 0.0, 0.05), (0.35, 0.55, 1.0), 5.6, lens=50),
           H.shoot(os.path.join(REN, "pv_face.png"), (0.0, 0.58, 0.08), (0.55, 1.0, 0.25), 1.05, lens=50),
           H.shoot(os.path.join(REN, "pv_face_front.png"), (0.0, 0.60, 0.09), (0.0, 1.0, 0.12), 0.95, lens=50),
           H.shoot(os.path.join(REN, "pv_below.png"), (0.9, -0.1, 0.0), (0.2, 0.3, -1.0), 5.6, lens=50),
           H.shoot(os.path.join(REN, "pv_body.png"), (0.3, 0.0, 0.05), (0.9, 0.5, 0.6), 2.2, lens=50)]
    return {"tris_hi": tris, "s": round(time.time() - t0, 1), "renders": out}


def build():
    H.fresh(samples=32)
    t0 = time.time()
    rep = {}
    hi = build_hi()
    rep["hi_tris"] = sum(len(p.vertices) - 2 for o in hi for p in o.data.polygons)
    t1 = time.time()
    lo = build_lo()
    rep["lo_s"] = round(time.time() - t1, 1)
    rep["tris"] = sum(len(p.vertices) - 2 for p in lo.data.polygons)
    t2 = time.time()
    big = os.path.join(MAPS, "_ss")
    imgs = H.bake_set(lo, hi, SS, "Bat", cage=0.022, maxray=0.05, ao_strength=0.55, ao_dist=0.15, outdir=big)
    rep["bake_s"] = round(time.time() - t2, 1)
    rep["miss_fraction"] = round(imgs["miss_fraction"], 4)
    rep["bone_texels"] = rebake_bones(lo, hi, imgs, SS)
    imgs = downsample(imgs, SS, TEX)
    for f in os.listdir(big):
        os.remove(os.path.join(big, f))
    os.rmdir(big)
    H.pbr_material(lo, "Bat_PBR", imgs)
    coll = bpy.data.collections.new("Sculpt_hi")
    bpy.context.scene.collection.children.link(coll)
    for o in hi:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)
        o.hide_render = True
    coll.hide_viewport = coll.hide_render = True
    arm = build_rig(lo)
    k, rep["anim"] = animate(arm)
    mn = Vector([min((lo.matrix_world @ v.co)[i] for v in lo.data.vertices) for i in range(3)])
    mx = Vector([max((lo.matrix_world @ v.co)[i] for v in lo.data.vertices) for i in range(3)])
    rep["size"] = [round(x, 3) for x in (mx - mn)]
    rep["bounds"] = [[round(x, 3) for x in mn], [round(x, 3) for x in mx]]
    rep["vgroups"] = sorted(g.name for g in lo.vertex_groups)
    infl = [sum(1 for g in v.groups if g.weight > 0) for v in lo.data.vertices]
    rep["max_influences"] = max(infl)
    rep["unweighted"] = sum(1 for x in infl if x == 0)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    rep["total_s"] = round(time.time() - t0, 1)
    return rep


def export():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    arm, lo = bpy.data.objects["Armature"], bpy.data.objects["Bat"]
    arm.data.pose_position = "REST"
    bpy.context.view_layer.update()
    for o in bpy.context.view_layer.objects:
        o.select_set(o in (arm, lo))
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.fbx(filepath=FBX_PATH, use_selection=True, global_scale=0.01, apply_unit_scale=True,
                             apply_scale_options="FBX_SCALE_NONE", axis_forward="-Z", axis_up="Y",
                             object_types={"ARMATURE", "MESH"}, use_mesh_modifiers=True, mesh_smooth_type="FACE",
                             add_leaf_bones=False, bake_anim=False, path_mode="COPY", embed_textures=True,
                             use_armature_deform_only=False)
    arm.data.pose_position = "POSE"
    return {"fbx": FBX_PATH, "kb": round(os.path.getsize(FBX_PATH) / 1024, 1),
            "tris": sum(len(p.vertices) - 2 for p in lo.data.polygons),
            "bones": [b.name for b in arm.data.bones]}


def compose(files, out, cols):
    imgs = [bpy.data.images.load(f, check_existing=False) for f in files]
    w, h = imgs[0].size
    rows = (len(imgs) + cols - 1) // cols
    big = np.ones((rows * h, cols * w, 4), np.float32)
    for i, im in enumerate(imgs):
        a = np.array(im.pixels[:], np.float32).reshape(h, w, 4)
        r, c = i // cols, i % cols
        big[(rows - 1 - r) * h:(rows - r) * h, c * w:(c + 1) * w] = a
    o = bpy.data.images.new("strip", cols * w, rows * h, alpha=True)
    o.pixels[:] = big.ravel()
    o.filepath_raw = out
    o.file_format = "PNG"
    o.save()
    return out


def set_act(arm, a):
    arm.animation_data.action = a
    if arm.animation_data.action_slot is None and a.slots:
        arm.animation_data.action_slot = a.slots[0]


def pose_copy(src, dst):
    for pb in src.pose.bones:
        q = dst.pose.bones[pb.name]
        q.rotation_quaternion = pb.rotation_quaternion.copy()
        q.location = pb.location.copy()


def render():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = H.review_setup(res=(1400, 1000))
    sc.render.film_transparent = False
    arm, lo = bpy.data.objects["Armature"], bpy.data.objects["Bat"]
    act = {a.name: a for a in bpy.data.actions}
    set_act(arm, act["fly"])
    out = []
    sc.frame_set(2)       # max-span power pose
    out.append(H.shoot(os.path.join(OUT, "review_bat_34.png"), (0.0, 0.1, 0.05), (0.55, 0.75, 0.55), 7.2, lens=50))
    out.append(H.shoot(os.path.join(OUT, "review_bat_below.png"), (0.0, 0.0, 0.0), (0.25, 0.35, -1.0), 7.0, lens=50))
    set_act(arm, act["glide"])
    sc.frame_set(0)
    out.append(H.shoot(os.path.join(OUT, "review_bat_face.png"), bs(0.0, 0.5, 0.09), (0.5, 1.0, 0.22), 1.25, lens=50))
    out.append(H.shoot(os.path.join(OUT, "review_bat_top.png"), (0.0, -0.1, 0.0), (0.0, -0.25, 1.0), 6.8, lens=50))
    # the flock at hub distance: 12 bats on a ring, each in another phase of the beat
    set_act(arm, act["fly"])
    copies = []
    ring_c, ring_r = Vector((0, 0, 0)), 14.0
    for i in range(12):
        sc.frame_set(i % FLY_N)
        a2 = arm.copy()
        a2.animation_data_clear()
        H.link(a2)
        pose_copy(arm, a2)
        l2 = lo.copy()
        H.link(l2)
        l2.parent = a2
        l2.modifiers["Armature"].object = a2
        ang = 2 * math.pi * i / 12
        pos = ring_c + Vector((math.cos(ang) * ring_r, math.sin(ang) * ring_r, 2.5 * math.sin(3 * ang)))
        tang = Vector((-math.sin(ang), math.cos(ang), 0))
        a2.matrix_world = Matrix.Translation(pos) @ (tang.to_track_quat("Y", "Z").to_matrix().to_4x4()) \
            @ Matrix.Rotation(math.radians(-18), 4, "Y")
        copies.append((a2, l2))
    lo.hide_render = True
    out.append(H.shoot(os.path.join(OUT, "review_flock_45studs.png"), ring_c + Vector((0, 0, 1.0)), (0.0, -1.0, 0.32), 45.0,
                       lens=50))
    out.append(H.shoot(os.path.join(OUT, "review_flock_below.png"), ring_c, (0.15, -0.45, -1.0), 30.0, lens=40))
    for a2, l2 in copies:
        bpy.data.objects.remove(l2)
        bpy.data.objects.remove(a2)
    lo.hide_render = False
    # flap strip: 8 frames of one wingbeat, 3/4 front view
    sc.render.resolution_x, sc.render.resolution_y = 480, 400
    files = []
    set_act(arm, act["fly"])
    for f in (0, 2, 4, 5, 7, 8, 9, 11):
        sc.frame_set(f)
        files.append(H.shoot(os.path.join(REN, "strip_f%02d.png" % f), (0.0, 0.0, 0.0), (0.45, 1.0, 0.30), 9.0, lens=50))
    out.append(compose(files, os.path.join(OUT, "review_flap_strip.png"), 4))
    files = []
    for f in (0, 2, 4, 5, 7, 8, 9, 11):
        sc.frame_set(f)
        files.append(H.shoot(os.path.join(REN, "stripF_f%02d.png" % f), (0.0, 0.0, 0.0), (0.0, 1.0, 0.06), 9.0, lens=50))
    out.append(compose(files, os.path.join(REN, "flap_strip_front.png"), 4))
    files = []
    set_act(arm, act["glide"])
    for f in (0, 18, 36, 54):
        sc.frame_set(f)
        files.append(H.shoot(os.path.join(REN, "glide_f%02d.png" % f), (0.0, 0.0, 0.0), (0.45, 1.0, 0.30), 9.0, lens=50))
    out.append(compose(files, os.path.join(REN, "glide_strip.png"), 4))
    sc.render.resolution_x, sc.render.resolution_y = 1400, 1000
    sc.frame_set(0)
    out.append(H.shoot(os.path.join(REN, "review_wing_close.png"), (1.55, 0.0, 0.1), (0.25, 0.35, 1.0), 2.4, lens=50))
    return out


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["preview"]
    rep = {}
    for step in argv:
        if step == "preview":
            rep["preview"] = preview()
        elif step == "build":
            rep["build"] = build()
        elif step == "export":
            rep["export"] = export()
        elif step == "render":
            rep["render"] = render()
    print("BAT_REPORT " + json.dumps(rep))
