package com.kutup.navigasyon

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import kotlin.math.abs

/**
 * Telefon Pusula Sensörü - Gerçek Sensor Entegrasyonu
 * 
 * Manyetik alan sensöründen azimuth (yön) alır.
 * 0° = Kuzey, 90° = Doğu, 180° = Güney, 270° = Batı
 */
class CompassSensor(private val context: Context) : SensorEventListener {
    
    private val sensorManager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager
    private val magneticFieldSensor = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD)
    private val accelerometerSensor = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
    
    private var azimuth: Float = 0f
    private var magnetometerData = FloatArray(3)
    private var accelerometerData = FloatArray(3)
    private var rotationMatrix = FloatArray(9)
    private var orientationValues = FloatArray(3)
    
    // Callback
    var onAzimuthChanged: ((Float) -> Unit)? = null
    
    // Durumu takip et
    var isListening = false
        private set
    
    fun startListening() {
        if (!isListening) {
            magneticFieldSensor?.let {
                sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_UI)
            }
            accelerometerSensor?.let {
                sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_UI)
            }
            isListening = true
        }
    }
    
    fun stopListening() {
        if (isListening) {
            sensorManager.unregisterListener(this)
            isListening = false
        }
    }
    
    override fun onSensorChanged(event: SensorEvent?) {
        event ?: return
        
        when (event.sensor.type) {
            Sensor.TYPE_MAGNETIC_FIELD -> {
                magnetometerData = event.values.copyOf()
            }
            Sensor.TYPE_ACCELEROMETER -> {
                accelerometerData = event.values.copyOf()
            }
        }
        
        // Rotation matrix hesapla
        val rotationMatrixComplete = FloatArray(9)
        val success = SensorManager.getRotationMatrix(
            rotationMatrixComplete,
            null,
            accelerometerData,
            magnetometerData
        )
        
        if (success) {
            // Orientation hesapla
            SensorManager.getOrientation(rotationMatrixComplete, orientationValues)
            
            // Azimuth (radyanı dereceye çevir)
            azimuth = Math.toDegrees(orientationValues[0].toDouble()).toFloat()
            
            // 0-360 aralığına normalize et
            if (azimuth < 0) {
                azimuth += 360f
            }
            
            // Callback çağır
            onAzimuthChanged?.invoke(azimuth)
        }
    }
    
    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        // Sensör doğruluk değişimi
    }
    
    fun getAzimuth(): Float = azimuth
    
    fun getCardinalDirection(): String {
        val directions = arrayOf(
            "Kuzey",
            "KuzeyDoğu",
            "Doğu",
            "DoğuGüney",
            "Güney",
            "GüneyBatı",
            "Batı",
            "BatıKuzey"
        )
        
        val index = ((azimuth + 22.5) / 45).toInt() % 8
        return directions[index]
    }
    
    fun isFacingNorth(tolerance: Float = 15f): Boolean {
        val northMin = 360 - tolerance
        val northMax = tolerance
        return azimuth >= northMin || azimuth <= northMax
    }
    
    fun getDeviationFromNorth(): Float {
        return if (azimuth <= 180) {
            azimuth
        } else {
            azimuth - 360f
        }
    }
    
    fun getCorrectionAngle(): Float = -getDeviationFromNorth()
}
