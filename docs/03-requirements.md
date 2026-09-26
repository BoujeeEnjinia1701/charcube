---
doc_id: CCB-REQ-001
title: CharCube requirements
project: CharCube
doc_type: Requirements
version: "0.4"
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); R5 relaxed to 5 h, R9 restated to 700 °C, R10 notes the safety kit; status from CCB-CAL-001 v0.2
---

# CharCube requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be revised after co-design sessions. R1 and R10 were redefined by Amish's decisions of 2026-09-25 (CCB-DDR-001 items 2 and 4); R5 was relaxed and R9 restated by his acceptance of the TRL 3 recommendations on the same day (CCB-DDR-002 items 14 and 15). The status column gives the TRL 3 result from CCB-CAL-001 v0.2 (central estimate, with the range where it matters): met, not met, at risk, or not verifiable at TRL 3.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (CCB-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Process a useful batch | 10 kg or more of air-dry residue (15 % moisture or less) per batch, **for the decided feedstock: bundled straw and mixed stalks and cobs, packed to about 120 kg/m³**. Loose straw is out of scope without a press (a separate project) | Retort volume and packed bulk density | Met: 12.0 kg (10.58 kg dry) |
| R2 | Make biochar efficiently | Biochar 25 % or more of dry feed mass | Mass balance; later weighed batches | At risk: 28 % (20 to 35 %), 2.96 kg |
| R3 | Make stable char | Retort core at 450 °C or more for 30 min or more per batch, logged; target molar H/Corg below 0.7, the [European Biochar Certificate](https://www.european-biochar.org/en) limit | Heat conduction and balance; later logged batches and lab analysis | At risk: core at 450 °C about 4.0 h after lighting (2.9 to 6.5 h), only if the annulus is kept hot |
| R4 | Burn the gas, not vent it | All retort gas passes the annulus fire and the burner throat; visible smoke only during the first 15 min after lighting and the last 10 min of a batch; methane below 24 g per kg of char (the retort field average in [Sparrevik et al. 2015](https://www.sciencedirect.com/science/article/abs/pii/S0961953414005170)) | Design review and air sizing; later emission measurement with a partner lab | Not verifiable at TRL 3: route closed, draft margin 2.4 with the baffle insert, throat holes (30) sized with 19 % spare area |
| R5 | Fit a daily routine | Light to end of flaming in **5 h** or less (relaxed from 4 h, CCB-DDR-002 item 14); char ready to unload within 16 h of lighting | Heat conduction and cooling; later logged batches | At risk: burn about 4.5 h (3.4 to 7.0 h); unload after about 8 h is met |
| R6 | Recover heat as hot water | 10 MJ or more into water per batch (60 L raised by 40 K) | Heat transfer; later measured water temperature | At risk: 11.5 MJ (9.0 to 19.1 MJ) with the spiral baffle insert and jacket blanket, about 45 K rise |
| R7 | Keep the water circuit safe | Jacket open to the air at all times; no valve or cap that can seal it; water drawn from a tap at the base; jacket kept away from the lid by a separate support | Design review and safety checklist | Met by design |
| R8 | Use little start-up fuel | 5 kg or less of dry wood per batch | Energy balance; later weighed batches | At risk: 3.7 kg with the lid blanket (1.7 to 9.8 kg); light-up alone 1.7 kg |
| R9 | Record each batch | Two type K channels (retort core, throat exit), class 1 probes, **±5 °C or better from 0 to 700 °C and indicative from 700 to 1,000 °C** (restated, CCB-DDR-002 item 15), logged every 10 s to removable storage, 24 h on a USB power bank | Component data; design review | Met: ±3.4 °C to 700 °C with class 1 probes; energy 6 of 31 Wh |
| R10 | Stay within the concept budget | Kiln parts $300 or less. **The safety kit (extinguisher or water and shovel, gloves, eye protection, dust mask, about $40) is required and listed separately, outside the kiln budget**; this requirement and `bom/bom-notes.md` are where the safety kit is stated (CCB-DDR-002 item 16) | Priced BOM | **Not met**: $319; the decided baffle insert, jacket blanket and lid blanket add $21 |
| R11 | Be built and handled by a small crew | Built with hand tools, drill and angle grinder, with at most one welded part (the water jacket); no single lift above 25 kg per person | Masses from the model; design review | Met: lift unit 46.6 kg for two people (23.3 kg each); retort with char 15.2 kg |
| R12 | Operate safely outdoors | Flue outlet 2.5 m or more above the ground; 5 m clear radius from structures and dry vegetation; no galvanized parts in the hot path | Model and BOM; safety checklist | Met: outlet 2.70 m; no galvanized lines |

## Requirements not met or at risk

- **R10 not met.** The kiln parts total $319 against $300 after adding the decided spiral baffle insert and jacket blanket ($15, CCB-DDR-002 item 12) and lid blanket ($6, item 13). Proposed, awaiting Amish: raise the kiln budget to $320 or cut a line (CCB-DDR-002, open item 17).
- **R5 at risk.** The central burn (about 4.5 h) meets the relaxed 5 h target, but a poorly conducting charge could take about 7 h.
- **R6 at risk.** The baffle insert and jacket blanket lift the central estimate to 11.5 MJ, but a short burn gives about 9.0 MJ, and the convection gain of the insert is an assumption until measured.
- **R8 at risk.** The lid blanket brings the central wood demand to 3.7 kg, but a long burn could need about 9.8 kg.
- **R2 and R3 at risk.** Yield and core temperature depend on feedstock and operation.
- **R4** cannot be shown without emission measurement.
- **R11** is met only with the jacket drained and two people lifting the tripod unit (23.3 kg each, close to the 25 kg limit).

## Assumptions

- Feedstock (decided): bundled straw, maize or cotton stalks, cobs or prunings at 10 to 15 % moisture (12 % in CCB-CAL-001), packed to about 120 kg/m³; about 18.2 MJ/kg dry and 16.0 MJ/kg air-dry (higher heating value).
- Start-up fuel: air-dry wood at about 16.2 MJ/kg (lower heating value), preferably from residues or prunings.
- Char: about 20 MJ/kg and about 55 % organic carbon with about 29 % ash for mixed straw and stalks ([IPCC 2019](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch02_Ap4_Biochar.pdf) defaults are 49 % for rice straw char and 65 % for herbaceous material).
- One batch a day for about 250 days a year.
- Ambient 10 to 40 °C, dry weather, wind below about 5 m/s.
- The kiln serves a household's or a trial plot's residue, not a whole field (see CCB-PRB-001, out of scope).
