---
doc_id: CCB-DDR-001
title: CharCube TRL 2 review decisions
project: CharCube
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 8 and 10); item 9 and the new TRL 3 items 11 to 16 remain proposed, awaiting Amish

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed ten items as "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." The same instruction approved cross-cutting SwapCell interface items, a pricing rule for shared SwapCell packs, and a rule that community designs pick co-design partners per area later.

This record lists what that instruction decides and what it leaves open because there was no recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 section) and CCB-PRC-001 v0.2. They are not repeated here.

## Decision

*Table 1. Decided items.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Heat recovery type | Decided by Amish, 2026-09-25: go with recommendation. Open-vented annular water jacket around the flue (option a), not the copper coil of the scaffold | CCB-PRC-001 v0.3, `cad/src/model.py` item 8 |
| 2 | Budget | Decided by Amish, 2026-09-25: go with recommendation. Keep `budget_usd: 300` for the kiln parts (option a). Safety equipment (about $40) is listed separately, is required, and sits outside the kiln budget | `project.yaml` (unchanged), CCB-REQ-001 R10, `bom/bom-notes.md` |
| 3 | Kiln type | Decided by Amish, 2026-09-25: go with recommendation. Nested-drum retort, not a Kon-Tiki flame-curtain kiln | CCB-PRC-001 v0.3 |
| 4 | Target feedstock | Decided by Amish, 2026-09-25: go with recommendation. Bundled straw and mixed stalks and cobs first; loose straw only with a press, which is a separate project | CCB-REQ-001 R1 (redefined), CCB-PRB-001 v0.3 |
| 5 | Burner throat with preheated secondary air | Decided by Amish, 2026-09-25: go with recommendation. Include it. Hole sizing at TRL 3 is in CCB-CAL-001 section 8 and leads to open item 11 | CCB-PRC-001 v0.3, CCB-CAL-001 |
| 6 | Temperature logger as standard | Decided by Amish, 2026-09-25: go with recommendation. Include it (about $32) as the batch record | `bom/bom.csv` line 13, CCB-REQ-001 R9 |
| 7 | Insulation | Decided by Amish, 2026-09-25: go with recommendation. 25 mm ceramic fibre blanket for the prototype | `bom/bom.csv` line 11 |
| 8 | Jacket support | Decided by Amish, 2026-09-25: go with recommendation. Tripod lifted aside by two people for loading | `cad/src/model.py` item 10, CCB-REQ-001 R11 |
| 10 | Name | Decided by Amish, 2026-09-25: go with recommendation. Keep the name CharCube; no reshaping of the concept | `project.yaml` (unchanged) |

The pitch and problem lines had no recommended rewording in the TRL 2 review and are unchanged.

Cross-cutting approvals from the same instruction, recorded here:

- **SwapCell interface v0.3.** Decided by Amish, 2026-09-25 (cross-cutting): the SwapCell interface adds a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles. CharCube does not use SwapCell (the logger runs from a USB power bank), so no v0.3 items apply.
- **Shared packs are priced once.** Decided by Amish, 2026-09-25 (cross-cutting). Not applicable: CharCube has no SwapCell pack.
- **Co-design partners per area later.** Decided by Amish, 2026-09-25 (cross-cutting): community designs pick co-design partners per area later. Partners stay open.

### Items that remain open

*Table 2. Open items, proposed, awaiting Amish.*

| # | Item | Status and recommendation |
| --- | --- | --- |
| 9 | First region, residue and partner for co-design | Proposed, awaiting Amish. No recommendation was made (the review gave examples only: paddy straw in northwest India, or maize and cotton stalks in East Africa). Portfolio rule: partners are chosen per area later |
| 11 | Secondary air manifold form | Proposed, awaiting Amish. CCB-CAL-001 shows the TRL 2 25 mm pipe ring would need about 46 Pa to pass the peak secondary air against about 8 Pa of available suction. The TRL 3 model uses a 230 mm sleeve (shroud) around the throat with an open bottom and band damper, and 24 holes of 12 mm. Recommendation: accept the shroud |
| 12 | R6 hot water shortfall (6.4 MJ against 10 MJ) | Proposed, awaiting Amish. Options: (a) add a spiral baffle insert in the jacket sleeve and 25 mm of blanket on the jacket shell (about 13.9 MJ on paper, about $15 more); (b) relax R6 to 5 MJ; (c) drop the jacket, as TRL 2 option (c). Recommendation: (a), checked at TRL 4 if Amish lifts the hold, since the insert also adds tar and soot fouling to clean |
| 13 | R8 start-up wood (5.8 kg central against 5 kg) | Proposed, awaiting Amish. Options: blanket the lid and top band (saves about 1.4 kW of loss), run at lower excess air, or relax R8 to 8 kg. Recommendation: blanket the lid (about $6) and keep the 5 kg target until batches are logged |
| 14 | R5 burn time (4.5 h central against 4 h) | Proposed, awaiting Amish. Heat conduction into the packed charge sets the burn time. Options: relax R5 to 5 h, or reduce the conduction path with a perforated central tube in the retort. Recommendation: relax R5 to 5 h light to end of flaming; the 16 h unload limit is met |
| 15 | R9 accuracy above 700 °C | Proposed, awaiting Amish. The MAX31855 accuracy is specified to 700 °C. Recommendation: keep class 1 probes and restate R9 as ±5 °C to 700 °C and indicative above |
| 16 | Kiln operating notes versus build notes | Proposed, awaiting Amish. The TRL 2 review said the safety kit would be "stated as required in the build notes at TRL 3". Build notes are TRL 4 material, so the requirement is stated in CCB-REQ-001 R10 and `bom/bom-notes.md` instead. Recommendation: accept |

## Consequences

- CCB-PRB-001, CCB-PRC-001 and CCB-REQ-001 move to v0.3 with these decisions; the precis no longer lists items 1 to 8 and 10 as proposed.
- CCB-REQ-001 R1 applies to the decided feedstock (packed or bundled), and R10 now states that the $300 budget covers kiln parts, with the safety kit required and listed separately.
- The TRL 3 model, drawing CCB-DWG-001 and CCB-CAL-001 follow the decided retort, jacket, throat, logger, blanket and tripod.
- TRL 4 work (building, testing, purchasing) is on hold by Amish's instruction, whatever the outcome of the open items.
