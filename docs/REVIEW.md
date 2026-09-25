# Review note: CharCube

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (CCB-PRB-001 v0.2): problem with cited scale, health and carbon figures; users; constraints; out of scope (including the field-scale gap); prior work (Adam retort, retort field emissions, Kon-Tiki kilns, IPCC permanence factors) with inline sources; open questions; co-design checklist added.
- `docs/03-requirements.md` (CCB-REQ-001 v0.2): 12 measurable requirements (R1 to R12) with targets, a status column against the concept estimates, a list of requirements not met and the assumptions.
- `docs/02-concept.md` (CCB-PRC-001 v0.2): how it works, numbered components, first-order numbers (batch, yield, energy, draft, hot water, carbon, methane, mass, cost), design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of the nested drums, lid, burner throat, secondary air manifold, flue, water jacket, tap, tripod, insulation, plinth and logger, each with a BOM number; 1.75 m scale figure.
- `media/`: `hero.png`, `concept-blueprint` (PNG, PDF, SVG), `cutaway.png`, `exploded.png` with BOM callouts, `flow.png` (energy per batch, estimates), `model.glb` and `viewer.html`. Temporary view folders removed.
- `bom/bom.csv` (14 lines, numbered to match the exploded view, indicative USD prices) and `bom/bom-notes.md`.
- `README.md`: hero image and links line before "## Problem"; problem, concept, key components and safety text brought in line with the concept.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml` unchanged. The pitch and problem remain accurate.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Feed per batch | about 12 kg packed residue; about 4 kg if loose chopped straw | R1 met for packed feed, **not met** for loose straw |
| Biochar yield | about 28 % (20 to 35 %), about 3.4 kg per batch | R2 at risk |
| Start-up wood | about 5 kg | R8 at the limit |
| Batch time | 2.5 to 3.5 h burning, 10 to 14 h sealed cooling | R5 met |
| Heat released | about 180 MJ per batch, about 17 kW average | |
| Hot water | about 15 MJ (10 to 25 MJ); 60 L raised about 60 K | R6 met; may boil on a hot batch |
| Carbon stored for 100 years | about 5.4 kg CO₂ per batch (IPCC medium-temperature factor) | |
| Methane penalty | about 2.3 kg CO₂e per batch at the retort field average | R4 **not shown** |
| Net removal | about 3 to 5 kg CO₂e per batch; about 0.8 to 1.4 t CO₂e a year at 250 batches | |
| Height and mass | about 2.7 m to the rain cap; about 85 kg dry; tripod, jacket and flue unit about 36 kg | R11 met only with a two-person lift |
| Parts cost | about $299 | R10 met with about $1 margin, safety equipment excluded |

Requirements not met or not yet shown:

- **R1 not met for loose chopped straw** (about 4 kg per batch). Straw must be bundled or packed, or mixed with stalks.
- **R4 not shown.** Gas routing is closed by design, but methane and smoke need measurement. At the published retort average, methane cancels about 40 % of the carbon benefit, so the burner throat carries much of the climate case.
- **R2, R3 and R8** rest on wide-range estimates.
- **R10** has no margin and excludes about $40 of safety equipment.
- **R11** needs two people to lift the drained tripod unit.
- **Scale.** One kiln handles about 3 t of residue a year, far less than one hectare of rice straw. The design serves a household, a trial plot or a cooperative with several kilns; it does not replace field burning at scale. This is stated in the problem statement.

### Proposed, awaiting Amish

1. **Heat recovery type (changes a listed component).** The scaffold listed a copper coil heat exchanger. Options: (a) open-vented annular water jacket around the flue, about 60 L; (b) copper coil in the flue feeding a separate tank by thermosiphon (tank about 2 m high) or pump; (c) no heat recovery, saving about $87. Recommendation: (a), because it needs no pump or raised tank and cannot build pressure. The README key components now describe (a) and say it is proposed.
2. **Budget.** Parts are about $299 against $300, excluding about $40 of safety equipment. Options: (a) keep $300 and list safety equipment separately; (b) raise `budget_usd` to $350 to include it; (c) use a clay and ash render in place of the blanket to save about $25 and fit most of the safety kit. Recommendation: (a) for the kiln budget, with the safety kit stated as required in the build notes at TRL 3. `project.yaml` is unchanged.
3. **Kiln type.** Nested-drum retort (recommended) rather than a Kon-Tiki flame-curtain kiln, which is cheaper and needs no start-up wood but is open and cannot feed a water jacket.
4. **Target feedstock.** Bundled straw and mixed stalks and cobs first (recommended); loose straw only with a press, which would be a separate project.
5. **Burner throat with preheated secondary air** in addition to burning in the annulus. Recommendation: include.
6. **Temperature logger as standard** (about $32). Recommendation: include, as the batch record for char quality.
7. **Insulation:** ceramic fibre blanket (recommended for the prototype) or clay and ash render.
8. **Tripod support** for the jacket and flue, lifted aside by two people for loading (recommended), or a swinging arm at extra cost.
9. **First region, residue and partner** for co-design: for example paddy straw in northwest India or maize and cotton stalks in East Africa.
10. **Name.** CharCube is a cylindrical drum kiln. Keep the name, or reshape the concept (for example a cubic frame) to suit it. Recommendation: keep the name; no change made.

SwapCell is not used; the logger runs from a USB power bank.

### Safety concerns

- Fire and burns: surfaces at 300 to 700 °C, hot char for many hours, embers. Outdoors only, 5 m clearance, extinguisher or water at hand, 3 m exclusion circle for children and animals.
- Flammable and toxic gas: carbon monoxide, hydrogen, methane and tar vapor. Opening a hot retort can cause a sudden flare. Never operate in or near enclosed spaces.
- Water jacket: may boil; must stay open-vented and never be connected to plumbing or sealed. Scald risk at the tap.
- Used drums that held fuel, solvent or pesticide can explode when cut and release toxic fumes when heated; galvanized parts release zinc fumes.
- Char dust: fire and inhalation hazard; wet before handling.
- Heavy lifts: the 36 kg tripod unit and a full jacket (about 76 kg, which must never be moved full).

### Problems and notes

- The cutaway shows the water jacket as a solid annulus because it is modelled as the water volume; the flue passes through its centre.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- The GWP100 of 28 for methane is the IPCC AR5 value; AR6 uses about 27 to 30 depending on source. The conclusion does not change.

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to check the retort heat balance, gas-hole and secondary-air sizing, draft, jacket heat transfer and surface temperatures by calculation, and to produce the parametric model and drawing sheet.
