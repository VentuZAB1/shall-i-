# Review round 1, part B: paper strips that read as soft torn toilet paper
src = open("tptree.py", encoding="utf-8").read()


def rep(a, b, cnt=1):
    global src
    assert src.count(a) == cnt, (a[:80], src.count(a))
    src = src.replace(a, b)


def replace_block(start_marker, end_marker, new_text):
    global src
    s = src.index(start_marker)
    e = src.index(end_marker, s)
    src = src[:s] + new_text + src[e:]


NEW_STRIP = r'''def strip_profile(d, rng):
    """Per dense sample: left / right half widths, each varying +-13 % (smooth), so the strip never has parallel
    edges; tapered to the exact roll width where it comes off a roll."""
    si = d["si"]
    o1 = Vector((rng.uniform(-80, 80), rng.uniform(-80, 80), 0.3))
    o2 = Vector((rng.uniform(-80, 80), rng.uniform(-80, 80), 0.7))
    n1 = np.array([noise.noise(Vector((float(s) * 0.9, 0.0, 0.0)) + o1) for s in si])
    n2 = np.array([noise.noise(Vector((float(s) * 0.9, 0.0, 0.0)) + o2) for s in si])
    k = sstep(0.0, 0.9, si - si[0]) if d.get("roll_start") else np.ones(len(si))
    d["hwl"] = HW * (1 + 0.13 * np.clip(n1 * 2.0, -1, 1) * k)
    d["hwr"] = HW * (1 + 0.13 * np.clip(n2 * 2.0, -1, 1) * k)


def crumple_low(d, col, rng, pin_s, branch_s):
    """Real crumple in the game mesh: cross-folds every 0.6-1.2 stud (0.035-0.07 high, sharp ridge, a little diagonal
    twist; outward only where the strip lies on something), bunching next to branch snags, and 1-2 sharp kinks on
    every free-hanging tail. Also records where the paper touches leaves / bark / soil (grime)."""
    P, N, si = d["P"].copy(), d["N"].copy(), d["si"]
    m = len(P)
    T = nrm(np.gradient(P, axis=0))
    idx = np.arange(0, m, 3)
    if idx[-1] != m - 1:
        idx = np.append(idx, m - 1)
    tch, sg, gr = [], [], []
    for i in idx:
        dcl, nr, kind = col.nearest(Vector(P[i].tolist()))
        t = 1.0 - float(sstep(0.03, 0.16, dcl))
        tch.append(t)
        sg.append(1.0 if nr is None or np.dot(N[i], np.array(tuple(nr))) >= 0 else -1.0)
        gr.append(t if kind in ("canopy", "trunk", "ground") else 0.0)
    touch = np.interp(si, si[idx], tch)
    sgn = np.sign(np.interp(si, si[idx], sg) + 1e-6)
    d["grime"] = np.interp(si, si[idx], gr)
    disp = np.zeros(m)
    twist = np.zeros(m)
    s0 = si[0] + (0.9 if d.get("roll_start") else 0.25)

    def fold(sc, w, A, sign, tw):
        g = np.clip(1 - np.abs((si - sc) / w), 0, 1) ** 1.6
        return sign * A * g, tw * g
    s = s0 + rng.uniform(0.1, 0.6)
    while s < si[-1] - 0.3:
        i = int(np.searchsorted(si, s))
        on = touch[min(i, m - 1)] > 0.5
        A = rng.uniform(0.035, 0.07) * (0.7 if on else 1.0)
        sign = sgn[min(i, m - 1)] if on else rng.choice([-1.0, 1.0])
        a, b = fold(s, rng.uniform(0.09, 0.16), A, sign, rng.uniform(-0.3, 0.3))
        disp += a
        twist += b
        s += rng.uniform(0.6, 1.2) * (1.6 if on else 1.0)
    for sb in branch_s:
        for _ in range(3):
            sc = sb + rng.uniform(-0.45, 0.45)
            if s0 < sc < si[-1] - 0.2:
                i = int(np.searchsorted(si, sc))
                a, b = fold(sc, rng.uniform(0.06, 0.1), rng.uniform(0.03, 0.05), sgn[min(i, m - 1)],
                            rng.uniform(-0.25, 0.25))
                disp += a
                twist += b
    P = P + N * disp[:, None]
    N = rotate_about(N, T, twist[:, None])
    # kinks on the free tails (beyond the last support / before the first support)
    anchor = touch > 0.5
    for sp_ in pin_s:
        anchor[np.abs(si - sp_) < 0.08] = True
    W = nrm(np.cross(T, N))
    sup = np.nonzero(anchor)[0]
    if len(sup):
        for end in (0, 1):
            if end == 1:
                a0, L = si[sup[-1]], si[-1] - si[sup[-1]]
            else:
                a0, L = si[sup[0]], si[sup[0]] - si[0]
            if L < 1.2 or (end == 0 and d.get("roll_start")):
                continue
            for _ in range(1 if L < 2.5 else 2):
                dist = rng.uniform(0.6, L - 0.4)
                sk = a0 + dist if end == 1 else a0 - dist
                i = int(np.clip(np.searchsorted(si, sk), 0, m - 1))
                o = W[i] * rng.uniform(-1, 1) + N[i] * rng.uniform(-1, 1)
                o = o / max(1e-6, np.linalg.norm(o)) * rng.uniform(0.08, 0.14)
                ramp = sstep(sk - 0.06, sk + 0.06, si) if end == 1 else sstep(sk + 0.06, sk - 0.06, si)
                P = P + o[None, :] * ramp[:, None]
    T = nrm(np.gradient(P, axis=0))
    N = nrm(N - T * np.sum(N * T, 1)[:, None])
    d["P"], d["T"], d["N"] = P, T, N


def tear_shape(d, rng):
    """Ragged torn ends (3 teeth over the last 0.18-0.3 stud, a little curl) for every free end."""
    d["tears"] = [None, None]
    for end in (0, 1):
        if not d["tear"][end]:
            continue
        tl = rng.uniform(0.18, 0.3)
        M = 6
        par = rng.randint(0, 1)
        ext = [tl * (rng.uniform(0.55, 1.0) if (j + par) % 2 == 0 else rng.uniform(0.04, 0.32)) for j in range(M)]
        u = [j / (M - 1) + (rng.uniform(-0.05, 0.05) if 0 < j < M - 1 else 0.0) for j in range(M)]
        d["tears"][end] = dict(ext=ext, u=u, curl=rng.uniform(0.15, 0.4) * rng.choice([-1, 1]), len=tl)


def ear_clip(pts):
    """Triangulate a simple CCW polygon (list of 2D points); returns index triples."""
    idx = list(range(len(pts)))
    tris = []
    area2 = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    guard = 0
    while len(idx) > 3 and guard < 200:
        guard += 1
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]
            a, b, c = pts[i0], pts[i1], pts[i2]
            if area2(a, b, c) <= 1e-12:
                continue
            if any(area2(a, b, pts[j]) >= 0 and area2(b, c, pts[j]) >= 0 and area2(c, a, pts[j]) >= 0
                   for j in idx if j not in (i0, i1, i2)):
                continue
            tris.append((i0, i1, i2))
            idx.pop(k)
            break
        else:
            break
    if len(idx) == 3:
        tris.append(tuple(idx))
    return tris


def sections(d, keep):
    s = d["si"][keep]
    C, Tk, Nk = d["P"][keep], d["T"][keep], d["N"][keep]
    W = nrm(np.cross(Tk, Nk))
    wl = edge_wave(s, -1, d["ph"])
    wr = edge_wave(s, 1, d["ph"])
    hl, hr = d["hwl"][keep][:, None], d["hwr"][keep][:, None]
    TL = C - W * hl + Nk * (TP_T / 2 + wl)[:, None]
    TR = C + W * hr + Nk * (TP_T / 2 + wr)[:, None]
    BR = C + W * hr + Nk * (-TP_T / 2 + wr)[:, None]
    BL = C - W * hl + Nk * (-TP_T / 2 + wl)[:, None]
    return s, Tk, Nk, W, TL, TR, BR, BL


def tear_geom(d, keep, end):
    """Torn-end geometry (shared by LO and HI): verts [top 8 | bottom 8], tris, + per-vert (ext, u, is_top)."""
    tr = d["tears"][end]
    s, Tk, Nk, W, TL, TR, BR, BL = sections(d, keep)
    e = 0 if end == 0 else -1
    dirv = -Tk[e] if end == 0 else Tk[e]
    tl_, tr_, bl_, br_ = TL[e], TR[e], BL[e], BR[e]
    tvec = (tl_ - bl_)
    top, info = [tl_], [(0.0, 0.0)]
    for x, u in zip(tr["ext"], tr["u"]):
        p = tl_ + (tr_ - tl_) * u + dirv * x + Nk[e] * (tr["curl"] * x * x / tr["len"])
        top.append(p)
        info.append((x, u))
    top.append(tr_)
    info.append((0.0, 1.0))
    top = np.array(top)
    bot = top - tvec[None, :]
    bot[0], bot[-1] = bl_, br_
    pts2 = [(x, u) for x, u in info]
    tri2 = ear_clip(pts2)
    V = np.vstack([top, bot])
    F = []
    nt = len(top)
    for a, b, c in tri2:
        ft = (a, b, c)
        n3 = np.cross(V[ft[1]] - V[ft[0]], V[ft[2]] - V[ft[0]])
        if np.dot(n3, Nk[e]) < 0:
            ft = (a, c, b)
        F.append(ft)
        F.append((ft[0] + nt, ft[2] + nt, ft[1] + nt))
    wdir = nrm(tr_ - tl_)
    for j in range(nt - 1):           # walls along the torn outline (TL->p0 ... p5->TR)
        a, b = j, j + 1
        dx, du = pts2[b][0] - pts2[a][0], pts2[b][1] - pts2[a][1]
        outw = dirv * du - wdir * dx
        q = (a, b, b + nt, a + nt)
        n3 = np.cross(V[q[1]] - V[q[0]], V[q[2]] - V[q[0]])
        if np.dot(n3, outw) < 0:
            q = (a, a + nt, b + nt, b)
        F += [(q[0], q[1], q[2]), (q[0], q[2], q[3])]
    return V, np.array(F, np.int32), info


def ribbon_low(d, keep, atlas):
    """Box section per kept sample (top / edge / bottom / edge split so the strip faces stay clean), varying width,
    torn ends (or a plain cap where the strip starts on a roll). Returns V, F (tris), UV per loop."""
    s, Tk, Nk, W, TL, TR, BR, BL = sections(d, keep)
    n = len(s)
    sides = [(TL, TR), (TR, BR), (BR, BL), (BL, TL)]
    V = np.concatenate([np.stack([a_, b_], 1) for a_, b_ in sides], 1).reshape(-1, 3)
    t0, t1 = d["tears"]
    s_alloc = list(s)
    if t0:
        s_alloc = [s[0] - t0["len"] - 0.03] + s_alloc
    if t1:
        s_alloc = s_alloc + [s[-1] + t1["len"] + 0.03]
    segs_all = atlas.strip(np.array(s_alloc)) if atlas is not None else [(0.0, 0.0, 0)] * (len(s_alloc) - 1)
    segs = segs_all[(1 if t0 else 0): len(segs_all) - (1 if t1 else 0)]
    F, UV = [], []
    pcoord = [0.0, TP_W, TP_W + TP_T, 2 * TP_W + TP_T, PERIM]
    S = atlas.size if atlas is not None else 1.0
    kk = atlas.k if atlas is not None else 1.0
    rowy = (lambda r: atlas.row_y(r)) if atlas is not None else (lambda r: 0.0)
    for a, (xa, xb, row) in enumerate(segs):
        y0 = rowy(row)
        for q in range(4):
            i00, i01 = a * 8 + 2 * q, a * 8 + 2 * q + 1
            i11, i10 = (a + 1) * 8 + 2 * q + 1, (a + 1) * 8 + 2 * q
            y_a = y0 + (PERIM - pcoord[q]) * kk
            y_b = y0 + (PERIM - pcoord[q + 1]) * kk
            uv00, uv01 = (xa / S, y_a / S), (xa / S, y_b / S)
            uv11, uv10 = (xb / S, y_b / S), (xb / S, y_a / S)
            tri = [(i00, i01, i11), (i00, i11, i10)]
            uvs = [uv00, uv01, uv11, uv00, uv11, uv10]
            p0, p1, p2 = V[tri[0][0]], V[tri[0][1]], V[tri[0][2]]
            F += tri
            UV += uvs
    F = np.array(F, np.int32).reshape(-1, 3)
    UV = np.array(UV, np.float32).reshape(-1, 2)
    p0, p1, p2 = V[F[0, 0]], V[F[0, 1]], V[F[0, 2]]
    if np.dot(np.cross(p1 - p0, p2 - p0), Nk[0]) < 0:
        F = F[:, [0, 2, 1]]
        UV = UV.reshape(-1, 3, 2)[:, [0, 2, 1], :].reshape(-1, 2)
    Fl, UVl = [F], [UV]
    for end in (0, 1):
        tr = d["tears"][end]
        base = len(V)
        if tr is None:                   # plain cap (strip starts on a roll)
            e = 0 if end == 0 else n - 1
            cap = np.stack([TL[e], TR[e], BR[e], BL[e]])
            Fc = np.array([(0, 3, 2), (0, 2, 1)] if end == 0 else [(0, 1, 2), (0, 2, 3)], np.int32)
            n3 = np.cross(cap[Fc[0, 1]] - cap[Fc[0, 0]], cap[Fc[0, 2]] - cap[Fc[0, 0]])
            if np.dot(n3, -Tk[0] if end == 0 else Tk[-1]) < 0:
                Fc = Fc[:, [0, 2, 1]]
            xa, xb, row = segs[0] if end == 0 else segs[-1]
            x = (xa if end == 0 else xb) / S
            y0 = rowy(row)
            cu = np.array([(x, (y0 + 0.2 * kk) / S)] * 6, np.float32)
            V = np.vstack([V, cap])
            Fl.append(Fc + base)
            UVl.append(cu)
            continue
        Vt, Ft, info = tear_geom(d, keep, end)
        V = np.vstack([V, Vt])
        Fl.append(Ft + base)
        xa, xb, row = segs_all[0] if end == 0 else segs_all[-1]
        y0 = rowy(row)
        xan = xb if end == 0 else xa
        sgn = -1.0 if end == 0 else 1.0
        nt = len(info)
        uvv = []
        for j, (x, u) in enumerate(info):
            uvv.append(((xan + sgn * x * kk) / S, (y0 + (PERIM - u * TP_W) * kk) / S))
        for j, (x, u) in enumerate(info):
            uvv.append(((xan + sgn * x * kk) / S, (y0 + (PERIM - (TP_W + TP_T + (1 - u) * TP_W)) * kk) / S))
        uvv = np.array(uvv, np.float32)
        # walls: put their loops on the right-edge band
        uvw = uvv.copy()
        for j in range(nt):
            uvw[j, 1] = (y0 + (PERIM - TP_W) * kk) / S
            uvw[j + nt, 1] = (y0 + (PERIM - TP_W - TP_T) * kk) / S
        ntri_faces = len(ear_clip([(x, u) for x, u in info])) * 2
        loops = []
        for fi, f in enumerate(Ft):
            src_uv = uvv if fi < ntri_faces else uvw
            loops += [src_uv[f[0]], src_uv[f[1]], src_uv[f[2]]]
        UVl.append(np.array(loops, np.float32))
    return V, np.vstack(Fl), np.vstack(UVl)


def ribbon_hi(d, keep):
    """HI bake source = the LO strip (interpolated between its sections) + bounded detail: crumple folds, a soft cup,
    edges that taper/round off over the outer 0.05 stud (no crisp outline), faint irregular perforations; colour
    with +-5 % value patches and warm grime where it touches bark / leaves / soil. Torn ends copied from the LO."""
    s_low, Tk, Nk, W, TL, TR, BR, BL = sections(d, keep)
    si, off = d["si"], d["off"]
    rng = random.Random(int(abs(off[0]) * 1000) % 99991)
    sp, a_, ang, dep, dk = [], s_low[0] + d["perf"], [], [], []
    while a_ < s_low[-1]:
        sp.append(a_)
        ang.append(rng.uniform(-0.15, 0.15))
        dep.append(rng.uniform(0.0022, 0.004))
        dk.append(rng.uniform(0.015, 0.035))
        a_ += rng.uniform(0.42, 0.6)
    s_new = si[(si >= s_low[0]) & (si <= s_low[-1])]
    s_new = np.unique(np.concatenate([s_new, s_low[[0, -1]]]))
    m = len(s_new)
    k = np.clip(np.searchsorted(s_low, s_new, side="right") - 1, 0, len(s_low) - 2)
    t = ((s_new - s_low[k]) / np.maximum(1e-9, s_low[k + 1] - s_low[k]))[:, None]
    lerp = lambda A: A[k] * (1 - t) + A[k + 1] * t
    Ns = nrm(lerp(Nk))
    uu = np.array([0.0, 0.04, 0.12, 0.3, 0.5, 0.7, 0.88, 0.96, 1.0])
    nx = len(uu)
    u = uu[None, :, None]
    width = np.linalg.norm(lerp(TR) - lerp(TL), axis=1)
    xs = (uu[None, :] - 0.5) * width[:, None]
    cr = crumple(np.repeat(s_new, nx), xs.ravel(), off).reshape(m, nx)
    cup = 0.008 * (1 - (2 * uu - 1) ** 2)
    edge = np.minimum(uu, 1 - uu)
    rnd = 0.022 * (1 - np.clip(edge / 0.12, 0, 1)) ** 2
    dperf = np.zeros((m, nx))
    perf = np.zeros((m, nx))
    for e_, an, de, dkk in zip(sp, ang, dep, dk):
        ds_ = np.abs(s_new[:, None] - e_ - xs * an)
        dperf -= de * np.clip(1 - ds_ / 0.02, 0, 1)
        perf += dkk * np.clip(1 - ds_ / 0.012, 0, 1)
    det = cr + cup[None, :] + dperf
    TLs, TRs, BRs, BLs = lerp(TL), lerp(TR), lerp(BR), lerp(BL)
    top = TLs[:, None, :] * (1 - u) + TRs[:, None, :] * u + Ns[:, None, :] * (det - rnd[None, :])[:, :, None]
    bot = BLs[:, None, :] * (1 - u) + BRs[:, None, :] * u + Ns[:, None, :] * (det + rnd[None, :])[:, :, None]
    V = np.concatenate([top, bot[:, ::-1, :]], 1)
    kk = 2 * nx
    i = np.arange(m - 1)[:, None]
    j = np.arange(kk)[None, :]
    jn = (j + 1) % kk
    a0, b0 = i * kk + j, i * kk + jn
    c0, d0 = (i + 1) * kk + jn, (i + 1) * kk + j
    F = np.concatenate([np.stack([a0, b0, c0], -1).reshape(-1, 3), np.stack([a0, c0, d0], -1).reshape(-1, 3)])
    Vf = V.reshape(-1, 3)
    p0, p1, p2 = Vf[F[0, 0]], Vf[F[0, 1]], Vf[F[0, 2]]
    if np.dot(np.cross(p1 - p0, p2 - p0), Ns[0]) < 0:
        F = F[:, [0, 2, 1]]
    T2 = nrm(lerp(Tk))
    e0 = np.array([[0, j2, j2 + 1] for j2 in range(1, kk - 1)])
    e1 = np.array([[(m - 1) * kk, (m - 1) * kk + j2 + 1, (m - 1) * kk + j2] for j2 in range(1, kk - 1)])
    c_ = np.cross(Vf[e0[0, 1]] - Vf[e0[0, 0]], Vf[e0[0, 2]] - Vf[e0[0, 0]])
    if np.dot(c_, T2[0]) > 0:
        e0 = e0[:, [0, 2, 1]]
        e1 = e1[:, [0, 2, 1]]
    F = np.vstack([F, e0, e1])
    # colour
    base = L(TP_RGB)
    o = Vector(off)
    patch = np.array([[noise.noise(Vector((float(sv) * 1.3, float(uv_) * 0.9, 2.0)) + o) for uv_ in uu]
                      for sv in s_new])
    grime = np.interp(s_new, si, d.get("grime", np.zeros(len(si))))
    colt = base[None, None, :] * (1 + 0.05 * np.clip(patch * 1.6, -1, 1))[:, :, None] * (1 - perf)[:, :, None]
    colt = colt * (1 - 0.04 * np.clip(-cr * 60, 0, 1))[:, :, None]
    warm = np.array([0.86, 0.79, 0.68])
    colb = colt * (1 - 0.55 * grime[:, None, None] * (1 - warm[None, None, :]))
    colt = colt * (1 - 0.18 * grime[:, None, None] * (1 - warm[None, None, :]))
    col = np.concatenate([colt, colb[:, ::-1, :]], 1).reshape(-1, 3)
    rough = np.full(m * kk, 0.86)
    Vs, Fs, Cs, Rs = [Vf], [F], [col], [rough]
    off_v = len(Vf)
    for end in (0, 1):
        if d["tears"][end] is None:
            continue
        Vt, Ft, info = tear_geom(d, keep, end)
        g = grime[0] if end == 0 else grime[-1]
        ct = np.tile(base * (1 - 0.18 * g * (1 - warm)), (len(Vt), 1))
        nt = len(info)
        for jj, (x, uv_) in enumerate(info):
            if x > 0:                       # the torn fibre edge a touch greyer
                ct[jj] *= 0.95
                ct[jj + nt] *= 0.95
        Vs.append(Vt)
        Fs.append(Ft + off_v)
        Cs.append(ct)
        Rs.append(np.full(len(Vt), 0.88))
        off_v += len(Vt)
    return np.vstack(Vs), np.vstack(Fs), np.clip(np.vstack(Cs), 0, 1), np.concatenate(Rs)


'''
replace_block("def ribbon_low(", "# ------------------------------------------------------------------ rolls", NEW_STRIP)

# bigger rolls (0.96 across), a 24-gon game mesh
rep('''ROLL = dict(Ro=0.34, Rc=0.15, Ri=0.125, hl=HW)''', '''ROLL = dict(Ro=0.48, Rc=0.2, Ri=0.17, hl=HW)''')
rep('''def roll_low(c, axis, rects, nseg=20):''', '''def roll_low(c, axis, rects, nseg=24):''')

NEW_BUILD = r'''def build_tp(specs, rolls, ctx, size, seed, budget, ds=0.1):
    """Simulate every strip in order (each collides with the canopy / trunk / rolls / ground / strips before it),
    shape it as paper (width, crumple, kinks, torn ends), lift it off earlier strips, then fit the whole TP into
    `budget` triangles (section spacing) and build the LO (one atlas, per-strip parts for the bake) + HI."""
    col = ctx["col"]
    rng = random.Random(seed)
    done = []
    prev = []
    for k, spec in enumerate(specs):
        X0, rest, pins, off, node_idx = init_ribbon(spec, ctx, ds)
        X = simulate(X0, rest, pins, col, steps=spec.get("steps", 300))
        X = laplace(X, pins, 2)
        T, N, contact = ribbon_frames(X, col, spec, ds)
        if spec.get("sway", 1.0) > 0:
            X = sway_tails(X, contact, pins, seed + k, amp=0.08 * spec.get("sway", 1.0),
                           grow=0.045 * spec.get("sway", 1.0))
            for i in range(len(X)):
                q, c = col.push(Vector(X[i].tolist()))
                X[i] = (q.x, q.y, q.z)
            X = laplace(X, pins, 1)
            T, N, contact = ribbon_frames(X, col, spec, ds)
        N = smooth_normals(T, N, 2.0)
        P, Tt, Nn, si = dense_curve(X, N)
        # sim-point index -> arc length on the dense curve
        cum = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(X, axis=0), axis=1))])
        sc_ = si[-1] / max(1e-9, cum[-1])
        pin_s = [cum[i] * sc_ for i in pins]
        branch_s = [cum[node_idx[j] + off] * sc_ for j, nd in enumerate(spec["nodes"])
                    if nd[0] in ("twig", "limb") and spec["pins"][j]]
        d = dict(name=spec["name"], P=P, T=Tt, N=Nn, si=si, ph=(rng.uniform(0, 6.28), rng.uniform(0, 6.28)),
                 off=(rng.uniform(-90, 90), rng.uniform(-90, 90), rng.uniform(-90, 90)), perf=rng.uniform(0.05, 0.45),
                 roll_start=bool(spec.get("roll_start")), tear=spec.get("tear", (True, True)))
        strip_profile(d, rng)
        crumple_low(d, col, rng, pin_s, branch_s)
        lifted = 0.0
        if prev:
            d["P"], lifted = lift_off(d["P"], d["T"], d["N"], prev)
            d["T"] = nrm(np.gradient(d["P"], axis=0))
            d["N"] = nrm(d["N"] - d["T"] * np.sum(d["N"] * d["T"], 1)[:, None])
        tear_shape(d, rng)
        keep = pick_low(d["P"], d["T"], d["N"], si)
        V, F, _ = ribbon_low(d, keep, None)
        b = bvh_np(V, F)
        col.add(b, 0.08, "ribbon")
        prev.append(b)
        done.append(d)
        log("  ribbon %-10s len %5.2f  sections %4d  contact %.2f  zmin %.2f  lift %.3f" %
            (spec["name"], si[-1], len(keep), contact.mean(), d["P"][:, 2].min(), lifted))
    roll_tris = 2 * 24 * 2 + 4 * 24 * 2 + 2 * 24 * 2       # wrap + 4 annuli + inner tube, per roll
    roll_tris = len(rolls) * roll_tris

    def strip_tris(d, keep):
        n = len(keep)
        t = 8 * (n - 1)
        for tr in d["tears"]:
            t += 2 if tr is None else (2 * 7 + 2 * 7)
        return t
    params = [(0.26, 12.0), (0.3, 13.0), (0.34, 14.0), (0.38, 15.0), (0.44, 16.0), (0.5, 18.0), (0.6, 20.0)]
    for ml, mt in params:
        keeps = [pick_low(d["P"], d["T"], d["N"], d["si"], ml, mt) for d in done]
        tris = sum(strip_tris(d, kp) for d, kp in zip(done, keeps)) + roll_tris
        if tris <= budget:
            break
    log("  TP section spacing <= %.2f, turn <= %.0f deg -> ~%d tris (budget %d)" % (ml, mt, tris, budget))
    total = sum(d["si"][-1] for d in done)
    k = 96
    while k > 24:
        at = Atlas(size, k)
        for d, kp in zip(done, keeps):
            ss = list(d["si"][kp])
            if d["tears"][0]:
                ss = [ss[0] - d["tears"][0]["len"] - 0.03] + ss
            if d["tears"][1]:
                ss = ss + [ss[-1] + d["tears"][1]["len"] + 0.03]
            at.strip(np.array(ss))
        _r, ybot = roll_rects(at, len(rolls))
        if ybot <= size - 2:
            break
        k -= 2
    atlas = Atlas(size, k)
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
    for j, (d, kp) in enumerate(zip(done, keeps)):
        V, F, UV = ribbon_low(d, kp, atlas)
        los.append(lo_obj("TPlo_%02d" % j, V, F, UV))
        V, F, Cc, Rr = ribbon_hi(d, kp)
        his.append(hi_obj("TPHi_%02d" % j, V, F, Cc, Rr))
    rects, ybot = roll_rects(atlas, len(rolls))
    for j, ((c, axis), rc) in enumerate(zip(rolls, rects)):
        V, F, UV = roll_low(c, axis, rc)
        los.append(lo_obj("TPlo_r%d" % j, V, F, UV))
        V, F, Cc = roll_hi(c, axis, seed + 100 + j)
        his.append(hi_obj("TPHi_r%d" % j, V, F, Cc, np.full(len(V), 0.84)))
    rep = dict(ribbons=len(done), length=round(float(total), 1), px_per_stud=k,
               tris=sum(tri_count(o) for o in los), hi_tris=sum(tri_count(o) for o in his),
               atlas_rows=atlas.used_rows(), atlas_bottom_px=int(ybot), spacing=ml, turn=mt)
    return los, his, done, rep


'''
replace_block("def build_tp(", "def lift_off(", NEW_BUILD)
open("tptree.py", "w", encoding="utf-8").write(src)
print("part B ok")
