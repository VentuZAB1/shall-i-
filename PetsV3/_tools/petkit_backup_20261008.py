# petkit: shared Blender toolkit for the SLINGSHOT "Pets V2" remake (2026-10-08).
# Style: the Cvetibara look the user loved - soft chibi forms (big head, round body, stubby legs), big glossy
# eyes with 2 highlights, warm saturated colours, gold/glow accents; NOT studded. Inspiration: Steal an Egg,
# Adopt Me, Pet Simulator 99, Grow a Garden (broader than one game).
# Pipeline per pet (pets/<Name>.py defines model(k), rig(k), anim(k)):
#   metaball body -> voxel remesh -> smooth -> decimate, parts placed with ray casts, per-vertex colours;
#   armature (bones oriented joint -> child, body skinned with bone-heat auto weights, parts rigid/split);
#   clips keyed on pose bones only, Bezier + auto-clamped, loops with a Cycles modifier (no seam), planted feet
#   solved per frame (animate-roblox-characters skill rules); audit; sample into the CreatureClips format
#   (root-space deltas, Blender (x, y, z) -> Roblox (-x, z, y)); bake colours x AO; FBX; Luau; portrait; GIFs.
# Model faces -Y, ground z = 0, about 2-3 BU tall (1 BU ~ 2.8 studs in game).
import bpy, bmesh, math, os, json
from mathutils import Vector, Matrix, Quaternion
from bpy_extras import anim_utils

ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV2"
IMP = r"C:\cdimp"
FPS = 30
K = 0.575  # metaball calibration: one element's surface half-size = 0.575 * radius * size


# ------------------------------------------------------------------ colour helpers
def lin(c):
    def f(x):
        x = x / 255.0
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return (f(c[0]), f(c[1]), f(c[2]), 1.0)


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(4))


def smooth(e0, e1, x):
    if e1 == e0:
        return 1.0 if x >= e0 else 0.0
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


WHITE = lin((255, 255, 255))
BLACKISH = lin((22, 16, 34))
GOLD = lin((255, 200, 64))
GOLD_DEEP = lin((235, 150, 30))
BLUSH = lin((255, 150, 165))


# ------------------------------------------------------------------ mesh primitives
def color_layer(bm):
    return bm.verts.layers.float_color.get("Col") or bm.verts.layers.float_color.new("Col")


def frame(origin, x_axis, z_axis):
    x = Vector(x_axis).normalized()
    z = Vector(z_axis)
    z = (z - x * z.dot(x))
    if z.length < 1e-6:
        z = x.orthogonal()
    z = z.normalized()
    y = z.cross(x)
    m = Matrix((x, y, z)).transposed().to_4x4()
    m.translation = Vector(origin)
    return m


def blob(bm, L, matrix, deform, color, useg=14, vseg=8):
    res = bmesh.ops.create_uvsphere(bm, u_segments=useg, v_segments=vseg, radius=1.0)
    for v in res["verts"]:
        u = v.co.copy()
        lc = deform(u)
        v.co = matrix @ lc
        v[L] = color(u, lc) if callable(color) else color
    return res["verts"]


def ellipsoid(bm, L, center, radii, color, x_axis=(1, 0, 0), z_axis=(0, 0, 1), useg=14, vseg=8):
    m = frame(center, x_axis, z_axis)
    return blob(bm, L, m, lambda u: Vector((u.x * radii[0], u.y * radii[1], u.z * radii[2])), color, useg, vseg)


def tube(bm, L, pts, radius, color, sides=8, cap=True):
    """Tube along pts; radius = number, (r0, r1) or callable(t); color = rgba or callable(t, ang)."""
    pts = [Vector(p) for p in pts]
    rings = []
    n = len(pts)
    prev_a = None
    for i, p in enumerate(pts):
        t = i / (n - 1)
        d = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        if prev_a is None:
            a = d.orthogonal().normalized()
        else:  # parallel transport so the tube doesn't twist
            a = (prev_a - d * prev_a.dot(d)).normalized()
        prev_a = a
        b = d.cross(a)
        if callable(radius):
            r = radius(t)
        elif isinstance(radius, (tuple, list)):
            r = radius[0] + (radius[1] - radius[0]) * t
        else:
            r = radius
        ring = []
        for j in range(sides):
            ang = 2 * math.pi * j / sides
            v = bm.verts.new(p + (a * math.cos(ang) + b * math.sin(ang)) * max(r, 1e-4))
            v[L] = color(t, ang) if callable(color) else color
            ring.append(v)
        rings.append(ring)
    for i in range(n - 1):
        for j in range(sides):
            bm.faces.new((rings[i][j], rings[i + 1][j], rings[i + 1][(j + 1) % sides], rings[i][(j + 1) % sides]))
    if cap:
        for idx, ring in ((0, rings[0]), (n - 1, rings[-1])):
            c = bm.verts.new(pts[idx])
            c[L] = ring[0][L]
            for j in range(sides):
                if idx == 0:
                    bm.faces.new((c, ring[(j + 1) % sides], ring[j]))
                else:
                    bm.faces.new((c, ring[j], ring[(j + 1) % sides]))


def arc_points(p0, direction, length, bend_axis=None, bend_deg=0.0, n=10, twist=None):
    """Points along a curve starting at p0 heading `direction`, bending about `bend_axis` by bend_deg total."""
    p = Vector(p0)
    d = Vector(direction).normalized()
    pts = [p.copy()]
    step = length / (n - 1)
    rot = Quaternion(Vector(bend_axis).normalized(), math.radians(bend_deg) / (n - 1)) if bend_axis else Quaternion()
    for _ in range(n - 1):
        p = p + d * step
        pts.append(p.copy())
        d = rot @ d
    return pts


def cone(bm, L, base, direction, length, r, color, bend_axis=None, bend_deg=0.0, sides=8, n=6):
    pts = arc_points(base, direction, length, bend_axis, bend_deg, n)
    tube(bm, L, pts, lambda t: r * (1 - t) ** 0.85 + 0.004, color, sides)


def star_points(r_out, r_in, n=5):
    return [Vector(((r_out if i % 2 == 0 else r_in) * math.cos(math.pi / 2 + math.pi * i / n),
                    (r_out if i % 2 == 0 else r_in) * math.sin(math.pi / 2 + math.pi * i / n), 0)) for i in range(n * 2)]


def puffy_star(bm, L, m, size, color, depth=0.28):
    ring = [bm.verts.new(m @ p) for p in star_points(size, size * 0.48)]
    top = bm.verts.new(m @ Vector((0, 0, size * depth)))
    bot = bm.verts.new(m @ Vector((0, 0, -size * 0.1)))
    for v in ring + [top, bot]:
        v[L] = color
    for i in range(len(ring)):
        a, b = ring[i], ring[(i + 1) % len(ring)]
        bm.faces.new((top, a, b))
        bm.faces.new((bot, b, a))


def torus(bm, L, center, radius, tube_r, color, x_axis=(1, 0, 0), z_axis=(0, 0, 1), N=36, M=8):
    m = frame(center, x_axis, z_axis)
    rows = []
    for i in range(N):
        a = 2 * math.pi * i / N
        ring = []
        for j in range(M):
            b = 2 * math.pi * j / M
            r = radius + tube_r * math.cos(b)
            v = bm.verts.new(m @ Vector((r * math.cos(a), r * math.sin(a), tube_r * math.sin(b))))
            v[L] = color(b) if callable(color) else color
            ring.append(v)
        rows.append(ring)
    for i in range(N):
        for j in range(M):
            bm.faces.new((rows[i][j], rows[(i + 1) % N][j], rows[(i + 1) % N][(j + 1) % M], rows[i][(j + 1) % M]))


# ------------------------------------------------------------------ the pet context
class Pet:
    def __init__(self, name, display=None):
        self.name = name
        self.display = display or name
        self.dir = os.path.join(ROOT, name)
        os.makedirs(os.path.join(self.dir, "renders"), exist_ok=True)
        self.parts = []      # (object, weights) weights = bone name | callable(co) -> {bone: w}
        self.glow = []       # glow objects (become Neon in Roblox), same weights format
        self.J = {}          # joint positions
        self.P = {}          # joint parents
        self.tail = {}       # optional bone tail direction per joint
        self.body_bones = [] # bones the body mesh is auto-weighted to
        self.clips = {}      # name -> (frames, loop)
        self.events = {}     # clip -> {event: fraction}
        self.meta = {"motion": "Walk", "rig": "quad", "height": 7.0, "walk_cycle": None}
        self.reset()

    # ---------------- scene
    def reset(self):
        for o in list(bpy.data.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        for block in (bpy.data.meshes, bpy.data.metaballs, bpy.data.materials, bpy.data.curves, bpy.data.armatures,
                      bpy.data.cameras, bpy.data.lights, bpy.data.actions, bpy.data.images):
            for d in list(block):
                if d.users == 0 or block is bpy.data.actions:
                    try:
                        block.remove(d)
                    except Exception:
                        pass
        for c in list(bpy.data.collections):
            bpy.data.collections.remove(c)
        self.coll = bpy.data.collections.new(self.name)
        bpy.context.scene.collection.children.link(self.coll)
        self.mat, self.mat_glow = self._materials()

    def _materials(self):
        def mat(name, glow):
            m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
            m.use_nodes = True
            nt = m.node_tree
            nt.nodes.clear()
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

    def obj_from_bm(self, name, bm, glow=False, smooth_shade=True):
        me = bpy.data.meshes.new(name)
        bm.to_mesh(me)
        bm.free()
        if smooth_shade:
            for p in me.polygons:
                p.use_smooth = True
        me.materials.append(self.mat_glow if glow else self.mat)
        ob = bpy.data.objects.new(name, me)
        self.coll.objects.link(ob)
        return ob

    def part(self, name, build, weights, glow=False, smooth_shade=True):
        """build(bm, L) adds geometry. weights: bone name or callable(co)->{bone: w}."""
        bm = bmesh.new()
        L = color_layer(bm)
        build(bm, L)
        o = self.obj_from_bm(name, bm, glow, smooth_shade)
        (self.glow if glow else self.parts).append((o, weights))
        return o

    # ---------------- body
    def body(self, elements, color_fn, tris=5200, voxel=0.028, smooth_iter=6):
        """elements: list of ("ell", co, radii) | ("box", co, half, round) | ("cap", p0, p1, r) | ("ball", co, r)
        optional last item in each tuple: stiffness."""
        mb = bpy.data.metaballs.new("BodyMB")
        mb.resolution = mb.render_resolution = 0.03
        mb.threshold = 0.6
        mbo = bpy.data.objects.new("BodyMB", mb)
        self.coll.objects.link(mbo)
        for e in elements:
            kind = e[0]
            if kind == "ell":
                co, radii = e[1], e[2]
                st = e[3] if len(e) > 3 else 2.0
                x = mb.elements.new(type="ELLIPSOID")
                x.co, x.radius, x.stiffness = co, 1.0, st
                x.size_x, x.size_y, x.size_z = (radii[0] / K, radii[1] / K, radii[2] / K)
            elif kind == "box":
                co, half, rr = e[1], e[2], e[3]
                st = e[4] if len(e) > 4 else 2.0
                x = mb.elements.new(type="CUBE")
                x.co, x.radius, x.stiffness = co, rr / K, st
                x.size_x, x.size_y, x.size_z = (max(0, half[0] - rr), max(0, half[1] - rr), max(0, half[2] - rr))
            elif kind == "cap":
                p0, p1, r = Vector(e[1]), Vector(e[2]), e[3]
                st = e[4] if len(e) > 4 else 2.0
                x = mb.elements.new(type="CAPSULE")
                x.co = (p0 + p1) / 2
                x.radius, x.stiffness = r / K, st
                x.size_x = (p1 - p0).length / 2
                x.rotation = Vector((1, 0, 0)).rotation_difference((p1 - p0).normalized())
            elif kind == "ball":
                x = mb.elements.new(type="BALL")
                x.co, x.radius = e[1], e[2] / K
                x.stiffness = e[3] if len(e) > 3 else 2.0
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        me = bpy.data.meshes.new_from_object(mbo.evaluated_get(dg))
        bpy.data.objects.remove(mbo, do_unlink=True)
        bpy.data.metaballs.remove(mb)
        body = bpy.data.objects.new("Body", me)
        self.coll.objects.link(body)
        me.remesh_voxel_size = voxel
        with bpy.context.temp_override(object=body, active_object=body, selected_objects=[body]):
            bpy.ops.object.voxel_remesh()
        sm = body.modifiers.new("Smooth", "SMOOTH")
        sm.factor, sm.iterations = 0.6, smooth_iter
        dec = body.modifiers.new("Decimate", "DECIMATE")
        dg = bpy.context.evaluated_depsgraph_get()
        t0 = sum(len(p.vertices) - 2 for p in body.evaluated_get(dg).data.polygons)
        dec.ratio = min(1.0, tris / max(t0, 1))
        with bpy.context.temp_override(object=body, active_object=body, selected_objects=[body]):
            bpy.ops.object.modifier_apply(modifier="Smooth")
            bpy.ops.object.modifier_apply(modifier="Decimate")
        for p in me.polygons:
            p.use_smooth = True
        me.materials.append(self.mat)
        self.bodyobj = body
        self.paint(body, color_fn)
        return body

    def paint(self, obj, fn):
        me = obj.data
        attr = me.color_attributes.get("Col") or me.color_attributes.new("Col", "FLOAT_COLOR", "POINT")
        me.color_attributes.active_color = attr
        for i, v in enumerate(me.vertices):
            attr.data[i].color = fn(v.co, v.normal)

    def surf(self, origin, target):
        d = (Vector(target) - Vector(origin)).normalized()
        ok, loc, nrm, _ = self.bodyobj.ray_cast(Vector(origin), d)
        if not ok:
            raise RuntimeError(f"{self.name}: no body surface from {tuple(origin)} toward {tuple(target)}")
        return loc, nrm

    # ---------------- faces
    def eyes(self, positions, size=(0.16, 0.19), style="big", iris=(112, 82, 196), lid=None, lid_tilt=18,
             depth=0.04, pupil="round", name="Eyes", bone="Head"):
        """positions: [(origin, target)] ray-cast pairs (one per eye, +X side first).
        style: big | fierce (angled brow lid) | sleepy (half lid) | cat (slit pupil, coloured iris)."""
        iris_c = lin(iris)
        lid_c = lid

        def build(bm, L):
            for idx, (o, t) in enumerate(positions):
                sx = 1 if idx == 0 else -1
                loc, n = self.surf(o, t)
                side = Vector((1, 0, 0)) - n * n.x
                m = frame(loc - n * depth, side, n)
                ex, ey = size
                if pupil == "slit":
                    # coloured iris + dark vertical slit pupil
                    blob(bm, L, m, lambda u: Vector((u.x * ex, u.y * ey, u.z * ex * 0.5)),
                         lambda u, lc: mix(iris_c, mix(iris_c, WHITE, 0.35), smooth(-0.6, 0.8, u.y)), 16, 10)
                    blob(bm, L, m @ Matrix.Translation((0, 0, ex * 0.25)),
                         lambda u: Vector((u.x * ex * 0.22, u.y * ey * 0.82, u.z * ex * 0.32)), BLACKISH, 10, 8)
                else:
                    blob(bm, L, m, lambda u: Vector((u.x * ex, u.y * ey, u.z * ex * 0.5)),
                         lambda u, lc: mix(BLACKISH, iris_c, smooth(0.15, -0.95, u.y)), 16, 10)
                hl = m @ Matrix.Translation((sx * ex * 0.32, ey * 0.4, ex * 0.42))
                blob(bm, L, hl, lambda u: Vector((u.x * ex * 0.37, u.y * ey * 0.33, u.z * 0.025)), WHITE, 10, 6)
                hl2 = m @ Matrix.Translation((-sx * ex * 0.33, -ey * 0.45, ex * 0.4))
                blob(bm, L, hl2, lambda u: Vector((u.x * ex * 0.17, u.y * ey * 0.14, u.z * 0.015)), WHITE, 8, 5)
                if style in ("fierce", "sleepy") and lid_c is not None:
                    tilt = math.radians(lid_tilt) * (-sx) if style == "fierce" else 0.0
                    drop = ey * (0.62 if style == "fierce" else 0.25)
                    lm = m @ Matrix.Translation((0, drop, ex * 0.18)) @ Matrix.Rotation(tilt, 4, "Z")
                    blob(bm, L, lm, lambda u: Vector((u.x * ex * 1.25, u.y * ey * 0.55, u.z * ex * 0.62 + 0.01)),
                         lid_c, 12, 8)
        return self.part(name, build, bone)

    # ---------------- rig
    def joint(self, name, pos, parent, tail=None):
        self.J[name] = Vector(pos)
        if parent:
            self.P[name] = parent
        if tail is not None:
            self.tail[name] = Vector(tail)

    def build_rig(self):
        mn, mx = self.bounds()
        self.J["Root"] = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, 0.0))
        ad = bpy.data.armatures.new("Armature")
        arm = bpy.data.objects.new("Armature", ad)
        self.coll.objects.link(arm)
        for o in bpy.context.view_layer.objects:
            o.select_set(False)
        arm.select_set(True)
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode="EDIT")
        kids = {}
        for b, p in self.P.items():
            kids.setdefault(p, []).append(b)
        order = ["Root"]
        i = 0
        while i < len(order):
            order += kids.get(order[i], [])
            i += 1
        for b in order:
            e = ad.edit_bones.new(b)
            e.head = self.J[b]
            if b in self.tail:
                tl = self.tail[b]
            elif b in kids and len(kids[b]) == 1 and (self.J[kids[b][0]] - self.J[b]).length > 0.05:
                tl = self.J[kids[b][0]] - self.J[b]
            else:
                tl = Vector((0, 0, 0.15))
            if tl.length < 0.03:
                tl = tl.normalized() * 0.1 if tl.length > 0 else Vector((0, 0, 0.1))
            e.tail = self.J[b] + tl
            e.roll = 0
            if b in self.P:
                e.parent = ad.edit_bones[self.P[b]]
        bpy.ops.object.mode_set(mode="OBJECT")
        self.arm = arm
        for pb in arm.pose.bones:
            pb.rotation_mode = "QUATERNION"
        # body: bone-heat auto weights on the body bones only
        body = self.bodyobj
        for b in ad.bones:
            b.use_deform = b.name in self.body_bones
        for o in bpy.context.view_layer.objects:
            o.select_set(False)
        body.select_set(True)
        arm.select_set(True)
        bpy.context.view_layer.objects.active = arm
        with bpy.context.temp_override(active_object=arm, object=arm, selected_objects=[body, arm],
                                       selected_editable_objects=[body, arm]):
            bpy.ops.object.parent_set(type="ARMATURE_AUTO")
        for b in ad.bones:
            b.use_deform = True
        # parts: rigid or split weights
        for o, w in self.parts + self.glow:
            self._weight(o, w)
        # join into Body + Glow_<hex> meshes
        parts = [o for o, _ in self.parts]
        main = self._join([body] + parts, "Body")
        glows = {}
        for o, _ in self.glow:
            hexs = getattr(o, "glow_hex", None) or o.get("glow_hex", "ffc840")
            glows.setdefault(hexs, []).append(o)
        self.glowobjs = {}
        for hexs, objs in glows.items():
            g = self._join(objs, "Glow_" + hexs)
            self.glowobjs[hexs] = g
        for o in [main] + list(self.glowobjs.values()):
            o.parent = arm
            mod = o.modifiers.get("Armature") or o.modifiers.new("Armature", "ARMATURE")
            mod.object = arm
        self.main = main
        return arm

    def _weight(self, o, w):
        bones = set(self.J.keys())
        if isinstance(w, str):
            g = o.vertex_groups.new(name=w)
            g.add([v.index for v in o.data.vertices], 1.0, "REPLACE")
            return
        groups = {}
        for v in o.data.vertices:
            for b, x in w(v.co).items():
                if b not in bones or x <= 0:
                    continue
                if b not in groups:
                    groups[b] = o.vertex_groups.new(name=b)
                groups[b].add([v.index], x, "REPLACE")

    def _join(self, objs, name):
        objs = [o for o in objs if o is not None]
        if len(objs) > 1:
            for o in bpy.context.view_layer.objects:
                o.select_set(False)
            for o in objs:
                o.select_set(True)
            bpy.context.view_layer.objects.active = objs[0]
            with bpy.context.temp_override(active_object=objs[0], selected_editable_objects=objs, selected_objects=objs):
                bpy.ops.object.join()
        objs[0].name = name
        objs[0].data.name = name
        return objs[0]

    def bounds(self):
        pts = [o.matrix_world @ Vector(c) for o in self.coll.objects if o.type == "MESH" for c in o.bound_box]
        mn = Vector([min(p[i] for p in pts) for i in range(3)])
        mx = Vector([max(p[i] for p in pts) for i in range(3)])
        return mn, mx

    # ---------------- animation keys
    def new_action(self, name, frames, loop):
        arm = self.arm
        if arm.animation_data is None:
            arm.animation_data_create()
        old = bpy.data.actions.get(name)
        if old:
            bpy.data.actions.remove(old)
        act = bpy.data.actions.new(name)
        act.use_fake_user = True
        arm.animation_data.action = act
        self.rest_pose()
        self.clips[name] = (frames, loop)
        return act

    def rest_pose(self):
        for pb in self.arm.pose.bones:
            pb.rotation_quaternion = (1, 0, 0, 0)
            pb.location = (0, 0, 0)

    def key(self, bone, f, rot=None, loc=None):
        """rot = (pitch, yaw, roll) degrees in armature axes (pitch about +X: nose down; yaw about +Z;
        roll about +Y), relative to the parent; loc = armature-axis offset."""
        if bone not in self.arm.pose.bones:
            return
        pb = self.arm.pose.bones[bone]
        R0 = self.arm.data.bones[bone].matrix_local.to_quaternion()
        if rot is not None:
            pb.rotation_quaternion = R0.inverted() @ Rq(*rot) @ R0
            pb.keyframe_insert("rotation_quaternion", frame=f, group=bone)
        if loc is not None:
            pb.location = R0.inverted() @ Vector(loc)
            pb.keyframe_insert("location", frame=f, group=bone)

    def fcurves(self):
        ad = self.arm.animation_data
        cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
        return cb.fcurves if cb else []

    def finish(self, loop=None):
        name = self.arm.animation_data.action.name
        n, lp = self.clips[name]
        loop = lp if loop is None else loop
        for fc in self.fcurves():
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
            if loop and not any(m.type == "CYCLES" for m in fc.modifiers):
                fc.modifiers.new("CYCLES")
            fc.update()
        act = self.arm.animation_data.action
        act.frame_range = (0, n)
        act.use_frame_range = True

    def set_action(self, name):
        self.rest_pose()
        act = bpy.data.actions[name]
        self.arm.animation_data.action = act
        if self.arm.animation_data.action_slot is None and act.slots:
            self.arm.animation_data.action_slot = act.slots[0]

    # planted-foot solve for single-bone legs (foot = joint x/y at ground in rest)
    def solve_leg(self, leg, f, T, foot_z=0.0):
        arm = self.arm
        pb = arm.pose.bones[leg]
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)
        bpy.context.view_layer.update()
        P = pb.head.copy()
        par = pb.parent
        Rp = par.matrix.to_quaternion() @ arm.data.bones[par.name].matrix_local.to_quaternion().inverted()
        h = self.J[leg].z - foot_z
        d = Vector(T) - P
        Qw = Vector((0, 0, -1)).rotation_difference(d.normalized())
        R0 = arm.data.bones[leg].matrix_local.to_quaternion()
        pb.rotation_quaternion = R0.inverted() @ (Rp.inverted() @ Qw) @ R0
        pb.location = R0.inverted() @ (Rp.inverted() @ (d.normalized() * (d.length - h)))
        pb.keyframe_insert("rotation_quaternion", frame=f, group=leg)
        pb.keyframe_insert("location", frame=f, group=leg)

    def foot_world(self, leg, foot_z=0.0):
        pb = self.arm.pose.bones[leg]
        rest = self.arm.data.bones[leg].matrix_local
        return (pb.matrix @ rest.inverted()) @ Vector((self.J[leg].x, self.J[leg].y, foot_z))

    def bake_bezier_now(self):
        for fc in self.fcurves():
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
            if not any(m.type == "CYCLES" for m in fc.modifiers):
                fc.modifiers.new("CYCLES")
            fc.update()


def Rq(pitch=0.0, yaw=0.0, roll=0.0):
    return (Quaternion((0, 0, 1), math.radians(yaw)) @ Quaternion((1, 0, 0), math.radians(pitch))
            @ Quaternion((0, 1, 0), math.radians(roll)))


def wave(f, n, phase=0.0, cycles=1):
    return math.sin(2 * math.pi * (cycles * f / n + phase))


def cwave(f, n, phase=0.0, cycles=1):
    return math.cos(2 * math.pi * (cycles * f / n + phase))


# ------------------------------------------------------------------ locomotion generators
def gait_target(k, leg, f, n, offset, stride_half, lift, duty=0.5, foot_z=0.0):
    """Foot path: planted + sweeping back at constant speed for `duty` of the cycle, eased swing forward."""
    t = ((f / n) + offset) % 1.0
    S = stride_half
    if t < duty:
        y, z = -S + 2 * S * (t / duty), foot_z
    else:
        u = (t - duty) / (1 - duty)
        y = S - 2 * S * (0.5 - 0.5 * math.cos(math.pi * u))
        z = foot_z + lift * math.sin(math.pi * u)
    return Vector((k.J[leg].x, k.J[leg].y + y, z))


def walk_cycle(k, n, legs, stride_half, lift, body_keys, duty=0.5, step=2):
    """legs: [(bone, phase_offset)]; body_keys(f) keys everything else (called every `step` frames).
    Returns the stride (distance per cycle) for CreatureClips."""
    k.new_action("walk", n, True)
    for f in range(0, n + 1, step):
        body_keys(f)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg, off in legs:
            k.solve_leg(leg, f, gait_target(k, leg, f, n, off, stride_half, lift, duty))
    k.finish()
    k.meta["walk_cycle"] = n
    # stride: body travel per cycle = planted sweep / duty
    return (2 * stride_half) / duty


def hold_legs(k, f, legs, foot_z=0.0):
    """Key legs so the feet stay planted at their rest spots under the current body pose (idles/acts)."""
    bpy.context.scene.frame_set(f)
    for leg in legs:
        k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, foot_z)))


def planted_legs_pass(k, n, legs, step=2):
    """After body keys of an idle/act: re-solve the legs every `step` frames so the feet never slide."""
    k.bake_bezier_now() if k.clips[k.arm.animation_data.action.name][1] else None
    for f in range(0, n + 1, step):
        hold_legs(k, f, legs)


# ------------------------------------------------------------------ audits
def audit(k):
    sc = bpy.context.scene
    rep = {}
    for name, (n, loop) in k.clips.items():
        k.set_action(name)
        r = {"linear": sum(1 for fc in k.fcurves() for kp in fc.keyframe_points if kp.interpolation == "LINEAR")}
        mesh_keys = [o.name for o in k.coll.objects if o.type == "MESH" and o.animation_data and o.animation_data.action]
        if mesh_keys:
            r["mesh_keys"] = mesh_keys
        if loop:
            sc.frame_set(0)
            a = {pb.name: pb.matrix.copy() for pb in k.arm.pose.bones}
            sc.frame_set(n)
            b = {pb.name: pb.matrix.copy() for pb in k.arm.pose.bones}
            r["loop_pos"] = round(max((a[x].translation - b[x].translation).length for x in a), 6)
            r["loop_rot"] = round(max(math.degrees(a[x].to_quaternion().rotation_difference(b[x].to_quaternion()).angle)
                                      for x in a), 4)
        if name == "walk" and k.meta.get("legs"):
            dev, hv = 0.0, 0.0
            duty = k.meta.get("duty", 0.5)
            for leg, off in k.meta["legs"]:
                pts = []
                for f in range(n + 1):
                    t = ((f / n) + off) % 1.0
                    if t < duty:
                        sc.frame_set(f)
                        pts.append((t, k.foot_world(leg)))
                pts.sort(key=lambda x: x[0])
                if len(pts) > 2:
                    t0, p0 = pts[0]
                    t1, p1 = pts[-1]
                    for t, p in pts:
                        exp = p0.y + (p1.y - p0.y) * (t - t0) / max(t1 - t0, 1e-6)
                        dev = max(dev, abs(p.y - exp), abs(p.x - p0.x))
                    hv = max(hv, max(p.z for _, p in pts) - min(p.z for _, p in pts))
            r["slide"] = round(dev, 4)
            r["foot_z_var"] = round(hv, 4)
        if name == "idle" and k.meta.get("planted"):
            sc.frame_set(0)
            p0 = {leg: k.foot_world(leg) for leg in k.meta["planted"]}
            drift = 0.0
            for f in range(0, n + 1, 3):
                sc.frame_set(f)
                for leg in k.meta["planted"]:
                    drift = max(drift, (k.foot_world(leg) - p0[leg]).length)
            r["idle_foot_drift"] = round(drift, 4)
        rep[name] = r
    return rep


# ------------------------------------------------------------------ sample -> CreatureClips JSON
def rq(q):
    return (-q.x, q.z, q.y, q.w)


def rv(v):
    return (-v.x, v.z, v.y)


def sample(k):
    sc = bpy.context.scene
    arm = k.arm
    bones = [b.name for b in arm.data.bones if b.name != "Root"]
    parent = {b.name: (b.parent.name if b.parent else "Root") for b in arm.data.bones}
    rest = {b: arm.data.bones[b].matrix_local for b in bones}
    R0q = {b: rest[b].to_quaternion() for b in bones}
    P0 = {b: rest[b].translation.copy() for b in bones}
    P0["Root"] = k.J["Root"]
    QI = Quaternion()
    out = {}
    for name, (n, loop) in k.clips.items():
        k.set_action(name)
        frames = []
        for f in (range(n) if loop else range(n + 1)):
            sc.frame_set(f)
            W = {"Root": (QI, k.J["Root"])}
            for b in bones:
                m = arm.pose.bones[b].matrix
                W[b] = (m.to_quaternion() @ R0q[b].inverted(), m.translation.copy())
            fr = {}
            for b in bones:
                Bq, P = W[b]
                Bpq, Pp = W[parent[b]]
                fr[b] = ((Bpq.inverted() @ Bq).normalized(), Bpq.inverted() @ (P - Pp) - (P0[b] - P0[parent[b]]))
            frames.append(fr)
        rot, pos, big = {}, {}, 0.0
        for b in bones:
            seq, moving = [], False
            for fr in frames:
                q = fr[b][0]
                if q.w < 0:
                    q = -q
                if abs(q.w) < 0.99999:
                    moving = True
                seq.extend(round(c, 5) for c in rq(q))
            if moving:
                rot[b] = seq
            vs = [fr[b][1] for fr in frames]
            if max(v.length for v in vs) > 1e-4:
                pos[b] = [round(c, 5) for v in vs for c in rv(v)]
                big = max(big, max(abs(c) for c in pos[b]))
        out[name] = {"n": len(frames), "loop": loop, "len": round(n / FPS, 4), "rot": rot, "pos": pos,
                     "ps": round(big * 1.05 + 1e-4, 5)}
    return out


ALPHA = "".join(chr(c) for c in range(33, 127) if c not in (34, 92))
B92 = len(ALPHA)
LEVELS = B92 * B92 - 1


def enc(v):
    v = max(-1.0, min(1.0, v))
    i = round((v + 1) / 2 * LEVELS)
    return ALPHA[i // B92] + ALPHA[i % B92]


def pack_q(seq):
    out = []
    for i in range(0, len(seq), 4):
        x, y, z, w = seq[i:i + 4]
        if w < 0:
            x, y, z = -x, -y, -z
        out.append(enc(x) + enc(y) + enc(z))
    return "".join(out)


def write_clips(k, data, stride):
    if "walk" in data:
        data["walk"]["stride"] = round(stride or 0, 4)
    ref = "Head" if "Head" in k.J else next(iter(k.P))
    js = {"name": k.name, "fps": FPS, "ref": {"bone": ref, "dist": round((k.J[ref] - k.J["Root"]).length, 5)},
          "clips": data, "events": k.events}
    with open(os.path.join(k.dir, k.name + ".json"), "w") as fh:
        json.dump(js, fh, separators=(",", ":"))
    L = [f"-- generated by PetsV2/petkit.py ({k.name}). Do not edit by hand.", "return {",
         f'\tfps = {FPS}, rig = "cd", style = "v2",', f'\tref = {{bone = "{ref}", dist = {js["ref"]["dist"]:.5f}}},',
         "\tclips = {"]
    for cn, c in data.items():
        L.append(f'\t\t{cn} = {{n = {c["n"]}, loop = {"true" if c["loop"] else "false"}, len = {c["len"]:.3f}, '
                 f'stride = {c.get("stride", 0):.4f}, ps = {c["ps"]:.5f},')
        L.append("\t\t\trot = {")
        for b, seq in c["rot"].items():
            L.append(f'\t\t\t\t["{b}"] = "{pack_q(seq)}",')
        L.append("\t\t\t},")
        if c["pos"]:
            L.append("\t\t\tpos = {")
            for b, seq in c["pos"].items():
                L.append(f'\t\t\t\t["{b}"] = "' + "".join(enc(v / c["ps"]) for v in seq) + '",')
            L.append("\t\t\t},")
        L.append("\t\t},")
    L.append("\t},")
    if k.events:
        ev = ", ".join(f'{c} = {{' + ", ".join(f"{e} = {v:.3f}" for e, v in d.items()) + "}" for c, d in k.events.items())
        L.append("\tevents = {" + ev + "},")
    else:
        L.append("\tevents = {},")
    L.append("}")
    src = "\n".join(L)
    with open(os.path.join(k.dir, k.name + ".lua"), "w", encoding="utf-8") as fh:
        fh.write(src)
    return len(src)


# ------------------------------------------------------------------ bake + export
def bake_and_export(k, tex=1024):
    import numpy as np
    sc = bpy.context.scene
    arm = k.arm
    arm.data.pose_position = "REST"
    bpy.context.view_layer.update()
    body = k.main
    old_engine = sc.render.engine
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    me = body.data
    if not me.uv_layers:
        me.uv_layers.new(name="UVMap")
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.01)
    bpy.ops.object.mode_set(mode="OBJECT")
    col_img = bpy.data.images.new(k.name + "_col", tex, tex)
    ao_img = bpy.data.images.new(k.name + "_ao", tex, tex)
    bm_ = bpy.data.materials.new("BakeMat")
    bm_.use_nodes = True
    nt = bm_.node_tree
    nt.nodes.clear()
    outn = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    vc = nt.nodes.new("ShaderNodeVertexColor")
    vc.layer_name = "Col"
    nt.links.new(vc.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs["Emission"], outn.inputs["Surface"])
    imgn = nt.nodes.new("ShaderNodeTexImage")
    nt.nodes.active = imgn
    me.materials.clear()
    me.materials.append(bm_)
    hidden = []
    for o in bpy.context.view_layer.objects:
        if o is not body and o.type == "MESH" and not o.hide_render:
            o.hide_render = True
            hidden.append(o)
    sc.cycles.samples = 16
    imgn.image = col_img
    bpy.ops.object.bake(type="EMIT", margin=6)
    sc.cycles.samples = 64
    imgn.image = ao_img
    if sc.world:
        sc.world.light_settings.distance = 0.6
    bpy.ops.object.bake(type="AO", margin=6)
    for o in hidden:
        o.hide_render = False
    c = np.array(col_img.pixels[:], dtype=np.float32).reshape(-1, 4)
    a = np.array(ao_img.pixels[:], dtype=np.float32).reshape(-1, 4)[:, :1]
    rgb = np.clip(c[:, :3] * (0.72 + 0.28 * a), 0, 1)
    final = bpy.data.images.new(k.name + "_tex", tex, tex)
    final.pixels[:] = np.concatenate([rgb, np.ones((rgb.shape[0], 1), np.float32)], axis=1).ravel().tolist()
    path = os.path.join(k.dir, k.name + "_tex.png")
    final.filepath_raw = path
    final.file_format = "PNG"
    final.save()
    fm = bpy.data.materials.new(k.name + "_Body")
    fm.use_nodes = True
    fnt = fm.node_tree
    fnt.nodes.clear()
    fo = fnt.nodes.new("ShaderNodeOutputMaterial")
    pb = fnt.nodes.new("ShaderNodeBsdfPrincipled")
    ti = fnt.nodes.new("ShaderNodeTexImage")
    ti.image = bpy.data.images.load(path, check_existing=True)
    fnt.links.new(ti.outputs["Color"], pb.inputs["Base Color"])
    fnt.links.new(pb.outputs["BSDF"], fo.inputs["Surface"])
    me.materials.clear()
    me.materials.append(fm)
    bpy.data.materials.remove(bm_)
    for hexs, g in k.glowobjs.items():
        gm = bpy.data.materials.new("Glow_" + hexs)
        rgb_ = tuple(int(hexs[i:i + 2], 16) for i in (0, 2, 4))
        gm.diffuse_color = lin(rgb_)
        g.data.materials.clear()
        g.data.materials.append(gm)
    sc.render.engine = old_engine
    os.makedirs(IMP, exist_ok=True)
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    sel = [arm, body] + list(k.glowobjs.values())
    for o in sel:
        o.select_set(True)
    bpy.context.view_layer.objects.active = arm
    fbx = os.path.join(IMP, k.name + ".fbx")
    bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, add_leaf_bones=False, bake_anim=False, path_mode="COPY",
                             embed_textures=True, object_types={"ARMATURE", "MESH"}, mesh_smooth_type="FACE")
    arm.data.pose_position = "POSE"
    return {"fbx": fbx, "tex": path, "kb": round(os.path.getsize(fbx) / 1024)}


# ------------------------------------------------------------------ preview stage + renders
def stage(k, ground=True):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    w = sc.world or bpy.data.worlds.new("World")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.62, 0.74, 0.92, 1)
    bg.inputs["Strength"].default_value = 0.9
    st = bpy.data.collections.get("Stage") or bpy.data.collections.new("Stage")
    if st.name not in sc.collection.children:
        sc.collection.children.link(st)
    for o in list(st.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    if ground:
        gme = bpy.data.meshes.new("Ground")
        bm = bmesh.new()
        bmesh.ops.create_circle(bm, cap_ends=True, radius=8, segments=48)
        bm.to_mesh(gme)
        bm.free()
        gm = bpy.data.materials.new("GroundMat")
        gm.use_nodes = True
        gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.55, 0.78, 0.45, 1)
        gme.materials.append(gm)
        st.objects.link(bpy.data.objects.new("Ground", gme))

    def light(name, kind, loc, energy, rot, size=1.0, color=(1, 1, 1)):
        ld = bpy.data.lights.new(name, kind)
        ld.energy, ld.color = energy, color
        if kind == "AREA":
            ld.size = size
        if kind == "SUN":
            ld.angle = math.radians(8)
        lo = bpy.data.objects.new(name, ld)
        lo.location, lo.rotation_euler = loc, rot
        st.objects.link(lo)
    light("Key", "SUN", (3, -4, 6), 3.2, (math.radians(50), 0, math.radians(35)), color=(1, 0.97, 0.92))
    light("Fill", "AREA", (-4, -3, 2.5), 350, (math.radians(70), 0, math.radians(-55)), 4, (0.85, 0.9, 1))
    light("Rim", "AREA", (0, 4.5, 3.5), 400, (math.radians(-55), 0, math.radians(180)), 3, (1, 0.95, 0.85))
    cd = bpy.data.cameras.new("Cam")
    cd.lens = 70
    cam = bpy.data.objects.new("Cam", cd)
    st.objects.link(cam)
    sc.camera = cam
    return cam


def aim(cam, loc, target):
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


VIEWS = {"tq": (1.0, -1.36, 0.62), "side": (1.0, 0.02, 0.18), "front": (0.0, -1.0, 0.2), "back": (-0.62, 1.0, 0.5)}


def camera_for(k, view, dist=None):
    mn, mx = k.bounds()
    c = (mn + mx) / 2
    size = max((mx - mn).length, 2.0)
    d = Vector(VIEWS[view]).normalized() * (dist or size * 1.75)
    return c + d, c


def shots(k, prefix, views=("tq", "side", "front", "back"), res=420, frame=None, action=None):
    sc = bpy.context.scene
    cam = sc.camera
    sc.render.resolution_x = sc.render.resolution_y = res
    if action and getattr(k, "arm", None):
        k.set_action(action)
    if frame is not None:
        sc.frame_set(frame)
    files = []
    for v in views:
        loc, tgt = camera_for(k, v)
        aim(cam, loc, tgt)
        p = os.path.join(k.dir, "renders", f"{prefix}_{v}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        files.append(p)
    return files


def sheet(files, out, cols=None, cell=300, labels=None):
    """Contact sheet with Pillow (runs in Blender's Python only if PIL exists; else returns None)."""
    try:
        from PIL import Image, ImageDraw
    except Exception:
        return None
    cols = cols or len(files)
    rows = (len(files) + cols - 1) // cols
    im = Image.new("RGB", (cols * cell, rows * cell), "white")
    d = ImageDraw.Draw(im)
    for i, f in enumerate(files):
        x, y = (i % cols) * cell, (i // cols) * cell
        im.paste(Image.open(f).convert("RGB").resize((cell, cell)), (x, y))
        if labels:
            d.text((x + 5, y + 4), labels[i], fill=(0, 0, 0))
    im.save(out)
    return out


def pose_renders(k, picks, view="tq", res=300):
    """picks: [(action, frame)] -> list of png paths"""
    sc = bpy.context.scene
    cam = sc.camera
    sc.render.resolution_x = sc.render.resolution_y = res
    k.set_action("idle")
    sc.frame_set(0)
    loc, tgt = camera_for(k, view)
    aim(cam, loc, tgt)
    files = []
    for act, f in picks:
        k.set_action(act)
        sc.frame_set(f)
        p = os.path.join(k.dir, "renders", f"pose_{view}_{act}_{f:02d}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        files.append(p)
    return files


def gif_frames(k, action, step=1, res=360, view="tq", lift=0.0):
    sc = bpy.context.scene
    cam = sc.camera
    sc.render.resolution_x = sc.render.resolution_y = res
    k.set_action("idle")
    sc.frame_set(0)
    loc, tgt = camera_for(k, view)
    tgt = tgt + Vector((0, 0, lift))
    aim(cam, loc + Vector((0, 0, lift)), tgt)
    n, loop = k.clips[action]
    d = os.path.join(k.dir, "renders", "gif", action)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    k.set_action(action)
    i = 0
    for f in range(0, n if loop else n + 1, step):
        sc.frame_set(f)
        sc.render.filepath = os.path.join(d, f"f{i:03d}.png")
        bpy.ops.render.render(write_still=True)
        i += 1
    return d, i


def portrait(k, res=512, action="idle", frame=0):
    sc = bpy.context.scene
    st = bpy.data.collections.get("Stage")
    ground = bpy.data.objects.get("Ground")
    if ground:
        ground.hide_render = True
    sc.render.film_transparent = True
    sc.render.resolution_x = sc.render.resolution_y = res
    # glow parts: emissive gold-ish for the picture
    olds = {}
    for hexs, g in getattr(k, "glowobjs", {}).items():
        gm = bpy.data.materials.new("PortraitGlow_" + hexs)
        gm.use_nodes = True
        p = gm.node_tree.nodes["Principled BSDF"]
        c = lin(tuple(int(hexs[i:i + 2], 16) for i in (0, 2, 4)))
        p.inputs["Base Color"].default_value = c
        p.inputs["Emission Color"].default_value = c
        p.inputs["Emission Strength"].default_value = 1.2
        olds[g] = list(g.data.materials)
        g.data.materials.clear()
        g.data.materials.append(gm)
    k.set_action(action)
    sc.frame_set(frame)
    cam = sc.camera
    loc, tgt = camera_for(k, "tq")
    aim(cam, loc, tgt)
    p = os.path.join(k.dir, k.name + "_portrait_raw.png")
    sc.render.filepath = p
    sc.render.image_settings.color_mode = "RGBA"
    bpy.ops.render.render(write_still=True)
    for g, mats in olds.items():
        g.data.materials.clear()
        for m in mats:
            g.data.materials.append(m)
    sc.render.film_transparent = False
    sc.render.image_settings.color_mode = "RGB"
    if ground:
        ground.hide_render = False
    return p


# ------------------------------------------------------------------ wings
def membrane_wing(k, side, S, W, tips, B, bone_arm, bone_tip, c_root, c_edge, c_bone, scallop=0.22,
                  arm_r=0.06, finger_r=0.035, claw=None, thick=0.012, attach_bone="Spine"):
    """Bat/dragon wing. S shoulder, W wrist, tips = finger tips (front -> back), B = rear attach on the body.
    Membrane between fingers is scalloped toward the wrist; double-sided; colour root -> edge by distance."""
    S, W, B = Vector(S), Vector(W), Vector(B)
    tips = [Vector(t) for t in tips]
    rays = tips + [B]
    # membrane normal (for thickness + scallop direction)
    nrm = (tips[0] - W).cross(B - W).normalized()
    reach = max((t - W).length for t in rays)

    def edge(i, t):
        a, b = rays[i], rays[i + 1]
        p = a.lerp(b, t)
        toward = (W - p)
        return p + toward * (scallop * math.sin(math.pi * t))

    def build(bm, L):
        grids = []
        R, A = 6, 5
        for i in range(len(rays) - 1):  # finger sectors around the wrist
            g = [[W.lerp(edge(i, t / A), s / R) for t in range(A + 1)] for s in range(R + 1)]
            grids.append(g)
        g = [[S.lerp(W.lerp(B, t / A), s / R) for t in range(A + 1)] for s in range(R + 1)]  # arm sector
        grids.append(g)
        for g in grids:
            for side_off, flip in ((thick, False), (-thick, True)):
                vs = [[None] * len(g[0]) for _ in g]
                for a_ in range(len(g)):
                    for b_ in range(len(g[0])):
                        p = g[a_][b_] + nrm * side_off
                        v = bm.verts.new(p)
                        d = (g[a_][b_] - W).length / reach
                        v[L] = mix(c_root, c_edge, smooth(0.15, 0.95, d))
                        vs[a_][b_] = v
                for a_ in range(len(g) - 1):
                    for b_ in range(len(g[0]) - 1):
                        q = (vs[a_][b_], vs[a_ + 1][b_], vs[a_ + 1][b_ + 1], vs[a_][b_ + 1])
                        try:
                            bm.faces.new(tuple(reversed(q)) if flip else q)
                        except ValueError:
                            pass
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
        tube(bm, L, [S, S.lerp(W, 0.5) + nrm * 0.02, W], (arm_r, arm_r * 0.75), c_bone, 8)
        for t in tips:
            tube(bm, L, [W, W.lerp(t, 0.5) + nrm * 0.01, t], (finger_r, finger_r * 0.4), c_bone, 6)
        if claw:
            cone(bm, L, W, (W - S).normalized() + nrm * 0.3, 0.14, arm_r * 0.9, claw)

    def weights(co):
        co = Vector(co)
        s = (co - W).length / reach
        along = (co - S).dot((W - S).normalized()) / max((W - S).length, 1e-6)
        wtip = smooth(-0.05, 0.25, s) * smooth(0.55, 1.0, along + 0.4 * s)
        nearB = smooth(0.32, 0.08, (co - B).length)
        w = {bone_tip: wtip, bone_arm: max(0.0, 1 - wtip)}
        if nearB > 0:
            w = {b: x * (1 - nearB) for b, x in w.items()}
            w[attach_bone] = nearB
        return w
    return k.part("Wing_" + side, build, weights)


def feather_wing(k, side, root, arm_dir, span, bone_arm, bone_tip, c_root, c_mid, c_tip, glow_trim=None,
                 n_prim=5, n_sec=6, n_cov=7, prim_len=(0.82, 1.02), sec_len=0.64, cov_len=0.34, width=0.15,
                 back_down=(0, 0.55, -0.85), arc=0.16):
    """Angel/bird wing (Cvetibara recipe): coverts, secondaries, primaries fanned along an arcing arm."""
    sx = 1 if side == "L" else -1
    root = Vector(root)
    arm = Vector(arm_dir).normalized()
    bd = Vector(back_down)
    e2 = (bd - arm * bd.dot(arm)).normalized()
    nrm = arm.cross(e2) * sx

    def arm_point(u):
        return root + arm * span * u + Vector((0, 0, arc)) * math.sin(math.pi * u)

    def fdir(theta):
        th = math.radians(theta)
        return e2 * math.cos(th) + arm * math.sin(th)

    def feather(bm, L, m, length, w, th, curl, root_c, tip_c, tip_from):
        def deform(u):
            t = (u.x + 1) * 0.5
            prof = math.sin(math.pi * min(t, 0.999) ** 0.8) ** 0.75
            return Vector((t * length, u.y * w * prof, u.z * th * prof - curl * length * t * t))

        def color(u, lc):
            t = (u.x + 1) * 0.5
            return mix(mix(root_c, c_mid, smooth(0.0, 0.35, t)), tip_c, smooth(tip_from, 0.98, t))
        blob(bm, L, m, deform, color, 10, 6)

    def build(bm, L):
        for i in range(n_prim):
            u = 0.5 + 0.5 * i / max(n_prim - 1, 1)
            feather(bm, L, frame(arm_point(u) - nrm * 0.03, fdir(28 + 56 * i / max(n_prim - 1, 1)), nrm),
                    prim_len[0] + (prim_len[1] - prim_len[0]) * i / max(n_prim - 1, 1), width, 0.05, 0.10, c_root,
                    c_tip, 0.62)
        for i in range(n_sec):
            u = 0.05 + 0.52 * i / max(n_sec - 1, 1)
            feather(bm, L, frame(arm_point(u) - nrm * 0.01, fdir(6 + 24 * i / max(n_sec - 1, 1)), nrm), sec_len,
                    width, 0.05, 0.10, c_root, c_tip, 0.7)
        for i in range(n_cov):
            u = 0.03 + 0.92 * i / max(n_cov - 1, 1)
            feather(bm, L, frame(arm_point(u) + nrm * 0.03, fdir(12 + 42 * i / max(n_cov - 1, 1)), nrm), cov_len,
                    width * 0.93, 0.05, 0.05, c_root, c_mid, 0.99)

    def weights(co):
        u = (Vector(co) - root).dot(arm) / span
        t = smooth(0.38, 0.62, u)
        return {bone_arm: 1 - t, bone_tip: t}
    w = k.part("Wing_" + side, build, weights)
    if glow_trim:
        def trim(bm, L):
            tube(bm, L, [arm_point(i / 16) for i in range(17)], (0.06, 0.035), glow_trim[1], 8)
            ellipsoid(bm, L, arm_point(1.0) + arm * 0.03, (0.065, 0.065, 0.065), glow_trim[1], useg=10, vseg=6)
        g = k.part("Glow_WingTrim_" + side, trim, weights, glow=True)
        g["glow_hex"] = glow_trim[0]
    return w, arm_point


def glow_part(k, name, hexs, build, weights):
    g = k.part(name, build, weights, glow=True)
    g["glow_hex"] = hexs
    return g


# ------------------------------------------------------------------ cloth / armour helpers (2026-10-08, Pharaoh Asparuh)
def strip(bm, L, pts, width, normal, color, thick=0.025, side_hint=None):
    """Flat ribbon (closed box section) along pts. width = number | callable(t); normal = vector | callable(t)
    (the ribbon's face normal); color = rgba | callable(t, s) with s in [-1, 1] across the width."""
    pts = [Vector(p) for p in pts]
    n = len(pts)
    rings = []
    for i, p in enumerate(pts):
        t = i / (n - 1)
        d = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        nr = Vector(normal(t) if callable(normal) else normal)
        nr = (nr - d * nr.dot(d)).normalized()
        s = d.cross(nr).normalized()
        w = (width(t) if callable(width) else width) / 2
        ring = []
        for (a, b) in ((-1, 1), (1, 1), (1, -1), (-1, -1)):
            v = bm.verts.new(p + s * w * a + nr * thick * 0.5 * b)
            v[L] = color(t, a) if callable(color) else color
            ring.append(v)
        rings.append(ring)
    for i in range(n - 1):
        for j in range(4):
            bm.faces.new((rings[i][j], rings[i][(j + 1) % 4], rings[i + 1][(j + 1) % 4], rings[i + 1][j]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])


def shell_cap(bm, L, center, radii, theta_max, color, thick=0.03, nu=40, nv=14, x_axis=(1, 0, 0), z_axis=(0, 0, 1),
              flare=None):
    """Closed shell over the top of an ellipsoid (helmet / headdress), in frame(center, x_axis, z_axis).
    theta_max(phi): how far down from the local +Z pole it reaches at azimuth phi (phi = 0 toward local +Y).
    color(r, phi, outer) -> rgba, r = 0 (pole) .. 1 (rim). Every row of quads gets its own vertices so colour
    bands stay crisp (no smeared stripes). flare(r, phi) -> (horizontal scale, extra drop) to flare the rim out."""
    m = frame(center, x_axis, z_axis)

    def pt(i, r, sc):
        phi = 2 * math.pi * i / nu
        th = theta_max(phi) * r
        fh, dz = flare(r, phi) if flare else (1.0, 0.0)
        return m @ (Vector((radii[0] * math.sin(th) * math.sin(phi) * fh, radii[1] * math.sin(th) * math.cos(phi) * fh,
                            radii[2] * math.cos(th) - dz)) * sc)
    for outer, sc in ((True, 1.0), (False, 1.0 - thick / max(radii))):
        for j in range(nv):
            r0, r1 = j / nv, (j + 1) / nv
            rows = []
            for r in (r0, r1):
                row = []
                for i in range(nu):
                    v = bm.verts.new(pt(i, r, sc))
                    v[L] = color((r0 + r1) / 2, 2 * math.pi * i / nu, outer)
                    row.append(v)
                rows.append(row)
            for i in range(nu):
                i2 = (i + 1) % nu
                q = (rows[0][i], rows[1][i], rows[1][i2], rows[0][i2])
                bm.faces.new(q if outer else tuple(reversed(q)))
    # rim
    ro, ri = [], []
    for i in range(nu):
        a = bm.verts.new(pt(i, 1.0, 1.0))
        b = bm.verts.new(pt(i, 1.0, 1.0 - thick / max(radii)))
        a[L] = b[L] = color(1.0, 2 * math.pi * i / nu, True)
        ro.append(a)
        ri.append(b)
    for i in range(nu):
        i2 = (i + 1) % nu
        bm.faces.new((ro[i], ri[i], ri[i2], ro[i2]))


def ear(bm, L, base, up, fwd, length, width, thick, color, bend=0.0):
    """Flat-ish triangular ear (cat/fox): base point, up direction, fwd = the ear's front normal.
    color(h, s) with h in [0, 1] base->tip, s across."""
    up = Vector(up).normalized()
    f = Vector(fwd)
    f = (f - up * f.dot(up)).normalized()
    side = up.cross(f).normalized()

    def deform(u):
        h = (u.z + 1) / 2
        w = width * (1 - h) ** 0.85 + 0.01
        cup = -0.35 * thick * (1 - u.x * u.x) * (1 - h)
        return side * (u.x * w) + f * (u.y * thick + cup) + up * (h * length) + f * (bend * h * h)

    res = bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=1.0)
    for v in res["verts"]:
        u = v.co.copy()
        v.co = Vector(base) + deform(u)
        v[L] = color((u.z + 1) / 2, u.x, u.y) if callable(color) else color
