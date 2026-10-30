# SLINGSHOT Meteor Shower - HIGH QUALITY storm cloud (owner 2026-10-11: "low polygon ... looks like trash" + "also the
# storm models fix"). Replaces Weather/Meteor/build_cloud.py (an 8k-tri metaball blob with a flat gradient).
#   1. a cumulonimbus built as a signed-distance field from THREE levels of billows: ~70 storm masses, ~1100 billows
#      sampled on their surface, ~6000 cauliflower puffs sampled on that surface (OpenVDB via Geometry Nodes: Points to
#      SDF Grid), cut flat by a rough storm base (SDF intersect), mammatus pouches hanging under it (SDF union), creases
#      softened (SDF fillet) -> a ~2M-tri sculpt
#   2. colour per vertex: near-black belly -> charcoal flanks -> smoky grey tops (neutral-warm: Roblox's blue sky light
#      turned a cool ramp navy), lighter where a billow faces the sky
#   3. game mesh: decimated to 4 x 19k tris (Roblox: max 20k per MeshPart), split into 4 pieces along the bank, each
#      with its own 1024 maps baked from the sculpt: albedo x AO, tangent normal map (+ one shared flat roughness map)
#      -> SurfaceAppearance. No emissive (owner rule): lightning and the belly glow stay VFX.
# Headless:
#   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python build_storm_hq.py -- all
#   steps: build | render | export | all
# Units: 1 Blender metre = 1 stud. Blender (x, y, z) -> Roblox (x, z, -y): the bank runs along Blender Y (the runway).
import bpy, bmesh, math, os, sys, random, json
from mathutils import Vector, noise
import numpy as np

OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Weather\Meteor\HQ"
BLEND = os.path.join(OUT, "storm_hq.blend")
W, L = 105.0, 220.0          # half width / half length of the footprint (as the old cloud)
FLOOR = 2.0                  # the flat storm base (before the pouches)
PIECES = 4
PIECE_TRIS = 19000
TEX = 1024
SEED = 11

GRADIENT = [  # (height 0..1, sRGB): charcoal belly -> smoky tops. Warm-neutral (Roblox's blue sky light cools it), and
    (0.00, (36, 32, 30)),   # not too black: in game a near-black belly (sRGB 10) read as a flat black ceiling with no
    (0.08, (40, 36, 34)),   # lobes; this keeps it a black storm while the ambient light still shows the structure
    (0.30, (47, 43, 42)),
    (0.60, (60, 56, 55)),
    (0.85, (80, 76, 74)),
    (1.00, (100, 96, 94)),
]


def lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


GRAD_LIN = [(v, tuple(lin(x) for x in c)) for v, c in GRADIENT]


def grad(v):
    v = min(1.0, max(0.0, v))
    for (v0, c0), (v1, c1) in zip(GRAD_LIN, GRAD_LIN[1:]):
        if v <= v1:
            k = (v - v0) / (v1 - v0)
            return tuple(a + (b - a) * k for a, b in zip(c0, c1))
    return GRAD_LIN[-1][1]


def in_ellipse(rng, scale=1.0):
    while True:
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        if x * x + y * y <= 1:
            return x * scale, y * scale


POUCHES = []  # (x, y, radius, depth): mammatus lobes hanging under the base, filled in by build()


def floor_z(x, y):
    z = FLOOR + noise.noise(Vector((x * 0.03, y * 0.03, 0.5))) * 0.8 + noise.noise(Vector((x * 0.11, y * 0.11, 3.1))) * 0.25
    for px, py, pr, pd in POUCHES:
        d2 = ((x - px) ** 2 + (y - py) ** 2) / (pr * pr)
        if d2 < 4.0:
            z -= pd * math.exp(-d2 * 1.5)
    return z


# ------------------------------------------------------------------ helpers
def mesh_from(ob, name):
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    me.name = name
    return me


def points_object(sc, name, pts):
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(pts))
    me.vertices.foreach_set("co", np.array([p[:3] for p in pts], dtype=np.float32).ravel())
    a = me.attributes.new("r", "FLOAT", "POINT")
    a.data.foreach_set("value", np.array([p[3] for p in pts], dtype=np.float32))
    ob = bpy.data.objects.new(name, me)
    sc.collection.objects.link(ob)
    return ob


def floor_box(sc):
    """A closed slab whose underside is the rough storm base; the cloud is intersected with it."""
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=200, y_segments=350, size=1.0)
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    for v in bm.verts:  # a 300 x 520 slab, 1.5-stud cells
        x = -150 + (v.co.x - x0) / (x1 - x0) * 300
        y = -260 + (v.co.y - y0) / (y1 - y0) * 520
        v.co = Vector((x, y, floor_z(x, y)))
    ret = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces), use_keep_orig=True)
    for v in [e for e in ret["geom"] if isinstance(e, bmesh.types.BMVert)]:
        v.co.z = 260.0
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    me = bpy.data.meshes.new("FloorBox")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("FloorBox", me)
    sc.collection.objects.link(ob)
    ob.hide_render = True
    return ob


def named_float(nt, name):
    n = nt.nodes.new("GeometryNodeInputNamedAttribute")
    n.data_type = "FLOAT"
    n.inputs["Name"].default_value = name
    out = [o for o in n.outputs if o.enabled][0]
    return out


def sdf_object(sc, name, pts_ob, box_ob, voxel, pouch_ob=None, fillet=0):
    """Geometry Nodes: spheres (points + r) -> SDF, cut by the floor box, + pouches, filleted -> mesh."""
    ng = bpy.data.node_groups.new(name + "_GN", "GeometryNodeTree")
    ng.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    nt = ng
    gi = nt.nodes.new("NodeGroupInput")
    go = nt.nodes.new("NodeGroupOutput")
    L_ = nt.links.new

    def sphere_grid(geo_socket):
        m2p = nt.nodes.new("GeometryNodeMeshToPoints")
        L_(geo_socket, m2p.inputs["Mesh"])
        L_(named_float(nt, "r"), m2p.inputs["Radius"])
        p2s = nt.nodes.new("GeometryNodePointsToSDFGrid")
        L_(m2p.outputs["Points"], p2s.inputs["Points"])
        L_(named_float(nt, "r"), p2s.inputs["Radius"])
        p2s.inputs["Voxel Size"].default_value = voxel
        return p2s.outputs[0]

    oi = nt.nodes.new("GeometryNodeObjectInfo")
    oi.inputs["Object"].default_value = pts_ob
    oi.transform_space = "RELATIVE"
    g = sphere_grid(oi.outputs["Geometry"])
    bi = nt.nodes.new("GeometryNodeObjectInfo")
    bi.inputs["Object"].default_value = box_ob
    bi.transform_space = "RELATIVE"
    m2s = nt.nodes.new("GeometryNodeMeshToSDFGrid")
    L_(bi.outputs["Geometry"], m2s.inputs["Mesh"])
    m2s.inputs["Voxel Size"].default_value = voxel
    inter = nt.nodes.new("GeometryNodeSDFGridBoolean")
    inter.operation = "INTERSECT"
    L_(g, inter.inputs[1])  # INTERSECT / UNION: one multi-input socket
    L_(m2s.outputs[0], inter.inputs[1])
    g = inter.outputs[0]
    if pouch_ob:
        pi = nt.nodes.new("GeometryNodeObjectInfo")
        pi.inputs["Object"].default_value = pouch_ob
        pi.transform_space = "RELATIVE"
        pg = sphere_grid(pi.outputs["Geometry"])
        uni = nt.nodes.new("GeometryNodeSDFGridBoolean")
        uni.operation = "UNION"
        L_(g, uni.inputs[1])
        L_(pg, uni.inputs[1])
        g = uni.outputs[0]
    if fillet:
        fl = nt.nodes.new("GeometryNodeSDFGridFillet")
        L_(g, fl.inputs["Grid"])
        fl.inputs["Iterations"].default_value = fillet
        g = fl.outputs[0]
    g2m = nt.nodes.new("GeometryNodeGridToMesh")
    L_(g, g2m.inputs["Grid"])
    g2m.inputs["Threshold"].default_value = 0.0
    g2m.inputs["Adaptivity"].default_value = 0.0
    L_(g2m.outputs["Mesh"], go.inputs[0])
    holder_me = bpy.data.meshes.new(name + "_holder")
    ob = bpy.data.objects.new(name, holder_me)
    sc.collection.objects.link(ob)
    mod = ob.modifiers.new("SDF", "NODES")
    mod.node_group = ng
    bpy.context.view_layer.update()
    me = mesh_from(ob, name)
    ob.modifiers.clear()
    ob.data = me
    return ob


def sample_surface(me, n, rng, rmin, rmax, inset, min_nz, taper=True):
    """Spheres on the upper / side surface of a mesh, weighted by area."""
    np_ = len(me.polygons)
    cen = np.empty(np_ * 3, dtype=np.float32)
    nor = np.empty(np_ * 3, dtype=np.float32)
    area = np.empty(np_, dtype=np.float32)
    me.polygons.foreach_get("center", cen)
    me.polygons.foreach_get("normal", nor)
    me.polygons.foreach_get("area", area)
    cen, nor = cen.reshape(-1, 3), nor.reshape(-1, 3)
    ok = (nor[:, 2] > min_nz) & (cen[:, 2] > FLOOR + 3.5)
    idx = np.nonzero(ok)[0]
    w = area[idx] / area[idx].sum()
    nrs = np.random.default_rng(rng.randint(0, 1 << 30))
    pick = nrs.choice(idx, size=n, p=w)
    pts = []
    for i in pick:
        c, nv = Vector(cen[i]), Vector(nor[i])
        r = rng.uniform(rmin, rmax)
        if taper:
            r *= 1.0 - 0.25 * min(1.0, abs(c.y) / L)
        p = c - nv * r * inset
        pts.append((p.x, p.y, p.z, r))
    return pts


# ------------------------------------------------------------------ 1. the sculpt
def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.name = "StormHQ"
    rng = random.Random(SEED)
    K = 0.8  # metaball radius -> sphere radius (the old recipe's proportions)
    L0 = []
    for _ in range(130):     # the broad lumpy slab, tapering toward the ends; reaches well below the base
        x, y = in_ellipse(rng, 0.9)
        L0.append((x * W * 0.82, y * L, rng.uniform(5, 13), rng.uniform(24, 34) * (1 - 0.38 * abs(y)) * K))
    for _ in range(45):      # body billows
        x, y = in_ellipse(rng, 0.72)
        L0.append((x * W * 0.82, y * L, rng.uniform(26, 40), rng.uniform(22, 30) * (1 - 0.3 * abs(y)) * K))
    for c in range(4):       # four towering heads (an anvil-ish storm silhouette)
        cy = (-0.62 + c * 0.42 + rng.uniform(-0.08, 0.08)) * L
        cx = rng.uniform(-0.3, 0.3) * W
        hgt = rng.uniform(48, 60)
        for _ in range(7):
            L0.append((cx + rng.uniform(-24, 24), cy + rng.uniform(-30, 30), hgt + rng.uniform(-10, 8), rng.uniform(20, 26) * K))
    prng = random.Random(SEED * 7)
    POUCHES.clear()
    for _ in range(46):      # mammatus lobes
        x, y = in_ellipse(prng, 0.74)
        POUCHES.append((x * W * 0.8, y * L, prng.uniform(8.0, 14.0) * (1 - 0.25 * abs(y)), prng.uniform(2.5, 6.5)))
    pouches = POUCHES
    box = floor_box(sc)
    p0 = points_object(sc, "L0pts", L0)
    m0 = sdf_object(sc, "Pass0", p0, box, 2.0)
    L1 = sample_surface(m0.data, 1100, rng, 6.0, 12.0, 0.45, -0.3)
    p1 = points_object(sc, "L01pts", L0 + L1)
    m1 = sdf_object(sc, "Pass1", p1, box, 1.0)
    L2 = sample_surface(m1.data, 6500, rng, 2.0, 4.6, 0.38, -0.15)
    pall = points_object(sc, "Allpts", L0 + L1 + L2)
    hi = sdf_object(sc, "StormHi", pall, box, 0.55, fillet=2)
    for o in (m0, m1):
        bpy.data.objects.remove(o)
    for o in (box, p0, p1, pall):
        o.hide_viewport = True
        o.hide_render = True
    me = hi.data
    # centre the bbox on the origin (Studio pivots MeshParts at the bbox centre)
    co = np.empty(len(me.vertices) * 3, dtype=np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    mn, mx = co.min(0), co.max(0)
    c = (mn + mx) / 2
    co -= c
    me.vertices.foreach_set("co", co.ravel())
    me.update()
    zmin, zmax = float(mn[2] - c[2]), float(mx[2] - c[2])
    base = FLOOR - float(c[2])  # where the flat base sits (centred coords)
    # 2. colour per vertex
    nor = np.empty(len(me.vertices) * 3, dtype=np.float32)
    me.vertices.foreach_get("normal", nor)
    nor = nor.reshape(-1, 3)
    cols = np.empty((len(co), 4), dtype=np.float32)
    off = Vector((17.3, 4.1, 9.7))
    lift = tuple(lin(x) for x in (124, 118, 116))
    bounce = tuple(lin(x) for x in (78, 70, 66))
    for i in range(len(co)):
        p = Vector(co[i])
        k = (p.z - base) / (zmax - base)
        k += noise.noise(p * 0.045 + off) * 0.07 + noise.noise(p * 0.16) * 0.03
        r, g, b = grad(k)
        up = max(0.0, nor[i][2])
        t = 0.5 * up * up * min(1.0, max(0.0, k + 0.15))         # sky-facing billow tops catch light
        r, g, b = r + (lift[0] - r) * t, g + (lift[1] - g) * t, b + (lift[2] - b) * t
        sag = min(1.0, max(0.0, (base - p.z) / 6.0))               # mammatus tips catch the ground bounce
        dn = max(0.0, -nor[i][2])
        t = 0.55 * sag * dn
        r, g, b = r + (bounce[0] - r) * t, g + (bounce[1] - g) * t, b + (bounce[2] - b) * t
        cols[i] = (r, g, b, 1.0)
    ca = me.color_attributes.new("Col", "FLOAT_COLOR", "POINT")
    ca.data.foreach_set("color", cols.ravel())
    for p_ in me.polygons:
        p_.use_smooth = True
    hi_tris = sum(len(p_.vertices) - 2 for p_ in me.polygons)
    # 3. game pieces
    lo = bpy.data.objects.new("StormLo", me.copy())
    sc.collection.objects.link(lo)
    for a in list(lo.data.color_attributes):
        lo.data.color_attributes.remove(a)
    dec = lo.modifiers.new("Dec", "DECIMATE")
    dec.ratio = min(1.0, PIECES * PIECE_TRIS / hi_tris)
    lo.modifiers.new("Tri", "TRIANGULATE")
    lo.data = mesh_from(lo, "StormLo")
    lo.modifiers.clear()
    pieces = split_pieces(sc, lo)
    bpy.data.objects.remove(lo)
    rough = bpy.data.images.new("StormCloud_rough", 64, 64, alpha=False)
    rough.colorspace_settings.name = "Non-Color"
    rough.pixels[:] = [0.95, 0.95, 0.95, 1.0] * (64 * 64)
    rough.filepath_raw = os.path.join(OUT, "StormCloud_rough.png")
    rough.file_format = "PNG"
    rough.save()
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 32
    if not sc.world:
        sc.world = bpy.data.worlds.new("W")
    sc.world.light_settings.distance = 12.0
    rep = {"hi_tris": hi_tris, "size": [round(float(v), 1) for v in (mx - mn)], "base_above_bottom": round(base - zmin, 2),
           "levels": [len(L0), len(L1), len(L2), len(pouches)], "pieces": []}
    for ob in pieces:
        bake_piece(sc, ob, hi, rough)
        rep["pieces"].append({"name": ob.name, "tris": len(ob.data.polygons), "size": [round(v, 1) for v in ob.dimensions],
                              "loc": [round(v, 1) for v in ob.location]})
    hi.hide_render = True
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return rep


def split_pieces(sc, lo):
    me = lo.data
    ys = sorted(p.center.y for p in me.polygons)
    cuts = [ys[int(len(ys) * k / PIECES)] for k in range(1, PIECES)]
    out = []
    for k in range(PIECES):
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.faces.ensure_lookup_table()
        kill = [f for f in bm.faces if sum(1 for cy in cuts if f.calc_center_median().y >= cy) != k]
        bmesh.ops.delete(bm, geom=kill, context="FACES")
        pm = bpy.data.meshes.new(f"StormCloud{k + 1}")
        bm.to_mesh(pm)
        bm.free()
        ob = bpy.data.objects.new(f"StormCloud{k + 1}", pm)
        sc.collection.objects.link(ob)
        for p_ in pm.polygons:
            p_.use_smooth = True
        out.append(ob)
    return out


def only(ob):
    for o in bpy.context.scene.objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob


def bake_piece(sc, lo, hi, rough_img):
    only(lo)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=0.003)
    bpy.ops.object.mode_set(mode="OBJECT")
    imgs = {}
    for key, cs in (("albedo", "sRGB"), ("normal", "Non-Color"), ("ao", "Non-Color")):
        img = bpy.data.images.new(f"{lo.name}_{key}", TEX, TEX, alpha=False)
        img.colorspace_settings.name = cs
        imgs[key] = img
    bm_ = bpy.data.materials.new(lo.name + "_bake")
    bm_.use_nodes = True
    tex = bm_.node_tree.nodes.new("ShaderNodeTexImage")
    lo.data.materials.clear()
    lo.data.materials.append(bm_)
    if not (len(hi.data.materials) == 1 and hi.data.materials[0] and hi.data.materials[0].name == "StormHi"):
        hi.data.materials.clear()
        hm = bpy.data.materials.new("StormHi")
        hm.use_nodes = True
        bsdf = hm.node_tree.nodes["Principled BSDF"]
        vc = hm.node_tree.nodes.new("ShaderNodeVertexColor")
        vc.layer_name = "Col"
        hm.node_tree.links.new(vc.outputs["Color"], bsdf.inputs["Base Color"])
        hi.data.materials.append(hm)
    hi.hide_render = False
    for o in sc.objects:
        o.select_set(False)
    hi.select_set(True)
    lo.select_set(True)
    bpy.context.view_layer.objects.active = lo

    def run(kind, img, **kw):
        tex.image = img
        bm_.node_tree.nodes.active = tex
        bpy.ops.object.bake(type=kind, use_selected_to_active=True, cage_extrusion=1.2, max_ray_distance=3.0, margin=6, **kw)

    run("NORMAL", imgs["normal"], normal_space="TANGENT")
    run("AO", imgs["ao"])
    run("DIFFUSE", imgs["albedo"], pass_filter={"COLOR"})
    a = np.array(imgs["albedo"].pixels[:], dtype=np.float32).reshape(-1, 4)
    o = np.array(imgs["ao"].pixels[:], dtype=np.float32).reshape(-1, 4)
    a[:, :3] *= (0.12 + 0.88 * o[:, :1] ** 1.3)  # deep crevices, lit lobes
    imgs["albedo"].pixels[:] = a.ravel()
    for key in imgs:
        imgs[key].filepath_raw = os.path.join(OUT, f"{lo.name}_{key}.png")
        imgs[key].file_format = "PNG"
        imgs[key].save()
    m = bpy.data.materials.new(lo.name + "_PBR")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    ta = nt.nodes.new("ShaderNodeTexImage")
    ta.image = imgs["albedo"]
    nt.links.new(ta.outputs["Color"], bsdf.inputs["Base Color"])
    tn = nt.nodes.new("ShaderNodeTexImage")
    tn.image = imgs["normal"]
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(tn.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    tr = nt.nodes.new("ShaderNodeTexImage")
    tr.image = rough_img
    nt.links.new(tr.outputs["Color"], bsdf.inputs["Roughness"])
    bsdf.inputs["Metallic"].default_value = 0.0
    lo.data.materials.clear()
    lo.data.materials.append(m)


# ------------------------------------------------------------------ review renders
def render_all(tag=""):
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = bpy.data.scenes["StormHQ"]
    pieces = [o for o in sc.objects if o.name.startswith("StormCloud")]
    hi = bpy.data.objects["StormHi"]
    hi.hide_render = True
    zmin = min((o.matrix_world @ Vector(c)).z for o in pieces for c in o.bound_box)
    for o in pieces:
        o.location.z += 85.0 - zmin + 0  # the bottom of the pouches ~ 85 - POUCH; good enough for a look
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = 1600, 900
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("Sky")
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.42, 0.62, 0.9, 1.0)
    bg.inputs["Strength"].default_value = 0.9
    sc.world = w
    for nm, rot, e, col in (("Key", (35, 0, 30), 3.5, (1, 0.97, 0.92)), ("Fill", (150, 0, -140), 0.6, (0.75, 0.8, 1.0))):
        ld = bpy.data.lights.new(nm, "SUN")
        ld.energy, ld.color = e, col
        lo = bpy.data.objects.new(nm, ld)
        lo.rotation_euler = [math.radians(a) for a in rot]
        sc.collection.objects.link(lo)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    fl = bpy.context.active_object
    fl.scale = (120, 400, 1)
    mfl = bpy.data.materials.new("Floor")
    mfl.use_nodes = True
    mfl.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.55, 0.75, 0.55, 1)
    fl.data.materials.append(mfl)
    views = {
        "storm_hq_player": ((8, 170, 6), (0, -60, 95), 22),
        "storm_hq_below": ((30, 60, 4), (0, 0, 140), 16),
        "storm_hq_side": ((520, -160, 120), (0, 0, 120), 35),
        "storm_hq_close": ((150, 120, 110), (0, 20, 110), 35),
    }
    out = []
    for name, (loc, tgt, lens) in views.items():
        cd = bpy.data.cameras.new("Cam")
        cam = bpy.data.objects.new("Cam", cd)
        sc.collection.objects.link(cam)
        cam.location = Vector(loc)
        cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
        cd.lens, cd.clip_end = lens, 6000
        sc.camera = cam
        p = os.path.join(OUT, name + tag + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True, scene=sc.name)
        bpy.data.objects.remove(cam)
        out.append(p)
    return out


FBX_ARGS = dict(use_selection=True, global_scale=0.01, apply_unit_scale=True, apply_scale_options="FBX_SCALE_NONE",
                axis_forward="-Z", axis_up="Y", object_types={"MESH"}, use_mesh_modifiers=True,
                mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False, path_mode="COPY",
                embed_textures=True)


def export():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = bpy.data.scenes["StormHQ"]
    pieces = [o for o in sc.objects if o.name.startswith("StormCloud")]
    for o in sc.objects:
        o.select_set(o in pieces)
    bpy.context.view_layer.objects.active = pieces[0]
    path = os.path.join(r"C:\cdimp", "StormCloudHQ.fbx")
    bpy.ops.export_scene.fbx(filepath=path, **FBX_ARGS)
    return {"fbx": path, "kb": round(os.path.getsize(path) / 1024, 1)}


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["all"]
    step = argv[0]
    rep = {}
    if step in ("build", "all"):
        rep["build"] = build()
    if step in ("render", "all"):
        rep["render"] = render_all()
    if step in ("export", "all"):
        rep["export"] = export()
    print("STORM_REPORT " + json.dumps(rep))
