---
doc_id: CCB-REQ-001
title: CharCube requirements
project: CharCube
doc_type: Requirements
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
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply Amish's 2026-09-25 decisions (CCB-DDR-001); R1 limited to the decided feedstock, R10 redefined to exclude the required safety kit, R9 probe class stated; status from CCB-CAL-001
---

# CharCube requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be revised after co-design sessions. R1 and R10 were redefined by Amish's decisions of 2026-09-25 (CCB-DDR-001 items 2 and 4). The status column gives the TRL 3 result from CCB-CAL-001 (central estimate, with the range where it matters): met, not met, at risk, or not verifiable at TRL 3.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (CCB-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Process a useful batch | 10 kg or more of air-dry residue (15 % moisture or less) per batch, **for the decided feedstock: bundled straw and mixed stalks and cobs, packed to about 120 kg/m³**. Loose straw is out of scope without a press (a separate project) | Retort volume and packed bulk density | Met: 12.0 kg (10.58 kg dry) |
| R2 | Make biochar efficiently | Biochar 25 % or more of dry feed mass | Mass balance; later weighed batches | At risk: 28 % (20 to 35 %), 2.96 kg |
| R3 | Make stable char | Retort core at 450 °C or more for 30 min or more per batch, logged; target molar H/Corg below 0.7, the [European Biochar Certificate](https://www.european-biochar.org/en) limit | Heat conduction and balance; later logged batches and lab analysis | At risk: core at 450 °C about 4.0 h after lighting (2.9 to 6.5 h), only if the annulus is kept hot |
| R4 | Burn the gas, not vent it | All retort gas passes the annulus fire and the burner throat; visible smoke only during the first 15 min after lighting and the last 10 min of a batch; methane below 24 g per kg of char (the retort field average in [Sparrevik et al. 2015](https://www.sciencedirect.com/science/article/abs/pii/S0961953414005170)) | Design review and air sizing; later emission measurement with a partner lab | Not verifiable at TRL 3: route closed, draft margin 3.2, throat holes sized with 15 % spare area |
| R5 | Fit a daily routine | Light to end of flaming in 4 h or less; char ready to unload within 16 h of lighting | Heat conduction and cooling; later logged batches | **Not met**: burn about 4.5 h (3.4 to 7.0 h); unload after about 8 h is met |
| R6 | Recover heat as hot water | 10 MJ or more into water per batch (60 L raised by 40 K) | Heat transfer; later measured water temperature | **Not met**: 6.4 MJ (4.9 to 9.2 MJ), about 25 K rise |
| R7 | Keep the water circuit safe | Jacket open to the air at all times; no valve or cap that can seal it; water drawn from a tap at the base; jacket kept away from the lid by a separate support | Design review and safety checklist | Met by design |
| R8 | Use little start-up fuel | 5 kg or less of dry wood per batch | Energy balance; later weighed batches | **Not met**: 5.8 kg (2.9 to 13.9 kg); light-up alone 1.7 kg |
| R9 | Record each batch | Two type K channels (retort core, throat exit), class 1 probes, 0 to 1,000 °C, ±5 °C or better, logged every 10 s to removable storage, 24 h on a USB power bank | Component data; design review | At risk: ±3.4 °C to 700 °C; amplifier accuracy not specified above 700 °C; energy 6 of 31 Wh |
| R10 | Stay within the concept budget | Kiln parts $300 or less. **The safety kit (extinguisher or water and shovel, gloves, eye protection, dust mask, about $40) is required and listed separately, outside the kiln budget** | Priced BOM | Met: $298 |
| R11 | Be built and handled by a small crew | Built with hand tools, drill and angle grinder, with at most one welded part (the water jacket); no single lift above 25 kg per person | Masses from the model; design review | Met: lift unit 43.3 kg for two people (21.6 kg each); retort with char 15.2 kg |
| R12 | Operate safely outdoors | Flue outlet 2.5 m or more above the ground; 5 m clear radius from structures and dry vegetation; no galvanized parts in the hot path | Model and BOM; safety checklist | Met: outlet 2.70 m; no galvanized lines |

## Requirements not met or at risk

- **R5 not met.** Heat conducts slowly into a 0.46 m diameter packed charge; the burn lasts about 4.5 h. Proposed, awaiting Amish: relax R5 to 5 h (CCB-DDR-001 item 14).
- **R6 not met.** A plain flue sleeve transfers about 4 to 5 W/m²K, so the jacket takes about 6.4 MJ, not the 15 MJ estimated at TRL 2. A baffle insert and a jacket blanket would give about 13.9 MJ on paper. Proposed, awaiting Amish (item 12).
- **R8 not met.** Keeping the annulus hot for the whole burn needs about 5.8 kg of wood. Proposed, awaiting Amish: blanket the lid and keep the target until batches are logged (item 13).
- **R2, R3 and R9 at risk.** Yield and core temperature depend on feedstock and operation; R9 needs class 1 probes and has no amplifier specification above 700 °C (item 15).
- **R4** cannot be shown without emission measurement.
- **R11** is met only with the jacket drained and two people lifting the tripod unit.

## Assumptions

- Feedstock (decided): bundled straw, maize or cotton stalks, cobs or prunings at 10 to 15 % moisture (12 % in CCB-CAL-001), packed to about 120 kg/m³; about 18.2 MJ/kg dry and 16.0 MJ/kg air-dry (higher heating value).
- Start-up fuel: air-dry wood at about 16.2 MJ/kg (lower heating value), preferably from residues or prunings.
- Char: about 20 MJ/kg and about 55 % organic carbon with about 29 % ash for mixed straw and stalks ([IPCC 2019](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch02_Ap4_Biochar.pdf) defaults are 49 % for rice straw char and 65 % for herbaceous material).
- One batch a day for about 250 days a year.
- Ambient 10 to 40 °C, dry weather, wind below about 5 m/s.
- The kiln serves a household's or a trial plot's residue, not a whole field (see CCB-PRB-001, out of scope).
