import UIKit
import Vision

/**
 iOS Yıldız Tespiti - Vision Framework
 
 Fotoğraftan parlak yıldızları tespit eder.
 */
struct Star {
    let x: CGFloat
    let y: CGFloat
    let brightness: Float
}

class StarDetector {
    
    func detectStars(from image: UIImage) -> [Star] {
        guard let cgImage = image.cgImage else { return [] }
        
        var stars: [Star] = []
        
        // Vision request oluştur
        let request = VNDetectContoursRequest { request, error in
            if let error = error {
                print("Vision hatası: \(error.localizedDescription)")
                return
            }
            
            guard let observations = request.results as? [VNContoursObservation] else {
                return
            }
            
            for observation in observations {
                // Kontur alanını kontrol et
                let area = observation.contourExtent
                if area > 0.0001 && area < 0.02 { // Piksel alanı normalize edilmiş
                    let rect = mapToImageCoordinates(observation.boundingBox, imageSize: image.size)
                    
                    let cx = rect.midX
                    let cy = rect.midY
                    
                    // TODO: Parlaklık hesabı (image processing gerekli)
                    let brightness: Float = 200
                    
                    stars.append(Star(x: cx, y: cy, brightness: brightness))
                }
            }
        }
        
        request.reportingLevel = .detailed
        
        // İsteği çalıştır
        let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
        try? handler.perform([request])
        
        return stars
    }
    
    private func mapToImageCoordinates(_ normalizedRect: CGRect, imageSize: CGSize) -> CGRect {
        let x = normalizedRect.origin.x * imageSize.width
        let y = (1 - normalizedRect.origin.y - normalizedRect.height) * imageSize.height
        let width = normalizedRect.width * imageSize.width
        let height = normalizedRect.height * imageSize.height
        
        return CGRect(x: x, y: y, width: width, height: height)
    }
    
    func getTopStars(_ stars: [Star], count: Int) -> [Star] {
        return stars.sorted { $0.y < $1.y }.prefix(count).map { $0 }
    }
    
    func getBrightestStars(_ stars: [Star], count: Int) -> [Star] {
        return stars.sorted { $0.brightness > $1.brightness }.prefix(count).map { $0 }
    }
}
