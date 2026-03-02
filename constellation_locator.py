import itertools
import math

from latitude_solver import pixel_to_degrees


def _pairwise_signature(points):
    """4 noktanın ölçekten bağımsız mesafe imzasını döndür."""
    dists = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dists.append(math.hypot(dx, dy))

    dists.sort()
    max_dist = dists[-1]
    if max_dist == 0:
        return None
    return [d / max_dist for d in dists]


# Küçük Ayı (UMI) ve Güney Haçı (CRUX) için yıldızlar arası oran şablonları.
# Not: Bunlar kabaca geometri temelli başlangıç şablonlarıdır.
_TEMPLATE_POINTS = {
    "UMI": [
        (0.0, 0.0),
        (1.6, 0.3),
        (2.9, 0.9),
        (3.6, 1.7),
    ],
    "CRUX": [
        (0.0, 0.0),
        (0.0, 2.4),
        (-0.8, 1.2),
        (1.0, 1.1),
    ],
}

CONSTELLATION_META = {
    "UMI": {"name_tr": "Küçük Ayı", "hemisphere": "north"},
    "CRUX": {"name_tr": "Güney Haçı", "hemisphere": "south"},
}

_TEMPLATE_SIGNATURES = {
    name: _pairwise_signature(points)
    for name, points in _TEMPLATE_POINTS.items()
}


def _signature_distance(sig_a, sig_b):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(sig_a, sig_b)) / len(sig_a))


def _select_pole_proxy(stars4, constellation_name):
    """
    Eşleşen 4 yıldızdan kutup için vekil bir piksel noktası seç.
    """
    if constellation_name == "UMI":
        # Küçük Ayı için üstteki (en küçük y) yıldızı kutup vekili al.
        return min(stars4, key=lambda s: s[1])

    # Güney Haçı için: uzun ekseni bulup onu aşağı doğru uzat.
    farthest_pair = None
    farthest_dist = -1
    for a, b in itertools.combinations(stars4, 2):
        d = math.hypot(a[0] - b[0], a[1] - b[1])
        if d > farthest_dist:
            farthest_dist = d
            farthest_pair = (a, b)

    a, b = farthest_pair
    lower, upper = (a, b) if a[1] > b[1] else (b, a)
    vx = lower[0] - upper[0]
    vy = lower[1] - upper[1]

    factor = 4.5
    proxy_x = lower[0] + vx * factor
    proxy_y = lower[1] + vy * factor
    return (proxy_x, proxy_y, lower[2])


def detect_constellation_and_latitude(
    stars,
    image_shape,
    vertical_fov,
    top_candidates=25,
    tolerance=0.12,
):
    """Yıldızlar arasındaki oranlardan otomatik takımyıldız tespit et, kaba enlem döndür."""
    if len(stars) < 4:
        return None

    candidate_stars = sorted(stars, key=lambda x: -x[2])[:top_candidates]
    if len(candidate_stars) < 4:
        return None

    allowed_constellations = ["UMI", "CRUX"]

    best = None
    for combo in itertools.combinations(candidate_stars, 4):
        points = [(s[0], s[1]) for s in combo]
        sig = _pairwise_signature(points)
        if sig is None:
            continue

        for constellation_key in allowed_constellations:
            tpl_sig = _TEMPLATE_SIGNATURES[constellation_key]
            score = _signature_distance(sig, tpl_sig)
            if best is None or score < best["score"]:
                best = {
                    "score": score,
                    "constellation": constellation_key,
                    "stars": combo,
                }

    if best is None or best["score"] > tolerance:
        return None

    height = image_shape[0]
    center_y = height / 2

    pole_proxy = _select_pole_proxy(best["stars"], best["constellation"])
    pixel_offset = center_y - pole_proxy[1]
    altitude = pixel_to_degrees(pixel_offset, height, vertical_fov)

    meta = CONSTELLATION_META[best["constellation"]]
    hemisphere = meta["hemisphere"]

    latitude = abs(altitude)
    if hemisphere == "south":
        latitude = -latitude

    ratio_error = min(best["score"] * 20, 3.0)
    total_error = math.sqrt(ratio_error ** 2 + 2.0 ** 2)

    confidence = max(0.0, min(1.0, 1.0 - (best["score"] / tolerance)))

    return {
        "method": "constellation-ratio",
        "constellation": meta["name_tr"],
        "hemisphere": hemisphere,
        "latitude": round(latitude, 2),
        "lower_bound": round(latitude - total_error, 2),
        "upper_bound": round(latitude + total_error, 2),
        "error_margin": round(total_error, 2),
        "altitude": round(abs(altitude), 2),
        "score": round(best["score"], 4),
        "confidence": round(confidence, 3),
        "matched_stars": [tuple(map(float, s)) for s in best["stars"]],
        "pole_proxy": (round(pole_proxy[0], 2), round(pole_proxy[1], 2)),
    }
