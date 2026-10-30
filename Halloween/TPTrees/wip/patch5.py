src = open("tptree.py", encoding="utf-8").read()


def rep(a, b, cnt=1):
    global src
    assert src.count(a) == cnt, (a[:70], src.count(a))
    src = src.replace(a, b)


# 1. HI strip lies exactly on the LO triangles (top split TL_k-TR_k+1, bottom split BR_k-BL_k+1), not bilinear
rep('''    k = np.clip(np.searchsorted(s_low, s_new, side="right") - 1, 0, len(s_low) - 2)
    t = ((s_new - s_low[k]) / np.maximum(1e-9, s_low[k + 1] - s_low[k]))[:, None]
    lerp = lambda A: A[k] * (1 - t) + A[k + 1] * t
    TLs, TRs, BRs, BLs = lerp(TL), lerp(TR), lerp(BR), lerp(BL)
    Ns = nrm(lerp(Nk))
    xs = np.linspace(-HW, HW, 9)
    u = ((xs + HW) / (2 * HW))[None, :, None]''', '''    k = np.clip(np.searchsorted(s_low, s_new, side="right") - 1, 0, len(s_low) - 2)
    t = ((s_new - s_low[k]) / np.maximum(1e-9, s_low[k + 1] - s_low[k]))[:, None]
    lerp = lambda A: A[k] * (1 - t) + A[k + 1] * t
    Ns = nrm(lerp(Nk))
    xs = np.linspace(-HW, HW, 9)
    u = ((xs + HW) / (2 * HW))[None, :, None]
    tt = t[:, :, None]
    a_, b_ = (lambda A: A[k][:, None, :]), (lambda A: A[k + 1][:, None, :])
    # top: triangles (TL_k, TR_k, TR_k+1) where u >= t, (TL_k, TR_k+1, TL_k+1) where u < t
    topA = a_(TL) + u * (a_(TR) - a_(TL)) + tt * (b_(TR) - a_(TR))
    topB = a_(TL) + tt * (b_(TL) - a_(TL)) + u * (b_(TR) - b_(TL))
    on_top = np.where(u >= tt, topA, topB)
    # bottom: triangles (BR_k, BL_k, BL_k+1) where u <= 1-t, (BR_k, BL_k+1, BR_k+1) where u > 1-t
    botA = a_(BR) + (1 - u) * (a_(BL) - a_(BR)) + tt * (b_(BL) - a_(BL))
    botB = a_(BR) + tt * (b_(BR) - a_(BR)) + (1 - u) * (b_(BL) - b_(BR))
    on_bot = np.where(u <= 1 - tt, botA, botB)''')
rep('''    top = TLs[:, None, :] * (1 - u) + TRs[:, None, :] * u + Ns[:, None, :] * det[:, :, None]
    bot = BLs[:, None, :] * (1 - u) + BRs[:, None, :] * u + Ns[:, None, :] * det[:, :, None]''',
    '''    top = on_top + Ns[:, None, :] * det[:, :, None]
    bot = on_bot + Ns[:, None, :] * det[:, :, None]''')

# 2. smooth the strip normal along the strip (the contact normals come from LO canopy facets and jitter)
rep('''def dense_curve(X, N, step=0.02):''', '''def smooth_normals(T, N, sigma=2.0):
    n = len(N)
    r = int(3 * sigma)
    ker = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    Np = np.pad(N, ((r, r), (0, 0)), mode="edge")
    S = np.stack([np.convolve(Np[:, c], ker, mode="valid") for c in range(3)], 1)
    S = S - T * np.sum(S * T, 1)[:, None]
    bad = np.linalg.norm(S, axis=1) < 1e-6
    S[bad] = N[bad]
    return nrm(S)


def dense_curve(X, N, step=0.02):''')
rep('''        P, Tt, Nn, si = dense_curve(X, N)
        lifted = 0.0''', '''        N = smooth_normals(T, N, 2.0)
        P, Tt, Nn, si = dense_curve(X, N)
        lifted = 0.0''')

# 3. section picker: twist limit applies at any spacing (min 0.03)
rep('''        if dist >= max_len or ((da > max_turn or dn > max_turn * 1.4) and dist > 0.05):''',
    '''        if dist >= max_len or ((da > max_turn or dn > max_turn) and dist > 0.03):''')
open("tptree.py", "w", encoding="utf-8").write(src)
print("ok")
