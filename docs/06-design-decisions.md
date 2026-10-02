---
doc_id: CCB-DEC-001
title: CharCube design decisions register
project: CharCube
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, the decision records and the build plan work
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: 'Amish approved the recommendations for all seven open decisions (2026-10-02); CCB-DDR-003 accepted; moved to decisions made; value-engineering note on the decided additions'
---

# CharCube design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, CCB-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The two drums' actual diameters and heights, and the gap between them (at least 40 mm) | Drum sizes vary by maker; the gas gap, brick positions and probe slot height depend on them | CCB-DDR-003 |
| 2 | The 160 mm pipe's actual outside diameter and the 168 mm sleeve's bore | The collar is rolled to the pipe; the slip joints need about 2 mm clearance | CCB-DDR-003, P2 and P8 |
| 3 | The effect of the 150 mm lid hole on draft (8 % less area than the throat bore), confirmed at the first burn (decided 2026-10-02) | The draft calculation does not model the lid entry; margin 2.4 at peak | CCB-DDR-003, P2; CCB-CAL-001 section 6 |
| 4 | Probe lengths (500 mm and 300 mm) and sheath rating | The core probe must reach the retort axis from outside the blanket | CCB-DDR-003, P12 |
| 5 | Blanket roll widths (681 mm drum strip, 540 mm jacket strip) | Sets how many joins each wrap has | Build plan sections 3.4, 3.14 |
| 6 | Prices of every BOM line once quoted, including the parts added for construction | The estimated cost against the value-engineering target rests on indicative prices | CCB-CAL-001 section 11 |
| 7 | The factor of 3 on gas-side heat transfer and the four velocity heads of pressure loss assumed for the spiral baffle | Heat to water (R6) and draft depend on them; they are assumptions until measured at TRL 4 | CCB-CAL-001 sections 1, 7 |

## Value engineering

Value-engineering target: USD 320 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 319 as priced (USD 1 under the target); the parts added for construction (U-bolts, fins, foot cleats and pads, guide strips, clips, rod, bolts) are not yet priced and probably add USD 5 to 10, which would put the estimate USD 4 to 9 over the target.

- **Main cost drivers:** the ceramic fibre blankets, the welded water jacket with its spiral baffle insert, the two drums, and the concrete plinth blocks and firebricks (see `bom/bom.csv`).
- **Decided additions not yet priced (2026-10-02):** the 25 mm ceramic fibre board under the drum floor (decision on CCB-DDR-003, A2), the lifting aid for the heat-recovery unit and the hot-surface warning labels. With the unpriced parts added for construction they will take the estimate further over the target; price them before reading the result against it.
- **Savings worth trying:** a cheaper logger box; a clay and ash render in place of the side blanket (about USD 25, from the TRL 2 review); and re-pricing the added small parts at purchase.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 8 and 10: open-vented annular water jacket; $300 kiln budget with the safety kit separate; nested-drum retort; bundled straw and stalks first; burner throat with preheated air; logger as standard; ceramic fibre blanket; tripod-carried jacket; keep the name | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | CCB-DDR-001 |
| 2026-09-25 | Items 11 to 16: air shroud in place of the 25 mm ring; spiral baffle insert and jacket blanket; lid and top band blanket; R5 relaxed to 5 h; R9 restated to 700 °C; safety kit stated in R10 and the BOM notes | Amish: "i accept all your recommendations, go with them across all repos." | CCB-DDR-002 |
| 2026-09-26 | Item 17: budget top-up from $300 to $320 for kiln parts | Amish: "I am ok with the budget top ups." | CCB-DDR-002, Table 1a |
| 2026-09-25 | TRL 4 on hold | Amish | `project.yaml`; CCB-DDR-001 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; outstanding decisions kept in this register, not in the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | CCB-DDR-003 (accepted on 2026-10-02, below) |
| 2026-10-02 | Design for construction accepted: the twelve changes of Table 1 and their knock-on changes, as made; the first burn confirms that the 150 mm lid hole (8 % less area than the throat bore) does not limit draft | Amish: "i approve your recommendations for all 555 open decisions." | CCB-DDR-003, Table 1 |
| 2026-10-02 | Plinth: a 25 mm ceramic fibre board between the pan and the blocks from the first burn, with a thermocouple on a block; the board is dropped on later builds only if a measured burn without it keeps the blocks under about 150 °C | Amish: "i approve your recommendations for all 555 open decisions." | CCB-DDR-003, A2 |
| 2026-10-02 | Jacket sleeve: the welder flares the bottom 20 mm of the sleeve to about 190 mm so it guides itself onto the throat | Amish: "i approve your recommendations for all 555 open decisions." | CCB-DDR-003, A3 |
| 2026-10-02 | Heat-recovery unit: a lifting aid, a swinging arm on a post or a hand winch, is designed for the first build; users are asked through the partner how it should work, not whether it is needed | Amish: "i approve your recommendations for all 555 open decisions." | CCB-PRC-001, open questions |
| 2026-10-02 | First region, residue and partner: kept open under the portfolio rule, chosen by this rule: a region where rice or wheat straw is still burned in the open, with a partner that already runs residue or biochar trials. First candidate to approach: an agricultural university's extension service, for example Punjab Agricultural University in India | Amish: "i approve your recommendations for all 555 open decisions." | CCB-DDR-001 item 9; CCB-DDR-002 Table 2 |
| 2026-10-02 | Rain cap: the conical cap is adopted in the model and drawings, on the three flat-bar legs and 60 mm gap set by the design for construction | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, appearance item 1 |
| 2026-10-02 | Hot-surface labels: durable ISO 7010 W017 hot-surface warning labels for the drum blanket and the jacket are added to BOM line 14 | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, appearance item 5 |
