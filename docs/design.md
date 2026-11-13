# Design

Last updated 2026-11-12. Status: nothing built yet.

Each decision is marked **Decided**, **Proposed** (a recommendation waiting for a yes), or **Open**.

Guiding rule from the owner: **boring, default parts.** Prefer the common catalog item over the clever one.

## 1. Requirements

| Requirement | Value |
|---|---|
| Shape | round tube only |
| Size | up to 3" OD. Common: 1", 1.5", 2", 2.5" |
| Wall | mostly 0.090" and 1/8", sometimes 16 gauge |
| Materials | steel, aluminum |
| Stock | 20 ft sticks passing through the headstock (3" x 1/8" wall steel is about 77 lb per stick) |
| Cut zone | 18" of torch travel along the tube at minimum |
| Torch | radial (always points at the tube centerline), no bevel |
| Plasma source | Hypertherm Powermax45 XP, machine torch, CPC port |
| Fabrication | plasma-cut plate (CrossFire Pro), 33" x 33" CNC router, Bambu P1S prints, MIG/TIG, bolt-together. No lathe. |
| Controller | standalone and open. Not a Langmuir/FireControl add-on. |
| Use | high volume, so loading and repeat cuts should be quick |
| Budget | about $1,100 to $1,200 excluding the plasma cutter |
| Torch | shared with the CrossFire Pro; comes off that table with one bolt, so this machine needs a matching quick mount and its own CPC cable |
| Shop | frame steel is on hand in most gauges; SendCutSend is available for accurate laser-cut plates; a PC is on hand |
| Placement | used on or beside the workbench, stored underneath, moved on wheels. Long infeed and outfeed runs are available. |
| Part shapes | arbitrary cuts modelled in Fusion 360, not only standard copes |
| Publication | open source, reproducible by someone with a similar shop |

Not required: square or rectangular tube, 4" tube, parts catching, automatic clocking between the two ends of a long part (done by hand with an indicator and a level).

Accuracy target (proposed): cut edge within ±0.5 mm (0.020") of intended, so copes fit up for welding with no grinding.

## 2. Architecture

```
 infeed roller stands        headstock        cut zone (18"+)          outfeed support
 ====o========o=============[  chuck  ]--o----------------------o=========
      20 ft stick passes     rotates A   ^ steady    torch on X / Z gantry
      through                            rollers     slag tray below
```

- **Headstock (A axis):** a three-jaw lathe chuck on a hollow rotating mount. The tube passes through and is clamped close to the cut. See [headstock.md](headstock.md).
- **Steady rollers:** support the tube just past the chuck. They carry weight and do not drive.
- **Gantry:** carries the torch along the tube (X) and up and down (Z). The tube does not move axially during a cut.
- **Infeed and outfeed stands:** carry the rest of the stick while it rotates.
- **Controller:** LinuxCNC with QtPlasmaC on a PC, Mesa 7i96S Ethernet card, open-loop stepper drives.
- **CAM:** our own tool, [cam.md](cam.md).

## 3. Decisions

### 3.1 Scope: round only, 3" max. Decided.

Round only removes a fourth axis and all square-tube handling, and lets a self-centering lathe chuck do the gripping. 3" is the largest tube that fits a commodity 10" chuck.

### 3.2 Chuck: K11-250 10" three-jaw self-centering lathe chuck, 80 mm bore. Decided.

One key, self-centering, a standard part sold everywhere. 49 lb. An 8" chuck is cheaper but its 65 mm bore is too tight for 2.5" tube.

### 3.3 How the chuck rotates: 011.10.150 slewing ring with a pinion. Decided.

An 011.10.150 external-gear slewing ring (100 mm bore, 105 teeth, module 2, 5.5 kg) bolts between the chuck and the frame through laser-cut plates. A 20-tooth pinion on a geared NEMA 23 (4.25:1) drives it at 22.3:1. Design and assembly order are in [headstock.md](headstock.md).

The alternatives looked at were a hollow rotary table ($554 and up for units found, through-hole unclear) and a shop-made ring on rollers.

The chuck and ring together weigh about 61 lb. The machine should still live on its own wheeled cart at bench height.

### 3.4 Motion: open-loop NEMA 23 steppers, three axes. Decided.

X on V-wheels and aluminum extrusion with a belt; Z on a small purchased slide. Both are standard hobby CNC parts.

### 3.5 Controller: LinuxCNC + QtPlasmaC + Mesa 7i96S. Proposed, with known gaps.

It is the only open controller with mature plasma support. Known gaps, found on the LinuxCNC forum on 2026-11-10 and not yet tested by us:

- **QtPlasmaC is built for flat tables.** Forum users report it is "not set up for 4-axis tube cutting" and work around it. Expect configuration work.
- **Feed rate.** LinuxCNC computes feed from linear axes only and ignores rotation when both move. The usual fix is inverse-time feed (G93), which our CAM tool emits. Whether QtPlasmaC accepts G93 moves is untested.

The fallback is plain LinuxCNC with a small custom torch-control component. The hardware stays the same.

### 3.6 Torch height: float-switch touch-off, then fixed height. Decided for the first build.

The tube is clamped and supported close to the cut, so height should hold. Arc-voltage control (Mesa THCAD2, $79) is an add-on if thin tube shows it is needed.

### 3.7 Work lead: dedicated rotating ground. Decided.

Cutting current must not return through the headstock bearing or the rollers: arcing pits bearing races. Use a rotary ground clamp or a sprung copper brush on the tube or chuck body.

### 3.8 CAM: own tool, fed from Fusion 360. Decided; approach proposed.

Fusion's plasma operations do not handle geometry wrapped around a tube. Parts are often unusual shapes, so the tool must take arbitrary cuts from a Fusion model, not just parametric copes. Plan in [cam.md](cam.md).

### 3.9 License. Decided.

MIT for software, CERN-OHL-P v2 for hardware.

## 4. Sizing notes

- **A-axis speed:** surface speed equals cut speed. 1" tube cut at 150 in/min turns at 48 rpm; 3" at 60 in/min turns at 6 rpm. Small thin tube sets the top speed.
- **A-axis ratio:** 22.3:1 from motor to chuck. At that ratio, 48 rpm is 1070 motor rpm, which is near the limit for an open-loop stepper on 48 V; 16 gauge on 1" tube may need a lower ratio or a slower cut. To be checked when the drive is chosen.
- **Resolution:** at about 25:1 and 1/8 microstepping, one step is 0.0002" on the surface of a 3" tube.
- **Z travel:** 4" covers 1" to 3" tube with clearance.
- **X travel:** 24" gives the 18" cut zone plus lead-ins and parking.

## 5. Open questions

For the owner: see the list in the README.

Engineering:

1. Headstock details still open: see [headstock.md](headstock.md).
2. Does QtPlasmaC accept G93 inverse-time moves?
3. Open-loop stepper speed for small thin tube (section 4).
4. A-axis home and a repeatable zero.
5. Slag and fume: water tray under the cut zone; sparks blown down the inside of the tube toward the chuck.
6. Outfeed support that lets a finished part be removed easily.

## 6. Roadmap

1. CAM spike: round-on-round cope, G-code and paper template. **Done.**
2. Validate the template by hand: print, wrap, cut, and fit a real joint. **Done by the owner, fit was good.**
3. Buy and measure the chuck; get a slewing ring drawing; lock the headstock design.
3a. CAM: Fusion 360 export of arbitrary cuts (in parallel with 3).
4. Build the headstock alone. Check runout with an indicator, and accuracy with a pen in place of the torch drawing on paper wrapped around a tube.
5. Gantry, controller, first cuts.
6. CAM: full parts (two ends and length), straight and miter cuts, holes and slots, STEP import.
7. Write build instructions and publish.

## 7. Later: possible full-spec version

Not planned, kept for reference. A machine for 4" round plus square and rectangular tube was costed at about $2,600 ([bom.md](bom.md)). It would use a geared slewing ring with V-jaws and profile insert plates ([headstock.md](headstock.md)).

Square tube needs a fourth axis to cut well. With the torch fixed over the centerline, the torch is square to a flat face only at mid-face; the cut edge is bevelled by up to 45° near the corners. A short Y axis lets each face be turned up and cut like flat plate. The controller card, PC, frame, gantry layout, and CAM tool would carry over.

## Sources

- [QtPlasmaC with fourth axis, LinuxCNC forum](https://forum.linuxcnc.org/plasmac/49293-qtplasmac-with-fourth-axis-rotary)
- [Feed rate priority on rotary and linear axis, LinuxCNC forum](https://www.forum.linuxcnc.org/38-general-linuxcnc-questions/32488-feed-rate-priority-on-rotary-and-linear-axis)
- [Inverse time feed with 4th rotary axis, LinuxCNC forum](https://forum.linuxcnc.org/20-g-code/50870-inverse-time-feed-g93-ignored-with-4th-rotary-axis)
- [Rotary cutting square tube with PlasmaC, LinuxCNC forum](https://forum.linuxcnc.org/plasmac/41087-rotary-cutting-square-tube-with-plasmac?start=10)
