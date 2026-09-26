"""CharCube parametric model (build123d), TRL 3 (DDR-002: baffle insert, jacket and lid blankets).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL of the assembly and its three lift units into cad/step and cad/stl.

Massing-plus level of detail: correct interfaces and main dimensions, not
fabrication detail. Coordinates in mm. Z up, ground at Z = 0, kiln axis on
X = Y = 0. Sizes are checked in CCB-CAL-001 (docs/04-calcs/sizing.py), which
imports PARAMS from this file.
"""
import math
from pathlib import Path

from build123d import Box, Compound, Cylinder, Plane, Pos, Rot, Solid, Torus, Vector, export_step, export_stl

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # plinth
    "BASE_H": 190.0,        # concrete blocks, 390 x 190 x 190
    "PAN_T": 3.0,           # steel ash pan on the blocks
    # 1 outer drum: 200 L (55 US gal) open head
    "OUT_D": 572.0, "OUT_H": 851.0, "OUT_T": 1.2,
    "PORT_W": 40.0, "PORT_H": 110.0, "PORT_Z": 20.0, "N_PORTS": 4,   # primary air ports, bottom edge above drum floor
    # 3 inner retort: 114 L (30 US gal) open head
    "RET_D": 463.0, "RET_H": 737.0, "RET_T": 1.0,
    "GAS_HOLE_D": 20.0, "N_GAS_HOLES": 8, "GAS_HOLE_PCD": 300.0,
    "FILL_H": 600.0,        # packed feed depth in the retort
    # 4 firebrick standoffs
    "STANDOFF": 60.0,
    # 2 outer lid and 6 burner throat
    "LID_T": 1.5, "COLLAR_H": 40.0,
    "FLUE_D": 160.0, "FLUE_T": 2.0,
    "THROAT_H": 400.0,
    # 5 secondary air shroud (sized in CCB-CAL-001; replaces the 25 mm pipe ring of TRL 2)
    "SHROUD_D": 230.0, "SHROUD_H": 150.0, "SHROUD_Z": 40.0,   # bottom edge above the lid top
    "AIR_HOLE_D": 12.0, "N_AIR_HOLES": 30, "AIR_RINGS": 2,   # 24 to 30 holes with the baffle (DDR-002)
    # 8 water jacket (annular tank with an integral flue sleeve)
    "JKT_D": 420.0, "JKT_H": 600.0, "JKT_T": 2.0,
    "SLEEVE_D": 168.0, "SLEEVE_T": 2.0, "SOCKET": 50.0,      # sleeve slips over the throat and takes the flue
    "WATER_H": 540.0,       # working water depth (90 % of the tank)
    # 7 flue above the jacket
    "FLUE_ABOVE": 650.0, "CAP_D": 260.0, "CAP_GAP": 60.0,
    # 10 tripod
    "FOOT_R": 720.0, "LEG_ANGLE_B": 40.0, "LEG_ANGLE_T": 4.0,
    # 11 insulation
    "INS_T": 25.0, "INS_BOTTOM": 140.0, "INS_TOP_GAP": 30.0,
    # 15 spiral baffle insert in the jacket sleeve (DDR-002, item 12): twisted steel strip, lifts out for cleaning
    "BAFFLE_W": 150.0, "BAFFLE_T": 1.5, "BAFFLE_PITCH": 300.0, "BAFFLE_SEGS": 24,
    # 16 jacket shell blanket (DDR-002, item 12): mineral wool held by wire, tap and vent left clear
    "JKT_INS_T": 25.0,
    # 17 lid and top band blanket (DDR-002, item 13): ceramic fibre, clear of the air shroud intake
    "LID_INS_T": 25.0,      # skirt covers the bare top band (INS_TOP_GAP) and the locking ring
}
P = PARAMS


def levels(p=PARAMS):
    """Key heights (mm above ground) derived from the parameters."""
    z0 = p["BASE_H"] + p["PAN_T"]                    # outer drum floor
    z_lid = z0 + p["OUT_H"]                          # outer lid underside
    z_thr = z_lid + p["LID_T"]                       # throat base (lid top)
    z_jkt = z_thr + p["THROAT_H"]                    # jacket underside
    z_jtop = z_jkt + p["JKT_H"]
    z_out = z_jtop + p["FLUE_ABOVE"]                 # flue outlet
    z_ret = z0 + p["OUT_T"] + p["STANDOFF"]          # retort underside
    return {"z0": z0, "z_lid": z_lid, "z_thr": z_thr, "z_jkt": z_jkt, "z_jtop": z_jtop,
            "z_out": z_out, "z_cap": z_out + p["CAP_GAP"], "z_ret": z_ret,
            "z_ret_top": z_ret + p["RET_H"], "z_ports": z0 + p["PORT_Z"] + p["PORT_H"] / 2}


def _zcyl(r, h, z, x=0.0, y=0.0):
    return Pos(x, y, z + h / 2) * Cylinder(r, h)


def _shell(r_out, r_in, h, z):
    return _zcyl(r_out, h, z) - _zcyl(r_in, h + 2, z - 1)


def _tube(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def build_parts(p=PARAMS):
    """Return {bom_no: (name, shape)} for the modelled BOM lines (item 14, hardware, is not modelled)."""
    L = levels(p)
    z0, z_lid, z_thr, z_jkt, z_ret = L["z0"], L["z_lid"], L["z_thr"], L["z_jkt"], L["z_ret"]
    ro, rr, rf = p["OUT_D"] / 2, p["RET_D"] / 2, p["FLUE_D"] / 2
    parts = {}

    # 12 Plinth: four concrete blocks and a steel ash pan
    plinth = None
    for sx in (-1, 1):
        for sy in (-1, 1):
            b = Pos(sx * 170, sy * 105, p["BASE_H"] / 2) * Box(390, 190, p["BASE_H"])
            plinth = b if plinth is None else plinth + b
    plinth = plinth + Pos(0, 0, p["BASE_H"] + p["PAN_T"] / 2) * Box(760, 600, p["PAN_T"])
    parts[12] = ("Plinth: blocks and ash pan", plinth)

    # 1 Outer drum with primary air ports near the base
    outer = _shell(ro, ro - p["OUT_T"], p["OUT_H"], z0) + _zcyl(ro, p["OUT_T"], z0)
    for k in range(p["N_PORTS"]):
        a = math.radians(45 + 360 / p["N_PORTS"] * k)
        port = (Pos(ro * math.cos(a), ro * math.sin(a), z0 + p["PORT_Z"] + p["PORT_H"] / 2)
                * Rot(0, 0, math.degrees(a)) * Box(20, p["PORT_W"], p["PORT_H"]))
        outer = outer - port
    parts[1] = ("Outer drum, 200 L (firebox shell)", outer)

    # 2 Outer lid with flue collar
    lid = _zcyl(ro + 6, p["LID_T"], z_lid) + _zcyl(rf + 4, p["COLLAR_H"], z_thr)
    lid = lid - _zcyl(rf, 400, z_lid - 100)
    parts[2] = ("Outer lid with flue collar", lid)

    # 3 Inner retort with bolt-ring lid and gas holes in the base
    retort = (_shell(rr, rr - p["RET_T"], p["RET_H"], z_ret) + _zcyl(rr, p["RET_T"], z_ret)
              + _zcyl(rr + 10, 1.5, z_ret + p["RET_H"]) + _shell(rr + 10, rr + 0.5, 14, z_ret + p["RET_H"] - 12))
    for k in range(p["N_GAS_HOLES"]):
        a = 2 * math.pi * k / p["N_GAS_HOLES"]
        retort = retort - _zcyl(p["GAS_HOLE_D"] / 2, 10, z_ret - 5,
                                p["GAS_HOLE_PCD"] / 2 * math.cos(a), p["GAS_HOLE_PCD"] / 2 * math.sin(a))
    parts[3] = ("Inner retort, 114 L, bolt-ring lid", retort)

    # 4 Firebrick standoffs, three half bricks under the retort
    stand = None
    for k in range(3):
        a = math.radians(90 + 120 * k)
        s = (Pos(150 * math.cos(a), 150 * math.sin(a), z0 + p["OUT_T"] + p["STANDOFF"] / 2)
             * Rot(0, 0, math.degrees(a)) * Box(114, 64, p["STANDOFF"]))
        stand = s if stand is None else stand + s
    parts[4] = ("Firebrick standoffs (3)", stand)

    # 6 Burner throat with two rings of secondary air holes inside the shroud
    throat = _shell(rf, rf - p["FLUE_T"], p["THROAT_H"], z_thr)
    per_ring = p["N_AIR_HOLES"] // p["AIR_RINGS"]
    for ring in range(p["AIR_RINGS"]):
        zh = z_thr + p["SHROUD_Z"] + 55 + 40 * ring
        for k in range(per_ring):
            a = 2 * math.pi * (k + 0.5 * ring) / per_ring
            throat = throat - _tube((0, 0, zh), (1.2 * rf * math.cos(a), 1.2 * rf * math.sin(a), zh), p["AIR_HOLE_D"] / 2)
    parts[6] = ("Burner throat (afterburner)", throat)

    # 5 Secondary air shroud: sleeve around the throat, closed at the top, open at the bottom with a band damper
    zs = z_thr + p["SHROUD_Z"]
    rs = p["SHROUD_D"] / 2
    shroud = _shell(rs, rs - 1.5, p["SHROUD_H"], zs) + (_zcyl(rs, 2, zs + p["SHROUD_H"]) - _zcyl(rf, 10, zs + p["SHROUD_H"] - 4))
    shroud = shroud + _shell(rs + 4, rs + 1, 40, zs)          # sliding band damper over the bottom gap
    parts[5] = ("Secondary air shroud and damper", shroud)

    # 8 Water jacket: annular tank with an integral flue sleeve, open vent, loose lid
    rj, rsl = p["JKT_D"] / 2, p["SLEEVE_D"] / 2
    jacket = (_shell(rj, rj - p["JKT_T"], p["JKT_H"], z_jkt)
              + (_zcyl(rj, p["JKT_T"], z_jkt) - _zcyl(rsl, 10, z_jkt - 5))
              + _shell(rsl, rsl - p["SLEEVE_T"], p["JKT_H"] + 2 * p["SOCKET"], z_jkt - p["SOCKET"]))
    jacket = jacket + (_zcyl(rj + 5, 2, p["JKT_H"] + z_jkt + 3) - _zcyl(rsl + 5, 10, p["JKT_H"] + z_jkt - 2))  # loose lid
    jacket = jacket + _tube((0, rj - 40, z_jkt + p["JKT_H"]), (0, rj - 40, z_jkt + p["JKT_H"] + 90), 12)       # open vent
    parts[8] = ("Water jacket, about 60 L, open-vented", jacket)

    # 9 Draw-off tap near the jacket base
    tap = (_tube((rj, 0, z_jkt + 40), (rj + 110, 0, z_jkt + 40), 11)
           + Pos(rj + 125, 0, z_jkt + 40) * Box(40, 36, 36)
           + _tube((rj + 125, 0, z_jkt + 58), (rj + 125, 0, z_jkt + 100), 5)
           + Pos(rj + 125, 0, z_jkt + 100) * Box(18, 90, 8))
    parts[9] = ("Draw-off tap", tap)

    # 7 Flue above the jacket (slips inside the sleeve spigot) with rain cap
    z_out = L["z_out"]
    flue = _shell(rf, rf - p["FLUE_T"], p["FLUE_ABOVE"] + p["SOCKET"], L["z_jtop"])
    flue = flue + Pos(0, 0, L["z_cap"]) * Box(p["CAP_D"], p["CAP_D"], 3)
    for k in range(3):
        a = 2 * math.pi * k / 3
        flue = flue + _tube((rf * 0.9 * math.cos(a), rf * 0.9 * math.sin(a), z_out - 40),
                            (rf * 0.9 * math.cos(a), rf * 0.9 * math.sin(a), L["z_cap"]), 4)
    parts[7] = ("Flue pipe with rain cap", flue)

    # 10 Tripod: ring seat under the jacket and three angle legs
    rseat = rj + 12
    tripod = Pos(0, 0, z_jkt - 12) * Torus(rseat, 10)
    for k in range(3):
        a = math.radians(30 + 120 * k)
        top = (rseat * math.cos(a), rseat * math.sin(a), z_jkt - 12)
        foot = (p["FOOT_R"] * math.cos(a), p["FOOT_R"] * math.sin(a), 0.0)
        tripod = tripod + _tube(foot, top, p["LEG_ANGLE_B"] / 2 * 0.7) + Pos(foot[0], foot[1], 4) * Box(80, 80, 8)
    parts[10] = ("Jacket support tripod", tripod)

    # 11 Insulation blanket on the outer drum, air ports left clear
    zi = z0 + p["INS_BOTTOM"]
    parts[11] = ("Insulation blanket", _shell(ro + p["INS_T"], ro + 0.5, p["OUT_H"] - p["INS_BOTTOM"] - p["INS_TOP_GAP"], zi))

    # 13 Thermocouple logger on a tripod leg, probes to the retort core and the throat exit
    a0 = math.radians(30)
    lz = 520.0
    lr = p["FOOT_R"] - (p["FOOT_R"] - rseat) * lz / (z_jkt - 12)
    lx, ly = lr * math.cos(a0), lr * math.sin(a0)
    zc = z_ret + p["FILL_H"] / 2
    logger = (Pos(lx, ly, lz) * Box(90, 60, 130)
              + _tube((70, 60, z_thr + 140), (70, 60, zc), 4)                       # retort core probe via lid glands
              + _tube((rf + 60, 0, z_jkt - 40), (0, 0, z_jkt - 40), 4)              # throat exit probe
              + _tube((lx, ly, lz + 65), (lx - 120, ly, z_lid + 120), 3)
              + _tube((lx - 120, ly, z_lid + 120), (70, 60, z_thr + 140), 3)
              + _tube((lx - 120, ly, z_lid + 120), (rf + 60, 0, z_jkt - 40), 3))
    parts[13] = ("Thermocouple logger and probes", logger)

    # 15 Spiral baffle insert: a twisted strip in the jacket sleeve, hung from a cross bar that sits in
    #    notches at the foot of the flue pipe, so it lifts out with the flue for cleaning
    zb0, hb = z_jkt + 10, p["JKT_H"] - 10
    n = p["BAFFLE_SEGS"]
    dz = hb / n
    baffle = None
    for k in range(n):
        ang = 180.0 * (k + 0.5) * dz / p["BAFFLE_PITCH"]          # half a turn per pitch, as a twisted tape
        seg = Pos(0, 0, zb0 + (k + 0.5) * dz) * Rot(0, 0, ang) * Box(p["BAFFLE_W"], p["BAFFLE_T"], dz + 0.5)
        baffle = seg if baffle is None else baffle + seg
    baffle = baffle + Pos(0, 0, L["z_jtop"] + 5) * Box(p["FLUE_D"] - 4, 10, 10)
    parts[15] = ("Spiral baffle insert", baffle)

    # 16 Jacket shell blanket: wrap on the jacket side, tap left clear
    tj = p["JKT_INS_T"]
    jins = _shell(rj + tj, rj + 0.5, p["JKT_H"] - 60, z_jkt + 60)
    parts[16] = ("Jacket shell blanket", jins)

    # 17 Lid and top band blanket: annular disc on the lid, clear of the shroud intake, and a short skirt
    ti = p["LID_INS_T"]
    lidins = (_zcyl(ro + p["INS_T"], ti, z_thr) - _zcyl(rs + 25, ti + 2, z_thr - 1))
    skirt = p["INS_TOP_GAP"] + p["LID_T"]
    lidins = lidins + _shell(ro + p["INS_T"], ro + 6.5, skirt, z_thr - skirt)
    parts[17] = ("Lid and top band blanket", lidins)
    return parts


UNITS = {
    "charcube-kiln": (1, 2, 3, 4, 5, 6, 11, 17),        # drums, lid, throat, shroud, bricks, blankets
    "charcube-heat-recovery-unit": (7, 8, 9, 10, 15, 16),  # lifted aside as one unit for loading
    "charcube-retort": (3,),
}


def assembly(parts=None):
    parts = parts or build_parts()
    return Compound([parts[k][1] for k in sorted(parts)])


if __name__ == "__main__":
    parts = build_parts()
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
    print(f"assembly bounding box: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    for k, v in L.items():
        print(f"  {k:10s} {v:7.0f} mm")
    for k in sorted(parts):
        print(f"  item {k:2d}  {parts[k][0]:40s} volume {parts[k][1].volume / 1e6:7.3f} L")
    print("wrote cad/step/*.step and cad/stl/*.stl")
