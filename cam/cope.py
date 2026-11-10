"""Saddle cope for a round tube landing on a round tube.

Outputs kerf-compensated G-code (X along the tube, A rotary in degrees)
and a 1:1 SVG wrap template. Standard library only.

Geometry (see docs/cam.md):
  The tube being cut ("branch", outer radius r) lies along the machine X axis.
  The tube it lands on ("header", outer radius R) crosses it at `angle` with
  the two centerlines `offset` apart. For a point on the branch at radius rho
  and angle phi, the branch meets the header surface at

      x(phi, rho) = (sqrt(R^2 - (offset + rho sin phi)^2) - rho cos phi cos angle) / sin angle

  x is measured along the branch from the point nearest the header centerline.
  The torch is radial (no bevel), so one cut removes the whole wall thickness
  at a given phi. To avoid interference we cut at the largest x anywhere in the
  wall; the gap left on the other side of the wall is filled by weld.
"""

import argparse
import math

MM_PER = {"in": 25.4, "mm": 1.0}


def cope_profile(od, wall, header_od, angle_deg, offset=0.0, n=360):
    """Return n points [(phi_radians, x)] of the finished cut edge. Stock is at larger x."""
    r, R = od / 2, header_od / 2
    theta = math.radians(angle_deg)
    if not 0 < wall < r:
        raise ValueError("wall must be between 0 and od/2")
    if not 10 <= angle_deg <= 170:
        raise ValueError("angle must be between 10 and 170 degrees")
    if abs(offset) + r > R + 1e-9:
        raise ValueError("branch does not fully land on header: need |offset| + od/2 <= header_od/2")

    rhos = [r - wall * i / 4 for i in range(5)]  # sample through the wall

    def x_at(phi, rho):
        y = offset + rho * math.sin(phi)
        return (math.sqrt(max(R * R - y * y, 0.0)) - rho * math.cos(phi) * math.cos(theta)) / math.sin(theta)

    return [(phi, max(x_at(phi, rho) for rho in rhos))
            for phi in (2 * math.pi * i / n for i in range(n))]


def kerf_offset(profile, od, kerf):
    """Shift the path kerf/2 toward the waste (-x) side, measured on the outer surface."""
    r, n = od / 2, len(profile)
    out = []
    for i, (phi, x) in enumerate(profile):
        dx = profile[(i + 1) % n][1] - profile[i - 1][1]
        ds = r * 4 * math.pi / n  # arc length between neighbours i-1 and i+1
        norm = math.hypot(dx, ds)
        # tangent is (dx, ds); the normal with a negative x component is (-ds, dx)
        out.append((phi + (dx / norm) * (kerf / 2) / r, x - (ds / norm) * (kerf / 2)))
    return out


def gcode(profile, od, feed, kerf, lead_in, units="in", title=""):
    """G-code for one cope. X0 is the finished long point of the part; A is degrees.

    Cutting moves use G93 (inverse time) so the feed is true surface speed:
    LinuxCNC otherwise ignores rotary motion when computing feed.
    """
    r = od / 2
    x0 = min(x for _, x in profile)
    path = kerf_offset(profile, od, kerf)
    start = max(range(len(path)), key=lambda i: path[i][1])  # deepest point: surely on material
    path = path[start:] + [(phi + 2 * math.pi, x) for phi, x in path[:start]]  # keep A increasing
    path.append((path[0][0] + 2 * math.pi, path[0][1]))  # close the loop

    def fmt(phi, x):
        return f"X{x - x0:.4f} A{math.degrees(phi):.3f}"

    phi0, xs = path[0]
    lines = [
        f"({title})",
        f"(X0 = finished long point of part. Path reaches X{-kerf / 2:.4f}: leave stock beyond X0.)",
        "(UNTESTED ON HARDWARE - dry run first)",
        "G20" if units == "in" else "G21",
        "G90 G94",
        f"G0 {fmt(phi0, xs - lead_in)}",
        "M3 $0 S1",
        f"G1 {fmt(phi0, xs)} F{feed:.1f}",
        "G93",
    ]
    prev = path[0]
    for phi, x in path[1:]:
        dist = math.hypot(x - prev[1], r * (phi - prev[0]))
        lines.append(f"G1 {fmt(phi, x)} F{feed / dist:.2f}")
        prev = (phi, x)
    lines += ["G94", "M5 $0", "M2"]
    return "\n".join(lines) + "\n"


def svg_template(profile, od, units="in", title=""):
    """1:1 wrap template. Width is the tube circumference; wrap it with the seam at 0 degrees."""
    k = MM_PER[units]
    r = od / 2 * k
    circ = 2 * math.pi * r
    x0 = min(x for _, x in profile)
    pts = [(r * phi, (x - x0) * k) for phi, x in profile]
    pts.append((circ, pts[0][1]))
    depth = max(y for _, y in pts)
    h = depth + 30  # room below the cut line for notes
    notes = title.split(", ") + [f"width = circumference = {circ:.1f} mm", "print at 100%; bar = 50 mm",
                                 "tube end at top, keep this side"]
    note_text = "".join(f'<text x="3" y="{h - 8 - 3 * i:.3f}">{t}</text>' for i, t in enumerate(reversed(notes)))
    poly = " ".join(f"{s:.3f},{y:.3f}" for s, y in pts)
    quarters = "".join(
        f'<line x1="{circ * q / 4:.3f}" y1="0" x2="{circ * q / 4:.3f}" y2="{h:.3f}" stroke="#999" stroke-dasharray="2 2"/>'
        f'<text x="{circ * q / 4 + 1:.3f}" y="{h - 1:.3f}">{q * 90}&#176;</text>'
        for q in range(4))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{circ:.3f}mm" height="{h:.3f}mm" viewBox="0 0 {circ:.3f} {h:.3f}">
<g fill="none" stroke="black" stroke-width="0.25">
<rect x="0" y="0" width="{circ:.3f}" height="{h:.3f}"/>
<polyline points="{poly}" stroke-width="0.4"/>
<line x1="3" y1="{h - 5:.3f}" x2="53" y2="{h - 5:.3f}" stroke-width="0.5"/>
<g font-family="sans-serif" font-size="2.5" fill="black" stroke="none">{quarters}{note_text}</g>
</g>
</svg>
"""


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--od", type=float, required=True, help="OD of the tube being cut")
    p.add_argument("--wall", type=float, required=True, help="wall of the tube being cut")
    p.add_argument("--header-od", type=float, required=True, help="OD of the tube it lands on")
    p.add_argument("--angle", type=float, default=90, help="angle between centerlines, degrees")
    p.add_argument("--offset", type=float, default=0, help="distance between centerlines")
    p.add_argument("--kerf", type=float, default=0.06, help="kerf width")
    p.add_argument("--feed", type=float, default=100, help="cut speed, units/min")
    p.add_argument("--lead-in", type=float, default=0.2)
    p.add_argument("--units", choices=["in", "mm"], default="in")
    p.add_argument("--out", default="cope", help="output file stem")
    a = p.parse_args()

    title = (f"cope {a.od}x{a.wall} onto {a.header_od} OD at {a.angle} deg, "
             f"offset {a.offset}, kerf {a.kerf} [{a.units}]")
    profile = cope_profile(a.od, a.wall, a.header_od, a.angle, a.offset)
    with open(a.out + ".ngc", "w") as f:
        f.write(gcode(profile, a.od, a.feed, a.kerf, a.lead_in, a.units, title))
    with open(a.out + ".svg", "w") as f:
        f.write(svg_template(profile, a.od, a.units, title))
    xs = [x for _, x in profile]
    print(f"{title}\ncope depth {max(xs) - min(xs):.4f}; long point is {min(xs):.4f} from the header "
          f"centerline (measured along the tube)\nwrote {a.out}.ngc, {a.out}.svg")


if __name__ == "__main__":
    main()
