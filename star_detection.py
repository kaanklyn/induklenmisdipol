import cv2
import numpy as np

def detect_stars(image_path):
    """
    Yıldızları tespit eder ve merkez koordinatlarıyla parlaklığını döndürür.
    
    Args:
        image_path: Gökyüzü fotoğrafı yolu
        
    Returns:
        stars: [(x, y, brightness), ...] listesi
        shape: Görüntü boyutları (height, width)
    """
    # Gri tonlamada oku
    img = cv2.imread(image_path, 0)
    
    if img is None:
        raise ValueError(f"Görüntü yüklenemedi: {image_path}")
    
    # Gaussian blur ile gürültü azalt
    img_blur = cv2.GaussianBlur(img, (5, 5), 0)
    
    # Parlaklık threshold (yıldızlar parlaktır)
    _, thresh = cv2.threshold(img_blur, 180, 255, cv2.THRESH_BINARY)
    
    # Küçük gürültüleri temizle
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Konturları bul
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    stars = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        # Alan filtresi: çok küçük gürültüyü, çok büyük bölgeleri eleyin
        if 3 < area < 200:
            x, y, w, h = cv2.boundingRect(cnt)
            cx = x + w / 2
            cy = y + h / 2
            
            # O bölgedeki ortalama parlaklık
            brightness = np.mean(img[y:y+h, x:x+w])
            
            stars.append((cx, cy, brightness))
    
    return stars, img.shape
