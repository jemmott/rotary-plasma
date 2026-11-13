# Draft BOM

Last updated 2026-11-12. This is a first pass for budgeting, not a shopping list.

**Only the rows marked "Checked" have a price read from a seller's page on 2026-11-10. Every other price is an estimate from general knowledge of the market and must be confirmed before ordering.** Shipping and tax are not included. The plasma cutter, torch, air supply, and a monitor and keyboard are assumed to be on hand.

## The build: round only, 3" max

Rough total **$1,170**. Same caveat: only "Checked" prices were read from a seller's page.

| Item | Qty | Each | Total | Price status |
|---|---|---|---|---|
| Mesa 7i96S | 1 | $149 | $149 | Checked |
| Open-loop NEMA 23 stepper with digital driver (X, Z, A) | 3 | $35 | $105 | Estimate |
| NEMA 23 planetary gearbox for A, 5:1 (or buy the A motor as a geared unit, StepperOnline 23HS22-2804S-HG5; price not checked) | 1 | $27 | $27 | Checked (via search result) |
| 48 V power supply | 1 | $35 | $35 | Estimate |
| PC: owner has one. It must be a PC (not a Mac), dedicated to the machine, running Linux, with an Ethernet port. | 1 | $0 | $0 | On hand |
| E-stop, relay, home switches, wiring | 1 | $80 | $80 | Estimate |
| Float switch for touch-off (printed, with a microswitch) | 1 | $10 | $10 | Estimate |
| Second CPC plug and cable, self-assembled (the existing one stays wired to the CrossFire) | 1 | $20 | $20 | Estimate |
| **Controller subtotal** | | | **$426** | |
| K11-250 10" three-jaw chuck, 80 mm bore, 49 lb, three M12 mounting bolts | 1 | $200 | $200 | Bought. Price paid not recorded. |
| Slewing ring 011.10.150, external gear, plain holes, 100 mm bore | 1 | $150 | $150 | Ordered. Price paid not recorded. |
| Laser-cut steel adapter plate, spacer ring, and frame plate from SendCutSend | 1 | $80 | $80 | Estimate |
| Module 2, 20-tooth steel pinion, 14 mm bore with keyway | 1 | $20 | $20 | Estimate. A 12 mm bore KHK SS2-20 was $30 at Zoro (checked 2026-11-12). |
| Dial indicator and magnetic base, to centre the chuck | 1 | $25 | $25 | Estimate |
| Rotary ground clamp | 1 | $40 | $40 | Estimate |
| **Headstock subtotal** | | | **$515** | |
| X: aluminum V-slot extrusion, wheels, belt | 1 | $70 | $70 | Estimate |
| Z slide, about 4" travel | 1 | $40 | $40 | Estimate |
| Printed magnetic breakaway torch mount | 1 | $10 | $10 | Estimate |
| **Gantry subtotal** | | | **$120** | |
| Steel for frame | 1 | $0 | $0 | On hand |
| Roller stands built from skate bearings | 4 | $10 | $40 | Estimate |
| Steady rollers, tray, shields, fasteners | 1 | $70 | $70 | Estimate |
| **Frame subtotal** | | | **$110** | |
| **Total** | | | **$1,171** | |

Later add-ons: THCAD2 arc-voltage height control ($79, checked), closed-loop motors (about $40 more per axis).

## To confirm before buying

1. Slewing ring: measure it against the table in [status.md](status.md) before cutting plates.
2. Geared motor: shaft diameter, keyway, and mounting holes, before buying the pinion and cutting the frame plate.
3. Hypertherm CPC pinout for start and arc-OK signals.

## Later: full-spec version (4" round, square and rectangular)

Not planned. Kept for reference; rough total $2,639. See [design.md](design.md) section 7.

### Controller and electrical

| Item | Qty | Each | Total | Source | Price status |
|---|---|---|---|---|---|
| Mesa 7i96S Ethernet step/dir + I/O card | 1 | $149 | $149 | [Mesa store](https://store.mesanet.com/index.php?route=product/search&search=7i96s) | Checked |
| Mesa THCAD2 arc voltage isolator | 1 | $79 | $79 | [Mesa store](https://store.mesanet.com/index.php?route=product/search&search=thcad) | Checked |
| Closed-loop NEMA 23 stepper, 3.0 Nm, with CL57T driver (X, Y, Z, A) | 4 | $73 | $292 | [StepperOnline 1-CL57T-S30A](https://www.omc-stepperonline.com/ts-series-3-0-nm-424-92oz-in-1-axis-closed-loop-stepper-cnc-kit-nema-23-motor-driver-w-2m-cable-1-cl57t-s30a) | Checked (via search result) |
| NEMA 23 planetary gearbox for A axis (10:1, 30 arc-min listed; 5:1 preferred, see design.md) | 1 | $27 | $27 | [StepperOnline MG series](https://www.omc-stepperonline.com/nema-23-stepper-motor-l-76mm-gear-ratio-10-1-plm-series-planetary-gearbox.html) | Checked (via search result) |
| Used small-form-factor PC with Ethernet, for LinuxCNC | 1 | $100 | $100 | eBay or local | Estimate |
| 48 V 350 W power supply for drives | 1 | $35 | $35 | StepperOnline or Amazon | Estimate |
| 24 V power supply for I/O | 1 | $20 | $20 | | Estimate |
| Inductive home/limit sensors | 4 | $8 | $32 | | Estimate |
| E-stop, torch-fire relay, terminal blocks, enclosure, cable, drag chain | 1 | $150 | $150 | | Estimate |
| CPC cable or connector kit for the Powermax | 1 | $50 | $50 | Hypertherm dealer | Estimate |
| Ohmic sensing: Hypertherm ohmic retaining cap plus isolated sense circuit, or a float switch | 1 | $80 | $80 | Hypertherm dealer | Estimate |
| **Subtotal** | | | **$1,014** | | |

### Headstock and chuck

| Item | Qty | Each | Total | Source | Price status |
|---|---|---|---|---|---|
| Slewing ring, external gear, clear bore 130 mm or more | 1 | $325 to $530 | $430 | [VXB 011.10 series](https://vxb.com/products/external-gear-turntable-bearings-01110100-01110120) | Checked, but the listing shows two contradictory prices and no bore size. Needs a quote. |
| Pinion to match the ring's gear module | 1 | $25 | $25 | Purchased, or cut in-house | Estimate |
| Left/right-hand lead screw with two nuts, for V-jaws | 1 | $60 | $60 | | Estimate |
| MGN12 rails and blocks for jaws | 2 | $25 | $50 | | Estimate |
| Rotary ground clamp | 1 | $50 | $50 | Welding supplier | Estimate |
| Steel plate for faceplate, jaws, mount | 1 | $100 | $100 | Shop stock | Estimate |
| **Subtotal** | | | **$715** | | |

### Gantry

| Item | Qty | Each | Total | Source | Price status |
|---|---|---|---|---|---|
| X: two HGR20 rails about 800 mm with four blocks | 1 | $110 | $110 | | Estimate |
| X drive: ball screw about 800 mm with supports, or belt | 1 | $60 | $60 | | Estimate |
| Y: short rail and ball screw, about 4" travel | 1 | $60 | $60 | | Estimate |
| Z: ball screw slide, about 6" travel | 1 | $70 | $70 | | Estimate |
| Magnetic breakaway torch mount | 1 | $60 | $60 | Purchased, or printed | Estimate |
| **Subtotal** | | | **$360** | | |

### Frame and supports

| Item | Qty | Each | Total | Source | Price status |
|---|---|---|---|---|---|
| Steel tube for base frame | 1 | $250 | $250 | Local steel yard | Estimate |
| Steady rollers near the cut (track rollers or cam followers) | 4 | $10 | $40 | | Estimate |
| Infeed and outfeed roller stands | 4 | $40 | $160 | Purchased pipe stands, or built | Estimate |
| Slag tray, spark shields, fasteners | 1 | $100 | $100 | | Estimate |
| **Subtotal** | | | **$550** | | |

### Total

| | |
|---|---|
| Controller and electrical | $1,014 |
| Headstock and chuck | $715 |
| Gantry | $360 |
| Frame and supports | $550 |
| **Total** | **$2,639** |
