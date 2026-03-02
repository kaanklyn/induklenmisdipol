#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telefon Pusula Sensörü Modülü

Manyetik alan sensöründen azimut (yön) bilgisini alır.
Mock ve gerçek mod destekler.

Azimut Sistemi:
  0° = Kuzey
  90° = Doğu
  180° = Güney
  270° = Batı
"""

import math
random_available = True
try:
    import random
except ImportError:
    random_available = False


class CompassSensor:
    """
    Telefon pusula sensörünü simüle eden sınıf.
    
    Gerçek uygulamada Android/iOS sensörüne bağlanır.
    Test için mock mod kullanabilir.
    """
    
    def __init__(self, mode="mock", azimuth=0.0):
        """
        Pusula sensörü başlat.
        
        Args:
            mode: 'mock' (simülasyon) veya 'sensor' (gerçek sensör)
            azimuth: Mock modda başlangıç azimuth (derece)
        """
        self.mode = mode
        self.azimuth = azimuth  # Derece cinsinden (0-360)
        self.noise = 0.0  # Sensör gürültüsü (derece)
        
    def get_azimuth(self, add_noise=False):
        """
        Mevcut azimuth değerini al.
        
        Args:
            add_noise: Gerçekçi gürültü ekle mi?
            
        Returns:
            azimuth: Derece cinsinden (0-360)
        """
        if self.mode == "mock":
            az = self.azimuth
        else:
            # Gerçek sensör kodu burada olacak
            # Android/iOS SDK çağrıları
            az = self.azimuth
        
        if add_noise and random_available:
            noise = random.gauss(0, 2)  # Standart sapma 2°
            az = (az + noise) % 360
        
        return az
    
    def set_azimuth(self, azimuth):
        """Mock modda azimutu ayarla (test için)"""
        self.azimuth = azimuth % 360
    
    def is_facing_north(self, tolerance=15):
        """
        Telefon kuzeye bakıyor mu?
        
        Args:
            tolerance: Kabul edilen sapma (derece)
            
        Returns:
            bool: True ise kuzeye bakıyor
        """
        az = self.get_azimuth()
        
        # Kuzey 0° etrafında
        # Örnek: 350°-10° aralığı kuzeye kabul edilir
        north_min = 360 - tolerance
        north_max = tolerance
        
        return az >= north_min or az <= north_max
    
    def get_cardinal_direction(self):
        """
        Azimuth'u ana yöne çevir.
        
        Returns:
            direction: 'Kuzey', 'KeuzeyDoğu', 'Doğu', vb.
        """
        az = self.get_azimuth()
        
        directions = [
            "Kuzey",
            "KuzeyDoğu",
            "Doğu",
            "DoğuGüney",
            "Güney",
            "GüneyBatı",
            "Batı",
            "BatıKuzey"
        ]
        
        # 8 ana yön, her biri 45°
        index = int((az + 22.5) / 45) % 8
        return directions[index]
    
    def get_deviation_from_north(self):
        """
        Kuzeye göre sapma açısını al.
        
        Returns:
            deviation: Negatif (batı sapması), pozitif (doğu sapması)
        """
        az = self.get_azimuth()
        
        # Kuzey 0° veya 360°'dir
        if az <= 180:
            deviation = az
        else:
            deviation = az - 360
        
        return deviation
    
    def get_correction_angle(self):
        """
        Fotoğrafta kuzeyi merkeze almak için gereken açı.
        
        Returns:
            angle: Rotate etmesi gereken açı (derece)
        """
        return -self.get_deviation_from_north()


class CompassCalibrator:
    """Pusula kalibrasyonu"""
    
    def __init__(self):
        self.readings = []
        self.expected_value = 0.0
    
    def collect_reading(self, azimuth):
        """Kalibrasyonluk okuma topla"""
        self.readings.append(azimuth)
    
    def calibrate(self, expected_azimuth=0):
        """
        Kalibrasyonu gerçekleştir.
        
        Args:
            expected_azimuth: Bilinen gerçek azimuth (derece)
            
        Returns:
            offset: Kalibrasyon ofset değeri
        """
        if not self.readings:
            return 0.0
        
        average = sum(self.readings) / len(self.readings)
        offset = expected_azimuth - average
        
        self.readings = []
        return offset


def test_compass():
    """Pusula sensörünü test et"""
    print("\n" + "="*60)
    print("🧭 PUSULA SENSÖRÜ TESTİ")
    print("="*60 + "\n")
    
    # Kuzeye bakan durumu test et
    compass_north = CompassSensor(mode="mock", azimuth=0)
    print("✓ Telefon KUZEYE bakıyor:")
    print(f"  Azimuth: {compass_north.get_azimuth()}°")
    print(f"  Yön: {compass_north.get_cardinal_direction()}")
    print(f"  Kuzeye bakıyor mu? {compass_north.is_facing_north()}")
    print(f"  Sapma: {compass_north.get_deviation_from_north()}°\n")
    
    # Doğuya bakan durumu test et
    compass_east = CompassSensor(mode="mock", azimuth=90)
    print("✓ Telefon DOĞUYA bakıyor:")
    print(f"  Azimuth: {compass_east.get_azimuth()}°")
    print(f"  Yön: {compass_east.get_cardinal_direction()}")
    print(f"  Kuzeye bakıyor mu? {compass_east.is_facing_north()}")
    print(f"  Sapma: {compass_east.get_deviation_from_north()}°\n")
    
    # Güneybatıya bakan durumu test et
    compass_sw = CompassSensor(mode="mock", azimuth=225)
    print("✓ Telefon GÜNEYBATIYA bakıyor:")
    print(f"  Azimuth: {compass_sw.get_azimuth()}°")
    print(f"  Yön: {compass_sw.get_cardinal_direction()}")
    print(f"  Kuzeye bakıyor mu? {compass_sw.is_facing_north()}")
    print(f"  Sapma: {compass_sw.get_deviation_from_north()}°\n")
    
    print("="*60)
    print("✅ Pusula Sensörü Çalışıyor!")
    print("="*60 + "\n")


if __name__ == "__main__":
    test_compass()
