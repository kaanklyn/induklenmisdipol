package com.kutup.navigasyon

import android.graphics.Bitmap
import org.opencv.core.*
import org.opencv.imgproc.Imgproc
import kotlin.math.hypot

/**
 * Yıldız Tespiti - OpenCV Kullanarak
 * 
 * Gökyüzü fotoğrafından parlak yıldızları tespit eder.
 * Her yıldız için (x, y) koordinatı ve parlaklık değeri döndürür.
 */
data class Star(
    val x: Float,
    val y: Float,
    val brightness: Float
)

class StarDetector {
    
    fun detectStars(bitmap: Bitmap): List<Star> {
        // Bitmap'i OpenCV Mat'a çevir
        val mat = Mat()
        org.opencv.android.Utils.bitmapToMat(bitmap, mat)
        
        // Gri tona çevir (görüntü işleme için)
        val grayMat = Mat()
        Imgproc.cvtColor(mat, grayMat, Imgproc.COLOR_RGB2GRAY)
        
        // Gaussian blur ile gürültü azalt
        val blurMat = Mat()
        Imgproc.GaussianBlur(grayMat, blurMat, org.opencv.core.Size(5.0, 5.0), 0.0)
        
        // Threshold - parlaklık 180 ve üzeri olanları seç
        val threshMat = Mat()
        Imgproc.threshold(blurMat, threshMat, 180.0, 255.0, Imgproc.THRESH_BINARY)
        
        // Morfolojik işlemler - gürültüyü temizle
        val kernel = Imgproc.getStructuringElement(Imgproc.MORPH_ELLIPSE, org.opencv.core.Size(3.0, 3.0))
        val morphMat = Mat()
        Imgproc.morphologyEx(threshMat, morphMat, Imgproc.MORPH_OPEN, kernel)
        
        // Konturları bul
        val contours = java.util.ArrayList<MatOfPoint>()
        val hierarchy = Mat()
        Imgproc.findContours(morphMat, contours, hierarchy, Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE)
        
        // Yıldız listesi
        val stars = mutableListOf<Star>()
        
        // Gri mat'tan direk pixel değeri alabilmek için
        val grayBytes = ByteArray(grayMat.rows() * grayMat.cols())
        grayMat.get(0, 0, grayBytes)
        
        for (contour in contours) {
            val area = Imgproc.contourArea(contour)
            
            // Alan filtresi (3-200 piksel arası)
            if (area > 3 && area < 200) {
                val rect = org.opencv.imgproc.Imgproc.boundingRect(contour)
                
                // Yıldız merkezi
                val cx = rect.x + rect.width / 2f
                val cy = rect.y + rect.height / 2f
                
                // O bölgedeki ortalama parlaklık
                var brightnessSum = 0f
                var pixelCount = 0
                
                for (y in rect.y until (rect.y + rect.height)) {
                    for (x in rect.x until (rect.x + rect.width)) {
                        if (y < grayMat.rows() && x < grayMat.cols()) {
                            val pixelValue = grayBytes[y * grayMat.cols() + x].toInt() and 0xFF
                            brightnessSum += pixelValue
                            pixelCount++
                        }
                    }
                }
                
                val brightness = if (pixelCount > 0) brightnessSum / pixelCount else 0f
                
                stars.add(Star(cx, cy, brightness))
            }
        }
        
        // Temizle
        mat.release()
        grayMat.release()
        blurMat.release()
        threshMat.release()
        morphMat.release()
        
        return stars
    }
    
    fun getBrightestStars(stars: List<Star>, count: Int): List<Star> {
        return stars
            .sortedByDescending { it.brightness }
            .take(count)
    }
    
    fun getTopStars(stars: List<Star>, count: Int): List<Star> {
        return stars
            .sortedBy { it.y }  // Y küçük olan = üstte olan
            .take(count)
    }
}
