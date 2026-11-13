import math

import plates


def holes(plate, d):
    return [(x, y) for x, y, dia in plate["circles"] if dia == d]


def test_adapter_matches_chuck_and_ring():
    p = plates.adapter_plate()
    m12 = holes(p, plates.M12_CLEARANCE)
    m8 = holes(p, plates.M8_TAP)
    assert len(m12) == 3 and len(m8) == 8
    assert all(math.isclose(math.hypot(x, y), 113) for x, y in m12)
    assert all(math.isclose(math.hypot(x, y), 90) for x, y in m8)
    # adjacent chuck holes: the owner measured 7 3/4 in (197 mm) with a tape
    assert abs(math.dist(m12[0], m12[1]) - 7.75 * 25.4) < 2


def test_no_holes_overlap():
    for make in plates.PLATES:
        small = [c for c in make()["circles"] if c[2] < 60]
        for i, (x1, y1, d1) in enumerate(small):
            for x2, y2, d2 in small[i + 1 :]:
                assert math.dist((x1, y1), (x2, y2)) > (d1 + d2) / 2 + 3


def test_frame_and_spacer_share_the_inner_ring_pattern():
    f = holes(plates.frame_plate(), plates.M8_CLEARANCE)
    s = holes(plates.spacer_ring(), plates.M8_CLEARANCE)
    assert f == s and len(f) == 8


def test_dxf_has_every_entity():
    p = plates.frame_plate()
    dxf = plates.to_dxf(p)
    assert dxf.count("CIRCLE") == len(p["circles"])
    assert dxf.count("LINE") == 4
    assert dxf.endswith("EOF\n")
