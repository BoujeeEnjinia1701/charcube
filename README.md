# CharCube

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** CleanTech · **TRL:** 3 of 9 (proof of concept on paper; TRL 4 on hold) · **Prototype budget:** about $300 USD · **Difficulty:** 2 of 5

Batch retort kiln that turns biomass into biochar, with a secondary burner that cleans up the syngas and a jacket that recovers heat for hot water.

![CharCube concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement CCB-DWG-001 (PDF)](cad/drawings/CCB-DWG-001.pdf) · [Calculations CCB-CAL-001](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Crop residue gets burned in the open, releasing carbon and smoke. India alone burns about 100 Mt of residue a year in the field, linked to tens of thousands of premature deaths from smoke. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## Concept

Batch retort kiln that turns biomass into biochar, with a secondary burner that cleans up the syngas and a jacket that recovers heat for hot water.

A 114 L steel drum packed with 12.0 kg of bundled residue sits inside a 200 L drum. Gas from the heated residue burns in the gap between the drums and again in a burner throat fed by an air shroud, then heats about 61 L of water in an open-vented jacket around the flue. The TRL 3 calculations (CCB-CAL-001, central estimates) give about 3.0 kg of biochar per batch in a burn of about 4.5 h with about 5.8 kg of wood, and only about 6.4 MJ of hot water, for $298 in kiln parts. Burn time, hot water and start-up wood miss their targets on paper; the options are in the review note. Nothing is measured yet.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Nested steel drum pair: 200 L outer drum and 114 L inner retort
- Burner throat with secondary air shroud
- Flue pipe with rain cap
- Open-vented water jacket around the flue (replaces the copper coil in the first sketch; decided by Amish, 2026-09-25)
- Two-channel thermocouple logger

The priced bill of materials is in [bom/bom.csv](bom/bom.csv). The parametric model is [cad/src/model.py](cad/src/model.py), with STEP and STL exports in `cad/step/` and `cad/stl/`.

## Safety

> Involves open flame, hot surfaces (about 125 to 260 °C outside, 400 to 650 °C gas inside), flammable and toxic pyrolysis gas (including carbon monoxide) and water near boiling. Operate outdoors only, at least 5 m from structures and dry vegetation, with the required safety kit (fire suppression, gloves, eye protection) on hand. Never open the kiln while hot, never seal the water jacket, and never use drums that held fuel or chemicals. See the safety section of the [design precis](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (CCB-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `CCB-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
