package com.kutup.navigasyon

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.os.Bundle
import android.util.Log
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

/**
 * Ana Uygulama - Kutup Navigasyon Sistemi
 * 
 * Telefonda çalışan, internetsiz, offline gözlemcilik uygulaması
 */
class MainActivity : AppCompatActivity() {
    
    companion object {
        private const val TAG = "KutupNav"
        private const val REQUEST_CODE_PERMISSIONS = 10
        private val REQUIRED_PERMISSIONS = arrayOf(
            Manifest.permission.CAMERA,
            Manifest.permission.ACCESS_FINE_LOCATION
        )
    }
    
    // UI Elements
    private lateinit var previewView: PreviewView
    private lateinit var captureButton: Button
    private lateinit var compassStatusTextView: TextView
    private lateinit var azimutuResultTextView: TextView
    private lateinit var latitudeResultTextView: TextView
    
    // Modüller
    private lateinit var compass: CompassSensor
    private lateinit var starDetector: StarDetector
    private lateinit var polarisFinder: PolarisFinder
    private lateinit var latitudeSolver: LatitudeSolver
    
    // Kamera
    private lateinit var cameraExecutor: ExecutorService
    private var camera: Camera? = null
    private var imageCapture: ImageCapture? = null
    
    // Ayarlar
    private val VERTICAL_FOV = 60f  // Tipik telefon kamerası
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // UI bileşenlerini başlat
        initializeUI()
        
        // İzinleri kontrol et
        if (allPermissionsGranted()) {
            startCamera()
        } else {
            ActivityCompat.requestPermissions(this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS)
        }
        
        // Modülleri başlat
        initializeModules()
        
        // Pusula sensörünü başlat
        compass.startListening()
    }
    
    private fun initializeUI() {
        previewView = findViewById(R.id.previewView)
        captureButton = findViewById(R.id.captureButton)
        compassStatusTextView = findViewById(R.id.compassStatus)
        azimutuResultTextView = findViewById(R.id.azimutuResult)
        latitudeResultTextView = findViewById(R.id.latitudeResult)
        
        captureButton.setOnClickListener {
            takePhoto()
        }
        
        cameraExecutor = Executors.newSingleThreadExecutor()
    }
    
    private fun initializeModules() {
        compass = CompassSensor(this)
        starDetector = StarDetector()
        polarisFinder = PolarisFinder()
        latitudeSolver = LatitudeSolver()
        
        // Pusula callback
        compass.onAzimuthChanged = { azimuth ->
            updateCompassDisplay(azimuth)
        }
    }
    
    private fun allPermissionsGranted() = REQUIRED_PERMISSIONS.all {
        ContextCompat.checkSelfPermission(baseContext, it) == PackageManager.PERMISSION_GRANTED
    }
    
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_CODE_PERMISSIONS) {
            if (allPermissionsGranted()) {
                startCamera()
            } else {
                Toast.makeText(this, "İzinler reddedildi", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }
    
    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)
        
        cameraProviderFuture.addListener({
            val cameraProvider = cameraProviderFuture.get()
            
            // Preview
            val preview = Preview.Builder()
                .build()
                .also {
                    it.setSurfaceProvider(previewView.surfaceProvider)
                }
            
            // Image Capture
            imageCapture = ImageCapture.Builder()
                .setCaptureMode(ImageCapture.CAPTURE_MODE_MINIMIZE_LATENCY)
                .build()
            
            // Arka kamera seç
            val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA
            
            try {
                cameraProvider.unbindAll()
                camera = cameraProvider.bindToLifecycle(
                    this, cameraSelector, preview, imageCapture
                )
            } catch (exc: Exception) {
                Log.e(TAG, "Kamera başlatma hatası", exc)
            }
        }, ContextCompat.getMainExecutor(this))
    }
    
    private fun takePhoto() {
        val imageCapture = imageCapture ?: return
        
        // Resim al
        imageCapture.takePicture(
            ContextCompat.getMainExecutor(this),
            object : ImageCapture.OnImageCapturedCallback() {
                override fun onCaptureSuccess(image: ImageProxy) {
                    processImage(image)
                }
                
                override fun onError(exc: ImageCaptureException) {
                    Log.e(TAG, "Fotoğraf çekme hatası", exc)
                }
            }
        )
    }
    
    private fun processImage(image: ImageProxy) {
        // Arka planda işle
        cameraExecutor.execute {
            try {
                // ImageProxy'yi Bitmap'e çevir
                val bitmap = imageToBitmap(image)
                
                // 1. Yıldız tespit et
                val stars = starDetector.detectStars(bitmap)
                Log.d(TAG, "Tespit edilen yıldız: ${stars.size}")
                
                if (stars.isEmpty()) {
                    runOnUiThread {
                        Toast.makeText(this, "Yıldız tespit edilemedi", Toast.LENGTH_SHORT).show()
                    }
                    return@execute
                }
                
                // 2. Polaris bul
                val (polaris, score) = polarisFinder.findPolaris(stars, bitmap.height, bitmap.width)
                Log.d(TAG, "Polaris bulundu. Skor: $score")
                
                // 3. Enlem hesapla
                val latitudeResult = latitudeSolver.calculateLatitude(
                    polaris.y,
                    bitmap.height,
                    VERTICAL_FOV
                )
                
                // 4. Sonuçları göster
                runOnUiThread {
                    displayResults(polaris, latitudeResult)
                }
                
            } catch (e: Exception) {
                Log.e(TAG, "İşleme hatası", e)
            } finally {
                image.close()
            }
        }
    }
    
    private fun imageToBitmap(image: ImageProxy): Bitmap {
        // YUV_420_888 formatını Bitmap'e çevir (Basitleştirilmiş versyon)
        val planes = image.planes
        val ySize = planes[0].buffer.remaining()
        val uSize = planes[1].buffer.remaining()
        val vSize = planes[2].buffer.remaining()
        
        val nv21 = ByteArray(ySize + uSize + vSize)
        planes[0].buffer.get(nv21, 0, ySize)
        planes[1].buffer.get(nv21, ySize, uSize)
        planes[2].buffer.get(nv21, ySize + uSize, vSize)
        
        // Basit gri ton dönüştürme (tam YUV dönüşümü karmaşık)
        val bitmap = Bitmap.createBitmap(image.width, image.height, Bitmap.Config.ARGB_8888)
        val pixels = IntArray(image.width * image.height)
        
        for (i in pixels.indices) {
            val y = (nv21[i].toInt() and 0xFF)
            pixels[i] = (0xFF shl 24) or (y shl 16) or (y shl 8) or y
        }
        
        bitmap.setPixels(pixels, 0, image.width, 0, 0, image.width, image.height)
        return bitmap
    }
    
    private fun updateCompassDisplay(azimuth: Float) {
        runOnUiThread {
            val direction = compass.getCardinalDirection()
            val facingNorth = compass.isFacingNorth()
            val status = if (facingNorth) "✓ Kuzeye Bakıyor" else "✗ Yanlış Yön"
            
            compassStatusTextView.text = """
                🧭 Pusula: $direction
                Azimuth: $azimuth°
                $status
            """.trimIndent()
        }
    }
    
    private fun displayResults(polaris: Star, result: LatitudeResult) {
        val resultsText = """
            📊 SONUÇLAR
            ═══════════════════════
            
            ENLEM: ${result.latitude}°
            HATA PAYI: ±${result.errorMargin}°
            ARALIK: ${result.lowerBound}° → ${result.upperBound}°
            
            Polaris Yüksekliği: ${result.altitude}°
            
            Polaris Konumu:
            X: ${polaris.x.toInt()} px
            Y: ${polaris.y.toInt()} px
            Parlaklık: ${polaris.brightness.toInt()}
        """.trimIndent()
        
        latitudeResultTextView.text = resultsText
    }
    
    override fun onDestroy() {
        super.onDestroy()
        compass.stopListening()
        cameraExecutor.shutdown()
    }
}
