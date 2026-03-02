package com.kutup.navigasyon

import kotlin.math.hypot
import kotlin.math.sqrt

/**
 * Polaris Bulma - Akıllı Algoritma
 * 
 * Yıldızlar arasından Polaris'i seçer.
 * 3 kriter kullanır: yukarıda olma, parlaklık, izolasyon
 */
data class StarScore(
    val star: Star,
    val heightScore: Float,
    val brightnessScore: Float,
    val isolationScore: Float,
    val totalScore: Float
)

class PolarisFinder {
    
    fun findPolaris(stars: List<Star>, imageHeight: Int, imageWidth: Int): Pair<Star, Float> {
        // En parlak 30 yıldızı inceleme adayı olarak al
        val candidates = if (stars.size > 30) {
            stars.sortedByDescending { it.brightness }.take(30)
        } else {
            stars
        }
        
        if (candidates.isEmpty()) {
            // Hata durumu - en parlak yıldızı döndür
            return Pair(stars.maxByOrNull { it.brightness } ?: Star(0f, 0f, 0f), 0f)
        }
        
        var bestStar: Star? = null
        var bestScore = -1f
        
        for (star in candidates) {
            // 1. Yukarıda olma skoru (Polaris üst kısmda)
            val centerY = imageHeight / 2f
            val verticalPosition = (centerY - star.y) / imageHeight
            var heightScore = verticalPosition + 0.5f  // Offset
            heightScore = heightScore.coerceIn(0f, 1f)
            
            // 2. Parlaklık skoru
            var brightnessScore = star.brightness / 255f
            brightnessScore = brightnessScore.coerceIn(0f, 1f)
            
            // 3. İzolasyon skoru
            val isolationScore = calculateIsolationScore(star, candidates, imageHeight)
            
            // Ağırlıklı kombinasyon
            val totalScore = (0.4f * heightScore) + (0.3f * brightnessScore) + (0.3f * isolationScore)
            
            if (totalScore > bestScore) {
                bestScore = totalScore
                bestStar = star
            }
        }
        
        return Pair(bestStar ?: candidates[0], bestScore)
    }
    
    private fun calculateIsolationScore(star: Star, allStars: List<Star>, imageHeight: Int): Float {
        // En yakın 5 komşunun ortalama mesafesi
        val distances = allStars
            .filter { it != star }
            .map { other ->
                hypot(star.x - other.x, star.y - other.y)
            }
            .sorted()
        
        val avgDistance = if (distances.size >= 5) {
            distances.take(5).average()
        } else {
            distances.average()
        }
        
        // Normalize et
        val maxPossibleDistance = hypot(imageHeight.toFloat(), imageHeight.toFloat())
        var isolationScore = avgDistance / maxPossibleDistance
        isolationScore = isolationScore.coerceIn(0f, 1f)
        
        return isolationScore
    }
    
    fun scoreStars(stars: List<Star>, imageHeight: Int): List<StarScore> {
        val candidates = if (stars.size > 30) {
            stars.sortedByDescending { it.brightness }.take(30)
        } else {
            stars
        }
        
        return candidates.map { star ->
            val centerY = imageHeight / 2f
            val verticalPosition = (centerY - star.y) / imageHeight
            var heightScore = verticalPosition + 0.5f
            heightScore = heightScore.coerceIn(0f, 1f)
            
            var brightnessScore = star.brightness / 255f
            brightnessScore = brightnessScore.coerceIn(0f, 1f)
            
            val isolationScore = calculateIsolationScore(star, candidates, imageHeight)
            
            val totalScore = (0.4f * heightScore) + (0.3f * brightnessScore) + (0.3f * isolationScore)
            
            StarScore(star, heightScore, brightnessScore, isolationScore, totalScore)
        }.sortedByDescending { it.totalScore }
    }
}
