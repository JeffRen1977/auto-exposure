"""
Chapter 8 - Example 5: Scene Analysis

This example demonstrates scene understanding for auto exposure:
1. Scene type classification
2. Face detection for exposure prioritization
3. Motion estimation
4. Scene-aware exposure adjustment

Learning Objectives:
- Classify different scene types
- Detect faces and prioritize exposure
- Estimate motion levels
- Adjust exposure based on scene context

This corresponds to Section 8.5 in the book.
"""

import numpy as np
import cv2
from typing import List, Tuple, Dict
from enum import Enum


class SceneType(Enum):
    """Scene types for exposure optimization"""
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    BACKLIT = "backlit"
    LOW_LIGHT = "low_light"
    HIGH_CONTRAST = "high_contrast"
    FACE_DETECTED = "face_detected"


def classify_scene(image: np.ndarray, brightness_mean: float, brightness_std: float) -> Tuple[SceneType, float]:
    """
    Classify scene type based on brightness characteristics.
    
    Different scene types require different exposure strategies:
    - Low light: Prevent blown highlights, accept some noise
    - High contrast: May need HDR techniques
    - Backlit: Compensate for bright background
    - Indoor: Slightly darker exposure
    - Outdoor: Standard exposure
    
    Args:
        image: Input image
        brightness_mean: Average brightness (0-255)
        brightness_std: Standard deviation of brightness
    
    Returns:
        Tuple of (SceneType, confidence)
    """
    # Decision tree based on brightness characteristics
    if brightness_mean < 80:
        return SceneType.LOW_LIGHT, 0.8
    elif brightness_mean > 200:
        return SceneType.HIGH_CONTRAST, 0.7
    elif brightness_std > 50:
        return SceneType.BACKLIT, 0.6
    elif brightness_mean < 120:
        return SceneType.INDOOR, 0.7
    else:
        return SceneType.OUTDOOR, 0.5


def detect_faces(image: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """
    Detect faces in the image using OpenCV's Haar Cascade.
    
    Face detection is important for auto exposure because:
    - Faces should be well-exposed (not too dark or bright)
    - Faces are often the main subject
    - Exposure should prioritize face regions
    
    Args:
        image: Input image (BGR format)
    
    Returns:
        List of face ROIs as (x, y, width, height) tuples
    """
    # Load face cascade classifier
    try:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    except:
        print("Warning: Could not load face cascade. Face detection disabled.")
        return []
    
    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,    # 10% scale reduction per pyramid level
        minNeighbors=4,     # Minimum rectangles to keep detection
        minSize=(30, 30)    # Minimum face size
    )
    
    return [(x, y, w, h) for x, y, w, h in faces]


def estimate_motion(image: np.ndarray) -> float:
    """
    Estimate motion level in the scene.
    
    This is a simplified motion estimation using edge detection.
    In a real implementation, you would compare with previous frames
    using optical flow or frame differencing.
    
    High motion → prefer shorter exposure time (less blur)
    Low motion → prefer longer exposure time (less noise)
    
    Args:
        image: Input image
    
    Returns:
        Motion level (0.0 to 1.0)
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Detect edges (motion creates more edges)
    edges = cv2.Canny(gray, 50, 150)
    
    # Motion level is proportional to edge density
    motion_level = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    # Normalize to [0, 1]
    return min(motion_level, 1.0)


def get_scene_exposure_adjustment(scene_type: SceneType) -> float:
    """
    Get exposure adjustment multiplier for different scene types.
    
    Different scenes need different target brightness:
    - Low light: Lower target (prevent highlights)
    - High contrast: Higher target (boost shadows)
    - Backlit: Slightly higher (compensate)
    - Face detected: Higher (brighten faces)
    
    Args:
        scene_type: Classified scene type
    
    Returns:
        Multiplier for target brightness (1.0 = no change)
    """
    adjustments = {
        SceneType.LOW_LIGHT: 0.8,      # 80% of normal (darker)
        SceneType.HIGH_CONTRAST: 1.2,  # 120% of normal (brighter)
        SceneType.BACKLIT: 1.1,        # 110% of normal
        SceneType.OUTDOOR: 1.0,        # 100% (standard)
        SceneType.INDOOR: 0.9,        # 90% of normal
        SceneType.FACE_DETECTED: 1.1,  # 110% (brighten faces)
    }
    
    return adjustments.get(scene_type, 1.0)


def analyze_scene(image: np.ndarray, brightness_mean: float, brightness_std: float) -> Dict:
    """
    Complete scene analysis for exposure adjustment.
    
    Args:
        image: Input image
        brightness_mean: Average brightness
        brightness_std: Standard deviation
    
    Returns:
        Dictionary with scene analysis results
    """
    # Classify scene
    scene_type, confidence = classify_scene(image, brightness_mean, brightness_std)
    
    # Detect faces
    face_rois = detect_faces(image)
    
    # If faces detected, update scene type
    if face_rois:
        scene_type = SceneType.FACE_DETECTED
        confidence = 0.9
    
    # Estimate motion
    motion_level = estimate_motion(image)
    
    # Get exposure adjustment
    exposure_adjustment = get_scene_exposure_adjustment(scene_type)
    
    return {
        'scene_type': scene_type,
        'confidence': confidence,
        'face_rois': face_rois,
        'face_count': len(face_rois),
        'motion_level': motion_level,
        'exposure_adjustment': exposure_adjustment
    }


def demonstrate_scene_analysis():
    """
    Demonstrate scene analysis techniques.
    """
    print("\n" + "=" * 60)
    print("SCENE ANALYSIS DEMONSTRATION")
    print("=" * 60)
    
    # Create test images with different scene characteristics
    print("\n1. Creating test images...")
    
    # Low light scene
    low_light = np.random.normal(50, 15, (480, 640, 3)).astype(np.uint8)
    low_light = np.clip(low_light, 0, 255)
    
    # High contrast scene
    high_contrast = np.concatenate([
        np.random.normal(220, 10, (240, 640, 3)),
        np.random.normal(30, 10, (240, 640, 3))
    ]).astype(np.uint8)
    high_contrast = np.clip(high_contrast, 0, 255)
    
    # Backlit scene (bright background, dark foreground)
    backlit = np.random.normal(200, 20, (480, 640, 3)).astype(np.uint8)
    backlit[200:, :] = np.random.normal(60, 15, (280, 640, 3)).astype(np.uint8)
    backlit = np.clip(backlit, 0, 255)
    
    # Indoor scene
    indoor = np.random.normal(100, 20, (480, 640, 3)).astype(np.uint8)
    indoor = np.clip(indoor, 0, 255)
    
    # Outdoor scene
    outdoor = np.random.normal(150, 30, (480, 640, 3)).astype(np.uint8)
    outdoor = np.clip(outdoor, 0, 255)
    
    images = [
        ("Low Light", low_light, 50, 15),
        ("High Contrast", high_contrast, 125, 80),
        ("Backlit", backlit, 130, 60),
        ("Indoor", indoor, 100, 20),
        ("Outdoor", outdoor, 150, 30),
    ]
    
    print("\n2. Scene Classification...")
    print("-" * 60)
    
    for name, image, mean, std in images:
        analysis = analyze_scene(image, mean, std)
        
        print(f"\n{name}:")
        print(f"  Scene Type:           {analysis['scene_type'].value}")
        print(f"  Confidence:           {analysis['confidence']:.2f}")
        print(f"  Faces Detected:       {analysis['face_count']}")
        print(f"  Motion Level:         {analysis['motion_level']:.2f}")
        print(f"  Exposure Adjustment:  {analysis['exposure_adjustment']:.2f}x")
        
        # Interpretation
        if analysis['exposure_adjustment'] > 1.0:
            print(f"  → Increase exposure by {(analysis['exposure_adjustment']-1.0)*100:.0f}%")
        elif analysis['exposure_adjustment'] < 1.0:
            print(f"  → Decrease exposure by {(1.0-analysis['exposure_adjustment'])*100:.0f}%")
        else:
            print(f"  → Standard exposure")
    
    print("\n" + "-" * 60)
    print("\n3. Scene Type Exposure Adjustments...")
    print("-" * 60)
    print("\nScene Type Adjustments Table:")
    print("-" * 60)
    print(f"{'Scene Type':<20} {'Multiplier':<12} {'Target Brightness':<20}")
    print("-" * 60)
    
    for scene_type in SceneType:
        adj = get_scene_exposure_adjustment(scene_type)
        target = int(128 * adj)
        print(f"{scene_type.value:<20} {adj:<12.2f} {target:<20}")
    
    print("\n" + "=" * 60)


def main():
    """
    Main function demonstrating scene analysis.
    """
    print("\n" + "=" * 60)
    print("CHAPTER 8 - EXAMPLE 5: SCENE ANALYSIS")
    print("=" * 60)
    print("\nThis example demonstrates:")
    print("1. Scene type classification")
    print("2. Face detection for exposure prioritization")
    print("3. Motion estimation")
    print("4. Scene-aware exposure adjustment")
    print("\n" + "=" * 60)
    
    demonstrate_scene_analysis()
    
    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("=" * 60)
    print("1. Different scenes need different exposure strategies")
    print("2. Face detection helps prioritize subject exposure")
    print("3. Motion estimation guides exposure time selection")
    print("4. Scene-aware adjustments improve image quality")
    print("\n" + "=" * 60)
    print("Next: Run 06_exposure_controller.py to learn about")
    print("      TES calculation and exposure distribution")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
