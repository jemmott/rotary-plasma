import math

import pytest

from cope import cope_profile, gcode, kerf_offset, svg_template


def test_square_cope_matches_closed_form():
    # 90 degrees, no offset, thin wall: x = sqrt(R^2 - r^2 sin^2 phi)
    r, R = 1.0, 1.5
    for phi, x in cope_profile(2 * r, 1e-6, 2 * R, 90):
        assert x == pytest.approx(math.sqrt(R**2 - (r * math.sin(phi)) ** 2), abs=1e-5)


def test_outer_surface_never_inside_header():
    # Rebuild 3D points from an angled, offset cope and check them against the header cylinder.
    od, wall, D, angle, offset = 1.75, 0.12, 2.5, 55, 0.3
    r, R, th = od / 2, D / 2, math.radians(angle)
    for phi, x in cope_profile(od, wall, D, angle, offset):
        for rho in (r, r - wall):
            px = x * math.sin(th) + rho * math.cos(phi) * math.cos(th)
            py = offset + rho * math.sin(phi)
            assert math.hypot(px, py) >= R - 1e-9


def test_angle_is_symmetric():
    # A 60 degree cope is a 120 degree cope rotated half a turn.
    a = cope_profile(1.5, 0.1, 2.0, 60, n=360)
    b = cope_profile(1.5, 0.1, 2.0, 120, n=360)
    for i in range(360):
        assert a[i][1] == pytest.approx(b[(i + 180) % 360][1])


def test_kerf_offset_distance():
    od, kerf = 1.75, 0.06
    prof = cope_profile(od, 0.12, 1.75, 45, n=720)
    surface = [(od / 2 * phi, x) for phi, x in prof]
    for phi, x in kerf_offset(prof, od, kerf)[::40]:
        d = min(math.hypot(od / 2 * phi - s, x - xx) for s, xx in surface)
        assert d == pytest.approx(kerf / 2, abs=0.003)
        assert x < max(xx for _, xx in surface)


def test_rejects_branch_that_misses_header():
    with pytest.raises(ValueError):
        cope_profile(2.0, 0.1, 1.5, 90)
    with pytest.raises(ValueError):
        cope_profile(1.5, 0.1, 2.0, 90, offset=0.5)


def test_outputs():
    prof = cope_profile(1.75, 0.12, 1.75, 60)
    g = gcode(prof, 1.75, feed=100, kerf=0.06, lead_in=0.2)
    assert g.count("M3 $0 S1") == 1 and "G93" in g and g.strip().endswith("M2")
    a = [float(line.split("A")[1].split()[0]) for line in g.splitlines() if line.startswith("G1")]
    assert a[-1] - a[0] == pytest.approx(360)
    assert all(b - c < 2 for b, c in zip(a[1:], a))  # one steady turn, no jumps or unwinding
    f = [float(line.split("F")[1]) for line in g.splitlines() if line.startswith("G1")][1:]
    assert max(f) / min(f) < 2  # inverse-time feeds stay in a sane band
    svg = svg_template(prof, 1.75)
    assert f'width="{math.pi * 1.75 * 25.4:.3f}mm"' in svg
