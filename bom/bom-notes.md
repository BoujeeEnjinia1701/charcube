# BOM notes

Prices are indicative USD estimates for TRL 3, priced by supplier type (drum reconditioner or scrap dealer, local fabricator, steel stockist, hardware shop, refractory supplier, electronics distributor). Named suppliers depend on the first region, which is still open (CCB-DDR-001 item 9). Item numbers match the exploded view (`media/exploded.png`), the components table in `docs/02-concept.md` and the drawing CCB-DWG-001. Item 14 is in the BOM but not modelled.

The 14 lines total **$298**, within the $300 kiln budget with $2 of margin (checked by `docs/04-calcs/sizing.py`, CCB-CAL-001 section 11).

## Safety kit (required, outside the kiln budget)

Decided by Amish, 2026-09-25 (CCB-DDR-001 item 2): the $300 budget covers kiln parts only, and the safety kit is required and listed separately.

| Item | Indicative cost (USD) |
| --- | --- |
| Fire extinguisher (or a 50 L water drum and a shovel) | 20 |
| Heat-resistant gloves | 10 |
| Eye protection | 5 |
| Dust mask for crushing char and cutting the blanket | 5 |
| **Total** | **40** |

## Changes at TRL 3

- Line 5: a 230 mm air shroud around the throat replaces the 25 mm pipe ring, which could not pass the secondary air (CCB-CAL-001 section 6; proposed, awaiting Amish, CCB-DDR-001 item 11). $12 to $14.
- Line 6: two rings of 12 x 12 mm air holes in place of one ring of 10 mm holes.
- Line 7: the flue is 700 mm, since the jacket now carries its own 168 mm flue sleeve. $30 to $22.
- Line 8: the jacket has 2 mm walls and an integral sleeve. $55 to $60.
- Line 13: class 1 (special limits) thermocouple probes, needed for R9.

## Not in the BOM (proposed, awaiting Amish)

- Spiral baffle insert for the jacket sleeve and a 25 mm blanket on the jacket shell (about $15), for R6 (CCB-DDR-001 item 12).
- Ceramic fibre disc for the lid and top band (about $6), for R8 (item 13).

Either would take the total over $300 unless another line is cut.

The largest cost drivers are the water jacket ($60), the insulation blanket ($35), the temperature logger ($32) and the retort drum ($25). Drums are priced as used. Never use a drum that held fuel, solvent or pesticide, and never use galvanized pipe or drums in the hot path.
