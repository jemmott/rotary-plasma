"""Laser-cut plates for the headstock: K11-250 chuck on an 011.10.150 slewing ring.

Writes one DXF (for SendCutSend) and one SVG preview per plate. All dimensions
in mm. Standard library only. See docs/headstock.md for the stack-up and the
assembly order.

Change the numbers below if the real parts measure differently, then re-run:

    python headstock/plates.py
"""

import math
from pathlib import Path

# Chuck: K11-250, measured 2026-11-12.
CHUCK_OD = 250
CHUCK_BOLT_CIRCLE = 226  # 3 x M12 tapped in the chuck's back face
M12_CLEARANCE = 13.5  # countersunk by hand after cutting

# Slewing ring: 011.10.150, from a supplier's table. Measure before cutting.
RING_BORE = 100
RING_INNER_OD = 149
RING_INNER_BOLT_CIRCLE = 120  # 8 x 9 mm plain holes, inner (fixed) ring
RING_OUTER_BOLT_CIRCLE = 180  # 8 x 9 mm plain holes, outer (geared) ring
RING_TEETH = 105
MODULE = 2

# Drive: 20-tooth module 2 pinion on a geared NEMA 23 (23HS22-2804S-PG4, 4.25:1).
PINION_TEETH = 20
CENTER_DISTANCE = MODULE * (RING_TEETH + PINION_TEETH) / 2  # 125

M8_CLEARANCE = 9
M8_TAP = 6.8  # check SendCutSend's required hole size for an M8 x 1.25 tap

# Frame plate outline. A placeholder until the frame is drawn.
FRAME_W, FRAME_H = 380, 320
FRAME_BOLT = 11  # M10 clearance, one per corner
FRAME_BOLT_INSET = 20
PINION_OPENING = 50  # clears the pinion hub; motor holes are added once the gearbox is measured
ACCESS_HOLE = 18  # reach the outer-ring bolt heads from behind, one at a time


def bolt_circle(diameter, count, hole, start_deg=0.0):
    """Circles (x, y, d) for `count` holes equally spaced on a bolt circle."""
    r = diameter / 2
    angles = [math.radians(start_deg + 360 * i / count) for i in range(count)]
    return [(r * math.cos(a), r * math.sin(a), hole) for a in angles]


def adapter_plate():
    """Rotates. Chuck bolts to the front, the ring's outer race to the back."""
    return {
        "name": "adapter_plate",
        "note": "3/8 in (9.5 mm) steel. Tap 8 x M8. Countersink 3 x M12 on the ring side.",
        "rect": None,
        "circles": [(0, 0, CHUCK_OD), (0, 0, 150)]
        + bolt_circle(CHUCK_BOLT_CIRCLE, 3, M12_CLEARANCE, start_deg=90)
        + bolt_circle(RING_OUTER_BOLT_CIRCLE, 8, M8_TAP, start_deg=22.5),
    }


def spacer_ring():
    """Fixed. Lifts the ring off the frame plate so the outer-ring bolt heads clear it."""
    return {
        "name": "spacer_ring",
        "note": "1/4 in (6.35 mm) steel.",
        "rect": None,
        "circles": [(0, 0, RING_INNER_OD - 1), (0, 0, RING_BORE + 2)]
        + bolt_circle(RING_INNER_BOLT_CIRCLE, 8, M8_CLEARANCE, start_deg=22.5),
    }


def frame_plate():
    """Fixed. Carries the ring's inner race; the motor mounts behind it."""
    x, y = FRAME_W / 2 - FRAME_BOLT_INSET, FRAME_H / 2 - FRAME_BOLT_INSET
    corners = [(sx * x, sy * y, FRAME_BOLT) for sx in (-1, 1) for sy in (-1, 1)]
    return {
        "name": "frame_plate",
        "note": "1/4 in (6.35 mm) steel. Motor mounting holes not drawn yet.",
        "rect": (FRAME_W, FRAME_H),
        "circles": [(0, 0, RING_BORE + 2)]
        + bolt_circle(RING_INNER_BOLT_CIRCLE, 8, M8_CLEARANCE, start_deg=22.5)
        + [(CENTER_DISTANCE, 0, PINION_OPENING)]
        + [(0, RING_OUTER_BOLT_CIRCLE / 2, ACCESS_HOLE)]
        + corners,
    }


def rect_lines(w, h):
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    return [(pts[i], pts[(i + 1) % 4]) for i in range(4)]


def to_dxf(plate):
    """Minimal ASCII DXF: millimetre units, CIRCLE and LINE entities on layer 0."""
    out = ["0", "SECTION", "2", "HEADER", "9", "$INSUNITS", "70", "4", "0", "ENDSEC"]
    out += ["0", "SECTION", "2", "ENTITIES"]
    for x, y, d in plate["circles"]:
        out += ["0", "CIRCLE", "8", "0", "10", f"{x:.4f}", "20", f"{y:.4f}", "40", f"{d / 2:.4f}"]
    if plate["rect"]:
        for (x1, y1), (x2, y2) in rect_lines(*plate["rect"]):
            out += ["0", "LINE", "8", "0", "10", f"{x1:.4f}", "20", f"{y1:.4f}", "11", f"{x2:.4f}", "21", f"{y2:.4f}"]
    out += ["0", "ENDSEC", "0", "EOF"]
    return "\n".join(out) + "\n"


def to_svg(plate):
    """1:1 preview in mm, y up like the DXF."""
    w, h = plate["rect"] or (plate["circles"][0][2],) * 2
    w, h = w + 20, h + 20
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" '
        f'viewBox="{-w / 2} {-h / 2} {w} {h}">',
        '<g fill="none" stroke="black" stroke-width="0.5">',
    ]
    if plate["rect"]:
        rw, rh = plate["rect"]
        out.append(f'<rect x="{-rw / 2}" y="{-rh / 2}" width="{rw}" height="{rh}"/>')
    for x, y, d in plate["circles"]:
        out.append(f'<circle cx="{x:.3f}" cy="{-y:.3f}" r="{d / 2:.3f}"/>')
    out.append("</g></svg>")
    return "\n".join(out) + "\n"


PLATES = [adapter_plate, spacer_ring, frame_plate]

if __name__ == "__main__":
    out_dir = Path(__file__).parent / "out"
    out_dir.mkdir(exist_ok=True)
    for make in PLATES:
        plate = make()
        (out_dir / f"{plate['name']}.dxf").write_text(to_dxf(plate))
        (out_dir / f"{plate['name']}.svg").write_text(to_svg(plate))
        print(f"{plate['name']}: {len(plate['circles'])} circles. {plate['note']}")
