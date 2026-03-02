package com.kutup.navigasyon

import kotlin.math.sqrt

/**
 * Enlem Çözücüsü
 * 
 * Polaris'in piksel konumundan enlemi hesaplar.
 * Formül: Polaris'in ufuk üstündeki yüksekliği = Bulunduğunuz Enlem
 */
data class LatitudeResult(
    val latitude: Float,
    val lowerBound: Float,
    val upperBound: Float,
    val errorMargin: Float,
    val altitude: Float
)

class LatitudeSolver {
    
    fun calculateLatitude(
        polariPixelY: Float,
        imageHeight: Int,
        verticalFov: Float
    ): LatitudeResult {
        // Merkez noktasından sapma
        val centerY = imageHeight / 2f
        val pixelOffset = centerY - polariPixelY
        
        // Dereceye çevir
        val degreesPerPixel = verticalFov / imageHeight
        val altitude = pixelOffset * degreesPerPixel
        
        // Polaris yüksekliği ≈ Enlem
        val latitude = altitude
        
        // Hata hesabı
        val fovUncertainty = 2f  // FOV ölçüm hatasında ±2° varsay
        val calibrationError = 1f  // Kalibrasyon hatası ±1°
        
        val latWithLowFov = (centerY - polariPixelY) * ((verticalFov - fovUncertainty) / imageHeight)
        val latWithHighFov = (centerY - polariPixelY) * ((verticalFov + fovUncertainty) / imageHeight)
        
        val fovError = maxOf(
            kotlin.math.abs(latWithLowFov - latitude),
            kotlin.math.abs(latWithHighFov - latitude)
        )
        
        val totalError = sqrt(fovError * fovError + calibrationError * calibrationError)
        
        return LatitudeResult(
            latitude = round(latitude, 2),
            lowerBound = round(latitude - totalError, 2),
            upperBound = round(latitude + totalError, 2),
            errorMargin = round(totalError, 2),
            altitude = round(altitude, 2)
        )
    }
    
    fun pixelToAngle(pixelOffset: Float, imageHeight: Int, verticalFov: Float): Float {
        val degreesPerPixel = verticalFov / imageHeight
        return pixelOffset * degreesPerPixel
    }
    
    private fun round(value: Float, decimals: Int): Float {
        val multiplier = kotlin.math.pow(10f, decimals.toFloat()).toInt()
        return (value * multiplier).toInt() / multiplier.toFloat()
    }
}
