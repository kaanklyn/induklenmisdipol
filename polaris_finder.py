import math
import numpy as np

def calculate_isolation_score(star, all_stars, image_height):
    """
    Yıldızın ne kadar izole olduğunu hesaplar.
    Polaris genelde etrafında az yıldız olan bölgededir.
    
    Args:
        star: (x, y, brightness) tuple
        all_stars: Tüm yıldızlar listesi
        image_height: Görüntü yüksekliği
        
    Returns:
        İzolasyon skoru (0-1 arası)
    """
    distances = []
    
    for other_star in all_stars:
        if star != other_star:
            dx = star[0] - other_star[0]
            dy = star[1] - other_star[1]
            d = math.hypot(dx, dy)
            distances.append(d)
    
    if len(distances) < 5:
        # Yeterince komşu yoksa, sınırlı olanların ortalamasını al
        avg_dist = np.mean(distances) if distances else 0
    else:
        # En yakın 5 komşunun ortalamasını al
        distances.sort()
        avg_dist = np.mean(distances[:5])
    
    # Normalize et (max beklenen mesafe = diyagonal)
    max_possible_dist = math.hypot(image_height, image_height)
    iso_score = min(avg_dist / max_possible_dist, 1.0)
    
    return iso_score


def find_polaris(stars, image_shape, top_candidates=30):
    """
    Polaris'i bulmak için akıllı algoritma.
    
    Polaris özellikleri:
    - Gökyüzünün üst kısmında (merkez+üzeri)
    - Oldukça parlak ama aşırı parlak değil
    - Etrafında yoğun yıldız kümesi yok (izole)
    
    Args:
        stars: [(x, y, brightness), ...] listesi
        image_shape: (height, width) 
        top_candidates: Kaç tane parlak yıldız incelenecek
        
    Returns:
        polaris: (x, y, brightness) tuple
        score: Seçim skoru
        debug_info: Debug bilgileri
    """
    
    height = image_shape[0]
    width = image_shape[1]
    
    # En parlak yıldızları al
    if len(stars) > top_candidates:
        sorted_stars = sorted(stars, key=lambda x: -x[2])[:top_candidates]
    else:
        sorted_stars = stars
    
    best_star = None
    best_score = -1
    scores_debug = []
    
    for star in sorted_stars:
        x, y, brightness = star
        
        # 1. Yukarıda olma skoru (Polaris üst kısmda)
        # Merkez alıntı: merkez üstündeki yıldızlar daha yüksek skor
        center_y = height / 2
        vertical_position = (center_y - y) / height  # Negatif = aşağıda, pozitif = yukarıda
        # Normalize et (0-1)
        height_score = max(0, vertical_position + 0.5)  # Offset ile merkez altı da kabul et
        height_score = min(height_score, 1.0)
        
        # 2. Parlaklık skoru (normalize)
        brightness_score = brightness / 255.0
        brightness_score = min(brightness_score, 1.0)
        
        # 3. İzolasyon skoru
        iso_score = calculate_isolation_score(star, sorted_stars, height)
        
        # Ağırlıklı skorla
        # Ağırlıklar: yukarıda olma(0.4), parlaklık(0.3), izolasyon(0.3)
        total_score = (0.4 * height_score) + (0.3 * brightness_score) + (0.3 * iso_score)
        
        scores_debug.append({
            'star': star,
            'height_score': height_score,
            'brightness_score': brightness_score,
            'iso_score': iso_score,
            'total_score': total_score
        })
        
        if total_score > best_score:
            best_score = total_score
            best_star = star
    
    debug_info = {
        'total_candidates': len(sorted_stars),
        'scores': scores_debug,
        'best_score': best_score
    }
    
    return best_star, best_score, debug_info
