---
doc_id: CCB-DDR-002
title: CharCube recommendations accepted
project: CharCube
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all open recommendations (items 11 to 16) and what changed in the repo; list the items still open
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish (item 17, $320)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 11 to 16; item 17 decided 2026-09-26); item 9 remains proposed, awaiting Amish

## Context

After the TRL 3 session, CCB-DDR-001 v0.1 and `docs/REVIEW.md` left items 9 and 11 to 16 as "Proposed, awaiting Amish". On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every open item that carried a recommendation is therefore decided as recommended. Item 9 had no recommendation and stays open. TRL 4 remains on hold by Amish's instruction, so nothing here is built, bought or tested.

## Options considered

The options for each item are in CCB-DDR-001 (Table 2) and `docs/REVIEW.md` (TRL 3 session). Where an item offered several options, the recommended option is the decision.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 11 | Secondary air manifold form | Accept the 230 mm air shroud with an open bottom and band damper in place of the 25 mm pipe ring | Shroud already in the model; precis and REVIEW wording changed from proposed to decided. Because the baffle insert (item 12) adds flow resistance, the throat now has 30 air holes of 12 mm in place of 24: 33.9 cm² provided against 28.5 cm² needed at peak (was 27.1 against 23.6). `cad/src/model.py` `N_AIR_HOLES`, `bom/bom.csv` line 6 |
| 12 | R6 hot water shortfall | Option (a): spiral baffle insert in the jacket sleeve plus a 25 mm blanket on the jacket shell. Checking the insert's heat transfer and fouling by measurement is TRL 4 work and is on hold | New parts 15 (twisted steel strip 150 mm wide, hung from a cross bar in notches at the foot of the flue so it lifts out for cleaning) and 16 (25 mm mineral wool on the jacket side). BOM lines 15 ($7) and 16 ($8). Heat to water 6.4 MJ to 11.5 MJ (central), 45 K rise in place of 25 K; R6 from not met to at risk (favourable, short burn, 9.0 MJ) |
| 13 | R8 start-up wood | Blanket the lid and top band (about $6) and keep the 5 kg target until batches are logged | New part 17 (25 mm ceramic fibre disc on the lid, clear of the shroud intake, with a skirt over the top band and locking ring). BOM line 17 ($6). Shell loss 5.69 to 4.47 kW (the lid blanket saves 1.22 kW, against about 1.4 kW estimated); wood 5.8 kg to 3.7 kg (central). R8 target unchanged at 5 kg; status from not met to at risk (unfavourable 9.8 kg) |
| 14 | R5 burn time | Relax R5 from 4 h to 5 h, light to end of flaming; the 16 h unload limit stays | CCB-REQ-001 R5. Burn 4.5 h (3.4 to 7.0 h) is unchanged; status from not met to at risk (unfavourable case above 5 h) |
| 15 | R9 accuracy above 700 °C | Keep class 1 probes and restate R9 as ±5 °C from 0 to 700 °C and indicative above | CCB-REQ-001 R9 restated; status from at risk to met (±3.4 °C to 700 °C) |
| 16 | Safety kit wording | The required safety kit is stated in CCB-REQ-001 R10 and `bom/bom-notes.md`, not in build notes, which are TRL 4 material | R10 text notes this; no build notes written |

Knock-on changes from items 12 and 13, all at TRL 3 and inside this repo:

- **Cost.** The BOM grows from 14 to 17 lines and from $298 to $319, over the $300 kiln budget. `budget_usd` stays at 300, the figure Amish decided in CCB-DDR-001 item 2. R10 was then **not met**; see item 17 below, decided 2026-09-26.
- **Draft.** The insert adds about four velocity heads of loss. Draft margin at peak falls from 3.2 to 2.4; available draft 16.9 to 16.7 Pa; suction at the throat holes 7.6 to 5.2 Pa.
- **Mass.** Kiln 91 to 96 kg dry; heat-recovery lift unit 43.3 to 46.6 kg (21.6 to 23.3 kg each for two people). R11 still met, with less margin.
- **Heat released.** 190 to 160 MJ per batch (central), because less wood is burned; flue gas 152 to 128 kg per batch.
- **Cooling.** 3.2 to 3.6 h sealed cooling; unload still about 8 h after lighting.
- **Boiling.** No scenario boils, but the unfavourable long burn now reaches 19.1 MJ against 20.6 MJ to boiling, so the open vent (R7) matters more.
- **Documents.** CCB-PRC-001 v0.4, CCB-REQ-001 v0.4, CCB-CAL-001 v0.2 (script and `results.csv` re-run), CCB-DDR-001 v0.2, drawing CCB-DWG-001 Rev P2, concept sheet CCB-DWG-010 Rev P2, media regenerated, `bom/bom-notes.md` and `README.md` updated.

The pitch and problem lines had no recommended rewording and are unchanged.

*Table 1a. Item decided by Amish, 2026-09-26.* On 2026-09-26 Amish wrote: "I am ok with the budget top ups."

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 17 | R10 budget after items 12 and 13 ($319 against $300) | Budget top-up to $320: decided by Amish, 2026-09-26. Option (a): `budget_usd` raised to $320 for kiln parts; the safety kit (about $40) stays required and listed separately | `project.yaml` `budget_usd` 300 to 320; CCB-REQ-001 v0.5 (R10 target $320, met); `sizing.py` now reads the budget from `project.yaml`, re-run; CCB-CAL-001 v0.3 (R10 met, $1 margin; six met, five at risk, one not verifiable); CCB-PRC-001 v0.5; README budget line |

## Items still open

*Table 2. Proposed, awaiting Amish.*

| # | Item | Status |
| --- | --- | --- |
| 9 | First region, residue and partner for co-design | Proposed, awaiting Amish. No recommendation was made; the portfolio rule is that partners are chosen per area later |
| 17 | R10 budget after items 12 and 13 ($319 against $300) | Decided by Amish, 2026-09-26: budget top-up to $320 (option (a)); see Table 1a |

## Consequences

- After the 2026-09-26 budget top-up, R10 is met with a $1 margin and no requirement is not met on paper; R2, R3, R5, R6 and R8 are at risk; R4 is not verifiable at TRL 3.
- The spiral insert collects tar and soot; it lifts out with the flue for cleaning. How fast it fouls is a TRL 4 question.
- TRL 4 (building, logging batches, measuring the insert's heat transfer and emissions, purchasing) remains on hold by Amish's instruction.
