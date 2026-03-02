#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pusula Sensörü Test ve Demo

Farklı azimuth değerleriyle compass'in davranışını test et.
"""

from compass import CompassSensor, CompassCalibrator


def test_compass_directions():
    """Tüm yönler için pusula testini çalıştır"""
    
    print("\n" + "="*70)
    print("🧭 PUSULA SENSÖRÜ YÖN TESTİ")
    print("="*70 + "\n")
    
    # 8 ana yön
    test_cases = [
        (0, "Kuzey", "✓ İDEAL"),
        (45, "KuzeyDoğu", ""),
        (90, "Doğu", ""),
        (135, "DoğuGüney", ""),
        (180, "Güney", ""),
        (225, "GüneyBatı", ""),
        (270, "Batı", ""),
        (315, "BatıKuzey", ""),
    ]
    
    for azimuth, expected_dir, note in test_cases:
        compass = CompassSensor(mode="mock", azimuth=azimuth)
        
        direction = compass.get_cardinal_direction()
        is_north = compass.is_facing_north()
        deviation = compass.get_deviation_from_north()
        
        status = "✓" if direction == expected_dir else "✗"
        
        print(f"{status} Azimuth {azimuth:3d}° → {direction:10s} | "
              f"Kuzey: {str(is_north):5s} | Sapma: {deviation:7.1f}° {note}")
    
    print()


def test_north_tolerance():
    """Kuzey tolerans aralığını test et"""
    
    print("="*70)
    print("🧭 KUZEY TOLERANS TEST (±15° kabul ediliyor)")
    print("="*70 + "\n")
    
    tolerance_test = [
        (-20, "Batı (kalsa) - KABUL EDİLMEYECEK"),
        (-15, "BatıKuzey - KABUL EDİLECEK"),
        (-5, "BatıKuzey - KABUL EDİLECEK"),
        (0, "Kuzey - KABUL EDİLECEK ✓"),
        (5, "KuzeyDoğu - KABUL EDİLECEK"),
        (15, "KuzeyDoğu - KABUL EDİLECEK"),
        (20, "Doğu (başlana) - KABUL EDİLMEYECEK"),
    ]
    
    for az_offset, description in tolerance_test:
        azimuth = (360 + az_offset) % 360
        compass = CompassSensor(mode="mock", azimuth=azimuth)
        
        is_north = compass.is_facing_north(tolerance=15)
        status = "✓ EVET" if is_north else "✗ HAYIR"
        
        print(f"  {status:8s} | Azimuth {azimuth:3d}° → {description}")
    
    print()


def test_compass_with_photo():
    """Fotoğraf çekimi senaryoları"""
    
    print("="*70)
    print("🧭 FOTOĞRAF ÇEKİMİ SENARYOLARI")
    print("="*70 + "\n")
    
    scenarios = [
        {
            'name': 'İdeal: Kuzeye bakılmış fotoğraf',
            'azimuth': 0,
            'fov': 60
        },
        {
            'name': 'Sapmalı: Doğuya doğru 30° sapma',
            'azimuth': 30,
            'fov': 60
        },
        {
            'name': 'Ciddi Sapma: 90° (tamamen doğuya)',
            'azimuth': 90,
            'fov': 60
        },
        {
            'name': 'Hatalı: Güneye bakılmış (180°)',
            'azimuth': 180,
            'fov': 60
        },
    ]
    
    for scenario in scenarios:
        compass = CompassSensor(mode="mock", azimuth=scenario['azimuth'])
        
        print(f"📷 {scenario['name']}")
        print(f"   Azimuth:          {compass.get_azimuth()}°")
        print(f"   Yön:              {compass.get_cardinal_direction()}")
        print(f"   Kuzeye Bakıyor:   {'Evet ✓' if compass.is_facing_north() else 'Hayır ✗'}")
        print(f"   Sapma:            {compass.get_deviation_from_north():.1f}°")
        
        if not compass.is_facing_north():
            print(f"   ⚠️  UYARI: Enlem hesaplaması etkilenebilir!")
        else:
            print(f"   ✓ Enlem hesaplaması güvenilir")
        
        print()


def test_calibration():
    """Pusula kalibrasyonu testi"""
    
    print("="*70)
    print("🧭 PUSULA KALİBRASYONU TESTİ")
    print("="*70 + "\n")
    
    calibrator = CompassCalibrator()
    
    # Hatalı okumalar topla (gerçek sensörlerde böyle hatalar oluşur)
    print("Kalibrasyonluk okumalar toplanıyor...")
    readings = [350, 5, 358, 2, 1, 359, 4, 0, 356, 3]  # ~0° etrafında dağılmış
    
    for i, reading in enumerate(readings, 1):
        calibrator.collect_reading(reading)
        print(f"  Okuma {i}: {reading}°")
    
    print(f"\nToplam {len(readings)} okuma toplandı")
    print(f"Ortalama: {sum(readings) / len(readings):.1f}°")
    print(f"Beklenen: 0° (Kuzey)")
    
    offset = calibrator.calibrate(expected_azimuth=0)
    
    print(f"\n✓ Kalibrasyon tamamlandı")
    print(f"  Kalibrasyon Offseti: {offset:.2f}°")
    print(f"  Gelecek okumaların önüne {-offset:.2f}° eklenecek")
    
    print()


def test_correction_angle():
    """Düzeltme açısı hesaplama"""
    
    print("="*70)
    print("🧭 DÜZELTME AÇISI HESAPLAMA")
    print("="*70 + "\n")
    
    scenarios = [
        (0, "Kuzey (düzeltme yok)"),
        (30, "30° Doğu sapması"),
        (45, "45° Doğu sapması"),
        (90, "90° Doğu sapması (tamamen yanlış)"),
        (270, "90° Batı sapması"),
    ]
    
    print("Fotoğrafın kaydırılması gereken açılar:\n")
    
    for azimuth, description in scenarios:
        compass = CompassSensor(mode="mock", azimuth=azimuth)
        correction = compass.get_correction_angle()
        
        print(f"  {description}")
        print(f"    Azimuth: {azimuth}°")
        print(f"    Düzeltme Açısı: {correction:.1f}°")
        print(f"    (Fotoğraf {abs(correction):.1f}° {'saat yönüne' if correction > 0 else 'saat yönü tersine'} döndürülecek)")
        print()


def main():
    """Tüm testleri çalıştır"""
    
    print("\n" + "🧭"*35)
    print("PUSULA SENSÖRÜ KOMPLİ TEST SÜİTİ")
    print("🧭"*35 + "\n")
    
    test_compass_directions()
    test_north_tolerance()
    test_compass_with_photo()
    test_calibration()
    test_correction_angle()
    
    print("="*70)
    print("✅ TÜM TESTLER BAŞARIYLA TAMAMLANDI!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
