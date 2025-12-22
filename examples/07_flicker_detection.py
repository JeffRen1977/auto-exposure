"""
Chapter 8 - Example 7: Flicker Detection

This example demonstrates AC flicker detection and mitigation:
1. Understanding AC flicker (50Hz/60Hz)
2. Flicker detection algorithm
3. Exposure time adjustment to avoid flicker
4. Safe exposure times for different AC frequencies

Learning Objectives:
- Understand AC lighting flicker
- Detect flicker from exposure time
- Adjust exposure times to avoid banding artifacts
- Calculate safe exposure times

This corresponds to Section 8.7 in the book.
"""

import numpy as np
from typing import List, Tuple


class FlickerDetector:
    """
    Detects and mitigates AC flicker in artificial lighting.
    
    AC-powered lights flicker at 2× the power frequency:
    - 50Hz AC → 100Hz flicker (10ms period)
    - 60Hz AC → 120Hz flicker (8.33ms period)
    
    If exposure time matches the flicker period, banding artifacts appear.
    """
    
    def __init__(self, flicker_frequencies: List[int] = None):
        """
        Initialize flicker detector.
        
        Args:
            flicker_frequencies: List of AC frequencies to detect (default: [50, 60])
        """
        if flicker_frequencies is None:
            flicker_frequencies = [50, 60]
        self.flicker_frequencies = flicker_frequencies
        self.detection_threshold = 0.1  # 100ms threshold
    
    def detect_flicker(self, exposure_time: float) -> bool:
        """
        Detect if exposure time causes flicker.
        
        Flicker occurs when exposure time is close to a flicker period.
        We check if exposure time is within threshold of any flicker period.
        
        Args:
            exposure_time: Exposure time in seconds
        
        Returns:
            True if flicker detected, False otherwise
        """
        for freq in self.flicker_frequencies:
            # Flicker frequency is 2× AC frequency
            flicker_freq = freq * 2
            period = 1.0 / flicker_freq
            
            # Check if exposure time is close to flicker period
            if abs(exposure_time - period) < self.detection_threshold:
                return True
        
        return False
    
    def adjust_for_flicker(self, exposure_time: float) -> float:
        """
        Adjust exposure time to avoid flicker.
        
        Strategy:
        - If exposure time is less than period → use half period
        - If exposure time is greater than period → use 1.5× period
        
        Safe exposure times are multiples of half-period:
        - 50Hz: 10ms, 20ms, 30ms, 40ms, etc.
        - 60Hz: 8.33ms, 16.67ms, 25ms, 33.33ms, etc.
        
        Args:
            exposure_time: Original exposure time in seconds
        
        Returns:
            Adjusted exposure time in seconds
        """
        for freq in self.flicker_frequencies:
            flicker_freq = freq * 2
            period = 1.0 / flicker_freq
            
            if abs(exposure_time - period) < self.detection_threshold:
                # Adjust to avoid flicker period
                if exposure_time < period:
                    return period * 0.5  # Use half period
                else:
                    return period * 1.5  # Use 1.5× period
        
        return exposure_time  # No adjustment needed
    
    def get_safe_exposure_times(self, max_time: float = 0.1) -> List[float]:
        """
        Get list of safe exposure times that avoid flicker.
        
        Safe times are multiples of half-period for all frequencies.
        
        Args:
            max_time: Maximum exposure time to consider (seconds)
        
        Returns:
            List of safe exposure times
        """
        safe_times = []
        
        for freq in self.flicker_frequencies:
            flicker_freq = freq * 2
            half_period = 1.0 / (flicker_freq * 2)
            
            # Generate multiples of half-period
            time = half_period
            while time <= max_time:
                safe_times.append(time)
                time += half_period
        
        # Remove duplicates and sort
        safe_times = sorted(list(set(safe_times)))
        
        return safe_times


def demonstrate_flicker_fundamentals():
    """
    Demonstrate AC flicker fundamentals.
    """
    print("\n" + "=" * 60)
    print("AC FLICKER FUNDAMENTALS")
    print("=" * 60)
    
    print("\nAC Power Frequencies:")
    print("-" * 60)
    print(f"{'AC Frequency':<20} {'Flicker Frequency':<20} {'Period (ms)':<15}")
    print("-" * 60)
    
    for ac_freq in [50, 60]:
        flicker_freq = ac_freq * 2
        period_ms = (1.0 / flicker_freq) * 1000
        print(f"{ac_freq} Hz{'':<15} {flicker_freq} Hz{'':<15} {period_ms:.2f} ms")
    
    print("\nWhy Flicker Occurs:")
    print("  AC power alternates direction, causing light intensity to vary")
    print("  Light flickers at 2× the AC frequency (full cycle)")
    print("  If camera exposure matches flicker period, banding appears")
    
    print("\n" + "=" * 60)


def demonstrate_flicker_detection():
    """
    Demonstrate flicker detection for various exposure times.
    """
    print("\n" + "=" * 60)
    print("FLICKER DETECTION")
    print("=" * 60)
    
    detector = FlickerDetector()
    
    # Test various exposure times
    test_times = [
        0.001,   # 1ms
        0.008,   # 8ms (close to 60Hz flicker)
        0.010,   # 10ms (50Hz flicker period)
        0.0167,  # 16.7ms (60Hz flicker period)
        0.020,   # 20ms
        0.033,   # 33ms
        0.050,   # 50ms
    ]
    
    print("\n" + "-" * 60)
    print(f"{'Exposure Time':<20} {'Has Flicker':<15} {'Adjusted Time (ms)':<20}")
    print("-" * 60)
    
    for exp_time in test_times:
        has_flicker = detector.detect_flicker(exp_time)
        adjusted = detector.adjust_for_flicker(exp_time)
        
        flicker_status = "Yes ⚠️" if has_flicker else "No ✓"
        
        print(f"{exp_time*1000:>6.2f} ms{'':<10} {flicker_status:<15} {adjusted*1000:>6.2f} ms")
    
    print("-" * 60)


def demonstrate_safe_exposure_times():
    """
    Demonstrate safe exposure times for different AC frequencies.
    """
    print("\n" + "=" * 60)
    print("SAFE EXPOSURE TIMES")
    print("=" * 60)
    
    # For 50Hz AC
    detector_50 = FlickerDetector([50])
    safe_50 = detector_50.get_safe_exposure_times(max_time=0.1)
    
    print("\n50Hz AC Lighting (100Hz flicker, 10ms period):")
    print("-" * 60)
    print("Safe exposure times (multiples of 5ms):")
    for i, time in enumerate(safe_50[:10]):  # Show first 10
        print(f"  {time*1000:>6.2f} ms ({1/time:.1f} fps)", end="")
        if (i + 1) % 3 == 0:
            print()  # New line every 3 items
    if len(safe_50) > 10:
        print(f"\n  ... and {len(safe_50)-10} more")
    print()
    
    # For 60Hz AC
    detector_60 = FlickerDetector([60])
    safe_60 = detector_60.get_safe_exposure_times(max_time=0.1)
    
    print("60Hz AC Lighting (120Hz flicker, 8.33ms period):")
    print("-" * 60)
    print("Safe exposure times (multiples of 4.17ms):")
    for i, time in enumerate(safe_60[:10]):  # Show first 10
        print(f"  {time*1000:>6.2f} ms ({1/time:.1f} fps)", end="")
        if (i + 1) % 3 == 0:
            print()  # New line every 3 items
    if len(safe_60) > 10:
        print(f"\n  ... and {len(safe_60)-10} more")
    print()
    
    # For both frequencies
    detector_both = FlickerDetector([50, 60])
    safe_both = detector_both.get_safe_exposure_times(max_time=0.1)
    
    print("Safe for both 50Hz and 60Hz:")
    print("-" * 60)
    print("Common safe exposure times:")
    for i, time in enumerate(safe_both[:10]):
        print(f"  {time*1000:>6.2f} ms ({1/time:.1f} fps)", end="")
        if (i + 1) % 3 == 0:
            print()
    if len(safe_both) > 10:
        print(f"\n  ... and {len(safe_both)-10} more")
    print()
    
    print("\n" + "=" * 60)


def demonstrate_flicker_mitigation():
    """
    Demonstrate flicker mitigation in practice.
    """
    print("\n" + "=" * 60)
    print("FLICKER MITIGATION IN PRACTICE")
    print("=" * 60)
    
    detector = FlickerDetector([50, 60])
    
    # Simulate exposure calculation that might cause flicker
    problematic_times = [
        (0.010, "10ms - matches 50Hz flicker period"),
        (0.0167, "16.7ms - matches 60Hz flicker period"),
        (0.020, "20ms - close to 50Hz period"),
        (0.0083, "8.3ms - close to 60Hz period"),
    ]
    
    print("\nProblematic Exposure Times:")
    print("-" * 60)
    print(f"{'Original (ms)':<15} {'Issue':<35} {'Adjusted (ms)':<15} {'FPS':<10}")
    print("-" * 60)
    
    for orig_time, issue in problematic_times:
        has_flicker = detector.detect_flicker(orig_time)
        adjusted = detector.adjust_for_flicker(orig_time)
        fps_orig = 1.0 / orig_time
        fps_adj = 1.0 / adjusted
        
        if has_flicker:
            print(f"{orig_time*1000:>6.2f}{'':<8} {issue:<35} {adjusted*1000:>6.2f}{'':<8} {fps_adj:>6.1f}")
        else:
            print(f"{orig_time*1000:>6.2f}{'':<8} {issue:<35} {orig_time*1000:>6.2f} (no change) {fps_orig:>6.1f}")
    
    print("-" * 60)
    
    print("\nKey Points:")
    print("1. Flicker detection is automatic")
    print("2. Exposure times are adjusted to safe values")
    print("3. Frame rate may change slightly")
    print("4. Banding artifacts are prevented")


def main():
    """
    Main function demonstrating flicker detection.
    """
    print("\n" + "=" * 60)
    print("CHAPTER 8 - EXAMPLE 7: FLICKER DETECTION")
    print("=" * 60)
    print("\nThis example demonstrates:")
    print("1. AC flicker fundamentals (50Hz/60Hz)")
    print("2. Flicker detection algorithm")
    print("3. Safe exposure times")
    print("4. Flicker mitigation in practice")
    print("\n" + "=" * 60)
    
    demonstrate_flicker_fundamentals()
    demonstrate_flicker_detection()
    demonstrate_safe_exposure_times()
    demonstrate_flicker_mitigation()
    
    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("=" * 60)
    print("1. AC lights flicker at 2× power frequency")
    print("2. Exposure times matching flicker period cause banding")
    print("3. Safe times are multiples of half-period")
    print("4. Automatic adjustment prevents artifacts")
    print("\n" + "=" * 60)
    print("Next: Run 08_apex_calculation.py to learn about")
    print("      APEX values and EXIF metadata")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()


