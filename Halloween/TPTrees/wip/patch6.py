# Review round 1 fixes (paper realism, rolls, layout, lobed canopies, gloss, gaps)
src = open("tptree.py", encoding="utf-8").read()


def rep(a, b, cnt=1):
    global src
    assert src.count(a) == cnt, (a[:80], src.count(a))
    src = src.replace(a, b)


def replace_func(name, new_text, next_marker):
    global src
    s = src.index(name)
    e = src.index(next_marker, s)
    src = src[:s] + new_text + src[e:]


# =========================================================== canopy: lobes, flatter underside leaves
rep('''def blob_mesh(name, blobs, voxel, smooth_iter, namp, nfreq, seed, zfloor=None):''',
    '''def lobe_field(V, N, area, spacing, rad, amp, seed):
    """Leaf-cluster lobes: Poisson-ish seeds on the surface (min distance `spacing`), each a rounded bump of radius
    rad (range) and height amp (range); the max of the bumps leaves creases between lobes. Returns the displacement
    (mean-centred so the canopy keeps its size) and the normalised lobe value (1 = lobe top)."""
    from mathutils.kdtree import KDTree
    rng = np.random.default_rng(seed)
    cell = spacing / math.sqrt(3)
    grid = {}
    seeds = []
    for i in rng.permutation(len(V))[: int(area / spacing ** 2 * 30)]:
        p = V[i]
        key = tuple((p // cell).astype(int))
        ok = True
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                for dz in (-2, -1, 0, 1, 2):
                    for j in grid.get((key[0] + dx, key[1] + dy, key[2] + dz), ()):
                        if np.sum((V[j] - p) ** 2) < spacing ** 2:
                            ok = False
                            break
                    if not ok:
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            grid.setdefault(key, []).append(i)
            seeds.append(i)
    S = V[seeds]
    R = rng.uniform(*rad, len(seeds))
    A = rng.uniform(*amp, len(seeds))
    kd = KDTree(len(S))
    for j, p in enumerate(S):
        kd.insert(Vector(p.tolist()), j)
    kd.balance()
    bump = np.zeros(len(V))
    top = np.zeros(len(V))
    for i in range(len(V)):
        best, bt = 0.0, 0.0
        for co, j, d in kd.find_n(Vector(V[i].tolist()), 4):
            t = 1.0 - (d / R[j]) ** 2
            if t > 0:
                b = A[j] * t * t
                if b > best:
                    best, bt = b, t * t
        bump[i] = best
        top[i] = bt
    return bump - 0.55 * float(np.mean(A)), top, len(seeds)


def blob_mesh(name, blobs, voxel, smooth_iter, namp, nfreq, seed, zfloor=None, lobes=None):''')
rep('''    d = noise_field(V, nfreq, 3, off, namp)
    V = V + N * d[:, None].astype(np.float32)
    if zfloor is not None:
        V[:, 2] = np.maximum(V[:, 2], zfloor)
    set_co(ob, V)
    return ob''', '''    d = noise_field(V, nfreq, 3, off, namp)
    V = V + N * d[:, None].astype(np.float32)
    lobe_top = np.zeros(len(V))
    if lobes:
        area = mesh_area(ob)
        disp, lobe_top, nseed = lobe_field(V, N, area, lobes["spacing"], lobes["rad"], lobes["amp"], seed + 7)
        V = V + N * disp[:, None].astype(np.float32)
        log("  lobes", nseed, "on", name)
    if zfloor is not None:
        V[:, 2] = np.maximum(V[:, 2], zfloor)
    set_co(ob, V)
    ob["lobe_top"] = 0
    LOBE_TOP[ob.name] = lobe_top
    return ob''')
rep('''def tree_clumps(seed):''', '''LOBE_TOP = {}


def tree_clumps(seed):''')
# leaves: flatter on undersides (no grazing smears), carry the lobe value to the colour function
rep('''    tilt = rng.uniform(*P["tilt"], n_leaves)''', '''    tilt = rng.uniform(*P["tilt"], n_leaves) * np.where(n[:, 2] < -0.15, 0.3, 1.0)''')
rep('''def scatter_leaves(name, base, n_leaves, P, colour_fn, seed):''',
    '''def scatter_leaves(name, base, n_leaves, P, colour_fn, seed, skip_bottom=None):''')
rep('''    idx = rng.choice(len(T), n_leaves, p=area / area.sum())''', '''    wgt = area.copy()
    if skip_bottom is not None:      # the flat bottom on the soil is never seen: no leaves there
        fc = (A + B + C) / 3
        fn = np.cross(B - A, C - A)
        wgt[(fc[:, 2] < skip_bottom) & (fn[:, 2] < 0)] = 0.0
    idx = rng.choice(len(T), n_leaves, p=wgt / wgt.sum())''')
rep('''    cb, ct, rough = colour_fn(pos, n, rng)''', '''    lt = LOBE_TOP.get(base.name)
    lobe = np.zeros(n_leaves) if lt is None else (lt[T[idx, 0]] * wa + lt[T[idx, 1]] * wb + lt[T[idx, 2]] * wc)
    cb, ct, rough = colour_fn(pos, n, rng, lobe)''')
# colours: rougher leaves, no near-black
rep('''    stops = [(0.0, (128, 20, 16)), (0.22, (184, 34, 20)), (0.45, (218, 72, 22)), (0.68, (236, 118, 26)),''',
    '''    stops = [(0.0, (150, 32, 22)), (0.22, (188, 40, 22)), (0.45, (218, 72, 22)), (0.68, (236, 118, 26)),''')
rep('''    def fn(pos, n, rng):
        m = len(pos)
        dist = np.linalg.norm(pos[:, None, :] - cc[None, :, :], axis=2) / cr[None, :]''',
    '''    def fn(pos, n, rng, lobe):
        m = len(pos)
        dist = np.linalg.norm(pos[:, None, :] - cc[None, :, :], axis=2) / cr[None, :]''')
rep('''        up = np.clip(n[:, 2], -1, 1)
        k = (0.78 + 0.22 * (up * 0.5 + 0.5))[:, None]
        cb *= k
        ct *= k
        rough = rng.uniform(0.5, 0.68, m)''', '''        up = np.clip(n[:, 2], -1, 1)
        k = ((0.88 + 0.12 * (up * 0.5 + 0.5)) * (0.93 + 0.1 * lobe))[:, None]
        cb *= k
        ct *= k
        rough = rng.uniform(0.82, 0.9, m)''')
rep('''    def fn(pos, n, rng):
        m = len(pos)
        rel = pos - np.asarray(centre)[None, :]''', '''    def fn(pos, n, rng, lobe):
        m = len(pos)
        rel = pos - np.asarray(centre)[None, :]''')
rep('''        fac = 0.25 * outer + 0.85 * height + 0.45 * patch + rng.normal(0, 0.04, m)
        a = sstep(0.45, 0.85, fac)''', '''        fac = 0.25 * outer + 0.75 * height + 0.4 * patch + 0.35 * lobe + rng.normal(0, 0.04, m)
        a = sstep(0.5, 0.9, fac)            # turning at the top AND at the tip of every leaf cluster''')
rep('''        greens *= (0.82 + 0.3 * np.clip(n[:, 2] * 0.5 + 0.5, 0, 1))[:, None]''',
    '''        greens *= (0.9 + 0.22 * np.clip(n[:, 2] * 0.5 + 0.5, 0, 1))[:, None]''')
rep('''        rough = rng.uniform(0.5, 0.66, m)
        return cb, ct, rough
    return fn


''', '''        rough = rng.uniform(0.84, 0.9, m)
        return cb, ct, rough
    return fn


''')
# bush: less symmetric + one off-centre bulge
rep('''    for k in range(3):
        a = math.radians(40 + 120 * k + rng.uniform(-15, 15))
        clumps.append((Vector((0.85 * math.cos(a), 0.85 * math.sin(a), 3.0 + rng.uniform(-0.1, 0.15))),
                       1.3 + rng.uniform(-0.1, 0.1), rng.random()))''', '''    for k in range(3):
        a = math.radians(40 + 120 * k + rng.uniform(-15, 15))
        clumps.append((Vector((0.85 * math.cos(a), 0.85 * math.sin(a), 3.0 + rng.uniform(-0.25, 0.25))),
                       1.3 + rng.uniform(-0.18, 0.12), rng.random()))
    # asymmetry: a low bulge on one side, a raised shoulder on the other
    a = math.radians(305)
    clumps.append((Vector((1.55 * math.cos(a), 1.55 * math.sin(a), 1.75)), 1.2, rng.random()))
    a = math.radians(150)
    clumps.append((Vector((1.05 * math.cos(a), 1.05 * math.sin(a), 3.15)), 1.15, rng.random()))''')

# =========================================================== canopy_parts: lobes + optional hidden-bottom removal
rep('''def canopy_parts(name, blobs, voxel, smooth_iter, namp, nfreq, seed, lo_tris, lo_push, zfloor=None):
    base = blob_mesh(name + "Base", blobs, voxel, smooth_iter, namp, nfreq, seed, zfloor)
    src = link(bpy.data.objects.new("LoSrc", base.data.copy()))
    V, T, N = obj_arrays(src)
    V = V + N * lo_push
    if zfloor is not None:
        V[:, 2] = np.maximum(V[:, 2], zfloor)
    set_co(src, V)
    lo = decimate_to(src, name, lo_tris)
    bpy.data.objects.remove(src)
    return base, lo''', '''def canopy_parts(name, blobs, voxel, smooth_iter, namp, nfreq, seed, lo_tris, lo_push, zfloor=None, lobes=None,
                 drop_bottom=None):
    base = blob_mesh(name + "Base", blobs, voxel, smooth_iter, namp, nfreq, seed, zfloor, lobes)
    src = link(bpy.data.objects.new("LoSrc", base.data.copy()))
    V, T, N = obj_arrays(src)
    V = V + N * lo_push
    if zfloor is not None:
        V[:, 2] = np.maximum(V[:, 2], zfloor)
    set_co(src, V)
    if drop_bottom is not None:      # the flat bottom resting on the soil is never seen: spend nothing there
        C = face_centers(src)
        me = src.data
        FN = np.empty(len(me.polygons) * 3, np.float32)
        me.polygons.foreach_get("normal", FN)
        FN = FN.reshape(-1, 3)
        delete_faces(src, (C[:, 2] < drop_bottom) & (FN[:, 2] < -0.6))
    lo = decimate_to(src, name, lo_tris)
    bpy.data.objects.remove(src)
    return base, lo


def drop_slivers(ob, min_faces=24):
    """Delete tiny disconnected pieces (a decimation leftover sliver)."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.faces.ensure_lookup_table()
    seen = set()
    kill = []
    for f in bm.faces:
        if f.index in seen:
            continue
        stack, comp = [f], []
        seen.add(f.index)
        while stack:
            g = stack.pop()
            comp.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        seen.add(h.index)
                        stack.append(h)
        if len(comp) < min_faces:
            kill += comp
    if kill:
        bmesh.ops.delete(bm, geom=kill, context="FACES")
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bm.to_mesh(ob.data)
    bm.free()
    return len(kill)''')

open("tptree.py", "w", encoding="utf-8").write(src)
print("part A ok")
