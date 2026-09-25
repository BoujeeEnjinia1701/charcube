---
doc_id: CCB-PRC-001
title: CharCube design precis
project: CharCube
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, first-order numbers, design choices, safety, media)
---

# CharCube design precis

CharCube is a batch retort kiln made from a 114 L (30 US gal) steel drum sealed inside a 200 L (55 US gal) drum. Crop residue packed into the inner drum (the retort) is heated without air; the gas it gives off escapes through holes in the retort base and burns in the gap between the drums, which keeps the process going. The flame and any unburned gas then pass through a burner throat fed with secondary air, and the hot flue gas rises through an open-vented water jacket of about 60 L before leaving a flue about 2.7 m above the ground. First-order estimates: about 12 kg of dry residue per batch gives about 3.4 kg of biochar and about 60 L of water heated by about 60 K, and the parts cost about $299 against the $300 budget.

![Hero render](../media/hero.png)

*Figure 1. CharCube on its block plinth with the jacket tripod, beside a 1.75 m person for scale. Massing model.*

## How it works

1. **Load.** The retort is packed with about 12 kg of dry residue (bundled straw, stalks, cobs or prunings), its lid is clamped on, and it stands upright on three firebrick standoffs inside the outer drum. The outer lid, carrying the burner throat, goes on top, and the tripod carrying the drained jacket and flue is set over it so the flue sits on the throat.
2. **Light.** About 5 kg of dry wood is lit in the 54 mm annulus around the retort and in the space beneath it. Primary air enters through four ports near the base of the outer drum.
3. **Pyrolysis.** After about 30 to 45 min the retort contents pass about 300 °C and start to release gas and tar vapor. The gas leaves through holes in the retort base, meets the fire and burns, so the wood fire can die down while the retort gas keeps the kiln hot. The target is a retort core of 450 to 600 °C for at least 30 min.
4. **Clean-up burn.** Everything leaving the outer drum passes the burner throat, a 160 mm steel pipe 400 mm long. A ring manifold admits preheated secondary air through holes in the throat wall, so gas that escaped the annulus fire burns there instead of leaving as smoke and methane.
5. **Heat recovery.** The hot gas (estimated 500 to 700 °C at the throat exit) rises through the flue, which passes through the centre of an annular water jacket. Heat conducts through the flue wall into the water. The jacket is open at the top, so it cannot build pressure. Hot water is drawn from a tap at its base.
6. **Finish and cool.** When the flame at the throat dies back (about 2.5 to 3.5 h after lighting, estimate), the primary ports and secondary damper are closed and the kiln is left sealed overnight. The char cools without air, so it does not burn away.
7. **Unload and log.** Next morning the tripod unit and lid are lifted off, the retort (about 15 kg with its char) is lifted out, and the char is tipped out, quenched or wetted, weighed and crushed. A two-channel thermocouple logger records the retort core and the throat exit every 10 s, giving a record of peak temperature and time at temperature for each batch.

![Energy flow](../media/flow.png)

*Figure 2. Energy per batch. All values are estimates: 12 kg of residue at 15 MJ/kg plus 5 kg of start-up wood at 16 MJ/kg, 3.4 kg of char at about 24 MJ/kg, and about 19 % of the flue gas heat recovered by the jacket.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 4.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Outer drum (firebox shell) | 200 L open-head steel drum, about 572 mm diameter x 851 mm, four 40 x 110 mm primary air ports with sliding dampers | Used drum; must have held a non-flammable, non-toxic product and be burned clean of paint before use |
| 2 | Outer lid with flue collar | The drum's own lid with a 160 mm collar | Sealed with ceramic gasket rope and the drum's locking ring |
| 3 | Inner retort | 114 L open-head steel drum, about 463 mm diameter x 737 mm, bolt-ring lid, eight 20 mm gas holes in the base | Holds the feedstock; replaced when it scales through (estimate 50 to 100 batches) |
| 4 | Firebrick standoffs | Three half firebricks, 60 mm high | Leave room for fire under the retort |
| 5 | Secondary air manifold | 25 mm steel pipe ring around the throat base, inlet pipe with a sliding damper | Air is preheated by the throat wall |
| 6 | Burner throat (afterburner) | 160 mm plain steel pipe, 400 mm long, with a ring of 10 mm air holes | The flue sits on its top end with a loose slip fit |
| 7 | Flue pipe with rain cap | 160 mm plain (not galvanized) steel, 1.2 m, rain cap | Outlet about 2.7 m above the ground |
| 8 | Water jacket | Annular steel tank, 420 mm outside diameter x 600 mm, about 60 L, open top with a loose lid and vent pipe | The one welded, water-tight part; local fabricator |
| 9 | Draw-off tap | 1/2 in brass ball valve with a short nipple | Drains the jacket before moving it |
| 10 | Jacket support tripod | Steel angle or pipe tripod with a ring seat | Carries the jacket and flue so the drum lid carries no water load |
| 11 | Insulation blanket | 25 mm ceramic fibre blanket held by wire mesh, air ports left clear | Keeps the annulus hot and the outer surface cooler |
| 12 | Plinth | Four concrete blocks and a steel ash pan | Lifts the air ports clear of the ground and keeps embers off it |
| 13 | Thermocouple logger | Two type K probes (retort core, throat exit), two MAX31855 amplifiers, a small microcontroller and microSD card, USB power bank | Mounted on a tripod leg, away from the heat |

Item 14 (fasteners, gasket rope, high-temperature sealant) is in the BOM but not modelled.

![Cutaway](../media/cutaway.png)

*Figure 3. Section looking from the front: retort (3) inside the outer drum (1) with the gas annulus between them, insulation (11) outside, lid (2) and burner throat (6) above, then the water jacket (8) around the flue (7).*

## First-order numbers

All values are estimates for concept review and will be checked by calculation at TRL 3. Assumptions: air-dry residue at 10 to 15 % moisture; packed bulk density 120 kg/m³ (bundled straw or mixed stalks; loose straw is far lower); higher heating value 15 MJ/kg for residue (rice straw is 14.1 to 15.1 MJ/kg per [Van Hung et al. 2020](https://link.springer.com/chapter/10.1007/978-3-030-32373-8_1)), 16 MJ/kg for air-dry wood and about 24 MJ/kg for high-ash char.

Table 2. Batch, energy, carbon and cost.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Retort usable volume | about 100 L | 114 L drum less head space | |
| Feed per batch | about 12 kg dry | 100 L at 120 kg/m³ | R1 met for packed feed; **not met** for loose chopped straw (about 4 kg at 40 kg/m³) |
| Biochar yield | about 28 % (range 20 to 35 %) | Retorts 30 to 42 % on wood ([Adam 2009](https://ideas.repec.org/a/eee/renene/v34y2009i8p1923-1925.html)); flame curtain 22 ± 5 % ([Cornelissen et al. 2016](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0154617)); straw's high ash and fine structure put it lower than wood | R2 at risk |
| Biochar per batch | about 3.4 kg (2.4 to 4.2 kg) | 12 kg x 28 % | |
| Start-up wood | about 5 kg | Retorts need ignition fuel ([Sparrevik et al. 2015](https://www.sciencedirect.com/science/article/abs/pii/S0961953414005170)) | R8 at the limit |
| Batch time | about 2.5 to 3.5 h burning, then 10 to 14 h sealed cooling | Small drum retort practice; to be logged | R5 met on estimate |
| Heat released in the kiln | about 180 MJ, about 17 kW average over 3 h | 260 MJ in, 80 MJ left in the char | |
| Stack draft | about 19 Pa | 2.45 m from air ports to flue outlet, 600 °C mean gas, 20 °C air | Enough for about 2 m/s in a 160 mm flue |
| Heat to water | about 15 MJ (range 10 to 25 MJ) | 0.30 m² flue wall in the jacket, about 15 W/m²K, about 400 K difference, about 2.5 h | R6 met on estimate |
| Water temperature rise | about 60 K for 60 L (20 to 80 °C) | 15 MJ / (4.19 kJ/kg K x 60 kg) | Above 20 MJ the jacket reaches boiling; see Safety |
| Organic carbon in the char | about 55 % (IPCC default 49 % for rice straw char, 65 % for herbaceous) | [IPCC 2019](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch02_Ap4_Biochar.pdf) | |
| Carbon stored for 100 years per batch | about 1.5 kg C, about 5.4 kg CO₂ | 3.4 kg x 0.55 x 0.80 (IPCC medium-temperature factor) | |
| Methane penalty per batch | about 2.3 kg CO₂e at the retort field average; less if the burner works as intended | 24 g CH₄ per kg char ([Sparrevik et al. 2015](https://www.sciencedirect.com/science/article/abs/pii/S0961953414005170)), GWP100 of 28 | R4 unverified |
| Net 100-year removal per batch | about 3 to 5 kg CO₂e | Carbon stored less methane; start-up wood assumed from residues | |
| Per year, 250 batches | about 850 kg biochar, about 0.8 to 1.4 t CO₂e, about 3 t of residue kept out of open burning | | Small against field-scale residue (see CCB-PRB-001) |
| Mass | about 85 kg without plinth and water; heaviest single parts the outer drum (about 18 kg) and the jacket (about 16 kg empty, about 76 kg full); tripod, jacket and flue unit about 36 kg empty | Drum and sheet weights | R11 met only if the jacket is drained and the tripod unit is lifted by two people |
| Height | about 2.7 m to the rain cap; footprint about 1.4 m across the tripod feet | Massing model | R12 met |
| Parts cost | about $299 | Indicative prices, see `bom/bom.csv` | R10 met with about $1 margin; excludes safety equipment |

## Key design choices

All are proposed, awaiting Amish.

- **Nested-drum retort rather than a flame-curtain kiln.** A Kon-Tiki cone costs less and needs no start-up wood, but it is open, its heat cannot be recovered and its yield on straw is lower. The retort encloses the feedstock, so the gas can be routed through a burner and a jacket. Recommendation: nested-drum retort.
- **Annular water jacket on the flue rather than the copper coil in the scaffold.** The scaffold listed a copper coil heat exchanger. A coil in the flue needs a separate tank above it for thermosiphon flow (a 100 L tank at about 2 m height) or a pump, and the coil can steam or crack if flow stops. A jacket around the flue holds its own water, needs no pump or hose, and is open to the air, so it cannot build pressure. It costs about the same and needs one welded part. Recommendation: annular jacket; keep the coil as an alternative for users who want water piped to a separate tank.
- **Burner throat with preheated secondary air.** Burning the gas in the annulus alone leaves smoke at light-up and at the end of a batch. A short throat with a secondary air ring gives a second chance to burn it, and heats the flue gas before the jacket. Recommendation: include it; tune hole size at TRL 3.
- **Jacket carried on a tripod, not on the drum lid.** A full jacket weighs about 76 kg, too much for a drum lid at 500 °C. The tripod carries it, and the drained tripod, jacket and flue unit (about 36 kg) is lifted aside by two people to load and unload the retort. A hinged or swinging arm would avoid the lift but adds cost. Recommendation: tripod for the prototype.
- **Target feedstock.** Stalks, cobs and prunings pack at 120 kg/m³ or more; loose straw does not. Recommendation: design for bundled straw and mixed stalks first, and treat a straw press as a separate idea.
- **Temperature logging as standard.** Adds about $32 but gives each batch a record of peak temperature, which decides whether the char is stable (IPCC high, medium or low temperature class) and is the first evidence any certification would ask for. Recommendation: include it.
- **Insulation blanket.** About $35 for faster heat-up, less start-up wood and a cooler outer surface. A local clay and ash render could replace it for about $10 at some loss of performance. Recommendation: blanket for the prototype.
- **Budget.** Parts are about $299 against $300, with no allowance for safety equipment (see Safety). Options are listed in `docs/REVIEW.md`. Proposed, awaiting Amish.

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with BOM numbers.*

## Safety

> **Safety:** CharCube is a fire. The drum surfaces, lid, throat and flue reach 300 to 700 °C, and the char stays hot enough to reignite for many hours. Run it outdoors only, on bare soil or paving, at least 5 m from buildings, fences, dry vegetation and residue piles, never under trees or roofs, and never during a local burning ban or high wind. Keep a fire extinguisher or at least 50 L of water and a shovel at hand, keep children and animals outside a marked 3 m circle, and wear heat-resistant gloves, eye protection and closed shoes.

> **Safety:** Pyrolysis gas is flammable and toxic (carbon monoxide, hydrogen, methane and tar vapor). Never open the retort or the outer lid while the kiln is hot: air entering a hot retort can ignite the gas suddenly and throw flame. Do not stand over the flue or downwind of the throat, never run the kiln in or near an enclosed space, and stop a batch that smokes heavily rather than leaving it.

> **Safety:** The water jacket can reach boiling on a hot batch. It must stay open to the air: never plug the vent or fit a sealed lid, and never connect it to household plumbing or a closed tank. Keep it at least three-quarters full while the kiln runs, never add cold water to a jacket that has boiled dry, and draw hot water slowly through the tap. Scalds from 80 °C water happen in under a second.

- **Used drums.** Use only open-head drums that held non-flammable, non-toxic products. Never cut, drill or grind a drum that held fuel, solvent or pesticide, and burn paint and liners off outdoors, upwind, before first use. Do not use galvanized pipe or drums: heated zinc gives off toxic fumes.
- **Char handling.** Tip char out only after overnight cooling, onto bare ground, and quench or wet it before bagging. Dry char dust is a fire and inhalation hazard; wet it and wear a dust mask when crushing.
- **Lifting.** Drain the jacket before moving it. The tripod, jacket and flue unit weighs about 36 kg empty and needs two people; move it only when the flue is cool enough to handle with gloves.
- **Sharp edges.** Cut drum edges and air ports must be deburred or folded.
- **Temperature logger.** Keep the logger and power bank on the tripod leg away from the heat; thermocouple leads must be rated for the temperature where they run.

## Open questions for TRL 3

- Confirm by calculation that the retort gas flow can sustain the annulus fire after the start-up wood burns out, and the number and size of gas holes in the retort base.
- Size the secondary air holes and damper for the range of gas flows over a batch.
- Check the draft and flue diameter against the peak gas flow, and whether the jacket cools the flue gas enough to condense tar in the upper flue.
- Estimate the outer surface temperature with and without the insulation blanket.
- Decide whether the 36 kg tripod lift is acceptable to users, or whether a swinging arm or a lighter jacket is needed.
- Establish the batch record needed for a biochar certificate, even if certification stays out of scope.
- Validate feedstock, packing, batch size, water use and price with users through a local partner.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
