"""CharCube product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the 200 L outer drum with chimes, rolling hoops and
sliding port dampers, wrapped in its ceramic fibre blanket held by a wire mesh, with a lid and top
band blanket; the riveted lid collar, air shroud with its band damper handle, burner throat and
flue with its stop clips and a conical rain cap on three riveted flat-bar legs; the teal water jacket
with its flared sleeve foot, mineral wool blanket, open vent, loose lid and brass ball-valve tap; the
jacket tripod of 40 x 40 x 4 mm steel angle bolted to fins welded on the jacket, with bolted foot
cleats and pads; the pinwheel concrete block plinth with its ceramic fibre board, block thermocouple
and ash pan; the retort with its bolt-ring lid and U-bolt handles on firebrick standoffs; the spiral
baffle; the thermocouple logger strapped beside a leg, with its probes; and the lifting aid (post in a
ground sleeve, bolted arm and brace, pulleys, hand winch, rope and hook), parked behind the kiln.
Revised 2026-10-02 to match the constructable design (CCB-DDR-003) and the 2026-10-02 decisions.
Hot-surface labels (yellow triangles) sit on both blankets and a teal name band on the drum
blanket. Context is a compact paved ground patch and the shared clay mannequin standing beside
the kiln for scale.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, height and interface comes from PARAMS, levels() and build_parts() in
model.py, with the same axes: Z up, ground at Z = 0, kiln axis on X = Y = 0, front toward -Y.
Differences from model.py are listed in docs/REVIEW.md (sessions 2026-09-26 and 2026-10-02).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".kit"))

from build123d import (Axis, Box, Cone, Cylinder, Plane, Polygon, Pos, Rectangle, Rot, Solid, Sphere,
                       Torus, Vector, extrude, fillet)
from build123d import Compound
from model import PARAMS, build_components, build_parts, levels

TITLE = "CharCube: retort kiln that makes biochar and hot water"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 22, "az": -40,
     "note": "Product render from the front right and above (about 22 deg elevation); blanketed kiln on its "
             "block plinth, burner throat and teal water jacket on the tripod above it, tap at right, "
             "person standing at left for scale"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): plinth and ash pan, "
             "outer drum, blanket, retort on firebricks, lid, air shroud, burner throat, water jacket, "
             "jacket blanket, spiral baffle, flue with conical rain cap, tripod and logger"},
    {"name": "site", "groups": ["shell", "internal", "site", "context"], "explode": False, "el": 14, "az": -30,
     "note": "Site view from the front right, slightly above (about 14 deg elevation): the kiln with the lifting "
             "aid's post 1.2 m behind it and its arm parked to the left, person standing at left for scale"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 16, "az": -35,
     "note": "Detail from the front right, slightly above (about 16 deg elevation): the kiln alone without "
             "the ground and person; air shroud and burner throat under the jacket, hot-surface labels, "
             "tap and logger"},
]

# Colours (restrained product palette; kit accent)
C_BLACK = "#2E3237"      # high-temperature black paint on the hot steel
C_SCALE = "#5A5048"      # scaled retort steel
C_BRICK = "#D6C29C"
C_CERAMIC = "#EFECE6"    # ceramic fibre blanket
C_WOOL = "#D9D1BF"       # mineral wool blanket
C_WIRE = "#9AA0A7"
C_ACCENT = "#0F766E"
C_TRIPOD = "#0F766E"
C_BOLT = "#B8BEC6"
C_BRASS = "#C9A227"
C_CONCRETE = "#B9B6AE"
C_PAN = "#3A3D42"
C_SHELL = "#E9EAEC"
C_SHELL2 = "#C9CDD3"
C_WINDOW = "#DCEBF5"
C_PCB = "#166534"
C_CHIP = "#111827"
C_LED_G = "#22C55E"
C_YELLOW = "#F2C230"
C_INK = "#1C1F24"
C_LABEL = "#F4F4F2"
C_CABLE = "#23262B"
C_GROUND = "#CBC5B8"
C_CLAY = "#9CA3AF"

MQ_AT = (-880.0, -260.0, 25.0)     # mannequin x, y and turn toward the kiln (deg)


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(r, h, z, x=0.0, y=0.0):
    """Cylinder on a vertical axis from z to z + h (as model.py)."""
    return Pos(x, y, z + h / 2) * Cylinder(r, h)


def _ring(r_out, r_in, h, z):
    return _zcyl(r_out, h, z) - _zcyl(r_in, h + 2, z - 1)


def _tube(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(points, r):
    """Round tube through `points` with spherical joints."""
    out = None
    for a, c in zip(points, points[1:]):
        seg = _tube(a, c, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _hoop(r, z, rw):
    return Pos(0, 0, z) * Torus(r, rw)


def _polar(r, ang_deg, z):
    a = math.radians(ang_deg)
    return (r * math.cos(a), r * math.sin(a), z)


def _wrap(profile, ang_deg, r_in, r_out, z0, z1):
    """Wrap a flat profile solid (drawn in the XZ plane, facing -Y) onto a cylinder band r_in..r_out
    between z0 and z1, centred on the direction `ang_deg` from +X."""
    band = _ring(r_out, r_in, z1 - z0, z0)
    return (Rot(0, 0, ang_deg + 90) * profile) & band


def _flat(pts, depth=2000.0):
    """Prism from a polygon in the XZ plane (x across, z up), extruded toward -Y."""
    return extrude(Plane.XZ * Polygon(*pts, align=None), amount=depth)


def _rect(cx, cz, w, h, depth=2000.0):
    return Pos(cx, 0, cz) * Box(w, depth, h) & Pos(0, -depth / 2, 0) * Box(4 * depth, depth, 4 * depth)


def _hot_label(ang, r, zc, s=1.0):
    """Hot-surface label: yellow triangle with a black border and three heat lines, on a cylinder."""
    h = 110 * s
    tri = [(-h * 0.577, zc - h / 3), (h * 0.577, zc - h / 3), (0, zc + 2 * h / 3)]
    tri_in = [(-h * 0.577 + 12 * s, zc - h / 3 + 7 * s), (h * 0.577 - 12 * s, zc - h / 3 + 7 * s),
              (0, zc + 2 * h / 3 - 14 * s)]
    base = _wrap(_flat(tri), ang, r, r + 0.6, zc - h, zc + h)
    border = _wrap(_flat(tri) - _flat(tri_in), ang, r + 0.6, r + 1.0, zc - h, zc + h)
    lines = None
    for k in (-1, 0, 1):
        for j in range(3):
            seg = _rect(k * 13 * s + (3 * s if j % 2 else -3 * s), zc - 20 * s + j * 12 * s, 4 * s, 11 * s)
            lines = seg if lines is None else lines + seg
    lines += _rect(0, zc - 27 * s, 46 * s, 4 * s)
    ink = border + _wrap(lines, ang, r + 0.6, r + 1.0, zc - h, zc + h)
    return base, ink


def _angle_leg(foot, top, ang_deg):
    """40 x 40 x 4 mm steel angle from foot to top, heel facing outward."""
    a, b = Vector(*foot), Vector(*top)
    d = (b - a).normalized()
    rh = Vector(math.cos(math.radians(ang_deg)), math.sin(math.radians(ang_deg)), 0)
    xd = (rh - d * rh.dot(d)).normalized()
    pl = Plane(origin=a, x_dir=xd, z_dir=d)
    L = (b - a).length
    f1 = extrude(pl * Pos(18, 0) * Rectangle(4, 40), amount=L)
    f2 = extrude(pl * Pos(0, 18) * Rectangle(40, 4), amount=L)
    return f1 + f2


def product_parts(P=PARAMS):
    L = levels(P)
    CM = build_components(P)
    M = build_parts(P, C=CM)
    z0, z_lid, z_thr, z_jkt, z_jtop = L["z0"], L["z_lid"], L["z_thr"], L["z_jkt"], L["z_jtop"]
    ro, rr, rf = P["OUT_D"] / 2, P["RET_D"] / 2, P["FLUE_D"] / 2
    rj, rsl = P["JKT_D"] / 2, P["SLEEVE_D"] / 2
    rs = P["SHROUD_D"] / 2
    rb = ro + P["INS_T"]                 # outside of the drum blanket
    rjb = rj + P["JKT_INS_T"]            # outside of the jacket blanket
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # explode offsets (mm)
    E_BLK, E_PAN = (0, 0, -520), (0, 0, -360)
    E_DRUM = (0, 0, 0)
    E_INS = (-1000, 0, 0)
    E_RET, E_BRK = (820, 0, 380), (820, 0, 60)
    E_LIDINS, E_LID = (0, 0, 520), (0, 0, 760)
    E_SHR, E_THR = (-620, 0, 980), (0, 0, 1000)
    E_JKT, E_JINS = (0, 0, 1650), (-760, 0, 1650)
    E_BAF = (700, 0, 1850)
    E_FLUE = (0, 0, 2350)
    E_TRI = (900, 1900, 1300)

    # ------------------------------------------------------------ 12 plinth: blocks and ash pan
    blocks = CM["blocks"].shape
    blocks = _fillet_try(blocks, blocks.edges(), [4.0, 2.0])
    add("Plinth concrete blocks", blocks, C_CONCRETE, "painted", 12, "shell", E_BLK)
    add("Ceramic fibre board", CM["board"].shape, C_CERAMIC, "fabric", 12, "shell", ((E_BLK[0] + E_PAN[0]) / 2, 0, (E_BLK[2] + E_PAN[2]) / 2))
    add("Block thermocouple", CM["btc"].shape, C_CABLE, "rubber", 13, "shell", E_BLK)
    hp = P["BASE_H"] + P["BOARD"][2]
    pan = CM["pan"].shape
    lip = _box(0, 0, hp + 9, 760, 600, 18) - _box(0, 0, hp + 10, 754, 594, 30)
    pan = _fillet_try(pan + lip, (pan + lip).edges().filter_by(Axis.Z), [3.0, 1.5])
    add("Steel ash pan", pan, C_PAN, "metal", 12, "shell", E_PAN)

    # ------------------------------------------------------------ 1 outer drum
    drum = M[1][1]
    drum += _hoop(ro, z0 + 5, 5.0) + _hoop(ro, z_lid - 6, 4.5)                 # chimes
    for f in (1 / 3, 2 / 3):
        drum += _hoop(ro, z0 + P["OUT_H"] * f, 6.0)                            # rolling hoops
    add("Outer drum, 200 L", drum, C_BLACK, "painted", 1, "shell", E_DRUM)

    # sliding port dampers: curved plates in guide strips, each half open, with a knob
    damp, knobs = None, None
    pz0, pz1 = z0 + P["PORT_Z"], z0 + P["PORT_Z"] + P["PORT_H"]
    for k in range(P["N_PORTS"]):
        a = 45 + 360 / P["N_PORTS"] * k
        plate = _wrap(_rect(28, (pz0 + pz1) / 2, 62, P["PORT_H"] + 14), a, ro + 1.5, ro + 3.5, pz0 - 20, pz1 + 20)
        rails = _wrap(_rect(0, pz0 - 10, 150, 6) + _rect(0, pz1 + 10, 150, 6), a, ro, ro + 5, pz0 - 20, pz1 + 20)
        d = plate + rails
        damp = d if damp is None else damp + d
        kx, ky, _ = _polar(ro + 3.5, a, 0)
        t = math.radians(a)
        tx, ty = -math.sin(t), math.cos(t)                                    # tangential direction
        kb = _tube((kx + tx * 44, ky + ty * 44, (pz0 + pz1) / 2),
                   (kx + tx * 44 + math.cos(t) * 22, ky + ty * 44 + math.sin(t) * 22, (pz0 + pz1) / 2), 7)
        kb += Pos(kx + tx * 44 + math.cos(t) * 22, ky + ty * 44 + math.sin(t) * 22, (pz0 + pz1) / 2) * Sphere(9)
        knobs = kb if knobs is None else knobs + kb
    add("Primary air port dampers", damp, "#4A4F56", "metal", 1, "shell", E_DRUM)
    add("Port damper knobs", knobs, C_INK, "plastic", 1, "shell", E_DRUM)

    # ------------------------------------------------------------ 11 drum blanket with wire mesh
    zi0, zi1 = z0 + P["INS_BOTTOM"], z_lid - P["INS_TOP_GAP"]
    ins = M[11][1]
    ins = _fillet_try(ins, ins.edges(), [6.0, 4.0, 2.0])
    flap = _wrap(_rect(0, (zi0 + zi1) / 2, 70, zi1 - zi0 - 6), 160, rb - 1, rb + 4, zi0, zi1)
    add("Ceramic fibre drum blanket", ins + flap, C_CERAMIC, "fabric", 11, "shell", E_INS)
    mesh = None
    n_h = 5
    for i in range(n_h):
        z = zi0 + 30 + (zi1 - zi0 - 60) * i / (n_h - 1)
        h = _ring(rb + 2.6, rb - 0.5, 2.6, z - 1.3)
        mesh = h if mesh is None else mesh + h
    for k in range(16):
        x, y, _ = _polar(rb + 0.6, 11.25 + 22.5 * k, 0)
        mesh += Pos(x, y, (zi0 + zi1) / 2) * Rot(0, 0, 11.25 + 22.5 * k) * Box(2.2, 2.2, zi1 - zi0 - 40)
    add("Blanket wire mesh", mesh, C_WIRE, "metal", 11, "shell", E_INS)
    base, ink = _hot_label(-40, rb + 3.0, zi0 + 300, 0.8)
    add("Hot-surface label, drum (yellow)", base, C_YELLOW, "paper", 14, "shell", E_INS)
    add("Hot-surface label print, drum", ink, C_INK, "paper", 14, "shell", E_INS)
    band = _wrap(_rect(0, zi1 - 120, 250, 64), -40, rb + 3.0, rb + 3.8, zi1 - 200, zi1 - 40)
    add("Name band", band, C_ACCENT, "painted", 14, "shell", E_INS)
    txt = None
    x = -96
    for w in (22, 16, 16, 12, 22, 16, 16, 16):                                  # "CharCube" as simple letter blocks
        seg = _rect(x + w / 2, zi1 - 120, w - 5, 26)
        txt = seg if txt is None else txt + seg
        x += w + 2
    txt += _rect(0, zi1 - 142, 150, 3)
    add("Name band lettering", _wrap(txt, -40, rb + 3.8, rb + 4.3, zi1 - 200, zi1 - 40), C_LABEL, "paper", 14,
        "shell", E_INS)

    # ------------------------------------------------------------ 3 retort and 4 firebricks (inside)
    ret = M[3][1]
    zr = L["z_ret"]
    for f in (1 / 3, 2 / 3):
        ret += _hoop(rr, zr + P["RET_H"] * f, 4.5)
    zt = zr + P["RET_H"]
    lug = _box(rr + 20, 0, zt - 5, 22, 30, 16) - _tube((rr + 20, -20, zt - 5), (rr + 20, 20, zt - 5), 4)
    ret += lug
    for k in range(3):                                                         # lid stiffening swages
        ret += Pos(0, 0, zt + 1.5) * (Torus(rr * (0.35 + 0.22 * k), 2.5) & _box(0, 0, 3, 2 * rr, 2 * rr, 6))
    add("Inner retort, 114 L", ret, C_SCALE, "metal", 3, "internal", E_RET)
    bolt = _tube((rr + 20, -24, zt - 5), (rr + 20, 24, zt - 5), 3.5) + _box(rr + 20, -27, zt - 5, 10, 6, 10)
    add("Retort bolt-ring clamp bolt", bolt, C_BOLT, "metal", 3, "internal", E_RET)
    bricks = M[4][1]
    bricks = _fillet_try(bricks, bricks.edges(), [4.0, 2.0])
    add("Firebrick standoffs (3)", bricks, C_BRICK, "painted", 4, "internal", E_BRK)

    # ------------------------------------------------------------ 17 lid blanket, 2 lid with collar
    lins = M[17][1]
    lins = _fillet_try(lins, lins.edges(), [5.0, 3.0, 1.5])
    add("Lid and top band blanket", lins, C_CERAMIC, "fabric", 17, "shell", E_LIDINS)
    lw = None
    ti = P["LID_INS_T"]
    for r in (rs + 60, rb - 25):
        h = _hoop(r, z_thr + ti + 1.0, 1.4)
        lw = h if lw is None else lw + h
    lw += _hoop(rb + 1.0, z_thr - 16, 1.4)
    add("Lid blanket tie wires", lw, C_WIRE, "metal", 17, "shell", E_LIDINS)

    lid = M[2][1]
    lid += _hoop(rf + 4, z_thr + P["COLLAR_H"], 2.5)                            # rolled collar edge
    add("Outer lid with flue collar", lid, C_BLACK, "painted", 2, "shell", E_LID)
    riv = None
    for k in range(6):
        x, y, _ = _polar(rf + 4.5, 30 + 60 * k, 0)
        r_ = Pos(x, y, z_thr + 12) * Sphere(4.0)
        riv = r_ if riv is None else riv + r_
    add("Collar rivets", riv, C_BOLT, "metal", 14, "shell", E_LID)

    # ------------------------------------------------------------ 6 throat, 5 air shroud
    add("Burner throat (afterburner)", M[6][1], "#3A3E44", "metal", 6, "shell", E_THR)
    zs = z_thr + P["SHROUD_Z"]
    shroud = M[5][1]
    shroud += _hoop(rs, zs + P["SHROUD_H"], 2.0)
    add("Secondary air shroud", shroud, C_BLACK, "painted", 5, "shell", E_SHR)
    x0, y0, _ = _polar(rs + 4, -40, 0)
    hx, hy, _ = _polar(rs + 58, -40, 0)
    handle = _tube((x0, y0, zs + 20), (hx, hy, zs + 20), 5) + Pos(hx, hy, zs + 20) * Sphere(12)
    add("Band damper handle", handle, C_INK, "plastic", 5, "shell", E_SHR)

    # ------------------------------------------------------------ 8 water jacket, 9 tap, 16 blanket
    jt = P["JKT_T"]
    jkt = CM["jacket"].shape                                                   # with the flared sleeve foot and lift-bar holes
    jkt += _hoop(rj, z_jkt + 2, 3.0) + _hoop(rj, z_jtop - 2, 3.0)
    jkt += _tube((0, rj - 40, z_jtop), (0, rj - 40, z_jtop + 90), 12) - _tube((0, rj - 40, z_jtop - 5),
                                                                               (0, rj - 40, z_jtop + 100), 9)
    add("Water jacket, about 60 L", jkt, C_ACCENT, "painted", 8, "shell", E_JKT)
    jlid = _zcyl(rj + 5, 2, z_jtop + 3) - _zcyl(rsl + 5, 10, z_jtop - 2) - _zcyl(14, 20, z_jtop - 5, 0, rj - 40)
    jlid += _ring(rj + 5, rj + 3, 12, z_jtop - 7)
    jlid = _fillet_try(jlid, jlid.edges(), [0.8, 0.4])
    add("Jacket loose lid", jlid, C_ACCENT, "painted", 8, "shell", (0, 0, 1650 + 280))
    vent = _hoop(12, z_jtop + 90, 2.0)
    add("Vent rim (open, never capped)", vent, C_BOLT, "metal", 8, "shell", (0, 0, 1650 + 280))

    jins = M[16][1]
    jins = _fillet_try(jins, jins.edges(), [5.0, 3.0])
    add("Mineral wool jacket blanket", jins, C_WOOL, "fabric", 16, "shell", E_JINS)
    jw = None
    for z in (z_jkt + 110, z_jkt + 330, z_jtop - 50):
        h = _hoop(rjb + 0.8, z, 1.4)
        jw = h if jw is None else jw + h
    add("Jacket blanket tie wires", jw, C_WIRE, "metal", 16, "shell", E_JINS)
    base, ink = _hot_label(-40, rjb + 2.5, z_jkt + 220, 0.8)
    add("Hot-surface label, jacket (yellow)", base, C_YELLOW, "paper", 14, "shell", E_JINS)
    add("Hot-surface label print, jacket", ink, C_INK, "paper", 14, "shell", E_JINS)

    zt_ = z_jkt + 40
    E_TAP = (E_JKT[0] + 220, 0, E_JKT[2])
    nip = _tube((rj - 2, 0, zt_), (rj + 104, 0, zt_), 11)
    for xh in (rj + 30, rj + 100):
        nip += Pos(xh, 0, zt_) * Rot(0, 90, 0) * Cylinder(15, 10)
    valve = Pos(rj + 125, 0, zt_) * Sphere(20) & _box(rj + 125, 0, zt_, 40, 36, 36)
    valve += _tube((rj + 105, 0, zt_), (rj + 145, 0, zt_), 13)
    valve += _tube((rj + 125, 0, zt_ - 14), (rj + 125, 0, zt_ - 44), 8)                  # spout
    valve += _tube((rj + 125, 0, zt_ + 18), (rj + 125, 0, zt_ + 30), 5)                  # stem
    add("Draw-off tap, brass ball valve", nip + valve, C_BRASS, "metal", 9, "shell", E_TAP)
    lever = _box(rj + 125, -58, zt_ + 36, 18, 120, 7)                                   # lever across the pipe (closed)
    lever = _fillet_try(lever, lever.edges().filter_by(Axis.Z), [3.5, 2.0])
    lever += _box(rj + 125, 0, zt_ + 34, 24, 24, 10)
    add("Tap lever", lever, C_INK, "rubber", 9, "shell", E_TAP)

    # ------------------------------------------------------------ 7 flue, 15 baffle
    fl = CM["flue"].shape + _hoop(rf, L["z_out"] - 2, 2.0)
    add("Flue pipe", fl, C_BLACK, "painted", 7, "shell", E_FLUE)
    add("Flue stop clips and cap legs", Compound(children=[CM["clips"].shape, CM["cap_legs"].shape]), C_BLACK, "painted", 7, "shell", E_FLUE)
    add("Conical rain cap", CM["cap"].shape, C_BLACK, "painted", 7, "shell", E_FLUE)
    add("Spiral baffle insert", M[15][1], "#4A4F56", "metal", 15, "internal", E_BAF)

    # ------------------------------------------------------------ 10 tripod: angle legs, ring seat, gussets
    add("Jacket support tripod", Compound(children=[CM[k].shape for k in ("tri_leg", "tri_cleat", "tri_pad")]),
        C_TRIPOD, "painted", 10, "shell", E_TRI)
    add("Jacket fins", CM["fins"].shape, C_ACCENT, "painted", 8, "shell", E_JKT)
    add("Tripod bolts", CM["tri_bolts"].shape, C_BOLT, "metal", 14, "shell", E_TRI)

    # ------------------------------------------------------------ 13 thermocouple logger and probes (positions from model.py)
    lg = CM["logger"].shape
    lbb = lg.bounding_box()
    add("Logger enclosure", lg, C_SHELL, "plastic", 13, "shell", E_TRI)
    lc = lbb.center()
    led = Pos(lc.X, lbb.min.Y - 1.5, lc.Z - 40) * Sphere(3.5)
    add("Logger status light, green (lit)", led, C_LED_G, "emissive", 13, "shell", E_TRI)
    add("Type K probes", CM["probes"].shape, C_BOLT, "metal", 13, "shell", E_TRI)
    zc = L["z_core"]
    wp = (lc.X, P["CORE_PROBE_L"] + 50, lbb.max.Z + 150)
    cab = _pipe([(lc.X, lc.Y, lbb.max.Z), wp, (0, P["CORE_PROBE_L"] + 50, zc)], 3)
    cab += _pipe([(lc.X + 10, lc.Y, lbb.max.Z), (lc.X + 10, P["THROAT_PROBE_L"] + 50, L["z_tprobe"]),
                  (0, P["THROAT_PROBE_L"] + 50, L["z_tprobe"])], 3)
    add("Probe cables", cab, C_CABLE, "rubber", 13, "shell", E_TRI)

    # ------------------------------------------------------------ 18 lifting aid, parked (footing below ground left out)
    E_AID = (0, 900, 0)
    add("Lifting aid post and ground sleeve", Compound(children=[CM["post"].shape, CM["gsleeve"].shape]), C_BLACK, "painted", 18, "site", E_AID)
    add("Lifting aid arm and brace", Compound(children=[CM["arm"].shape, CM["brace"].shape]), C_BLACK, "painted", 18, "site", E_AID)
    add("Lifting aid pulleys, bolts and hook", Compound(children=[CM[k].shape for k in ("pulleys", "aid_bolts", "hook")]),
        C_BOLT, "metal", 18, "site", E_AID)
    add("Hand winch", CM["winch"].shape, C_ACCENT, "painted", 18, "site", E_AID)
    add("Steel wire rope", CM["rope"].shape, C_WIRE, "metal", 18, "site", E_AID)

    # ------------------------------------------------------------ context: ground patch and person
    gx0, gx1, gy0, gy1 = -1500.0, 850.0, -950.0, 1500.0
    ground = _box((gx0 + gx1) / 2, (gy0 + gy1) / 2, -30, gx1 - gx0, gy1 - gy0, 60)
    ground = _fillet_try(ground, ground.faces().sort_by(Axis.Z)[-1].edges(), [10.0, 5.0])
    for x in (-1000, -500, 0, 500):                                           # paver joints every 500 mm
        ground -= _box(x, (gy0 + gy1) / 2, 0, 6, gy1 - gy0 + 20, 6)
    for y in (-500, 0, 500):
        ground -= _box((gx0 + gx1) / 2, y, 0, gx1 - gx0 + 20, 6, 6)
    add("Paved ground patch", ground, C_GROUND, "painted", None, "context", (0, 0, 0))
    from context_parts import mannequin
    person = Pos(MQ_AT[0], MQ_AT[1], 0) * Rot(0, 0, MQ_AT[2]) * mannequin(1750, "stand")
    add("Person, 1.75 m (clay mannequin)", person, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
