"""Auto-rig a Meshy creature (single mesh, faces -Y, Z up) with a simple skeleton + geometric skin weights.

blender -b -P rigger.py -- <Name> <type> [options as key=value] [--pose] [--export]
Types: quad, biped, bird, wingquad, multileg, serpent, jelly, kraken, moth, seahorse
Output: rig/out/<Name>.fbx (+ <Name>_pose.png when --pose)
Bone names (used by the Roblox animator): Root, Hips, Chest, Neck, Head, Tail1..n,
Leg<i>_U / Leg<i>_L (i = 1..n; legs sorted front->back, left(+x)->right), Arm L/R (_U/_L),
WingL1..3 / WingR1..3, Tent<i>_1..3.
"""
import bpy, bmesh, sys, os, math
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
NAME, TYPE = argv[0], argv[1]
OPT = {k: float(v) for k, v in (a.split("=") for a in argv[2:] if "=" in a)}
POSE = "--pose" in argv
EXPORT = "--export" in argv
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
SRC = os.path.expanduser(f"~/Downloads/Meshy/{NAME}.glb")
if os.path.exists(os.path.join(HERE, "src", NAME + ".glb")):  # prepared Claude Design models
    SRC = os.path.join(HERE, "src", NAME + ".glb")

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
mesh = [o for o in bpy.context.scene.objects if o.type == "MESH"][0]
for o in list(bpy.context.scene.objects):
    if o is not mesh and o.type != "MESH":
        pass
# apply transforms, unparent
bpy.ops.object.select_all(action="DESELECT")
mesh.select_set(True)
bpy.context.view_layer.objects.active = mesh
bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
for o in list(bpy.context.scene.objects):
    if o is not mesh:
        bpy.data.objects.remove(o)
mesh.name = NAME

# normalise: feet on z=0, centred in x/y, height = 2 units (Roblox scales later)
vs = [v.co.copy() for v in mesh.data.vertices]
mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
s = 2.0 / (mx.z - mn.z)
off = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z))
for v in mesh.data.vertices:
    v.co = (v.co - off) * s
mesh.data.update()
P = [v.co.copy() for v in mesh.data.vertices]
N = len(P)
xs = [p.x for p in P]; ys = [p.y for p in P]; zs = [p.z for p in P]
W = max(xs) - min(xs); L = max(ys) - min(ys); H = max(zs)
YMIN, YMAX = min(ys), max(ys)


def kmeans(pts, inits, iters=25):
    cs = [Vector(c) for c in inits]
    for _ in range(iters):
        groups = [[] for _ in cs]
        for p in pts:
            i = min(range(len(cs)), key=lambda k: (p - cs[k]).length_squared)
            groups[i].append(p)
        cs = [sum(g, Vector()) / len(g) if g else cs[i] for i, g in enumerate(groups)]
    return cs, groups


def centroid(sel):
    sel = list(sel)
    return sum(sel, Vector()) / len(sel) if sel else None


def top_at(y, band=0.06):
    c = [p.z for p in P if abs(p.y - y) < band * L and abs(p.x) < 0.25 * W]
    return max(c) if c else H


def bottom_at(y, band=0.06):
    c = [p.z for p in P if abs(p.y - y) < band * L and abs(p.x) < 0.2 * W]
    return min(c) if c else 0


# ------------------------------------------------------------------ skeleton
bones = {}   # name -> (head, tail, parent)
tail = []
groups = {}  # name -> per-vertex weights list


def bone(name, h, t, parent=None):
    if (t - h).length < 1e-3:
        t = h + Vector((0, 0, 0.05))
    bones[name] = (Vector(h), Vector(t), parent)


def seg_dist(p, a, b):
    ab = b - a
    t = max(0.0, min(1.0, (p - a).dot(ab) / max(ab.length_squared, 1e-9)))
    return (p - (a + ab * t)).length, t


nlegs = int(OPT.get("legs", {"quad": 4, "biped": 2, "bird": 2, "wingquad": 4, "multileg": 8,
                             "seahorse": 2}.get(TYPE, 0)))
has_wings = TYPE in ("bird", "wingquad", "moth") or OPT.get("wings", 0) > 0
has_tail = OPT.get("tail", 1) > 0 and TYPE not in ("jelly", "kraken", "moth")
foot_h = OPT.get("foot", 0.07) * H

# feet ---------------------------------------------------------------------
feet = []
if nlegs:
    low = [p for p in P if p.z < foot_h]
    if TYPE in ("biped", "bird"):
        inits = [(0.2 * W, 0, 0), (-0.2 * W, 0, 0)]
    elif nlegs == 4:
        inits = [(0.25 * W, YMIN + 0.25 * L, 0), (-0.25 * W, YMIN + 0.25 * L, 0),
                 (0.25 * W, YMAX - 0.3 * L, 0), (-0.25 * W, YMAX - 0.3 * L, 0)]
    elif TYPE == "seahorse":
        inits = [(0.2 * W, YMIN + 0.3 * L, 0), (-0.2 * W, YMIN + 0.3 * L, 0)]
    else:  # multileg: ring of feet
        inits = []
        for i in range(nlegs):
            a = (i + 0.5) / nlegs * 2 * math.pi
            inits.append((math.cos(a) * W * 0.45, math.sin(a) * L * 0.45, 0))
    flat = [Vector((p.x, p.y, 0)) for p in low]
    cs, gs = kmeans(flat, inits)
    feet = [c for c, g in zip(cs, gs) if len(g) > 5]
    # order: front (low y) first, then left (+x) first
    feet.sort(key=lambda c: (round((c.y - YMIN) / (0.15 * L)), -c.x))

# body line ------------------------------------------------------------------
belly = OPT.get("belly", 0)
if not belly:
    mids = [p.z for p in P if abs(p.x) < 0.12 * W and abs(p.y - (YMIN + YMAX) / 2) < 0.12 * L and p.z > foot_h]
    belly = min(mids) if mids else 0.4 * H
    if TYPE in ("biped", "bird"):
        belly = OPT.get("hip", 0.45) * H
belly = max(belly, 0.15 * H) if nlegs else 0

if TYPE in ("quad", "wingquad", "multileg", "seahorse"):
    fy = [f.y for f in feet[:2]] if feet else [YMIN + 0.3 * L]
    by = [f.y for f in feet[-2:]] if len(feet) > 2 else [YMAX - 0.3 * L]
    chest_y, hip_y = sum(fy) / len(fy), sum(by) / len(by)
    if TYPE == "seahorse":
        hip_y = (YMIN + YMAX) / 2 + 0.1 * L
    if TYPE == "multileg":
        chest_y, hip_y = YMIN + 0.35 * L, YMIN + 0.6 * L
    cz = lambda y: (max(bottom_at(y), belly * 0.9) + top_at(y)) / 2
    hips = Vector((0, hip_y, cz(hip_y)))
    chest = Vector((0, chest_y, cz(chest_y)))
    bone("Root", Vector((0, (hip_y + chest_y) / 2, 0)), Vector((0, (hip_y + chest_y) / 2, 0.2)))
    bone("Hips", hips, (hips + chest) / 2, "Root")
    bone("Chest", (hips + chest) / 2, chest, "Hips")
    # head: centroid of the front-most slab
    front = [p for p in P if p.y < YMIN + OPT.get("headlen", 0.12) * L and p.z > belly]
    head_c = centroid(front) or Vector((0, YMIN, H * 0.7))
    neck_base = chest + Vector((0, -0.08 * L, 0.05 * H))
    neck_top = Vector((0, (neck_base.y + head_c.y) / 2 + 0.03 * L, (neck_base.z + head_c.z) / 2 + 0.05 * H))
    bone("Neck", neck_base, neck_top, "Chest")
    bone("Head", neck_top, Vector((0, YMIN, head_c.z)), "Neck")
    spine_root = hips
elif TYPE in ("biped", "bird"):
    hips = Vector((0, sum(f.y for f in feet) / max(len(feet), 1) if feet else 0, belly))
    shoulder_z = OPT.get("shoulder", 0.72) * H
    chest = Vector((0, hips.y - OPT.get("lean", 0.05) * L, shoulder_z))
    bone("Root", Vector((hips.x, hips.y, 0)), Vector((hips.x, hips.y, 0.2)), None)
    bone("Hips", hips, hips + (chest - hips) * 0.5, "Root")
    bone("Chest", hips + (chest - hips) * 0.5, chest, "Hips")
    top = [p for p in P if p.z > OPT.get("headz", 0.8) * H and abs(p.x) < 0.25 * W]
    head_c = centroid(top) or Vector((0, 0, H))
    bone("Neck", chest, chest + (head_c - chest) * 0.4, "Chest")
    hd = head_c - chest
    bone("Head", chest + hd * 0.4, head_c + Vector((0, -0.08 * L, 0.05 * H)), "Neck")
    spine_root = hips
elif TYPE == "snake":  # long body lying along Y, head at -Y: chain of segments
    def mid_at(y, band=0.04):
        sl = [p for p in P if abs(p.y - y) < band * L]
        c = centroid(sl)
        return c if c else Vector((0, y, H * 0.3))
    head_c = mid_at(YMIN + 0.05 * L)
    neck_b = mid_at(YMIN + 0.16 * L)
    hips_p = mid_at(YMIN + 0.26 * L)
    bone("Root", Vector((0, hips_p.y, 0)), Vector((0, hips_p.y, 0.2)))
    bone("Hips", hips_p, neck_b, "Root")
    bone("Chest", neck_b, neck_b + (neck_b - hips_p) * 0.3, "Hips")
    bone("Neck", neck_b + (neck_b - hips_p) * 0.3, mid_at(YMIN + 0.1 * L), "Chest")
    bone("Head", mid_at(YMIN + 0.1 * L), Vector((head_c.x, YMIN, head_c.z)), "Neck")
    n = 8
    prev, last = "Hips", hips_p
    for k in range(1, n + 1):
        p = mid_at(hips_p.y + (YMAX - hips_p.y) * k / n) if k < n else Vector((0, YMAX, mid_at(YMAX - 0.02 * L).z))
        bone(f"Tail{k}", last, p, prev)
        prev, last = f"Tail{k}", p
        tail.append(prev)
    spine_root = hips_p
    has_tail = False
else:  # serpent, jelly, kraken, moth: vertical core
    cx = centroid([p for p in P if p.z > 0.5 * H]) or Vector((0, 0, H * 0.75))
    bone("Root", Vector((0, cx.y, 0)), Vector((0, cx.y, 0.2)))
    if TYPE == "serpent":
        coil_top = OPT.get("coil", 0.45) * H
        neck = [p for p in P if p.z > coil_top]
        nb = centroid([p for p in neck if p.z < coil_top + 0.1 * H]) or Vector((0, 0, coil_top))
        hc = centroid([p for p in neck if p.z > 0.85 * H]) or Vector((0, 0, H))
        tipf = min(neck, key=lambda p: p.y) if neck else hc
        bone("Hips", Vector((0, cx.y, 0.1)), Vector((nb.x, nb.y, coil_top * 0.7)), "Root")
        bone("Chest", Vector((nb.x, nb.y, coil_top * 0.7)), nb, "Hips")
        mid = (nb + hc) / 2 + Vector((0, 0.05 * L, 0))
        bone("Neck", nb, mid, "Chest")
        bone("Head", mid, Vector((tipf.x, tipf.y, hc.z)), "Neck")
    else:
        bell_z = OPT.get("bell", 0.55) * H
        bc = centroid([p for p in P if p.z > bell_z]) or Vector((0, 0, H * 0.8))
        bone("Hips", Vector((bc.x, bc.y, bell_z)), Vector((bc.x, bc.y, (bell_z + H) / 2)), "Root")
        bone("Chest", Vector((bc.x, bc.y, (bell_z + H) / 2)), Vector((bc.x, bc.y, H)), "Hips")
        if TYPE == "moth":
            bones.pop("Chest")
    spine_root = bones["Hips"][0]

# tail -------------------------------------------------------------------------
if has_tail and TYPE in ("quad", "wingquad", "multileg", "seahorse", "biped", "bird"):
    rear_start = OPT.get("tailstart", None)
    rear_start = YMAX - (rear_start if rear_start is not None else 0.3) * L
    if TYPE in ("biped", "bird"):
        rear_start = max(rear_start, hips.y + 0.12 * L)
    else:
        rear_start = max(rear_start, hips.y + 0.05 * L)
    rear = [p for p in P if p.y > rear_start and p.z > foot_h * 1.5]
    if len(rear) > 50 and YMAX - hips.y > 0.12 * L:
        n = 4
        pts = [spine_root]
        edges = [rear_start + (YMAX - rear_start) * k / n for k in range(n + 1)]
        for k in range(n):
            sl = [p for p in rear if edges[k] <= p.y <= edges[k + 1]]
            c = centroid(sl)
            if c:
                pts.append(Vector((c.x, c.y, c.z)))
        prev = "Hips"
        for i in range(1, len(pts)):
            bone(f"Tail{i}", pts[i - 1], pts[i], prev)
            prev = f"Tail{i}"
            tail.append(prev)

# legs -------------------------------------------------------------------------
legs = []
for i, f in enumerate(feet):
    parent = "Chest" if f.y < (bones["Hips"][0].y + bones["Chest"][1].y) / 2 or TYPE in ("biped", "bird") else "Hips"
    if TYPE in ("biped", "bird"):
        parent = "Hips"
    top_z = belly + 0.08 * H
    knee = Vector((f.x, f.y + (0.03 if parent == "Chest" else -0.03) * L, top_z * 0.5))
    u, lname = f"Leg{i + 1}_U", f"Leg{i + 1}_L"
    bone(u, Vector((f.x * 0.8, f.y, top_z)), knee, parent)
    bone(lname, knee, Vector((f.x, f.y, 0)), u)
    legs.append((u, lname, f))

# wings (lateral extremes above the body) ---------------------------------------
wings = []
if has_wings:
    root_x = OPT.get("wingroot", 0.18) * W
    wz = OPT.get("wingz", 0.0) * H
    for side, sgn in (("L", 1), ("R", -1)):
        sel = [p for p in P if p.x * sgn > root_x and p.z > max(wz, belly * 0.8)]
        if len(sel) < 30:
            continue
        xmax = max(p.x * sgn for p in sel)
        pts = []
        for k in range(4):
            a = root_x + (xmax - root_x) * k / 3
            b = a + (xmax - root_x) / 6
            sl = [p for p in sel if a - (xmax - root_x) / 6 <= p.x * sgn <= b]
            c = centroid(sl)
            if c:
                pts.append(c)
        parent = "Chest" if "Chest" in bones else "Hips"
        for k in range(1, len(pts)):
            nm = f"Wing{side}{k}"
            bone(nm, pts[k - 1], pts[k], parent)
            parent = nm
            wings.append(nm)

# tentacles (kraken / jelly): radial clusters of the low vertices -----------------
tents = []
if TYPE in ("kraken", "jelly"):
    bell_z = OPT.get("bell", 0.55) * H
    low = [p for p in P if p.z < bell_z]
    nt = int(OPT.get("tents", 8))
    inits = [(math.cos(a) * W * 0.4, math.sin(a) * L * 0.4, bell_z * 0.4)
             for a in [(i + 0.5) / nt * 2 * math.pi for i in range(nt)]]
    flat = [Vector((p.x, p.y, 0)) for p in low]
    cs, gs = kmeans(flat, [(x, y, 0) for x, y, _ in inits])
    for i, c in enumerate(cs):
        mine = [low[j] for j in range(len(low)) if (flat[j] - c).length < 0.2 * max(W, L)]
        if len(mine) < 30:
            continue
        pts = [Vector((c.x * 0.3, c.y * 0.3, bell_z))]
        for k in range(3):
            zt = bell_z * (1 - (k + 1) / 3)
            sl = [p for p in mine if abs(p.z - zt) < bell_z / 6] or mine
            pts.append(centroid(sl))
        prev = "Hips"
        for k in range(1, 4):
            nm = f"Tent{i + 1}_{k}"
            bone(nm, pts[k - 1], pts[k], prev)
            prev = nm
            tents.append(nm)

# arms for bipeds: lateral extremes at mid height ------------------------------------
if TYPE == "biped" and OPT.get("arms", 1) > 0:
    sz = OPT.get("shoulder", 0.72) * H
    for side, sgn in (("L", 1), ("R", -1)):
        sel = [p for p in P if p.x * sgn > OPT.get("armroot", 0.28) * W and p.z > belly * 0.6 and p.z < sz + 0.1 * H]
        if len(sel) < 30:
            continue
        hand = min(sel, key=lambda p: p.z)
        sh = Vector((sgn * OPT.get("armroot", 0.28) * W, bones["Chest"][1].y, sz))
        el = (sh + hand) / 2 + Vector((0, 0.05 * L, 0))
        bone(f"Arm{side}_U", sh, el, "Chest")
        bone(f"Arm{side}_L", el, hand, f"Arm{side}_U")

# ------------------------------------------------------------------ weights
# Each vertex picks a region (leg / wing / tentacle / arm / spine) by geometry, then is
# weighted by inverse distance to the bones of that region (+ a soft blend into the body).
names = list(bones)
W8 = {n: [0.0] * N for n in names}
spine = [n for n in names if n in ("Hips", "Chest", "Neck", "Head") or n.startswith("Tail")]
arm_names = [n for n in names if n.startswith("Arm")]


def give(i, cands, falloff=2.5):
    ws = []
    for n in cands:
        h, t, _ = bones[n]
        d, _ = seg_dist(P[i], h, t)
        ws.append((n, 1.0 / (d + 0.02) ** falloff))
    ws.sort(key=lambda x: -x[1])
    ws = ws[:3]
    tot = sum(w for _, w in ws)
    return [(n, w / tot) for n, w in ws]


def add(i, lst, scale=1.0):
    for n, w in lst:
        W8[n][i] += w * scale


leg_top = belly + 0.06 * H
for i, p in enumerate(P):
    done = False
    # legs
    if legs and p.z < leg_top + 0.08 * H:
        fl = Vector((p.x, p.y, 0))
        best = min(legs, key=lambda lg: (fl - lg[2]).length)
        if (fl - best[2]).length < OPT.get("legr", 0.22) * max(W, L) or p.z < foot_h * 2:
            blend = max(0.0, min(1.0, (p.z - (leg_top - 0.04 * H)) / (0.12 * H)))  # 0 = leg, 1 = body
            add(i, give(i, [best[0], best[1]]), 1 - blend)
            if blend > 0:
                add(i, give(i, [n for n in spine if n in ("Hips", "Chest")]), blend)
            done = True
    if not done and wings:
        side = "L" if p.x > 0 else "R"
        root_x = OPT.get("wingroot", 0.18) * W
        ax = abs(p.x)
        mine = [n for n in wings if n.startswith("Wing" + side)]
        if mine and ax > root_x * 0.7 and p.z > belly * 0.8:
            blend = max(0.0, min(1.0, (ax - root_x * 0.7) / (root_x * 0.6)))
            add(i, give(i, mine), blend)
            if blend < 1:
                add(i, give(i, [n for n in spine if not n.startswith("Tail")]), 1 - blend)
            done = True
    if not done and arm_names:
        side = "L" if p.x > 0 else "R"
        mine = [n for n in arm_names if n.startswith("Arm" + side)]
        if mine and abs(p.x) > OPT.get("armroot", 0.28) * W * 0.85 and p.z > belly * 0.6:
            add(i, give(i, mine))
            done = True
    if not done and tents and p.z < OPT.get("bell", 0.55) * H:
        best = min(tents, key=lambda n: seg_dist(p, bones[n][0], bones[n][1])[0])
        chain = [n for n in tents if n.split("_")[0] == best.split("_")[0]]
        blend = max(0.0, min(1.0, (p.z - OPT.get("bell", 0.55) * H * 0.85) / (0.1 * H)))
        add(i, give(i, chain), 1 - blend)
        if blend > 0:
            add(i, [("Hips", 1.0)], blend)
        done = True
    if not done:
        add(i, give(i, [n for n in spine if n in bones]))

for n in names:
    if n == "Root":
        continue
    vg = mesh.vertex_groups.new(name=n)
    for i, w in enumerate(W8[n]):
        if w > 0.001:
            vg.add([i], w, "REPLACE")

# ------------------------------------------------------------------ armature
arm_data = bpy.data.armatures.new(NAME + "_Rig")
arm = bpy.data.objects.new(NAME + "_Rig", arm_data)
bpy.context.scene.collection.objects.link(arm)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="EDIT")
eb = {}
for n, (h, t, par) in bones.items():
    b = arm_data.edit_bones.new(n)
    b.head, b.tail = h, t
    eb[n] = b
for n, (h, t, par) in bones.items():
    if par and par in eb:
        eb[n].parent = eb[par]
bpy.ops.object.mode_set(mode="OBJECT")
mesh.parent = arm
mod = mesh.modifiers.new("Armature", "ARMATURE")
mod.object = arm

print("RIG", NAME, TYPE, "bones", len(bones), "feet", len(feet), "wings", len(wings), "tail", len(tail), "tents", len(tents))
print("BONES", sorted(bones))

# ------------------------------------------------------------------ pose test render
if POSE:
    import math as m
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"; sc.display.shading.light = "STUDIO"; sc.display.shading.color_type = "TEXTURE"
    sc.render.resolution_x = 360; sc.render.resolution_y = 300
    cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"; cam.data.ortho_scale = 3.2
    pb = arm.pose.bones
    for b in pb:
        b.rotation_mode = "XYZ"
    def pose(k):
        for b in pb:
            b.rotation_euler = (0, 0, 0)
        if k == 1:
            for j, (u, l, f) in enumerate(legs):
                pb[u].rotation_euler = (m.radians(35 if j % 3 == 0 else -35), 0, 0)
            for n in tail: pb[n].rotation_euler = (0, 0, m.radians(20))
            if "Head" in pb: pb["Head"].rotation_euler = (m.radians(25), 0, 0)
            for n in wings: pb[n].rotation_euler = (0, m.radians(30), 0)
            for n in tents: pb[n].rotation_euler = (m.radians(30), 0, 0)
            for n in arm_names:
                if n.endswith("_U"): pb[n].rotation_euler = (m.radians(40), 0, 0)
    shots = []
    for k in (0, 1):
        pose(k)
        bpy.context.view_layer.update()
        for v, (loc, rot) in enumerate([((5, 0, 1), (m.radians(90), 0, m.radians(90))), ((3.5, -3.5, 2.2), (m.radians(70), 0, m.radians(45)))]):
            cam.location = loc; cam.rotation_euler = rot
            p = os.path.join(OUT, f"_{NAME}_{k}{v}.png"); sc.render.filepath = p
            bpy.ops.render.render(write_still=True); shots.append(p)
    print("SHOTS", ";".join(shots))
    for b in pb:
        b.rotation_euler = (0, 0, 0)

if EXPORT:
    for img in bpy.data.images:
        if img.size[0] > 1024:
            img.scale(1024, 1024)
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True); mesh.select_set(True)
    bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + ".fbx"), use_selection=True,
                             add_leaf_bones=False, bake_anim=False, path_mode="COPY", embed_textures=True,
                             object_types={"ARMATURE", "MESH"}, mesh_smooth_type="FACE")
    print("EXPORTED", os.path.join(OUT, NAME + ".fbx"))
