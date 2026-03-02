# iOS Podfile - Kütüphane Yöneticisi

platform :ios, '14.0'

target 'KutupNavigasyon' do
  # Pod::Specs şu anda boş - Vision, CoreLocation, MapKit sistem framework'ü
  
  # İsteğe bağlı: Görüntü işleme kütüphaneleri
  # pod 'OpenCV-iOS'  # Eğer OpenCV kullanmamız gerekirse
  
end

post_install do |installer|
  installer.pods_project.targets.each do |target|
    flutter_additional_ios_build_settings(target)
  end
end
