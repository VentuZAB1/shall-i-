# SLINGSHOT Halloween garden - DeadTree + HauntedTree (builder: DeadTrees agent, 2026-10-12).
# Headless:
#   blender.exe -b --factory-startup --python trees.py -- <tree> <step> [<step> ...] [fast]
#   tree = dead | haunted ; steps = preview | build | bake | render | export | report
# Pipeline (see treekit.py): skeleton -> SDF core (VDB) + bark tubes = HI sculpt with per-vertex colour; coarse SDF
# decimated + low tubes = GAME meshes; bakes 1024; webs / silk / leaves are textured procedurally.
import sys, os
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\DeadTrees")
from treekit import *  # noqa

from haunted import HAUNTED, HAUNTED_LV, HAUNTED_BARK_TRUNK, haunted_face, build_leaves  # noqa

CFG = dict(fast=False)
RC = 0.13            # branches thinner than this are tubes, thicker parts live in the SDF core


# ================================================================== DeadTree skeleton
DEAD_LV = {
    1: dict(kind="limb", crook=0.24, fq=0.38, kink=0.3, kink_deg=(16, 30), trop=0.07, spread=0.12, ds=0.14,
            twist=0.3, rmax=5.8, zmax=14.0, bark=dict(f=2.5, depth=0.12, patch=0.7, patch_lo=0.2)),
    2: dict(kind="branch", fork=2, fork_ang=(24, 42), fork_r=(0.8, 0.92), side=(2, 3), side_t=(0.2, 0.75),
            side_ang=(38, 64), side_L=0.85, side_r=(0.5, 0.64), L=(2.3, 3.3), end_k=0.3, tip_r=0.042, crook=0.4,
            kink=0.6, kink_deg=(16, 34), trop=0.13, spread=0.1, curl=0.25, ds=0.1, up=0.1, out=0.34, pw=1.0,
            twist=0.35, rmax=6.3, zmax=15.6, bark=dict(f=2.9, depth=0.1, patch=0.5, patch_lo=0.22)),
    3: dict(kind="twig", fork=2, fork_ang=(20, 38), fork_r=(0.82, 0.92), side=(0, 1), side_t=(0.3, 0.7),
            side_ang=(30, 55), side_L=0.7, side_r=(0.55, 0.7), L=(0.9, 1.5), end_k=0.42, tip_r=0.02,
            crook=0.6, kink=0.75, kink_deg=(14, 32), trop=0.26, curl=0.7, ds=0.07, up=0.2, out=0.15, pw=1.0,
            twist=0.3, rmax=6.6, zmax=16.0, bark=dict(f=3.3, depth=0.08)),
    4: dict(kind="twig", fork=2, fork_ang=(18, 32), fork_r=(0.8, 0.9), side=(0, 0), side_t=(0.3, 0.7),
            side_ang=(30, 50), L=(0.4, 0.78), end_k=0.5, tip_r=0.012, crook=0.6, kink=0.5, kink_deg=(12, 26),
            trop=0.3, curl=1.2, ds=0.06, up=0.2, out=0.1, pw=1.0, twist=0.3, rmax=6.8, zmax=16.3,
            bark=dict(f=3.3, depth=0.06)),
}
DEAD_BARK_TRUNK = dict(f=2.3, depth=0.14, stretch=3.6, patch=0.35, patch_lo=0.27)

DEAD = dict(
    name="DeadTree", seed=34, height=16.0, width=13.0, spiders=3, leaves=False,
    # review round 1: bigger webs, one facing the front (+-Y), one the side (+-X), one low near eye level
    web_requests=[dict(orient="front", r=2.7, zmin=6.0, zmax=10.5), dict(orient="side", r=2.6, zmin=8.0, zmax=13.0),
                  dict(orient="front", r=2.1, zmin=3.8, zmax=6.8, in_back=True)],
    trunk=dict(top=5.4, sway=((0.32, 0.9, 0.4), (0.22, 1.3, 2.1)), r_top=0.8, r_base=0.95, flare=0.42,
               flare_h=0.55, twist=0.26),
    # (start height on the trunk, azimuth, [elevations of the runs], [run lengths], base r, end r, tip hook)
    limbs=[(5.1, 18, [30, 56, 22, 58], [2.0, 1.8, 1.6, 1.7], 0.56, 0.19, 0.0),
           (4.9, 128, [18, 44, 10, 46], [2.2, 1.8, 1.7, 1.5], 0.54, 0.18, 0.5),
           (5.25, 238, [34, 62, 28, 64], [1.8, 2.0, 1.5, 1.8], 0.55, 0.19, 0.0),
           (3.5, 304, [10, 30, 4, 38], [2.0, 1.6, 1.6, 1.3], 0.46, 0.16, 0.55),
           (5.45, 72, [64, 80, 52, 74], [1.6, 1.8, 1.5, 1.5], 0.46, 0.16, 0.0)],
    roots=7, root_len=(1.9, 2.7), root_r=(0.5, 0.64),
    stubs=[("trunk", 2.95, 200, 0.6, 0.24), ("limb0", 2.3, 0, 0.45, 0.16), ("limb2", 3.3, 0, 0.42, 0.14)],
    knots=[("trunk", 1.5, 115, 0.22), ("trunk", 4.0, 40, 0.18), ("limb1", 1.9, 0, 0.13), ("limb3", 1.6, 0, 0.12)],
    hollow=dict(z=2.05, az=-62, w=0.42, hgt=0.78, depth=1.0, lip=0.15),
    max_level=4,
)


def trunk_branch(T, rng, bark):
    n = 60
    pts, rads = [], []
    ph = [rng.uniform(0, 6.28) for _ in range(4)]
    for i in range(n + 1):
        z = -0.45 + (T["top"] + 0.45) * i / n
        u = max(0.0, z) / T["top"]
        (ax, fx, px), (ay, fy, py) = T["sway"]
        x = ax * math.sin(math.pi * fx * u + px) - ax * math.sin(px) + 0.06 * noise.noise(Vector((z * 0.9, ph[0], 0)))
        y = ay * math.sin(math.pi * fy * u + py) - ay * math.sin(py) + 0.06 * noise.noise(Vector((z * 0.9, ph[1], 0)))
        pts.append(Vector((x * min(1.0, u * 4), y * min(1.0, u * 4), z)))
        zz = max(0.0, z)
        ba, bz, bw = T.get("bulge", (0.0, 0.0, 1.0))
        rads.append(T["r_top"] + (T["r_base"] - T["r_top"]) * (1 - zz / T["top"])
                    + T["flare"] * math.exp(-zz / T["flare_h"]) + ba * math.exp(-((zz - bz) / bw) ** 2))
    return Br(pts, rads, 0, "trunk", None, 0.0, twist=T["twist"], seed=rng.randint(1, 10 ** 6), bark=bark)


def root_branches(n, T, rng, trunk, Lr, Rr, bark):
    out = []
    az0 = rng.uniform(0, 360)
    for i in range(n):
        az = math.radians(az0 + 360 * i / n + rng.uniform(-18, 18))
        c, s = math.cos(az), math.sin(az)
        L = rng.uniform(*Lr)
        r0 = rng.uniform(*Rr)
        ctrl = [Vector((0.45 * c, 0.45 * s, 1.0)), Vector((1.05 * c, 1.05 * s, 0.4)),
                Vector(((0.5 + 0.55 * L) * c, (0.5 + 0.55 * L) * s, 0.1)), Vector(((0.5 + L) * c, (0.5 + L) * s, -0.62))]
        pts = []
        for k in range(len(ctrl) - 1):
            a, b = ctrl[k], ctrl[k + 1]
            m = 6
            for j in range(m if k < len(ctrl) - 2 else m + 1):
                pts.append(a.lerp(b, j / m))
        # gnarl: sideways wobble along the ground
        off = rng.uniform(0, 100)
        side = Vector((-s, c, 0))
        for j, p in enumerate(pts):
            t = j / (len(pts) - 1)
            p += side * 0.35 * noise.noise(Vector((t * 3.0, off, 0.5))) * t
            p.z += 0.07 * noise.noise(Vector((t * 5.0, off, 2.5))) * t
        # smooth a bit
        for _ in range(2):
            pts = [pts[0]] + [(pts[j - 1] + pts[j] * 2 + pts[j + 1]) / 4 for j in range(1, len(pts) - 1)] + [pts[-1]]
        rads = [r0 * (1 - 0.5 * (j / (len(pts) - 1)) ** 0.9) for j in range(len(pts))]
        b = Br(pts, rads, 1, "root", trunk, 0.5, twist=0.1, seed=rng.randint(1, 10 ** 6), bark=bark)
        b.k = 0.42
        out.append(b)
    return out


def limb_branches(spec, rng, trunk, lv):
    out = []
    for (zs, az, elevs, lens, r0, r1, hook) in spec["limbs"]:
        s = trunk.length * (zs + 0.45) / (spec["trunk"]["top"] + 0.45)
        p, r, T = trunk.at(s)
        a = math.radians(az)
        start = V(p) + Vector((math.cos(a), math.sin(a), 0)) * r * 0.25
        pts = elbow_path(start, az + rng.uniform(-6, 6), [e + rng.uniform(-4, 4) for e in elevs],
                         [L * rng.uniform(0.92, 1.08) for L in lens], rng, ds=lv.get("ds", 0.13), hook=hook)
        rads = taper(len(pts), r0, r1, 0.85)
        b = Br(pts, rads, 1, "limb", trunk, s, twist=lv.get("twist", 0.3), seed=rng.randint(1, 10 ** 6),
               bark=lv.get("bark"))
        trunk.children.append(b)
        b.k = 0.32
        out.append(b)
    return out


def build_skeleton(spec, LV, trunk_bark):
    Br._n = 0
    for lv in LV:
        if lv >= 2:
            LV[lv]["avoid"] = spec.get("avoid", (1.9, 5.6))
    rng = random.Random(spec["seed"])
    trunk = trunk_branch(spec["trunk"], rng, trunk_bark)
    roots = root_branches(spec["roots"], spec["trunk"], rng, trunk, spec["root_len"], spec["root_r"], trunk_bark)
    limbs = limb_branches(spec, rng, trunk, LV[1])
    tree = [trunk] + roots + limbs
    for lb in limbs:
        grow_children(tree, lb, LV, rng, spec["max_level"])
    for b in tree:
        if b.level >= 2 and b.k == 0:
            b.k = min(0.16, 0.7 * float(b.R[0]))
    return tree, trunk, roots, limbs


def choose_seed(spec, LV, tb, seeds):
    """grow many skeletons, keep the most balanced wide crown (width ~ spec width in X and Y, centred)."""
    best = None
    base = spec["seed"]
    for sd in seeds:
        spec["seed"] = sd
        tree, trunk, roots, limbs = build_skeleton(spec, LV, tb)
        fit_scale(tree, spec)
        P = np.concatenate([b.P for b in tree if b.kind not in ("trunk", "root")])
        lo, hi = P.min(0), P.max(0)
        wx, wy = hi[0] - lo[0], hi[1] - lo[1]
        cx, cy = (hi[0] + lo[0]) / 2, (hi[1] + lo[1]) / 2
        mc = P[:, :2].mean(0)
        score = abs(wx - spec["width"]) + abs(wy - spec["width"]) + 2.0 * math.hypot(cx, cy) + 2.0 * float(
            np.hypot(*mc)) + 3.0 * max(0.0, max(wx, wy) - spec["width"] - 0.6)
        if best is None or score < best[0]:
            best = (score, sd, [round(wx, 2), round(wy, 2), round(cx, 2), round(cy, 2)])
    spec["seed"] = best[1]
    log("seed search", best)
    return best[1]


def fit_scale(tree, spec):
    """uniform scale about the base so the crown matches the target height (radii scaled too)."""
    zmax = max(float(b.P[:, 2].max() + b.R.max()) for b in tree)
    k = spec["height"] / zmax
    for b in tree:
        b.P *= k
        b.ps *= k
        b.R *= k ** 0.5
        b.update()
    return k


def stats(tree):
    allp = np.concatenate([b.P for b in tree])
    lv = {}
    for b in tree:
        lv[b.level] = lv.get(b.level, 0) + 1
    return dict(bmin=[round(v, 2) for v in allp.min(0)], bmax=[round(v, 2) for v in allp.max(0)], levels=lv,
                n=len(tree))


# ================================================================== core / tube split
def split_items(tree):
    core, tubes = [], []
    for b in tree:
        if b.kind in ("trunk", "root", "limb", "stub"):
            core.append((b, b.P, b.R))
            continue
        sc = b.s_at_radius(RC)
        if sc > 0.15:
            P, R = b.cut(0.0, sc)
            core.append((b, P, R))
            s0 = max(0.0, sc - 1.6 * RC)
            P2, R2 = b.cut(s0, b.length)
            # while it is still inside the core branch the tube is thinner (fully covered), then it swells to full
            # size right where it leaves the core's rounded end -> no exposed, wrongly baked tube base
            s_abs = s0 + np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P2, axis=0), axis=1))])
            # (round 2: it leaves the core at ~0.9 r and only reaches full size 2.5 r further on, so its rim never
            # overhangs the decimated core end = no lip / dark ring where core and tube meet)
            R2 = R2 * (0.8 + 0.12 * sm(sc - 0.1 * RC, sc + 0.6 * RC, s_abs) + 0.08 * sm(sc + 0.6 * RC, sc + 2.5 * RC, s_abs))
            tubes.append((b, P2, R2, s0))
        else:
            tubes.append((b, b.P, b.R, 0.0))
    return core, tubes


def stub_branches(spec, rng, trunk, limbs):
    out = []
    for host, s_or_z, az, L, r in spec["stubs"]:
        hb = trunk if host == "trunk" else limbs[int(host[4:])]
        s = (s_or_z + 0.45) if host == "trunk" else s_or_z
        p, rh, T = hb.at(s)
        T = Vector(T)
        if host == "trunk":
            out_d = Vector((math.cos(math.radians(az)), math.sin(math.radians(az)), 0.25)).normalized()
        else:
            side = T.cross(Vector((0, 0, 1)))
            out_d = (side.normalized() + Vector((0, 0, 0.6))).normalized()
        start = V(p)
        end = start + out_d * (rh + L)
        pts = [start.lerp(end, j / 6) for j in range(7)]
        rads = [r * (1.25 - 0.25 * j / 6) for j in range(7)]
        b = Br(pts, rads, 2, "stub", hb, s, twist=0.2, seed=rng.randint(1, 10 ** 6), bark=dict(DEAD_BARK_TRUNK))
        b.k = 0.14
        b.stub_end = (tuple(end), tuple(out_d), r)
        out.append(b)
    return out


def knot_list(spec, trunk, limbs):
    out = []
    for host, s_or_z, az, r in spec["knots"]:
        hb = trunk if host == "trunk" else limbs[int(host[4:])]
        s = (s_or_z + 0.45) if host == "trunk" else s_or_z
        p, rh, T = hb.at(s)
        if host == "trunk":
            n = Vector((math.cos(math.radians(az)), math.sin(math.radians(az)), 0))
        else:
            T = Vector(T)
            n = T.cross(Vector((0, 0, 1))).normalized()
        c = V(p) + n * rh
        out.append((c, n, r))
    return out


# ================================================================== the SDF core
def hollow_rr(Q, c_surf, n, H):
    """normalised 'radius' of the almond-shaped hollow opening (1 = the rim) + local coords (z = out of the bark)."""
    rot = frame_from(n)
    L = (Q - c_surf) @ rot.T
    ang = np.arctan2(L[:, 1] / H["hgt"], L[:, 0] / H["w"])
    wob = 1.0 + 0.12 * PNZ(np.cos(ang) * 1.3 + 4.0, np.sin(ang) * 1.3, 7.7) + 0.05 * np.sin(3 * ang + 1)
    ex = L[:, 0] / (H["w"] * wob * (1 - 0.35 * np.clip(np.abs(L[:, 1]) / H["hgt"], 0, 1) ** 2))
    ey = L[:, 1] / (H["hgt"] * wob)
    return np.sqrt(ex * ex + ey * ey), L


def core_sdf(spec, core, stubs, knots, h, groove, hollow=True, face=None, deflect=None):
    allP = np.concatenate([P for _, P, _ in core])
    allR = max(float(R.max()) for _, _, R in core)
    lo = allP.min(0) - allR - 0.6
    hi = allP.max(0) + allR + 0.6
    lo[2] = -0.6
    band = 0.42
    sdf = SDF(lo, hi, h, band)
    t0 = time.time()
    for br, P, R in core:
        add_branch_sdf(sdf, br, P, R, groove, br.k, deflect if br.kind == "trunk" else None)
    log("  sdf branches", len(core), "%.1fs" % (time.time() - t0))
    # knots: a swollen ring of bark with a sunken eye
    for c, n, r in knots:
        c = np.array(c)
        n_ = np.array(n)

        def fk(buf, Q, c=c, n_=n_, r=r):
            rot = frame_from(n_)
            bump = sd_ellipsoid(Q, c - n_ * r * 0.2, (r * 1.15, r * 1.5, r * 0.75), rot)
            d = smin(buf, bump, r * 0.9)
            eye = sd_ellipsoid(Q, c + n_ * r * 0.42, (r * 0.42, r * 0.6, r * 0.32), rot)
            return smax(d, -eye, r * 0.25)
        sdf.apply_points(c - 2.2 * r - band, c + 2.2 * r + band, fk)
    # broken stub ends: jagged splintered cut
    for b in stubs:
        e, dvec, r = b.stub_end
        e = np.array(e)
        dv = np.array(dvec)

        def fs(buf, Q, e=e, dv=dv, r=r, seed=b.seed):
            plane = (Q - (e - dv * r * 0.5)) @ dv
            jag = 0.09 * PNZ(Q[:, 0] * 9 + seed % 50, Q[:, 1] * 9, Q[:, 2] * 9) + 0.07 * np.sin(
                np.arctan2(Q[:, 1] - e[1], Q[:, 0] - e[0]) * 5)
            return np.maximum(buf, plane + jag)
        sdf.apply_points(e - 3 * r - band, e + 3 * r + band, fs)
    # hollow (DeadTree): rolled lip, then the cavity
    hol = None
    if hollow and spec.get("hollow"):
        H = spec["hollow"]
        trunk = core[0][0]
        s = H["z"] + 0.45
        p, r, T = trunk.at(s)
        a = math.radians(H["az"])
        n = np.array([math.cos(a), math.sin(a), 0.0])
        c_surf = np.array(p) + n * r * 0.95
        hol = dict(c=c_surf, n=n, r=r)

        def fh(buf, Q):
            rr, L = hollow_rr(Q, c_surf, n, H)
            scale = 0.5 * (H["w"] + H["hgt"]) * 0.75
            # the callus lip: a thick rolled ring of bark around the opening, swelling out of the trunk
            ring = np.sqrt(((rr - 1.08) * scale) ** 2 + (L[:, 2] - 0.02) ** 2) - H["lip"]
            d = smin(buf, ring, 0.16)
            cav = np.maximum((rr - 0.9) * scale, -(L[:, 2] + H["depth"]))
            cav = smax(cav, -(L[:, 2] + H["depth"] * 1.0), 0.2)
            return smax(d, -cav, 0.07)
        sdf.apply_points(c_surf - 1.6, c_surf + 1.6, fh)
    if face is not None:
        face(sdf)
    # the ground: nothing below z = -0.25
    xy_lo, xy_hi = lo.copy(), hi.copy()
    xy_lo[2], xy_hi[2] = -0.6, 0.15

    def fg(buf, Q):
        return np.maximum(buf, -0.25 - Q[:, 2])
    sdf.apply_points(xy_lo, xy_hi, fg)
    return sdf, hol


# ================================================================== colour for the core
def make_extra(spec, hol, face_info=None):
    def extra(col, rough, Vw, Nw):
        if hol is not None:
            H = spec["hollow"]
            rr, L = hollow_rr(Vw, hol["c"], hol["n"], H)
            depth = -L[:, 2]                          # how far into the trunk
            inside = sm(1.02, 0.92, rr) * sm(0.02, 0.14, depth)
            dark = mixc(np.tile(PAL["hollow2"], (len(Vw), 1)), np.tile(PAL["hollow"], (len(Vw), 1)),
                        sm(0.12, 0.5, depth))
            col = mixc(col, dark, inside)
            rough = rough * (1 - inside) + 0.95 * inside
        if face_info is not None:
            col, rough = face_info(col, rough, Vw, Nw)
        return col, rough
    return extra


def stub_colour(stubs):
    def f(col, rough, Vw, Nw):
        for b in stubs:
            e, dv, r = b.stub_end
            e, dv = np.array(e), np.array(dv)
            along = (Vw - e) @ dv
            lat = np.linalg.norm((Vw - e) - np.outer(along, dv), axis=1)
            m = sm(-r * 0.75, -r * 0.35, along) * (1 - sm(r * 0.85, r * 1.05, lat)) * np.clip(Nw @ dv, 0, 1) ** 0.5
            ring = 0.5 + 0.5 * np.sin(lat / max(r, 0.05) * 22)
            wood = mixc(np.tile(PAL["stubend"], (len(Vw), 1)), np.tile(PAL["wood2"], (len(Vw), 1)), 0.4 * ring)
            col = mixc(col, wood, m)
            rough = rough * (1 - m) + 0.7 * m
        return col, rough
    return f


def colour_core(ob, core, extra, seed, deflect=None, lichen_fn=None):
    me = ob.data
    n = len(me.vertices)
    Vt = np.empty(n * 3, np.float32)
    me.vertices.foreach_get("co", Vt)
    Vt = Vt.reshape(-1, 3).astype(np.float64)
    Nt = np.empty(n * 3, np.float32)
    me.vertices.foreach_get("normal", Nt)
    Nt = Nt.reshape(-1, 3).astype(np.float64)
    at = core_vertex_attrs(core, Vt, deflect)
    col, rough = bark_colours(at, Vt, Nt, seed=seed, extra=extra, lichen_fn=lichen_fn)
    set_colors(me, "Col", [tuple(c) for c in col])
    set_colors(me, "Rough", [(r, r, r) for r in rough])


def light_smooth(ob, factor=0.5, iters=2):
    m = ob.modifiers.new("Sm", "SMOOTH")
    m.factor = factor
    m.iterations = iters
    apply_mods(ob)


# ================================================================== tubes
def tube_colfn(seed):
    def f(at, Pv, dirs):
        return bark_colours(at, Pv, dirs, seed=seed, lichen_amt=0.8)
    return f


def buried_fn_for(br):
    """flag tube points that lie inside the branch this tube grows out of (its parent, or its own SDF part)."""
    cont = []
    sc = br.s_at_radius(RC)
    if sc > 0.15:
        cont.append(br.cut(0.0, sc))
    if br.parent is not None:
        cont.append((br.parent.P, br.parent.R))

    def f(Pv):
        out = np.zeros(len(Pv), np.float32)
        for P, R in cont:
            d, seg, t = branch_seg_points(np.asarray(P, np.float64), np.asarray(R, np.float64),
                                          np.asarray(Pv, np.float64), 0.3)
            out = np.maximum(out, ((seg >= 0) & (d < -0.012)).astype(np.float32))
        return out
    return f


def build_tubes_hi(tubes, name, seed, mat):
    acc = MeshAcc()
    cf = tube_colfn(seed)
    for br, P, R, s0 in tubes:
        tube_hi(acc, br, P, R, s0, step=0.035, colfn=cf, tip_cap=True, start_cap=True, buried_fn=buried_fn_for(br))
    ob = acc.build(name)
    ob.data.materials.append(mat)
    return ob


def lo_sides(r):
    return 10 if r >= 0.1 else 8 if r >= 0.06 else 6 if r >= 0.035 else 5 if r >= 0.022 else 4


def build_tubes_lo(tubes, name):
    acc = MeshAcc()
    for br, P, R, s0 in tubes:
        tube_lo(acc, P, R, lo_sides(float(R.max())), tip_cap=True, start_cap=False,
                ang_deg=9.0 if R.max() > 0.05 else 13.0, max_len=0.6)
    ob = acc.build(name, colors=False, uvs=True)
    return ob


# ================================================================== webs + silk + spider points
class SubBranch:
    """a view of a branch from arclength s0 on (the side of a crotch between a branch and its side branch)."""

    def __init__(self, br, s0):
        self.br, self.s0 = br, s0
        self.length = br.length - s0

    def at(self, s):
        return self.br.at(self.s0 + s)


def fork_candidates(tree, trunk, limbs):
    """crotches a web can span: (fork point, its radius, side 1, side 2, start arclength on side 1 / side 2)."""
    out = []
    for b in tree:
        if b.level not in (1, 2):
            continue
        kids = [c for c in b.children if abs(c.ps - b.length) < 1e-6]
        if len(kids) >= 2:
            out.append((V(b.P[-1]), float(b.R[-1]), kids[0], kids[1], 0.15, 0.15))
    # between neighbouring main limbs above the trunk
    top = V(trunk.P[-1])
    L = [l for l in limbs if l.ps > trunk.length * 0.8]
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            out.append((top, float(trunk.R[-1]) * 0.8, L[i], L[j], 0.9, 0.9))
    # between a branch (or the trunk) and a side branch growing out of it
    for b in tree:
        if b.level > 2 or b.kind in ("root", "stub"):
            continue
        for c in b.children:
            if c.kind == "stub" or c.ps > b.length - 1.2 or c.length < 1.5:
                continue
            p, r, T = b.at(c.ps)
            out.append((V(p), float(r), SubBranch(b, c.ps), c, float(r) * 1.3, float(r) * 1.3))
    return out


def side_points(c, s_lo, s_hi, cen, m, push=1.06):
    pts = []
    for k in range(m + 1):
        s = s_lo + (s_hi - s_lo) * k / m
        p, r, T = c.at(s)
        p, T = V(p), V(T)
        to = cen - p
        perp = to - T * to.dot(T)
        pts.append(p + perp.normalized() * r * push)
    return pts


def web_frame(F, rF, c1, c2, l1, l2, sA, sB):
    """the web's frame polygon in a crotch: crotch point, points along both branches, a sagging free edge."""
    A, B = V(c1.at(sA)[0]), V(c2.at(sB)[0])
    cen = (F + A + B) / 3
    Fp = F + (cen - F).normalized() * rF * 1.1
    side1 = side_points(c1, l1, sA, cen, max(4, int((sA - l1) / 0.3)))
    side2 = side_points(c2, l2, sB, cen, max(4, int((sB - l2) / 0.3)))
    Ap, Bp = side1[-1], side2[-1]
    dn = ((F - (Ap + Bp) * 0.5).normalized() * 0.55 + Vector((0, 0, -0.45))).normalized()
    cat = catenary(Ap, Bp, 10, 0.09 * (Ap - Bp).length, down=dn)
    frame3 = [Fp] + side1 + cat[1:-1] + list(reversed(side2))
    return dict(A=A, B=B, cen=cen, Fp=Fp, side1=side1, side2=side2, Ap=Ap, Bp=Bp, cat=cat, frame3=frame3)


def frame_metrics(frame3, hub_frac=0.28):
    """what build_web will really make of a frame: its best-fit plane normal, the planar frame's widths (max / min
    over 24 directions = how big and how un-sliver-like the web is), the hub and the spoke lengths."""
    c = sum(frame3, Vector()) / len(frame3)
    M = np.array([tuple(p - c) for p in frame3])
    _, sv, vt = np.linalg.svd(M)
    nrm = Vector(vt[2]).normalized()
    e1 = Vector(vt[0]).normalized()
    e2 = nrm.cross(e1).normalized()
    P2 = np.array([((p - c).dot(e1), (p - c).dot(e2)) for p in frame3])
    th = np.linspace(0, math.pi, 24, endpoint=False)
    D = np.stack([np.cos(th), np.sin(th)], 1)
    pr = P2 @ D.T
    w = pr.max(0) - pr.min(0)
    ax, ay = P2.mean(0)
    hx, hy = ax + (P2[0, 0] - ax) * hub_frac, ay + (P2[0, 1] - ay) * hub_frac
    poly2 = [tuple(q) for q in P2]
    L = []
    for k in range(12):
        a = 2 * math.pi * k / 12
        h = poly_hit((hx, hy), (math.cos(a), math.sin(a)), poly2)
        L.append(h[0] if h else 0.0)
    L = np.array(L)
    return dict(n=nrm, wmax=float(w.max()), wmin=float(w.min()), hub=c + e1 * hx + e2 * hy,
                spoke_med=float(np.median(L)), spokes_ok=int((L > 0.5).sum()), c=c, e1=e1, e2=e2, P2=P2,
                apex=Vector(frame3[0]), frame3=frame3)


def _in_poly(x, y, P2):
    inside = False
    n = len(P2)
    for i in range(n):
        x1, y1 = P2[i]
        x2, y2 = P2[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def pierce_count(m, segs, skip_r=0.6):
    """how many segments (3D (p, q) pairs) pass through the web's planar frame polygon (away from its apex)."""
    c, n = m["c"], m["n"]
    k = 0
    for p, q in segs:
        da, db = (p - c).dot(n), (q - c).dot(n)
        if da * db >= 0:
            continue
        x = p + (q - p) * (da / (da - db))
        if (x - m["apex"]).length < skip_r:
            continue
        if _in_poly((x - c).dot(m["e1"]), (x - c).dot(m["e2"]), m["P2"]):
            k += 1
    return k


def branch_segs(tree, skip=()):
    out = []
    for b in tree:
        if b.level > 2 or b.kind == "root" or any(b is x for x in skip):
            continue
        for i in range(len(b.P) - 1):
            out.append((V(b.P[i]), V(b.P[i + 1])))
    return out


def pick_webs(cands, requests, tree=()):
    """one crotch per request {orient: front|side|any, r: web radius, zmin/zmax: hub height, in_front}.
    front = the web plane faces Blender +-Y within ~30 deg (seen face-on from the front and the back),
    side = faces +-X. Webs are kept > 3.2 studs apart.
    Review round 1: score what build_web REALLY builds (the best-fit plane of the whole frame polygon, its widths)
    instead of the crotch triangle: a crotch whose branches curve out of the triangle's plane gave a sliver web."""
    grid = [1.2 + 0.4 * k for k in range(13)]
    chosen = []
    cache = {}
    for q in requests:
        # stage 1: cheap triangle score (no orientation) -> the 400 best pairs
        pre = []
        for ci, (F, rF, c1, c2, l1, l2) in enumerate(cands):
            if any(ci == x[0] for x in chosen):
                continue
            pa = [(sA, V(c1.at(sA)[0])) for sA in grid if l1 + 0.6 <= sA <= 0.88 * c1.length]
            pb = [(sB, V(c2.at(sB)[0])) for sB in grid if l2 + 0.6 <= sB <= 0.88 * c2.length]
            for sA, A in pa:
                for sB, B in pb:
                    if (A - F).cross(B - F).length < 1e-6:
                        continue
                    ang = math.degrees((A - F).angle(B - F))
                    hub = (F + A + B) / 3
                    hub = hub + (F - hub) * 0.28
                    R = 0.85 * max((hub - F).length, (hub - A).length, (hub - B).length)
                    sc = -abs(R - q["r"]) / 0.6 - max(0.0, 30 - ang) / 10 - max(0.0, ang - 125) / 10
                    sc -= 1.5 * (max(0.0, q["zmin"] - hub.z) + max(0.0, hub.z - q["zmax"]))
                    pre.append((sc, ci, sA, sB))
        pre.sort(key=lambda t: -t[0])
        best = None
        for _, ci, sA, sB in pre[:900]:
            key = (ci, sA, sB)
            if key not in cache:
                F, rF, c1, c2, l1, l2 = cands[ci]
                fr = web_frame(F, rF, c1, c2, l1, l2, sA, sB)
                cache[key] = frame_metrics(fr["frame3"])
            m = cache[key]
            n_, hub = m["n"], m["hub"]
            if "pierce" not in m:
                F, rF, c1, c2, l1, l2 = cands[ci]
                own = [getattr(c1, "br", c1), getattr(c2, "br", c2)]
                own += [b for b in tree if any(x in b.children for x in own)]       # the crotch's parent branch
                m["pierce"] = pierce_count(m, branch_segs(tree, own))
            Wt = 2.0 * q["r"]
            sc = -abs(m["wmax"] - Wt) / 0.8 - 6.0 * max(0.0, 0.62 * Wt - m["wmin"]) / Wt
            sc -= 0.5 * max(0, 10 - m["spokes_ok"])
            sc -= 3.0 * max(0.0, abs(n_.z) - 0.55)
            sc -= 1.5 * (max(0.0, q["zmin"] - hub.z) + max(0.0, hub.z - q["zmax"]))
            if q["orient"] == "front":
                sc -= 10.0 * max(0.0, 0.87 - abs(n_.y))
            elif q["orient"] == "side":
                sc -= 10.0 * max(0.0, 0.8 - abs(n_.x))
            if q.get("in_front"):
                sc -= 2.0 * max(0.0, hub.y + 0.2)
            if q.get("in_back"):
                sc -= 2.0 * max(0.0, 0.2 - hub.y)
            sc -= 8.0 * m["pierce"]
            for x in chosen:
                # another web: never closer than 2 studs, and the two frames must not cut through each other
                mx = x[5]
                fa, fb = m["frame3"], mx["frame3"]
                cross = pierce_count(mx, [(fa[i], fa[(i + 1) % len(fa)]) for i in range(len(fa))], 0.9) +                     pierce_count(m, [(fb[i], fb[(i + 1) % len(fb)]) for i in range(len(fb))], 0.9)
                if (hub - x[2]).length < 2.0 or cross:
                    sc -= 20.0
            if best is None or sc > best[0]:
                best = (sc, ci, hub, sA, sB, n_, m)
        if best is None:
            continue
        sc, ci, hub, sA, sB, n_, m = best
        chosen.append((ci, q, hub, sA, sB, m))
        log("web pick", q, "score %.2f" % sc, "hub", tuple(round(v, 2) for v in hub),
            "n", tuple(round(v, 2) for v in n_), "width max %.2f min %.2f spokes %d pierced %d" % (
                m["wmax"], m["wmin"], m["spokes_ok"], m["pierce"]))
    return [(q,) + tuple(cands[ci]) + (sA, sB) for ci, q, hub, sA, sB, m in chosen]


def build_webs(forks, name, rng):
    S = Strands()
    silk = MeshAcc()
    infos = []
    for wi, (q, F, rF, c1, c2, l1, l2, sA, sB) in enumerate(forks):
        fr = web_frame(F, rF, c1, c2, l1, l2, sA, sB)
        cen, Fp, Ap, Bp, cat, frame3 = fr["cen"], fr["Fp"], fr["Ap"], fr["Bp"], fr["cat"], fr["frame3"]
        fm = frame_metrics(frame3)
        Rq = q["r"]
        info = build_web(S, frame3, 0.28, radials=12 if Rq >= 2.2 else 10, rings=max(5, int(round(Rq / 0.34))),
                         rng=rng, bow=0.12 + 0.06 * Rq, broken=0.07, loose=2, r_frame=0.062, r_rad=0.05,
                         r_spi=0.04)
        nrm = Vector(info["normal"])
        lift = info.pop("lift")
        wc = Vector(info["centre"])
        onp = lambda qq: lift(qq - nrm * (qq - wc).dot(nrm))
        # silk: a gauzy mat filling the crotch (attached along both branches, frayed outer edge)
        nv, nu = 6, 6
        grid, uvg = [], []
        isl = 0 if wi % 2 == 0 else 2
        ox, oy = (isl % 2) * 0.5, (isl // 2) * 0.5
        for i in range(nv + 1):
            v = i / nv
            p1 = side_points(c1, l1, l1 + 0.42 * (sA - l1) * max(v, 0.04), cen, 1)[-1]
            p2 = side_points(c2, l2, l2 + 0.42 * (sB - l2) * max(v, 0.04), cen, 1)[-1]
            row, urow = [], []
            for j in range(nu + 1):
                u = j / nu
                qq = p1.lerp(p2, u)
                qq += Vector((0, 0, -1)) * 0.22 * (p1 - p2).length * math.sin(math.pi * u) * (0.3 + 0.7 * v)
                qq = onp(qq) + nrm * (-0.05 + 0.05 * math.sin(math.pi * u) * math.sin(math.pi * v))
                row.append(qq)
                urow.append((ox + 0.5 * (0.03 + 0.94 * u), oy + 0.5 * (0.03 + 0.94 * (1 - v))))
            grid.append(row)
            uvg.append(urow)
        two_sided_sheet(silk, grid, uvg, [(i, j) for i in range(nv) for j in range(nu)])
        # silk: a tattered drape hanging from the free edge thread
        isl = 1
        ox, oy = (isl % 2) * 0.5, (isl // 2) * 0.5
        nu2, nv2 = 8, 5
        top = [onp(cat[int(round(1 + 8 * j / nu2))]) - nrm * 0.03 for j in range(nu2 + 1)]
        grid, uvg = [], []
        seed = rng.uniform(0, 50)
        Ls = [0.55 + 0.75 * (0.5 + 0.5 * noise.noise(Vector((j * 0.45, seed, 0.3)))) * math.sin(
            math.pi * (0.1 + 0.8 * j / nu2)) ** 0.6 for j in range(nu2 + 1)]
        for i in range(nv2 + 1):
            v = i / nv2
            row, urow = [], []
            for j in range(nu2 + 1):
                u = j / nu2
                qq = top[j] + Vector((0, 0, -Ls[j] * v))
                qq += nrm * (0.08 * math.sin(math.pi * v) + 0.06 * math.sin(2 * math.pi * (u * 2 + v * 0.5) + seed) * v)
                row.append(qq)
                urow.append((ox + 0.5 * (0.03 + 0.94 * u), oy + 0.5 * (0.03 + 0.94 * (1 - v))))
            grid.append(row)
            uvg.append(urow)
        keep = [(i, j) for i in range(nv2) for j in range(nu2)
                if i == 0 or noise.noise(Vector((j * 0.7 + seed, i * 0.9, 1.1))) < 0.32]
        two_sided_sheet(silk, grid, uvg, keep)
        # silk: a denser, paler mat round the hub (island 3, radial fade) = a pale mass that survives at 40 studs
        hub = Vector(info["hub"])
        e1 = nrm.orthogonal().normalized()
        e2 = nrm.cross(e1).normalized()
        Rp = 0.32 * info["radius"]
        n_ = 6
        grid, uvg = [], []
        for i in range(n_ + 1):
            row, urow = [], []
            for j in range(n_ + 1):
                x, y = (j / n_ * 2 - 1) * Rp, (i / n_ * 2 - 1) * Rp
                row.append(hub + e1 * x + e2 * y - nrm * 0.025)
                urow.append((0.5 + 0.5 * (0.03 + 0.94 * (j / n_)), 0.5 + 0.5 * (0.03 + 0.94 * (i / n_))))
            grid.append(row)
            uvg.append(urow)
        two_sided_sheet(silk, grid, uvg, [(i, j) for i in range(n_) for j in range(n_)])
        info.update(fork=tuple(F), anchors=[tuple(Fp), tuple(Ap), tuple(Bp)], request=q,
                    span_max=round(fm["wmax"], 2), span_min=round(fm["wmin"], 2))
        infos.append(info)
    web = S.acc.build(name + "_Web", colors=False)
    # planar UVs for the small strand texture
    me = web.data
    uvl = me.uv_layers.new(name="UVMap")
    co = np.array([v.co for v in me.vertices])
    lo, hi = co.min(0), co.max(0)
    uv = []
    for lp in me.loops:
        c = co[lp.vertex_index]
        uv += [float((c[0] - lo[0] + 0.37 * (c[1] - lo[1])) / max(1e-6, (hi - lo)[0] + 0.37 * (hi - lo)[1])),
               float((c[2] - lo[2]) / max(1e-6, (hi - lo)[2]))]
    uvl.data.foreach_set("uv", uv)
    sk = silk.build(name + "_WebSilk", colors=False, uvs=True)
    return web, sk, infos


def spider_points(tree, objs, n, exclude):
    bvh = []
    for o in objs:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bvh.append(BVHTree.FromBMesh(bm))
        bm.free()

    def drop(p, maxd=8.0):
        best = maxd
        for t in bvh:
            hit = t.ray_cast(p, Vector((0, 0, -1)), maxd)
            if hit[0] is not None:
                best = min(best, hit[3])
        return best

    cands = []
    for b in tree:
        if b.level not in (1, 2) or b.kind == "stub":
            continue
        for s in np.arange(0.6, b.length - 0.3, 0.25):
            p, r, T = b.at(float(s))
            p, T = V(p), V(T)
            hd = math.hypot(p.x, p.y)
            if abs(T.z) > 0.6 or not (6.0 < p.z < 11.5) or hd < 2.4 or r < 0.07:
                continue
            u = p - Vector((0, 0, r * 0.98))
            free = drop(u - Vector((0, 0, 0.02)))
            ring = min(drop(u + Vector((math.cos(a) * 1.2, math.sin(a) * 1.2, -0.3)))
                       for a in np.linspace(0, 6.28, 7)[:-1])
            if free < 4.0:
                continue
            cands.append((min(free, 6.0) + 0.6 * min(ring, 6.0) + 0.3 * hd, u, free, ring, b.id, r))
    cands.sort(key=lambda c: -c[0])
    chosen = []
    for c in cands:
        u = c[1]
        if any((u - Vector(e)).length < 2.0 for e in exclude):
            continue
        az = math.atan2(u.y, u.x)
        if all(abs((az - math.atan2(o[1].y, o[1].x) + math.pi) % (2 * math.pi) - math.pi) > math.radians(70)
               for o in chosen):
            chosen.append(c)
        if len(chosen) >= n:
            break
    return [dict(point=tuple(round(v, 3) for v in c[1]), free_drop=round(c[2], 2), clear_ring=round(c[3], 2),
                 branch_radius=round(c[5], 3)) for c in chosen]


# ================================================================== shared setup
def get_spec(kind):
    if kind == "dead":
        return DEAD, DEAD_LV, DEAD_BARK_TRUNK
    return HAUNTED, HAUNTED_LV, HAUNTED_BARK_TRUNK


def setup(kind):
    spec, LV, tb = get_spec(kind)
    if "seed_search" in CFG:
        choose_seed(spec, LV, tb, range(1, 80))
    tree, trunk, roots, limbs = build_skeleton(spec, LV, tb)
    k = fit_scale(tree, spec)
    log("skeleton", stats(tree), "scale", round(k, 3), "seed", spec["seed"])
    rng = random.Random(spec["seed"] + 5)
    stubs = stub_branches(spec, rng, trunk, limbs)
    knots = knot_list(spec, trunk, limbs)
    core, tubes = split_items(tree)
    core += [(b, b.P, b.R) for b in stubs]
    return dict(spec=spec, LV=LV, tree=tree, trunk=trunk, roots=roots, limbs=limbs, stubs=stubs, knots=knots,
                core=core, tubes=tubes, rng=rng)


def face_hooks(ctx):
    """(sdf face function, colour hook, bark deflection) - the HauntedTree overrides these."""
    if ctx["spec"].get("face"):
        return haunted_face(ctx)
    return None, None, None


def chain_hooks(*fs):
    fs = [f for f in fs if f is not None]

    def f(col, rough, Vw, Nw):
        for g in fs:
            col, rough = g(col, rough, Vw, Nw)
        return col, rough
    return f


def preview(kind):
    sc = fresh(8)
    ctx = setup(kind)
    spec, core, tubes, stubs, knots = ctx["spec"], ctx["core"], ctx["tubes"], ctx["stubs"], ctx["knots"]
    face_fn, face_col, deflect = face_hooks(ctx)
    h = 0.05 if CFG["fast"] else 0.028
    sdf, hol = core_sdf(spec, core, stubs, knots, h, groove=True, face=face_fn, deflect=deflect)
    ob = sdf.mesh("Core_hi")
    log("core mesh", len(ob.data.polygons))
    colour_core(ob, core, make_extra(spec, hol, chain_hooks(stub_colour(stubs), face_col)), spec["seed"], deflect,
                getattr(face_col, "lichen_fn", None))
    ob.data.materials.append(mat_vc("BarkPrev"))
    tob = build_tubes_hi(tubes, "Tubes_hi", spec["seed"], mat_vc("BarkPrevT"))
    log("tubes hi", len(tob.data.polygons))
    if spec.get("leaves") and "noleaves" not in CFG:
        build_leaves(ctx, "Prev")
    review_setup(res=(1200, 900))
    garden_set()
    shoot_fov(os.path.join(WIP, kind + "_prev_25.png"), (6, -24, 9), (0, 0, 7.0), vfov=70)
    shoot_fov(os.path.join(WIP, kind + "_prev_side.png"), (24, 5, 9), (0, 0, 7.0), vfov=70)
    if spec.get("face"):
        fz = spec["face"]["z"]
        shoot_fov(os.path.join(WIP, kind + "_prev_close.png"), (1.2, -7.5, fz + 0.6), (0, 0, fz - 0.2), lens=35)
        shoot_fov(os.path.join(WIP, kind + "_prev_40.png"), (4.0, -40.0, 7.5), (0, 0, 5.0), vfov=70)
    else:
        shoot_fov(os.path.join(WIP, kind + "_prev_close.png"), (3.0, -7.5, 3.0), (0.3, 0, 2.2), lens=35)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(WIP, kind + "_preview.blend"))


# ================================================================== build (hi + game meshes, webs, UVs)
def split_core(lo, name, zc):
    bm = bmesh.new()
    bm.from_mesh(lo.data)
    bm.faces.ensure_lookup_table()
    bm.faces.index_update()
    # by face centre height, then hand every small island a cut leaves behind (< 60 faces, e.g. a sliver of an arm
    # underside dipping below the cut) to the other part, where it is connected
    up = np.array([f.calc_center_median().z >= zc for f in bm.faces])
    for _ in range(2):
        seen = np.zeros(len(up), bool)
        for f in bm.faces:
            if seen[f.index]:
                continue
            side = up[f.index]
            comp, stack = [f.index], [f]
            seen[f.index] = True
            while stack:
                g = stack.pop()
                for e in g.edges:
                    for h in e.link_faces:
                        if not seen[h.index] and up[h.index] == side:
                            seen[h.index] = True
                            stack.append(h)
                            comp.append(h.index)
            if len(comp) < 60:
                up[comp] = not side
    out = []
    for nm, keep in (("Trunk", False), ("Limbs", True)):
        b2 = bm.copy()
        b2.faces.ensure_lookup_table()
        b2.faces.index_update()
        bmesh.ops.delete(b2, geom=[f for f in b2.faces if up[f.index] != keep], context="FACES")
        bmesh.ops.delete(b2, geom=[v for v in b2.verts if not v.link_faces], context="VERTS")
        me = bpy.data.meshes.new(name + "_" + nm)
        b2.to_mesh(me)
        b2.free()
        for p in me.polygons:
            p.use_smooth = True
        out.append(link(bpy.data.objects.new(name + "_" + nm, me)))
    bm.free()
    bpy.data.objects.remove(lo)
    return out


def texel_density(ob, size):
    me = ob.data
    uvl = me.uv_layers.active.data
    a3 = a2 = 0.0
    for p in me.polygons:
        a3 += p.area
        uv = [uvl[li].uv for li in p.loop_indices]
        for k in range(1, len(uv) - 1):
            a2 += abs((uv[k][0] - uv[0][0]) * (uv[k + 1][1] - uv[0][1])
                      - (uv[k + 1][0] - uv[0][0]) * (uv[k][1] - uv[0][1])) / 2
    return dict(uv_fill=round(a2, 3), px_per_stud=round((a2 * size * size / max(a3, 1e-6)) ** 0.5, 1),
                area=round(a3, 1))


TRI = dict(dead=dict(Trunk=13800), haunted=dict(Trunk=13500))


def blend_path(kind):
    return os.path.join(OUT, kind + "_tree.blend")


def build(kind):
    sc = fresh(24)
    t0 = time.time()
    ctx = setup(kind)
    spec, core, tubes, stubs, knots = ctx["spec"], ctx["core"], ctx["tubes"], ctx["stubs"], ctx["knots"]
    name = spec["name"]
    face_fn, face_col, deflect = face_hooks(ctx)
    rep = {}
    # ---- HI core
    h = 0.05 if CFG["fast"] else 0.025
    sdf, hol = core_sdf(spec, core, stubs, knots, h, groove=True, face=face_fn, deflect=deflect)
    hi = sdf.mesh(name + "_Trunk_hi")
    del sdf
    rep["core_hi_clean"] = clean_mesh(hi, min_faces=400, hole_edges=24)
    colour_core(hi, core, make_extra(spec, hol, chain_hooks(stub_colour(stubs), face_col)), spec["seed"], deflect,
                getattr(face_col, "lichen_fn", None))
    hi.data.materials.append(mat_bark_hi("BarkHi", bump=0.3))
    rep["trunk_hi_tris"] = 2 * len(hi.data.polygons)
    log("hi core", rep["trunk_hi_tris"])
    # ---- HI tubes
    thi = build_tubes_hi(tubes, name + "_Branches_hi", spec["seed"], mat_bark_hi("BarkHiT", bump=0.2, scale=40))
    rep["branches_hi_tris"] = tris_of(thi)
    log("hi tubes", rep["branches_hi_tris"])
    # ---- GAME core: the same field, no furrows, coarse voxels, decimated
    sdf, _ = core_sdf(spec, core, stubs, knots, 0.06 if CFG["fast"] else 0.045, groove=False, face=face_fn,
                      deflect=deflect)
    lo = sdf.mesh(name + "_Core")
    del sdf
    rep["core_lo_clean"] = clean_mesh(lo, min_faces=200, hole_edges=24)
    n0 = len(lo.data.polygons) * 2
    target = TRI[kind]["Trunk"]
    dec = lo.modifiers.new("Dec", "DECIMATE")
    dec.ratio = min(1.0, target / n0)
    lo.modifiers.new("Tri", "TRIANGULATE")
    apply_mods(lo)
    rep["core_lo_clean2"] = clean_mesh(lo, min_faces=60, hole_edges=24, closed=True)
    # the flat ground cut under the trunk and roots is never seen: delete it
    bm = bmesh.new()
    bm.from_mesh(lo.data)
    cap = [f for f in bm.faces if f.normal.z < -0.85 and f.calc_center_median().z < -0.15]
    rep["ground_cap_faces"] = len(cap)
    bmesh.ops.delete(bm, geom=cap, context="FACES")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bm.to_mesh(lo.data)
    bm.free()
    # the cap's rim leaves a few single faces behind: drop every bit under 60 faces (no hole filling: the open
    # bottom stays open)
    rep["core_lo_clean3"] = clean_mesh(lo, min_faces=60, hole_edges=0)
    rep["trunk_tris"] = tris_of(lo)
    log("lo core", n0, "->", rep["trunk_tris"])
    # ---- GAME tubes
    tlo = build_tubes_lo(tubes, name + "_Branches")
    tlo.modifiers.new("Tri", "TRIANGULATE")
    apply_mods(tlo)
    rep["branches_tris"] = tris_of(tlo)
    log("lo tubes", rep["branches_tris"])
    # ---- split the core: Trunk (base .. just above the crotch) + Limbs, each gets its own 1024 maps
    zc = float(ctx["trunk"].P[-1][2]) + spec.get("split_dz", 0.8)
    lo_parts = split_core(lo, name, zc)
    rep["split_z"] = round(zc, 3)
    # ---- UVs
    for part in lo_parts:
        rep[part.name + "_uv"] = cyl_uv(part, core, margin=0.004)
        rep[part.name.split("_")[-1] + "_tris"] = tris_of(part)
    pack_uv(tlo, margin=0.004)
    rep["texel"] = {o.name: texel_density(o, 1024) for o in lo_parts + [tlo]}
    # ---- webs + silk
    rng = random.Random(spec["seed"] + 77)
    forks = pick_webs(fork_candidates(ctx["tree"], ctx["trunk"], ctx["limbs"]), spec["web_requests"], ctx["tree"])
    web, silk, winfo = build_webs(forks, name, rng)
    simg = strand_texture(256, 5, os.path.join(MAPS, name + "_Web_albedo.png"))
    web.data.materials.append(mat_img(name + "_WebMat", simg, rough=0.5))
    kimg = silk_texture(512, 4, 41, os.path.join(MAPS, name + "_WebSilk_albedo.png"))
    silk.data.materials.append(mat_img(name + "_SilkMat", kimg, alpha=True, rough=0.8))
    rep["web_tris"] = tris_of(web)
    rep["silk_tris"] = tris_of(silk)
    rep["webs"] = winfo
    # ---- leaves (HauntedTree)
    if spec.get("leaves"):
        lv = build_leaves(ctx, name)
        rep["leaves_tris"] = tris_of(lv)
    # ---- spider thread points
    # branch joints for the review close-ups (where tubes leave the core, 4.5 < z < 10)
    jts = []
    for br, P2, R2, s0 in tubes:
        if s0 > 0:
            jp = V(br.at(br.s_at_radius(RC))[0])
            if 4.5 < jp.z < 10 and all((jp - Vector(q)).length > 2.0 for q in jts):
                jts.append(tuple(jp))
    rep["joints"] = jts[:4]
    rep["spiders"] = spider_points(ctx["tree"], [hi, thi, web, silk], spec["spiders"], [w["hub"] for w in winfo])
    for o in (hi, thi):
        o.hide_render = True
        o.hide_viewport = True
    rep["build_s"] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, kind + "_build.json"), "w") as fh:
        json.dump(rep, fh, indent=1, default=str)
    bpy.ops.wm.save_as_mainfile(filepath=blend_path(kind))
    log("BUILD", json.dumps({k: v for k, v in rep.items() if k not in ("webs",)}, default=str))
    return rep


def bake(kind, which=("Trunk", "Limbs", "Branches")):
    bpy.ops.wm.open_mainfile(filepath=blend_path(kind))
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.render.threads_mode = "FIXED"
    sc.render.threads = 6
    spec = get_spec(kind)[0]
    name = spec["name"]
    o = bpy.data.objects
    lows = [x for x in o if x.type == "MESH" and not x.name.endswith("_hi")]
    his = [o[name + "_Trunk_hi"], o[name + "_Branches_hi"]]
    for hh in his:
        hh.hide_viewport = False
        hh.hide_render = False
    size = 256 if CFG["fast"] else 1024
    out = {}
    t0 = time.time()
    for part in ("Trunk", "Limbs"):
        if part not in which:
            continue
        lo = o[name + "_" + part]
        imgs = bake_part(lo, [o[name + "_Trunk_hi"]], size, name + "_" + part, cage=0.16, maxray=0.38,
                         ao_strength=0.48, ao_dist=1.3, all_lows=lows)
        pbr_material(lo, name + "_" + part + "_PBR", imgs)
        out[part + "_miss"] = round(imgs["miss_fraction"], 4)
        log("baked", part, out, "%.0fs" % (time.time() - t0))
    if "Branches" in which:
        lo = o[name + "_Branches"]
        # the core sculpt stays out of the branch bake: its AO drew a dark ring round every tube where it leaves the
        # core (the buried part is masked anyway); the core bake still gets its contact shade from the tubes
        o[name + "_Trunk_hi"].hide_render = True
        imgs = bake_part(lo, [o[name + "_Branches_hi"]], size, name + "_Branches", cage=0.05, maxray=0.12,
                         ao_strength=0.4, ao_dist=0.7, all_lows=lows, buried_attr="Buried")
        o[name + "_Trunk_hi"].hide_render = False
        out["Branches_buried_masked"] = round(imgs["buried_fraction"], 4)
        pbr_material(lo, name + "_Branches_PBR", imgs)
        out["Branches_miss"] = round(imgs["miss_fraction"], 4)
        log("baked branches", out, "%.0fs" % (time.time() - t0))
    for hh in his:
        hh.hide_render = True
        hh.hide_viewport = True
    for x in lows:
        for attr in ("visible_shadow", "visible_diffuse", "visible_glossy", "visible_transmission"):
            setattr(x, attr, True)
    bpy.ops.wm.save_as_mainfile(filepath=blend_path(kind))
    with open(os.path.join(OUT, kind + "_bake.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    return out


def export_parts(kind):
    spec = get_spec(kind)[0]
    name = spec["name"]
    o = bpy.data.objects
    names = [name + "_Trunk", name + "_Limbs", name + "_Branches"] + \
        ([name + "_Leaves"] if spec.get("leaves") else []) + [name + "_Web", name + "_WebSilk"]
    return [o[n] for n in names]


def hub_bed():
    """the hub look used by the reviewer: lawn, light-green garden bed (92,168,70) r 7.5, an orange 2 x 1 x 5 stud
    block = a player's height."""
    g = mat_noise("Lawn", lin((80, 150, 58)), lin((64, 128, 46)), nscale=0.35, detail=6, rough=0.9, lo=0.3, hi=0.7)
    bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, -0.03))
    bpy.context.active_object.data.materials.append(g)
    bed = mat_flat("Bed", lin((92, 168, 70)), rough=0.9)
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=7.5, depth=0.1, location=(0, 0, -0.05))
    bpy.context.active_object.data.materials.append(bed)
    blk = mat_flat("Player", lin((214, 102, 40)), rough=0.6)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(9.0, -1.0, 2.5))
    o = bpy.context.active_object
    o.scale = (2.0, 1.0, 5.0)
    o.data.materials.append(blk)


def render(kind):
    bpy.ops.wm.open_mainfile(filepath=blend_path(kind))
    sc = review_setup(res=(1280, 900))
    sc.eevee.taa_render_samples = 48
    sc.world.node_tree.nodes["Background"].inputs["Color"].default_value = (*lin((150, 196, 240)), 1)
    hub_bed()
    key_light(sc, az=-125, el=42, energy=4.2)
    spec = get_spec(kind)[0]
    for o in export_parts(kind):
        for m in o.data.materials:
            m.use_backface_culling = True            # Roblox renders single-sided
    rep = json.load(open(os.path.join(OUT, kind + "_build.json")))
    pre = os.path.join(OUT, "review_" + kind)
    for f in os.listdir(OUT):
        if f.startswith("review_" + kind) and f.endswith(".png"):
            os.remove(os.path.join(OUT, f))
    E = 5.0
    shots = {"front_25": ((0, -25, E), (0, 0, 7.0)), "back_25": ((0, 25, E), (0, 0, 7.0)),
             "left_25": ((-25, 0, E), (0, 0, 7.0)), "right_25": ((25, 0, E), (0, 0, 7.0)),
             "front_45": ((0, -45, E), (0, 0, 6.5)), "left_45": ((-45, 0, E), (0, 0, 6.5)),
             "q34_40": ((-28.3, -28.3, E), (0, 0, 6.5))}
    if spec.get("face"):
        fz = spec["face"]["z"]
        shots.update({"face_18": ((0.1, -18, E), (0, -1.4, fz)), "face_8": ((0.1, -8, E), (0, -1.4, fz)),
                      "face_side_R_6": ((6.0, -1.6, fz), (0.0, -1.2, fz - 0.1)),
                      "face_side_L_6": ((-6.0, -1.6, fz), (0.0, -1.2, fz - 0.1)),
                      "face_q34_15": ((-9, -12, E), (0, -1.4, fz)), "mouth_low_4": ((1.6, -4.4, 3.0), (0.05, -1.6, 3.5))})
    else:
        H = spec["hollow"]
        a = math.radians(H["az"])
        tgt = Vector((math.cos(a) * 0.8, math.sin(a) * 0.8, H["z"]))
        shots["hollow_7"] = (tuple(tgt + Vector((math.cos(a) * 7.0, math.sin(a) * 7.0, E - tgt.z))), tuple(tgt))
    for i, w in enumerate(rep.get("webs", [])):
        hub, nrm = Vector(w["hub"]), Vector(w["normal"])
        if nrm.dot(Vector((hub.x, hub.y, 0))) < 0:
            nrm = -nrm
        d = Vector((nrm.x, nrm.y, 0)).normalized()
        shots["web%d_close" % i] = (tuple(hub + d * 7.0 + Vector((0, 0, E - hub.z))), tuple(hub))
    for i, j in enumerate(rep.get("joints", [])[:3]):
        jv = Vector(j)
        d = Vector((jv.x, jv.y, 0)).normalized() if math.hypot(jv.x, jv.y) > 0.3 else Vector((0, -1, 0))
        shots["joint%d_below" % i] = (tuple(jv + d * 4.5 + Vector((0, 0, -3.0))), tuple(jv))
    out = []
    for nm, (loc, tgt) in shots.items():
        out.append(shoot_fov(pre + "_" + nm + ".png", loc, tgt, vfov=70))
    return out


def key_light(sc, az, el, energy=4.0):
    """sun coming FROM azimuth az (deg, 0 = +X, -90 = -Y = the front), elevation el: a raking front-side key"""
    sun = [o for o in sc.objects if o.type == "LIGHT"][0]
    a, e = math.radians(az), math.radians(el)
    d = -Vector((math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)))
    sun.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    sun.data.energy = energy


def export(kind):
    bpy.ops.wm.open_mainfile(filepath=blend_path(kind))
    spec = get_spec(kind)[0]
    objs = export_parts(kind)
    r = export_fbx(objs, os.path.join(CDIMP, "Halloween_" + spec["name"] + ".fbx"))
    lo, hi = bbox_of(objs)
    r["bbox_blender"] = [[round(float(v), 3) for v in lo], [round(float(v), 3) for v in hi]]
    r["tris"] = {o.name: tris_of(o) for o in objs}
    r["total_tris"] = sum(r["tris"].values())
    with open(os.path.join(OUT, kind + "_export.json"), "w") as fh:
        json.dump(r, fh, indent=1)
    log("EXPORT", json.dumps(r))
    return r


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    for flag in ("fast", "noleaves"):
        if flag in argv:
            CFG[flag] = True
            argv.remove(flag)
    if "seeds" in argv:
        CFG["seed_search"] = True
        argv.remove("seeds")
    kind = argv[0]
    for step in argv[1:]:
        if step == "preview":
            preview(kind)
        elif step == "build":
            build(kind)
        elif step == "bake":
            bake(kind)
        elif step == "bake_trunk":
            bake(kind, ("Trunk", "Limbs"))
        elif step == "bake_branches":
            bake(kind, ("Branches",))
        elif step == "render":
            render(kind)
        elif step == "export":
            export(kind)
    log("DONE")
