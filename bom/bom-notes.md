# BOM notes

Prices are indicative USD estimates for TRL 3, priced by supplier type (drum reconditioner or scrap dealer, local fabricator, steel stockist, hardware shop, refractory supplier, electronics distributor). Named suppliers depend on the first region, which is still open (CCB-DDR-001 item 9). Item numbers match the exploded view (`media/exploded.png`), the components table in `docs/02-concept.md` and the drawing CCB-DWG-001. Item 14 is in the BOM but not modelled.

Value-engineering target: USD 320. Estimated cost of the constructable design: USD 546 (USD 226 over the target). The 18 lines are all priced, each with its basis in its notes (checked by `docs/04-calcs/sizing.py`, CCB-CAL-001 v0.6 section 11). Lines 15 to 17 ($22) were added when Amish accepted the recommendations for R6 and R8 on 2026-09-25 (CCB-DDR-002 items 12 and 13). The lifting aid (line 18, $160) is most of the overrun; it could serve several kilns on one site.

## Safety kit (required, outside the kiln parts target)

Decided by Amish, 2026-09-25 (CCB-DDR-001 item 2): the kiln parts value-engineering target ($320) covers kiln parts only, and the safety kit is required and listed separately. Decided by Amish, 2026-09-25 (CCB-DDR-002 item 16): this table and CCB-REQ-001 R10 are where the safety kit requirement is stated, since build notes are TRL 4 material.

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

## Changes for construction (CCB-DDR-003, 2026-09-30, Draft)

Made under Amish's 2026-09-30 instruction to make the design physically buildable; accepted by Amish on 2026-10-02. The added parts were priced on 2026-10-02 (below).

- Line 1: sliding port dampers now held in riveted guide strips; 10 mm core probe hole.
- Line 2: 150 mm lid hole; collar rolled to the throat and riveted on by six tabs.
- Line 3: probe slot in the retort side; two M8 U-bolt handles on the lid.
- Line 4: bricks laid round the retort's edge, clear of the gas holes.
- Line 5: shroud riveted to the throat by six tabs; 60 mm band damper with a wing screw.
- Line 6: probe hole; riveted to the collar.
- Line 7: flue 650 mm (was 700 mm), resting on three riveted stop clips; rain cap on three riveted legs.
- Line 8: three 6 mm fins welded to the jacket for the legs; loose lid located by tabs; vent nipple with locknuts.
- Line 10: legs bolted to the jacket fins and pinned to bolted foot cleats and pads; the flat-bar ring seat is gone.
- Line 12: blocks laid as a pinwheel.
- Line 13: core probe 500 mm, in through the drum side; throat probe 300 mm.
- Line 14: fasteners listed (rivets, M10 and M8 bolts, U-bolts, wing screw, hose clips).
- Line 15: strip about 615 mm, hung on a 10 mm rod through the flue foot.

## Priced on 2026-10-02 (approved follow-ups)

- Parts added for construction, $17 in all: line 1 guide strips +$2, line 3 U-bolts +$3, line 7 clips and cap legs +$2 (the conical cap from 1.5 mm sheet costs about the same as the flat 3 mm plate it replaces), line 8 fins, flare and lift-bar holes +$5, line 10 foot cleats and pads +$5, line 14 extra fasteners +$3 (with the labels below), line 15 hanger rod +$1 (the baffle line is now $8).
- Decided on 2026-10-02, $186 in all: line 12 ceramic fibre board +$28; line 13 block thermocouple and third amplifier +$10; line 14 two ISO 7010 W017 labels +$8; line 18 lifting aid $160.
- Line 8: the bottom 20 mm of the sleeve is flared to about 190 mm, and two 18 mm holes across the top socket take the lift bar.

The largest cost drivers are the lifting aid ($160), the water jacket ($65), the temperature logger ($42), the plinth with its fibre board ($40), the insulation blanket ($35) and the retort drum ($28). Drums are priced as used. Never use a drum that held fuel, solvent or pesticide, and never use galvanized pipe or drums in the hot path.
