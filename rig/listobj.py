import bpy, sys
from mathutils import Vector
f = sys.argv[sys.argv.index("--")+1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=f)
rows=[]
for o in bpy.context.scene.objects:
    if o.type!="MESH": continue
    ws=[o.matrix_world@v.co for v in o.data.vertices]
    if not ws: continue
    mn=Vector(map(min,*zip(*ws))) if False else Vector((min(w.x for w in ws),min(w.y for w in ws),min(w.z for w in ws)))
    mx=Vector((max(w.x for w in ws),max(w.y for w in ws),max(w.z for w in ws)))
    rows.append((o.name, len(ws), tuple(round(x,2) for x in mn), tuple(round(x,2) for x in mx), tuple(round(s,3) for s in o.matrix_world.to_scale())))
for r in rows: print("OBJ", *r)
