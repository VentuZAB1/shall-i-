# SLINGSHOT Meteor Shower - HIGH QUALITY models (owner 2026-10-11: "they are low polygon, we need high quality").
# Game-art pipeline, all procedural and headless:
#   1. a dense sculpt (icosphere up to 330k tris) displaced by layered noise: lumpy body, Voronoi plates, magma cracks
#      along some plate edges, craters with rims, thumbprint pits (regmaglypts) on the ablated leading face, fine grain;
#      per-vertex albedo + roughness (basalt, scorched fusion crust, soot, a hot crack ramp)
#   2. a game mesh: the sculpt decimated to a budget (Roblox: max 20k tris), smooth shaded, Smart UV
#   3. bakes from sculpt to game mesh (Cycles): tangent NORMAL map, albedo (DIFFUSE colour), ROUGHNESS, AO (multiplied
#      into the albedo) -> SurfaceAppearance in Roblox. No emissive / neon (owner rule): the magma is albedo colour, the
#      glow is VFX.
# Headless:
#   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python build_hq.py -- rocks
#   steps: rocks | cloud | render | export | all
# Units: 1 Blender metre = 1 Roblox stud (FBX global_scale 0.01). Rocks: the hot leading face points along Blender +Y =
# Roblox -Z (LookVector), like the old models (the client flies them with CFrame.lookAt(pos, pos + velocity)).
import bpy, bmesh, math, os, sys, random, json
from mathutils import Vector, noise
import numpy as np

OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Weather\Meteor\HQ"
os.makedirs(OUT, exist_ok=True)
BLEND = os.path.join(OUT, "meteor_hq.blend")

ROCKS = {  # name: seed, radius, sculpt subdiv, game tris, texture px, stretch (x, y=front, z), plate scale, craters
    "Meteor": (101, 3.5, 8, 7000, 1024, (1.0, 1.1, 0.9), 2.0, 3),
    "MeteorBig": (202, 30.0, 9, 19500, 1024, (1.0, 1.14, 0.88), 2.4, 6),
    "MeteorChunk": (303, 1.1, 7, 1500, 512, (1.0, 1.15, 0.8), 1.6, 1),
}


def smoothstep(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def fbm(p, octaves, lac=2.03, gain=0.5):
    s, a, f = 0.0, 1.0, 1.0
    for _ in range(octaves):
        s += a * noise.noise(p * f)
        a *= gain
        f *= lac
    return s


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


HOT_RAMP = [  # crack depth -> colour (linear): ember wall -> red -> orange -> yellow core
    (0.0, (0.05, 0.02, 0.012)),
    (0.3, (0.30, 0.035, 0.008)),
    (0.55, (0.85, 0.16, 0.02)),
    (0.8, (1.0, 0.42, 0.05)),
    (1.0, (1.0, 0.72, 0.22)),
]


def ramp(t, stops):
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t <= t1:
            return mix(c0, c1, (t - t0) / (t1 - t0))
    return stops[-1][1]


def fresh():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 24
    w = bpy.data.worlds.new("W")
    sc.world = w
    return sc


# ------------------------------------------------------------------ 1. the sculpt
def smin(a, b, k):
    h = max(k - abs(a - b), 0.0) / k
    return min(a, b) - h * h * k * 0.25


def warp(p, amt, f, o):
    return p + Vector((noise.noise(p * f + o), noise.noise(p * f + o + Vector((5.2, 1.3, 2.8))),
                       noise.noise(p * f + o + Vector((1.7, 9.2, 4.4))))) * amt


def sculpt_rock(sc, name, seed, R, subdiv, stretch, plate_k, n_craters):
    rng = random.Random(seed)
    off = Vector((rng.uniform(-60, 60), rng.uniform(-60, 60), rng.uniform(-60, 60)))
    planes = []  # fracture faces: the rock is a broken chunk, not a ball
    for _ in range(rng.randint(5, 7)):
        n = Vector((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))).normalized()
        planes.append((n, rng.uniform(0.66, 0.86)))
    craters = []
    for _ in range(n_craters):
        c = Vector((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))).normalized()
        if c.y > 0.3:  # the burning front is ablating: no craters there
            c = Vector((c.x, -abs(c.y), c.z)).normalized()
        craters.append((c, rng.uniform(0.14, 0.3), rng.uniform(0.025, 0.055)))
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    cols, roughs, hots = [], [], []
    for v in bm.verts:
        d = v.co.normalized()
        p = d + off
        front = smoothstep(0.15, 0.85, d.y)
        back = smoothstep(0.1, 0.8, -d.y)
        side = 1.0 - smoothstep(0.35, 0.9, abs(d.y))
        # big form: lumps, then the fracture faces (smooth-min = slightly worn edges)
        h = 1.0 + 0.2 * fbm(p * 0.9, 3)
        for n, dk in planes:
            dn = d.dot(n)
            if dn > 0.05:
                h = smin(h, dk / dn, 0.07)
        h += 0.035 * (1 - abs(noise.noise(p * 3.1 + Vector((2, 7, 1))))) ** 2 * (1 - 0.7 * front)  # ridged rock
        # crack network: domain-warped Voronoi seams, uneven width, mostly on the hot half
        q = warp(p * plate_k, 0.45, 0.8, Vector((3, 3, 3)))
        dist, _pts = noise.voronoi(q, distance_metric="DISTANCE")
        edge = dist[1] - dist[0]
        width = (0.05 + 0.07 * (0.5 + 0.5 * noise.noise(p * 2.4 + Vector((8, 1, 6)))))
        present = min(1.0, smoothstep(-0.2, 0.25, noise.noise(p * 1.25 + Vector((7, 7, 7)))) + 0.8 * front)
        crack = (1 - smoothstep(0.0, width, edge)) * present
        halo = (1 - smoothstep(0.0, width * 3.2, edge)) * present
        seam = (1 - smoothstep(0.0, 0.05, edge)) * (1 - present)                 # dead (cold) seams elsewhere
        h -= 0.055 * crack ** 0.7 + 0.012 * seam
        crater_floor = 0.0
        for c, r, dep in craters:
            t = math.acos(max(-1.0, min(1.0, d.dot(c)))) / r
            if t < 1.7:
                if t < 1:
                    h -= dep * (1 - t * t) ** 1.5
                    crater_floor = max(crater_floor, 1 - t)
                h += dep * 0.35 * math.exp(-((t - 1) / 0.22) ** 2)
        # melt-flow streaks on the flanks, running from the burning front back (along Y)
        s = Vector((d.x * 10.0, d.y * 1.4, d.z * 10.0)) + off
        streak = (1 - abs(noise.noise(s))) ** 4
        h += 0.012 * streak * side
        h += 0.007 * fbm(p * 13.0, 3) * (1 - 0.6 * front)                       # grain
        v.co = Vector((d.x * stretch[0], d.y * stretch[1], d.z * stretch[2])) * h * R
        # colour (linear): charcoal basalt, dusty crater floors, a dark glassy fusion crust on the front, soot behind
        g = 0.5 + 0.5 * fbm(p * 5.0 + Vector((9, 2, 4)), 3)
        col = mix((0.024, 0.022, 0.021), (0.068, 0.062, 0.058), g)
        col = mix(col, (0.09, 0.085, 0.08), 0.45 * crater_floor)
        col = mix(col, (0.035, 0.016, 0.01), 0.8 * front)
        col = mix(col, (0.045, 0.025, 0.016), 0.5 * streak * side)
        col = mix(col, (0.013, 0.012, 0.012), 0.55 * back)
        rough = 0.88 - 0.3 * front - 0.15 * streak * side
        col = mix(col, (0.22, 0.025, 0.004), 0.85 * halo * (1 - crack))       # heated rims
        if crack > 0.001:
            col = mix(col, ramp(min(1.0, crack * (1.1 + 0.5 * front)), HOT_RAMP), smoothstep(0.0, 0.35, crack))
            rough = rough + (0.62 - rough) * crack
        cols.append(col)
        roughs.append(rough)
        hots.append(max(crack, 0.6 * halo))
    me = bpy.data.meshes.new(name + "_hi")
    bm.to_mesh(me)
    bm.free()
    for nm, vals in (("Col", [[c[0], c[1], c[2], 1.0] for c in cols]), ("Rough", [[r, r, r, 1.0] for r in roughs]),
                     ("Hot", [[h, h, h, 1.0] for h in hots])):
        ca = me.color_attributes.new(nm, "FLOAT_COLOR", "POINT")
        ca.data.foreach_set("color", np.array(vals, dtype=np.float32).ravel())
    for poly in me.polygons:
        poly.use_smooth = True
    ob = bpy.data.objects.new(name + "_hi", me)
    sc.collection.objects.link(ob)
    return ob


# ------------------------------------------------------------------ 2. the game mesh
def mesh_from(ob, name):
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    me.name = name
    return me


def only(ob):
    for o in bpy.context.scene.objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob


def game_mesh(sc, hi, name, target):
    lo = bpy.data.objects.new(name, hi.data.copy())
    sc.collection.objects.link(lo)
    dec = lo.modifiers.new("Decimate", "DECIMATE")
    dec.ratio = min(1.0, target / len(hi.data.polygons))
    lo.modifiers.new("Tri", "TRIANGULATE")
    me = mesh_from(lo, name)
    lo.modifiers.clear()
    lo.data = me
    for a in list(me.color_attributes):
        me.color_attributes.remove(a)
    for poly in me.polygons:
        poly.use_smooth = True
    only(lo)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.004)
    bpy.ops.object.mode_set(mode="OBJECT")
    return lo


# ------------------------------------------------------------------ 3. bakes
def save_png(img, path):
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()


def bake_set(sc, lo, hi, size, prefix, R, albedo_from_vc=True, ao_strength=0.6):
    imgs = {}
    for key, cs in (("albedo", "sRGB"), ("normal", "Non-Color"), ("rough", "Non-Color"), ("ao", "Non-Color"),
                    ("hot", "Non-Color")):
        img = bpy.data.images.new(prefix + "_" + key, size, size, alpha=False)
        img.colorspace_settings.name = cs
        imgs[key] = img
    mat = bpy.data.materials.new(prefix + "_bake")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    lo.data.materials.clear()
    lo.data.materials.append(mat)
    hm = bpy.data.materials.new(prefix + "_hi")
    hm.use_nodes = True
    bsdf = hm.node_tree.nodes["Principled BSDF"]
    if albedo_from_vc:
        vc = hm.node_tree.nodes.new("ShaderNodeVertexColor")
        vc.layer_name = "Col"
        hm.node_tree.links.new(vc.outputs["Color"], bsdf.inputs["Base Color"])
        vr = hm.node_tree.nodes.new("ShaderNodeVertexColor")
        vr.layer_name = "Rough"
        hm.node_tree.links.new(vr.outputs["Color"], bsdf.inputs["Roughness"])
        vh = hm.node_tree.nodes.new("ShaderNodeVertexColor")
        vh.layer_name = "Hot"
        hm.node_tree.links.new(vh.outputs["Color"], bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = 1.0
    hi.data.materials.clear()
    hi.data.materials.append(hm)
    sc.world.light_settings.distance = 0.3 * R
    for o in sc.objects:
        o.select_set(False)
    hi.select_set(True)
    lo.select_set(True)
    bpy.context.view_layer.objects.active = lo

    def run(kind, img, **kw):
        tex.image = img
        nt.nodes.active = tex
        bpy.ops.object.bake(type=kind, use_selected_to_active=True, cage_extrusion=0.03 * R,
                            max_ray_distance=0.15 * R, margin=8, **kw)

    run("NORMAL", imgs["normal"], normal_space="TANGENT")
    run("AO", imgs["ao"])
    if albedo_from_vc:
        run("DIFFUSE", imgs["albedo"], pass_filter={"COLOR"})
        run("ROUGHNESS", imgs["rough"])
        run("EMIT", imgs["hot"])
    # AO into the albedo (Roblox has no AO slot), except where the cracks glow
    a = np.array(imgs["albedo"].pixels[:], dtype=np.float32).reshape(-1, 4)
    o = np.array(imgs["ao"].pixels[:], dtype=np.float32).reshape(-1, 4)
    hot = np.clip(np.array(imgs["hot"].pixels[:], dtype=np.float32).reshape(-1, 4)[:, :1], 0, 1) if albedo_from_vc else 0
    k = (1 - ao_strength) + ao_strength * o[:, :1]
    k = k + (1 - k) * hot
    a[:, :3] *= k
    imgs["albedo"].pixels[:] = a.ravel()
    paths = {}
    for key in ("albedo", "normal", "rough", "ao", "hot"):
        paths[key] = os.path.join(OUT, f"{prefix}_{key}.png")
        save_png(imgs[key], paths[key])
    return imgs, paths


def pbr_material(lo, name, imgs):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    t_a = nt.nodes.new("ShaderNodeTexImage")
    t_a.image = imgs["albedo"]
    nt.links.new(t_a.outputs["Color"], bsdf.inputs["Base Color"])
    t_n = nt.nodes.new("ShaderNodeTexImage")
    t_n.image = imgs["normal"]
    nmap = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(t_n.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    t_r = nt.nodes.new("ShaderNodeTexImage")
    t_r.image = imgs["rough"]
    nt.links.new(t_r.outputs["Color"], bsdf.inputs["Roughness"])
    bsdf.inputs["Metallic"].default_value = 0.0
    lo.data.materials.clear()
    lo.data.materials.append(m)


def build_rocks():
    sc = fresh()
    sc.name = "MeteorHQ"
    rep = {}
    x = 0.0
    for name, (seed, R, sub, tris, px, stretch, pk, ncr) in ROCKS.items():
        hi = sculpt_rock(sc, name, seed, R, sub, stretch, pk, ncr)
        lo = game_mesh(sc, hi, name, tris)
        hi.location.x = lo.location.x = x + R   # placed apart BEFORE the bake (rays must not hit the other rocks)
        bpy.context.view_layer.update()
        imgs, paths = bake_set(sc, lo, hi, px, name, R)
        pbr_material(lo, name + "_PBR", imgs)
        hi.hide_render = True
        hi.hide_viewport = True
        x += 2.4 * R + 6
        rep[name] = {"sculpt_tris": len(hi.data.polygons), "game_tris": len(lo.data.polygons),
                     "size": [round(v, 2) for v in lo.dimensions], "maps": list(paths.values())}
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return rep


# ------------------------------------------------------------------ review renders
def review(models=("Meteor", "MeteorBig", "MeteorChunk")):
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = 1400, 1000
    sc.view_settings.view_transform = "AgX"
    sc.render.film_transparent = False
    w = sc.world
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.32, 0.45, 0.65, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.7
    for nm, rot, e, col in (("Key", (40, 0, 35), 4.5, (1, 0.95, 0.88)), ("Rim", (70, 0, 200), 2.5, (1, 0.6, 0.35))):
        ld = bpy.data.lights.new(nm, "SUN")
        ld.energy, ld.color = e, col
        lo = bpy.data.objects.new(nm, ld)
        lo.rotation_euler = [math.radians(a) for a in rot]
        sc.collection.objects.link(lo)
    out = []
    for name in models:
        ob = bpy.data.objects[name]
        for o in sc.objects:
            if o.type == "MESH":
                o.hide_render = o is not ob
        r = max(ob.dimensions) / 2
        for tag, d in (("front", Vector((0.5, 1.0, 0.35))), ("side", Vector((1.0, -0.25, 0.3)))):
            cd = bpy.data.cameras.new("Cam")
            cam = bpy.data.objects.new("Cam", cd)
            sc.collection.objects.link(cam)
            cam.location = ob.location + d.normalized() * r * 4.2
            cam.rotation_euler = (ob.location - cam.location).to_track_quat("-Z", "Y").to_euler()
            cd.lens = 50
            sc.camera = cam
            p = os.path.join(OUT, f"review_{name}_{tag}.png")
            sc.render.filepath = p
            bpy.ops.render.render(write_still=True)
            bpy.data.objects.remove(cam)
            out.append(p)
    return out


FBX_ARGS = dict(use_selection=True, global_scale=0.01, apply_unit_scale=True, apply_scale_options="FBX_SCALE_NONE",
                axis_forward="-Z", axis_up="Y", object_types={"MESH"}, use_mesh_modifiers=True,
                mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False, path_mode="COPY",
                embed_textures=True)


def export(models=("Meteor", "MeteorBig", "MeteorChunk")):
    """One FBX per model, the model at the origin (Studio pivots a MeshPart at its bbox centre)."""
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    out = {}
    for name in models:
        ob = bpy.data.objects[name]
        keep = ob.location.copy()
        ob.location = (0, 0, 0)
        for o in bpy.context.scene.objects:
            o.select_set(o is ob)
        bpy.context.view_layer.objects.active = ob
        path = os.path.join(r"C:\cdimp", name + "HQ.fbx")
        bpy.ops.export_scene.fbx(filepath=path, **FBX_ARGS)
        ob.location = keep
        out[name] = {"fbx": path, "kb": round(os.path.getsize(path) / 1024, 1), "tris": len(ob.data.polygons)}
    return out


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["rocks"]
    step = argv[0]
    rep = {}
    if step in ("rocks", "all"):
        rep["rocks"] = build_rocks()
    if step in ("render", "all"):
        rep["render"] = review()
    if step in ("export", "all"):
        rep["export"] = export()
    print("HQ_REPORT " + json.dumps(rep))
