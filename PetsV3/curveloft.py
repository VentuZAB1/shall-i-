# curveloft.py (2026-10-14, Cosmic Leviathan): smooth lofted hulls along a CURVED centreline in the y-z plane (a
# serpent / S-body), built on blockkit's Tube primitive. Same ideas as AbyssalOrca.hull_tube / band, but the rings
# stand perpendicular to the curve instead of on y = const planes.
#   L = Loft(stations, n=2.4, seg=24)   stations: [(y, z, half_width, half_height), ...] head -> tail
#   L.tube(B, s0, s1, color, bone, j0=, j1=, grow=, zlo=, zhi=)      closed solid between arc lengths s0..s1
#   L.band(B, s0, s1, color, bone, zlo=, zhi=, grow=, inset=, narrow1=)  flush pattern shell (top / bottom band)
#   L.at(s) -> (centre, T, N, hw, hh)   T = tangent (head -> tail), N = the section's "up", X = +x (the side)
#   L.surf(s, a, f=1.0) -> point on the section at angle a (0 = +x side, pi/2 = top), scaled by f
#   L.s_at_y(y) -> arc length where the centreline crosses y (first crossing)
import math
from mathutils import Vector

X = Vector((1, 0, 0))


def _cr(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def se(a, n):
    """superellipse unit coords for angle a"""
    c, s = math.cos(a), math.sin(a)
    return math.copysign(abs(c) ** (2.0 / n), c), math.copysign(abs(s) ** (2.0 / n), s)


class Loft:
    def __init__(self, stations, n=2.4, seg=24, res=0.02):
        self.n, self.seg = n, seg
        P = [Vector((0.0, st[0], st[1])) for st in stations]
        W = [(st[2], st[3]) for st in stations]
        ext = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
        self.pts, self.wh = [], []
        for i in range(len(P) - 1):
            L = (P[i + 1] - P[i]).length
            m = max(2, int(L / res))
            for j in range(m):
                t = j / m
                self.pts.append(_cr(ext[i], ext[i + 1], ext[i + 2], ext[i + 3], t))
                u = t * t * (3 - 2 * t)                                      # smooth width between stations
                self.wh.append((W[i][0] + (W[i + 1][0] - W[i][0]) * u, W[i][1] + (W[i + 1][1] - W[i][1]) * u))
        self.pts.append(P[-1])
        self.wh.append(W[-1])
        self.s = [0.0]
        for a, b in zip(self.pts, self.pts[1:]):
            self.s.append(self.s[-1] + (b - a).length)
        self.length = self.s[-1]
        self.station_s = []
        for p in P:
            self.station_s.append(min(range(len(self.pts)), key=lambda i: (self.pts[i] - p).length))
        self.station_s = [self.s[i] for i in self.station_s]

    def _idx(self, s):
        s = max(0.0, min(self.length, s))
        lo, hi = 0, len(self.s) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.s[mid] <= s:
                lo = mid
            else:
                hi = mid
        t = 0.0 if self.s[hi] == self.s[lo] else (s - self.s[lo]) / (self.s[hi] - self.s[lo])
        return lo, hi, t

    def at(self, s):
        lo, hi, t = self._idx(s)
        c = self.pts[lo].lerp(self.pts[hi], t)
        a = self.pts[max(0, lo - 1)]
        b = self.pts[min(len(self.pts) - 1, hi + 1)]
        T = (b - a).normalized()
        N = X.cross(T).normalized()                                          # T along -y (forward) .. +y: N = up
        if N.z < 0:
            N = -N
        w = self.wh[lo][0] + (self.wh[hi][0] - self.wh[lo][0]) * t
        h = self.wh[lo][1] + (self.wh[hi][1] - self.wh[lo][1]) * t
        return c, T, N, w, h

    def surf(self, s, a, f=1.0, grow=0.0):
        c, T, N, w, h = self.at(s)
        cx, sz = se(a, self.n)
        return c + X * ((w + grow) * f * cx) + N * ((h + grow) * f * sz)

    def s_at_y(self, y):
        for i in range(len(self.pts) - 1):
            a, b = self.pts[i].y, self.pts[i + 1].y
            if (a - y) * (b - y) <= 0 and a != b:
                return self.s[i] + (self.s[i + 1] - self.s[i]) * (y - a) / (b - a)
        return 0.0 if abs(self.pts[0].y - y) < abs(self.pts[-1].y - y) else self.length

    def _ss(self, s0, s1, extra=(), step=0.05):
        m = max(2, int(math.ceil((s1 - s0) / step)))
        out = set([s0 + (s1 - s0) * i / m for i in range(m + 1)])
        out |= set(v for v in list(self.station_s) + list(extra) if s0 < v < s1)
        return sorted(out)

    def ring(self, s, grow=0.0, a0=0.0, a1=2 * math.pi, sc=1.0, seg=None):
        seg = seg or self.seg
        c, T, N, w, h = self.at(s)
        closed = abs((a1 - a0) - 2 * math.pi) < 1e-6
        cnt = seg if closed else seg + 1
        out = []
        for i in range(cnt):
            cx, sz = se(a0 + (a1 - a0) * i / seg, self.n)
            out.append(c + X * ((w * sc + grow) * cx) + N * ((h * sc + grow) * sz))
        return out

    def zang(self, f):
        return math.asin(max(-1.0, min(1.0, math.copysign(abs(f) ** (self.n / 2.0), f))))

    def tube(self, B, s0, s1, color, bone, j0=None, j1=None, grow=0.0, zlo=-1.0, zhi=1.0, ov=0.06, nostud=False,
             step=0.05):
        """closed solid between arc lengths s0..s1. j0 / j1 = joint arc length at the front / back end: the tube runs
        past it (under the neighbour) shrinking to 0.985 (flush joints, no crease). zlo / zhi: keep only the part
        above / below that section-height fraction (flat chord)."""
        rings = []
        for s in self._ss(s0, s1, [v for v in (j0, j1) if v is not None], step):
            sc = 1.0
            if j0 is not None and s < j0:
                sc -= 0.015 * min(1.0, (j0 - s) / ov)
            if j1 is not None and s > j1:
                sc -= 0.015 * min(1.0, (s - j1) / ov)
            if zlo > -1:
                a = self.zang(zlo)
                rings.append(self.ring(s, grow, a, math.pi - a, sc, self.seg // 2))
            elif zhi < 1:
                a = self.zang(zhi)
                rings.append(self.ring(s, grow, math.pi - a, 2 * math.pi + a, sc, self.seg // 2))
            else:
                rings.append(self.ring(s, grow, sc=sc))
        return B.tube(rings, color, bone, nostud=nostud)

    def band(self, B, s0, s1, color, bone, zlo=-1.0, zhi=1.0, grow=0.008, inset=0.02, narrow1=None, zhi1=None,
             step=0.04, arc=None, aseg=None):
        """flush pattern shell: bottom band (zlo = -1, up to zhi) or top band (from zlo over the back). narrow1 shrinks
        a top band toward the spine along the piece (chevron point), zhi1 ramps a bottom band's edge. arc = (a0, a1)
        explicit section angles (rad, 0 = +x side, pi/2 = top) e.g. one half of a split saddle; aseg = its segments."""
        rings = []
        for s in self._ss(s0, s1, (), step):
            t = (s - s0) / (s1 - s0) if s1 > s0 else 0.0
            if zlo <= -1:
                a = self.zang(zhi if zhi1 is None else zhi + (zhi1 - zhi) * t)
                a0, a1 = a, -math.pi - a
            else:
                a = self.zang(zlo)
                a0, a1 = math.pi - a, a
                if narrow1 is not None:
                    k_ = 1.0 + (narrow1 - 1.0) * t
                    a0, a1 = math.pi / 2 + (a0 - math.pi / 2) * k_, math.pi / 2 + (a1 - math.pi / 2) * k_
            if arc is not None:
                a0, a1 = arc
            o = self.ring(s, grow, a0, a1, seg=aseg or self.seg // 2)
            i = self.ring(s, -inset, a0, a1, seg=aseg or self.seg // 2)
            rings.append((o, i))
        return B.tube(rings, color, bone, closed=False)
