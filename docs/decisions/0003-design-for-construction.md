---
doc_id: CCB-DDR-003
title: CharCube design for construction
project: CharCube
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-09-30
- **Status:** Draft. The changes in Tables 1 and 2 were made under Amish's 2026-09-30 instruction to make the design physically buildable; they are open for his review. The questions in Table 3 change what the product costs, its safety case or how it is handled, so they are proposed, awaiting Amish, and are listed in the design decisions register (CCB-DEC-001).

## Context

On 2026-09-30 Amish asked for a prototype build plan that shows how each component is made and how it fits the next, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of CCB-DDR-002 showed what CharCube does, but a constructability review with build123d (overlaps, contacts and clearances between every pair of neighbouring parts) and a part-by-part review of how each is made found twelve places where it could not be built, fixed or used as drawn.

The changes keep what CharCube does: the same two drums, retort fill, gas holes, burner throat, air shroud, secondary air holes, water jacket, baffle, blankets, flue outlet height, tripod footprint and logger. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now builds each component as it is made and runs 68 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must not touch are apart by at least the stated clearance, and nothing overlaps. All 68 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The four 390 x 190 mm plinth blocks were drawn centred 170 mm each side of the axis, so each pair overlapped by 50 mm (1.8 L of solid block in the same place). | The blocks are laid as a pinwheel: each block's end butts the next block's side, giving a 580 mm square with a 200 mm square hole in the middle. The ash pan lies on top, and the drum's 572 mm rim stands over the blocks all round. | The pinwheel is the only way four blocks of this size make a square big enough for the drum, and the drum's rim is then carried on block everywhere, not on a 3 mm pan spanning a gap. |
| P2 | The lid's hole was 160 mm, the same as the throat pipe's outside diameter, so the throat had nothing to stand on and would drop into the drum; the collar's bore was also 160 mm with nothing joining it to the throat. | The lid hole is 150 mm. The throat stands on the 5 mm ring of lid inside the collar. The collar is rolled from 1.5 mm sheet to fit the throat snugly and is riveted to the lid by six folded tabs; four rivets join the throat to the collar. | The lid, collar, throat and shroud now lift off as one unit, as the precis describes. The 150 mm hole is a little smaller than the throat's 156 mm bore (8 % less area); the draft calculation does not model this entry, so it is listed in the register to confirm. |
| P3 | The air shroud's top ring only touched the throat, with no fixing. Its band damper was drawn 1 mm clear of the shroud with nothing holding it, and at 40 mm tall it could not close the 40 mm intake gap while still on the shroud. | Six tabs folded up from the shroud's top ring are riveted to the throat. The band damper is 60 mm tall, slides on the shroud and is held by an M6 wing screw in a riveted nut; slid down to the lid it closes the intake with 20 mm still on the shroud. | Riveted and folded, no welding, as BOM line 5 requires. The shroud's position and the 40 mm intake are unchanged, so the secondary air sizing stands. |
| P4 | The four sliding port dampers in BOM line 1 were not modelled and had no way to stay on the drum. | Each port has a curved 60 x 122 mm damper of 1.2 mm sheet that slides 55 mm sideways between two 10 mm guide strips, joggled at their ends and riveted to the drum beyond the damper's travel. Everything stays below the blanket's lower edge, 140 mm above the floor. | A sliding damper must be held top and bottom; riveting through the joggled ends keeps the rivets clear of the damper's path. |
| P5 | The three firebricks stood 150 mm from the axis, exactly under the gas holes' 300 mm circle: one brick covered a gas hole completely and two covered parts of others. | The bricks lie with their long side round the retort, centred 200 mm from the axis, so they carry the retort's edge and stay 8 mm clear of every gas hole. | The gas holes must vent freely into the fire under the retort; the edge of the retort base is also its stiffest part. |
| P6 | The retort sits in a 43 mm annulus inside the outer drum, too narrow for hands, and had nothing to lift it by. | Two M8 U-bolt handles through the retort lid, 130 mm each side of centre, nuts and large washers under the lid. They stand 17 mm below the outer lid. | Bought parts, fitted with a drill; the retort with char (15.5 kg) is lifted by its lid, which is bolted on for the whole batch. |
| P7 | The tripod's ring seat was drawn 7 mm below the jacket and outside its footprint (the ring ran from 212 to 232 mm radius, the jacket's edge is at 210 mm), so nothing carried the jacket. The legs were round stand-ins, the foot plates were not joined to them, and a flat ring of 40 x 6 mm bar is hard to roll without a ring roller. | Three 6 mm steel fins are welded to the jacket shell (the jacket is already the one welded part). Each leg is 40 x 40 x 4 mm angle, one face bolted flat to a fin with two M10 bolts. At the ground each leg is pinned by one M10 bolt to a cleat of the same angle, screwed to a 100 x 100 x 6 mm foot pad. The ring seat is gone. | Every joint is face to face and bolted. Two bolts at each fin make the top joints rigid; with pinned feet the tripod is stable. The leg layout keeps the 1.44 m foot circle; legs are 1.55 m long and lean 18 degrees. |
| P8 | The flue had no seat: it could slide down inside the sleeve. Its rain cap posts were drawn inside the flue bore, touching nothing. The pipe was 700 mm long from a foot 50 mm inside the sleeve, which put the outlet at 2.75 m and the cap only 10 mm above it. | The flue is 650 mm long, so its outlet is at 2.70 m as calculated. Three 20 x 20 x 3 mm angle clips riveted 50 mm above its foot rest on the sleeve rim. The rain cap is riveted to three flat-bar legs riveted to the outside of the flue, 60 mm above the outlet. | Restores the outlet height and cap gap used in CCB-CAL-001; the clips carry the flue and the baffle on the jacket. |
| P9 | The baffle's cross bar (10 x 10 x 156 mm) cut into the flue wall and its "notches" held it in no direction. | The baffle strip has an 11 mm hole near its top and hangs on a 10 mm rod, 160 mm long, through two 11 mm holes 15 mm above the flue's foot. The strip is about 615 mm long and stays 3 mm clear of the sleeve and 10 mm above the throat. | The rod is captured by the holes and the baffle by the rod, so both lift out with the flue for cleaning, as decided in CCB-DDR-002 item 12. |
| P10 | The jacket's loose lid floated 2 mm above the rim, and the vent tube stood on nothing. | The lid (1.5 mm, 420 mm, with a 210 mm centre hole) rests on the shell rim, located by three tabs inside it; the 3/4 in vent nipple passes through it, held by two locknuts. | The jacket stays open to the air through the vent and the centre hole; the hole also clears the flue clips. |
| P11 | The logger box was drawn centred on a tripod leg, so the leg passed through it (REVIEW 2026-09-26, appearance item 3). | The box sits beside the leg's flat face, 520 mm up, held by two hose clips. | As recommended in that review item. |
| P12 | The core probe was drawn coming down through the outer lid from inside the air shroud, under its top ring where it could not be inserted, and through the retort lid; a 300 mm probe could not reach the middle of the charge 490 mm below the lid. The throat probe passed through the sleeve's slip joint as well as the throat. | The core probe (now 500 mm) goes in horizontally at the back, through a 10 mm hole in the drum, a slit in the blanket and a 10 x 40 mm slot in the retort, to the axis at mid-fill (300 mm up the charge). The throat probe (300 mm) goes in at the back 70 mm below the jacket, below the sleeve, through an 8 mm hole. | Plain holes, no glands: the annulus and throat are below atmospheric pressure, so little air leaks in, and any retort gas through the slot burns in the annulus as designed. The core probe is withdrawn before the retort is lifted. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Masses | Kiln 97 kg (was 96 kg); jacket empty 23.3 kg (fins, thicker loose lid); lift unit 47.4 kg, 23.7 kg each for two people (was 46.6 kg, 23.3 kg); retort with char 15.5 kg; full jacket 85 kg. Tripod leg free length 1.43 m, factor of safety against buckling 58 (was 51) [CCB-CAL-001 section 4]. R11 is still met, with 1.3 kg per person to spare. | Fins, U-bolts, 60 mm band, cleats and pads added; ring seat removed; flue 50 mm shorter. |
| Energy | Flue gas heat at the jacket inlet 61 MJ (was 60 MJ, rounding of a 0.1 MJ change in stored heat); heat to water unchanged at 11.5 MJ; secondary hole area needed 28.6 cm² (was 28.5) against 33.9 cm². No requirement status changed. | Calculations re-run (`docs/04-calcs/sizing.py`). |
| BOM | Lines 1 to 8, 10, 12 to 15 re-specified to the parts above; prices left as they were ($319). | Small parts were added without re-pricing; see Table 3, A1. |
| Drawings and media | CCB-DWG-001 Rev P5; concept sheet CCB-DWG-010 Rev P4; making sketches CCB-DWG-101 to 114; STEP, STL, the interactive model and concept media regenerated. | Follows the model. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Cost. The parts added for construction (U-bolts, fins, foot cleats and pads, guide strips, clips, rod, bolts) are not priced; together they probably add about $5 to $10 against a $1 margin (R10). | (a) keep `budget_usd: 320` and re-price at purchase; (b) top up to $330 now; (c) find savings elsewhere (for example a cheaper logger box). | (b), since R10 is unlikely to hold once the parts are quoted. A budget change is Amish's decision. |
| A2 | The fire under the retort heats the drum floor, which stands on a 3 mm pan on concrete blocks. Concrete can crack or spall when heated. | (a) build as modelled and measure the block surface temperature on the first burn; (b) lay a 25 mm ceramic fibre board between the pan and the blocks. | (a), with a hold point in the build plan's first checks; (b) if the blocks pass about 150 °C. |
| A3 | The jacket sleeve must be lowered over the throat with 2 mm clear all round, by two people lifting a 47 kg unit to about 1.5 m. | (a) as modelled; (b) flare the bottom 20 mm of the sleeve out to about 190 mm so it guides itself onto the throat (a welding detail for the fabricator). | (b): it costs little at the welder and makes the lift safer. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CCB-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status is unchanged: six met, five at risk (R2, R3, R5, R6, R8), one not verifiable at TRL 3 (R4) (CCB-CAL-001 v0.4).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept's ring seat, round-post rain cap and logger position; they need updating on Amish's Mac, where Blender is. Appearance items 2 and 3 of the 2026-09-26 review (tripod sections, logger position) are now settled by P7 and P11.
- Drum sizes vary by maker; the 43 mm annulus, the retort's bolt ring and the probe slot position must be checked on the drums actually bought.
