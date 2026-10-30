# blender -b --factory-startup --python _tools/portrait_carrier.py -- out.fbx A.png B.png ...
# One FBX holding a textured plane per portrait PNG (embedded). Studio's 3D importer (creator ZAB Studio) then uploads
# every PNG as a GROUP-owned Image asset; read the ids from the imported MeshParts' TextureID and delete the model.
# (2026-10-14: the MCP upload_image tool uploads under the owner's USER account, but SLINGSHOT is group-owned.)
import bpy, sys, os
args = sys.argv[sys.argv.index("--") + 1:]
out, pngs = args[0], args[1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
for i, p in enumerate(pngs):
    name = os.path.splitext(os.path.basename(p))[0]
    bpy.ops.mesh.primitive_plane_add(size=1, location=(i * 1.5, 0, 0))
    ob = bpy.context.active_object
    ob.name = ob.data.name = name
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(os.path.abspath(p))
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    ob.data.materials.append(mat)
bpy.ops.export_scene.fbx(filepath=out, path_mode="COPY", embed_textures=True, use_selection=False,
                         object_types={"MESH"}, apply_unit_scale=True)
print("wrote", out, len(pngs))
