# Status

Last updated 2026-11-11. Read this first when picking the project back up.

## Where things stand

- **Scope is decided:** round tube only, up to 3" OD, three axes (X, A, Z), boring catalog parts, about $1,130. See [design.md](design.md).
- **Chuck is ordered:** Vevor K11-250 10" three-jaw, 80 mm bore. Waiting on delivery.
- **CAM spike works in software and on paper:** `cam/cope.py` makes G-code and a wrap template for round-on-round copes. The owner printed the template, cut by hand, and the fit was good. The G-code has not run on any machine.
- **Nothing is built and no CAD exists yet.**

## Waiting on

**Chuck measurements, when it arrives:**

1. Through-bore diameter. Does 3" tube pass with room to spare?
2. Back face: number of mounting holes, thread size (listings said M10 or M12), bolt circle diameter, and whether the bolts go in from the back or through from the front.
3. Back face: diameter and depth of the centering recess or boss, if there is one.
4. Body outside diameter and thickness, and weight.
5. Smallest tube it grips securely (1" is the smallest common size).
6. Runout, if an indicator is handy: clamp a straight tube and turn the chuck by hand.

## Next steps, in order

1. **Pick the slewing ring** once the chuck is measured. It needs a seller's dimensioned drawing showing a bore of 85 mm or more, gear module, tooth count, bolt circles, and weight. Fallback is a hollow rotary table. Details in [design.md](design.md) section 3.3.
2. **Draw the headstock:** laser-cut adapter plate (SendCutSend) between chuck and ring, pinion, motor mount, frame mount.
3. **CAM for arbitrary shapes from Fusion 360.** This does not depend on the chuck and can start any time. Plan in [cam.md](cam.md): a small Fusion script exports the cut edges of a selected tube body as unwrapped loops, and the existing tool turns loops into G-code and a template. The owner confirmed tubes are modelled as hollow bodies. The Fusion script can only be tested by the owner running it inside Fusion.
4. Gantry, torch quick mount (must match the one-bolt mount on the CrossFire Pro), second CPC cable, controller.

## Open risks

- **QtPlasmaC and tube cutting.** It is built for flat tables. Whether it accepts the inverse-time (G93) feed moves the CAM tool writes is untested. Fallback is plain LinuxCNC with simple torch control.
- **Slewing ring dimensions.** Listings for the small sizes give prices ($119 to $184) but no bore. The one dimensioned unit found weighs 24 kg.
- **Weight.** Chuck plus bearing is roughly 80 to 100 lb, so the machine should sit on its own wheeled cart.
- **Small thin tube speed.** 16 gauge on 1" tube may need the chuck to turn faster than an open-loop stepper likes.
- **Prices.** Most of the BOM is estimates. See [bom.md](bom.md) for which were checked.

## Housekeeping

- Everything is committed on `main`. There is no git remote; nothing has been pushed or published.
- The CERN-OHL-P v2 license text still needs adding before publishing.
- Tests: `cd cam && uv run --no-project --with pytest pytest` (6 pass).
