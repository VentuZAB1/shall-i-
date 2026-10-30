src = open("tptree.py", encoding="utf-8").read()


def rep(a, b, cnt=1):
    global src
    assert src.count(a) == cnt, (a[:70], src.count(a))
    src = src.replace(a, b)


s = src.index("def ribbon_hi(")
e = src.index("# ------------------------------------------------------------------ rolls")
src = src[:s] + '''def ribbon_hi(P, T, Nn, si, keep, ph, off, perf_phase):
    """HI bake source = the LO strip itself (its box section interpolated between the LO sections) + bounded detail
    only: a soft cup across the strip, crumple folds (mostly across) and perforation creases every 0.5 stud. The HI
    therefore never drifts more than ~0.025 from the LO surface, so every bake ray (cage 0.045) lands on the right
    face of the right strip. 9 verts across the top, 9 across the bottom."""
    s_low = si[keep]
    C, Tk, Nk = P[keep], T[keep], Nn[keep]
    Wk = nrm(np.cross(Tk, Nk))
    wl = edge_wave(s_low, -1, ph)
    wr = edge_wave(s_low, 1, ph)
    TL = C - Wk * HW + Nk * (TP_T / 2 + wl)[:, None]
    TR = C + Wk * HW + Nk * (TP_T / 2 + wr)[:, None]
    BR = C + Wk * HW + Nk * (-TP_T / 2 + wr)[:, None]
    BL = C - Wk * HW + Nk * (-TP_T / 2 + wl)[:, None]
    sp = np.arange(perf_phase, s_low[-1], 0.5)
    extra = np.concatenate([sp - 0.012, sp, sp + 0.012])
    extra = extra[(extra > s_low[0] + 0.01) & (extra < s_low[-1] - 0.01)]
    base_s = si[(si >= s_low[0]) & (si <= s_low[-1])]
    ok = np.ones(len(base_s), bool)
    for e_ in sp:
        ok &= np.abs(base_s - e_) > 0.008
    s_new = np.unique(np.concatenate([base_s[ok], extra, s_low[[0, -1]]]))
    m = len(s_new)
    k = np.clip(np.searchsorted(s_low, s_new, side="right") - 1, 0, len(s_low) - 2)
    t = ((s_new - s_low[k]) / np.maximum(1e-9, s_low[k + 1] - s_low[k]))[:, None]
    lerp = lambda A: A[k] * (1 - t) + A[k + 1] * t
    TLs, TRs, BRs, BLs = lerp(TL), lerp(TR), lerp(BR), lerp(BL)
    Ns = nrm(lerp(Nk))
    xs = np.linspace(-HW, HW, 9)
    u = ((xs + HW) / (2 * HW))[None, :, None]
    cr = crumple(np.repeat(s_new, 9), np.tile(xs, m), off).reshape(m, 9)
    cup = 0.010 * (1 - (xs / HW) ** 2)
    dperf = np.zeros(m)
    for e_ in sp:
        dperf -= 0.006 * np.clip(1 - np.abs(s_new - e_) / 0.013, 0, 1)
    det = cr + cup[None, :] + dperf[:, None]
    top = TLs[:, None, :] * (1 - u) + TRs[:, None, :] * u + Ns[:, None, :] * det[:, :, None]
    bot = BLs[:, None, :] * (1 - u) + BRs[:, None, :] * u + Ns[:, None, :] * det[:, :, None]
    V = np.concatenate([top, bot[:, ::-1, :]], 1)      # ring of 18: top L->R, bottom R->L
    kk = 18
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
    base = L(TP_RGB)
    drift = np.array([noise.noise(Vector((float(sv) * 0.6, 1.7, 3.3)) + Vector(off)) for sv in s_new])
    perf = np.zeros(m)
    for e_ in sp:
        perf += np.clip(1 - np.abs(s_new - e_) / 0.01, 0, 1)
    col_s = base[None, :] * (1 + 0.035 * drift)[:, None] * (1 - 0.08 * perf)[:, None]
    col = np.repeat(col_s, kk, 0)
    crv = np.concatenate([cr, cr[:, ::-1]], 1).reshape(-1)
    col = col * (1 - 0.05 * np.clip(-crv * 60, 0, 1))[:, None]
    rough = np.full(m * kk, 0.86)
    return Vf, F, np.clip(col, 0, 1), rough


''' + src[e:]
rep('''        V, F, Cc, Rr = ribbon_hi(d["P"], d["T"], d["N"], d["si"], d["ph"], d["off"], d["perf"])''',
    '''        V, F, Cc, Rr = ribbon_hi(d["P"], d["T"], d["N"], d["si"], d["keep"], d["ph"], d["off"], d["perf"])''')
rep('''    ("TP", None, ["CanopyA", "CanopyB", "Trunk"], 1024, "TPTree_TP", 0.045, 0.075, 0.5, 0.45),''',
    '''    ("TP", None, ["CanopyA", "CanopyB", "Trunk"], 1024, "TPTree_TP", 0.045, 0.07, 0.5, 0.45),''')
rep('''    ("TP", None, ["Canopy"], 512, "TPBush_TP", 0.045, 0.075, 0.5, 0.45),''',
    '''    ("TP", None, ["Canopy"], 512, "TPBush_TP", 0.045, 0.07, 0.5, 0.45),''')
open("tptree.py", "w", encoding="utf-8").write(src)
print("ok")
