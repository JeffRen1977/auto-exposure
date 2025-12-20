"""
Chapter 8 - Example 4: Histogram Analysis

This example demonstrates histogram-based exposure analysis:
1. Histogram generation and interpretation
2. Dynamic range calculation
3. Exposure bias detection
4. Shannon entropy calculation

Learning Objectives:
- Understand histogram interpretation
- Calculate dynamic range from percentiles
- Detect exposure bias (over/under exposure)
- Use entropy as a measure of image complexity

This corresponds to Section 8.4 in the book.
"""

import numpy as np
import cv2
from typing import Dict


def generate_histogram(image: np.ndarray, bins: int = 256) -> np.ndarray:
    """
    Generate a histogram of pixel brightness values.
    
    Histograms show the distribution of brightness in the image:
    - Left side (low values) = dark pixels
    - Right side (high values) = bright pixels
    - Height = number of pixels at that brightness level
    
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


def calculate_percentiles(histogram: np.ndarray) -> Dict[str, int]:
    """
    Calculate key percentiles from histogram.
    
    Percentiles help understand the distribution:
    - p5: 5% of pixels are darker than this
    - p50 (median): Half of pixels are darker, half brighter
    - p95: 95% of pixels are darker than this
    
    Args:
        histogram: Histogram array
    
    Returns:
        Dictionary with percentile values
    """
    # Normalize histogram to probability distribution
    hist_norm = histogram / np.sum(histogram)
    
    # Calculate cumulative distribution function (CDF)
    cumsum = np.cumsum(hist_norm)
    
    # Find percentiles
    p5 = np.argmax(cumsum >= 0.05)
    p25 = np.argmax(cumsum >= 0.25)
    p50 = np.argmax(cumsum >= 0.50)
    p75 = np.argmax(cumsum >= 0.75)
    p95 = np.argmax(cumsum >= 0.95)
    
    return {
        'p5': int(p5),
        'p25': int(p25),
        'p50': int(p50),
        'p75': int(p75),
        'p95': int(p95)
    }


def calculate_dynamic_range(histogram: np.ndarray) -> Dict[str, float]:
    """
    Calculate dynamic range from histogram.
    
    Dynamic range measures the spread of brightness values:
    - High dynamic range = wide range of brightness (high contrast)
    - Low dynamic range = narrow range (low contrast)
    
    We use the 5th to 95th percentile range to avoid outliers.
    
    Args:
        histogram: Histogram array
    
    Returns:
        Dictionary with dynamic range metrics
    """
    percentiles = calculate_percentiles(histogram)
    
    # Dynamic range: spread between 5th and 95th percentiles
    dynamic_range = percentiles['p95'] - percentiles['p5']
    
    # Interquartile range (IQR): spread between 25th and 75th percentiles
    iqr = percentiles['p75'] - percentiles['p25']
    
    return {
        'dynamic_range': float(dynamic_range),
        'iqr': float(iqr),
        'p5': percentiles['p5'],
        'p95': percentiles['p95'],
        'p25': percentiles['p25'],
        'p75': percentiles['p75']
    }


def calculate_exposure_bias(histogram: np.ndarray) -> float:
    """
    Calculate exposure bias from histogram.
    
    Exposure bias indicates if the image is over or under exposed:
    - Positive bias: Image is too bright (overexposed)
    - Negative bias: Image is too dark (underexposed)
    - Near zero: Well exposed
    
    Formula: (median - 128) / 128
    - 128 is middle gray (ideal exposure)
    
    Args:
        histogram: Histogram array
    
    Returns:
        Exposure bias value (-1.0 to 1.0)
    """
    percentiles = calculate_percentiles(histogram)
    median = percentiles['p50']
    
    # Calculate bias: how far median is from middle gray (128)
    exposure_bias = (median - 128) / 128.0
    
    return float(exposure_bias)


def calculate_entropy(histogram: np.ndarray) -> float:
    """
    Calculate Shannon entropy of the histogram.
    
    Entropy measures the information content and complexity of the image:
    - High entropy (>7.5): High detail, texture, complexity
    - Low entropy (<5): Low detail, smooth regions, simple scenes
    
    Formula: Entropy = -Σ(p(i) × log₂(p(i)))
    where p(i) is the probability of brightness level i
    
    Args:
        histogram: Histogram array
    
    Returns:
        Entropy value (bits)
    """
    # Normalize to probability distribution
    hist_norm = histogram / np.sum(histogram)
    
    # Remove zero bins (log(0) is undefined)
    hist_norm = hist_norm[hist_norm > 0]
    
    # Calculate entropy
    entropy = -np.sum(hist_norm * np.log2(hist_norm))
    
    return float(entropy)


def analyze_histogram(image: np.ndarray) -> Dict[str, float]:
    """
    Complete histogram analysis for exposure assessment.
    
    Args:
        image: Input image
    
    Returns:
        Dictionary with all histogram metrics
    """
    # Generate histogram
    histogram = generate_histogram(image)
    
    # Calculate metrics
    percentiles = calculate_percentiles(histogram)
    dynamic_range_metrics = calculate_dynamic_range(histogram)
    exposure_bias = calculate_exposure_bias(histogram)
    entropy = calculate_entropy(histogram)
    
    return {
        'p5': percentiles['p5'],
        'p25': percentiles['p25'],
        'p50': percentiles['p50'],
        'p75': percentiles['p75'],
        'p95': percentiles['p95'],
        'dynamic_range': dynamic_range_metrics['dynamic_range'],
        'iqr': dynamic_range_metrics['iqr'],
        'exposure_bias': exposure_bias,
        'entropy': entropy
    }


def demonstrate_histogram_analysis():
    """
    Demonstrate histogram analysis techniques.
    """
    print("\n" + "=" * 60)
    print("HISTOGRAM ANALYSIS DEMONSTRATION")
    print("=" * 60)
    
    # Create test images with different exposure characteristics
    print("\n1. Creating test images...")
    
    # Well-exposed image (centered histogram)
    well_exposed = np.random.normal(128, 30, (480, 640)).astype(np.uint8)
    well_exposed = np.clip(well_exposed, 0, 255)
    
    # Over-exposed image (histogram shifted right)
    over_exposed = np.random.normal(200, 20, (480, 640)).astype(np.uint8)
    over_exposed = np.clip(over_exposed, 0, 255)
    
    # Under-exposed image (histogram shifted left)
    under_exposed = np.random.normal(60, 20, (480, 640)).astype(np.uint8)
    under_exposed = np.clip(under_exposed, 0, 255)
    
    # High contrast image (wide histogram)
    high_contrast = np.concatenate([
        np.random.normal(50, 10, (240, 640)).astype(np.uint8),
        np.random.normal(200, 10, (240, 640)).astype(np.uint8)
    ])
    high_contrast = np.clip(high_contrast, 0, 255)
    
    # Low contrast image (narrow histogram)
    low_contrast = np.random.normal(128, 10, (480, 640)).astype(np.uint8)
    low_contrast = np.clip(low_contrast, 0, 255)
    
    images = [
        ("Well Exposed", well_exposed),
        ("Over Exposed", over_exposed),
        ("Under Exposed", under_exposed),
        ("High Contrast", high_contrast),
        ("Low Contrast", low_contrast),
    ]
    
    print("\n2. Histogram Percentiles...")
    print("-" * 60)
    
    for name, image in images:
        analysis = analyze_histogram(image)
        
        print(f"\n{name}:")
        print(f"  5th percentile:  {analysis['p5']:3d}")
        print(f"  25th percentile: {analysis['p25']:3d}")
        print(f"  50th percentile: {analysis['p50']:3d} (median)")
        print(f"  75th percentile: {analysis['p75']:3d}")
        print(f"  95th percentile: {analysis['p95']:3d}")
    
    print("\n" + "-" * 60)
    print("\n3. Dynamic Range Analysis...")
    print("-" * 60)
    
    for name, image in images:
        analysis = analyze_histogram(image)
        
        print(f"\n{name}:")
        print(f"  Dynamic Range (p5-p95): {analysis['dynamic_range']:.1f}")
        print(f"  IQR (p25-p75):          {analysis['iqr']:.1f}")
        
        # Interpretation
        if analysis['dynamic_range'] > 200:
            print(f"  → High dynamic range - consider HDR techniques")
        elif analysis['dynamic_range'] < 100:
            print(f"  → Low dynamic range - low contrast scene")
        else:
            print(f"  → Moderate dynamic range - normal scene")
    
    print("\n" + "-" * 60)
    print("\n4. Exposure Bias Detection...")
    print("-" * 60)
    
    for name, image in images:
        analysis = analyze_histogram(image)
        
        print(f"\n{name}:")
        print(f"  Exposure Bias: {analysis['exposure_bias']:+.3f}")
        
        # Interpretation
        if analysis['exposure_bias'] > 0.1:
            print(f"  ⚠️  Image is overexposed (too bright)")
            print(f"     → Reduce exposure by {analysis['exposure_bias']*100:.1f}%")
        elif analysis['exposure_bias'] < -0.1:
            print(f"  ⚠️  Image is underexposed (too dark)")
            print(f"     → Increase exposure by {abs(analysis['exposure_bias'])*100:.1f}%")
        else:
            print(f"  ✓ Well exposed")
    
    print("\n" + "-" * 60)
    print("\n5. Entropy Analysis...")
    print("-" * 60)
    
    for name, image in images:
        analysis = analyze_histogram(image)
        
        print(f"\n{name}:")
        print(f"  Entropy: {analysis['entropy']:.2f} bits")
        
        # Interpretation
        if analysis['entropy'] > 7.5:
            print(f"  → High entropy: Complex scene with lots of detail")
        elif analysis['entropy'] < 5.0:
            print(f"  → Low entropy: Simple scene, smooth regions")
        else:
            print(f"  → Moderate entropy: Normal scene complexity")
    
    print("\n" + "=" * 60)


def main():
    """
    Main function demonstrating histogram analysis.
    """
    print("\n" + "=" * 60)
    print("CHAPTER 8 - EXAMPLE 4: HISTOGRAM ANALYSIS")
    print("=" * 60)
    print("\nThis example demonstrates:")
    print("1. Histogram generation and interpretation")
    print("2. Percentile calculation")
    print("3. Dynamic range measurement")
    print("4. Exposure bias detection")
    print("5. Shannon entropy calculation")
    print("\n" + "=" * 60)
    
    demonstrate_histogram_analysis()
    
    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("=" * 60)
    print("1. Histograms show brightness distribution")
    print("2. Percentiles help understand exposure")
    print("3. Dynamic range indicates scene contrast")
    print("4. Exposure bias detects over/under exposure")
    print("5. Entropy measures image complexity")
    print("\n" + "=" * 60)
    print("Next: Run 05_scene_analysis.py to learn about")
    print("      scene classification and face detection")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
