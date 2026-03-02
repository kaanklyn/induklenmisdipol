# APK Indirme Linki

Bu depoda `Build and Publish APK` GitHub Actions calistiginda APK, release olarak yayimlanir.

## En Son APK (latest)

`https://github.com/<kullanici>/<repo>/releases/latest/download/kutup-navigasyon-debug.apk`

Ornek:

`https://github.com/retya/kutup_navigasyon/releases/latest/download/kutup-navigasyon-debug.apk`

## Bu Surumdeki Davranis (Takimyildiz Mantigi)

Son guncel surumde enlem bulma akisinda takimyildiz tabanli kontrol **otomatik** calisir:

- Kuzey icin **Kucuk Ayi (UMI)** oranlari
- Guney icin **Guney Haci (CRUX)** oranlari
- Sistem bu iki deseni karsilastirip en iyi eslesmeye gore kuzey/guney kararini kendi verir.

Not: Release APK'nin bu degisiklikleri icermesi icin ilgili commit'in release'e alinmis olmasi gerekir.

## Belirli Surum APK Indirme

Eger belirli bir release etiketi (tag) icin indirmek isterseniz:

`https://github.com/<kullanici>/<repo>/releases/download/<tag>/kutup-navigasyon-debug.apk`

Ornek:

`https://github.com/retya/kutup_navigasyon/releases/download/v1.2.0/kutup-navigasyon-debug.apk`

## Dogrulama

Indirdikten sonra Android cihazda:

1. Ayarlar > Guvenlik > Bilinmeyen kaynaklara izin ver
2. APK'yi acip kur
3. Uygulama icinde sonuc ekraninda kuzey/guney yorumunu ve enlem sonucunu kontrol et
