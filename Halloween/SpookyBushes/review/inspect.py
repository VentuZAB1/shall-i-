# Independent reviewer: fresh FBX import + technical checks. Usage: blender -b --factory-startup --python inspect.py -- <fbx>...
import bpy, sys, os, json
import numpy as np
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
out = {}
for path in args:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=path)
    dg = bpy.context.evaluated_depsgraph_get()
    rec = {"objects": {}, "images": {}}
    allmin = Vector((1e9,) * 3); allmax = Vector((-1e9,) * 3)
    for ob in bpy.context.scene.objects:
        if ob.type != "MESH":
            rec["objects"][ob.name] = {"type": ob.type}
            continue
        me = ob.data
        me.calc_loop_triangles()
        tris = len(me.loop_triangles)
        mw = ob.matrix_world
        co = np.array([(mw @ v.co)[:] for v in me.vertices]) / ob.scale[0]   # studs (import scale is 0.01)
        mn, mx = co.min(0), co.max(0)
        allmin = Vector(np.minimum(allmin[:], mn)); allmax = Vector(np.maximum(allmax[:], mx))
        mats = []
        for m in me.materials:
            if not m:
                continue
            info = {"name": m.name, "tex": []}
            if m.use_nodes:
                for n in m.node_tree.nodes:
                    if n.type == "TEX_IMAGE" and n.image:
                        outs = [l.to_node.type + ":" + l.to_socket.name for o in n.outputs for l in o.links]
                        info["tex"].append({"img": n.image.name, "links": outs})
                info["blend_method"] = getattr(m, "blend_method", None)
            mats.append(info)
        rec["objects"][ob.name] = {
            "tris": tris, "verts": len(me.vertices), "loc": [round(x, 4) for x in ob.location],
            "rot": [round(x, 4) for x in ob.rotation_euler], "scale": [round(x, 4) for x in ob.scale],
            "dims_world": [round(float(x), 3) for x in (mx - mn)],
            "min": [round(float(x), 3) for x in mn], "max": [round(float(x), 3) for x in mx],
            "uv_layers": [u.name for u in me.uv_layers], "color_attrs": [c.name for c in me.color_attributes],
            "smooth_frac": round(sum(p.use_smooth for p in me.polygons) / max(1, len(me.polygons)), 3),
            "materials": mats,
        }
        # vertices below ground
        below = co[:, 2] < -0.3
        rec["objects"][ob.name]["n_verts_below_-0.3"] = int(below.sum())
    for img in bpy.data.images:
        if img.size[0] == 0:
            rec["images"][img.name] = {"size": [0, 0], "packed": bool(img.packed_file)}
            continue
        px = np.empty(img.size[0] * img.size[1] * 4, dtype=np.float32)
        img.pixels.foreach_get(px)
        px = px.reshape(-1, 4)
        a = px[:, 3]
        rec["images"][img.name] = {
            "size": list(img.size), "channels": img.channels, "depth": img.depth, "packed": bool(img.packed_file),
            "filepath": img.filepath, "alpha_min": round(float(a.min()), 3), "alpha_mean": round(float(a.mean()), 3),
            "frac_alpha_lt_0.5": round(float((a < 0.5).mean()), 3),
            "rgb_mean": [round(float(x), 3) for x in px[:, :3].mean(0)],
            "frac_near_black": round(float((px[:, :3].max(1) < 0.03).mean()), 4),
        }
    tot = sum(o.get("tris", 0) for o in rec["objects"].values())
    rec["total_tris"] = tot
    rec["bbox_min"] = [round(x, 3) for x in allmin]; rec["bbox_max"] = [round(x, 3) for x in allmax]
    rec["size_roblox_XYZ"] = [round(allmax.x - allmin.x, 3), round(allmax.z - allmin.z, 3), round(allmax.y - allmin.y, 3)]
    rec["unit_scale"] = bpy.context.scene.unit_settings.scale_length
    out[os.path.basename(path)] = rec

dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inspect_report" + os.environ.get("REVIEW_TAG", "") + ".json")
with open(dst, "w") as f:
    json.dump(out, f, indent=1)
print("WROTE", dst)
