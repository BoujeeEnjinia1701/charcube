"""CharCube concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. Z up, ground at Z = 0, kiln axis on X = Y = 0.
Reference sizes: 200 L (55 US gal) open-head steel drum, about 572 mm inside
diameter x 851 mm tall; 114 L (30 US gal) open-head drum, about 463 mm diameter
x 737 mm tall, used as the inner retort.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Torus, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all

# ---------------- key dimensions (mm) ----------------
BASE_H = 190.0                 # concrete block plinth
PAN_T = 10.0                   # steel ash pan on the blocks
OUT_R, OUT_H, WALL = 286.0, 851.0, 3.0   # outer drum (wall exaggerated for rendering)
RET_R, RET_H = 231.5, 737.0    # inner retort
STANDOFF = 60.0                # retort raised on firebrick standoffs
Z0 = BASE_H + PAN_T            # outer drum floor
Z_LID = Z0 + OUT_H             # outer lid underside
LID_T = 12.0
FLUE_R = 80.0                  # 160 mm outside diameter flue and burner throat
THROAT_H = 400.0               # burner throat (afterburner) above the lid
JKT_H, JKT_R = 600.0, 210.0    # annular water jacket around the flue, about 60 L
FLUE_ABOVE = 600.0             # plain flue above the jacket
INS_T = 25.0                   # ceramic fibre blanket


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def zcyl(r, h, z, x=0.0, y=0.0):
    """Cylinder of radius r and height h standing on z."""
    return Pos(x, y, z + h / 2) * Cylinder(r, h)


def shell(r_out, r_in, h, z):
    return zcyl(r_out, h, z) - zcyl(r_in, h + 2, z - 1)


# 12 Plinth: four concrete blocks and a steel ash pan
blocks = None
for sx in (-1, 1):
    for sy in (-1, 1):
        b = Pos(sx * 170, sy * 105, BASE_H / 2) * Box(390, 190, BASE_H)
        blocks = b if blocks is None else blocks + b
plinth = blocks + Pos(0, 0, BASE_H + PAN_T / 2) * Box(760, 600, PAN_T)

# 1 Outer drum (firebox shell) with four primary air ports near the base
outer = shell(OUT_R, OUT_R - WALL, OUT_H, Z0) + zcyl(OUT_R, WALL, Z0)
for k in range(4):
    a = math.radians(45 + 90 * k)
    port = Pos(OUT_R * math.cos(a), OUT_R * math.sin(a), Z0 + 70) * Rot(0, 0, math.degrees(a)) * Box(40, 110, 60)
    outer = outer - port

# 2 Outer lid with flue collar
lid = zcyl(OUT_R + 8, LID_T, Z_LID) + zcyl(FLUE_R + 6, 40, Z_LID + LID_T)
lid = lid - zcyl(FLUE_R - 2, 200, Z_LID - 50)

# 3 Inner retort with clamped lid and gas holes in the base (holes too small to show)
z_ret = Z0 + WALL + STANDOFF
retort = (shell(RET_R, RET_R - WALL, RET_H, z_ret) + zcyl(RET_R, WALL, z_ret)
          + zcyl(RET_R + 10, 14, z_ret + RET_H))          # bolt-ring lid
# 4 Firebrick standoffs, three under the retort
stand = None
for k in range(3):
    a = math.radians(90 + 120 * k)
    s = Pos(150 * math.cos(a), 150 * math.sin(a), Z0 + WALL + STANDOFF / 2) * Rot(0, 0, math.degrees(a)) * Box(110, 64, STANDOFF)
    stand = s if stand is None else stand + s

# 11 Insulation blanket on the outer drum, leaving the air ports clear
ins = shell(OUT_R + INS_T, OUT_R + 1, OUT_H - 170, Z0 + 140)

# 6 Burner throat (afterburner) on the lid
z_thr = Z_LID + LID_T
throat = shell(FLUE_R, FLUE_R - 3, THROAT_H, z_thr)

# 5 Secondary air manifold: ring around the throat base with an inlet pipe and damper
z_man = z_thr + 90
manifold = (Pos(0, 0, z_man) * Torus(FLUE_R + 26, 14)
            + tube3((FLUE_R + 26, 0, z_man), (OUT_R + 90, 0, z_man), 14)
            + Pos(OUT_R + 90, 0, z_man) * Box(24, 50, 50))

# 8 Annular water jacket around the flue, open-vented, about 60 L
z_jkt = z_thr + THROAT_H
jacket = shell(JKT_R, FLUE_R + 6, JKT_H, z_jkt) + zcyl(JKT_R, 3, z_jkt)
jacket = jacket + tube3((0, JKT_R - 30, z_jkt + JKT_H), (0, JKT_R - 30, z_jkt + JKT_H + 90), 12)   # open vent and fill

# 9 Draw-off tap near the jacket base
tap = (tube3((JKT_R, 0, z_jkt + 40), (JKT_R + 140, 0, z_jkt + 40), 15)
       + Pos(JKT_R + 150, 0, z_jkt + 20) * Box(50, 50, 80)
       + tube3((JKT_R + 150, 0, z_jkt + 60), (JKT_R + 150, 0, z_jkt + 120), 6)
       + Pos(JKT_R + 150, 0, z_jkt + 120) * Box(20, 110, 12))

# 7 Flue pipe through the jacket and above it
flue = shell(FLUE_R, FLUE_R - 2, JKT_H + FLUE_ABOVE, z_jkt) + Pos(0, 0, z_jkt + JKT_H + FLUE_ABOVE + 60) * Box(260, 260, 4)
flue = flue + tube3((0, 0, z_jkt + JKT_H + FLUE_ABOVE), (0, 0, z_jkt + JKT_H + FLUE_ABOVE + 60), 4)  # rain cap post

# 10 Support tripod carrying the jacket and flue, so they lift off as one unit for loading
tripod = Pos(0, 0, z_jkt - 12) * Torus(JKT_R + 12, 10)
feet = []
for k in range(3):
    a = math.radians(30 + 120 * k)
    top = ((JKT_R + 12) * math.cos(a), (JKT_R + 12) * math.sin(a), z_jkt - 12)
    foot = (720 * math.cos(a), 720 * math.sin(a), 0.0)
    tripod = tripod + tube3(foot, top, 14) + Pos(foot[0], foot[1], 4) * Box(80, 80, 8)
    feet.append(foot)

# 13 Thermocouple logger on a tripod leg, with probes into the retort and the throat exit
a0 = math.radians(30)
lz = 520.0
lr = 720 - (720 - (JKT_R + 12)) * lz / (z_jkt - 12)   # leg radius at the logger height
lx, ly = lr * math.cos(a0), lr * math.sin(a0)          # box clamped around the leg
logger = Pos(lx, ly, lz) * Box(90, 60, 130)
probe_ret = tube3((70, 60, Z_LID + LID_T + 140), (70, 60, z_ret + RET_H * 0.5), 4)
probe_flue = tube3((FLUE_R + 60, 0, z_jkt - 40), (0, 0, z_jkt - 40), 4)
lead = (tube3((lx, ly, lz + 65), (lx - 120, ly, Z_LID + 120), 3)
        + tube3((lx - 120, ly, Z_LID + 120), (70, 60, Z_LID + LID_T + 140), 3)
        + tube3((lx - 120, ly, Z_LID + 120), (FLUE_R + 60, 0, z_jkt - 40), 3))
logger = logger + probe_ret + probe_flue + lead

STEEL = "#6B7280"
parts = [
    Part("Outer drum, 200 L (firebox shell)", outer, "#4B5563", 1, (0, 0, 0)),
    Part("Outer lid with flue collar", lid, "#374151", 2, (0, 0, 1050)),
    Part("Inner retort, 114 L, clamped lid", retort, "#9A3412", 3, (1150, 0, 250)),
    Part("Firebrick standoffs (3)", stand, "#B45309", 4, (1150, 0, -60)),
    Part("Secondary air manifold", manifold, "#0EA5E9", 5, (-150, -700, 1150)),
    Part("Burner throat (afterburner)", throat, "#C2410C", 6, (0, 0, 1300)),
    Part("Flue pipe with rain cap", flue, STEEL, 7, (0, 0, 2300)),
    Part("Water jacket, about 60 L, open-vented", jacket, "#0F766E", 8, (0, 0, 1700)),
    Part("Draw-off tap", tap, "#D4A017", 9, (550, 0, 1450)),
    Part("Jacket support tripod", tripod, "#A16207", 10, (-850, 300, 1300)),
    Part("Insulation blanket", ins, "#E5E7EB", 11, (0, -800, 0)),
    Part("Plinth: blocks and ash pan", plinth, "#9CA3AF", 12, (0, 0, -350)),
    Part("Thermocouple logger and probes", logger, "#7C3AED", 13, (2000, 300, 200)),
]

if __name__ == "__main__":
    render_all(
        parts, project="CharCube", title="Retort kiln with heat recovery", dwg_no="CCB-DWG-010",
        key_figures=["200 L outer drum, 114 L inner retort; about 2.7 m to the flue cap",
                     "About 12 kg dry residue per batch; about 3.4 kg biochar (28 %, estimate)",
                     "Retort gas burned in the annulus and burner throat (secondary air)",
                     "About 60 L water raised about 60 K per batch (estimate)",
                     "Parts about $299 against a $300 budget (indicative)"],
        cut=True, cut_exclude=("Jacket support tripod", "Thermocouple logger and probes"),
        flow={"title": "energy per batch, MJ (estimates: 12 kg residue at 15 MJ/kg plus 5 kg start-up wood)",
              "unit": "MJ",
              "stages": [("Residue and wood", 260), ("Heat released in kiln", 180),
                         ("Flue gas at jacket", 80), ("Hot water", 15)],
              "losses": [(0, "Kept in biochar (product)", 80), (1, "Retort, drying, drum walls", 100),
                         (2, "Up the stack", 65)]},
    )
