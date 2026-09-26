# BOM notes

Prices are indicative USD estimates for TRL 3, priced by supplier type (drum reconditioner or scrap dealer, local fabricator, steel stockist, hardware shop, refractory supplier, electronics distributor). Named suppliers depend on the first region, which is still open (CCB-DDR-001 item 9). Item numbers match the exploded view (`media/exploded.png`), the components table in `docs/02-concept.md` and the drawing CCB-DWG-001. Item 14 is in the BOM but not modelled.

The 17 lines total **$319**, $19 over the $300 kiln budget (checked by `docs/04-calcs/sizing.py`, CCB-CAL-001 v0.2 section 11). Lines 15 to 17 ($21) were added when Amish accepted the recommendations for R6 and R8 on 2026-09-25 (CCB-DDR-002 items 12 and 13). Whether to raise the kiln budget to $320 or cut a line is proposed, awaiting Amish (CCB-DDR-002 item 17); `budget_usd` stays at 300 until then.

## Safety kit (required, outside the kiln budget)

Decided by Amish, 2026-09-25 (CCB-DDR-001 item 2): the $300 budget covers kiln parts only, and the safety kit is required and listed separately. Decided by Amish, 2026-09-25 (CCB-DDR-002 item 16): this table and CCB-REQ-001 R10 are where the safety kit requirement is stated, since build notes are TRL 4 material.

| Item | Indicative cost (USD) |
| --- | --- |
| Fire extinguisher (or a 50 L water drum and a shovel) | 20 |
| Heat-resistant gloves | 10 |
| Eye protection | 5 |
| Dust mask for crushing char and cutting the blanket | 5 |
| **Total** | **40** |

## Changes at TRL 3

- Line 5: a 230 mm air shroud around the throat replaces the 25 mm pipe ring, which could not pass the secondary air (CCB-CAL-001 section 6; decided by Amish, 2026-09-25, CCB-DDR-002 item 11). $12 to $14.
- Line 6: two rings of 12 mm air holes in place of one ring of 10 mm holes; 30 holes (15 per ring) since DDR-002, to offset the baffle insert pressure drop.
- Line 7: the flue is 700 mm, since the jacket now carries its own 168 mm flue sleeve. $30 to $22.
- Line 8: the jacket has 2 mm walls and an integral sleeve. $55 to $60.
- Line 13: class 1 (special limits) thermocouple probes, needed for R9.

## Changes from DDR-002 (decided by Amish, 2026-09-25)

- Line 15: spiral baffle insert in the jacket sleeve, $7 (item 12).
- Line 16: 25 mm mineral wool blanket on the jacket shell, $8 (item 12). Mineral wool suits the jacket because its outer face stays below 100 °C.
- Line 17: 25 mm ceramic fibre blanket on the lid and top band, $6 (item 13), cut from the same product as line 11.

The largest cost drivers are the water jacket ($60), the insulation blanket ($35), the temperature logger ($32) and the retort drum ($25). Drums are priced as used. Never use a drum that held fuel, solvent or pesticide, and never use galvanized pipe or drums in the hot path.
