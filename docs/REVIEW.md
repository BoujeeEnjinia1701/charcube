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
- Item 17 (new), **decided by Amish, 2026-09-26: budget top-up to $320** (see Session 2026-09-26 below): R10 is over budget after items 12 and 13 ($319 against $300). Options: (a) raise `budget_usd` to $320 for kiln parts; (b) cut a line, for example clay and ash render instead of the side blanket; (c) drop the jacket blanket. Recommendation: (a), since (b) and (c) undo part of a decided item. Not applied, because raising a budget needs Amish's decision.

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

Decide item 17 (budget); decided 2026-09-26. Item 9 stays open until co-design partners are chosen per area.

## Session 2026-09-26: sources strengthened

Amish asked on 2026-09-26 to "fix the weaker sources" and wrote "I am ok with the budget top ups."

### Sources replaced

| Item | Old source | New source |
| --- | --- | --- |
| Brazil (São Paulo) row | Instituto Escolhas article (NGO summary) | Text of State Law 11,241 of 2002 on the Assembleia Legislativa do Estado de São Paulo site, plus the state Instituto de Economia Agrícola (2014) for the 2021 and 2031 deadlines, which the row now states |
| United States (California) row | FindLaw copy of Health and Safety Code 41865 | Statute text as published by the Glenn County Air Pollution Control District (subdivisions (c)(4) and (i): 25 % of planted acres from 2001) |
| East Africa row and What sparked the idea | IDEAS/RePEc listing of Adam (2009) | Publisher DOI 10.1016/j.renene.2008.12.009 (Elsevier, *Renewable Energy* 34(8)); also in CCB-PRB-001 (v0.3 to v0.4) |
| Kenya and East Africa row | Uncited "maize and cotton stalks" claim | Row renamed East Africa and limited to what Adam (2009) supports (pilot units in East Africa) |
| Vietnam and Southeast Asia row | Van Hung et al. (2020), kept | Row renamed Southeast Asia and reworded to what the chapter supports (100 to 140 Mt of straw a year in the region, short turnaround, burning despite bans) |
| Europe row | "(Switzerland, Germany)" uncited | Label shortened to Europe; European Biochar Certificate link kept |
| What sparked the idea | "masonry kiln ... surplus heat goes to waste" not in the source | Replaced by "It was built for wood charcoal" |

Checked and kept: Lan et al. (2022, *Nature Communications*), the WHO ambient air quality fact sheet, Sparrevik et al. (2015, *Biomass and Bioenergy*) and Van Hung et al. (2020). The European Biochar Certificate page is the program's own site; it could not be re-fetched this session. The inspiration event (Adam retort) is unchanged, now linked to the publisher's DOI.

### Budget change

Budget top-up to $320: decided by Amish, 2026-09-26 (CCB-DDR-002 v0.2, item 17). `project.yaml` `budget_usd` 300 to 320. `docs/04-calcs/sizing.py` now reads the budget from `project.yaml`; re-run, `results.csv` updated. R10 is met with a $1 margin ($319 against $320); requirement status is now 6 met, 5 at risk, 1 not verifiable at TRL 3, none not met. Documents: CCB-REQ-001 v0.4 to v0.5, CCB-CAL-001 v0.2 to v0.3, CCB-PRC-001 v0.4 to v0.5, CCB-DDR-002 v0.1 to v0.2, CCB-PRB-001 v0.3 to v0.4 (sources). README budget line and concept paragraph updated; `bom/bom-notes.md` updated. The budget note on CCB-DWG-001 and the key figures on the concept sheet CCB-DWG-010 were updated in `cad/src/sheets.py` and `cad/src/concept_media.py` (both Rev P2 to P3) and all drawings and media regenerated; temporary view folders deleted. `trl: 3` and `trl_target: 3` unchanged.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders; no design, sizing or BOM content changed.

### What was done

- `cad/src/product_model.py` (new): `product_parts()` returns 49 parts (47 product parts in the shell and internal groups, 2 context parts) with colour, material, BOM line, group and explode offset, plus `TITLE` and `RENDER_VIEWS` (hero, exploded and a detail view without the ground and person). It imports `PARAMS`, `levels()` and `build_parts()` from `cad/src/model.py`, so every main dimension, height and interface is unchanged. It adds:
  - outer drum chimes and rolling hoops, and sliding port dampers with knobs on the four primary air ports;
  - the drum blanket with a wire mesh, overlap flap, a teal name band and a hot-surface label; the lid blanket with tie wires;
  - riveted lid collar with a rolled edge, a band damper handle on the air shroud, a rolled flue outlet and a conical rain cap on the three posts;
  - the water jacket painted in the kit accent, with its loose lid, open vent rim, mineral wool blanket with tie wires and a second hot-surface label, and a brass ball-valve tap with a lever;
  - tripod legs drawn as 40 x 40 x 4 mm angle on a flat-bar ring seat, with bolted gussets, foot plates and ground pins;
  - retort rolling hoops, lid swages and a bolt-ring clamp bolt; chamfered firebricks; block joints and an ash pan lip on the plinth;
  - the logger as a weatherproof box with a clear window over its board, modules and power bank, a lit green status light, cable glands, straps to the leg, probe cables and type K probes;
  - context: a compact paved ground patch and the shared clay mannequin (1.75 m, "stand") beside the kiln.
- `README.md`: hero image now `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced later by the orchestrator.
- Self-check previews (matplotlib, clear parts omitted) were made outside the repo.

### Differences from model.py

Each is an appearance choice only; model.py, the drawing and the BOM are unchanged.

1. **Rain cap shape.** model.py draws a 260 mm square plate; the appearance model draws a 260 mm conical cap on the same three posts at the same height. Proposed, awaiting Amish. Recommendation: adopt the conical cap in model.py and CCB-DWG-001 at the next model update, since the BOM does not fix the shape and a cone sheds rain better.
2. **Tripod leg and ring seat sections.** model.py draws round stand-ins (28 mm round legs and a 20 mm round ring seat); the appearance model draws the BOM section: 40 x 40 x 4 mm angle legs, a flat-bar ring seat just under the jacket, and bolted gussets. Foot and top points are unchanged. Proposed, awaiting Amish. Recommendation: carry the angle section into model.py so drawings and renders agree.
3. **Logger position.** model.py centres the logger box on the tripod leg, so the leg passes through it; the appearance model puts the box on the front face of the same leg, 62 mm toward -Y, strapped to it, at the same height. Proposed, awaiting Amish. Recommendation: move the box in model.py to the same position.
4. **Tap lever.** model.py draws the handle as a 90 mm bar above the valve; the appearance model draws a ball-valve lever across the pipe (closed position) at the valve body. Proposed, awaiting Amish. Recommendation: keep the model.py envelope for drawings; no action needed.
5. **Added detail not in model.py** (port dampers, name band, hot-surface labels, rivets, bolts, logger internals, straps): all belong to existing BOM lines (1, 13 and 14). The name band and labels are not priced in the BOM. Proposed, awaiting Amish. Recommendation: add hot-surface labels to line 14 (hardware and consumables) when the BOM is next revised; they cost little and support the safety section.

### Safety

The renders show hot-surface labels on the drum blanket and the jacket blanket and the open, uncapped jacket vent, consistent with the safety section of the design precis. They are illustrative; the labels are not a specified safety sign set.

### TRL

This is an appearance model only, with no tolerances or fabrication detail. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-09-30: design made constructable and prototype build plan (kit 1.7.0)

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Constructability review of every component with build123d. `cad/src/model.py` now builds each component as it is made and fitted (`build_components()`) and runs 68 checks of contacts, clearances and overlaps (`python cad/src/model.py --check`): 68 of 68 pass. STEP and STL regenerated.
- `docs/decisions/0003-design-for-construction.md` (CCB-DDR-003 v0.1, Draft): twelve changes, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/05-build-plan.md` (CCB-BLD-001 v0.1): the illustrated prototype build plan, 21 components in build order, 19 assembly steps, first checks, safety stops. Pictures from `cad/src/build_plan_media.py`: overview, 14 making sketches (`cad/drawings/CCB-DWG-101` to `114`), 11 joint close-ups and 19 step pictures in `docs/05-build-plan/`.
- `docs/06-design-decisions.md` (CCB-DEC-001 v0.1): open decisions, items to confirm when parts are bought, and decisions made.
- Calculations re-run: CCB-CAL-001 v0.4 (`docs/04-calcs/sizing.py` now takes the tripod geometry from the model). CCB-PRC-001 v0.6, CCB-REQ-001 v0.6, `bom/bom.csv` and `bom/bom-notes.md` updated. CCB-DWG-001 Rev P5; concept sheet CCB-DWG-010 Rev P4; concept media and `media/model.glb` regenerated.
- `project.yaml`: `design_state: constructable`; the build plan, the register and CCB-DDR-003 added to `trl_evidence`. README: links line and a "Building the prototype" section.

### Design changes made for construction (CCB-DDR-003)

1. Plinth blocks laid as a pinwheel, 580 mm square (they overlapped by 50 mm).
2. Lid hole 150 mm; the throat stands on the lid inside a collar rolled to fit it, riveted to the lid by six tabs and to the throat by four rivets (the throat could drop through the 160 mm hole).
3. Air shroud riveted to the throat by six tabs; band damper 60 mm with a wing screw (no fixing; the band floated and could not close the intake).
4. Port dampers modelled as curved plates sliding in riveted guide strips (listed but not drawn or held).
5. Firebricks laid round the retort's edge, 200 mm out, 8 mm clear of the gas holes (they covered gas holes).
6. Two M8 U-bolt handles on the retort lid (no way to lift the retort out of a 43 mm gap).
7. Jacket stand: three fins welded to the jacket, angle legs bolted flat to them, pinned at bolted foot cleats and pads; ring seat removed (the ring was 7 mm below and outside the jacket, so nothing carried it).
8. Flue 650 mm on three stop clips resting on the sleeve rim; rain cap on three riveted legs, 60 mm above the outlet (no seat for the flue; cap posts inside the bore; cap 10 mm above the outlet at 2.75 m).
9. Baffle hung on a 10 mm rod through the flue foot (the cross bar cut into the flue wall).
10. Jacket loose lid resting on the rim on three tabs, with a 210 mm centre hole and the vent nipple through it (lid and vent floated).
11. Logger box strapped beside the leg (the leg passed through it).
12. Core probe 500 mm in through the drum side and a retort slot; throat probe below the sleeve (the probe could not be inserted or reach the core).

### Key results

- Masses (CCB-CAL-001 v0.4): kiln 97 kg (was 96 kg); lift unit 47.4 kg, 23.7 kg each for two (was 46.6 kg); retort with char 15.5 kg; full jacket 85 kg. R11 still met with 1.3 kg per person to spare. Tripod leg buckling factor 58.
- Flue outlet stays 2.70 m. Draft margin 2.4, secondary hole area 33.9 cm² against 28.6 cm² needed. Heat to water unchanged at 11.5 MJ.
- No requirement changed status: six met, five at risk (R2, R3, R5, R6, R8), one not verifiable at TRL 3 (R4). R10 is within the $320 value-engineering target only on the unchanged prices ($319 estimated); the added parts are not priced.

### Proposed, awaiting Amish

All in the design decisions register (CCB-DEC-001): accept CCB-DDR-003 (1); concrete blocks under the hot drum floor (2); flared sleeve bottom to guide the jacket onto the throat (3); two-person lift or a swinging arm (4); first region and partner (5); conical rain cap (6); hot-surface labels in the BOM (7). The register's Value engineering section holds the $320 target, the $319 estimate and the savings worth trying.

### Safety concerns

- The plinth's concrete blocks sit under the fire below the retort; their temperature is a first check.
- Lowering the 47 kg heat-recovery unit onto the throat with 2 mm clearance at about 1.5 m is the hardest handling step; it needs two people and a drained jacket.
- Both probes must be pulled out before the retort or the heat-recovery unit is moved.

### Stale media

The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and `cad/src/product_model.py` still show the concept's ring seat, round rain cap posts and the logger through the leg. They are made on Amish's Mac and were not regenerated here.

### TRL

`trl: 3`, `trl_target: 3`. The build plan is TRL 3 paper work; nothing was built, bought or tested. TRL 4 remains on hold by Amish's instruction.

### Recommended next step

Amish to review CCB-DDR-003 and decide the open items in CCB-DEC-001; then refresh the photoreal renders on the Mac.

## Session 2026-10-02: open decisions decided by Amish

Authority: Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." The recommendations approved are those written for the open decisions in the design decisions register. No model, BOM quantity or price, or picture was changed; where a decision needs one, it is listed below as a follow-up. `trl` and `trl_target` stay at 3. No commit or push.

### Decisions recorded

7, all moved to "Decisions made" in `docs/06-design-decisions.md`, dated 2026-10-02:

1. Design for construction (CCB-DDR-003) accepted: all twelve changes, with the first burn to confirm that the 150 mm lid hole does not limit draft.
2. Plinth: 25 mm ceramic fibre board between pan and blocks from the first burn, with a thermocouple on a block; dropped later only if a measured burn keeps the blocks under about 150 °C.
3. Jacket sleeve: bottom 20 mm flared to about 190 mm.
4. Heat-recovery unit: a lifting aid (swinging arm on a post or hand winch) designed for the first build; users asked how it should work.
5. First region, residue and partner: selection rule set (open straw burning, partner already running residue or biochar trials); first candidate to approach an agricultural university extension service such as Punjab Agricultural University.
6. Rain cap: conical cap adopted in the model and drawings.
7. Hot-surface labels (ISO 7010 W017) for the drum blanket and jacket added to BOM line 14.

### Documents changed

- `docs/06-design-decisions.md` (CCB-DEC-001 v0.3)
- `docs/decisions/0003-design-for-construction.md` (CCB-DDR-003 v0.3): accepted; A2 and A3 recorded; status stays Draft
- `docs/02-concept.md` (CCB-PRC-001 v0.8): lifting aid, fibre board, labels, conical cap, partner rule
- `docs/03-requirements.md` (CCB-REQ-001 v0.8): R11 note on the lifting aid
- `bom/bom.csv`: notes on lines 7, 12 and 14 only; no quantity or price changed

### Follow-up actions to carry approved decisions into the design

1. Decision 2 (model): Add the 25 mm ceramic fibre board between the ash pan and the blocks in `cad/src/model.py` and check the raised kiln (port height, flue outlet height, contacts); regenerate CCB-DWG-001 and the plinth making sketch.
2. Decision 2 (pictures): Show the fibre board and the block thermocouple in build plan section 3.1 and its first checks.
3. Decision 2 (bom): Add the fibre board to the BOM line 12 spec and price, and a block thermocouple to line 13.
4. Decision 3 (model): Flare the bottom 20 mm of the jacket sleeve to about 190 mm in the model, the jacket making sketch and build plan section 3.11, step 15.
5. Decision 4 (model): Design the lifting aid (a swinging arm on a post or a hand winch) for the heat-recovery unit in the model and drawings.
6. Decision 4 (pictures): Show the lifting aid in build plan sections 3.15 and 3.16.
7. Decision 4 (bom): Add the lifting aid to the BOM with a price.
8. Decision 4 (calcs): Check the lifting aid's loads and re-judge R11 and R10 in CCB-CAL-001.
9. Decision 6 (model): Model the conical rain cap on the three flat-bar legs and 60 mm gap; regenerate CCB-DWG-001, the flue making sketch and build plan section 3.18; update the BOM line 7 spec.
10. Decision 7 (bom): Add the hot-surface warning labels to the BOM line 14 spec and price, and show them in build plan section 3.21.
11. Decision 1 (calcs): Price the parts added for construction and the additions decided on 2026-10-02, and re-state the value-engineering result in CCB-CAL-001, section 11.

### Points found in the review

- Value engineering is not like for like: the USD 319 estimate leaves the parts added for construction unpriced (about USD 5 to 10), and items 2, 4 and 7 as recommended add more. Price them before reading the result against the USD 320 target.
- R11 (no lift above 25 kg per person) ignores lift height and the reduced capacity of team lifts; the 47 kg unit lifted to about 1.5 m meets the letter of R11 but not common manual-handling guidance.
- The register still describes the rain cap as resting on 'posts'; the design for construction replaced them with three riveted flat-bar legs.

## Session 2026-10-02: Approved follow-ups carried out

Authority: Amish, 2026-10-02: "497 follow-up actions that need CAD, drawing, picture, BOM or calculation work ... APPROVED CHANGES, COMPLETE THESE", and "Photoreal renders are out of date in most repos ... COMPLETE THESE" (render scenes prepared here; photoreal images, `media/card.png` and `media/social-preview.png` are made on Amish's Mac). `trl` and `trl_target` stay at 3. No commit or push.

### Follow-ups

1. Decision 2 (model): done. A 600 x 600 x 25 mm ceramic fibre board now lies between the blocks and the pan, with a groove in its underside for the block thermocouple. The kiln rises 25 mm: drum floor 218 mm, air ports clear of the board by 13 mm, flue outlet 2.72 m (was 2.70 m), kiln 2.84 m to the top of the cap; all contacts re-checked. CCB-DWG-001 (Rev P6) and the plinth making sketch CCB-DWG-101 regenerated.
2. Decision 2 (pictures): done. Build plan section 3.1, Figures 2 and 3 (joint 1), step 1 and the first checks (block temperature from the block thermocouple, logger check on three channels).
3. Decision 2 (BOM): done. Line 12 $12 to $40 (board $28); line 13 $32 to $42 (bare-wire type K and a third amplifier, $10).
4. Decision 3 (model): done. The bottom 20 mm of the jacket sleeve is a cone flaring to 190 mm; CCB-DWG-108, joint 5 and build plan section 3.11 (and step 15) updated. Two 18 mm lift-bar holes added to the top socket for item 5.
5. Decision 4 (model): done. Lifting aid designed and modelled (BOM line 18): a post of 88.9 x 3.2 mm tube, 4.0 m above the ground, turning in a ground sleeve in a 600 x 600 x 750 mm footing 1.2 m behind the kiln; a bolted arm of two 50 x 50 x 5 mm angles with a 40 x 40 x 4 mm brace; two pulleys, a 270 kg hand brake winch, 5 mm steel wire rope and a hook; a 16 mm lift bar through the sleeve socket. It raises the drained unit 1.55 m (feet above the throat top), so the unit clears the kiln on any path, and swings it a quarter turn to set it down. New making sketches CCB-DWG-115 and CCB-DWG-116; shown on CCB-DWG-001.
6. Decision 4 (pictures): done. Build plan new section 3.22 (Figures 28 to 31, joints 12 and 13), notes in sections 3.15 and 3.16, step 15 picture and text, step 18, safety stop S4, first checks, tools and workspace.
7. Decision 4 (BOM): done. Line 18, $160, priced item by item in its notes.
8. Decision 4 (calcs): done. CCB-CAL-001 section 4, Table 4a: post stress factor 4.3 on yield, top deflection about 46 mm, arm factor 4.1, brace buckling factor 51, lift bar factor 3.2, winch and rope factors 3.8 and 21, footing overturning factor 2.1 by weight alone. R11 re-judged: met, nobody carries the unit; heaviest hand lift the retort with char, 15.5 kg (setting up: post about 16 kg each for two). R10 re-judged: not met.
9. Decision 6 (model): done. Conical cap (260 mm, 30 degree slope, 1.5 mm sheet) on the three flat-bar legs, at least 60 mm from the flue lip; CCB-DWG-001, CCB-DWG-112, CCB-DWG-113, joint 9, build plan section 3.18 and BOM line 7 updated.
10. Decision 7 (BOM): done. Line 14 $15 to $26 (two 100 mm aluminium W017 labels, $8, and $3 of fasteners added for construction); labels modelled at the front right of both blankets and shown in build plan section 3.21 (Figure 27, joint 14).
11. Decision 1 (calcs): done. Every BOM line priced with its basis; CCB-CAL-001 section 11 restated: Value-engineering target: USD 320. Estimated cost of the constructable design: USD 546 (USD 226 over the target). Parts added for construction $17; 2026-10-02 additions $186 (lifting aid $160). `budget_usd` unchanged.

### Requirement status changes

- R10: met to **not met** ($546 against $320).
- R11: stays met, re-judged on the lifting aid (was 23.7 kg each for two people).
- No other change: met 5 (R1, R7, R9, R11, R12), at risk 5 (R2, R3, R5, R6, R8), not verifiable 1 (R4), not met 1 (R10). Outlet 2.72 m; tripod leg factor 56; heat to water and draft unchanged (11.5 MJ; margin 2.4).

### Cost and mass

Estimated cost $546 (18 lines). Kiln 97 kg without plinth and water; heat-recovery unit 47.2 kg (was 47.4 kg, lighter cap); fibre board 2.9 kg; lifting aid post 32 kg and arm, brace, pulleys and winch 23 kg, plus a 621 kg concrete footing.

### Documents changed (new versions)

- `cad/src/model.py`: fibre board, block thermocouple, sleeve flare and lift-bar holes, conical cap, labels, lifting aid; 100 of 100 constructability checks pass (was 68). STEP and STL regenerated, with a new `charcube-lifting-aid` unit.
- `bom/bom.csv` (18 lines, $546) and `bom/bom-notes.md`.
- `docs/04-calcs/sizing.py` and `results.csv`; `docs/04-calcs/01-sizing.md` CCB-CAL-001 v0.6.
- `docs/03-requirements.md` CCB-REQ-001 v0.9; `docs/02-concept.md` CCB-PRC-001 v0.9; `docs/06-design-decisions.md` CCB-DEC-001 v0.4 (Value engineering section); `docs/05-build-plan.md` CCB-BLD-001 v0.2; `README.md`.
- Drawings and pictures: CCB-DWG-001 Rev P6 (now 1:50, footing left off); concept media CCB-DWG-010 Rev P5 (`media/hero.png`, `concept-blueprint`, `cutaway.png`, `exploded.png`, `flow.png`, `model.glb`); build plan overview, all 19 step pictures, joints 1, 5, 9, 12 (new), 13 (new), 14 (new); making sketches CCB-DWG-101, 108, 112, 113, 115 (new), 116 (new).
- `cad/src/product_model.py`: brought to the constructable design (fins, bolted legs and pads, clips, conical cap on legs, pinwheel plinth with board, flared sleeve, logger and probes from the model) with every main dimension from `model.py`; the lifting aid is a new `site` group with a new `site` view (hero, exploded and detail kept). Render scenes exported to `/home/claude/renders/charcube` (hero, exploded, detail, site; `.npz` and `.json` each, and `charcube__jobs.json`).
- `drawing.py --check-text`: no hits.

### Not done

- Asking users through the partner how the lifting aid should work (decision 4): not done: outreach by Amish.
- Photoreal renders, `media/card.png` and `media/social-preview.png`: not done here by instruction; made on Amish's Mac from the exported scenes.

### Cross-repo actions

None.

### Proposed, awaiting Amish

- Whether the lifting aid ($160) counts against the kiln parts target or is site equipment listed beside the safety kit (it can serve several kilns). Recommendation: list it as site equipment; the kiln estimate would then be $386, still $66 over.
- Cheaper alternative to try: a winch hung from an existing strong beam or tree where a site has one.

### Safety

- The unit hangs 1.55 m up while it is swung: S4 now requires the winch only, the flue out first, and nobody under the load. The post's top moves about 46 mm under full load; the first check holds the unit 100 mm up for 5 minutes before a full lift.
- The arm is parked away from the flue during burns.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, site, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.

## 2026-10-03: decisions recorded

Amish decided on 2026-10-03: "Cost over target - i accept all the cost variations and overruns". Recorded for this repo: the estimated cost of USD 546 against the USD 320 target (USD 226 over), with the lifting aid (USD 160) counted in the kit cost as it stands.

- `docs/06-design-decisions.md`: row added to decisions made; value engineering section says the overrun was accepted by Amish on 2026-10-03.
