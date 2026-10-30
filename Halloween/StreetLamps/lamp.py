# SLINGSHOT Halloween hub - STREET LAMP "Pumpkin lantern post" (2026-10-13), headless Blender 5.2 only.
#   blender.exe -b --factory-startup --python lamp.py -- [fast] preview | build | bake post | bake cage |
#               bake pumpkin | web | export | verify | calib | review
# One FBX: C:\cdimp\Halloween_StreetLamp.fbx with Post / Cage / Pumpkin / Web / WebSilk. FBX origin = ground contact
# point at the base centre. The arm, the hook and the pumpkin face point to Blender -Y.
# Pipeline: every shape is a generator (lathe / sweep / param surface) sampled twice - dense + displaced + per-vertex
# Col/Rough/Wear (bake source) and coarse (game mesh, explicit param UVs) - then per-part Cycles bakes (bake_groups:
# each lo part only ray-matches its own hi part), PBR material, FBX. The pumpkin follows PumpkinEggs (same cutter on
# hi and lo, planar caps, repair_attrs, hole check).
import sys, os
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\StreetLamps")
from lampkit import *  # noqa: F401,F403

SRC = os.path.join(OUT, "lamp_src.blend")
FINAL = os.path.join(OUT, "lamp.blend")
FBX = os.path.join(CDIMP, "Halloween_StreetLamp.fbx")

# ===================================================================== design
HANG_Y = -3.55                       # hanging axis (Blender y); x = 0
CROOK = dict(a1=1.8, b1=1.8, b2=1.2, r0=0.56, r1=0.29, W=285.0, apex_z=17.58)
POLE_R0, POLE_R1, POLE_Z0, POLE_Z1 = 0.29, 0.22, 2.64, 15.60
FLUTE_D = 0.03
TWIST = dict(z0=6.40, z1=7.90, pitch=1.0, amp=0.21)
COLLARS = [(6.06, 6.40), (7.90, 8.24)]          # + collar 3 at the pole top (set from the crook start)
PUMP = dict(N=8, R=1.35, Rz=0.96, egg=0.0, depth=0.10, crest=0.45, lumps=0.025, micro=0.003, dtop=0.14,
            dtop_w=0.38, dbot=0.04, flat=0.9, flat_k=0.18, seed=505, phase=0.0)
SHELL = 0.17
STRAP_GAP = 0.36                    # strap centreline offset from the pumpkin's max-radius envelope
BUDGET = {"Post": 6500, "Cage": 3300, "Pumpkin": 3700, "Web": 1500, "WebSilk": 320}
TOTAL_CAP = 14000
RING = dict(ri=0.15, rw=0.04)       # round ring over the hook cradle (inner radius / wire)
LINK = dict(Li=0.27, Wi=0.15, rw=0.045)
HOLE_R = 0.055


def rp(z):
    return POLE_R0 + (POLE_R1 - POLE_R0) * (z - POLE_Z0) / (POLE_Z1 - POLE_Z0)


def RES():
    f = CFG["fast"]
    return dict(hs=2 if f else 1, tex_big=256 if f else 1024, tex_small=256 if f else 512, samples=8 if f else 24)


# ===================================================================== the crook centreline (y' = -y, z)
def crook_curve(a1, b1, a2, b2, r0, r1, W, apex_z, n=6000):
    """Rising quarter-ellipse (a1, b1) + descending quarter-ellipse (a2, b2) + an inward spiral curl (radius r0 ->
    r1 over W degrees), built from the radius-of-curvature vs turned-angle function (blended at the joints) and
    integrated, so the bar is G2-smooth. Returns dense arrays."""
    def Rell(a, b, th):
        return a * a * b * b / (a * a * np.sin(th) ** 2 + b * b * np.cos(th) ** 2) ** 1.5
    phi = np.linspace(0.0, 180.0 + W, n)
    th = np.radians(90.0 - phi)
    R1, R2 = Rell(a1, b1, th), Rell(a2, b2, th)
    Rc = r0 + (r1 - r0) * np.clip((phi - 180.0) / W, 0, 1)

    def ramp(c, w):
        t = np.clip((phi - (c - w)) / (2 * w), 0, 1)
        return t * t * (3 - 2 * t)
    t1, t2 = ramp(90.0, 16.0), ramp(180.0, 14.0)
    k = (1 - t1) / R1 + t1 / R2
    k = (1 - t2) * k + t2 / Rc
    R = 1 / k
    ds = R * np.radians(phi[1] - phi[0])
    y = np.concatenate([[0], np.cumsum(np.cos(th[:-1]) * ds[:-1])])
    z = np.concatenate([[0], np.cumsum(np.sin(th[:-1]) * ds[:-1])])
    ia = int(np.argmin(abs(phi - 90)))
    z = z + (apex_z - z[ia])
    s = np.concatenate([[0], np.cumsum(ds[:-1])])
    return dict(phi=phi, y=y, z=z, R=R, s=s, ia=ia, ic=int(np.argmin(abs(phi - 270))),
                idn=int(np.argmin(abs(phi - 180))))


def crook_design():
    c = CROOK
    lo, hi = 0.8, 4.0
    for _ in range(48):
        a2 = (lo + hi) / 2
        cv = crook_curve(c["a1"], c["b1"], a2, c["b2"], c["r0"], c["r1"], c["W"], c["apex_z"])
        if cv["y"][cv["ic"]] > -HANG_Y:
            hi = a2
        else:
            lo = a2
    cv["a2"] = a2
    cv["zs"] = cv["z"][0]
    return cv


def crook_radius(cv, s):
    """Bar radius along the crook arc length s (s = 0 at the crook start, negative inside collar 3)."""
    sa, sd, sc, se = cv["s"][cv["ia"]], cv["s"][cv["idn"]], cv["s"][cv["ic"]], cv["s"][-1]
    xs = [-1.0, 0.0, sa, sd, sc, se]
    rs = [0.215, 0.215, 0.172, 0.125, 0.097, 0.086]
    r = np.interp(s, xs, rs)
    sb = sd - 0.30                                          # forged bead where the arm turns into the hook
    r = r + 0.026 * np.exp(-((np.asarray(s) - sb) / 0.035) ** 2)
    return r


# ===================================================================== column (lathe)
BASE_PRIO = 1.6                     # texel priority of the base island (round 2: crisp gothic panels)
BASE_PROFILE = [
    (0.200, 0.000), (0.200, 0.860), (0.215, 0.935), (0.250, 0.965), (0.360, 0.968), (0.405, 0.945), (0.430, 0.890),
    (0.447, 0.815), (0.560, 0.790), (0.600, 0.752), (0.625, 0.706), (0.668, 0.716),
    (0.775, 0.660), (0.950, 0.668), (1.100, 0.676), (1.300, 0.656), (1.500, 0.602), (1.700, 0.532),
    (1.900, 0.476), (2.100, 0.443), (2.262, 0.430),
    (2.315, 0.478), (2.385, 0.492), (2.545, 0.400), (2.600, 0.335), (2.640, rp(2.64))]


def collar_rings(z0, z1, top=False):
    pts = [(z0, rp(z0)), (z0 + 0.06, rp(z0) + 0.072), (z1 - 0.06, rp(z1) + 0.072)]
    pts.append((z1, 0.19 if top else rp(z1)))
    return pts


def seam_shift(acc, uvg, flipped, k_face):
    """Move the UV seam of the grid just added to acc (closed, nj columns) to vertex column k_face[f] per face (round
    2, NICE 7: seams go to the lamp's back (+Y, away from the path) and into a twist groove, not across the collars
    on the path side). uvg: the (ni, nj+1, 2) UVs the grid was added with."""
    idx, uq, m, sm = acc.faces[-1]
    ni, nj = uvg.shape[0], uvg.shape[1] - 1
    I = np.repeat(np.arange(ni - 1), nj)
    J = np.tile(np.arange(nj), ni - 1)
    ring_c = np.stack([I, I, I + 1, I + 1], 1)
    if flipped:
        ring_c = ring_c[:, ::-1]
    k = np.asarray(k_face, int)
    P = uvg[:, nj, 0] - uvg[:, 0, 0]
    uk = uvg[ring_c, k[:, None], 0]
    add = (J < k)[:, None] * P[ring_c]
    uq = uq.copy()
    uq[..., 0] = uq[..., 0] - uk + add
    acc.faces[-1] = (idx, uq, m, sm)


def column_profile_lo(zs):
    """Lo rings (z, r, zone). zone: 0 base, 1 lower pole, 2 twist, 3 upper pole."""
    c3 = (zs - 0.30, zs + 0.02)
    rings = [(z, r, 0) for z, r in BASE_PROFILE]
    rings += [(2.74, rp(2.74), 1)]                       # straight runs: end rings only (round 2)
    rings += [(z, r, 1) for z, r in collar_rings(*COLLARS[0])]
    nt = 20                                              # round 3: 2 more rings, denser in the end ramps
    for k in range(1, nt):
        u = k / nt
        u = u - 0.2 * math.sin(2 * math.pi * u) / (2 * math.pi)
        z = TWIST["z0"] + (TWIST["z1"] - TWIST["z0"]) * u
        rings.append((z, rp(z), 2))
    rings += [(z, r, 3) for z, r in collar_rings(*COLLARS[1])]
    rings += [(z, r, 3) for z, r in collar_rings(*c3, top=True)]
    rings.append((zs + 0.035, 0.0, 3))
    return rings, c3


def flute_fade(z, zs):
    """1 inside the fluted runs, fading to 0 over 0.1 at the collar edges."""
    c3 = (zs - 0.30, zs + 0.02)
    runs = [(2.64, COLLARS[0][0]), (COLLARS[1][1], c3[0])]
    out = np.zeros_like(np.asarray(z, float))
    for a, b in runs:
        u0 = np.clip((np.asarray(z, float) - a) / 0.18, 0, 1)
        u1 = np.clip((b - np.asarray(z, float)) / 0.18, 0, 1)
        s0 = u0 ** 3 * (u0 * (u0 * 6 - 15) + 10)
        s1 = u1 ** 3 * (u1 * (u1 * 6 - 15) + 10)
        out = np.maximum(out, s0 * s1)
    return out


TW_RAMP = 0.22                  # round 3: the lobes grow out of / sink into the collars over 0.22 (was 0.06)


def twist_amp(z):
    z = np.asarray(z, float)
    u0 = np.clip((z - TWIST["z0"]) / TW_RAMP, 0, 1)
    u1 = np.clip((TWIST["z1"] - z) / TW_RAMP, 0, 1)
    return (u0 ** 3 * (u0 * (u0 * 6 - 15) + 10)) * (u1 ** 3 * (u1 * (u1 * 6 - 15) + 10))


def twist_phi(z):
    return 2 * np.pi * (np.clip(z, TWIST["z0"], TWIST["z1"]) - TWIST["z0"]) / TWIST["pitch"]


def sgnpow(x, p):
    return np.sign(x) * np.abs(x) ** p


def flute_depth(theta):
    """Concave flutes: groove centres at k*30 deg, sharp fillets at 15 + k*30 deg. 1 at the groove centre."""
    u = (np.degrees(theta) % 30.0) / 30.0
    u = np.minimum(u, 1 - u)                     # 0 at the groove centre .. 0.5 at the fillet
    return np.clip(1 - (u / 0.42) ** 2, 0, 1)


def bell_rib(z, theta):
    """Round 2: the bell is a clean round ogee lathe (no raised ribs)."""
    return 0.0 * np.asarray(z, float)


def column_radius(z, theta, r_prof, zs, hi=False):
    """Final radius at (z, theta): profile radius x flutes x twist + bell ribs."""
    z = np.asarray(z, float)
    fd = flute_fade(z, zs)
    amp = twist_amp(z)
    th_t = theta - twist_phi(z)
    tw = TWIST["amp"] * amp * sgnpow(np.cos(4 * th_t), 0.75)
    if hi:
        fl = FLUTE_D * fd * flute_depth(theta)
    else:
        fl = 0.0 * fd                      # round 2: lo pole is round; the flutes are carried by the normal map
    return r_prof * (1 + tw) - fl * (amp < 0.5) + bell_rib(z, theta)


def build_column(zs, hi, at_fn=None):
    """Lo: 24 columns, explicit UV islands per zone. Hi: 384 columns, dense rings + panels / rivets / hammering."""
    rings, c3 = column_profile_lo(zs)
    acc = Acc(attrs=hi)
    if not hi:
        zr_all = np.array([r[0] for r in rings])
        rr_all = np.array([r[1] for r in rings])
        zone_all = np.array([r[2] for r in rings])
        nb = int(np.sum(zone_all == 0))                    # the base rings come first
        # ---- base: a clean 32-sided round lathe (own UV island, 1.6x texel priority)
        nj0 = 32
        th0 = 2 * np.pi * np.arange(nj0) / nj0
        zb_, rb_ = zr_all[1:nb], rr_all[1:nb]
        Gb = np.stack([rb_[:, None] * np.cos(th0)[None, :], rb_[:, None] * np.sin(th0)[None, :],
                       np.repeat(zb_[:, None], nj0, 1)], -1)
        vb = np.concatenate([[0], np.cumsum(np.sqrt(np.diff(zb_) ** 2 + np.diff(rb_) ** 2))])
        uvb = section_uv(Gb[..., :2], vb)
        base_b, fl_b = acc.add_grid(Gb, uvb, centres=np.stack([0 * zb_, 0 * zb_, zb_], 1))
        seam_shift(acc, uvb, fl_b, np.full((len(zb_) - 1) * nj0, nj0 // 4))
        ib, uqb, mb, smb = acc.faces[-1]
        acc.faces[-1] = (ib, uqb * BASE_PRIO + acc.new_island() * 4.0, mb, smb)
        ring0 = base_b + np.arange(nj0)
        cu = np.array([30.0, 0.0])
        uvr = np.stack([0.5 + 0.5 * np.cos(th0), 0.5 + 0.5 * np.sin(th0)], 1) * 1.72 * BASE_PRIO + cu
        acc.add_fan(ring0, (0, 0, zr_all[0]), uvr, np.array([0.5, 0.5]) * 1.72 * BASE_PRIO + cu,
                    outward=np.array([0, 0, -1.0]))
        ringA = base_b + (len(zb_) - 1) * nj0 + np.arange(nj0)
        # ---- pole (+ twist + collars): 24 columns
        zr, rr, zone = zr_all[nb:], rr_all[nb:], zone_all[nb:]
        nj = 24
        base_th = 2 * np.pi * np.arange(nj) / nj
        phi = np.where(zone == 2, twist_phi(zr), np.where(zr >= TWIST["z1"], twist_phi(TWIST["z1"]), 0.0))
        TH = base_th[None, :] + phi[:, None]
        Rg = np.array([column_radius(np.full(nj, zr[i]), base_th, rr[i], zs) for i in range(len(zr))])
        for i in range(len(zr)):
            if zone[i] == 2 or (TWIST["z0"] <= zr[i] <= TWIST["z1"]):
                Rg[i] = column_radius(np.full(nj, zr[i]), TH[i], rr[i], zs)
        G = np.stack([Rg * np.cos(TH), Rg * np.sin(TH), np.repeat(zr[:, None], nj, 1)], -1)
        S = np.stack([Rg * np.cos(base_th)[None, :], Rg * np.sin(base_th)[None, :]], -1)
        dv = np.sqrt(np.diff(zr) ** 2 + np.diff(rr) ** 2)
        v = np.concatenate([[0], np.cumsum(dv)])
        uvg = section_uv(S, v)
        prio = {1: 1.25, 2: 1.2, 3: 1.0}
        rowzone = np.maximum(zone[:-1], zone[1:])
        isl_off = {zz: np.array([5.0 * (zz + 1), 0.0]) for zz in (1, 2, 3)}
        base, flipped = acc.add_grid(G, uvg, centres=np.stack([0 * zr, 0 * zr, zr], 1))
        kz = {1: 6, 2: 3, 3: (6 - int(round(np.degrees(twist_phi(TWIST["z1"])) / 15.0))) % nj}
        seam_shift(acc, uvg, flipped, np.repeat([kz[z] for z in rowzone], nj))
        idx, uq, m, sm = acc.faces[-1]
        rows = np.repeat(np.arange(len(zr) - 1), nj)
        rz = rowzone[rows]
        for zz in (1, 2, 3):
            sel = rz == zz
            if sel.any():
                uq[sel, :, 1] -= uq[sel, :, 1].min()
                uq[sel] = uq[sel] * prio[zz] + isl_off[zz]
        acc.faces[-1] = (idx, uq, m, sm)
        # ---- stitch band 32 -> 24 between the base neck (z 2.64) and the first pole ring (z 2.74)
        ringB = base + np.arange(nj)
        tri, uvt = [], []
        circ = 2 * np.pi * float(rr[0])
        off = acc.new_island() * 4.0 + np.array([0.0, 20.0])
        i = j = 0
        while i < nj0 or j < nj:
            ai, bj = (i + 1) / nj0, (j + 1) / nj
            if j >= nj or (i < nj0 and ai <= bj):
                tri.append([ringA[i % nj0], ringA[(i + 1) % nj0], ringB[j % nj]])
                uvt.append([(i / nj0 * circ, 0.0), ((i + 1) / nj0 * circ, 0.0), (j / nj * circ, 0.1)])
                i += 1
            else:
                tri.append([ringA[i % nj0], ringB[(j + 1) % nj], ringB[j % nj]])
                uvt.append([(i / nj0 * circ, 0.0), ((j + 1) / nj * circ, 0.1), (j / nj * circ, 0.1)])
                j += 1
        tri, uvt = np.array(tri), np.array(uvt)
        a_ = uvt[..., 0] / circ
        lower = a_.mean(1) < 0.25
        uvt[..., 0] = np.where(lower[:, None], a_ - 0.25 + 1.0, a_ - 0.25) * circ
        uvt = uvt * BASE_PRIO + off
        Vv = acc._vcat()
        p0, p1, p2 = Vv[tri[0, 0]], Vv[tri[0, 1]], Vv[tri[0, 2]]
        if np.dot(np.cross(p1 - p0, p2 - p0), np.array([p0[0], p0[1], 0.0])) < 0:
            tri, uvt = tri[:, ::-1], uvt[:, ::-1]
        acc.add_faces(tri, uvt)
        return acc, None
    # ---------------- hi
    hs = RES()["hs"]
    nj = 384 // hs
    theta = 2 * np.pi * np.arange(nj) / nj
    prof = []
    base_dense = catmull([(r, z) for z, r in BASE_PROFILE[1:]], 14 // hs)
    for r, z in base_dense:
        prof.append((z, r))
    zl = [(2.64, 6.06), (8.24, c3[0])]

    def run(a, b, step):
        n = max(2, int((b - a) / step))
        return [(a + (b - a) * k / n) for k in range(1, n + 1)]
    # lower fluted run: dense near the ends (fades), coarse in the middle
    for z in run(2.64, 2.80, 0.008 * hs) + run(2.80, 5.90, 0.03) + run(5.90, 6.06, 0.008 * hs):
        prof.append((z, rp(z)))
    for z0, z1, top in ((COLLARS[0][0], COLLARS[0][1], False),):
        for r, z in catmull([(r, z) for z, r in collar_rings(z0, z1)], 24 // hs)[1:]:
            prof.append((z, r))
    for z in run(TWIST["z0"], TWIST["z1"], 0.006 * hs):
        prof.append((z, rp(z)))
    for r, z in catmull([(r, z) for z, r in collar_rings(*COLLARS[1])], 24 // hs)[1:]:
        prof.append((z, r))
    for z in run(8.24, 8.40, 0.008 * hs) + run(8.40, c3[0] - 0.16, 0.03) + run(c3[0] - 0.16, c3[0], 0.008 * hs):
        prof.append((z, rp(z)))
    for r, z in catmull([(r, z) for z, r in collar_rings(*c3, top=True)], 24 // hs)[1:]:
        prof.append((z, r))
    prof = np.array(prof)
    zr, rr = prof[:, 0], prof[:, 1]
    # collar bead detail: two bead rings + a groove on each collar band (hi only)
    for z0, z1 in COLLARS + [c3]:
        zm = 0.5 * (z0 + z1)
        band = sstep(z0 + 0.05, z0 + 0.07, zr) * (1 - sstep(z1 - 0.07, z1 - 0.05, zr))
        rr = rr + band * (0.010 * np.exp(-((zr - (zm - 0.075)) / 0.012) ** 2) +
                          0.010 * np.exp(-((zr - (zm + 0.075)) / 0.012) ** 2) -
                          0.008 * np.exp(-((zr - zm) / 0.010) ** 2))
    Rg = np.empty((len(zr), nj))
    for i in range(len(zr)):
        Rg[i] = column_radius(np.full(nj, zr[i]), theta, rr[i], zs, hi=True)
    # bell panels: 4 recessed gothic arches (front panel faces -Y) with a raised spider-web relief
    bell = (zr > 0.95) & (zr < 2.05)
    if bell.any():
        for pc in (-np.pi / 2, 0.0, np.pi / 2, np.pi):
            dth = (theta[None, :] - pc + np.pi) % (2 * np.pi) - np.pi
            s = dth * rr[:, None]
            z = zr[:, None]
            w, zsp, Ra, zb0 = 0.20, 1.62, 0.32, 1.06
            ztop = zsp + np.sqrt(np.maximum(Ra ** 2 - (np.abs(s) + (Ra - w)) ** 2, 0))
            inside = (np.abs(s) < w) & (z > zb0) & (z < ztop)
            # signed distance-ish to the panel border
            dside = w - np.abs(s)
            dtop = ztop - z
            dbot = z - zb0
            dmin = np.minimum(np.minimum(dside, dtop), dbot)
            recess = np.where(inside, -0.02 * sstep(0.0, 0.018, dmin), 0.0)
            bead = 0.011 * np.exp(-((dmin + 0.016) / 0.008) ** 2) * (np.abs(s) < w + 0.04) * (z > zb0 - 0.04) * \
                (z < ztop + 0.04)
            # web relief: 8 spokes + 3 polygon rings around the hub (0, 1.46)
            hz = 1.46
            ang = np.arctan2(z - hz, s)
            rad = np.sqrt(s ** 2 + (z - hz) ** 2)
            spoke = np.abs(((ang + np.pi / 8) % (np.pi / 4)) - np.pi / 8) * rad
            webl = np.exp(-(spoke / 0.007) ** 2) * (rad > 0.02)
            angk = ((ang + np.pi / 8) % (np.pi / 4)) - np.pi / 8
            polyr = rad * np.cos(angk)
            for rk in (0.07, 0.14, 0.21, 0.29):
                webl = np.maximum(webl, np.exp(-((polyr - rk) / 0.007) ** 2))
            webl = webl * inside * sstep(0.01, 0.03, dmin)
            Rg[bell] += (recess + bead + 0.009 * webl)[bell]
    # hammered forging: subtle low-frequency dents
    TH = np.repeat(theta[None, :], len(zr), 0)
    X, Y = Rg * np.cos(TH), Rg * np.sin(TH)
    Z = np.repeat(zr[:, None], nj, 1)
    G = np.stack([X, Y, Z], -1)
    flat = G.reshape(-1, 3)
    dent = np.array([noise.noise(Vector(p) * 11.0) for p in flat]).reshape(Rg.shape)
    Rg = Rg * (1 + 0.006 * dent)
    G = np.stack([Rg * np.cos(TH), Rg * np.sin(TH), Z], -1)
    ki, kj, _ = grid_curvature(G)
    conv = blur_grid(np.maximum(np.maximum(ki, kj), 0), it=1)
    conc = blur_grid(np.maximum(np.maximum(-ki, -kj), 0), it=1)
    # explicit wear: twist crests + flute fillets; explicit rust: plinth inner corners handled by concavity
    th_t = TH - twist_phi(Z)
    crest = sstep(0.55, 0.92, np.cos(4 * th_t)) * twist_amp(Z)
    fil = sstep(0.75, 1.0, 1 - flute_depth(TH)) * flute_fade(Z, zs)
    wear_extra = np.maximum(crest * 0.95, fil * 0.7)
    # round 2: the twist must read as rusty IRON, not copper -> rust only along the deepest groove line
    tw_a = twist_amp(Z)
    groove_t = sstep(0.86, 0.98, -np.cos(4 * th_t)) * tw_a
    rust_extra = groove_t * 0.22
    rust_mask = (1 - 0.8 * tw_a) + 0.8 * tw_a * groove_t
    rivets = column_rivets(zs)
    if rivets:
        RV = np.array([p for p, n, r in rivets])
        # rust ring around each rivet + a short streak running down from it
        for p, n, r in rivets:
            d = np.linalg.norm(G - p, axis=2)
            ring = np.exp(-((d - r * 1.25) / (r * 0.45)) ** 2)
            dz = p[2] - G[..., 2]
            lat = np.linalg.norm((G - p)[..., :2] - ((G - p)[..., :2] * 0), axis=2)
            streak = np.exp(-((np.linalg.norm(G[..., :2] - p[:2], axis=2)) / 0.03) ** 2) * \
                sstep(0.0, 0.03, dz) * np.exp(-np.maximum(dz, 0) / 0.18)
            rust_extra = np.maximum(rust_extra, 0.75 * ring + 0.5 * streak)
    conc_eff = conc * (1 - 0.6 * tw_a)                   # the twist grooves are not crevices: keep them iron-dark only
    col, rough, wear = iron_shade(G.reshape(-1, 3), conv.ravel(), conc_eff.ravel(), seed=1,
                                  wear_extra=wear_extra.ravel(), rust_extra=rust_extra.ravel(),
                                  rust_mask=np.maximum(rust_mask, (rust_extra > 0.3) * 1.0).ravel())
    col = col * (1 + 0.20 * tw_a.ravel())[:, None]        # twist albedo ~ the plain pole iron (AO darkens grooves)
    at = {"Col": col.reshape(G.shape), "Rough": rough.reshape(G.shape), "Wear": wear.reshape(G.shape)}
    uvg = np.zeros((len(zr), nj + 1, 2))
    base, flipped = acc.add_grid(G, uvg, at=at, centres=np.stack([0 * zr, 0 * zr, zr], 1))
    ring0 = base + np.arange(nj)
    acc.add_fan(ring0, (0, 0, zr[0]), np.zeros((nj, 2)), np.zeros(2),
                at_c={"Col": col[:1], "Rough": rough[:1], "Wear": wear[:1]}, outward=np.array([0, 0, -1.0]))
    last = base + (len(zr) - 1) * nj + np.arange(nj)
    acc.add_fan(last, (0, 0, zs + 0.035), np.zeros((nj, 2)), np.zeros(2),
                at_c={"Col": col[:1], "Rough": rough[:1], "Wear": wear[:1]}, outward=np.array([0, 0, 1.0]))
    return acc, rivets


def column_rivets(zs):
    """(position, outward normal, radius) of the hi rivet heads on the column."""
    out = []
    c3 = (zs - 0.30, zs + 0.02)
    for z0, z1 in COLLARS + [c3]:
        zm = 0.5 * (z0 + z1)
        r = rp(zm) + 0.072
        for k in range(8):
            a = math.radians(22.5 + 45 * k)
            n = np.array([math.cos(a), math.sin(a), 0.0])
            out.append((np.array([0, 0, zm]) + n * r, n, 0.032))
    for k in range(8):
        a = math.radians(45 * k)
        n = np.array([math.cos(a), math.sin(a), 0.0])
        out.append((np.array([0, 0, 2.385]) + n * 0.492, n, 0.03))
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        n = np.array([math.cos(a), math.sin(a), 0.0])
        out.append((np.array([0, 0, 0.305]) + n * 0.968, n, 0.032))
    return out


def rivet_acc(rivets, acc, seed=3, sink=0.35):
    """Hi rivet domes as small UV-sphere caps sunk into the surface."""
    nu, nv = 16, 8
    for p, n, r in rivets:
        n = np.asarray(n, float) / np.linalg.norm(n)
        t1 = np.cross(n, [0, 0, 1.0])
        if np.linalg.norm(t1) < 1e-3:
            t1 = np.cross(n, [1.0, 0, 0])
        t1 /= np.linalg.norm(t1)
        t2 = np.cross(n, t1)
        th = np.linspace(0.08, np.pi * 0.62, nv)            # from the top of the dome down below the surface
        ph = 2 * np.pi * np.arange(nu) / nu
        G = (p[None, None, :] + r * (np.cos(th)[:, None, None] - sink) * n[None, None, :] +
             r * np.sin(th)[:, None, None] * (np.cos(ph)[None, :, None] * t1 + np.sin(ph)[None, :, None] * t2))
        flat = G.reshape(-1, 3)
        h = (np.cos(th)[:, None] * np.ones(nu)[None, :]).ravel()
        col, rough, wear = iron_shade(flat, np.full(len(flat), 30.0) * sstep(0.2, 0.8, h),
                                      np.full(len(flat), 0.0), seed=seed)
        at = {"Col": col.reshape(G.shape), "Rough": rough.reshape(G.shape), "Wear": wear.reshape(G.shape)}
        base, fl = acc.add_grid(G, np.zeros((nv, nu + 1, 2)), at=at,
                                centres=np.repeat((p - n * r * 2)[None, :], nv, 0))
        top = base + np.arange(nu)
        acc.add_fan(top, p + n * r * (1 - sink), np.zeros((nu, 2)), np.zeros(2),
                    at_c={"Col": col[:1], "Rough": rough[:1], "Wear": wear[:1]}, outward=n)
    return acc


# ===================================================================== generic shaded sweep (hi) / plain sweep (lo)
def sweep_part(acc, P, Nf, Bf, S, v, hi, closed_j=True, prio=1.0, mat=0, seed=0, wear_extra=None, rust_extra=None,
               flip=None, uv_off=None, centres=None, wear_k=(14.0, 40.0)):
    """Add one swept grid. Lo: explicit UV island (scaled by prio). Hi: curvature-driven iron shading."""
    G = sweep_grid(P, Nf, Bf, S)
    cen = P if centres is None else centres
    if not hi:
        uvg = section_uv(S, v, closed=closed_j) * prio
        off = acc.new_island() if uv_off is None else uv_off
        uvg = uvg + off
        return acc.add_grid(G, uvg, closed_j=closed_j, mat=mat, centres=cen, flip=flip), G
    ki, kj, _ = grid_curvature(G, closed_j=closed_j)
    conv = blur_grid(np.maximum(np.maximum(ki, kj), 0), closed_j=closed_j)
    conc = blur_grid(np.maximum(np.maximum(-ki, -kj), 0), closed_j=closed_j)
    col, rough, wear = iron_shade(G.reshape(-1, 3), conv.ravel(), conc.ravel(), seed=seed,
                                  wear_extra=None if wear_extra is None else np.asarray(wear_extra).ravel(),
                                  rust_extra=None if rust_extra is None else np.asarray(rust_extra).ravel(),
                                  wear_k=wear_k)
    at = {"Col": col.reshape(G.shape), "Rough": rough.reshape(G.shape), "Wear": wear.reshape(G.shape)}
    nj = G.shape[1]
    uvg = np.zeros((G.shape[0], nj + 1 if closed_j else nj, 2))
    return acc.add_grid(G, uvg, at=at, closed_j=closed_j, mat=mat, centres=cen, flip=flip), G


def cap_end(acc, base, ni, nj, idx_ring, centre, outward, hi, G=None):
    ring = base + idx_ring * nj + np.arange(nj)
    uvr = np.zeros((nj, 2)) + acc.new_island() if not hi else np.zeros((nj, 2))
    if hi and G is not None:
        p = G[idx_ring].reshape(-1, 3)[:1]
        col, rough, wear = iron_shade(p, np.zeros(1), np.zeros(1))
        at = {"Col": col, "Rough": rough, "Wear": wear}
    else:
        at = None
    return acc.add_fan(ring, centre, uvr, uvr[0], at_c=at, outward=np.asarray(outward, float))


def ellipsoid_part(acc, c, radii, rot, nu, nv, hi, prio=1.0, mat=0, seed=0, disp=None):
    """Lat-long ellipsoid; rot = 3x3 matrix; disp(theta, phi, p) -> radial scale (hi)."""
    c = np.asarray(c, float)
    th = np.pi * np.arange(1, nv) / nv
    ph = 2 * np.pi * np.arange(nu) / nu
    TH, PH = np.meshgrid(th, ph, indexing="ij")
    loc = np.stack([np.sin(TH) * np.cos(PH) * radii[0], np.sin(TH) * np.sin(PH) * radii[1], np.cos(TH) * radii[2]], -1)
    if disp is not None:
        loc = loc * disp(TH, PH, loc)[..., None]
    G = c + loc @ np.asarray(rot).T
    top, bot = c + np.asarray(rot) @ np.array([0, 0, radii[2]]), c + np.asarray(rot) @ np.array([0, 0, -radii[2]])
    if not hi:
        S = np.stack([np.sin(TH) * radii[0], np.zeros_like(TH)], -1)
        uv = np.stack([PH / (2 * np.pi) * 2 * np.pi * np.mean(radii[:2]), TH * radii[2]], -1)
        uvg = np.concatenate([uv, uv[:, :1] + np.array([2 * np.pi * np.mean(radii[:2]), 0])], 1) * prio + acc.new_island()
        base, fl = acc.add_grid(G, uvg, mat=mat, centres=np.repeat(c[None, :], nv - 1, 0))
        acc.add_fan(base + np.arange(nu), top, uvg[0, :nu], uvg[0, 0] - np.array([0, radii[2] * 0.3 * prio]),
                    outward=top - c)
        acc.add_fan(base + (nv - 2) * nu + np.arange(nu), bot, uvg[-1, :nu], uvg[-1, 0] + np.array([0, 0.1 * prio]),
                    outward=bot - c)
        return G
    ki, kj, _ = grid_curvature(G)
    conv = blur_grid(np.maximum(np.maximum(ki, kj), 0))
    conc = blur_grid(np.maximum(np.maximum(-ki, -kj), 0))
    col, rough, wear = iron_shade(G.reshape(-1, 3), conv.ravel(), conc.ravel(), seed=seed)
    at = {"Col": col.reshape(G.shape), "Rough": rough.reshape(G.shape), "Wear": wear.reshape(G.shape)}
    base, fl = acc.add_grid(G, np.zeros((nv - 1, nu + 1, 2)), at=at, mat=mat, centres=np.repeat(c[None, :], nv - 1, 0))
    a1 = {"Col": col[:1], "Rough": rough[:1], "Wear": wear[:1]}
    acc.add_fan(base + np.arange(nu), top, np.zeros((nu, 2)), np.zeros(2), at_c=a1, outward=top - c)
    acc.add_fan(base + (nv - 2) * nu + np.arange(nu), bot, np.zeros((nu, 2)), np.zeros(2), at_c=a1, outward=bot - c)
    return G


# ===================================================================== crook + knob
def crook_path3d(cv):
    """Dense 3D centreline (with the 0.32 lead-in inside collar 3) + arc length (0 at the crook start)."""
    y, z = -cv["y"], cv["z"]
    zs = cv["zs"]
    lead = np.linspace(zs - 0.32, zs, 33)[:-1]
    P = np.concatenate([np.stack([0 * lead, 0 * lead, lead], 1), np.stack([0 * y, y, z], 1)])
    Rloc = np.concatenate([np.full(len(lead), 1e6), cv["R"]])
    s = np.concatenate([lead - zs, cv["s"]])
    return P, Rloc, s


def build_crook(cv, hi):
    acc = Acc(attrs=hi)
    P, Rloc, s = crook_path3d(cv)
    sb = cv["s"][cv["idn"]] - 0.30
    if hi:
        idx = np.arange(0, len(P), 4 * RES()["hs"])
        if idx[-1] != len(P) - 1:
            idx = np.append(idx, len(P) - 1)
        nj = 64 // RES()["hs"]
    else:
        idx = adaptive_samples(P, Rloc, sag=0.0065, max_len=0.38,
                               extra=tuple(e - s[0] for e in (sb - 0.06, sb - 0.03, sb, sb + 0.03, sb + 0.06, 0.0)))
        nj = 12
    Ps, ss = P[idx], s[idx]
    T, N, B = frames_planar(Ps, (1.0, 0.0, 0.0))
    # seam on the outer side of the curve: outer = +B or -B; the crook always turns the same way
    K = np.gradient(T, axis=0)
    sign = -np.sign(np.sum(np.einsum("ij,ij->i", K, B)))   # outer side = -curvature direction
    r = crook_radius(cv, ss)
    a = np.pi / 2 * sign + 2 * np.pi * np.arange(nj) / nj
    S = np.stack([r[:, None] * np.cos(a)[None, :], r[:, None] * np.sin(a)[None, :]], -1)
    if hi:
        # hammered bar: low-frequency dents + flattened forge facets
        dent = np.array([[noise.noise(Vector((ss[i] * 9.0, math.cos(aj) * 1.7, math.sin(aj) * 1.7)))
                          for aj in a] for i in range(len(ss))])
        S = S * (1 + 0.012 * dent)[..., None]
    (base, fl), G = sweep_part(acc, Ps, N, B, S, ss - ss[0], hi, prio=0.9, seed=5)
    # end: cap + ball knob
    end, tang = Ps[-1], T[-1]
    cap_end(acc, base, len(Ps), nj, len(Ps) - 1, end + tang * r[-1] * 0.4, tang, hi, G)
    kc = end + tang * 0.035
    kr = 0.088
    if hi:
        ellipsoid_part(acc, kc, (kr, kr, kr), np.eye(3), 48 // RES()["hs"], 24 // RES()["hs"], True, seed=6)
    else:
        ellipsoid_part(acc, kc, (kr, kr, kr), np.eye(3), 10, 6, False, prio=0.9)
    return acc, dict(P=P, s=s, end=end, knob=kc)


# ===================================================================== volute in the bend
VOLUTE_CACHE = os.path.join(OUT, "volute_cache.json")


def volute_curve(cv, n=900):
    """Log-spiral scroll nested in the bend; the centre / start radius are solved so that the outer coil touches the
    crook's inner side near the pole (cached in volute_cache.json)."""
    A_tot, r_end, beta0 = np.radians(600.0), 0.12, np.radians(186.0)
    key = json.dumps(CROOK, sort_keys=True)
    if os.path.exists(VOLUTE_CACHE):
        with open(VOLUTE_CACHE) as fh:
            cache = json.load(fh)
        if cache.get("key") == key:
            Cy, Cz, rho0 = cache["Cy"], cache["Cz"], cache["rho0"]
            k = math.log(rho0 / r_end) / A_tot
            al = np.linspace(0, A_tot, n)
            rho = rho0 * np.exp(-k * al)
            return dict(y=Cy + rho * np.cos(beta0 - al), z=Cz + rho * np.sin(beta0 - al), C=(Cy, Cz), rho0=rho0,
                        gaps=tuple(cache["gaps"]), rho=rho, al=al)
    P, Rloc, s = crook_path3d(cv)
    yq, zq = -P[:, 1], P[:, 2]
    sel = (yq < 1.9) & (zq > cv["zs"] - 0.05)
    cy, cz = yq[sel][::4], zq[sel][::4]
    cr = crook_radius(cv, s[sel][::4])
    zs = cv["zs"]
    th_half = 0.0375
    A_tot = np.radians(600.0)
    r_end = 0.12
    beta0 = np.radians(186.0)
    best = None
    for Cy in np.linspace(0.55, 1.35, 33):
        for Cz in np.linspace(cv["zs"] + 0.30, cv["zs"] + 1.30, 41):
            for rho0 in np.linspace(0.40, 0.90, 26):
                k = math.log(rho0 / r_end) / A_tot
                al = np.linspace(0, np.radians(230.0), 70)
                rho = rho0 * np.exp(-k * al)
                py = Cy + rho * np.cos(beta0 - al)
                pz = Cz + rho * np.sin(beta0 - al)
                d = np.sqrt((py[:, None] - cy[None, :]) ** 2 + (pz[:, None] - cz[None, :]) ** 2) - cr[None, :]
                g = d.min(1) - th_half
                if g.min() < 0.002:
                    continue
                low = pz < zs + 0.06
                if np.any(py[low] < 0.34):
                    continue
                if np.any(py > 1.55):                      # keep the web's area under the arc free
                    continue
                g_start = g[0]
                g_top = g[(al > np.radians(60)) & (al < np.radians(150))].min()
                if g_start > 0.025:
                    continue
                score = -rho0 + 2.0 * g_start + 1.5 * g_top
                if best is None or score < best[0]:
                    best = (score, Cy, Cz, rho0, float(g.min()), float(g_start), float(g_top))
    if best is None:
        raise RuntimeError("volute: no placement touches the crook")
    _, Cy, Cz, rho0, gmin, g0, gmid = best
    with open(VOLUTE_CACHE, "w") as fh:
        json.dump(dict(key=key, Cy=float(Cy), Cz=float(Cz), rho0=float(rho0),
                       gaps=[round(gmin, 4), round(g0, 4), round(gmid, 4)]), fh)
    k = math.log(rho0 / r_end) / A_tot
    al = np.linspace(0, A_tot, n)
    rho = rho0 * np.exp(-k * al)
    py = Cy + rho * np.cos(beta0 - al)
    pz = Cz + rho * np.sin(beta0 - al)
    return dict(y=py, z=pz, C=(Cy, Cz), rho0=rho0, gaps=(round(gmin, 4), round(g0, 4), round(gmid, 4)),
                rho=rho, al=al)


def build_volute(vc, hi):
    acc = Acc(attrs=hi)
    P2 = np.stack([vc["y"], vc["z"]], 1)
    P = np.stack([0 * P2[:, 0], -P2[:, 0], P2[:, 1]], 1)
    Rl = polyline_curv_radius(P, k=4)
    if hi:
        idx = np.arange(0, len(P), 1)
        sec = rrect(0.11, 0.075, n_corner=6, cr=0.02)
    else:
        idx = adaptive_samples(P, Rl, sag=0.0045, max_len=0.28)
        sec = np.array([(0.055, 0.0), (0.035, 0.0375), (-0.035, 0.0375), (-0.055, 0.0), (-0.035, -0.0375),
                        (0.035, -0.0375)])
    Ps = P[idx]
    T, N, B = frames_planar(Ps, (1.0, 0.0, 0.0))
    d = np.linalg.norm(np.diff(Ps, axis=0), axis=1)
    v = np.concatenate([[0], np.cumsum(d)])
    S = np.repeat(sec[None, :, :], len(Ps), 0)
    # thin the scroll end a little
    S = S * (1 - 0.25 * sstep(0.7, 1.0, v / v[-1]))[:, None, None]
    (base, fl), G = sweep_part(acc, Ps, N, B, S, v, hi, prio=0.9, seed=7, wear_k=(25.0, 60.0))
    nj = S.shape[1]
    cap_end(acc, base, len(Ps), nj, 0, Ps[0] - T[0] * 0.01, -T[0], hi, G)
    cap_end(acc, base, len(Ps), nj, len(Ps) - 1, Ps[-1] + T[-1] * 0.02, T[-1], hi, G)
    return acc


# ===================================================================== claw feet
FOOT_LEG = [(0.62, 0.33), (0.80, 0.325), (0.94, 0.300), (1.03, 0.245), (1.085, 0.170), (1.115, 0.110), (1.135, 0.075)]


def build_feet(hi):
    acc = Acc(attrs=hi)
    hs = RES()["hs"]
    for kf in range(4):
        az = math.radians(45 + 90 * kf)
        dvec = np.array([math.cos(az), math.sin(az), 0.0])
        side = np.array([-math.sin(az), math.cos(az), 0.0])
        pts2 = catmull(FOOT_LEG, 12 if hi else 3)
        P = np.array([dvec * rho + np.array([0, 0, z]) for rho, z in pts2])
        if not hi:
            P, _ = resample_poly(P, n=5)
        T, N, B = frames_planar(P, side)
        t = np.linspace(0, 1, len(P))
        r = np.interp(t, [0, 0.35, 0.55, 1.0], [0.128, 0.142, 0.118, 0.088])
        nj = (48 // hs) if hi else 8
        a = 2 * np.pi * np.arange(nj) / nj
        S = np.stack([r[:, None] * np.cos(a)[None, :], r[:, None] * np.sin(a)[None, :]], -1)
        wear_extra = None
        if hi:
            # knee scroll relief: a raised curl on the top of the knee + knuckle rings at the ankle
            A, Tt = np.meshgrid(a, t)
            top = np.cos(A - np.pi / 2 * 0)                  # +N side = up-ish? use the B axis (in-plane) below
            curl = np.exp(-((Tt - 0.38) / 0.06) ** 2) * sstep(0.3, 0.9, np.sin(A))
            spiral = np.exp(-((((A * 0.5 + Tt * 18.0) % 1.0) - 0.5) / 0.12) ** 2) * curl
            knuck = np.exp(-((Tt - 0.82) / 0.025) ** 2) * 0.06
            S = S * (1 + 0.10 * spiral + knuck)[..., None]
            wear_extra = 0.6 * spiral
        (base, fl), G = sweep_part(acc, P, N, B, S, np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0),
                                                                                           axis=1))]),
                                   hi, prio=1.25, seed=10 + kf, wear_extra=wear_extra)
        # paw blob
        paw = dvec * 1.17 + np.array([0, 0, 0.062])
        rot = np.stack([dvec, side, np.array([0, 0, 1.0])], 1)
        if hi:
            def bump(TH, PH, loc):
                return 1 + 0.06 * np.cos(3 * (PH - 0.0)) * np.sin(TH) ** 2
            ellipsoid_part(acc, paw, (0.15, 0.13, 0.072), rot, 48 // hs, 24 // hs, True, seed=20 + kf, disp=bump)
        else:
            ellipsoid_part(acc, paw, (0.15, 0.13, 0.072), rot, 8, 4, False, prio=1.25)
        # 3 toes with hooked talons
        for kt, dang in enumerate((-20.0, 0.0, 20.0)):
            ta = az + math.radians(dang)
            td = np.array([math.cos(ta), math.sin(ta), 0.0])
            tside = np.array([-math.sin(ta), math.cos(ta), 0.0])
            ctrl = [paw + td * 0.05 + np.array([0, 0, 0.012]), paw + td * 0.15 + np.array([0, 0, 0.002]),
                    paw + td * 0.215 - np.array([0, 0, 0.028]), paw + td * 0.255 - np.array([0, 0, 0.062])]
            Pt = catmull(ctrl, 10 if hi else 1)
            if not hi:
                Pt = np.array(ctrl)
            tt = np.linspace(0, 1, len(Pt))
            rt = np.interp(tt, [0, 0.5, 0.8, 1.0], [0.048, 0.042, 0.028, 0.007])
            Tt_, Nt, Bt = frames_planar(Pt, tside)
            njt = (24 // hs) if hi else 4
            at_ = 2 * np.pi * np.arange(njt) / njt
            St = np.stack([rt[:, None] * np.cos(at_)[None, :], rt[:, None] * np.sin(at_)[None, :]], -1)
            if hi:
                TT, AA = np.meshgrid(tt, at_, indexing="ij")
                St = St * (1 + 0.12 * np.exp(-((TT - 0.45) / 0.05) ** 2))[..., None]
            (bt, flt), Gt = sweep_part(acc, Pt, Nt, Bt, St,
                                       np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(Pt, axis=0), axis=1))]),
                                       hi, prio=1.25, seed=30 + kf * 3 + kt, wear_k=(20.0, 70.0))
            cap_end(acc, bt, len(Pt), njt, len(Pt) - 1, Pt[-1] + Tt_[-1] * 0.008, Tt_[-1], hi, Gt)
    return acc


# ===================================================================== bat ornament
def bat_frame(cv):
    ia = cv["ia"]
    ya, za = -cv["y"][ia], cv["z"][ia]
    ra = float(crook_radius(cv, cv["s"][ia]))
    return np.array([0.0, ya, za + ra]), ra


def wing_outline(n_curve):
    """2D wing outline (u outward along the span, v up), jagged finger tips with concave scallops."""
    S0, W, Th = (0.0, 0.03), (0.45, 0.21), (0.485, 0.315)
    T1, T2, T3, T4, B0 = (0.97, 0.17), (0.90, -0.07), (0.71, -0.34), (0.42, -0.47), (0.02, -0.24)

    def qb(a, c, b):
        return quad_bezier(a, c, b, n_curve)
    pts = chain(qb(S0, (0.22, 0.17), W), qb(W, (0.47, 0.27), Th), qb(Th, (0.50, 0.24), (0.53, 0.225)),
                qb((0.53, 0.225), (0.76, 0.27), T1), qb(T1, (0.74, 0.06), T2), qb(T2, (0.62, -0.12), T3),
                qb(T3, (0.48, -0.25), T4), qb(T4, (0.22, -0.27), B0), qb(B0, (-0.03, -0.08), S0))
    return [(u * 1.08, v * 1.08) for u, v in pts], dict(W=W, T=[T1, T2, T3, T4], S0=S0)


def wing_map(sgn, origin):
    """2D wing (u, v) -> 3D. sgn = +1 wing toward -Y (the arm), -1 toward +Y. Dihedral 15 deg, sweep 12 deg (+X)."""
    dh, sw = math.radians(15.0), math.radians(12.0)
    D = np.array([math.sin(sw) * math.cos(dh), -sgn * math.cos(sw) * math.cos(dh), math.sin(dh)])
    Z = np.array([0, 0, 1.0])
    V = Z - D * D.dot(Z)
    V /= np.linalg.norm(V)
    n = np.cross(D, V)
    if n[0] < 0:
        n = -n                                              # n points to the bat's front (+X)
    S = origin + np.array([0.0, -sgn * 0.085, 0.33])

    def f(u, v, w=0.0):
        u, v = np.asarray(u, float), np.asarray(v, float)
        camber = -0.035 * np.sin(np.pi * np.clip(u / 1.05, 0, 1)) * sstep(0.25, -0.3, v)
        return S[None, :] + u[:, None] * D[None, :] + v[:, None] * V[None, :] + (camber + w)[:, None] * n[None, :]
    return f, n


def build_bat(cv, hi):
    acc = Acc(attrs=hi)
    O, ra = bat_frame(cv)
    hs = RES()["hs"]
    for sgn in (1, -1):
        outline, keyp = wing_outline(14 if hi else 3)
        outline = clean(outline)
        f, n = wing_map(sgn, O)
        Wk = np.array(keyp["W"]) * 1.08
        tips = [np.array(t) * 1.08 for t in keyp["T"]]
        S0 = np.array(keyp["S0"]) * 1.08
        if not hi:
            uv2 = np.array(outline)
            tri = geometry.tessellate_polygon([[Vector((p[0], p[1], 0)) for p in outline]])
            front = f(uv2[:, 0], uv2[:, 1], 0.025)
            back = f(uv2[:, 0], uv2[:, 1], -0.025)
            k = len(outline)
            V = np.vstack([front, back])
            F, UV = [], []
            off = acc.new_island()
            off2 = acc.new_island()
            for t in tri:
                F.append([t[0], t[1], t[2]])
                UV.append([uv2[t[0]] * 1.3 + off, uv2[t[1]] * 1.3 + off, uv2[t[2]] * 1.3 + off])
                F.append([k + t[2], k + t[1], k + t[0]])
                UV.append([uv2[t[2]] * 1.3 + off2, uv2[t[1]] * 1.3 + off2, uv2[t[0]] * 1.3 + off2])
            # rim strip
            per = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(np.vstack([uv2, uv2[:1]]), axis=0), axis=1))])
            off3 = acc.new_island()
            for i in range(k):
                j = (i + 1) % k
                F.append([i, j, k + j, k + i])
                UV.append([np.array([per[i], 0.0]) * 1.3 + off3, np.array([per[i + 1], 0.0]) * 1.3 + off3,
                           np.array([per[i + 1], 0.07]) * 1.3 + off3, np.array([per[i], 0.07]) * 1.3 + off3])
            # orientation: front faces must point along +n
            p0, p1, p2 = V[F[0][0]], V[F[0][1]], V[F[0][2]]
            if np.dot(np.cross(p1 - p0, p2 - p0), n) < 0:
                F = [list(reversed(fc)) for fc in F]
                UV = [list(reversed(u)) for u in UV]
            acc.merge_mesh(V, F, UV, smooth=True)
            continue
    return acc


def _inside(poly, pts):
    """Even-odd point-in-polygon test (numpy)."""
    x, y = pts[:, 0], pts[:, 1]
    inside = np.zeros(len(pts), bool)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        cond = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / ((y2 - y1) + 1e-12) + x1)
        inside ^= cond
    return inside


def _seg_dist(pts, a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ab = b - a
    t = np.clip(((pts - a) @ ab) / max(ab @ ab, 1e-12), 0, 1)
    return np.linalg.norm(pts - (a + t[:, None] * ab), axis=1), t


def bat_foot_path(O, ra, sy, n=8):
    y0 = 0.055 * sy
    pts = [O + np.array([0.0, y0, 0.11])]
    for ang in np.radians([95, 80, 62, 42, 22]):
        pts.append(O + np.array([0.0, y0, -ra]) + (ra + 0.022) * np.array([math.cos(ang), 0, math.sin(ang)]))
    return catmull([tuple(p) for p in pts], n)


def build_bat_hi(cv):
    acc = Acc(attrs=True)
    O, ra = bat_frame(cv)
    hs = RES()["hs"]
    for sgn in (1, -1):
        outline, keyp = wing_outline(40 // hs)
        outline = clean(outline, 1e-4)
        poly = np.array(outline)
        f, n = wing_map(sgn, O)
        Wk = np.array(keyp["W"]) * 1.08
        tips = [np.array(t) * 1.08 for t in keyp["T"]]
        S0 = np.array(keyp["S0"]) * 1.08
        step = 0.012 * hs
        mn, mx = poly.min(0), poly.max(0)
        gx, gy = np.meshgrid(np.arange(mn[0] + step / 2, mx[0], step), np.arange(mn[1] + step / 2, mx[1], step))
        cand = np.stack([gx.ravel(), gy.ravel()], 1)
        cand = cand[_inside(poly, cand)]
        # keep interior points away from the outline
        dmin = np.full(len(cand), 9.0)
        for i in range(len(poly)):
            d, _ = _seg_dist(cand, poly[i], poly[(i + 1) % len(poly)])
            dmin = np.minimum(dmin, d)
        cand = cand[dmin > step * 0.6]
        verts = [Vector((p[0], p[1])) for p in np.vstack([poly, cand])]
        kp = len(poly)
        edges = [(i, (i + 1) % kp) for i in range(kp)]
        res = geometry.delaunay_2d_cdt(verts, edges, [], 2, 1e-7)
        vo, eo, fo = res[0], res[1], res[2]
        uv2 = np.array([[v.x, v.y] for v in vo])
        tris = [list(fc) for fc in fo]
        # ridges: arm bone S0 -> W, fingers W -> tips; thickness swells along them
        ridge = np.zeros(len(uv2))
        d, _ = _seg_dist(uv2, S0 + np.array([0.0, 0.0]), Wk)
        ridge = np.maximum(ridge, 1.6 * np.exp(-(d / 0.028) ** 2))
        for tp in tips:
            d, t = _seg_dist(uv2, Wk, tp)
            ridge = np.maximum(ridge, np.exp(-(d / (0.018 * (1.2 - 0.6 * t))) ** 2) * (1 - 0.5 * t))
        # membrane wrinkles running from the body toward the trailing edge
        wr = np.array([noise.noise(Vector((p[0] * 14.0, p[1] * 4.0, sgn * 3.0))) for p in uv2])
        # distance to the outline for the rim rounding
        dout = np.full(len(uv2), 9.0)
        for i in range(len(poly)):
            dd, _ = _seg_dist(uv2, poly[i], poly[(i + 1) % len(poly)])
            dout = np.minimum(dout, dd)
        rim = np.sqrt(np.clip(1 - (1 - np.clip(dout / 0.025, 0, 1)) ** 2, 0, 1))
        half = (0.022 + 0.022 * ridge) * rim + 0.003 * wr * (ridge < 0.3)
        front = f(uv2[:, 0], uv2[:, 1], half)
        back = f(uv2[:, 0], uv2[:, 1], -half)
        k = len(uv2)
        V = np.vstack([front, back])
        F = [[t[0], t[1], t[2]] for t in tris] + [[k + t[2], k + t[1], k + t[0]] for t in tris]
        p0, p1, p2 = V[F[0][0]], V[F[0][1]], V[F[0][2]]
        if np.dot(np.cross(p1 - p0, p2 - p0), n) < 0:
            F = [list(reversed(fc)) for fc in F]
        # shading: wear on ridges + rim, crevices beside the ridges
        conv = np.concatenate([30 * ridge + 40 * (1 - rim), 30 * ridge + 40 * (1 - rim)])
        conc = np.concatenate([18 * np.exp(-((ridge - 0.35) / 0.2) ** 2)] * 2)
        col, rough, wear = iron_shade(V, conv, conc, seed=40 + sgn)
        acc.merge_mesh(V, F, [[(0, 0)] * 3] * len(F), at={"Col": col, "Rough": rough, "Wear": wear})
    # body, head, ears, feet
    tilt = Matrix.Rotation(math.radians(12.0), 3, "Y")
    rotB = np.array(tilt)
    body_c = O + np.array([0.015, 0.0, 0.205])

    def body_disp(TH, PH, loc):
        chest = 0.05 * np.exp(-((PH - 0.0) / 0.7) ** 2) * np.sin(TH) ** 3
        ribs = 0.015 * np.cos(9 * TH) * np.exp(-((PH - 0.0) / 0.9) ** 2)
        fur = 0.012 * np.sin(23 * TH + 5 * PH)
        return 1 + chest + ribs + fur
    ellipsoid_part(acc, body_c, (0.10, 0.118, 0.205), rotB, 96 // hs, 64 // hs, True, seed=50, disp=body_disp)
    head_c = O + np.array([0.075, 0.0, 0.435])
    rotH = np.array(Matrix.Rotation(math.radians(-30.0), 3, "Y") @ Matrix.Rotation(math.radians(0.0), 3, "Z"))

    def head_disp(TH, PH, loc):
        # muzzle toward +X (phi = 0), brow ridge, eye sockets
        muzzle = 0.30 * np.exp(-((PH) / 0.45) ** 2) * np.exp(-((TH - 1.75) / 0.35) ** 2)
        brow = 0.10 * np.exp(-((PH) / 0.9) ** 2) * np.exp(-((TH - 1.15) / 0.12) ** 2)
        eyes = -0.12 * (np.exp(-(((PH - 0.55) / 0.16) ** 2 + ((TH - 1.32) / 0.13) ** 2)) +
                        np.exp(-(((PH + 0.55) / 0.16) ** 2 + ((TH - 1.32) / 0.13) ** 2)))
        snarl = 0.03 * np.sin(18 * PH) * np.exp(-((PH) / 0.4) ** 2) * np.exp(-((TH - 1.6) / 0.15) ** 2)
        return 1 + muzzle + brow + eyes + snarl
    ellipsoid_part(acc, head_c, (0.088, 0.08, 0.076), rotH, 96 // hs, 64 // hs, True, seed=51, disp=head_disp)
    # fangs: two small cones under the muzzle
    for sy in (-1, 1):
        base = head_c + np.array([0.12, 0.022 * sy, -0.035])
        tip = base + np.array([0.01, 0.0, -0.05])
        Pf = np.stack([base + (tip - base) * t for t in np.linspace(0, 1, 6)])
        T, N, B = frames_transport(Pf)
        rf = np.linspace(0.012, 0.001, 6)
        a = 2 * np.pi * np.arange(12) / 12
        S = np.stack([rf[:, None] * np.cos(a)[None, :], rf[:, None] * np.sin(a)[None, :]], -1)
        sweep_part(acc, Pf, N, B, S, np.linspace(0, 0.05, 6), True, seed=52)
    # ears: tall pointed, slightly cupped
    for sy in (-1, 1):
        eb = head_c + np.array([-0.012, 0.042 * sy, 0.055])
        et = head_c + np.array([-0.035, 0.088 * sy, 0.235])
        Pe = np.stack([eb + (et - eb) * t for t in np.linspace(0, 1, 30)])
        T, N, B = frames_transport(Pe, ref=(1, 0, 0))
        te = np.linspace(0, 1, 30)
        re = 0.036 * (1 - te) ** 0.8 + 0.002
        a = 2 * np.pi * np.arange(32) / 32
        S = np.stack([re[:, None] * np.cos(a)[None, :] * 0.45, re[:, None] * np.sin(a)[None, :]], -1)
        cup = -0.35 * np.exp(-((a - 0.0) / 0.9) ** 2)
        S[..., 0] = S[..., 0] * (1 + cup[None, :])
        sweep_part(acc, Pe, N, B, S, np.linspace(0, 0.2, 30), True, seed=53)
    # feet: two hooked feet side by side gripping the bar (toes curl over its +X side)
    for sy in (-1, 1):
        Pfoot = bat_foot_path(O, ra, sy)
        T, N, B = frames_transport(Pfoot)
        tf = np.linspace(0, 1, len(Pfoot))
        rf = np.interp(tf, [0, 0.25, 1.0], [0.032, 0.024, 0.008])
        a = 2 * np.pi * np.arange(16) / 16
        S = np.stack([rf[:, None] * np.cos(a)[None, :], rf[:, None] * np.sin(a)[None, :]], -1)
        sweep_part(acc, Pfoot, N, B, S, np.linspace(0, 0.3, len(Pfoot)), True, seed=54, wear_k=(25, 60))
    return acc


def build_bat_lo(cv):
    acc = build_bat(cv, False)
    O, ra = bat_frame(cv)
    ellipsoid_part(acc, O + np.array([0.015, 0.0, 0.205]), (0.10, 0.118, 0.205),
                   np.array(Matrix.Rotation(math.radians(12.0), 3, "Y")), 10, 6, False, prio=1.3)
    rotH = np.array(Matrix.Rotation(math.radians(-30.0), 3, "Y"))
    head_c = O + np.array([0.075, 0.0, 0.435])
    ellipsoid_part(acc, head_c + np.array([0.012, 0, -0.006]), (0.10, 0.08, 0.078), rotH, 8, 5, False, prio=1.3)
    for sy in (-1, 1):
        eb = head_c + np.array([-0.012, 0.042 * sy, 0.055])
        et = head_c + np.array([-0.035, 0.088 * sy, 0.235])
        Pe = np.stack([eb, et])
        T, N, B = frames_transport(Pe, ref=(1, 0, 0))
        a = 2 * np.pi * np.arange(5) / 5
        S = np.stack([np.array([0.036, 0.004])[:, None] * np.cos(a)[None, :] * 0.5,
                      np.array([0.036, 0.004])[:, None] * np.sin(a)[None, :]], -1)
        (b, fl), G = sweep_part(acc, Pe, N, B, S, np.array([0, 0.2]), False, prio=1.3)
        cap_end(acc, b, 2, 5, 1, et + (et - eb) * 0.05, et - eb, False)
    for sy in (-1, 1):
        Pd = bat_foot_path(O, ra, sy)
        Pfoot = Pd[np.linspace(0, len(Pd) - 1, 4).astype(int)]
        T, N, B = frames_transport(Pfoot)
        rf = np.array([0.032, 0.026, 0.018, 0.008])
        a = 2 * np.pi * np.arange(5) / 5
        S = np.stack([rf[:, None] * np.cos(a)[None, :], rf[:, None] * np.sin(a)[None, :]], -1)
        (b, fl), G = sweep_part(acc, Pfoot, N, B, S, np.linspace(0, 0.3, 4), False, prio=1.3)
        cap_end(acc, b, 4, 5, 3, Pfoot[-1] + T[-1] * 0.008, T[-1], False)
    return acc


# ===================================================================== the pumpkin (eggs pipeline)
def face_lamp():
    """Bold face for 40-stud reads (viewer coords, studs, from the pumpkin centre): slanted scowling triangle eyes
    0.66 wide, a 0.32 nose, a 1.91-wide grin open 0.50 at the centre with 2 + 2 teeth >= 0.24 wide."""
    eye = chain(quad_bezier((0.18, 0.26), (0.52, 0.405), (0.84, 0.52), 5),
                quad_bezier((0.84, 0.52), (0.77, 0.24), (0.60, 0.04), 4),
                quad_bezier((0.60, 0.04), (0.36, 0.12), (0.18, 0.26), 4))
    nose = chain(quad_bezier((0.0, 0.20), (-0.09, 0.07), (-0.16, -0.07), 3),
                 quad_bezier((-0.16, -0.07), (0.0, -0.10), (0.16, -0.07), 3),
                 quad_bezier((0.16, -0.07), (0.09, 0.07), (0.0, 0.20), 3))
    mouth = grin(0.90, (-0.20, 0.12), (-0.70, 0.36),
                 top_teeth=[(-0.30, 0.26, 0.14, 0.20), (0.30, 0.26, 0.14, 0.20)],
                 bot_teeth=[(-0.62, 0.24, 0.12, 0.16), (0.62, 0.24, 0.12, 0.16)],
                 corner_up=0.10, step=0.085, jit=0.008, seed=21)
    return {"EyeR": eye, "EyeL": mirror(eye), "Nose": nose, "Mouth": mouth}


CANDLE_K = dict(pos=(0.0, 0.0), H=1.05, R=0.44, seed=12, wax=(206, 142, 64), notches=[(1.2, 0.10, 0.3)], extra=4)
CANDLE_SCALE = 0.38


RIND_COL = (120, 45, 10)
RIND_W = (0.028, 0.042)          # dark rind band on the skin side of every outer knife edge (round 2, MUST 1c)


def rim_distance_attr(ob, skin=0, wall=2, step=0.004):
    """Per-vertex distance (studs) to the nearest OUTER knife edge (skin face | wall face), as the POINT attribute
    'RimD'. Interpolated linearly across the faces, then thresholded in the skin shader -> a crisp band."""
    from mathutils.kdtree import KDTree
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    pts = []
    for e in bm.edges:
        ms = {f.material_index for f in e.link_faces}
        if skin in ms and wall in ms:
            a, b = e.verts[0].co, e.verts[1].co
            n = max(1, int((b - a).length / step))
            pts += [a.lerp(b, k / n) for k in range(n + 1)]
    kd = KDTree(len(pts))
    for i, p in enumerate(pts):
        kd.insert(p, i)
    kd.balance()
    d = np.full(len(bm.verts), 9.0, np.float32)
    for v in bm.verts:
        if any(f.material_index == skin for f in v.link_faces):
            d[v.index] = kd.find(v.co)[2]
    bm.free()
    at = me.attributes.new("RimD", "FLOAT", "POINT")
    at.data.foreach_set("value", d)
    return dict(edge_pts=len(pts), band_verts=int((d < RIND_W[1]).sum()))


def mat_skin_rind(name="Skin"):
    """mat_vc + the dark rind band from 'RimD' (only the hi bake source carries RimD; elsewhere it is absent = 0 ->
    callers must give every mesh using this material a RimD attribute)."""
    m = mat_vc(name)
    nt = m.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    src = bsdf.inputs["Base Color"].links[0].from_socket
    at = nt.nodes.new("ShaderNodeAttribute")
    at.attribute_name = "RimD"
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.interpolation_type = "SMOOTHSTEP"
    mr.inputs["From Min"].default_value = RIND_W[0]
    mr.inputs["From Max"].default_value = RIND_W[1]
    mr.inputs["To Min"].default_value = 1.0
    mr.inputs["To Max"].default_value = 0.0
    nt.links.new(at.outputs["Fac"], mr.inputs["Value"])
    mx = nt.nodes.new("ShaderNodeMix")
    mx.data_type = "RGBA"
    fac = [x for x in mx.inputs if x.identifier == "Factor_Float"][0]
    a_ = [x for x in mx.inputs if x.identifier == "A_Color"][0]
    b_ = [x for x in mx.inputs if x.identifier == "B_Color"][0]
    nt.links.new(mr.outputs["Result"], fac)
    nt.links.new(src, a_)
    b_.default_value = (*lin(RIND_COL), 1)
    nt.links.new([x for x in mx.outputs if x.identifier == "Result_Color"][0], bsdf.inputs["Base Color"])
    return m


def build_pumpkin(hi_on=True):
    """Local build (centre at the origin, face toward +Y like the eggs), then rotated 180 deg about Z (face -> -Y).
    Returns dict of objects (local) + numbers; the caller translates to the hanging axis."""
    hs = RES()["hs"]
    P = PUMP
    pl = dict(SKIN)
    skin, inner_m, flesh = mat_skin_rind("Skin"), mat_inner(), mat_flesh()
    stem_m, wax_m, wick_m = mat_vc("StemMat"), mat_vc("WaxMat"), mat_vc("WickMat")
    Pi = inner_params(P, SHELL)
    outl = {k: clean(v) for k, v in face_lamp().items()}
    cut = cutter_planar("Cutter", outl, P["R"], P["Rz"], flesh, egg=0.0)
    out = {"cut": cut}
    if hi_on:
        hi = build_mesh("Pumpkin_hi", [
            sphere_surface(egg_field(P, pl), 288 // hs, 200 // hs) + (0, 1.0),
            sphere_surface(egg_field(dict(Pi, scrape=0.006), pl), 160 // hs, 120 // hs, flip=True) + (1, 0.0)],
            [skin, inner_m])
        carve2(hi, cut)
        out["repair"] = repair_attrs(hi)
        out["rim"] = rim_distance_attr(hi)
        log("rind band source", out["rim"])
        log("pumpkin hi carved, repaired (fixed, left):", out["repair"])
        out["hi"] = hi
    f_lo = egg_field(dict(P, micro=0.0), pl)
    lo = build_mesh("Pumpkin", [sphere_surface(f_lo, 48, 18) + (0, 1.0),
                                sphere_surface(egg_field(Pi, pl), 28, 8, flip=True) + (1, 0.0)], [skin, inner_m])
    carve2(lo, cut)
    lo.data.attributes.new("RimD", "FLOAT", "POINT").data.foreach_set("value", np.full(len(lo.data.vertices), 9.0,
                                                                                         np.float32))
    out["lo"] = lo
    holes = {"lo": euler_holes(lo), "cut": len(outl)}
    if hi_on:
        holes["hi"] = euler_holes(out["hi"])
    log("pumpkin holes", holes)
    if holes["lo"] != len(outl) or (hi_on and holes["hi"] != len(outl)):
        raise RuntimeError("a hole did not open: %s" % holes)
    out["holes"] = holes
    top = f_lo(Vector((0.0, 0.0, 1.0)))[0]
    sbase = (0.0, 0.0, top.z - 0.05)
    st = dict(L=0.32, r0=0.09, seed=17, sp=dict(base=(66, 86, 34), mid=(108, 100, 52), top=(148, 126, 80),
                                                 hi=(196, 180, 124), lo=(48, 44, 22), cap=(206, 184, 130)))
    V, F, C, Rr, tip = gnarly_stem(st["L"], st["r0"], st["seed"], sbase, st["sp"], False, lean_scale=0.35)
    out["stem_lo"] = make_obj("Stem_lo", V, F, C, Rr, mats=[stem_m], recalc=True)
    out["stem_tip"] = tip
    if hi_on:
        V, F, C, Rr, _ = gnarly_stem(st["L"], st["r0"], st["seed"], sbase, st["sp"], True, lean_scale=0.35)
        out["stem_hi"] = make_obj("Stem_hi", V, F, C, Rr, mats=[stem_m], recalc=True)
    # candle on the flat inner floor
    fi = egg_field(Pi, pl)
    itop, ibot = fi(Vector((0, 0, 1)))[0].z, fi(Vector((0, 0, -1)))[0].z
    out["itop"], out["ibot"] = itop, ibot
    K = CANDLE_K
    cf, zf = candle_field(K)
    M = Matrix.Translation((0, 0, ibot - 0.012)) @ Matrix.Scale(CANDLE_SCALE, 4)
    th_lo = [2 * math.pi * j / 10 for j in range(10)]
    s_lo = [0.0, 0.3, 0.6, 0.7, 0.78, 0.86, 0.9, 0.95]
    cl = make_obj("Candle_lo", *grid_surface(cf, th_lo, s_lo, 1.0), mats=[wax_m])
    cl.data.transform(M)
    out["candle_lo"] = cl
    wp = wick_pts(K, zf, 40)
    wl = make_obj("Wick_lo", *wick_mesh(wick_pts(K, zf, 6), 6, rscale=1.5), mats=[wick_m], recalc=True)
    wl.data.transform(M)
    out["wick_lo"] = wl
    out["wick_tip"] = M @ wp[-1]
    out["wick_top"] = M @ max(wp, key=lambda p: p.z)
    if hi_on:
        th_hi = [2 * math.pi * j / (192 // hs) for j in range(192 // hs)]
        s_hi = [i / (160 // hs) for i in range(160 // hs)]
        ch = make_obj("Candle_hi", *grid_surface(cf, th_hi, s_hi, 1.0), mats=[wax_m])
        ch.data.transform(M)
        wh = make_obj("Wick_hi", *wick_mesh(wp, 12, rscale=1.5), mats=[wick_m], recalc=True)
        wh.data.transform(M)
        out["candle_hi"], out["wick_hi"] = ch, wh
    # small wax puddle around the candle foot
    for tag, nth, hi_flag in (("lo", 8, False), ("hi", 128 // hs, True)):
        if hi_flag and not hi_on:
            continue
        prof = [(0.150, 0.012), (0.215, 0.010), (0.250, 0.004), (0.258, -0.004)]
        if hi_flag:
            prof = [tuple(p) for p in catmull(prof, 8)]
        V, Fc, Cc, Rc = [], [], [], []
        rngp = random.Random(4)
        for i, (r, z) in enumerate(prof):
            for j in range(nth):
                a = 2 * math.pi * j / nth
                wob = 1 + 0.12 * noise.noise(Vector((math.cos(a) * 1.4, math.sin(a) * 1.4, 0.3)))
                V.append(Vector((r * wob * math.cos(a), r * wob * math.sin(a), ibot - 0.002 + z)))
                Cc.append(mix(lin((204, 144, 68)), lin((176, 118, 50)), 0.4 * i / len(prof)))
                Rc.append((0.22, 0.22, 0.22))
        for i in range(len(prof) - 1):
            for j in range(nth):
                jn = (j + 1) % nth
                Fc.append((i * nth + j, i * nth + jn, (i + 1) * nth + jn, (i + 1) * nth + j))
        pu = make_obj("Puddle_" + tag, V, Fc, Cc, Rc, mats=[wax_m], recalc=True)
        out["puddle_" + tag] = pu
    return out


def pumpkin_envelope(skin_obj=None, nb=200, n_az=240, n_pol=360):
    """Max radius from the pumpkin axis per height, over EVERY azimuth (so it holds for any 90-degree turn of the
    pumpkin), evaluated on the outer-skin field itself (local coords, centre at the origin)."""
    f = egg_field(PUMP, dict(SKIN))
    pts = []
    for i in range(1, n_pol):
        th = math.pi * i / n_pol
        for j in range(n_az):
            ph = 2 * math.pi * j / n_az
            pts.append(tuple(f(Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th))))[0]))
    co = np.array(pts)
    r = np.linalg.norm(co[:, :2], axis=1)
    z = co[:, 2]
    edges = np.linspace(z.min(), z.max(), nb + 1)
    zc = 0.5 * (edges[:-1] + edges[1:])
    rmax = np.zeros(nb)
    for i in range(nb):
        sel = (z >= edges[i]) & (z <= edges[i + 1])
        rmax[i] = r[sel].max() if sel.any() else np.nan
    ok = ~np.isnan(rmax)
    rmax = np.interp(zc, zc[ok], rmax[ok])
    return zc, rmax, float(z.min()), float(z.max())


def strap_profile(env, z_col, r_col, z_ring, r_ring, gap=STRAP_GAP):
    """Strap centreline in (r, z) local to the pumpkin centre: the outward offset of the max-radius envelope,
    blended into the bottom collar and the top ring."""
    zc, rmax, zmin, zmax = env
    # envelope polyline: bottom centre -> flat bottom edge -> side -> top shoulder -> top centre
    Q = [(0.0, zmin)] + [(r, z) for r, z in zip(rmax, zc)] + [(0.0, zmax)]
    Q = np.array(Q)
    Q, _ = resample_poly(Q, step=0.01)
    # smooth
    for _ in range(6):
        Q[1:-1] = 0.25 * Q[:-2] + 0.5 * Q[1:-1] + 0.25 * Q[2:]
    d = np.gradient(Q, axis=0)
    d /= np.linalg.norm(d, axis=1)[:, None] + 1e-12
    nrm = np.stack([d[:, 1], -d[:, 0]], 1)                  # right-hand side = outward (counter-clockwise walk)
    O = Q + gap * nrm
    i_lo = np.argmax((O[:, 0] > 0.64) & (np.arange(len(O)) < len(O) // 2))
    i_hi = len(O) - 1 - np.argmax((O[::-1, 0] > r_ring + 0.05) & (np.arange(len(O))[::-1] > len(O) // 2))
    mid = O[i_lo:i_hi + 1]
    for _ in range(10):
        mid[1:-1] = 0.25 * mid[:-2] + 0.5 * mid[1:-1] + 0.25 * mid[2:]
    pts = [(r_col, z_col), (0.5 * (r_col + mid[0, 0]), 0.5 * (z_col + mid[0, 1]) - 0.03)]
    pts += [tuple(p) for p in mid[::6]]
    pts += [(0.5 * (mid[-1, 0] + r_ring), 0.5 * (mid[-1, 1] + z_ring) + 0.01), (r_ring, z_ring)]
    S = catmull(pts, 6)
    S, _ = resample_poly(S, step=0.01)
    S = round_strap_corner(S)
    return S, Q


def round_strap_corner(S, frac=0.4, half=28, iters=220):
    """Round 3: the under-loop met the collar run at a slight corner (visible <= 8 studs). Find the sharpest turn
    in the lower part of the strap and relax the curve around it (weighted Laplacian, both ends pinned)."""
    S = np.array(S, float)
    n = len(S)
    d = np.diff(S, axis=0)
    a = np.arctan2(d[:, 1], d[:, 0])
    turn = np.abs((np.diff(a) + np.pi) % (2 * np.pi) - np.pi)
    lo_end = int(frac * n)
    turn_s = np.convolve(turn, np.ones(5) / 5, mode="same")
    ic = int(np.argmax(turn_s[3:lo_end])) + 4
    idx = np.arange(n)
    w = np.clip(1 - np.abs(idx - ic) / half, 0, 1) ** 1.5
    w[:3] = 0
    w[-3:] = 0
    for _ in range(iters):
        L = np.zeros_like(S)
        L[1:-1] = 0.5 * (S[:-2] + S[2:]) - S[1:-1]
        S = S + 0.5 * w[:, None] * L
    return S


# ===================================================================== cage
def lathe_part(acc, prof, nth, hi, centre, prio=1.0, seed=0, disp=None, mat=0):
    """Lathe of a (r, z) profile (absolute z) about the vertical axis through centre (x, y). Both profile ends may sit
    on the axis (r = 0): they are closed with fans. Faces point out of the solid (profile orientation by its signed
    area)."""
    prof = np.asarray(prof, float)
    cx, cy = centre
    closed_poly = np.vstack([prof, prof[:1]])
    area = 0.5 * np.sum(closed_poly[:-1, 0] * closed_poly[1:, 1] - closed_poly[1:, 0] * closed_poly[:-1, 1])
    ccw = area > 0
    ends = []
    body = prof
    if prof[0, 0] < 1e-6:
        ends.append(("first", prof[0]))
        body = body[1:]
    if prof[-1, 0] < 1e-6:
        ends.append(("last", prof[-1]))
        body = body[:-1]
    th = 2 * np.pi * np.arange(nth) / nth
    R = np.repeat(body[:, 0:1], nth, 1)
    Z = np.repeat(body[:, 1:2], nth, 1)
    if disp is not None:
        R = R * disp(np.repeat(th[None, :], len(body), 0), Z)
    G = np.stack([cx + R * np.cos(th)[None, :], cy + R * np.sin(th)[None, :], Z], -1)

    def out2(d):
        n = np.array([d[1], -d[0]])                     # right-hand side of the walking direction
        return n if ccw else -n
    if not hi:
        v = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(body, axis=0), axis=1))])
        uvg = np.zeros((len(body), nth + 1, 2))
        per = 2 * np.pi * body[:, 0]
        for j in range(nth + 1):
            uvg[:, j, 0] = per * j / nth - per / 2 + per.max() / 2
        uvg[:, :, 1] = v[:, None]
        uvg = uvg * prio + acc.new_island()
        at = None
    else:
        ki, kj, _ = grid_curvature(G)
        conv = blur_grid(np.maximum(np.maximum(ki, kj), 0))
        conc = blur_grid(np.maximum(np.maximum(-ki, -kj), 0))
        col, rough, wear = iron_shade(G.reshape(-1, 3), conv.ravel(), conc.ravel(), seed=seed)
        at = {"Col": col.reshape(G.shape), "Rough": rough.reshape(G.shape), "Wear": wear.reshape(G.shape)}
        uvg = np.zeros((len(body), nth + 1, 2))
    i0 = int(np.argmax(np.linalg.norm(np.diff(body, axis=0), axis=1)))
    n2 = out2(body[i0 + 1] - body[i0])
    a_, b_, c_ = G[i0, 0], G[i0, 1], G[i0 + 1, 0]
    fn = np.cross(b_ - a_, c_ - a_)
    flip = np.dot(fn, np.array([n2[0], 0.0, n2[1]])) < 0
    base, fl = acc.add_grid(G, uvg, at=at, flip=flip, mat=mat)
    nb = len(body)
    a1 = None if at is None else {k: v.reshape(-1, 3)[:1] for k, v in at.items()}
    for which, p in ends:
        i = 0 if which == "first" else nb - 1
        ring = base + i * nth + np.arange(nth)
        d = (body[0] - p) if which == "first" else (p - body[-1])
        n2 = out2(d)
        uvr = uvg[i, :nth] if not hi else np.zeros((nth, 2))
        acc.add_fan(ring, (cx, cy, p[1]), uvr, uvr[0], at_c=a1, outward=np.array([0.0, 0.0, np.sign(n2[1]) or 1.0]),
                    mat=mat)
    return G


def torus_part(acc, centre, normal, R, r, nmaj, nmin, hi, prio=1.0, seed=0, stadium=None, mat=0):
    """Torus (or a stadium-shaped chain link when stadium=(half straight length)) in the plane with the given
    normal. The link's long axis is vertical (z)."""
    normal = np.asarray(normal, float) / np.linalg.norm(normal)
    up = np.array([0, 0, 1.0])
    e1 = up - normal * normal.dot(up)
    if np.linalg.norm(e1) < 1e-6:
        e1 = np.array([1.0, 0, 0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(normal, e1)
    t = 2 * np.pi * np.arange(nmaj) / nmaj
    if stadium:
        L = stadium
        # stadium centreline param by angle-like t: straight parts along e1
        pts = []
        per = 2 * L + 2 * np.pi * R
        for tt in t / (2 * np.pi) * per:
            if tt < L:
                pts.append(e1 * (-L / 2 + tt) + e2 * R)
            elif tt < L + np.pi * R:
                a = (tt - L) / R
                pts.append(e1 * (L / 2) + R * (e2 * math.cos(a) + e1 * math.sin(a)))
            elif tt < 2 * L + np.pi * R:
                pts.append(e1 * (L / 2 - (tt - L - np.pi * R)) - e2 * R)
            else:
                a = (tt - 2 * L - np.pi * R) / R
                pts.append(-e1 * (L / 2) - R * (e2 * math.cos(a) + e1 * math.sin(a)))
        Pc = np.array(pts) + centre
    else:
        Pc = centre + R * (np.cos(t)[:, None] * e1 + np.sin(t)[:, None] * e2)
    # closed path: tangents by periodic differences
    T = np.roll(Pc, -1, 0) - np.roll(Pc, 1, 0)
    T /= np.linalg.norm(T, axis=1)[:, None]
    N = np.tile(normal, (nmaj, 1))
    B = np.cross(T, N)
    a = 2 * np.pi * np.arange(nmin) / nmin
    S = np.stack([r * np.cos(a)[None, :].repeat(nmaj, 0), r * np.sin(a)[None, :].repeat(nmaj, 0)], -1)
    G = sweep_grid(Pc, N, B, S)
    # close the loop: append the first ring again for a periodic i direction
    Gc = np.concatenate([G, G[:1]], 0)
    cen = np.concatenate([Pc, Pc[:1]], 0)
    if not hi:
        per = 2 * np.pi * r
        v = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(cen, axis=0), axis=1))])
        uvg = section_uv(np.concatenate([S, S[:1]], 0), v) * prio + acc.new_island()
        base, fl = acc.add_grid(Gc, uvg, centres=cen, mat=mat)
    else:
        ki, kj, _ = grid_curvature(Gc)
        conv = blur_grid(np.maximum(np.maximum(ki, kj), 0))
        conc = blur_grid(np.maximum(np.maximum(-ki, -kj), 0))
        col, rough, wear = iron_shade(Gc.reshape(-1, 3), conv.ravel(), conc.ravel(), seed=seed, wear_k=(22.0, 50.0))
        at = {"Col": col.reshape(Gc.shape), "Rough": rough.reshape(Gc.shape), "Wear": wear.reshape(Gc.shape)}
        base, fl = acc.add_grid(Gc, np.zeros((nmaj + 1, nmin + 1, 2)), at=at, centres=cen)
    return Gc


def spear_outline():
    """Flat spear-head finial (s across, t up from the neck, straight; the bend is applied afterwards)."""
    right = [(0.05, -0.03), (0.06, 0.02), (0.095, 0.055), (0.108, 0.095), (0.100, 0.140), (0.078, 0.172),
             (0.058, 0.200), (0.074, 0.222), (0.052, 0.262), (0.024, 0.305)]
    tip = [(0.0, 0.335)]
    left = [(-s, t) for s, t in reversed(right)]
    return right + tip + left


def spear_bend(pts, t0=0.16, ang=28.0):
    """Bend the blade above t0 toward +s by up to `ang` degrees (smoothly), in its own plane."""
    out = []
    for s, t in pts:
        if t <= t0:
            out.append((s, t))
            continue
        k = smoothstep(t0, 0.335, t)
        a = math.radians(ang) * k
        dt = t - t0
        out.append((s * math.cos(a) + dt * math.sin(a), t0 + dt * math.cos(a) - s * math.sin(a)))
    return out


def build_spear(acc, hole_c, hi, axis_xy, mat=0):
    """Blade in the Y-Z plane (x = 0 offset by axis), thickness 0.05, pierced near its base; bent toward +Y."""
    x0, y0 = axis_xy
    neck_z = hole_c - 0.085
    outer = spear_outline()
    if hi:
        outer = [tuple(p) for p in catmull(outer + [outer[0]], 6)][:-1]
        nh = 48
    else:
        nh = 10
    hole = [(HOLE_R * math.cos(2 * math.pi * k / nh), 0.085 + HOLE_R * math.sin(2 * math.pi * k / nh)) for k in range(nh)]
    hole = list(reversed(hole))
    ob2, hb2 = spear_bend(outer), spear_bend(hole)
    # 2D -> 3D: s -> +Y (toward the pole = 'back'), t -> z
    def to3(pts, w):
        return np.array([[x0 + w, y0 + s, neck_z + t] for s, t in pts])
    allp = ob2 + hb2
    if hi:
        # dense interior via CDT for the bevel + forged texture
        poly = np.array(ob2)
        step = 0.006
        mn, mx = poly.min(0), poly.max(0)
        gx, gy = np.meshgrid(np.arange(mn[0], mx[0], step), np.arange(mn[1], mx[1], step))
        cand = np.stack([gx.ravel(), gy.ravel()], 1)
        cand = cand[_inside(poly, cand) & ~_inside(np.array(hb2), cand)]
        verts = [Vector(p) for p in ob2 + hb2] + [Vector(p) for p in cand]
        ko, kh = len(ob2), len(hb2)
        edges = [(i, (i + 1) % ko) for i in range(ko)] + [(ko + i, ko + (i + 1) % kh) for i in range(kh)]
        res = geometry.delaunay_2d_cdt(verts, edges, [], 3, 1e-8)
        uv2 = np.array([[v.x, v.y] for v in res[0]])
        tris = [list(f) for f in res[2]]
        dout = np.full(len(uv2), 9.0)
        for loop in (ob2, hb2):
            L = np.array(loop)
            for i in range(len(L)):
                dd, _ = _seg_dist(uv2, L[i], L[(i + 1) % len(L)])
                dout = np.minimum(dout, dd)
        rim = np.sqrt(np.clip(1 - (1 - np.clip(dout / 0.018, 0, 1)) ** 2, 0, 1))
        mid = np.exp(-(uv2[:, 0] / 0.02) ** 2) * (uv2[:, 1] > 0.15)      # a raised mid-rib on the spear point
        half = 0.025 * rim * (1 + 0.25 * mid)
        V = np.vstack([np.column_stack([x0 + half, y0 + uv2[:, 0], neck_z + uv2[:, 1]]),
                       np.column_stack([x0 - half, y0 + uv2[:, 0], neck_z + uv2[:, 1]])])
        k = len(uv2)
        F = [[t[0], t[1], t[2]] for t in tris] + [[k + t[2], k + t[1], k + t[0]] for t in tris]
        p0, p1, p2 = V[F[0][0]], V[F[0][1]], V[F[0][2]]
        if np.cross(p1 - p0, p2 - p0)[0] < 0:
            F = [list(reversed(f)) for f in F]
        conv = np.concatenate([40 * (1 - rim) + 20 * mid] * 2)
        col, rough, wear = iron_shade(V, conv, np.zeros(len(V)), seed=61)
        acc.merge_mesh(V, F, [[(0, 0)] * 3] * len(F), at={"Col": col, "Rough": rough, "Wear": wear})
        return
    tri = geometry.tessellate_polygon([[Vector((s, t, 0)) for s, t in ob2], [Vector((s, t, 0)) for s, t in hb2]])
    k = len(allp)
    V = np.vstack([to3(allp, 0.025), to3(allp, -0.025)])
    a2 = np.array(allp)
    F, UV = [], []
    o1, o2, o3 = acc.new_island(), acc.new_island(), acc.new_island()
    for t in tri:
        F.append([t[0], t[1], t[2]])
        UV.append([a2[t[0]] * 1.2 + o1, a2[t[1]] * 1.2 + o1, a2[t[2]] * 1.2 + o1])
        F.append([k + t[2], k + t[1], k + t[0]])
        UV.append([a2[t[2]] * 1.2 + o2, a2[t[1]] * 1.2 + o2, a2[t[0]] * 1.2 + o2])
    for loop_start, loop_len in ((0, len(ob2)), (len(ob2), len(hb2))):
        for i in range(loop_len):
            a_, b_ = loop_start + i, loop_start + (i + 1) % loop_len
            F.append([a_, b_, k + b_, k + a_])
            UV.append([np.array([i * 0.03, 0]) + o3, np.array([(i + 1) * 0.03, 0]) + o3,
                       np.array([(i + 1) * 0.03, 0.06]) + o3, np.array([i * 0.03, 0.06]) + o3])
        o3 = o3 + np.array([0, 0.2])
    p0, p1, p2 = V[F[0][0]], V[F[0][1]], V[F[0][2]]
    if np.cross(p1 - p0, p2 - p0)[0] < 0:
        F = [list(reversed(f)) for f in F]
        UV = [list(reversed(u)) for u in UV]
    acc.merge_mesh(V, F, UV, mat=mat)


def head_stack(cv):
    """Chain + cap heights from the hook cradle. Returns a dict of z values (Blender)."""
    c = float(cv["z"][cv["ic"]])
    rc = float(crook_radius(cv, cv["s"][cv["ic"]]))
    ri, rw = RING["ri"], RING["rw"]
    Li, Wi, lw = LINK["Li"], LINK["Wi"], LINK["rw"]
    H = dict(cradle=c, rc=rc)
    H["ring_c"] = c + rc - ri                      # the ring's inner top rests on the bar top
    H["ring_ib"] = H["ring_c"] - ri
    H["l1_it"] = H["ring_ib"]
    H["l1_ib"] = H["l1_it"] - Li
    H["l2_it"] = H["l1_ib"]
    H["l2_ib"] = H["l2_it"] - Li
    H["hole_top"] = H["l2_ib"]
    H["hole_c"] = H["hole_top"] - HOLE_R
    H["neck"] = H["hole_c"] - 0.085
    H["rim"] = H["neck"] - CAP_H
    H["ring_z"] = H["rim"] - 0.005
    H["chain_top"] = c + rc
    return H


# witch hat: a tall cone (0.66 to the neck) with a concave flare into a flat brim; the underside cavity (the stem
# clearance) is unchanged from round 1
CAP_H = 0.66
CAP_PROFILE = [(0.0, CAP_H), (0.05, CAP_H - 0.03), (0.12, 0.46), (0.20, 0.30), (0.30, 0.165), (0.44, 0.082),
               (0.62, 0.035), (0.80, 0.012), (0.842, -0.012), (0.79, -0.036), (0.62, 0.0), (0.30, 0.090),
               (0.0, 0.330)]


CAGE_GROUPS = ("straps", "body", "ring_l2", "link1", "seat")


def build_cage(cv, env, zc, H, hi):
    """Straps (offset of the pumpkin envelope), top ring, cap + spear, saucer, bottom collar, drop finial, chain.
    Lo: one Acc, material index = bake group. Hi: one Acc per bake group."""
    if hi:
        accs = {g: Acc(attrs=True) for g in CAGE_GROUPS}
    else:
        one = Acc(attrs=False)
        accs = {g: one for g in CAGE_GROUPS}
    gm = {g: i for i, g in enumerate(CAGE_GROUPS)}
    hs = RES()["hs"]
    ax = (0.0, HANG_Y)
    axv = np.array([0.0, HANG_Y, 0.0])
    zcl, rmax, zmin, zmax = env
    zb = zc + zmin                                  # pumpkin bottom (world)
    sauc_top = zb - 0.002
    col0, col1 = sauc_top - 0.07 - 0.13, sauc_top - 0.07
    z_col = 0.5 * (col0 + col1)
    S2, Q = strap_profile(env, z_col - zc, 0.265, H["ring_z"] - zc - 0.01, 0.50 + 0.01)
    straps_check = []
    for k in range(4):
        az = math.radians(45 + 90 * k)
        dvec = np.array([math.cos(az), math.sin(az), 0.0])
        side = np.array([-math.sin(az), math.cos(az), 0.0])
        P = np.array([axv + dvec * r + np.array([0, 0, zc + z]) for r, z in S2])
        Rl = polyline_curv_radius(P, k=6)
        if hi:
            idx = np.arange(0, len(P), 1)
            sec = rrect(0.14, 0.055, n_corner=5, cr=0.018)
        else:
            idx = adaptive_samples(P, Rl, sag=0.004, max_len=0.22, max_turn=13.0)
            sec = np.array([(0.07, 0.0), (0.05, 0.0275), (-0.05, 0.0275), (-0.07, 0.0), (-0.05, -0.0275),
                            (0.05, -0.0275)])
        Ps = P[idx]
        T, N, B = frames_planar(Ps, side)
        v = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(Ps, axis=0), axis=1))])
        S = np.repeat(sec[None, :, :], len(Ps), 0)
        wear_extra = None
        if hi:
            # raised centre bead line along the strap's outer face + end rivets
            a_ = np.arctan2(S[..., 1], S[..., 0])
            bead = np.exp(-((S[..., 0]) / 0.012) ** 2) * (S[..., 1] > 0)
            S = S.copy()
            S[..., 1] += 0.006 * bead
            wear_extra = 0.5 * bead
        (base, fl), G = sweep_part(accs["straps"], Ps, N, B, S, v, hi, prio=1.0, seed=70 + k,
                                   wear_extra=wear_extra, wear_k=(25.0, 70.0), mat=0 if hi else gm["straps"])
        rr = np.linalg.norm(Ps[:, :2] - axv[:2], axis=1)
        straps_check.append((Ps, rr))
        if hi:
            # end rivets on the strap's outer face
            for t_ in (0.06, 0.94):
                i = int(t_ * (len(Ps) - 1))
                outward = B[i] * np.sign(np.dot(B[i], dvec) + 1e-9) if abs(np.dot(B[i], dvec)) > 0.1 else B[i]
                rivet_acc([(Ps[i] + outward * 0.0275, outward, 0.024)], accs["straps"], seed=80 + k)
    nth = (128 // hs) if hi else 20
    # top ring (torus) and bottom collar
    torus_part(accs["body"], np.array([0, HANG_Y, H["ring_z"]]), (0, 0, 1.0), 0.50, 0.035,
               (192 // hs) if hi else 24, (24 // hs) if hi else 6, hi, seed=90, mat=0 if hi else gm["body"])
    coll = [(0.0, col1 + 0.002), (0.20, col1), (0.255, col1 - 0.02), (0.265, z_col), (0.255, col0 + 0.02),
            (0.20, col0), (0.0, col0 - 0.002)]
    if hi:
        coll = [tuple(p) for p in catmull(coll, 6)]
    lathe_part(accs["seat"], [(r, z) for r, z in coll], nth if hi else 20, hi, ax, seed=91,
               mat=0 if hi else gm["seat"])
    # saucer: flat plate, rolled edge curling down
    sau = [(0.0, sauc_top), (0.50, sauc_top), (0.538, sauc_top - 0.016), (0.548, sauc_top - 0.045),
           (0.522, sauc_top - 0.066), (0.46, sauc_top - 0.056), (0.25, sauc_top - 0.062), (0.0, sauc_top - 0.068)]
    if hi:
        sau = [tuple(p) for p in catmull(sau, 6)]
    lathe_part(accs["seat"], sau, nth if hi else 20, hi, ax, prio=0.8, seed=92, mat=0 if hi else gm["seat"])
    # drop finial under the collar
    z0 = col0
    drop = [(0.0, z0 + 0.002), (0.19, z0), (0.13, z0 - 0.03), (0.075, z0 - 0.05), (0.086, z0 - 0.08),
            (0.072, z0 - 0.115), (0.038, z0 - 0.135), (0.02, z0 - 0.165), (0.0, z0 - 0.21)]
    if hi:
        drop = [tuple(p) for p in catmull(drop, 6)]
    lathe_part(accs["seat"], drop, nth if hi else 14, hi, ax, seed=93, mat=0 if hi else gm["seat"])
    # witch-hat cap (closed shell lathe)
    capz = [(r, H["rim"] + z) for r, z in CAP_PROFILE]
    if hi:
        capz = [tuple(p) for p in catmull(capz, 10)]
    lathe_part(accs["body"], capz, nth if hi else 28, hi, ax, seed=94, mat=0 if hi else gm["body"])
    build_spear(accs["body"], H["hole_c"], hi, ax, mat=0 if hi else gm["body"])
    # chain: ring over the hook cradle (plane X-Z), link 1 (Y-Z), link 2 (X-Z)
    torus_part(accs["ring_l2"], np.array([0, HANG_Y, H["ring_c"]]), (0, 1.0, 0), RING["ri"] + RING["rw"],
               RING["rw"], (96 // hs) if hi else 12, (16 // hs) if hi else 5, hi, prio=0.8, seed=95,
               mat=0 if hi else gm["ring_l2"])
    hw = LINK["Wi"] / 2 + LINK["rw"]
    Ls = LINK["Li"] - 2 * hw + 2 * LINK["rw"]
    for k, (it, nrm) in enumerate(((H["l1_it"], (1.0, 0, 0)), (H["l2_it"], (0, 1.0, 0)))):
        cz = it - LINK["Li"] / 2
        g = "link1" if k == 0 else "ring_l2"
        torus_part(accs[g], np.array([0, HANG_Y, cz]), nrm, hw, LINK["rw"], (96 // hs) if hi else 10,
                   (16 // hs) if hi else 5, hi, prio=0.8, seed=96 + k, stadium=Ls, mat=0 if hi else gm[g])
    return (accs if hi else accs["straps"]), dict(sauc_top=sauc_top, col=(col0, col1), drop_tip=z0 - 0.21, straps=straps_check, strap2d=S2)


# ===================================================================== web + silk
def web_frame(cv, vc, H):
    """The frame polygon of the crook web in (y', z) = (-y, z) + the iron member id of each point (1 pole, 2 volute,
    3 arc, 4 curl, 5 chain link; an edge whose two ends share a member lies along that iron, every other edge is a
    frame thread)."""
    P, Rl, s = crook_path3d(cv)
    yq, zq = -P[:, 1], P[:, 2]
    rq = crook_radius(cv, s)
    pts, mem = [], []

    def add(p, m):
        pts.append((float(p[0]), float(p[1])))
        mem.append(m)
    for z in np.linspace(13.30, cv["zs"] - 0.36, 6):
        add((rp(z) - 0.025, z), 1)          # threads tuck 0.025 into the pole (wrapped on, no gap)
    vy, vz, al = vc["y"], vc["z"], vc["al"]
    Cy, Cz = vc["C"]
    sel = (np.degrees(al) >= 185) & (np.degrees(al) <= 335)
    vpts = np.stack([vy[sel], vz[sel]], 1)
    outward = vpts - np.array([Cy, Cz])
    outward /= np.linalg.norm(outward, axis=1)[:, None]
    vpts = (vpts + outward * 0.042)[::-1]
    for p in list(vpts[::max(1, len(vpts) // 7)]) + [vpts[-1]]:
        add(p, 2)
    arc_sel = (yq > vpts[-1][0] + 0.35) & (yq < 2.95) & (np.arange(len(yq)) < len(yq) * 0.6) &         (zq > cv["z"][cv["ia"]] - 0.9)
    ai = np.nonzero(arc_sel)[0]
    ai = ai[np.argsort(yq[ai])]
    for i in ai[::max(1, len(ai) // 8)]:
        add((yq[i], zq[i] - rq[i] - 0.004), 3)
    curl = np.arange(len(yq)) > (cv["ic"] + 32)
    ci = np.nonzero(curl)[0]
    il = ci[np.argmin(yq[ci])]
    add((yq[il] - rq[il] - 0.004, zq[il]), 4)
    hw = LINK["Wi"] / 2 + LINK["rw"]
    add((-HANG_Y - hw - 0.004, H["l1_it"] - 0.06), 5)
    add((-HANG_Y - hw - 0.004, H["l1_ib"] + 0.04), 5)
    return np.array(pts), np.array(mem), il


def parallel_runs(chords, hub, tol_deg=4.0):
    """Longest run of radially neighbouring ring chords in one sector whose directions differ by < tol_deg (a
    'ladder'). chords: (ring, sector, pa, pb) in the web plane."""
    by = {}
    for kr, i, pa, pb in chords:
        d = pb - pa
        by.setdefault(i, []).append((kr, math.degrees(math.atan2(d[1], d[0]))))
    best = 1
    for i, lst in by.items():
        lst.sort()
        run = 1
        for (k0, a0), (k1, a1) in zip(lst, lst[1:]):
            da = abs((a1 - a0 + 90) % 180 - 90)
            run = run + 1 if (k1 == k0 + 1 and da < tol_deg) else 1
            best = max(best, run)
    return best


def build_web(cv, vc, H):
    """Orb web filling the crook (Y-Z plane, bowing 0.1 toward +X). Returns (strands object, silk object, info)."""
    rng = random.Random(77)
    poly, mem, il = web_frame(cv, vc, H)
    # lower free edge: catenary from link 1 back to the pole bottom anchor
    a, b = poly[-1], poly[0]
    sag = [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t - 0.28 * 4 * t * (1 - t)) for t in np.linspace(0, 1, 12)]
    full = [tuple(p) for p in poly] + sag[1:-1]
    flags = list(mem) + [0] * (len(sag) - 2)
    P2 = np.array(full)
    # hub: area centroid pulled toward the upper part
    x, y = P2[:, 0], P2[:, 1]
    A = 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)
    cx = np.sum((x + np.roll(x, -1)) * (x * np.roll(y, -1) - np.roll(x, -1) * y)) / (6 * A)
    cy = np.sum((y + np.roll(y, -1)) * (x * np.roll(y, -1) - np.roll(x, -1) * y)) / (6 * A)
    hub = np.array([cx, cy + 0.25])
    Rmax = float(np.max(np.linalg.norm(P2 - hub, axis=1)))
    S = Strands()

    def lift(p2):
        d = np.linalg.norm(np.asarray(p2) - hub) / Rmax
        return Vector((0.10 * max(0.0, 1 - d * d) + 0.012 * noise.noise(Vector((p2[0] * 1.3, p2[1] * 1.3, 0.5))),
                       -p2[0], p2[1] - 0.06 * d * max(0.0, 1 - d)))
    # ---- round 2 (MUST 2): no ladder / comb. Spokes are placed, not random: one spoke to the top pole anchor (by
    # collar 3) and one to the z 13.3 anchor (fanned >= 35 deg apart), one between them, and the rest spread so that
    # NO sector is wider than ~28 deg. Rings are spaced geometrically (x1.25 outward), every chord gets its own
    # small radius jitter + the long ones sag toward the hub, so no 4 neighbouring spans run parallel.
    R_FR = 0.060
    pole_pts = [np.array(full[i]) for i in range(len(full)) if flags[i] == 1]
    p_top = max(pole_pts, key=lambda q: q[1])
    p_bot = min(pole_pts, key=lambda q: q[1])
    a_top = math.atan2(p_top[1] - hub[1], p_top[0] - hub[0]) % (2 * math.pi)
    a_bot = math.atan2(p_bot[1] - hub[1], p_bot[0] - hub[0]) % (2 * math.pi)
    if (a_bot - a_top) % (2 * math.pi) > math.pi:
        a_top, a_bot = a_bot, a_top
    fan = (a_bot - a_top) % (2 * math.pi)
    angs = [a_top, a_top + fan / 2, a_top + fan]
    rest = 2 * math.pi - fan
    nrest = int(math.ceil(rest / math.radians(28.0)))
    for k in range(1, nrest):
        angs.append(a_top + fan + rest * k / nrest + rng.uniform(-1, 1) * math.radians(1.5))
    ends = []
    for th in angs:
        hit = poly_hit(tuple(hub), (math.cos(th), math.sin(th)), full)
        if hit is None:
            continue
        t, si, u = hit
        p = np.array(full[si]) + (np.array(full[(si + 1) % len(full)]) - np.array(full[si])) * u
        ends.append((th % (2 * math.pi), p, t))
    ends.sort(key=lambda e: e[0])
    sect = [math.degrees((ends[(i + 1) % len(ends)][0] - ends[i][0]) % (2 * math.pi)) for i in range(len(ends))]
    for th, p, L in ends:
        n = max(3, int(L / 0.9))
        pts = [lift(hub + (p - hub) * k / n) for k in range(n + 1)]
        S.tube(pts, [0.044 + 0.016 * (k / n) for k in range(n + 1)], 3)        # tapering spoke 0.088 -> 0.12
    nring = 7
    fr = [0.92 / 1.25 ** (nring - 1 - k) for k in range(nring)]                   # 0.24 ... 0.92, x1.25 outward
    # rings are rounder than the frame (tanh-compressed toward the frame on short spokes) and every chord end gets
    # an alternating +-2.8 % (+ random) radius offset -> neighbouring spans in a sector never run parallel
    Ls = np.array([np.linalg.norm(p - hub) for th, p, L in ends])
    Lref = float(np.percentile(Ls, 70))
    jit = [[1 + 0.028 * (1 if (kr + i) % 2 else -1) + 0.012 * rng.uniform(-1, 1) for i in range(len(ends))]
           for kr in range(nring)]
    skip = {(4, rng.randrange(len(ends))), (6, rng.randrange(len(ends)))}        # two broken chords (no stubs)
    chords = []
    prev = None
    crowd = 0
    for kr in range(nring):
        row = []
        for i, (th, p, L) in enumerate(ends):
            Li = float(Ls[i])
            rr_ = fr[kr] * math.sqrt(Li * Lref) * jit[kr][i]          # geometric spacing, half-way to round
            # true geometric rings round the hub; where the frame comes closer the ring simply stops (no bunching)
            row.append(hub + (p - hub) / Li * rr_ if rr_ < 0.93 * Li - 0.04 else None)
        rad = 0.0425 + 0.0145 * kr / (nring - 1)                                  # 0.085 at the hub .. 0.114 out
        for i in range(len(row)):
            j = (i + 1) % len(row)
            if (kr, i) in skip:
                continue
            if row[i] is None or row[j] is None:
                crowd += 1                                  # the ring meets the frame here: stop it
                continue
            pa, pb = row[i], row[j]
            span = np.linalg.norm(pb - pa)
            nseg = 1 if span < 0.6 else 2
            mid_to_hub = hub - (pa + pb) * 0.5
            pts2 = []
            for q in range(nseg + 1):
                t = q / nseg
                pp = pa + (pb - pa) * t + mid_to_hub / max(np.linalg.norm(mid_to_hub), 1e-6) * 0.09 * span *                     4 * t * (1 - t)
                pp = pp - np.array([0, 0.04 * span * 4 * t * (1 - t)])
                pts2.append(pp)
            chords.append((kr, i, pa, pb))
            S.tube([lift(p) for p in pts2], rad, 3)
        prev = row
    # frame threads only where the frame bridges between iron members (+ the free lower edge)
    nfull = len(full)
    for i in range(nfull):
        j = (i + 1) % nfull
        if flags[i] == flags[j] and flags[i] != 0:
            continue                                        # this edge lies along iron
        pa, pb = np.array(full[i]), np.array(full[j])
        n = max(2, int(np.linalg.norm(pb - pa) / 0.65))
        S.tube([lift(pa + (pb - pa) * k / n) for k in range(n + 1)], R_FR, 4)
    # ONE long loose thread drapes from the lower edge near the pole and curls at its end (replaces the stubs)
    k = int(0.80 * (len(sag) - 1))
    p0 = lift(sag[k])
    th_pts, d = [p0], Vector((0.03, 0.10, -1.0)).normalized()
    for q in range(9):
        d = (d.lerp(Vector((0, 0, -1)), 0.25) + Vector((0.012, 0.035 * math.sin(q * 0.9), 0))).normalized()
        th_pts.append(th_pts[-1] + d * 0.075)
    c = th_pts[-1] + Vector((0, 0.05, 0.0))
    for q in range(1, 6):
        an = -math.pi / 2 - 1.15 * q
        th_pts.append(c + Vector((0, 0.05 * math.cos(an + math.pi), 0.05 * math.sin(an + math.pi) + 0.0)))
    S.tube(th_pts, [0.045 - 0.012 * q / (len(th_pts) - 1) for q in range(len(th_pts))], 3)
    info_web = dict(sectors_deg=[round(x, 1) for x in sect], pole_fan_deg=round(math.degrees(fan), 1),
                    ring_fracs=[round(x, 3) for x in fr], parallel_max_run=parallel_runs(chords, hub),
                    chords=len(chords), crowded_skipped=crowd)
    S.blob(lift(hub) + Vector((0.01, 0, 0)), 0.06, 0.16, 0.16, nu=7, nv=4)
    # UVs: planar (y', z) over the web bbox
    mnp, mxp = P2.min(0) - 0.3, P2.max(0) + 0.3
    W = float(max(mxp - mnp))

    def uvfun(co):
        return (min(1, max(0, (-co.y - mnp[0]) / W)), min(1, max(0, (co.z - mnp[1]) / W)))
    web = S.to_object("Web", uvfun)
    info = dict(hub=[0.0, float(-hub[0]), float(hub[1])], Rmax=round(Rmax, 3), spokes=len(ends), rings=nring,
                **info_web,
                span_y=round(float(P2[:, 0].max() - P2[:, 0].min()), 3),
                span_z=round(float(P2[:, 1].max() - P2[:, 1].min()), 3), bbox2d=[mnp.tolist(), mxp.tolist()])
    silk = build_silk(full, poly, hub, lift, vc, cv, sag)
    return web, silk, info


class Strands:
    """(copied from webs_spiders.py) tube strands accumulated in one bmesh."""

    def __init__(self):
        self.bm = bmesh.new()

    def tube(self, pts, r, sides=3):
        n = len(pts)
        if n < 2:
            return
        bm = self.bm
        T = []
        for i in range(n):
            t = pts[min(n - 1, i + 1)] - pts[max(0, i - 1)]
            T.append(t.normalized() if t.length > 1e-9 else Vector((1, 0, 0)))
        ref = Vector((1, 0, 0))
        N = ref - T[0] * ref.dot(T[0])
        if N.length < 1e-3:
            alt = Vector((0, 0, 1))
            N = alt - T[0] * alt.dot(T[0])
        N.normalize()
        rings = []
        for i in range(n):
            N = N - T[i] * N.dot(T[i])
            if N.length < 1e-6:
                N = ref - T[i] * ref.dot(T[i])
            N.normalize()
            B = T[i].cross(N)
            rr = r[i] if isinstance(r, (list, tuple)) else r
            rings.append([bm.verts.new(pts[i] + (N * math.cos(2 * math.pi * j / sides)
                                                  + B * math.sin(2 * math.pi * j / sides)) * rr)
                          for j in range(sides)])
        for i in range(n - 1):
            for j in range(sides):
                k = (j + 1) % sides
                bm.faces.new((rings[i][j], rings[i][k], rings[i + 1][k], rings[i + 1][j]))

    def blob(self, centre, rx, ry, rz, nu=8, nv=5):
        bm = self.bm
        top = bm.verts.new(centre + Vector((0, 0, rz)))
        rings = []
        for i in range(1, nv):
            th = math.pi * i / nv
            ring = []
            for j in range(nu):
                a = 2 * math.pi * j / nu
                k = 1 + 0.15 * math.sin(3 * a + 1.3)
                ring.append(bm.verts.new(centre + Vector((rx * math.sin(th) * math.cos(a) * k,
                                                          ry * math.sin(th) * math.sin(a) * k, rz * math.cos(th)))))
            rings.append(ring)
        bot = bm.verts.new(centre - Vector((0, 0, rz)))
        fs = []
        for j in range(nu):
            k = (j + 1) % nu
            fs.append(bm.faces.new((top, rings[0][j], rings[0][k])))
            for i in range(len(rings) - 1):
                fs.append(bm.faces.new((rings[i][j], rings[i + 1][j], rings[i + 1][k], rings[i][k])))
            fs.append(bm.faces.new((rings[-1][k], rings[-1][j], bot)))
        bmesh.ops.recalc_face_normals(bm, faces=fs)

    def to_object(self, name, uvfun):
        bmesh.ops.triangulate(self.bm, faces=self.bm.faces[:])
        me = bpy.data.meshes.new(name)
        self.bm.to_mesh(me)
        self.bm.free()
        for p in me.polygons:
            p.use_smooth = True
        uv = me.uv_layers.new(name="UVMap")
        data = []
        for lp in me.loops:
            data.extend(uvfun(me.vertices[lp.vertex_index].co))
        uv.data.foreach_set("uv", data)
        return link(bpy.data.objects.new(name, me))


def two_sided(bm, uvs, grid, keep, uvgrid, front_dir):
    """(after webs_spiders._two_sided) front faces along front_dir, plus a back copy."""
    rows, cols = len(grid), len(grid[0])
    used = set()
    for i, j in keep:
        used |= {(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)}
    front, back = {}, {}
    for ij in sorted(used):
        front[ij] = bm.verts.new(grid[ij[0]][ij[1]])
        uvs.append(uvgrid[ij[0]][ij[1]])
    for ij in sorted(used):
        back[ij] = bm.verts.new(grid[ij[0]][ij[1]])
        uvs.append(uvgrid[ij[0]][ij[1]])
    i0, j0 = keep[0]
    a, b, c = grid[i0][j0], grid[i0][j0 + 1], grid[i0 + 1][j0]
    flip = (b - a).cross(c - a).dot(front_dir) < 0
    for i, j in keep:
        q = [front[(i, j)], front[(i, j + 1)], front[(i + 1, j + 1)], front[(i + 1, j)]]
        if flip:
            q.reverse()
        bm.faces.new(q)
        qb = [back[(i, j)], back[(i, j + 1)], back[(i + 1, j + 1)], back[(i + 1, j)]]
        if not flip:
            qb.reverse()
        bm.faces.new(qb)


def build_silk(full, poly, hub, lift, vc, cv, sag):
    bm = bmesh.new()
    uvs = []
    rng = random.Random(41)
    fdir = Vector((1, 0, 0))
    # (0) gauze in the corner between the pole top / collar 3 and the volute (island 0)
    Cy, Cz = vc["C"]
    zs = cv["zs"]
    c00 = np.array([rp(zs - 0.5) + 0.01, zs - 0.62])
    c10 = np.array([rp(zs - 0.36) + 0.01, zs - 0.36])
    vy, vz = vc["y"], vc["z"]
    ib = int(np.argmin(vz[: len(vz) // 2]))
    c11 = np.array([vy[ib], vz[ib] - 0.05])
    c01 = np.array([c11[0] * 0.75, zs - 0.70])
    n = 5
    grid, uvg = [], []
    for i in range(n + 1):
        row, urow = [], []
        for j in range(n + 1):
            a_, b_ = i / n, j / n
            p = (c00 * (1 - a_) * (1 - b_) + c10 * a_ * (1 - b_) + c01 * (1 - a_) * b_ + c11 * a_ * b_)
            p = p + np.array([0.0, -0.08 * math.sin(math.pi * a_) * math.sin(math.pi * b_)])
            v3 = lift(p) + Vector((-0.02, 0, 0))
            row.append(v3)
            urow.append((0.5 * (0.03 + 0.94 * b_), 0.5 * (0.03 + 0.94 * a_)))
        grid.append(row)
        uvg.append(urow)
    two_sided(bm, uvs, grid, [(i, j) for i in range(n) for j in range(n)], uvg, fdir)
    # (1) tattered drape hanging from the lower free edge near the pole (island 1)
    k0, k1 = int(0.58 * (len(sag) - 1)), int(0.86 * (len(sag) - 1))
    top = [np.array(sag[k0]) + (np.array(sag[k1]) - np.array(sag[k0])) * t for t in np.linspace(0, 1, 7)]
    nu, nv = 6, 5
    grid, uvg = [], []
    seed = rng.uniform(0, 100)
    for i in range(nv + 1):
        v = i / nv
        row, urow = [], []
        for j in range(nu + 1):
            u = j / nu
            L = 0.62 * (0.5 + 0.5 * math.sin(math.pi * (0.1 + 0.8 * u)) ** 0.8) * \
                (0.8 + 0.4 * (0.5 + 0.5 * noise.noise(Vector((u * 3.1, seed, 0.2)))))
            p = top[j] + np.array([0.0, -v * L])
            v3 = lift(top[j])
            v3 = Vector((v3.x + 0.03 * math.sin(math.pi * u) * v, -p[0], v3.z - v * L))
            row.append(v3)
            urow.append((0.5 + 0.5 * (0.03 + 0.94 * u), 0.5 * (0.03 + 0.94 * (1 - v))))
        grid.append(row)
        uvg.append(urow)
    keep = []
    for i in range(nv):
        for j in range(nu):
            h = noise.noise(Vector(((j + 0.5) / nu * 2.4 + seed, (i + 0.5) / nv * 2.4, 1.1)))
            if i > 0 and h > 0.45:
                continue
            keep.append((i, j))
    two_sided(bm, uvs, grid, keep, uvg, fdir)
    # (3) hub patch: a dense disc of silk round the hub (island 3, radial alpha)
    nseg, nr = 10, 2
    grid, uvg = [], []
    for i in range(nr + 1):
        rr = 0.56 * i / nr
        row, urow = [], []
        for j in range(nseg + 1):
            a_ = 2 * math.pi * j / nseg
            p = hub + rr * np.array([math.cos(a_), math.sin(a_)])
            v3 = lift(p) + Vector((0.006, 0, 0))
            row.append(v3)
            urow.append((0.5 + 0.25 * (1 + (i / nr) * math.cos(a_) * 0.94), 0.5 + 0.25 * (1 + (i / nr) * math.sin(a_) * 0.94)))
        grid.append(row)
        uvg.append(urow)
    two_sided(bm, uvs, grid, [(i, j) for i in range(nr) for j in range(nseg)], uvg, fdir)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new("WebSilk")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    uv = me.uv_layers.new(name="UVMap")
    data = []
    for lp in me.loops:
        data.extend(uvs[lp.vertex_index])
    uv.data.foreach_set("uv", data)
    return link(bpy.data.objects.new("WebSilk", me))


def silk_texture(size, path):
    """RGBA gauze atlas (2x2 islands; 0 = corner gauze tied along u=0 and v=1, 1 = hanging drape, 3 = radial hub
    patch) - after webs_spiders.silk_map / treekit.silk_texture."""
    rng = np.random.default_rng(5)
    n = size // 2
    atlas = np.zeros((size, size, 4), np.float32)
    uu = (np.arange(n) + 0.5) / n
    Uq, Vq = np.meshgrid(uu, uu)
    for isl in (0, 1, 3):
        fib = np.zeros((n, n), np.float32)
        nfib = 480
        for f in range(nfib):
            vertical = rng.random() < (0.7 if isl == 1 else 0.35)
            ang = (math.pi / 2 + rng.normal(0, 0.28)) if vertical else rng.uniform(0, math.pi)
            L = rng.uniform(25, 160)
            steps = int(L / 0.5)
            x, y = rng.uniform(0, n), rng.uniform(0, n)
            w = rng.uniform(0.3, 0.8)
            xs, ys = np.empty(steps), np.empty(steps)
            for st in range(steps):
                ang += rng.normal(0, 0.03)
                x += 0.5 * math.cos(ang)
                y += 0.5 * math.sin(ang)
                xs[st], ys[st] = x, y
            ok = (xs >= 0) & (xs < n - 1) & (ys >= 0) & (ys < n - 1)
            xs, ys = xs[ok], ys[ok]
            if len(xs) == 0:
                continue
            x0, y0 = np.floor(xs).astype(int), np.floor(ys).astype(int)
            fx, fy = xs - x0, ys - y0
            for dx, dy, ww in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy),
                               (1, 1, fx * fy)):
                np.add.at(fib, (y0 + dy, x0 + dx), ww * w)
        fib = np.clip(fib, 0, 1)
        sd = 100 + isl * 10
        film = 0.14 + 0.5 * mnoise(n, 3.0, sd, 4, aspect=(1.0, 0.5))
        holes = mnoise(n, 3.4, sd + 1, 3)
        keep = np.clip((0.66 - holes) / 0.07, 0, 1)
        film = film * keep
        fib = fib * (0.35 + 0.65 * keep)
        alpha = 1 - (1 - film) * (1 - fib)
        rag = mnoise(n, 7.0, sd + 2, 3)
        if isl == 1:
            edge = np.clip(np.minimum(Uq, 1 - Uq) / 0.13, 0, 1) * np.clip((Vq - 0.06 * rag) / 0.3, 0, 1)
        elif isl == 0:
            edge = np.clip((1 - Uq - 0.12 * rag) / 0.35, 0, 1) * np.clip((Vq - 0.12 * rag) / 0.35, 0, 1)
        else:
            rad = np.sqrt((Uq - 0.5) ** 2 + (Vq - 0.5) ** 2) * 2
            edge = np.clip((0.95 - rad - 0.15 * rag) / 0.45, 0, 1)
            film = np.maximum(film, 0.5 * np.clip(1 - rad / 0.7, 0, 1))
            alpha = 1 - (1 - film) * (1 - fib)
        alpha = np.clip(alpha * edge * 1.15, 0, 1)
        dust = np.clip((mnoise(n, 4.5, sd + 3, 4) - 0.45) * 2.2, 0, 1) * 0.6
        silk_c = np.array(srgb((228, 224, 216)))
        dust_c = np.array(srgb((150, 138, 120)))
        bright = np.array(srgb((248, 247, 244)))
        col = silk_c[None, None, :] * (1 - dust[..., None]) + dust_c[None, None, :] * dust[..., None]
        col = col * (1 - 0.5 * fib[..., None]) + bright[None, None, :] * 0.5 * fib[..., None]
        oy, ox = (isl // 2) * n, (isl % 2) * n
        atlas[oy:oy + n, ox:ox + n, :3] = col
        atlas[oy:oy + n, ox:ox + n, 3] = alpha
    return make_image("WebSilk_albedo", atlas, "sRGB", path)


def strand_maps(size, seed=29):
    """Planar colour + roughness map for the strands: silver-grey silk, dustier toward the frame / iron."""
    rng = np.random.default_rng(seed)
    n = size
    u = (np.arange(n) + 0.5) / n
    U, V = np.meshgrid(u, u)
    edge = np.clip(np.hypot(U - 0.48, V - 0.52) / 0.5, 0, 1) ** 2
    nz = mnoise(n, 4.0, seed, 4)
    dm = np.clip((nz - 0.45) * 2.0 * 0.6 + 0.8 * edge, 0, 1)
    sp = (rng.random((n, n)) > 0.993).astype(np.float32) * 0.35
    dm = np.clip(dm + sp * 0.6, 0, 1)
    hi = np.clip((mnoise(n, 8.0, seed + 1, 3) - 0.55) * 3, 0, 1) * (1 - dm)
    # round 2: one step greyer / silvery, dustier toward the iron (no white PVC look up close)
    base, dust, bright = srgb((205, 207, 214)), srgb((162, 156, 146)), srgb((236, 238, 244))
    col = np.zeros((n, n, 4), np.float32)
    for c in range(3):
        col[..., c] = (base[c] * (1 - dm) + dust[c] * dm) * (1 - 0.35 * hi) + bright[c] * 0.35 * hi
    col[..., 3] = 1
    rgh = np.zeros((n, n, 4), np.float32)
    r = 0.36 + 0.36 * dm
    for c in range(3):
        rgh[..., c] = r
    rgh[..., 3] = 1
    ci = make_image("Web_albedo", col, "sRGB", os.path.join(MAPS, "Web_albedo.png"), alpha=False)
    ri = make_image("Web_rough", rgh, "Non-Color", os.path.join(MAPS, "Web_rough.png"), alpha=False)
    return ci, ri


# ===================================================================== flat preview materials
def flat_mats():
    return dict(iron=mat_flat("PrevIron", lin((44, 46, 54)), rough=0.6),
                skin=mat_flat("PrevSkin", lin((236, 120, 22)), rough=0.5),
                flesh=mat_flat("PrevFlesh", lin((246, 196, 110)), rough=0.6),
                stem=mat_flat("PrevStem", lin((90, 96, 44)), rough=0.8),
                wax=mat_flat("PrevWax", lin((232, 210, 164)), rough=0.4),
                web=mat_flat("PrevWeb", lin((214, 216, 222)), rough=0.6))


# ===================================================================== assembly (lo + hi) in one scene
def place_pumpkin(pk, zc):
    """Rotate the local pumpkin 180 deg about Z (face -> -Y) and move it to the hanging axis at height zc."""
    M = Matrix.Translation((0.0, HANG_Y, zc)) @ Matrix.Rotation(math.pi, 4, "Z")
    for k, ob in pk.items():
        if hasattr(ob, "data") and getattr(ob, "type", "") == "MESH":
            ob.data.transform(M)
            ob.data.update()
    for k in ("wick_tip", "wick_top", "stem_tip"):
        pk[k] = M @ pk[k]
    return M


def assemble(hi_on):
    """Build every part. Returns dict with lo objects per part, hi objects per bake group, numbers."""
    rep = {}
    cv = crook_design()
    zs = cv["zs"]
    rep["crook"] = dict(a2=round(cv["a2"], 4), zs=round(zs, 4),
                        apex=[0.0, round(-cv["y"][cv["ia"]], 3), round(cv["z"][cv["ia"]], 3)],
                        cradle=[0.0, round(-cv["y"][cv["ic"]], 3), round(cv["z"][cv["ic"]], 3)],
                        outermost_y=round(-cv["y"].max(), 3), Rmax=round(float(cv["R"].max()), 3),
                        Rmin=round(float(cv["R"].min()), 3), length=round(float(cv["s"][-1]), 3))
    curl = cv["phi"] >= 180
    rep["crook"]["curl_across"] = round(float(cv["y"][curl].max() - cv["y"][curl].min()), 3)
    rep["crook"]["curl_wrap_deg"] = CROOK["W"]
    log("crook", rep["crook"])
    vc = volute_curve(cv)
    rep["volute"] = dict(C=[round(vc["C"][0], 3), round(vc["C"][1], 3)], rho0=round(vc["rho0"], 3), gaps=vc["gaps"])
    log("volute", rep["volute"])
    H = head_stack(cv)
    rep["stack"] = {k: round(v, 4) for k, v in H.items()}
    log("stack", rep["stack"])
    # ---------------- pumpkin (local first: envelope -> zc)
    pk = build_pumpkin(hi_on)
    env = pumpkin_envelope()
    zcl, rmax, zmin, zmax = env
    # top ring height in pumpkin-local coords: the envelope near r = 0.5 on the top side, + the strap gap
    top_side = zcl > 0.2
    z_at_05 = float(np.interp(0.5, rmax[top_side][::-1], zcl[top_side][::-1]))
    z_ring_local = z_at_05 + STRAP_GAP + 0.02
    zc = H["ring_z"] - z_ring_local
    rep["pumpkin"] = dict(zc=round(zc, 4), bottom=round(zc + zmin, 4), top_skin=round(zc + zmax, 4),
                          rmax=round(float(rmax.max()), 4), holes=pk["holes"], repair=pk.get("repair"))
    log("pumpkin", rep["pumpkin"])
    place_pumpkin(pk, zc)
    if hi_on:
        cut = pk["cut"]
    # ---------------- iron parts
    parts_lo, groups = {}, {}
    col_lo, _ = build_column(zs, False)
    feet_lo = build_feet(False)
    crook_lo, crook_info = build_crook(cv, False)
    vol_lo = build_volute(vc, False)
    bat_lo = build_bat_lo(cv)
    # one Post acc with material slots per bake group
    post = Acc(attrs=False)
    for gi, a in enumerate((col_lo, feet_lo, crook_lo, vol_lo, bat_lo)):
        _merge_acc(post, a, gi)
    rep["post_tris"] = dict(zip(("column", "feet", "crook", "volute", "bat"),
                                (a.tris() for a in (col_lo, feet_lo, crook_lo, vol_lo, bat_lo))))
    log("post tris", rep["post_tris"])
    cage_lo, cage_info = build_cage(cv, env, zc, H, False)
    rep["cage"] = dict(sauc_top=round(cage_info["sauc_top"], 4), collar=[round(x, 4) for x in cage_info["col"]],
                       drop_tip=round(cage_info["drop_tip"], 4))
    log("cage", rep["cage"])
    out = dict(cv=cv, vc=vc, H=H, pk=pk, env=env, zc=zc, rep=rep, cage_info=cage_info, crook_info=crook_info)
    out["post_acc"], out["cage_acc"] = post, cage_lo
    if hi_on:
        log("building hi parts ...")
        col_hi, rivets = build_column(zs, True)
        rivet_acc(rivets, col_hi)
        log("  column hi", col_hi.n, "verts")
        feet_hi = build_feet(True)
        crook_hi, _ = build_crook(cv, True)
        vol_hi = build_volute(vc, True)
        bat_hi = build_bat_hi(cv)
        cage_hi, _ = build_cage(cv, env, zc, H, True)
        log("  hi built")
        out["hi_accs"] = dict(column=col_hi, feet=feet_hi, crook=crook_hi, volute=vol_hi, bat=bat_hi, cage=cage_hi)
    return out


def _merge_acc(dst, src, mat):
    """Append src's verts / faces into dst with material index `mat` and a UV island shift."""
    base = dst.n
    for P in src.V:
        dst.add_v(P)
    shift = dst.new_island() * 40.0
    for idx, uv, m, sm in src.faces:
        dst.add_faces(idx + base, uv + shift, mat, sm)
    dst.isl += src.isl + 1


# ===================================================================== steps
def step_preview():
    """Lo geometry with flat colours: proportions, silhouettes, face, straps, web (wip renders)."""
    sc = fresh(samples=8)
    A = assemble(False)
    M = flat_mats()
    post = A["post_acc"].build("Post", mats=[M["iron"]])
    cage = A["cage_acc"].build("Cage", mats=[M["iron"]])
    pk = A["pk"]
    pk["lo"].data.materials.clear()
    for m in (M["skin"], M["flesh"], M["flesh"]):
        pk["lo"].data.materials.append(m)
    for k, m in (("stem_lo", M["stem"]), ("candle_lo", M["wax"]), ("puddle_lo", M["wax"]), ("wick_lo", M["iron"])):
        pk[k].data.materials.clear()
        pk[k].data.materials.append(m)
    pk["cut"].hide_render = True
    web, silk, winfo = build_web(A["cv"], A["vc"], A["H"])
    web.data.materials.append(M["web"])
    silk.data.materials.append(M["web"])
    rep = A["rep"]
    rep["web"] = winfo
    rep["tris"] = {"Post": A["post_acc"].tris(), "Cage": A["cage_acc"].tris(),
                   "Pumpkin": _tris_of_objs([pk["lo"], pk["stem_lo"], pk["candle_lo"], pk["wick_lo"], pk["puddle_lo"]]),
                   "Web": _tris_of_objs([web]), "WebSilk": _tris_of_objs([silk])}
    log("tris (approx, pumpkin before triangulation)", rep["tris"])
    objs = [post, cage, pk["lo"], pk["stem_lo"], pk["candle_lo"], pk["wick_lo"], pk["puddle_lo"], web, silk]
    bb = _bbox(objs)
    rep["bbox"] = bb
    log("bbox", bb)
    review_setup(res=(1200, 1000))
    ground(sc)
    tgt = Vector((0, -1.8, 9.0))
    out = []
    out.append(shoot_fov(os.path.join(WIP, "pv_front34_25.png"), _cam(tgt, (-0.57, -0.82), 25), tgt))
    out.append(shoot_fov(os.path.join(WIP, "pv_side_25.png"), _cam(tgt, (1, 0), 25), tgt))
    out.append(shoot_fov(os.path.join(WIP, "pv_front_25.png"), _cam(tgt, (0, -1), 25), tgt))
    head = Vector((0, HANG_Y, 13.6))
    out.append(shoot_fov(os.path.join(WIP, "pv_head_close.png"), head + Vector((-3.2, -5.5, -1.6)), head, lens=50))
    out.append(shoot_fov(os.path.join(WIP, "pv_head_below15.png"), Vector((0, HANG_Y - 14.0, 5.0)), head))
    crook = Vector((0, -1.9, 16.4))
    out.append(shoot_fov(os.path.join(WIP, "pv_crook_side.png"), crook + Vector((9, 0, -1.0)), crook, lens=50))
    out.append(shoot_fov(os.path.join(WIP, "pv_base.png"), Vector((-3.5, -5.0, 2.6)), Vector((0, 0, 1.0)), lens=40))
    # flat-black silhouette from +X at 40 studs (MUST 1)
    blk = mat_flat("Black", (0, 0, 0), rough=1.0)
    for o in bpy.context.scene.objects:
        if o.type == "MESH" and o.name not in ("Ground", "Path"):
            o.data.materials.clear()
            o.data.materials.append(blk)
        elif o.name in ("Ground", "Path"):
            o.hide_render = True
    w = sc.world.node_tree.nodes["Background"]
    w.inputs["Color"].default_value = (1, 1, 1, 1)
    w.inputs["Strength"].default_value = 1.0
    sc.view_settings.view_transform = "Standard"
    out.append(shoot_fov(os.path.join(WIP, "pv_silhouette_side_40.png"), _cam(tgt, (1, 0), 40), tgt))
    out.append(shoot_fov(os.path.join(WIP, "pv_silhouette_front34_40.png"), _cam(tgt, (-0.57, -0.82), 40), tgt))
    with open(os.path.join(WIP, "preview.json"), "w") as fh:
        json.dump(rep, fh, indent=1, default=float)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(WIP, "preview.blend"))
    return out


def _tris_of_objs(objs):
    return sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in objs)


def _bbox(objs):
    vs = np.vstack([np.array([o.matrix_world @ v.co for v in o.data.vertices]) for o in objs])
    return dict(min=[round(float(x), 3) for x in vs.min(0)], max=[round(float(x), 3) for x in vs.max(0)])


def _cam(tgt, dxy, dist, h=5.0):
    d = Vector((dxy[0], dxy[1], 0)).normalized()
    return Vector((tgt.x + d.x * dist, tgt.y + d.y * dist, h))


GREEN = (118, 199, 104)        # night-calibrated albedos (see calib): green ~ the hub floor, cream ~ the plaza paths
CREAM = (231, 222, 216)


def ground(sc, path_y=(-9.25, -1.25), size=400):
    g = mat_noise("Lawn", lin(GREEN), lin(tuple(int(c * 0.9) for c in GREEN)), nscale=0.35, detail=4, rough=0.9,
                  lo=0.3, hi=0.7)
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, -0.01))
    gr = bpy.context.active_object
    gr.name = "Ground"
    gr.data.materials.append(g)
    p = mat_noise("PathMat", lin(CREAM), lin(tuple(int(c * 0.95) for c in CREAM)), nscale=0.6, detail=3, rough=0.85,
                  lo=0.3, hi=0.7)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0.5 * (path_y[0] + path_y[1]), 0.0))
    pa = bpy.context.active_object
    pa.name = "Path"
    pa.scale = (size, path_y[1] - path_y[0], 1)
    pa.data.materials.append(p)
    return gr, pa



# ===================================================================== build / bake / web / export / verify
POST_GROUPS = ("column", "feet", "crook", "volute", "bat")
BAKE = {
    "Post": dict(tex="tex_big", ao=(0.55, 0.35), metal=True,
                 groups=[(g, cg) for g, cg in zip(POST_GROUPS, ((0.05, 0.10), (0.04, 0.08), (0.03, 0.07),
                                                                  (0.03, 0.06), (0.12, 0.25)))]),
    "Cage": dict(tex="tex_small", ao=(0.5, 0.2), metal=True,
                 groups=[(g, cg) for g, cg in zip(CAGE_GROUPS, ((0.03, 0.06), (0.03, 0.07), (0.025, 0.06),
                                                                  (0.025, 0.06), (0.03, 0.07)))]),
}


def pumpkin_seams_world():
    loc = pick_seams(PUMP["N"], PUMP["phase"], [48, 32], [25.0, 155.0, 270.0])
    return [round((a + 180.0) % 360.0, 4) for a in loc]


def world_verts(ob):
    me = ob.data
    co = np.empty(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    M = np.array(ob.matrix_world)
    return co @ M[:3, :3].T + M[:3, 3]


def bvh_faces(ob, keep_mat=None, drop_mat=None, drop_fn=None):
    me = ob.data
    V = [ob.matrix_world @ v.co for v in me.vertices]
    F = [tuple(p.vertices) for p in me.polygons
         if (keep_mat is None or p.material_index in keep_mat) and (drop_mat is None or p.material_index not in drop_mat)
         and (drop_fn is None or not drop_fn(p))]
    return BVHTree.FromPolygons(V, F, all_triangles=False)


def nearest(bvh, P):
    best, where = 1e9, None
    for p in P:
        h = bvh.find_nearest(Vector(tuple(float(x) for x in p)))
        if h[0] is not None and h[3] < best:
            best, where = h[3], [round(float(x), 3) for x in p]
    return round(best, 4), where


def rot_about_axis(P, k):
    a = math.radians(90.0 * k)
    c, s_ = math.cos(a), math.sin(a)
    Q = np.asarray(P, float).copy()
    x, y = Q[:, 0] - 0.0, Q[:, 1] - HANG_Y
    Q[:, 0], Q[:, 1] = c * x - s_ * y, HANG_Y + s_ * x + c * y
    return Q


def smooth_shell_normals(lo, zc):
    """Give the carved Skin / Inner corners the smooth normals of the UNCUT lo shells (barycentric on the uncut
    grid). The boolean leaves sliver triangles round the face holes whose own vertex normals bend the shading
    (light/dark wedges at close range); with the uncut normals the shading is what the clean shell would give."""
    from mathutils.bvhtree import BVHTree
    from mathutils.interpolate import poly_3d_calc
    M = Matrix.Translation((0.0, HANG_Y, zc)) @ Matrix.Rotation(math.pi, 4, "Z")
    pl = dict(SKIN)
    tmp = bpy.data.materials.new("RefTmp")
    refs = {"Skin": sphere_surface(egg_field(dict(PUMP, micro=0.0), pl), 48, 18) + (0, 1.0),
            "Inner": sphere_surface(egg_field(inner_params(PUMP, SHELL), pl), 28, 8, flip=True) + (0, 0.0)}
    me = lo.data
    names = [m.name for m in me.materials]
    cn = np.array([c.vector[:] for c in me.corner_normals], float)
    cv_ = np.zeros(len(me.loops), int)
    me.loops.foreach_get("vertex_index", cv_)
    co = np.array([v.co[:] for v in me.vertices])
    stats = {}
    for nm, part in refs.items():
        ref = build_mesh("Ref" + nm, [part], [tmp])
        ref.data.transform(M)
        triangulate(ref)
        rv = [v.co.copy() for v in ref.data.vertices]
        rn = [v.normal.copy() for v in ref.data.vertices]
        tris = [tuple(p.vertices) for p in ref.data.polygons]
        bvh = BVHTree.FromPolygons(rv, tris)
        mi = names.index(nm)
        dmax, nchg, cache = 0.0, 0, {}
        for p in me.polygons:
            if p.material_index != mi:
                continue
            for li in p.loop_indices:
                vi = int(cv_[li])
                if vi not in cache:
                    loc, _, ti, dist = bvh.find_nearest(Vector(co[vi]))
                    a, b, c = (rv[i] for i in tris[ti])
                    w = poly_3d_calc([a, b, c], loc)
                    n = sum((rn[i] * wi for i, wi in zip(tris[ti], w)), Vector())
                    cache[vi] = n.normalized()
                    dmax = max(dmax, dist)
                n = cache[vi]
                nchg += 1
                cn[li] = n[:]
        stats[nm] = dict(corners=nchg, max_dist=round(dmax, 4))
        bpy.data.objects.remove(ref)
    me.normals_split_custom_set([tuple(n) for n in cn])
    bpy.data.materials.remove(tmp)
    return stats


def column_creases(post, ang=44.0):
    """Round 2 (NICE 7): split the lo normals at the real creases of the column (collar chamfers, the base neck,
    plinth steps; not the twist). Without them the long pole bands inherit a tilted normal from the collar chamfer
    and the bake shows diagonal streaks on the collar's top edge."""
    bm = bmesh.new()
    bm.from_mesh(post.data)
    n = 0
    for e in bm.edges:
        lf = e.link_faces
        if len(lf) != 2 or lf[0].material_index != 0 or lf[1].material_index != 0:
            continue
        z = 0.5 * (e.verts[0].co.z + e.verts[1].co.z)
        if TWIST["z0"] + 0.02 < z < TWIST["z1"] - 0.02:
            continue
        if math.degrees(e.calc_face_angle(0.0)) > ang:
            e.smooth = False
            n += 1
    bm.to_mesh(post.data)
    bm.free()
    return n


def step_build():
    R = RES()
    fresh(samples=R["samples"])
    A = assemble(True)
    rep = A["rep"]
    pk, H, zc = A["pk"], A["H"], A["zc"]
    ironhi = mat_iron_hi("IronHi")
    # ---- Post
    post = A["post_acc"].build("Post", mats=[bpy.data.materials.new("PostG_" + g) for g in POST_GROUPS])
    triangulate(post)
    rep["column_sharp_edges"] = column_creases(post)
    pack_uv(post)
    for g in POST_GROUPS:
        A["hi_accs"][g].build("Hi_Post_" + g, mats=[ironhi])
    # ---- Cage
    cage = A["cage_acc"].build("Cage", mats=[bpy.data.materials.new("CageG_" + g) for g in CAGE_GROUPS])
    triangulate(cage)
    pack_uv(cage)
    for g in CAGE_GROUPS:
        A["hi_accs"]["cage"][g].build("Hi_Cage_" + g, mats=[ironhi])
    # ---- Pumpkin lo: shell + stem + candle + wick + puddle -> one object
    lo = join([pk["lo"], pk["stem_lo"], pk["candle_lo"], pk["wick_lo"], pk["puddle_lo"]], "Pumpkin")
    triangulate(lo)
    strip_colors(lo)
    for at in list(lo.data.attributes):
        if at.name in ("Depth", "RimD"):
            lo.data.attributes.remove(at)
    seams = pumpkin_seams_world()
    nseam = uv_layout(lo, seams, {"Skin", "Inner"}, {"Inner": 0.55, "WaxMat": 0.6, "WickMat": 0.6},
                      centre_xy=(0.0, HANG_Y))
    rep["pumpkin_uv"] = dict(seams=seams, seam_edges=nseam)
    rep["pumpkin_normals"] = smooth_shell_normals(lo, zc)
    log("pumpkin smooth shell normals", rep["pumpkin_normals"])
    for k_, nm in (("hi", "Hi_Pumpkin"), ("stem_hi", "Hi_Stem"), ("candle_hi", "Hi_Candle"), ("wick_hi", "Hi_Wick"),
                   ("puddle_hi", "Hi_Puddle")):
        pk[k_].name = nm
    pk["cut"].name = "Cutter"
    pk["cut"].hide_render = True
    pk["cut"].hide_viewport = True
    if pk["repair"][1] != 0:
        raise RuntimeError("repair_attrs left %d vertices" % pk["repair"][1])
    # ---- triangle budgets
    tris = {"Post": len(post.data.polygons), "Cage": len(cage.data.polygons), "Pumpkin": len(lo.data.polygons)}
    rep["tris"] = tris
    log("tris", tris)
    for k_, v in tris.items():
        if v > BUDGET[k_]:
            raise RuntimeError("%s has %d tris > %d" % (k_, v, BUDGET[k_]))
    # ---- texel density
    rep["texel_px_per_stud"] = {o.name: round(texel_density(o, s_)[0], 1)
                                for o, s_ in ((post, R["tex_big"]), (cage, R["tex_small"]), (lo, R["tex_big"]))}
    log("texel", rep["texel_px_per_stud"])
    # ---- clearances
    chk = {}
    zb = rep["pumpkin"]["bottom"]
    skin = world_verts(bpy.data.objects["Hi_Pumpkin"])
    skin = skin[skin[:, 2] > zb + 0.10][::3]
    stem = world_verts(bpy.data.objects["Hi_Stem"])[::2]
    # the seat zone (saucer, collar, drop finial and the strap ends converging under the saucer) is exempt
    cb = bvh_faces(cage, drop_mat={CAGE_GROUPS.index("seat")},
                   drop_fn=lambda p: (p.center.z < zb + 0.02 and math.hypot(p.center.x, p.center.y - HANG_Y) < 0.66))
    for k_ in range(4):
        chk["pumpkin_skin_vs_cage_rot%d" % (90 * k_)] = nearest(cb, rot_about_axis(skin, k_))
        chk["stem_vs_cage_rot%d" % (90 * k_)] = nearest(cb, rot_about_axis(stem, k_))
    pb = bvh_faces(post)
    cv_ = world_verts(cage)
    vm = np.zeros(len(cv_), np.int64)
    for poly in cage.data.polygons:
        vm[list(poly.vertices)] = poly.material_index
    away = cv_[(vm != CAGE_GROUPS.index("ring_l2")) & (vm != CAGE_GROUPS.index("link1"))][::2]
    chk["cage_vs_post"] = nearest(pb, away)
    chk["link1_vs_post"] = nearest(pb, cv_[vm == CAGE_GROUPS.index("link1")])
    O, ra = bat_frame(A["cv"])
    pv = world_verts(post)
    pm = np.zeros(len(pv), np.int64)
    for poly in post.data.polygons:
        pm[list(poly.vertices)] = poly.material_index
    wings = pv[(pm == POST_GROUPS.index("bat")) & (np.abs(pv[:, 1] - O[1]) > 0.16)]
    crb = bvh_faces(post, keep_mat={POST_GROUPS.index("crook")})
    chk["bat_wings_vs_crook"] = nearest(crb, wings)
    rep["clearance"] = chk
    log("clearance", chk)
    bad = [k_ for k_, v in chk.items() if (k_.startswith(("pumpkin", "stem")) and v[0] < 0.30) or
           (k_ == "cage_vs_post" and v[0] < 0.40) or (k_ == "link1_vs_post" and v[0] < 0.004) or
           (k_ == "bat_wings_vs_crook" and v[0] < 0.035)]
    if bad:
        log("CLEARANCE FAIL", bad)
        rep["clearance_fail"] = bad
    # ---- attachment points (Blender object space = world; every object keeps the FBX origin)
    itop, ibot = pk["itop"], pk["ibot"]
    wt = pk["wick_top"]
    att = {
        "wick_tip": [round(v, 3) for v in pk["wick_tip"]],
        "wick_top": [round(v, 3) for v in wt],
        "flame_centre": [round(wt.x, 3), round(wt.y, 3), round(wt.z + 0.05, 3)],
        "cavity_centre": [0.0, HANG_Y, round(zc + 0.5 * (itop + ibot), 3)],
        "cavity_floor": [0.0, HANG_Y, round(zc + ibot, 3)],
        "suggested_pointlight": [round(wt.x, 3), round(wt.y, 3), round(wt.z + 0.06, 3)],
        "ground_light": [0.0, HANG_Y, round(A["cage_info"]["col"][0] - 0.03, 3)],
        "chain_top": [0.0, HANG_Y, round(H["chain_top"], 3)],
        "pumpkin_pivot": [0.0, HANG_Y, round(zc, 3)],
        "bat_perch": [round(float(x), 3) for x in O],
    }
    rep["attach"] = att
    log("attach", att)
    for o in (post, cage, lo):
        o.hide_render = False
    with open(os.path.join(OUT, "build.json"), "w") as fh:
        json.dump(rep, fh, indent=1, default=float)
    bpy.ops.wm.save_as_mainfile(filepath=SRC)
    return rep


def _hide_for_bake():
    for o in bpy.context.scene.objects:
        if o.type != "MESH":
            continue
        o.hide_render = not o.name.startswith("Hi_")
    bpy.data.objects["Hi_Pumpkin"].hide_render = True       # its split copies take its place


def step_bake(part):
    R = RES()
    bpy.ops.wm.open_mainfile(filepath=SRC)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = R["samples"]
    lo = bpy.data.objects[part]
    groups, made = [], []
    hp = bpy.data.objects["Hi_Pumpkin"]
    hk = {"Skin": "HiSplit_Skin", "Flesh": "HiSplit_Wall", "Inner": "HiSplit_Inner"}
    hs_ = {v: split_copy(hp, v, (lambda n_: lambda f, nm: nm[f.material_index] == n_)(k)) for k, v in hk.items()}
    his_split = list(hs_.values())
    _hide_for_bake()
    for o in his_split:
        o.hide_render = False
    if part == "Pumpkin":
        # round 2: AO strength per group - the cavity seen through the holes must stay bright (<= 0.2)
        defs = [("LoSkin", ("Skin", "StemMat"), [hs_["HiSplit_Skin"], bpy.data.objects["Hi_Stem"]], 0.04, 0.09, 0.5),
                ("LoWall", ("Flesh",), [hs_["HiSplit_Wall"]], 0.03, 0.07, 0.15),
                ("LoInner", ("Inner",), [hs_["HiSplit_Inner"]], 0.04, 0.09, 0.08),
                ("LoWax", ("WaxMat",), [bpy.data.objects["Hi_Candle"], bpy.data.objects["Hi_Puddle"]], 0.035, 0.08,
                 0.3),
                ("LoWick", ("WickMat",), [bpy.data.objects["Hi_Wick"]], 0.012, 0.03, 0.3)]
        for nm, mats, his, cage_, maxray, ao_g in defs:
            o = split_copy(lo, nm, (lambda ms: lambda f, names: names[f.material_index] in ms)(mats))
            made.append(o)
            groups.append((o, his, cage_, maxray, ao_g))
        size, ao, metal = R["tex_big"], (0.5, 0.25), False
    else:
        cfg = BAKE[part]
        prefix = "Hi_Post_" if part == "Post" else "Hi_Cage_"
        for gi, (g, (cage_, maxray)) in enumerate(cfg["groups"]):
            o = split_copy(lo, "Lo_" + g, (lambda i: lambda f, names: f.material_index == i)(gi))
            made.append(o)
            groups.append((o, [bpy.data.objects[prefix + g]], cage_, maxray))
        size, ao, metal = R[cfg["tex"]], cfg["ao"], cfg["metal"]
    lo.hide_render = True
    imgs = bake_groups(groups, size, part, ao[0], ao[1], metal=metal, ss=2,
                       ids_path=os.path.join(WIP, part + "_ids.png"))
    for o in made + his_split:
        bpy.data.objects.remove(o)
    lo.hide_render = False
    pbr_material(lo, part + "_PBR", imgs)
    info = dict(part=part, size=size, stats=imgs["stats"],
                albedo_mean_srgb=albedo_mean(os.path.join(MAPS, part + "_albedo.png")))
    log("bake", info)
    with open(os.path.join(OUT, "bake_%s.json" % part.lower()), "w") as fh:
        json.dump(info, fh, indent=1)
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            o.hide_render = o.name.startswith("Hi_") or o.name == "Cutter"
    bpy.ops.wm.save_as_mainfile(filepath=SRC)
    return info


def albedo_mean(path):
    img = bpy.data.images.load(path, check_existing=False)
    a = np.empty(img.size[0] * img.size[1] * 4, np.float32)
    img.pixels.foreach_get(a)
    a = a.reshape(-1, 4)[:, :3]
    nz = a[a.sum(1) > 0.003]
    out = [round(float(x) * 255, 1) for x in nz.mean(0)]
    bpy.data.images.remove(img)
    return out


def step_web():
    R = RES()
    bpy.ops.wm.open_mainfile(filepath=SRC)
    for nm in ("Web", "WebSilk"):
        if nm in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[nm])
    cv = crook_design()
    vc = volute_curve(cv)
    H = head_stack(cv)
    web, silk, info = build_web(cv, vc, H)
    ci, ri = strand_maps(R["tex_small"])
    web.data.materials.append(mat_tex("Web_Mat", ci, ri, rough=0.6))
    simg = silk_texture(R["tex_small"], os.path.join(MAPS, "WebSilk_albedo.png"))
    silk.data.materials.append(mat_tex("WebSilk_Mat", simg, None, alpha=True, rough=0.8))
    for o in (web, silk):
        o.visible_shadow = False
    wv = world_verts(web)
    info["tris"] = {"Web": _tris_of_objs([web]), "WebSilk": _tris_of_objs([silk])}
    info["strand_bbox"] = dict(y=[round(float(wv[:, 1].min()), 3), round(float(wv[:, 1].max()), 3)],
                               z=[round(float(wv[:, 2].min()), 3), round(float(wv[:, 2].max()), 3)])
    info["strand_span"] = dict(y=round(float(wv[:, 1].max() - wv[:, 1].min()), 3),
                               z=round(float(wv[:, 2].max() - wv[:, 2].min()), 3))
    cage = bpy.data.objects["Cage"]
    cb = bvh_faces(cage)
    info["web_vs_cage"] = nearest(cb, wv[::2])
    info["silk_vs_cage"] = nearest(cb, world_verts(silk))
    pb = bvh_faces(bpy.data.objects["Pumpkin"])
    info["web_vs_pumpkin"] = nearest(pb, wv[::2])
    log("web", info)
    for nm, lim in (("Web", BUDGET["Web"]), ("WebSilk", BUDGET["WebSilk"])):
        if info["tris"][nm] > lim:
            raise RuntimeError("%s over budget" % nm)
    with open(os.path.join(OUT, "web.json"), "w") as fh:
        json.dump(info, fh, indent=1, default=float)
    bpy.ops.wm.save_as_mainfile(filepath=SRC)
    return info


FINAL_NAMES = ("Post", "Cage", "Pumpkin", "Web", "WebSilk")


def step_export():
    bpy.ops.wm.open_mainfile(filepath=SRC)
    objs = [bpy.data.objects[n] for n in FINAL_NAMES]
    for o in objs:
        o.hide_render = False
        o.hide_viewport = False
        o.hide_set(False)
    with open(os.path.join(OUT, "build.json")) as fh:
        rep = json.load(fh)
    with open(os.path.join(OUT, "web.json")) as fh:
        web = json.load(fh)
    tris = {o.name: _tris_of_objs([o]) for o in objs}
    total = sum(tris.values())
    if total > TOTAL_CAP or any(v > 8000 for v in tris.values()):
        raise RuntimeError("budget: %s total %d" % (tris, total))
    allv = np.vstack([world_verts(o) for o in objs])
    pv = world_verts(objs[0])
    base = pv[pv[:, 2] < 1.0]
    sizes = {}
    for o in objs:
        w = world_verts(o)
        mn, mx = w.min(0), w.max(0)
        sizes[o.name] = dict(size=[round(float(x), 3) for x in mx - mn], min=[round(float(x), 3) for x in mn],
                             max=[round(float(x), 3) for x in mx], centre=[round(float(x), 3) for x in (mn + mx) / 2])
    chk = dict(min_z=round(float(allv[:, 2].min()), 4), height=round(float(allv[:, 2].max()), 3),
               footprint=[round(float(base[:, 0].max() - base[:, 0].min()), 3),
                          round(float(base[:, 1].max() - base[:, 1].min()), 3)],
               reach_iron=round(float(-pv[:, 1].min()), 3),
               lowest_head=round(float(world_verts(objs[1])[:, 2].min()), 3))
    if chk["min_z"] < -0.05:
        raise RuntimeError("geometry below the ground: %s" % chk["min_z"])
    if max(chk["footprint"]) > 2.6:
        raise RuntimeError("footprint %s" % chk["footprint"])
    res = export_fbx(objs, FBX)
    out = dict(fbx=FBX, kb=res["kb"], tris=tris, total=total, sizes=sizes, checks=chk, attach=rep["attach"],
               clearance=rep["clearance"], web=web)
    log("export", json.dumps(out, default=float)[:2000])
    with open(os.path.join(OUT, "export.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    bpy.ops.wm.save_as_mainfile(filepath=SRC)
    for o in list(bpy.data.objects):
        if o.name not in FINAL_NAMES:
            bpy.data.objects.remove(o)
    bpy.ops.wm.save_as_mainfile(filepath=FINAL)
    return out


def import_lamp(path=FBX):
    """Import the FBX and bake its 0.01 object scale into the meshes (studs, identity transforms)."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    objs = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    for o in objs:
        M = o.matrix_world.copy()
        o.data.transform(Matrix.Scale(100.0, 4) @ M)
        o.matrix_world = Matrix.Identity(4)
    for o in [o for o in bpy.data.objects if o not in before and o.type != "MESH"]:
        bpy.data.objects.remove(o)
    return {o.name.split(".")[0]: o for o in objs}


def step_verify():
    fresh(4)
    objs = import_lamp()
    rep = {}
    for nm, o in objs.items():
        me = o.data
        imgs = []
        for m in me.materials:
            if m and m.use_nodes:
                for n in m.node_tree.nodes:
                    if n.type == "TEX_IMAGE" and n.image:
                        im = n.image
                        a = np.empty(im.size[0] * im.size[1] * 4, np.float32)
                        im.pixels.foreach_get(a)
                        al = a.reshape(-1, 4)[:, 3]
                        sock = [l.to_socket.name for l in m.node_tree.links if l.from_node == n]
                        imgs.append(dict(name=im.name, size=list(im.size), packed=im.packed_file is not None,
                                         linked_to=sock, alpha=[round(float(al.min()), 3), round(float(al.max()), 3),
                                                                round(float(al.mean()), 3)]))
        w = world_verts(o)
        rep[nm] = dict(tris=_tris_of_objs([o]), images=imgs, min=[round(float(x), 3) for x in w.min(0)],
                       max=[round(float(x), 3) for x in w.max(0)], object_scale_on_import=0.01)
    pk = objs.get("Pumpkin")
    if pk:
        lab = components(pk)
        me = pk.data
        ev = np.empty(len(me.edges) * 2, np.int64)
        me.edges.foreach_get("vertices", ev)
        ev = ev.reshape(-1, 2)
        comps = {}
        for c in np.unique(lab):
            vs = lab == c
            ne = int(vs[ev[:, 0]].sum())
            nf = sum(1 for p in me.polygons if vs[p.vertices[0]])
            comps[int(c)] = (int(vs.sum()), ne, nf)
        big = max(comps.values(), key=lambda t: t[0])
        chi = big[0] - big[1] + big[2]
        rep["pumpkin_shell"] = dict(components=len(comps), euler=chi, holes=(4 - chi) / 2)
    rep["total_tris"] = sum(v["tris"] for k, v in rep.items() if isinstance(v, dict) and "tris" in v)
    log("verify", json.dumps(rep)[:3000])
    with open(os.path.join(OUT, "verify.json"), "w") as fh:
        json.dump(rep, fh, indent=1)
    return rep


# ===================================================================== lighting: night calibration + review
NIGHT_TARGET = {"green": (93, 159, 88), "cream": (184, 177, 185)}
CALIB = os.path.join(OUT, "calib.json")
IN_LIGHT_COL = lin((255, 150, 60))
SPOT_COL = lin((255, 176, 104))


def night_world(sc, L, moon_strength, moon_col, sky_cam=True):
    """World: L lights the scene; camera rays see a dark-blue starry sky. A cool moon sun gives the shadows."""
    w = sc.world
    w.use_nodes = True
    nt = w.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg_l = nt.nodes.new("ShaderNodeBackground")
    bg_l.inputs["Color"].default_value = (*L, 1)
    bg_l.inputs["Strength"].default_value = 1.0
    if sky_cam:
        tc = nt.nodes.new("ShaderNodeTexCoord")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position = 0.0
        ramp.color_ramp.elements[0].color = (*lin((58, 72, 138)), 1)
        ramp.color_ramp.elements[1].position = 0.55
        ramp.color_ramp.elements[1].color = (*lin((16, 22, 62)), 1)
        nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
        vor = nt.nodes.new("ShaderNodeTexVoronoi")
        vor.inputs["Scale"].default_value = 260.0
        nt.links.new(tc.outputs["Generated"], vor.inputs["Vector"])
        st = nt.nodes.new("ShaderNodeMapRange")
        st.inputs["From Min"].default_value = 0.06
        st.inputs["From Max"].default_value = 0.0
        st.inputs["To Max"].default_value = 0.9
        nt.links.new(vor.outputs["Distance"], st.inputs["Value"])
        add = nt.nodes.new("ShaderNodeMix")
        add.data_type = "RGBA"
        add.blend_type = "ADD"
        add.inputs["Factor"].default_value = 1.0
        nt.links.new(ramp.outputs["Color"], add.inputs["A"])
        nt.links.new(st.outputs["Result"], add.inputs["B"])
        bg_s = nt.nodes.new("ShaderNodeBackground")
        nt.links.new(add.outputs["Result"], bg_s.inputs["Color"])
        lp = nt.nodes.new("ShaderNodeLightPath")
        mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs["Fac"])
        nt.links.new(bg_l.outputs["Background"], mx.inputs[1])
        nt.links.new(bg_s.outputs["Background"], mx.inputs[2])
        nt.links.new(mx.outputs["Shader"], out.inputs["Surface"])
    else:
        nt.links.new(bg_l.outputs["Background"], out.inputs["Surface"])
    for o in [o for o in sc.objects if o.type == "LIGHT" and o.name.startswith("Sun")]:
        bpy.data.objects.remove(o)
    ld = bpy.data.lights.new("SunMoon", "SUN")
    ld.energy, ld.color = moon_strength, moon_col
    ld.angle = math.radians(1.5)
    mo = link(bpy.data.objects.new("SunMoon", ld))
    mo.rotation_euler = (math.radians(40), 0, math.radians(-35))
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0.0
    return mo


def _read_png(path):
    img = bpy.data.images.load(path, check_existing=False)
    a = np.empty(img.size[0] * img.size[1] * 4, np.float32)
    img.pixels.foreach_get(a)
    a = a.reshape(img.size[1], img.size[0], 4)
    bpy.data.images.remove(img)
    return a


def _tolin(v):
    v = np.asarray(v, float) / 255.0
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def step_calib():
    """Fit the night world + moon so a plain green plane and a cream patch render as the in-game Moonlit night
    (green ~ (93,159,88), cream ~ (184,177,185) sRGB)."""
    sc = fresh(8)
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.dither_intensity = 0.0
    sc.render.resolution_x, sc.render.resolution_y = 64, 32
    gm = mat_flat("G", lin(GREEN), rough=0.9)
    cm = mat_flat("C", lin(CREAM), rough=0.9)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(-0.5, 0, 0))
    bpy.context.active_object.data.materials.append(gm)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0.5, 0, 0))
    bpy.context.active_object.data.materials.append(cm)
    cd = bpy.data.cameras.new("Cam")
    cd.type = "ORTHO"
    cd.ortho_scale = 2.0
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = (0, 0, 5)
    sc.camera = cam
    E = np.array([0.60, 0.60, 0.70])
    moon_col = np.array([0.80, 0.86, 1.0])
    moon_frac = 0.38
    cosz = math.cos(math.radians(40))
    hist = []

    def setup(E):
        L = E * (1 - moon_frac)
        S = float((E * moon_frac)[2] * math.pi / (moon_col[2] * cosz))
        mcol = (E * moon_frac) * math.pi / (S * cosz)
        return L, S, mcol
    for it in range(5):
        L, S, mcol = setup(E)
        night_world(sc, tuple(L), S, tuple(np.clip(mcol, 0, 10)), sky_cam=False)
        path = os.path.join(WIP, "calib_%d.png" % it)
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        a = _read_png(path)
        gpx = a[8:24, 6:26, :3].reshape(-1, 3).mean(0)
        cpx = a[8:24, 38:58, :3].reshape(-1, 3).mean(0)
        meas = {"green": [round(float(x) * 255, 1) for x in gpx], "cream": [round(float(x) * 255, 1) for x in cpx]}
        hist.append(dict(E=[round(float(x), 4) for x in E], measured=meas))
        log("calib", it, hist[-1])
        err = float(np.abs(np.array(meas["green"]) - NIGHT_TARGET["green"]).sum() +
                    np.abs(np.array(meas["cream"]) - NIGHT_TARGET["cream"]).sum())
        hist[-1]["err"] = round(err, 2)
        rg = _tolin(NIGHT_TARGET["green"]) / np.maximum(_tolin(meas["green"]), 1e-4)
        rc = _tolin(NIGHT_TARGET["cream"]) / np.maximum(_tolin(meas["cream"]), 1e-4)
        E = E * np.sqrt(rg * rc)
    best = min(hist, key=lambda h: h["err"])
    E = np.array(best["E"])
    L, S, mcol = setup(E)
    final = dict(E=[float(x) for x in E], best=best, moon_frac=moon_frac, moon_col=[float(x) for x in moon_col], history=hist,
                 target=NIGHT_TARGET, albedo_green=GREEN, albedo_cream=CREAM, world_L=[float(x) for x in L],
                 moon_strength=S, moon_rgb=[float(x) for x in mcol])
    with open(CALIB, "w") as fh:
        json.dump(final, fh, indent=1)
    return final


def apply_night(sc, darker=1.0):
    with open(CALIB) as fh:
        cal = json.load(fh)
    L = np.array(cal["world_L"]) * darker
    night_world(sc, tuple(L), cal["moon_strength"] * darker, tuple(cal["moon_rgb"]))
    sc.render.engine = "BLENDER_EEVEE"


def lamp_lights(att, energy_in, energy_spot, offset=(0, 0, 0), rot_k=0):
    off = Vector(offset)
    pl = Vector(att["suggested_pointlight"])
    ft = Vector(att["flame_centre"])
    if rot_k:
        pl = Vector(rot_about_axis(np.array([tuple(pl)]), rot_k)[0])
        ft = Vector(rot_about_axis(np.array([tuple(ft)]), rot_k)[0])
    out = [point("InLight", pl + off, energy_in, col=IN_LIGHT_COL, radius=0.06, shadow=True),
           spot("GroundSpot", Vector(att["ground_light"]) + off, energy_spot, 110.0, SPOT_COL, blend=0.75),
           flame("Flame", ft + off + Vector((0, 0, 0.02)), 0.05, 0.13, 30.0)]
    return out


def rotate_pumpkin(ob, k):
    a = math.radians(90.0 * k)
    M = Matrix.Translation((0, HANG_Y, 0)) @ Matrix.Rotation(a, 4, "Z") @ Matrix.Translation((0, -HANG_Y, 0))
    ob.matrix_world = M @ ob.matrix_world


def review_scene(night, energy_in, energy_spot, darker=1.0):
    sc = fresh(16)
    review_setup(res=(1600, 1200))
    sc.eevee.taa_render_samples = 64
    objs = import_lamp()
    for o in objs.values():
        for m in o.data.materials:
            if m:
                m.use_backface_culling = True
    for m in objs["WebSilk"].data.materials:
        try:
            m.surface_render_method = "BLENDED"
        except Exception:
            pass
    for nm in ("Web", "WebSilk"):
        objs[nm].visible_shadow = False
    ground(sc)
    if night:
        apply_night(sc, darker)
    with open(os.path.join(OUT, "build.json")) as fh:
        att = json.load(fh)["attach"]
    lamp_lights(att, energy_in, energy_spot)
    return sc, objs, att


def _turn_lamp_lights(sc, k):
    for o in [o for o in sc.objects if o.name.startswith(("InLight", "Flame"))]:
        o.location = Vector(rot_about_axis(np.array([tuple(o.location)]), k)[0])


def shots_lamp(sc, objs, night):
    tgt = Vector((0, -1.8, 9.0))
    head = Vector((0, HANG_Y, 13.35))
    out = []
    tag = "night" if night else "day"
    out.append(shoot_fov(os.path.join(OUT, "review_%s_25.png" % tag), _cam(tgt, (-0.57, -0.82), 25), tgt))
    out.append(shoot_fov(os.path.join(OUT if not night else WIP, "review_%s_25_side.png" % tag), _cam(tgt, (1, 0), 25),
                         tgt))
    if not night:
        out.append(shoot_fov(os.path.join(OUT, "review_day_50.png"), _cam(tgt, (-0.57, -0.82), 50), tgt))
        out.append(shoot_fov(os.path.join(WIP, "rv_day_40_front.png"), _cam(tgt, (0, -1), 40), tgt))
        out.append(shoot_fov(os.path.join(WIP, "rv_day_40_side.png"), _cam(tgt, (1, 0), 40), tgt))
        out.append(shoot_fov(os.path.join(WIP, "rv_day_25_back.png"), _cam(tgt, (0.3, 1), 25), tgt))
        out.append(shoot_fov(os.path.join(OUT, "review_close_head.png"), head + Vector((-3.4, -5.6, -1.8)), head, lens=50))
        out.append(shoot_fov(os.path.join(WIP, "rv_head_below12.png"), Vector((1.5, HANG_Y - 11.0, 5.0)), head))
        out.append(shoot_fov(os.path.join(WIP, "rv_base_5.png"), Vector((-2.6, -4.2, 3.2)), Vector((0, 0, 1.1)), lens=40))
        crook = Vector((0, -1.9, 16.4))
        out.append(shoot_fov(os.path.join(WIP, "rv_crook_8.png"), crook + Vector((8.0, -0.5, -1.5)), crook, lens=45))
        out.append(shoot_fov(os.path.join(WIP, "rv_twist_4.png"), Vector((2.4, -3.0, 7.0)), Vector((0, 0, 7.2)), lens=45))
    else:
        out.append(shoot_fov(os.path.join(OUT, "review_night_close.png"), head + Vector((-3.4, -5.6, -1.8)), head,
                             lens=50))
    rotate_pumpkin(objs["Pumpkin"], 1)
    _turn_lamp_lights(sc, 1)
    out.append(shoot_fov(os.path.join(OUT, "review_%s_25_side_face.png" % tag), _cam(tgt, (1, 0), 25), tgt))
    out.append(shoot_fov(os.path.join(WIP, "rv_%s_head_side_face.png" % tag), head + Vector((7.0, -1.0, -1.6)), head,
                         lens=50))
    rotate_pumpkin(objs["Pumpkin"], -1)
    _turn_lamp_lights(sc, -1)
    return out


def path_of_lamps(sc, objs, att, energy_in, energy_spot, tag):
    """3 lamps 16 studs apart along the path, faces turned along the path toward the camera (+X)."""
    rotate_pumpkin(objs["Pumpkin"], 1)
    for o in [o for o in sc.objects if o.name.startswith(("InLight", "Flame", "GroundSpot"))]:
        bpy.data.objects.remove(o)
    for dx in (-16.0, 0.0, 16.0):
        if dx != 0.0:
            for nm, o in objs.items():
                c = o.copy()
                link(c)
                c.matrix_world = Matrix.Translation((dx, 0, 0)) @ o.matrix_world
        lamp_lights(att, energy_in, energy_spot, offset=(dx, 0, 0), rot_k=1)
    cam = Vector((44.0, -5.25, 5.0))
    tgt = Vector((0.0, -3.0, 9.0))
    return shoot_fov(os.path.join(OUT, "review_%s_path_3lamps.png" % tag), cam, tgt)


LIGHT_E = dict(inside=40.0, spot=2500.0)


def step_review(which="all"):
    outs = []
    E_IN, E_SPOT = LIGHT_E["inside"], LIGHT_E["spot"]
    if which in ("all", "day"):
        sc, objs, att = review_scene(False, E_IN, E_SPOT)
        outs += shots_lamp(sc, objs, False)
        outs.append(path_of_lamps(sc, objs, att, E_IN, E_SPOT, "day"))
    if which in ("all", "night"):
        sc, objs, att = review_scene(True, E_IN, E_SPOT)
        outs += shots_lamp(sc, objs, True)
        outs.append(path_of_lamps(sc, objs, att, E_IN, E_SPOT, "night"))
        sc, objs, att = review_scene(True, E_IN, E_SPOT, darker=0.35)
        tgt = Vector((0, -1.8, 9.0))
        outs.append(shoot_fov(os.path.join(WIP, "rv_night_dark_variant_25.png"), _cam(tgt, (-0.57, -0.82), 25), tgt))
    log("review", outs)
    return outs


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if "fast" in argv:
        CFG["fast"] = True
        argv.remove("fast")
    step = argv[0] if argv else "preview"
    if step == "preview":
        step_preview()
    elif step == "build":
        step_build()
    elif step == "bake":
        step_bake({"post": "Post", "cage": "Cage", "pumpkin": "Pumpkin"}[argv[1]])
    elif step == "web":
        step_web()
    elif step == "export":
        step_export()
    elif step == "verify":
        step_verify()
    elif step == "calib":
        step_calib()
    elif step == "review":
        step_review(argv[1] if len(argv) > 1 else "all")
    log("done", step)
