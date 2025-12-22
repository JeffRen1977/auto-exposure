"""
Chapter 8 - Example 9: Complete Auto Exposure System

This example demonstrates the complete auto exposure pipeline:
1. System integration of all components
2. End-to-end processing pipeline
3. Temporal consistency
4. Real-time operation

Learning Objectives:
- Understand complete AE pipeline
- See how all components work together
- Learn about temporal smoothing
- Optimize for real-time performance

This corresponds to Section 8.8 in the book.
"""

import numpy as np
import cv2
from typing import Dict, List
from dataclasses import dataclass

# Import concepts from previous examples (simplified versions)
# In real implementation, these would be from core modules


@dataclass
class ExposureResult:
    """Exposure calculation result"""
    exposure_time: float
    analog_gain: float
    digital_gain: float
    total_exposure_sensitivity: float
    brightness_value: float


class CompleteAESystem:
    """
    Complete Auto Exposure System integrating all components.
    
    Pipeline:
    1. Extract image statistics
    2. Spatial analysis
    3. Histogram analysis
    4. Scene analysis
    5. Calculate TES
    6. Distribute exposure
    7. Flicker detection
    8. Calculate APEX values
    9. Temporal smoothing
    """
    
    def __init__(self):
        self.target_brightness = 128
        self.exposure_history: List[ExposureResult] = []
        self.max_history = 10
    
    def extract_statistics(self, image: np.ndarray) -> Dict:
        """Extract basic image statistics"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        return {
            'brightness_mean': float(np.mean(gray)),
            'brightness_std': float(np.std(gray)),
            'histogram': cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
        }
    
    def analyze_spatial(self, image: np.ndarray) -> Dict:
        """Spatial analysis (simplified)"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Center-weighted metering
        h, w = gray.shape
        center_h, center_w = h // 2, w // 2
        y, x = np.ogrid[:h, :w]
        center_dist = np.sqrt((x - center_w)**2 + (y - center_h)**2)
        max_dist = np.sqrt(center_w**2 + center_h**2)
        weight_mask = 1.0 - (center_dist / max_dist)
        weight_mask = np.maximum(weight_mask, 0.1)
        center_weight = np.average(gray, weights=weight_mask)
        
        return {'center_weight': float(center_weight)}
    
    def analyze_histogram(self, histogram: np.ndarray) -> Dict:
        """Histogram analysis (simplified)"""
        hist_norm = histogram / np.sum(histogram)
        cumsum = np.cumsum(hist_norm)
        p50 = np.argmax(cumsum >= 0.50)
        exposure_bias = (p50 - 128) / 128.0
        
        return {'exposure_bias': float(exposure_bias), 'median': int(p50)}
    
    def analyze_scene(self, image: np.ndarray, stats: Dict) -> Dict:
        """Scene analysis (simplified)"""
        brightness_mean = stats['brightness_mean']
        
        if brightness_mean < 80:
            scene_type = "low_light"
            adjustment = 0.8
        elif brightness_mean > 200:
            scene_type = "high_contrast"
            adjustment = 1.2
        elif stats['brightness_std'] > 50:
            scene_type = "backlit"
            adjustment = 1.1
        else:
            scene_type = "normal"
            adjustment = 1.0
        
        # Simple motion estimation
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        edges = cv2.Canny(gray, 50, 150)
        motion_level = min(np.sum(edges > 0) / (edges.shape[0] * edges.shape[1]), 1.0)
        
        return {
            'scene_type': scene_type,
            'exposure_adjustment': adjustment,
            'motion_level': float(motion_level)
        }
    
    def calculate_tes(self, current_brightness: float, scene_info: Dict) -> float:
        """Calculate Total Exposure Sensitivity"""
        target = self.target_brightness * scene_info['exposure_adjustment']
        tes = target / max(current_brightness, 1.0)
        return tes
    
    def distribute_exposure(self, tes: float, motion_level: float) -> tuple:
        """Distribute exposure between time and gain"""
        min_time = 1/10000
        max_time = 1/15
        motion_factor = 1.0 - (motion_level * 0.5)
        optimal_time = min_time + (max_time - min_time) * motion_factor
        required_gain = tes / optimal_time
        
        exposure_time = np.clip(optimal_time, min_time, max_time)
        analog_gain = np.clip(required_gain, 1.0, 16.0)
        digital_gain = 1.0
        
        return exposure_time, analog_gain, digital_gain
    
    def detect_flicker(self, exposure_time: float) -> bool:
        """Simple flicker detection"""
        for freq in [50, 60]:
            period = 1.0 / (freq * 2)
            if abs(exposure_time - period) < 0.1:
                return True
        return False
    
    def adjust_for_flicker(self, exposure_time: float) -> float:
        """Adjust exposure time to avoid flicker"""
        for freq in [50, 60]:
            period = 1.0 / (freq * 2)
            if abs(exposure_time - period) < 0.1:
                return period * 0.5 if exposure_time < period else period * 1.5
        return exposure_time
    
    def calculate_apex(self, exposure_time: float, gain: float, aperture: float) -> float:
        """Calculate brightness value (Bv)"""
        import math
        return math.log2(exposure_time * gain * aperture)
    
    def temporal_smoothing(self, new_result: ExposureResult) -> ExposureResult:
        """Apply temporal smoothing to exposure results"""
        if not self.exposure_history:
            return new_result
        
        # Average with recent history (simple moving average)
        recent = self.exposure_history[-3:] if len(self.exposure_history) >= 3 else self.exposure_history
        
        avg_time = np.mean([r.exposure_time for r in recent] + [new_result.exposure_time])
        avg_gain = np.mean([r.analog_gain for r in recent] + [new_result.analog_gain])
        
        # Use 70% new value, 30% average (smooth transition)
        smoothed_time = 0.7 * new_result.exposure_time + 0.3 * avg_time
        smoothed_gain = 0.7 * new_result.analog_gain + 0.3 * avg_gain
        
        return ExposureResult(
            exposure_time=smoothed_time,
            analog_gain=smoothed_gain,
            digital_gain=new_result.digital_gain,
            total_exposure_sensitivity=new_result.total_exposure_sensitivity,
            brightness_value=new_result.brightness_value
        )
    
    def process_frame(self, image: np.ndarray, aperture: float = 2.8) -> ExposureResult:
        """
        Process a single frame through the complete AE pipeline.
        
        Args:
            image: Input image
            aperture: Aperture setting (f-number)
        
        Returns:
            ExposureResult with recommended settings
        """
        # Step 1: Extract statistics
        stats = self.extract_statistics(image)
        
        # Step 2: Spatial analysis
        spatial = self.analyze_spatial(image)
        
        # Step 3: Histogram analysis
        histogram_analysis = self.analyze_histogram(stats['histogram'])
        
        # Step 4: Scene analysis
        scene_info = self.analyze_scene(image, stats)
        
        # Step 5: Calculate TES
        tes = self.calculate_tes(stats['brightness_mean'], scene_info)
        
        # Step 6: Distribute exposure
        exposure_time, analog_gain, digital_gain = self.distribute_exposure(
            tes, scene_info['motion_level']
        )
        
        # Step 7: Flicker detection and adjustment
        if self.detect_flicker(exposure_time):
            exposure_time = self.adjust_for_flicker(exposure_time)
        
        # Step 8: Calculate APEX values
        bv = self.calculate_apex(exposure_time, analog_gain, aperture)
        
        # Create result
        result = ExposureResult(
            exposure_time=exposure_time,
            analog_gain=analog_gain,
            digital_gain=digital_gain,
            total_exposure_sensitivity=tes,
            brightness_value=bv
        )
        
        # Step 9: Temporal smoothing
        smoothed_result = self.temporal_smoothing(result)
        
        # Update history
        self.exposure_history.append(smoothed_result)
        if len(self.exposure_history) > self.max_history:
            self.exposure_history.pop(0)
        
        return smoothed_result


def demonstrate_complete_pipeline():
    """
    Demonstrate the complete AE pipeline.
    """
    print("\n" + "=" * 60)
    print("COMPLETE AUTO EXPOSURE PIPELINE")
    print("=" * 60)
    
    # Initialize system
    ae_system = CompleteAESystem()
    
    # Create test images with different characteristics
    print("\n1. Processing different scenes...")
    print("-" * 60)
    
    scenes = [
        ("Very Dark Scene", np.random.normal(40, 10, (480, 640, 3)).astype(np.uint8)),
        ("Dark Scene", np.random.normal(70, 15, (480, 640, 3)).astype(np.uint8)),
        ("Normal Scene", np.random.normal(128, 30, (480, 640, 3)).astype(np.uint8)),
        ("Bright Scene", np.random.normal(180, 20, (480, 640, 3)).astype(np.uint8)),
        ("Very Bright Scene", np.random.normal(220, 15, (480, 640, 3)).astype(np.uint8)),
    ]
    
    print(f"\n{'Scene':<20} {'Time (ms)':<12} {'Gain':<8} {'TES':<8} {'Bv':<8} {'FPS':<8}")
    print("-" * 60)
    
    for name, image in scenes:
        result = ae_system.process_frame(image)
        
        fps = 1.0 / result.exposure_time if result.exposure_time > 0 else 0
        
        print(f"{name:<20} {result.exposure_time*1000:>6.2f}{'':<5} "
              f"{result.analog_gain:>6.2f} {result.total_exposure_sensitivity:>6.2f} "
              f"{result.brightness_value:>6.2f} {fps:>6.1f}")
    
    print("-" * 60)


def demonstrate_temporal_consistency():
    """
    Demonstrate temporal smoothing across frames.
    """
    print("\n" + "=" * 60)
    print("TEMPORAL CONSISTENCY")
    print("=" * 60)
    
    ae_system = CompleteAESystem()
    
    # Simulate sudden brightness change
    print("\nSimulating sudden scene change (dark → bright)...")
    print("-" * 60)
    
    # Start with dark scene
    dark_image = np.random.normal(50, 10, (480, 640, 3)).astype(np.uint8)
    
    print(f"\n{'Frame':<8} {'Time (ms)':<12} {'Gain':<8} {'Change':<15}")
    print("-" * 60)
    
    prev_time = None
    for i in range(5):
        result = ae_system.process_frame(dark_image)
        
        if prev_time is not None:
            change = ((result.exposure_time - prev_time) / prev_time) * 100
            change_str = f"{change:+.1f}%"
        else:
            change_str = "initial"
        
        print(f"{i+1:<8} {result.exposure_time*1000:>6.2f}{'':<5} "
              f"{result.analog_gain:>6.2f} {change_str:<15}")
        
        prev_time = result.exposure_time
    
    # Sudden change to bright scene
    bright_image = np.random.normal(200, 15, (480, 640, 3)).astype(np.uint8)
    
    print("\n--- Sudden scene change ---\n")
    
    for i in range(5, 10):
        result = ae_system.process_frame(bright_image)
        
        change = ((result.exposure_time - prev_time) / prev_time) * 100
        print(f"{i+1:<8} {result.exposure_time*1000:>6.2f}{'':<5} "
              f"{result.analog_gain:>6.2f} {change:+.1f}%{'':<10}")
        
        prev_time = result.exposure_time
    
    print("-" * 60)
    print("\nNote: Temporal smoothing prevents sudden jumps in exposure")
    print("      providing smooth transitions between frames")


def demonstrate_pipeline_steps():
    """
    Demonstrate each step of the pipeline.
    """
    print("\n" + "=" * 60)
    print("PIPELINE STEP-BY-STEP")
    print("=" * 60)
    
    ae_system = CompleteAESystem()
    
    # Create test image
    test_image = np.random.normal(100, 25, (480, 640, 3)).astype(np.uint8)
    test_image = np.clip(test_image, 0, 255)
    
    print("\nProcessing test image through pipeline:")
    print("-" * 60)
    
    # Step 1
    stats = ae_system.extract_statistics(test_image)
    print(f"\nStep 1: Extract Statistics")
    print(f"  Mean Brightness: {stats['brightness_mean']:.1f}")
    print(f"  Std Deviation:  {stats['brightness_std']:.1f}")
    
    # Step 2
    spatial = ae_system.analyze_spatial(test_image)
    print(f"\nStep 2: Spatial Analysis")
    print(f"  Center-Weighted: {spatial['center_weight']:.1f}")
    
    # Step 3
    histogram_analysis = ae_system.analyze_histogram(stats['histogram'])
    print(f"\nStep 3: Histogram Analysis")
    print(f"  Exposure Bias: {histogram_analysis['exposure_bias']:.3f}")
    print(f"  Median: {histogram_analysis['median']}")
    
    # Step 4
    scene_info = ae_system.analyze_scene(test_image, stats)
    print(f"\nStep 4: Scene Analysis")
    print(f"  Scene Type: {scene_info['scene_type']}")
    print(f"  Adjustment: {scene_info['exposure_adjustment']:.2f}x")
    print(f"  Motion Level: {scene_info['motion_level']:.2f}")
    
    # Step 5
    tes = ae_system.calculate_tes(stats['brightness_mean'], scene_info)
    print(f"\nStep 5: Calculate TES")
    print(f"  TES: {tes:.2f}")
    
    # Step 6
    exp_time, gain, dig_gain = ae_system.distribute_exposure(tes, scene_info['motion_level'])
    print(f"\nStep 6: Distribute Exposure")
    print(f"  Exposure Time: {exp_time*1000:.2f}ms")
    print(f"  Analog Gain: {gain:.2f}x")
    print(f"  Digital Gain: {dig_gain:.2f}x")
    
    # Step 7
    has_flicker = ae_system.detect_flicker(exp_time)
    if has_flicker:
        exp_time = ae_system.adjust_for_flicker(exp_time)
        print(f"\nStep 7: Flicker Detection & Adjustment")
        print(f"  Flicker detected, adjusted to: {exp_time*1000:.2f}ms")
    else:
        print(f"\nStep 7: Flicker Detection")
        print(f"  No flicker detected")
    
    # Step 8
    bv = ae_system.calculate_apex(exp_time, gain, 2.8)
    print(f"\nStep 8: Calculate APEX")
    print(f"  Brightness Value (Bv): {bv:.2f}")
    
    print("\n" + "-" * 60)
    print("\nFinal Result:")
    print(f"  Exposure Time: {exp_time*1000:.2f}ms ({1/exp_time:.1f} fps)")
    print(f"  Analog Gain: {gain:.2f}x")
    print(f"  Total Exposure Sensitivity: {tes:.2f}")
    print(f"  Brightness Value: {bv:.2f}")
    
    print("\n" + "=" * 60)


def main():
    """
    Main function demonstrating complete AE system.
    """
    print("\n" + "=" * 60)
    print("CHAPTER 8 - EXAMPLE 9: COMPLETE AUTO EXPOSURE SYSTEM")
    print("=" * 60)
    print("\nThis example demonstrates:")
    print("1. Complete AE pipeline integration")
    print("2. End-to-end processing")
    print("3. Temporal consistency")
    print("4. Real-time operation")
    print("\n" + "=" * 60)
    
    demonstrate_complete_pipeline()
    demonstrate_temporal_consistency()
    demonstrate_pipeline_steps()
    
    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("=" * 60)
    print("1. Complete pipeline integrates all components")
    print("2. Temporal smoothing prevents sudden changes")
    print("3. Each step builds on previous analysis")
    print("4. System is optimized for real-time operation")
    print("\n" + "=" * 60)
    print("Congratulations! You've completed all examples.")
    print("You now understand the complete auto exposure system!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()


