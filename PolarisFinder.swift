import UIKit

/**
 iOS Polaris Bulma
 
 Yıldızlar arasından Polaris'i seçer.
 */
struct StarScore {
    let star: Star
    let heightScore: Float
    let brightnessScore: Float
    let isolationScore: Float
    let totalScore: Float
}

class PolarisFinder {
    
    func findPolaris(in stars: [Star], imageHeight: CGFloat, imageWidth: CGFloat) -> (Star, Float) {
        // En parlak 30'u al
        var candidates = stars.sorted { $0.brightness > $1.brightness }
        if candidates.count > 30 {
            candidates = Array(candidates.prefix(30))
        }
        
        guard !candidates.isEmpty else {
            return (stars.max { $0.brightness < $1.brightness } ?? Star(x: 0, y: 0, brightness: 0), 0)
        }
        
        var bestStar: Star?
        var bestScore: Float = -1
        
        for star in candidates {
            // 1. Yukarıda olma skoru
            let centerY = imageHeight / 2
            let verticalPosition = (centerY - star.y) / imageHeight
            var heightScore = verticalPosition + 0.5
            heightScore = max(0, min(1, heightScore))
            
            // 2. Parlaklık skoru
            var brightnessScore = star.brightness / 255
            brightnessScore = max(0, min(1, brightnessScore))
            
            // 3. İzolasyon skoru
            let isolationScore = calculateIsolationScore(for: star, among: candidates, imageHeight: imageHeight)
            
            // Ağırlıklı kombinasyon
            let totalScore = (0.4 * heightScore) + (0.3 * brightnessScore) + (0.3 * isolationScore)
            
            if totalScore > bestScore {
                bestScore = totalScore
                bestStar = star
            }
        }
        
        return (bestStar ?? candidates[0], bestScore)
    }
    
    private func calculateIsolationScore(for star: Star, among candidates: [Star], imageHeight: CGFloat) -> Float {
        // En yakın 5 komşunun mesafesi
        var distances: [CGFloat] = []
        
        for other in candidates {
            if other.x != star.x || other.y != star.y {
                let dx = star.x - other.x
                let dy = star.y - other.y
                let distance = sqrt(dx * dx + dy * dy)
                distances.append(distance)
            }
        }
        
        distances.sort()
        
        let avgDistance: CGFloat
        if distances.count >= 5 {
            avgDistance = distances.prefix(5).reduce(0, +) / 5
        } else if !distances.isEmpty {
            avgDistance = distances.reduce(0, +) / CGFloat(distances.count)
        } else {
            avgDistance = 0
        }
        
        let maxDistance = sqrt(imageHeight * imageHeight * 2)
        var isolationScore: Float = Float(avgDistance / (maxDistance > 0 ? maxDistance : 1))
        isolationScore = max(0, min(1, isolationScore))
        
        return isolationScore
    }
    
    func scoreStars(_ stars: [Star], imageHeight: CGFloat) -> [StarScore] {
        var candidates = stars.sorted { $0.brightness > $1.brightness }
        if candidates.count > 30 {
            candidates = Array(candidates.prefix(30))
        }
        
        var scores: [StarScore] = []
        
        for star in candidates {
            let centerY = imageHeight / 2
            let verticalPosition = (centerY - star.y) / imageHeight
            var heightScore = verticalPosition + 0.5
            heightScore = max(0, min(1, heightScore))
            
            var brightnessScore = star.brightness / 255
            brightnessScore = max(0, min(1, brightnessScore))
            
            let isolationScore = calculateIsolationScore(for: star, among: candidates, imageHeight: imageHeight)
            
            let totalScore = (0.4 * heightScore) + (0.3 * brightnessScore) + (0.3 * isolationScore)
            
            scores.append(StarScore(
                star: star,
                heightScore: heightScore,
                brightnessScore: brightnessScore,
                isolationScore: isolationScore,
                totalScore: totalScore
            ))
        }
        
        return scores.sorted { $0.totalScore > $1.totalScore }
    }
}
