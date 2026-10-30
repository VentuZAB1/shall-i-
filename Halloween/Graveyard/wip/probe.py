import bpy, mathutils
from mathutils import noise, Vector
print("VER", bpy.app.version_string)
print([n for n in dir(noise) if not n.startswith("_")])
d, p = noise.voronoi(Vector((0.3,0.2,0.1)))
print("VOR", d, p[0], noise.cell(p[0]))
print(bpy.ops.uv.pack_islands.get_rna_type().properties.keys())
print(bpy.ops.object.bake.get_rna_type().properties.keys())
