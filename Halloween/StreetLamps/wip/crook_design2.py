# crook = rising quarter-ellipse (a1,b1) + descending quarter-ellipse (a2,b2) + inward spiral curl; built from the
# radius-of-curvature vs turned-angle function (blended at the joints) and integrated -> G2 centreline
import numpy as np, sys
def Rell(a, b, th):
    return a*a*b*b / (a*a*np.sin(th)**2 + b*b*np.cos(th)**2) ** 1.5
def crook(a1, b1, a2, b2, r0, r1, W, apex_z=17.58, n=6000, blend=(16.0, 14.0)):
    phi = np.linspace(0.0, 180.0 + W, n)
    th = np.radians(90.0 - phi)
    R1 = Rell(a1, b1, th); R2 = Rell(a2, b2, th)
    Rc = r0 + (r1 - r0) * np.clip((phi - 180.0) / W, 0, 1)
    def mixw(c, w):
        return np.clip((phi - (c - w)) / (2 * w), 0, 1)
    t1 = mixw(90.0, blend[0]); t1 = t1 * t1 * (3 - 2 * t1)
    t2 = mixw(180.0, blend[1]); t2 = t2 * t2 * (3 - 2 * t2)
    # blend in curvature (1/R)
    k = (1 - t1) / R1 + t1 / R2
    k = (1 - t2) * k + t2 / Rc
    R = 1 / k
    dphi = np.radians(phi[1] - phi[0])
    ds = R * dphi
    th_mid = th
    y = np.concatenate([[0], np.cumsum(np.cos(th_mid[:-1]) * ds[:-1])])
    z = np.concatenate([[0], np.cumsum(np.sin(th_mid[:-1]) * ds[:-1])])
    ia = np.argmin(abs(phi - 90)); ic = np.argmin(abs(phi - 270))
    zs = apex_z - z[ia]
    z = z + zs
    curl = phi >= 180
    return dict(phi=phi, y=y, z=z, R=R, s=np.concatenate([[0], np.cumsum(ds[:-1])]), zs=zs,
                apex=(y[ia], z[ia]), cradle=(y[ic], z[ic]), end=(y[-1], z[-1]), ymax=y.max(),
                curl_w=y[curl].max() - y[curl].min(), curl_h=z[curl].max() - z[curl].min(), Rmax=R.max(), Rmin=R.min(),
                length=ds.sum())
def solve(a1, b1, b2, r0, r1, W, target_y=3.55):
    lo, hi = 0.8, 4.0
    for _ in range(50):
        a2 = (lo + hi) / 2
        c = crook(a1, b1, a2, b2, r0, r1, W)
        if c["cradle"][0] > target_y: hi = a2
        else: lo = a2
    return a2, c
if __name__ == "__main__":
    for args in eval(sys.argv[1]):
        a2, c = solve(*args)
        print(args, "a2=%.3f" % a2, "zs=%.3f" % c["zs"], "apex=(%.3f,%.3f)" % c["apex"], "cradle=(%.3f,%.3f)" % c["cradle"],
              "end=(%.3f,%.3f)" % c["end"], "ymax=%.3f" % c["ymax"], "curl %.3fx%.3f" % (c["curl_w"], c["curl_h"]),
              "Rmax=%.2f Rmin=%.2f L=%.2f" % (c["Rmax"], c["Rmin"], c["length"]))
