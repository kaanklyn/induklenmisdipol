#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kutup Navigasyon Sistemi - Ana Program

Gökyüzü fotoğrafından Polaris'i tespit ederek enlem hesaplar.

Kullanım:
    python main.py sky.jpg --fov 60
    python main.py sky.jpg --fov 55 --debug
"""

import sys
import argparse
import math
from pathlib import Path

from star_detection import detect_stars
from polaris_finder import find_polaris
from latitude_solver import calculate_latitude_with_error_bounds
from compass import CompassSensor
from map_viewer import TurkiyeMap
from constellation_locator import detect_constellation_and_latitude


def print_header():
    print("\n" + "="*60)
    print("🌌 KUTUP NAVIGASYON SİSTEMİ - POLARIS ENLEMİ HESAPLAYICI 🌌")
    print("="*60 + "\n")


def print_results(polaris, latitude_data, debug_info, image_shape, vertical_fov, compass=None):
    """Sonuçları düzgün formatta yazdır"""
    
    # Pusula uyarısı
    if compass is not None and not compass.is_facing_north():
        print("\n⚠️ PUSULA UYARISI")
        print("-" * 60)
        print(f"Telefon kuzeye bakmiyor!")
        print(f"   Mevcut Yön: {compass.get_cardinal_direction()}")
        print(f"   Sapma: {compass.get_deviation_from_north():.1f}° " + 
              ("(batı)" if compass.get_deviation_from_north() > 0 else "(doğu)"))
        print(f"Enlem hesaplaması etkilenebilir. Lütfen kuzeye çevirin.")
        print()
    
    print("📊 SONUÇLAR")
    print("-" * 60)
    print(f"Tahmini Enlem:        {latitude_data['latitude']}°")
    print(f"Hata Payı:            ±{latitude_data['error_margin']}°")
    print(f"Aralık:               {latitude_data['lower_bound']}° → {latitude_data['upper_bound']}°")
    print(f"Polaris Yüksekliği:   {latitude_data['altitude']}°")
    print()
    
    print("🔍 POLARIS KONUMU")
    print("-" * 60)
    print(f"X (Yatay):            {polaris[0]:.1f} piksel")
    print(f"Y (Dikey):            {polaris[1]:.1f} piksel")
    print(f"Parlaklık:            {polaris[2]:.1f}")
    print()
    
    # Pusula bilgisi
    if compass is not None:
        print("🧭 PUSULA BİLGİSİ")
        print("-" * 60)
        print(f"Azimuth:              {compass.get_azimuth():.1f}°")
        print(f"Yön:                  {compass.get_cardinal_direction()}")
        print(f"Kuzeye Sapma:         {compass.get_deviation_from_north():.1f}°")
        facing = "Evet ✓" if compass.is_facing_north() else "Hayır ✗"
        print(f"Kuzeye Bakıyor mu:    {facing}")
        print()
    
    print("📸 GÖRÜNTÜ BİLGİSİ")
    print("-" * 60)
    print(f"Görüntü Boyutu:       {image_shape[1]}x{image_shape[0]} piksel")
    print(f"Dikey FOV:            {vertical_fov}°")
    print(f"Toplam Yıldız:        {debug_info['total_stars']} (tespit edilen)")
    print()


def print_debug_info(debug_info, polaris_info):
    """Debug bilgileri yazdır"""
    
    print("🔧 DEBUG BİLGİLERİ")
    print("-" * 60)
    print(f"Polaris Seçim Skoru:  {polaris_info['score']:.3f}")
    print(f"İncelenen Adaylar:    {polaris_info['candidates']}")
    print()
    
    # Top 5 adayı göster
    scores = polaris_info['scores']
    if scores:
        print("🎯 EN İYİ 5 ADAY")
        print("-" * 60)
        for i, score_info in enumerate(scores[:5], 1):
            star = score_info['star']
            total = score_info['total_score']
            height_s = score_info['height_score']
            bright_s = score_info['brightness_score']
            iso_s = score_info['iso_score']
            
            print(f"{i}. Skor: {total:.3f} | Yük: {height_s:.2f} | Par: {bright_s:.2f} | İzo: {iso_s:.2f}")
            print(f"   Konum: ({star[0]:.1f}, {star[1]:.1f})")


def main():
    # Argümanları parse et
    parser = argparse.ArgumentParser(
        description='Polaris tespit ederek enlem hesapla'
    )
    parser.add_argument('image', type=str, help='Gökyüzü fotoğrafı yolu')
    parser.add_argument('--fov', type=float, default=60, 
                       help='Kameranın dikey FOV değeri (derece, default: 60)')
    parser.add_argument('--debug', action='store_true', 
                       help='Detaylı debug çıktısı göster')
    parser.add_argument('--azimuth', type=float, default=0,
                       help='Pusula azimuth değeri (derece, 0=Kuzey, 90=Doğu)')
    parser.add_argument('--no-compass', action='store_true',
                       help='Pusula sensörü devre dışı bırak')
    parser.add_argument('--method', choices=['auto', 'constellation', 'polaris'], default='auto',
                       help='Enlem yöntemi: auto/constellation/polaris')
    
    args = parser.parse_args()
    
    image_path = args.image
    vertical_fov = args.fov
    show_debug = args.debug
    
    # Başlık
    print_header()
    
    # Pusula sensörünü başlat
    if not args.no_compass:
        compass = CompassSensor(mode="mock", azimuth=args.azimuth)
        compass_enabled = True
        
        print(f"🧭 Pusula Sensörü: AÇIK")
        print(f"   Azimuth: {compass.get_azimuth()}°")
        print(f"   Yön: {compass.get_cardinal_direction()}")
        print()
    else:
        compass = None
        compass_enabled = False
        print("🧭 Pusula Sensörü: KAPAL\n")
    
    # Görüntü yükü kontrol et
    if not Path(image_path).exists():
        print(f"❌ HATA: Dosya bulunamadı: {image_path}")
        sys.exit(1)
    
    print(f"📂 Yükleniyor: {image_path}")
    print(f"📐 Dikey FOV: {vertical_fov}°\n")
    
    try:
        # Yıldızları tespit et
        print("⭐ Yıldızlar tespit ediliyor...")
        stars, image_shape = detect_stars(image_path)
        print(f"   ✓ {len(stars)} yıldız tespit edildi\n")
        
        if len(stars) == 0:
            print("❌ HATA: Yıldız tespit edilemedi.")
            print("   Görüntü çok koyu veya gürültülü olabilir.")
            sys.exit(1)
        
        debug_info = {'total_stars': len(stars)}
        polaris_info = None

        latitude_data = None
        polaris = None

        # 1) Takımyıldız oran yöntemi (istenirse ya da auto)
        if args.method in ("auto", "constellation"):
            print("🧩 Takımyıldız oran eşleşmesi aranıyor (Küçük Ayı / Güney Haçı)...")
            latitude_data = detect_constellation_and_latitude(
                stars, image_shape, vertical_fov
            )
            if latitude_data is not None:
                print("   ✓ Takımyıldız eşleşmesi bulundu")
                print(f"   ✓ Takımyıldız: {latitude_data['constellation']}")
                print(f"   ✓ Yarımküre: {'Kuzey' if latitude_data['hemisphere']=='north' else 'Güney'}")
                print(f"   ✓ Güven: %{latitude_data['confidence']*100:.1f}\n")
                polaris = (
                    latitude_data['pole_proxy'][0],
                    latitude_data['pole_proxy'][1],
                    stars[0][2] if stars else 0,
                )
            elif args.method == "constellation":
                print("❌ HATA: Takımyıldız oran eşleşmesi bulunamadı.")
                print("   Farklı bir fotoğraf deneyin ya da --method auto/polaris kullanın.")
                sys.exit(1)

        # 2) Fallback: Polaris yöntemi
        if latitude_data is None:
            print("🔍 Polaris aranıyor...")
            polaris, score, polaris_debug = find_polaris(stars, image_shape)
            print(f"   ✓ Polaris bulundu\n")

            print("📐 Enlem hesaplanıyor...")
            latitude_data = calculate_latitude_with_error_bounds(
                polaris[1], image_shape[0], vertical_fov
            )
            print(f"   ✓ Enlem hesaplanması tamamlandı\n")

            polaris_info = {
                'score': score,
                'candidates': polaris_debug['total_candidates'],
                'scores': polaris_debug['scores']
            }

        print_results(polaris, latitude_data, debug_info, image_shape, vertical_fov, compass)

        if latitude_data.get('method') == 'constellation-ratio':
            print("🧩 TAKIMYILDIZ EŞLEŞME DETAYI")
            print("-" * 60)
            print(f"Yöntem:               Yıldızlar arası oran")
            print(f"Takımyıldız:          {latitude_data['constellation']}")
            print(f"Yarımküre:            {'Kuzey' if latitude_data['hemisphere']=='north' else 'Güney'}")
            print(f"Eşleşme skoru:        {latitude_data['score']}")
            print(f"Güven:                %{latitude_data['confidence']*100:.1f}")
            print()

        # Debug modu
        if show_debug and polaris_info is not None:
            print_debug_info(debug_info, polaris_info)
        
        # Harita oluştur
        print("\n🗺️  Harita hazırlanıyor...")
        map_handler = TurkiyeMap(output_path="enlem_haritasi.png")
        map_handler.plot_location(
            latitude=latitude_data['latitude'],
            error_margin=latitude_data['error_margin'],
            show_cities=True,
            title=f"Kutup Navigasyonu - Enlem: {latitude_data['latitude']}°"
        )
        
        # En yakın şehir
        nearest = map_handler.get_nearest_city(latitude_data['latitude'], latitude_data['error_margin'])
        print(f"📍 {nearest['message']}")
        
        print("=" * 60)
        print("✅ İşlem başarıyla tamamlandı!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"❌ HATA: {e}")
        if show_debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
