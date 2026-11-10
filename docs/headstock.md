# Headstock and chuck concepts

Last updated 2026-11-10. Costs are rough; see [bom.md](bom.md) for which prices were checked.

The headstock has two jobs that can be chosen separately: **rotate** (a hollow bearing with a drive) and **grip** (a chuck on its face). It needs a clear bore of about 130 mm, must be buildable without a lathe, and must clamp close to the torch.

## Recommendation

**Current build (round only, 3" max):** a K11-250 10" three-jaw lathe chuck (concept E below). What it rotates on is still open. In order of preference under the "boring, default parts" rule:

1. A small slewing ring bolted to the back of the chuck (concept A, in a smaller size than the 4" machine needed), if a quote comes in reasonable.
2. A purchased hollow rotary table with a bore of 80 mm or more, which would include the bearing and gear reduction in one unit. Not yet priced or checked for bore size.
3. A routed ring on V-rollers with a belt (concept C). Cheapest, but shop-made and the least proven.

The rest of this document compares concepts for the original full-spec machine (4" round plus square and rectangular) and is kept for reference.

## Rotation concepts

| | Concept | Rough cost | Lathe needed | Backlash | Main risk |
|---|---|---|---|---|---|
| A | Geared slewing ring + pinion | $350 to $650 | No | Gear mesh, adjustable by pinion position | Price and quality vary a lot by supplier; specs on listings are thin |
| B | Two thin-section ball bearings in routed plates + belt | $150 to $250 | No, but needs accurate routed bores | None (belt) | Bearing seats must be routed to about ±0.05 mm |
| C | Routed ring riding on V-rollers + belt | $100 to $200 | No | None (belt) | Roundness is only as good as the routed ring; open to slag |
| D | Purchased hollow rotary chuck | $1,000 and up | No | Depends on unit | Few have a 4" through-bore; prices unverified |
| E | Large lathe chuck on a hollow spindle | $800 and up | Yes | Depends on drive | Rejected |

### A. Geared slewing ring

One race bolts to the machine frame, the other carries the faceplate. Gear teeth on the outer race mesh with a pinion on a geared stepper. Everything attaches to flat faces with bolts.

- For: no precision fits to make; rigid; handles the overhung weight of a 200 lb stick; one part is bearing, bore, and gear.
- Against: light-series steel rings with external teeth were listed at $325 to $530 at VXB (011.10 series; the listing did not state bore sizes and its two prices contradict each other). Direct-from-China pricing is probably $150 to $300 but is not verified. igus polymer slewing rings offer gear options but an ungeared 200 mm unit was already $823.
- The pinion can be plasma or router cut to match the module, or purchased.
- Mount the motor on a slotted plate so mesh backlash can be set.

### B. Thin-section bearings and belt

Two large thin ball bearings (for example 140 mm bore) sit in routed aluminum plates, with a hub made of stacked routed plates between them. A timing belt runs around a large printed or routed pulley on the hub.

- For: cheap bearings, zero backlash, quiet.
- Against: the bearing seats and hub must be accurate and concentric, which is asking a lot of a router. Bearing retaining compound can take up a few hundredths of a millimetre.

### C. Ring on rollers

A routed aluminum ring, 3/8" or thicker, rides on three or four V-groove rollers, one of them on an eccentric for adjustment. Belt drive around the ring.

- For: cheapest, any bore size, every part is made in the shop.
- Against: runout equals the roundness of the routed edge; the rollers and ring edge are exposed to slag and need shielding. A plasma-cut ring is not round enough for this.

### D. Purchased rotary chuck

Hollow chucks sold for plasma pipe cutting. Bulltear's Rotacut with an 8" four-jaw chuck was listed at $988 to $1,400 in an undated forum post; Precision Plasma sells one without a listed price. Units with a full 4" through-bore are uncommon. Worth one more look before committing to A, since it could save weeks.

### E. Lathe chuck on a hollow spindle. Rejected for 4", chosen for the round-only build.

A 4" through-bore needs a chuck of 12" or more, weighing over 100 lb, and a machined spindle and backplate.

At 3" maximum and round tube only, this changes. A commodity K11-250 10" three-jaw chuck has an 80 mm (3.15") bore and self-centers with one key, which is the fastest loading of any option here. K11-200 8" chucks (65 mm bore) were listed at $102 to $142; the 10" size had no US price in the listings found and is estimated at about $200. It weighs roughly 55 lb.

No spindle is needed: the chuck bolts by its back face to a routed plate ring, and that ring is the rotating element, riding on V-rollers with a belt drive (concept C) or bolted to a smaller slewing ring (concept A). The chuck's own runout then matters less than how well the ring is centered on the chuck, which can be shimmed or dialed in once with an indicator.

A three-jaw scroll chuck does not hold square or rectangular tube, so this is a round-only choice.

## Gripping concepts

| | Concept | Round | Square | Rectangular | Speed per load | Rough cost |
|---|---|---|---|---|---|---|
| G1 | Two V-jaws on one left/right-hand screw | Yes, self-centering | Yes, on corners | No | One handwheel | $100 to $150 |
| G2 | Four independent jaws, two used as fixed stops | Yes | Yes, on flats | Yes | Set two jaws once per size, then one or two screws per load | $100 to $150 |
| G3 | Profile insert plate per tube size | With a clamp screw | Yes, on flats | Yes | Slide through, one clamp | A few dollars of plate per size |
| G4 | Scroll chuck | Yes | Square only with 4 jaws | No | Fast | Ruled out with concept E |

### G1. Two V-jaws

Two opposed 90° V-jaws slide on short linear rails on the faceplate and are driven together by a single screw with left-hand thread on one half and right-hand on the other. Round tube is held on four lines and centers itself at any diameter. Square tube nests corner-first into the Vs and also centers itself; the faces end up at 45° to the jaws, which is only an angular offset in software.

Rectangular tube does not center in opposed Vs, because its diagonal is not in line with the jaws.

### G2. Four independent jaws

Four flat jaws on screws. Centering every load by hand is too slow for volume, but two adjacent jaws can be set once for a tube size and left as fixed stops, and only the opposite two are used to clamp. This grips flats and handles rectangles.

### G3. Profile insert plates

A plate with the tube's outline plus clearance, cut on the CrossFire, bolted to a standard pattern on the faceplate. Square and rectangular tube is driven by its flats with no adjustment; one thumbscrew or cam takes out the clearance. Two plates spaced a few inches apart keep the tube aligned. The same plates can serve in the passive steady that supports square tube near the cut.

Clearance needed for weld seams and tube tolerance causes a small centering error, set by the clearance. Good enough for plasma.

## Square tube: how it is gripped depends on how it is cut

See [design.md](design.md) section 7 for why square tube needs a fourth axis. Either method works with G1 or G3. Indexed cutting needs the faces to index squarely to the torch, so the chuck needs a repeatable angular zero: home the A axis, then set an offset per jaw type (45° for V-jaws).

## Sources

- [VXB external gear turntable bearings 011.10.100 / 120 / 150](https://vxb.com/products/external-gear-turntable-bearings-01110100-01110120)
- [igus PRT slewing ring bearings](https://www.igus.eu/prt/slewing-ring-bearings)
- [igus PRT-01-200 at Zoro](https://zoro.com/igus-slewing-ring-bearing-rpm-80-prt-01-200/i/G8000702)
- [K11-200 chuck, 65 mm bore, Nassau Electrical](https://www.nassauelectrical.com/products/k11-200a-8-self-centering-steel-lathe-chuck-for-versatile-machinery)
- [VEVOR K11-250 chuck, 80 mm bore](https://woodartsupply.com/a/s/products/vevor-3-jaw-lathe-chuck-10-self-centering-lathe-chuck-0-24-9-84-in-6-250-mm-clamping-range-with-t-key-fixing-screws-hexagon-wrench-for-lathe-3d-printer-machining-center-milling-drilling-machine)
- [Bulltear Rotacut forum post](https://forum.bulltear.com/d/37775--otary-axis-from-ulltear-the-quot-quot--dup2)
- [Precision Plasma rotary chuck](https://en.industryarena.com/forum/precision-plasma-llc-6-rotary-chuck-cnc-plasma-cutting--105914.html)
