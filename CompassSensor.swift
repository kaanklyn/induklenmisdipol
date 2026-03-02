import CoreLocation
import UIKit

/**
 iOS Pusula Sensörü - Core Location Framework
 
 iPhone'un manyetik alan sensöründen azimuth alır.
 0° = Kuzey, 90° = Doğu, 180° = Güney, 270° = Batı
 */
class CompassSensor: NSObject, CLLocationManagerDelegate {
    
    private let locationManager = CLLocationManager()
    var azimuth: CLLocationDegrees = 0
    var onAzimuthChanged: ((CLLocationDegrees) -> Void)?
    
    let cardinalDirections = [
        "Kuzey",
        "KuzeyDoğu",
        "Doğu",
        "DoğuGüney",
        "Güney",
        "GüneyBatı",
        "Batı",
        "BatıKuzey"
    ]
    
    override init() {
        super.init()
        locationManager.delegate = self
    }
    
    func startListening() {
        locationManager.startUpdatingHeading()
    }
    
    func stopListening() {
        locationManager.stopUpdatingHeading()
    }
    
    // CLLocationManagerDelegate
    func locationManager(_ manager: CLLocationManager, 
                        didUpdateHeading newHeading: CLHeading) {
        azimuth = newHeading.trueHeading >= 0 ? newHeading.trueHeading : newHeading.magneticHeading
        onAzimuthChanged?(azimuth)
    }
    
    func locationManager(_ manager: CLLocationManager,
                        didFailWithError error: Error) {
        print("Pusula hatası: \(error.localizedDescription)")
    }
    
    func getCardinalDirection() -> String {
        let index = Int((azimuth + 22.5) / 45) % 8
        return cardinalDirections[index]
    }
    
    func isFacingNorth(tolerance: CLLocationDegrees = 15) -> Bool {
        let northMin = 360 - tolerance
        let northMax = tolerance
        return azimuth >= northMin || azimuth <= northMax
    }
    
    func getDeviationFromNorth() -> CLLocationDegrees {
        return azimuth <= 180 ? azimuth : azimuth - 360
    }
}
