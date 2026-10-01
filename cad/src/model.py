"""CharCube parametric model (build123d), TRL 3, constructable design (CCB-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL and prints the constructability checks
    python cad/src/model.py --check    prints the constructability checks only

Every component is modelled as it is made and fitted (CCB-DDR-003, design for construction):
the plinth blocks laid as a pinwheel, the retort on bricks clear of its gas holes, the throat
standing on the lid inside a riveted collar, the shroud riveted to the throat, sliding port
dampers in riveted guides, the jacket carried by three welded fins bolted to angle legs, the
flue resting on the sleeve rim on three clips, the baffle hung on a rod through the flue foot,
and the logger strapped beside a leg. Coordinates in mm. Z up, ground at Z = 0, kiln axis on
X = Y = 0, front toward -Y. Sizes are checked in CCB-CAL-001 (docs/04-calcs/sizing.py), which
imports PARAMS, levels() and tripod_geometry() from this file.
"""
import math
import sys
from pathlib import Path

from build123d import (Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, Solid, Vector, export_step,
                       export_stl, extrude)

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 12 plinth: four concrete blocks laid as a pinwheel (580 mm square, 200 mm hole) and a steel ash pan
    "BASE_H": 190.0, "BLOCK": (390.0, 190.0), "PAN": (760.0, 600.0), "PAN_T": 3.0,
    # 1 outer drum: 200 L (55 US gal) open head
    "OUT_D": 572.0, "OUT_H": 851.0, "OUT_T": 1.2,
    "PORT_W": 40.0, "PORT_H": 110.0, "PORT_Z": 20.0, "N_PORTS": 4,   # primary air ports, bottom edge above drum floor
    "DAMPER": (60.0, 122.0, 1.2), "DAMPER_OPEN": 55.0,               # sliding port damper: arc width, height, thickness; travel
    "GUIDE_H": 10.0, "GUIDE_T": 1.5,                                 # riveted guide strips above and below each port
    # 3 inner retort: 114 L (30 US gal) open head
    "RET_D": 463.0, "RET_H": 737.0, "RET_T": 1.0,
    "GAS_HOLE_D": 20.0, "N_GAS_HOLES": 8, "GAS_HOLE_PCD": 300.0,
    "FILL_H": 600.0,        # packed feed depth in the retort
    "PROBE_SLOT": (10.0, 40.0),                                      # slot in the retort side for the core probe
    # 4 firebrick standoffs: long side tangential, centred on this radius (clear of the gas holes)
    "STANDOFF": 60.0, "BRICK": (114.0, 64.0), "BRICK_R": 200.0,
    # 2 outer lid and 6 burner throat
    "LID_T": 1.5, "COLLAR_H": 40.0, "COLLAR_T": 1.5, "LID_HOLE_D": 150.0,
    "FLUE_D": 160.0, "FLUE_T": 2.0,
    "THROAT_H": 400.0,
    # 5 secondary air shroud (sized in CCB-CAL-001; replaces the 25 mm pipe ring of TRL 2)
    "SHROUD_D": 230.0, "SHROUD_H": 150.0, "SHROUD_Z": 40.0,   # bottom edge above the lid top
    "SHROUD_T": 1.5, "BAND_H": 60.0, "BAND_T": 3.0,           # sliding band damper, open position on the shroud
    "AIR_HOLE_D": 12.0, "N_AIR_HOLES": 30, "AIR_RINGS": 2,   # 24 to 30 holes with the baffle (DDR-002)
    # 8 water jacket (annular tank with an integral flue sleeve)
    "JKT_D": 420.0, "JKT_H": 600.0, "JKT_T": 2.0,
    "SLEEVE_D": 168.0, "SLEEVE_T": 2.0, "SOCKET": 50.0,      # sleeve slips over the throat and takes the flue
    "WATER_H": 540.0,       # working water depth (90 % of the tank)
    "JLID_HOLE_D": 210.0, "VENT_D": 26.7, "VENT_R": 170.0,   # loose lid: hole round the sleeve; 3/4 in vent nipple
    "FIN": (210.0, 295.0, -80.0, 60.0, 6.0),                 # welded fins: r from, r to, z from, z to (from jacket underside), thickness
    # 7 flue above the jacket
    "FLUE_ABOVE": 650.0, "CAP_D": 260.0, "CAP_GAP": 60.0,    # flue pipe 650 long: its foot 50 mm inside the sleeve socket
    # 10 tripod: three 40 x 40 x 4 mm angle legs bolted to the fins, pinned at bolted foot cleats
    "FOOT_R": 720.0, "LEG_ANGLE_B": 40.0, "LEG_ANGLE_T": 4.0,
    "LEG_ANGLES": (30.0, 150.0, 270.0), "LEG_BOLT_R": 245.0, "LEG_BOLT_DZ": 15.0, "LEG_BOLT_PITCH": 70.0,
    "FOOT_PAD": (100.0, 6.0), "CLEAT_L": 60.0, "LEG_FOOT_Z": 12.0, "FOOT_BOLT_Z": 30.0,
    # 11 insulation
    "INS_T": 25.0, "INS_BOTTOM": 140.0, "INS_TOP_GAP": 30.0,
    # 15 spiral baffle insert in the jacket sleeve (DDR-002, item 12): twisted steel strip, lifts out with the flue
    "BAFFLE_W": 150.0, "BAFFLE_T": 1.5, "BAFFLE_PITCH": 300.0, "BAFFLE_SEGS": 24,
    "ROD_D": 10.0, "ROD_L": 160.0, "ROD_Z": 15.0,            # hanger rod through the flue foot, above the flue foot
    # 16 jacket shell blanket (DDR-002, item 12): mineral wool held by wire, tap and vent left clear
    "JKT_INS_T": 25.0,
    # 17 lid and top band blanket (DDR-002, item 13): ceramic fibre, clear of the air shroud intake
    "LID_INS_T": 25.0,      # skirt covers the bare top band (INS_TOP_GAP) and the locking ring
    # 13 logger and probes, both probes at the back (+Y)
    "CORE_PROBE_L": 500.0, "THROAT_PROBE_L": 300.0, "THROAT_PROBE_DZ": 70.0, "LOGGER_Z": 520.0,
}
P = PARAMS


def levels(p=PARAMS):
    """Key heights (mm above ground) derived from the parameters."""
    z0 = p["BASE_H"] + p["PAN_T"]                    # outer drum floor
    z_lid = z0 + p["OUT_H"]                          # outer lid underside
    z_thr = z_lid + p["LID_T"]                       # throat base (lid top)
    z_jkt = z_thr + p["THROAT_H"]                    # jacket underside
    z_jtop = z_jkt + p["JKT_H"]
    z_out = z_jtop + p["FLUE_ABOVE"]                 # flue outlet (flue foot at z_jtop, inside the sleeve socket)
    z_ret = z0 + p["OUT_T"] + p["STANDOFF"]          # retort underside
    return {"z0": z0, "z_lid": z_lid, "z_thr": z_thr, "z_jkt": z_jkt, "z_jtop": z_jtop,
            "z_out": z_out, "z_cap": z_out + p["CAP_GAP"], "z_ret": z_ret,
            "z_ret_top": z_ret + p["RET_H"], "z_ports": z0 + p["PORT_Z"] + p["PORT_H"] / 2,
            "z_core": z_ret + p["FILL_H"] / 2, "z_tprobe": z_jkt - p["THROAT_PROBE_DZ"]}


# ------------------------------------------------------------------ geometry helpers
def _zcyl(r, h, z, x=0.0, y=0.0):
    return Pos(x, y, z + h / 2) * Cylinder(r, h)


def _shell(r_out, r_in, h, z):
    return _zcyl(r_out, h, z) - _zcyl(r_in, h + 2, z - 1)


def _tube(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _bx(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _wedge(a0, a1, z0, z1, big=2000.0):
    """Angular sector between a0 and a1 (degrees, a1 - a0 < 180) from z0 to z1."""
    h, zc = z1 - z0, (z0 + z1) / 2
    left = Rot(0, 0, a0) * Pos(0, big / 2, zc) * Box(2 * big, big, h)
    right = Rot(0, 0, a1) * Pos(0, -big / 2, zc) * Box(2 * big, big, h)
    return left & right


def _arc(r_in, r_out, z0, z1, a0, a1):
    """A curved strip: part of a ring between radii r_in and r_out, heights z0 and z1, angles a0 to a1."""
    return _shell(r_out, r_in, z1 - z0, z0) & _wedge(a0, a1, z0 - 1, z1 + 1)


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _hexnut(a, b, af):
    """Hex prism from point a to point b, across flats af."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    r = af / math.sqrt(3)
    pts = [(r * math.cos(math.radians(60 * k)), r * math.sin(math.radians(60 * k))) for k in range(6)]
    return extrude(Plane(origin=a, z_dir=d.normalized()) * Polygon(*pts, align=None), amount=d.length)


def _bolt(a, b, d, af):
    """Bolt from a (head side) to b (nut side): shank plus a head and a nut."""
    a, b = Vector(*a), Vector(*b)
    u = (b - a).normalized()
    h = 0.7 * d
    return (_tube(tuple(a), tuple(b), d / 2) + _hexnut(tuple(a - u * h), tuple(a), af)
            + _hexnut(tuple(b), tuple(b + u * h), af))


# ------------------------------------------------------------------ tripod geometry
def tripod_geometry(p=PARAMS):
    """Leg layout in the leg's own radial plane (X radial, Z up): the leg axis runs from the ground
    point G (FOOT_R, 0) to the upper fin bolt B1. Returns points, unit vectors and lengths (mm)."""
    L = levels(p)
    g = (p["FOOT_R"], 0.0)
    b1 = (p["LEG_BOLT_R"], L["z_jkt"] + p["LEG_BOLT_DZ"])
    dx, dz = b1[0] - g[0], b1[1] - g[1]
    ln = math.hypot(dx, dz)
    d = (dx / ln, dz / ln)                     # up the leg
    n = (d[1], -d[0])                          # across the leg, outward and up (heel side)
    pt = lambda s: (g[0] + s * d[0], g[1] + s * d[1])   # noqa: E731
    s_b1 = ln
    s_b2 = ln - p["LEG_BOLT_PITCH"]
    s_top = ln + 25.0
    s_bot = p["LEG_FOOT_Z"] / d[1]
    s_foot_bolt = p["FOOT_BOLT_Z"] / d[1]
    return {"g": g, "d": d, "n": n, "pt": pt, "b1": pt(s_b1), "b2": pt(s_b2), "top": pt(s_top),
            "bot": pt(s_bot), "foot_bolt": pt(s_foot_bolt), "len": s_top - s_bot,
            "tilt_deg": math.degrees(math.atan2(-dx, dz)), "s": {"b1": s_b1, "b2": s_b2, "top": s_top, "bot": s_bot}}


def _leg_local(p=PARAMS):
    """One leg, its fin, foot cleat, pad and bolts for the leg at angle 0 (radial along +X).
    The leg's radial flange lies flat against the +Y face of the fin and of the cleat."""
    T = tripod_geometry(p)
    d, n, pt = T["d"], T["n"], T["pt"]
    t = p["LEG_ANGLE_T"]
    b = p["LEG_ANGLE_B"]
    fh = p["FIN"][4] / 2

    def strip(s0, s1, w0, w1, y0, y1):
        pts = []
        for s, w in ((s0, w0), (s1, w0), (s1, w1), (s0, w1)):
            x, z = pt(s)
            pts.append((x + w * n[0], z + w * n[1]))
        prof = Polygon(*pts, align=None)
        sol = extrude(Plane.XZ * prof, amount=y1 - y0)
        return Pos(0, y0 - sol.bounding_box().min.Y, 0) * sol

    s0, s1 = T["s"]["bot"] - 30, T["s"]["top"]
    flange_r = strip(s0, s1, -(b - 22), 22, fh, fh + t)          # radial flange, 40 wide, beside the fin
    flange_o = strip(s0, s1, 22 - t, 22, fh, fh + b)             # outstanding flange at the heel, pointing +Y
    leg = (flange_r + flange_o) & _bx(-5000, 5000, -5000, 5000, p["LEG_FOOT_Z"], 1e5)
    # bolt holes through the radial flange
    holes = []
    for key in ("b1", "b2", "foot_bolt"):
        x, z = T[key]
        holes.append(_tube((x, -50, z), (x, 50, z), 5.5))
    leg = leg - _fuse(holes)
    # fin, welded to the jacket shell (part of the jacket, BOM 8)
    L = levels(p)
    r0, r1, zf0, zf1, ft = p["FIN"]
    fin = _bx(r0, r1, -ft / 2, ft / 2, L["z_jkt"] + zf0, L["z_jkt"] + zf1)
    fin = fin - _fuse(holes[:2])
    # foot: cleat (40 x 40 x 4 angle, CLEAT_L long) on a pad, leg pinned by one M10 bolt
    xc = T["foot_bolt"][0]
    pw, pt_ = p["FOOT_PAD"]
    cl = p["CLEAT_L"]
    cleat = (_bx(xc - cl / 2, xc + cl / 2, fh - t, fh, pt_, pt_ + b)
             + _bx(xc - cl / 2, xc + cl / 2, fh - b, fh, pt_, pt_ + t))
    cleat = cleat - holes[2]
    pad_y = fh - b / 2
    pad = _bx(xc - pw / 2, xc + pw / 2, pad_y - pw / 2, pad_y + pw / 2, 0, pt_)
    pbolts = []
    for sx in (-1, 1):
        hole = _zcyl(4.5, 30, -10, xc + sx * 18, fh - 22)
        cleat = cleat - hole
        pad = pad - hole
        # countersunk M8 screw from under the pad (flush), nyloc nut on the cleat flange
        pbolts.append(_zcyl(4, pt_ + t, 0, xc + sx * 18, fh - 22)
                      + _hexnut((xc + sx * 18, fh - 22, pt_ + t), (xc + sx * 18, fh - 22, pt_ + t + 8), 13))
    # M10 bolts: two through fin and leg, one through cleat and leg
    bolts = []
    for key, y0 in (("b1", -fh), ("b2", -fh), ("foot_bolt", fh - t)):
        x, z = T[key]
        bolts.append(_bolt((x, y0, z), (x, fh + t, z), 10, 17))
    return {"leg": leg, "fin": fin, "cleat": cleat, "pad": pad, "bolts": _fuse(bolts + pbolts)}


# ------------------------------------------------------------------ components
class Comp:
    def __init__(self, name, shape, bom, kind):
        self.name, self.shape, self.bom, self.kind = name, shape, bom, kind


def build_components(p=PARAMS):
    """Every component as it is made and fitted, keyed by a short name. kind is made, bought,
    drum (a used drum, cut) or fixing."""
    L = levels(p)
    z0, z_lid, z_thr, z_jkt, z_jtop = L["z0"], L["z_lid"], L["z_thr"], L["z_jkt"], L["z_jtop"]
    z_ret, z_rt = L["z_ret"], L["z_ret_top"]
    ro, rr, rf = p["OUT_D"] / 2, p["RET_D"] / 2, p["FLUE_D"] / 2
    rs = p["SHROUD_D"] / 2
    rj, rsl = p["JKT_D"] / 2, p["SLEEVE_D"] / 2
    zc, ztp = L["z_core"], L["z_tprobe"]
    C = {}

    def add(key, name, shape, bom, kind):
        C[key] = Comp(name, shape, bom, kind)

    # 12 plinth: pinwheel of four blocks, 580 mm square with a 200 mm square hole, and the ash pan
    bl, bw = p["BLOCK"]
    h = p["BASE_H"]
    q = (bl + bw) / 2                     # 290: half the square
    m = (bl - bw) / 2                     # 100: half the hole
    blocks = [_bx(-q, m, m, q, 0, h), _bx(m, q, -m, q, 0, h), _bx(-m, q, -q, -m, 0, h), _bx(-q, -m, -q, m, 0, h)]
    add("blocks", "Concrete blocks (4)", _fuse(blocks), 12, "bought")
    pw, pd = p["PAN"]
    add("pan", "Ash pan", _bx(-pw / 2, pw / 2, -pd / 2, pd / 2, h, h + p["PAN_T"]), 12, "made")

    # 1 outer drum: shell and floor, four primary air ports, the core probe hole at the back
    outer = _shell(ro, ro - p["OUT_T"], p["OUT_H"], z0) + _zcyl(ro, p["OUT_T"], z0)
    port_angles = [45 + 360 / p["N_PORTS"] * k for k in range(p["N_PORTS"])]
    for a in port_angles:
        ar = math.radians(a)
        outer = outer - (Pos(ro * math.cos(ar), ro * math.sin(ar), z0 + p["PORT_Z"] + p["PORT_H"] / 2)
                         * Rot(0, 0, a) * Box(20, p["PORT_W"], p["PORT_H"]))
    outer = outer - _tube((0, ro - 10, zc), (0, ro + 10, zc), 5.0)
    add("drum", "Outer drum, cut", outer, 1, "drum")

    # 1 sliding port dampers and their riveted guides (shown open)
    dw, dh, dt = p["DAMPER"]
    zp0 = z0 + p["PORT_Z"]
    zd0 = zp0 + p["PORT_H"] / 2 - dh / 2
    gh, gt = p["GUIDE_H"], p["GUIDE_T"]
    deg = lambda mm: math.degrees(mm / ro)   # noqa: E731
    dampers, guides = [], []
    for a in port_angles:
        c = a + deg(p["DAMPER_OPEN"])
        dampers.append(_arc(ro, ro + dt, zd0, zd0 + dh, c - deg(dw / 2), c + deg(dw / 2)))
        g0, g1 = a - deg(dw / 2 + 10), a + deg(p["DAMPER_OPEN"] + dw / 2 + 10)
        for zg in (zd0 - 4, zd0 + dh + 4 - gh):          # each guide laps 6 mm over the plate edge
            guides.append(_arc(ro + dt, ro + dt + gt, zg, zg + gh, g0, g1))
            for e0, e1 in ((g0, g0 + deg(10)), (g1 - deg(10), g1)):      # joggled end pads, riveted to the drum
                guides.append(_arc(ro, ro + dt, zg, zg + gh, e0, e1))
    add("dampers", "Port dampers (4)", _fuse(dampers), 1, "made")
    add("guides", "Damper guides (8)", _fuse(guides), 1, "made")

    # 4 firebrick standoffs, long side tangential, clear of the gas holes
    stand = []
    bwl, bwr = p["BRICK"]
    for k in range(3):
        a = 90 + 120 * k
        stand.append(Rot(0, 0, a) * Pos(p["BRICK_R"], 0, z0 + p["OUT_T"] + p["STANDOFF"] / 2) * Box(bwr, bwl, p["STANDOFF"]))
    add("bricks", "Firebrick standoffs (3)", _fuse(stand), 4, "bought")

    # 3 inner retort: shell, floor with gas holes, slot for the core probe, bolt-ring lid, U-bolt handles
    retort = _shell(rr, rr - p["RET_T"], p["RET_H"], z_ret) + _zcyl(rr, p["RET_T"], z_ret)
    for k in range(p["N_GAS_HOLES"]):
        a = 2 * math.pi * k / p["N_GAS_HOLES"]
        retort = retort - _zcyl(p["GAS_HOLE_D"] / 2, 10, z_ret - 5,
                                p["GAS_HOLE_PCD"] / 2 * math.cos(a), p["GAS_HOLE_PCD"] / 2 * math.sin(a))
    sw, sh = p["PROBE_SLOT"]
    retort = retort - _bx(-sw / 2, sw / 2, rr - 10, rr + 10, zc - sh / 2, zc + sh / 2)
    add("retort", "Retort drum, cut", retort, 3, "drum")
    rlid = _zcyl(rr + 10, 1.5, z_rt) + _shell(rr + 10, rr + 0.5, 14, z_rt - 12.5)
    ub = []
    for sx in (-1, 1):
        x = sx * 130
        for sy in (-1, 1):
            rlid = rlid - _zcyl(4.5, 10, z_rt - 5, x, sy * 40)
            ub.append(_zcyl(4, 40, z_rt - 8, x, sy * 40))                      # U-bolt legs through the lid
            ub.append(_hexnut((x, sy * 40, z_rt - 7), (x, sy * 40, z_rt), 13))  # nut under the lid
        ub.append(_tube((x, -44, z_rt + 32), (x, 44, z_rt + 32), 4))          # U-bolt grip
    add("rlid", "Retort lid and bolt ring", rlid, 3, "drum")
    add("handles", "U-bolt handles (2)", _fuse(ub), 3, "bought")

    # 2 outer lid (the drum's own) with a 150 mm hole, and the collar riveted to it by six tabs
    lid = _zcyl(ro + 6, p["LID_T"], z_lid) - _zcyl(p["LID_HOLE_D"] / 2, 10, z_lid - 5)
    add("lid", "Outer lid, cut", lid, 2, "drum")
    ct = p["COLLAR_T"]
    collar = _shell(rf + ct, rf, p["COLLAR_H"], z_thr)
    for k in range(6):
        collar = collar + Rot(0, 0, 60 * k) * _bx(rf + ct / 2, rf + 20, -7.5, 7.5, z_thr, z_thr + ct)
    add("collar", "Throat collar", collar, 2, "made")

    # 6 burner throat: stands on the lid inside the collar; two rings of air holes; throat probe hole
    throat = _shell(rf, rf - p["FLUE_T"], p["THROAT_H"], z_thr)
    per_ring = p["N_AIR_HOLES"] // p["AIR_RINGS"]
    zs = z_thr + p["SHROUD_Z"]
    for ring in range(p["AIR_RINGS"]):
        zh = zs + 55 + 40 * ring
        for k in range(per_ring):
            a = 2 * math.pi * (k + 0.5 * ring) / per_ring
            throat = throat - _tube((0, 0, zh), (1.2 * rf * math.cos(a), 1.2 * rf * math.sin(a), zh), p["AIR_HOLE_D"] / 2)
    throat = throat - _tube((0, rf - 10, ztp), (0, rf + 10, ztp), 4.0)
    add("throat", "Burner throat", throat, 6, "made")

    # 5 secondary air shroud: sleeve and top ring, riveted to the throat by six tabs; sliding band damper
    st = p["SHROUD_T"]
    H = p["SHROUD_H"]
    shroud = _shell(rs, rs - st, H, zs) + (_zcyl(rs, st, zs + H) - _zcyl(rf, 10, zs + H - 4))
    for k in range(6):
        shroud = shroud + Rot(0, 0, 30 + 60 * k) * _bx(rf, rf + st, -7.5, 7.5, zs + H + st, zs + H + st + 20)
    add("shroud", "Air shroud", shroud, 5, "made")
    add("band", "Shroud band damper", _shell(rs + p["BAND_T"], rs, p["BAND_H"], zs), 5, "made")

    # 8 water jacket: shell, bottom ring and sleeve, welded; three fins welded on; tap socket
    jacket = (_shell(rj, rj - p["JKT_T"], p["JKT_H"], z_jkt)
              + (_zcyl(rj, p["JKT_T"], z_jkt) - _zcyl(rsl, 10, z_jkt - 5))
              + _shell(rsl, rsl - p["SLEEVE_T"], p["JKT_H"] + 2 * p["SOCKET"], z_jkt - p["SOCKET"]))
    legs = _leg_local(p)
    jacket = jacket - _tube((rj - 5, 0, z_jkt + 40), (rj + 5, 0, z_jkt + 40), 8)
    add("jacket", "Water jacket", jacket, 8, "made")
    add("fins", "Jacket fins (3)", _fuse([Rot(0, 0, a) * legs["fin"] for a in p["LEG_ANGLES"]]), 8, "made")
    # loose lid with three locating tabs inside the rim and a 3/4 in vent nipple held by two locknuts
    jl = _zcyl(rj, 1.5, z_jtop) - _zcyl(p["JLID_HOLE_D"] / 2, 10, z_jtop - 5)
    for k in range(3):
        jl = jl + Rot(0, 0, 60 + 120 * k) * _bx(rj - p["JKT_T"] - 2.0, rj - p["JKT_T"] - 0.5, -10, 10, z_jtop - 15, z_jtop)
    vr = p["VENT_R"]
    jl = jl - _zcyl(p["VENT_D"] / 2, 10, z_jtop - 5, 0, vr)
    add("jlid", "Jacket loose lid", jl, 8, "made")
    vent = _zcyl(p["VENT_D"] / 2, 80, z_jtop - 15, 0, vr) - _zcyl(p["VENT_D"] / 2 - 2.9, 90, z_jtop - 20, 0, vr)
    vent = vent + (_hexnut((0, vr, z_jtop + 1.5), (0, vr, z_jtop + 9.5), 36) - _zcyl(p["VENT_D"] / 2, 20, z_jtop, 0, vr))
    vent = vent + (_hexnut((0, vr, z_jtop - 8), (0, vr, z_jtop), 36) - _zcyl(p["VENT_D"] / 2, 20, z_jtop - 10, 0, vr))
    add("vent", "Vent nipple and locknuts", vent, 8, "bought")

    # 9 draw-off tap
    tap = (_tube((rj, 0, z_jkt + 40), (rj + 110, 0, z_jkt + 40), 10.5)
           + Pos(rj + 125, 0, z_jkt + 40) * Box(40, 36, 36)
           + _tube((rj + 125, 0, z_jkt + 58), (rj + 125, 0, z_jkt + 100), 5)
           + Pos(rj + 125, 0, z_jkt + 100) * Box(18, 90, 8))
    add("tap", "Draw-off tap", tap, 9, "bought")

    # 7 flue: 650 mm pipe, foot inside the sleeve socket, resting on the sleeve rim on three angle clips;
    #   rain cap on three flat-bar legs riveted to the pipe
    z_out, z_cap = L["z_out"], L["z_cap"]
    flue = _shell(rf, rf - p["FLUE_T"], p["FLUE_ABOVE"], z_jtop)
    zrod = z_jtop + p["ROD_Z"]
    a_top = _baffle_angle(p, z_jtop + p["ROD_Z"] + 10)
    nrm = (-math.sin(math.radians(a_top)), math.cos(math.radians(a_top)))
    rod_hole = _tube((-90 * nrm[0], -90 * nrm[1], zrod + 0.5), (90 * nrm[0], 90 * nrm[1], zrod + 0.5), p["ROD_D"] / 2 + 0.5)
    flue = flue - rod_hole
    add("flue", "Flue pipe", flue, 7, "made")
    clips = []
    zr = z_jtop + p["SOCKET"]
    for k in range(3):
        clips.append(Rot(0, 0, 15 + 120 * k) * (_bx(rf, rf + 3, -10, 10, zr, zr + 20) + _bx(rf, rf + 20, -10, 10, zr, zr + 3)))
    add("clips", "Flue stop clips (3)", _fuse(clips), 7, "made")
    cap_legs = []
    for k in range(3):
        cap_legs.append(Rot(0, 0, 75 + 120 * k) * (_bx(rf, rf + 3, -10, 10, z_out - 60, z_cap - 1.5)
                                                   + _bx(rf, rf + 30, -10, 10, z_cap - 4.5, z_cap - 1.5)))
    add("cap_legs", "Rain cap legs (3)", _fuse(cap_legs), 7, "made")
    add("cap", "Rain cap", Pos(0, 0, z_cap) * Box(p["CAP_D"], p["CAP_D"], 3), 7, "made")

    # 15 spiral baffle: twisted strip hung on a 10 mm rod through the flue foot
    zb0 = z_jkt + 10
    ztop_b = zrod + 10
    hb = ztop_b - zb0
    n = p["BAFFLE_SEGS"]
    dz = hb / n
    segs = []
    for k in range(n):
        ang = _baffle_angle(p, zb0 + (k + 0.5) * dz)
        segs.append(Pos(0, 0, zb0 + (k + 0.5) * dz) * Rot(0, 0, ang) * Box(p["BAFFLE_W"], p["BAFFLE_T"], dz + 0.5))
    baffle = _fuse(segs) - _tube((-20 * nrm[0], -20 * nrm[1], zrod - 0.5), (20 * nrm[0], 20 * nrm[1], zrod - 0.5), p["ROD_D"] / 2 + 0.5)
    add("baffle", "Spiral baffle strip", baffle, 15, "made")
    rl = p["ROD_L"] / 2
    add("rod", "Baffle hanger rod", _tube((-rl * nrm[0], -rl * nrm[1], zrod), (rl * nrm[0], rl * nrm[1], zrod), p["ROD_D"] / 2), 15, "made")

    # 10 tripod: legs, foot cleats and pads (fins are part of the jacket)
    for name, key, bom in (("Tripod legs (3)", "leg", 10), ("Foot cleats (3)", "cleat", 10), ("Foot pads (3)", "pad", 10),
                           ("Tripod bolts", "bolts", 14)):
        add(f"tri_{key}", name, _fuse([Rot(0, 0, a) * legs[key] for a in p["LEG_ANGLES"]]), bom, "fixing" if bom == 14 else "made")

    # 11 drum blanket, air ports and dampers left clear, slit for the core probe
    zi = z0 + p["INS_BOTTOM"]
    ins = _shell(ro + p["INS_T"], ro, p["OUT_H"] - p["INS_BOTTOM"] - p["INS_TOP_GAP"], zi)
    ins = ins - _tube((0, ro - 5, zc), (0, ro + p["INS_T"] + 5, zc), 10.0)
    add("blanket", "Drum blanket", ins, 11, "bought")

    # 16 jacket shell blanket
    tj = p["JKT_INS_T"]
    add("jblanket", "Jacket blanket", _shell(rj + tj, rj, p["JKT_H"] - 60, z_jkt + 60), 16, "bought")

    # 17 lid and top band blanket
    ti = p["LID_INS_T"]
    lidins = (_zcyl(ro + p["INS_T"], ti, z_thr) - _zcyl(rs + 25, ti + 2, z_thr - 1))
    skirt = p["INS_TOP_GAP"] + p["LID_T"]
    lidins = lidins + _shell(ro + p["INS_T"], ro + 6, skirt, z_thr - skirt)
    add("lblanket", "Lid blanket", lidins, 17, "bought")

    # 13 logger and probes: core probe through the drum and the retort slot; throat probe through the throat
    cp = _tube((0, 0, zc), (0, p["CORE_PROBE_L"], zc), 3) + _tube((0, p["CORE_PROBE_L"], zc), (0, p["CORE_PROBE_L"] + 50, zc), 8)
    tp = _tube((0, 0, ztp), (0, p["THROAT_PROBE_L"], ztp), 3) + _tube((0, p["THROAT_PROBE_L"], ztp), (0, p["THROAT_PROBE_L"] + 50, ztp), 8)
    add("probes", "Thermocouple probes (2)", cp + tp, 13, "bought")
    T = tripod_geometry(p)
    a0 = p["LEG_ANGLES"][0]
    s_l = p["LOGGER_Z"] / T["d"][1]
    lx, lzz = T["pt"](s_l)
    fh = p["FIN"][4] / 2
    box_local = Plane(origin=(lx, fh - 30, lzz), x_dir=(T["n"][0], 0, T["n"][1]), z_dir=(T["d"][0], 0, T["d"][1])) * Box(90, 60, 130)
    add("logger", "Logger box", Rot(0, 0, a0) * box_local, 13, "bought")
    return C


def _baffle_angle(p, z):
    L = levels(p)
    return 180.0 * (z - (L["z_jkt"] + 10)) / p["BAFFLE_PITCH"]


PART_KEYS = {   # BOM line: component keys
    1: ("drum", "dampers", "guides"), 2: ("lid", "collar"), 3: ("retort", "rlid", "handles"), 4: ("bricks",),
    5: ("shroud", "band"), 6: ("throat",), 7: ("flue", "clips", "cap_legs", "cap"), 8: ("jacket", "fins", "jlid", "vent"),
    9: ("tap",), 10: ("tri_leg", "tri_cleat", "tri_pad"), 11: ("blanket",), 12: ("blocks", "pan"),
    13: ("probes", "logger"), 15: ("baffle", "rod"), 16: ("jblanket",), 17: ("lblanket",),
}
NAMES = {
    1: "Outer drum, 200 L (firebox shell)", 2: "Outer lid with flue collar", 3: "Inner retort, 114 L, bolt-ring lid",
    4: "Firebrick standoffs (3)", 5: "Secondary air shroud and damper", 6: "Burner throat (afterburner)",
    7: "Flue pipe with rain cap", 8: "Water jacket, about 60 L, open-vented", 9: "Draw-off tap",
    10: "Jacket support tripod", 11: "Insulation blanket", 12: "Plinth: blocks and ash pan",
    13: "Thermocouple logger and probes", 15: "Spiral baffle insert", 16: "Jacket shell blanket",
    17: "Lid and top band blanket",
}


def build_parts(p=PARAMS, C=None):
    """Return {bom_no: (name, shape)} for the modelled BOM lines (item 14, hardware, is not included)."""
    C = C or build_components(p)
    return {k: (NAMES[k], _fuse([C[c].shape for c in keys])) for k, keys in PART_KEYS.items()}


UNITS = {
    "charcube-kiln": (1, 2, 3, 4, 5, 6, 11, 17),        # drums, lid, throat, shroud, bricks, blankets
    "charcube-heat-recovery-unit": (7, 8, 9, 10, 15, 16),  # lifted aside as one unit for loading
    "charcube-retort": (3,),
}


def assembly(parts=None):
    parts = parts or build_parts()
    return Compound([parts[k][1] for k in sorted(parts)])


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    """Overlap volume, solid by solid (a boolean on a whole compound is not reliable)."""
    tot = 0.0
    try:
        for sa in a.solids():
            for sb in b_.solids():
                ba, bb = sa.bounding_box(), sb.bounding_box()
                if (ba.max.X < bb.min.X or bb.max.X < ba.min.X or ba.max.Y < bb.min.Y or bb.max.Y < ba.min.Y
                        or ba.max.Z < bb.min.Z or bb.max.Z < ba.min.Z):
                    continue
                s = sa & sb
                tot += s.volume if s is not None else 0.0
        return tot
    except Exception:
        return float("nan")


def checks(p=PARAMS, C=None):
    """Pairs that must touch, and pairs that must stay apart by a clearance (mm).
    Returns a list of (description, overlap mm3, gap mm, expectation, ok)."""
    C = C or build_components(p)
    S = lambda *ks: _fuse([C[k].shape for k in ks])   # noqa: E731
    L = levels(p)
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1.0 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    bl, bw = p["BLOCK"]
    q, m, h = (bl + bw) / 2, (bl - bw) / 2, p["BASE_H"]
    blocks = [_bx(-q, m, m, q, 0, h), _bx(m, q, -m, q, 0, h), _bx(-m, q, -q, -m, 0, h), _bx(-q, -m, -q, m, 0, h)]
    for i in range(4):
        chk(f"Block {i + 1} beside block {(i + 1) % 4 + 1} (no overlap)", blocks[i], blocks[(i + 1) % 4], "touch")
    chk("Ash pan on the blocks", S("pan"), S("blocks"), "touch")
    chk("Outer drum on the ash pan", S("drum"), S("pan"), "touch")
    chk("Bricks on the drum floor", S("bricks"), S("drum"), "touch")
    chk("Retort on the bricks", S("retort"), S("bricks"), "touch")
    holes = _fuse([_zcyl(p["GAS_HOLE_D"] / 2, p["STANDOFF"], L["z0"] + p["OUT_T"],
                         p["GAS_HOLE_PCD"] / 2 * math.cos(2 * math.pi * k / p["N_GAS_HOLES"]),
                         p["GAS_HOLE_PCD"] / 2 * math.sin(2 * math.pi * k / p["N_GAS_HOLES"])) for k in range(p["N_GAS_HOLES"])])
    chk("Bricks clear of the space under every gas hole", S("bricks"), holes, 5.0)
    chk("Retort clear of the outer drum (annulus)", S("retort", "rlid"), S("drum"), 40.0)
    chk("Retort lid on the retort", S("rlid"), S("retort"), "touch")
    chk("U-bolt handles on the retort lid", S("handles"), S("rlid"), "touch")
    chk("Handles clear of the outer lid", S("handles"), S("lid"), 8.0)
    chk("Outer lid on the drum rim", S("lid"), S("drum"), "touch")
    chk("Collar on the lid", S("collar"), S("lid"), "touch")
    chk("Throat standing on the lid (round the 150 mm hole)", S("throat"), S("lid"), "touch")
    chk("Throat inside the collar", S("throat"), S("collar"), "touch")
    chk("Shroud riveted to the throat", S("shroud"), S("throat"), "touch")
    chk("Shroud clear of the lid (air intake)", S("shroud"), S("lid"), 35.0)
    chk("Shroud clear of the collar", S("shroud"), S("collar"), 5.0)
    chk("Band damper on the shroud", S("band"), S("shroud"), "touch")
    chk("Band damper clear of the lid when open", S("band"), S("lid"), 35.0)
    chk("Lid blanket on the lid", S("lblanket"), S("lid"), "touch")
    chk("Lid blanket clear of the shroud and band", S("lblanket"), S("shroud", "band"), 15.0)
    chk("Drum blanket on the drum", S("blanket"), S("drum"), "touch")
    chk("Drum blanket clear of the dampers and guides", S("blanket"), S("dampers", "guides"), 0.0)
    chk("Dampers on the drum", S("dampers"), S("drum"), "touch")
    chk("Damper guides riveted to the drum", S("guides"), S("drum"), "touch")
    chk("Dampers held by the guides", S("dampers"), S("guides"), "touch")
    chk("Dampers clear of the ash pan", S("dampers", "guides"), S("pan"), 3.0)
    chk("Jacket sleeve clear round the throat (slip joint)", S("jacket"), S("throat"), 1.5)
    chk("Jacket clear of the shroud", S("jacket"), S("shroud", "band"), 100.0)
    chk("Jacket blanket on the jacket", S("jblanket"), S("jacket"), "touch")
    chk("Tap in the jacket socket", S("tap"), S("jacket"), "touch")
    chk("Tap clear of the jacket blanket", S("tap"), S("jblanket"), 5.0)
    chk("Fins welded to the jacket shell", S("fins"), S("jacket"), "touch")
    chk("Fins clear of the jacket blanket", S("fins"), S("jblanket"), 0.0)
    chk("Legs bolted flat to the jacket fins", S("tri_leg"), S("fins"), "touch")
    chk("Legs clear of the jacket shell", S("tri_leg"), S("jacket"), 5.0)
    chk("Legs bolted flat to the foot cleats", S("tri_leg"), S("tri_cleat"), "touch")
    chk("Cleats bolted to the foot pads", S("tri_cleat"), S("tri_pad"), "touch")
    chk("Legs clear of the foot pads", S("tri_leg"), S("tri_pad"), 3.0)
    chk("Legs clear of the jacket blanket", S("tri_leg"), S("jblanket"), 3.0)
    chk("Legs clear of the drum blanket and lid blanket", S("tri_leg"), S("blanket", "lblanket"), 30.0)
    chk("Legs clear of the ash pan and blocks", S("tri_leg"), S("pan", "blocks"), 30.0)
    chk("Legs clear of the tap", S("tri_leg"), S("tap"), 30.0)
    chk("Legs clear of the throat probe", S("tri_leg"), S("probes"), 30.0)
    chk("Flue clips resting on the sleeve rim", S("clips"), S("jacket"), "touch")
    chk("Flue clips riveted to the flue", S("clips"), S("flue"), "touch")
    chk("Flue clear inside the sleeve socket", S("flue"), S("jacket"), 1.5)
    chk("Jacket lid on the shell rim", S("jlid"), S("jacket"), "touch")
    chk("Jacket lid clear of the flue clips", S("jlid"), S("clips"), 3.0)
    chk("Jacket lid clear of the flue", S("jlid"), S("flue"), 20.0)
    chk("Vent nipple in the jacket lid", S("vent"), S("jlid"), "touch")
    chk("Vent nipple clear of the jacket", S("vent"), S("jacket"), 10.0)
    chk("Cap legs riveted to the flue", S("cap_legs"), S("flue"), "touch")
    chk("Rain cap on its legs", S("cap"), S("cap_legs"), "touch")
    chk("Rain cap clear above the flue outlet", S("cap"), S("flue"), p["CAP_GAP"] - 2)
    chk("Baffle strip clear of the sleeve and flue", S("baffle"), S("jacket", "flue"), 2.0)
    chk("Baffle strip clear of the throat", S("baffle"), S("throat"), 5.0)
    chk("Baffle strip hangs on the rod", S("baffle"), S("rod"), "touch")
    chk("Rod rests in the flue holes", S("rod"), S("flue"), "touch")
    chk("Rod clear of the sleeve", S("rod"), S("jacket"), 0.5)
    chk("Probes clear of the drum, retort and throat (through holes)", S("probes"), S("drum", "retort", "throat"), 0.9)
    chk("Probes clear of the blankets", S("probes"), S("blanket", "lblanket", "jblanket"), 3.0)
    chk("Probes clear of the sleeve and shroud", S("probes"), S("jacket", "shroud", "band"), 10.0)
    chk("Logger strapped to the leg", S("logger"), S("tri_leg"), "touch")
    chk("Logger clear of the drum blanket", S("logger"), S("blanket"), 50.0)
    return rows


def print_checks(p=PARAMS, C=None):
    rows = checks(p, C)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:9.1f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    C = build_components()
    if "--check" in sys.argv:
        sys.exit(1 if print_checks(C=C) else 0)
    parts = build_parts(C=C)
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    asm = assembly(parts)
    shapes = {"charcube-assembly": asm}
    for name, keys in UNITS.items():
        shapes[name] = Compound([parts[k][1] for k in keys])
    for name, shp in shapes.items():
        export_step(shp, str(root / "step" / f"{name}.step"))
        export_stl(shp, str(root / "stl" / f"{name}.stl"))
    bb = asm.bounding_box()
    L = levels()
    T = tripod_geometry()
    print(f"assembly bounding box: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    for k, v in L.items():
        print(f"  {k:10s} {v:7.0f} mm")
    print(f"tripod leg: {T['len']:.0f} mm long, {T['tilt_deg']:.1f} deg from vertical; upper bolts at r {T['b1'][0]:.0f} "
          f"and {T['b2'][0]:.0f} mm, {T['b1'][1] - L['z_jkt']:.0f} and {T['b2'][1] - L['z_jkt']:.0f} mm from the jacket underside")
    for k in sorted(parts):
        print(f"  item {k:2d}  {parts[k][0]:40s} volume {parts[k][1].volume / 1e6:7.3f} L")
    print("wrote cad/step/*.step and cad/stl/*.stl")
    print_checks(C=C)
