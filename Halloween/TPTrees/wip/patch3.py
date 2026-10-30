src = open("tptree.py", encoding="utf-8").read()


def rep(a, b, cnt=1):
    global src
    assert src.count(a) == cnt, (a[:70], src.count(a))
    src = src.replace(a, b)


# ---- 1. tail slots
rep('''        dict(name="OverC", nodes=[D(200, 2), D(212, 52), D(330, 58), D(342, 4)],''',
    '''        dict(name="OverC", nodes=[D(205, 2), D(215, 52), D(320, 58), D(318, 4)],''')
rep('''        dict(name="FestFront", nodes=[D(248, -14), D(300, -12)], spans=["sag:1.16"], pins=[True, True],
             tail0=1.4, tail1=2.2, twist=0.12),
        dict(name="FestRight", nodes=[D(18, -16), D(70, -12)], spans=["sag:1.14"], pins=[True, True],
             tail0=0.9, tail1=2.8, twist=0.12),
        dict(name="FestBack", nodes=[D(140, -10), D(196, -15)], spans=["sag:1.18"], pins=[True, True],
             tail0=2.4, tail1=1.1, twist=0.12),''',
    '''        dict(name="FestFront", nodes=[D(262, -13), D(296, -12)], spans=["sag:1.2"], pins=[True, True],
             tail0=0.5, tail1=1.6, twist=0.12),
        dict(name="FestRight", nodes=[D(22, -16), D(56, -12)], spans=["sag:1.18"], pins=[True, True],
             tail0=0.9, tail1=2.4, twist=0.12),
        dict(name="FestBack", nodes=[D(136, -10), D(190, -15)], spans=["sag:1.18"], pins=[True, True],
             tail0=2.2, tail1=0.8, twist=0.12),''')
rep('''        dict(name="TwigA", nodes=[("twig", 0, 0.9)], spans=[], pins=[True], tail0=2.2, tail1=3.1, twist=0.2),
        dict(name="TwigB", nodes=[("twig", 1, 0.9)], spans=[], pins=[True], tail0=3.0, tail1=2.0, twist=0.18),
        dict(name="TwigC", nodes=[("twig", 2, 0.9)], spans=[], pins=[True], tail0=1.8, tail1=3.4, twist=0.2),''',
    '''        dict(name="TwigA", nodes=[("twig", 0, 0.9)], spans=[], pins=[True], tail0=0.55, tail1=3.1, twist=0.2),
        dict(name="TwigB", nodes=[("twig", 1, 0.9)], spans=[], pins=[True], tail0=3.0, tail1=0.6, twist=0.18),
        dict(name="TwigC", nodes=[("twig", 2, 0.9)], spans=[], pins=[True], tail0=0.5, tail1=3.4, twist=0.2),''')

# ---- 2. lift pass + per-ribbon objects
rep('''        P, Tt, Nn, si = dense_curve(X, N)
        keep = pick_low(P, Tt, Nn, si)
        ph = (rng.uniform(0, 6.28), rng.uniform(0, 6.28))
        V, F, _ = ribbon_low(P, Tt, Nn, si, keep, ph, None)
        col.add(bvh_np(V, F), 0.08, "ribbon")''',
    '''        P, Tt, Nn, si = dense_curve(X, N)
        lifted = 0.0
        if prev:
            P, lifted = lift_off(P, Tt, Nn, prev)
        keep = pick_low(P, Tt, Nn, si)
        ph = (rng.uniform(0, 6.28), rng.uniform(0, 6.28))
        V, F, _ = ribbon_low(P, Tt, Nn, si, keep, ph, None)
        b = bvh_np(V, F)
        col.add(b, 0.08, "ribbon")
        prev.append(b)''')
rep('''    col = ctx["col"]
    rng = random.Random(seed)
    done = []
    for k, spec in enumerate(specs):''', '''    col = ctx["col"]
    rng = random.Random(seed)
    done = []
    prev = []
    for k, spec in enumerate(specs):''')
rep('''        log("  ribbon %-10s len %5.2f  low sections %4d  contact %.2f  zmin %.2f" %
            (spec["name"], si[-1], len(keep), contact.mean(), P[:, 2].min()))''',
    '''        log("  ribbon %-10s len %5.2f  low sections %4d  contact %.2f  zmin %.2f  lift %.3f" %
            (spec["name"], si[-1], len(keep), contact.mean(), P[:, 2].min(), lifted))''')
rep('''    atlas = Atlas(size, k)
    Vs, Fs, UVs, off_v = [], [], [], 0
    for d in done:
        V, F, UV = ribbon_low(d["P"], d["T"], d["N"], d["si"], d["keep"], d["ph"], atlas)
        Vs.append(V)
        Fs.append(F + off_v)
        UVs.append(UV)
        off_v += len(V)
    rects, ybot = roll_rects(atlas, len(rolls))
    for (c, axis), rc in zip(rolls, rects):
        V, F, UV = roll_low(c, axis, rc)
        Vs.append(V)
        Fs.append(F + off_v)
        UVs.append(UV)
        off_v += len(V)
    lo = mesh_np("TP", np.vstack(Vs), np.vstack(Fs))
    uvl = lo.data.uv_layers.new(name="UVMap")
    uvl.data.foreach_set("uv", np.vstack(UVs).astype(np.float32).ravel())
    # HI
    Vs, Fs, Cs, Rs, off_v = [], [], [], [], 0
    for d in done:
        V, F, Cc, Rr = ribbon_hi(d["P"], d["T"], d["N"], d["si"], d["ph"], d["off"], d["perf"])
        Vs.append(V)
        Fs.append(F + off_v)
        Cs.append(Cc)
        Rs.append(Rr)
        off_v += len(V)
    for j, (c, axis) in enumerate(rolls):
        V, F, Cc = roll_hi(c, axis, seed + 100 + j)
        Vs.append(V)
        Fs.append(F + off_v)
        Cs.append(Cc)
        Rs.append(np.full(len(V), 0.84))
        off_v += len(V)
    hi = mesh_np("TPHi", np.vstack(Vs), np.vstack(Fs))
    set_colors(hi.data, "Col", np.vstack(Cs))
    rr = np.concatenate(Rs)
    set_colors(hi.data, "Rough", np.stack([rr, rr, rr], 1))
    hi.data.materials.append(mat_vc("TPHiMat"))
    rep = dict(ribbons=len(done), length=round(total, 1), px_per_stud=k, tris=tri_count(lo),
               hi_tris=tri_count(hi), atlas_rows=atlas.used_rows(), atlas_bottom_px=int(ybot))
    return lo, hi, done, rep''',
    '''    atlas = Atlas(size, k)
    hmat = mat_vc("TPHiMat")
    los, his = [], []

    def lo_obj(name, V, F, UV):
        o = mesh_np(name, V, F)
        uvl = o.data.uv_layers.new(name="UVMap")
        uvl.data.foreach_set("uv", UV.astype(np.float32).ravel())
        return o

    def hi_obj(name, V, F, Cc, Rr):
        o = mesh_np(name, V, F)
        set_colors(o.data, "Col", Cc)
        set_colors(o.data, "Rough", np.stack([Rr, Rr, Rr], 1))
        o.data.materials.append(hmat)
        return o
    for j, d in enumerate(done):
        V, F, UV = ribbon_low(d["P"], d["T"], d["N"], d["si"], d["keep"], d["ph"], atlas)
        los.append(lo_obj("TPlo_%02d" % j, V, F, UV))
        V, F, Cc, Rr = ribbon_hi(d["P"], d["T"], d["N"], d["si"], d["ph"], d["off"], d["perf"])
        his.append(hi_obj("TPHi_%02d" % j, V, F, Cc, Rr))
    rects, ybot = roll_rects(atlas, len(rolls))
    for j, ((c, axis), rc) in enumerate(zip(rolls, rects)):
        V, F, UV = roll_low(c, axis, rc)
        los.append(lo_obj("TPlo_r%d" % j, V, F, UV))
        V, F, Cc = roll_hi(c, axis, seed + 100 + j)
        his.append(hi_obj("TPHi_r%d" % j, V, F, Cc, np.full(len(V), 0.84)))
    rep = dict(ribbons=len(done), length=round(total, 1), px_per_stud=k, tris=sum(tri_count(o) for o in los),
               hi_tris=sum(tri_count(o) for o in his), atlas_rows=atlas.used_rows(), atlas_bottom_px=int(ybot))
    return los, his, done, rep''')
rep('''def wedge_roll(la, lb, ro):''', '''def lift_off(P, T, Nn, prev, gap=0.035, iters=4):
    """Push a new strip off the strips already placed: probe its centre and both edges against their LO meshes and
    move it along their surface normal where it is closer than half-thickness + gap; the push is a smooth bump
    along the strip (running max, then a gaussian)."""
    W = nrm(np.cross(T, Nn))
    P = P.copy()
    m = len(P)
    total = 0.0
    ker = np.exp(-0.5 * (np.arange(-21, 22) / 7.0) ** 2)
    ker /= ker.sum()
    for _ in range(iters):
        push = np.zeros((m, 3))
        mag = np.zeros(m)
        for i in range(0, m, 2):
            for off in (-HW * 0.97, -HW * 0.5, 0.0, HW * 0.5, HW * 0.97):
                q = Vector((P[i] + W[i] * off).tolist())
                for b in prev:
                    loc, nr, idx, dist = b.find_nearest(q, 0.3)
                    if loc is None:
                        continue
                    need = TP_T / 2 + gap - (q - loc).dot(nr)
                    if need > mag[i]:
                        mag[i] = need
                        push[i] = (nr.x, nr.y, nr.z)
        if mag.max() <= 1e-4:
            break
        pad = np.pad(mag, 12)
        mx = np.lib.stride_tricks.sliding_window_view(pad, 25).max(1)
        mx = np.convolve(mx, ker, mode="same")
        dv = np.stack([np.convolve(push[:, c] * mag, ker, mode="same") for c in range(3)], 1)
        dv = nrm(dv + 1e-12)
        P = P + dv * mx[:, None] * 1.05
        total += float(mag.max())
    return P, total


def wedge_roll(la, lb, ro):''')

# ---- 3. build_tree / build_bush: TP parts are lists now
rep('''    tp, tp_hi, done, trep = build_tp(specs, [(cA, axA), (cB, axB)], ctx, 1024, 4242)''',
    '''    tp_los, tp_his, done, trep = build_tp(specs, [(cA, axA), (cB, axB)], ctx, 1024, 4242)''')
rep('''    rep["tris"] = {o.name: tri_count(o) for o in (trunk, canA, canB, tp)}
    rep["hi_tris"] = {o.name: tri_count(o) for o in (trunk_hi, base, leaves, tp_hi)}
    rep["bbox"] = bbox_of([trunk, canA, canB, tp])
    save_json(rep, os.path.join(WIP, "tree_build.json"))
    for o in (trunk_hi, base, leaves, tp_hi):
        o.hide_render = True''', '''    rep["tris"] = {o.name: tri_count(o) for o in (trunk, canA, canB)}
    rep["tris"]["TP"] = trep["tris"]
    rep["hi_tris"] = {o.name: tri_count(o) for o in (trunk_hi, base, leaves)}
    rep["hi_tris"]["TPHi"] = trep["hi_tris"]
    rep["bbox"] = bbox_of([trunk, canA, canB] + tp_los)
    save_json(rep, os.path.join(WIP, "tree_build.json"))
    for o in [trunk_hi, base, leaves] + tp_his:
        o.hide_render = True''')
rep('''    tp, tp_hi, done, trep = build_tp(bush_specs(roll_top), [(c, axis)], ctx, 512, 5151)
    rep["tp"] = trep
    log("TP", trep)
    smart_uv(canopy)
    rep["tris"] = {o.name: tri_count(o) for o in (canopy, tp)}
    rep["hi_tris"] = {o.name: tri_count(o) for o in (base, leaves, tp_hi)}
    rep["bbox"] = bbox_of([canopy, tp])
    save_json(rep, os.path.join(WIP, "bush_build.json"))
    for o in (base, leaves, tp_hi):
        o.hide_render = True''', '''    tp_los, tp_his, done, trep = build_tp(bush_specs(roll_top), [(c, axis)], ctx, 512, 5151)
    rep["tp"] = trep
    log("TP", trep)
    smart_uv(canopy)
    rep["tris"] = {"Canopy": tri_count(canopy), "TP": trep["tris"]}
    rep["hi_tris"] = {o.name: tri_count(o) for o in (base, leaves)}
    rep["hi_tris"]["TPHi"] = trep["hi_tris"]
    rep["bbox"] = bbox_of([canopy] + tp_los)
    save_json(rep, os.path.join(WIP, "bush_build.json"))
    for o in [base, leaves] + tp_his:
        o.hide_render = True''')

# ---- 4. group bake for the TP (each strip matched only against its own hi), then join into one TP object
rep('''TREE_BAKES = [  # lo, his, occluder los, size, prefix, cage, maxray, ao strength, ao distance''',
    '''def bake_groups_ss(groups, occluders, size, prefix, ao_strength, ao_dist, ss=2):
    """(Adapted from the PumpkinEggs builder's bake_groups.) groups: [(lo, [his], cage, maxray)], the lo parts share
    one UV atlas. Each lo only matches rays against ITS OWN hi parts (a strip can never pick up a neighbouring strip
    that crosses it). Coverage of each lo + its hit mask (EMIT) are baked with margin 0; covered texels that missed
    are grown from that group's hits; the empty space is dilated at the end. AO sees every hi part plus the
    `occluders` (LO meshes); the lo parts are invisible to rays. Baked at ss x size, box-filtered down."""
    sc = bpy.context.scene
    sc.world.light_settings.distance = ao_dist
    big = size * ss
    shp = (big, big, 4)
    acc = {k: np.zeros(shp, np.float32) for k in ("albedo", "normal", "rough", "ao")}
    owned = np.zeros((big, big), bool)
    zero = np.zeros(big * big * 4, np.float32)
    t_lin = bpy.data.images.new(prefix + "_tmpL", big, big, alpha=False)
    t_lin.colorspace_settings.name = "Non-Color"
    t_rgb = bpy.data.images.new(prefix + "_tmpC", big, big, alpha=False)
    bmat = bpy.data.materials.new(prefix + "_bake")
    bmat.use_nodes = True
    tex = bmat.node_tree.nodes.new("ShaderNodeTexImage")
    bmat.node_tree.nodes.active = tex
    cmat = bpy.data.materials.new(prefix + "_cov")
    cmat.use_nodes = True
    nt = cmat.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1, 1, 1, 1)
    nt.links.new(em.outputs["Emission"], nt.nodes["Material Output"].inputs["Surface"])
    ctex = nt.nodes.new("ShaderNodeTexImage")
    ctex.image = t_lin
    nt.nodes.active = ctex
    los = [g[0] for g in groups]
    his_all = [h for g in groups for h in g[1]]
    keep = {}
    for o in sc.objects:
        if o.type != "MESH":
            continue
        keep[o.name] = (o.hide_render, o.visible_diffuse, o.visible_shadow, o.visible_glossy, o.visible_transmission)
        if o in los:
            o.hide_render, vis = False, False
        elif o in his_all or o in occluders:
            o.hide_render, vis = False, True
        else:
            o.hide_render, vis = True, True
        o.visible_diffuse = o.visible_shadow = o.visible_glossy = o.visible_transmission = vis

    def bake(node, img, kind, s2a, cage=0.0, maxray=0.0, **kw):
        node.image = img
        img.pixels.foreach_set(zero)
        bpy.ops.object.bake(type=kind, use_selected_to_active=s2a, cage_extrusion=cage, max_ray_distance=maxray,
                            margin=0, use_clear=False, **kw)
        a = np.empty(big * big * 4, np.float32)
        img.pixels.foreach_get(a)
        return a.reshape(shp)

    def emit_white(hs, saved):
        for h in hs:
            for m in h.data.materials:
                for n in m.node_tree.nodes:
                    if n.type == "BSDF_PRINCIPLED":
                        ls = [l for l in m.node_tree.links if l.to_socket == n.inputs["Emission Color"]]
                        saved.append((m, n, tuple(n.inputs["Emission Color"].default_value),
                                      n.inputs["Emission Strength"].default_value,
                                      [(l.from_socket, l.to_socket) for l in ls]))
                        for l in ls:
                            m.node_tree.links.remove(l)
                        n.inputs["Emission Color"].default_value = (1, 1, 1, 1)
                        n.inputs["Emission Strength"].default_value = 1.0

    def restore(saved):
        for m, n, colr, st, ls in saved:
            n.inputs["Emission Color"].default_value = colr
            n.inputs["Emission Strength"].default_value = st
            for a, b in ls:
                m.node_tree.links.new(a, b)
    t0 = time.time()
    miss_tot, cov_tot = 0, 0
    for lo, hs, cage, maxray in groups:
        for o in sc.objects:
            o.select_set(False)
        lo.select_set(True)
        bpy.context.view_layer.objects.active = lo
        lo.data.materials.clear()
        lo.data.materials.append(cmat)
        cov = bake(ctex, t_lin, "EMIT", False)[..., 0] > 0.5
        lo.data.materials.clear()
        lo.data.materials.append(bmat)
        for h in hs:
            h.select_set(True)
        out = {"normal": bake(tex, t_lin, "NORMAL", True, cage, maxray, normal_space="TANGENT"),
               "ao": bake(tex, t_lin, "AO", True, cage, maxray),
               "albedo": bake(tex, t_rgb, "DIFFUSE", True, cage, maxray, pass_filter={"COLOR"}),
               "rough": bake(tex, t_lin, "ROUGHNESS", True, cage, maxray)}
        saved = []
        emit_white(hs, saved)
        hit = bake(tex, t_lin, "EMIT", True, cage, maxray)[..., 0] > 0.5
        restore(saved)
        hit &= cov
        for k2, arr in out.items():
            if k2 == "normal":
                arr = arr.copy()
                arr[~hit] = (0.5, 0.5, 1.0, 1.0)
            filled = fill_misses(arr, hit, iters=6) if k2 != "normal" else arr
            acc[k2][cov] = filled[cov]
        owned |= cov
        miss_tot += int((cov & ~hit).sum())
        cov_tot += int(cov.sum())
    for o in sc.objects:
        if o.name in keep:
            (o.hide_render, o.visible_diffuse, o.visible_shadow, o.visible_glossy, o.visible_transmission) = keep[o.name]
    for k2 in acc:
        if k2 == "normal":
            acc[k2][~owned] = (0.5, 0.5, 1.0, 1.0)
            acc[k2] = fill_misses(acc[k2], owned, iters=16)
        else:
            acc[k2] = fill_misses(acc[k2], owned, iters=16)
    acc["albedo"][..., :3] *= (1 - ao_strength) + ao_strength * acc["ao"][..., :1]
    imgs = {}
    for k2, cs in (("albedo", "sRGB"), ("normal", "Non-Color"), ("rough", "Non-Color"), ("ao", "Non-Color")):
        acc[k2][..., 3] = 1.0
        img = bpy.data.images.new(prefix + "_" + k2 + "_ss", big, big, alpha=False)
        img.colorspace_settings.name = cs
        img.pixels.foreach_set(acc[k2].ravel())
        imgs[k2] = downsample(img, prefix + "_" + k2, size, k2, MAPS)
        bpy.data.images.remove(img)
    for i in (t_lin, t_rgb):
        bpy.data.images.remove(i)
    imgs["miss_fraction"] = miss_tot / max(1, cov_tot)
    log("  baked %s %dpx (x%d, %d groups) in %.0fs, covered-texel miss %.4f" %
        (prefix, size, ss, len(groups), time.time() - t0, imgs["miss_fraction"]))
    return imgs


def join_parts(names, into):
    objs = [bpy.data.objects[n] for n in names]
    for o in bpy.context.scene.objects:
        o.select_set(o in objs)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.name = into
    ob.data.name = into
    return ob


TREE_BAKES = [  # lo, his, occluder los, size, prefix, cage, maxray, ao strength, ao distance''')
rep('''    ("TP", ["TPHi"], ["CanopyA", "CanopyB", "Trunk"], 1024, "TPTree_TP", 0.045, 0.075, 0.5, 0.45),
]''', '''    ("TP", None, ["CanopyA", "CanopyB", "Trunk"], 1024, "TPTree_TP", 0.045, 0.075, 0.5, 0.45),
]''')
rep('''    ("TP", ["TPHi"], ["Canopy"], 512, "TPBush_TP", 0.045, 0.075, 0.5, 0.45),''',
    '''    ("TP", None, ["Canopy"], 512, "TPBush_TP", 0.045, 0.075, 0.5, 0.45),''')
rep('''    for lo, his, occ, size, prefix, cage, maxray, aos, aod in plan:
        imgs = bake_part(ob[lo], [ob[h] for h in his], [ob[o] for o in occ], size, prefix, cage, maxray, aos, aod)
        pbr_material(ob[lo], lo + "_PBR", imgs)
        rep[lo] = dict(size=size, miss=round(imgs["miss_fraction"], 4))
    for o in ob:
        if o.name.endswith("Hi"):
            o.hide_render = True
            o.hide_viewport = True''', '''    for lo, his, occ, size, prefix, cage, maxray, aos, aod in plan:
        if lo == "TP":
            los = sorted(o.name for o in ob if o.name.startswith("TPlo_"))
            groups = [(ob[n], [ob[n.replace("TPlo_", "TPHi_")]], cage, maxray) for n in los]
            imgs = bake_groups_ss(groups, [ob[o] for o in occ], size, prefix, aos, aod)
            tp = join_parts(los, "TP")
            pbr_material(tp, "TP_PBR", imgs)
        else:
            imgs = bake_part(ob[lo], [ob[h] for h in his], [ob[o] for o in occ], size, prefix, cage, maxray, aos,
                             aod)
            pbr_material(ob[lo], lo + "_PBR", imgs)
        rep[lo] = dict(size=size, miss=round(imgs["miss_fraction"], 4))
    for o in ob:
        if o.name.endswith("Hi") or o.name.startswith("TPHi_"):
            o.hide_render = True
            o.hide_viewport = True''')
# preview: TP hi parts are TPHi_xx
rep('''            ishi = o.name.endswith("Hi")''', '''            ishi = o.name.endswith("Hi") or o.name.startswith("TPHi_")''')
open("tptree.py", "w", encoding="utf-8").write(src)
print("ok")
