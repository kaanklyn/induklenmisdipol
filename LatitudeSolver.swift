import UIKit

/**
 iOS Enlem Çözücüsü
 
 Polaris'in piksel konumundan enlemi hesaplar.
 */
struct LatitudeResult {
    let latitude: Double
    let lowerBound: Double
    let upperBound: Double
    let errorMargin: Double
    let altitude: Double
}

class LatitudeSolver {
    
    func calculateLatitude(
        polariPixelY: CGFloat,
        imageHeight: CGFloat,
        verticalFov: Double
    ) -> LatitudeResult {
        // Merkez noktasından sapma
        let centerY = imageHeight / 2
        let pixelOffset = centerY - polariPixelY
        
        // Dereceye çevir
        let degreesPerPixel = verticalFov / Double(imageHeight)
        let altitude = Double(pixelOffset) * degreesPerPixel
        
        // Polaris yüksekliği ≈ Enlem
        let latitude = altitude
        
        // Hata hesabı
        let fovUncertainty: Double = 2.0
        let calibrationError: Double = 1.0
        
        let latWithLowFov = Double(centerY - polariPixelY) * ((verticalFov - fovUncertainty) / Double(imageHeight))
        let latWithHighFov = Double(centerY - polariPixelY) * ((verticalFov + fovUncertainty) / Double(imageHeight))
        
        let fovError = max(abs(latWithLowFov - latitude), abs(latWithHighFov - latitude))
        let totalError = sqrt(fovError * fovError + calibrationError * calibrationError)
        
        return LatitudeResult(
            latitude: round(latitude * 100) / 100,
            lowerBound: round((latitude - totalError) * 100) / 100,
            upperBound: round((latitude + totalError) * 100) / 100,
            errorMargin: round(totalError * 100) / 100,
            altitude: round(altitude * 100) / 100
        )
    }
    
    func pixelToAngle(pixelOffset: CGFloat, imageHeight: CGFloat, verticalFov: Double) -> Double {
        let degreesPerPixel = verticalFov / Double(imageHeight)
        return Double(pixelOffset) * degreesPerPixel
    }
}
