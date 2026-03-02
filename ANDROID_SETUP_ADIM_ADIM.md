# 📱 Android Studio'da Kurmak - Adım Adım Rehber

## ✅ Ön Koşullar

- **Android Studio** 2023.1+
- **Java 11+** 
- **Android SDK 34** (API Level 34)
- **Minimum telefon**: Android 8.0 (API 26)

---

## 1️⃣ Android Studio Kurulum

### Windows
1. https://developer.android.com/studio adresinden indir
2. Kurulumu çalıştır
3. "Android SDK", "Android Emulator" seçeneklerini işaretle
4. SDK Manager'dan API 26-34 arası indir

### Mac/Linux
```bash
# Homebrew ile (Mac)
brew install android-studio

# Manual (Linux)
# İndir: https://developer.android.com/studio
# Unzip ve çalıştır: ./studio.sh
```

---

## 2️⃣ Proje Strukturu Oluştur

### Klasör Yapısını Oluştur
```
kutup_navigasyon_android/
│
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── AndroidManifest.xml          ← Verildi
│   │       ├── java/
│   │       │   └── com/kutup/navigasyon/
│   │       │       ├── MainActivity.kt      ← Verildi
│   │       │       ├── CompassSensor.kt     ← Verildi
│   │       │       ├── StarDetector.kt      ← Verildi
│   │       │       ├── PolarisFinder.kt     ← Verildi
│   │       │       └── LatitudeSolver.kt    ← Verildi
│   │       └── res/
│   │           ├── layout/
│   │           │   └── activity_main.xml    ← Verildi
│   │           ├── values/
│   │           │   └── colors.xml
│   │           │   └── strings.xml
│   │           │   └── themes.xml
│   │           └── drawable/
│   │               └── button_background.xml
│   ├── build.gradle.kts                     ← Verildi
│   └── proguard-rules.pro
│
├── build.gradle.kts                         ← Verildi
└── settings.gradle.kts
```

---

## 3️⃣ Android Studio'da Yeni Proje Oluştur

### Adım 1: Proje Başlat
1. **File → New → New Project**
2. **Empty Activity** seç
3. **Proje Adı**: `kutup_navigasyon`
4. **Package**: `com.kutup.navigasyon`
5. **Language**: **Kotlin** (önemli!)
6. **Minimum SDK**: **API 26** (Android 8.0)

### Adım 2: Dosyaları Yerleştir
Yukarıda verilmiş olan `.kt` dosyalarını şu klasörlere kopyala:
```
app/src/main/java/com/kutup/navigasyon/
```

XML dosyalarını:
```
app/src/main/res/layout/activity_main.xml
```

Manifest:
```
app/src/main/AndroidManifest.xml
```

---

## 4️⃣ build.gradle.kts Güncelle

`app/build.gradle.kts` dosyasında verilmiş kodu kullan.

**Önemli**: CameraX ve OpenCV kütüphanelerinin versiyonlarını kontrol et.

---

## 5️⃣ Resource Dosyalarını Oluştur

### `res/values/colors.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="white">#FFFFFF</color>
    <color name="black">#000000</color>
    <color name="dark_gray">#303030</color>
    <color name="light_gray">#CCCCCC</color>
    <color name="primary_blue">#2196F3</color>
    <color name="secondary_blue">#1976D2</color>
</resources>
```

### `res/values/strings.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Kutup Navigasyon</string>
</resources>
```

### `res/values/themes.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.KutupNavigasyon" parent="Theme.AppCompat.DayNight">
        <item name="colorPrimary">@color/primary_blue</item>
        <item name="colorSecondary">@color/secondary_blue</item>
    </style>
</resources>
```

### `res/drawable/button_background.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/primary_blue" />
    <corners android:radius="8dp" />
</shape>
```

---

## 6️⃣ OpenCV SDK Entegrasyonu

### OpenCV Modülünü Ekle

1. **File → New → Import Module**
2. **Import .JAR/.AAR Package** seç
3. İndir: https://github.com/opencv/opencv/releases/download/4.8.0/opencv-android-sdk-4.8.0.zip
4. `opencv-android-sdk/sdk` klasörünü seç

### settings.gradle.kts Güncelle
```gradle
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "KutupNavigasyon"
include(":app")
include(":opencv-android-sdk")
```

---

## 7️⃣ Kütüphaneleri Senkronize Et

1. **File → Sync Now** (veya Gradle:Sync Now)
2. Android Studio indirecek:
   - OpenCV 4.8.0
   - CameraX 1.3.0
   - Kotlin Coroutines

<img src="https://via.placeholder.com/400x200?text=Sync+Gradle" />

---

## 8️⃣ Emülatör Kurma

### Virtual Device Oluştur
1. **Tools → Device Manager**
2. **Create Virtual Device**
3. **Pixel 4** seç
4. **API 34** seç
5. **Finish**

### Emülatörü Başlat
1. Device Manager'dan play butonu tıkla
2. Emülatör açılacak (İlk sefer 30-60 saniye sürebilir)

---

## 9️⃣ Derleme ve Çalıştırma

### Build Et
```
Build → Make Project
```

### Telefonda/Emülatörde Çalıştır
```
Run → Run 'app'
```

Telefon varsa:
1. **USB Debug Mode Aç** (Settings → Developer Options → USB Debugging)
2. USB kablosuyla bilgisayarına bağla
3. Android Studio otomatik tespit edecek
4. Run'a tıkla

---

## 🔟 Fiziksel Telefonda Test

### Gerekli Ayarlar
1. **Developer Options Aç**
   - Settings → About Phone
   - Build Number'a 7 kez tıkla
   
2. **USB Debugging Aç**
   - Developer Options → USB Debugging → ON
   
3. **USB Kablo Bağla**
   - "Trust this device" seç

4. **Run** tıkla

---

## ⚙️ APK Derleme (Dağıtım İçin)

### Release APK Oluştur
```
Build → Generate Signed Bundle/APK
```

1. **Yeni Keystore Oluştur** (İlk sefer)
   - Path: `~/.android/kutup.jks`
   - Password: Güvenli bir şifre koy
   
2. **APK** seç
3. **Release** build variant seç
4. **Finish**

APK şu konumda olacak:
```
app/release/app-release.apk
```

Bu dosyayı doğrudan telefona kopyalayabilirsin.

---

## 🐛 Sık Sorunlar

### "Build failed"
```
→ Build → Clean Project
→ Build → Rebuild Project
```

### "OpenCV not found"
```
→ File → Sync Now
→ File → Invalidate Caches → Restart
```

### "Permission denied"
```
→ AndroidManifest.xml dosyasında tüm izinleri kontrol et
→ Telefonda Settings → Apps → Kutup Navigasyon → Permissions
```

### "Emülatör çok yavaş"
```
→ Settings → VM acceleration'ı aç
→ Faster GPU rendering seç
```

---

## 📊 Proje Yapısı Özetle

| Dosya | Görev |
|-------|-------|
|`MainActivity.kt`|Ana uygulama, UI, kamera|
|`CompassSensor.kt`|Pusula sensörü (manyetik alan)|
|`StarDetector.kt`|OpenCV ile yıldız tespiti|
|`PolarisFinder.kt`|Akıllı Polaris seçimi|
|`LatitudeSolver.kt`|Enlem hesaplama|
|`activity_main.xml`|UI Layout (ekran tasarımı)|
|`AndroidManifest.xml`|Uygulama manifest (izinler)|
|`build.gradle.kts`|Kütüphane bağımlılıkları|

---

## ✅ Kontrol Listesi

- [ ] Android Studio 2023.1+ kurulu
- [ ] Kotlin dosyaları oluşturuldu
- [ ] XML resource dosyaları oluşturuldu
- [ ] OpenCV SDK entegre edildi
- [ ] Gradle senkronize edildi
- [ ] Fiziksel telefon veya emülatör hazır
- [ ] Derlemesi başarılı
- [ ] Telefonda çalışıyor ✓

---

## 🚀 İlk Çalıştırma

1. Uygulamayı aç
2. Kamera izni ver
3. Pusula sensörü bilgisini gör
4. Gece gökyüzüne çevir
5. **📸 FOTOĞRAF ÇEK** butonuna tıkla
6. Enlem hesaplaması başlacak
7. Sonuçları göreceksin! ✓

---

## 💡 İpuçları

- **Kamera FOV Ayarı**: `MainActivity.kt` satır 95'te `VERTICAL_FOV = 60f`
- **Debug Modu**: Logcat'te `KutupNav` tag'ı ara
- **Hızlı Test**: Emülatör yerine telefonla daha hızlı
- **Offline Çalışır**: İnternet gerekmez

---

Herhangi sorun olursa, Android Studio'nuz "Run" der > Look at Logcat tab'ı açın ve hatalar görün! 📲
