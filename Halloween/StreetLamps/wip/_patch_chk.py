p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\StreetLamps\lamp.py"
s = open(p, encoding="utf-8").read()
old = '''def bvh_faces(ob, keep_mat=None, drop_mat=None):
    me = ob.data
    V = [ob.matrix_world @ v.co for v in me.vertices]
    F = [tuple(p.vertices) for p in me.polygons
         if (keep_mat is None or p.material_index in keep_mat) and (drop_mat is None or p.material_index not in drop_mat)]
    return BVHTree.FromPolygons(V, F, all_triangles=False)'''
new = '''def bvh_faces(ob, keep_mat=None, drop_mat=None, drop_fn=None):
    me = ob.data
    V = [ob.matrix_world @ v.co for v in me.vertices]
    F = [tuple(p.vertices) for p in me.polygons
         if (keep_mat is None or p.material_index in keep_mat) and (drop_mat is None or p.material_index not in drop_mat)
         and (drop_fn is None or not drop_fn(p))]
    return BVHTree.FromPolygons(V, F, all_triangles=False)'''
assert old in s
s = s.replace(old, new)
old2 = '''    cb = bvh_faces(cage, drop_mat={CAGE_GROUPS.index("seat")})'''
new2 = '''    # the seat zone (saucer, collar, drop finial and the strap ends converging under the saucer) is exempt
    cb = bvh_faces(cage, drop_mat={CAGE_GROUPS.index("seat")},
                   drop_fn=lambda p: (p.center.z < zb + 0.02 and math.hypot(p.center.x, p.center.y - HANG_Y) < 0.66))'''
assert old2 in s
s = s.replace(old2, new2)
open(p, "w", encoding="utf-8").write(s)
print("ok")
