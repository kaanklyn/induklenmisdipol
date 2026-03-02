📱 iOS SETUP - XCODE KURULUM KILAVUZU
========================================

## 🍎 Gerekli Araçlar

- **Xcode 14+** (https://developer.apple.com/xcode/)
- **macOS 12+**
- **iPhone 11+** veya Simulator
- **Apple Developer Account** (ücretsiz)

---

## 1️⃣ XCODE'DA YENİ PRO

FILE → NEW → PROJECT

Seçenekler:
- **iOS**
- **App**
- **Interface**: Storyboard
- **Language**: Swift
- **Project Name**: KutupNavigasyon
- **Organization ID**: com.kutup.navigasyon

---

## 2️⃣ DOSYALARI EKLE

### Min Swift Sınıflarını Ekle

```
Project Navigator'da sağ click
→ New File → Swift File

Eklenecek dosyalar:
```

```
CompassSensor.swift     ← Verildi
StarDetector.swift      ← Verildi  
PolarisFinder.swift     ← Verildi
LatitudeSolver.swift    ← Verildi
ViewController.swift    ← Verildi
```

### Her dosyayı kopyala ve yapıştır:

1. Xcode'da **New File** → **Swift File**
2. Ad ver (örn: CompassSensor.swift)
3. Verilmiş kodu yapıştır

---

## 3️⃣ STORYBOARD BAĞLANTILARI

### Main.storyboard Ayarları

1. Object Library'den ekle (⌘⇧L):

```
View Controller × 1
Image View × 1
Label × 3
Button × 1
Map Kit View × 1
```

Dikkat: MapKit View'ı Object Library'de bulabilir veya:
1. View Controller seç
2. Identity Inspector → Class = MKMapViewController
3. View'ı MKMapView olarak ayarla

### Outlet Bağlantıları

Control+Drag ile bağla:

```
previewImage    → Image View (ortada)
compassLabel    → Label (üst)
latitudeLabel   → Label (orta)
mapView         → Map Kit View (alt)
captureButton   → Button (alt)
```

### ViewController Sınıfı Ayarla

1. Main.storyboard'u aç
2. View Controller seç
3. **Identity Inspector** (⌘⌥3)
4. **Class** = ViewController
5. **Module** = KutupNavigasyon

---

## 4️⃣ İZİNLERİ AYARLA

### Info.plist Dosyası

Seç: **Project → Info**

Ekle:

```
Key: Privacy - Camera Usage Description
Value: "Gökyüzü fotoğrafı çekmek için kamera gereklidir"

Key: Privacy - Location When In Use Usage Description
Value: "Pusula sensöründen yön bilgisi almak için konum ve 
        pusula erişimi gereklidir"

Key: Privacy - Heading Usage Description
Value: "Manyetik kuzey yönünü belirlemek için pusula gereklidir"
```

### Capabilities

1. **Signing & Capabilities** sekmesi aç
2. **+ Capability** tıkla
3. Ekle: **Maps** (harita desteği için)

---

## 5️⃣ İMPORT EDİLECEK FRAMEWORK'LER

Xcode otomatik olarak ekler:

✓ AVFoundation (kamera)
✓ Vision (görüntü işleme)
✓ CoreLocation (pusula)
✓ MapKit (harita)
✓ UIKit (UI) 

---

## 6️⃣ BUILD AYARLARI

### General Tab

- **Minimum Deployments**: iOS 14.0
- **Device Orientation**: Portrait

### Build Settings

Search: Code Signing

```
Code Signing Identity: Apple Development
Development Team: (Apple ID'niz)
Provisioning Profile: Automatic
```

---

## 7️⃣ SIMULATOR'DA TEST

### Simulator Swift

1. **Product → Destination** → iPhone 15 (veya seç)
2. **Product → Build** (⌘B)
3. **Product → Run** (⌘R)

### Simulator Ayarları

**Features:**

Compass testi:
1. Simulator açık
2. **Features → Location** 
3. **Freeway Drive** seç (hareket içinde)
4. App kamera isteyecek

---

## 8️⃣ FİZİKSEL TELEFONDA TEST

### Xcode'da Setup

1. **Signing & Capabilities**
2. **Team** = Tüm Apple Account'a
3. **Bundle Identifier** = com.kutup.navigasyon

### Mac'de Yetkilendirme

Terminal'de:

```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

### İPhone Hazırla

1. USB ile Mac'a bağla
2. İPhone'de **Trust** seç
3. Xcode Window'da iPhone görünmeli

### Deploy

1. **Product → Destination** → İPhone seç
2. **Product → Run**
3. App iPhone'a yüklenecek

---

## 9️⃣ APK BENZERİN iOS'ta

### App Store İçin Derleme

```bash
# Terminal'de:
xcodebuild -scheme KutupNavigasyon \
           -configuration Release \
           -derivedDataPath build

# .ipa dosyası üret
xcodebuild -exportArchive \
           -archivePath build/KutupNavigasyon.xcarchive \
           -exportPath build/
```

---

## 🔟 SIKI SORUNLAR

### "Build failed - Code signing"
```
→ Xcode → Preferences (⌘,)
→ Accounts → Add Apple ID
→ Reload
```

### "No such module 'MapKit'"
```
→ Build Phases → Link Binary With Libraries
→ + MapKit.framework
```

### "Camera permission denied"
```
Simulator:
→ Settings → KutupNavigasyon → Camera = ON
→ Location Services = ON
```

### "Compass Simulator'da çalışmıyor"
```
Simulator → Features → Location → Custom Location
Boylam/Enlem gir ve yön değişir
```

---

## 📊 XCODE LAYOUT

```
┌─────────────────────────────────────┐
│ Navigator | Main | Inspector        │
├─────────────────────────────────────┤
│           │ Storyboard / Code  │    │
│ Project   │                    │    │
│ Files     │                    │    │
└─────────────────────────────────────┘
   ⌘1          ⌘2 (çalış)     ⌘3
```

---

## ✅ KONTROL LİSTESİ

- [ ] Xcode 14+ kurulu
- [ ] 5 Swift dosyası oluşturuldu
- [ ] Storyboard Outlet'leri bağlandı
- [ ] Info.plist izinleri ayarlandı
- [ ] Code Signing ayarlandı
- [ ] Simulator veya telefon hazır
- [ ] Derlemesi başarılı (⌘B)
- [ ] App çalışıyor (⌘R)

---

## 🚀 İLK ÇALIŞMA

1. App açılır
2. Kamera izni ver
3. Pusula bilgisini gör
4. **Fotoğraf Çek** tıkla
5. Enlem hesaplanır
6. Harita gösterilir ✓

---

## 💡 İPUÇLARI

- **Debug**: Xcode Console'dan (View → Debug Area → Show Console)
- **Log**: `print("Debug: \(variable)")` kullan
- **Breakpoint**: Satır numarası üzerine tıkla
- **Simulator Hızı**: Product → Scheme → Edit Scheme → Run → +
