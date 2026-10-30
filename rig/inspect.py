import bpy, sys, os, glob
from mathutils import Vector
src = os.path.expanduser("~/Downloads/Meshy")
for f in sorted(glob.glob(os.path.join(src, "*.glb"))):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=f)
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    tris = 0; mins = Vector((1e9,)*3); maxs = Vector((-1e9,)*3)
    for o in meshes:
        dg = bpy.context.evaluated_depsgraph_get()
        m = o.evaluated_get(dg).to_mesh()
        m.calc_loop_triangles(); tris += len(m.loop_triangles)
        for v in m.vertices:
            w = o.matrix_world @ v.co
            mins = Vector(map(min, mins, w)); maxs = Vector(map(max, maxs, w))
    imgs = [(i.name, tuple(i.size)) for i in bpy.data.images]
    arm = [o.name for o in bpy.context.scene.objects if o.type == "ARMATURE"]
    print("INSPECT", os.path.basename(f), "objs", len(meshes), "tris", tris, "size", tuple(round(x,2) for x in (maxs-mins)), "imgs", imgs, "arm", arm)
