---
doc_id: CCB-DEC-001
title: CharCube design decisions register
project: CharCube
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
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
---

# CharCube design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, CCB-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Design for construction: accept the twelve changes that make the concept buildable (pinwheel plinth, lid hole and collar, riveted shroud and 60 mm band, port damper guides, brick positions, retort handles, fins and bolted angle legs in place of the ring seat, 650 mm flue on stop clips with a riveted rain cap, baffle hanger rod, located jacket lid and vent, logger beside the leg, probes in through the side) | Accept; amend any change | Accept: none changes what the kiln does, its pitch or its safety case | The whole build plan | CCB-DDR-003, Table 1 |
| 2 | Concrete blocks under a hot drum floor may crack or spall | (a) build as modelled and measure the block temperature on the first burn; (b) a 25 mm ceramic fibre board between pan and blocks | (a), then (b) if the blocks pass about 150 °C | Plinth (build plan section 3.1, first checks) | CCB-DDR-003, A2 |
| 3 | Guiding the jacket sleeve onto the throat (2 mm clearance, 47 kg unit lowered by two people) | (a) as modelled; (b) flare the bottom 20 mm of the sleeve to about 190 mm | (b), a small extra for the welder | Water jacket (section 3.11), step 15 | CCB-DDR-003, A3 |
| 4 | Is the 47 kg two-person lift of the heat-recovery unit acceptable to users, or is a swinging arm needed? | (a) two-person lift as modelled; (b) a swinging arm on a post | None yet; ask users through a co-design partner | Tripod and lifts (sections 3.15, 3.16) | CCB-PRC-001, open questions |
| 5 | First region, residue and partner for co-design | Region and residue of the first adopting partner | None (portfolio rule: partners are chosen per area later) | Feedstock used for the first batches; named suppliers | CCB-DDR-001 item 9; CCB-DDR-002 Table 2 |
| 6 | Rain cap shape: the photoreal renders show a conical cap; the model and drawings a flat 260 mm square | (a) adopt the cone in the model and drawings; (b) keep the flat cap | (a): a cone sheds rain better and the BOM does not fix the shape | Rain cap (section 3.18) | REVIEW 2026-09-26, appearance item 1 |
| 7 | Hot-surface labels shown on the renders are not in the BOM | (a) add them to BOM line 14; (b) leave them out | (a): they cost little and support the safety section | Bought fixings (section 3.21) | REVIEW 2026-09-26, appearance item 5 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The two drums' actual diameters and heights, and the gap between them (at least 40 mm) | Drum sizes vary by maker; the gas gap, brick positions and probe slot height depend on them | CCB-DDR-003 |
| 2 | The 160 mm pipe's actual outside diameter and the 168 mm sleeve's bore | The collar is rolled to the pipe; the slip joints need about 2 mm clearance | CCB-DDR-003, P2 and P8 |
| 3 | The effect of the 150 mm lid hole on draft (8 % less area than the throat bore) | The draft calculation does not model the lid entry; margin 2.4 at peak | CCB-DDR-003, P2; CCB-CAL-001 section 6 |
| 4 | Probe lengths (500 mm and 300 mm) and sheath rating | The core probe must reach the retort axis from outside the blanket | CCB-DDR-003, P12 |
| 5 | Blanket roll widths (681 mm drum strip, 540 mm jacket strip) | Sets how many joins each wrap has | Build plan sections 3.4, 3.14 |
| 6 | Prices of every BOM line once quoted, including the parts added for construction | The estimated cost against the value-engineering target rests on indicative prices | CCB-CAL-001 section 11 |
| 7 | The factor of 3 on gas-side heat transfer and the four velocity heads of pressure loss assumed for the spiral baffle | Heat to water (R6) and draft depend on them; they are assumptions until measured at TRL 4 | CCB-CAL-001 sections 1, 7 |

## Value engineering

Value-engineering target: USD 320 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 319 as priced (USD 1 under the target); the parts added for construction (U-bolts, fins, foot cleats and pads, guide strips, clips, rod, bolts) are not yet priced and probably add USD 5 to 10, which would put the estimate USD 4 to 9 over the target.

- **Main cost drivers:** the ceramic fibre blankets, the welded water jacket with its spiral baffle insert, the two drums, and the concrete plinth blocks and firebricks (see `bom/bom.csv`).
- **Savings worth trying:** a cheaper logger box; a clay and ash render in place of the side blanket (about USD 25, from the TRL 2 review); and re-pricing the added small parts at purchase.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 8 and 10: open-vented annular water jacket; $300 kiln budget with the safety kit separate; nested-drum retort; bundled straw and stalks first; burner throat with preheated air; logger as standard; ceramic fibre blanket; tripod-carried jacket; keep the name | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | CCB-DDR-001 |
| 2026-09-25 | Items 11 to 16: air shroud in place of the 25 mm ring; spiral baffle insert and jacket blanket; lid and top band blanket; R5 relaxed to 5 h; R9 restated to 700 °C; safety kit stated in R10 and the BOM notes | Amish: "i accept all your recommendations, go with them across all repos." | CCB-DDR-002 |
| 2026-09-26 | Item 17: budget top-up from $300 to $320 for kiln parts | Amish: "I am ok with the budget top ups." | CCB-DDR-002, Table 1a |
| 2026-09-25 | TRL 4 on hold | Amish | `project.yaml`; CCB-DDR-001 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; outstanding decisions kept in this register, not in the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | CCB-DDR-003 (its changes are Draft, open decision 1) |
