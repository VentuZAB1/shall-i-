# ================================================================== BUSH_THORN (v2, after review round 1)
# A clumpy bramble mound in 5 lobes (dark gaps), ~4.5 tall; an asymmetric tangle of thorny canes: two front canes that
# hold up an orb web hanging down the front, one holding a second orb web down the left side, a tall back cane, a
# snapped dead cane, a spider cane on the right, four canes arcing out of the sides into the soil, two ground runners
# and two short spikes. Webs: near-vertical two-sided silk sheets with a painted orb (radials + sagging catch spiral +
# hub + torn bits) in an RGBA map, plus real frame threads and irregular anchor threads (to thorns, leaf tips,
# foliage).
TH_BODY = dict(
    lobe_list=[((-1.15, -0.85, 1.95), (1.45, 1.35, 1.6), 5),      # front-left
               ((-0.85, 1.05, 2.55), (1.45, 1.35, 1.95), 5),      # back-left, the tallest
               ((1.3, 0.45, 2.25), (1.4, 1.55, 1.75), 5),         # right
               ((0.85, -1.35, 1.45), (1.25, 1.15, 1.3), 4),       # front-right, low
               ((0.05, 0.1, 3.05), (1.05, 1.05, 1.25), 3)],       # crown
    base=((0.0, 0.0, 0.7), (1.9, 1.8, 0.75)),
    r_small=0.45, per_mid=(2, 3), disp=(0.17, 0.8, 0.05, 2.8), zflat=0.14, dims=(5.45, 5.25, 4.5), smooth=2)
TH_G = [(0.0, lin((30, 72, 44))), (0.5, lin((40, 94, 58))), (1.0, lin((28, 86, 78)))]
TH_P = [(0.0, lin((136, 30, 60))), (0.35, lin((122, 38, 92))), (0.7, lin((100, 46, 122))), (1.0, lin((84, 40, 108)))]
TH_CANE = dict(base=lin((84, 92, 44)), mid=lin((96, 30, 60)), dark=lin((62, 20, 40)), bloom=lin((156, 124, 156)),
               tip=lin((136, 42, 62)))
TH_DEAD = dict(base=lin((92, 80, 66)), mid=lin((112, 98, 84)), dark=lin((58, 48, 40)), bloom=lin((150, 140, 128)),
               tip=lin((128, 112, 96)))
# waypoints (r, azimuth deg, z); azimuth 270 = Blender -Y = the front
TH_CANES = [
    dict(name="F1", kind="arch", r=(0.105, 0.04),        # front-left: holds the front web's top-left corner
         wps=[(0.4, 225, -0.05), (0.6, 228, 2.0), (0.8, 238, 4.3), (1.35, 248, 5.05), (2.2, 244, 4.85),
              (2.85, 239.4, 4.5), (3.0, 238, 4.15)]),
    dict(name="F2", kind="arch", r=(0.1, 0.038),         # front-right: holds the front web's top-right corner
         wps=[(0.5, 330, -0.05), (0.7, 325, 2.2), (0.9, 312, 4.6), (1.6, 302, 5.3), (2.84, 298.4, 4.7),
              (3.05, 296, 4.2)]),
    dict(name="S", kind="arch", r=(0.098, 0.038),        # the spider cane (right-front)
         wps=[(0.5, 10, -0.05), (0.8, 0, 2.5), (1.1, 345, 4.6), (1.9, 335, 5.0), (2.7, 330, 4.6), (3.1, 326, 3.85)]),
    dict(name="A0", kind="arch", r=(0.11, 0.042),        # back-left, the tallest
         wps=[(0.4, 140, -0.05), (0.6, 138, 2.5), (0.8, 132, 5.0), (1.3, 128, 5.7), (2.0, 135, 5.3),
              (2.6, 145, 4.2)]),
    dict(name="A1", kind="broken", r=(0.1, 0.06), dead=True,   # back-right: snapped, the top hangs down, dead
         wps=[(0.4, 40, -0.05), (0.6, 45, 2.5), (0.9, 50, 4.7), (1.2, 55, 5.15)],
         hang=[(1.2, 55, 5.15), (1.45, 62, 4.9), (1.62, 66, 4.35), (1.74, 70, 3.8)]),
    dict(name="L1", kind="arch", r=(0.095, 0.036),       # left: holds the side web's top-front corner
         wps=[(0.4, 190, -0.05), (0.6, 195, 2.5), (0.9, 205, 4.4), (1.7, 210, 4.8), (2.66, 208, 4.05),
              (2.85, 207, 3.7)]),
    dict(name="D1", kind="side", r=(0.085, 0.035),       # out of the sides and down into the soil
         wps=[(1.0, 50, 1.8), (2.0, 54, 3.1), (2.9, 58, 2.7), (3.3, 62, 1.2), (3.35, 64, -0.12)]),
    dict(name="D2", kind="side", r=(0.085, 0.035),
         wps=[(1.0, 95, 2.0), (2.0, 99, 3.3), (2.9, 103, 2.8), (3.3, 107, 1.3), (3.35, 109, -0.12)]),
    dict(name="D3", kind="side", r=(0.085, 0.035),
         wps=[(1.0, 150, 1.9), (2.0, 146, 3.2), (2.95, 142, 2.6), (3.3, 138, 1.1), (3.35, 136, -0.12)]),
    dict(name="D4", kind="side", r=(0.085, 0.035),
         wps=[(1.0, 12, 1.7), (2.0, 8, 2.9), (2.9, 5, 2.5), (3.25, 2, 1.1), (3.3, 0, -0.12)]),
    dict(name="R1", kind="low", r=(0.08, 0.034),         # thorny runners along the ground
         wps=[(0.5, 215, 0.12), (1.5, 222, 0.22), (2.4, 232, 0.14), (3.2, 244, 0.2), (3.55, 252, 0.13)]),
    dict(name="R2", kind="low", r=(0.08, 0.034),
         wps=[(0.5, 80, 0.12), (1.5, 74, 0.2), (2.4, 66, 0.13), (3.2, 76, 0.22), (3.5, 84, 0.14)]),
    dict(name="K1", kind="spike", r=(0.07, 0.03),
         wps=[(1.6, 168, 1.2), (2.6, 172, 1.4), (3.15, 177, 1.2)]),
    dict(name="K2", kind="spike", r=(0.07, 0.03),
         wps=[(1.6, 300, 0.9), (2.6, 305, 1.15), (3.1, 310, 0.95)]),
]
# the two webs: corners as (viewer's) BL, BR, TL, TR; a corner given as a cane name is snapped onto that cane
TH_WEBS = [
    dict(name="front", out=(0.0, -1.0, 0.0), seed=11, n_rad=11, hub=(0.47, 0.57),
         BL=(-1.55, -2.95, 2.05), BR=(1.45, -3.0, 2.15), TL=("F1", (-1.45, -2.45, 4.5)), TR=("F2", (1.35, -2.5, 4.7))),
    dict(name="left", out=(-1.0, 0.0, 0.0), seed=23, n_rad=10, hub=(0.52, 0.55),
         BL=(-2.85, 1.15, 1.65), BR=(-2.95, -1.15, 1.55), TL=("A0", (-2.2, 1.05, 4.3)), TR=("L1", (-2.35, -1.25, 4.05))),
]
SPIDER_CANE = "S"


def lobe_balls(B, seed):
    """Explicit lobes: each = a core ellipsoid + mid clumps on its outer side + small puffs on the mid clumps; plus a
    low base that ties the lobes together. Gaps between lobes stay as deep crevices."""
    rng = random.Random(seed)
    bc, ba = B["base"]
    balls = [(Vector(bc), 1.0, ba)]
    for c, ax, nmid in B["lobe_list"]:
        c = Vector(c)
        balls.append((c, 1.0, tuple(a * 0.74 for a in ax)))
        outw = Vector((c.x, c.y, 0.0))
        outw = (outw.normalized() if outw.length > 0.2 else Vector((0, 0, 0))) + Vector((0, 0, 0.45))
        for _ in range(nmid):
            while True:
                d = Vector((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))).normalized()
                d = (d + outw * 0.6).normalized()
                if d.z > -0.35:
                    break
            e = Vector((d.x * ax[0], d.y * ax[1], d.z * ax[2]))
            rm = min(ax) * rng.uniform(0.45, 0.6)
            cm = c + e * rng.uniform(0.55, 0.68)
            balls.append((cm, rm, (1.0, 1.0, rng.uniform(0.85, 1.0))))
            for _ in range(rng.randint(*B["per_mid"])):
                e2 = (d + Vector((rng.gauss(0, 0.55), rng.gauss(0, 0.55), rng.gauss(0, 0.55) + 0.2))).normalized()
                balls.append((cm + e2 * rm * rng.uniform(0.62, 0.8), B["r_small"] * rng.uniform(0.75, 1.25),
                               (1.0, 1.0, 1.0)))
    return balls


def catmull(P, n_per=40):
    out = []
    for i in range(len(P) - 1):
        p0, p1, p2, p3 = P[max(0, i - 1)], P[i], P[i + 1], P[min(len(P) - 1, i + 2)]
        for k in range(n_per):
            t = k / n_per
            out.append(0.5 * ((2 * p1) + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (3 * p1 - p0 - 3 * p2 + p3) * t * t * t))
    out.append(P[-1].copy())
    return out


def cane_from(spec, rng, step=0.04):
    """Smooth path through the waypoints (+ a hanging snapped top for 'broken'), then a gentle helical twist and a
    low-frequency wobble that fade out at the ends (so waypoints that hold a web stay close)."""
    raw = catmull([cyl(*w) for w in spec["wps"]])
    kink = None
    if spec.get("hang"):
        kink = len(resample(raw, step)) - 1
        raw = raw + catmull([cyl(*w) for w in spec["hang"]])[1:]
    pts = resample(raw, step)
    T, Ns, Bs = frames(pts)
    s = arclen(pts)
    o = Vector((rng.uniform(-40, 40), rng.uniform(-40, 40), rng.uniform(-40, 40)))
    ph = rng.uniform(0, TAU)
    twist, period, wob = {"arch": (0.04, 1.5, 0.07), "broken": (0.04, 1.5, 0.05), "side": (0.05, 1.0, 0.06),
                          "low": (0.05, 0.9, 0.05), "spike": (0.03, 0.9, 0.03)}[spec["kind"]]
    out = []
    for i, p in enumerate(pts):
        t = s[i] / s[-1]
        env = math.sin(math.pi * min(1.0, t * 1.1)) ** 0.5 * (1 - 0.7 * smoothstep(0.75, 1.0, t))
        a = TAU * s[i] / period + ph
        q = p + (Ns[i] * math.cos(a) + Bs[i] * math.sin(a)) * twist * env
        q += Vector((noise.noise(o + Vector((s[i] * 0.6, 0, 0))), noise.noise(o + Vector((0, s[i] * 0.6, 3.1))),
                     noise.noise(o + Vector((7.7, 0, s[i] * 0.6))))) * wob * env
        out.append(q)
    return out, kink


def thorn_cfn(rng, p, n, off):
    """Regional colour (coherent patches), small per-leaf variation: green centre turning purple / wine at the margin
    and tip; more purple on top and in some patches."""
    g = ramp(TH_G, 0.5 + 0.7 * fbm(p * 0.6 + off * 1.3, 2) + rng.gauss(0, 0.08))
    pu = ramp(TH_P, 0.5 + 0.7 * fbm(p * 0.5 + off * 0.7, 2) + rng.gauss(0, 0.08))
    k = max(0.0, 0.5 + 0.85 * fbm(p * 0.42 + off, 2) + 0.15 * (p.z - 2.2) / 2.0 + rng.gauss(0, 0.12))
    lift = rng.uniform(0.94, 1.08)

    def f(u, v):
        e = max(abs(u), v ** 1.5)
        c = mix(g, pu, clamp01(k * (0.3 + 0.8 * e)))
        return kcol(mix(kcol(c, 0.85), c, smoothstep(0.0, 0.5, v)), lift)
    return f


def cane_cfn(o, dead=False):
    C = TH_DEAD if dead else TH_CANE

    def f(t, a):
        c = mix(C["base"], C["mid"], smoothstep(0.0, 0.22, t))
        c = mix(c, C["tip"], smoothstep(0.7, 1.0, t))
        g = noise.noise(Vector((math.cos(a) * 1.4, math.sin(a) * 1.4, t * 16.0)) + o)
        c = mix(c, C["dark"], 0.45 * smoothstep(0.0, 0.5, g))
        c = mix(c, C["bloom"], 0.4 * smoothstep(0.25, 0.65, -g))
        return c
    return f


def cane_rfn(o, period_k):
    def f(t, a):
        r = 1 + 0.09 * math.cos(4 * a + t * period_k)
        r *= 1 + 0.04 * noise.noise(Vector((math.cos(a) * 2, math.sin(a) * 2, t * 40)) + o)
        return r
    return f


def thorn_spots(pts, radii, rng, spacing=(0.2, 0.3)):
    """Thorns along a cane: (base point, direction, length, base radius, ring index, normal)."""
    T, Ns, Bs = frames(pts)
    s = arclen(pts)
    out = []
    nxt = rng.uniform(0.15, 0.3)
    ang = rng.uniform(0, TAU)
    for i in range(1, len(pts) - 2):
        if s[i] < nxt:
            continue
        nxt = s[i] + rng.uniform(*spacing)
        ang += 2.4 + rng.uniform(-0.3, 0.3)
        nrm = Ns[i] * math.cos(ang) + Bs[i] * math.sin(ang)
        d = (nrm * 0.78 - T[i] * 0.62).normalized()
        L = (0.11 + 0.11 * radii[i] / 0.1) * rng.uniform(0.85, 1.2)
        out.append((pts[i] + nrm * radii[i] * 0.75, d, L, min(0.055, radii[i] * 0.55), i, nrm))
    return out


def cone(mb, base, d, L, r0, sides, ts=(0.0,), mat=0, cfn=None, rough=0.5, uv=True, shared=None):
    """A straight cone from base along d: rings at fractions ts (radius r0 (1-t)^0.9), then the tip. shared = a dict:
    every cone given the same dict maps onto ONE UV template (tiny repeated parts, e.g. thorns)."""
    d = d.normalized()
    n1 = d.orthogonal().normalized()
    n2 = d.cross(n1)
    first = False
    if uv and shared is not None:
        if "o" not in shared:
            shared["C"], shared["L"] = TAU * r0, L
            shared["o"] = mb.alloc(shared["C"] + 0.02, L + 0.04)
            first = True
        C, L_uv, (ox, oy) = shared["C"], shared["L"], shared["o"]
    else:
        C, L_uv = TAU * r0, L
        ox, oy = mb.alloc(C + 0.02, L + 0.04) if uv else (0.0, 0.0)
    rings = []
    for t in ts:
        r = r0 * (1 - t) ** 0.9
        rings.append([mb.v(base + d * (L * t) + (n1 * math.cos(TAU * j / sides) + n2 * math.sin(TAU * j / sides)) * r,
                           cfn(t, 0.0) if cfn else (0.5, 0.5, 0.5), rough) for j in range(sides)])
    tip = mb.v(base + d * L, cfn(1.0, 0.0) if cfn else (0.5, 0.5, 0.5), rough)
    f0 = len(mb.F)
    for k in range(len(ts) - 1):
        for j in range(sides):
            jn = (j + 1) % sides
            mb.f((rings[k][j], rings[k][jn], rings[k + 1][jn], rings[k + 1][j]), mat,
                 [(ox + C * j / sides, oy + L_uv * ts[k]), (ox + C * (j + 1) / sides, oy + L_uv * ts[k]),
                  (ox + C * (j + 1) / sides, oy + L_uv * ts[k + 1]), (ox + C * j / sides, oy + L_uv * ts[k + 1])]
                 if uv else None)
    for j in range(sides):
        jn = (j + 1) % sides
        mb.f((rings[-1][j], rings[-1][jn], tip), mat,
             [(ox + C * j / sides, oy + L_uv * ts[-1]), (ox + C * (j + 1) / sides, oy + L_uv * ts[-1]),
              (ox + C * (j + 0.5) / sides, oy + L_uv)] if uv else None)
    if uv and shared is not None:
        fids = list(range(f0, len(mb.F)))
        if first:
            shared["faces"] = fids
        else:
            for a, b in zip(fids, shared["faces"]):
                mb.copies.append((a, b, False))
                mb.skipf.add(a)


def thorn_mesh(mb, base, d, L, r0, sides, hi, mat, cane_col, rough, uv=True, shared=None):
    ivory, dark = lin((228, 206, 174)), lin((92, 28, 30))

    def cf(t, a):
        c = mix(cane_col, ivory, smoothstep(0.1, 0.55, t))
        return mix(c, dark, smoothstep(0.75, 1.0, t))
    cone(mb, base, d, L, r0, sides, (0.0, 0.3, 0.6, 0.82) if hi else (0.0,), mat, cf, rough, uv, shared)


def berry_hi(mb, c, r, kind, rng, mat):
    ripe = {"black": (lin((30, 14, 40)), lin((10, 6, 14)), 0.14), "red": (lin((176, 24, 40)), lin((108, 10, 24)), 0.22),
            "purple": (lin((92, 18, 64)), lin((40, 8, 30)), 0.16)}[kind]
    hi_c, lo_c, rgh = ripe
    sphere_mesh(mb, c, r * 0.82, 16, 10, mat, lo_c, rgh, uv=False, sq=1.1)
    n = 30
    ga = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        z = 0.82 - 1.7 * (i + 0.5) / n
        rr = math.sqrt(max(0.0, 1 - z * z))
        d = Vector((rr * math.cos(ga * i), rr * math.sin(ga * i), z))
        dc = mix(hi_c, lo_c, rng.uniform(0.0, 0.35))
        sphere_mesh(mb, c + Vector((d.x * r * 0.74, d.y * r * 0.74, d.z * r * 0.82)), r * 0.33, 10, 7, mat, dc, rgh,
                    uv=False, cfn=lambda q, dc=dc, d=d: mix(dc, lo_c, 0.6 * smoothstep(0.2, -0.6, q.dot(d))))
    for k in range(5):
        a = TAU * k / 5 + rng.uniform(-0.2, 0.2)
        t = Vector((math.cos(a), math.sin(a), 0.0))
        fr = leaf_frame(UP, t, math.radians(-15))
        P = dict(L=r * 0.7, W=r * 0.16, cup=0.2, bend=0.3, kind="lance")
        leaf_hi(mb, c + Vector((0, 0, r * 0.95)), fr, P, lambda u, v: lin((84, 78, 40)), 0.7, mat, nu=3, nv=3)


# ---------------------------------------------------------------- the webs
def ray_hit2(o, d, poly):
    best = None
    for i in range(len(poly) - 1):
        p, q = poly[i], poly[i + 1]
        e = (q[0] - p[0], q[1] - p[1])
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-12:
            continue
        w = (p[0] - o[0], p[1] - o[1])
        t = (w[0] * e[1] - w[1] * e[0]) / den
        u = (w[0] * d[1] - w[1] * d[0]) / den
        if t > 1e-6 and -1e-6 <= u <= 1 + 1e-6 and (best is None or t < best):
            best = t
    return best


def web_frame_uv(rng):
    """An irregular frame polygon in (s, t) 0..1 (top corners near the cane anchors)."""
    base = [(0.05, 0.07), (0.5, 0.02), (0.94, 0.09), (0.98, 0.52), (0.95, 0.96), (0.52, 0.9), (0.04, 0.95),
            (0.02, 0.5)]
    return [(min(0.99, max(0.01, u + rng.uniform(-0.025, 0.025))), min(0.99, max(0.01, v + rng.uniform(-0.025, 0.025))))
            for u, v in base]


def orb_threads(W, H, frame_uv, hub_uv, n_rad, seed):
    """Orb-web threads in local studs (s right, t up): frame, radials, a catch spiral sagging between the radials with
    a few breaks, two torn holes, dangling broken ends and a hub mat. -> [(points, width, alpha)]."""
    rng = random.Random(seed)
    F = [(u * W, v * H) for u, v in frame_uv]
    Fc = F + [F[0]]
    hub = (hub_uv[0] * W, hub_uv[1] * H)
    out = [(Fc, 0.09, 1.0)]
    angs = sorted(TAU * k / n_rad + rng.uniform(-0.2, 0.2) for k in range(n_rad))
    lens = []
    for a in angs:
        t = ray_hit2(hub, (math.cos(a), math.sin(a)), Fc) or 0.5
        lens.append(t)
        out.append(([hub, (hub[0] + math.cos(a) * t, hub[1] + math.sin(a) * t)], 0.075, 0.95))
    holes = [((rng.uniform(0.25, 0.75) * W, rng.uniform(0.12, 0.45) * H), rng.uniform(0.22, 0.34)) for _ in range(2)]
    pitch = 0.135
    r = 0.16
    k = 0
    prev = None
    rmax = max(lens) * 0.93
    while r < rmax:
        i = k % n_rad
        a, L = angs[i], lens[i]
        if r > 0.9 * L:
            prev = None
        else:
            p = (hub[0] + math.cos(a) * r, hub[1] + math.sin(a) * r)
            if prev is not None:
                mid = ((prev[0] + p[0]) / 2, (prev[1] + p[1]) / 2)
                hole = any(math.hypot(mid[0] - hc[0], mid[1] - hc[1]) < hr for hc, hr in holes)
                ln = math.hypot(p[0] - prev[0], p[1] - prev[1])
                if not hole and rng.random() > 0.06:
                    sag = 0.07 * ln + 0.01
                    seg = [(prev[0] + (p[0] - prev[0]) * u, prev[1] + (p[1] - prev[1]) * u - sag * 4 * u * (1 - u))
                           for u in (0.0, 0.25, 0.5, 0.75, 1.0)]
                    out.append((seg, 0.062, 0.9))
                elif rng.random() < 0.45:
                    dl = rng.uniform(0.12, 0.3)
                    out.append(([prev, (prev[0] + rng.uniform(-0.05, 0.05), prev[1] - dl * 0.6),
                                 (prev[0] + rng.uniform(-0.08, 0.08), prev[1] - dl)], 0.055, 0.85))
            prev = p
        k += 1
        r += pitch / n_rad
    for j in range(3):                                       # hub mat
        rr = 0.035 + 0.04 * j
        ring = [(hub[0] + math.cos(TAU * q / 9) * rr * rng.uniform(0.8, 1.2),
                 hub[1] + math.sin(TAU * q / 9) * rr * rng.uniform(0.8, 1.2)) for q in range(10)]
        ring[-1] = ring[0]
        out.append((ring, 0.05, 0.85))
    return out, F, hub


def paint_threads(A, threads, ox, oy, sc):
    h, w = A.shape
    for pts, wd, al in threads:
        hw = max(0.7, wd * sc / 2)
        for a, b in zip(pts[:-1], pts[1:]):
            ax, ay, bx, by = ox + a[0] * sc, oy + a[1] * sc, ox + b[0] * sc, oy + b[1] * sc
            x0, x1 = int(max(0, math.floor(min(ax, bx) - hw - 2))), int(min(w - 1, math.ceil(max(ax, bx) + hw + 2)))
            y0, y1 = int(max(0, math.floor(min(ay, by) - hw - 2))), int(min(h - 1, math.ceil(max(ay, by) + hw + 2)))
            if x1 < x0 or y1 < y0:
                continue
            X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            dx, dy = bx - ax, by - ay
            L2 = max(1e-9, dx * dx + dy * dy)
            t = np.clip(((X - ax) * dx + (Y - ay) * dy) / L2, 0, 1)
            d = np.hypot(X - (ax + t * dx), Y - (ay + t * dy))
            v = al * np.clip(hw + 0.5 - d, 0, 1)
            sub = A[y0:y1 + 1, x0:x1 + 1]
            np.maximum(sub, v, out=sub)


def poly_mask(X, Y, poly):
    m = np.zeros(X.shape, bool)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        m ^= ((y1 > Y) != (y2 > Y)) & (X < (x2 - x1) * (Y - y1) / (y2 - y1 + 1e-12) + x1)
    return m


def web_texture(prefix, size, webs):
    """RGBA silk atlas: per web region, a faint torn film inside the frame + the painted orb threads (alpha ~0.9),
    silvery off-white, a little dust. webs: [dict(threads, frame, hub, ox, oy, sc, W, H, seed)]."""
    A = np.zeros((size, size), np.float32)
    film = np.zeros((size, size), np.float32)
    for wb in webs:
        paint_threads(A, wb["threads"], wb["ox"], wb["oy"], wb["sc"])
        x0, y0 = int(wb["ox"]), int(wb["oy"])
        x1, y1 = int(min(size, wb["ox"] + wb["W"] * wb["sc"] + 2)), int(min(size, wb["oy"] + wb["H"] * wb["sc"] + 2))
        X, Y = np.meshgrid((np.arange(x0, x1) + 0.5 - wb["ox"]) / wb["sc"], (np.arange(y0, y1) + 0.5 - wb["oy"]) / wb["sc"])
        inside_m = poly_mask(X, Y, wb["frame"])
        n1 = mnoise(max(x1 - x0, y1 - y0), 3.5, wb["seed"], 3)[:y1 - y0, :x1 - x0]
        n2 = mnoise(max(x1 - x0, y1 - y0), 2.6, wb["seed"] + 5, 3)[:y1 - y0, :x1 - x0]
        hd = np.hypot(X - wb["hub"][0], Y - wb["hub"][1])
        f = (0.07 + 0.12 * n1) * np.clip((0.68 - n2) / 0.1, 0, 1) + 0.45 * np.exp(-(hd / 0.1) ** 2)
        film[y0:y1, x0:x1] = np.where(inside_m, f, 0.0)
    alpha = 1 - (1 - A) * (1 - film)
    dust = np.clip((mnoise(size, 6.0, 77, 3) - 0.5) * 2.0, 0, 1) * 0.35
    thr, flm, dc = srgb((222, 224, 230)), srgb((200, 200, 208)), srgb((168, 160, 150))
    w = np.clip(A / np.maximum(alpha, 1e-4), 0, 1)[..., None]
    col = thr[None, None, :] * w + flm[None, None, :] * (1 - w)
    col = col * (1 - dust[..., None]) + dc[None, None, :] * dust[..., None]
    img = np.zeros((size, size, 4), np.float32)
    img[..., :3] = col
    img[..., 3] = alpha
    return make_image(prefix + "_albedo", img, "sRGB", os.path.join(MAPS, prefix + "_albedo.png"))


def nearest_on(pts, q):
    i = min(range(len(pts)), key=lambda k: (pts[k] - q).length_squared)
    return pts[i].copy(), i


def build_webs(bvh, canes_by_name, targets, rng):
    """Two orb webs. Returns (Web strands object, WebSilk object, info). targets: candidate anchor points (thorn
    bases, leaf tips)."""
    fast = CFG["fast"]
    size = 512 if fast else 1024
    nu, nv = (5, 4) if fast else (7, 6)
    webs = []
    for spec in TH_WEBS:
        cr = {}
        for key in ("BL", "BR", "TL", "TR"):
            v = spec[key]
            if isinstance(v[0], str):
                p, _ = nearest_on(canes_by_name[v[0]]["pts"], Vector(v[1]))
                cr[key] = p
            else:
                cr[key] = Vector(v)
        W = ((cr["BR"] - cr["BL"]).length + (cr["TR"] - cr["TL"]).length) / 2
        H = ((cr["TL"] - cr["BL"]).length + (cr["TR"] - cr["BR"]).length) / 2
        n_out = Vector(spec["out"]).normalized()
        G = []
        for i in range(nv + 1):
            t = i / nv
            row = []
            for j in range(nu + 1):
                s = j / nu
                p = (cr["BL"].lerp(cr["BR"], s)).lerp(cr["TL"].lerp(cr["TR"], s), t)
                p += n_out * (0.12 * math.sin(math.pi * s) * math.sin(math.pi * t))
                for _ in range(12):                      # keep the sheet 0.15 clear of the foliage (pushed outward)
                    loc, nrm, idx, dist = bvh.find_nearest(p)
                    inside_ = (p - loc).dot(nrm) < 0
                    if not inside_ and dist >= 0.15:
                        break
                    p += n_out * 0.06
                row.append(p)
            G.append(row)
        rngw = random.Random(spec["seed"])
        frame_uv = web_frame_uv(rngw)
        threads, F, hub = orb_threads(W, H, frame_uv, spec["hub"], spec["n_rad"], spec["seed"])
        webs.append(dict(spec=spec, cr=cr, W=W, H=H, G=G, n_out=n_out, threads=threads, frame=F, hub=hub,
                         frame_uv=frame_uv, seed=spec["seed"]))
    # atlas layout: stacked, isotropic scale
    sc = min((size - 24) / (webs[0]["H"] + webs[1]["H"]), (size - 16) / max(webs[0]["W"], webs[1]["W"]))
    webs[0]["ox"], webs[0]["oy"], webs[0]["sc"] = 8.0, 8.0, sc
    webs[1]["ox"], webs[1]["oy"], webs[1]["sc"] = 8.0, 16.0 + webs[0]["H"] * sc, sc
    img = web_texture("BushThornSilk", size, webs)

    def sheet_at(wb, s, t, lift=0.0):
        G = wb["G"]
        x, y = min(0.9999, max(0.0, s)) * nu, min(0.9999, max(0.0, t)) * nv
        j, i = int(x), int(y)
        fx, fy = x - j, y - i
        p = (G[i][j] * (1 - fx) * (1 - fy) + G[i][j + 1] * fx * (1 - fy) + G[i + 1][j] * (1 - fx) * fy
             + G[i + 1][j + 1] * fx * fy)
        return p + wb["n_out"] * lift

    mbs = MB()
    for wb in webs:
        G = wb["G"]

        def uvst(s, t, wb=wb):
            return ((wb["ox"] + s * wb["W"] * wb["sc"]) / size, (wb["oy"] + t * wb["H"] * wb["sc"]) / size)

        for side in (1, -1):
            ids = [[mbs.v(G[i][j]) for j in range(nu + 1)] for i in range(nv + 1)]
            for i in range(nv):
                for j in range(nu):
                    q = (ids[i][j], ids[i][j + 1], ids[i + 1][j + 1], ids[i + 1][j])
                    uvs = [uvst(j / nu, i / nv), uvst((j + 1) / nu, i / nv), uvst((j + 1) / nu, (i + 1) / nv),
                           uvst(j / nu, (i + 1) / nv)]
                    a, b, c = G[i][j], G[i][j + 1], G[i + 1][j + 1]
                    facing = (b - a).cross(c - a).dot(wb["n_out"]) > 0
                    if facing != (side > 0):
                        q, uvs = tuple(reversed(q)), list(reversed(uvs))
                    mbs.f(q, 0, uvs)
    silk = mbs.obj("WebSilk", [mat_tex("BushThornSilk_Mat", img, rough=0.7, alpha=True)])
    for a in list(silk.data.color_attributes):
        silk.data.color_attributes.remove(a)

    # ------------------------------------------------ strand geometry: frame threads + anchor threads
    def clear_of_body(pts, margin=0.04):
        for q in pts[1:-1]:
            loc, nrm, idx, dist = bvh.find_nearest(q)
            if (q - loc).dot(nrm) < 0 or dist < margin:
                return False
        return True

    def hang(a, b, sag):
        n = max(5, int((b - a).length / 0.2))
        for k in range(6):
            pts = catenary(a, b, n, sag * (1 - k / 6))
            if clear_of_body(pts):
                return pts
        return None

    mbw = MB()
    lines = []
    rngs = random.Random(5)
    for wb in webs:
        F = wb["frame"]
        fr_pts = []
        Fc = F + [F[0]]
        for a, b in zip(Fc[:-1], Fc[1:]):                    # frame threads on the sheet
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            n = max(2, int(L / 0.3))
            for k in range(n):
                u = k / n
                fr_pts.append(sheet_at(wb, (a[0] + (b[0] - a[0]) * u) / wb["W"], (a[1] + (b[1] - a[1]) * u) / wb["H"],
                                       0.015))
        fr_pts.append(fr_pts[0])
        lines.append((fr_pts, 0.042))
        verts = [sheet_at(wb, u, v, 0.015) for u, v in wb["frame_uv"]]
        corners = {"TL": wb["cr"]["TL"], "TR": wb["cr"]["TR"]}
        for k, p in enumerate(verts):                          # anchor threads out of every frame corner
            u, v = wb["frame_uv"][k]
            if v > 0.85 and (u < 0.15 or u > 0.85):            # top corners: tie to the supporting cane
                c = corners["TL"] if u < 0.5 else corners["TR"]
                pts = hang(p, c, 0.02)
                if pts:
                    lines.append((pts, 0.042))
            cand = [q for q in targets if 0.45 < (q - p).length < 1.7 and (q - p).dot(wb["n_out"]) > -0.4]
            rngs.shuffle(cand)
            made = 0
            for q in cand:
                if made >= (2 if v < 0.2 else 1):
                    break
                pts = hang(p, q, rngs.uniform(0.04, 0.22) * (q - p).length)
                if pts:
                    lines.append((pts, rngs.uniform(0.038, 0.044)))
                    made += 1
        for u in (0.3, 0.68):                                  # two short broken ends hanging off the bottom
            p = sheet_at(wb, u, 0.05, 0.02)
            ln = rngs.uniform(0.3, 0.45)
            sw = rngs.choice((-1, 1)) * 0.12
            pts = [p + Vector((0, 0, 0))] + [p + Vector((0, 0, -ln * k / 4)) + wb["n_out"] * (0.04 * k)
                                            + Vector((sw * math.sin(k / 4 * 1.6), 0, 0)) for k in range(1, 5)]
            if clear_of_body(pts, 0.02):
                lines.append((pts, 0.038))
    for pts, r in lines:
        tube(mbw, pts, [r] * len(pts), 3, 0, cap_tip=False, uv=False)
    web = mbw.obj("Web", [], uv=None)
    mn, mx = bbox_of([web])
    szw = max(mx[0] - mn[0], mx[1] - mn[1], mx[2] - mn[2])
    lay = web.data.uv_layers.new(name="UVMap")
    data = []
    for lp in web.data.loops:
        co = web.data.vertices[lp.vertex_index].co
        data.extend(((co.x - mn[0]) / szw, (co.z - mn[2]) / szw))
    lay.data.foreach_set("uv", data)
    web.data.materials.append(mat_tex("BushThornWeb_Mat", strand_texture("BushThornWeb", 128), rough=0.6))
    for a in list(web.data.color_attributes):
        web.data.color_attributes.remove(a)
    info = {"web_lines": len(lines), "webs": {}}
    for wb in webs:
        hub3 = sheet_at(wb, wb["hub"][0] / wb["W"], wb["hub"][1] / wb["H"])
        info["webs"][wb["spec"]["name"]] = {"size_studs": [round(wb["W"], 2), round(wb["H"], 2)],
                                            "hub_roblox": rb(hub3),
                                            "corners_roblox": {k: rb(v) for k, v in wb["cr"].items()}}
    return web, silk, info


def build_thorn():
    fast = CFG["fast"]
    size = 256 if fast else 1024
    fresh(8)
    rng = random.Random(1307)
    nrng = np.random.default_rng(1307)
    off = Vector((3.3, 9.1, 4.4))
    m_body = mat_vc("ThornBodyHi")
    m_leaf = mat_leaf("ThornLeafHi", vein_light=0.55, edge_dark=0.4, bump=0.6, freq=6.5, edge_col=lin((70, 18, 64)))
    m_wood = mat_vc("ThornWoodHi")
    m_berry = mat_vc("ThornBerryHi")

    def body_col(p, n):
        t = 0.5 + 0.5 * fbm(p * 0.8 + off, 2)
        return mix(lin((18, 12, 24)), lin((24, 38, 28)), t), 0.8

    hi = clump_body("ThornBody_hi", TH_BODY, 17, 0.1 if fast else 0.055, m_body, body_col)
    log("thorn body hi", tris_of(hi))
    body_lo = decimate_to(hi, "ThornBody_lo", 2750, inflate=0.1)
    smart_uv(body_lo)
    log("thorn body lo", tris_of(body_lo))
    bvh, bvh_bm = bvh_of([body_lo])
    # ---------------------------------------------------------------- canes
    canes = []
    for spec in TH_CANES:
        pts, kink = cane_from(spec, rng)
        n = len(pts)
        r0, r1 = spec["r"]
        c = dict(spec=spec, name=spec["name"], kind=spec["kind"], pts=pts, dead=spec.get("dead", False),
                 radii=[r0 + (r1 - r0) * (i / (n - 1)) ** 0.9 for i in range(n)],
                 o=Vector((rng.uniform(-30, 30), rng.uniform(-30, 30), rng.uniform(-30, 30))))
        if kink:                                      # the snapped point: a ragged swelling
            for i in range(max(0, kink - 2), min(n, kink + 3)):
                c["radii"][i] *= 1.25
        c["thorns"] = thorn_spots(pts, c["radii"], rng)
        c["out"] = [not inside(bvh, p) and p.z > 0.02 for p in pts]
        canes.append(c)
    by_name = {c["name"]: c for c in canes}
    mbh_w, mbh_b, mbh_l, mbh_p, mbl = MB(), MB(), MB(), MB(), MB()
    mbl.add_object_mesh(body_lo, 0)
    MAT_BODY, MAT_TOP, MAT_BOT, MAT_WOOD, MAT_BERRY = 0, 1, 2, 3, 4
    thorn_uv = {}
    targets = []
    for c in canes:
        cf, rf = cane_cfn(c["o"], c["dead"]), cane_rfn(c["o"], 22.0)
        tube(mbh_w, c["pts"], c["radii"], 6 if fast else 12, 0, cfn=cf, rfn=rf, rough=0.55 if c["dead"] else 0.45,
             cap_tip=True, tipk=2.0, uv=False)
        for base, d, L, r0, i, nrm in c["thorns"]:
            thorn_mesh(mbh_w, base - nrm * 0.01, d, L, r0, 8, True, 0, cf(i / len(c["pts"]), 0.0), 0.42, uv=False)
        idx = [i for i, o in enumerate(c["out"]) if o]
        if not idx:
            continue
        i0, i1 = max(0, idx[0] - 10), min(len(c["pts"]) - 1, idx[-1] + 4)
        sub = c["pts"][i0:i1 + 1]
        lo_pts = resample(sub, 0.26 if c["kind"] in ("arch", "broken") else 0.3)
        lo_r = interp_radii(sub, c["radii"][i0:i1 + 1], lo_pts)
        sides = 5 if c["kind"] in ("arch", "broken") else 4
        tip_in_soil = c["pts"][-1].z < 0.0
        tube(mbl, lo_pts, lo_r, sides, MAT_WOOD, cap_tip=not tip_in_soil, tipk=2.0, t0=i0 / (len(c["pts"]) - 1),
             t1=i1 / (len(c["pts"]) - 1))
        for base, d, L, r0, i, nrm in c["thorns"]:
            if c["out"][i] and i0 <= i <= i1:
                thorn_mesh(mbl, base - nrm * 0.012, d, L, r0, 3, False, MAT_WOOD, (0.5,) * 3, 0.42, shared=thorn_uv)
                targets.append(base + d * L * 0.8)
    # ---------------------------------------------------------------- the clump leaves (bake source)
    P_s, N_s, area = surface_samples(hi, int(30 * 96 * (0.35 if fast else 1.0)), nrng)
    nleaf = 0
    for p, n in zip(P_s, N_s):
        if p.z < TH_BODY["zflat"] + 0.06:
            continue
        L = rng.uniform(0.34, 0.52)
        P = dict(L=L, W=L * rng.uniform(0.27, 0.33), cup=rng.uniform(0.2, 0.45), bend=rng.uniform(0.1, 0.32),
                 twist=rng.uniform(-0.4, 0.4), kind="broad" if rng.random() < 0.5 else "ovate")
        fr = leaf_frame(n, tangent_dir(n, rng), math.radians(rng.uniform(8, 36)), rng.uniform(-0.45, 0.45))
        leaf_hi(mbh_l, p + n * rng.uniform(-0.05, 0.1), fr, P, thorn_cfn(rng, p, n, off), 0.76, 0,
                nu=5, nv=5 if fast else 7)
        nleaf += 1
    log("thorn hi leaves", nleaf, "area", round(area, 1))

    # ---------------------------------------------------------------- protruding leaves: on the OUTLINE
    def behind_web(p):
        for spec in TH_WEBS:
            nout = Vector(spec["out"])
            if spec["name"] == "front" and p.y > -1.2:
                continue
            if spec["name"] == "left" and p.x > -1.2:
                continue
            if 1.9 < p.z < 4.6 and (abs(p.x) < 1.5 if spec["name"] == "front" else abs(p.y) < 1.2):
                return True
        return False

    def outline_w(p, n):
        side = 1.0 - min(1.0, abs(n.z) / 0.75)
        low = 1.0 + 0.8 * smoothstep(2.6, 0.6, p.z)
        return (0.15 + side) * low * (0.3 if behind_web(p) else 1.0)

    P_l, N_l, _ = surface_samples(body_lo, 3000, nrng)
    cands = [(p, n) for p, n in zip(P_l, N_l) if n.z > -0.55 and p.z > 0.35 and rng.random() < outline_w(p, n) / 2.0]
    prot = dart(cands, 0.4, 82)
    n_out_leaf = n_in_leaf = 0
    tips = []
    for p, n in prot:
        outline = abs(n.z) < 0.6 or p.z < 1.6
        L = rng.uniform(0.5, 0.68) if outline else rng.uniform(0.46, 0.58)
        P = dict(L=L, W=L * rng.uniform(0.27, 0.32), cup=rng.uniform(0.25, 0.4), bend=rng.uniform(0.18, 0.38),
                 twist=rng.uniform(-0.35, 0.35), kind="broad" if rng.random() < 0.5 else "ovate")
        tilt = rng.uniform(22, 55) if outline else rng.uniform(12, 32)
        fr = leaf_frame(n, tangent_dir(n, rng, 0.75 if outline else 0.5), math.radians(tilt), rng.uniform(-0.4, 0.4))
        B = p - n * 0.07
        leaf_lo(mbl, B, fr, P, MAT_TOP, MAT_BOT, vs=(0.15, 0.38, 0.62, 0.85) if outline else (0.33, 0.68))
        leaf_hi(mbh_p, B, fr, P, thorn_cfn(rng, p, n, off), 0.76, 0, nu=5, nv=7)
        tips.append(leaf_point(B, fr, P, 0.0, 1.0))
        if outline:
            n_out_leaf += 1
        else:
            n_in_leaf += 1
    # leaves drooping over the base rim (break the lower outline)
    n_base = 0
    base_c = [(p, n) for p, n in zip(P_l, N_l) if 0.2 < p.z < 1.0 and n.z < 0.35]
    for p, n in dart(base_c, 0.55, 16):
        hz = Vector((n.x, n.y, 0.0))
        if hz.length < 0.2:
            continue
        hz.normalize()
        L = rng.uniform(0.5, 0.66)
        P = dict(L=L, W=L * 0.3, cup=0.3, bend=rng.uniform(0.15, 0.3), twist=rng.uniform(-0.3, 0.3),
                 kind="broad" if rng.random() < 0.5 else "ovate")
        d = (hz * 0.8 + DOWN * rng.uniform(0.3, 0.6)).normalized()
        nb = (hz.cross(UP)).normalized()
        upv = d.cross(nb)
        if upv.z < 0:
            upv = -upv
        B = p - n * 0.05
        fr = (d, upv, d.cross(upv))
        if leaf_point(B, fr, P, 0.0, 1.0).z < 0.05 or min(leaf_point(B, fr, P, u, 0.8).z for u in (-1, 1)) < 0.04:
            continue
        leaf_lo(mbl, B, fr, P, MAT_TOP, MAT_BOT)
        leaf_hi(mbh_p, B, fr, P, thorn_cfn(rng, p, n, off), 0.76, 0, nu=5, nv=7)
        tips.append(leaf_point(B, fr, P, 0.0, 1.0))
        n_base += 1
    # small leaves along the exposed (live) canes
    ncl = 0
    for c in canes:
        if c["dead"]:
            continue
        pts = c["pts"]
        T, Ns, Bs = frames(pts)
        s = arclen(pts)
        nxt = rng.uniform(0.3, 0.8)
        for i in range(len(pts) - 6):
            if not c["out"][i] or s[i] < nxt or ncl >= 16:
                continue
            nxt = s[i] + rng.uniform(1.0, 1.5)
            a = rng.uniform(0, TAU)
            nrm = Ns[i] * math.cos(a) + Bs[i] * math.sin(a)
            nrm = (nrm + UP * 0.5).normalized()
            L = rng.uniform(0.42, 0.56)
            P = dict(L=L, W=L * 0.3, cup=0.3, bend=rng.uniform(0.2, 0.35), twist=rng.uniform(-0.3, 0.3), kind="ovate")
            fr = leaf_frame(nrm, (T[i] + nrm * 0.2).normalized(), math.radians(rng.uniform(35, 60)),
                            rng.uniform(-0.5, 0.5))
            B = pts[i] + nrm * c["radii"][i] * 0.5
            leaf_lo(mbl, B, fr, P, MAT_TOP, MAT_BOT, vs=(0.33, 0.68))
            leaf_hi(mbh_p, B, fr, P, thorn_cfn(rng, pts[i], nrm, off), 0.76, 0, nu=5, nv=7)
            tips.append(leaf_point(B, fr, P, 0.0, 1.0))
            ncl += 1
    log("thorn leaves: outline", n_out_leaf, "inner", n_in_leaf, "base", n_base, "cane", ncl)
    # ---------------------------------------------------------------- berries: mostly black / deep purple
    berries = []
    d1 = by_name["D1"]["pts"]
    top_i = max(range(len(d1)), key=lambda k: d1[k].z)
    for ci_pt, nb in ((d1[top_i], 3), (by_name["A0"]["pts"][-1], 3)):
        for k in range(nb):
            a = TAU * k / nb + rng.uniform(-0.3, 0.3)
            berries.append((ci_pt + Vector((0.13 * math.cos(a), 0.13 * math.sin(a), -0.2 - 0.06 * k)), ci_pt))
    o3 = cyl(4.0, 235, 1.55)
    hit = bvh.ray_cast(o3, (Vector((0, 0, 1.55)) - o3).normalized())
    if hit[0] is not None:
        fp, fn = hit[0], hit[1]
        for k in range(4):
            a = TAU * k / 4 + 0.4
            berries.append((fp + fn * 0.17 + Vector((0.16 * math.cos(a), 0, 0.16 * math.sin(a))), fp + fn * 0.02))
    kinds = ["black", "black", "purple", "black", "purple", "black", "black", "red", "black", "purple"]
    for k, (c, anchor) in enumerate(berries):
        r = rng.uniform(0.13, 0.15)
        kind = kinds[k % len(kinds)]
        berry_hi(mbh_b, c, r, kind, rng, 0)
        sphere_mesh(mbl, c, r * 1.02, 7, 5, MAT_BERRY, sq=1.1)
        stalk = [anchor, anchor.lerp(c, 0.5) + Vector((0, 0, 0.03)), c + Vector((0, 0, r * 0.9))]
        tube(mbh_w, stalk, [0.022, 0.02, 0.018], 6, 0, cfn=lambda t, a: lin((70, 76, 36)), rough=0.6, cap_tip=False,
             uv=False)
        tube(mbl, stalk, [0.026, 0.024, 0.022], 3, MAT_WOOD, cap_tip=False)
    # ---------------------------------------------------------------- objects + bake
    wood_hi = mbh_w.obj("ThornWood_hi", [m_wood], uv=None)
    berry_hi_o = mbh_b.obj("ThornBerries_hi", [m_berry], uv=None)
    leaves_hi = mbh_l.obj("ThornLeaves_hi", [m_leaf], uv="LeafUV")
    prot_hi = mbh_p.obj("ThornProt_hi", [m_leaf], uv="LeafUV")
    bush = mbl.obj("Bush", placeholder_mats(["Body", "LeafTop", "LeafBot", "Wood", "Berry"]))
    log("thorn game mesh by material", tris_by_mat(bush))
    log("thorn game mesh tris", tris_of(bush), "hi:", tris_of(leaves_hi), tris_of(prot_hi), tris_of(wood_hi),
        tris_of(berry_hi_o))
    hide(body_lo)
    pack_uvs(bush, {MAT_TOP: 1.25, MAT_BERRY: 1.6, MAT_WOOD: 1.1}, mbl.skipf)
    copy_uvs(bush, mbl.copies)
    bush.hide_render = True
    groups = []
    for nm, keep, his, cage, maxray in (("G_Body", (MAT_BODY,), [hi, leaves_hi, wood_hi, berry_hi_o], 0.36, 0.7),
                                        ("G_Leaf", (MAT_TOP,), [prot_hi], 0.03, 0.08),
                                        ("G_Wood", (MAT_WOOD,), [wood_hi], 0.05, 0.12),
                                        ("G_Berry", (MAT_BERRY,), [berry_hi_o], 0.05, 0.12)):
        groups.append((split_mats(bush, nm, keep), his, cage, maxray))
    imgs = bake_groups(groups, size, "BushThorn", ao_strength=0.6, ao_dist=0.8, ao_tint=(0.2, 0.05, 0.24))
    for g in groups:
        bpy.data.objects.remove(g[0])
    finish_lo(bush, "BushThorn", imgs)
    hide(hi, leaves_hi, prot_hi, wood_hi, berry_hi_o)
    # ---------------------------------------------------------------- the webs
    web, silk, web_info = build_webs(bvh, by_name, targets + tips, rng)
    sp = by_name[SPIDER_CANE]["pts"][-1] + Vector((0, 0, -0.06))
    loc = bvh.ray_cast(sp + Vector((0, 0, -0.05)), DOWN)[0]
    rep = {"tris": {o.name: tris_of(o) for o in (bush, web, silk)}, "texture": size, "bake": imgs["stats"],
           "atlas_coverage": imgs["coverage"], "hi_leaves": nleaf,
           "game_leaves": {"outline": n_out_leaf, "inner": n_in_leaf, "base": n_base, "cane": ncl},
           "berries": len(berries), "spider_point_blender": [round(v, 3) for v in sp], "spider_point_roblox": rb(sp),
           "spider_free_drop": round((sp.z - loc.z) if loc is not None else sp.z, 3)}
    rep.update(web_info)
    mn, mx = bbox_of([bush, web, silk])
    rep["bbox_blender"] = [[round(float(v), 3) for v in mn], [round(float(v), 3) for v in mx]]
    rep["size_roblox_XYZ"] = [round(float(mx[0] - mn[0]), 3), round(float(mx[2] - mn[2]), 3),
                              round(float(mx[1] - mn[1]), 3)]
    bvh_bm.free()
    finish("thorn", rep)
    return rep


