---
doc_id: CCB-CAL-001
title: CharCube sizing and first-principles checks
project: CharCube
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (batch, char, heating time, shell loss, masses, energy balance, draft and air, jacket, cooling, carbon, logger, cost) against every requirement
---

# CharCube sizing and first-principles checks

On paper the nested-drum retort works as a kiln, but it is weaker as a water heater and hungrier for wood than the TRL 2 estimates said. Five of the twelve requirements are met, three are at risk and one cannot be verified at TRL 3. Three are **not met** on the central estimate: R5 (burn about 4.5 h against 4 h, because heat conducts slowly into the packed charge), R6 (about 6.4 MJ into the water against 10 MJ, because a plain flue sleeve transfers only about 4 to 5 W/m²K) and R8 (about 5.8 kg of wood against 5 kg, because the burn is long and the shell loses about 5.7 kW). The 25 mm secondary air ring of TRL 2 would have starved the burner throat; the model now uses an air shroud.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `PARAMS` in `cad/src/model.py` and the prices from `bom/bom.csv`, so the model, the drawing CCB-DWG-001 and this note agree. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless marked as decided.*

| Input | Value | Basis |
| --- | --- | --- |
| Kiln, jacket, throat, logger, blanket, tripod | As decided | CCB-DDR-001 items 1 to 8 |
| Feedstock | Bundled straw, maize or cotton stalks and cobs, packed to 120 kg/m³ air-dry at 12 % moisture (wet basis) | Decided feedstock, CCB-DDR-001 item 4; density as TRL 2 |
| Feed, dry ultimate analysis | C 45, H 5.8, O 40.4, N 0.8, ash 8.0 % | Typical for maize and cotton stalks; straw-rich loads have more ash |
| Char | C 55, H 2.5, N 1.0 %, ash from a mass balance, O by difference | Yield 28 % of dry feed (20 to 35 %), as TRL 2 |
| Heating values | Channiwala and Parikh correlation from the analyses | [Channiwala and Parikh 2002, *Fuel* 81: 1051 to 1063](https://doi.org/10.1016/S0016-2361(01)00131-4) |
| Start-up wood | Air-dry, 12 % moisture; C 50, H 6.0, O 43.2 % dry | Prunings or split wood |
| Burn | Annulus gas held at 650 °C, retort wall at 600 °C, until the core reaches 450 °C, then 30 min more (R3) | Operating intent |
| Charge | Effective heat capacity 2.72 kJ/kg K per kg dry (sensible, drying and 0.4 MJ/kg net pyrolysis heat); bed conductivity 0.20, 0.35 or 0.50 W/m K | Packed straw is about 0.1 W/m K cold; radiation in the pores raises it when hot |
| Air | Overall excess air ratio 1.6, 2.0 or 2.4; 40 % of the air enters as secondary air at the throat; 15 % of the volatiles burn in the throat | Small batch kilns run lean; damper setting |
| Combustion efficiency | 95, 90 or 85 % of the lower heating value | Allows for CO, methane, tar and soot |
| Blanket | 25 mm ceramic fibre, 128 kg/m³, 0.09 W/m K at a mean of about 350 °C | Supplier data typical; air ports, lid and throat bare |
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

The times include 0.5 h of warm-up and a 30 min hold at 450 °C for R3. R3 is **at risk**: it is reachable if the annulus is held hot long enough, which is what drives the wood demand in section 5. R5 is **not met** on the central estimate. Sealed cooling (section 8) is short enough for the 16 h unload limit.

## 4. Shell loss, surfaces and masses (R11, R12)

*Table 3. Heat loss during the burn (annulus gas 650 °C).*

| Surface | Area | Surface temperature | Loss |
| --- | --- | --- | --- |
| Blanketed side | 1.33 m² | 125 °C | 2.20 kW |
| Port band, bare | 0.25 m² | 168 °C | 0.69 kW |
| Lid and top band, bare | 0.32 m² | 257 °C | 1.90 kW |
| Burner throat, bare | 0.20 m² | 223 °C | 0.91 kW |
| **Total** | | | **5.69 kW** |

Without the blanket the side would run at about 311 °C and lose 11.3 kW, so the blanket (decided, item 7) roughly halves the loss. A blanket on the lid and top band (not in the design) would cut that part from 1.90 to 0.50 kW; see CCB-DDR-001 item 13.

*Table 4. Masses.*

| Part | Mass |
| --- | --- |
| Outer drum with hoops and ring | 18.8 kg |
| Outer lid with collar | 3.4 kg |
| Retort with lid | 12.3 kg |
| Burner throat; air shroud | 3.2 kg; 1.9 kg |
| Firebricks (3); blanket | 2.6 kg; 4.3 kg |
| Water jacket, empty | 21.3 kg |
| Flue with cap; tripod; tap | 6.5 kg; 14.8 kg; 0.6 kg |
| **Kiln without plinth and water** | **91 kg** |
| Heat-recovery lift unit (tripod, drained jacket, flue, tap) | 43.3 kg: 21.6 kg each for two people |
| Retort with char | 15.2 kg: one person |
| Jacket full (61.4 L at 540 mm depth) | 83 kg, never moved full |

R11 is **met**: no lift exceeds 25 kg per person, but only if the jacket is drained and two people lift the unit. The only welded part is the jacket; the collar, shroud and tripod are riveted or bolted. Each tripod leg (40 x 40 x 4 mm angle, 1.52 m, slenderness 195) carries about 320 N with a full jacket against an Euler load of 16.9 kN, a factor of about 53.

R12 is **met**: the flue outlet is 2.70 m above the ground and no BOM line calls for galvanized parts. The 5 m clearance is an operating rule (CCB-PRC-001, Safety).

## 5. Energy balance and start-up wood (R8)

Wood makes up whatever the burning volatiles cannot supply while the annulus is held at 650 °C for the whole burn. The sinks are the retort charge and steel (19 MJ), the stored heat in the drum, lid, throat, bricks and blanket (8 MJ), the shell loss over the burn, and the heat carried out by the annulus gas.

*Table 5. Energy per batch.*

| Quantity | Favourable | Central | Unfavourable |
| --- | --- | --- | --- |
| Burn time | 3.4 h | 4.5 h | 7.0 h |
| Volatiles, lower heating value | 104 MJ | 117 MJ | 132 MJ |
| Energy left in the char | 73 MJ | 60 MJ | 45 MJ |
| Shell loss over the burn | 70 MJ | 91 MJ | 144 MJ |
| **Wood needed (R8)** | 2.9 kg | **5.8 kg** | 13.9 kg |
| Heat released in the kiln | 143 MJ | 190 MJ | 303 MJ |
| Flue gas per batch | 89 kg | 152 kg | 301 kg |
| Gas leaving the throat (jacket inlet) | 465 °C | 430 °C | 400 °C |

Light-up alone needs about 1.7 kg of wood. The rest keeps the annulus hot while conduction does its work. R8 is **not met** on the central estimate. Excess air matters as much as burn time: every kilogram of surplus air leaves at 650 °C. Figure 2 in CCB-PRC-001 shows the central energy flow: 286 MJ in (residue at its higher heating value, wood at its lower), 60 MJ kept in the char, 36 MJ as latent heat and unburned gas, 190 MJ released, 118 MJ to the charge, structure and shell, and 71 MJ in the flue gas at the jacket.

## 6. Gas flow, draft and air (R4)

*Table 6. Flow checks at the central case; peak flow is taken as twice the mean.*

| Check | Result |
| --- | --- |
| Volatiles leaving the retort, mean and peak | 0.73 and 1.46 g/s |
| Eight 20 mm gas holes (25.1 cm²) at peak | 1.3 m/s, 1.0 Pa: little back-pressure in the retort |
| Flue gas, mean and peak | 9.5 and 18.9 g/s |
| Draft, air ports to outlet (2.43 m) | 16.9 Pa |
| Losses at peak: flue path and primary ports | 3.9 and 0.24 Pa; margin 3.2 |
| Throat velocity at peak; flue velocity above the jacket | 2.0 m/s; 0.94 m/s |
| Secondary air at peak (40 % of air) | 4.88 g/s |
| Suction at the throat air holes at peak | 7.6 Pa |
| Secondary hole area needed and provided | 23.6 and 27.1 cm² (24 x 12 mm in two rings, 42 mm pitch) |
| TRL 2 25 mm inlet pipe at the same flow | 7.2 m/s and about 46 Pa: **would not work** |
| Air shroud intake (230 mm sleeve, 204 cm²) | 0.20 m/s |

The draft is enough, with a margin of about 3 at peak, and the throat holes pass the peak secondary air with about 15 % spare area. The TRL 2 pipe ring could not have admitted the air, so the model uses a shroud around the throat; this is open item 11 in CCB-DDR-001. R4 is **not verifiable at TRL 3**: the gas route is closed by design and the air paths are sized, but smoke and methane depend on mixing and temperature and need measurement.

## 7. Water jacket (R6, R7)

The 600 mm flue sleeve (164 mm bore, 0.31 m² wetted) sees gas at 400 to 465 °C and a Reynolds number of about 1,600 to 2,600, which is laminar or transitional. Convection gives only about 1 to 3 W/m²K and gas radiation about 2 to 2.5 W/m²K, so the sleeve takes only 11 to 13 % of the gas heat.

*Table 7. Heat into the water per batch (61.4 L, starting at 20 °C).*

| Case | Heat to water | Water temperature rise |
| --- | --- | --- |
| Favourable (short burn) | 4.9 MJ | |
| **Central** | **6.4 MJ** | about 25 K |
| Unfavourable (long burn) | 9.2 MJ | |
| Central with 25 mm blanket on the jacket shell | 7.6 MJ | |
| Central with a spiral baffle insert (convection x 3) | 11.4 MJ | |
| Central with both | 13.9 MJ | |

R6 is **not met**: the TRL 2 estimate of about 15 MJ assumed 15 W/m²K, about three times what a plain sleeve gives. The options are open item 12 in CCB-DDR-001. The water does not boil in any scenario (boiling needs 20.6 MJ), but a baffle insert on a long burn could approach it, so R7 (open vent, loose lid, no sealing valve) stays essential. R7 is **met** by design.

The sleeve wall runs close to the water temperature, far below the tar dew point, so any tar that escapes the throat will deposit there and cut heat transfer further. While the water is below about 41 °C, water vapor from the flue gas condenses on the sleeve and will drip back into the throat.

## 8. Cooling and unloading (R5)

With the ports and damper closed, the kiln and char (29 kJ/K) lose heat through a shell conductance of about 12.8 W/K, a time constant of about 0.6 h, so the shell falls to 60 °C in about 1.6 h. The char core then needs about 1.6 h more by conduction. The sum, about **3.2 h**, puts unloading at about 8 h after lighting in the central case, inside the 16 h limit. The char should still be left sealed overnight, because air reaching hot char can reignite it (CCB-PRC-001, Safety).

## 9. Carbon

*Table 8. Carbon per batch (100-year basis).*

| Scenario | Carbon stored | CO₂ | Methane penalty | Net |
| --- | --- | --- | --- | --- |
| Favourable | 1.63 kg C | 6.0 kg | 2.5 kg CO₂e | 3.5 kg CO₂e |
| Central | 1.30 kg C | 4.8 kg | 2.0 kg CO₂e | **2.8 kg CO₂e** |
| Unfavourable | 0.93 kg C | 3.4 kg | 1.4 kg CO₂e | 2.0 kg CO₂e |

At 250 batches a year the central case makes about 740 kg of char and a net removal of about **0.70 t CO₂e**, and keeps about 3.0 t of residue out of open burning. The methane penalty assumes the retort field average; a working burner throat would lower it, but that cannot be shown without measurement. Start-up wood is assumed to come from residues or prunings and is not counted as an emission.

## 10. Logger (R9)

A type K class 2 probe is good to ±5.2 °C at 700 °C; with the MAX31855 amplifier (±2 °C from −200 to 700 °C, [datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/max31855.pdf)) the combined error is about ±5.6 °C, just outside the ±5 °C target. Class 1 (special limits) probes give about ±3.4 °C to 700 °C, so the BOM now calls for class 1. Above 700 °C the amplifier accuracy is not specified, so R9 is **at risk** over the full 0 to 1,000 °C range (open item 15). A 0.25 W logger uses about 6 Wh in 24 h against about 31 Wh usable from a 10,000 mAh power bank, and writes about 276 kB a day.

## 11. Cost (R10)

The 14 BOM lines total **$298** against the $300 budget, a margin of $2. The safety kit (about $40) is required and listed separately in `bom/bom-notes.md`, outside the kiln budget (CCB-DDR-001 item 2). R10 is **met**, with almost no room for the jacket improvements in open item 12 (about $15) or a lid blanket (about $6).

## 12. Results against requirements

*Table 9. Every requirement in CCB-REQ-001 v0.3. Also written to `docs/04-calcs/results.csv`.*

| ID | Requirement (short) | Value (central, range) | Target | Status |
| --- | --- | --- | --- | --- |
| R5 | Light to end of flaming; unload | Burn 4.5 h (3.4 to 7.0 h); unload after about 8 h | 4 h or less; 16 h or less | **Not met** |
| R6 | Heat into water per batch | 6.4 MJ (4.9 to 9.2 MJ) | 10 MJ or more | **Not met** |
| R8 | Start-up wood per batch | 5.8 kg (2.9 to 13.9 kg); light-up alone 1.7 kg | 5 kg or less | **Not met** |
| R2 | Char yield | 28 % (20 to 35 %); 2.96 kg | 25 % or more | At risk |
| R3 | Core 450 °C for 30 min | Core at 450 °C 4.0 h after lighting (2.9 to 6.5 h) if the annulus is held at 650 °C | 450 °C, 30 min | At risk |
| R9 | Logger accuracy and endurance | ±3.4 °C to 700 °C with class 1 probes; unspecified above 700 °C; 6 of 31 Wh | ±5 °C, 0 to 1,000 °C | At risk |
| R4 | Burn the gas; smoke; methane | Route closed by design; draft margin 3.2; air holes sized | Methane below 24 g/kg | Not verifiable at TRL 3 |
| R1 | Batch size, decided feedstock | 12.0 kg packed (loose straw 4.0 kg, excluded) | 10 kg or more | Met |
| R7 | Open water circuit | Open vent, loose lid, tap at base, tripod-carried | By design | Met |
| R10 | Kiln parts cost | $298 | $300 or less | Met |
| R11 | Crew and lifts | 21.6 kg each for two; retort with char 15.2 kg | 25 kg per person or less | Met |
| R12 | Outlet height; no galvanized hot parts | 2.70 m; none | 2.5 m or more | Met |

## 13. Limits of this note

- The heating-time model treats the charge as a solid with a fixed effective conductivity. Real beds shrink, crack and release gas, which can speed or slow heating; the three scenarios bracket this but do not replace logged batches.
- Surface coefficients assume still air. Wind raises the shell loss and the wood demand.
- The methane figure is a literature average, not a prediction for this design.
- Nothing here has been measured. Checking these numbers against logged batches is TRL 4 work, which is on hold by Amish's instruction.

> **Safety:** These are paper estimates for a fire that produces flammable, toxic gas and hot water. The surface temperatures in Table 3 (125 to 257 °C on the shell, higher on the flue) burn skin on contact. The water jacket must stay open-vented whatever changes are made to raise its heat transfer. See CCB-PRC-001, Safety.
