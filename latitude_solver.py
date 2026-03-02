import math

def pixel_to_degrees(pixel_offset, image_height, vertical_fov):
    """
    Piksel farkını dereceye çevirir.
    
    Args:
        pixel_offset: Merkez noktasından bu kadar piksel uzak
        image_height: Görüntü yüksekliği (piksel)
        vertical_fov: Kameranın dikey görüş alanı (derece)
        
    Returns:
        Derece olarak açı
    """
    degrees_per_pixel = vertical_fov / image_height
    degrees = pixel_offset * degrees_per_pixel
    return degrees


def calculate_latitude_from_polaris(polaris_pixel_y, image_height, vertical_fov):
    """
    Polaris'in piksel konumundan enlem hesapla.
    
    Mantık: Polaris'in ufuk üstündeki yüksekliği = bulunduğun enlem
    
    Args:
        polaris_pixel_y: Polaris'in Y piksel koordinatı (0 = üst)
        image_height: Görüntü yüksekliği
        vertical_fov: Dikey görüş alanı (derece)
        
    Returns:
        latitude: Tahmini enlem (derece)
        altitude: Polaris'in yüksekliği (derece)
    """
    
    # Merkez noktası
    center_y = image_height / 2
    
    # Merkez noktasından ne kadar uzak (piksel)
    pixel_offset = center_y - polaris_pixel_y
    
    # Dereceye çevir
    altitude = pixel_to_degrees(pixel_offset, image_height, vertical_fov)
    
    # Polaris yüksekliği ≈ enlem
    latitude = altitude
    
    return latitude, altitude


def calculate_latitude_with_error_bounds(polaris_pixel_y, image_height, vertical_fov, 
                                         fov_uncertainty=2, calibration_error=1):
    """
    Enlem hesapla ve hata sınırlarını da döndür.
    
    Hata kaynakları:
    - FOV ölçümü hataları
    - Kamera kalibrasyonu
    - Lens distorsiyonu
    
    Args:
        polaris_pixel_y: Polaris Y koordinatı
        image_height: Görüntü yüksekliği
        vertical_fov: Dikey FOV (nominal)
        fov_uncertainty: FOV ölçüm belirsizliği (derece)
        calibration_error: Kalibrasyon hatası (derece)
        
    Returns:
        result: {
            'latitude': hesaplanan enlem,
            'lower_bound': minimum enlem,
            'upper_bound': maksimum enlem,
            'error_margin': hata payı (±)
        }
    """
    
    latitude, altitude = calculate_latitude_from_polaris(
        polaris_pixel_y, image_height, vertical_fov
    )
    
    # FOV hatası etkisi
    lat_with_low_fov, _ = calculate_latitude_from_polaris(
        polaris_pixel_y, image_height, vertical_fov - fov_uncertainty
    )
    lat_with_high_fov, _ = calculate_latitude_from_polaris(
        polaris_pixel_y, image_height, vertical_fov + fov_uncertainty
    )
    
    # Hata sınırları
    fov_error = max(abs(lat_with_low_fov - latitude), abs(lat_with_high_fov - latitude))
    total_error = math.sqrt(fov_error**2 + calibration_error**2)
    
    result = {
        'latitude': round(latitude, 2),
        'lower_bound': round(latitude - total_error, 2),
        'upper_bound': round(latitude + total_error, 2),
        'error_margin': round(total_error, 2),
        'altitude': round(altitude, 2)
    }
    
    return result
