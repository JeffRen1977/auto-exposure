"""
Chapter 8 - Example 1: Basic Exposure Concepts

This example demonstrates the fundamental concepts of auto exposure:
1. What is exposure? (Exposure Time, Gain, Aperture)
2. How to measure image brightness
3. Basic exposure compensation calculation

Learning Objectives:
- Understand the exposure triangle
- Calculate simple exposure compensation
- See how brightness relates to exposure settings

This corresponds to Section 8.1 in the book.
"""

import numpy as np
import cv2


def calculate_brightness(image):
    """
    Calculate the average brightness of an image.
    
    This is the simplest metric for exposure - just the mean pixel value.
    In a properly exposed image, this should be around 128 (middle gray).
    
    Args:
        image: Input image (grayscale or color)
    
    Returns:
        Average brightness value (0-255)
    """
    if len(image.shape) == 3:
        # Convert color to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    return np.mean(gray)


def calculate_exposure_compensation(current_brightness, target_brightness=128):
    """
    Calculate how much to adjust exposure to reach target brightness.
    
    This is the core of auto exposure: if the image is too dark, we need
    more exposure. If too bright, we need less exposure.
    
    Formula: compensation = target_brightness / current_brightness
    
    Example:
        - Current brightness: 64 (too dark)
        - Target brightness: 128 (middle gray)
        - Compensation: 128 / 64 = 2.0 (need 2x more exposure)
    
    Args:
        current_brightness: Current average brightness (0-255)
        target_brightness: Desired brightness (default: 128 = middle gray)
    
    Returns:
        Exposure compensation factor (1.0 = no change, >1.0 = increase, <1.0 = decrease)
    """
    # Avoid division by zero
    if current_brightness < 1.0:
        current_brightness = 1.0
    
    compensation = target_brightness / current_brightness
    return compensation


def demonstrate_exposure_triangle():
    """
    Demonstrate the exposure triangle: Exposure Time, Gain, and Aperture.
    
    These three parameters control how much light reaches the sensor:
    - Exposure Time: How long the sensor is exposed (shutter speed)
    - Gain: Amplification of the signal (ISO)
    - Aperture: Size of the lens opening (f-number)
    
    All three affect brightness, but have different trade-offs:
    - Longer exposure time → more light, but risk of motion blur
    - Higher gain → more light, but more noise
    - Larger aperture → more light, but shallower depth of field
    """
    print("=" * 60)
    print("EXPOSURE TRIANGLE DEMONSTRATION")
    print("=" * 60)
    
    # Example: We need 2x more light
    compensation_needed = 2.0
    
    print(f"\nScenario: Image is too dark, need {compensation_needed}x more light")
    print("\nOptions to increase exposure:")
    
    # Option 1: Increase exposure time
    current_time = 1/60  # 1/60 second
    new_time = current_time * compensation_needed
    print(f"\n1. Increase Exposure Time:")
    print(f"   Current: {current_time:.4f}s ({1/current_time:.1f} fps)")
    print(f"   New:     {new_time:.4f}s ({1/new_time:.1f} fps)")
    print(f"   Trade-off: Risk of motion blur")
    
    # Option 2: Increase gain
    current_gain = 2.0
    new_gain = current_gain * compensation_needed
    print(f"\n2. Increase Gain (ISO):")
    print(f"   Current: {current_gain:.1f}x")
    print(f"   New:     {new_gain:.1f}x")
    print(f"   Trade-off: More image noise")
    
    # Option 3: Increase aperture (lower f-number)
    current_aperture = 2.8
    # Aperture is f-number, which is inversely related to opening size
    # To double light, we need to halve the f-number (multiply by 1/√2)
    new_aperture = current_aperture / np.sqrt(compensation_needed)
    print(f"\n3. Increase Aperture (open lens more):")
    print(f"   Current: f/{current_aperture:.1f}")
    print(f"   New:     f/{new_aperture:.1f}")
    print(f"   Trade-off: Shallower depth of field")
    
    print("\n" + "=" * 60)


def demonstrate_brightness_measurement():
    """
    Demonstrate how to measure image brightness and calculate compensation.
    """
    print("\n" + "=" * 60)
    print("BRIGHTNESS MEASUREMENT AND COMPENSATION")
    print("=" * 60)
    
    # Create example images with different brightness levels
    scenarios = [
        ("Very Dark", 32),
        ("Dark", 64),
        ("Slightly Dark", 96),
        ("Well Exposed", 128),
        ("Slightly Bright", 160),
        ("Bright", 224),
        ("Very Bright", 240),
    ]
    
    target_brightness = 128  # Middle gray
    
    print(f"\nTarget Brightness: {target_brightness} (middle gray)")
    print("\n" + "-" * 60)
    print(f"{'Scenario':<20} {'Current':<12} {'Compensation':<15} {'Action'}")
    print("-" * 60)
    
    for scenario, brightness in scenarios:
        compensation = calculate_exposure_compensation(brightness, target_brightness)
        
        if compensation > 1.5:
            action = "Significantly increase exposure"
        elif compensation > 1.1:
            action = "Increase exposure"
        elif compensation < 0.7:
            action = "Significantly decrease exposure"
        elif compensation < 0.9:
            action = "Decrease exposure"
        else:
            action = "Well exposed ✓"
        
        print(f"{scenario:<20} {brightness:<12} {compensation:<15.2f} {action}")
    
    print("-" * 60)


def main():
    """
    Main function demonstrating basic exposure concepts.
    """
    print("\n" + "=" * 60)
    print("CHAPTER 8 - EXAMPLE 1: BASIC EXPOSURE CONCEPTS")
    print("=" * 60)
    print("\nThis example demonstrates:")
    print("1. The exposure triangle (Time, Gain, Aperture)")
    print("2. Brightness measurement")
    print("3. Exposure compensation calculation")
    print("\n" + "=" * 60)
    
    # Demonstrate exposure triangle
    demonstrate_exposure_triangle()
    
    # Demonstrate brightness measurement
    demonstrate_brightness_measurement()
    
    # Example with a real image (if available)
    print("\n" + "=" * 60)
    print("PRACTICAL EXAMPLE")
    print("=" * 60)
    
    # Create a synthetic image for demonstration
    # In practice, you would load a real image
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Make it darker for demonstration
    dark_image = (test_image * 0.5).astype(np.uint8)
    
    current_brightness = calculate_brightness(dark_image)
    target_brightness = 128
    
    print(f"\nTest Image Analysis:")
    print(f"  Current Brightness: {current_brightness:.1f}")
    print(f"  Target Brightness:  {target_brightness}")
    
    compensation = calculate_exposure_compensation(current_brightness, target_brightness)
    print(f"  Compensation Needed: {compensation:.2f}x")
    
    if compensation > 1.0:
        print(f"\n  → Image is too dark, need {compensation:.2f}x more exposure")
        print(f"  → Options:")
        print(f"     - Increase exposure time by {compensation:.2f}x")
        print(f"     - Increase gain by {compensation:.2f}x")
        print(f"     - Open aperture by {np.sqrt(compensation):.2f}x")
    elif compensation < 1.0:
        print(f"\n  → Image is too bright, need {1/compensation:.2f}x less exposure")
    else:
        print(f"\n  → Image is well exposed!")
    
    print("\n" + "=" * 60)
    print("Next: Run 02_image_statistics.py to learn about")
    print("      extracting detailed image statistics")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()


