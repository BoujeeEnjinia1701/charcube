---
doc_id: CCB-PRC-001
title: CharCube design precis
project: CharCube
doc_type: Design precis
version: "0.3"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; decisions of 2026-09-25 recorded (CCB-DDR-001), numbers replaced by CCB-CAL-001 results, air shroud replaces the 25 mm ring, parametric model and CCB-DWG-001
---

# CharCube design precis

CharCube is a batch retort kiln made from a 114 L (30 US gal) steel drum sealed inside a 200 L (55 US gal) drum. Crop residue packed into the inner drum (the retort) is heated without air; the gas it gives off escapes through holes in the retort base and burns in the gap between the drums, which keeps the process going. The flame and any unburned gas then pass through a burner throat fed with secondary air, and the hot flue gas rises through an open-vented water jacket of about 61 L before leaving a flue 2.70 m above the ground. The TRL 3 calculations (CCB-CAL-001) give, for the central case: 12.0 kg of air-dry residue per batch makes about 3.0 kg of biochar in a burn of about 4.5 h using about 5.8 kg of wood, and heats the water by only about 25 K (6.4 MJ). The kiln parts cost $298 against the $300 budget. Three requirements are not met on paper: burn time (R5), hot water (R6) and start-up wood (R8).

![Hero render](../media/hero.png)

*Figure 1. CharCube on its block plinth with the jacket tripod, beside a 1.75 m person for scale. TRL 3 parametric model (`cad/src/model.py`).*

## How it works

1. **Load.** The retort is packed to 600 mm with 12.0 kg of air-dry residue (bundled straw, stalks, cobs or prunings), its lid is clamped on, and it stands upright on three firebrick standoffs inside the outer drum. The outer lid, carrying the burner throat, goes on top, and the tripod carrying the drained jacket and flue is set over it so the jacket sleeve slips over the top of the throat.
2. **Light.** Dry wood is lit in the 53 mm annulus around the retort and in the space beneath it; about 1.7 kg brings the kiln up to temperature, and more is fed to keep the annulus hot (about 5.8 kg in all, central estimate). Primary air enters through four ports near the base of the outer drum.
3. **Pyrolysis.** After about 30 to 45 min the retort contents pass about 300 °C and start to release gas and tar vapor. The gas leaves through holes in the retort base, meets the fire and burns. The retort gas then supplies much of the heat, but CCB-CAL-001 shows that wood must still be fed to hold the annulus near 650 °C for the whole burn. The target is a retort core of 450 to 600 °C for at least 30 min. Heat conducts slowly into the packed charge, so the core reaches 450 °C about 4.0 h after lighting (2.9 to 6.5 h).
4. **Clean-up burn.** Everything leaving the outer drum passes the burner throat, a 160 mm steel pipe 400 mm long. A 230 mm sleeve (the air shroud) around its base admits secondary air, preheated by the throat wall, through 24 holes of 12 mm, so gas that escaped the annulus fire burns there instead of leaving as smoke and methane.
5. **Heat recovery.** The hot gas (about 400 to 465 °C at the throat exit, after mixing with the secondary air) rises through a 168 mm sleeve that forms the centre of an annular water jacket. Heat passes through the sleeve wall into the water, but slowly: the gas flow is laminar or transitional. The jacket is open at the top, so it cannot build pressure. Hot water is drawn from a tap at its base.
6. **Finish and cool.** When the flame at the throat dies back (about 4.5 h after lighting; 3.4 to 7.0 h), the primary ports and secondary damper are closed and the kiln is left sealed overnight. The char cools without air, so it does not burn away.
7. **Unload and log.** Next morning the tripod unit and lid are lifted off, the retort (about 15.2 kg with its char) is lifted out, and the char is tipped out, quenched or wetted, weighed and crushed. A two-channel thermocouple logger records the retort core and the throat exit every 10 s, giving a record of peak temperature and time at temperature for each batch.

![Energy flow](../media/flow.png)

*Figure 2. Energy per batch, central estimates from CCB-CAL-001: 12.0 kg of residue at 16.0 MJ/kg (air-dry, higher heating value) plus 5.8 kg of wood at 16.2 MJ/kg (lower heating value); 2.96 kg of char at 20.2 MJ/kg; the jacket takes about 9 % of the flue gas heat.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv`, Figure 4 and CCB-DWG-001. Dimensions are the parameters of `cad/src/model.py`.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Outer drum (firebox shell) | 200 L open-head steel drum, 572 mm diameter x 851 mm, four 40 x 110 mm primary air ports with sliding dampers | Used drum; must have held a non-flammable, non-toxic product and be burned clean of paint before use |
| 2 | Outer lid with flue collar | The drum's own lid with a 160 mm collar, 40 mm high, riveted | Sealed with ceramic gasket rope and the drum's locking ring |
| 3 | Inner retort | 114 L open-head steel drum, 463 mm diameter x 737 mm, bolt-ring lid, eight 20 mm gas holes on a 300 mm circle in the base | Holds the feedstock; replaced when it scales through (estimate 50 to 100 batches) |
| 4 | Firebrick standoffs | Three half firebricks, 60 mm high | Leave room for fire under the retort |
| 5 | Secondary air shroud | 230 mm sleeve, 150 mm high, around the throat base; closed top, open bottom with a sliding band damper | Replaces the 25 mm pipe ring of TRL 2, which could not pass the air (CCB-CAL-001 section 6); proposed, awaiting Amish (CCB-DDR-001 item 11) |
| 6 | Burner throat (afterburner) | 160 x 2 mm plain steel pipe, 400 mm long, two staggered rings of 12 x 12 mm air holes inside the shroud | The jacket sleeve slips over its top end |
| 7 | Flue pipe with rain cap | 160 x 2 mm plain (not galvanized) steel, 700 mm, slipping 50 mm into the jacket sleeve; rain cap on three posts | Outlet 2.70 m above the ground |
| 8 | Water jacket | Annular steel tank, 420 mm outside diameter x 600 mm, 2 mm walls, around an integral 168 mm flue sleeve; about 61 L at 540 mm depth; open top with a loose lid and 24 mm vent | The one welded, water-tight part; local fabricator |
| 9 | Draw-off tap | 1/2 in brass ball valve with a short nipple | Drains the jacket before moving it |
| 10 | Jacket support tripod | Three 40 x 40 x 4 mm angle legs bolted to a flat-bar ring seat, feet on a 1.44 m circle | Carries the jacket and flue so the drum lid carries no water load |
| 11 | Insulation blanket | 25 mm ceramic fibre blanket held by wire mesh, air ports left clear | Halves the shell loss (CCB-CAL-001 section 4) |
| 12 | Plinth | Four concrete blocks and a steel ash pan | Lifts the air ports clear of the ground and keeps embers off it |
| 13 | Thermocouple logger | Two type K class 1 probes (retort core, throat exit), two MAX31855 amplifiers, a small microcontroller and microSD card, USB power bank | Mounted on a tripod leg, away from the heat |

Item 14 (fasteners, gasket rope, high-temperature sealant) is in the BOM but not modelled.

![Cutaway](../media/cutaway.png)

*Figure 3. Section looking from the front: retort (3) inside the outer drum (1) with the gas annulus between them, insulation (11) outside, lid (2), air shroud (5) and burner throat (6) above, then the water jacket (8) around its flue sleeve, with the tap (9). Tripod and logger omitted.*

## Numbers from the TRL 3 calculations

All values are central estimates from CCB-CAL-001 (`docs/04-calcs/sizing.py`), with the favourable to unfavourable range where it matters. Assumptions are listed there: air-dry feed at 12 % moisture packed to 120 kg/m³, a dry feed analysis typical of maize and cotton stalks, 28 % char yield, and the annulus held at 650 °C until the core reaches 450 °C. Nothing is measured.

Table 2. Batch, energy, carbon and cost.

| Quantity | Value | Requirement |
| --- | --- | --- |
| Retort fill | 100 L at 600 mm depth (123 L geometric) | |
| Feed per batch | 12.0 kg air-dry (10.58 kg dry); loose chopped straw would give 4.0 kg and is outside the decided feedstock | R1 met |
| Biochar | 2.96 kg (2.12 to 3.70 kg) at 28 % (20 to 35 %); about 29 % ash, 20.2 MJ/kg | R2 at risk |
| Core at 450 °C | 4.0 h after lighting (2.9 to 6.5 h) | R3 at risk |
| Burn, light to end of flaming | 4.5 h (3.4 to 7.0 h) | R5 **not met** |
| Sealed cooling; unload | About 3.2 h; unload about 8 h after lighting, though overnight is safer | R5 16 h limit met |
| Start-up and support wood | 5.8 kg (2.9 to 13.9 kg); light-up alone 1.7 kg | R8 **not met** |
| Heat released in the kiln | 190 MJ (143 to 303 MJ) | |
| Shell loss while burning | 5.7 kW: blanketed side 125 °C, bare lid 257 °C, throat 223 °C | |
| Stack draft | 16.9 Pa over 2.43 m; peak losses about 5 Pa including the gas holes, margin 3.2 | R4 air paths sized |
| Secondary air holes | 27.1 cm² provided against 23.6 cm² needed at peak | R4 |
| Heat to water | 6.4 MJ (4.9 to 9.2 MJ); 61 L raised about 25 K; no boiling in any case | R6 **not met** |
| Carbon stored for 100 years | 1.30 kg C, 4.8 kg CO₂ per batch (2.96 kg x 0.55 x 0.80) | |
| Methane penalty | 2.0 kg CO₂e per batch at the retort field average (24 g CH₄ per kg char, GWP100 28) | R4 not verifiable |
| Net removal | 2.8 kg CO₂e per batch (2.0 to 3.5); 0.70 t CO₂e and about 740 kg of char a year at 250 batches; about 3.0 t of residue kept out of open burning | |
| Mass | About 91 kg without plinth and water; lift unit (tripod, drained jacket, flue) 43.3 kg for two people; retort with char 15.2 kg; full jacket 83 kg | R11 met |
| Height | Flue outlet 2.70 m; footprint about 1.44 m across the tripod feet | R12 met |
| Parts cost | $298 against $300; safety kit (about $40) listed separately | R10 met |

The main changes from TRL 2: the char carries its ash, so its mass and heating value are lower; the burn is set by conduction into the charge and is longer; a longer burn needs more wood; and the plain jacket sleeve transfers about a third of the heat assumed at TRL 2.

## Key design choices

Items 1 to 8 and 10 of the TRL 2 review were decided by Amish on 2026-09-25: go with the recommendation (CCB-DDR-001).

- **Nested-drum retort rather than a flame-curtain kiln.** Decided by Amish, 2026-09-25. A Kon-Tiki cone costs less and needs no start-up wood, but it is open, its heat cannot be recovered and its yield on straw is lower.
- **Annular water jacket on the flue rather than a copper coil.** Decided by Amish, 2026-09-25. It needs no pump or raised tank and cannot build pressure. CCB-CAL-001 shows it recovers only about 6.4 MJ per batch with a plain sleeve; a spiral baffle insert and a jacket blanket are proposed, awaiting Amish (CCB-DDR-001 item 12).
- **Burner throat with preheated secondary air.** Decided by Amish, 2026-09-25. The TRL 3 sizing replaced the 25 mm pipe ring with an air shroud; that change is proposed, awaiting Amish (item 11).
- **Jacket carried on a tripod, not on the drum lid.** Decided by Amish, 2026-09-25. The drained lift unit weighs 43.3 kg, 21.6 kg each for two people.
- **Target feedstock.** Decided by Amish, 2026-09-25: bundled straw and mixed stalks and cobs first; a straw press is a separate project.
- **Temperature logging as standard.** Decided by Amish, 2026-09-25. Class 1 probes are needed to meet ±5 °C (CCB-CAL-001 section 10).
- **Insulation blanket.** Decided by Amish, 2026-09-25: ceramic fibre for the prototype. A lid blanket (not yet in the design) would save about 1.4 kW; proposed, awaiting Amish (item 13).
- **Budget.** Decided by Amish, 2026-09-25: $300 covers the kiln parts; the safety kit is required and listed separately.
- **Name.** Decided by Amish, 2026-09-25: keep CharCube.

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with BOM numbers.*

## Safety

> **Safety:** CharCube is a fire. CCB-CAL-001 estimates about 125 °C on the blanket and 170 to 260 °C on average over the bare port band, lid and throat, with hotter spots at gaps, the collar and the air ports; the gas inside is at 400 to 650 °C, and the char stays hot enough to reignite for many hours. Run it outdoors only, on bare soil or paving, at least 5 m from buildings, fences, dry vegetation and residue piles, never under trees or roofs, and never during a local burning ban or high wind. Keep a fire extinguisher or at least 50 L of water and a shovel at hand, keep children and animals outside a marked 3 m circle, and wear heat-resistant gloves, eye protection and closed shoes. This safety kit is required for every batch; it is listed separately from the kiln budget (CCB-REQ-001 R10).

> **Safety:** Pyrolysis gas is flammable and toxic (carbon monoxide, hydrogen, methane and tar vapor). Never open the retort or the outer lid while the kiln is hot: air entering a hot retort can ignite the gas suddenly and throw flame. Do not stand over the flue or downwind of the throat, never run the kiln in or near an enclosed space, and stop a batch that smokes heavily rather than leaving it.

> **Safety:** The water jacket is not expected to boil with the plain sleeve, but it can if a baffle insert is added or a batch runs long. It must stay open to the air: never plug the vent or fit a sealed lid, and never connect it to household plumbing or a closed tank. Keep it at least three-quarters full while the kiln runs, never add cold water to a jacket that has boiled dry, and draw hot water slowly through the tap. Scalds from 80 °C water happen in under a second.

- **Used drums.** Use only open-head drums that held non-flammable, non-toxic products. Never cut, drill or grind a drum that held fuel, solvent or pesticide, and burn paint and liners off outdoors, upwind, before first use. Do not use galvanized pipe or drums: heated zinc gives off toxic fumes.
- **Char handling.** Tip char out only after overnight cooling, onto bare ground, and quench or wet it before bagging. Dry char dust is a fire and inhalation hazard; wet it and wear a dust mask when crushing.
- **Lifting.** Drain the jacket before moving it. The tripod, jacket and flue unit weighs about 43 kg empty and needs two people; a full jacket weighs about 83 kg and must never be moved; move it only when the flue is cool enough to handle with gloves.
- **Sharp edges.** Cut drum edges and air ports must be deburred or folded.
- **Temperature logger.** Keep the logger and power bank on the tripod leg away from the heat; thermocouple leads must be rated for the temperature where they run.

## Open questions

The TRL 3 open questions on gas holes, secondary air, draft, jacket heat transfer and surface temperatures are answered in CCB-CAL-001. What remains:

- Should R5, R6 and R8 be relaxed, or should the design change (lid blanket, jacket baffle and blanket, central tube in the retort)? Proposed, awaiting Amish (CCB-DDR-001 items 12 to 14).
- Is the 43 kg two-person lift acceptable to users, or is a swinging arm needed?
- How fast does tar foul the jacket sleeve, and how is it cleaned?
- Establish the batch record needed for a biochar certificate, even if certification stays out of scope.
- First region, residue and partner: proposed, awaiting Amish; partners are chosen per area later.
- Validate feedstock, packing, batch size, water use and price with users through a local partner.

TRL 4 (building and logging batches) is on hold by Amish's instruction.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html). General arrangement: [CCB-DWG-001](../cad/drawings/CCB-DWG-001.pdf). Calculations: [CCB-CAL-001](04-calcs/01-sizing.md).
