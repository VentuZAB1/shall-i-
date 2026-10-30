# blender -b <rigged.blend> --python topvert.py : highest mesh vertices (world) and their vertex group, rest pose
import bpy
for ob in bpy.data.objects:
    if ob.type != "MESH":
        continue
    names = {g.index: g.name for g in ob.vertex_groups}
    vs = sorted(ob.data.vertices, key=lambda v: -(ob.matrix_world @ v.co).z)[:5]
    for v in vs:
        g = names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None
        print("TOPVERT", ob.name, tuple(round(c, 3) for c in ob.matrix_world @ v.co), g)
ob = bpy.data.objects.get("Body")
names = {g.index: g.name for g in ob.vertex_groups}
for v in sorted(ob.data.vertices, key=lambda v: (ob.matrix_world @ v.co).z)[:3]:
    g = names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None
    print("LOWVERT", tuple(round(c, 3) for c in ob.matrix_world @ v.co), g)
dg = bpy.context.evaluated_depsgraph_get()
ev = ob.evaluated_get(dg)
me = ev.to_mesh()
zs = [(ev.matrix_world @ v.co).z for v in me.vertices]
print("EVAL z range", round(min(zs), 3), round(max(zs), 3), "frame", bpy.context.scene.frame_current,
      bpy.data.objects["Armature"].animation_data.action.name if bpy.data.objects.get("Armature") and bpy.data.objects["Armature"].animation_data and bpy.data.objects["Armature"].animation_data.action else None)
i = max(range(len(me.vertices)), key=lambda i: zs[i])
print("EVAL top", tuple(round(c, 3) for c in ev.matrix_world @ me.vertices[i].co))
arm = bpy.data.objects.get("Armature")
for b in ("Neck", "Head", "Chest", "Spine"):
    if arm and b in arm.pose.bones:
        print("POSE", b, [round(x, 3) for x in arm.pose.bones[b].rotation_quaternion], [round(x, 3) for x in arm.pose.bones[b].location])
