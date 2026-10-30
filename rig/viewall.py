import bpy, os, math, glob
src=os.path.expanduser("~/Downloads/Meshy")
for f in sorted(glob.glob(src+"/*.glb")):
    n=os.path.basename(f)[:-4]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=f)
    sc=bpy.context.scene; sc.render.engine="BLENDER_WORKBENCH"; sc.display.shading.light="STUDIO"; sc.display.shading.color_type="TEXTURE"
    sc.render.resolution_x=sc.render.resolution_y=200
    cam=bpy.data.objects.new("c",bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera=cam
    cam.data.type="ORTHO"; cam.data.ortho_scale=2.2
    for k,(loc,rot) in {"side":((4,0,0.8),(math.radians(90),0,math.radians(90))),"front":((0,-4,0.8),(math.radians(90),0,0)),"top":((0,0,4),(0,0,0))}.items():
        cam.location=loc; cam.rotation_euler=rot
        sc.render.filepath=os.path.abspath(f"views/{n}_{k}.png"); bpy.ops.render.render(write_still=True)
