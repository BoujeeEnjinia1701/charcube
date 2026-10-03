---
doc_id: CCB-CAL-001
title: CharCube sizing and first-principles checks
project: CharCube
doc_type: Calculation note
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (batch, char, heating time, shell loss, masses, energy balance, draft and air, jacket, cooling, carbon, logger, cost) against every requirement
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); baffle insert, jacket and lid blankets, 30 throat air holes, R5 at 5 h, R9 to 700 °C; all tables re-run
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish
- version: "0.4"
  date: '2026-09-30'
  author: Amish Chadha
  change: Re-run for the constructable design (CCB-DDR-003); masses, tripod legs on fins, flue length; no requirement status changed
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: Approved 2026-10-02 decisions carried in (fibre board, sleeve flare, conical cap, labels, lifting aid); lifting aid loads added; every part priced; R10 now not met
---

# CharCube sizing and first-principles checks

On paper the nested-drum retort works as a kiln, and with the changes Amish accepted on 2026-09-25 (CCB-DDR-002) it also works as a water heater. Five of the twelve requirements are met, five are at risk, one cannot be verified at TRL 3 and one is not met. R10 is not met: with every part priced, including the parts added for construction and the additions Amish decided on 2026-10-02 (fibre board, block thermocouple, hot-surface labels and the lifting aid), the estimated cost is $546 against the $320 value-engineering target. The baffle and jacket blanket raise the heat into the water from 6.4 MJ to about 11.5 MJ (R6 at risk), the lid blanket cuts the wood from 5.8 kg to about 3.7 kg (R8 at risk), and R5 was relaxed to 5 h (at risk). The 25 mm secondary air ring of TRL 2 would have starved the burner throat; the model uses an air shroud with 30 air holes. The lifting aid (section 4) means nobody lifts the 47 kg heat-recovery unit by hand, so R11 is met with a wide margin.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `PARAMS` in `cad/src/model.py` and the prices from `bom/bom.csv`, so the model, the drawing CCB-DWG-001 and this note agree. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless marked as decided.*

| Input | Value | Basis |
| --- | --- | --- |
| Kiln, jacket, throat, logger, blanket, tripod | As decided | CCB-DDR-001 items 1 to 8 |
| Air shroud, baffle insert, jacket and lid blankets | As decided | CCB-DDR-002 items 11 to 13 |
| Feedstock | Bundled straw, maize or cotton stalks and cobs, packed to 120 kg/m³ air-dry at 12 % moisture (wet basis) | Decided feedstock, CCB-DDR-001 item 4; density as TRL 2 |
| Feed, dry ultimate analysis | C 45, H 5.8, O 40.4, N 0.8, ash 8.0 % | Typical for maize and cotton stalks; straw-rich loads have more ash |
| Char | C 55, H 2.5, N 1.0 %, ash from a mass balance, O by difference | Yield 28 % of dry feed (20 to 35 %), as TRL 2 |
| Heating values | Channiwala and Parikh correlation from the analyses | [Channiwala and Parikh 2002, *Fuel* 81: 1051 to 1063](https://doi.org/10.1016/S0016-2361(01)00131-4) |
| Start-up wood | Air-dry, 12 % moisture; C 50, H 6.0, O 43.2 % dry | Prunings or split wood |
| Burn | Annulus gas held at 650 °C, retort wall at 600 °C, until the core reaches 450 °C, then 30 min more (R3) | Operating intent |
| Charge | Effective heat capacity 2.72 kJ/kg K per kg dry (sensible, drying and 0.4 MJ/kg net pyrolysis heat); bed conductivity 0.20, 0.35 or 0.50 W/m K | Packed straw is about 0.1 W/m K cold; radiation in the pores raises it when hot |
| Air | Overall excess air ratio 1.6, 2.0 or 2.4; 40 % of the air enters as secondary air at the throat; 15 % of the volatiles burn in the throat | Small batch kilns run lean; damper setting |
| Combustion efficiency | 95, 90 or 85 % of the lower heating value | Allows for CO, methane, tar and soot |
| Blankets | 25 mm ceramic fibre, 128 kg/m³, 0.09 W/m K at a mean of about 350 °C, on the side and on the lid and top band; 25 mm mineral wool, 0.05 W/m K, on the jacket shell | Supplier data typical; air ports, throat and the lid under the shroud bare |
| Spiral baffle insert | Gas-side convection in the sleeve multiplied by 3; 4 extra velocity heads of pressure loss | Assumption for a twisted strip in laminar and transitional flow; to be measured (TRL 4, on hold) |
| Outside surfaces | Emissivity 0.9, still air at 20 °C | Worst case for surface temperature is sun and no wind |
| Carbon | 100-year permanence factor 0.80 (IPCC medium temperature); methane 24 g per kg of char at GWP100 28 | As CCB-PRC-001 v0.2, with sources there |

Three scenarios bracket the result: **favourable** (bed conductivity 0.50 W/m K, excess air 1.6, efficiency 95 %, yield 35 %), **central** (0.35, 2.0, 90 %, 28 %) and **unfavourable** (0.20, 2.4, 85 %, 20 %). Central values are quoted unless a range is given.

## 2. Batch and char (R1, R2)

The retort holds 100 L of packed feed at a 600 mm fill depth (123 L geometric volume), which is **12.0 kg** air-dry: 10.58 kg of dry matter and 1.44 kg of water. R1 is **met** for the decided feedstock. Loose chopped straw at 40 kg/m³ would give only 4.0 kg; it is outside the decided feedstock (CCB-DDR-001 item 4).

At 28 % yield the batch makes **2.96 kg** of char (2.12 to 3.70 kg). All the feed ash stays in the char, so the char is about 29 % ash (23 to 40 %), and its heating value is about 20.2 MJ/kg, lower than the 24 MJ/kg assumed at TRL 2. About 34 % of the feed carbon stays in the char. R2 is **at risk**: the 28 % central estimate clears the 25 % target, but the range does not.

A straw-rich load with 15 % ash would push char ash above 45 %, which is not consistent with 55 % carbon; the script warns when that happens.

## 3. Heating time (R3, R5)

The burn is set by heat conduction into the packed charge, not by the fire. A one-term solution for a finite cylinder (radius 0.23 m, 0.6 m high, heated on all faces) gives the core 450 °C after:

*Table 2. Heating and burn time.*

| Scenario | Bed conductivity | Core at 450 °C after lighting | Light to end of burn (R5) |
| --- | --- | --- | --- |
| Favourable | 0.50 W/m K | 2.9 h | 3.4 h |
| Central | 0.35 W/m K | 4.0 h | **4.5 h** |
| Unfavourable | 0.20 W/m K | 6.5 h | 7.0 h |

The times include 0.5 h of warm-up and a 30 min hold at 450 °C for R3. R3 is **at risk**: it is reachable if the annulus is held hot long enough, which is what drives the wood demand in section 5. R5, relaxed to 5 h by Amish's decision (CCB-DDR-002 item 14), is met on the central estimate but **at risk** because the unfavourable case takes 7.0 h. The blankets do not change the burn time, which conduction into the charge sets. Sealed cooling (section 8) is short enough for the 16 h unload limit.

## 4. Shell loss, surfaces and masses (R11, R12)

*Table 3. Heat loss during the burn (annulus gas 650 °C).*

| Surface | Area | Surface temperature | Loss |
| --- | --- | --- | --- |
| Blanketed side | 1.33 m² | 125 °C | 2.20 kW |
| Port band, bare | 0.25 m² | 168 °C | 0.69 kW |
| Lid and top band, blanketed | 0.28 m² | 120 °C | 0.43 kW |
| Lid under the air shroud, bare | 0.04 m² | 257 °C | 0.24 kW |
| Burner throat, bare | 0.20 m² | 223 °C | 0.91 kW |
| **Total** | | | **4.47 kW** |

Without the side blanket the side would run at about 311 °C and lose 11.3 kW, so the side blanket (decided, item 7) roughly halves the loss. The lid and top band blanket (CCB-DDR-002 item 13) cuts that part from 1.90 kW (257 °C, v0.1) to 0.67 kW, a saving of **1.22 kW**, a little less than the 1.4 kW estimated in v0.1 because the lid under the shroud stays bare so the secondary air is not blocked.

*Table 4. Masses.*

| Part | Mass |
| --- | --- |
| Outer drum with hoops and ring | 18.8 kg |
| Outer lid with collar | 3.4 kg |
| Retort with lid and U-bolt handles | 12.6 kg |
| Burner throat; air shroud with band damper | 3.2 kg; 2.0 kg |
| Firebricks (3); side blanket; lid blanket | 2.6 kg; 4.3 kg; 1.0 kg |
| Water jacket, empty, with fins and loose lid | 23.3 kg |
| Spiral baffle insert; jacket shell blanket | 1.2 kg; 2.2 kg |
| Flue with clips and conical cap; tripod legs, cleats and pads; tap | 6.2 kg; 13.9 kg; 0.6 kg |
| **Kiln without plinth and water** | **97 kg** |
| Heat-recovery lift unit (tripod, drained jacket with baffle and blanket, flue, tap) | 47.2 kg, raised by the lifting aid's winch |
| Fibre board under the pan (plinth, stays in place) | 2.9 kg |
| Retort with char | 15.5 kg: one person |
| Jacket full (61.4 L at 540 mm depth) | 85 kg, never moved full |

R11 is **met**. Since Amish's decision of 2026-10-02 the drained heat-recovery unit is raised and moved by the lifting aid, so nobody carries it; the heaviest hand lift in use is the retort with char, 15.5 kg, and the heaviest when setting up is the lifting aid's post, about 16 kg each for two people. The only welded part of the kiln is the jacket, with its three leg fins; the collar, shroud, baffle, tripod and lifting aid are riveted, bolted or folded (CCB-DDR-003). Each tripod leg (40 x 40 x 4 mm angle bolted to a jacket fin and pinned at a foot cleat, 1.46 m between the foot pin and the lower fin bolt, slenderness 187) carries about 325 N with a full jacket against an Euler load of 18.3 kN, a factor of about 56. The 25 mm fibre board under the pan raises the whole kiln by 25 mm; the air ports, draft and every clearance were re-checked in the model.

**Lifting aid (decided by Amish, 2026-10-02).** A post of 88.9 x 3.2 mm tube, 4.0 m above the ground, turns in a ground sleeve set in a concrete footing 1.2 m behind the kiln. Two 50 x 50 x 5 mm angles bolted either side of its top make the arm, braced by two 40 x 40 x 4 mm angles; a hand brake winch on the post winds a 5 mm steel wire rope over two pulleys to a hook 1.2 m out, over the kiln's axis. With the flue lifted out, a 16 mm bar goes through two holes in the jacket sleeve's top socket and the hook takes it by a shackle. The winch raises the unit 1.55 m, until its feet are above the top of the burner throat, so it clears the kiln whichever way it turns on the hook; the arm then swings it 90 degrees and sets it down clear of the kiln. Everything is bolted.

*Table 4a. Lifting aid loads (hook load with a dynamic factor of 1.5).*

| Check | Result |
| --- | --- |
| Hook load: drained unit, lift bar and shackle | 47.8 kg; 704 N with the factor |
| Bending at the ground in the post | 967 N m; 54 MPa, a factor of 4.3 on yield; top deflection about 46 mm |
| Arm (two 50 x 50 x 5 angles) at the brace | 352 N m; 58 MPa, a factor of 4.1 |
| Brace (two 40 x 40 x 4 angles) | 1,561 N against an Euler load of 39.6 kN each |
| Lift bar, 16 mm across the 168 mm sleeve | 74 MPa, a factor of 3.2 |
| Winch rated 270 kg; 5 mm steel wire rope (about 15 kN breaking) | Factors of 3.8 and 21 |
| Footing 600 x 600 x 750 mm (621 kg) against overturning, by its weight alone | 1,988 N m against 967 N m, a factor of 2.1 |
| Heaviest hand lifts | Retort with char 15.5 kg; post 16 kg each for two; one arm angle 5.7 kg |

R12 is **met**: the flue outlet is 2.72 m above the ground and no BOM line calls for galvanized parts. The 5 m clearance is an operating rule (CCB-PRC-001, Safety); the lifting aid's arm is swung away from the flue while the kiln burns.

## 5. Energy balance and start-up wood (R8)

Wood makes up whatever the burning volatiles cannot supply while the annulus is held at 650 °C for the whole burn. The sinks are the retort charge and steel (19 MJ), the stored heat in the drum, lid, throat, bricks and blankets (9 MJ), the shell loss over the burn, and the heat carried out by the annulus gas.

*Table 5. Energy per batch.*

| Quantity | Favourable | Central | Unfavourable |
| --- | --- | --- | --- |
| Burn time | 3.4 h | 4.5 h | 7.0 h |
| Volatiles, lower heating value | 104 MJ | 117 MJ | 132 MJ |
| Energy left in the char | 73 MJ | 60 MJ | 45 MJ |
| Shell loss over the burn | 55 MJ | 72 MJ | 113 MJ |
| **Wood needed (R8)** | 1.7 kg | **3.7 kg** | 9.8 kg |
| Heat released in the kiln | 125 MJ | 160 MJ | 247 MJ |
| Flue gas per batch | 79 kg | 128 kg | 246 kg |
| Gas leaving the throat (jacket inlet) | 471 °C | 432 °C | 396 °C |

Light-up alone needs about 1.7 kg of wood; in the favourable case that is all the wood needed. R8 is met on the central estimate (3.7 kg against 5 kg) but **at risk**, because a long burn with a poorly conducting charge needs about 9.8 kg. Excess air matters as much as burn time: every kilogram of surplus air leaves at 650 °C. Figure 2 in CCB-PRC-001 shows the central energy flow: 253 MJ in (residue at its higher heating value, wood at its lower), 60 MJ kept in the char, 33 MJ as latent heat and unburned gas, 160 MJ released, 99 MJ to the charge, structure and shell, and 61 MJ in the flue gas at the jacket, of which 11.5 MJ goes into the water.

## 6. Gas flow, draft and air (R4)

*Table 6. Flow checks at the central case; peak flow is taken as twice the mean.*

| Check | Result |
| --- | --- |
| Volatiles leaving the retort, mean and peak | 0.73 and 1.46 g/s |
| Eight 20 mm gas holes (25.1 cm²) at peak | 1.3 m/s, 1.0 Pa: little back-pressure in the retort |
| Flue gas, mean and peak | 8.0 and 15.9 g/s |
| Draft, air ports to outlet (2.43 m) | 16.7 Pa |
| Losses at peak: flue path (including 4 velocity heads for the baffle) and primary ports | 5.6 and 0.17 Pa; margin 2.4 |
| Throat velocity at peak; flue velocity above the jacket | 1.69 m/s; 0.75 m/s |
| Secondary air at peak (40 % of air) | 4.88 g/s |
| Suction at the throat air holes at peak | 5.2 Pa |
| Secondary hole area needed and provided | 28.6 and 33.9 cm² (30 x 12 mm in two rings, 34 mm pitch) |
| TRL 2 25 mm inlet pipe at the same flow | 7.2 m/s and about 46 Pa: **would not work** |
| Air shroud intake (230 mm sleeve, 204 cm²) | 0.20 m/s |

The draft is enough, with a margin of about 2.4 at peak (3.2 before the baffle). The baffle's resistance lowers the suction at the throat holes from 7.6 to 5.2 Pa, so the 24 holes of v0.1 (27.1 cm²) would have been about 5 % short; the model now has 30 holes with about 19 % spare area. The air shroud was accepted by Amish (CCB-DDR-002 item 11). R4 is **not verifiable at TRL 3**: the gas route is closed by design and the air paths are sized, but smoke and methane depend on mixing and temperature and need measurement.

## 7. Water jacket (R6, R7)

The 600 mm flue sleeve (164 mm bore, 0.31 m² wetted) sees gas at 396 to 471 °C and a Reynolds number of about 1,400 to 2,100, which is laminar or transitional. A plain sleeve gives only about 1 to 3 W/m²K by convection and 2 to 2.5 W/m²K by gas radiation. The spiral baffle insert (CCB-DDR-002 item 12) is taken to triple the convection, to about 4 to 7 W/m²K, so the sleeve takes about 21 to 24 % of the gas heat, and the mineral wool blanket keeps most of it in the water.

*Table 7. Heat into the water per batch (61.4 L, starting at 20 °C).*

| Case | Heat to water | Water temperature rise |
| --- | --- | --- |
| Favourable (short burn) | 9.0 MJ | |
| **Central, design (baffle and jacket blanket)** | **11.5 MJ** | about 45 K |
| Unfavourable (long burn) | 19.1 MJ | |
| Central, plain sleeve and bare jacket (v0.1 design) | 5.6 MJ | |
| Central, jacket blanket only | 6.7 MJ | |
| Central, baffle insert only | 9.5 MJ | |

The comparison rows use the v0.2 flue gas flow, which is lower than in v0.1 because less wood is burned; that is why the plain sleeve now gives 5.6 MJ, not 6.4 MJ. R6 is **at risk**: the central case meets 10 MJ, but a short burn gives about 9.0 MJ, and the factor of 3 for the insert is an assumption until measured. The water does not boil in any scenario (boiling needs 20.6 MJ), but the long burn reaches 19.1 MJ, so R7 (open vent, loose lid, no sealing valve) is essential. R7 is **met** by design.

The sleeve wall and the baffle run close to the water temperature, far below the tar dew point, so any tar that escapes the throat will deposit there and cut heat transfer. The baffle hangs from the foot of the flue and lifts out with it for cleaning. While the water is below about 41 °C, water vapor from the flue gas condenses on the sleeve and will drip back into the throat.

## 8. Cooling and unloading (R5)

With the ports and damper closed, the kiln and char (30 kJ/K) lose heat through a shell conductance of about 10.2 W/K (lower than v0.1 because the lid is blanketed), a time constant of about 0.8 h, so the shell falls to 60 °C in about 2.1 h. The char core then needs about 1.6 h more by conduction. The sum, about **3.6 h**, puts unloading at about 8 h after lighting in the central case, inside the 16 h limit. The char should still be left sealed overnight, because air reaching hot char can reignite it (CCB-PRC-001, Safety).

## 9. Carbon

*Table 8. Carbon per batch (100-year basis).*

| Scenario | Carbon stored | CO₂ | Methane penalty | Net |
| --- | --- | --- | --- | --- |
| Favourable | 1.63 kg C | 6.0 kg | 2.5 kg CO₂e | 3.5 kg CO₂e |
| Central | 1.30 kg C | 4.8 kg | 2.0 kg CO₂e | **2.8 kg CO₂e** |
| Unfavourable | 0.93 kg C | 3.4 kg | 1.4 kg CO₂e | 2.0 kg CO₂e |

At 250 batches a year the central case makes about 740 kg of char and a net removal of about **0.70 t CO₂e**, and keeps about 3.0 t of residue out of open burning. The methane penalty assumes the retort field average; a working burner throat would lower it, but that cannot be shown without measurement. Start-up wood is assumed to come from residues or prunings and is not counted as an emission.

## 10. Logger (R9)

A type K class 2 probe is good to ±5.2 °C at 700 °C; with the MAX31855 amplifier (±2 °C from −200 to 700 °C, [datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/max31855.pdf)) the combined error is about ±5.6 °C, just outside ±5 °C. Class 1 (special limits) probes give about ±3.4 °C to 700 °C. R9 was restated by Amish's decision (CCB-DDR-002 item 15) as ±5 °C from 0 to 700 °C and indicative above, so it is **met** with class 1 probes. A 0.25 W logger uses about 6 Wh in 24 h against about 31 Wh usable from a 10,000 mAh power bank, and writes about 276 kB a day.

## 11. Cost (R10)

Value-engineering target: USD 320. Estimated cost of the constructable design: USD 546 (USD 226 over the target).

The 18 BOM lines are now all priced, each with its basis in the line's notes (2026-10-02). The parts added for construction (guide strips, U-bolts, clips and cap legs, fins, foot cleats and pads, extra fasteners, hanger rod) add $17 to the earlier $319. The additions Amish decided on 2026-10-02 add $186: the fibre board $28, the block thermocouple and its amplifier $10, the two hot-surface labels $8 and the lifting aid $160 (line 18, about $53 of tube, $30 for the winch and $25 for the footing among it). Lines 15 to 17 (baffle insert $8, jacket blanket $8, lid blanket $6) came from items 12 and 13 of CCB-DDR-002. The safety kit (about $40) is required and listed separately in `bom/bom-notes.md`, outside the kiln parts target (CCB-DDR-001 item 2). The script reads the target from `project.yaml`, which is unchanged. R10 is **not met**. Without the lifting aid the estimate would be $386, still $66 over.

## 12. Results against requirements

*Table 9. Every requirement in CCB-REQ-001 v0.9. Also written to `docs/04-calcs/results.csv`.*

| ID | Requirement (short) | Value (central, range) | Target | Status |
| --- | --- | --- | --- | --- |
| R10 | Kiln parts cost | $546, every part priced (lifting aid $160) | $320 or less (target) | Not met ($226 over) |
| R2 | Char yield | 28 % (20 to 35 %); 2.96 kg | 25 % or more | At risk |
| R3 | Core 450 °C for 30 min | Core at 450 °C 4.0 h after lighting (2.9 to 6.5 h) if the annulus is held at 650 °C | 450 °C, 30 min | At risk |
| R5 | Light to end of flaming; unload | Burn 4.5 h (3.4 to 7.0 h); unload after about 8 h | 5 h or less (relaxed); 16 h or less | At risk |
| R6 | Heat into water per batch | 11.5 MJ (9.0 to 19.1 MJ) with baffle and jacket blanket | 10 MJ or more | At risk |
| R8 | Start-up wood per batch | 3.7 kg (1.7 to 9.8 kg); light-up alone 1.7 kg | 5 kg or less | At risk |
| R4 | Burn the gas; smoke; methane | Route closed by design; draft margin 2.4; air holes sized | Methane below 24 g/kg | Not verifiable at TRL 3 |
| R1 | Batch size, decided feedstock | 12.0 kg packed (loose straw 4.0 kg, excluded) | 10 kg or more | Met |
| R7 | Open water circuit | Open vent, loose lid, tap at base, tripod-carried | By design | Met |
| R9 | Logger accuracy and endurance | ±3.4 °C to 700 °C with class 1 probes; 6 of 31 Wh | ±5 °C to 700 °C (restated) | Met |
| R11 | Crew and lifts | Unit raised by the lifting aid's winch; heaviest hand lift the retort with char, 15.5 kg | 25 kg per person or less | Met |
| R12 | Outlet height; no galvanized hot parts | 2.72 m; none | 2.5 m or more | Met |

## 13. Limits of this note

- The heating-time model treats the charge as a solid with a fixed effective conductivity. Real beds shrink, crack and release gas, which can speed or slow heating; the three scenarios bracket this but do not replace logged batches.
- The baffle insert's heat transfer gain (x3) and pressure loss (4 velocity heads) are assumptions; fouling will reduce the gain over a season.
- Surface coefficients assume still air. Wind raises the shell loss and the wood demand.
- The methane figure is a literature average, not a prediction for this design.
- The lifting aid is checked by hand formulas with a dynamic factor of 1.5. The footing check ignores the soil's support, and the winch and rope ratings are catalogue figures to confirm at purchase.
- Nothing here has been measured. Checking these numbers against logged batches is TRL 4 work, which is on hold by Amish's instruction.

> **Safety:** These are paper estimates for a fire that produces flammable, toxic gas and hot water. The surface temperatures in Table 3 (120 to 257 °C on the shell, higher on the flue) burn skin on contact. With the baffle and jacket blanket a long batch brings the water within about 1.5 MJ of boiling, so the water jacket must stay open-vented and at least three-quarters full. See CCB-PRC-001, Safety.
