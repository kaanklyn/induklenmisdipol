#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harita Modülü - Enlem/Boylam Gösterimi

Türkiye haritasında bulunduğunuz konumu gösterir.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle
import numpy as np
from pathlib import Path


class TurkiyeMap:
    """Türkiye haritası ve koordinat gösterimi"""
    
    # Türkiye'nin yaklaşık sınırları
    TURKEY_BOUNDS = {
        'north': 42.0,
        'south': 36.0,
        'east': 45.0,
        'west': 26.0
    }
    
    # Önemli şehirler
    CITIES = {
        'İstanbul': (41.0, 28.97),
        'Ankara': (39.93, 32.86),
        'İzmir': (38.41, 27.13),
        'Antalya': (36.88, 30.70),
        'Adana': (36.99, 35.31),
        'Gaziantep': (37.07, 37.38),
        'Diyarbakır': (37.92, 40.23),
        'Van': (38.63, 43.38),
        'Trabzon': (40.98, 39.72),
        'Rize': (41.20, 40.51),
    }
    
    def __init__(self, output_path: str = "map_result.png"):
        self.output_path = output_path
    
    def plot_location(self, latitude: float, error_margin: float = 1.0, 
                     show_cities: bool = True, title: str = "Kutup Navigasyon Sonucu"):
        """
        Harita üzerinde konumu göster
        
        Args:
            latitude: Hesaplanan enlem
            error_margin: Hata payı (derece)
            show_cities: Şehirleri goster mi?
            title: Grafik başlığı
        """
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Harita arka planı (açık mavi = su)
        ax.set_facecolor('#E3F2FD')
        
        # Türkiye sınırları (basit rectangle)
        turkey = patches.Rectangle(
            (self.TURKEY_BOUNDS['west'], self.TURKEY_BOUNDS['south']),
            self.TURKEY_BOUNDS['east'] - self.TURKEY_BOUNDS['west'],
            self.TURKEY_BOUNDS['north'] - self.TURKEY_BOUNDS['south'],
            linewidth=2,
            edgecolor='black',
            facecolor='#C8E6C9',
            alpha=0.7
        )
        ax.add_patch(turkey)
        
        # Enlem çizgileri (paraleller)
        for lat in range(36, 43):
            ax.axhline(y=lat, color='gray', linestyle='--', alpha=0.3, linewidth=0.5)
            ax.text(self.TURKEY_BOUNDS['west'] - 1, lat, f'{lat}°', fontsize=9)
        
        # Boylam çizgileri (meridienler)
        for lon in range(26, 46, 2):
            ax.axvline(x=lon, color='gray', linestyle='--', alpha=0.3, linewidth=0.5)
            ax.text(lon, self.TURKEY_BOUNDS['south'] - 0.5, f'{lon}°', fontsize=9)
        
        # Enlem bantı (hata payı çizgisi)
        lat_lower = latitude - error_margin
        lat_upper = latitude + error_margin
        
        ax.axhline(y=latitude, color='red', linestyle='-', linewidth=3, 
                  label=f'Bulunan Enlem: {latitude:.2f}°', zorder=5)
        
        ax.fill_between(
            [self.TURKEY_BOUNDS['west'], self.TURKEY_BOUNDS['east']],
            lat_lower, lat_upper,
            color='red', alpha=0.2, label=f'Hata Payı: ±{error_margin:.1f}°'
        )
        
        # Şehirleri göster
        if show_cities:
            for city, (lat, lon) in self.CITIES.items():
                ax.plot(lon, lat, 'bo', markersize=6)
                ax.text(lon + 0.3, lat + 0.2, city, fontsize=8)
        
        # Eksen ayarları
        ax.set_xlim(self.TURKEY_BOUNDS['west'] - 2, self.TURKEY_BOUNDS['east'] + 2)
        ax.set_ylim(self.TURKEY_BOUNDS['south'] - 1, self.TURKEY_BOUNDS['north'] + 1)
        
        ax.set_xlabel('Boylam (°)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Enlem (°)', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        ax.legend(loc='upper left', fontsize=11)
        ax.grid(True, alpha=0.2)
        
        # Kaydet
        plt.tight_layout()
        plt.savefig(self.output_path, dpi=150, bbox_inches='tight')
        print(f"\n✓ Harita kaydedildi: {self.output_path}")
        
        plt.show()
    
    def plot_observation_history(self, observations: list, title: str = "Gözlem Geçmişi"):
        """
        Birden fazla gözlemi harita üzerinde göster
        
        Args:
            observations: [{'latitude': 40.5, 'error': 1.0, 'timestamp': '10:15'}, ...]
            title: Grafik başlığı
        """
        
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_facecolor('#E3F2FD')
        
        # Türkiye
        turkey = patches.Rectangle(
            (self.TURKEY_BOUNDS['west'], self.TURKEY_BOUNDS['south']),
            self.TURKEY_BOUNDS['east'] - self.TURKEY_BOUNDS['west'],
            self.TURKEY_BOUNDS['north'] - self.TURKEY_BOUNDS['south'],
            linewidth=2,
            edgecolor='black',
            facecolor='#C8E6C9',
            alpha=0.7
        )
        ax.add_patch(turkey)
        
        # Her gözlem için
        colors = plt.cm.rainbow(np.linspace(0, 1, len(observations)))
        
        for i, obs in enumerate(observations):
            lat = obs['latitude']
            error = obs.get('error', 1.0)
            label = obs.get('timestamp', f'Gözlem {i+1}')
            
            # Enlem çizgisi
            ax.axhline(y=lat, color=colors[i], linestyle='-', linewidth=2, alpha=0.7)
            
            # Hata payı
            ax.fill_between(
                [self.TURKEY_BOUNDS['west'], self.TURKEY_BOUNDS['east']],
                lat - error, lat + error,
                color=colors[i], alpha=0.15
            )
            
            # Etiket
            ax.text(self.TURKEY_BOUNDS['east'] + 0.5, lat, 
                   f'{label}: {lat:.2f}°', fontsize=10, color=colors[i], fontweight='bold')
        
        # Eksen
        ax.set_xlim(self.TURKEY_BOUNDS['west'] - 2, self.TURKEY_BOUNDS['east'] + 4)
        ax.set_ylim(self.TURKEY_BOUNDS['south'] - 1, self.TURKEY_BOUNDS['north'] + 1)
        
        ax.set_xlabel('Boylam (°)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Enlem (°)', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        ax.grid(True, alpha=0.2)
        
        plt.tight_layout()
        plt.savefig("observations_history.png", dpi=150, bbox_inches='tight')
        print(f"\n✓ Gözlem geçmişi kaydedildi: observations_history.png")
        
        plt.show()
    
    def get_nearest_city(self, latitude: float, error_margin: float) -> dict:
        """
        En yakın şehri bul
        
        Args:
            latitude: Bulunduğunuz enlem
            error_margin: Hata payı
            
        Returns:
            Bilgilendirici mesaj
        """
        
        nearest_city = None
        nearest_distance = float('inf')
        
        for city, (city_lat, city_lon) in self.CITIES.items():
            distance = abs(city_lat - latitude)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_city = city
        
        in_range = nearest_distance <= error_margin
        
        if nearest_city:
            return {
                'city': nearest_city,
                'distance': nearest_distance,
                'in_range': in_range,
                'message': f"{'✓ Yakında' if in_range else '⚠️ Yaklaşık'}: {nearest_city} "
                          f"({nearest_distance:.1f}° uzaklıkta)"
            }
        
        return {'message': 'Şehir bulunamadı'}


def demo_harita():
    """Harita sistemini test et"""
    
    print("\n" + "="*60)
    print("🗺️  HARITA GÖSTERIMI DEMO")
    print("="*60 + "\n")
    
    # Örnek konumlar
    locations = [
        {'latitude': 40.5, 'error': 1.5, 'timestamp': '10:15 - Polaris'},
        {'latitude': 41.0, 'error': 1.2, 'timestamp': '10:45 - Tekrar'},
        {'latitude': 39.9, 'error': 1.8, 'timestamp': '11:30 - 3. deneme'},
    ]
    
    map_handler = TurkiyeMap()
    
    # Tek konum göster
    print("📍 Tek Konum Gösterimi...")
    map_handler.plot_location(40.5, error_margin=1.5, title="Kutup Navigasyon - Tek Gözlem")
    
    # En yakın şehir
    result = map_handler.get_nearest_city(40.5, 1.5)
    print(f"\n{result['message']}")
    
    # Geçmiş göster
    print("\n📈 Gözlem Geçmişi Gösterimi...")
    map_handler.plot_observation_history(locations, title="3 Gözlem Karşılaştırması")


if __name__ == "__main__":
    demo_harita()
