// SLINGSHOT Halloween VFX - shared OSL helpers (included by every shader in this folder).
// Conventions: one plane covers the whole flipbook atlas (2 x 2 units per tile, cols x cols tiles, row-major from the
// top-left = Roblox FlipbookLayout GridNxN). tile() returns the local tile coords x, y in [-1, 1] (+y up) and the
// animation time T = frame / frames in [0, 1). Colours are written as sRGB 0-1 values (vfx.py stores them as-is);
// mode 0 renders the straight colour, mode 1 renders the alpha as grey.

float sq(float a) { return a * a; }

// distance between two phases on a loop of length 1
float wrapd(float a, float b)
{
    float d = abs(a - b);
    d = d - floor(d);
    return min(d, 1.0 - d);
}

// signed wrapped difference a - b in [-0.5, 0.5)
float wraps(float a, float b)
{
    float d = a - b;
    return d - floor(d + 0.5);
}

void tile(point Q, int cols, output float x, output float y, output float T, output float frame)
{
    float hc = cols;
    float ci = clamp(floor((Q[0] + hc) * 0.5), 0.0, hc - 1.0);
    float ri = clamp(floor((hc - Q[1]) * 0.5), 0.0, hc - 1.0);
    frame = ri * hc + ci;
    T = frame / (hc * hc);
    x = Q[0] + hc - 2.0 * ci - 1.0;
    y = Q[1] - hc + 2.0 * ri + 1.0;
}

// signed fractal noise, roughly in [-0.7, 0.7]
float fbm(point p, int octaves, float gain)
{
    float s = 0.0;
    float a = 0.5;
    point q = p;
    for (int i = 0; i < octaves; i++) {
        s += a * noise("perlin", q);
        q = q * 2.03 + point(1.7, 9.2, 4.1);
        a *= gain;
    }
    return s;
}

// billowy noise in [0, 1] (rounded puffs, used for smoke and mist)
float billow(point p, int octaves, float gain)
{
    float s = 0.0;
    float a = 0.5;
    float norm = 0.0;
    point q = p;
    for (int i = 0; i < octaves; i++) {
        s += a * (1.0 - abs(noise("perlin", q)));
        norm += a;
        q = q * 2.07 + point(5.3, 1.1, 7.7);
        a *= gain;
    }
    return s / norm;
}

// piecewise-linear ramp through 7 stops
color ramp7(float h, float K[7], color C[7])
{
    float v = clamp(h, 0.0, 1.0);
    color c = C[6];
    for (int i = 0; i < 6; i++) {
        if (v <= K[i + 1]) {
            c = mix(C[i], C[i + 1], (v - K[i]) / max(K[i + 1] - K[i], 1e-5));
            break;
        }
    }
    return c;
}

// rounded "uneven capsule": circle r1 at (0,0), circle r2 at (0,h), tangent sides (exact SDF, I. Quilez)
float sd_uneven_capsule(float px, float py, float r1, float r2, float h)
{
    float x = abs(px);
    float b = (r1 - r2) / h;
    float a = sqrt(1.0 - b * b);
    float k = -b * x + a * py;
    if (k < 0.0) return hypot(x, py) - r1;
    if (k > a * h) return hypot(x, py - h) - r2;
    return a * x + b * py - r1;
}

// round cone between circles (a, r1) and (b, r2) in the xy plane (exact SDF, I. Quilez)
float sd_round_cone(float px, float py, float ax, float ay, float bx, float by, float r1, float r2)
{
    float bax = bx - ax, bay = by - ay;
    float l2 = bax * bax + bay * bay;
    float rr = r1 - r2;
    float a2 = l2 - rr * rr;
    float il2 = 1.0 / l2;
    float pax = px - ax, pay = py - ay;
    float yy = pax * bax + pay * bay;
    float z = yy - l2;
    float qx = pax * l2 - bax * yy, qy = pay * l2 - bay * yy;
    float x2 = qx * qx + qy * qy;
    float y2 = yy * yy * l2;
    float z2 = z * z * l2;
    float k = sign(rr) * rr * rr * x2;
    if (sign(z) * a2 * z2 > k) return sqrt(x2 + z2) * il2 - r2;
    if (sign(yy) * a2 * y2 < k) return sqrt(x2 + y2) * il2 - r1;
    return (sqrt(x2 * a2 * il2) + yy * rr) * il2 - r1;
}

// polynomial smooth minimum
float smin(float a, float b, float k)
{
    float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
    return mix(b, a, h) - k * h * (1.0 - h);
}

// fade to zero near the tile border (safety margin for mip-maps / flipbook bleeding): starts at 1 - m, exactly 0 in
// the outer 4 % of the tile (2.5 px at 128 px frames)
float border(float x, float y, float m)
{
    return (1.0 - smoothstep(1.0 - m, 0.955, abs(x))) * (1.0 - smoothstep(1.0 - m, 0.955, abs(y)));
}
