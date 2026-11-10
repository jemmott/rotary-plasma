# Rotary Plasma

An open-source, garage-scale CNC plasma tube cutter and coper. Standalone machine: it brings its own motion and controller, and uses a plasma cutter you already own.

**Status: design phase.** Nothing has been built or cut yet. The docs here are the shared source of truth; change them when a decision changes.

## Target

| | |
|---|---|
| Tube | round only, up to 3" OD |
| Material | steel and aluminum |
| Stock length | up to 20 ft, passing through the headstock |
| Cut zone | 18" minimum |
| Axes | X (along tube), A (rotation), Z (torch height) |
| Budget | about $1,200 excluding the plasma cutter |
| Torch | radial, no bevel. Reference build: Hypertherm Powermax45 XP machine torch |
| Built with | plasma-cut plate, router-cut parts, 3D prints, bolts, purchased bearings. No lathe. |

## Needed from the owner before the design is locked

1. Result of the paper template test (print `examples/*.svg`, wrap, cut, fit).
2. Is the torch shared with the CrossFire Pro, or does this machine get its own?
3. Does the Powermax have the CPC port fitted?
4. Spare PC with an Ethernet port, or buy one?
5. Frame steel on hand (sizes), and what the router can cut (aluminum plate? how thick?).
6. Where the machine goes: working height, and room past the cut zone for the longest finished part.
7. Cut types wanted besides copes: straight cutoffs, miters, holes, slots?
8. Is a 55 lb, roughly $200 chuck acceptable?

## Docs

- [docs/design.md](docs/design.md): requirements, architecture, decisions, open questions
- [docs/headstock.md](docs/headstock.md): headstock and chuck concepts compared, with rough costs
- [docs/bom.md](docs/bom.md): draft bill of materials with prices
- [docs/cam.md](docs/cam.md): how the CAM tool works and how to validate it

## CAM tool

`cam/cope.py` turns a tube joint into kerf-compensated G-code plus a 1:1 paper wrap template. It needs Python 3 and nothing else. So far it does one thing: a round tube coped to land on another round tube, at any angle and centerline offset.

```sh
python3 cam/cope.py --od 1.75 --wall 0.12 --header-od 1.75 --angle 60 --out examples/cope_1.75_on_1.75_60deg
```

This writes `.ngc` (G-code) and `.svg` (template). Print the SVG at 100%, wrap it around the tube, and compare it with a hand-fit joint before trusting the G-code. Example output is in [examples/](examples/).

Tests: `cd cam && uv run --no-project --with pytest pytest`

## Layout

```
docs/       design docs
cam/        CAM tool and tests
examples/   generated sample output
```

CAD, controller config, and build instructions will get their own folders when they exist.

## License

Software is MIT ([LICENSE](LICENSE)). Hardware designs and documentation are [CERN-OHL-P v2](https://ohwr.org/cern_ohl_p_v2.txt); the full license text still needs to be added to the repo before publishing.
