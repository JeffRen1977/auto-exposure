"""
Chapter 8 - Example 8: APEX Calculation

This example demonstrates APEX (Additive System of Photographic Exposure) values:
1. APEX system fundamentals
2. Bv, Av, Tv, Sv calculation
3. EXIF metadata generation
4. APEX value relationships

Learning Objectives:
- Understand the APEX system
- Calculate Bv (Brightness), Av (Aperture), Tv (Time), Sv (Sensitivity)
- Generate EXIF metadata
- Use APEX values for exposure control

This corresponds to Section 8.7 in the book.
"""

import math
from typing import Dict


def calculate_brightness_value(exposure_time: float, gain: float, aperture: float) -> float:
    """
    Calculate Brightness Value (Bv).
    
    Bv represents the overall scene brightness in APEX units.
    
    Formula: Bv = log₂(exposure_time × gain × aperture)
    
    Args:
        exposure_time: Exposure time in seconds
        gain: Analog gain (ISO/100)
        aperture: F-number (e.g., 2.8)
    
    Returns:
        Brightness Value (Bv)
    """
    bv = math.log2(exposure_time * gain * aperture)
    return bv


def calculate_aperture_value(aperture: float) -> float:
    """
    Calculate Aperture Value (Av).
    
    Av represents the aperture setting in APEX units.
    
    Formula: Av = log₂(f-number²)
    
    Larger Av = smaller aperture (higher f-number)
    
    Args:
        aperture: F-number (e.g., 2.8)
    
    Returns:
        Aperture Value (Av)
    """
    av = math.log2(aperture * aperture)
    return av


def calculate_time_value(exposure_time: float) -> float:
    """
    Calculate Time Value (Tv).
    
    Tv represents the shutter speed in APEX units.
    
    Formula: Tv = -log₂(exposure_time)
    
    Larger Tv = faster shutter (shorter exposure time)
    
    Args:
        exposure_time: Exposure time in seconds
    
    Returns:
        Time Value (Tv)
    """
    tv = -math.log2(exposure_time)
    return tv


def calculate_sensitivity_value(gain: float, base_iso: int = 100) -> float:
    """
    Calculate Sensitivity Value (Sv).
    
    Sv represents the ISO sensitivity in APEX units.
    
    Formula: Sv = log₂(ISO)
    
    Using gain × base_iso as ISO equivalent.
    
    Args:
        gain: Analog gain
        base_iso: Base ISO (default: 100)
    
    Returns:
        Sensitivity Value (Sv)
    """
    iso = gain * base_iso
    sv = math.log2(iso)
    return sv


def calculate_all_apex_values(exposure_time: float, gain: float, aperture: float) -> Dict[str, float]:
    """
    Calculate all APEX values.
    
    Args:
        exposure_time: Exposure time in seconds
        gain: Analog gain
        aperture: F-number
    
    Returns:
        Dictionary with all APEX values
    """
    return {
        'bv': calculate_brightness_value(exposure_time, gain, aperture),
        'av': calculate_aperture_value(aperture),
        'tv': calculate_time_value(exposure_time),
        'sv': calculate_sensitivity_value(gain)
    }


def demonstrate_apex_fundamentals():
    """
    Demonstrate APEX system fundamentals.
    """
    print("\n" + "=" * 60)
    print("APEX SYSTEM FUNDAMENTALS")
    print("=" * 60)
    
    print("\nAPEX (Additive System of Photographic Exposure):")
    print("  - Logarithmic system for exposure values")
    print("  - Values can be added/subtracted (additive)")
    print("  - Used in EXIF metadata")
    print("  - Standardized exposure representation")
    
    print("\nAPEX Values:")
    print("-" * 60)
    print("  Bv (Brightness Value):  Scene brightness")
    print("  Av (Aperture Value):    Aperture setting")
    print("  Tv (Time Value):        Shutter speed")
    print("  Sv (Sensitivity Value): ISO sensitivity")
    
    print("\nAPEX Relationship:")
    print("  Bv = Av + Tv - Sv")
    print("  (Brightness = Aperture + Time - Sensitivity)")
    
    print("\n" + "=" * 60)


def demonstrate_apex_calculations():
    """
    Demonstrate APEX value calculations for different exposure settings.
    """
    print("\n" + "=" * 60)
    print("APEX VALUE CALCULATIONS")
    print("=" * 60)
    
    # Test scenarios
    scenarios = [
        ("Bright Daylight", 1/1000, 1.0, 2.8),
        ("Normal Daylight", 1/250, 1.0, 2.8),
        ("Indoor", 1/60, 2.0, 2.8),
        ("Low Light", 1/30, 4.0, 2.8),
        ("Very Low Light", 1/15, 8.0, 2.8),
    ]
    
    print("\n" + "-" * 60)
    print(f"{'Scenario':<20} {'Time':<12} {'Gain':<8} {'Aperture':<10} {'Bv':<8} {'Av':<8} {'Tv':<8} {'Sv':<8}")
    print("-" * 60)
    
    for name, exp_time, gain, aperture in scenarios:
        apex = calculate_all_apex_values(exp_time, gain, aperture)
        
        time_str = f"1/{int(1/exp_time)}" if exp_time < 1 else f"{exp_time:.3f}"
        
        print(f"{name:<20} {time_str:<12} {gain:<8.1f} f/{aperture:<9.1f} "
              f"{apex['bv']:<8.2f} {apex['av']:<8.2f} {apex['tv']:<8.2f} {apex['sv']:<8.2f}")
    
    print("-" * 60)


def demonstrate_apex_relationships():
    """
    Demonstrate relationships between APEX values.
    """
    print("\n" + "=" * 60)
    print("APEX VALUE RELATIONSHIPS")
    print("=" * 60)
    
    # Example: Same brightness with different settings
    print("\nExample: Maintaining same brightness (Bv) with different settings")
    print("-" * 60)
    
    # Scenario 1: Fast shutter, high ISO
    exp_time1 = 1/500
    gain1 = 4.0
    aperture1 = 2.8
    apex1 = calculate_all_apex_values(exp_time1, gain1, aperture1)
    
    # Scenario 2: Slow shutter, low ISO (same brightness)
    # Bv = Av + Tv - Sv
    # To maintain same Bv, if we change Tv, we must adjust Sv
    exp_time2 = 1/125  # 2 stops slower (Tv decreases by 2)
    gain2 = 1.0  # 2 stops lower ISO (Sv decreases by 2)
    aperture2 = 2.8
    apex2 = calculate_all_apex_values(exp_time2, gain2, aperture2)
    
    print(f"\nScenario 1: Fast shutter, high ISO")
    print(f"  Exposure: 1/{int(1/exp_time1)}, Gain: {gain1}x, Aperture: f/{aperture1}")
    print(f"  Bv = {apex1['bv']:.2f}, Av = {apex1['av']:.2f}, Tv = {apex1['tv']:.2f}, Sv = {apex1['sv']:.2f}")
    
    print(f"\nScenario 2: Slow shutter, low ISO")
    print(f"  Exposure: 1/{int(1/exp_time2)}, Gain: {gain2}x, Aperture: f/{aperture2}")
    print(f"  Bv = {apex2['bv']:.2f}, Av = {apex2['av']:.2f}, Tv = {apex2['tv']:.2f}, Sv = {apex2['sv']:.2f}")
    
    print(f"\nRelationship Check:")
    print(f"  Bv1 = Av1 + Tv1 - Sv1 = {apex1['av']:.2f} + {apex1['tv']:.2f} - {apex1['sv']:.2f} = {apex1['av'] + apex1['tv'] - apex1['sv']:.2f}")
    print(f"  Bv2 = Av2 + Tv2 - Sv2 = {apex2['av']:.2f} + {apex2['tv']:.2f} - {apex2['sv']:.2f} = {apex2['av'] + apex2['tv'] - apex2['sv']:.2f}")
    print(f"  Bv values are {'equal ✓' if abs(apex1['bv'] - apex2['bv']) < 0.01 else 'different'}")
    
    print("\n" + "=" * 60)


def demonstrate_exif_generation():
    """
    Demonstrate EXIF metadata generation from APEX values.
    """
    print("\n" + "=" * 60)
    print("EXIF METADATA GENERATION")
    print("=" * 60)
    
    # Example exposure settings
    exposure_time = 1/60
    gain = 2.0
    aperture = 2.8
    base_iso = 100
    
    apex = calculate_all_apex_values(exposure_time, gain, aperture)
    iso = gain * base_iso
    
    print(f"\nExposure Settings:")
    print(f"  Exposure Time: {exposure_time:.4f}s (1/{int(1/exposure_time)})")
    print(f"  Gain: {gain:.1f}x")
    print(f"  Aperture: f/{aperture:.1f}")
    print(f"  ISO: {int(iso)}")
    
    print(f"\nAPEX Values:")
    print(f"  Bv (Brightness):  {apex['bv']:.2f}")
    print(f"  Av (Aperture):    {apex['av']:.2f}")
    print(f"  Tv (Time):        {apex['tv']:.2f}")
    print(f"  Sv (Sensitivity): {apex['sv']:.2f}")
    
    print(f"\nEXIF Metadata (example):")
    print("-" * 60)
    print(f"  EXIF ExposureTime:     {exposure_time:.6f}")
    print(f"  EXIF FNumber:          {aperture:.1f}")
    print(f"  EXIF ISOSpeedRatings:  {int(iso)}")
    print(f"  EXIF BrightnessValue:  {apex['bv']:.2f}")
    print(f"  EXIF ApertureValue:    {apex['av']:.2f}")
    print(f"  EXIF ShutterSpeedValue: {apex['tv']:.2f}")
    print(f"  EXIF SensitivityType:  {int(apex['sv']):.0f}")
    
    print("\n" + "=" * 60)


def main():
    """
    Main function demonstrating APEX calculation.
    """
    print("\n" + "=" * 60)
    print("CHAPTER 8 - EXAMPLE 8: APEX CALCULATION")
    print("=" * 60)
    print("\nThis example demonstrates:")
    print("1. APEX system fundamentals")
    print("2. Bv, Av, Tv, Sv calculation")
    print("3. APEX value relationships")
    print("4. EXIF metadata generation")
    print("\n" + "=" * 60)
    
    demonstrate_apex_fundamentals()
    demonstrate_apex_calculations()
    demonstrate_apex_relationships()
    demonstrate_exif_generation()
    
    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("=" * 60)
    print("1. APEX uses logarithmic scale for exposure values")
    print("2. Bv = Av + Tv - Sv (additive relationship)")
    print("3. APEX values are used in EXIF metadata")
    print("4. Values can be added/subtracted for exposure compensation")
    print("\n" + "=" * 60)
    print("Next: Run 09_complete_ae_system.py to see")
    print("      the complete auto exposure pipeline")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()


