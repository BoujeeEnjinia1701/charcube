---
doc_id: CCB-BLD-001
title: CharCube prototype build plan
project: CharCube
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (CCB-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Amish's 2026-10-02 decisions built in (fibre board and block thermocouple, flared sleeve foot, conical rain cap, hot-surface labels, lifting aid); pictures regenerated
---

# CharCube prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order.*

The prototype is one CharCube kiln, about 2.84 m tall to its rain cap, with a lifting aid beside it: a 114 L steel drum (the retort) packed with residue, standing on bricks inside a 200 L drum on a block plinth shielded by a fibre board, with a burner throat and air shroud on the outer drum's lid, and a water jacket carried above it on a three-legged stand with the flue rising through it. A post with a swinging arm and a hand winch stands 1.2 m behind the kiln to lift the heat-recovery unit on and off. Figure 1 shows the 26 components in the order you make or fit them. Most are made in a small workshop from two used drums, plain steel pipe, sheet, strip and angle, by cutting, drilling, rolling sheet by hand, folding and riveting; the legs and feet are bolted. The water jacket is the one welded part and goes to a welder. The lifting aid is bolted together from steel tube and angle. The blocks, fibre board, bricks, blankets, tap, probes, logger, labels and winch are bought. The parts cost about $546 from the bill of materials, of which the lifting aid is about $160.

> **Safety:** CharCube is a fire that makes flammable, toxic gas and hot water. Build it so that it is only ever lit outdoors, at least 5 m from buildings, fences and dry vegetation, with a fire extinguisher or 50 L of water and a shovel at hand. Use only drums that held non-flammable, non-toxic products, and never cut, drill or grind a drum that held fuel, solvent or pesticide. Never use galvanized pipe or sheet anywhere in the hot path. Wear eye protection, gloves and hearing protection when cutting and grinding, and a dust mask when cutting ceramic fibre or mineral wool. The water jacket must stay open to the air: never fit a sealed lid, valve or plug.

## 2. What changed to make it buildable

The concept showed what the kiln does; some of its parts could not be made, fixed or used as drawn. Each change below keeps what the kiln does, and all of them are recorded in decision record CCB-DDR-003, which Amish accepted on 2026-10-02 together with the fibre board, the flared sleeve foot, the conical rain cap, the labels and the lifting aid.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Plinth | Four blocks that overlapped each other by 50 mm | Four blocks laid as a pinwheel, 580 mm square with a 200 mm hole (Figure 3) | The drum's rim stands on block all round |
| Lid and throat | A 160 mm lid hole the same size as the throat, so the throat had nothing to stand on | A 150 mm hole; the throat stands on the lid inside a riveted collar and is riveted to it (Figure 12) | Lid, throat and shroud lift off as one unit |
| Air shroud | No fixing; a band damper that floated and could not close the intake | Six tabs riveted to the throat; a 60 mm band with a wing screw (Figure 12) | Riveted and folded, no welding |
| Port dampers | Listed but not drawn | A curved plate sliding in two riveted guide strips per port (Figure 6) | A damper must be held top and bottom |
| Firebricks | Standing under the gas holes | Long side round the retort, 200 mm out, 8 mm clear of the holes (Figure 8) | The gas holes vent freely |
| Retort | Nothing to lift it by in a 43 mm gap | Two U-bolt handles on its lid | Hands do not fit beside it |
| Jacket stand | A ring seat 7 mm below the jacket and outside its edge; round stand-in legs | Three fins welded to the jacket; angle legs bolted flat to them; bolted foot cleats and pads (Figures 18, 20) | Every joint is face to face and bolted |
| Flue and rain cap | No seat for the flue; cap posts inside the bore; cap 10 mm above the outlet | A 650 mm flue resting on three clips; a conical cap on three riveted legs, at least 60 mm from the flue's top edge (Figures 22, 24) | The flue sits on the jacket; the outlet is at 2.72 m |
| Baffle | A cross bar cut into the flue wall | A rod through two holes in the flue foot; the strip hangs on it (Figure 22) | It lifts out with the flue |
| Jacket lid | Floating above the rim; a vent standing on nothing | Rests on the rim on three tabs; vent nipple through it (Figure 16) | Open to the air, located, removable |
| Logger | Box drawn through a leg | Strapped beside the leg | A box cannot share space with a leg |
| Probes | A short core probe through two lids from under the shroud | A 500 mm probe through the drum side into a slot in the retort; the throat probe below the sleeve (Figure 26) | Both can be pushed in and pulled out from outside |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Front" is the side the operator works from; "back", "left" and "right" are as seen standing in front of the kiln, and the tap is on the right. Workshop tolerance is 1 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Plinth blocks, fibre board, block thermocouple and ash pan

![Figure 2. Making sketch of the ash pan and fibre board](../cad/drawings/CCB-DWG-101.png)

*Figure 2. Plinth making sketch: ash pan, fibre board and block thermocouple (CCB-DWG-101).*

**What it is and what it is made from.** Four bought concrete blocks, 390 x 190 x 190; a 25 mm ceramic fibre board, 600 x 600, that keeps the heat of the fire off the blocks, since concrete can crack or spall when heated; a thermocouple with its tip on a block, to show how hot the blocks get; and a steel plate, 760 x 600 x 3, that lifts the drum's air ports clear of the ground and catches embers.

**How to make it.**

1. Cut the pan from 3 mm mild steel plate, 760 x 600. Grind the edges and round the corners to about 10.
2. Scribe a 572 circle in the middle and a centre line each way; the drum stands on the circle.
3. Cut the board, 600 x 600, from a sheet of 25 mm ceramic fibre board (1260 °C grade) with a fine saw, wearing a dust mask. On its underside cut a groove 4 wide and 4 deep, starting 150 behind the centre and 50 to the left of it and running straight out to the back edge.
4. The block thermocouple is bought: a bare-wire type K with glass-fibre insulation and a 1 m lead (section 3.20).

**How it fits the parts next to it.**

![Figure 3. Joint 1: drum, ash pan and block plinth](05-build-plan/joint-01.png)

*Figure 3. The four blocks make a 580 mm square round a 200 mm hole; the fibre board lies on them, the pan on the board, and the drum's rim stands over the blocks.*

Each block's end butts against the side of the next, turning the same way round the square. The thermocouple's tip lies on the back block, 150 behind the centre, and its lead runs out at the back along the groove, so the board does not pinch it. The board lies centred on the blocks and the pan lies flat on the board; the pan is 80 wider than the board at each side so embers from the ports land on steel.

**Check before moving on.** The pan lies level (a spirit level both ways) and does not rock; the thermocouple reads room temperature at the logger.

### 3.2 Outer drum

![Figure 4. Cutting sketch of the outer drum](../cad/drawings/CCB-DWG-102.png)

*Figure 4. Outer drum cutting sketch (CCB-DWG-102).*

**What it is and what it is made from.** A used 200 L open-head steel drum, 572 across and 851 tall, 1.2 thick, with its lid and locking ring: the firebox shell.

**How to make it.**

1. Check what the drum held. Burn off paint and liners outdoors, upwind, before any cutting (safety stop S1).
2. Mark four air ports, 40 wide and 110 tall, their bottom edges 20 above the floor, on the four diagonals (front left, front right, back left, back right).
3. Drill a 6 hole in each corner of each port and cut between the holes with an angle grinder and a thin disc. File the edges smooth.
4. Drill one 10 hole at the back, 361 above the floor, for the core probe.
5. Drill the damper guide rivet holes once the guides are made (section 3.3).
6. Deburr every edge.

**How it fits the parts next to it.** It stands on the pan over the blocks (Figure 3); the lid and its locking ring close on its rim; the blanket wraps it from 140 above the floor to 30 below the rim.

**Check before moving on.** The lid and locking ring still close on the rim.

### 3.3 Port dampers and guides (make 4 sets)

![Figure 5. Making sketch of the port damper and guides](../cad/drawings/CCB-DWG-103.png)

*Figure 5. Port damper and guide strips making sketch (CCB-DWG-103).*

**What it is and what it is made from.** At each port, a curved plate that slides sideways to open or close the port, held by two strips. Damper: 1.2 mm mild steel sheet. Guides: 1.5 mm steel strip, 10 wide.

**How to make it.**

1. Cut four dampers, 60 x 122. Roll each by hand over a pipe until it lies against the drum.
2. Cut eight guide strips about 135 long. Joggle 10 at each end by 1.2 so the ends sit on the drum and the middle stands off it by the damper's thickness.
3. Hold a damper over its port. Place one guide just below the port with its top edge 6 over the damper's lower edge, and one just above the port overlapping the damper's top edge by 6. The guides run from 10 short of the closed damper on one side to 10 past the open damper on the other.
4. Drill 4.9 through each joggled end and the drum and fit 4.8 steel rivets.

**How it fits the parts next to it.**

![Figure 6. Joint 2: sliding port damper in its guides](05-build-plan/joint-02.png)

*Figure 6. The damper slides 55 mm sideways under the two guides; closed, it covers the port with 6 mm to spare all round.*

**Check before moving on.** Each damper slides by hand from fully open to fully closed and stays where it is put.

### 3.4 Drum blanket

**What it is and what it is made from.** Bought 25 mm ceramic fibre blanket, 128 kg/m³, held by plain steel wire mesh: it halves the heat lost through the drum's side.

**How to make it.** Wearing a dust mask, cut a strip 681 wide and about 1.96 m long (once round the blanketed drum plus a 10 overlap). Cut a 20 slit where it crosses the probe hole.

**How it fits the parts next to it.** It wraps the drum from 140 above the floor (just above the port guides) to 30 below the rim; the lid blanket's skirt covers the top 30. Wire mesh over it, twisted tight, holds it.

**Check before moving on.** No blanket over any port or damper; the probe hole is clear.

### 3.5 Firebricks

**What it is and what it is made from.** Three bought half firebricks, about 114 x 64 x 60, that hold the retort 60 above the drum floor so fire can burn under it.

**How to make it.** Nothing to make. Lay them on the drum floor with their long side running round the drum, their centres 200 from the middle: one at the back and two toward the front, 120 degrees apart.

**How it fits the parts next to it.**

![Figure 7. Making sketch of the retort](../cad/drawings/CCB-DWG-104.png)

*Figure 7. Retort cutting sketch (CCB-DWG-104), shown here because the bricks are placed to suit its gas holes.*

![Figure 8. Joint 3: the retort on its bricks, seen from below](05-build-plan/joint-03.png)

*Figure 8. The bricks carry the retort's edge and stay 8 mm clear of every gas hole.*

**Check before moving on.** With the retort in place, every gas hole can be seen from below, clear of the bricks.

### 3.6 Retort

**What it is and what it is made from.** A used 114 L open-head steel drum with its bolt-ring lid, 463 across and 737 tall, 1.0 thick (Figure 7). It holds the residue; it wears out in about 50 to 100 batches.

**How to make it.**

1. Same checks on past contents and paint as the outer drum (safety stop S1).
2. Mark eight gas holes in the base on a 300 circle, 45 degrees apart, one of them on the line of the probe slot. Step drill to 20.
3. Mark the probe slot, 10 wide and 40 tall, in the side, centred 300 above the base (the middle of the 600 fill). Drill and file it.
4. Drill four 9 holes in the lid, 130 each side of centre and 40 each side of the centre line, and fit two M8 U-bolts with large washers and nuts under the lid.
5. Mark the slot's position on the lid rim with a punch line, so it can be lined up with the drum's probe hole when the lid is on.

**How it fits the parts next to it.** It stands on the three bricks (Figure 8), 43 clear of the outer drum all round, with the U-bolts 17 below the outer lid.

**Check before moving on.** The lid seals on its gasket when the ring is bolted; the U-bolts carry the drum's weight without the lid bending.

### 3.7 Outer lid and throat collar

![Figure 9. Making sketch of the outer lid and collar](../cad/drawings/CCB-DWG-105.png)

*Figure 9. Outer lid and throat collar making sketch (CCB-DWG-105).*

**What it is and what it is made from.** The outer drum's own lid with a 150 hole, and a short collar of 1.5 mm sheet that holds the burner throat upright on it.

**How to make it.**

1. Cut a 150 hole in the middle of the lid with a jigsaw and a metal blade, and file it to a scribed circle.
2. Cut a strip of 1.5 sheet 40 wide and about 520 long, with six tabs 15 wide and 20 long along one edge.
3. Roll the strip round a piece of the 160 throat pipe so it fits the pipe snugly, and rivet the overlap.
4. Fold the tabs out flat, stand the collar on the lid centred on the hole, drill through each tab and the lid at 4.9, and rivet.
5. Glue ceramic gasket rope into the lid's rim channel with high-temperature sealant.

**How it fits the parts next to it.** The throat stands on the 5 ring of lid inside the collar and is riveted to it (Figure 12). The lid closes on the drum with its locking ring.

**Check before moving on.** A 160 pipe slides into the collar by hand, with no gap wider than 1, and sits flat on the lid.

### 3.8 Burner throat

![Figure 10. Making sketch of the burner throat](../cad/drawings/CCB-DWG-106.png)

*Figure 10. Burner throat making sketch (CCB-DWG-106).*

**What it is and what it is made from.** A 400 length of 160 x 2 plain steel pipe, where the gas finishes burning with air from the shroud.

**How to make it.**

1. Cut 400 of pipe and square the ends.
2. Wrap a paper template round the pipe and mark two rings of fifteen 12 holes, 24 degrees apart, 95 and 135 above the bottom end, the upper ring turned 12 degrees from the lower. Drill and deburr inside.
3. Drill one 8 hole at the back, 330 above the bottom end, for the throat probe.
4. Stand it in the collar and drill four 4.9 holes through the collar and pipe, 20 above the lid; rivet.

**How it fits the parts next to it.** Collar and lid below (Figure 12); the shroud is riveted to it 200 above its bottom end; the jacket sleeve slips over its top 50 (Figure 14).

**Check before moving on.** It stands square to the lid; every air hole is clear.

### 3.9 Air shroud and band damper

![Figure 11. Making sketch of the air shroud and band damper](../cad/drawings/CCB-DWG-107.png)

*Figure 11. Air shroud and band damper making sketch (CCB-DWG-107).*

**What it is and what it is made from.** A sleeve of 1.5 mm sheet round the base of the throat, open at the bottom, closed at the top, that feeds air to the throat's holes; and a band that slides down to close its intake.

**How to make it.**

1. Roll a strip 150 wide to 230 outside diameter and rivet the overlap.
2. Cut a 230 disc. Cut a 160 hole in it, first cutting six tabs 15 wide into the hole's edge, and fold the tabs up 20.
3. Fold or rivet the disc onto the top of the sleeve.
4. Band: roll 3 mm strip, 60 wide, to slide round the sleeve; rivet a nut into it and fit an M6 wing screw.

**How it fits the parts next to it.**

![Figure 12. Joint 4: throat, collar, lid and air shroud](05-build-plan/joint-04.png)

*Figure 12. The throat stands on the lid inside the collar; the shroud's tabs are riveted to the throat with its bottom edge 40 mm above the lid; air enters there and passes through the two rings of holes.*

Slide the shroud over the throat onto a 40 spacer block on the lid, drill through the six tabs and the throat at 4.9 and rivet. The band rides on the shroud: up and screwed tight for the burn, slid down to the lid to close the intake at the end.

**Check before moving on.** The gap under the shroud is 40 all round; the band slides and the wing screw holds it.

### 3.10 Lid blanket

**What it is and what it is made from.** Bought 25 mm ceramic fibre blanket: a disc on the lid and a skirt over the drum's top band and locking ring.

**How to make it.** Cut a ring 622 outside and 280 inside diameter, and a skirt 32 wide and about 1.96 m long. The 280 hole keeps the blanket 25 clear of the shroud so the intake is never blocked.

**How it fits the parts next to it.** It lies on the lid round the shroud (Figure 12); the skirt hangs over the rim and locking ring down to the side blanket. Tie wire holds both. It lifts off with the lid.

**Check before moving on.** The blanket is at least 25 from the shroud and band all round.

### 3.11 Water jacket

![Figure 13. Fabrication sketch of the water jacket](../cad/drawings/CCB-DWG-108.png)

*Figure 13. Water jacket fabrication sketch (CCB-DWG-108).*

**What it is and what it is made from.** An annular tank round a flue sleeve that heats about 61 L of water, made by a welder from 2 mm mild steel sheet, a 700 length of 168 x 2 pipe and 6 mm plate. It is the one welded part.

**How to make it (for the welder).**

1. Shell: 2 mm sheet rolled to 420 outside diameter, 600 tall. Bottom: a 2 mm ring, 420 outside with a 168 hole.
2. Weld the bottom to the shell and the sleeve through the bottom, water-tight, with the sleeve standing 50 out of the top and 50 out of the bottom. The top is open; nothing is welded over it. Weld the sleeve all round: when the unit is lifted, the sleeve carries all of it.
3. Flare the bottom 20 of the sleeve out to about 190 across, a short cone, so the sleeve guides itself onto the throat as the unit is lowered.
4. Drill two 18 holes straight across the top socket, 35 above the shell's top edge, for the lift bar (section 3.22). Turn them a quarter turn from where the flue's rod holes will sit.
5. Fins: three 6 mm plates, 85 wide and 140 tall, welded on edge to the shell, one at the front and one each at the back left and back right, 120 degrees apart. Each fin runs from 60 up the shell to 80 below the jacket's underside. Drill two 11 holes in each: 245 from the jacket's axis and 15 above its underside, and 267 from the axis and 52 below the underside.
6. Weld a 1/2 in socket into the shell on the right side, 40 above the bottom, for the tap.
7. Fill with water and leave overnight; fix any leak. Then paint the outside with high-temperature paint.

**How it fits the parts next to it.**

![Figure 14. Joint 5: the jacket sleeve over the throat](05-build-plan/joint-05.png)

*Figure 14. The lower 50 mm of the sleeve slips over the top of the throat with 2 mm clear all round; its flared foot guides it on; the baffle hangs 10 mm above the throat.*

The legs bolt to the fins (Figure 18); the flue rests on the sleeve's upper rim (Figure 22).

**Check before moving on.** It holds water overnight with no drip; the sleeve slides over a short piece of 160 pipe.

### 3.12 Tap

**What it is and what it is made from.** A bought 1/2 in brass ball valve with a short steel nipple.

**How to make it.** Nothing to make. Wrap the nipple's threads with PTFE tape.

**How it fits the parts next to it.** It screws into the jacket's socket on the right side, lever up. It must never be the only way the jacket breathes: the top stays open.

**Check before moving on.** No drip at the socket with the jacket full.

### 3.13 Jacket loose lid and vent

![Figure 15. Making sketch of the jacket loose lid](../cad/drawings/CCB-DWG-109.png)

*Figure 15. Jacket loose lid making sketch (CCB-DWG-109).*

**What it is and what it is made from.** A 420 disc of 1.5 mm sheet with a 210 centre hole that keeps rain and leaves out of the jacket; a 3/4 in steel nipple, 80 long, as a vent.

**How to make it.**

1. Cut the disc and the centre hole.
2. Rivet three tabs, 20 x 15, under the lid, 120 degrees apart, folded down so they sit 2 inside the shell.
3. Cut a 27 hole 170 from the centre and fit the nipple with a locknut each side.

**How it fits the parts next to it.** The centre hole clears the flue's stop clips (section 3.17).

![Figure 16. Joint 11: jacket loose lid and vent](05-build-plan/joint-11.png)

*Figure 16. The lid rests on the shell rim, located by its tabs; it is never fixed, sealed or weighted.*

**Check before moving on.** The lid lifts off by hand, and the vent and centre hole are clear.

### 3.14 Jacket blanket

**What it is and what it is made from.** Bought 25 mm mineral wool (rock wool) blanket that keeps the heat in the water; the jacket's outside stays below 100 °C, so mineral wool is enough.

**How to make it.** Wearing a dust mask, cut a strip 540 wide and about 1.42 m long. Cut it round the tap.

**How it fits the parts next to it.** It wraps the jacket from 60 above its bottom (above the fins and the tap) to the rim, held by tie wire.

**Check before moving on.** The tap, vent and lid are clear of the blanket.

### 3.15 Tripod legs (make 3)

![Figure 17. Making sketch of the tripod leg](../cad/drawings/CCB-DWG-110.png)

*Figure 17. Tripod leg making sketch (CCB-DWG-110), drawn upright.*

**What it is and what it is made from.** The three legs that carry the jacket, water and flue over the kiln so the drum's lid carries no water load. Steel equal angle, 40 x 40 x 4.

**How to make it.**

1. Cut three lengths, 1579 on the longest edge. Cut the lower end 18 degrees off square, so it stands level when the leg leans 18 degrees in; cut the upper end square.
2. On one face of the angle (the flat face), on a line 18 from its free edge, drill three 11 holes, measured along the leg from the middle of the lower end: 19 (the foot pin), 1477 and 1547 (the fin bolts).
3. Drill the three legs clamped together so the holes match.

**How it fits the parts next to it.**

![Figure 18. Joint 6: leg bolted to its jacket fin](05-build-plan/joint-06.png)

*Figure 18. The leg's flat face lies on the fin; two M10 bolts make the joint rigid.*

The flat face lies against the side of a fin, the other face pointing away from the jacket, with two M10 bolts and nyloc nuts. The leg stays 21 clear of the jacket blanket and 40 clear of the drum blanket.

The legs and their feet are what the heat-recovery unit stands on when the lifting aid sets it down (section 3.22); the unit is never carried by its legs.

**Check before moving on.** Hole centres within 1 of the figures.

### 3.16 Foot cleats and pads (make 3 sets)

![Figure 19. Making sketch of the foot cleat and pad](../cad/drawings/CCB-DWG-111.png)

*Figure 19. Foot cleat and pad making sketch (CCB-DWG-111).*

**What it is and what it is made from.** A short cleat of the leg angle on a steel foot pad, so each leg stands on a broad, flat foot. Angle 40 x 40 x 4, plate 6.

**How to make it.**

1. Cut three cleats 60 long. In the upright face, drill one 11 hole at mid-length, 24 up from the underside of the flat face. In the flat face, drill two 9 holes, 18 each side of the middle and 22 in from the heel.
2. Cut three pads 100 x 100 from 6 plate; drill two 9 holes to match the cleat and countersink them from below.
3. Screw each cleat to its pad with two M8 countersunk screws from below and nyloc nuts on top.

**How it fits the parts next to it.**

![Figure 20. Joint 7: leg foot on its cleat and pad](05-build-plan/joint-07.png)

*Figure 20. One M10 bolt pins the leg to the cleat, so the leg can settle as the unit is set down.*

The leg's flat face lies on the cleat's upright face, outside it; one M10 bolt with a nyloc nut, snug. The foot centres sit on a 1.44 m circle. The pin lets each leg settle as the lifting aid lowers the unit onto its feet, beside the kiln or over it.

**Check before moving on.** Each pad sits flat with the screw heads flush.

### 3.17 Flue and stop clips

![Figure 21. Making sketch of the flue pipe](../cad/drawings/CCB-DWG-112.png)

*Figure 21. Flue pipe and stop clips making sketch (CCB-DWG-112).*

**What it is and what it is made from.** A 650 length of 160 x 2 plain steel pipe that carries the gas from the jacket to the outlet, 2.72 m above the ground. Three clips of 20 x 20 x 3 angle seat it on the jacket.

**How to make it.**

1. Cut 650 of pipe and square the ends. The lower end is the foot.
2. Drill two 11 holes opposite each other, 15 above the foot, for the baffle rod.
3. Cut three clips 20 long. Rivet each by its upright leg to the pipe with two 4.8 rivets, 120 degrees apart, with the underside of its flat leg 50 above the foot.

**How it fits the parts next to it.**

![Figure 22. Joint 8: flue foot in the sleeve socket](05-build-plan/joint-08.png)

*Figure 22. The flue's foot sits 50 mm down the sleeve with 2 mm clear; its three clips rest on the sleeve rim; the rod through the foot carries the baffle.*

**Check before moving on.** The pipe drops into the sleeve to its clips without forcing.

### 3.18 Rain cap and legs

![Figure 23. Making sketch of the conical rain cap and legs](../cad/drawings/CCB-DWG-113.png)

*Figure 23. Conical rain cap and legs making sketch (CCB-DWG-113).*

**What it is and what it is made from.** A cone of 1.5 mm sheet, 260 across with a 30 degree slope, on three legs of 20 x 3 flat bar, keeping rain out of the flue.

**How to make it.**

1. Cut a 300 disc from 1.5 sheet. Cut out a 48 degree wedge to the centre, roll the rest into a cone 260 across and rivet the overlap with three 4.8 rivets.
2. Cut three legs 142 long and bend each 90 degrees 30 from one end to make a foot.
3. Rivet the legs to the outside of the flue top, 120 degrees apart, two 4.8 rivets each, with the bent feet 52 above the flue's top edge. Rivet the cone to the feet.

**How it fits the parts next to it.**

![Figure 24. Joint 9: rain cap on its three legs](05-build-plan/joint-09.png)

*Figure 24. The shortest gap from the flue's top edge to the cone is 60 mm all round: less than that chokes the draft.*

**Check before moving on.** The gap under the cap is the same all round.

### 3.19 Spiral baffle and hanger rod

![Figure 25. Making sketch of the spiral baffle and rod](../cad/drawings/CCB-DWG-114.png)

*Figure 25. Spiral baffle insert and hanger rod making sketch (CCB-DWG-114).*

**What it is and what it is made from.** A twisted strip of 150 x 1.5 plain steel that swirls the gas against the sleeve wall so more heat reaches the water, hung on a 10 mm steel rod.

**How to make it.**

1. Cut 615 of strip. Drill an 11 hole on its centre line, 10 from one end (the top).
2. Clamp the top end in a vice, clamp a bar across the bottom end and turn it with a long spanner: half a turn for every 300, just over one full turn in all. Keep the edges straight.
3. Cut 160 of 10 round bar and file the ends square.

**How it fits the parts next to it.** Hold the strip inside the flue foot, push the rod through one flue hole, the strip's hole and the other flue hole (Figure 22). The strip hangs down the sleeve 3 clear of its wall, its bottom 10 above the throat (Figure 14), and lifts out with the flue for cleaning.

**Check before moving on.** The twisted strip passes through a 160 ring along its whole length.

### 3.20 Logger and probes

**What it is and what it is made from.** Bought: a weatherproof box with a small microcontroller, three thermocouple amplifiers, a microSD card and a USB power bank; two type K class 1 probes with 6 stainless sheaths, 500 long (retort core) and 300 long (throat exit); and the block thermocouple, a bare-wire type K with glass-fibre insulation and a 1 m lead (section 3.1).

**How to make it.** Wire the three amplifiers to the microcontroller as their makers describe and lead the probe cables through cable glands in the box. The logging program is not part of this plan.

**How it fits the parts next to it.**

![Figure 26. Joint 10: core probe through the drum, blanket and retort slot](05-build-plan/joint-10.png)

*Figure 26. The core probe passes through the drum's 10 mm hole and the blanket slit, crosses the 43 mm gas gap and enters the retort through its slot to the middle of the charge.*

The core probe goes in at the back, 361 above the drum floor, until its tip reaches the retort's axis. The throat probe goes into the throat's 8 hole at the back, 70 below the jacket, until its tip reaches the throat's axis. The box is strapped with two stainless hose clips beside the back right leg, 520 above the ground, away from the heat; probe cables are rated for the temperature where they run.

**Check before moving on.** All three channels read room temperature, within 5 °C of a reference thermometer.

### 3.21 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Drums (lines 1 and 3).** A 200 L open-head steel drum with lid and locking ring, about 572 across, and a 114 L open-head drum with bolt-ring lid, about 463 across, both that held non-flammable, non-toxic products only. Check the gap between them is at least 40 all round.
- **Firebricks (line 4).** Three half firebricks, about 114 x 64 x 60.
- **Pipe (lines 6 and 7).** Plain (not galvanized) steel pipe, 160 outside diameter, 2 wall: 400 for the throat and 650 for the flue.
- **Tap (line 9).** 1/2 in brass ball valve and nipple.
- **Blankets (lines 11, 16 and 17).** 25 mm ceramic fibre blanket, 128 kg/m³, about 2.6 m² in all for the drum and lid; 25 mm mineral wool blanket, about 0.8 m², for the jacket; wire mesh and tie wire.
- **Plinth (line 12).** Four 390 x 190 x 190 concrete blocks and a 600 x 900 sheet of 25 mm ceramic fibre board, 1260 °C grade.
- **Logger (line 13).** As section 3.20.
- **Fixings and consumables (line 14).** 4.8 steel rivets (about 80); nine M10 x 30 bolts and six M8 x 20 countersunk screws, with nyloc nuts and washers; two M8 U-bolts, legs 80 apart; one M6 wing screw and rivet nut; ceramic gasket rope; high-temperature sealant; tie wire; two stainless hose clips; high-temperature paint.
- **Hot-surface labels (line 14).** Two ISO 7010 W017 hot-surface warning signs, 100 mm aluminium triangles with two holes. Wire one to the drum blanket's mesh and one to the jacket blanket, both at the front right where the operator stands (Figure 27). Check after each season that they are still there and readable.

![Figure 27. The two hot-surface labels on the drum blanket and the jacket blanket](05-build-plan/joint-14.png)

*Figure 27. The two hot-surface labels, at the front right of the drum blanket and of the jacket blanket.*

### 3.22 Lifting aid

![Figure 28. Making sketch of the lifting aid post, ground sleeve and footing](../cad/drawings/CCB-DWG-115.png)

*Figure 28. Lifting aid post, ground sleeve and footing making sketch (CCB-DWG-115).*

![Figure 29. Making sketch of the lifting aid arm and brace](../cad/drawings/CCB-DWG-116.png)

*Figure 29. Lifting aid arm, brace and pulleys making sketch (CCB-DWG-116).*

**What it is and what it is made from.** A post that turns in a sleeve set in the ground, with an arm on top and a hand winch, so that the drained heat-recovery unit (about 47 kg) is wound up, swung clear of the kiln and set down, and nobody carries it. Steel tube 88.9 x 3.2 and 101.6 x 3.6, angle 50 x 50 x 5 and 40 x 40 x 4, two 100 steel pulleys, a hand brake winch rated 270 kg, 5 mm steel wire rope, a hook with a safety latch, a 16 round bar and concrete. It is bolted; nothing on it is welded except the plate in the bottom of the ground sleeve, which can be a loose plate held by a bolt instead.

**How to make it.**

1. Footing: dig a hole 600 x 600 and 750 deep with its centre 1.2 m straight behind the kiln's centre. Stand the ground sleeve (730 of 101.6 tube with its bottom closed) in it, 30 proud of the ground and plumb, and fill the hole with concrete. Leave it at least three days before loading it.
2. Post: cut 4.69 m of 88.9 tube; close the top end with a 3 mm plate. Drill two 17 holes straight across it, 20 and 715 below its top end, as on Figure 28.
3. Arm: cut two lengths of 50 x 50 x 5 angle, 1500. Drill each as on Figure 29: a 17 hole for the post bolt, 200 from the back end, and 13 holes for the back pulley, the brace and the tip pulley.
4. Brace: cut two lengths of 40 x 40 x 4 angle, 990, and drill a hole near each end; cut two 5 mm packing plates for the brace's lower end.
5. Lift bar: cut 230 of 16 round bar.

**How it fits the parts next to it.**

![Figure 30. Joint 13: the arm on the post top](05-build-plan/joint-13.png)

*Figure 30. The two arm angles are bolted through the post with one M16 bolt; the brace runs down to a second M16 bolt; the rope runs from the winch over the back pulley and along the arm to the tip pulley.*

Two people stand the post in its sleeve (about 16 kg each). From a stepladder, bolt the two arm angles either side of the post top, then the brace angles with their packing plates, then the pulleys on their axles between the arm angles with spacer tubes. Bolt the winch to the post 1 m above the ground with two U-bolts on the side away from the arm, and reeve the rope from the winch over the back pulley, along the arm and over the tip pulley to the hook. With the arm turned toward the kiln, the hook hangs over the kiln's centre; parked, the arm points to the left, away from the flue.

![Figure 31. Joint 12: the lift bar through the jacket sleeve's top socket](05-build-plan/joint-12.png)

*Figure 31. With the flue lifted out, the lift bar goes through the two holes in the sleeve's top socket; the hook's shackle goes on its middle.*

**Check before moving on.** The post turns by hand through a quarter turn; the winch holds a load with the handle let go; with the unit hanging 100 off the ground, the post leans no more than about 50 at its top.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: lay the plinth

![Step 1](05-build-plan/step-01.png)

On firm, level, bare soil or paving at least 5 m from anything that can burn, 1.2 m in front of the lifting aid's post (section 3.22; pour its footing first so the concrete has set by step 15). Lay the four blocks as a pinwheel, lay the block thermocouple's tip on the back block, then the fibre board, groove down over the lead, and the pan on top, centred.

### Step 2: fit the port dampers and guides

![Step 2](05-build-plan/step-02.png)

With the drum on its side on a bench, rivet two guides per port through their joggled ends with each damper in place between them. Check every damper slides.

### Step 3: stand the drum on the ash pan

![Step 3](05-build-plan/step-03.png)

Centred on the marked circle, with a port toward each corner of the pan.

### Step 4: wrap the drum blanket

![Step 4](05-build-plan/step-04.png)

From 140 above the floor to 30 below the rim; wire mesh over it, twisted tight. Slit at the probe hole.

### Step 5: set the bricks in the drum

![Step 5](05-build-plan/step-05.png)

Long side round the drum, centred 200 out: one at the back, two toward the front.

### Step 6: lower the retort onto the bricks

![Step 6](05-build-plan/step-06.png)

Pack the retort with residue to 600 and bolt its lid on. Two people lower it by the U-bolt handles, turned so the punch mark on its rim faces the drum's probe hole at the back. **Hold point:** the gas gap is even all round (at least 40) and the slot lines up with the probe hole.

### Step 7: collar and throat onto the lid

![Step 7](05-build-plan/step-07.png)

Rivet the collar's tabs to the lid; stand the throat in the collar on the lid; rivet the throat to the collar.

### Step 8: air shroud and band onto the throat

![Step 8](05-build-plan/step-08.png)

Shroud on a 40 spacer, tabs riveted to the throat; band on the shroud, wing screw tight.

### Step 9: lid blanket onto the lid

![Step 9](05-build-plan/step-09.png)

Ring round the shroud, 25 clear of it; skirt over the rim; tie wire.

### Step 10: lid unit onto the drum

![Step 10](05-build-plan/step-10.png)

Gasket clean; lower the lid unit by the throat and close the locking ring.

### Step 11: tap, loose lid and vent onto the jacket

![Step 11](05-build-plan/step-11.png)

Tap into its socket on PTFE tape, lever closed; vent nipple through the lid with a locknut each side; lid loose on the rim.

### Step 12: wrap the jacket blanket

![Step 12](05-build-plan/step-12.png)

From 60 above the bottom to the rim, cut round the tap; tie wire.

### Step 13: legs onto the fins

![Step 13](05-build-plan/step-13.png)

With the jacket upside down on a padded stand, bolt each leg's flat face to its fin, two M10 bolts and nyloc nuts, tight.

### Step 14: foot cleats and pads onto the legs

![Step 14](05-build-plan/step-14.png)

One M10 bolt and nyloc nut through each leg and cleat, snug so the leg can pivot. Turn the unit upright.

### Step 15: heat-recovery unit over the kiln

![Step 15](05-build-plan/step-15.png)

Jacket empty and flue out (safety stop S4). Push the lift bar through the sleeve's top socket and hook the shackle onto its middle. Wind the unit up until its feet are above the top of the throat (about 1.55 m), swing the arm over the kiln, steadying the unit by a leg, and wind it down so the flared sleeve foot finds the throat and slides over it. Pull out the lift bar. **Hold point:** the gap between sleeve and throat is about 2 all round and every foot pad sits flat. To unload later, do the same the other way: wind up, swing the arm a quarter turn and set the unit down to the left of the kiln.

### Step 16: clips and rain cap onto the flue

![Step 16](05-build-plan/step-16.png)

Rivet the three clips 50 up from the foot and the cap legs at the top; rivet the cap onto the legs.

### Step 17: hang the baffle in the flue foot

![Step 17](05-build-plan/step-17.png)

Line the strip's hole up between the two flue holes and push the rod through all three.

### Step 18: flue into the jacket sleeve

![Step 18](05-build-plan/step-18.png)

From a stable step ladder, with a helper, lower the flue until its clips rest on the sleeve rim; the baffle goes down inside the sleeve. Then swing the lifting aid's arm back to its parked place, away from the flue.

### Step 19: logger and probes

![Step 19](05-build-plan/step-19.png)

Seen from the back right. Strap the logger box to the back right leg. Push the core probe through the drum hole into the retort, and the throat probe into the throat. **Hold point:** both probes are pulled out before the retort or the heat-recovery unit is moved.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of CCB-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Batch size | R1 | Pack the retort to 600 with bundled residue and weigh what went in | 10 kg or more air-dry |
| Air paths open | R4 | Slide each damper and the band from open to closed; look through the throat's holes; measure the gap under the rain cap | Every damper and the band move by hand; all 30 holes clear; at least 60 from the flue's top edge to the cone all round |
| Gas path sealed | R4 | Retort lid bolted on its gasket; outer lid on its rope gasket and locking ring | No visible gap at either lid |
| Jacket open and tight | R7 | Fill to 540 deep; leave overnight; look at the vent and the centre hole | No drip; vent and hole clear; nothing seals the top |
| Tap | R7 | Open and close the tap with the jacket full | Water runs and stops cleanly |
| Logger | R9 | The two class 1 probes and the block thermocouple in an ice bath and in boiling water against a reference thermometer | Within 5 °C at both points; a day's record on the card |
| Lifts | R11 | Weigh the drained heat-recovery unit on the winch with a hanging scale, and the retort with a batch of char | Unit about 47 kg, lifted only by the winch; retort with char about 16 kg |
| Lifting aid | R11 | Raise the drained unit 100 off the ground and hold it 5 minutes; then raise it 1.55 m and swing it a quarter turn and back | Winch holds; post top moves no more than about 50; the feet clear the throat; footing does not move |
| Outlet height | R12 | Tape from the ground to the flue's top edge | 2.72 m or more |
| Stand | R11 | Push on the jacket top sideways by hand | No movement at any joint; all three pads flat |
| Block temperature | Safety (S3); no requirement | Log the block thermocouple under the fibre board through the first burn | Recorded; no cracking. If a later burn without the board keeps the blocks under about 150 °C, the board may be left off later builds |
| Hot-surface labels | Safety; no requirement | Look at the drum blanket and the jacket blanket from the front | Both labels in place and readable |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before cutting, drilling or heating either drum.** You know what the drum held, and it was not fuel, solvent, pesticide or anything flammable or toxic; it is empty, washed and open. Paint and liners are burned off outdoors, upwind, with nobody downwind.
- **S2. Before the jacket is used.** It has held water overnight without leaking. The top is open, the vent nipple is clear, and no sealed lid, valve or plug is fitted anywhere.
- **S3. Before the first fire.** The site is bare soil or paving at least 5 m from buildings, fences, dry vegetation and residue piles, not under trees or a roof, with no burning ban and little wind. A fire extinguisher or 50 L of water and a shovel are at hand. A 3 m circle is marked; children and animals stay outside it. Everyone near the kiln wears heat-resistant gloves, eye protection and closed shoes. The jacket is at least three-quarters full. All first checks of section 5 have passed except the ones that need a burn.
- **S4. Before lifting the heat-recovery unit.** The jacket is drained, the flue is cool enough to hold with gloves, both probes are out, and the flue is lifted out. The unit is moved only with the lifting aid's winch, never carried; nobody stands or reaches under it while it hangs, and the winch handle is held until the brake holds. Never move the jacket full (about 85 kg).
- **S5. While the kiln is hot.** Never open the retort or the outer lid: air reaching hot gas or char can flash. Never stand over the flue or downwind of the throat. Stop a batch that smokes heavily. Draw hot water slowly from the tap; never add cold water to a jacket that has boiled dry.
- **S6. Before unloading.** The kiln has stood sealed overnight with every damper and the band closed; the shell is cool to the gloved hand. Tip the char onto bare ground and wet it before bagging.

## 7. Tools, skills and workspace

**Tools.** Angle grinder with thin cutting and flap discs; jigsaw with metal blades; drill with bits from 4.9 to 12 and a step drill to 20; hand rivet tool for 4.8 rivets; hacksaw; bench vice; files; tin snips; scriber, steel rule, tape, square, protractor and a 0.5 m spirit level; a length of 160 pipe and a larger pipe as rolling formers; spanners and a socket set for M6 to M16; a long spanner and a clamped bar for twisting the baffle; countersink; tape measure to 3 m; a 50 kg luggage scale; a reference thermometer. A stable step ladder for the flue and for bolting the lifting aid's arm; a spade and a bucket or mixer for the footing; a hanging scale to 100 kg. The water jacket goes to a welder.

**Skills.** Basic metalwork: marking out, cutting with a grinder and jigsaw, drilling, rolling thin sheet by hand, riveting and bolting. No certified trade is needed except the welder for the jacket. Running the kiln needs someone who has been shown how to light and close down a retort kiln safely.

**Workspace.** An outdoor or well-ventilated workshop for cutting and grinding (sparks travel several metres); an outdoor area for burning paint off the drums; the kiln site of S3 for assembly, since the finished kiln is moved in its three lifts (drum and plinth stay; the lid unit lifts off by hand and the heat-recovery unit by the lifting aid). Leave a clear space about 1.5 m across to the left of the kiln, where the unit is set down.

**Personal protective equipment.** Eye protection and hearing protection for grinding; cut-resistant gloves for sheet and drum edges; a dust mask for cutting blankets; heat-resistant gloves, eye protection and closed shoes for every burn.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 100 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/CCB-DWG-101` to `CCB-DWG-116`.
- General arrangement: `cad/drawings/CCB-DWG-001.pdf`, Rev P6.
- Calculations: `docs/04-calcs/01-sizing.md` (CCB-CAL-001 v0.6) and `docs/04-calcs/sizing.py`; masses, tripod and lifting aid section 4, draft and air section 6, jacket section 7.
- Bill of materials: `bom/bom.csv` and `bom/bom-notes.md`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (CCB-DDR-003), with CCB-DDR-001 and CCB-DDR-002; register `docs/06-design-decisions.md` (CCB-DEC-001).
- Requirements: `docs/03-requirements.md` (CCB-REQ-001 v0.9).
