# 🌌 Kutup Navigasyon Sistemi - Polaris Enlem Hesaplayıcı

Gece gökyüzü fotoğrafından **Polaris (Kutup Yıldızı)** tespit ederek bulunduğunuz **enlem**i hesaplar.

## 🎯 Sistem Nedir?

- **Polaris'i Otomatik Tespit**: Foto içinden akıllı algoritma ile Polaris bulur
- **Enlem Hesaplar**: Polaris'in yüksekliğinden enlem çıkarır
- **Offline Çalışır**: İnternet gerekmez, sadece fotoğraf ve algoritma yeterli
- **Hata Analizi**: Hesaplanan enlem için hata payını döndürür

## 📋 Kurulum

### 1. Python 3.8+ Gerekli

```bash
python --version
```

### 2. Sanal Ortam Oluştur

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Kütüphaneleri Yükle

```bash
pip install -r requirements.txt
```

## 🚀 Kullanım

### Basit Kullanım

```bash
python main.py sky.jpg
```

### Kamera FOV Belirtme

```bash
python main.py sky.jpg --fov 55
```

**Tipik FOV Değerleri:**
- Akıllı telefon geniş açı: 60-70°
- Standart telefon: 50-60°
- Teleskop: 1-2°

### Pusula Sensörü Entegrasyonu

```bash
# Telefon kuzeye bakıyor (default)
python main.py sky.jpg --fov 60 --azimuth 0

# Telefon doğuya bakıyor
python main.py sky.jpg --fov 60 --azimuth 90

# Telefon batıya bakıyor
python main.py sky.jpg --fov 60 --azimuth 270

# Pusula sensörünü devre dışı bırak
python main.py sky.jpg --fov 60 --no-compass
```

**Azimuth Sistemi:**
- `0°` = Kuzey ✓ (İDEAL)
- `90°` = Doğu
- `180°` = Güney
- `270°` = Batı

### Debug Modu (Detaylı Çıktı)

```bash
python main.py sky.jpg --fov 60 --debug
```

## 📸 Fotoğraf Çekme İpuçları

1. **Telefonu kuzeye çevirin** - Polaris, gökyüzünün kuzeyde en üst noktasına yakındır
2. **Tripod kullanın** - Kararlı tutmak gerekli
3. **Uzun pozlama yapın** - ISO yüksek, açıklık f/2.8 veya daha açık
4. **Ufuk görünmesin** - Merkeze yıldızları al
5. **Şehir ışıklarından uzak** - Daha temiz yıldızlar

## 📊 Çıktı Örneği

```
============================================================
🌌 KUTUP NAVIGASYON SİSTEMİ - POLARIS ENLEMİ HESAPLAYICI 🌌
============================================================

🧭 Pusula Sensörü: AÇIK
   Azimuth: 0°
   Yön: Kuzey

📊 SONUÇLAR
────────────────────────────────────────────────────────────
Tahmini Enlem:        40.25°
Hata Payı:            ±1.5°
Aralık:               38.75° → 41.75°
Polaris Yüksekliği:   40.25°

🔍 POLARIS KONUMU
────────────────────────────────────────────────────────────
X (Yatay):            512.3 piksel
Y (Dikey):            285.7 piksel
Parlaklık:            185.2

🧭 PUSULA BİLGİSİ
────────────────────────────────────────────────────────────
Azimuth:              0.0°
Yön:                  Kuzey
Kuzeye Sapma:         0.0°
Kuzeye Bakıyor mu:    Evet ✓

📸 GÖRÜNTÜ BİLGİSİ
────────────────────────────────────────────────────────────
Görüntü Boyutu:       1080x1920 piksel
Dikey FOV:            60°
Toplam Yıldız:        156 (tespit edilen)
```

## 🔧 Sistem Mimarisi

```
main.py
├── star_detection.py    → Görüntüde yıldız tespit
├── polaris_finder.py    → Polaris seçim algoritması
├── latitude_solver.py   → Enlem hesaplama
└── compass.py           → Pusula sensörü (azimuth/yön)
```

### star_detection.py
- OpenCV ile eşik değer uygulanır
- Parlak noktalar tespit edilir
- Her yıldız için merkez koordinatı ve parlaklık kaydedilir

### polaris_finder.py
- En parlak 30 yıldız incelenir
- 3 kriter skorlanır:
  - **Yukarıda Olma (0.4 ağırlık)**: Polaris üst kısımda
  - **Parlaklık (0.3 ağırlık)**: Yeterince parlak
  - **İzolasyon (0.3 ağırlık)**: Etrafında az yıldız

### latitude_solver.py
- Polaris piksel Y koordinatını dereceye çevirir
- **Formül**: Polaris yüksekliği (°) ≈ Enlem (°)
- Hata payını hesaplar

### compass.py
- Telefon pusula sensöründen azimuth alır
- Hangi yöne baktığını belirler (Kuzey, Doğu, vb.)
- Kuzeye bakıp bakmadığını kontrol eder
- **Mock mod**: Test için simülasyon
- **Sensör mod**: Gerçek Android/iOS sensörü (geliştirme aşamasında)

## ⚠️ Hassasiyet ve Hata

| Durum | Hata Payı |
|-------|-----------|
| Tripodsuz, el titreşimi | ±3-5° |
| Tripod, sabit tutma | ±1-2° |
| Profesyonel kurulum | ±0.5-1° |

## 🌍 Kullanım Alanları

- ✅ Kutup Yarışması
- ✅ Astronomik navigasyon eğitimi
- ✅ Acil durum konumlandırması (GPS yokken)
- ✅ Gökbilim öğrenci projeleri

## 📱 Mobil Versiyona Taşıma

Bu Python prototipi şu platformlara taşınabilir:
- **Android**: Kotlin + OpenCV SDK
- **iOS**: Swift + Vision Framework
- **Web**: Python Flask + OpenCV

## 🧮 Matematiksel Temeller

**Polaris Yüksekliği = Bulunduğunuz Enlem**

Gözlemci homojen Dünya'nın üzerindeyse:
```
h = Polaris'in açısal yüksekliği (derece)
φ = Bulunduğunuz enlem (derece)

h ≈ φ (Kutup Yıldızı basit yaklaşımı için)
```

Daha doğru:
```
h = 89.26° - RA(Polaris) + Local Sidereal Time
```

Şu anda basit yaklaşım kullanıyoruz.

## 🚧 Gelecek Geliştirmeler

- [ ] Cassiopeia fotoğraflarıyla da çalışmasını sağla
- [ ] Tam plate solving algoritması (tüm gökyüzü)
- [ ] Çoklu yıldız üçgenlerine dayalı konum bulma
- [ ] Telefon pusulayla doğu-batı sensörleme
- [ ] Boylam hesaplama (hassas saat gerekir)

## 💡 İpuçları

- FOV değerini telefon spesifikasyonundan öğrenin
- Test için bilinen enlemden fotoğraf çekin
- Parlaklık threshold'u (180) kararsızsa değiştirin
- Debug modu ile algoritmanın çalışmasını gözlemleyin

## 📝 Lisans

Eğitim ve araştırma amaçlı kullanılabilir.

## 🤝 Destek

Sorun yaşarsanız:
1. Debug modu çalıştırın: `python main.py sky.jpg --debug`
2. Fotoğraf kalitesini kontrol edin
3. FOV değerini doğrulayın

---

**Yapıldı**: Kutup Yarışması
**Hedef**: GPS olmadan yıldızlarla konum bulma

## APK Download
- See APK_DOWNLOAD.md for direct release link format.

