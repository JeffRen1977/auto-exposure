"""
Auto Exposure (AE) System
A sophisticated software library designed to automatically adjust camera exposure 
for optimal image brightness on mobile devices.

This system integrates various inputs, algorithms, and features to achieve 
accurate and pleasing exposure across diverse scenes.
"""

import numpy as np
import cv2
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import math


class SceneType(Enum):
    """Scene types for exposure optimization"""
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    BACKLIT = "backlit"
    LOW_LIGHT = "low_light"
    HIGH_CONTRAST = "high_contrast"
    FACE_DETECTED = "face_detected"


@dataclass
class ImageStatistics:
    """Image statistics for exposure analysis"""
    bayer_stats: np.ndarray  # 64x48 grid of pixel sums and counts
    histogram: np.ndarray
    saturated_pixels: int
    brightness_mean: float
    brightness_std: float
    center_weight: float


@dataclass
class SceneInformation:
    """Scene analysis results"""
    scene_type: SceneType
    confidence: float
    face_rois: List[Tuple[int, int, int, int]]  # (x, y, w, h)
    motion_level: float
    dynamic_range: float


@dataclass
class SensorInfo:
    """Sensor and hardware information"""
    exposure_time: float
    analog_gain: float
    digital_gain: float
    iso: int
    aperture: float


@dataclass
class ExposureResult:
    """Final exposure calculation results"""
    exposure_time: float
    analog_gain: float
    digital_gain: float
    total_exposure_sensitivity: float
    brightness_value: float
    aperture_value: float
    time_value: float
    sensitivity_value: float


class SpatialFrameAnalyzer:
    """Analyzes spatial statistics to understand brightness distribution"""
    
    def __init__(self, grid_size: Tuple[int, int] = (64, 48)):
        self.grid_size = grid_size
        
    def analyze_spatial_distribution(self, bayer_stats: np.ndarray) -> Dict[str, float]:
        """Analyze spatial brightness distribution"""
        if bayer_stats.shape != self.grid_size:
            bayer_stats = cv2.resize(bayer_stats, self.grid_size)
            
        # Calculate center-weighted metering
        center_weight = self._calculate_center_weight(bayer_stats)
        
        # Calculate brightness distribution
        brightness_mean = np.mean(bayer_stats)
        brightness_std = np.std(bayer_stats)
        
        # Calculate exposure zones (highlights, midtones, shadows)
        highlights = np.sum(bayer_stats > brightness_mean + brightness_std)
        shadows = np.sum(bayer_stats < brightness_mean - brightness_std)
        midtones = bayer_stats.size - highlights - shadows
        
        return {
            'center_weight': center_weight,
            'brightness_mean': brightness_mean,
            'brightness_std': brightness_std,
            'highlights_ratio': highlights / bayer_stats.size,
            'shadows_ratio': shadows / bayer_stats.size,
            'midtones_ratio': midtones / bayer_stats.size
        }
    
    def _calculate_center_weight(self, stats: np.ndarray) -> float:
        """Calculate center-weighted metering value"""
        h, w = stats.shape
        center_h, center_w = h // 2, w // 2
        
        # Create center-weighted mask
        y, x = np.ogrid[:h, :w]
        center_dist = np.sqrt((x - center_w)**2 + (y - center_h)**2)
        max_dist = np.sqrt(center_w**2 + center_h**2)
        weight_mask = 1.0 - (center_dist / max_dist)
        weight_mask = np.maximum(weight_mask, 0.1)  # Minimum weight
        
        return np.average(stats, weights=weight_mask)


class HistogramAnalyzer:
    """Utilizes histograms to understand light distribution and dynamic range"""
    
    def __init__(self, bins: int = 256):
        self.bins = bins
        
    def analyze_histogram(self, histogram: np.ndarray) -> Dict[str, float]:
        """Analyze histogram for exposure decisions"""
        # Normalize histogram
        hist_norm = histogram / np.sum(histogram)
        
        # Calculate cumulative distribution
        cumsum = np.cumsum(hist_norm)
        
        # Find key percentiles
        p5 = np.argmax(cumsum >= 0.05)
        p25 = np.argmax(cumsum >= 0.25)
        p50 = np.argmax(cumsum >= 0.50)
        p75 = np.argmax(cumsum >= 0.75)
        p95 = np.argmax(cumsum >= 0.95)
        
        # Calculate dynamic range
        dynamic_range = p95 - p5
        
        # Calculate exposure bias
        exposure_bias = (p50 - 128) / 128.0
        
        return {
            'p5': p5,
            'p25': p25,
            'p50': p50,
            'p75': p75,
            'p95': p95,
            'dynamic_range': dynamic_range,
            'exposure_bias': exposure_bias,
            'histogram_entropy': self._calculate_entropy(hist_norm)
        }
    
    def _calculate_entropy(self, hist: np.ndarray) -> float:
        """Calculate histogram entropy"""
        hist = hist[hist > 0]  # Remove zero values
        return -np.sum(hist * np.log2(hist))


class SceneAnalyzer:
    """Interprets scene context to tailor exposure"""
    
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def analyze_scene(self, image: np.ndarray, spatial_stats: Dict[str, float]) -> SceneInformation:
        """Analyze scene content and characteristics"""
        # Detect faces
        face_rois = self._detect_faces(image)
        
        # Determine scene type
        scene_type, confidence = self._classify_scene(image, spatial_stats)
        
        # Estimate motion level (simplified)
        motion_level = self._estimate_motion(image)
        
        # Calculate dynamic range
        dynamic_range = spatial_stats.get('dynamic_range', 0)
        
        return SceneInformation(
            scene_type=scene_type,
            confidence=confidence,
            face_rois=face_rois,
            motion_level=motion_level,
            dynamic_range=dynamic_range
        )
    
    def _detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces in the image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return [(x, y, w, h) for x, y, w, h in faces]
    
    def _classify_scene(self, image: np.ndarray, spatial_stats: Dict[str, float]) -> Tuple[SceneType, float]:
        """Classify scene type based on image characteristics"""
        brightness_mean = spatial_stats.get('brightness_mean', 128)
        brightness_std = spatial_stats.get('brightness_std', 0)
        
        # Simple scene classification logic
        if brightness_mean < 80:
            return SceneType.LOW_LIGHT, 0.8
        elif brightness_mean > 200:
            return SceneType.HIGH_CONTRAST, 0.7
        elif brightness_std > 50:
            return SceneType.BACKLIT, 0.6
        else:
            return SceneType.OUTDOOR, 0.5
    
    def _estimate_motion(self, image: np.ndarray) -> float:
        """Estimate motion level in the scene (simplified)"""
        # This is a placeholder - in a real implementation, you'd compare with previous frames
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        edges = cv2.Canny(gray, 50, 150)
        motion_level = np.sum(edges) / (edges.shape[0] * edges.shape[1])
        return min(motion_level, 1.0)


class ExposureController:
    """Controls exposure sensitivity and distribution"""
    
    def __init__(self):
        self.target_brightness = 128  # Target brightness value
        self.min_exposure_time = 1/10000  # 0.1ms
        self.max_exposure_time = 1/15    # 66ms
        self.min_gain = 1.0
        self.max_gain = 16.0
        
    def calculate_total_exposure_sensitivity(self, current_stats: ImageStatistics, 
                                           scene_info: SceneInformation) -> float:
        """Calculate Total Exposure Sensitivity (TES) required for target brightness"""
        current_brightness = current_stats.brightness_mean
        
        # Adjust target brightness based on scene type
        adjusted_target = self._adjust_target_for_scene(self.target_brightness, scene_info)
        
        # Calculate exposure compensation
        exposure_compensation = adjusted_target / max(current_brightness, 1.0)
        
        # Apply face detection boost
        if scene_info.face_rois:
            exposure_compensation *= 1.2  # Boost exposure for faces
        
        return exposure_compensation
    
    def _adjust_target_for_scene(self, base_target: float, scene_info: SceneInformation) -> float:
        """Adjust target brightness based on scene type"""
        adjustments = {
            SceneType.LOW_LIGHT: 0.8,
            SceneType.HIGH_CONTRAST: 1.2,
            SceneType.BACKLIT: 1.1,
            SceneType.OUTDOOR: 1.0,
            SceneType.INDOOR: 0.9,
            SceneType.FACE_DETECTED: 1.1
        }
        
        multiplier = adjustments.get(scene_info.scene_type, 1.0)
        return base_target * multiplier
    
    def distribute_exposure(self, tes: float, sensor_info: SensorInfo, 
                          motion_level: float) -> Tuple[float, float, float]:
        """Distribute TES into exposure time and gain values"""
        # Balance between motion blur and noise
        # Higher motion -> shorter exposure time, higher gain
        # Lower motion -> longer exposure time, lower gain
        
        motion_factor = 1.0 - (motion_level * 0.5)  # 0.5 to 1.0
        
        # Calculate optimal exposure time
        optimal_time = self.min_exposure_time + (self.max_exposure_time - self.min_exposure_time) * motion_factor
        
        # Calculate required gain
        required_gain = tes / optimal_time
        
        # Clamp values to valid ranges
        exposure_time = np.clip(optimal_time, self.min_exposure_time, self.max_exposure_time)
        analog_gain = np.clip(required_gain, self.min_gain, self.max_gain)
        digital_gain = 1.0  # Keep digital gain at 1.0 for best quality
        
        return exposure_time, analog_gain, digital_gain


class FlickerDetector:
    """Detects and mitigates flickering artificial lights"""
    
    def __init__(self):
        self.flicker_frequencies = [50, 60]  # Common AC frequencies
        self.detection_threshold = 0.1
        
    def detect_flicker(self, exposure_time: float) -> bool:
        """Detect if exposure time causes flicker"""
        for freq in self.flicker_frequencies:
            period = 1.0 / freq
            if abs(exposure_time - period) < self.detection_threshold:
                return True
        return False
    
    def adjust_for_flicker(self, exposure_time: float) -> float:
        """Adjust exposure time to avoid flicker"""
        for freq in self.flicker_frequencies:
            period = 1.0 / freq
            if abs(exposure_time - period) < self.detection_threshold:
                # Adjust to avoid flicker
                if exposure_time < period:
                    return period * 0.5
                else:
                    return period * 1.5
        return exposure_time


class AutoExposureSystem:
    """Main Auto Exposure System"""
    
    def __init__(self):
        self.spatial_analyzer = SpatialFrameAnalyzer()
        self.histogram_analyzer = HistogramAnalyzer()
        self.scene_analyzer = SceneAnalyzer()
        self.exposure_controller = ExposureController()
        self.flicker_detector = FlickerDetector()
        
        # System state
        self.previous_frame = None
        self.exposure_history = []
        
    def process_frame(self, image: np.ndarray, sensor_info: SensorInfo) -> ExposureResult:
        """Process a single frame and return exposure recommendations"""
        # Extract image statistics
        image_stats = self._extract_image_statistics(image)
        
        # Analyze spatial distribution
        spatial_stats = self.spatial_analyzer.analyze_spatial_distribution(image_stats.bayer_stats)
        
        # Analyze histogram
        histogram_stats = self.histogram_analyzer.analyze_histogram(image_stats.histogram)
        
        # Analyze scene
        scene_info = self.scene_analyzer.analyze_scene(image, spatial_stats)
        
        # Calculate total exposure sensitivity
        tes = self.exposure_controller.calculate_total_exposure_sensitivity(image_stats, scene_info)
        
        # Distribute exposure
        exposure_time, analog_gain, digital_gain = self.exposure_controller.distribute_exposure(
            tes, sensor_info, scene_info.motion_level
        )
        
        # Check for flicker and adjust
        if self.flicker_detector.detect_flicker(exposure_time):
            exposure_time = self.flicker_detector.adjust_for_flicker(exposure_time)
        
        # Calculate APEX values
        apex_values = self._calculate_apex_values(exposure_time, analog_gain, sensor_info.aperture)
        
        # Create result
        result = ExposureResult(
            exposure_time=exposure_time,
            analog_gain=analog_gain,
            digital_gain=digital_gain,
            total_exposure_sensitivity=tes,
            brightness_value=apex_values['bv'],
            aperture_value=apex_values['av'],
            time_value=apex_values['tv'],
            sensitivity_value=apex_values['sv']
        )
        
        # Update system state
        self._update_system_state(image, result)
        
        return result
    
    def _extract_image_statistics(self, image: np.ndarray) -> ImageStatistics:
        """Extract image statistics for analysis"""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Create Bayer statistics (simplified - in real implementation, this would come from sensor)
        bayer_stats = cv2.resize(gray, (64, 48))
        
        # Calculate histogram
        histogram = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
        
        # Calculate basic statistics
        brightness_mean = np.mean(gray)
        brightness_std = np.std(gray)
        
        # Count saturated pixels
        saturated_pixels = np.sum(gray >= 250) + np.sum(gray <= 5)
        
        # Calculate center weight
        center_weight = self.spatial_analyzer._calculate_center_weight(gray)
        
        return ImageStatistics(
            bayer_stats=bayer_stats,
            histogram=histogram,
            saturated_pixels=saturated_pixels,
            brightness_mean=brightness_mean,
            brightness_std=brightness_std,
            center_weight=center_weight
        )
    
    def _calculate_apex_values(self, exposure_time: float, gain: float, aperture: float) -> Dict[str, float]:
        """Calculate APEX (Additive System of Photographic Exposure) values"""
        # Brightness Value (Bv)
        bv = math.log2(exposure_time * gain * aperture)
        
        # Aperture Value (Av)
        av = math.log2(aperture * aperture)
        
        # Time Value (Tv)
        tv = -math.log2(exposure_time)
        
        # Sensitivity Value (Sv)
        sv = math.log2(gain * 100)  # Assuming ISO 100 base
        
        return {
            'bv': bv,
            'av': av,
            'tv': tv,
            'sv': sv
        }
    
    def _update_system_state(self, image: np.ndarray, result: ExposureResult):
        """Update system state for next frame"""
        self.previous_frame = image.copy()
        self.exposure_history.append(result)
        
        # Keep only recent history
        if len(self.exposure_history) > 10:
            self.exposure_history.pop(0)


# Example usage and testing
def main():
    """Example usage of the Auto Exposure System"""
    # Initialize the system
    ae_system = AutoExposureSystem()
    
    # Simulate sensor information
    sensor_info = SensorInfo(
        exposure_time=1/60,
        analog_gain=2.0,
        digital_gain=1.0,
        iso=200,
        aperture=2.8
    )
    
    # Load a test image
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Process the frame
    result = ae_system.process_frame(test_image, sensor_info)
    
    # Print results
    print("Auto Exposure Results:")
    print(f"Exposure Time: {result.exposure_time:.6f}s")
    print(f"Analog Gain: {result.analog_gain:.2f}")
    print(f"Digital Gain: {result.digital_gain:.2f}")
    print(f"Total Exposure Sensitivity: {result.total_exposure_sensitivity:.2f}")
    print(f"Brightness Value (Bv): {result.brightness_value:.2f}")
    print(f"Aperture Value (Av): {result.aperture_value:.2f}")
    print(f"Time Value (Tv): {result.time_value:.2f}")
    print(f"Sensitivity Value (Sv): {result.sv:.2f}")


if __name__ == "__main__":
    main()


