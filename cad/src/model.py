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
import os
import sys
import time
from pathlib import Path

from build123d import (Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, Solid, Vector, export_step,
                       export_stl, extrude)

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 12 plinth: four concrete blocks laid as a pinwheel (580 mm square, 200 mm hole) and a steel ash pan
    "BASE_H": 190.0, "BLOCK": (390.0, 190.0), "PAN": (760.0, 600.0), "PAN_T": 3.0,
    # 12 ceramic fibre board between the blocks and the pan (decided 2026-10-02, CCB-DDR-003 A2): 600 x 600 x 25
    "BOARD": (600.0, 600.0, 25.0),
    # 13 block thermocouple: bare-wire type K in a groove cut in the board's underside, tip on the back block
    "BLOCK_TC_D": 3.0, "BLOCK_TC_TIP": (-50.0, 150.0), "BLOCK_TC_L": 270.0, "TC_GROOVE": (4.0, 3.5),
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
    "SLEEVE_FLARE": (20.0, 190.0),                           # bottom 20 mm of the sleeve flared to 190 mm (decided 2026-10-02, A3)
    "JLID_HOLE_D": 210.0, "VENT_D": 26.7, "VENT_R": 170.0,   # loose lid: hole round the sleeve; 3/4 in vent nipple
    "FIN": (210.0, 295.0, -80.0, 60.0, 6.0),                 # welded fins: r from, r to, z from, z to (from jacket underside), thickness
    # 7 flue above the jacket
    "FLUE_ABOVE": 650.0, "CAP_D": 260.0, "CAP_GAP": 60.0,    # flue pipe 650 long: its foot 50 mm inside the sleeve socket
    "CAP_SLOPE": 30.0, "CAP_T": 1.5,                          # conical cap (decided 2026-10-02): 30 deg, 1.5 mm; CAP_GAP is the
                                                              #   shortest gap from the flue lip to the cap's underside
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
    # 14 hot-surface labels (ISO 7010 W017, decided 2026-10-02): 100 mm aluminium triangles wired on, front right
    "LABEL_S": 100.0, "LABEL_ANG": -40.0, "LABEL_DZ": (300.0, 220.0),   # above the blanket bottom; above the jacket underside
    # 18 lifting aid (decided 2026-10-02): a post that turns in a ground sleeve, a bolted arm and brace, a hand winch;
    #   lifts the drained heat-recovery unit by a bar through the sleeve socket and swings it clear of the kiln
    "POST": (88.9, 3.2), "POST_R": 1200.0, "POST_ANG": 90.0, "ARM_PARK": 180.0,   # post at the back; arm parked to the left
    "GSLEEVE": (101.6, 3.6, 700.0), "FOOTING": (600.0, 750.0),
    "ARM_ANG": (50.0, 5.0), "ARM_L": 1300.0, "ARM_TAIL": 200.0,                    # two 50 x 50 x 5 angles either side of the post
    "BRACE_DZ": 700.0, "BRACE_X": 700.0, "PULLEY_D": 100.0, "PULLEY_W": 20.0,
    "LIFT": 1550.0, "HOOK_DROP": 300.0,          # hook travel; lift bar to the arm's underside at full lift
    "LIFT_BAR": (16.0, 230.0), "LIFT_HOLE_DZ": 35.0, "WINCH_Z": 1000.0,
}
P = PARAMS
VERBOSE = bool(os.environ.get("CCB_VERBOSE"))
T0 = time.time()


def levels(p=PARAMS):
    """Key heights (mm above ground) derived from the parameters."""
    z0 = p["BASE_H"] + p["BOARD"][2] + p["PAN_T"]    # outer drum floor (blocks, fibre board, pan)
    z_lid = z0 + p["OUT_H"]                          # outer lid underside
    z_thr = z_lid + p["LID_T"]                       # throat base (lid top)
    z_jkt = z_thr + p["THROAT_H"]                    # jacket underside
    z_jtop = z_jkt + p["JKT_H"]
    z_out = z_jtop + p["FLUE_ABOVE"]                 # flue outlet (flue foot at z_jtop, inside the sleeve socket)
    z_ret = z0 + p["OUT_T"] + p["STANDOFF"]          # retort underside
    return {"z0": z0, "z_lid": z_lid, "z_thr": z_thr, "z_jkt": z_jkt, "z_jtop": z_jtop,
            "z_out": z_out, "z_cap": z_out + cap_geometry(p)["rim"], "z_ret": z_ret,
            "z_ret_top": z_ret + p["RET_H"], "z_ports": z0 + p["PORT_Z"] + p["PORT_H"] / 2,
            "z_core": z_ret + p["FILL_H"] / 2, "z_tprobe": z_jkt - p["THROAT_PROBE_DZ"],
            "z_cap_top": z_out + cap_geometry(p)["apex"], "z_lp": z_jtop + p["LIFT_HOLE_DZ"],
            "z_arm": z_jtop + p["LIFT_HOLE_DZ"] + p["LIFT"] + p["HOOK_DROP"]}


def cap_geometry(p=PARAMS):
    """Conical rain cap, heights above the flue outlet (mm): underside at radius r is rim + (R - r) tan(slope).
    The rim is set so the shortest gap from the flue lip (r = FLUE_D / 2) to the underside is CAP_GAP."""
    t = math.tan(math.radians(p["CAP_SLOPE"]))
    R, rf = p["CAP_D"] / 2, p["FLUE_D"] / 2
    under_rf = p["CAP_GAP"] / math.cos(math.radians(p["CAP_SLOPE"]))
    rim = under_rf - (R - rf) * t
    under = lambda r: rim + (R - r) * t   # noqa: E731
    dt = p["CAP_T"] / math.cos(math.radians(p["CAP_SLOPE"]))
    return {"rim": rim, "under": under, "apex": rim + R * t + dt, "h": R * t, "dt": dt,
            "slant": R / math.cos(math.radians(p["CAP_SLOPE"]))}


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
    # ceramic fibre board on the blocks, a groove in its underside for the block thermocouple
    fbw, fbd, fbt = p["BOARD"]
    gw, gd = p["TC_GROOVE"]
    tx, ty = p["BLOCK_TC_TIP"]
    board = _bx(-fbw / 2, fbw / 2, -fbd / 2, fbd / 2, h, h + fbt) - _bx(tx - gw / 2, tx + gw / 2, ty - 5, fbd, h - 1, h + gd)
    add("board", "Ceramic fibre board", board, 12, "bought")
    hp = h + fbt
    pw, pd = p["PAN"]
    add("pan", "Ash pan", _bx(-pw / 2, pw / 2, -pd / 2, pd / 2, hp, hp + p["PAN_T"]), 12, "made")
    rt = p["BLOCK_TC_D"] / 2
    add("btc", "Block thermocouple", _tube((tx, ty, h + rt), (tx, ty + p["BLOCK_TC_L"], h + rt), rt), 13, "bought")

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
    fl_h, fl_d = p["SLEEVE_FLARE"]
    zfl = z_jkt - p["SOCKET"]
    st_ = p["SLEEVE_T"]
    flare = (Solid.make_cone(fl_d / 2, rsl, fl_h, Plane(origin=(0, 0, zfl)))
             - Solid.make_cone(fl_d / 2 - st_, rsl - st_, fl_h, Plane(origin=(0, 0, zfl)))
             - _zcyl(rsl - st_, fl_h + 2, zfl - 1))
    jacket = (_shell(rj, rj - p["JKT_T"], p["JKT_H"], z_jkt)
              + (_zcyl(rj, p["JKT_T"], z_jkt) - _zcyl(rsl, 10, z_jkt - 5))
              + _shell(rsl, rsl - st_, p["JKT_H"] + 2 * p["SOCKET"] - fl_h, zfl + fl_h) + flare)
    lb_dir = lift_bar_dir(p)
    zlp = L["z_lp"]
    jacket = jacket - _tube((-100 * lb_dir[0], -100 * lb_dir[1], zlp), (100 * lb_dir[0], 100 * lb_dir[1], zlp), p["LIFT_BAR"][0] / 2 + 1)
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
    cg = cap_geometry(p)
    z_tab = z_out + cg["under"](rf + 30)            # foot top, touching the cap's underside at its outer end
    cap_legs = []
    for k in range(3):
        cap_legs.append(Rot(0, 0, 75 + 120 * k) * (_bx(rf, rf + 3, -10, 10, z_out - 60, z_tab)
                                                   + _bx(rf, rf + 30, -10, 10, z_tab - 3, z_tab)))
    add("cap_legs", "Rain cap legs (3)", _fuse(cap_legs), 7, "made")
    R_ = p["CAP_D"] / 2
    zr_ = z_out + cg["rim"]
    cone_in = Solid.make_cone(R_, 0, cg["h"], Plane(origin=(0, 0, zr_)))
    cone_out = Solid.make_cone(R_, 0, cg["h"], Plane(origin=(0, 0, zr_ + cg["dt"])))
    add("cap", "Conical rain cap", cone_out - cone_in, 7, "made")

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

    # 14 hot-surface labels (ISO 7010 W017): flat 1 mm triangles wired to the blanket mesh, front right
    S_ = p["LABEL_S"]
    tri = [(-S_ / 2, -S_ * math.sqrt(3) / 6), (S_ / 2, -S_ * math.sqrt(3) / 6), (0, S_ * math.sqrt(3) / 3)]
    plate = extrude(Plane.XZ * Polygon(*tri, align=None), amount=1.0)          # y from -1 to 0
    labs = []
    for r_, zc_ in ((ro + p["INS_T"], z0 + p["INS_BOTTOM"] + p["LABEL_DZ"][0]), (rj + p["JKT_INS_T"], z_jkt + p["LABEL_DZ"][1])):
        labs.append(Rot(0, 0, p["LABEL_ANG"] + 90) * Pos(0, -r_, zc_) * plate)
    add("labels", "Hot-surface labels (2)", _fuse(labs), 14, "bought")

    # 18 lifting aid, parked (arm swung clear of the kiln); built in its own frame, arm along +X
    for key, (name, shape) in lifting_aid_local(p).items():
        add(key, name, aid_place(p, shape), 18, "fixing" if key == "aid_bolts" else ("bought" if key in ("winch", "rope", "hook") else "made"))
    return C


def lift_bar_dir(p=PARAMS):
    """Unit vector of the lift bar: square to the baffle hanger rod, so its holes in the sleeve socket miss the rod."""
    L = levels(p)
    a = math.radians(_baffle_angle(p, L["z_jtop"] + p["ROD_Z"] + 10))
    return (math.cos(a), math.sin(a))


def aid_place(p, shape, arm_deg=None, lift=0.0, unit=False):
    """Put a lifting-aid part (built with the post on the origin, arm along +X) at the post, with the arm at arm_deg."""
    a = math.radians(p["POST_ANG"])
    px, py = p["POST_R"] * math.cos(a), p["POST_R"] * math.sin(a)
    return Pos(px, py, lift) * Rot(0, 0, p["ARM_PARK"] if arm_deg is None else arm_deg) * shape


def swing_unit(p, shape, swing_deg, lift):
    """A heat-recovery-unit part raised by lift and swung about the post by swing_deg (0: over the kiln).
    The unit turns with the arm."""
    a = math.radians(p["POST_ANG"])
    px, py = p["POST_R"] * math.cos(a), p["POST_R"] * math.sin(a)
    return Pos(px, py, lift) * Rot(0, 0, swing_deg) * Pos(-px, -py, 0) * shape


def lifting_aid_local(p=PARAMS):
    """The lifting aid with the post axis on the origin and the arm along +X. Returns {key: (name, shape)}."""
    L = levels(p)
    za = L["z_arm"]
    rpo, tpo = p["POST"][0] / 2, p["POST"][1]
    gd, gt, gl = p["GSLEEVE"]
    rg = gd / 2
    fw, fd = p["FOOTING"]
    ab, at = p["ARM_ANG"]
    tail, al = p["ARM_TAIL"], p["ARM_L"]
    rp = p["PULLEY_D"] / 2
    zax = za + ab / 2                                  # axle and bolt line, mid-height of the arm angles
    z_bp = zax - p["BRACE_DZ"]                         # brace bolt through the post
    xb = p["BRACE_X"]
    x_tip = p["POST_R"] - rp - 2.5                     # tip pulley: the rope hangs at POST_R from the post
    x_back = -100.0
    z_ptop = za + 37.0
    out = {}
    footing = _bx(-fw / 2, fw / 2, -fw / 2, fw / 2, -fd, 0) - _zcyl(rg, gl, -gl)
    out["footing"] = ("Lifting aid footing, concrete", footing)
    out["gsleeve"] = ("Lifting aid ground sleeve", _shell(rg, rg - gt, gl + 30, -gl) + _zcyl(rg - gt, 6, -gl))
    post = _shell(rpo, rpo - tpo, z_ptop - (-gl + 6), -gl + 6) + _zcyl(rpo, 3, z_ptop)
    holes = [_tube((0, -60, za + 20), (0, 60, za + 20), 8.5), _tube((0, -60, z_bp), (0, 60, z_bp), 8.5)]
    post = post - _fuse(holes)
    out["post"] = ("Lifting aid post", post)
    arm, brace, bolts, pulleys = [], [], [], []
    ax_holes = [_tube((x, -80, z), (x, 80, z), 6.5) for x, z in ((x_tip, zax), (x_back, zax), (xb, zax))]
    for sy in (-1, 1):
        y0, y1 = sorted((sy * rpo, sy * (rpo + at)))
        h0, h1 = sorted((sy * rpo, sy * (rpo + ab)))
        a_ = _bx(-tail, al, y0, y1, za, za + ab) + _bx(-tail, al, h0, h1, za + ab - at, za + ab)
        arm.append(a_ - holes[0] - _fuse(ax_holes))
        # brace: 40 x 40 x 4 angle, flat leg on the arm's vertical leg and on a 5 mm packing plate at the post
        b0, b1 = sorted((sy * (rpo + at), sy * (rpo + at + 4)))
        o0, o1 = sorted((sy * (rpo + at), sy * (rpo + at + 40)))
        dx, dz = xb, zax - z_bp
        ln = math.hypot(dx, dz)
        d = (dx / ln, dz / ln)
        n = (d[1], -d[0])
        pt = lambda s_, w_: (s_ * d[0] + w_ * n[0], z_bp + s_ * d[1] + w_ * n[1])   # noqa: E731

        def strip(s0, s1, w0, w1, ya, yb):
            pts = [pt(s0, w0), pt(s1, w0), pt(s1, w1), pt(s0, w1)]
            sol = extrude(Plane.XZ * Polygon(*pts, align=None), amount=yb - ya)
            return Pos(0, ya - sol.bounding_box().min.Y, 0) * sol
        br = strip(-25, ln + 25, -20, 20, b0, b1) + strip(-25, ln + 25, 16, 20, o0, o1)
        br = br & _bx(-30, xb + 60, -200, 200, z_bp - 60, za + ab - at - 1)
        br = br - _fuse([_tube((0, -80, z_bp), (0, 80, z_bp), 8.5), _tube((xb, -80, zax), (xb, 80, zax), 6.5)])
        brace.append(br)
        pk0, pk1 = sorted((sy * rpo, sy * (rpo + at)))
        brace.append(_bx(-25, 25, pk0, pk1, z_bp - 30, z_bp + 30) - holes[1])
        # spacer tubes on the axles and the brace bolt
        for x, z in ((x_tip, zax), (x_back, zax)):
            bolts.append(_tube((x, sy * (p["PULLEY_W"] / 2), z), (x, sy * rpo, z), 9) - _tube((x, -80, z), (x, 80, z), 6.5))
    bolts.append(_tube((xb, -rpo, zax), (xb, rpo, zax), 9) - _tube((xb, -80, zax), (xb, 80, zax), 6.5))
    out["arm"] = ("Lifting aid arm (2 angles)", _fuse(arm))
    out["brace"] = ("Lifting aid brace and packing", _fuse(brace))
    w = rpo + at + 4
    bolts += [_bolt((0, -(rpo + at), za + 20), (0, rpo + at, za + 20), 16, 24),
              _bolt((0, -w, z_bp), (0, w, z_bp), 16, 24), _bolt((xb, -w, zax), (xb, w, zax), 12, 19),
              _bolt((x_tip, -(rpo + at), zax), (x_tip, rpo + at, zax), 12, 19),
              _bolt((x_back, -(rpo + at), zax), (x_back, rpo + at, zax), 12, 19)]
    out["aid_bolts"] = ("Lifting aid bolts, axles and spacers", _fuse(bolts))
    for x in (x_tip, x_back):
        pulleys.append(_tube((x, -p["PULLEY_W"] / 2, zax), (x, p["PULLEY_W"] / 2, zax), rp) - _tube((x, -20, zax), (x, 20, zax), 6.5))
    out["pulleys"] = ("Lifting aid pulleys (2)", _fuse(pulleys))
    zw = p["WINCH_Z"]
    winch = (_bx(-rpo - 120, -rpo, -55, 55, zw, zw + 140) + _tube((-rpo - 60, 55, zw + 70), (-rpo - 60, 125, zw + 70), 6)
             + _tube((-rpo - 60, 125, zw + 70), (-rpo - 60, 125, zw + 150), 10))
    out["winch"] = ("Hand winch, bolted to the post", winch)
    xr_b, xr_t = x_back - rp - 2.5, x_tip + rp + 2.5
    rope = (_tube((xr_b, 0, zw + 140), (xr_b, 0, zax), 2.5) + _tube((x_back, 0, zax + rp + 2.5), (x_tip, 0, zax + rp + 2.5), 2.5)
            + _tube((xr_t, 0, zax), (xr_t, 0, za - 250), 2.5))
    out["rope"] = ("Steel wire rope", rope)
    out["hook"] = ("Hook with safety latch", _bx(xr_t - 10, xr_t + 10, -6, 6, za - 340, za - 250))
    return out


def lift_bar(p=PARAMS):
    """The 12 mm lift bar through the two holes in the sleeve socket (fitted only for lifting, flue out)."""
    L = levels(p)
    d = lift_bar_dir(p)
    hl = p["LIFT_BAR"][1] / 2
    return _tube((-hl * d[0], -hl * d[1], L["z_lp"]), (hl * d[0], hl * d[1], L["z_lp"]), p["LIFT_BAR"][0] / 2)


def _baffle_angle(p, z):
    L = levels(p)
    return 180.0 * (z - (L["z_jkt"] + 10)) / p["BAFFLE_PITCH"]


PART_KEYS = {   # BOM line: component keys
    1: ("drum", "dampers", "guides"), 2: ("lid", "collar"), 3: ("retort", "rlid", "handles"), 4: ("bricks",),
    5: ("shroud", "band"), 6: ("throat",), 7: ("flue", "clips", "cap_legs", "cap"), 8: ("jacket", "fins", "jlid", "vent"),
    9: ("tap",), 10: ("tri_leg", "tri_cleat", "tri_pad"), 11: ("blanket",), 12: ("blocks", "board", "pan"),
    13: ("probes", "btc", "logger"), 14: ("labels",), 15: ("baffle", "rod"), 16: ("jblanket",), 17: ("lblanket",),
    18: ("footing", "gsleeve", "post", "arm", "brace", "aid_bolts", "pulleys", "winch", "rope", "hook"),
}
NAMES = {
    1: "Outer drum, 200 L (firebox shell)", 2: "Outer lid with flue collar", 3: "Inner retort, 114 L, bolt-ring lid",
    4: "Firebrick standoffs (3)", 5: "Secondary air shroud and damper", 6: "Burner throat (afterburner)",
    7: "Flue pipe with rain cap", 8: "Water jacket, about 60 L, open-vented", 9: "Draw-off tap",
    10: "Jacket support tripod", 11: "Insulation blanket", 12: "Plinth: blocks, fibre board and ash pan",
    13: "Thermocouple logger and probes", 14: "Hot-surface labels", 15: "Spiral baffle insert", 16: "Jacket shell blanket",
    17: "Lid and top band blanket", 18: "Lifting aid for the heat-recovery unit",
}


def build_parts(p=PARAMS, C=None):
    """Return {bom_no: (name, shape)} for the modelled BOM lines (of item 14, hardware, only the labels are modelled)."""
    C = C or build_components(p)
    return {k: (NAMES[k], _fuse([C[c].shape for c in keys])) for k, keys in PART_KEYS.items()}


UNITS = {
    "charcube-kiln": (1, 2, 3, 4, 5, 6, 11, 17),        # drums, lid, throat, shroud, bricks, blankets
    "charcube-heat-recovery-unit": (7, 8, 9, 10, 15, 16),  # lifted aside as one unit for loading
    "charcube-retort": (3,),
    "charcube-lifting-aid": (18,),
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
        if VERBOSE:
            print(f"    [{time.time() - T0:6.1f} s] {desc}", flush=True)

    bl, bw = p["BLOCK"]
    q, m, h = (bl + bw) / 2, (bl - bw) / 2, p["BASE_H"]
    blocks = [_bx(-q, m, m, q, 0, h), _bx(m, q, -m, q, 0, h), _bx(-m, q, -q, -m, 0, h), _bx(-q, -m, -q, m, 0, h)]
    for i in range(4):
        chk(f"Block {i + 1} beside block {(i + 1) % 4 + 1} (no overlap)", blocks[i], blocks[(i + 1) % 4], "touch")
    chk("Fibre board on the blocks", S("board"), S("blocks"), "touch")
    chk("Ash pan on the fibre board", S("pan"), S("board"), "touch")
    chk("Ash pan clear of the blocks (board between)", S("pan"), S("blocks"), p["BOARD"][2] - 0.5)
    chk("Block thermocouple on the back block", S("btc"), S("blocks"), "touch")
    chk("Block thermocouple clear in the board groove", S("btc"), S("board"), 0.4)
    chk("Block thermocouple clear of the ash pan", S("btc"), S("pan"), 3.0)
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
    chk("Dampers clear of the fibre board", S("dampers", "guides"), S("board"), 10.0)
    chk("Jacket sleeve clear round the throat (slip joint)", S("jacket"), S("throat"), 1.5)
    fl_h, fl_d = p["SLEEVE_FLARE"]
    flare_zone = _zcyl(fl_d / 2 + 5, fl_h + 2, L["z_jkt"] - p["SOCKET"] - 1)
    chk("Sleeve flare clear of the shroud and band", S("jacket") & flare_zone, S("shroud", "band"), 100.0)
    chk("Sleeve flare clear of the throat probe", S("jacket") & flare_zone, S("probes"), 10.0)
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
    chk("Conical rain cap clear above the flue outlet", S("cap"), S("flue"), p["CAP_GAP"] - 0.5)
    chk("Rain cap clear of the hanger rod and baffle", S("cap"), S("rod", "baffle"), 100.0)
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
    chk("Hot-surface labels on the blankets", S("labels"), S("blanket", "jblanket"), "touch")
    chk("Labels clear of the legs, tap and dampers", S("labels"), S("tri_leg", "tap", "dampers", "guides"), 20.0)
    # lifting aid, parked
    chk("Ground sleeve in the footing", S("gsleeve"), S("footing"), "touch")
    chk("Post standing in the ground sleeve", S("post"), S("gsleeve"), "touch")
    chk("Arm angles on the post", S("arm"), S("post"), "touch")
    chk("Brace on the arm and the post packing", S("brace"), S("arm"), "touch")
    chk("Brace packing on the post", S("brace"), S("post"), "touch")
    chk("Bolts and axles in their holes (no overlap)", S("aid_bolts"),
        Compound(children=[C[k].shape for k in ("post", "arm", "brace")]), 0.0)   # a fused union of these is not reliable
    chk("Pulleys on their axles", S("pulleys"), S("aid_bolts"), "touch")
    chk("Pulleys clear of the arm and the post", S("pulleys"), S("arm", "post"), 3.0)
    chk("Winch bolted to the post", S("winch"), S("post"), "touch")
    chk("Rope over the pulleys", S("rope"), S("pulleys"), "touch")
    chk("Rope clear of the arm, brace and post", S("rope"), S("arm", "brace", "post"), 3.0)
    chk("Hook on the rope", S("hook"), S("rope"), "touch")
    unit_keys = ("jacket", "fins", "jlid", "vent", "tap", "jblanket", "tri_leg", "tri_cleat", "tri_pad", "tri_bolts")
    kiln_keys = ("drum", "dampers", "guides", "blanket", "lid", "collar", "throat", "shroud", "band", "lblanket",
                 "pan", "board", "blocks")
    chk("Post clear of the tripod legs and feet", S("post", "gsleeve", "winch"), S("tri_leg", "tri_cleat", "tri_pad"), 300.0)
    chk("Footing clear of the plinth", S("footing"), S("blocks", "board", "pan"), 300.0)
    chk("Post clear of the drum blanket and probes", S("post", "winch"), S("blanket", "probes", "btc"), 300.0)
    chk("Parked arm clear of the rain cap and flue", S("arm", "brace", "pulleys", "rope", "hook"), S("cap", "flue", "cap_legs"), 300.0)
    # lifting: lift bar in the sleeve socket; hook over the kiln axis; raised unit swung clear of the kiln
    chk("Lift bar through the sleeve socket holes", lift_bar(p), S("jacket"), 0.5)
    off = _rope_offset(p)
    rows.append(("Rope over the kiln axis with the arm toward the kiln (offset)", 0.0, off, "<= 5 mm", off <= 5.0))
    zr = L["z_lp"] + p["LIFT"]
    za = L["z_arm"]
    rows.append(("Hook at full lift below the tip pulley (room, mm)", 0.0, za - p["PULLEY_D"] / 2 - zr, 150.0,
                 za - p["PULLEY_D"] / 2 - zr >= 150.0))
    unit = [C[k].shape for k in unit_keys]
    low = min(sh.bounding_box().min.Z for sh in unit) + p["LIFT"]
    top = max(C[k].shape.bounding_box().max.Z for k in kiln_keys)
    rows.append(("Raised unit's lowest point above the throat top (clear, mm)", 0.0, low - top, 50.0, low - top >= 50.0))
    # The raised unit turns about the post with the arm, so its horizontal distance from the post stays as installed
    # ("Post clear of the tripod legs and feet"); with its lowest point above the throat top it clears the kiln on any
    # path. Where it is set down, its feet stay clear of the plinth by the margin below (bounding radii, conservative).
    def r_max(keys):
        r = 0.0
        for k in keys:
            bb = C[k].shape.bounding_box()
            r = max(r, max(math.hypot(x, y) for x in (bb.min.X, bb.max.X) for y in (bb.min.Y, bb.max.Y)))
        return r
    d_park = 2 * p["POST_R"] * math.sin(math.radians(45.0))          # unit axis moves along a 90 deg arc about the post
    gap_park = d_park - r_max(("tri_pad", "tri_cleat", "tri_leg", "tap")) - r_max(("pan", "blocks", "board", "blanket"))
    rows.append(("Unit set down clear of the plinth and kiln, swung 90 deg (clear, mm)", 0.0, gap_park, 150.0, gap_park >= 150.0))
    return rows


def _rope_offset(p=PARAMS):
    """Horizontal distance (mm) from the kiln axis to the hanging rope with the arm turned toward the kiln."""
    rope = lifting_aid_local(p)["rope"][1]
    a = math.radians(p["POST_ANG"])
    hang = [so for so in rope.solids()] if hasattr(rope, "solids") else [rope]
    best = None
    for so in hang:
        bb = so.bounding_box()
        if bb.size.Z > 100 and bb.min.X > 100:          # the hanging run at the tip
            x_local = (bb.min.X + bb.max.X) / 2
            px, py = p["POST_R"] * math.cos(a), p["POST_R"] * math.sin(a)
            # arm toward the kiln: local +X points from the post to the axis
            d = (-math.cos(a), -math.sin(a))
            best = math.hypot(px + d[0] * x_local, py + d[1] * x_local)
    return best if best is not None else float("nan")


def print_checks(p=PARAMS, C=None):
    rows = checks(p, C)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = exp if isinstance(exp, str) else f">= {exp:g} mm"
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
