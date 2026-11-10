# Design

Last updated 2026-11-10. Status: nothing built yet.

Each decision below is marked **Decided**, **Proposed** (a recommendation waiting for a yes), or **Open**.

## 1. Requirements

| Requirement | Value |
|---|---|
| Round tube | up to 4" OD, continuous rotation |
| Square / rectangular tube | up to 2" |
| Materials | steel, aluminum |
| Stock | up to 20 ft sticks passing through the headstock (a 4" x 1/4" wall steel stick weighs about 200 lb) |
| Cut zone | 18" of torch travel along the tube at minimum |
| Torch | radial (always points at the tube centerline), no bevel |
| Plasma source | Hypertherm Powermax45 XP, machine torch, CPC port |
| Fabrication | plasma-cut plate (CrossFire Pro), 33" x 33" CNC router, Bambu P1S prints, MIG/TIG, bolt-together. No lathe. Outsourced parts are acceptable where needed. |
| Controller | standalone and open. Not a Langmuir/FireControl add-on. |
| Use | high volume, so loading and repeat cuts should be quick |
| Publication | open source, reproducible by someone with a similar shop |

Accuracy target (proposed): cut edge within ±0.5 mm (0.020") of intended, so copes fit up for welding with no grinding. Kerf is about 1.5 mm, so this is realistic for plasma.

## 2. Architecture

```
 infeed roller stands        headstock        cut zone (18"+)          outfeed support
 ====o========o=============[  chuck  ]--o----------------------o=========
      20 ft stick passes     rotates A   ^ steady    torch on X / Z gantry
      through                            rollers     (plus short Y, proposed)
                                         slag tray below
```

- **Headstock (A axis):** a hollow rotating ring with a chuck on its face. The tube passes through the bore and is clamped close to the cut. See [headstock.md](headstock.md).
- **Steady rollers:** support the tube just past the chuck. They carry weight and do not drive.
- **Gantry:** carries the torch along the tube (X) and up and down (Z). The tube does not move axially during a cut.
- **Infeed and outfeed stands:** carry the rest of the stick while it rotates.
- **Controller:** LinuxCNC with QtPlasmaC on a PC, Mesa 7i96S Ethernet card, stepper drives.
- **CAM:** our own tool, [cam.md](cam.md).

## 3. Decisions

### 3.1 Headstock: geared slewing ring. Proposed.

A slewing ring is a large bearing with bolt holes in both races and gear teeth on one. It bolts to flat plate, so nothing needs to be turned on a lathe, and it gives a large bore, the bearing, and the final drive gear in one purchased part. Comparison and costs in [headstock.md](headstock.md).

### 3.2 Chuck: two self-centering V-jaws, plus profile insert plates. Proposed.

Two V-jaws on one left/right-hand screw center round tube of any size with one handwheel, and hold square tube by its corners. For rectangular tube, and for high-volume runs of one size, a plasma-cut plate with the tube's profile cut into it bolts to the faceplate and drives the tube by its flats. Details in [headstock.md](headstock.md).

### 3.3 Square and rectangular tube: add a short Y axis. Proposed, and it changes the "3 axes are enough" assumption.

Three axes are enough for round tube. For square tube they give a poor cut, for this reason:

With the torch fixed over the centerline, the torch is square to a flat face only at the middle of that face. As the tube turns, the torch meets the face at an increasing angle, reaching 45° at the corners of a square tube and more on the short side of a rectangle. The cut edge comes out bevelled by that angle, and the arc has to go through up to 41% more metal. Surface speed also swings widely as corners go past.

| Approach | Axes | Cut quality on flats | Corners | Notes |
|---|---|---|---|---|
| Continuous rotation, Z follows the surface | X, A, Z | Bevelled edge, 0° at mid-face up to 45° near corners | Cut on the fly | Z must move 0.41" per quarter turn on 2" square. Simplest machine. |
| Indexed: face up, cut it flat, turn 90° | X, Y, A, Z | Same as cutting flat plate | Torch off between faces, or rolled (below) | Needs Y travel of the tube width plus margin |
| Indexed faces with rolled corners | X, Y, A, Z | Same as flat plate | Tube turns while Y and Z track the corner, torch stays lit | What commercial tube machines do. Most CAM work. |

Recommendation: build the gantry with about 4" of Y travel from the start. It costs roughly $60 and one more motor, the 7i96S has five step/dir outputs so there is room, and it lets square tube be cut face by face. Start with indexed faces with the torch off between them, and add rolled corners later in software. If Y is rejected, continuous rotation with Z following is the fallback and the bevel is accepted.

### 3.4 Controller: LinuxCNC + QtPlasmaC + Mesa 7i96S. Proposed, with known gaps.

It is the only open controller with mature plasma support (torch height control, probing, pierce sequencing). Known gaps, found on the LinuxCNC forum on 2026-11-10 and not yet tested by us:

- **QtPlasmaC is built for flat tables.** Forum users report it is "not set up for 4-axis tube cutting" and work around it. Expect configuration work, not a stock install.
- **Feed rate.** LinuxCNC computes feed from linear axes only and ignores rotation when both move. A move that is mostly rotation would run far too fast at the tube surface. The usual fix is inverse-time feed (G93), which our CAM tool emits. Whether QtPlasmaC's G-code filter and its velocity-based torch height hold work with G93 moves is untested.
- **Torch height control during rotation** needs testing for the same reason: the controller's idea of cutting speed does not include rotation.

The fallback if QtPlasmaC fights us is plain LinuxCNC with a small custom torch-control component. The motion hardware stays the same.

### 3.5 Torch height: ohmic or float-switch probing for start height, arc voltage via THCAD2 while cutting. Proposed.

Round tube that runs true could be cut at a fixed height, but real tube is bowed and jaws are not perfect, so height control is worth having. The Powermax45 XP's CPC port provides a divided arc voltage through a selectable divider card; the divider setting and the matching THCAD2 range still need to be confirmed against the Hypertherm and Mesa manuals.

### 3.6 Work lead: dedicated rotating ground. Decided.

Cutting current must not return through the slewing ring or the roller bearings: arcing pits bearing races quickly. Use a rotary ground clamp or a sprung copper brush riding on the tube or chuck body, and electrically consider the bearing path as something to avoid.

### 3.7 CAM: own tool. Decided.

Fusion's plasma operations do not handle geometry wrapped around a tube. See [cam.md](cam.md).

## 4. Sizing notes

- **Bore:** 4" round needs about 102 mm, plus room for jaws to open. Target a clear bore of 130 mm or more.
- **A-axis speed:** surface speed equals cut speed. 1" OD tube cut at 150 in/min turns at 48 rpm; 4" OD at 60 in/min turns at 5 rpm. Small thin tube sets the top speed.
- **A-axis ratio:** about 25:1 from motor to ring is a reasonable start (for example a 5:1 gearbox and a 5:1 pinion-to-ring ratio). That puts 48 rpm at 1200 motor rpm, and one 1/8-microstep at 0.0003" on the surface of a 4" tube.
- **Backlash:** a 30 arc-minute gearbox behind a 5:1 ring stage contributes 0.1° at the tube, which is 0.0035" at the surface of a 4" tube. Gear mesh adds to this. Both are small next to the kerf, but direction reversals mid-cut should still be avoided.
- **Z travel:** 4" for the tube size range plus clearance; 6" is comfortable.
- **X travel:** 24" gives the 18" cut zone plus room for lead-ins and parking.

## 5. Open questions

For the owner:

1. **Part length versus the 18" cut zone.** A part coped at both ends that is longer than the torch travel must be released, advanced, and re-clamped between ends. Nothing then keeps the two copes clocked to each other on round tube. Options: longer X travel, a non-rotating feed gripper, a scribed witness line, or accept hand-clocking. What part lengths are typical?
2. **Y axis for square tube** (section 3.3): yes or no?
3. **License.** CERN-OHL-P or CERN-OHL-S for hardware and MIT for software are the usual choices.
4. **Common sizes and walls.** Which three or four tube sizes are most of the volume? This sets jaw design and which insert plates to draw first.
5. **Parts catching.** Should cut parts drop into a bin, or be supported until unloaded? Long parts will sag and pinch the kerf at the end of the cut.

Engineering:

6. Does QtPlasmaC accept G93 inverse-time moves with torch height control active? (section 3.4)
7. THCAD2 range and Powermax divider setting.
8. Does ohmic sensing work reliably on a rotating tube with mill scale, or is a float switch better?
9. Supporting rotating square tube: rollers under a turning square tube bounce. Likely needs a second passive ring with a profile insert as a steady.
10. Slewing ring selection: actual bore, gear module, runout, and price need a supplier quote. See [bom.md](bom.md).
11. Slag and fume: water tray under the cut zone, and sparks blown down the inside of the tube toward the headstock.
12. A-axis homing and a repeatable zero for clocking multiple cuts on one part.

## 6. Roadmap

1. CAM spike: round-on-round cope, G-code and paper template. **Done** (untested on hardware).
2. Validate the template by hand: print, wrap, cut, and fit a real joint.
3. Pick the slewing ring and build the headstock alone. Check runout and backlash with a pen in place of the torch, drawing on paper wrapped around a tube.
4. Gantry, controller, and first cuts on round tube.
5. Square tube.
6. CAM: full parts (two ends, clocking, length), holes and slots, STEP import.
7. Write build instructions and publish.

## Sources

- [QtPlasmaC with fourth axis, LinuxCNC forum](https://forum.linuxcnc.org/plasmac/49293-qtplasmac-with-fourth-axis-rotary)
- [Rotary cutting square tube with PlasmaC, LinuxCNC forum](https://forum.linuxcnc.org/plasmac/41087-rotary-cutting-square-tube-with-plasmac?start=10)
- [Feed rate priority on rotary and linear axis, LinuxCNC forum](https://www.forum.linuxcnc.org/38-general-linuxcnc-questions/32488-feed-rate-priority-on-rotary-and-linear-axis)
- [Inverse time feed with 4th rotary axis, LinuxCNC forum](https://forum.linuxcnc.org/20-g-code/50870-inverse-time-feed-g93-ignored-with-4th-rotary-axis)
- [THCAD-10, 5, or 300 for Powermax45 XP, LinuxCNC forum](https://www.forum.linuxcnc.org/plasmac/39999-thcad-10-5-or-300-for-hypertherm-powermax45-xp)
