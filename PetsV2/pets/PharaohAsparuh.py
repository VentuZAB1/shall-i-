# Pharaoh Asparuh (Asparuh's pet): a fluffy Persian cat dressed as a little pharaoh. Chibi round head with the
# flat Persian face, huge copper slit-pupil eyes with Egyptian kohl wings, blue + gold striped nemes headdress with
# a golden cobra (uraeus) and a glowing turquoise gem, a broad gold/turquoise/lapis usekh collar with a glowing ankh,
# gold anklets, a big fluffy tail with gold rings. Personality: regal and a bit smug - chin up, slow royal blinks,
# looks down his nose at you; grooms his paw; does a cheeky butt-wiggle pounce when he thinks nobody is watching.
import math
import bmesh
from mathutils import Vector
import petkit as pk

DISPLAY = "Pharaoh Asparuh"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.0
C = pk.lin
FUR_TOP = C((228, 180, 122))
FUR = C((250, 232, 206))
FUR_W = C((255, 250, 240))
PAW = C((255, 246, 236))
PINK = C((246, 150, 160))
INNER_EAR = C((250, 178, 182))
LAPIS = C((34, 62, 168))
LAPIS_D = C((22, 38, 112))
GOLD = C((255, 202, 66))
GOLD_D = C((214, 140, 28))
TURQ = C((48, 196, 196))
KOHL = C((24, 18, 34))
GEM = "4cf2ff"

HEAD_C = Vector((0, -0.56, 1.50))
HEAD_R = (0.62, 0.52, 0.55)
EYE_PTS = [((0.62, -2.6, 1.56), (0.21, -0.7, 1.50)), ((-0.62, -2.6, 1.56), (-0.21, -0.7, 1.50))]
EYE_SIZE = (0.185, 0.205)
TAIL = [Vector((0, 0.92, 0.70)), Vector((0, 1.20, 0.96)), Vector((0, 1.34, 1.32)), Vector((0, 1.24, 1.66)),
        Vector((0, 1.05, 1.80))]


def body_color(co, n):
    c = pk.mix(FUR, FUR_TOP, pk.smooth(0.15, 0.9, n.z) * pk.smooth(-0.6, 0.2, co.y) * pk.smooth(0.3, 0.9, co.z))
    c = pk.mix(c, FUR_TOP, pk.smooth(0.85, 1.2, co.y) * 0.55)              # sandy tail + rump
    chest = pk.smooth(-0.1, -0.7, n.y) * pk.smooth(1.3, 0.75, co.z) * pk.smooth(0.3, -0.2, co.y)
    c = pk.mix(c, FUR_W, max(chest, pk.smooth(-0.2, -0.8, n.z)))            # white ruff + belly
    face = pk.smooth(-0.5, -0.95, n.y) * pk.smooth(0.95, 1.35, co.z) * pk.smooth(1.75, 1.45, co.z)
    c = pk.mix(c, FUR_W, face * 0.85)                                        # pale muzzle
    c = pk.mix(c, PAW, pk.smooth(0.16, 0.05, co.z))
    for sx in (1, -1):                                                       # blush
        c = pk.mix(c, PINK, pk.smooth(0.17, 0.04, (co - Vector((sx * 0.40, -1.00, 1.30))).length) * 0.55)
    return c


def model(k):
    hc, hr = HEAD_C, HEAD_R
    E = [
        ("ell", (0, 0.32, 0.66), (0.50, 0.70, 0.46)),                       # loaf body
        ("ell", (0, -0.16, 0.80), (0.48, 0.38, 0.46)),                      # chest
        ("ell", tuple(hc), hr),                                             # big round head
        ("ell", (0, -0.98, 1.34), (0.21, 0.10, 0.13)),                      # tiny flat muzzle
        ("ell", (0, -0.86, 1.14), (0.19, 0.13, 0.11)),                      # chin
        ("cap", TAIL[0], TAIL[1], 0.20), ("cap", TAIL[1], TAIL[2], 0.21),   # big fluffy tail
        ("cap", TAIL[2], TAIL[3], 0.19), ("cap", TAIL[3], TAIL[4], 0.15),
    ]
    for sx in (1, -1):
        E += [("ell", (sx * 0.44, -0.74, 1.28), (0.24, 0.20, 0.21)),        # fluffy cheeks
              ("ell", (sx * 0.56, -0.62, 1.20), (0.14, 0.13, 0.13)),        # cheek tuft
              ("cap", (sx * 0.27, -0.20, 0.50), (sx * 0.28, -0.26, 0.12), 0.15),
              ("ell", (sx * 0.28, -0.33, 0.08), (0.15, 0.19, 0.09)),        # front paws
              ("ell", (sx * 0.32, 0.70, 0.52), (0.25, 0.32, 0.31)),         # haunches
              ("cap", (sx * 0.33, 0.72, 0.36), (sx * 0.33, 0.70, 0.12), 0.15),
              ("ell", (sx * 0.33, 0.62, 0.08), (0.15, 0.19, 0.09))]
    for i in range(9):                                                      # scalloped chest ruff
        a = math.radians(-70 + 140 * i / 8)
        E.append(("ball", (0.40 * math.sin(a), -0.40 - 0.16 * math.cos(a), 1.00 - 0.10 * abs(math.sin(a))), 0.13))
    for i, t in enumerate((0.25, 0.5, 0.75)):                               # tail fluff bumps
        p = TAIL[1].lerp(TAIL[3], t)
        E.append(("ball", (0.0, p.y + 0.08, p.z), 0.17))
    k.body(E, body_color, tris=6000)

    k.eyes(EYE_PTS, size=EYE_SIZE, style="big", iris=(255, 150, 40), pupil="slit")

    def face(bm, L):
        loc, n = k.surf((0, -2.5, 1.40), (0, -0.8, 1.40))
        pk.ellipsoid(bm, L, loc + n * 0.005, (0.055, 0.04, 0.03), PINK, x_axis=(1, 0, 0), z_axis=n)
        for sx in (1, -1):
            # little 'w' mouth
            a, _ = k.surf((sx * 0.005, -2.5, 1.33), (sx * 0.005, -0.8, 1.33))
            b, _ = k.surf((sx * 0.06, -2.5, 1.30), (sx * 0.06, -0.8, 1.30))
            c, _ = k.surf((sx * 0.11, -2.5, 1.33), (sx * 0.11, -0.8, 1.33))
            pk.tube(bm, L, [a + Vector((0, -0.01, 0)), b + Vector((0, -0.01, 0)), c + Vector((0, -0.01, 0))],
                    0.011, KOHL, sides=6)
            # Egyptian kohl wings from the outer eye corners
            (o, t) = EYE_PTS[0 if sx > 0 else 1]
            eye, en = k.surf(o, t)
            ex, ey = EYE_SIZE
            pts = []
            for j, (dx, dz) in enumerate(((0.55, 0.15), (0.90, 0.12), (1.20, 0.30), (1.45, 0.55))):
                q = eye + Vector((sx * ex * dx, 0, ey * dz))
                try:
                    p, pn = k.surf(q + Vector((-sx * 0.3, -0.6, 0)), q + Vector((sx * 0.15, 0.4, 0)))
                except RuntimeError:
                    continue
                pts.append(p + pn * 0.012)
            pk.tube(bm, L, pts, lambda tt: 0.022 * (1 - tt) + 0.006, KOHL, sides=6)
            pts = []
            for dx, dz in ((0.2, -0.85), (0.7, -0.7), (1.15, -0.35)):
                q = eye + Vector((sx * ex * dx, 0, ey * dz))
                try:
                    p, pn = k.surf(q + Vector((-sx * 0.3, -0.6, 0)), q + Vector((sx * 0.15, 0.4, 0)))
                except RuntimeError:
                    continue
                pts.append(p + pn * 0.012)
            pk.tube(bm, L, pts, lambda tt: 0.012 * (1 - tt) + 0.005, KOHL, sides=6)
            # whiskers
            root, rn = k.surf((sx * 0.16, -2.5, 1.34), (sx * 0.16, -0.8, 1.34))
            for dz in (0.03, -0.02):
                pk.cone(bm, L, root + rn * 0.01 + Vector((0, 0, dz)), (sx * 1.0, -0.15, dz * 4), 0.30, 0.011, FUR_W,
                        bend_axis=(0, 1, 0), bend_deg=sx * 12, sides=5, n=5)
    k.part("Face", face, "Head")

    # --- nemes headdress: striped cap over the crown, gold brow band, lappets down the chest, back queue
    def nemes_tm(phi):
        # phi = 0 toward local +Y (pet's back); pi toward the face (-Y)
        f = 0.5 - 0.5 * math.cos(phi)          # 1 at the face, 0 at the back
        side = abs(math.sin(phi))
        return math.radians(118 - 74 * f + 14 * side * (1 - f))

    def nemes_col(r, phi, outer):
        f = 0.5 - 0.5 * math.cos(phi)
        if r > 0.84 and f > 0.5:
            return GOLD                           # brow band
        if not outer:
            return LAPIS_D
        return LAPIS if int(r * 11) % 2 == 0 else GOLD

    def nemes(bm, L):
        def flare(r, phi):
            # the classic nemes silhouette: the cloth flares out wide behind the cheeks and drops to the shoulders
            side = abs(math.sin(phi)) ** 1.5
            back = 0.5 + 0.5 * math.cos(phi)
            w = pk.smooth(0.55, 1.0, r)
            return 1.0 + 0.30 * w * max(side, back * 0.6), 0.22 * w * w * max(side, back * 0.5)
        pk.shell_cap(bm, L, hc + Vector((0, 0.02, 0.03)), (hr[0] * 1.06, hr[1] * 1.08, hr[2] * 1.07), nemes_tm,
                     nemes_col, thick=0.035, nu=64, nv=24, flare=flare)
        for sx in (1, -1):
            # lappets: from under the cap at the side of the head, laid over the cheek fluff + chest ruff
            out = Vector((sx * 0.8, -0.6, 0.1)).normalized()
            pts, nrms = [], []
            for i in range(9):
                t = i / 8
                q = Vector((sx * (0.56 - 0.14 * t), -0.46 - 0.12 * t, 1.18 - 0.58 * t))
                try:
                    hit, hn = k.surf(q + out * 1.2, q - out * 0.5)
                except RuntimeError:
                    continue
                pts.append(hit + hn * 0.035)
                nrms.append(hn)
            pk.strip(bm, L, pts, lambda t: 0.21 + 0.07 * t, lambda t: nrms[min(int(t * (len(nrms) - 1) + 0.5), len(nrms) - 1)],
                     lambda t, s: LAPIS if (int(t * 9) % 2 == 0 and t < 0.92) else GOLD, thick=0.04)
        # back queue (the gathered cloth tail)
        q0 = hc + Vector((0, 0.50, -0.22))
        pk.tube(bm, L, [q0, q0 + Vector((0, 0.12, -0.16)), q0 + Vector((0, 0.16, -0.36))], (0.13, 0.07),
                lambda t, a: GOLD if (int(t * 6) % 2 == 0) else LAPIS, sides=10)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    def nemes_w(co):
        if co.z > 1.18:
            return {"Head": 1.0}
        t = pk.smooth(0.92, 1.18, co.z)
        return {"Head": t, "Spine": 1 - t}
    k.part("Nemes", nemes, nemes_w)

    # --- uraeus: golden cobra rising from the brow band (gem = glow part)
    brow, bn = k.surf(hc + Vector((0, -2.0, 0.40)), hc + Vector((0, 0, 0.30)))
    k.uraeus = brow + bn * 0.07

    def uraeus(bm, L):
        b = k.uraeus
        pts = [b, b + Vector((0, -0.03, 0.06)), b + Vector((0, -0.04, 0.13))]
        pk.tube(bm, L, pts, (0.042, 0.034), GOLD, sides=8)
        pk.ellipsoid(bm, L, b + Vector((0, -0.05, 0.17)), (0.095, 0.03, 0.105), GOLD_D, z_axis=(0, -0.25, 1))
        pk.ellipsoid(bm, L, b + Vector((0, -0.075, 0.25)), (0.04, 0.05, 0.032), GOLD)
    k.part("Uraeus", uraeus, "Head")

    # --- ears poke out through the nemes, with gold cuffs
    def ears(bm, L):
        for sx in (1, -1):
            base, n = k.surf(hc + Vector((sx * 0.80, 0.05, 1.1)), hc + Vector((sx * 0.25, 0.05, 0.25)))
            up = Vector((sx * 0.55, 0.05, 1.0))
            pk.ear(bm, L, base - n * 0.05, up, (0, -1, 0.15), 0.40, 0.20, 0.07,
                   lambda h, s, f: INNER_EAR if (f < -0.2 and abs(s) < 0.65 and h < 0.8) else pk.mix(FUR_TOP, FUR, h * 0.3),
                   bend=-0.06)
            pk.torus(bm, L, base + up.normalized() * 0.15 - n * 0.02, 0.06, 0.022, GOLD,
                     x_axis=(1, 0, 0), z_axis=up, N=16, M=6)

    def ear_w(co):
        return {"Ear_L" if co.x > 0 else "Ear_R": 1.0}
    k.part("Ears", ears, ear_w)

    # --- usekh collar: bands of gold / turquoise / gold / lapis / gold beads conformed onto the chest
    def collar(bm, L):
        cen = Vector((0, -0.40, 1.00))
        nrm = Vector((0, -0.93, 0.36)).normalized()
        xa = Vector((1, 0, 0))
        ya = nrm.cross(xa).normalized()
        bands = [(0.20, 0.24, GOLD), (0.24, 0.30, TURQ), (0.30, 0.33, GOLD), (0.33, 0.40, LAPIS), (0.40, 0.44, GOLD)]
        N = 56
        a0, a1 = math.radians(-100), math.radians(100)   # a bib under the chin

        def onbody(r, a):
            q = cen + (xa * math.sin(a) + ya * -math.cos(a)) * r
            try:
                p, pn = k.surf(q + nrm * 0.9, q - nrm * 0.6)
            except RuntimeError:
                return None
            return p + pn * 0.03
        for r0, r1, col in bands:
            row0, row1 = [], []
            for i in range(N + 1):
                a = a0 + (a1 - a0) * i / N
                p0, p1 = onbody(r0, a), onbody(r1, a)
                if p0 is None or p1 is None:
                    row0.append(None)
                    row1.append(None)
                    continue
                v0, v1 = bm.verts.new(p0), bm.verts.new(p1)
                v0[L] = v1[L] = col
                row0.append(v0)
                row1.append(v1)
            for i in range(N):
                q = (row0[i], row1[i], row1[i + 1], row0[i + 1])
                if None not in q:
                    bm.faces.new(q)
        # bead drops on the outer edge
        for i in range(15):
            a = a0 + (a1 - a0) * (i + 0.5) / 15
            p = onbody(0.465, a)
            if p is not None:
                pk.ellipsoid(bm, L, p, (0.035, 0.035, 0.035), TURQ if i % 2 else GOLD, useg=8, vseg=6)
        # anklets on the front legs
        for sx in (1, -1):
            pk.torus(bm, L, (sx * 0.28, -0.27, 0.20), 0.165, 0.035, lambda b: GOLD if math.cos(b) > -0.2 else GOLD_D,
                     N=24, M=6)
    k.part("Collar", collar, lambda co: {"Leg_FL": 1.0} if (co.z < 0.4 and co.x > 0) else
           ({"Leg_FR": 1.0} if co.z < 0.4 else {"Spine": 1.0}))

    # --- gold rings on the tail
    def tail_rings(bm, L):
        for t, bone in ((0.30, None), (0.62, None)):
            p = TAIL[1].lerp(TAIL[2], t) if t < 0.5 else TAIL[2].lerp(TAIL[3], t - 0.3)
            d = (TAIL[2] - TAIL[1]).normalized() if t < 0.5 else (TAIL[3] - TAIL[2]).normalized()
            pk.torus(bm, L, p, 0.215, 0.05, lambda b: GOLD if math.cos(b) > -0.3 else GOLD_D, x_axis=(1, 0, 0),
                     z_axis=d, N=24, M=6)

    def tail_w(co):
        return {"Tail2": 1.0} if co.z < 1.3 else {"Tail3": 1.0}
    k.part("TailRings", tail_rings, tail_w)

    # --- eyelids for the slow royal blink (own bones, rotate down over the eyes)
    def lids(bm, L):
        for idx, (o, t) in enumerate(EYE_PTS):
            loc, n = k.surf(o, t)
            ex, ey = EYE_SIZE
            side = Vector((1, 0, 0)) - n * n.x
            m = pk.frame(loc - n * 0.04, side, n)
            # upper lid: top cap of a slightly bigger eye ellipsoid, fur coloured
            verts = pk.blob(bm, L, m, lambda u: Vector((u.x * ex * 1.13, max(u.y, 0.25) * ey * 1.12,
                                                         u.z * ex * 0.62 + 0.012)), FUR, 14, 9)
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-5)

    def lid_w(co):
        return {"Lid_L" if co.x > 0 else "Lid_R": 1.0}
    k.part("Lids", lids, lid_w)

    # --- glowing turquoise gems: uraeus gem + ankh pendant on the collar
    def gems(bm, L):
        b = k.uraeus
        pk.ellipsoid(bm, L, b + Vector((0, -0.085, 0.16)), (0.038, 0.022, 0.048), pk.lin((76, 242, 255)))
        top, tn = k.surf((0, -2.0, 0.55), (0, -0.3, 0.55))
        a = top + tn * 0.06
        col = pk.lin((76, 242, 255))
        pk.torus(bm, L, a + Vector((0, 0, 0.07)), 0.045, 0.016, col, x_axis=(1, 0, 0), z_axis=tn, N=14, M=6)
        pk.tube(bm, L, [a + Vector((0, 0, 0.03)), a + Vector((0, 0, -0.13))], 0.019, col, sides=6)
        pk.tube(bm, L, [a + Vector((-0.065, 0, 0.0)), a + Vector((0.065, 0, 0.0))], 0.017, col, sides=6)

    def gem_w(co):
        return {"Head": 1.0} if co.z > 1.3 else {"Spine": 1.0}
    pk.glow_part(k, "Glow_Gem", GEM, gems, gem_w)


def rig(k):
    k.joint("Spine", (0, 0.32, 0.72), "Root", tail=(0, -0.45, 0.2))
    k.joint("Neck", (0, -0.20, 1.00), "Spine")
    k.joint("Head", (0, -0.46, 1.26), "Neck", tail=(0, -0.3, 0.1))
    for side, sx in (("L", 1), ("R", -1)):
        o, t = EYE_PTS[0 if sx > 0 else 1]
        loc, n = k.surf(o, t)
        k.joint("Lid_" + side, loc - n * 0.04, "Head", tail=(sx * 0.1, 0, 0))
        k.joint("Ear_" + side, HEAD_C + Vector((sx * 0.40, 0.05, 0.42)), "Head", tail=(sx * 0.15, 0, 0.25))
        k.joint("Leg_F" + side, (sx * 0.27, -0.21, 0.50), "Spine", tail=(0, 0, -0.42))
        k.joint("Leg_B" + side, (sx * 0.33, 0.71, 0.50), "Spine", tail=(0, 0, -0.42))
    k.joint("Tail1", tuple(TAIL[0]), "Spine")
    k.joint("Tail2", tuple(TAIL[1]), "Tail1")
    k.joint("Tail3", tuple(TAIL[2]), "Tail2", tail=TAIL[4] - TAIL[2])
    k.body_bones = ["Spine", "Neck", "Head", "Tail1", "Tail2", "Tail3", "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]


# ------------------------------------------------------------------ animation
LEGS = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
LID_OPEN = -6       # resting: a regal, slightly lowered lid
LID_SHUT = 62


def lids(k, f, a):
    for s in ("L", "R"):
        k.key("Lid_" + s, f, rot=(a, 0, 0))


def tail(k, f, n, sway, curl=0.0, phase=0.0, cycles=1, flick=0.0):
    for i, b in enumerate(("Tail1", "Tail2", "Tail3")):
        lag = phase - 0.12 * i
        k.key(b, f, rot=(4 + curl * (0.4 + 0.5 * i) + (flick if i == 2 else 0) * pk.wave(f, n, lag, cycles * 2),
                         sway * (0.7 + 0.5 * i) * pk.wave(f, n, lag, cycles), 0))


def ears(k, f, n, twitch=0.0):
    k.key("Ear_L", f, rot=(0, 0, 0))
    k.key("Ear_R", f, rot=(twitch, 0, -twitch * 0.5))


def plant(k, n, step=1):
    import bpy
    k.bake_bezier_now()
    for f in range(0, n + 1, step):
        bpy.context.scene.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


def idle(k):
    """Royal idle (3 s): chin up, looks down his nose to one side, then the other, slow royal blink in the
    middle, ear twitch, tail sways in a lazy S with a flicking tip."""
    n = 90
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n)
        k.key("Spine", f, rot=(-1.5 - 1.0 * s, 0, 0.8 * pk.wave(f, n, 0.25)), loc=(0, 0, 0.012 * (1 + s) / 2))
        look = 20 * pk.wave(f, n, 0.0) * abs(pk.wave(f, n, 0.0)) ** 0.4
        k.key("Neck", f, rot=(-7 + 1.5 * pk.cwave(f, n), look * 0.4, 0))
        k.key("Head", f, rot=(-9 + 2.0 * pk.wave(f, n, 0.15, 2), look * 0.6, 6 * pk.wave(f, n, 0.05) * pk.cwave(f, n, 0.05)))
        tail(k, f, n, 9, curl=10, phase=0.1, flick=9)
    # slow royal blink at the front-most look (f 40..56) + a quick one at f 78
    for f, a in ((0, LID_OPEN), (38, LID_OPEN), (45, LID_SHUT), (49, LID_SHUT), (57, LID_OPEN), (75, LID_OPEN),
                 (78, LID_SHUT), (81, LID_OPEN), (90, LID_OPEN)):
        lids(k, f, a)
    for f, tw in ((0, 0), (62, 0), (65, -22), (68, 6), (71, -18), (76, 0), (90, 0)):
        ears(k, f, n, tw)
    plant(k, n)
    k.finish()
    k.meta["planted"] = LEGS


def walk(k):
    """Dainty proud strut: lateral-sequence cat walk, head held level, tail high with a curled, bobbing tip."""
    n = 24

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.2 * pk.wave(f, n, 0.1, 2), 2.5 * pk.wave(f, n, 0.1), 3.0 * pk.wave(f, n)),
              loc=(0, 0, 0.028 * b))
        k.key("Neck", f, rot=(-6 - 1.2 * pk.wave(f, n, 0.15, 2), -2.0 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(-7 + 1.5 * pk.wave(f, n, 0.2, 2), -1.5 * pk.wave(f, n, 0.1), -2.5 * pk.wave(f, n)))
        tail(k, f, n, 6, curl=20, phase=0.2, flick=7)
        lids(k, f, LID_OPEN)
        ears(k, f, n, 0)
    k.meta["legs"] = [("Leg_BL", 0.0), ("Leg_FL", 0.25), ("Leg_BR", 0.5), ("Leg_FR", 0.75)]
    k.meta["duty"] = 0.62
    stride = pk.walk_cycle(k, n, k.meta["legs"], 0.42 * math.sin(math.radians(19)), 0.10, body, duty=0.62)
    return stride


def roar(k):
    """'roar' slot = a royal yawn + stretch: front stretch with the rump up, chin to the sky, eyes squeezed shut,
    tail straight up and quivering, then a satisfied settle."""
    n = 54
    k.new_action("roar", n, False)
    P = [(0, 0, 0, -7, -9, LID_OPEN, 0.0),
         (12, 10, 0.0, -2, 6, LID_OPEN, 0.0),
         (22, 16, -0.07, -18, -26, LID_SHUT, 1.0),
         (36, 15, -0.07, -20, -28, LID_SHUT, 1.0),
         (44, 2, -0.01, -9, -12, 20, 0.3),
         (54, 0, 0, -7, -9, LID_OPEN, 0.0)]
    for f, sp, z, nk, hd, lid, tup in P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        lids(k, f, lid)
        for i, b in enumerate(("Tail1", "Tail2", "Tail3")):
            k.key(b, f, rot=(4 + 26 * tup * (0.5 + 0.4 * i), 0, 0))
        ears(k, f, n, -15 * tup)
    for f in range(24, 37, 3):     # tail-tip quiver at the top of the stretch
        k.key("Tail3", f, rot=(28, 7 * (1 if (f // 3) % 2 else -1), 0))
    plant(k, n)
    k.finish(loop=False)


def groom(k):
    """act: lifts the right front paw, licks it a few times (head bobs), wipes it over the face, sets it down."""
    import bpy
    n = 66
    k.new_action("act_groom", n, False)
    P = [(0, 0, -7, -9, 0), (10, 3, 2, 6, 0), (16, 4, 6, 12, 1), (46, 4, 6, 12, 1), (56, 2, -2, -2, 0), (66, 0, -7, -9, 0)]
    for f, sp, nk, hd, paw in P:
        k.key("Spine", f, rot=(sp, 0, -3 * paw), loc=(0, 0, 0))
        k.key("Neck", f, rot=(nk, 6 * paw, 0))
        k.key("Head", f, rot=(hd, 10 * paw, -10 * paw))
        lids(k, f, LID_OPEN if not paw else 30)
        tail(k, f, n, 4, curl=8, phase=0.3)
        ears(k, f, n, 0)
    for f in range(18, 46, 4):    # licks: little head bobs
        k.key("Head", f, rot=(12 + (8 if (f // 4) % 2 else -2), 10, -10))
    plant(k, n)
    # paw: lift the right front leg up in front of the chest while licking (drop its planted keys in 9..55)
    for fc in k.fcurves():
        if fc.data_path.startswith('pose.bones["Leg_FR"]'):
            for i in reversed(range(len(fc.keyframe_points))):
                if 9 <= fc.keyframe_points[i].co.x <= 55:
                    fc.keyframe_points.remove(fc.keyframe_points[i])
            fc.update()
    for f, a, z in ((14, -74, 0.17), (30, -76, 0.18), (44, -78, 0.18), (52, -14, 0.03)):
        k.key("Leg_FR", f, rot=(a, 6, 10), loc=(0, 0, z))
    k.finish(loop=False)


def wiggle(k):
    """act: hunting butt-wiggle then a cheeky pounce in place (all four paws leave the ground) and a proud land."""
    import bpy
    n = 52
    k.new_action("act_wiggle", n, False)
    # crouch + wiggle 0-22, leap 26-34 (airborne), land 36, recover to 52
    keys = [(0, 0, 0.0, -7, -9, 0), (8, 6, -0.10, -8, -8, 0), (22, 6, -0.10, -8, -8, 0), (27, -14, 0.30, -12, -10, 1),
            (32, 6, 0.26, 0, -2, 1), (37, 10, -0.06, 4, 2, 0), (44, -2, 0.01, -8, -10, 0), (52, 0, 0.0, -7, -9, 0)]
    for f, sp, z, nk, hd, air in keys:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        lids(k, f, 10 if 6 <= f <= 22 else LID_OPEN)
        ears(k, f, n, -12 if 6 <= f <= 22 else 0)
    for f in range(8, 23, 2):   # the butt wiggle
        w = 1 if (f // 2) % 2 else -1
        k.key("Spine", f, rot=(6, 4 * w, 6 * w), loc=(0, 0, -0.10))
        k.key("Tail1", f, rot=(-4, 10 * w, 0))
        k.key("Tail2", f, rot=(-4, 14 * w, 0))
        k.key("Tail3", f, rot=(-2, 18 * w, 0))
    for f in (0, 6, 24, 30, 38, 52):
        tail(k, f, n, 0, curl=-12 if f in (24, 30) else 6)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        if 25 <= f <= 34:
            continue
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f, fa, ba in ((28, -40, 35), (31, -45, 40)):     # legs stretched out in the air: front reach, back push
        for leg in LEGS:
            k.key(leg, f, rot=(fa if "F" in leg[4] else ba, 0, 0), loc=(0, 0, 0))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    groom(k)
    wiggle(k)
    return stride
