"""creature_kit: tiny helpers for building low-poly SLINGSHOT creatures in Blender.

Conventions
- Blender Z is up, creatures face -Y, 1 Blender unit ~ 1 stud before the Studio rescale.
- Every mesh is built in world space (object at origin, identity rotation/scale); pivot() then
  moves the origin to the joint so Studio sees the joint as the part's position.
- One 64x64 palette PNG per creature: 8x8 cells of 8 px. Each face's UVs point at the centre of
  its colour's cell (Closest sampling), so colours survive Roblox's importer exactly.
- Rig-part names (Body, Head, Jaw, LegFL..., Tail1..., WingL...) are the Studio contract; helper
  pieces must be merged into a rig part with join_as().
"""
import bpy, bmesh, os, math
from mathutils import Matrix, Vector, Euler

ROOT = os.path.dirname(os.path.abspath(__file__))
EXPORT = os.path.join(ROOT, "export")
RENDERS = os.path.join(ROOT, "renders")
SOURCE = os.path.join(ROOT, "source")
for d in (EXPORT, RENDERS, SOURCE):
    os.makedirs(d, exist_ok=True)

_S = {"name": None, "colors": {}, "mat": None}


def new_scene(name):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _S.update(name=name, colors={}, mat=None)


def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def palette(colors):
    """colors: {name: '#rrggbb'} (max 64). Builds the palette image + the single material."""
    img = bpy.data.images.new(_S["name"] + "_palette", 64, 64, alpha=False)
    px = [0.0] * (64 * 64 * 4)
    for i, (cname, hexv) in enumerate(colors.items()):
        _S["colors"][cname] = i
        r, g, b = _hex(hexv)
        cx, cy = (i % 8) * 8, (i // 8) * 8
        for y in range(cy, cy + 8):
            for x in range(cx, cx + 8):
                k = (y * 64 + x) * 4
                px[k:k + 4] = [r, g, b, 1.0]
    img.pixels = px
    img.filepath_raw = os.path.join(EXPORT, _S["name"] + "_palette.png")
    img.file_format = "PNG"
    img.save()
    mat = bpy.data.materials.new(_S["name"] + "_mat")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.8
    _S["mat"] = mat
    return mat


def _uv(color):
    i = _S["colors"][color]
    return ((i % 8) + 0.5) / 8, ((i // 8) + 0.5) / 8


def _finish(bm, name, color, loc, rot, smooth):
    m = Matrix.Translation(Vector(loc)) @ Euler([math.radians(a) for a in rot]).to_matrix().to_4x4()
    bmesh.ops.transform(bm, matrix=m, verts=bm.verts)
    uvl = bm.loops.layers.uv.verify()
    u, v = _uv(color)
    for f in bm.faces:
        f.smooth = smooth
        for l in f.loops:
            l[uvl].uv = (u, v)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(_S["mat"])
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def box(name, size, loc, color, bevel=0.12, rot=(0, 0, 0), taper=None, segs=1):
    """Beveled box. size=(x,y,z). taper=(sx,sy) scales the top (+Z) face."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for vert in bm.verts:
        vert.co = Vector((vert.co.x * size[0], vert.co.y * size[1], vert.co.z * size[2]))
        if taper and vert.co.z > 0:
            vert.co.x *= taper[0]
            vert.co.y *= taper[1]
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel * min(size), segments=segs,
                        profile=0.5, affect="EDGES", clamp_overlap=True)
    return _finish(bm, name, color, loc, rot, smooth=False)


def ellipsoid(name, radii, loc, color, segs=12, rings=8, rot=(0, 0, 0), smooth=True):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=1.0)
    for vert in bm.verts:
        vert.co = Vector((vert.co.x * radii[0], vert.co.y * radii[1], vert.co.z * radii[2]))
    return _finish(bm, name, color, loc, rot, smooth)


def cone(name, r1, r2, depth, loc, color, verts=8, rot=(0, 0, 0), smooth=False):
    """Cone/cylinder along +Z, base (r1) at loc, tip (r2) at loc + depth (before rot)."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=verts,
                          radius1=r1, radius2=max(r2, 0.0001), depth=depth)
    bmesh.ops.translate(bm, vec=Vector((0, 0, depth / 2)), verts=bm.verts)
    return _finish(bm, name, color, loc, rot, smooth)


def limb(name, p0, p1, r0, r1, color, verts=8, smooth=True):
    """Tapered cylinder from world point p0 (radius r0) to p1 (radius r1)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=verts,
                          radius1=r0, radius2=max(r1, 0.0001), depth=d.length)
    bmesh.ops.translate(bm, vec=Vector((0, 0, d.length / 2)), verts=bm.verts)
    rotm = d.normalized().to_track_quat("Z", "Y").to_matrix().to_4x4()
    bmesh.ops.transform(bm, matrix=Matrix.Translation(p0) @ rotm, verts=bm.verts)
    return _finish(bm, name, color, (0, 0, 0), (0, 0, 0), smooth)


def mirror_x(ob, name):
    """Copy of ob mirrored across X=0 (world). Keeps UVs/colours."""
    me = ob.data.copy()
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.scale(bm, vec=Vector((-1, 1, 1)), verts=bm.verts)
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    new = bpy.data.objects.new(name, me)
    new.location = Vector((-ob.location.x, ob.location.y, ob.location.z))
    bpy.context.scene.collection.objects.link(new)
    return new


def join_as(name, objs):
    objs = [o for o in objs if o]
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.name = name
    ob.data.name = name
    return ob


def pivot(ob, point):
    """Move ob's origin to world point without moving its geometry."""
    p = Vector(point)
    delta = p - ob.location
    ob.data.transform(Matrix.Translation(-delta))
    ob.location = p


def eye_pair(x, y, z, r, white="white", pupil="pupil", shine="white", look=0.0):
    """Cute eyes on the -Y face: white ball, dark pupil, tiny highlight. Returns [objs]."""
    out = []
    for sx in (1, -1):
        ex = x * sx
        out.append(ellipsoid("_eye", (r, r * 0.6, r), (ex, y, z), white, segs=10, rings=6))
        out.append(ellipsoid("_pupil", (r * 0.62, r * 0.35, r * 0.7),
                             (ex + look * r * sx, y - r * 0.42, z - r * 0.05), pupil, segs=8, rings=6))
        out.append(ellipsoid("_shine", (r * 0.2, r * 0.12, r * 0.2),
                             (ex + r * 0.25 * sx, y - r * 0.7, z + r * 0.3), shine, segs=6, rings=4))
    return out


def meshes():
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]


def tri_count():
    return sum(len(p.vertices) - 2 for o in meshes() for p in o.data.polygons)


def check_names():
    bad = [o.name for o in meshes() if o.name.startswith("_")]
    assert not bad, "helper pieces not joined into a rig part: %s" % bad


def export_fbx(path):
    check_names()
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes():
        o.select_set(True)
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, path_mode="COPY",
                             embed_textures=True, apply_unit_scale=True, object_types={"MESH"},
                             add_leaf_bones=False)


def render(path, size=512):
    sc = bpy.context.scene
    lo = Vector((1e9,) * 3)
    hi = Vector((-1e9,) * 3)
    for o in meshes():
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            lo = Vector(map(min, lo, w))
            hi = Vector(map(max, hi, w))
    ctr = (lo + hi) / 2
    rad = (hi - lo).length / 2
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    sc.collection.objects.link(cam)
    d = rad * 3.0
    cam.location = ctr + Vector((d * 0.55, -d * 0.8, d * 0.35))
    cam.rotation_euler = (ctr - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 50
    sc.camera = cam
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light = "STUDIO"
    sh.color_type = "TEXTURE"
    sh.show_cavity = True
    sh.show_shadows = True
    sc.render.film_transparent = False
    sc.world = sc.world or bpy.data.worlds.new("W")
    sc.render.resolution_x = sc.render.resolution_y = size
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)


def write_joints(path):
    """Sidecar for the Studio rigger: per part its joint (origin) and bbox centre, Blender coords."""
    import json
    data = {}
    for o in meshes():
        ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
        lo = Vector((min(w.x for w in ws), min(w.y for w in ws), min(w.z for w in ws)))
        hi = Vector((max(w.x for w in ws), max(w.y for w in ws), max(w.z for w in ws)))
        data[o.name] = {"joint": list(o.location), "center": list((lo + hi) / 2), "size": list(hi - lo)}
    with open(path, "w") as f:
        json.dump(data, f, indent=1)


def save_source():
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(SOURCE, _S["name"] + ".blend"))


def finish(name):
    """Standard end of a creature build: checks, source .blend, FBX, preview render."""
    tris = tri_count()
    assert tris < 3000, "%s has %d tris" % (name, tris)
    save_source()
    export_fbx(os.path.join(EXPORT, name + ".fbx"))
    write_joints(os.path.join(EXPORT, name + "_joints.json"))
    render(os.path.join(RENDERS, name + ".png"))
    print("CREATURE_OK", name, tris, sorted(o.name for o in meshes()))
    return tris
