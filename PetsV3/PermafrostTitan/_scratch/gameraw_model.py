# blender -b --factory-startup --python PermafrostTitan/_scratch/gameraw_model.py -- <Name>
# model-only twin of _tools/game_raw.py (pets without clips yet): rest pose from the GAME camera, transparent
# -> <Name>/<Name>_game_raw.png, then: python _tools/game_icon.py <Name> <cmps> (gold px counter + strips)
import sys, runpy, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk = R3["pk"]
R3["model"](name, views=("tq",), res=200)
k = R3["STATE"]["k"]
sc = bpy.context.scene
g = bpy.data.objects.get("Ground")
if g:
    g.hide_render = True
sc.render.film_transparent = True
sc.render.resolution_x = sc.render.resolution_y = 512
loc, tgt = pk.camera_for(k, "game")
pk.aim(sc.camera, loc, tgt)
sc.render.image_settings.color_mode = "RGBA"
sc.render.filepath = os.path.join(k.dir, name + "_game_raw.png")
bpy.ops.render.render(write_still=True)
print("GAME_RAW ok", sc.render.filepath)
