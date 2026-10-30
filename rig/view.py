import bpy, sys, os, math
from mathutils import Vector
name = sys.argv[sys.argv.index("--")+1]; out = sys.argv[sys.argv.index("--")+2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.expanduser(f"~/Downloads/Meshy/{name}.glb"))
objs=[o for o in bpy.context.scene.objects if o.type in("MESH","ARMATURE")]
sc=bpy.context.scene; sc.render.engine="BLENDER_WORKBENCH"; sc.display.shading.light="STUDIO"; sc.display.shading.color_type="TEXTURE"
sc.render.resolution_x=sc.render.resolution_y=400; sc.render.film_transparent=False
cam=bpy.data.objects.new("c",bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera=cam
cam.data.type="ORTHO"; cam.data.ortho_scale=2.4
import bpy_extras
views={"side":((4,0,0.6),(math.radians(90),0,math.radians(90))),"front":((0,-4,0.6),(math.radians(90),0,0)),"top":((0,0,4),(0,0,0))}

ims=[]
for k,(loc,rot) in views.items():
    cam.location=loc; cam.rotation_euler=rot
    p=f"{out}_{k}.png"; sc.render.filepath=p; bpy.ops.render.render(write_still=True); ims.append(p)
