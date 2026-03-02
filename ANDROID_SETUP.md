📱 ANDROID APP KURULUM KILAVUZU
================================

Telefonda çalışan Kutup Navigasyon Sistemi

## 👨‍💻 GEREKLI ARAÇLAR

1. **Android Studio** (Ücretsiz)
   - https://developer.android.com/studio
   - 4 GB RAM minimum
   - 8 GB disk alan

2. **Kotlin Bilgisi** 
   - Temel Android bilgisi yeterli
   - Örnek kodları sağlıyoruz

## 🏗️ PROJE MİMARİSİ

```
kutup_navigasyon_android/
│
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── AndroidManifest.xml
│   │   │   ├── res/
│   │   │   │   ├── layout/
│   │   │   │   │   └── activity_main.xml
│   │   │   │   ├── values/
│   │   │   │   │   └── strings.xml
│   │   │   │   └── drawable/
│   │   │   └── java/com/kutup/
│   │   │       ├── MainActivity.kt
│   │   │       ├── StarDetector.kt
│   │   │       ├── PolarisFinder.kt
│   │   │       ├── LatitudeSolver.kt
│   │   │       └── CompassSensor.kt
│   │
│   ├── build.gradle.kts
│   └── proguard-rules.pro
│
├── build.gradle.kts
└── settings.gradle.kts

```

## 🔧 KOTLIN'E ÇEVRİLEN KODLAR

Tüm Python modülleri Kotlin'de yazılacak:

1. **StarDetector.kt** - Python'daki star_detection.py
2. **PolarisFinder.kt** - Python'daki polaris_finder.py
3. **LatitudeSolver.kt** - Python'daki latitude_solver.py
4. **CompassSensor.kt** - Python'daki compass.py

## 📱 ANDROID ÖZELLİKLERİ

✅ Kamera Erişimi
✅ Manyetik Alan Sensörü (Pusula)
✅ Ekran Görüntüleme
✅ Dosya Kaydetme
✅ İnternet Gereksiz (Tamamen Offline)

## 🌐 KULLANICI AKIŞI (UI)

```
┌─────────────────────────┐
│   Ana Ekran             │
├─────────────────────────┤
│ [📸 Foto Çek] Butonu    │
│                         │
│ Pusula Bilgisi:         │
│  Azimuth: 45°           │
│  Yön: KuzeyDoğu         │
│  Kuzeye Bakıyor: Hayır  │
│                         │
│ ⚠️  Kuzeye Yönlendir!   │
└─────────────────────────┘
        ↓ (fotoçekme)
┌─────────────────────────┐
│ İşleme Ekranı           │
│                         │
│ ⏳ Yıldızlar tespit...  │
│ ⏳ Polaris bulunuyor... │
│ ⏳ Enlem hesaplanıyor..│
└─────────────────────────┘
        ↓
┌─────────────────────────┐
│ Sonuçlar Ekranı         │
├─────────────────────────┤
│ ENLEM: 40.25°           │
│ HATA PAYI: ±1.5°        │
│                         │
│ Polaris Konumu          │
│ Azimuth: 0°             │
│ Parlaklık: 185          │
│                         │
│ [🔄 Tekrar] [✓ Kaydet]  │
└─────────────────────────┘
```

## 💾 VERI DEPOLAMA

Offline çalışması için:

**1. Yıldız Kataloğu (SQLite)**
```sql
CREATE TABLE stars (
    id INTEGER PRIMARY KEY,
    ra REAL,           -- Right Ascension (0-24 saat)
    dec REAL,          -- Declination (-90 to 90 derece)
    magnitude REAL,    -- Parlaklık
    name TEXT          -- Yıldız adı
);

-- Sadece uydu gözle görülebilen ~9000 yıldız
-- Boyut: ~1-2 MB
```

**2. Kullanıcı Verileri (SharedPreferences)**
- Kamera FOV ayarı
- Kalibrasyon verileri
- Daha önceki konumlar

**3. Fotoğraflar (Dosya Sistemi)**
- Çekilen gökyüzü fotoğrafı
- Sonuç ekran görüntüsü

## 🔩 TEKNIK DETAYLAR

### Kütüphaneler

```gradle
dependencies {
    // Core Android
    implementation("androidx.core:core:1.10.1")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    
    // OpenCV (Görüntü İşleme)
    implementation("org.opencv:opencv-android:4.8.0")
    
    // Kotlin Coroutines (Arka plan işleri)
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.6.4")
    
    // SQLite (Veri tabanı)
    implementation("androidx.room:room-runtime:2.5.1")
    
    // Material Design (UI)
    implementation("com.google.android.material:material:1.9.0")
}
```

### Gerekli Permissions

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-feature android:name="android.hardware.camera" />
<uses-feature android:name="android.hardware.sensor.compass" />
```

## 🚀 KURULUM ADIMI

1. Android Studio indir ve kur
2. Proje dosyalarını aç
3. OpenCV SDK yükle (SDK Manager)
4. Emülatör veya fiziksel telefon bağla
5. Derle ve Çalıştır

## 📊 HANGİ TELEFON?

İdeal Özellikler:
- Android 8.0+ (API 26+)
- Geniş açı kamera (50-70° FOV)
- Manyetik alan sensörü
- 2-3 GB RAM minimum

Uyumlu Telefonlar:
- Samsung (Galaxy S serisi, A serisi)
- Xiaomi (Redmi, Poco)
- Motorola
- Google Pixel

## ⚠️ KISITLAMALAR

❌ İnternet gereksiz (Çalışır)
❌ GPS gereksiz (Çalışır)
❌ Çoklu dil (Türkçe yazılı)
⚠️ Aşırı parlak fotoğraf veya siyah gökyüzü
⚠️ Pusula kalibrasyonu (cihazdan cihaza farklı)

## 📈 İLERİ ÖZELLIKLER (Sonrası)

- [ ] Cloud senkronizasyonu (isteğe bağlı)
- [ ] İstatistik grafikleri
- [ ] Tarihçe kaydı
- [ ] Widget (sistem)
- [ ] iOS versiyonu

---

Sana Kotlin kodu hazırlamaya başlayabilirim.

İstersen:
✓ Android Studio projesi şablonu
✓ Tüm Kotlin dosyaları (StarDetector, PolarisFinder, vb.)
✓ UI Layout XML dosyaları
✓ Yıldız kataloğu (SQLite dump)

Hangisinden başlayalım?
