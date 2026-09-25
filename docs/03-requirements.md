---
doc_id: CCB-REQ-001
title: CharCube requirements
project: CharCube
doc_type: Requirements
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
  change: First measurable requirements for TRL 2, with status against the concept estimates
---

# CharCube requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be checked by calculation at TRL 3 and revised after co-design sessions. The status column compares each target with the estimates in CCB-PRC-001; "unverified" means the concept cannot yet show it either way.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Process a useful batch | 10 kg or more of air-dry residue (15 % moisture or less) per batch | Retort volume and packed bulk density | Met on estimate for bundled straw and stalks (about 12 kg); **not met** for loose chopped straw (about 4 kg) |
| R2 | Make biochar efficiently | Biochar 25 % or more of dry feed mass | Mass balance; later weighed batches | At risk: estimate 28 %, range 20 to 35 % |
| R3 | Make stable char | Retort core at 450 °C or more for 30 min or more per batch, logged; target molar H/Corg below 0.7, the [European Biochar Certificate](https://www.european-biochar.org/en) limit | Heat balance; later logged batches and lab analysis | Unverified |
| R4 | Burn the gas, not vent it | All retort gas passes the annulus fire and the burner throat; visible smoke only during the first 15 min after lighting and the last 10 min of a batch; methane below 24 g per kg of char (the retort field average in [Sparrevik et al. 2015](https://www.sciencedirect.com/science/article/abs/pii/S0961953414005170)) | Design review; later emission measurement with a partner lab | **Not shown**: routing is met by design, emissions cannot be shown at TRL 2 |
| R5 | Fit a daily routine | Light to end of flaming in 4 h or less; char ready to unload within 16 h of lighting | Heat balance; later logged batches | Met on estimate (2.5 to 3.5 h burning, 10 to 14 h cooling) |
| R6 | Recover heat as hot water | 10 MJ or more into water per batch (60 L raised by 40 K) | Heat transfer estimate; later measured water temperature | Met on estimate (about 15 MJ, range 10 to 25 MJ) |
| R7 | Keep the water circuit safe | Jacket open to the air at all times; no valve or cap that can seal it; water drawn from a tap at the base; jacket kept away from the lid by a separate support | Design review and safety checklist | Met by design |
| R8 | Use little start-up fuel | 5 kg or less of dry wood per batch | Heat balance; later weighed batches | At the limit (about 5 kg); unverified |
| R9 | Record each batch | Two type K channels (retort core, throat exit), 0 to 1,000 °C, ±5 °C or better, logged every 10 s to removable storage, 24 h on a USB power bank | Component data; design review | Met by design |
| R10 | Stay within the concept budget | Parts $300 or less | Priced BOM | Met with about $1 margin (about $299); safety equipment not included |
| R11 | Be built and handled by a small crew | Built with hand tools, drill and angle grinder, with at most one welded part (the water jacket); no single lift above 25 kg per person | Design review; massing model | Met only if the jacket is drained and the 36 kg tripod unit is lifted by two people |
| R12 | Operate safely outdoors | Flue outlet 2.5 m or more above the ground; 5 m clear radius from structures and dry vegetation; no galvanized parts in the hot path | Design review and safety checklist | Met by design (outlet about 2.7 m) |

## Requirements not met or not yet shown

- **R1** is not met for loose chopped straw: at about 40 kg/m³ the retort holds only about 4 kg. Straw must be bundled or packed, or mixed with stalks and cobs.
- **R4** cannot be shown at TRL 2. The gas route is closed by design, but methane and smoke depend on burner tuning and need measurement.
- **R2, R3 and R8** are estimates with wide ranges and depend on feedstock and operator.
- **R10** leaves no margin and excludes a fire extinguisher, gloves and eye protection (about $40).
- **R11** depends on two people lifting the drained tripod unit.

## Assumptions

- Feedstock: air-dry cereal straw, maize or cotton stalks, cobs or prunings at 10 to 15 % moisture, packed to about 120 kg/m³, higher heating value about 15 MJ/kg.
- Start-up fuel: about 5 kg of dry wood at about 16 MJ/kg, preferably from residues or prunings.
- Char: about 24 MJ/kg and about 55 % organic carbon for mixed straw and stalks ([IPCC 2019](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch02_Ap4_Biochar.pdf) defaults are 49 % for rice straw char and 65 % for herbaceous material).
- One batch a day for about 250 days a year.
- Ambient 10 to 40 °C, dry weather, wind below about 5 m/s.
- The kiln serves a household's or a trial plot's residue, not a whole field (see CCB-PRB-001, out of scope).
