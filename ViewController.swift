import UIKit
import AVFoundation
import MapKit

/**
 iOS Ana Uygulama - UIViewController
 
 Kamera, pusula ve harita entegrasyonu
 */
class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate, MKMapViewDelegate {
    
    // UI Componenents
    @IBOutlet weak var previewImage: UIImageView!
    @IBOutlet weak var compassLabel: UILabel!
    @IBOutlet weak var latitudeLabel: UILabel!
    @IBOutlet weak var mapView: MKMapView!
    @IBOutlet weak var captureButton: UIButton!
    
    // Modüller
    let compass = CompassSensor()
    let starDetector = StarDetector()
    let polarisFinder = PolarisFinder()
    let latitudeSolver = LatitudeSolver()
    
    // Kamera
    var imagePicker: UIImagePickerController!
    let cameraManager = AVCaptureSession()
    
    // Ayarlar
    let VERTICAL_FOV: Double = 60.0
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        setupUI()
        setupCompass()
        setupMap()
        setupCamera()
    }
    
    private func setupUI() {
        title = "🌌 Kutup Navigasyon"
        
        captureButton.setTitle("📸 FOTOĞRAF ÇEK", for: .normal)
        captureButton.backgroundColor = UIColor.systemBlue
        captureButton.setTitleColor(.white, for: .normal)
        captureButton.addTarget(self, action: #selector(capturePhoto), for: .touchUpInside)
        
        previewImage.contentMode = .scaleAspectFit
        previewImage.backgroundColor = .black
    }
    
    private func setupCompass() {
        compass.startListening()
        
        compass.onAzimuthChanged = { [weak self] azimuth in
            DispatchQueue.main.async {
                self?.updateCompassUI(azimuth: azimuth)
            }
        }
    }
    
    private func setupMap() {
        mapView.delegate = self
        mapView.mapType = .standard
        
        // Türkiye'yi odakla
        let turkeyCenter = CLLocationCoordinate2D(latitude: 39.0, longitude: 35.0)
        let region = MKCoordinateRegion(
            center: turkeyCenter,
            span: MKCoordinateSpan(latitudeDelta: 7, longitudeDelta: 10)
        )
        mapView.setRegion(region, animated: true)
    }
    
    private func setupCamera() {
        imagePicker = UIImagePickerController()
        imagePicker.delegate = self
        imagePicker.sourceType = .camera
        imagePicker.cameraFlashMode = .off
    }
    
    @objc private func capturePhoto() {
        present(imagePicker, animated: true)
    }
    
    // MARK: - Image Picker Delegate
    func imagePickerController(_ picker: UIImagePickerController,
                            didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        
        picker.dismiss(animated: true)
        
        guard let image = info[.originalImage] as? UIImage else { return }
        
        previewImage.image = image
        
        // Arka planda işle
        DispatchQueue.global().async { [weak self] in
            self?.processImage(image)
        }
    }
    
    private func processImage(_ image: UIImage) {
        // 1. Yıldız tespit et
        let stars = starDetector.detectStars(from: image)
        print("✓ Tespit edilen yıldız: \(stars.count)")
        
        guard !stars.isEmpty else {
            DispatchQueue.main.async {
                self.showAlert("Hata", "Yıldız tespit edilemedi")
            }
            return
        }
        
        // 2. Polaris bul
        let (polaris, score) = polarisFinder.findPolaris(
            in: stars,
            imageHeight: image.size.height,
            imageWidth: image.size.width
        )
        print("✓ Polaris bulundu. Skor: \(score)")
        
        // 3. Enlem hesapla
        let result = latitudeSolver.calculateLatitude(
            polariPixelY: polaris.y,
            imageHeight: image.size.height,
            verticalFov: VERTICAL_FOV
        )
        
        // 4. UI güncelle
        DispatchQueue.main.async {
            self.displayResults(latitude: result)
            self.showOnMap(latitude: result.latitude)
        }
    }
    
    private func updateCompassUI(azimuth: CLLocationDegrees) {
        let direction = compass.getCardinalDirection()
        let isFacingNorth = compass.isFacingNorth() ? "✓" : "✗"
        
        compassLabel.text = """
        🧭 \(direction)
        Azimuth: \(String(format: "%.1f", azimuth))°
        \(isFacingNorth) Kuzeye Bakıyor
        """
    }
    
    private func displayResults(latitude: LatitudeResult) {
        latitudeLabel.text = """
        📊 SONUÇLAR
        Enlem: \(latitude.latitude)°
        Hata: ±\(latitude.errorMargin)°
        Aralık: \(latitude.lowerBound)° → \(latitude.upperBound)°
        """
    }
    
    private func showOnMap(latitude: Double) {
        // Harita üzerinde göster
        let pin = MKPointAnnotation()
        pin.coordinate = CLLocationCoordinate2D(latitude: latitude, longitude: 35.0) // Orta Boylam
        pin.title = "Enlem: \(String(format: "%.2f", latitude))°"
        
        mapView.addAnnotation(pin)
        
        // Odakla
        let region = MKCoordinateRegion(
            center: pin.coordinate,
            span: MKCoordinateSpan(latitudeDelta: 3, longitudeDelta: 5)
        )
        mapView.setRegion(region, animated: true)
    }
    
    private func showAlert(_ title: String, _ message: String) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        present(alert, animated: true)
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        compass.stopListening()
    }
}
