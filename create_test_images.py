#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Örneği - Sanal Polaris Fotoğrafı Oluştur

Bu script, test amaçlı yapay bir gökyüzü görüntüsü oluşturur
ve sistemi denemenizi sağlar.
"""

import numpy as np
import cv2
import random
from pathlib import Path

def generate_test_sky(
    filename="test_sky.jpg",
    width=1080,
    height=1920,
    star_count=100,
    polaris_position="top_center",
    brightness_level=50
):
    """
    Test amaçlı yapay gökyüzü görüntüsü oluştur.
    
    Args:
        filename: Kaydedilecek dosya adı
        width: Genişlik (piksel)
        height: Yükseklik (piksel)
        star_count: Yıldız sayısı
        polaris_position: Polaris konumu ('top_center', 'top_left', 'top_right')
        brightness_level: Arka plan parlaklığı (0-100)
    """
    
    # Siyah arka plan (koyu gökyüzü)
    img = np.ones((height, width), dtype=np.uint8) * brightness_level
    
    # Random yıldızlar ekle
    for _ in range(star_count):
        x = random.randint(0, width - 1)
        y = random.randint(int(height * 0.3), height - 1)  # Alt 70% alanda
        brightness = random.randint(200, 255)
        size = random.randint(1, 3)
        
        # Yıldız çiz (Gaussian blob)
        cv2.circle(img, (x, y), size, brightness, -1)
        cv2.GaussianBlur(img, (5, 5), 0)
    
    # Polaris konumunu belirle
    center_x = width // 2
    if polaris_position == "top_center":
        polaris_x = center_x
        polaris_y = int(height * 0.2)
    elif polaris_position == "top_left":
        polaris_x = int(width * 0.3)
        polaris_y = int(height * 0.15)
    elif polaris_position == "top_right":
        polaris_x = int(width * 0.7)
        polaris_y = int(height * 0.15)
    else:
        polaris_x = center_x
        polaris_y = int(height * 0.2)
    
    # Polaris'i çiz (parlak ve izole)
    cv2.circle(img, (polaris_x, polaris_y), 4, 255, -1)
    
    # Etrafında az sayıda yıldız (izole hissi)
    for _ in range(3):
        offset_x = random.randint(-50, 50)
        offset_y = random.randint(-50, 50)
        x = polaris_x + offset_x
        y = polaris_y + offset_y
        if 0 <= x < width and 0 <= y < height:
            brightness = random.randint(150, 200)
            cv2.circle(img, (x, y), 2, brightness, -1)
    
    # Gaussian blur ile düzleştir (birçok teleskop görüntüsü böyle)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    
    # Kaydet
    cv2.imwrite(filename, img)
    
    return filename, (polaris_x, polaris_y)


def create_test_files():
    """Birkaç test görüntüsü oluştur"""
    
    print("🔧 Test görüntüleri oluşturuluyor...\n")
    
    # Test 1: Polaris merkez üst
    print("✓ test_sky_center.jpg oluşturuluyor...")
    create_file1, pos1 = generate_test_sky(
        "test_sky_center.jpg",
        polaris_position="top_center",
        star_count=80
    )
    print(f"  Polaris konumu (piksel): {pos1}\n")
    
    # Test 2: Polaris sol taraf
    print("✓ test_sky_left.jpg oluşturuluyor...")
    create_file2, pos2 = generate_test_sky(
        "test_sky_left.jpg",
        polaris_position="top_left",
        star_count=100
    )
    print(f"  Polaris konumu (piksel): {pos2}\n")
    
    # Test 3: Polaris sağ taraf
    print("✓ test_sky_right.jpg oluşturuluyor...")
    create_file3, pos3 = generate_test_sky(
        "test_sky_right.jpg",
        polaris_position="top_right",
        star_count=120
    )
    print(f"  Polaris konumu (piksel): {pos3}\n")
    
    print("="*60)
    print("✅ Test dosyaları oluşturuldu!")
    print("="*60)
    print("\nÇalıştırmak için:")
    print("  python main.py test_sky_center.jpg --fov 60")
    print("  python main.py test_sky_left.jpg --fov 60 --debug")
    print("  python main.py test_sky_right.jpg --fov 60 --debug")
    print()


if __name__ == "__main__":
    create_test_files()
