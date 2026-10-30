import bpy, sys, os, math
f = sys.argv[sys.argv.index("--")+1]; out = sys.argv[sys.argv.index("--")+2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=f)
sc=bpy.context.scene; sc.render.engine="BLENDER_WORKBENCH"; sc.display.shading.light="STUDIO"; sc.display.shading.color_type="MATERIAL"
sc.render.resolution_x=sc.render.resolution_y=300
import mathutils
objs=[o for o in sc.objects if o.type=="MESH"]
mn=mathutils.Vector((1e9,)*3); mx=-mn
for o in objs:
    for c in o.bound_box:
        w=o.matrix_world@mathutils.Vector(c); mn=mathutils.Vector(map(min,mn,w)); mx=mathutils.Vector(map(max,mx,w))
ctr=(mn+mx)/2; size=max(mx-mn)
cam=bpy.data.objects.new("c",bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera=cam
cam.data.type="ORTHO"; cam.data.ortho_scale=size*1.2
cam.location=ctr+mathutils.Vector((0,-size*3,0)); cam.rotation_euler=(math.radians(90),0,0)
sc.render.filepath=out; bpy.ops.render.render(write_still=True)
print("SIZE", tuple(round(x,2) for x in (mx-mn)), "meshes", len(objs), "mats", len(bpy.data.materials), "imgs", [(i.name,tuple(i.size)) for i in bpy.data.images])
