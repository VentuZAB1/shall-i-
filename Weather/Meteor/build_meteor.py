# SLINGSHOT - "Meteor Shower" weather models (Meteor, MeteorBig, MeteorChunk) + the HUD icon, built procedurally.
# Headless (does not touch the GUI Blender session):
#   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python build_meteor.py -- all
#   steps: build | render | export | icon | all
# Units: 1 Blender metre = 1 Roblox stud (FBX global_scale 0.01, like Weather/UFO/build_ufo.py).
# Colours: one 64x64 palette PNG (16 px cells), every face's UVs on the centre of its colour cell, Closest.
# Owner rule: NO emissive / neon on the game meshes. The magma cracks are inset geometry in hot palette colours; the
# glow comes later from VFX Studio effects. (The icon's flame trail is render-only and never exported.)
# Model axes: the HOT leading face points along Blender +Y = Roblox -Z (LookVector): the client flies a meteor with
# CFrame.lookAt(pos, pos + velocity), so the glowing side always leads.
import bpy, bmesh, math, os, sys, random, json
from mathutils import Vector, noise

OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Weather\Meteor"
BLEND = os.path.join(OUT, "meteor_models.blend")
os.makedirs(OUT, exist_ok=True)

PALETTE = [  # (name, sRGB hex); cell i -> column i % 4, row i // 4 (row 0 = bottom of the PNG)
    ("CHAR",    "1C1614"),   # 0  crater floors, deepest rock
    ("BASALT_D", "2E2522"),  # 1  dark basalt
    ("BASALT",  "463935"),   # 2  basalt
    ("ASH",     "655650"),   # 3  light ash ridges
    ("SCORCH",  "5A2E1E"),   # 4  heat-scorched rock (leading face)
    ("EMBER",   "7E2410"),   # 5  crack walls (dark red)
    ("MAGMA_R", "C9361A"),   # 6  magma red
    ("MAGMA_O", "FF7A1F"),   # 7  magma orange (the weather's colour)
    ("MAGMA_Y", "FFC247"),   # 8  magma yellow core
    ("HOTWHITE", "FFE9B0"),  # 9  hottest specks (leading face only)
    ("RUST",    "7A4A36"),   # 10 rusty iron flecks
    ("SOOT",    "241E1D"),   # 11 soot band behind the hot face
]
CI = {n: i for i, (n, _) in enumerate(PALETTE)}


def cell_uv(i):
    return ((i % 4) * 16 + 8) / 64.0, ((i // 4) * 16 + 8) / 64.0


def srgb_to_lin(c):
    return (c / 12.92) if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hexrgb(h):
    return tuple(int(h[k:k + 2], 16) / 255.0 for k in (0, 2, 4))


# ------------------------------------------------------------------ palette + material
def make_palette():
    path = os.path.join(OUT, "meteor_palette.png")
    img = bpy.data.images.new("meteor_palette_tmp", 64, 64, alpha=False)
    px = [0.0] * (64 * 64 * 4)
    for y in range(64):
        for x in range(64):
            i = (y // 16) * 4 + x // 16
            r, g, b = hexrgb(PALETTE[i][1] if i < len(PALETTE) else PALETTE[2][1])
            o = (y * 64 + x) * 4
            px[o:o + 4] = [r, g, b, 1.0]
    img.pixels[:] = px
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    bpy.data.images.remove(img)
    img = bpy.data.images.load(path, check_existing=False)
    img.name = "meteor_palette.png"
    return img


def palette_material(img):
    m = bpy.data.materials.new("Meteor_Palette")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.82
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    m.use_backface_culling = True
    return m


# ------------------------------------------------------------------ rock generator
def sphere_points(rng, n):
    pts = []
    for _ in range(n):
        z = rng.uniform(-1, 1)
        a = rng.uniform(0, 2 * math.pi)
        r = math.sqrt(1 - z * z)
        pts.append(Vector((r * math.cos(a), r * math.sin(a), z)))
    return pts


def build_rock(name, seed, radius, subdiv, craters, crack_cells, crack_w, inset=True, stretch=(1.0, 0.92, 1.08),
               bumps=0.17):
    rng = random.Random(seed)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    off = Vector((rng.uniform(0, 50), rng.uniform(0, 50), rng.uniform(0, 50)))
    crs = [(d, rng.uniform(0.26, 0.48), rng.uniform(0.10, 0.2)) for d in sphere_points(rng, craters)]
    # never put a crater dead-centre on the hot leading face (it reads as a hole in the glow)
    for v in bm.verts:
        d = v.co.normalized()
        h = noise.fractal(d * 1.6 + off, 0.75, 2.1, 4) * bumps + noise.noise(d * 4.5 + off) * bumps * 0.35
        for c, rad, depth in crs:
            a = d.angle(c)
            if a < rad * 1.25:
                x = a / rad
                if x < 0.85:
                    h -= depth * (1 - (x / 0.85) ** 2)
                else:
                    h += depth * 0.45 * math.sin((x - 0.85) / 0.4 * math.pi)
        s = 1.0 + h
        v.co = Vector((d.x * stretch[0], d.y * stretch[1], d.z * stretch[2])) * s * radius
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    pal = bm.faces.layers.int.new("pal")
    cells = sphere_points(rng, crack_cells)
    fwd = Vector((0, 1, 0))
    cell_shade = [rng.random() for _ in cells]

    def cell_of(d):
        return min(range(len(cells)), key=lambda k: (d - cells[k]).length)

    # 1. plates: every face belongs to the nearest Voronoi cell; plates are coloured per cell (+ heat, craters)
    cid = {}
    for f in bm.faces:
        d = f.calc_center_median().normalized()
        k = cell_of(d)
        cid[f] = k
        heat = max(0.0, d.dot(fwd))                      # 1 on the leading face, 0 at the sides/back
        n = noise.noise(d * 3.2 + off * 0.5) * 0.5 + cell_shade[k] - 0.5
        crater = any(d.angle(cc) < rad * 0.72 for cc, rad, _ in crs)
        if crater:
            f[pal] = CI["CHAR"] if heat < 0.55 else CI["SCORCH"]
        elif heat > 0.88:
            f[pal] = CI["MAGMA_R"] if n > 0.15 else CI["SCORCH"]
        elif heat > 0.62:
            f[pal] = CI["SCORCH"] if n > -0.25 else CI["BASALT_D"]
        elif d.dot(fwd) < -0.6 and n > 0.15:
            f[pal] = CI["SOOT"]
        else:
            f[pal] = CI["ASH"] if n > 0.33 else CI["BASALT"] if n > -0.1 else CI["BASALT_D"]
            if rng.random() < 0.03:
                f[pal] = CI["RUST"]
    # 2. cracks: the edges between two plates -> a thin bevelled groove, recessed, magma inside
    if inset:
        edges = [e for e in bm.edges if len(e.link_faces) == 2 and cid.get(e.link_faces[0]) != cid.get(e.link_faces[1])]
        heat_of = {e: max(0.0, ((e.verts[0].co + e.verts[1].co) / 2).normalized().dot(fwd)) for e in edges}
        res = bmesh.ops.bevel(bm, geom=edges, offset=crack_w * radius, offset_type="OFFSET", segments=1,
                              profile=0.5, affect="EDGES", clamp_overlap=True)
        groove = [f for f in res["faces"] if f.is_valid]
        for f in groove:
            f[pal] = CI["MAGMA_O"]
        ins = bmesh.ops.inset_region(bm, faces=groove, thickness=crack_w * radius * 0.25, depth=-crack_w * radius * 0.9,
                                     use_even_offset=True, use_boundary=True)
        for f in ins["faces"]:
            f[pal] = CI["EMBER"]            # the crack walls
        for f in groove:
            if f.is_valid:
                h = max(0.0, f.calc_center_median().normalized().dot(fwd))
                f[pal] = CI["MAGMA_Y"] if h > 0.55 else CI["MAGMA_O"]   # hotter (yellow) toward the leading face
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    uvl = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        u, v = cell_uv(f[pal])
        for l in f.loops:
            l[uvl].uv = (u, v)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = False             # faceted low-poly rock
    ob = bpy.data.objects.new(name, me)
    return ob


# ------------------------------------------------------------------ scene
STATE = {}


def fresh_file():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.name = "Meteors"
    return sc


def build_models():
    sc = fresh_file()
    img = make_palette()
    mat = palette_material(img)
    coll = bpy.data.collections.new("Meteors")
    sc.collection.children.link(coll)
    specs = [  # name, seed, radius, ico subdiv, craters, plates (Voronoi cells), crack half-width (x radius), cracks?
        ("Meteor", 101, 3.5, 3, 3, 11, 0.03, True, (1.0, 0.94, 1.06), 0.17),
        ("MeteorBig", 202, 30.0, 4, 7, 17, 0.019, True, (1.0, 0.9, 1.12), 0.15),
        ("MeteorChunk", 303, 1.1, 1, 0, 5, 0.0, False, (1.0, 0.85, 1.1), 0.22),
    ]
    x = 0.0
    objs = {}
    for name, seed, r, sub, ncr, cells, w, ins, st, bu in specs:
        ob = build_rock(name, seed, r, sub, ncr, cells, w, ins, st, bu)
        ob.data.materials.append(mat)
        coll.objects.link(ob)
        ob.location = (x + r, 0, 0)
        x += 2 * r + 6
        objs[name] = ob
    STATE["objs"] = objs
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return {n: {"tris": sum(len(p.vertices) - 2 for p in o.data.polygons), "size": [round(v, 2) for v in o.dimensions]}
            for n, o in objs.items()}


# ------------------------------------------------------------------ renders (review) + icon
def eevee(sc, res):
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.view_settings.view_transform = "Standard"
    try:
        sc.eevee.taa_render_samples = 64
    except Exception:
        pass


def world(sc, strength=0.6, col=(0.55, 0.5, 0.5)):
    w = bpy.data.worlds.new("MeteorWorld")
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (*col, 1.0)
    bg.inputs["Strength"].default_value = strength
    sc.world = w


def sun(sc, name, rot, energy, col=(1, 1, 1), ang=10):
    ld = bpy.data.lights.new(name, "SUN")
    ld.energy, ld.color, ld.angle = energy, col, math.radians(ang)
    o = bpy.data.objects.new(name, ld)
    o.rotation_euler = [math.radians(a) for a in rot]
    sc.collection.objects.link(o)
    return o


def camera(sc, loc, target, lens=50, ortho=None):
    cd = bpy.data.cameras.new("Cam")
    cam = bpy.data.objects.new("Cam", cd)
    sc.collection.objects.link(cam)
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cd.lens = lens
    cd.clip_end = 5000
    if ortho:
        cd.type = "ORTHO"
        cd.ortho_scale = ortho
    sc.camera = cam
    return cam


def render(sc, path):
    sc.render.filepath = path
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    bpy.ops.render.render(write_still=True, scene=sc.name)
    return path


def open_models():
    bpy.ops.wm.open_mainfile(filepath=BLEND)   # always a clean copy from disk (steps never save their extras)
    return bpy.data.scenes["Meteors"]


def review_renders():
    sc = open_models()
    eevee(sc, (1600, 900))
    world(sc)
    sun(sc, "Key", (40, 0, 35), 3.2, (1, 0.96, 0.9))
    sun(sc, "Fill", (200, 0, -150), 1.0, (0.8, 0.85, 1.0), 30)
    sun(sc, "Rim", (70, 0, 200), 1.6)
    objs = {o.name: o for o in sc.objects if o.type == "MESH"}
    out = []
    # each rock alone, three-quarter from the hot side and from the back
    for name, o in objs.items():
        for o2 in objs.values():
            o2.hide_render = o2 is not o
        r = max(o.dimensions) / 2
        c = o.location
        for tag, d in (("hot", Vector((0.55, 1.0, 0.45))), ("back", Vector((-0.6, -1.0, 0.35)))):
            cam = camera(sc, c + d.normalized() * r * 7.5, c, 50)
            out.append(render(sc, os.path.join(OUT, f"{name}_{tag}.png")))
            bpy.data.objects.remove(cam)
    for o2 in objs.values():
        o2.hide_render = False
    # lineup with a 5-stud player capsule
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=5, location=(-4, 0, 0))
    cap = bpy.context.active_object
    cap.name = "Player5"
    xs = [o.location.x for o in objs.values()] + [-4]
    camera(sc, ((min(xs) + max(xs)) / 2, -400, 25), ((min(xs) + max(xs)) / 2, 0, 0), ortho=(max(xs) - min(xs)) + 70)
    out.append(render(sc, os.path.join(OUT, "Meteor_lineup.png")))
    bpy.data.objects.remove(cap)
    return out


def trail_mesh(name, length, radius, segs=28, rings=22, wav=0.12, seed=1):
    """A flame tongue along +Z from the origin: radius r(s) = radius * (1-s)^0.75 with a little waviness. Vertex colour
    attribute 'Col' (rgba): yellow-white at the head -> orange -> red -> dark red, alpha fading to the tip."""
    rng = random.Random(seed)
    bm = bmesh.new()
    col = bm.loops.layers.float_color.new("Col")
    rows = []
    for j in range(rings + 1):
        s = j / rings
        flare = 0.42 + 0.58 * math.sin(min(1.0, s / 0.24) * math.pi / 2)   # narrow at the rock, flares out
        r = radius * flare * (1 - s) ** 0.75 * (1 + wav * math.sin(s * 9 + seed))
        z = s * length
        row = []
        for i in range(segs):
            a = 2 * math.pi * i / segs
            rr = r * (1 + wav * 0.6 * math.sin(a * 3 + s * 12 + seed))
            row.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a), z)))
        rows.append(row)
    stops = [(0.0, (1.0, 0.82, 0.4)), (0.2, (1.0, 0.52, 0.1)), (0.45, (0.95, 0.27, 0.05)), (0.75, (0.6, 0.08, 0.03)),
             (1.0, (0.25, 0.03, 0.02))]

    def grad(s):
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            if s <= b:
                k = (s - a) / (b - a)
                return tuple(ca[i] + (cb[i] - ca[i]) * k for i in range(3))
        return stops[-1][1]
    for j in range(rings):
        for i in range(segs):
            f = bm.faces.new((rows[j][i], rows[j][(i + 1) % segs], rows[j + 1][(i + 1) % segs], rows[j + 1][i]))
            for l in f.loops:
                s = l.vert.co.z / length
                c = grad(s)
                l[col] = (*c, max(0.0, 1 - s) ** 1.4)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    return bpy.data.objects.new(name, me)


def flame_material(name, strength, alpha_mul):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    attr = nt.nodes.new("ShaderNodeVertexColor")
    attr.layer_name = "Col"
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = alpha_mul
    nt.links.new(attr.outputs["Color"], em.inputs["Color"])
    nt.links.new(attr.outputs["Alpha"], mul.inputs[0])
    nt.links.new(mul.outputs[0], mix.inputs["Fac"])
    nt.links.new(tr.outputs["BSDF"], mix.inputs[1])
    nt.links.new(em.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    try:
        m.surface_render_method = "BLENDED"
    except Exception:
        m.blend_method = "BLEND"
    m.use_backface_culling = False
    return m


def icon():
    sc = open_models()
    for o in list(sc.objects):
        if o.type == "MESH" and o.name != "Meteor":
            o.hide_render = True
    met = sc.objects["Meteor"]
    met.location = (0, 0, 0)
    # dive toward the lower left: the hot face (+Y of the model) points along travel
    travel = Vector((-1.0, 0.0, -0.78)).normalized()
    from mathutils import Quaternion
    met.rotation_mode = "QUATERNION"
    met.rotation_quaternion = Quaternion(travel, math.radians(25)) @ Vector((0, 1, 0)).rotation_difference(travel)
    back = -travel
    q = Vector((0, 0, 1)).rotation_difference(back)
    for nm, L, R, strength, am, seed in (("TrailOuter", 17, 5.2, 1.0, 0.7, 3), ("TrailMid", 13, 4.2, 1.5, 0.9, 5),
                                          ("TrailCore", 7.5, 3.0, 2.2, 1.0, 7)):
        t = trail_mesh(nm, L, R, seed=seed)
        t.data.materials.append(flame_material(nm + "_Mat", strength, am))
        t.rotation_mode = "QUATERNION"
        t.rotation_quaternion = q
        t.location = back * 1.4
        sc.collection.objects.link(t)
    rng = random.Random(9)
    em = flame_material("Ember_Mat", 2.5, 1.0)
    for k in range(12):
        s = rng.uniform(0.35, 1.0)
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=rng.uniform(0.25, 0.55) * (1.2 - s))
        col = bm.loops.layers.float_color.new("Col")
        for f in bm.faces:
            for l in f.loops:
                l[col] = (1.0, 0.55 + 0.3 * rng.random(), 0.15, 1.0)
        me = bpy.data.meshes.new("Ember%d" % k)
        bm.to_mesh(me)
        bm.free()
        o = bpy.data.objects.new("Ember%d" % k, me)
        o.data.materials.append(em)
        side = Vector((-back.z, 0, back.x)) * rng.uniform(-3.2, 3.2) * s
        o.location = back * (4 + 13 * s) + side + Vector((0, rng.uniform(-1, 1), 0))
        sc.collection.objects.link(o)
    eevee(sc, (512, 512))
    world(sc, 0.5, (0.6, 0.55, 0.55))
    sun(sc, "Key", (35, 0, -60), 2.6, (1, 0.93, 0.85))
    sun(sc, "Rim", (60, 0, 160), 1.2)
    # the fire lights the rock from behind/above: a warm point light at the trail root
    pl = bpy.data.lights.new("FireLight", "POINT")
    pl.energy, pl.color, pl.shadow_soft_size = 2500, (1.0, 0.5, 0.15), 2.0
    po = bpy.data.objects.new("FireLight", pl)
    po.location = back * 5.5 + Vector((0, -4, 0))
    sc.collection.objects.link(po)
    centre = back * 5.0
    camera(sc, centre + Vector((0, -200, 0)), centre, ortho=23)
    raw = render(sc, os.path.join(OUT, "icon", "meteor_icon_raw.png"))
    return raw


def outline_icon():
    """512 px icon with the same dark sticker outline as the saucer icon (needs PIL: run from normal Python)."""
    from PIL import Image, ImageFilter
    src = Image.open(os.path.join(OUT, "icon", "meteor_icon_raw.png")).convert("RGBA")
    a = src.split()[3]
    mask = a.point(lambda v: 255 if v > 70 else 0)
    ink = mask.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.GaussianBlur(1.2))
    base = Image.new("RGBA", src.size, (22, 18, 20, 0))
    base.putalpha(ink)
    out = Image.alpha_composite(base, src)
    out.save(os.path.join(OUT, "icon", "meteor_icon.png"))
    return os.path.join(OUT, "icon", "meteor_icon.png")


FBX_ARGS = dict(use_selection=True, global_scale=0.01, apply_unit_scale=True, apply_scale_options="FBX_SCALE_NONE",
                axis_forward="-Z", axis_up="Y", object_types={"MESH"}, use_mesh_modifiers=True,
                mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False, path_mode="COPY",
                embed_textures=True)


def export():
    sc = open_models()
    objs = [o for o in sc.objects if o.type == "MESH" and o.name in ("Meteor", "MeteorBig", "MeteorChunk")]
    for o in sc.objects:
        o.select_set(o in objs)
    bpy.context.view_layer.objects.active = objs[0]
    path = os.path.join(OUT, "Meteors.fbx")
    bpy.ops.export_scene.fbx(filepath=path, **FBX_ARGS)
    return {"fbx": path, "kb": round(os.path.getsize(path) / 1024, 1)}


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["all"]
    step = argv[0]
    rep = {}
    if step in ("build", "all"):
        rep["build"] = build_models()
    if step in ("render", "all"):
        rep["render"] = review_renders()
    if step in ("export", "all"):
        rep["export"] = export()
    if step in ("icon", "all"):
        rep["icon"] = icon()
    print("METEOR_REPORT " + json.dumps(rep))
