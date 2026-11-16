# -*- coding: utf-8 -*-
"""Kleiner Software-Renderer.

Genug fuer Produktbilder: Perspektive, Z-Puffer, weiche Normalen,
Lambert + Blinn-Phong, Schlagschatten auf den Boden, Spiegelung,
Supersampling, Vignette und etwas Korn. Alles in numpy - keine
Grafikkarte, keine externe Bibliothek ausser scipy fuer den Weichzeichner.
"""
import numpy as np
from scipy.ndimage import gaussian_filter

F32 = np.float32


def norm(v):
    v = np.asarray(v, F32)
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / np.maximum(n, 1e-9)


# --------------------------------------------------------------- Material
def mat(albedo=(0.8, 0.8, 0.8), spec=0.25, shin=38.0, metal=0.0,
        emis=(0.0, 0.0, 0.0), tex=None):
    """tex: f(P) -> (H,W,3) Faktor auf die Grundfarbe, P sind Weltkoordinaten."""
    return dict(albedo=np.array(albedo, F32), spec=F32(spec),
                shin=F32(shin), metal=F32(metal),
                emis=np.array(emis, F32), tex=tex)


def hexcol(s, gamma=2.2):
    s = s.lstrip("#")
    rgb = np.array([int(s[i:i + 2], 16) / 255.0 for i in (0, 2, 4)], F32)
    return rgb ** gamma                      # sRGB -> linear


# ------------------------------------------------------------------ Mesh
class Mesh:
    def __init__(self, verts, faces, material, smooth=True, no_shadow=False):
        self.v = np.asarray(verts, F32)
        self.f = np.asarray(faces, np.int32)
        self.m = material
        self.smooth = smooth
        self.no_shadow = no_shadow

    def transform(self, M):
        v = np.concatenate([self.v, np.ones((len(self.v), 1), F32)], 1)
        self.v = (v @ np.asarray(M, F32).T)[:, :3]
        return self

    def vertex_normals(self):
        a, b, c = self.v[self.f[:, 0]], self.v[self.f[:, 1]], self.v[self.f[:, 2]]
        fn = np.cross(b - a, c - a)
        if not self.smooth:
            return None, norm(fn)
        vn = np.zeros_like(self.v)
        for k in range(3):
            np.add.at(vn, self.f[:, k], fn)
        return norm(vn), norm(fn)


def mat4(t=(0, 0, 0), s=(1, 1, 1), rx=0.0, ry=0.0, rz=0.0):
    sx, sy, sz = s
    M = np.diag([sx, sy, sz, 1.0]).astype(F32)
    for ang, ax in ((rx, 0), (ry, 1), (rz, 2)):
        if ang:
            c, s_ = np.cos(ang), np.sin(ang)
            R = np.eye(4, dtype=F32)
            if ax == 0:
                R[1, 1], R[1, 2], R[2, 1], R[2, 2] = c, -s_, s_, c
            elif ax == 1:
                R[0, 0], R[0, 2], R[2, 0], R[2, 2] = c, s_, -s_, c
            else:
                R[0, 0], R[0, 1], R[1, 0], R[1, 1] = c, -s_, s_, c
            M = R @ M
    M[0, 3], M[1, 3], M[2, 3] = t
    return M


# ------------------------------------------------------------- Primitive
def box(sx, sy, sz, center=(0, 0, 0), smooth=False, material=None):
    x, y, z = sx / 2, sy / 2, sz / 2
    cx, cy, cz = center
    v = np.array([[-x, -y, -z], [x, -y, -z], [x, y, -z], [-x, y, -z],
                  [-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]], F32)
    v += np.array([cx, cy, cz], F32)
    f = np.array([[0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7],
                  [0, 1, 5], [0, 5, 4], [3, 7, 6], [3, 6, 2],
                  [0, 4, 7], [0, 7, 3], [1, 2, 6], [1, 6, 5]], np.int32)
    return Mesh(v, f, material or mat(), smooth=smooth)


def rbox(sx, sy, sz, r=0.0, center=(0, 0, 0), seg=4, material=None):
    """Quader mit gerundeten Kanten - als Lathe-Ersatz ueber Subdivision."""
    if r <= 0:
        return box(sx, sy, sz, center, False, material)
    # Punktwolke eines abgerundeten Quaders ueber Superellipsoid-Naeherung
    n = max(6, seg * 4)
    u = np.linspace(0, np.pi, n)
    t = np.linspace(0, 2 * np.pi, 2 * n, endpoint=False)
    U, T = np.meshgrid(u, t, indexing="ij")
    p = 1.0 / max(0.08, r / max(sx, sy, sz))
    p = np.clip(p, 2.0, 14.0)

    def sgnpow(a, e):
        return np.sign(a) * np.abs(a) ** e
    X = sgnpow(np.sin(U), 2 / p) * sgnpow(np.cos(T), 2 / p) * (sx / 2)
    Y = sgnpow(np.cos(U), 2 / p) * (sy / 2)
    Z = sgnpow(np.sin(U), 2 / p) * sgnpow(np.sin(T), 2 / p) * (sz / 2)
    V = np.stack([X, Y, Z], -1).reshape(-1, 3) + np.array(center, F32)
    faces = []
    H, W = U.shape
    for i in range(H - 1):
        for j in range(W):
            a = i * W + j
            b = i * W + (j + 1) % W
            c = (i + 1) * W + (j + 1) % W
            d = (i + 1) * W + j
            faces += [[a, b, c], [a, c, d]]
    return Mesh(V, np.array(faces, np.int32), material or mat(), smooth=True)


def lathe(profile, seg=48, axis="z", center=(0, 0, 0), material=None,
          smooth=True):
    """Dreht ein Profil [(r, h), ...] um eine Achse."""
    pr = np.asarray(profile, F32)
    a = np.linspace(0, 2 * np.pi, seg, endpoint=False)
    ca, sa = np.cos(a), np.sin(a)
    R = pr[:, 0][:, None] * ca[None, :]
    S = pr[:, 0][:, None] * sa[None, :]
    Hh = np.repeat(pr[:, 1][:, None], seg, 1)
    if axis == "z":
        V = np.stack([R, S, Hh], -1)
    elif axis == "x":
        V = np.stack([Hh, R, S], -1)
    else:
        V = np.stack([R, Hh, S], -1)
    V = V.reshape(-1, 3) + np.array(center, F32)
    faces = []
    n = len(pr)
    for i in range(n - 1):
        for j in range(seg):
            a0 = i * seg + j
            b0 = i * seg + (j + 1) % seg
            c0 = (i + 1) * seg + (j + 1) % seg
            d0 = (i + 1) * seg + j
            faces += [[a0, b0, c0], [a0, c0, d0]]
    return Mesh(V, np.array(faces, np.int32), material or mat(), smooth=smooth)


def extrude(poly, depth, center=(0, 0, 0), material=None, smooth=False,
            plane="xy"):
    """Zieht ein 2D-Polygon in die Tiefe. Polygon gegen den Uhrzeigersinn."""
    p = np.asarray(poly, F32)
    n = len(p)
    d = depth / 2.0
    if plane == "xy":
        front = np.stack([p[:, 0], p[:, 1], np.full(n, d)], -1)
        back = np.stack([p[:, 0], p[:, 1], np.full(n, -d)], -1)
    else:
        front = np.stack([p[:, 0], np.full(n, d), p[:, 1]], -1)
        back = np.stack([p[:, 0], np.full(n, -d), p[:, 1]], -1)
    V = np.concatenate([front, back]) + np.array(center, F32)
    faces = []
    for i in range(1, n - 1):                        # Deckel
        faces += [[0, i, i + 1], [n, n + i + 1, n + i]]
    for i in range(n):                               # Mantel
        j = (i + 1) % n
        faces += [[i, n + i, n + j], [i, n + j, j]]
    return Mesh(V, np.array(faces, np.int32), material or mat(), smooth=smooth)


def tube(p0, p1, r, seg=16, material=None, caps=True):
    p0 = np.asarray(p0, F32); p1 = np.asarray(p1, F32)
    d = p1 - p0
    L = float(np.linalg.norm(d))
    if L < 1e-6:
        return None
    zc = d / L
    tmp = np.array([0, 1, 0], F32)
    if abs(float(zc @ tmp)) > 0.95:
        tmp = np.array([1, 0, 0], F32)
    xc = norm(np.cross(tmp, zc)); yc = np.cross(zc, xc)
    a = np.linspace(0, 2 * np.pi, seg, endpoint=False)
    ring = (np.cos(a)[:, None] * xc + np.sin(a)[:, None] * yc) * r
    V = np.concatenate([p0 + ring, p1 + ring])
    faces = []
    for i in range(seg):
        j = (i + 1) % seg
        faces += [[i, seg + i, seg + j], [i, seg + j, j]]
    if caps:
        V = np.concatenate([V, p0[None], p1[None]])
        c0, c1 = 2 * seg, 2 * seg + 1
        for i in range(seg):
            j = (i + 1) % seg
            faces += [[c0, j, i], [c1, seg + i, seg + j]]
    return Mesh(V, np.array(faces, np.int32), material or mat(), smooth=True)


def plane(size, y=0.0, material=None, n=40):
    """Boden als Raster kleiner Kacheln - grosse Dreiecke, die teilweise
    hinter der Kamera liegen, wuerden sonst komplett wegfallen."""
    s = size / 2.0
    g = np.linspace(-s, s, n + 1, dtype=F32)
    X, Z = np.meshgrid(g, g, indexing="ij")
    V = np.stack([X, np.full_like(X, y), Z], -1).reshape(-1, 3)
    faces = []
    for i in range(n):
        for j in range(n):
            a = i * (n + 1) + j
            b = a + 1
            c = (i + 1) * (n + 1) + j + 1
            d = (i + 1) * (n + 1) + j
            faces += [[a, b, c], [a, c, d]]
    return Mesh(V, np.array(faces, np.int32), material or mat(),
                smooth=False, no_shadow=True)


# ------------------------------------------------------------- Renderer
class Scene:
    def __init__(self):
        self.meshes = []

    def add(self, *ms):
        for m in ms:
            if m is not None:
                self.meshes.append(m)
        return self


class Camera:
    def __init__(self, eye, target, up=(0, 1, 0), fov=34.0):
        self.eye = np.array(eye, F32)
        self.target = np.array(target, F32)
        self.up = np.array(up, F32)
        self.fov = float(fov)

    def basis(self):
        fwd = norm(self.target - self.eye)
        right = norm(np.cross(fwd, self.up))
        up = np.cross(right, fwd)
        return right, up, fwd


def _project(V, cam, W, H):
    right, up, fwd = cam.basis()
    d = V - cam.eye
    x = d @ right; y = d @ up; z = d @ fwd
    fy = (H / 2.0) / np.tan(np.radians(cam.fov) / 2.0)
    z_safe = np.where(z > 1e-4, z, 1e-4)
    sx = W / 2.0 + fy * x / z_safe
    sy = H / 2.0 - fy * y / z_safe
    return sx.astype(F32), sy.astype(F32), z.astype(F32)


def _raster(meshes, cam, W, H, want_attrs=True):
    """G-Buffer: Tiefe, Normale, Albedo, Spiegelglanz, Weltposition, Objekt-Id."""
    z_buf = np.full((H, W), np.inf, F32)
    nrm = np.zeros((H, W, 3), F32)
    alb = np.zeros((H, W, 3), F32)
    spc = np.zeros((H, W), F32)
    shn = np.ones((H, W), F32)
    met = np.zeros((H, W), F32)
    emi = np.zeros((H, W, 3), F32)
    pos = np.zeros((H, W, 3), F32)
    oid = np.zeros((H, W), np.int32)

    for mi, me in enumerate(meshes, start=1):
        vn, fn = me.vertex_normals()
        sx, sy, z = _project(me.v, cam, W, H)
        f = me.f
        ax, ay, az = sx[f[:, 0]], sy[f[:, 0]], z[f[:, 0]]
        bx, by, bz = sx[f[:, 1]], sy[f[:, 1]], z[f[:, 1]]
        cx, cy, cz = sx[f[:, 2]], sy[f[:, 2]], z[f[:, 2]]
        area = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
        ok = (np.abs(area) > 1e-7) & (az > 1e-3) & (bz > 1e-3) & (cz > 1e-3)
        idx = np.nonzero(ok)[0]
        if len(idx) == 0:
            continue
        A = me.m
        for t in idx:
            x0 = max(int(np.floor(min(ax[t], bx[t], cx[t]))), 0)
            x1 = min(int(np.ceil(max(ax[t], bx[t], cx[t]))) + 1, W)
            y0 = max(int(np.floor(min(ay[t], by[t], cy[t]))), 0)
            y1 = min(int(np.ceil(max(ay[t], by[t], cy[t]))) + 1, H)
            if x1 <= x0 or y1 <= y0:
                continue
            xs = np.arange(x0, x1, dtype=F32) + 0.5
            ys = np.arange(y0, y1, dtype=F32) + 0.5
            PX, PY = np.meshgrid(xs, ys)
            ar = area[t]
            w0 = ((cx[t] - bx[t]) * (PY - by[t]) - (cy[t] - by[t]) * (PX - bx[t])) / ar
            w1 = ((ax[t] - cx[t]) * (PY - cy[t]) - (ay[t] - cy[t]) * (PX - cx[t])) / ar
            w2 = 1.0 - w0 - w1
            m = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
            if not m.any():
                continue
            iz = w0 / az[t] + w1 / bz[t] + w2 / cz[t]
            zz = 1.0 / np.maximum(iz, 1e-9)
            sub = z_buf[y0:y1, x0:x1]
            upd = m & (zz < sub)
            if not upd.any():
                continue
            sub[upd] = zz[upd]
            if not want_attrs:
                continue
            p0 = (w0 / az[t]) * zz; p1 = (w1 / bz[t]) * zz; p2 = (w2 / cz[t]) * zz
            tri = me.f[t]
            if vn is not None:
                N = (p0[..., None] * vn[tri[0]] + p1[..., None] * vn[tri[1]]
                     + p2[..., None] * vn[tri[2]])
            else:
                N = np.broadcast_to(fn[t], p0.shape + (3,))
            P = (p0[..., None] * me.v[tri[0]] + p1[..., None] * me.v[tri[1]]
                 + p2[..., None] * me.v[tri[2]])
            nrm[y0:y1, x0:x1][upd] = N[upd]
            pos[y0:y1, x0:x1][upd] = P[upd]
            alb[y0:y1, x0:x1][upd] = A["albedo"]
            spc[y0:y1, x0:x1][upd] = A["spec"]
            shn[y0:y1, x0:x1][upd] = A["shin"]
            met[y0:y1, x0:x1][upd] = A["metal"]
            emi[y0:y1, x0:x1][upd] = A["emis"]
            oid[y0:y1, x0:x1][upd] = mi
    return dict(z=z_buf, n=nrm, alb=alb, spec=spc, shin=shn, metal=met,
                emis=emi, pos=pos, oid=oid)


def _shadow_mask(meshes, cam, W, H, L, blur=7.0):
    """Schlagschatten: Geometrie entlang des Lichts auf y=0 projizieren."""
    if L[1] <= 0.05:
        return np.zeros((H, W), F32)
    flat = []
    for me in meshes:
        if me.no_shadow:
            continue
        v = me.v.copy()
        t = v[:, 1] / L[1]
        v = v - L[None, :] * t[:, None]
        v[:, 1] = 0.004
        flat.append(Mesh(v, me.f, mat(), smooth=False, no_shadow=True))
    if not flat:
        return np.zeros((H, W), F32)
    g = _raster(flat, cam, W, H, want_attrs=False)
    m = (np.isfinite(g["z"])).astype(F32)
    # harter Kernschatten plus weiter Halbschatten - so entsteht der
    # dunkle Kontaktpunkt unter dem Objekt
    core = gaussian_filter(m, max(0.6, blur * 0.22))
    soft = gaussian_filter(m, max(1.5, blur))
    return np.clip(core * 0.78 + soft * 0.46, 0, 1)


DEF_LIGHT = norm(np.array([-0.52, 0.72, 0.46], F32))


def render(scene, cam, W, H, ss=2,
           light=None, light_col=(1.28, 1.24, 1.18), light2_col=(0.24, 0.27, 0.33),
           sky=(0.42, 0.47, 0.55), ground_amb=(0.11, 0.115, 0.125),
           bg=None, shadow=0.74, shadow_blur=4.5, reflect=0.0,
           vignette=0.30, grain=0.012, exposure=1.0, gamma=2.2, fog=None,
           _linear=False, _mask=False):
    """Rendert die Szene und liefert ein uint8-RGB-Bild (H, W, 3)."""
    L = DEF_LIGHT if light is None else norm(np.array(light, F32))
    L2 = norm(np.array([0.62, 0.34, -0.58], F32))
    w, h = W * ss, H * ss
    g = _raster(scene.meshes, cam, w, h)
    hit = np.isfinite(g["z"])

    for mi, me in enumerate(scene.meshes, start=1):
        t = me.m.get("tex")
        if t is None:
            continue
        sel = (g["oid"] == mi)
        if sel.any():
            g["alb"][sel] = g["alb"][sel] * t(g["pos"][sel])

    N = g["n"]
    nn = np.linalg.norm(N, axis=-1, keepdims=True)
    N = np.divide(N, np.maximum(nn, 1e-9))
    V = norm(cam.eye[None, None, :] - g["pos"])
    # Normalen zur Kamera drehen (Rueckseiten koennen falsch orientiert sein)
    flip = (np.sum(N * V, -1) < 0)[..., None]
    N = np.where(flip, -N, N)

    sky = np.array(sky, F32); gnd = np.array(ground_amb, F32)
    amb = gnd[None, None, :] + (sky - gnd)[None, None, :] * \
        (0.5 + 0.5 * N[..., 1:2])

    lc = np.array(light_col, F32); lc2 = np.array(light2_col, F32)
    ndl = np.clip(np.sum(N * L[None, None, :], -1), 0, 1)[..., None]
    ndl2 = np.clip(np.sum(N * L2[None, None, :], -1), 0, 1)[..., None]

    sh = np.ones((h, w), F32)
    if shadow > 0:
        sm = _shadow_mask(scene.meshes, cam, w, h, L, blur=shadow_blur * ss)
        sh = 1.0 - np.clip(sm, 0, 1) * shadow
    shn3 = sh[..., None]

    Hv = norm(L[None, None, :] + V)
    ndh = np.clip(np.sum(N * Hv, -1), 0, 1)
    spec = (ndh ** np.maximum(g["shin"], 1.0)) * g["spec"] * sh

    alb = g["alb"]
    col = alb * (amb + ndl * lc * shn3 + ndl2 * lc2)
    col = col + spec[..., None] * (lc * (0.35 + 0.65 * g["metal"][..., None]))
    # Metall faerbt den Glanz ein
    col = col + g["emis"]
    # Randlicht
    rim = np.clip(1.0 - np.abs(np.sum(N * V, -1)), 0, 1) ** 3
    col = col + rim[..., None] * np.array([0.10, 0.12, 0.15], F32) * hit[..., None]

    if fog is not None:
        fcol, fstart, fend = fog
        z = np.where(hit, g["z"], fend)
        t = np.clip((z - fstart) / max(1e-6, fend - fstart), 0, 1)[..., None]
        col = col * (1 - t) + np.array(fcol, F32)[None, None, :] * t

    # Hintergrund
    if bg is None:
        bg = _bg_gradient(w, h)
    col = np.where(hit[..., None], col, bg)

    if reflect > 0:
        ground = hit & (np.abs(g["pos"][..., 1]) < 2e-3)
        objs = [m for m in scene.meshes if not m.no_shadow]
        if ground.any() and objs:
            sub = Scene()
            for me in objs:
                v = me.v.copy(); v[:, 1] *= -1.0
                sub.meshes.append(Mesh(v, me.f, me.m, smooth=me.smooth,
                                       no_shadow=True))
            L_m = np.array([L[0], -L[1], L[2]], F32)
            rc, rm = render(sub, cam, W, H, ss=ss, light=L_m,
                            light_col=light_col, light2_col=light2_col,
                            sky=sky, ground_amb=ground_amb,
                            bg=np.zeros((h, w, 3), F32), shadow=0.0,
                            reflect=0.0, vignette=0.0, grain=0.0,
                            exposure=exposure, gamma=gamma,
                            _linear=True, _mask=True)
            rm = gaussian_filter(rm, 1.1 * ss)
            rc = np.stack([gaussian_filter(rc[..., k], 1.5 * ss)
                           for k in range(3)], -1)
            yy = np.mgrid[0:h, 0:w][0].astype(F32) / h
            fall = np.clip((yy - 0.30) * 2.2, 0.0, 1.0)
            k = (reflect * rm * fall * ground.astype(F32))[..., None]
            col = col * (1 - k) + rc * k

    if vignette > 0:
        yy, xx = np.mgrid[0:h, 0:w].astype(F32)
        r = np.sqrt(((xx / w) - 0.5) ** 2 + ((yy / h) - 0.5) ** 2) / 0.707
        col = col * (1.0 - vignette * np.clip(r, 0, 1) ** 2.2)[..., None]

    col = col * exposure
    col = col / (1.0 + col * 0.42)                      # weicher Rolloff
    col = np.clip(col, 0, 1) ** (1.0 / gamma)
    if _linear:
        return (col, hit.astype(F32)) if _mask else col

    if grain > 0:
        rng = np.random.default_rng(7)
        col = col + rng.normal(0, grain, col.shape).astype(F32)

    col = np.clip(col, 0, 1)
    if ss > 1:
        col = col.reshape(H, ss, W, ss, 3).mean((1, 3))
    return (col * 255 + 0.5).astype(np.uint8)


def _bg_gradient(w, h, top=(0.30, 0.335, 0.385), bot=(0.10, 0.11, 0.125)):
    t = np.linspace(0, 1, h, dtype=F32)[:, None, None]
    top = np.array(top, F32)[None, None, :]
    bot = np.array(bot, F32)[None, None, :]
    g = top * (1 - t) + bot * t
    yy, xx = np.mgrid[0:h, 0:w].astype(F32)
    r = np.sqrt(((xx / w) - 0.46) ** 2 + ((yy / h) - 0.30) ** 2)
    glow = np.exp(-(r / 0.46) ** 2)[..., None] * 0.22
    return np.broadcast_to(g, (h, w, 3)) + glow



