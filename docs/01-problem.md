---
doc_id: CCB-PRB-001
title: CharCube problem statement
project: CharCube
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, out of scope, prior work with sources)
---

# CharCube problem statement

Crop residue gets burned in the open, releasing carbon and smoke. Farmers burn it because it is the fastest and cheapest way to clear a field between harvests, and nothing nearby pays for it. CharCube is a small batch retort kiln, built from two steel drums, that turns a farm's residue into biochar for its own soil, burns the smoky gas instead of venting it, and returns some of that heat as hot water. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## The problem

Open burning of crop residue is large, seasonal and harmful:

- **Scale.** India alone generates about 500 Mt of crop residue a year and burns about 100 Mt of it in the field ([Lan et al. 2022, *Nature Communications*](https://www.nature.com/articles/s41467-022-34093-z)). World rice straw production is about 370 to 520 Mt a year, and much of it is burned where the next crop follows quickly ([Van Hung et al. 2020](https://link.springer.com/chapter/10.1007/978-3-030-32373-8_1)).
- **Health.** In India, residue burning was linked to an estimated 44,000 to 98,000 premature deaths a year from particulate exposure between 2003 and 2019, with downwind PM2.5 peaks of 200 to 1,200 µg/m³ during the burning season ([Lan et al. 2022](https://www.nature.com/articles/s41467-022-34093-z)).
- **Carbon.** Burning returns almost all of the residue's carbon to the air as CO₂, plus methane, carbon monoxide and black carbon. Turning the same residue into biochar can keep a large share of its carbon in the soil for a century or more: the IPCC default is that 65 to 89 % of biochar carbon remains after 100 years, depending on production temperature ([IPCC 2019 Refinement, Vol. 4, Ch. 2, Appendix 4](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch02_Ap4_Biochar.pdf)).

Making biochar badly can undo much of the benefit. Traditional earth and pit kilns emit large amounts of methane and carbon monoxide. Field measurements of medium-sized kilns in rural tropical areas found about 54 g of methane per kilogram of charcoal from traditional kilns and about 24 g/kg from improved retort kilns ([Sparrevik et al. 2015, *Biomass and Bioenergy*](https://www.sciencedirect.com/science/article/abs/pii/S0961953414005170)). At a 100-year global warming potential of about 28, 24 g of methane is about 0.7 kg CO₂e per kilogram of char, a large fraction of the carbon the char stores. The gas has to be burned, not vented.

Three gaps remain for smallholders:

- **Cost and skill.** Proven designs such as the Adam retort are brick or steel structures sized for charcoal businesses; flame-curtain (Kon-Tiki) kilns are cheap but open-topped and waste their heat.
- **Wasted heat.** Every design burns its pyrolysis gas to protect the air, but few put the heat to use. A household that also heats water on a wood or dung fire gains a second reason to run the kiln.
- **Evidence.** Few low-cost kilns publish temperature logs, so a user cannot tell whether a batch reached the 450 to 600 °C needed for stable char.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Smallholder farmer with cereal or cotton residue | Clear residue without open burning; make a soil amendment from it | Rice, wheat, maize or cotton; short gap between harvest and sowing; residue often wet or bulky |
| Farm household | Hot water for washing and cleaning from the same fire | Water often heated on wood, dung or LPG |
| Farmer group, cooperative or NGO | Several kilns shared between farms, with records of how much char each batch made | Village or block level; carbon or soil-health programs |
| Agricultural extension worker or researcher | A cheap, repeatable kiln with logged temperatures, to compare feedstocks and char quality | Research station, college farm, field trials |
| Local fabricator | A design built from standard drums and pipe with hand tools, drill and angle grinder | Village workshop; welding available for one part only |
| Open hardware community | A documented, open reference retort with honest numbers | Makerspaces, university labs, NGOs |

## Constraints

- Garage-buildable prototype, concept budget about $300 USD for parts.
- Built from standard 200 L (55 US gal) and 114 L (30 US gal) open-head steel drums, plain (not galvanized) steel pipe and bought fittings.
- Outdoor, batch operation by one or two adults, one batch a day, with cooling overnight.
- No electricity needed to run the kiln. The temperature logger may use a small USB power bank.
- Must burn its pyrolysis gas under all normal operating conditions; smoke only during light-up.
- Hot water circuit open to the air (unpressurized) so it cannot build pressure.
- Feedstock is low-density crop residue: loose rice straw is only 13 to 18 kg/m³ dry ([Van Hung et al. 2020](https://link.springer.com/chapter/10.1007/978-3-030-32373-8_1)) and chopped wheat straw about 36 to 43 kg/m³ ([Chevanan et al. 2010, *Bioresource Technology*](https://www.academia.edu/6707237/Bulk_density_and_compaction_behavior_of_knife_mill_chopped_switchgrass_wheat_straw_and_corn_stover)), so it must be packed, bundled or mixed with denser stalks and cobs to fill a drum usefully.

## Out of scope

- Clearing a whole field in one season. At about 12 kg per batch, one kiln handles about 3 t of dry residue a year; a hectare of rice leaves several tonnes of straw. CharCube serves a household's or a trial plot's residue, and a cooperative would need several kilns. This scale gap is stated plainly in CCB-REQ-001.
- Selling charcoal for cooking fuel.
- Certified carbon credits. Certification (for example the [European Biochar Certificate](https://www.european-biochar.org/en)) needs lab analysis and audited records beyond this project; the logger only supports it.
- Pressurized hot water, space heating or connection to household plumbing.
- Wet feedstock (manure, food waste) that needs drying first.

## Prior work

- **Adam retort (Improved Charcoal Production System).** A brick retort that burns its volatiles in a separate chamber and uses the heat to speed carbonization; reported conversion efficiency of 30 to 42 % against 10 to 22 % for earth mounds, up to 75 % lower emissions and a 12 h cycle ([Adam 2009, *Renewable Energy*](https://ideas.repec.org/a/eee/renene/v34y2009i8p1923-1925.html)).
- **Field emissions of retort kilns.** Retorts cut methane by about 56 % and carbon monoxide by about 67 % against traditional kilns, but yield was not significantly higher, partly because start-up needs extra wood ([Sparrevik et al. 2015](https://www.sciencedirect.com/science/article/abs/pii/S0961953414005170)). CharCube's start-up fuel is therefore counted in its energy budget.
- **Kon-Tiki flame-curtain kilns.** Open cone kilns that need no start-up fuel; measured char yield of 22 ± 5 % on a dry mass basis, 76 ± 9 % carbon, methane 30 ± 60 g/kg and CO 54 ± 35 g/kg of biochar ([Cornelissen et al. 2016, *PLOS ONE*](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0154617); [Schmidt and Taylor 2014, *the Biochar Journal*](https://www.biochar-journal.org/itjo/media/doc/1437139451142.pdf)). They are the main low-cost alternative to CharCube.
- **Nested-drum retorts.** Two-drum retorts with the gas vented from the inner drum into a fire in the annulus are widely built by hobbyists and extension projects. Specific published designs were not verified for this note and are not cited.
- **Biochar persistence.** The IPCC gives default fractions of biochar carbon remaining after 100 years (0.65 low, 0.80 medium, 0.89 high temperature) and default organic carbon contents (0.49 for rice husk and straw char, 0.65 for herbaceous material) ([IPCC 2019](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch02_Ap4_Biochar.pdf)). Later work argues most carbon in well-made biochar persists far longer ([the Biochar Journal](https://www.biochar-journal.org/en/ct/109)). CharCube uses the IPCC defaults, which are conservative.

## Open questions

- Which region and residue first: paddy straw in northwest India, maize and cotton stalks in East Africa, or another? Proposed, awaiting Amish.
- Is hot water valued enough to justify the water jacket, or would users rather have a lower-cost kiln without it?
- How will users pack straw: hand bundles, a simple press, or mixing with stalks? A press is a separate project.
- Where will the char go: own fields, a cooperative's compost, or a buyer?
- Do local open-burning rules restrict running a kiln during burning bans?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
