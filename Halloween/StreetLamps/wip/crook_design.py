# quick numeric design of the shepherd's-crook centreline: radius as a function of the turned angle phi
import numpy as np, sys
def crook(knots, z_cradle=16.085, n=4000):
    ph = np.array([k[0] for k in knots], float); R = np.array([k[1] for k in knots], float)
    phi = np.linspace(0, ph[-1], n)
    r = np.interp(phi, ph, R)
    th = np.radians(90 - phi)
    dphi = np.radians(phi[1] - phi[0])
    ds = r * dphi
    y = np.concatenate([[0], np.cumsum(np.cos(th[:-1]) * ds[:-1])])
    z = np.concatenate([[0], np.cumsum(np.sin(th[:-1]) * ds[:-1])])
    ia = np.argmin(abs(phi - 90)); ic = np.argmin(abs(phi - 270)); idn = np.argmin(abs(phi - 180))
    zs = z_cradle - z[ic]
    z = z + zs
    curl = phi >= 180
    return dict(y=y, z=z, phi=phi, r=r, apex=(y[ia], z[ia]), cradle=(y[ic], z[ic]), down=(y[idn], z[idn]),
                zs=zs, ymax=y.max(), curl_w=y[curl].max() - y[curl].min(), curl_h=z[curl].max() - z[curl].min(),
                end=(y[-1], z[-1]), length=ds.sum(), zmax=z.max(), rmax=r.max())
if __name__ == "__main__":
    K = eval(sys.argv[1])
    c = crook(K)
    for k in ("apex", "cradle", "down", "end", "zs", "ymax", "curl_w", "curl_h", "length", "zmax", "rmax"):
        v = c[k]
        print(k, np.round(v, 3) if not isinstance(v, tuple) else tuple(round(float(x), 3) for x in v))
