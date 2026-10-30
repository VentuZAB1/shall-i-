# blockkit: Steal-an-Egg style pets for SLINGSHOT (PetsV3, 2026-10-08).
# Style rules (from the user's 25+ reference images):
#   - built BIG: real proportions (long legs, real neck, moderate head) so a heavy KG pet looks huge, not a giant baby
#   - chunky blocks with small chamfered edges, flat shading, bright solid colours in clear zones
#   - small raised square studs scattered over the surfaces (fixed size -> they read as scale cues on big pets)
#   - small simple faces (square eyes / plates), rare pets get glow cracks, crystals, floating bits
# Every block is rigid on ONE bone (no rubbery skinning).
import math, random
import bmesh, bpy
from mathutils import Vector, Matrix, Euler
import petkit as pk

NO_GLOW = True   # user 2026-10-08: glowing (Neon) parts look ugly -> every part is a normal solid colour
FACES = {"+x": (0, 1), "-x": (0, -1), "+y": (1, 1), "-y": (1, -1), "+z": (2, 1), "-z": (2, -1)}


def rgb(c):
    return pk.lin(c) if isinstance(c, tuple) else c


class Block:
    def __init__(self, center, half, color, bone, rot=(0, 0, 0), top=(1, 1), bot=(1, 1), top_shift=(0, 0),
                 bevel=0.03, studs=None, density=0.5, glow=None, name="", R=None):
        self.c = Vector(center)
        self.h = Vector(half)
        self.color = rgb(color)
        self.bone = bone
        self.R = R.copy() if R is not None else Euler([math.radians(a) for a in rot], "XYZ").to_matrix()
        self.top, self.bot, self.ts = top, bot, top_shift
        self.bevel = bevel
        self.studs = studs          # None = all faces except -z ; [] = none ; list of face keys
        self.density = density
        self.glow = None if NO_GLOW else glow   # hex string -> Neon part
        self.name = name

    # local corner for signs (sx, sy, sz) in {-1, 1}
    def local(self, sx, sy, sz):
        sc = self.top if sz > 0 else self.bot
        sh = self.ts if sz > 0 else (0, 0)
        return Vector((sx * self.h.x * sc[0] + sh[0], sy * self.h.y * sc[1] + sh[1], sz * self.h.z))

    def world(self, p):
        return self.c + self.R @ Vector(p)

    def contains(self, p, pad=0.0):
        q = self.R.transposed() @ (Vector(p) - self.c)
        if abs(q.z) > self.h.z + pad:
            return False
        t = (q.z / self.h.z + 1) / 2 if self.h.z > 0 else 0.5
        sx = self.bot[0] + (self.top[0] - self.bot[0]) * t
        sy = self.bot[1] + (self.top[1] - self.bot[1]) * t
        ox, oy = self.ts[0] * t, self.ts[1] * t
        return abs(q.x - ox) <= self.h.x * sx + pad and abs(q.y - oy) <= self.h.y * sy + pad

    def face_corners(self, key):
        ax, s = FACES[key]
        # 4 corners of that face in a consistent (u, v) order, world space
        if ax == 2:
            cs = [(-1, -1, s), (1, -1, s), (1, 1, s), (-1, 1, s)]
        elif ax == 0:
            cs = [(s, -1, -1), (s, 1, -1), (s, 1, 1), (s, -1, 1)]
        else:
            cs = [(-1, s, -1), (1, s, -1), (1, s, 1), (-1, s, 1)]
        return [self.world(self.local(*c)) for c in cs]


class Poly:
    """thin prism through N points (fan from pts[0], so pts must be star-shaped around it): wing membranes, fins"""
    def __init__(self, pts, thick, color, bone, glow=None):
        self.pts = [Vector(p) for p in pts]
        self.thick = thick
        self.color = rgb(color)
        self.bone = bone
        self.glow = None if NO_GLOW else glow
        self.studs = []
        self.c = sum(self.pts, Vector()) / len(self.pts)

    def contains(self, p, pad=0.0):
        return False


def _poly_bm(pl):
    bm = bmesh.new()
    P = pl.pts
    n = Vector()
    for i in range(1, len(P) - 1):
        n += (P[i] - P[0]).cross(P[i + 1] - P[0])
    n.normalize()
    top = [bm.verts.new(p + n * pl.thick / 2) for p in P]
    bot = [bm.verts.new(p - n * pl.thick / 2) for p in P]
    N = len(P)
    for i in range(1, N - 1):
        bm.faces.new((top[0], top[i], top[i + 1]))
        bm.faces.new((bot[0], bot[i + 1], bot[i]))
    for i in range(N):
        j = (i + 1) % N
        bm.faces.new((top[i], bot[i], bot[j], top[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def _box_bm(blk):
    """chamfered (tapered) box in its own bmesh, world space"""
    bm = bmesh.new()
    vs = {}
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                vs[(sx, sy, sz)] = bm.verts.new(blk.world(blk.local(sx, sy, sz)))
    quads = [((-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1)),   # -z
             ((-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)),       # +z
             ((-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)),   # -y
             ((-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1)),       # +y
             ((-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1)),   # -x
             ((1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1))]       # +x
    for q in quads:
        bm.faces.new([vs[c] for c in q])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mn = min(blk.h.x * min(blk.top[0], blk.bot[0]), blk.h.y * min(blk.top[1], blk.bot[1]), blk.h.z)
    off = min(blk.bevel, mn * 0.45)
    if off > 0.004:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=off, offset_type="OFFSET", segments=1, profile=0.5,
                        affect="EDGES", clamp_overlap=True)
    return bm


def _stud(bm, L, ctr, u, v, n, a, b, hgt, color):
    """raised square tile: straight sides then a chamfered top (a, b = half extents along u, v)"""
    c = min(a, b) * 0.32
    rings = []
    for (da, db, dz) in ((a, b, -0.006), (a, b, hgt * 0.5), (a - c, b - c, hgt)):
        ring = []
        for (su, sv) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            vt = bm.verts.new(ctr + u * (su * da) + v * (sv * db) + n * dz)
            vt[L] = color
            ring.append(vt)
        rings.append(ring)
    for i in range(2):
        for j in range(4):
            bm.faces.new((rings[i][j], rings[i][(j + 1) % 4], rings[i + 1][(j + 1) % 4], rings[i + 1][j]))
    bm.faces.new(rings[2])


def frame_from(p0, p1, n):
    """rotation whose local z runs p0 -> p1 and local x is the surface normal n"""
    z = (Vector(p1) - Vector(p0)).normalized()
    x = Vector(n)
    x = (x - z * x.dot(z)).normalized()
    y = z.cross(x)
    return Matrix((x, y, z)).transposed()


class Blocks:
    def __init__(self, k, cell=0.105, stud_h=0.03, seed=7):
        self.k = k
        self.items = []
        self.cell = cell
        self.stud_h = stud_h
        self.rnd = random.Random(seed)
        self.stud_count = 0

    def add(self, *a, **kw):
        b = Block(*a, **kw)
        self.items.append(b)
        return b

    def seg(self, p0, p1, hw, hd, color, bone, side=(1, 0, 0), ext=0.0, ext1=0.0, **kw):
        """block from p0 to p1 (local z along it), half width hw (along `side`), half depth hd; ext/ext1 extend the
        start/end (to bury the ends in neighbouring parts)"""
        p0, p1 = Vector(p0), Vector(p1)
        d = (p1 - p0).normalized()
        p0, p1 = p0 - d * ext, p1 + d * ext1
        return self.add((p0 + p1) / 2, (hw, hd, (p1 - p0).length / 2), color, bone, R=frame_from(p0, p1, side), **kw)

    def poly(self, pts, thick, color, bone, glow=None):
        pl = Poly(pts, thick, color, bone, glow)
        self.items.append(pl)
        return pl

    def on_face(self, blk, key, u, v, hu, hv, thick, color, bone=None, **kw):
        """plate lying on face `key` of an (untapered) block at face coords (u, v) in local units"""
        ax, sg = FACES[key]
        h = blk.h
        if ax == 1:
            loc, half = Vector((u, sg * (h.y + thick / 2 + 0.002), v)), (hu, thick / 2, hv)
        elif ax == 0:
            loc, half = Vector((sg * (h.x + thick / 2 + 0.002), u, v)), (thick / 2, hu, hv)
        else:
            loc, half = Vector((u, v, sg * (h.z + thick / 2 + 0.002))), (hu, hv, thick / 2)
        kw.setdefault("studs", [])
        kw.setdefault("bevel", min(0.012, thick * 0.6))
        return self.add(blk.world(loc), half, color, bone or blk.bone, R=blk.R, **kw)

    def spike(self, base, direction, length, w, color, bone, side=(1, 0, 0), **kw):
        """pointed block from base along direction (horns, crystals, claws, teeth)"""
        base = Vector(base)
        tip = base + Vector(direction).normalized() * length
        kw.setdefault("studs", [])
        kw.setdefault("top", (0.12, 0.12))
        return self.add((base + tip) / 2, (w, w, length / 2), color, bone, R=frame_from(base, tip, side), **kw)

    def bar(self, p0, p1, n, width, thick, color, bone, **kw):
        """flat bar from p0 to p1 lying on a surface with normal n (thin side along n)"""
        p0, p1 = Vector(p0), Vector(p1)
        return self.add((p0 + p1) / 2, (thick, width / 2, (p1 - p0).length / 2), color, bone,
                        R=frame_from(p0, p1, n), **kw)

    def mirror(self, *a, **kw):
        """add a block for x > 0 and its mirror; rot (rx, ry, rz) flips ry, rz; bone names *_L / *_R or Leg_?L"""
        center, half, color, bone = a[0], a[1], a[2], a[3]
        rot = kw.pop("rot", (0, 0, 0))
        ts = kw.pop("top_shift", (0, 0))
        out = []
        for s, side in ((1, "L"), (-1, "R")):
            bn = bone.replace("{s}", side) if bone else bone
            out.append(self.add((s * center[0], center[1], center[2]), half, color, bn,
                                rot=(rot[0], s * rot[1], s * rot[2]), top_shift=(s * ts[0], ts[1]), **kw))
        return out

    def _studs_for(self, blk, bm, L):
        keys = blk.studs if blk.studs is not None else ["+x", "-x", "+y", "-y", "+z"]
        others = [o for o in self.items if o is not blk and not o.glow]
        cell = self.cell
        for key in keys:
            P = blk.face_corners(key)       # p0 (u-,v-), p1 (u+,v-), p2 (u+,v+), p3 (u-,v+)
            n = (P[1] - P[0]).cross(P[3] - P[0])
            if n.length < 1e-9:
                continue
            n.normalize()
            ctr = sum(P, Vector()) / 4
            if (ctr - blk.c).dot(n) < 0:
                n = -n
            lu = ((P[1] - P[0]).length + (P[2] - P[3]).length) / 2
            lv = ((P[3] - P[0]).length + (P[2] - P[1]).length) / 2
            margin = blk.bevel + cell * 0.25
            nu, nv = int((lu - 2 * margin) / cell), int((lv - 2 * margin) / cell)
            if nu < 1 or nv < 1:
                continue
            used = set()
            for i in range(nu):
                for j in range(nv):
                    if (i, j) in used or self.rnd.random() > blk.density:
                        continue
                    w = 1
                    hgt = 1
                    r = self.rnd.random()
                    if r < 0.25 and i + 1 < nu and (i + 1, j) not in used:
                        w = 2
                    elif r < 0.45 and j + 1 < nv and (i, j + 1) not in used:
                        hgt = 2
                    for di in range(-1, w + 1):
                        for dj in range(-1, hgt + 1):
                            used.add((i + di, j + dj))
                    # cell centre in (s, t) face coordinates [0, 1]
                    s0 = (margin + (i + w / 2) * cell + (lu - 2 * margin - nu * cell) / 2) / lu
                    t0 = (margin + (j + hgt / 2) * cell + (lv - 2 * margin - nv * cell) / 2) / lv
                    p = (P[0].lerp(P[1], s0)).lerp(P[3].lerp(P[2], s0), t0)
                    u = (P[1] - P[0]).lerp(P[2] - P[3], t0).normalized()
                    v = n.cross(u).normalized()
                    if any(o.contains(p + n * 0.02, pad=0.01) for o in others):
                        continue
                    a = cell * (w - 0.28) / 2
                    b = cell * (hgt - 0.28) / 2
                    _stud(bm, L, p, u, v, n, a, b, self.stud_h, blk.color)
                    self.stud_count += 1

    def _apply_head_xf(self):
        """HEAD_XF: [(pivot, scale, bones)] - grow whole head groups about their neck junction (2026-10-08 user: heads
        were far too small for the big bodies). Joints of those bones are transformed the same way (BlockPet.joint)."""
        for pivot, sc, bones in getattr(self.k, "head_xf", []):
            for blk in self.items:
                if blk.bone not in bones:
                    continue
                if isinstance(blk, Poly):
                    blk.pts = [pivot + (p - pivot) * sc for p in blk.pts]
                    blk.thick *= sc
                    blk.c = sum(blk.pts, Vector()) / len(blk.pts)
                else:
                    blk.c = pivot + (blk.c - pivot) * sc
                    blk.h = blk.h * sc
                    blk.bevel *= sc

    def build(self):
        """one rigid part per (bone, glow) -> k.parts / k.glow"""
        self._apply_head_xf()
        groups = {}
        for blk in self.items:
            groups.setdefault((blk.bone, blk.glow), []).append(blk)
        objs = []
        for (bone, glow), blks in groups.items():
            def build(bm, L, blks=blks):
                for blk in blks:
                    tmp = _poly_bm(blk) if isinstance(blk, Poly) else _box_bm(blk)
                    m = {}
                    for vt in tmp.verts:
                        nv = bm.verts.new(vt.co)
                        nv[L] = blk.color
                        m[vt] = nv
                    for f in tmp.faces:
                        try:
                            bm.faces.new([m[vt] for vt in f.verts])
                        except ValueError:
                            pass
                    tmp.free()
                    if not glow and blk.studs != [] and not isinstance(blk, Poly):
                        self._studs_for(blk, bm, L)
            name = ("G_" + glow if glow else "P") + "_" + bone
            if glow:
                o = pk.glow_part(self.k, name, glow, build, bone)
            else:
                o = self.k.part(name, build, bone, smooth_shade=False)
            if glow:
                for p in o.data.polygons:
                    p.use_smooth = False
            objs.append(o)
        return objs


def head_point(k, bone, p):
    """transform a rest-space point carried by `bone` with the pet's head scaling (identity if none)"""
    p = Vector(p)
    for pivot, sc, bones in getattr(k, "head_xf", []):
        if bone in bones:
            return pivot + (p - pivot) * sc, sc
    return p, 1.0


class BlockPet(pk.Pet):
    """Pet whose mesh is all rigid blocks: no bone-heat body, every part weighted to its own bone.
    Optional 2-bone legs: add_leg2("Leg_L", "Shin_L", "Foot_L", knee=(0, -1, 0)); then solve_leg("Leg_L", f, T)
    plants the foot (ankle above ground point T, foot kept flat) with the knee bending toward `knee`."""

    def joint(self, name, pos, parent, tail=None):
        pos, sc = head_point(self, name, pos)
        if tail is not None and sc != 1.0:
            tail = Vector(tail) * sc
        return super().joint(name, pos, parent, tail)

    def add_leg2(self, leg, shin, foot, knee=(0, -1, 0)):
        if not hasattr(self, "legs2"):
            self.legs2 = {}
        self.legs2[leg] = {"shin": shin, "foot": foot, "knee": Vector(knee)}

    def _aim(self, bone, f, q_world):
        """key `bone` so its armature-space orientation = q_world @ rest (q_world = rotation delta in armature space)"""
        arm = self.arm
        pb = arm.pose.bones[bone]
        pb.rotation_quaternion = (1, 0, 0, 0)
        bpy.context.view_layer.update()
        par = pb.parent
        Rp = par.matrix.to_quaternion() @ arm.data.bones[par.name].matrix_local.to_quaternion().inverted()
        R0 = arm.data.bones[bone].matrix_local.to_quaternion()
        pb.rotation_quaternion = R0.inverted() @ (Rp.inverted() @ q_world) @ R0
        pb.keyframe_insert("rotation_quaternion", frame=f, group=bone)
        bpy.context.view_layer.update()

    def solve_leg(self, leg, f, T, foot_z=0.0, toe=None):
        L = getattr(self, "legs2", {}).get(leg)
        if L is None:
            return super().solve_leg(leg, f, T, foot_z)
        from mathutils import Quaternion
        arm, J = self.arm, self.J
        hipR, kneeR, ankR = J[leg], J[L["shin"]], J[L["foot"]]
        L1, L2 = (kneeR - hipR).length, (ankR - kneeR).length
        T = Vector(T)
        A = Vector((T.x + ankR.x - hipR.x, T.y + ankR.y - hipR.y, T.z - foot_z + ankR.z))
        pb = arm.pose.bones[leg]
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)
        bpy.context.view_layer.update()
        H = pb.head.copy()
        par = pb.parent
        Rp = par.matrix.to_quaternion() @ arm.data.bones[par.name].matrix_local.to_quaternion().inverted()
        d = A - H
        dist = min(max(d.length, abs(L1 - L2) * 1.02 + 1e-4), (L1 + L2) * 0.999)
        dn = d.normalized()
        kd = Rp @ L["knee"]
        pole = kd - dn * kd.dot(dn)
        pole = pole.normalized() if pole.length > 1e-6 else Vector((0, -1, 0))
        ca = max(-1.0, min(1.0, (L1 * L1 + dist * dist - L2 * L2) / (2 * L1 * dist)))
        a = math.acos(ca)
        K = H + dn * math.cos(a) * L1 + pole * math.sin(a) * L1
        A2 = H + dn * dist
        self._aim(leg, f, (kneeR - hipR).rotation_difference(K - H))
        pb.keyframe_insert("location", frame=f, group=leg)
        self._aim(L["shin"], f, (ankR - kneeR).rotation_difference(A2 - K))
        lift = max(0.0, T.z - foot_z)
        tdeg = (35.0 * min(1.0, lift / 0.12)) if toe is None else toe
        self._aim(L["foot"], f, Quaternion((1, 0, 0), math.radians(tdeg)))

    def foot_world(self, leg, foot_z=0.0):
        L = getattr(self, "legs2", {}).get(leg)
        if L is None:
            return super().foot_world(leg, foot_z)
        return self.arm.matrix_world @ self.arm.pose.bones[L["foot"]].head

    def build_rig(self):
        mn, mx = self.bounds()
        self.J["Root"] = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, 0.0))
        ad = bpy.data.armatures.new("Armature")
        arm = bpy.data.objects.new("Armature", ad)
        self.coll.objects.link(arm)
        bpy.context.view_layer.update()
        for o in bpy.context.scene.objects:
            if o is not None:
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
        for o, w in self.parts + self.glow:
            self._weight(o, w)
        main = self._join([o for o, _ in self.parts], "Body")
        glows = {}
        for o, _ in self.glow:
            glows.setdefault(o.get("glow_hex", "ffc840"), []).append(o)
        self.glowobjs = {}
        for hexs, objs in glows.items():
            self.glowobjs[hexs] = self._join(objs, "Glow_" + hexs)
        for o in [main] + list(self.glowobjs.values()):
            o.parent = arm
            mod = o.modifiers.get("Armature") or o.modifiers.new("Armature", "ARMATURE")
            mod.object = arm
        self.main = main
        self.bodyobj = main
        return arm


def _seg_dist(p, a, b):
    ab = b - a
    t = 0.0 if ab.length_squared < 1e-12 else max(0.0, min(1.0, (p - a).dot(ab) / ab.length_squared))
    return (p - (a + ab * t)).length


def _tri_hits(A, B):
    """points where the edges of triangle A cross triangle B and vice versa"""
    from mathutils import geometry
    pts = []
    for T, U in ((A, B), (B, A)):
        for i in range(3):
            p, q = T[i], T[(i + 1) % 3]
            d = q - p
            L = d.length
            if L < 1e-9:
                continue
            for o, r in ((p, d), (q, -d)):
                x = geometry.intersect_ray_tri(U[0], U[1], U[2], r, o, True)
                if x is not None and (x - o).length <= L + 1e-6:
                    pts.append(x)
                    break
    return pts


def overlap_report(k, pairs, step=2, clips=None, joints=None, frames=None, detail=False):
    """For each clip, frames where the parts of two bones really CUT THROUGH each other.
    pairs: [(boneA, boneB)]. joints: [(p0, p1, r, bone)] rest-space hinge/knuckle segments carried by `bone`:
    an intersection whose crossing points all lie within r of a (posed) joint segment is a hinge sliver, ignored.
    Contacts already present in the rest pose are ignored too. frames: {clip: [f, ...]}.
    Returns {clip: {"A|B": (colliding_triangle_pairs, worst_frame)}}."""
    from mathutils.bvhtree import BVHTree
    sc = bpy.context.scene
    arm = k.arm
    body = k.main
    me = body.data
    names = {g.index: g.name for g in body.vertex_groups}
    owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in me.vertices]
    want = sorted(set(a for pr in pairs for a in pr))
    J = []
    for a, b, r, bn in (joints or []):
        a2, sc = head_point(k, bn, a)
        b2, _ = head_point(k, bn, b)
        J.append((a2, b2, r * sc, bn))

    def posed_joints():
        out = []
        for a, b, r, bn in J:
            pbn = arm.pose.bones[bn]
            M = arm.matrix_world @ pbn.matrix @ arm.data.bones[bn].matrix_local.inverted()
            out.append((M @ a, M @ b, r))
        return out

    def trees():
        dg = bpy.context.evaluated_depsgraph_get()
        ev = body.evaluated_get(dg)
        em = ev.to_mesh()
        em.calc_loop_triangles()
        co = [ev.matrix_world @ v.co for v in em.vertices]
        tris = {}
        for t in em.loop_triangles:
            g = owner[t.vertices[0]]
            if g in want:
                tris.setdefault(g, []).append(tuple(t.vertices))
        T = {}
        for g in want:
            tl = tris.get(g, [])
            T[g] = (BVHTree.FromPolygons(co, [list(t) for t in tl], all_triangles=True), tl)
        ev.to_mesh_clear()
        return T, co

    def hits(T, co, a, b, pj):
        ta, la = T[a]
        tb, lb = T[b]
        out = set()
        for x, y in ta.overlap(tb):
            A = [co[i] for i in la[x]]
            B = [co[i] for i in lb[y]]
            pts = _tri_hits(A, B)
            if not pts:
                continue
            if pj and all(any(_seg_dist(p, j0, j1) < r for j0, j1, r in pj) for p in pts):
                continue
            out.add((la[x], lb[y]))
        return out

    arm.data.pose_position = "REST"
    bpy.context.view_layer.update()
    T, co = trees()
    pj = posed_joints()
    base = {pr: hits(T, co, pr[0], pr[1], pj) for pr in pairs}
    arm.data.pose_position = "POSE"
    rep = {}
    for clip, (n, loop) in k.clips.items():
        if clips and clip not in clips:
            continue
        k.set_action(clip)
        worst = {}
        for f in (frames or {}).get(clip, range(0, n + 1, step)):
            sc.frame_set(f)
            T, co = trees()
            pj = posed_joints()
            for pr in pairs:
                c = len(hits(T, co, pr[0], pr[1], pj) - base[pr])
                if c > worst.get(pr, (0, -1))[0]:
                    worst[pr] = (c, f)
        rep[clip] = {a + "|" + b: v for (a, b), v in worst.items()}
    return rep
