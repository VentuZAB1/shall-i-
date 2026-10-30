# blender -b --factory-startup --python _tools/game_raw.py -- <Name> [res=512]
# Idle f0 render from the GAME camera on a transparent background -> <Name>/<Name>_game_raw.png (for a game-cam icon,
# the same way <Name>_portrait_raw.png feeds icon3). Then: python _tools/game_icon.py <Name> <CmpA,CmpB,...>
import sys, runpy, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
res = int(opts.get("res", "512"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk = R3["pk"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
k.set_action("idle")
sc = bpy.context.scene
sc.frame_set(0)
g = bpy.data.objects.get("Ground")
if g:
    g.hide_render = True
sc.render.film_transparent = True
sc.render.resolution_x = sc.render.resolution_y = res
loc, tgt = pk.camera_for(k, "game")
pk.aim(sc.camera, loc, tgt)
sc.render.image_settings.color_mode = "RGBA"
sc.render.filepath = os.path.join(k.dir, name + "_game_raw.png")
bpy.ops.render.render(write_still=True)
print("GAME_RAW ok", sc.render.filepath)
