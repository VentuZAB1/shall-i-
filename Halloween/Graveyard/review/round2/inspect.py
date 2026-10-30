# Independent reviewer: import each FBX fresh, report technical facts (read-only on builder files).
import bpy, sys, os, json, math
from mathutils import Vector
names = ["Halloween_Grave_C", "Halloween_DeadGrass_A", "Halloween_DeadGrass_B"]
out = {}
for n in names:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    p = os.path.join(r"C:\cdimp", n + ".fbx")
    bpy.ops.import_scene.fbx(filepath=p)
    bpy.context.view_layer.update()
    rec = {"objects": []}
    allv = []
    for ob in bpy.context.scene.objects:
        if ob.type != "MESH":
            rec["objects"].append({"name": ob.name, "type": ob.type})
            continue
        me = ob.data
        me.calc_loop_triangles()
        tris = len(me.loop_triangles)
        mw = ob.matrix_world
        vs = [mw @ v.co for v in me.vertices]
        allv += vs
        mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
        mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
        mats = []
        for m in me.materials:
            imgs = []
            if m and m.use_nodes:
                for nd in m.node_tree.nodes:
                    if nd.type == "TEX_IMAGE" and nd.image:
                        im = nd.image
                        links = [l.to_socket.name + "@" + l.to_node.name for l in nd.outputs[0].links] + [l.to_socket.name + "@" + l.to_node.name for l in nd.outputs[1].links]
                        imgs.append({"img": im.name, "size": list(im.size), "packed": bool(im.packed_file), "file": im.filepath,
                                     "cs": im.colorspace_settings.name, "links": links, "channels": im.channels})
            mats.append({"mat": m.name if m else None, "imgs": imgs})
        # vertex colour attrs
        attrs = [a.name for a in me.color_attributes]
        uvs = [u.name for u in me.uv_layers]
        # normals: check if custom split normals / smooth
        smooth_frac = sum(1 for p_ in me.polygons if p_.use_smooth) / max(1, len(me.polygons))
        # facing: centroid of faces by normal direction weighted area
        aY = {"-Y": 0.0, "+Y": 0.0}
        for p_ in me.polygons:
            nW = (mw.to_3x3() @ p_.normal).normalized()
            if nW.y < -0.7: aY["-Y"] += p_.area
            if nW.y > 0.7: aY["+Y"] += p_.area
        rec["objects"].append({"name": ob.name, "tris": tris, "verts": len(me.vertices), "faces": len(me.polygons),
                               "loc": list(ob.location), "rot": [round(math.degrees(r), 2) for r in ob.rotation_euler],
                               "scale": list(ob.scale), "dims": [round(d, 3) for d in ob.dimensions],
                               "bbox_min": [round(c, 3) for c in mn], "bbox_max": [round(c, 3) for c in mx],
                               "materials": mats, "color_attrs": attrs, "uvs": uvs, "smooth_frac": round(smooth_frac, 3),
                               "area_facing": {k: round(v, 3) for k, v in aY.items()}})
        # verts below -0.3
        rec["objects"][-1]["verts_below_-0.3"] = sum(1 for v in vs if v.z < -0.3)
        rec["objects"][-1]["verts_below_0"] = sum(1 for v in vs if v.z < 0)
        # centroid xy of verts with z<0.05 (ground contact) 
        g = [v for v in vs if v.z < 0.05]
        if g:
            rec["objects"][-1]["ground_centroid_xy"] = [round(sum(v.x for v in g) / len(g), 3), round(sum(v.y for v in g) / len(g), 3)]
    out[n] = rec
print("REVIEWJSON" + json.dumps(out, indent=1))
with open(os.path.join(os.path.dirname(__file__), "inspect.json"), "w") as f:
    json.dump(out, f, indent=1)
