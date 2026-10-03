"""CharCube general arrangement drawing CCB-DWG-001 (Rev P6).

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
from build123d import Compound  # noqa: E402
from model import PARAMS as P, PART_KEYS, build_components, build_parts, levels  # noqa: E402

C = build_components()
parts = build_parts(C=C)
# the lifting aid's concrete footing is below ground and left off this sheet (see CCB-DWG-115)
parts[18] = (parts[18][0], Compound(children=[C[k].shape for k in PART_KEYS[18] if k != "footing"]))
asm = Compound([parts[k][1] for k in sorted(parts)])
bb = asm.bounding_box()
L = levels()

work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="CharCube", title="General arrangement, TRL 3 model", dwg_no="CCB-DWG-001",
          rev="P6", author="Amish Chadha", date="2026-10-02", concept=True, scale=1 / 50,
          material="Plain carbon steel drums, sheet and pipe; no galvanized parts. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (CCB-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "DDR-002: baffle insert, jacket and lid blankets, 30 air holes", "2026-09-25", "AC"),
                     ("P3", "DDR-002 item 17: budget top-up to $320; R10 met", "2026-09-26", "AC"),
                     ("P4", "Layout and labels tidied", "2026-09-30", "AC"),
                     ("P5", "CCB-DDR-003: design made constructable (fins and legs, collar, clips)", "2026-09-30", "AC"),
                     ("P6", "2026-10-02 decisions: fibre board, sleeve flare, conical cap, labels, lifting aid", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 49, 140, 53, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions (mm) and data", [
    f"Kiln {L['z_cap_top']:.0f} H to cap; 40 x 40 x 4 tripod legs, feet on {2 * P['FOOT_R']:.0f} circle",
    f"Plinth: blocks, {P['BOARD'][2]:.0f} mm fibre board, pan; drum floor at {L['z0']:.0f}",
    f"Outer drum {P['OUT_D']:.0f} dia x {P['OUT_H']:.0f}, 200 L",
    f"Retort {P['RET_D']:.0f} dia x {P['RET_H']:.0f}, 114 L, on {P['STANDOFF']:.0f} mm bricks; fill {P['FILL_H']:.0f}",
    f"{P['N_GAS_HOLES']} x {P['GAS_HOLE_D']:.0f} gas holes in retort base, {P['GAS_HOLE_PCD']:.0f} PCD",
    f"{P['N_PORTS']} primary ports {P['PORT_W']:.0f} x {P['PORT_H']:.0f} with dampers",
    f"Throat {P['FLUE_D']:.0f} x {P['FLUE_T']:.0f} x {P['THROAT_H']:.0f}; {P['N_AIR_HOLES']} x {P['AIR_HOLE_D']:.0f} air holes, 2 rings",
    f"Air shroud {P['SHROUD_D']:.0f} dia x {P['SHROUD_H']:.0f}, open bottom, band damper",
    f"Jacket {P['JKT_D']:.0f} dia x {P['JKT_H']:.0f}, sleeve {P['SLEEVE_D']:.0f}, foot flared to {P['SLEEVE_FLARE'][1]:.0f}; 61 L",
    f"Spiral baffle {P['BAFFLE_W']:.0f} wide in sleeve, hung from flue foot; {P['JKT_INS_T']:.0f} mm wool on jacket",
    f"{P['LID_INS_T']:.0f} mm ceramic fibre on lid and top band, clear of shroud",
    f"Jacket underside {L['z_jkt']:.0f}; flue outlet {L['z_out']:.0f}; conical cap {P['CAP_D']:.0f}, {P['CAP_GAP']:.0f} gap",
    f"Lifting aid: post {L['z_arm'] / 1000 + 0.04:.1f} m high, {P['POST_R']:.0f} behind the kiln; arm {P['POST_R']:.0f} reach",
    f"  hand winch raises the drained unit {P['LIFT']:.0f} and swings it clear",
    "Jacket OPEN-VENTED: never fit a sealed lid, valve or plug",
    "Kiln about 97 kg dry; unit 47 kg, by the lifting aid (CCB-CAL-001)",
    "Est. cost $546 against the $320 target. See CCB-CAL-001 v0.6",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=119, width=140)
s.save(ROOT / "cad/drawings/CCB-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/CCB-DWG-001.svg, .pdf, .png")
