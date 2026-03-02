from constellation_locator import detect_constellation_and_latitude


def _scale_translate(points, scale=100, tx=500, ty=300, brightness=220):
    return [(x * scale + tx, y * scale + ty, brightness) for x, y in points]


def test_detect_umi_auto():
    umi = [(0.0, 0.0), (1.6, 0.3), (2.9, 0.9), (3.6, 1.7)]
    stars = _scale_translate(umi)
    stars += [(50, 700, 100), (900, 50, 90), (1000, 600, 80)]

    result = detect_constellation_and_latitude(stars, image_shape=(1080, 1920), vertical_fov=60)
    assert result is not None
    assert result["hemisphere"] == "north"
    assert result["constellation"] == "Küçük Ayı"


def test_detect_crux_auto():
    crux = [(0.0, 0.0), (0.0, 2.4), (-0.8, 1.2), (1.0, 1.1)]
    stars = _scale_translate(crux, scale=90, tx=700, ty=200)
    stars += [(50, 700, 100), (900, 50, 90), (1000, 600, 80)]

    result = detect_constellation_and_latitude(stars, image_shape=(1080, 1920), vertical_fov=60)
    assert result is not None
    assert result["hemisphere"] == "south"
    assert result["constellation"] == "Güney Haçı"


def test_auto_decides_by_best_ratio_match():
    umi = _scale_translate([(0.0, 0.0), (1.6, 0.3), (2.9, 0.9), (3.6, 1.7)], scale=100, tx=450, ty=240)
    crux_distorted = _scale_translate([(0.0, 0.0), (0.0, 2.4), (-0.8, 1.2), (1.0, 1.1)], scale=100, tx=900, ty=500)
    # Güney haçı grubunu bilinçli boz (oranı kötüleşsin)
    crux_distorted[2] = (crux_distorted[2][0] + 80, crux_distorted[2][1] + 120, crux_distorted[2][2])

    stars = umi + crux_distorted

    result = detect_constellation_and_latitude(stars, image_shape=(1080, 1920), vertical_fov=60)
    assert result is not None
    assert result["constellation"] == "Küçük Ayı"
    assert result["hemisphere"] == "north"
