# SLINGSHOT Halloween garden - HauntedTree pieces: skeleton spec, the carved bark FACE (signed-distance features +
# bark furrows flowing around them + dark hollow colouring) and the dead-leaf clusters (curled two-sided leaves with
# a procedural 2x2 leaf atlas: colour, normal, roughness).
import copy
from treekit import *  # noqa

HAUNTED_LV = {
    1: dict(kind="limb", crook=0.24, fq=0.38, kink=0.3, kink_deg=(16, 30), trop=0.07, spread=0.12, ds=0.14,
            twist=0.45, rmax=4.8, zmax=12.8, bark=dict(f=2.4, depth=0.12, patch=0.45, patch_lo=0.24)),
    2: dict(kind="branch", fork=2, fork_ang=(24, 42), fork_r=(0.8, 0.92), side=(1, 3), side_t=(0.2, 0.75),
            side_ang=(38, 64), side_L=0.8, side_r=(0.5, 0.64), L=(2.0, 2.9), end_k=0.3, tip_r=0.042, crook=0.4,
            kink=0.6, kink_deg=(16, 34), trop=0.13, spread=0.1, curl=0.25, ds=0.1, up=0.1, out=0.34, pw=1.0,
            twist=0.45, rmax=5.0, zmax=14.2, bark=dict(f=2.8, depth=0.1, patch=0.35, patch_lo=0.25)),
    3: dict(kind="twig", fork=2, fork_ang=(20, 38), fork_r=(0.82, 0.92), side=(0, 1), side_t=(0.3, 0.7),
            side_ang=(30, 55), side_L=0.7, side_r=(0.55, 0.7), L=(0.85, 1.35), end_k=0.42, tip_r=0.02,
            crook=0.6, kink=0.75, kink_deg=(14, 32), trop=0.22, curl=0.7, ds=0.07, up=0.2, out=0.15, pw=1.0,
            twist=0.4, rmax=5.3, zmax=14.7, bark=dict(f=3.2, depth=0.08)),
    4: dict(kind="twig", fork=2, fork_ang=(18, 32), fork_r=(0.8, 0.9), side=(0, 0), side_t=(0.3, 0.7),
            side_ang=(30, 50), L=(0.38, 0.7), end_k=0.5, tip_r=0.012, crook=0.6, kink=0.5, kink_deg=(12, 26),
            trop=0.28, curl=1.2, ds=0.06, up=0.2, out=0.1, pw=1.0, twist=0.4, rmax=5.5, zmax=15.0,
            bark=dict(f=3.2, depth=0.06)),
}
HAUNTED_BARK_TRUNK = dict(f=2.2, depth=0.15, stretch=5.5, patch=0.22, patch_lo=0.3)

HAUNTED = dict(
    name="HauntedTree", seed=51, height=15.0, width=12.0, spiders=2,
    web_requests=[dict(orient="front", r=2.4, zmin=7.6, zmax=11.0, in_front=True)], leaves=True, avoid=(2.3, 7.2),
    trunk=dict(top=6.5, sway=((0.14, 0.8, 0.3), (0.1, 1.1, 1.0)), r_top=0.92, r_base=1.08, flare=0.5,
               flare_h=0.6, twist=0.42, bulge=(0.36, 4.4, 1.7)),
    # (start height on the trunk, azimuth, [elevations of the runs], [run lengths], base r, end r, tip hook)
    # the face looks along -Y (azimuth -90): two arm-like limbs reach out to the sides, the crown goes up behind
    limbs=[(5.95, -12, [12, 36, 2, 32], [1.55, 1.2, 1.15, 0.85], 0.5, 0.17, 0.45),
           (5.75, 192, [16, 40, 6, 36], [1.45, 1.25, 1.1, 0.85], 0.5, 0.17, 0.45),
           (6.3, 84, [56, 76, 42, 70], [1.6, 1.6, 1.4, 1.4], 0.5, 0.17, 0.0),
           (6.15, 140, [40, 64, 30, 60], [1.8, 1.6, 1.4, 1.3], 0.48, 0.16, 0.0),
           (6.2, 30, [42, 66, 28, 62], [1.7, 1.6, 1.4, 1.3], 0.48, 0.16, 0.0),
           (6.45, -105, [62, 74, 40, 64], [1.4, 1.6, 1.5, 1.3], 0.44, 0.15, 0.0)],
    roots=7, root_len=(1.8, 2.5), root_r=(0.56, 0.7),
    stubs=[("trunk", 2.1, 135, 0.5, 0.22), ("limb3", 2.0, 0, 0.4, 0.14)],
    knots=[("trunk", 1.5, 35, 0.2), ("trunk", 2.6, 215, 0.2), ("limb2", 1.6, 0, 0.13)],
    hollow=None,
    # the face: centre height, eyes (u, v, half width, half height, tilt), brows, nose, mouth
    face=dict(z=4.35, eye_u=0.62, eye_v=0.6, eye_w=0.5, eye_h=0.29, eye_tilt=26.0, eye_depth=0.62,
              mouth_v=-0.84, mouth_w=0.8, mouth_h=0.6, mouth_depth=0.82, nose_v=0.1,
              burl=(1.95, 2.0, 1.1), burl_v=-0.15, burl_out=0.55),
    max_level=4, leaf_clusters=13,
)


# ================================================================== the face
def _trunk_s_at_z(trunk, z):
    zs = trunk.P[:, 2]
    i = int(np.clip(np.searchsorted(zs, z) - 1, 0, len(zs) - 2))
    t = (z - zs[i]) / max(1e-9, zs[i + 1] - zs[i])
    return float(trunk.S[i] + t * trunk.seglen[i])


def _local_angle(br, s, d):
    i = int(np.clip(np.searchsorted(br.S, s, side="right") - 1, 0, len(br.P) - 2))
    u = (s - br.S[i]) / br.seglen[i]
    N = br.N[i] * (1 - u) + br.N[i + 1] * u
    T = br.T[i] * (1 - u) + br.T[i + 1] * u
    T /= np.linalg.norm(T)
    N = N - T * N.dot(T)
    N /= np.linalg.norm(N)
    B = np.cross(T, N)
    return math.atan2(float(np.dot(d, B)), float(np.dot(d, N)))


def haunted_face(ctx):
    """The face sits on a BURL: an ellipsoid swelling of bark that pushes the face ~0.55 forward and widens it, so
    every feature is carved into solid wood. Eye sockets, pupils and the mouth are blind pockets carved straight back
    (Blender +Y), with >= 0.3 stud of wood between them and the trunk's sides (review round 1: the old radial
    sockets on the bare trunk opened sideways and showed sky / grass through the face)."""
    spec = ctx["spec"]
    F = spec["face"]
    trunk = ctx["trunk"]
    trunk.soft_s = 0.15            # smooth arclength off-axis: no dashed bark on the burl (see local_coords)
    zf = F["z"]
    sf = _trunk_s_at_z(trunk, zf)
    pf, rf, Tf = trunk.at(sf)
    pf, Tf = np.array(pf), np.array(Tf)
    n_face = np.array([0.0, -1.0, 0.0])
    n_face = n_face - Tf * n_face.dot(Tf)
    n_face /= np.linalg.norm(n_face)
    e_u = np.cross(Tf, n_face)
    BA, BB, BC = F["burl"]                       # burl radii: across, up, depth
    bv = F["burl_v"]                             # burl centre height offset from the face centre
    Cb = pf + Tf * bv + n_face * (rf + F["burl_out"] - BC)
    rotB = np.array([e_u, Tf, n_face], np.float32)

    def S(u, v, out=0.0):
        """point on the burl's front surface at (u across, v up) + its outward normal."""
        x, z = u, v - bv
        q = max(0.03, 1 - (x / BA) ** 2 - (z / BB) ** 2)
        y = BC * math.sqrt(q)
        nn = e_u * x / BA ** 2 + Tf * z / BB ** 2 + n_face * y / BC ** 2
        nn /= np.linalg.norm(nn)
        p = Cb + e_u * x + Tf * z + n_face * y
        return p + nn * out, nn

    def rot_tilt(tilt_deg):
        c, s_ = math.cos(math.radians(tilt_deg)), math.sin(math.radians(tilt_deg))
        return np.array([e_u * c + Tf * s_, -e_u * s_ + Tf * c, n_face], np.float32)

    def face_uv(Q):
        """face coords: u across, v up (from the face centre), depth below the (trunk + burl) surface, angle."""
        rel = Q - pf
        v = rel @ Tf
        radial = rel - np.outer(v, Tf)
        x = radial @ e_u
        y = radial @ n_face
        phi = np.arctan2(x, y)
        rr = np.interp(sf + v, trunk.S, trunk.R)
        d_trunk = rr - np.sqrt(x * x + y * y)
        L = (Q - Cb) @ rotB.T
        q = 1 - (L[:, 0] / BA) ** 2 - (L[:, 1] / BB) ** 2
        d_burl = np.where(q > 0, BC * np.sqrt(np.clip(q, 0, 1)) - L[:, 2], -9.0)
        return x, v, np.maximum(d_trunk, d_burl), phi

    eyes = []
    for sgn in (1, -1):
        c, nn = S(sgn * F["eye_u"], F["eye_v"])
        eyes.append((c, nn, rot_tilt(sgn * F["eye_tilt"])))
    mouth_c, mouth_n = S(0.0, F["mouth_v"])
    mouth_rot = rotB
    # fangs: (x as a fraction of the half width, length as a fraction of that half height, half width fraction)
    TEETH_TOP = [(-0.52, 0.5, 0.14), (-0.04, 0.3, 0.1), (0.5, 0.52, 0.14)]
    TEETH_BOT = [(-0.27, 0.5, 0.13), (0.3, 0.46, 0.13)]

    def mouth_rr(Q):
        """a wide jagged grin: upper / lower edge curves along x, triangular wooden fangs, corners turned up.
        rr < 1 inside the opening, = 1 on the rim. L = mouth-frame coords (z = out of the face)."""
        L = (Q - mouth_c) @ mouth_rot.T
        w, h = F["mouth_w"], F["mouth_h"]
        xn = np.clip(L[:, 0] / w, -1.5, 1.5)
        y = L[:, 1] - 0.16 * h * xn * xn                   # the corners turn up into a sinister grin
        base = np.sqrt(np.clip(1 - xn * xn, 0, 1))
        wob = 1.0 + 0.07 * PNZ(xn * 2.3 + 4.0, 1.7, 3.3)
        tt = np.zeros(len(Q))
        tb = np.zeros(len(Q))
        for x0, ln, hw in TEETH_TOP:
            tt = np.maximum(tt, ln * np.clip(1 - np.abs(xn - x0) / hw, 0, 1))
        for x0, ln, hw in TEETH_BOT:
            tb = np.maximum(tb, ln * np.clip(1 - np.abs(xn - x0) / hw, 0, 1))
        yt = np.maximum(1e-3, 0.62 * h * (base * wob - tt))
        yb = np.maximum(1e-3, 0.72 * h * (base * wob * (1 + 0.12 * base) - tb))
        rr = np.maximum(np.abs(xn), np.where(y >= 0, y / yt, -y / yb))
        return rr, L

    def eye_rr(Q, e):
        c, nn, R = e
        L = (Q - c) @ R.T
        return np.sqrt((L[:, 0] / F["eye_w"]) ** 2 + (L[:, 1] / F["eye_h"]) ** 2), L

    def face_fn(sdf):
        lo_c, _ = S(0, 0)
        box_lo = np.minimum(lo_c, pf) - 2.8
        box_hi = np.maximum(lo_c, pf) + 2.8

        def f(buf, Q):
            # the burl, with the trunk's own bark furrows (grain bending round the features)
            burl = sd_ellipsoid(Q, Cb, (BA, BB, BC), rotB)
            near = np.nonzero(np.abs(burl) < 0.35)[0]
            if len(near):
                q = Q[near].astype(np.float64)
                dm, seg, tt = branch_seg_points(trunk.P, trunk.R, q, 3.0)
                ok = seg >= 0
                if ok.any():
                    s_, a_, r_ = local_coords(trunk, trunk.P, trunk.S, q[ok], seg[ok], tt[ok].astype(np.float64))
                    off, _ = bark_eval(trunk, s_, a_, r_, deflect)
                    tmp = np.zeros(len(near), np.float32)
                    tmp[ok] = off
                    burl[near] -= tmp
            d = smin(buf, burl, 0.5)
            # brow ridges: heavy bark folds over the eyes, inner ends low (a V = angry)
            for sgn in (1, -1):
                a, _ = S(sgn * 0.14, F["eye_v"] + 0.28, 0.08)
                m, _ = S(sgn * 0.56, F["eye_v"] + 0.46, 0.1)
                b, _ = S(sgn * 1.0, F["eye_v"] + 0.52, 0.0)
                br = np.minimum(sd_capsule(Q, a, m, 0.19, 0.17), sd_capsule(Q, m, b, 0.17, 0.1))
                d = smin(d, br, 0.2)
                # sunken under-eye bags
                c1, _ = S(sgn * 0.3, F["eye_v"] - 0.32, -0.02)
                c2, _ = S(sgn * 0.8, F["eye_v"] - 0.22, -0.04)
                d = smin(d, sd_capsule(Q, c1, c2, 0.08, 0.06), 0.12)
                # cheek folds from the nose wings down past the mouth corners
                k1, _ = S(sgn * 0.2, F["nose_v"] - 0.05, -0.02)
                k2, _ = S(sgn * 0.66, F["mouth_v"] + 0.18, -0.02)
                k3, _ = S(sgn * 0.8, F["mouth_v"] - 0.36, -0.05)
                d = smin(d, np.minimum(sd_capsule(Q, k1, k2, 0.075, 0.085), sd_capsule(Q, k2, k3, 0.085, 0.05)),
                         0.12)
            # a gnarled knot nose, hooked down
            nc, nn = S(0.0, F["nose_v"], 0.06)
            d = smin(d, sd_ellipsoid(Q, nc, (0.16, 0.3, 0.2), rot_tilt(0)), 0.14)
            tip, _ = S(0.0, F["nose_v"] - 0.22, 0.17)
            d = smin(d, sd_ellipsoid(Q, tip, (0.11, 0.1, 0.1), rot_tilt(0)), 0.08)
            # thick rolled lips (0.28 across) round the mouth
            rr, L = mouth_rr(Q)
            scale = 0.5 * (F["mouth_w"] + F["mouth_h"]) * 0.8
            lip = np.sqrt(((rr - 1.12) * scale) ** 2 + (L[:, 2] + 0.02) ** 2) - 0.14
            d = smin(d, lip, 0.14)
            # carve: the mouth, a blind pocket straight back with a rounded floor
            cav = smax((rr - 0.92) * scale, -(L[:, 2] + F["mouth_depth"]), 0.18)
            d = smax(d, -cav, 0.06)
            # carve: eye sockets (blind ellipsoid pockets straight back) + deeper pupil holes
            for e in eyes:
                c, nn, R = e
                sock = sd_ellipsoid(Q, c - n_face * 0.22, (F["eye_w"], F["eye_h"], F["eye_depth"]), R)
                d = smax(d, -sock, 0.07)
                pup = sd_ellipsoid(Q, c - n_face * 0.55, (F["eye_w"] * 0.5, F["eye_h"] * 0.62, 0.75), R)
                d = smax(d, -pup, 0.06)
            return d
        sdf.apply_points(box_lo, box_hi, f)

    # bark furrows bend around the features (like grain around a knot)
    feats = []
    for (u, v, rho, amp) in ((F["eye_u"], F["eye_v"], 0.55, 0.55), (-F["eye_u"], F["eye_v"], 0.55, 0.55),
                             (0.0, F["mouth_v"], 0.85, 0.6), (0.0, F["nose_v"], 0.35, 0.4)):
        s_i = sf + v
        p_i, _ = S(u, v)
        p_ax = np.array(trunk.at(s_i)[0])
        d = p_i - p_ax
        d = d - Tf * d.dot(Tf)
        d /= np.linalg.norm(d)
        feats.append((_local_angle(trunk, s_i, d) + trunk.twist * s_i, s_i, rho, amp))

    def deflect(br, ang, s, R0):
        if br is not trunk:
            return ang, s
        for fa, fs, rho, amp in feats:
            du = ((ang - fa + np.pi) % (2 * np.pi) - np.pi) * R0
            dv = s - fs
            f = amp * np.exp(-(du * du + dv * dv) / (rho * rho))
            ang = fa + du * (1 - f) / R0
            s = fs + dv * (1 - f)
        return ang, s

    def face_col(col, rough, Vw, Nw):
        u, v, depth, phi = face_uv(Vw)
        front = (np.abs(phi) < 1.3).astype(np.float64)
        n = len(Vw)
        hollow = np.zeros(n)
        for e in eyes:
            er, Le = eye_rr(Vw, e)
            hollow = np.maximum(hollow, sm(1.15, 0.98, er) * sm(-0.02, 0.2, depth))
            hollow = np.maximum(hollow, sm(1.1, 0.9, er) * sm(-0.15, -0.55, Nw[:, 2]))   # brow undersides
        mr, Lm = mouth_rr(Vw)
        hollow = np.maximum(hollow, sm(1.12, 0.98, mr) * sm(-0.02, 0.2, depth))
        hollow *= front
        dark = mixc(np.tile(PAL["hollow2"], (n, 1)), np.tile(PAL["hollow"], (n, 1)), sm(0.02, 0.3, depth))
        col = mixc(col, dark, hollow)
        rough = rough * (1 - hollow) + 0.95 * hollow
        # the face's raised features catch the light: paler, worn bark on brows / nose / lips / cheek folds
        raised = sm(0.02, 0.12, -depth) * front * np.exp(-((u / 1.3) ** 2 + ((v + 0.1) / 1.25) ** 2))
        col = mixc(col, np.clip(col * 1.22 + 0.015, 0, 1), 0.7 * raised * (1 - hollow))
        return col, rough

    def lichen_fn(Vw):
        u, v, depth, phi = face_uv(Vw)
        front = (np.abs(phi) < 1.4).astype(np.float64)
        return 1 - 0.92 * front * np.exp(-((u / 1.7) ** 2 + ((v + 0.1) / 1.7) ** 2) ** 2)

    face_col.lichen_fn = lichen_fn
    return face_fn, face_col, deflect


# ================================================================== dead leaves
LEAF_VARIANTS = [
    dict(base=(124, 30, 22), mid=(150, 46, 26), edge=(64, 26, 18), vein=(196, 118, 56), lobes=5, phase=0.3),
    dict(base=(160, 70, 26), mid=(186, 98, 34), edge=(84, 40, 20), vein=(214, 156, 74), lobes=4, phase=1.4),
    dict(base=(98, 58, 34), mid=(124, 80, 44), edge=(52, 32, 20), vein=(170, 128, 80), lobes=5, phase=2.2),
    dict(base=(96, 24, 34), mid=(126, 38, 40), edge=(46, 16, 22), vein=(178, 92, 70), lobes=4, phase=0.9),
]


def leaf_halfwidth(t, var):
    """normalised half width (0..0.5) of a leaf at t (0 base .. 1 tip), lobed oak-ish outline."""
    t = np.asarray(t, np.float64)
    base = np.sin(np.pi * np.clip(t, 0, 1)) ** 0.75 * (1 - 0.25 * t)
    lob = 1 + 0.22 * np.sin(t * var["lobes"] * np.pi + var["phase"]) * np.sin(np.pi * t)
    return 0.5 * base * lob / 1.12


def leaf_atlas(size, path_prefix):
    """2x2 atlas, one leaf variant per cell. Returns images dict (albedo, normal, rough)."""
    n = size // 2
    alb = np.zeros((size, size, 4), np.float32)
    hgt = np.zeros((size, size), np.float32)
    rgh = np.zeros((size, size, 4), np.float32)
    pn = PN(77)
    vv, uu = np.meshgrid((np.arange(n) + 0.5) / n, (np.arange(n) + 0.5) / n, indexing="ij")   # v along, u across
    for k, var in enumerate(LEAF_VARIANTS):
        t = 0.03 + 0.94 * vv                     # cell v -> leaf t (small margins)
        x = (uu - 0.5) / 0.94                    # across, -0.5..0.5
        hw = leaf_halfwidth(t, var)
        edge_d = hw - np.abs(x)                  # >0 inside the outline
        mid = np.exp(-(x / 0.012) ** 2)
        # side veins: from the midrib out and toward the tip
        sv = np.zeros_like(x)
        for j in range(7):
            t0 = 0.12 + 0.11 * j
            line = t - (t0 + 0.55 * np.abs(x))
            sv = np.maximum(sv, np.exp(-(line / 0.008) ** 2) * (np.abs(x) < hw * 0.95))
        crinkle = pn.fbm(uu * 9 + k * 5, vv * 9, k * 1.7, 3)
        blot = pn.fbm(uu * 3 + k, vv * 3, 4.0 + k, 3) * 0.5 + 0.5
        c = np.array(var["base"]) / 255.0
        cm = np.array(var["mid"]) / 255.0
        ce = np.array(var["edge"]) / 255.0
        cv = np.array(var["vein"]) / 255.0
        col = c[None, None] * (1 - blot[..., None]) + cm[None, None] * blot[..., None]
        col = col * (1 - 0.65 * np.clip(mid + 0.6 * sv, 0, 1)[..., None]) + cv[None, None] * 0.65 * np.clip(
            mid + 0.6 * sv, 0, 1)[..., None]
        edgeband = 1 - np.clip(edge_d / 0.06, 0, 1)
        spots = np.clip((pn(uu * 22 + k, vv * 22, 9.0) - 0.45) * 4, 0, 1) * 0.6
        col = col * (1 - (0.75 * edgeband + 0.4 * spots)[..., None]) + ce[None, None] * (0.75 * edgeband + 0.4 * spots)[..., None]
        col *= (0.9 + 0.12 * crinkle)[..., None]
        oy, ox = (k // 2) * n, (k % 2) * n
        alb[oy:oy + n, ox:ox + n, :3] = np.clip(col, 0, 1)
        alb[oy:oy + n, ox:ox + n, 3] = 1
        hgt[oy:oy + n, ox:ox + n] = 0.6 * mid + 0.35 * sv + 0.25 * crinkle - 0.4 * edgeband
        r = 0.7 + 0.1 * crinkle + 0.15 * edgeband
        rgh[oy:oy + n, ox:ox + n, :3] = np.clip(r, 0, 1)[..., None]
        rgh[oy:oy + n, ox:ox + n, 3] = 1
    # petiole / stem patch: the corners between cells are brown (petioles map there)
    gy, gx = np.gradient(hgt)
    k = 6.0
    nx, ny = -gx * k, -gy * k
    nz = np.ones_like(nx)
    ln = np.sqrt(nx * nx + ny * ny + nz * nz)
    nrm = np.zeros((size, size, 4), np.float32)
    nrm[..., 0] = nx / ln * 0.5 + 0.5
    nrm[..., 1] = ny / ln * 0.5 + 0.5
    nrm[..., 2] = nz / ln * 0.5 + 0.5
    nrm[..., 3] = 1
    imgs = {}
    for key, arr, cs in (("albedo", alb, "sRGB"), ("normal", nrm, "Non-Color"), ("rough", rgh, "Non-Color")):
        img = bpy.data.images.new(os.path.basename(path_prefix) + "_" + key, size, size, alpha=False)
        img.colorspace_settings.name = cs
        img.pixels.foreach_set(arr.ravel())       # colours are already sRGB-encoded (byte image, sRGB space)
        img.filepath_raw = path_prefix + "_" + key + ".png"
        img.file_format = "PNG"
        img.save()
        imgs[key] = img
    return imgs


def leaf_geometry(acc, base, d_along, d_side, L, W, var_idx, curl, cup, twist, rng, uvcell):
    """one curled dead leaf, two-sided (front + offset back), UV into its atlas cell."""
    var = LEAF_VARIANTS[var_idx]
    nr, nc = 5, 5
    nrm = d_along.cross(d_side).normalized()
    rows = []
    uvs = []
    for i in range(nr):
        t = i / (nr - 1)
        hw = float(leaf_halfwidth(0.03 + 0.94 * t, var))
        row, urow = [], []
        for j in range(nc):
            x = (j / (nc - 1) - 0.5) * 2 * hw          # -hw .. hw (normalised to W)
            xs = x * W
            # dead-leaf curl: edges roll up (cup), the blade curls along its length, a twist toward the tip
            z = cup * (x / 0.5) ** 2 * W + curl * (t ** 2) * L
            ang = twist * t
            side = d_side * math.cos(ang) + nrm * math.sin(ang)
            up = nrm * math.cos(ang) - d_side * math.sin(ang)
            p = base + d_along * (t * L * (1 - 0.25 * curl * t)) + side * xs + up * z
            row.append(p)
            # atlas cell: u = 0.5 + 0.94 x across, v = t along (the atlas evaluates the outline at 0.03 + 0.94 v)
            urow.append((uvcell[0] + 0.5 * (0.5 + 0.94 * x), uvcell[1] + 0.5 * t))
        rows.append(row)
        uvs.append(urow)
    off = 0.012
    for side_sign in (1, -1):
        flat = [tuple(p - nrm * off * (side_sign < 0)) for row in rows for p in row]
        i0 = acc.add_verts(flat)
        for i in range(nr - 1):
            for j in range(nc - 1):
                q = [i0 + i * nc + j, i0 + i * nc + j + 1, i0 + (i + 1) * nc + j + 1, i0 + (i + 1) * nc + j]
                quv = [uvs[i][j], uvs[i][j + 1], uvs[i + 1][j + 1], uvs[i + 1][j]]
                if side_sign > 0:
                    acc.face(q, quv)
                else:
                    acc.face(list(reversed(q)), list(reversed(quv)))
    return nrm


def build_leaves(ctx, name):
    spec = ctx["spec"]
    rng = random.Random(spec["seed"] + 303)
    tips = [b for b in ctx["tree"] if b.kind == "twig" and not b.children and b.P[-1][2] > 7.5]
    rng.shuffle(tips)
    chosen = []
    for b in tips:
        p = V(b.P[-1])
        if all((p - V(o.P[-1])).length > 1.6 for o in chosen):
            chosen.append(b)
        if len(chosen) >= spec["leaf_clusters"]:
            break
    acc = MeshAcc()
    cells = [(0.0, 0.0), (0.5, 0.0), (0.0, 0.5), (0.5, 0.5)]
    n_leaves = 0
    for b in chosen:
        k = rng.randint(5, 9)
        for j in range(k):
            s = b.length * (1.0 - 0.55 * rng.random() ** 1.4)
            p, r, T = b.at(s)
            p, T = V(p), V(T)
            # hang down and out, turned randomly
            out = Vector((p.x, p.y, 0)).normalized() if math.hypot(p.x, p.y) > 0.1 else Vector((1, 0, 0))
            az = rng.uniform(0, 2 * math.pi)
            sidev = Vector((math.cos(az), math.sin(az), 0))
            d_al = (Vector((0, 0, -1)) * rng.uniform(0.6, 1.0) + out * rng.uniform(0.0, 0.5) + sidev * 0.35)
            d_al.normalize()
            d_sd = d_al.cross(Vector((0, 0, 1)))
            if d_sd.length < 1e-3:
                d_sd = Vector((1, 0, 0))
            d_sd = rot_about(d_sd.normalized(), d_al, rng.uniform(-1.2, 1.2))
            base = p + d_al * r * 0.6 + Vector((0, 0, -0.03))
            # a short petiole from the twig to the leaf
            pet_end = base + d_al * 0.08
            L = rng.uniform(0.55, 0.8)
            W = L * rng.uniform(0.62, 0.78)
            vi = rng.randrange(4)
            leaf_geometry(acc, pet_end, d_al, d_sd, L, W, vi, curl=rng.uniform(0.3, 0.65),
                          cup=rng.uniform(0.45, 0.8), twist=rng.uniform(-0.8, 0.8), rng=rng, uvcell=cells[vi])
            # petiole: 3-sided tube, UV in the leaf's base (brown midrib)
            pts = [p, base, pet_end]
            i0 = acc.add_verts([tuple(q + (Vector((math.cos(a), math.sin(a), 0)) * 0.012)) for q in pts
                                for a in (0, 2.09, 4.19)])
            uvb = (cells[vi][0] + 0.25, cells[vi][1] + 0.5 * 0.035)
            for i in range(2):
                for jj in range(3):
                    kk = (jj + 1) % 3
                    acc.face((i0 + i * 3 + jj, i0 + i * 3 + kk, i0 + (i + 1) * 3 + kk, i0 + (i + 1) * 3 + jj),
                             [uvb, uvb, uvb, uvb])
            n_leaves += 1
    ob = acc.build(name + "_Leaves", colors=False, uvs=True)
    ob.modifiers.new("Tri", "TRIANGULATE")
    apply_mods(ob)
    imgs = leaf_atlas(512, os.path.join(MAPS, name + "_Leaves"))
    pbr_material(ob, name + "_Leaves_PBR", imgs)
    log("leaves", n_leaves, "clusters", len(chosen), "tris", tris_of(ob))
    ob["clusters"] = [list(V(b.P[-1])) for b in chosen]
    return ob
