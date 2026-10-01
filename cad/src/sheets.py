"""CharCube general arrangement drawing CCB-DWG-001 (Rev P5).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/CCB-DWG-001.svg, .pdf and .png from the parametric model.
The concept sheet in media/ uses CCB-DWG-010. Figures quoted in the notes come
from CCB-CAL-001 (python docs/04-calcs/sizing.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assembly, build_parts, levels  # noqa: E402

parts = build_parts()
asm = assembly(parts)
bb = asm.bounding_box()
L = levels()

work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="CharCube", title="General arrangement, TRL 3 model", dwg_no="CCB-DWG-001",
          rev="P5", author="Amish Chadha", date="2026-09-30", concept=True, scale=1 / 30,
          material="Plain carbon steel drums, sheet and pipe; no galvanized parts. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (CCB-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "DDR-002: baffle insert, jacket and lid blankets, 30 air holes", "2026-09-25", "AC"),
                     ("P3", "DDR-002 item 17: budget top-up to $320; R10 met", "2026-09-26", "AC"),
                     ("P4", "Layout and labels tidied", "2026-09-30", "AC"),
                     ("P5", "CCB-DDR-003: design made constructable (fins and legs, collar, clips)", "2026-09-30", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 44, 140, 62, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions (mm) and data", [
    f"Overall {bb.size.X:.0f} x {bb.size.Y:.0f} (tripod feet) x {bb.size.Z:.0f} H to rain cap",
    f"Outer drum {P['OUT_D']:.0f} dia x {P['OUT_H']:.0f}, 200 L; floor at {L['z0']:.0f} on plinth",
    f"Retort {P['RET_D']:.0f} dia x {P['RET_H']:.0f}, 114 L, on {P['STANDOFF']:.0f} mm bricks; fill {P['FILL_H']:.0f}",
    f"{P['N_GAS_HOLES']} x {P['GAS_HOLE_D']:.0f} gas holes in retort base, {P['GAS_HOLE_PCD']:.0f} PCD",
    f"{P['N_PORTS']} primary ports {P['PORT_W']:.0f} x {P['PORT_H']:.0f} with dampers",
    f"Throat {P['FLUE_D']:.0f} x {P['FLUE_T']:.0f} x {P['THROAT_H']:.0f}; {P['N_AIR_HOLES']} x {P['AIR_HOLE_D']:.0f} air holes, 2 rings",
    f"Air shroud {P['SHROUD_D']:.0f} dia x {P['SHROUD_H']:.0f}, open bottom, band damper",
    f"Jacket {P['JKT_D']:.0f} dia x {P['JKT_H']:.0f}, sleeve {P['SLEEVE_D']:.0f}; 61 L at {P['WATER_H']:.0f} deep",
    f"Spiral baffle {P['BAFFLE_W']:.0f} wide in sleeve, hung from flue foot; {P['JKT_INS_T']:.0f} mm wool on jacket",
    f"{P['LID_INS_T']:.0f} mm ceramic fibre on lid and top band, clear of shroud",
    f"Jacket underside {L['z_jkt']:.0f}; flue outlet {L['z_out']:.0f} above ground",
    f"Tripod feet on {2 * P['FOOT_R']:.0f} circle; 40 x 40 x 4 legs bolted to jacket fins",
    "Jacket OPEN-VENTED: never fit a sealed lid, valve or plug",
    "Kiln about 97 kg dry; lift unit 47 kg, two people (CCB-CAL-001)",
    "Parts $319 against the $320 budget (R10 met). See CCB-CAL-001 v0.3",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=124, width=140)
s.save(ROOT / "cad/drawings/CCB-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/CCB-DWG-001.svg, .pdf, .png")
