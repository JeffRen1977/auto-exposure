"""
Chapter 8 - Example 2: Image Statistics Extraction

This example demonstrates how to extract detailed statistics from images
for auto exposure analysis:
1. Bayer statistics (grid-based sampling)
2. Histogram generation
3. Saturated pixel detection
4. Brightness distribution analysis

Learning Objectives:
- Understand Bayer statistics format
- Generate and interpret histograms
- Detect over/under exposure from statistics
- Extract spatial brightness information

This corresponds to Section 8.2 in the book.
"""

import numpy as np
import cv2
from typing import Tuple, Dict


def extract_bayer_statistics(image: np.ndarray, grid_size: Tuple[int, int] = (64, 48)) -> np.ndarray:
    """
    Extract Bayer statistics from an image using a grid-based approach.
    
    In real camera systems, the sensor provides statistics in a grid format
    (e.g., 64x48) rather than processing every pixel. This is much more efficient
    for real-time processing.
    
    The grid contains average brightness values for each region, which we can
    use to understand the spatial distribution of light in the scene.
    
    Args:
        image: Input image (grayscale or color)
        grid_size: Size of the statistics grid (width, height)
    
    Returns:
        Grid of average brightness values
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Resize to grid size - this gives us average values for each grid cell
    # In real systems, this is done in hardware on the sensor
    bayer_stats = cv2.resize(gray, grid_size, interpolation=cv2.INTER_AREA)
    
    return bayer_stats


def generate_histogram(image: np.ndarray, bins: int = 256) -> np.ndarray:
    """
    Generate a histogram of pixel brightness values.
    
    Histograms show the distribution of brightness in the image:
    - Left side = dark pixels
    - Right side = bright pixels
    - Height = number of pixels at that brightness
    
    A well-exposed image typically has a histogram centered around middle gray (128).
    
    Args:
        image: Input image (grayscale or color)
        bins: Number of histogram bins (default: 256 for 8-bit images)
    
    Returns:
        Histogram array (count of pixels at each brightness level)
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Calculate histogram
    histogram = cv2.calcHist([gray], [0], None, [bins], [0, 256])
    
    return histogram.flatten()


def detect_saturated_pixels(image: np.ndarray, 
                           highlight_threshold: int = 250,
                           shadow_threshold: int = 5) -> Dict[str, int]:
    """
    Detect saturated (clipped) pixels in highlights and shadows.
    
    Saturated pixels are pixels that have reached the maximum or minimum
    brightness value and cannot represent the true scene brightness.
    
    - Highlight saturation: Pixels at maximum brightness (255 or near it)
    - Shadow saturation: Pixels at minimum brightness (0 or near it)
    
    Too many saturated pixels indicate over/under exposure.
    
    Args:
        image: Input image
        highlight_threshold: Brightness value above which pixels are considered saturated
        shadow_threshold: Brightness value below which pixels are considered saturated
    
    Returns:
        Dictionary with counts of saturated pixels
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    total_pixels = gray.size
    
    # Count saturated pixels
    highlight_saturated = np.sum(gray >= highlight_threshold)
    shadow_saturated = np.sum(gray <= shadow_threshold)
    
    return {
        'highlight_saturated': int(highlight_saturated),
        'shadow_saturated': int(shadow_saturated),
        'highlight_ratio': highlight_saturated / total_pixels,
        'shadow_ratio': shadow_saturated / total_pixels,
        'total_pixels': total_pixels
    }


def analyze_brightness_distribution(bayer_stats: np.ndarray) -> Dict[str, float]:
    """
    Analyze the spatial distribution of brightness.
    
    This function calculates statistics about how brightness is distributed
    across the image, which helps understand the scene characteristics.
    
    Args:
        bayer_stats: Grid of brightness statistics
    
    Returns:
        Dictionary with distribution statistics
    """
    return {
        'mean': float(np.mean(bayer_stats)),
        'std': float(np.std(bayer_stats)),
        'min': float(np.min(bayer_stats)),
        'max': float(np.max(bayer_stats)),
        'median': float(np.median(bayer_stats)),
        'q25': float(np.percentile(bayer_stats, 25)),
        'q75': float(np.percentile(bayer_stats, 75)),
    }


def demonstrate_statistics_extraction():
    """
    Demonstrate extracting and analyzing image statistics.
    """
    print("\n" + "=" * 60)
    print("IMAGE STATISTICS EXTRACTION DEMONSTRATION")
    print("=" * 60)
    
    # Create test images with different characteristics
    print("\n1. Creating test images...")
    
    # Well-exposed image
    well_exposed = np.random.normal(128, 30, (480, 640)).astype(np.uint8)
    well_exposed = np.clip(well_exposed, 0, 255)
    
    # Over-exposed image (too bright)
    over_exposed = np.random.normal(200, 20, (480, 640)).astype(np.uint8)
    over_exposed = np.clip(over_exposed, 0, 255)
    
    # Under-exposed image (too dark)
    under_exposed = np.random.normal(60, 20, (480, 640)).astype(np.uint8)
    under_exposed = np.clip(under_exposed, 0, 255)
    
    images = [
        ("Well Exposed", well_exposed),
        ("Over Exposed", over_exposed),
        ("Under Exposed", under_exposed),
    ]
    
    print("\n2. Extracting Bayer Statistics (64x48 grid)...")
    print("-" * 60)
    
    for name, image in images:
        # Extract Bayer statistics
        bayer_stats = extract_bayer_statistics(image, grid_size=(64, 48))
        
        # Analyze distribution
        distribution = analyze_brightness_distribution(bayer_stats)
        
        print(f"\n{name}:")
        print(f"  Grid Size: {bayer_stats.shape}")
        print(f"  Mean Brightness: {distribution['mean']:.1f}")
        print(f"  Std Deviation: {distribution['std']:.1f}")
        print(f"  Range: {distribution['min']:.0f} - {distribution['max']:.0f}")
        print(f"  Median: {distribution['median']:.1f}")
        print(f"  IQR (Q25-Q75): {distribution['q25']:.1f} - {distribution['q75']:.1f}")
    
    print("\n" + "-" * 60)
    print("\n3. Generating Histograms...")
    print("-" * 60)
    
    for name, image in images:
        histogram = generate_histogram(image)
        
        # Find key percentiles
        cumsum = np.cumsum(histogram)
        total = cumsum[-1]
        
        p5 = np.argmax(cumsum >= total * 0.05)
        p50 = np.argmax(cumsum >= total * 0.50)
        p95 = np.argmax(cumsum >= total * 0.95)
        
        print(f"\n{name} Histogram:")
        print(f"  Median (p50): {p50}")
        print(f"  5th percentile: {p5}")
        print(f"  95th percentile: {p95}")
        print(f"  Dynamic range: {p95 - p5}")
    
    print("\n" + "-" * 60)
    print("\n4. Detecting Saturated Pixels...")
    print("-" * 60)
    
    for name, image in images:
        saturation = detect_saturated_pixels(image)
        
        print(f"\n{name}:")
        print(f"  Highlight Saturated: {saturation['highlight_saturated']:,} "
              f"({saturation['highlight_ratio']*100:.1f}%)")
        print(f"  Shadow Saturated: {saturation['shadow_saturated']:,} "
              f"({saturation['shadow_ratio']*100:.1f}%)")
        
        if saturation['highlight_ratio'] > 0.1:
            print(f"  ⚠️  Warning: High highlight saturation - image may be over-exposed")
        if saturation['shadow_ratio'] > 0.1:
            print(f"  ⚠️  Warning: High shadow saturation - image may be under-exposed")
    
    print("\n" + "=" * 60)


def main():
    """
    Main function demonstrating image statistics extraction.
    """
    print("\n" + "=" * 60)
    print("CHAPTER 8 - EXAMPLE 2: IMAGE STATISTICS EXTRACTION")
    print("=" * 60)
    print("\nThis example demonstrates:")
    print("1. Bayer statistics extraction (grid-based)")
    print("2. Histogram generation and analysis")
    print("3. Saturated pixel detection")
    print("4. Brightness distribution analysis")
    print("\n" + "=" * 60)
    
    demonstrate_statistics_extraction()
    
    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("=" * 60)
    print("1. Bayer statistics provide efficient spatial brightness information")
    print("2. Histograms show the distribution of brightness values")
    print("3. Saturated pixels indicate over/under exposure")
    print("4. Distribution statistics help understand scene characteristics")
    print("\n" + "=" * 60)
    print("Next: Run 03_spatial_analysis.py to learn about")
    print("      center-weighted metering and exposure zones")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()


