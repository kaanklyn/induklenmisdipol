#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performans Testi Çalıştır
"""

from performance_analyzer import PerformanceAnalyzer


def main():
    analyzer = PerformanceAnalyzer()
    
    print("\n" + "🕐"*40)
    print("📊 KUTUP NAVIGASYON - PERFORMANS TEST")
    print("🕐"*40 + "\n")
    
    # Senaryo 1: Standart
    print("SENARYO 1: Standart Koşullar (200 yıldız)")
    print("-" * 70)
    
    for platform in ['python', 'android', 'ios']:
        time_result = analyzer.get_total_time(platform, star_count=200)
        print(f"  {platform.upper():10s}: {analyzer.format_time(time_result)}")
    
    print()
    
    # Senaryo 2: Hızlı (100 yıldız, harita yok)
    print("SENARYO 2: Hızlı Mod (100 yıldız, harita yok - Python)")
    print("-" * 70)
    time_result = analyzer.get_total_time('python', star_count=100, with_map=False)
    print(f"  Python: {analyzer.format_time(time_result)}")
    print()
    
    # Senaryo 3: Cihaz karşılaştırması
    print("SENARYO 3: Android Cihaz Karşılaştırması (200 yıldız)")
    print("-" * 70)
    
    devices = {
        'high_end': 'Yeni Telefon (Snapdragon 8 Gen 3)',
        'mid_range': 'Orta Model (Snapdragon 7 Gen 1)',
        'budget': 'Düşük Fiyat (MediaTek Helio G85)'
    }
    
    for device_key, device_name in devices.items():
        time_result = analyzer.get_total_time('android', star_count=200, device=device_key)
        print(f"  {device_name:40s}: {analyzer.format_time(time_result)}")
    
    print()
    
    # Senaryo 4: Yıldız sayısı etkisi
    print("SENARYO 4: Yıldız Sayısı Etkisi (Android, orta model)")
    print("-" * 70)
    
    for star_count in [100, 200, 300, 500]:
        time_result = analyzer.get_total_time('android', star_count=star_count)
        print(f"  {star_count} yıldız: {analyzer.format_time(time_result)}")
    
    print()
    
    # Senaryo 5: Detaylı breakdown
    print("SENARYO 5: Detaylı Zaman Dağılımı (Python, 200 yıldız)")
    print("-" * 70)
    analyzer.detailed_breakdown('python', 'mid_range', 200)
    print()
    
    # Senaryo 6: Platform karşılaştırması
    print("SENARYO 6: Platform Karşılaştırması")
    print("-" * 70)
    analyzer.comparison_table()


if __name__ == "__main__":
    main()
