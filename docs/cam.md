# CAM tool

Last updated 2026-11-10. Status: spike. One joint type, tested in software only.

## What it does today

`cam/cope.py` computes the end cut on a round tube (the branch) so it lands on another round tube (the header), and writes:

- `.ngc`: kerf-compensated G-code, X along the tube and A in degrees
- `.svg`: a 1:1 template to wrap around the tube

```sh
python3 cam/cope.py --od 1.75 --wall 0.12 --header-od 1.75 --angle 60 --offset 0 --kerf 0.06 --feed 100
```

| Option | Meaning | Default |
|---|---|---|
| `--od`, `--wall` | the tube being cut | required |
| `--header-od` | the tube it lands on | required |
| `--angle` | angle between the two centerlines, degrees | 90 |
| `--offset` | distance between the two centerlines; 0 means they intersect | 0 |
| `--kerf` | kerf width | 0.06 |
| `--feed` | cut speed at the tube surface, per minute | 100 |
| `--lead-in` | lead-in length | 0.2 |
| `--units` | `in` or `mm`, applies to every value | in |
| `--out` | output file stem | cope |

The branch must land fully on the header: `offset + od/2` cannot exceed `header_od/2`.

## Geometry

The branch lies along X. A point on it is described by its angle `phi` around the tube and its radius `rho`. With header radius `R`, joint angle `theta`, and centerline offset `e`, the branch meets the header surface at

```
x(phi, rho) = ( sqrt(R² − (e + rho·sin phi)²) − rho·cos phi·cos theta ) / sin theta
```

measured along the branch from the point nearest the header centerline.

**Wall thickness.** The torch is radial, so one pass cuts the whole wall at a given angle. The inside and outside of the wall meet the header at different X positions. The tool samples through the wall and cuts at whichever position leaves no metal inside the header. The other side of the wall is left with a small gap, which the weld fills. This is why the template shows slight kinks: they are where the controlling surface switches between the inner and outer wall.

**Kerf.** The path is shifted half a kerf toward the scrap side, measured on the tube's outer surface.

**Scaling per diameter.** The tool works in angle, so the output is correct for the diameter given and nothing in the machine configuration changes between tube sizes.

## G-code conventions

- `X0` is the finished long point of the part. The path extends half a kerf past it, so leave stock beyond X0.
- The cut starts at the deepest point of the cope with a straight lead-in from the scrap side, then makes one full turn with A increasing.
- `M3 $0 S1` and `M5 $0` start and stop the torch, as QtPlasmaC expects. No Z moves are written; the controller handles probing and height.
- Cutting moves use `G93` inverse-time feed so that speed is correct at the tube surface. See [design.md](design.md) section 3.4 for why, and for the open question of whether QtPlasmaC accepts it.
- Which way positive A turns is a machine setting. If the first paper test comes out mirrored, flip the A direction in the controller, not in the tool.

## Validation plan

1. **Template against a hand-fit joint.** Print the SVG at 100% and check the 50 mm bar. Wrap it around the tube with the seam on a scribed line, trace, cut by hand, and fit it to the header.
2. **Machine against the template.** Put a pen in the torch holder, wrap paper around a tube in the chuck, run the G-code, unwrap, and lay it over the printed template.
3. **Steel.** Cut, fit, and measure the gap. Adjust kerf.

Templates wider than a sheet of paper (tube over about 3" OD on letter or A4) need a large-format or tiled print.

## Tests

```sh
cd cam && uv run --no-project --with pytest pytest
```

The tests check the profile against the closed-form answer for a square joint, check in 3D that no part of the tube wall ends up inside the header, and check the kerf offset distance and the G-code structure.

## Not done yet

- A whole part: two ends, length between them, and clocking of one end to the other
- Holes and slots through the tube wall; header-side cutouts
- Branch larger than, or only partly landing on, the header
- Lead-out and overcut; pierce placement options
- Square and rectangular tube
- STEP import
- A material table (kerf and feed by material and thickness)
