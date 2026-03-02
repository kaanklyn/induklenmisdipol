#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android'e Kurulum Yardımcı Script
Kurulum öncesi kontrolleri yapar
"""

import os
import subprocess
import sys
from pathlib import Path


def check_adb():
    """ADB kurulu mu kontrol et"""
    try:
        result = subprocess.run(['adb', 'version'], capture_output=True, text=True)
        return True
    except:
        return False


def list_connected_devices():
    """Bağlı cihazları listele"""
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        return result.stdout
    except:
        return None


def find_apk():
    """APK dosyasını bul"""
    possible_paths = [
        Path("app/release/app-release.apk"),
        Path("app/release/app-debug.apk"),
        Path("app/build/outputs/apk/release/app-release.apk"),
        Path("app/build/outputs/apk/debug/app-debug.apk"),
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path.absolute())
    
    return None


def show_menu():
    """Ana menü göster"""
    print("\n" + "🚀"*35)
    print("📱 ANDROID'E KURULUM YARDIMCISI")
    print("🚀"*35 + "\n")
    
    print("Hangi yöntemi kullanmak istiyorsun?\n")
    print("1️⃣  Android Studio'dan Doğrudan Kur")
    print("   → Telefon USB'de bağlı olmalı")
    print("   → Tercih: Android Studio açık olmalı")
    print()
    print("2️⃣  APK Dosyası Oluştur")
    print("   → Build yapacak")
    print("   → Release APK'sı hazırlayacak")
    print()
    print("3️⃣  Bağlı Cihazları Kontrol Et")
    print("   → ADB'nin çalışıp çalışmadığını kontrol et")
    print()
    print("4️⃣  APK'yı ADB ile Kur")
    print("   → Mevcut APK'yı telefona yükle")
    print()
    print("5️⃣  Kurulum Rehberi Göster")
    print("   → Detaylı adımları oku")
    print()
    print("0️⃣  Çıkış\n")


def method_1():
    """Method 1: Android Studio'dan çalıştır"""
    print("\n" + "="*70)
    print("1️⃣  ANDROID STUDIO'DAN DOĞRUDAN KURULUM")
    print("="*70 + "\n")
    
    print("""
✓ Gerekli:
  - Android Studio açık
  - Telefon USB'ye bağlı
  - USB Debug: ON
  
✓ Adımlar:

1. Android Studio'da proje açık olmalı
2. Telefonu USB ile bağla
3. Telefonda "Trust" seç
4. Android Studio'da: Run → Run 'app'
   (Veya: ⇧Ctrl+F10 Windows, ⌘R Mac)

5. İşlemi izle:
   - Derliyor... (30-60 sn)
   - Yüklüyor... (10-20 sn)
   - Başlatıyor...
   
6. Telefonda uygulama açılacak! ✅

💡 İpucu:
   - İlk sefer biraz uzun sürer
   - 2. sefer çok hızlı olur
   - Sorun olursa: Build → Clean Project
    """)


def method_2():
    """Method 2: APK oluştur"""
    print("\n" + "="*70)
    print("2️⃣  APK DOSYASI OLUŞTUR")
    print("="*70 + "\n")
    
    print("""
✓ Bu method:
  - Kurulaştırılmış APK dosyası oluşturur
  - Arkadaşlara göndermeye uygun
  - Manual kurulum için hazırlar

✓ Adımlar:

Android Studio'da:
  1. Build → Generate Signed Bundle/APK
  2. APK seçerek Next'e tıkla
  3. Keystore oluştur (ilk sefer):
     - Path: C:\\Users\\retya\\kutup.jks
     - Password: Güvenli şifre
  4. Key Alias: kutup_key
  5. Next → Release seçerek Finish

Tamamlandıktan sonra:
  - Pencerede "locate" link'ine tıkla
  - Veya manual: app/release/app-release.apk

Dosya hazır olunca:
  → Telefona USB ile transfer et
  → Telefonun Dosyalar uygulamasında aç
  → "Kurulum" butonu tıkla ✅

📦 Dosya Boyutu: ~60 MB
    """)


def method_3():
    """Method 3: Cihazları kontrol et"""
    print("\n" + "="*70)
    print("3️⃣  BAĞLI CİHAZLARI KONTROL ET")
    print("="*70 + "\n")
    
    if not check_adb():
        print("❌ ADB yüklü değil!")
        print("\nAndroid SDK Platform Tools'ı kur:")
        print("  1. Android Studio → SDK Manager")
        print("  2. SDK Platform Tools seçerek indir")
        print("  3. Bilgisayarı restart et")
        return
    
    print("✓ ADB kurulu!\n")
    
    devices = list_connected_devices()
    if devices:
        print("📱 Bağlı Cihazlar:")
        print(devices)
    
    if "device" not in devices.lower():
        print("\n⚠️  Hiç cihaz görünmüyor!")
        print("\nKontrol et:")
        print("  1. USB kablosu bağlı mı?")
        print("  2. Telefon USB Debug modu açık mı?")
        print("     (Settings → Developer Options → USB Debugging)")
        print("  3. Telefonda USB'ye güven ver (Trust) mi?")
        print("  4. Bilgisayarı restart et")
    else:
        print("\n✅ Kurulum için hazır!")


def method_4():
    """Method 4: ADB ile kur"""
    print("\n" + "="*70)
    print("4️⃣  ADB İLE KURULUM")
    print("="*70 + "\n")
    
    # APK bul
    apk_path = find_apk()
    
    if not apk_path:
        print("❌ APK dosyası bulunamadı!")
        print("\nÖnce: Method 2 (APK Oluştur) çalıştır")
        return
    
    print(f"✓ APK Bulundu: {apk_path}\n")
    
    if check_adb():
        print("✓ ADB Kurulu\n")
        
        print("Komutu çalıştırmak için:")
        print(f"\nadb install -r \"{apk_path}\"\n")
        
        sorun = input("Şimdi çalıştırsın mı? (e/h): ").lower()
        
        if sorun == 'e':
            print("\nKurulum başlıyor...\n")
            result = subprocess.run(
                ['adb', 'install', '-r', apk_path],
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            if result.returncode == 0:
                print("\n✅ Başarılı! Uygulama telefonda.")
            else:
                print(f"\n❌ Hata:\n{result.stderr}")
    else:
        print("❌ ADB yüklü değil!")
        print("Kurulum için: Method 1 veya Method 2 kullan")


def method_5():
    """Method 5: Rehber göster"""
    print("\n" + "="*70)
    print("5️⃣  KURULUM REHBERİ")
    print("="*70 + "\n")
    
    rehber_file = Path("TELEFONA_YUKLE.md")
    if rehber_file.exists():
        with open(rehber_file, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("📄 TELEFONA_YUKLE.md dosyası yok!")
        print("Tekrar dene veya método 1-4 kullan")


def main():
    while True:
        show_menu()
        
        choice = input("Seçim (0-5): ").strip()
        
        if choice == '1':
            method_1()
        elif choice == '2':
            method_2()
        elif choice == '3':
            method_3()
        elif choice == '4':
            method_4()
        elif choice == '5':
            method_5()
        elif choice == '0':
            print("\n👋 Hoşça kalın!\n")
            break
        else:
            print("\n❌ Geçersiz seçim! 0-5 arası seç.")
        
        input("\nDevam etmek için Enter'a bas...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Çıkıldı.\n")
        sys.exit(0)
