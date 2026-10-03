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
from build123d import Compound  # noqa: E402
from model import PART_KEYS, build_components, build_parts  # noqa: E402

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
    15: ("#78716C", (-700, 0, 2000)),
    16: ("#FDE68A", (700, -300, 1900)),
    14: ("#F2C230", (0, -900, 600)),
    17: ("#F3F4F6", (0, 0, 850)),
    18: ("#475569", (0, 900, 0)),
}

_C = build_components()
model = build_parts(C=_C)
# the lifting aid without its footing and the buried part of its ground sleeve (both below ground)
model[18] = (model[18][0], Compound(children=[_C[k].shape for k in PART_KEYS[18] if k not in ("footing", "gsleeve")]))
parts = [Part(name, shape, STYLE[k][0], k, STYLE[k][1]) for k, (name, shape) in sorted(model.items())]

if __name__ == "__main__":
    render_all(
        parts, project="CharCube", title="Retort kiln with heat recovery", dwg_no="CCB-DWG-010", rev="P5", date="2026-10-02",
        key_figures=["200 L outer drum, 114 L retort; flue outlet 2.72 m above ground",
                     "12.0 kg air-dry feed per batch; about 3.0 kg biochar (28 %, estimate)",
                     "Burn about 4.5 h with about 3.7 kg of wood (CCB-CAL-001, estimate)",
                     "Hot water about 11.5 MJ per batch, 61 L raised about 45 K",
                     "Unit lifted by a winch on a swinging arm; estimated cost $546 (target $320)"],
        cut=True, cut_exclude=("Jacket support tripod", "Thermocouple logger and probes", "Lifting aid for the heat-recovery unit"),
        flow={"title": "energy per batch, MJ (CCB-CAL-001 v0.3 central estimates: 12.0 kg residue, 3.7 kg wood)",
              "unit": "MJ",
              "stages": [("Residue and wood", 253), ("Heat released in kiln", 160),
                         ("Flue gas at jacket", 61), ("Hot water", 12)],
              "losses": [(0, "Biochar 60, latent heat 33", 93), (1, "Retort, structure, shell", 100),
                         (2, "Up the stack", 49)]},
    )
