"""CharCube concept media from the TRL 3 parametric model.

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py; figures come from CCB-CAL-001
(python docs/04-calcs/sizing.py). Not for fabrication.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / ".kit"))
sys.path.insert(0, str(HERE))
from concept import Part, render_all  # noqa: E402
from model import build_parts  # noqa: E402

STYLE = {   # bom: (colour, exploded-view offset in mm)
    1: ("#4B5563", (0, 0, 0)),
    2: ("#374151", (0, 0, 1050)),
    3: ("#9A3412", (1150, 0, 250)),
    4: ("#B45309", (1150, 0, -60)),
    5: ("#0EA5E9", (0, -700, 1150)),
    6: ("#C2410C", (0, 0, 1300)),
    7: ("#6B7280", (0, 0, 2300)),
    8: ("#0F766E", (0, 0, 1700)),
    9: ("#D4A017", (550, 0, 1450)),
    10: ("#A16207", (-850, 300, 1300)),
    11: ("#E5E7EB", (0, -800, 0)),
    12: ("#9CA3AF", (0, 0, -350)),
    13: ("#7C3AED", (2000, 300, 200)),
}

model = build_parts()
parts = [Part(name, shape, STYLE[k][0], k, STYLE[k][1]) for k, (name, shape) in sorted(model.items())]

if __name__ == "__main__":
    render_all(
        parts, project="CharCube", title="Retort kiln with heat recovery", dwg_no="CCB-DWG-010",
        key_figures=["200 L outer drum, 114 L retort; flue outlet 2.70 m above ground",
                     "12.0 kg air-dry feed per batch; about 3.0 kg biochar (28 %, estimate)",
                     "Burn about 4.5 h with about 5.8 kg of wood (CCB-CAL-001, estimate)",
                     "Hot water about 6 MJ per batch, 61 L raised about 25 K (below R6)",
                     "Parts $298 against a $300 budget (indicative)"],
        cut=True, cut_exclude=("Jacket support tripod", "Thermocouple logger and probes"),
        flow={"title": "energy per batch, MJ (CCB-CAL-001 central estimates: 12.0 kg residue, 5.8 kg wood)",
              "unit": "MJ",
              "stages": [("Residue and wood", 286), ("Heat released in kiln", 190),
                         ("Flue gas at jacket", 71), ("Hot water", 6)],
              "losses": [(0, "Biochar 60, latent heat 36", 96), (1, "Retort, structure, shell", 118),
                         (2, "Up the stack", 65)]},
    )
