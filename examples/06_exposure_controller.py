"""
Chapter 8 - Example 6: Exposure Control

This example demonstrates exposure control algorithms:
1. Total Exposure Sensitivity (TES) calculation
2. Exposure distribution (Time vs Gain)
3. Motion blur vs noise trade-off
4. Exposure limits and constraints

Learning Objectives:
- Calculate TES from brightness difference
- Distribute exposure between time and gain
- Balance motion blur and noise
- Apply exposure constraints

This corresponds to Section 8.6 in the book.
"""

import numpy as np
from typing import Tuple


class ExposureController:
    """
    Controls exposure sensitivity and distribution.
    
    The key challenge is balancing:
    - Motion blur (longer exposure time)
    - Image noise (higher gain)
    - Scene brightness (exposure compensation)
    """
    
    def __init__(self):
        self.target_brightness = 128  # Target brightness (middle gray)
        self.min_exposure_time = 1/10000  # 0.1ms (for bright scenes)
        self.max_exposure_time = 1/15     # 66ms (for low light)
        self.min_gain = 1.0
        self.max_gain = 16.0
    
    def calculate_tes(self, current_brightness: float, 
                     target_brightness: float = None) -> float:
        """
        Calculate Total Exposure Sensitivity (TES).
        
        TES is the factor by which we need to adjust exposure to reach
        the target brightness. It combines exposure time and gain.
        
        Formula: TES = target_brightness / current_brightness
        
        Example:
            Current: 64 (too dark)
            Target: 128 (middle gray)
            TES = 128 / 64 = 2.0 (need 2x more exposure)
        
        Args:
            current_brightness: Current average brightness (0-255)
            target_brightness: Desired brightness (default: self.target_brightness)
        
        Returns:
            TES value (>1.0 = increase, <1.0 = decrease)
        """
        if target_brightness is None:
            target_brightness = self.target_brightness
        
        # Avoid division by zero
        if current_brightness < 1.0:
            current_brightness = 1.0
        
        tes = target_brightness / current_brightness
        
        return tes
    
    def distribute_exposure(self, tes: float, motion_level: float) -> Tuple[float, float]:
        """
        Distribute TES between exposure time and gain.
        
        The key trade-off:
        - Longer exposure time → more light, but risk of motion blur
        - Higher gain → more light, but more image noise
        
        Strategy:
        - High motion → prefer shorter exposure, higher gain
        - Low motion → prefer longer exposure, lower gain
        
        Args:
            tes: Total Exposure Sensitivity
            motion_level: Motion level (0.0 = no motion, 1.0 = high motion)
        
        Returns:
            Tuple of (exposure_time, analog_gain)
        """
        # Motion factor: 0.5 (high motion) to 1.0 (no motion)
        # High motion → shorter exposure time
        motion_factor = 1.0 - (motion_level * 0.5)
        
        # Calculate exposure time based on motion
        time_range = self.max_exposure_time - self.min_exposure_time
        optimal_time = self.min_exposure_time + time_range * motion_factor
        
        # Calculate required gain to achieve TES
        # TES = exposure_time × gain
        # gain = TES / exposure_time
        required_gain = tes / optimal_time
        
        # Clamp to valid ranges
        exposure_time = np.clip(optimal_time, 
                               self.min_exposure_time,
                               self.max_exposure_time)
        
        analog_gain = np.clip(required_gain,
                             self.min_gain,
                             self.max_gain)
        
        return exposure_time, analog_gain


def demonstrate_tes_calculation():
    """
    Demonstrate TES calculation for different brightness levels.
    """
    print("\n" + "=" * 60)
    print("TOTAL EXPOSURE SENSITIVITY (TES) CALCULATION")
    print("=" * 60)
    
    controller = ExposureController()
    target = 128  # Middle gray
    
    scenarios = [
        ("Very Dark", 32),
        ("Dark", 64),
        ("Slightly Dark", 96),
        ("Well Exposed", 128),
        ("Slightly Bright", 160),
        ("Bright", 224),
    ]
    
    print(f"\nTarget Brightness: {target} (middle gray)")
    print("-" * 60)
    print(f"{'Scenario':<20} {'Current':<10} {'TES':<10} {'Action'}")
    print("-" * 60)
    
    for name, current in scenarios:
        tes = controller.calculate_tes(current, target)
        
        if tes > 1.5:
            action = f"Increase {tes:.2f}x"
        elif tes > 1.1:
            action = f"Increase {tes:.2f}x"
        elif tes < 0.7:
            action = f"Decrease {1/tes:.2f}x"
        elif tes < 0.9:
            action = f"Decrease {1/tes:.2f}x"
        else:
            action = "Well exposed ✓"
        
        print(f"{name:<20} {current:<10} {tes:<10.2f} {action}")
    
    print("-" * 60)


def demonstrate_exposure_distribution():
    """
    Demonstrate exposure distribution for different scenarios.
    """
    print("\n" + "=" * 60)
    print("EXPOSURE DISTRIBUTION (TIME vs GAIN)")
    print("=" * 60)
    
    controller = ExposureController()
    
    # Test scenarios
    scenarios = [
        ("Dark Scene, No Motion", 50, 0.1),
        ("Dark Scene, High Motion", 50, 0.9),
        ("Normal Scene, No Motion", 128, 0.1),
        ("Normal Scene, High Motion", 128, 0.9),
        ("Bright Scene, No Motion", 200, 0.1),
        ("Bright Scene, High Motion", 200, 0.9),
    ]
    
    print("\n" + "-" * 60)
    print(f"{'Scenario':<30} {'TES':<8} {'Time (ms)':<12} {'Gain':<8} {'FPS':<8}")
    print("-" * 60)
    
    for name, brightness, motion in scenarios:
        # Calculate TES
        tes = controller.calculate_tes(brightness)
        
        # Distribute exposure
        exposure_time, gain = controller.distribute_exposure(tes, motion)
        
        fps = 1.0 / exposure_time if exposure_time > 0 else 0
        
        print(f"{name:<30} {tes:<8.2f} {exposure_time*1000:<12.2f} {gain:<8.2f} {fps:<8.1f}")
    
    print("-" * 60)


def demonstrate_trade_offs():
    """
    Demonstrate the trade-off between motion blur and noise.
    """
    print("\n" + "=" * 60)
    print("MOTION BLUR vs NOISE TRADE-OFF")
    print("=" * 60)
    
    controller = ExposureController()
    tes = 3.0  # Need 3x more exposure (dark scene)
    
    print(f"\nScenario: Dark scene requiring {tes}x exposure")
    print("-" * 60)
    print(f"{'Motion Level':<15} {'Time (ms)':<12} {'Gain':<8} {'Trade-off'}")
    print("-" * 60)
    
    motion_levels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    
    for motion in motion_levels:
        exposure_time, gain = controller.distribute_exposure(tes, motion)
        
        if motion < 0.3:
            tradeoff = "Low motion → Longer time, lower gain (less noise)"
        elif motion > 0.7:
            tradeoff = "High motion → Shorter time, higher gain (less blur)"
        else:
            tradeoff = "Balanced"
        
        print(f"{motion:<15.1f} {exposure_time*1000:<12.2f} {gain:<8.2f} {tradeoff}")
    
    print("-" * 60)
    
    print("\nKey Insights:")
    print("1. Low motion → Prefer longer exposure time (less noise)")
    print("2. High motion → Prefer shorter exposure time (less blur)")
    print("3. Gain is adjusted to compensate for time constraints")
    print("4. Maximum gain is limited to prevent excessive noise")


def demonstrate_step_by_step():
    """
    Demonstrate step-by-step exposure calculation.
    """
    print("\n" + "=" * 60)
    print("STEP-BY-STEP EXPOSURE CALCULATION")
    print("=" * 60)
    
    controller = ExposureController()
    
    # Example: Very dark scene with low motion
    current_brightness = 36
    target_brightness = 128
    motion_level = 0.3
    
    print(f"\nGiven:")
    print(f"  Current Brightness: {current_brightness}")
    print(f"  Target Brightness:  {target_brightness}")
    print(f"  Motion Level:       {motion_level}")
    
    # Step 1: Calculate TES
    tes = controller.calculate_tes(current_brightness, target_brightness)
    print(f"\nStep 1: Calculate TES")
    print(f"  TES = {target_brightness} / {current_brightness} = {tes:.2f}")
    
    # Step 2: Calculate motion factor
    motion_factor = 1.0 - (motion_level * 0.5)
    print(f"\nStep 2: Calculate Motion Factor")
    print(f"  motion_factor = 1.0 - ({motion_level} × 0.5) = {motion_factor:.2f}")
    
    # Step 3: Calculate optimal exposure time
    time_range = controller.max_exposure_time - controller.min_exposure_time
    optimal_time = controller.min_exposure_time + time_range * motion_factor
    print(f"\nStep 3: Calculate Optimal Exposure Time")
    print(f"  time_range = {controller.max_exposure_time:.4f} - {controller.min_exposure_time:.4f} = {time_range:.4f}")
    print(f"  optimal_time = {controller.min_exposure_time:.4f} + {time_range:.4f} × {motion_factor:.2f}")
    print(f"  optimal_time = {optimal_time:.4f}s ({optimal_time*1000:.1f}ms)")
    
    # Step 4: Calculate required gain
    required_gain = tes / optimal_time
    print(f"\nStep 4: Calculate Required Gain")
    print(f"  required_gain = {tes:.2f} / {optimal_time:.4f} = {required_gain:.2f}x")
    
    # Step 5: Clamp values
    exposure_time = np.clip(optimal_time, controller.min_exposure_time, controller.max_exposure_time)
    analog_gain = np.clip(required_gain, controller.min_gain, controller.max_gain)
    print(f"\nStep 5: Clamp to Valid Ranges")
    print(f"  exposure_time = clip({optimal_time:.4f}, {controller.min_exposure_time:.4f}, {controller.max_exposure_time:.4f})")
    print(f"  exposure_time = {exposure_time:.4f}s ({exposure_time*1000:.1f}ms)")
    print(f"  analog_gain = clip({required_gain:.2f}, {controller.min_gain:.1f}, {controller.max_gain:.1f})")
    print(f"  analog_gain = {analog_gain:.2f}x")
    
    print(f"\nResult:")
    print(f"  Exposure Time: {exposure_time*1000:.1f}ms ({1/exposure_time:.1f} fps)")
    print(f"  Analog Gain:   {analog_gain:.2f}x")
    print(f"  Effective Exposure: {exposure_time * analog_gain:.4f}")
    
    print("\n" + "=" * 60)


def main():
    """
    Main function demonstrating exposure control.
    """
    print("\n" + "=" * 60)
    print("CHAPTER 8 - EXAMPLE 6: EXPOSURE CONTROL")
    print("=" * 60)
    print("\nThis example demonstrates:")
    print("1. Total Exposure Sensitivity (TES) calculation")
    print("2. Exposure distribution (Time vs Gain)")
    print("3. Motion blur vs noise trade-off")
    print("4. Step-by-step exposure calculation")
    print("\n" + "=" * 60)
    
    demonstrate_tes_calculation()
    demonstrate_exposure_distribution()
    demonstrate_trade_offs()
    demonstrate_step_by_step()
    
    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("=" * 60)
    print("1. TES = target_brightness / current_brightness")
    print("2. High motion → shorter exposure time, higher gain")
    print("3. Low motion → longer exposure time, lower gain")
    print("4. Balance between motion blur and noise")
    print("\n" + "=" * 60)
    print("Next: Run 07_flicker_detection.py to learn about")
    print("      AC flicker detection and mitigation")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
