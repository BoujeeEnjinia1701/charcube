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

Status update: items 1 to 8 and 10 were decided by Amish, 2026-09-25: go with recommendation (CCB-DDR-001). Item 9 had no recommendation and remains proposed, awaiting Amish.

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

## Session 2026-09-25: TRL 3

Amish reviewed the TRL 2 points on 2026-09-25 and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." This session applied that to CharCube and produced the TRL 3 evidence. TRL 4 is on hold by Amish's instruction.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CCB-DDR-001 v0.1): the nine decided items, the cross-cutting approvals (SwapCell items not applicable), and the open items.
- `docs/04-calcs/01-sizing.md` (CCB-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: batch and char mass balance, charge heating time by conduction, shell loss and surface temperatures, masses and tripod buckling, energy balance and wood demand, draft, gas holes and air sizing, jacket heat transfer, sealed cooling, carbon, logger accuracy and cost, in three scenarios. The script reads `cad/src/model.py` and `bom/bom.csv`.
- `cad/src/model.py`: parametric build123d model (all key dimensions in `PARAMS`), exporting `cad/step/` and `cad/stl/` `charcube-assembly`, `charcube-kiln`, `charcube-heat-recovery-unit` and `charcube-retort`.
- `cad/src/sheets.py` and `cad/drawings/CCB-DWG-001` (SVG, PDF, PNG): general arrangement at Rev P1, 1:30, "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps CCB-DWG-010.
- `bom/bom.csv`: 14 lines, all priced by supplier type, total $298; `bom/bom-notes.md` lists the required safety kit ($40) outside the budget.
- `cad/src/concept_media.py` now builds from the model; all media refreshed (hero, blueprint, cutaway, exploded, flow, GLB viewer) and checked by eye. Temporary view folders deleted.
- CCB-PRB-001, CCB-PRC-001 and CCB-REQ-001 moved to v0.3 with the decisions and CCB-CAL-001 numbers; `README.md` updated; `project.yaml` set to `trl: 3`, `trl_target: 3` with the evidence list.

### Requirements (CCB-CAL-001, central estimates)

5 met, 3 at risk, 1 not verifiable at TRL 3, **3 not met**.

| ID | Status | Value | Target |
| --- | --- | --- | --- |
| R5 | **Not met** | Burn 4.5 h (3.4 to 7.0 h); unload about 8 h after lighting | 4 h; 16 h |
| R6 | **Not met** | 6.4 MJ into water (4.9 to 9.2 MJ), about 25 K rise | 10 MJ |
| R8 | **Not met** | 5.8 kg wood (2.9 to 13.9 kg); light-up alone 1.7 kg | 5 kg |
| R2 | At risk | 28 % yield (20 to 35 %), 2.96 kg char | 25 % |
| R3 | At risk | Core at 450 °C about 4.0 h after lighting | 450 °C, 30 min |
| R9 | At risk | ±3.4 °C to 700 °C with class 1 probes; amplifier unspecified above 700 °C | ±5 °C to 1,000 °C |
| R4 | Not verifiable at TRL 3 | Gas route closed; draft 16.9 Pa, margin 3.2; throat holes 27.1 cm² against 23.6 needed | CH₄ below 24 g/kg |
| R1, R7, R10, R11, R12 | Met | 12.0 kg batch; open jacket; $298; lift 21.6 kg each for two; outlet 2.70 m | |

Other key numbers: heat released 190 MJ per batch; shell loss 5.7 kW (blanket surface 125 °C, bare lid 257 °C); kiln about 91 kg dry; net removal 2.8 kg CO₂e per batch, about 0.70 t CO₂e a year.

Numbers that changed from TRL 2: char 3.4 to 2.96 kg (ash now carried in the char, and 12 kg is air-dry, not dry); hot water about 15 to 6.4 MJ (a plain sleeve gives about 4 to 5 W/m²K, not 15); burn 2.5 to 3.5 h to about 4.5 h; wood 5 to 5.8 kg; draft 19 to 16.9 Pa; lift unit 36 to 43 kg; cost $299 to $298. The 25 mm secondary air ring would have needed about 46 Pa against about 8 Pa available, so the model uses an air shroud.

### Decisions recorded (CCB-DDR-001)

Decided by Amish, 2026-09-25, go with recommendation: (1) open-vented annular water jacket; (2) keep `budget_usd: 300` for kiln parts, safety kit required and separate (budget kept; its scope is written into R10); (3) nested-drum retort; (4) bundled straw and mixed stalks and cobs first (R1 redefined); (5) burner throat with preheated secondary air; (6) logger as standard; (7) ceramic fibre blanket; (8) tripod support; (10) keep the name. Pitch and problem lines had no recommended rewording and are unchanged. Cross-cutting SwapCell items do not apply (no SwapCell pack).

### Still awaiting Amish

- Item 9: first region, residue and partner (no recommendation; partners are chosen per area later).
- Item 11: accept the air shroud in place of the 25 mm ring (recommended). Decided by Amish, 2026-09-25: go with recommendation (CCB-DDR-002).
- Item 12: R6 shortfall. Recommended: spiral baffle insert plus a jacket blanket (about 13.9 MJ on paper, about $15), or relax R6 to 5 MJ, or drop the jacket. Decided by Amish, 2026-09-25: go with recommendation (CCB-DDR-002).
- Item 13: R8 shortfall. Recommended: blanket the lid (about $6, saves about 1.4 kW) and keep the 5 kg target until batches are logged. Decided by Amish, 2026-09-25: go with recommendation (CCB-DDR-002).
- Item 14: R5 shortfall. Recommended: relax R5 to 5 h. Decided by Amish, 2026-09-25: go with recommendation (CCB-DDR-002).
- Item 15: restate R9 as ±5 °C to 700 °C and indicative above. Decided by Amish, 2026-09-25: go with recommendation (CCB-DDR-002).
- Item 16: the safety kit requirement lives in R10 and the BOM notes, not in build notes (which are TRL 4). Decided by Amish, 2026-09-25: go with recommendation (CCB-DDR-002).
- Items 12 and 13 together would take the BOM over $300 unless a line is cut.

### Safety concerns

- Fire, hot surfaces (125 to 260 °C average outside, hotter locally) and hot char for hours; flammable, toxic pyrolysis gas; flare risk if opened hot.
- The jacket must stay open-vented. It does not boil with the plain sleeve, but it could with a baffle insert on a long burn.
- Tar and condensate will deposit on the jacket sleeve, which runs far below the tar dew point.
- Two-person lift of the 43 kg unit near hot steel; a full jacket (83 kg) must never be moved.
- Used drums, no galvanized parts, char dust and blanket fibres (dust mask).

### Problems and notes

- No TRL 4 material exists in the repo; `build-log/README.md` is the kit scaffold and was not extended. Firmware is not started.
- Citations: the TRL 2 note listed no unchecked citations. New sources in CCB-CAL-001 (Channiwala and Parikh 2002; the MAX31855 datasheet) were found by web search; the IEC 60584 thermocouple tolerances used in section 10 are quoted from general knowledge and were not checked against the standard.
- The heating-time model (a solid bed with fixed conductivity) is the largest uncertainty; it drives R3, R5 and R8.

### Recommended next step

Decide items 11 to 16, above all whether to relax R5, R6 and R8 or add the lid blanket and jacket insert. Any design change can be re-run through `sizing.py` and the model at TRL 3. TRL 4 is on hold by Amish's instruction. For reference only, TRL 4 would need: a built kiln, weighed and logged batches (core temperature, wood, char yield, water temperature), lab analysis of the char (H/Corg), smoke and ideally methane measurement with a partner lab, a test report (TST, `environment: lab`) and build log entries.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now decided by Amish, 2026-09-25: go with recommendation. They are recorded in `docs/decisions/0002-recommendations-accepted.md` (CCB-DDR-002 v0.1). TRL 4 remains on hold by Amish's instruction.

### Decisions applied and what changed

| # | Decision | Change in the repo | Before | After |
| --- | --- | --- | --- | --- |
| 11 | Air shroud in place of the 25 mm ring | Wording only; throat air holes raised to keep up with the baffle's resistance | 24 holes, 27.1 cm² (23.6 needed) | 30 holes, 33.9 cm² (28.5 needed) |
| 12 | Spiral baffle insert and jacket blanket | New parts 15 and 16 in the model, BOM ($7 and $8), drawing and media | Hot water 6.4 MJ, 25 K rise; R6 not met | 11.5 MJ (9.0 to 19.1), 45 K rise; R6 at risk |
| 13 | Lid and top band blanket, R8 target kept at 5 kg | New part 17 in the model, BOM ($6), drawing and media | Shell loss 5.69 kW; wood 5.8 kg; R8 not met | 4.47 kW; wood 3.7 kg (1.7 to 9.8); R8 at risk |
| 14 | Relax R5 to 5 h | CCB-REQ-001 R5 | Target 4 h; not met | Target 5 h; burn 4.5 h (3.4 to 7.0); at risk |
| 15 | Restate R9 to ±5 °C to 700 °C, indicative above | CCB-REQ-001 R9 | At risk | Met (±3.4 °C) |
| 16 | Safety kit stated in R10 and BOM notes, not build notes | CCB-REQ-001 R10 and `bom/bom-notes.md` wording | | |

Knock-on numbers (central): BOM 14 lines $298 to 17 lines $319; draft 16.9 to 16.7 Pa and margin 3.2 to 2.4; kiln 91 to 96 kg; lift unit 43.3 to 46.6 kg (23.3 kg each for two); heat released 190 to 160 MJ; sealed cooling 3.2 to 3.6 h; unfavourable hot water 19.1 MJ against 20.6 MJ to boiling.

Files changed: `cad/src/model.py` (parts 15 to 17, `N_AIR_HOLES` 30; STEP and STL re-exported), `cad/src/sheets.py` and `cad/drawings/CCB-DWG-001` (Rev P1 to P2), `cad/src/concept_media.py` and `media/` (concept sheet CCB-DWG-010 Rev P2; hero, blueprint, cutaway, exploded, flow, GLB viewer regenerated and checked by eye; temporary view folders deleted), `bom/bom.csv`, `bom/bom-notes.md`, `docs/04-calcs/sizing.py` and `results.csv` (re-run), CCB-CAL-001 v0.1 to v0.2, CCB-REQ-001 v0.3 to v0.4, CCB-PRC-001 v0.3 to v0.4, CCB-DDR-001 v0.1 to v0.2, new CCB-DDR-002 v0.1, `README.md` (concept numbers, key components and the four new write-up sections), `project.yaml` (DDR-002 added to the TRL evidence). `budget_usd` stays at 300 and `trl: 3`, `trl_target: 3` are unchanged. The pitch and problem lines had no recommended rewording and are unchanged. CCB-PRB-001 did not attribute the idea to any review session and is unchanged. All PDFs, drawings and media were re-rendered so none shows the old personal-site domain.

### Requirement status (CCB-CAL-001 v0.2, central estimates)

1 not met, 5 at risk, 1 not verifiable at TRL 3, 5 met.

| ID | Status | Value | Target |
| --- | --- | --- | --- |
| R10 | **Not met** | $319 | $300 kiln parts |
| R2 | At risk | 28 % (20 to 35 %), 2.96 kg | 25 % |
| R3 | At risk | Core at 450 °C about 4.0 h after lighting | 450 °C, 30 min |
| R5 | At risk | Burn 4.5 h (3.4 to 7.0 h) | 5 h (relaxed) |
| R6 | At risk | 11.5 MJ (9.0 to 19.1 MJ) | 10 MJ |
| R8 | At risk | 3.7 kg (1.7 to 9.8 kg) | 5 kg |
| R4 | Not verifiable at TRL 3 | Draft margin 2.4; 30 throat holes with 19 % spare area | CH₄ below 24 g/kg |
| R1, R7, R9, R11, R12 | Met | 12.0 kg batch; open jacket; ±3.4 °C to 700 °C; 23.3 kg each for two; outlet 2.70 m | |

### Still awaiting Amish

- Item 9: first region, residue and partner (no recommendation; partners are chosen per area later).
- Item 17 (new): R10 is over budget after items 12 and 13 ($319 against $300). Options: (a) raise `budget_usd` to $320 for kiln parts; (b) cut a line, for example clay and ash render instead of the side blanket; (c) drop the jacket blanket. Recommendation: (a), since (b) and (c) undo part of a decided item. Not applied, because raising a budget needs Amish's decision.

### Cross-repo actions

None. CharCube does not use SwapCell or any other portfolio module, and no decision here needs a change in another repo.

### Safety concerns

- The baffle and jacket blanket bring the water close to boiling on a long burn (19.1 MJ against 20.6 MJ). The vent must never be closed and the jacket must be kept at least three-quarters full.
- Tar and soot collect on the baffle; it lifts out with the flue only when cool.
- The lid blanket must stay clear of the air shroud intake, or the throat will starve of secondary air.
- The lift unit is now 46.6 kg (23.3 kg each for two people), close to the 25 kg per person limit.
- Ceramic fibre and mineral wool need a dust mask when cut.

### Problems and notes

- The factor of 3 on gas-side convection and the 4 velocity heads of loss for the baffle insert are assumptions, not sourced figures; they need measurement.
- The lid blanket saves 1.22 kW, a little less than the 1.4 kW estimated in CCB-CAL-001 v0.1, because the lid under the shroud stays bare.
- The 30-hole throat is a consequence of item 12, not a separate decision; it is recorded in CCB-DDR-002 under item 11.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No build, test, purchase, PCB or firmware work was done. For reference, TRL 4 would measure the baffle's heat transfer and fouling, wood use, char yield and emissions on logged batches.

### Recommended next step

Decide item 17 (budget). Item 9 stays open until co-design partners are chosen per area.
