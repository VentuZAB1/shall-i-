# SLINGSHOT Halloween hub - SPIDER WEBS (corner + torn) and the hanging SPIDER.
# Headless:  blender.exe -b --factory-startup --python webs_spiders.py -- webs render_webs export_webs spider render_spider export_spider
# (export_webs adds the _Mirror copies to webs.blend, so render before exporting.)
#
# Webs: real tube strands (radials / frame / anchors 4-sided, catch spiral 3-sided) laid out in 2D (x, z), warped by a
# smooth noise field (so junctions stay joined) and lifted to 3D by a gentle bow toward +Y (the viewers). The web lies
# in the Blender X-Z plane, the corner at the origin, filling x in [0, R], z in [-R, 0]; the wall is at y = -0.3.
# Strands carry a small planar-projected dust/colour map; the torn web's silk sheets are a separate part with an RGBA
# fibre map (SurfaceAppearance AlphaMode = Transparency in Roblox).
# Spider: dense procedural sculpt (hairs, spines, eyes, fangs) -> its own coarse game mesh (same functions, low res)
# -> 1024 bakes (normal, colour x AO, roughness) -> FBX. Hanging pose: abdomen up, dorsal side facing +Y.
import sys, os
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import *  # noqa
import json, time
from mathutils import Matrix
from mathutils.bvhtree import BVHTree

OUT = os.path.join(HERE, "WebsSpiders")
MAPS = os.path.join(OUT, "maps")
BLEND_WEBS = os.path.join(OUT, "webs.blend")
BLEND_SPIDER = os.path.join(OUT, "spider.blend")
os.makedirs(MAPS, exist_ok=True)


# ================================================================== shared helpers
def srgb(c):
    return tuple(v / 255.0 for v in c)


def vnoise(n, cells, rng, octaves=4, gain=0.5):
    """numpy value-noise fBm on an n x n grid, 0..1."""
    out = np.zeros((n, n), np.float32)
    amp, tot, c = 1.0, 0.0, cells
    for _ in range(octaves):
        g = rng.random((c + 2, c + 2)).astype(np.float32)
        xs = np.arange(n, dtype=np.float32) * (c / n)
        i0 = np.floor(xs).astype(int)
        f = xs - i0
        f = f * f * (3 - 2 * f)
        a = g[np.ix_(i0, i0)]
        b = g[np.ix_(i0, i0 + 1)]
        cc = g[np.ix_(i0 + 1, i0)]
        d = g[np.ix_(i0 + 1, i0 + 1)]
        fx, fy = f[None, :], f[:, None]
        out += amp * ((a * (1 - fx) + b * fx) * (1 - fy) + (cc * (1 - fx) + d * fx) * fy)
        tot += amp
        amp *= gain
        c *= 2
    return out / tot


def mnoise(n, scale, seed, octaves=3, aspect=(1.0, 1.0)):
    """n x n fBm from mathutils noise (organic, no value-noise grid), normalised to 0..1."""
    out = np.empty((n, n), np.float32)
    off = Vector((seed * 13.17, seed * 7.31, seed * 3.77))
    sx, sy = scale * aspect[0] / n, scale * aspect[1] / n
    for j in range(n):
        for i in range(n):
            out[j, i] = fbm(Vector((i * sx, j * sy, 0.0)) + off, octaves)
    lo, hi = np.percentile(out, 1), np.percentile(out, 99)
    return np.clip((out - lo) / max(1e-6, hi - lo), 0, 1)


def make_image(name, arr, colorspace, path):
    """arr: (h, w, 4) float 0..1 (sRGB-encoded values for colour images, raw for data)."""
    h, w = arr.shape[:2]
    img = bpy.data.images.new(name, w, h, alpha=True)
    img.colorspace_settings.name = colorspace
    img.pixels.foreach_set(np.ascontiguousarray(arr, dtype=np.float32).ravel())
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    img.alpha_mode = "STRAIGHT"
    return img


def mat_tex(name, col_img, rough_img=None, alpha=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = col_img
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    if alpha:
        nt.links.new(t.outputs["Alpha"], b.inputs["Alpha"])
        try:
            m.surface_render_method = "DITHERED"
        except Exception:
            pass
    if rough_img:
        tr = nt.nodes.new("ShaderNodeTexImage")
        tr.image = rough_img
        sep = nt.nodes.new("ShaderNodeSeparateColor")
        nt.links.new(tr.outputs["Color"], sep.inputs["Color"])
        nt.links.new(sep.outputs["Red"], b.inputs["Roughness"])
    b.inputs["Metallic"].default_value = 0.0
    return m


def set_uvs(me, uv_of_vert):
    """uv_of_vert: list (per vertex) of (u, v)."""
    uv = me.uv_layers.new(name="UVMap")
    data = []
    for lp in me.loops:
        data.extend(uv_of_vert[lp.vertex_index])
    uv.data.foreach_set("uv", data)


def tris_of(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


def shoot_fov(path, loc, target, vfov=70.0, lens=None, res=None):
    """In-game style camera: vertical FOV like Roblox (70 deg), or a lens for close-ups."""
    sc = bpy.context.scene
    if res:
        sc.render.resolution_x, sc.render.resolution_y = res
    cd = bpy.data.cameras.new("Cam")
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    if lens:
        cd.lens = lens
    else:
        cd.sensor_fit = "VERTICAL"
        cd.sensor_height = 24.0
        cd.lens = 12.0 / math.tan(math.radians(vfov / 2))
    cd.clip_start = 0.05
    cd.clip_end = 5000
    sc.camera = cam
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    return path


# ================================================================== WEBS
class Strands:
    """Accumulates tube geometry for thin strands in one bmesh."""

    def __init__(self):
        self.bm = bmesh.new()

    def tube(self, pts, r, sides=3):
        n = len(pts)
        if n < 2:
            return
        bm = self.bm
        T = []
        for i in range(n):
            t = pts[min(n - 1, i + 1)] - pts[max(0, i - 1)]
            T.append(t.normalized() if t.length > 1e-9 else Vector((1, 0, 0)))
        ref = Vector((0, 1, 0))
        N = ref - T[0] * ref.dot(T[0])
        if N.length < 1e-3:
            alt = Vector((0, 0, 1))
            N = alt - T[0] * alt.dot(T[0])
        N.normalize()
        rings = []
        for i in range(n):
            N = N - T[i] * N.dot(T[i])
            if N.length < 1e-6:
                N = ref - T[i] * ref.dot(T[i])
            N.normalize()
            B = T[i].cross(N)
            rr = r[i] if isinstance(r, (list, tuple)) else r
            rings.append([bm.verts.new(pts[i] + (N * math.cos(2 * math.pi * j / sides)
                                                  + B * math.sin(2 * math.pi * j / sides)) * rr)
                          for j in range(sides)])
        for i in range(n - 1):
            for j in range(sides):
                k = (j + 1) % sides
                bm.faces.new((rings[i][j], rings[i][k], rings[i + 1][k], rings[i + 1][j]))

    def blob(self, centre, rx, ry, rz, nu=8, nv=5, fn=None):
        """Closed ellipsoid-ish shell (hub mat, cocoon). fn(t, a) -> radius factor (t 0..1 top->bottom)."""
        bm = self.bm
        top = bm.verts.new(centre + Vector((0, 0, rz)))
        rings = []
        for i in range(1, nv):
            t = i / nv
            th = math.pi * t
            ring = []
            for j in range(nu):
                a = 2 * math.pi * j / nu
                k = fn(t, a) if fn else 1.0
                ring.append(bm.verts.new(centre + Vector((rx * math.sin(th) * math.cos(a) * k,
                                                          ry * math.sin(th) * math.sin(a) * k,
                                                          rz * math.cos(th)))))
            rings.append(ring)
        bot = bm.verts.new(centre - Vector((0, 0, rz)))
        fs = []
        for j in range(nu):
            k = (j + 1) % nu
            fs.append(bm.faces.new((top, rings[0][j], rings[0][k])))
            for i in range(len(rings) - 1):
                fs.append(bm.faces.new((rings[i][j], rings[i + 1][j], rings[i + 1][k], rings[i][k])))
            fs.append(bm.faces.new((rings[-1][k], rings[-1][j], bot)))
        bmesh.ops.recalc_face_normals(bm, faces=fs)

    def to_object(self, name, uvfun):
        bmesh.ops.triangulate(self.bm, faces=self.bm.faces[:])
        me = bpy.data.meshes.new(name)
        self.bm.to_mesh(me)
        self.bm.free()
        for p in me.polygons:
            p.use_smooth = True
        set_uvs(me, [uvfun(v.co) for v in me.vertices])
        return link(bpy.data.objects.new(name, me))


def sag2(a, b, n, sv, k=2.4):
    """2D catenary from a to b; sv = offset at the middle."""
    c0 = math.cosh(k / 2)
    out = []
    for i in range(n + 1):
        t = i / n
        s = (math.cosh(k * (t - 0.5)) - c0) / (1 - c0)
        out.append((a[0] + (b[0] - a[0]) * t + sv[0] * s, a[1] + (b[1] - a[1]) * t + sv[1] * s))
    return out


def ray_hit(o, d, poly):
    best = None
    for i in range(len(poly) - 1):
        p, q = poly[i], poly[i + 1]
        e = (q[0] - p[0], q[1] - p[1])
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-12:
            continue
        w = (p[0] - o[0], p[1] - o[1])
        t = (w[0] * e[1] - w[1] * e[0]) / den
        u = (w[0] * d[1] - w[1] * d[0]) / den
        if t > 1e-6 and -1e-6 <= u <= 1 + 1e-6 and (best is None or t < best):
            best = t
    return best


def hanging(p0, d0, length, n, rng, drift=0.04):
    """A loose strand: starts at p0 heading d0 and falls under gravity (3D points)."""
    pts = [p0.copy()]
    d = Vector(d0).normalized()
    d.z = min(d.z, -0.25)          # a snapped strand never springs upward: it falls from where it broke
    d.normalize()
    seg = length / n
    down = Vector((0, 0, -1))
    for _ in range(n):
        d = (d.lerp(down, 0.42) + Vector((rng.uniform(-0.1, 0.1), rng.uniform(-0.02, drift), 0))).normalized()
        pts.append(pts[-1] + d * seg)
    return pts


class Web:
    def __init__(self, P):
        self.P = P
        self.rng = random.Random(P["seed"])
        self.S = Strands()
        self.off = Vector((P["seed"] * 1.37, P["seed"] * 0.71, 3.3))
        self.info = {}

    def warp(self, x, z):
        P = self.P
        k = smoothstep(0.0, P["edge"], x) * smoothstep(0.0, P["edge"], -z) * P["warp"]
        p = Vector((x * 0.21, z * 0.21, 0.0)) + self.off
        return x + k * noise.noise(p), z + k * noise.noise(p + Vector((17.3, 5.1, 3.3)))

    def to3(self, x, z):
        P = self.P
        x, z = self.warp(x, z)
        hx, hz = P["hub"]
        d = math.hypot(x - hx, z - hz)
        e = smoothstep(0.0, P["edge"], x) * smoothstep(0.0, P["edge"], -z)
        f = e * max(0.0, 1.0 - (d / P["D"]) ** 2)
        y = P["y0"] + P["bow"] * f + P["yjit"] * e * noise.noise(Vector((x * 0.6, z * 0.6, 0)) + self.off * 0.5)
        return Vector((x, y, z))

    def line(self, pts2):
        return [self.to3(x, z) for x, z in pts2]

    # ---------------------------------------------------------- layout
    def build_orb(self):
        P, rng, S = self.P, self.rng, self.S
        hx, hz = P["hub"]
        H = (hx, hz)
        # frame: sagging threads between the frame vertices (pulled toward the hub)
        frame2 = []
        F = P["frame"]
        for k in range(len(F) - 1):
            a, b = F[k], F[k + 1]
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            to_h = Vector((hx - m[0], hz - m[1])).normalized()
            seg = sag2(a, b, P["frame_seg"], (to_h.x * P["frame_sag"], to_h.y * P["frame_sag"] - P["frame_g"]))
            frame2 += seg if k == 0 else seg[1:]
        self.frame2 = frame2
        # radials
        th0 = math.atan2(F[0][1] - hz, F[0][0] - hx)
        th1 = math.atan2(F[-1][1] - hz, F[-1][0] - hx)
        N = P["radials"]
        rad = []
        for i in range(N):
            th = th0 + (th1 - th0) * i / (N - 1)
            if 0 < i < N - 1:
                th += math.radians(rng.uniform(-1.0, 1.0) * P["rad_jit"])
            d = (math.cos(th), math.sin(th))
            L = ray_hit(H, d, frame2)
            if i == 0:
                L = math.hypot(F[0][0] - hx, F[0][1] - hz)
            if i == N - 1:
                L = math.hypot(F[-1][0] - hx, F[-1][1] - hz)
            rad.append((th, d, L))
        self.rad = rad
        # catch spiral ring distances (per radial jitter)
        K = P["rings"]
        dk = [P["d0"] + P["sp"] * k + P["sp_g"] * k * k for k in range(K)]
        ringpts = []
        for k in range(K):
            row = []
            for i, (th, d, L) in enumerate(rad):
                dd = dk[k] * (1 + P["ring_jit"] * noise.noise(Vector((i * 0.83, k * 0.41, 7.7)) + self.off)) \
                     + rng.uniform(-0.04, 0.04)
                row.append((hx + d[0] * dd, hz + d[1] * dd) if dd < P["ring_stop"] * L else None)
            ringpts.append(row)
        self.ringpts = ringpts
        return frame2, rad, ringpts

    def span_curve(self, a, b, k_frac):
        P = self.P
        hx, hz = P["hub"]
        span = math.hypot(b[0] - a[0], b[1] - a[1])
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        to_h = Vector((hx - m[0], hz - m[1])).normalized()
        s_in = (P["sag_in"] + P["sag_in_out"] * k_frac) * span
        s_g = P["sag_g"] * span
        n = max(2, min(6, int(round(span / P["seg_len"]))))
        return sag2(a, b, n, (to_h.x * s_in, to_h.y * s_in - s_g))

    def draw_rings(self, broken_fn, r, sides, loose_p, loose_len):
        """Rings as polylines; broken spans split them, some leave a loose hanging end."""
        rng, S = self.rng, self.S
        K = len(self.ringpts)
        loose = []
        for k, row in enumerate(self.ringpts):
            cur = []
            for i in range(len(row) - 1):
                a, b = row[i], row[i + 1]
                if a is None or b is None or broken_fn(k, i, a, b):
                    if len(cur) > 1:
                        S.tube(self.line(cur), r, sides)
                    cur = []
                    if a is not None and b is not None and rng.random() < loose_p:
                        # the snapped thread curls down from one side
                        src, dst = (a, b) if rng.random() < 0.5 else (b, a)
                        p0 = self.to3(*src)
                        d0 = self.to3(*dst) - p0
                        L = rng.uniform(*loose_len) * d0.length
                        pts = hanging(p0, d0, max(0.35, L), max(3, int(L / 0.18)), rng)
                        S.tube(pts, [r * (1 - 0.45 * t / (len(pts) - 1)) for t in range(len(pts))], sides)
                        loose.append((k, i))
                    continue
                seg = self.span_curve(a, b, k / max(1, K - 1))
                cur += seg if not cur else seg[1:]
            if len(cur) > 1:
                S.tube(self.line(cur), r, sides)
        return loose

    def draw_radials(self, r, sides, cut_fn=None, loose_p=0.0, loose_len=(0.6, 1.4)):
        P, rng, S = self.P, self.rng, self.S
        hx, hz = P["hub"]
        for i, (th, d, L) in enumerate(self.rad):
            n = max(6, min(16, int(round(L / P["rad_seg"]))))
            pts = [(hx + d[0] * L * t / n, hz + d[1] * L * t / n) for t in range(n + 1)]
            pieces, cur = [], []
            for p in pts:
                if cut_fn and cut_fn(*p):
                    if len(cur) > 1:
                        pieces.append(cur)
                    cur = []
                else:
                    cur.append(p)
            if len(cur) > 1:
                pieces.append(cur)
            for pc in pieces:
                S.tube(self.line(pc), r, sides)
                if cut_fn and loose_p > 0:
                    for end, prev in ((pc[-1], pc[-2]), (pc[0], pc[1])):
                        far_from_ends = math.hypot(end[0] - hx, end[1] - hz) > 0.5 and \
                                        math.hypot(end[0] - (hx + d[0] * L), end[1] - (hz + d[1] * L)) > 0.3
                        if far_from_ends and rng.random() < loose_p:
                            p0 = self.to3(*end)
                            d0 = p0 - self.to3(*prev)
                            ll = rng.uniform(*loose_len)
                            hp = hanging(p0, d0, ll, max(4, int(ll / 0.2)), rng)
                            S.tube(hp, [r * (1 - 0.5 * t / (len(hp) - 1)) for t in range(len(hp))], sides)

    def draw_hub(self, r_spiral, r_anchor, back_angles, turns, d_in, d_out):
        P, rng, S = self.P, self.rng, self.S
        hx, hz = P["hub"]
        # anchors from the hub back to the pillar / trim / corner
        dirs = [th for th, d, L in self.rad]
        for ang in back_angles:
            th = math.radians(ang + rng.uniform(-3, 3))
            c, s = math.cos(th), math.sin(th)
            ts = []
            if c < 0:
                ts.append(-hx / c)
            if s > 0:
                ts.append(-hz / s)
            t = min(ts)
            end = (hx + c * t, hz + s * t)
            n = max(3, int(t / 0.5))
            S.tube(self.line([(hx + (end[0] - hx) * i / n, hz + (end[1] - hz) * i / n) for i in range(n + 1)]),
                   r_anchor, 4)
            dirs.append(th)
        # hub spiral: a tight irregular spiral crossing every radial / anchor
        dirs = sorted(((a + 2 * math.pi) % (2 * math.pi)) for a in dirs)
        pts = []
        total = turns * len(dirs)
        for n_ in range(int(total) + 1):
            a = dirs[n_ % len(dirs)] + 2 * math.pi * (n_ // len(dirs))
            dd = d_in + (d_out - d_in) * n_ / total
            dd *= 1 + 0.08 * rng.uniform(-1, 1)
            pts.append((hx + math.cos(a) * dd, hz + math.sin(a) * dd))
        dense = []
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            span = math.hypot(b[0] - a[0], b[1] - a[1])
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            to_h = Vector((hx - m[0], hz - m[1])).normalized() * 0.12 * span
            seg = sag2(a, b, 2 if span < 0.5 else 3, (to_h.x, to_h.y))
            dense += seg if not dense else seg[1:]
        S.tube(self.line(dense), r_spiral, 3)
        # the silk mat in the middle of the hub
        S.blob(self.to3(hx, hz) + Vector((0, 0.02, 0)), 0.2, 0.06, 0.2, nu=8, nv=5,
               fn=lambda t, a: 1 + 0.18 * math.sin(3 * a + 1.3))

    def draw_frame(self, r, guys):
        S, P = self.S, self.P
        hx, hz = P["hub"]
        S.tube(self.line(self.frame2), r, 4)
        for (fx, fz), extra in guys:
            p0 = self.to3(fx, fz)
            out = Vector((fx - hx, 0, fz - hz)).normalized()
            if extra == "wall":
                end = Vector((fx, -0.3 + r * 0.6, fz)) + out * 0.55
                S.tube([p0, p0.lerp(end, 0.5), end], r * 0.8, 4)
            else:  # an anchor to an edge point (x, z)
                ex, ez = extra
                n = 4
                S.tube(self.line([(fx + (ex - fx) * i / n, fz + (ez - fz) * i / n) for i in range(n + 1)]), r, 4)

    def cocoon(self, at2, drop, length, radius, seed):
        """A silk-wrapped prey bundle hanging under a ring point on a short thread."""
        rng = random.Random(seed)
        p0 = self.to3(*at2)
        top = p0 + Vector((rng.uniform(-0.05, 0.05), 0.05, -drop))
        self.S.tube([p0, p0.lerp(top, 0.5) + Vector((0.02, 0, 0)), top + Vector((0, 0, 0.05))], 0.03, 3)
        c = top - Vector((0, 0, length / 2))
        ph = rng.uniform(0, 6.28)
        self.S.blob(c, radius, radius * 0.9, length / 2, nu=8, nv=12,
                    fn=lambda t, a: (0.75 + 0.25 * math.sin(math.pi * t)) * (1 + 0.1 * math.sin(a + t * 15 + ph))
                    * (1 + 0.06 * math.sin(3 * a - t * 9)))


def strand_maps(prefix, size, seed, base, dust, bright, dusty, rough_lo, rough_hi):
    """Planar colour + roughness map for a web: silver silk, dust collecting toward the wall edges / corner."""
    rng = np.random.default_rng(seed)
    n = size
    u = (np.arange(n) + 0.5) / n
    U, V = np.meshgrid(u, u)          # V: 0 bottom (z=-R) .. 1 top (z=0)
    edge = np.clip(1 - np.minimum(U, 1 - V) / 0.22, 0, 1)            # near the pillar (u=0) / trim (v=1)
    corner = np.exp(-((U) ** 2 + (1 - V) ** 2) / 0.05)
    nz = mnoise(n, 4.0, seed, 4)
    dm = np.clip((nz - 0.45) * 2.2 * dusty + 0.55 * edge * dusty + 0.4 * corner, 0, 1)
    sp = (rng.random((n, n)) > 0.993).astype(np.float32) * 0.35    # dust specks
    dm = np.clip(dm + sp * dusty, 0, 1)
    hi = np.clip((mnoise(n, 8.0, seed + 1, 3) - 0.55) * 3, 0, 1) * (1 - dm)
    col = np.zeros((n, n, 4), np.float32)
    for c in range(3):
        col[..., c] = (srgb(base)[c] * (1 - dm) + srgb(dust)[c] * dm) * (1 - 0.35 * hi) + srgb(bright)[c] * 0.35 * hi
    col[..., 3] = 1
    rgh = np.zeros((n, n, 4), np.float32)
    r = rough_lo + (rough_hi - rough_lo) * dm
    for c in range(3):
        rgh[..., c] = r
    rgh[..., 3] = 1
    ci = make_image(prefix + "_albedo", col, "sRGB", os.path.join(MAPS, prefix + "_albedo.png"))
    ri = make_image(prefix + "_rough", rgh, "Non-Color", os.path.join(MAPS, prefix + "_rough.png"))
    return ci, ri


# ---------------------------------------------------------------- corner web
CORNER = dict(seed=7, R=13.0, hub=(1.75, -1.7), D=11.2, y0=0.05, bow=0.42, yjit=0.06, edge=2.2, warp=0.3,
              frame=[(12.7, 0.0), (12.35, -4.7), (10.0, -9.05), (5.3, -12.05), (0.0, -12.8)],
              frame_seg=12, frame_sag=0.3, frame_g=0.05,
              radials=15, rad_jit=3.4, rad_seg=1.3,
              rings=16, d0=2.55, sp=0.43, sp_g=0.0065, ring_jit=0.05, ring_stop=0.93,
              sag_in=0.075, sag_in_out=0.05, sag_g=0.03, seg_len=0.27)


def build_corner():
    P = CORNER
    W = Web(P)
    W.build_orb()
    rng = W.rng
    breaks = set()
    while len(breaks) < 6:   # a few snapped spiral spans in the outer half
        breaks.add((rng.randint(6, P["rings"] - 1), rng.randint(1, P["radials"] - 3)))
    W.draw_rings(lambda k, i, a, b: (k, i) in breaks, 0.0375, 3, loose_p=0.85, loose_len=(0.45, 0.8))
    W.draw_radials(0.05, 4)
    W.draw_hub(0.034, 0.056, back_angles=(40, 90, 135, 180, 228), turns=3.2, d_in=0.22, d_out=1.05)
    F = P["frame"]
    W.draw_frame(0.06, guys=[(F[1], "wall"), (F[2], "wall"), (F[3], "wall"), (F[1], (13.05, 0.0))])
    # two long old threads hanging off the lower frame + one from the web
    fr = W.frame2
    for idx, ln in ((int(len(fr) * 0.72), 0.9), (int(len(fr) * 0.43), 1.3)):
        p0 = W.to3(*fr[idx])
        W.S.tube(hanging(p0, Vector((0.3, 0.05, -1)), ln, 7, rng), 0.032, 3)
    ring = W.ringpts[9]
    if ring[4] is not None:
        p0 = W.to3(*ring[4])
        W.S.tube(hanging(p0, Vector((0.2, 0.05, -1)), 1.5, 9, rng), 0.03, 3)
    # one small wrapped prey bundle
    pt = W.ringpts[7][6] or W.ringpts[6][6]
    W.cocoon(pt, 0.28, 0.6, 0.15, seed=3)
    R = 14.0
    ob = W.S.to_object("SpiderWeb_Corner", lambda co: (min(1, max(0, co.x / R)), min(1, max(0, 1 + co.z / R))))
    ci, ri = strand_maps("WebCorner", 256, 11, base=(228, 230, 236), dust=(184, 178, 168), bright=(250, 251, 255),
                         dusty=0.55, rough_lo=0.38, rough_hi=0.72)
    ob.data.materials.append(mat_tex("WebCorner_Mat", ci, ri))
    return ob


# ---------------------------------------------------------------- torn web
TORN = dict(seed=23, R=18.0, hub=(2.5, -2.35), D=15.5, y0=0.05, bow=0.55, yjit=0.09, edge=2.6, warp=0.32,
            frame=[(17.5, 0.0), (17.0, -6.6), (13.9, -12.7), (7.6, -16.6), (0.0, -17.5)],
            frame_seg=14, frame_sag=0.55, frame_g=0.35,
            radials=12, rad_jit=4.5, rad_seg=1.4,
            rings=14, d0=3.3, sp=0.72, sp_g=0.011, ring_jit=0.07, ring_stop=0.9,
            sag_in=0.08, sag_in_out=0.06, sag_g=0.13, seg_len=0.43)
TORN_HOLES = [((9.6, -6.2), 2.6), ((6.4, -12.0), 2.0), ((14.0, -9.6), 1.7), ((3.4, -8.6), 1.2)]


def build_torn():
    P = TORN
    W = Web(P)
    W.build_orb()
    rng = W.rng

    def in_hole(x, z):
        for (cx, cz), r in TORN_HOLES:
            rr = r * (1 + 0.22 * noise.noise(Vector((x * 0.7, z * 0.7, 2.2))))
            if (x - cx) ** 2 + (z - cz) ** 2 < rr * rr:
                return True
        return False

    def broken(k, i, a, b):
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        return in_hole(*m) or rng.random() < 0.09

    W.draw_rings(broken, 0.04, 3, loose_p=0.28, loose_len=(0.5, 1.3))
    W.draw_radials(0.052, 4, cut_fn=in_hole, loose_p=0.75, loose_len=(0.7, 2.0))
    W.draw_hub(0.036, 0.06, back_angles=(42, 92, 135, 178, 226), turns=3.0, d_in=0.28, d_out=1.35)
    F = P["frame"]
    W.draw_frame(0.066, guys=[(F[1], "wall"), (F[2], "wall"), (F[3], "wall"), (F[1], (17.9, 0.0)),
                              (F[3], (0.0, -17.85))])
    S = W.S
    # drooping clumps: 2-3 strands twisted into a loose rope, sagging under their own weight
    clumps = [((12.0, -1.6), (16.6, -7.2), 1.6, 3), ((4.4, -4.2), (11.8, -3.8), 2.3, 3),
              ((0.0, -6.0), (4.6, -12.4), 1.4, 2), ((7.0, -14.9), (12.6, -12.0), 1.0, 2),
              ((13.2, -5.0), (15.6, -11.0), 1.2, 2)]
    for a2, b2, droop, nstr in clumps:
        A, B = W.to3(*a2), W.to3(*b2)
        L = (B - A).length
        n = max(10, int(L / 0.28))
        cen = []
        for i in range(n + 1):
            t = i / n
            s = (math.cosh(2.0 * (t - 0.5)) - math.cosh(1.0)) / (1 - math.cosh(1.0))
            cen.append(A.lerp(B, t) + Vector((0, 0.18 * s, -droop * s)))
        ph0 = rng.uniform(0, 6.28)
        for sidx in range(nstr):
            pts = []
            for i, c in enumerate(cen):
                t = i / n
                T = (cen[min(n, i + 1)] - cen[max(0, i - 1)]).normalized()
                Nn = Vector((0, 1, 0)) - T * T.y
                Nn.normalize()
                Bn = T.cross(Nn)
                a = ph0 + sidx * 2 * math.pi / nstr + t * L * 3.2
                rad = 0.065 * math.sin(math.pi * t) ** 0.5
                pts.append(c + (Nn * math.cos(a) + Bn * math.sin(a)) * rad)
            S.tube(pts, 0.04, 3)
    # long single strands sagging from the frame, and a snapped bundle hanging free
    for a2, droop in (((16.6, -3.0), 2.4), ((10.6, -13.3), 1.6), ((1.5, -15.5), 1.2)):
        p0 = W.to3(*a2)
        S.tube(hanging(p0, Vector((-0.4, 0.1, -1)), droop, 9, rng), 0.035, 3)
    p0 = W.to3(8.6, -3.5)
    for j in range(3):
        S.tube(hanging(p0 + Vector((0.04 * j, 0, 0)), Vector((0.3 - 0.2 * j, 0.1, -1)), 2.6 - 0.4 * j, 11, rng),
               0.034, 3)
    # tangle threads: slack criss-cross silk near the corner and along the wall edges (old cobweb mess)
    for _ in range(12):
        if rng.random() < 0.5:
            a2 = (rng.uniform(0.0, 0.3), rng.uniform(-9.0, -1.0))          # from the pillar
        else:
            a2 = (rng.uniform(1.0, 10.0), rng.uniform(-0.3, 0.0))          # from the trim
        ang = rng.uniform(0, 2 * math.pi)
        ln = rng.uniform(2.0, 5.0)
        b2 = (min(16.0, max(0.4, a2[0] + abs(math.cos(ang)) * ln)), max(-16.0, min(-0.4, a2[1] - abs(math.sin(ang)) * ln)))
        A, B = W.to3(*a2), W.to3(*b2)
        L = (B - A).length
        n = max(5, int(L / 0.5))
        dr = rng.uniform(0.12, 0.35) * L
        pts = []
        for i in range(n + 1):
            t = i / n
            sg = (math.cosh(2.0 * (t - 0.5)) - math.cosh(1.0)) / (1 - math.cosh(1.0))
            pts.append(A.lerp(B, t) + Vector((0, 0.1 * sg, -dr * sg)))
        S.tube(pts, 0.03, 3)
    # wrapped prey
    W.cocoon(W.ringpts[5][7] or (11.0, -9.0), 0.4, 0.75, 0.2, seed=8)
    W.cocoon(W.ringpts[9][3] or (12.0, -4.0), 0.55, 0.55, 0.15, seed=9)
    R = 19.0
    ob = W.S.to_object("SpiderWeb_Torn", lambda co: (min(1, max(0, co.x / R)), min(1, max(0, 1 + co.z / R))))
    ci, ri = strand_maps("WebTorn", 256, 29, base=(206, 202, 194), dust=(148, 138, 122), bright=(236, 234, 228),
                         dusty=1.0, rough_lo=0.55, rough_hi=0.85)
    ob.data.materials.append(mat_tex("WebTorn_Mat", ci, ri))
    silk = build_silk(W)
    return ob, silk


# ---------------------------------------------------------------- dusty silk sheets (torn web)
def resample(pts, n):
    """Resample a 2D polyline to n+1 points evenly by length."""
    acc = [0.0]
    for i in range(1, len(pts)):
        acc.append(acc[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    out, j = [], 0
    for k in range(n + 1):
        s = acc[-1] * k / n
        while j < len(acc) - 2 and acc[j + 1] < s:
            j += 1
        t = (s - acc[j]) / max(1e-9, acc[j + 1] - acc[j])
        out.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * t, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * t))
    return out


def build_silk(W):
    rng = random.Random(41)
    bm = bmesh.new()
    uvs = []
    # (top curve 2D, hang length, nu, nv, island, hole threshold, bulge, fold, gather)
    sheets = [
        (sag2((5.6, -2.9), (11.2, -5.4), 12, (0.0, -0.9)), 3.0, 13, 9, 0, 9.0, 0.35, 0.22, 0.3),
        (sag2((0.0, -2.6), (3.3, -3.3), 8, (0.0, -0.4)), 3.6, 8, 9, 1, 9.0, 0.25, 0.16, 0.35),
        (sag2((14.9, -2.6), (16.7, -4.6), 6, (0.0, -0.3)), 3.1, 6, 9, 2, 9.0, 0.3, 0.18, 0.4),
    ]
    for top2, length, nu, nv, isl, thr, bulge, fold, gather in sheets:
        silk_sheet(W, bm, uvs, resample(top2, nu), length, nu, nv, isl, thr, bulge, fold, gather, rng)
    # the dense old silk filling the very corner (island 3): a curved triangle tied to the pillar and the trim
    corner_mat(W, bm, uvs, rng)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new("SpiderWeb_Torn_Silk")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    set_uvs(me, uvs)
    ob = link(bpy.data.objects.new("SpiderWeb_Torn_Silk", me))
    img = silk_map()
    ob.data.materials.append(mat_tex("WebSilk_Mat", img, None, alpha=True))
    ob.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
    return ob


def _two_sided(bm, uvs, grid, faces_idx, uvgrid):
    """grid: 2D list of Vectors. faces_idx: list of (i, j) quads to keep. Front faces +Y, plus a back copy."""
    rows, cols = len(grid), len(grid[0])
    front = [[None] * cols for _ in range(rows)]
    back = [[None] * cols for _ in range(rows)]
    used = set()
    for i, j in faces_idx:
        used |= {(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)}
    for (i, j) in sorted(used):
        front[i][j] = bm.verts.new(grid[i][j])
        uvs.append(uvgrid[i][j])
    for (i, j) in sorted(used):
        back[i][j] = bm.verts.new(grid[i][j])
        uvs.append(uvgrid[i][j])
    # orientation: make the front face +Y
    i0, j0 = faces_idx[0]
    a, b, c = grid[i0][j0], grid[i0][j0 + 1], grid[i0 + 1][j0]
    flip = (b - a).cross(c - a).y < 0
    for i, j in faces_idx:
        q = [front[i][j], front[i][j + 1], front[i + 1][j + 1], front[i + 1][j]]
        if flip:
            q.reverse()
        bm.faces.new(q)
        qb = [back[i][j], back[i][j + 1], back[i + 1][j + 1], back[i + 1][j]]
        if not flip:
            qb.reverse()
        bm.faces.new(qb)


def silk_sheet(W, bm, uvs, top2, length, nu, nv, island, thr, bulge, fold, gather, rng):
    seed = rng.uniform(0, 100)
    top3 = [W.to3(x, z) + Vector((0, 0.04, 0)) for x, z in top2]
    xc = sum(p.x for p in top3) / len(top3)
    Ls = []
    for j in range(nu + 1):
        u = j / nu
        L = length * (0.42 + 0.58 * math.sin(math.pi * (0.08 + 0.84 * u)) ** 0.8)
        L *= 0.78 + 0.44 * (0.5 + 0.5 * noise.noise(Vector((u * 3.3, seed, 0.5))))
        Ls.append(L)
    for _ in range(2):   # tattered strips hanging lower
        j = rng.randint(1, nu - 1)
        for dj, f in ((0, 1.55), (-1, 1.2), (1, 1.2)):
            if 0 <= j + dj <= nu:
                Ls[j + dj] *= f
    grid, uvg = [], []
    ox, oy = (island % 2) * 0.5, (island // 2) * 0.5
    for i in range(nv + 1):
        v = i / nv
        row, urow = [], []
        for j in range(nu + 1):
            u = j / nu
            p = top3[j].copy()
            L = Ls[j]
            p.z -= v * L
            p.x = xc + (p.x - xc) * (1 - gather * v)
            p.x += fold * 0.6 * math.sin(2 * math.pi * (v * 1.1 + u * 0.7) + seed) * v
            p.y += bulge * math.sin(math.pi * min(1.0, v * 1.2)) * (0.5 + 0.5 * math.sin(math.pi * u)) \
                + fold * math.sin(2 * math.pi * (u * 2.6 + v * 0.4) + seed) * (0.25 + v)
            row.append(p)
            urow.append((ox + 0.5 * (0.03 + 0.94 * u), oy + 0.5 * (0.03 + 0.94 * (1 - v))))
        grid.append(row)
        uvg.append(urow)
    keep = []
    for i in range(nv):
        for j in range(nu):
            u, v = (j + 0.5) / nu, (i + 0.5) / nv
            h = noise.noise(Vector((u * 2.4 + seed, v * 2.4 * length / 3.0, 1.1)))
            if i > 0 and h > thr:
                continue
            keep.append((i, j))
    _two_sided(bm, uvs, grid, keep, uvg)


def corner_mat(W, bm, uvs, rng):
    """The dense old silk in the very corner: a quad patch tied to the pillar and the trim, its two outer edges
    sagging in toward the corner; it sits behind the strands. The alpha frays the outer edges."""
    n = 7
    grid, uvg = [], []
    for i in range(n + 1):
        row, urow = [], []
        for j in range(n + 1):
            a, b = i / n, j / n          # a along the pillar (down), b along the trim (right)
            x = 3.6 * b * (1 - 0.58 * a)
            z = -3.6 * a * (1 - 0.58 * b)
            p = W.to3(x, z)
            p.y += -0.13 + 0.1 * math.sin(math.pi * a) * math.sin(math.pi * b)
            p.z -= 0.3 * a * b
            row.append(p)
            urow.append((0.5 + 0.5 * (0.03 + 0.94 * b), 0.5 + 0.5 * (0.03 + 0.94 * (1 - a))))
        grid.append(row)
        uvg.append(urow)
    _two_sided(bm, uvs, grid, [(i, j) for i in range(n) for j in range(n)], uvg)


def silk_map(size=512):
    """RGBA fibre atlas, 4 islands (2x2): a gauzy film with torn organic holes, hanging fibres (some bridging the
    holes), crossing threads, dust patches. Islands 0-2 = hanging sheets (top = attachment), 3 = the corner mat."""
    rng = np.random.default_rng(5)
    n = size // 2
    atlas = np.zeros((size, size, 4), np.float32)
    uu = (np.arange(n) + 0.5) / n
    Uq, Vq = np.meshgrid(uu, uu)          # Vq 0 = bottom of the island = bottom of the sheet
    for isl in range(4):
        fib = np.zeros((n, n), np.float32)
        nfib = 520 if isl < 3 else 600
        for f in range(nfib):
            vertical = rng.random() < (0.7 if isl < 3 else 0.3)
            ang = (math.pi / 2 + rng.normal(0, 0.28)) if vertical else rng.uniform(0, math.pi)
            L = rng.uniform(30, 190)
            steps = int(L / 0.5)
            x, y = rng.uniform(0, n), rng.uniform(0, n)
            w = rng.uniform(0.25, 0.7)
            xs, ys = np.empty(steps), np.empty(steps)
            for st in range(steps):
                ang += rng.normal(0, 0.025)
                x += 0.5 * math.cos(ang)
                y += 0.5 * math.sin(ang)
                xs[st], ys[st] = x, y
            ok = (xs >= 0) & (xs < n - 1) & (ys >= 0) & (ys < n - 1)
            xs, ys = xs[ok], ys[ok]
            if len(xs) == 0:
                continue
            x0, y0 = np.floor(xs).astype(int), np.floor(ys).astype(int)
            fx, fy = xs - x0, ys - y0
            for dx, dy, ww in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy),
                               (1, 1, fx * fy)):
                np.add.at(fib, (y0 + dy, x0 + dx), ww * w)
        fib = np.clip(fib, 0, 1)
        sd = 100 + isl * 10
        film = 0.12 + 0.5 * mnoise(n, 3.0, sd, 4, aspect=(1.0, 0.45))        # streaky along the hang
        holes = mnoise(n, 3.4, sd + 1, 3)
        keep = np.clip((0.66 - holes) / 0.07, 0, 1)                             # torn openings
        film = film * keep
        fib = fib * (0.35 + 0.65 * keep)                                        # some fibres bridge the holes
        alpha = 1 - (1 - film) * (1 - fib)
        rag = mnoise(n, 7.0, sd + 2, 3)
        if isl < 3:
            edge = np.clip(np.minimum(Uq, 1 - Uq) / 0.13, 0, 1) * np.clip((Vq - 0.06 * rag) / 0.3, 0, 1)
        else:   # corner mat: tied along the pillar (u=0) and the trim (v=1); frays toward u=1 and v=0
            edge = np.clip((1 - Uq - 0.12 * rag) / 0.35, 0, 1) * np.clip((Vq - 0.12 * rag) / 0.35, 0, 1)
        alpha = np.clip(alpha * edge * 1.15, 0, 1)
        dust = np.clip((mnoise(n, 4.5, sd + 3, 4) - 0.45) * 2.2, 0, 1) * 0.7
        spk = (rng.random((n, n)) > 0.997).astype(np.float32)
        silk_c = np.array(srgb((228, 224, 216)))
        dust_c = np.array(srgb((150, 138, 120)))
        bright = np.array(srgb((248, 247, 244)))
        col = silk_c[None, None, :] * (1 - dust[..., None]) + dust_c[None, None, :] * dust[..., None]
        col = col * (1 - 0.5 * fib[..., None]) + bright[None, None, :] * 0.5 * fib[..., None]
        col = col * (1 - 0.35 * spk[..., None])
        oy, ox = (isl // 2) * n, (isl % 2) * n
        atlas[oy:oy + n, ox:ox + n, :3] = col
        atlas[oy:oy + n, ox:ox + n, 3] = alpha
    return make_image("WebSilk_albedo", atlas, "sRGB", os.path.join(MAPS, "WebSilk_albedo.png"))


def build_webs():
    fresh(8)
    t0 = time.time()
    corner = build_corner()
    torn, silk = build_torn()
    torn.location.x = 0  # same frame; kept at the origin (the renders move a copy)
    rep = {"SpiderWeb_Corner": tris_of(corner), "SpiderWeb_Torn": tris_of(torn),
           "SpiderWeb_Torn_Silk": tris_of(silk)}
    for ob in (corner, torn, silk):
        bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
        rep[ob.name + "_bbox"] = [[round(min(v[i] for v in bb), 3) for i in range(3)],
                                  [round(max(v[i] for v in bb), 3) for i in range(3)]]
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_WEBS)
    rep["s"] = round(time.time() - t0, 1)
    return rep


def wall_set(span, height, col=(104, 98, 92)):
    """Stand-in for the hub wall bay: wall at y=-0.3, pillar side at x=0 (pillar x<0), top trim z>0."""
    m = mat_noise("Stone", lin(col), lin(tuple(int(c * 0.82) for c in col)), nscale=1.2, detail=4, rough=0.85,
                  lo=0.3, hi=0.7)
    m2 = mat_noise("Trim", lin((84, 70, 62)), lin((66, 54, 48)), nscale=1.5, detail=3, rough=0.8)
    objs = []
    for nm, mn, mx, mat in (("Wall", (-4, -1.3, -height), (span, -0.3, 2.0), m),
                            ("Pillar", (-4, -1.3, -height), (0.0, 2.6, 2.0), m2),
                            ("Trim", (-4, -1.3, 0.0), (span, 1.6, 2.0), m2)):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co = Vector(tuple(mn[i] + (v.co[i] + 0.5) * (mx[i] - mn[i]) for i in range(3)))
        o = obj_from_bm(bm, nm, smooth=False)
        o.data.materials.append(mat)
        objs.append(o)
    return objs


def front_sun(sc, energy=3.5):
    sun = bpy.data.objects.get("Sun")
    if sun:
        sun.rotation_euler = (math.radians(-48), 0, math.radians(24))   # light travels toward -Y and down
        sun.data.energy = energy
    return sc


def render_webs():
    bpy.ops.wm.open_mainfile(filepath=BLEND_WEBS)
    sc = review_setup()
    front_sun(sc)
    sc.eevee.taa_render_samples = 64
    out = []
    corner = bpy.data.objects["SpiderWeb_Corner"]
    torn = bpy.data.objects["SpiderWeb_Torn"]
    silk = bpy.data.objects["SpiderWeb_Torn_Silk"]
    # 1) plain sky background, both webs side by side (torn moved 16 studs right for the shot)
    torn.location.x = silk.location.x = 16.0
    out.append(shoot_fov(os.path.join(OUT, "review_webs_sky_30.png"), (17, 30, -12), (16, 0, -9), vfov=70,
                         res=(1400, 1000)))
    # 2) in context: a wall bay, seen from the hub floor ~30 studs away (eye 18 studs below the trim)
    torn.location.x = silk.location.x = 0.0
    walls = wall_set(24, 26)
    torn.hide_render = silk.hide_render = True
    out.append(shoot_fov(os.path.join(OUT, "review_corner_wall_30.png"), (9, 28, -19), (6.0, 0, -6.5), vfov=70))
    out.append(shoot_fov(os.path.join(OUT, "review_corner_close.png"), (4.5, 7.5, -6.5), (3.6, 0, -3.6),
                         lens=35))
    torn.hide_render = silk.hide_render = False
    corner.hide_render = True
    out.append(shoot_fov(os.path.join(OUT, "review_torn_wall_30.png"), (12, 28, -24), (8.0, 0, -8.5), vfov=70))
    out.append(shoot_fov(os.path.join(OUT, "review_torn_close.png"), (8.0, 9.0, -9.5), (6.5, 0, -6.0), lens=35))
    out.append(shoot_fov(os.path.join(OUT, "review_webs_60.png"), (10, 55, -30), (8, 0, -8), vfov=70))
    return out


def mirrored_copy(ob, name):
    """Roblox cannot mirror a MeshPart (no negative size) and a 90-degree turn would make the sag / hanging strands
    / silk fall sideways, so the other-hand corner is a real mirrored mesh: x -> -x, faces flipped, UVs kept."""
    me = ob.data.copy()
    me.name = name
    me.transform(Matrix.Scale(-1, 4, (1, 0, 0)))
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    o = link(bpy.data.objects.new(name, me))
    return o


def bbox_info(objs):
    vs = [o.matrix_world @ v.co for o in objs for v in o.data.vertices]
    mn = Vector(tuple(min(v[i] for v in vs) for i in range(3)))
    mx = Vector(tuple(max(v[i] for v in vs) for i in range(3)))
    return mn, mx


def export_webs():
    bpy.ops.wm.open_mainfile(filepath=BLEND_WEBS)
    o = bpy.data.objects
    out, info = [], {}
    sets = {"Halloween_SpiderWeb_Corner": [o["SpiderWeb_Corner"]],
            "Halloween_SpiderWeb_Torn": [o["SpiderWeb_Torn"], o["SpiderWeb_Torn_Silk"]]}
    for fname, objs in list(sets.items()):
        sets[fname + "_Mirror"] = [mirrored_copy(ob, ob.name.replace("SpiderWeb_Corner", "SpiderWeb_Corner_Mirror")
                                                 .replace("SpiderWeb_Torn", "SpiderWeb_Torn_Mirror")) for ob in objs]
    for fname, objs in sets.items():
        out.append(export_fbx(objs, os.path.join(CDIMP, fname + ".fbx")))
        for ob in objs:
            mn, mx = bbox_info([ob])
            info[ob.name] = {"min": [round(v, 3) for v in mn], "max": [round(v, 3) for v in mx],
                             "centre": [round((mn[i] + mx[i]) / 2, 3) for i in range(3)],
                             "size": [round(mx[i] - mn[i], 3) for i in range(3)], "tris": tris_of(ob)}
    with open(os.path.join(OUT, "webs_report.json"), "w") as fh:
        json.dump(info, fh, indent=1)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_WEBS)
    return out


# ================================================================== SPIDER
# Build frame: +X = forward (head), +Y = the spider's left, +Z = dorsal (up). hang_matrix() turns it into the hanging
# pose: head down, abdomen up (spinnerets at the top), dorsal side facing +Y (the hub), tilted 15 deg to face down.
# The game mesh carries its own UVs made at build time (one cylindrical island per leg segment / tube, the body blobs
# unwrapped around their long axis with the seam on the belly) and shelf-packed with a texel priority (abdomen, head
# and jaws get more pixels than the hidden coxae and spines).
SPC = dict(CX=0.55, CA=0.6, CB=0.47, CCt=0.29, CCb=0.17, AX=-0.9, AA=0.95, AB=0.74, AC=0.64, AZ=0.2)
COL = dict(body=lin((40, 23, 50)), body2=lin((84, 50, 108)), ink=lin((13, 8, 16)), hair=lin((150, 128, 166)),
           orange=lin((242, 112, 18)), orange2=lin((255, 178, 66)), orange_dim=lin((178, 86, 28)),
           band=lin((132, 58, 22)), eye=lin((30, 3, 6)), eye2=lin((150, 18, 26)), fang=lin((20, 8, 11)),
           fangtip=lin((206, 78, 40)), under=lin((54, 36, 44)), clyp=lin((30, 15, 30)), spine=lin((70, 54, 64)),
           jaw=lin((92, 28, 32)))
CHEV = [(0.42, 0.52), (0.06, 0.46), (-0.29, 0.37), (-0.6, 0.26)]


class MB:
    """bmesh + per-vertex colour / roughness (vertex creation order = mesh vertex order) + optional UV islands."""

    def __init__(self, uv=False):
        self.bm = bmesh.new()
        self.cols, self.rgh = [], []
        self.uvl = self.bm.loops.layers.uv.new("UVMap") if uv else None
        self.islands = []

    def v(self, co, col=(0.5, 0.5, 0.5), r=0.5):
        self.cols.append(tuple(col)[:3])
        self.rgh.append((r, r, r))
        return self.bm.verts.new(co)

    def island(self, pri=1.0):
        isl = {"pri": pri, "faces": []}
        if self.uvl is not None:
            self.islands.append(isl)
        return isl

    def f(self, vs, uvs=None, isl=None):
        face = self.bm.faces.new(vs)
        if self.uvl is not None and uvs is not None and isl is not None:
            for lp, uv in zip(face.loops, uvs):
                lp[self.uvl].uv = uv
            isl["faces"].append(face)
        return face

    def prep_uv(self):
        """Each island: local UVs (studs) x priority, moved to the origin; Blender's packer places them later."""
        uvl = self.uvl
        for isl in self.islands:
            if not isl["faces"]:
                continue
            us = [lp[uvl].uv.copy() for f in isl["faces"] for lp in f.loops]
            u0, v0 = min(u.x for u in us), min(u.y for u in us)
            k = isl["pri"]
            for f in isl["faces"]:
                for lp in f.loops:
                    u, v = lp[uvl].uv
                    lp[uvl].uv = ((u - u0) * k * 0.05, (v - v0) * k * 0.05)

    def obj(self, name, smooth=True):
        me = bpy.data.meshes.new(name)
        self.bm.to_mesh(me)
        self.bm.free()
        set_colors(me, "Col", self.cols)
        set_colors(me, "Rough", self.rgh)
        for p in me.polygons:
            p.use_smooth = smooth
        return link(bpy.data.objects.new(name, me))


def soften_normal(img, path, passes=1):
    """Binomial 3x3 blur of the tangent-space XY + renormalise: the 1-2 px hair ridges stop glittering up close
    (and alias less in Roblox) while the combed streaks stay."""
    w, h = img.size
    a = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)
    n = a[..., :3] * 2 - 1
    for _ in range(passes):
        for ax in (0, 1):
            n = (np.roll(n, 1, ax) + 2 * n + np.roll(n, -1, ax)) / 4
    n /= np.maximum(1e-6, np.linalg.norm(n, axis=2, keepdims=True))
    a[..., :3] = n * 0.5 + 0.5
    img.pixels.foreach_set(a.ravel())
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()


def blender_pack(ob, margin=0.006):
    only(ob)
    bpy.context.scene.tool_settings.use_uv_select_sync = True
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    try:
        bpy.ops.uv.pack_islands(rotate=True, margin=margin, shape_method="CONCAVE")
    except TypeError:
        bpy.ops.uv.pack_islands(rotate=True, margin=margin)
    bpy.ops.object.mode_set(mode="OBJECT")
    me = ob.data
    uv = me.uv_layers.active.data
    a_uv = a_3d = 0.0
    for poly in me.polygons:
        lps = list(poly.loop_indices)
        p0 = uv[lps[0]].uv
        for i in range(1, len(lps) - 1):
            p1, p2 = uv[lps[i]].uv, uv[lps[i + 1]].uv
            a_uv += abs((p1.x - p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * (p1.y - p0.y)) / 2
        a_3d += poly.area
    return math.sqrt(a_uv / max(1e-9, a_3d))


def axial_blob(B, nu, nv, fn, pri=1.0):
    """Closed shell, poles on +X (front) and -X (rear). fn(d) -> (pos, col, rough) for a unit direction d.
    UVs: unwrapped around the X axis, the dorsal midline in the middle of the island, the seam on the belly."""
    def dv(th, ph):
        return Vector((math.cos(th), math.sin(th) * math.sin(ph), math.sin(th) * math.cos(ph)))
    vf = B.v(*fn(Vector((1, 0, 0))))
    rings = []
    for i in range(1, nv):
        th = math.pi * i / nv
        rings.append([B.v(*fn(dv(th, 2 * math.pi * j / nu))) for j in range(nu)])
    vr = B.v(*fn(Vector((-1, 0, 0))))
    circ = max(sum((r[j].co - r[(j + 1) % nu].co).length for j in range(nu)) for r in rings)

    def merid(j):
        return ((rings[0][j].co - vf.co).length + (vr.co - rings[-1][j].co).length
                + sum((rings[i + 1][j].co - rings[i][j].co).length for i in range(nv - 2)))
    mer = 0.5 * (merid(0) + merid(nu // 4))
    isl = B.island(pri)
    fs = []
    for j in range(nu):
        k = (j + 1) % nu
        U = ((j / nu) + 0.5) % 1.0
        a, b = U * circ, (U + 1.0 / nu) * circ
        fs.append(B.f((vf, rings[0][j], rings[0][k]), [((a + b) / 2, 0.0), (a, mer / nv), (b, mer / nv)], isl))
        for i in range(nv - 2):
            fs.append(B.f((rings[i][j], rings[i + 1][j], rings[i + 1][k], rings[i][k]),
                          [(a, (i + 1) * mer / nv), (a, (i + 2) * mer / nv), (b, (i + 2) * mer / nv),
                           (b, (i + 1) * mer / nv)], isl))
        fs.append(B.f((rings[-1][k], rings[-1][j], vr),
                      [(b, (nv - 1) * mer / nv), (a, (nv - 1) * mer / nv), ((a + b) / 2, mer)], isl))
    bmesh.ops.recalc_face_normals(B.bm, faces=fs)
    return fs


def seg_tube(B, a, b, rfn, sides, ts, cfn, up, bow=0.0, cap=(0.5, 0.5), oval=1.0, pri=1.0):
    """Closed tube a->b; rfn(t, ang) radius, cfn(t, ang) -> (col, rough); ts = ring parameters 0..1.
    Returns (point(t, ang) -> (pos, normal, tangent), faces). UVs: one cylindrical island."""
    L = (b - a).length
    N0 = up - (b - a).normalized() * up.dot((b - a).normalized())
    N0.normalize()

    def centre(t):
        return a + (b - a) * t + N0 * (bow * L * 4 * t * (1 - t))

    def frame(t):
        T = ((b - a) + N0 * (bow * L * 4 * (1 - 2 * t))).normalized()
        N = N0 - T * N0.dot(T)
        N.normalize()
        return T, N, T.cross(N)

    def point(t, ang):
        T, N, Bv = frame(t)
        r = rfn(t, ang)
        pos = centre(t) + (N * math.cos(ang) * oval + Bv * math.sin(ang)) * r
        return pos, (N * math.cos(ang) / oval + Bv * math.sin(ang)).normalized(), T

    rings = []
    for t in ts:
        ring = []
        for j in range(sides):
            ang = 2 * math.pi * j / sides
            p, n, T = point(t, ang)
            c, r = cfn(t, ang)
            ring.append(B.v(p, c, r))
        rings.append(ring)
    circ = 2 * math.pi * 0.5 * (rfn(0.25, 0.0) + rfn(0.75, 0.0)) * (1 + oval) / 2
    isl = B.island(pri)
    us = [circ * j / sides for j in range(sides + 1)]
    fs = []
    for i in range(len(ts) - 1):
        for j in range(sides):
            k = (j + 1) % sides
            fs.append(B.f((rings[i][j], rings[i][k], rings[i + 1][k], rings[i + 1][j]),
                          [(us[j], ts[i] * L), (us[j + 1], ts[i] * L), (us[j + 1], ts[i + 1] * L),
                           (us[j], ts[i + 1] * L)], isl))
    T, N, Bv = frame(0.0)
    c0 = rfn(0.0, 0.0) * cap[0]
    v0 = B.v(centre(0.0) - T * c0, *cfn(0.0, 0.0))
    T, N, Bv = frame(1.0)
    c1 = rfn(1.0, 0.0) * cap[1]
    v1 = B.v(centre(1.0) + T * c1, *cfn(1.0, 0.0))
    for j in range(sides):
        k = (j + 1) % sides
        um = (us[j] + us[j + 1]) / 2
        fs.append(B.f((rings[0][k], rings[0][j], v0), [(us[j + 1], 0.0), (us[j], 0.0), (um, -c0)], isl))
        fs.append(B.f((rings[-1][j], rings[-1][k], v1), [(us[j], L), (us[j + 1], L), (um, L + c1)], isl))
    bmesh.ops.recalc_face_normals(B.bm, faces=fs)
    return point, fs


def path_tube(B, pts, radii, sides, cfn, up=Vector((0, 0, 1)), pri=1.0):
    """Closed tube along a polyline; the last radius may be ~0 (a point). cfn(t, ang) -> (col, rough)."""
    n = len(pts)
    T = [(pts[min(n - 1, i + 1)] - pts[max(0, i - 1)]).normalized() for i in range(n)]
    N = up - T[0] * up.dot(T[0])
    N.normalize()
    rings = []
    for i in range(n):
        N = N - T[i] * N.dot(T[i])
        N.normalize()
        Bv = T[i].cross(N)
        t = i / (n - 1)
        rings.append([B.v(pts[i] + (N * math.cos(2 * math.pi * j / sides) + Bv * math.sin(2 * math.pi * j / sides))
                          * max(radii[i], 1e-4), *cfn(t, 2 * math.pi * j / sides)) for j in range(sides)])
    vs = [0.0]
    for i in range(1, n):
        vs.append(vs[-1] + (pts[i] - pts[i - 1]).length)
    circ = 2 * math.pi * radii[0]
    us = [circ * j / sides for j in range(sides + 1)]
    isl = B.island(pri)
    fs = []
    for i in range(n - 1):
        for j in range(sides):
            k = (j + 1) % sides
            fs.append(B.f((rings[i][j], rings[i][k], rings[i + 1][k], rings[i + 1][j]),
                          [(us[j], vs[i]), (us[j + 1], vs[i]), (us[j + 1], vs[i + 1]), (us[j], vs[i + 1])], isl))
    v0 = B.v(pts[0] - T[0] * radii[0] * 0.4, *cfn(0.0, 0.0))
    v1 = B.v(pts[-1] + T[-1] * max(radii[-1], 0.004), *cfn(1.0, 0.0))
    for j in range(sides):
        k = (j + 1) % sides
        um = (us[j] + us[j + 1]) / 2
        fs.append(B.f((rings[0][k], rings[0][j], v0), [(us[j + 1], 0.0), (us[j], 0.0), (um, -radii[0] * 0.4)], isl))
        fs.append(B.f((rings[-1][j], rings[-1][k], v1), [(us[j], vs[-1]), (us[j + 1], vs[-1]), (um, vs[-1] + 0.01)],
                      isl))
    bmesh.ops.recalc_face_normals(B.bm, faces=fs)
    return fs


def hair(B, p, n, comb, L, rb, el, col0, col1, r0=0.55, r1=0.7, sides=3, sink=0.5, pri=0.5):
    """A thin cone leaning along `comb` at elevation el (radians) above the surface."""
    t = comb - n * comb.dot(n)
    if t.length < 1e-6:
        t = n.orthogonal()
    t.normalize()
    D = (t * math.cos(el) + n * math.sin(el)).normalized()
    N = n - D * n.dot(D)
    if N.length < 1e-6:
        N = D.orthogonal()
    N.normalize()
    Bv = D.cross(N)
    base = p - n * rb * sink
    ring = [B.v(base + (N * math.cos(2 * math.pi * j / sides) + Bv * math.sin(2 * math.pi * j / sides)) * rb,
                col0, r0) for j in range(sides)]
    tip = B.v(base + D * L, col1, r1)
    isl = B.island(pri) if B.uvl is not None else None
    circ = 2 * math.pi * rb
    for j in range(sides):
        B.f((ring[j], ring[(j + 1) % sides], tip),
            [(circ * j / sides, 0.0), (circ * (j + 1) / sides, 0.0), (circ * (j + 0.5) / sides, L)], isl)


def scatter(B, faces, count, rng, fn):
    """Calls fn(p, n, col) at `count` area-weighted random points on `faces`."""
    B.bm.normal_update()
    B.bm.verts.index_update()
    areas = np.array([f.calc_area() for f in faces])
    cum = np.cumsum(areas)
    tot = cum[-1]
    pts = []
    for _ in range(count):
        f = faces[min(len(faces) - 1, int(np.searchsorted(cum, rng.random() * tot)))]
        vs = f.verts
        tri = (vs[0], vs[2], vs[3]) if (len(vs) == 4 and rng.random() < 0.5) else (vs[0], vs[1], vs[2])
        r1, r2 = rng.random(), rng.random()
        if r1 + r2 > 1:
            r1, r2 = 1 - r1, 1 - r2
        p = tri[0].co + (tri[1].co - tri[0].co) * r1 + (tri[2].co - tri[0].co) * r2
        c0, c1, c2 = (Vector(B.cols[v.index]) for v in tri)
        pts.append((p.copy(), f.normal.copy(), tuple(c0 + (c1 - c0) * r1 + (c2 - c0) * r2)))
    for p, n, col in pts:
        fn(p, n, col)


def lighten(col, k):
    """Hair tip colour: dark areas -> purple-grey, orange areas -> pale orange (subtle: the fur, not speckle)."""
    lum = 0.3 * col[0] + 0.6 * col[1] + 0.1 * col[2]
    if col[0] > 2.5 * col[2] and lum > 0.08:
        return mix(col, COL["orange2"], k)
    return mix(col, COL["hair"], k)


# ---------------------------------------------------------------- body parts
def ceph_fn(q):
    off = Vector((3.1, 7.7, 1.9))

    def fn(d):
        x, y, z = d.x, d.y, d.z
        s = x
        halfw = SPC["CB"] * (1 - 0.30 * smoothstep(0.05, 1.0, s)) * (1 - 0.12 * smoothstep(-0.5, -1.0, s))
        hz = SPC["CCt"] if z >= 0 else SPC["CCb"]
        px = SPC["CX"] + SPC["CA"] * x
        py = halfw * y
        pz = hz * z
        if z > 0:
            pz += 0.10 * smoothstep(-0.2, 0.75, s) * z ** 1.2           # the raised head region
        fx = SPC["CX"] - 0.14
        rr = math.hypot(px - fx, py)
        phi = math.atan2(py, px - fx)
        groove = 0.0
        if z > 0.15:
            w = smoothstep(0.15, 0.45, z)
            pz -= w * 0.045 * math.exp(-(rr / 0.055) ** 2)              # fovea
            groove = (0.5 + 0.5 * math.cos(8 * phi)) ** 8 * smoothstep(0.07, 0.16, rr) \
                * smoothstep(0.42, 0.24, rr) * w                          # radial striae
            pz -= 0.018 * groove
        p = Vector((px, py, pz))
        if q:
            p += d * 0.004 * fbm(p * 30 + off, 2)
        col = COL["body"]
        col = mix(col, COL["body2"], 0.4 * max(0.0, z) * smoothstep(-0.1, 0.5, fbm(p * 5 + off, 2)))
        col = mix(col, COL["ink"], 0.6 * groove)
        marg = math.exp(-(z / 0.3) ** 2) * smoothstep(0.62, 0.4, s)
        col = mix(col, lin((100, 78, 116)), 0.42 * marg)
        med = math.exp(-(py / 0.07) ** 2) * smoothstep(-0.6, 0.2, s) * smoothstep(0.65, 0.35, s) * smoothstep(0.3, 0.6, z)
        col = mix(col, COL["hair"], 0.28 * med)
        col = mix(col, COL["clyp"], smoothstep(0.55, 0.85, s) * (1 - smoothstep(0.35, 0.75, z)))   # dark clypeus
        if z < -0.25:
            col = mix(col, COL["under"], smoothstep(-0.25, -0.6, z))
        return p, col, 0.34 + 0.14 * marg + 0.1 * groove
    return fn


def abd_shape(d, q):
    x, y, z = d.x, d.y, d.z
    s = x
    wscale = 0.80 + 0.20 * math.exp(-((s - 0.2) / 0.65) ** 2)
    taper = 1 - 0.30 * smoothstep(-0.35, -1.0, s)
    hs = 1.0 if z >= 0 else 0.82
    p = Vector((SPC["AX"] + SPC["AA"] * x, SPC["AB"] * y * wscale * taper,
                SPC["AZ"] + SPC["AC"] * z * hs * taper * (0.92 + 0.08 * wscale)))
    for sgn in (1, -1):                                   # shoulder humps
        c = Vector((0.52, 0.42 * sgn, 0.74)).normalized()
        p += d * 0.09 * math.exp(-((d - c).length / 0.23) ** 2)
    for ss, ww in ((0.3, 0.17), (0.05, 0.2), (-0.2, 0.17), (-0.44, 0.13)):   # muscle sigilla (paired dimples)
        for sgn in (1, -1):
            c = Vector((ss, ww * sgn, math.sqrt(max(0.0, 1 - ss * ss - ww * ww)))).normalized()
            p -= d * 0.017 * math.exp(-((d - c).length / 0.055) ** 2)
    if q:
        p += d * 0.003 * fbm(p * 34 + Vector((5.5, 1.1, 9.3)), 2)
    return p


def abd_fn(q):
    off = Vector((9.1, 2.2, 4.4))

    def fn(d):
        p = abd_shape(d, q)
        s = d.x
        w = math.atan2(d.y, d.z) / (math.pi / 2)
        aw = abs(w)
        col = COL["body"]
        col = mix(col, COL["body2"], 0.38 * smoothstep(-0.1, 0.45, fbm(p * 6 + off, 3)))
        stri = (0.5 + 0.5 * math.sin(22 * (s * 0.9 + 0.3 * aw) + 2 * noise.noise(p * 3 + off))) ** 3
        col = mix(col, COL["hair"], 0.3 * stri * smoothstep(0.55, 0.85, aw) * smoothstep(1.45, 1.15, aw))
        # folium: a dark leaf down the back, outlined by a thin wavy rust line
        fw = 0.56 * (0.35 + 0.65 * smoothstep(-1.0, 0.3, s)) + 0.04 * math.sin(s * 28)
        col = mix(col, COL["ink"], 0.55 * smoothstep(fw + 0.1, fw - 0.05, aw))
        col = mix(col, COL["orange_dim"], 0.65 * smoothstep(0.04, 0.0, abs(aw - fw)) * smoothstep(-0.95, -0.6, s)
                  * smoothstep(0.85, 0.6, s))
        rgh = 0.4
        for sk, wm in CHEV:                                # bold nested orange chevrons, black rim behind each
            sl = sk - 0.72 * aw + 0.025 * noise.noise(p * 7 + off)
            dd = s - sl
            band = smoothstep(0.085, 0.052, abs(dd)) * smoothstep(wm, wm - 0.06, aw)
            rim = smoothstep(0.2, 0.1, abs(dd + 0.12)) * (1.0 if dd < 0 else 0.0) * smoothstep(wm + 0.06, wm - 0.04, aw)
            col = mix(col, COL["ink"], 0.75 * rim)
            col = mix(col, COL["orange"], band)
            col = mix(col, COL["orange2"], band * smoothstep(0.045, 0.0, abs(dd)) * 0.55)
            rgh = rgh + 0.1 * band
        for sgn in (1, -1):                                # shoulder spots on the humps
            ds = math.hypot(s - 0.55, (w - 0.47 * sgn) * 0.9)
            m = smoothstep(0.15, 0.1, ds)
            col = mix(col, COL["ink"], 0.6 * smoothstep(0.21, 0.15, ds) * (1 - m))
            col = mix(col, COL["orange"], m)
            col = mix(col, COL["orange2"], 0.5 * smoothstep(0.07, 0.0, ds))
        if d.z < -0.45:                                    # red-orange hourglass on the belly
            hg = smoothstep(0.03, 0.0, abs(d.y) - (0.05 + 0.55 * abs(s + 0.1))) * smoothstep(0.42, 0.36, abs(s + 0.1))
            col = mix(col, COL["under"], 0.5 * smoothstep(-0.45, -0.7, d.z))
            col = mix(col, lin((226, 70, 20)), hg * smoothstep(-0.55, -0.7, d.z))
        return p, col, rgh
    return fn


def ster_fn(d):
    p = Vector((SPC["CX"] - 0.02 + 0.36 * d.x, 0.27 * d.y, -0.15 + 0.07 * d.z))
    col = mix(COL["under"], lin((120, 96, 92)), 0.4 * math.exp(-(d.y / 0.2) ** 2) * max(0.0, -d.z))
    return p, col, 0.45


EYES = [((1.0, 0.21, 0.42), 0.072, True),     # AME
        ((0.62, 0.3, 0.8), 0.086, True),      # PME
        ((0.8, 0.62, 0.2), 0.05, False),      # ALE
        ((0.3, 0.88, 0.42), 0.046, False)]    # PLE


def eye_spots(ceph_bm):
    bvh = BVHTree.FromBMesh(ceph_bm)
    O = Vector((SPC["CX"] + 0.28, 0.0, 0.06))
    out = []
    for (dx, dy, dz), r, big in EYES:
        for side in (1, -1):
            d = Vector((dx, dy * side, dz)).normalized()
            hit, nrm, idx, dist = bvh.ray_cast(O, d, 3.0)
            if hit is None:
                continue
            n = (hit - O).normalized().lerp(nrm if nrm.dot(d) > 0 else -nrm, 0.6).normalized()
            out.append((hit - n * r * 0.38, n, r, big))
    return out


def eye_ball(B, c, n, r, nu, nv, pri=1.2):
    def fn(d):
        k = d.dot(n)
        col = mix(COL["eye2"], COL["eye"], smoothstep(0.1, 0.85, k))
        return c + d * r, col, 0.05
    top = B.v(*fn(n))
    T1 = n.orthogonal().normalized()
    T2 = n.cross(T1)
    rings = []
    for i in range(1, nv):
        th = math.pi * i / nv
        rings.append([B.v(*fn((n * math.cos(th) + (T1 * math.cos(2 * math.pi * j / nu)
                                                    + T2 * math.sin(2 * math.pi * j / nu)) * math.sin(th))))
                      for j in range(nu)])
    bot = B.v(*fn(-n))
    circ, mer = 2 * math.pi * r, math.pi * r
    isl = B.island(pri)
    fs = []
    for j in range(nu):
        k = (j + 1) % nu
        a, b = circ * j / nu, circ * (j + 1) / nu
        fs.append(B.f((top, rings[0][j], rings[0][k]), [((a + b) / 2, 0.0), (a, mer / nv), (b, mer / nv)], isl))
        for i in range(nv - 2):
            fs.append(B.f((rings[i][j], rings[i + 1][j], rings[i + 1][k], rings[i][k]),
                          [(a, (i + 1) * mer / nv), (a, (i + 2) * mer / nv), (b, (i + 2) * mer / nv),
                           (b, (i + 1) * mer / nv)], isl))
        fs.append(B.f((rings[-1][k], rings[-1][j], bot),
                      [(b, (nv - 1) * mer / nv), (a, (nv - 1) * mer / nv), ((a + b) / 2, mer)], isl))
    bmesh.ops.recalc_face_normals(B.bm, faces=fs)


# ---------------------------------------------------------------- legs
LEGS = [dict(az=24, el=46, bends=(36, 16, 12, 10), drift=(0, 0, 0, -4, -7, -8, -6), L=4.3, T=0.1, base=(0.31, 0.32)),
        dict(az=56, el=54, bends=(48, 22, 16, 12), drift=(0, 0, 0, -2, -3, -4, -3), L=3.9, T=0.096, base=(0.12, 0.38)),
        dict(az=106, el=64, bends=(72, 30, 22, 14), drift=(0, 0, 0, 3, 5, 6, 4), L=2.8, T=0.086, base=(-0.08, 0.385)),
        dict(az=146, el=50, bends=(54, 22, 16, 10), drift=(0, 0, 0, 4, 7, 9, 6), L=3.6, T=0.092, base=(-0.26, 0.32))]
# name, length fraction, r0, r1 (x leg thickness), game-mesh sides, game-mesh rings, texel priority
SEGS = [("coxa", 0.065, 1.15, 1.05, 10, [0, 0.5, 1], 0.5), ("troch", 0.045, 1.0, 0.95, 10, [0, 1], 0.5),
        ("femur", 0.27, 1.0, 0.86, 10, [0, 0.12, 0.4, 0.7, 0.9, 1], 1.0),
        ("patella", 0.10, 0.9, 0.84, 8, [0, 0.3, 0.75, 1], 1.0),
        ("tibia", 0.215, 0.84, 0.7, 10, [0, 0.12, 0.45, 0.8, 1], 1.0),
        ("meta", 0.195, 0.66, 0.52, 8, [0, 0.15, 0.6, 1], 0.9),
        ("tarsus", 0.11, 0.52, 0.3, 6, [0, 0.4, 0.8, 1], 0.85)]
SPINES = {"femur": [(0.3, 0.0), (0.55, 0.2), (0.8, -0.1), (0.45, 1.35), (0.72, 1.45)],
          "patella": [(0.5, 0.25), (0.6, -1.3)],
          "tibia": [(0.25, 1.15), (0.25, -1.15), (0.62, 1.2), (0.62, -1.2), (0.45, 0.1)],
          "meta": [(0.2, 1.05), (0.2, -1.05), (0.58, 1.1), (0.58, -1.1)]}


def leg_rfn(r0, r1, hi, kind):
    def f(t, ang):
        r = (r0 + (r1 - r0) * t) * (0.74 + 0.26 * smoothstep(0.0, 0.14, t))
        if kind != "tarsus":
            r *= 1 + 0.07 * math.exp(-((t - 0.9) / 0.06) ** 2)
        if hi:
            r *= 1 + 0.03 * math.cos(4 * ang + 0.6) * smoothstep(0.12, 0.3, t) * smoothstep(0.95, 0.8, t)
        return r
    return f


def leg_cfn(kind):
    def f(t, ang):
        dors = max(0.0, math.cos(ang))
        col = mix(COL["body"], COL["body2"], 0.35 * dors)
        a = ang if ang <= math.pi else ang - 2 * math.pi
        if kind in ("femur", "tibia"):                       # pale dorsal hair stripe
            col = mix(col, COL["hair"], 0.2 * math.exp(-(a / 0.32) ** 2) * smoothstep(0.1, 0.3, t)
                      * smoothstep(0.95, 0.75, t))
        band = 0.0
        if kind == "femur":
            band = smoothstep(0.5, 0.68, t) * (1 - smoothstep(0.86, 0.95, t))
        elif kind == "tibia":
            band = smoothstep(0.04, 0.14, t) * (1 - smoothstep(0.26, 0.38, t)) \
                + 0.8 * smoothstep(0.66, 0.78, t) * (1 - smoothstep(0.88, 0.96, t))
        elif kind == "meta":
            band = smoothstep(0.04, 0.14, t) * (1 - smoothstep(0.3, 0.42, t))
        elif kind == "patella":
            band = 0.35 * smoothstep(0.3, 0.5, t) * (1 - smoothstep(0.7, 0.9, t))
        col = mix(col, COL["band"], 0.8 * band * (0.75 + 0.25 * dors))
        if kind in ("coxa", "troch"):
            col = mix(COL["under"], COL["body"], 0.4)
        if t > 0.96 or t < 0.04:
            col = mix(col, COL["ink"], 0.5)
        if kind == "tarsus":
            col = mix(col, COL["ink"], smoothstep(0.6, 1.0, t))
        return col, 0.42 + 0.08 * band
    return f


def leg_chain(i, side, jit):
    P = LEGS[i]
    az0, el = P["az"] + jit[0], P["el"] + jit[1]
    pitches = [-28, 5, el, el - P["bends"][0], el - sum(P["bends"][:2]), el - sum(P["bends"][:3]), el - sum(P["bends"])]
    J = [Vector((SPC["CX"] + P["base"][0], side * P["base"][1], -0.08))]
    az = az0
    for k, seg in enumerate(SEGS):
        az += P["drift"][k] + (jit[2] if k >= 3 else 0)
        pt, a = math.radians(pitches[k]), math.radians(az)
        d = Vector((math.cos(pt) * math.cos(a), side * math.cos(pt) * math.sin(a), math.sin(pt)))
        J.append(J[-1] + d * P["L"] * seg[1])
    return J


def build_leg(B, i, side, jit, hi, rng_hair):
    P = LEGS[i]
    J = leg_chain(i, side, jit)
    rs = random.Random(1000 + i * 10 + (1 if side > 0 else 2))   # spines: identical on hi and lo
    for k, (name, frac, r0, r1, sides, ts, pri) in enumerate(SEGS):
        a, b = J[k], J[k + 1]
        d = (b - a).normalized()
        R0, R1 = r0 * P["T"], r1 * P["T"]
        a2 = a - d * (0.35 * R0 if k > 0 else 0.0)
        segL = (b - a2).length
        if hi:
            nts = max(16, int(segL / 0.012))
            tts = [t / nts for t in range(nts + 1)]
            nsd = 24
        else:
            tts, nsd = ts, sides
        bow = {"femur": 0.035, "tibia": 0.02, "meta": 0.015}.get(name, 0.0)
        cap = (0.5, 1.6) if name == "tarsus" else (0.5, 0.45)
        point, fs = seg_tube(B, a2, b, leg_rfn(R0, R1, hi, name), nsd, tts, leg_cfn(name), Vector((0, 0, 1)),
                             bow=bow, cap=cap, oval=0.92, pri=pri)
        cfn = leg_cfn(name)
        if hi and name not in ("coxa", "troch"):
            area = 2 * math.pi * (R0 + R1) / 2 * segL
            for _ in range(int(330 * area)):
                t, ang = rng_hair.uniform(0.06, 0.94), rng_hair.uniform(0, 2 * math.pi)
                p, n, T = point(t, ang)
                c0 = cfn(t, ang)[0]
                comb = T + n.cross(T) * rng_hair.uniform(-0.3, 0.3)
                hair(B, p, n, comb, rng_hair.uniform(1.0, 1.5) * P["T"], 0.011,
                     math.radians(rng_hair.uniform(5, 13)), c0, lighten(c0, 0.12), 0.6, 0.72, sink=0.35)
        for ts_, ang_ in SPINES.get(name, []):
            t = ts_ + rs.uniform(-0.05, 0.05)
            ang = ang_ * side + rs.uniform(-0.15, 0.15)
            Ls, el = rs.uniform(2.0, 2.7) * P["T"], math.radians(rs.uniform(38, 52))
            p, n, T = point(t, ang)
            hair(B, p, n, T, Ls, 0.19 * P["T"], el, COL["ink"], COL["spine"], 0.35, 0.4, sides=6 if hi else 3,
                 sink=0.8, pri=0.45)
    return J


def build_palp(B, side, hi, rng_hair):
    J = [Vector((SPC["CX"] + 0.36, side * 0.25, -0.12))]
    for (pt, az, ln) in ((28, 34, 0.3), (2, 26, 0.1), (-35, 16, 0.2), (-70, 8, 0.19)):
        p, a = math.radians(pt), math.radians(az)
        J.append(J[-1] + Vector((math.cos(p) * math.cos(a), side * math.cos(p) * math.sin(a), math.sin(p))) * ln)
    rr = [(0.06, 0.054), (0.054, 0.05), (0.05, 0.046), (0.046, 0.028)]
    for k in range(4):
        a, b = J[k], J[k + 1]
        d = (b - a).normalized()
        a2 = a - d * (0.3 * rr[k][0] if k else 0)
        kind = ("femur", "patella", "tibia", "tarsus")[k]
        if hi:
            nts = max(14, int((b - a2).length / 0.012))
            tts, nsd = [t / nts for t in range(nts + 1)], 20
        else:
            tts, nsd = [0, 0.5, 1] if k else [0, 0.35, 0.75, 1], 6
        point, fs = seg_tube(B, a2, b, leg_rfn(rr[k][0], rr[k][1], hi, kind), nsd, tts, leg_cfn(kind),
                             Vector((0, 0, 1)), cap=(0.5, 0.9 if k == 3 else 0.45), oval=0.95, pri=0.9)
        if hi:
            cfn = leg_cfn(kind)
            for _ in range(int(340 * 2 * math.pi * rr[k][0] * (b - a2).length)):
                t, ang = rng_hair.uniform(0.06, 0.94), rng_hair.uniform(0, 2 * math.pi)
                p, n, T = point(t, ang)
                c0 = cfn(t, ang)[0]
                hair(B, p, n, T, rng_hair.uniform(0.07, 0.11), 0.01, math.radians(rng_hair.uniform(6, 16)),
                     c0, lighten(c0, 0.18), 0.6, 0.72, sink=0.35)


def build_jaws(B, side, hi):
    """A chelicera (big, glossy dark red-black, bristled) with its curved fang, spread open."""
    a = Vector((SPC["CX"] + 0.5, side * 0.12, 0.0))
    dirc = Vector((0.56, side * 0.12, -0.82)).normalized()
    b = a + dirc * 0.54

    def rfn(t, ang):
        r = 0.14 * (1 - 0.3 * t) * (1 + 0.12 * math.exp(-((t - 0.28) / 0.2) ** 2))
        if hi:
            r *= 1 + 0.02 * math.cos(3 * ang)
        return r

    def cfn(t, ang):
        c = mix(COL["clyp"], COL["body2"], 0.25 * max(0.0, math.cos(ang)))
        c = mix(c, COL["jaw"], 0.75 * smoothstep(0.25, 1.0, t))
        return c, 0.2
    if hi:
        nts = 64
        tts, nsd = [t / nts for t in range(nts + 1)], 28
    else:
        tts, nsd = [0, 0.2, 0.5, 0.8, 1], 8
    point, fs = seg_tube(B, a, b, rfn, nsd, tts, cfn, Vector((1, 0, 0)), bow=0.06, cap=(0.3, 0.55), pri=1.3)
    # the fang: hooks down and inward, the tip curling back toward the mouth
    P0 = b - dirc * 0.04 + Vector((0.04, -side * 0.04, 0))
    P1 = P0 + Vector((0.14, -side * 0.09, -0.18))
    P2 = P0 + Vector((0.0, -side * 0.24, -0.33))
    n = 32 if hi else 6
    pts, rad = [], []
    for i in range(n + 1):
        t = i / n
        pts.append(P0 * (1 - t) ** 2 + P1 * 2 * (1 - t) * t + P2 * t * t)
        rad.append(0.056 * (1 - t) ** 0.85 + 0.0028)

    def fcol(t, ang):
        return mix(COL["fang"], COL["fangtip"], smoothstep(0.5, 1.0, t)), 0.1
    path_tube(B, pts, rad, 14 if hi else 6, fcol, up=Vector((1, 0, 0)), pri=1.3)
    return point, fs


def spinneret_pts():
    ds = Vector((-0.95, 0.0, -0.31)).normalized()
    base = abd_shape(ds, False)
    dirs = Vector((-0.86, 0.0, -0.51)).normalized()
    return base, dirs


def build_spinnerets(B, hi):
    base, dirs = spinneret_pts()
    tips = []
    for off, ln, rb in ((Vector((0, 0, 0)), 0.15, 0.04), (Vector((0.02, 0.05, -0.01)), 0.11, 0.03),
                        (Vector((0.02, -0.05, -0.01)), 0.11, 0.03)):
        a = base + off - dirs * 0.04
        b = a + dirs * ln
        nts = 12 if hi else 2
        seg_tube(B, a, b, lambda t, ang, rb=rb: rb * (1 - 0.55 * t), 12 if hi else 5,
                 [t / nts for t in range(nts + 1)], lambda t, ang: (mix(COL["under"], COL["ink"], t), 0.4),
                 Vector((0, 0, 1)), cap=(0.4, 0.6), pri=0.6)
        tips.append(b)
    return tips[0] + dirs * 0.04 * 0.6


def hang_matrix():
    return (Matrix.Rotation(math.radians(-15), 4, "X") @ Matrix.Rotation(math.radians(90), 4, "Z")
            @ Matrix.Rotation(math.radians(90), 4, "Y"))


LEG_JIT = {}


def leg_jit(i, side):
    if (i, side) not in LEG_JIT:
        r = random.Random(500 + i * 7 + (0 if side > 0 else 3))
        LEG_JIT[(i, side)] = (r.uniform(-5, 5), r.uniform(-6, 6), r.uniform(-1.5, 1.5)) if side < 0 else \
            (r.uniform(-2, 2), r.uniform(-2, 2), 0.0)
    return LEG_JIT[(i, side)]


def build_spider():
    fresh(24)
    t0 = time.time()
    rh = random.Random(78)
    # ---------- dense sculpt (4 objects)
    Bc = MB()
    fs_c = axial_blob(Bc, 160, 96, ceph_fn(True))
    eyes = eye_spots(Bc.bm)
    Bc.bm.verts.index_update()
    for v in Bc.bm.verts:          # dark sockets around every eye
        for c, n, r, big in eyes:
            dd = (v.co - c).length
            if dd < r * 1.9:
                Bc.cols[v.index] = mix(Bc.cols[v.index], COL["ink"], smoothstep(r * 1.9, r * 1.2, dd))
    scatter(Bc, fs_c, 520, rh, lambda p, n, col: hair(
        Bc, p, n, Vector((-1, 0, 0)) + Vector((0, p.y, 0)) * 2.0, rh.uniform(0.07, 0.11), 0.0105,
        math.radians(rh.uniform(4, 11)), col, lighten(col, 0.08), 0.55, 0.7, sink=0.35))
    for side in (1, -1):           # long setae over the eyes, pointing forward
        for k in range(5):
            p = Vector((SPC["CX"] + 0.44 + 0.03 * k, side * (0.03 + 0.04 * k), 0.24 - 0.02 * k))
            hair(Bc, p, Vector((0.2, 0, 1)).normalized(), Vector((1, side * 0.3, 0.4)), 0.13, 0.011,
                 math.radians(28), COL["ink"], COL["spine"], 0.4, 0.5, sides=6)
    axial_blob(Bc, 48, 24, ster_fn)
    ceph_hi = Bc.obj("Sp_Ceph_hi")
    Ba = MB()
    fs_a = axial_blob(Ba, 220, 140, abd_fn(True))
    scatter(Ba, fs_a, 1500, rh, lambda p, n, col: hair(
        Ba, p, n, Vector((-1, 0, -0.25)), rh.uniform(0.1, 0.16), 0.0125, math.radians(rh.uniform(3, 10)),
        col, lighten(col, 0.07), 0.55, 0.7, sink=0.35))
    attach = build_spinnerets(Ba, True)
    abd_hi = Ba.obj("Sp_Abd_hi")
    Bl = MB()
    for i in range(4):
        for side in (1, -1):
            build_leg(Bl, i, side, leg_jit(i, side), True, rh)
    for side in (1, -1):
        build_palp(Bl, side, True, rh)
    legs_hi = Bl.obj("Sp_Legs_hi")
    Bh = MB()
    for c, n, r, big in eyes:
        eye_ball(Bh, c, n, r, 32, 20)
    for side in (1, -1):
        point, fs = build_jaws(Bh, side, True)
        for _ in range(60):        # bristles on the front of the chelicerae
            t, ang = rh.uniform(0.05, 0.7), rh.uniform(-1.2, 1.2)
            p, n, T = point(t, ang)
            hair(Bh, p, n, -T, rh.uniform(0.07, 0.11), 0.01, math.radians(rh.uniform(10, 22)),
                 COL["clyp"], COL["spine"], 0.4, 0.55, sink=0.35)
    head_hi = Bh.obj("Sp_Head_hi")
    his = [ceph_hi, abd_hi, legs_hi, head_hi]
    for o in his:
        o.data.materials.append(mat_vc(o.name + "_M"))
    t1 = time.time()
    # ---------- the game mesh: the same functions at low resolution (one object, its own UV islands)
    L = MB(uv=True)
    axial_blob(L, 22, 14, ceph_fn(False), pri=1.35)
    axial_blob(L, 8, 4, ster_fn, pri=0.6)
    axial_blob(L, 30, 18, abd_fn(False), pri=1.45)
    build_spinnerets(L, False)
    for c, n, r, big in eyes:
        eye_ball(L, c, n, r, 8 if big else 6, 5 if big else 4)
    for side in (1, -1):
        build_jaws(L, side, False)
        build_palp(L, side, False, None)
    for i in range(4):
        for side in (1, -1):
            build_leg(L, i, side, leg_jit(i, side), False, None)
    L.prep_uv()
    bmesh.ops.triangulate(L.bm, faces=L.bm.faces[:])
    lo = L.obj("Spider")
    uv_per_stud = blender_pack(lo, 0.006)
    for a in list(lo.data.color_attributes):
        lo.data.color_attributes.remove(a)
    # ---------- hanging pose + centring
    M = hang_matrix()
    for o in his + [lo]:
        o.data.transform(M)
    attach_w = M @ attach
    bb = [v.co.copy() for v in lo.data.vertices]
    ctr = Vector(tuple((min(v[i] for v in bb) + max(v[i] for v in bb)) / 2 for i in range(3)))
    Tm = Matrix.Translation(-ctr)
    for o in his + [lo]:
        o.data.transform(Tm)
        o.data.update()
    attach_w = attach_w - ctr
    eye_w = M @ (sum((c for c, n, r, big in eyes), Vector()) / len(eyes)) - ctr
    # the silk dragline (optional helper part): 10 studs straight up from the spinnerets
    S = Strands()
    S.tube([attach_w + Vector((0, 0, -0.06)), attach_w + Vector((0, 0, 5.0)), attach_w + Vector((0, 0, 10.0))],
           0.035, 6)
    thread = S.to_object("SpiderThread", lambda co: (0.5, 0.5))
    thread.data.materials.append(mat_flat("ThreadMat", lin((226, 226, 230)), rough=0.45))
    # ---------- bake
    imgs = bake_set(lo, his, 1024, "Spider", cage=0.05, maxray=0.12, ao_strength=0.55, ao_dist=0.45, outdir=MAPS)
    soften_normal(imgs["normal"], os.path.join(MAPS, "Spider_normal.png"))
    pbr_material(lo, "Spider_PBR", imgs)
    for o in his:
        o.hide_render = True
        o.hide_viewport = True
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_SPIDER)
    bb = [v.co.copy() for v in lo.data.vertices]
    rep = {"hi_tris": {o.name: tris_of(o) for o in his}, "Spider": tris_of(lo), "SpiderThread": tris_of(thread),
           "size": [round(max(v[i] for v in bb) - min(v[i] for v in bb), 3) for i in range(3)],
           "attach_blender": [round(v, 3) for v in attach_w], "eyes_blender": [round(v, 3) for v in eye_w],
           "px_per_stud": round(uv_per_stud * 1024, 1),
           "miss": round(imgs["miss_fraction"], 4), "sculpt_s": round(t1 - t0, 1), "total_s": round(time.time() - t0, 1)}
    with open(os.path.join(OUT, "spider_report.json"), "w") as fh:
        json.dump(rep, fh, indent=1)
    return rep


def render_spider():
    bpy.ops.wm.open_mainfile(filepath=BLEND_SPIDER)
    sc = review_setup()
    front_sun(sc)
    sc.eevee.taa_render_samples = 64
    out = []
    out.append(shoot_fov(os.path.join(OUT, "review_spider_30.png"), (5, 26, -15), (0, 0, 0), vfov=70,
                         res=(1400, 1000)))
    out.append(shoot_fov(os.path.join(OUT, "review_spider_close.png"), (1.6, 8.6, -4.2), (0, 0, -0.4), lens=50))
    out.append(shoot_fov(os.path.join(OUT, "review_spider_34.png"), (7.5, 5.5, -2.5), (0, 0, 0), lens=50))
    eye = Vector(json.load(open(os.path.join(OUT, "spider_report.json")))["eyes_blender"])
    out.append(shoot_fov(os.path.join(OUT, "review_spider_face.png"), eye + Vector((0.9, 3.4, -1.9)),
                         eye + Vector((0, 0, -0.35)), lens=50))
    walls = wall_set(14, 30)
    for w in walls:
        w.location = (-7.0, -2.7, 9.0)
    out.append(shoot_fov(os.path.join(OUT, "review_spider_wall_30.png"), (5, 26, -15), (0, 0, 0), vfov=70))
    return out


def export_spider():
    bpy.ops.wm.open_mainfile(filepath=BLEND_SPIDER)
    o = bpy.data.objects
    return export_fbx([o["Spider"], o["SpiderThread"]], os.path.join(CDIMP, "Halloween_Spider.fbx"))


# ================================================================== main
if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["webs"]
    rep = {}
    for step in argv:
        t0 = time.time()
        fn = globals().get({"webs": "build_webs", "render_webs": "render_webs", "export_webs": "export_webs",
                            "spider": "build_spider", "render_spider": "render_spider",
                            "export_spider": "export_spider"}.get(step, step))
        rep[step] = fn()
        print("HW_STEP", step, round(time.time() - t0, 1), "s", flush=True)
    print("HW_REPORT " + json.dumps(rep, default=str))
