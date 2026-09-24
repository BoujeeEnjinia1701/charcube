# CharCube

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** CleanTech · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $300 USD · **Difficulty:** 2 of 5

Batch retort kiln that turns biomass into biochar, with a secondary burner that cleans up the syngas and a jacket that recovers heat for hot water.

## Problem

Crop residue gets burned in the open, releasing carbon and smoke.

## Concept

Batch retort kiln that turns biomass into biochar, with a secondary burner that cleans up the syngas and a jacket that recovers heat for hot water.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Nested steel barrel pair
- Flue pipe
- Secondary air manifold
- Copper coil heat exchanger
- Thermocouple logger

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Involves open flame and combustible syngas. Operate outdoors, away from structures, with fire suppression on hand.

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
