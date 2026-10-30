# Pet signature VFX, rendered in Blender (owner 2026-10-15: "why don't you make it on blender the vfx?").
# blender -b --factory-startup --python _vfx/render_vfx.py -- <outdir> [effect ...]
# Every effect is real Blender geometry / shader nodes, rendered with EEVEE through an orthographic camera:
#   frame = the XZ plane, x and z in [-1, 1]; emission only, black = nothing (pack.py turns brightness into alpha,
#   adds the glow and lays the frames out as Roblox flipbook sheets).
# Most textures are WHITE so Roblox can tint them per pet (ParticleEmitter.Color); fire is coloured (toon bands).
import bpy, bmesh, math, os, random, sys
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
OUT = os.path.abspath(args[0])
ONLY = set(args[1:])
TAU = math.tau


# ------------------------------------------------------------------ scene
def reset(res):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = "BLENDER_EEVEE"
    s.render.resolution_x = s.render.resolution_y = res
    s.render.resolution_percentage = 100
    s.render.film_transparent = True
    s.render.image_settings.file_format = "PNG"
    s.render.image_settings.color_mode = "RGBA"
    s.render.image_settings.color_depth = "8"
    s.view_settings.view_transform = "Standard"
    s.view_settings.look = "None"
    s.eevee.taa_render_samples = 16
    cam = bpy.data.cameras.new("cam")
    cam.type = "ORTHO"
    cam.ortho_scale = 2.0
    co = bpy.data.objects.new("cam", cam)
    co.location = (0, -10, 0)
    co.rotation_euler = (math.pi / 2, 0, 0)
    s.collection.objects.link(co)
    s.camera = co
    return s


def clear_objects():
    for o in list(bpy.data.objects):
        if o.type != "CAMERA":
            bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes):
        if m.users == 0:
            bpy.data.meshes.remove(m)


def render(name, i):
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    s = bpy.context.scene
    s.render.filepath = os.path.join(d, f"{i:03d}.png")
    bpy.ops.render.render(write_still=True)


def new_mat(name):
    m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    return m, nt, out


def vcol_mat():
    """emission = the mesh's per-vertex colour 'Col' (lets geometry carry soft gradients)"""
    m, nt, out = new_mat("vcol")
    at = nt.nodes.new("ShaderNodeAttribute")
    at.attribute_name = "Col"
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = 1.0
    nt.links.new(at.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    return m


# small node-expression helpers (shader math chains stay readable)
class N:
    def __init__(self, nt):
        self.nt = nt

    def _in(self, node, idx, v):
        if isinstance(v, (int, float)):
            node.inputs[idx].default_value = v
        else:
            self.nt.links.new(v, node.inputs[idx])

    def m(self, op, a, b=None, clamp=False):
        n = self.nt.nodes.new("ShaderNodeMath")
        n.operation = op
        n.use_clamp = clamp
        self._in(n, 0, a)
        if b is not None:
            self._in(n, 1, b)
        return n.outputs[0]

    def value(self, v):
        n = self.nt.nodes.new("ShaderNodeValue")
        n.outputs[0].default_value = v
        return n

    def combine(self, x, y, z=0.0):
        n = self.nt.nodes.new("ShaderNodeCombineXYZ")
        for i, v in enumerate((x, y, z)):
            self._in(n, i, v)
        return n.outputs[0]


def mesh_obj(name, verts2d, faces, cols, mat):
    me = bpy.data.meshes.new(name)
    me.from_pydata([(x, 0.0, z) for x, z in verts2d], [], faces)
    a = me.color_attributes.new("Col", "FLOAT_COLOR", "POINT")
    for i, c in enumerate(cols):
        a.data[i].color = (c[0], c[1], c[2], 1.0)
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    me.materials.append(mat)
    return ob


def ribbon(name, pts, widths, bright, mat, edge=0.0):
    """soft strip along a 2D polyline: centre line = bright[i], both edges = bright[i] * edge"""
    V, C, F = [], [], []
    n = len(pts)
    for i in range(n):
        p = Vector(pts[i])
        a = Vector(pts[max(i - 1, 0)])
        b = Vector(pts[min(i + 1, n - 1)])
        t = (b - a)
        t = t.normalized() if t.length > 1e-9 else Vector((0, 1))
        nrm = Vector((-t.y, t.x)) * widths[i]
        c = bright[i] if isinstance(bright[i], (tuple, list)) else (bright[i],) * 3
        V += [tuple(p - nrm), tuple(p), tuple(p + nrm)]
        C += [tuple(x * edge for x in c), c, tuple(x * edge for x in c)]
    for i in range(n - 1):
        k, j = 3 * i, 3 * (i + 1)
        F += [(k, k + 1, j + 1, j), (k + 1, k + 2, j + 2, j + 1)]
    return mesh_obj(name, V, F, C, mat)


def disc(name, rings, mat, seg=72, center=(0, 0)):
    """concentric rings [(radius, brightness), ...] from the centre out -> radial gradient fan/annulus"""
    V, C, F = [], [], []
    cx, cz = center
    for r, b in rings:
        for s in range(seg):
            a = TAU * s / seg
            V.append((cx + r * math.cos(a), cz + r * math.sin(a)))
            C.append(b if isinstance(b, (tuple, list)) else (b,) * 3)
    for k in range(len(rings) - 1):
        for s in range(seg):
            a0, a1 = k * seg + s, k * seg + (s + 1) % seg
            F.append((a0, a1, a1 + seg, a0 + seg))
    return mesh_obj(name, V, F, C, mat)


def jag(p0, p1, rough, depth, rng):
    """midpoint-displacement lightning between two 2D points"""
    pts = [Vector(p0), Vector(p1)]
    for d in range(depth):
        nxt = []
        amp = rough * (0.55 ** d)
        for a, b in zip(pts, pts[1:]):
            m = (a + b) / 2
            t = (b - a)
            nrm = Vector((-t.y, t.x)).normalized() if t.length > 1e-9 else Vector((1, 0))
            nxt += [a, m + nrm * rng.uniform(-amp, amp) * t.length]
        nxt.append(pts[-1])
        pts = nxt
    return [tuple(p) for p in pts]


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


# ------------------------------------------------------------------ effects
def fx_bolt():
    """forked lightning strike, one-shot: grows down in 3 frames, holds + flickers, branches re-fork, fades"""
    reset(256)
    mat = vcol_mat()
    rng = random.Random(7)
    main = jag((0.02, 0.98), (-0.04, -0.98), 0.22, 7, rng)
    for f in range(16):
        clear_objects()
        grow = min(1.0, (f + 1) / 3.0)
        fade = 1.0 if f < 9 else max(0.0, 1 - (f - 8) / 7.5)
        flick = (1.0, 0.65, 1.0, 0.8, 1.0, 0.55, 0.9)[f % 7] if 3 <= f <= 10 else 1.0
        b = fade * flick
        n = max(2, int(len(main) * grow))
        pts = main[:n]
        ribbon("core", pts, [0.016 * (0.6 + 0.4 * fade)] * n, [b] * n, mat, edge=0.3)
        ribbon("halo", pts, [0.03] * n, [0.32 * b] * n, mat, edge=0.0)
        r2 = random.Random(100 + f // 3)
        for k in range(4):
            i0 = int(len(main) * (0.15 + 0.2 * k + r2.uniform(-0.05, 0.05)))
            if i0 >= n - 2:
                continue
            p0 = Vector(main[i0])
            side = -1 if k % 2 else 1
            p1 = p0 + Vector((side * r2.uniform(0.25, 0.5), -r2.uniform(0.2, 0.45)))
            br = jag(tuple(p0), tuple(p1), 0.3, 5, r2)
            m = len(br)
            ribbon(f"br{k}", br, [0.006 * (1 - j / m) + 0.002 for j in range(m)],
                   [0.75 * b * (1 - 0.7 * j / m) for j in range(m)], mat)
        render("bolt", f)


def fx_arc():
    """electric crackle: short arcs jumping out of the centre, a new pattern every frame (FlipbookMode Random)"""
    reset(256)
    mat = vcol_mat()
    for f in range(16):
        clear_objects()
        rng = random.Random(500 + f)
        disc("core", [(0, 1.0), (0.035, 0.45), (0.12, 0.08), (0.3, 0.0)], mat, seg=36)
        for k in range(rng.randint(4, 6)):
            a = rng.uniform(0, TAU)
            L = rng.uniform(0.6, 0.98)
            p1 = (math.cos(a) * L, math.sin(a) * L)
            pts = jag((0, 0), p1, 0.35, 5, rng)
            m = len(pts)
            ribbon(f"a{k}", pts, [0.012 * (1 - 0.6 * j / m) for j in range(m)], [1.0 - 0.5 * j / m for j in range(m)], mat)
            ribbon(f"h{k}", pts, [0.028] * m, [0.25] * m, mat)
            j0 = rng.randint(m // 3, 2 * m // 3)
            q = Vector(pts[j0])
            b2 = a + rng.choice((-1, 1)) * rng.uniform(0.5, 1.0)
            fork = jag(tuple(q), tuple(q + Vector((math.cos(b2), math.sin(b2))) * L * 0.4), 0.4, 4, rng)
            ribbon(f"f{k}", fork, [0.006] * len(fork), [0.7] * len(fork), mat)
        render("arc", f)


def fx_ring():
    """shockwave ring: thin bright outer rim, soft fade inward (sized up over the particle's life in Roblox)"""
    reset(512)
    mat = vcol_mat()
    disc("ring", [(0.62, 0.0), (0.82, 0.06), (0.9, 0.22), (0.945, 0.7), (0.962, 1.0), (0.975, 0.35), (0.988, 0.0)], mat, seg=128)
    render("ring", 0)


def fx_slash():
    """crescent blade slash: the cut sweeps 200 degrees, sharp leading tip, tail thins and fades"""
    reset(256)
    mat = vcol_mat()
    for f in range(16):
        clear_objects()
        head = ease(f / 7.0)
        tail = ease((f - 3) / 11.0)
        a_end = math.radians(-100 + 220 * head)
        a_start = math.radians(-100 + 220 * tail)
        if a_end - a_start < 0.02:
            render("slash", f)
            continue
        pts, w, br = [], [], []
        K = 40
        for j in range(K + 1):
            u = j / K
            a = a_start + (a_end - a_start) * u
            r = 0.8 + 0.06 * math.sin(math.pi * u)
            pts.append((r * math.cos(a), r * math.sin(a)))
            w.append(0.015 + 0.13 * math.sin(math.pi * u ** 0.7) * (1 - 0.5 * tail))
            br.append((0.2 + 0.8 * u ** 1.3) * (1 - 0.8 * max(0, (f - 10) / 6)))
        ribbon("blade", pts, w, br, mat, edge=0.25)
        ribbon("edge", [(x * 1.035, z * 1.035) for x, z in pts], [x * 0.18 for x in w], [min(1, b * 1.4) for b in br], mat)
        render("slash", f)


def fx_splash():
    """water splash crown: a rising crown sheet + ballistic droplets stretched along their velocity"""
    reset(256)
    mat_v = vcol_mat()
    m, nt, out = new_mat("drop")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = (1, 1, 1, 1)
    mix.inputs["B"].default_value = (0.45, 0.45, 0.45, 1)
    nt.links.new(lw.outputs["Facing"], mix.inputs["Factor"])
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(mix.outputs["Result"], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    rng = random.Random(3)
    drops = []
    for k in range(26):
        a = rng.uniform(math.radians(25), math.radians(155))
        sp = rng.uniform(3.0, 4.6)
        drops.append((Vector((math.cos(a) * sp * 0.8, math.sin(a) * sp)), rng.uniform(0.035, 0.065), rng.uniform(-0.15, 0.15)))
    g = -9.0
    for f in range(16):
        clear_objects()
        t = (f + 1) / 16 * 0.62
        # crown sheet: fan of soft quads rising then collapsing
        h = 1.45 * math.sin(min(1.0, t / 0.3) * math.pi * 0.5) * (1 - max(0, (t - 0.3) / 0.34))
        if h > 0.02:
            V, C, F = [], [], []
            K = 24
            for j in range(K + 1):
                u = j / K
                x0 = -0.75 + 1.5 * u
                lean = (u - 0.5) * 0.9 * h
                tip = h * (0.75 + 0.25 * math.sin(u * 37.0))
                V += [(x0 * 0.7, -0.85), (x0 * 0.85 + lean * 0.5, -0.85 + tip * 0.6), (x0 + lean, -0.85 + tip)]
                C += [(0.35,) * 3, (0.75,) * 3, (0.15,) * 3]
            for j in range(K):
                k, n2 = 3 * j, 3 * (j + 1)
                F += [(k, k + 1, n2 + 1, n2), (k + 1, k + 2, n2 + 2, n2 + 1)]
            mesh_obj("crown", V, F, C, mat_v)
        disc("base", [(0, 0.55), (0.25, 0.25), (0.62, 0.0)], mat_v, seg=48, center=(0, -0.88))
        for i, (v, r, x0) in enumerate(drops):
            tt = t - 0.04 * (i % 4)
            if tt <= 0:
                continue
            p = Vector((x0, -0.8)) + v * tt + Vector((0, 0.5 * g * tt * tt))
            vel = v + Vector((0, g * tt))
            if p.y < -1.0:
                continue
            bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=r * (1 - 0.5 * t))
            o = bpy.context.active_object
            o.location = (p.x, 0, p.y)
            o.rotation_euler = (0, -math.atan2(vel.y, vel.x), 0)
            o.scale = (1 + 0.35 * vel.length, 1, 1)
            o.data.materials.append(m)
        render("splash", f)


def flame_shader(name, toon_cols, toon_pos, smoke=False):
    """procedural toon fire / smoke on a plane: 4D noise scrolled upward, masked by a teardrop, cut into bands"""
    m, nt, out = new_mat(name)
    x = N(nt)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    u, v = sep.outputs[0], sep.outputs[1]
    T = x.value(0.0)          # time
    R = x.value(0.6)          # size
    D = x.value(0.0)          # dissolve
    rise = 1.0 if not smoke else 0.5
    # noise coords: scroll up with time
    nv = x.combine(x.m("MULTIPLY", u, 2.4), x.m("MULTIPLY", x.m("SUBTRACT", v, x.m("MULTIPLY", T.outputs[0], 1.6 * rise)), 2.4), 0.0)
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.noise_dimensions = "4D"
    nz.inputs["Scale"].default_value = 1.6
    nz.inputs["Detail"].default_value = 4.0
    nz.inputs["Roughness"].default_value = 0.55
    nt.links.new(nv, nz.inputs["Vector"])
    nt.links.new(x.m("MULTIPLY", T.outputs[0], 0.9), nz.inputs["W"])
    # teardrop mask: centre low, narrows upward (fire) / round puff (smoke)
    cy = -0.35 if not smoke else 0.0
    dy = x.m("SUBTRACT", v, cy)
    up = x.m("MAXIMUM", dy, 0.0)
    narrow = x.m("ADD", 1.0, x.m("MULTIPLY", up, 1.3 if not smoke else 0.0))
    dx = x.m("MULTIPLY", u, narrow)
    dyy = x.m("MULTIPLY", dy, x.m("ADD", 0.55, x.m("MULTIPLY", x.m("LESS_THAN", dy, 0.0), 0.6)) if not smoke else 1.0)
    dist = x.m("SQRT", x.m("ADD", x.m("MULTIPLY", dx, dx), x.m("MULTIPLY", dyy, dyy)))
    mask = x.m("SUBTRACT", 1.0, x.m("DIVIDE", dist, R.outputs[0]), clamp=True)
    dens = x.m("SUBTRACT", x.m("MULTIPLY", mask, 1.5), x.m("MULTIPLY", x.m("SUBTRACT", 1.0, nz.outputs["Fac"]), 0.85))
    dens = x.m("SUBTRACT", dens, D.outputs[0], clamp=True)
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "CONSTANT"
    els = ramp.color_ramp.elements
    els[0].position, els[0].color = 0.0, (0, 0, 0, 1)
    els[1].position, els[1].color = toon_pos[0], toon_cols[0]
    for p, c in zip(toon_pos[1:], toon_cols[1:]):
        e = els.new(p)
        e.color = c
    nt.links.new(dens, ramp.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(ramp.outputs[0], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    return m, T.outputs[0], R.outputs[0], D.outputs[0]


def plane(mat):
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0, 0, 0), rotation=(math.pi / 2, 0, 0))
    o = bpy.context.active_object
    o.data.materials.append(mat)
    return o


def fx_fire():
    """toon fire burst (coloured): ignites, roars, then burns out from the bottom up"""
    reset(256)
    m, T, R, D = flame_shader("fire",
        [(0.55, 0.06, 0.02, 1), (1.0, 0.32, 0.03, 1), (1.0, 0.68, 0.1, 1), (1.0, 0.95, 0.65, 1)],
        [0.03, 0.2, 0.42, 0.66])
    plane(m)
    for f in range(16):
        t = f / 15
        T.default_value = t * 1.6
        R.default_value = 0.3 + 0.6 * ease(f / 4.0)
        D.default_value = 0.85 * ease((f - 8) / 7.0)
        render("fire", f)


def fx_smoke():
    """toon smoke puff (white, tinted per use): bulges out, then breaks up and vanishes"""
    reset(256)
    m, T, R, D = flame_shader("smoke", [(0.55, 0.55, 0.55, 1), (0.8, 0.8, 0.8, 1), (1, 1, 1, 1)], [0.04, 0.22, 0.45], smoke=True)
    plane(m)
    for f in range(16):
        T.default_value = f / 15 * 1.2
        R.default_value = 0.35 + 0.6 * ease(f / 6.0)
        D.default_value = 0.9 * ease((f - 6) / 9.0)
        render("smoke", f)


def fx_swirl():
    """void vortex: 4 spiral arms in toon bands, empty eye, soft outer edge (spun by RotSpeed in Roblox)"""
    reset(512)
    m, nt, out = new_mat("swirl")
    x = N(nt)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    u, v = sep.outputs[0], sep.outputs[1]
    r = x.m("SQRT", x.m("ADD", x.m("MULTIPLY", u, u), x.m("MULTIPLY", v, v)))
    ang = x.m("ARCTAN2", v, u)
    arms = x.m("ADD", x.m("MULTIPLY", ang, 4 / TAU), x.m("MULTIPLY", x.m("LOGARITHM", x.m("MAXIMUM", r, 0.02), math.e), 1.6))
    band = x.m("SINE", x.m("MULTIPLY", arms, TAU))
    band = x.m("MULTIPLY", x.m("ADD", band, 1.0), 0.5)
    ring_in = x.m("MINIMUM", 1.0, x.m("MULTIPLY", x.m("SUBTRACT", r, 0.12), 6.0))
    edge = x.m("SUBTRACT", 1.0, x.m("POWER", x.m("DIVIDE", r, 0.98), 3.0), clamp=True)
    val = x.m("MULTIPLY", x.m("MULTIPLY", band, x.m("MAXIMUM", ring_in, 0.0)), edge)
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "CONSTANT"
    els = ramp.color_ramp.elements
    els[0].position, els[0].color = 0.0, (0, 0, 0, 1)
    els[1].position, els[1].color = 0.12, (0.35, 0.35, 0.35, 1)
    e = els.new(0.38); e.color = (0.7, 0.7, 0.7, 1)
    e = els.new(0.62); e.color = (1, 1, 1, 1)
    nt.links.new(val, ramp.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(ramp.outputs[0], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    plane(m)
    render("swirl", 0)


def star_shape(mat, rays, length, width, core, glow_r):
    disc("glow", [(0, core), (glow_r * 0.06, core * 0.55), (glow_r * 0.18, core * 0.22), (glow_r * 0.45, core * 0.06),
                  (glow_r, 0.0)], mat, seg=64)
    for k, (ang, L, W, b) in enumerate(rays):
        a = math.radians(ang)
        d = Vector((math.cos(a), math.sin(a)))
        nrm = Vector((-d.y, d.x))
        V = [(0, 0), tuple(d * L * length), tuple(nrm * W * width), tuple(-d * L * length), tuple(-nrm * W * width)]
        C = [(b,) * 3, (0,) * 3, (b * 0.2,) * 3, (0,) * 3, (b * 0.2,) * 3]
        F = [(0, 2, 1), (0, 1, 4), (0, 4, 3), (0, 3, 2)]
        mesh_obj(f"ray{k}", V, F, C, mat)


def fx_star():
    """sharp 4-point twinkle star"""
    reset(256)
    mat = vcol_mat()
    star_shape(mat, [(90, 1.0, 1.0, 1.0), (0, 0.78, 1.0, 1.0), (45, 0.34, 0.8, 0.6), (135, 0.34, 0.8, 0.6)], 0.95, 0.075, 1.0, 0.28)
    render("star", 0)


def fx_flare():
    """big soft flare: wide glow, long thin cross rays"""
    reset(256)
    mat = vcol_mat()
    star_shape(mat, [(0, 1.0, 1.0, 0.8), (90, 0.7, 1.0, 0.7), (30, 0.4, 0.6, 0.35), (150, 0.4, 0.6, 0.35)], 0.98, 0.03, 1.0, 0.75)
    render("flare", 0)


def fx_streak():
    """vertical comet streak: round bright head at the top, long tapering tail (VelocityParallel particles)"""
    reset(256)
    mat = vcol_mat()
    K = 40
    pts = [(0.0, 0.92 - 1.8 * j / K) for j in range(K + 1)]
    ribbon("tail", pts, [0.07 * (1 - j / K) ** 1.4 + 0.004 for j in range(K + 1)], [(1 - j / K) ** 1.6 for j in range(K + 1)], mat, edge=0.0)
    disc("head", [(0, 1.0), (0.05, 0.85), (0.12, 0.0)], mat, seg=40, center=(0, 0.86))
    render("streak", 0)


def fx_drip():
    """teardrop (venom / water drop), round bottom, pointed top, bright highlight"""
    reset(256)
    mat = vcol_mat()
    V, C, F = [(0.0, -0.25)], [(1.0,) * 3], []
    K = 48
    for j in range(K):
        a = TAU * j / K
        s = math.sin(a)
        r = 0.42 if s < 0 else 0.42 * (1 - 0.92 * (s ** 1.2))
        x0, z0 = r * math.cos(a), -0.35 + (0.42 if s < 0 else 1.15) * s
        V.append((x0, z0))
        C.append((0.55,) * 3)
    for j in range(K):
        F.append((0, 1 + j, 1 + (j + 1) % K))
    mesh_obj("drop", V, F, C, mat)
    disc("hi", [(0, 1.0), (0.07, 0.0)], mat, seg=24, center=(-0.14, -0.2))
    render("drip", 0)


def fx_bubble():
    """bubble: thin bright rim + crescent highlight, clear middle"""
    reset(256)
    mat = vcol_mat()
    disc("rim", [(0.7, 0.0), (0.84, 0.25), (0.9, 0.85), (0.93, 0.0)], mat, seg=96)
    K = 24
    pts = [(0.62 * math.cos(math.radians(100 + 70 * j / K)), 0.62 * math.sin(math.radians(100 + 70 * j / K))) for j in range(K + 1)]
    ribbon("hl", pts, [0.07 * math.sin(math.pi * j / K) + 0.005 for j in range(K + 1)], [1.0] * (K + 1), mat, edge=0.0)
    render("bubble", 0)


def fx_leaf():
    """blade-shaped leaf with a midrib (Grass bursts)"""
    reset(256)
    mat = vcol_mat()
    V, C, F = [], [], []
    K = 30
    for j in range(K + 1):
        u = j / K
        z = -0.9 + 1.8 * u
        w = 0.36 * math.sin(math.pi * u) ** 0.9 * (1 - 0.25 * u)
        V += [(-w, z + 0.05 * math.sin(math.pi * u)), (0.0, z), (w, z + 0.05 * math.sin(math.pi * u))]
        C += [(0.6,) * 3, (1.0,) * 3, (0.75,) * 3]
    for j in range(K):
        k, n2 = 3 * j, 3 * (j + 1)
        F += [(k, k + 1, n2 + 1, n2), (k + 1, k + 2, n2 + 2, n2 + 1)]
    mesh_obj("leaf", V, F, C, mat)
    render("leaf", 0)


def periodic_line(rng, n, amp, freqs):
    ph = [rng.uniform(0, TAU) for _ in freqs]
    am = [rng.uniform(0.4, 1.0) / (1 + i * 0.6) for i in range(len(freqs))]
    out = []
    for j in range(n + 1):
        x = j / n
        y = sum(a * math.sin(TAU * f * x + p) for a, f, p in zip(am, freqs, ph))
        out.append((x, y * amp))
    return out


def fx_beams():
    """tiling beam textures, 512 x 128 (x = along the beam): 3 jagged electric variants + silk threads"""
    for name, seed in (("zap1", 11), ("zap2", 12), ("zap3", 13)):
        reset(512)
        s = bpy.context.scene
        s.render.resolution_y = 128
        bpy.context.scene.camera.data.ortho_scale = 2.0
        mat = vcol_mat()
        rng = random.Random(seed)
        for k in range(3):
            line = periodic_line(rng, 160, 0.16 if k == 0 else 0.1, [1, 2, 3, 5, 8, 13, 21])
            pts = [(-1 + 2 * x, y) for x, y in line]
            b = 1.0 if k == 0 else 0.55
            ribbon(f"z{k}", pts, [0.011 if k == 0 else 0.007] * len(pts), [b] * len(pts), mat)
            ribbon(f"h{k}", pts, [0.03] * len(pts), [0.22 * b] * len(pts), mat)
        render(name, 0)
    reset(512)
    s = bpy.context.scene
    s.render.resolution_y = 128
    mat = vcol_mat()
    rng = random.Random(21)
    for k in range(4):
        line = periodic_line(rng, 120, 0.08, [1, 2, 3])
        pts = [(-1 + 2 * x, y + (k - 1.5) * 0.04) for x, y in line]
        ribbon(f"s{k}", pts, [0.006] * len(pts), [0.9 - 0.15 * k] * len(pts), mat, edge=0.2)
    render("silk", 0)


FX = {
    "bolt": fx_bolt, "arc": fx_arc, "ring": fx_ring, "slash": fx_slash, "splash": fx_splash, "fire": fx_fire,
    "smoke": fx_smoke, "swirl": fx_swirl, "star": fx_star, "flare": fx_flare, "streak": fx_streak, "drip": fx_drip,
    "bubble": fx_bubble, "leaf": fx_leaf, "beams": fx_beams,
}
for name, fn in FX.items():
    if ONLY and name not in ONLY:
        continue
    fn()
    print("VFX done", name)
