# -*- coding: utf-8 -*-
"""Umgebungen: Boden, Licht, Hintergrund. Ein Satz Vorgaben je Schauplatz."""
import numpy as np
import r3d
from r3d import mat, hexcol, plane, box, rbox, tube, lathe, F32


def _noise(P, scale, seed=0, amp=0.12):
    x = P[..., 0] * scale + seed * 11.7
    z = P[..., 2] * scale + seed * 5.3
    n = (np.sin(x * 1.0) * np.sin(z * 1.3)
         + 0.5 * np.sin(x * 2.7 + 1.1) * np.sin(z * 2.1 + 0.4)
         + 0.25 * np.sin(x * 6.1 + 2.3) * np.sin(z * 5.3 + 1.9))
    return 1.0 + amp * (n / 1.75)


def tex_asphalt(P):
    f = _noise(P, 7.0, 1, 0.16) * _noise(P, 31.0, 3, 0.09)
    return np.repeat(f[..., None], 3, -1)


def tex_concrete(P):
    f = _noise(P, 3.0, 5, 0.10) * _noise(P, 23.0, 7, 0.06)
    # Dehnfugen alle 3 m
    gx = np.minimum(np.abs((P[..., 0] % 3.0) - 1.5), 1.5)
    gz = np.minimum(np.abs((P[..., 2] % 3.0) - 1.5), 1.5)
    joint = np.clip(np.minimum(gx, gz) / 0.035, 0, 1) * 0.45 + 0.55
    return np.repeat((f * joint)[..., None], 3, -1)


def tex_track(P):
    """Asphalt mit weisser Begrenzungslinie bei z = +-3,2 m."""
    f = tex_asphalt(P)
    d = np.minimum(np.abs(np.abs(P[..., 2]) - 3.2), 9.9)
    line = np.clip(1.0 - d / 0.07, 0, 1)
    out = f * (1 - line[..., None]) + line[..., None] * 7.5
    return out


def tex_studio(P):
    r = np.sqrt(P[..., 0] ** 2 + P[..., 2] ** 2)
    return np.repeat(np.clip(1.25 - r * 0.035, 0.45, 1.3)[..., None], 3, -1)


PRESETS = {
    "studio": dict(
        floor=mat(hexcol("#2c3138"), spec=0.46, shin=150, tex=tex_studio),
        light=(-0.46, 0.76, 0.46), light_col=(1.34, 1.30, 1.24),
        light2_col=(0.26, 0.29, 0.35), sky=(0.40, 0.45, 0.54),
        ground_amb=(0.10, 0.105, 0.115),
        bg_top=(0.33, 0.365, 0.42), bg_bot=(0.085, 0.095, 0.11),
        fog=((0.155, 0.175, 0.20), 8.0, 34.0),
        reflect=0.38, shadow=0.85, shadow_blur=3.4, vignette=0.34),
    "hall": dict(
        floor=mat(hexcol("#595f66"), spec=0.20, shin=48, tex=tex_concrete),
        light=(-0.38, 0.84, 0.38), light_col=(1.30, 1.27, 1.20),
        light2_col=(0.30, 0.31, 0.34), sky=(0.52, 0.55, 0.60),
        ground_amb=(0.18, 0.18, 0.19),
        bg_top=(0.40, 0.43, 0.47), bg_bot=(0.20, 0.215, 0.235),
        fog=((0.30, 0.32, 0.35), 10.0, 36.0),
        reflect=0.10, shadow=0.72, shadow_blur=4.2, vignette=0.26),
    "track": dict(
        floor=mat(hexcol("#3e4248"), spec=0.14, shin=30, tex=tex_track),
        light=(-0.30, 0.82, 0.49), light_col=(1.50, 1.44, 1.30),
        light2_col=(0.30, 0.36, 0.48), sky=(0.60, 0.70, 0.88),
        ground_amb=(0.17, 0.175, 0.18),
        bg_top=(0.46, 0.57, 0.74), bg_bot=(0.60, 0.64, 0.70),
        fog=((0.56, 0.61, 0.69), 14.0, 60.0),
        reflect=0.06, shadow=0.80, shadow_blur=3.0, vignette=0.22),
    "dark": dict(
        floor=mat(hexcol("#1a1e23"), spec=0.40, shin=130, tex=tex_studio),
        light=(-0.50, 0.70, 0.50), light_col=(0.95, 0.94, 0.92),
        light2_col=(0.16, 0.19, 0.26), sky=(0.22, 0.26, 0.33),
        ground_amb=(0.05, 0.055, 0.065),
        bg_top=(0.135, 0.16, 0.20), bg_bot=(0.045, 0.05, 0.062),
        fog=((0.07, 0.08, 0.10), 7.0, 30.0),
        reflect=0.30, shadow=0.88, shadow_blur=3.6, vignette=0.42),
}


def backdrop(w, h, top, bot, warm=0.0):
    t = np.linspace(0, 1, h, dtype=F32)[:, None, None]
    top = np.array(top, F32)[None, None, :]
    bot = np.array(bot, F32)[None, None, :]
    g = np.broadcast_to(top * (1 - t) + bot * t, (h, w, 3)).copy()
    yy, xx = np.mgrid[0:h, 0:w].astype(F32)
    r = np.sqrt(((xx / w) - 0.40) ** 2 + ((yy / h) - 0.22) ** 2)
    g += np.exp(-(r / 0.42) ** 2)[..., None] * (0.20 + warm * 0.2)
    return g


def scene_base(kind, floor_size=150.0, n=56):
    p = PRESETS[kind]
    sc = r3d.Scene()
    sc.add(plane(floor_size, 0.0, p["floor"], n=n))
    return sc, p


def render_opts(p, w, h, ss=2, reflect=None):
    return dict(ss=ss, light=p["light"], light_col=p["light_col"],
                light2_col=p["light2_col"], sky=p["sky"],
                ground_amb=p["ground_amb"],
                bg=backdrop(w * ss, h * ss, p["bg_top"], p["bg_bot"]),
                fog=p["fog"],
                reflect=p["reflect"] if reflect is None else reflect,
                shadow=p["shadow"], shadow_blur=p["shadow_blur"],
                vignette=p["vignette"], grain=0.010)
