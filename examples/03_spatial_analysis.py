"""
Chapter 8 - Example 3: Spatial Analysis and Metering

This example demonstrates spatial brightness analysis for auto exposure:
1. Center-weighted metering
2. Exposure zone classification (highlights, midtones, shadows)
3. Spatial brightness distribution analysis

Learning Objectives:
- Understand center-weighted metering algorithm
- Classify pixels into exposure zones
- Analyze spatial brightness distribution
- Implement different metering modes

This corresponds to Section 8.3 in the book.
"""

import numpy as np
import cv2
from typing import Dict, Tuple


def calculate_center_weighted_metering(image: np.ndarray) -> float:
    """
    Calculate center-weighted metering value.
    
    Center-weighted metering gives more importance to the center of the image,
    which is typically where the main subject is located. This is based on the
    observation that photographers usually frame subjects in the center.
    
    The weight decreases linearly from center (weight=1.0) to edges (weight=0.1).
    
    Args:
        image: Input image (grayscale or color)
    
    Returns:
        Center-weighted brightness value (0-255)
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    h, w = gray.shape
    center_h, center_w = h // 2, w // 2
    
    # Create distance map from center
    y, x = np.ogrid[:h, :w]
    center_dist = np.sqrt((x - center_w)**2 + (y - center_h)**2)
    max_dist = np.sqrt(center_w**2 + center_h**2)
    
    # Weight decreases linearly with distance from center
    # Center has weight 1.0, edges have minimum weight 0.1
    weight_mask = 1.0 - (center_dist / max_dist)
    weight_mask = np.maximum(weight_mask, 0.1)  # Minimum 10% weight
    
    # Calculate weighted average
    center_weighted = np.average(gray, weights=weight_mask)
    
    return float(center_weighted)


def classify_exposure_zones(image: np.ndarray) -> Dict[str, float]:
    """
    Classify pixels into exposure zones: highlights, midtones, and shadows.
    
    This is based on the Zone System developed by Ansel Adams:
    - Highlights: Very bright areas (may be overexposed)
    - Midtones: Well-exposed areas (main subject)
    - Shadows: Dark areas (may be underexposed)
    
    Classification uses standard deviation from mean brightness.
    
    Args:
        image: Input image (grayscale or color)
    
    Returns:
        Dictionary with zone statistics
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Calculate statistics
    brightness_mean = np.mean(gray)
    brightness_std = np.std(gray)
    
    total_pixels = gray.size
    
    # Classify zones based on standard deviation
    # Highlights: brightness > mean + std
    highlights = np.sum(gray > brightness_mean + brightness_std)
    
    # Shadows: brightness < mean - std
    shadows = np.sum(gray < brightness_mean - brightness_std)
    
    # Midtones: everything else
    midtones = total_pixels - highlights - shadows
    
    return {
        'highlights_count': int(highlights),
        'shadows_count': int(shadows),
        'midtones_count': int(midtones),
        'highlights_ratio': highlights / total_pixels,
        'shadows_ratio': shadows / total_pixels,
        'midtones_ratio': midtones / total_pixels,
        'brightness_mean': float(brightness_mean),
        'brightness_std': float(brightness_std)
    }


def extract_spatial_statistics(image: np.ndarray, grid_size: Tuple[int, int] = (64, 48)) -> Dict[str, float]:
    """
    Extract spatial statistics using a grid-based approach.
    
    Real camera systems use a grid (e.g., 64x48) to efficiently analyze
    spatial brightness distribution without processing every pixel.
    
    Args:
        image: Input image
        grid_size: Size of the statistics grid (width, height)
    
    Returns:
        Dictionary with spatial statistics
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Resize to grid size (this simulates sensor statistics)
    bayer_stats = cv2.resize(gray, grid_size, interpolation=cv2.INTER_AREA)
    
    # Calculate center-weighted metering
    center_weight = calculate_center_weighted_metering(bayer_stats)
    
    # Classify zones
    zones = classify_exposure_zones(bayer_stats)
    
    return {
        'grid_size': grid_size,
        'center_weight': center_weight,
        'brightness_mean': zones['brightness_mean'],
        'brightness_std': zones['brightness_std'],
        'highlights_ratio': zones['highlights_ratio'],
        'shadows_ratio': zones['shadows_ratio'],
        'midtones_ratio': zones['midtones_ratio']
    }


def compare_metering_modes(image: np.ndarray) -> Dict[str, float]:
    """
    Compare different metering modes.
    
    Metering modes:
    - Average: Equal weight to all pixels
    - Center-weighted: More weight to center
    - Spot: Only center region (simplified here)
    
    Args:
        image: Input image
    
    Returns:
        Dictionary with metering values for different modes
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Average metering (equal weight everywhere)
    average_metering = np.mean(gray)
    
    # Center-weighted metering
    center_weighted = calculate_center_weighted_metering(gray)
    
    # Spot metering (center 10% of image)
    h, w = gray.shape
    center_h, center_w = h // 2, w // 2
    spot_size = min(h, w) // 10
    spot_region = gray[center_h-spot_size:center_h+spot_size,
                       center_w-spot_size:center_w+spot_size]
    spot_metering = np.mean(spot_region) if spot_region.size > 0 else average_metering
    
    return {
        'average': float(average_metering),
        'center_weighted': float(center_weighted),
        'spot': float(spot_metering)
    }


def demonstrate_spatial_analysis():
    """
    Demonstrate spatial analysis and metering techniques.
    """
    print("\n" + "=" * 60)
    print("SPATIAL ANALYSIS AND METERING DEMONSTRATION")
    print("=" * 60)
    
    # Create test images with different spatial characteristics
    print("\n1. Creating test images...")
    
    # Image 1: Center-bright (typical portrait)
    center_bright = np.zeros((480, 640), dtype=np.uint8)
    center_bright[:] = 100  # Dark background
    cv2.circle(center_bright, (320, 240), 100, 200, -1)  # Bright center
    center_bright = cv2.GaussianBlur(center_bright, (21, 21), 0)
    
    # Image 2: Edge-bright (backlit scene)
    edge_bright = np.zeros((480, 640), dtype=np.uint8)
    edge_bright[:] = 200  # Bright background
    cv2.rectangle(edge_bright, (200, 150), (440, 330), 50, -1)  # Dark center
    edge_bright = cv2.GaussianBlur(edge_bright, (21, 21), 0)
    
    # Image 3: Uniform (even lighting)
    uniform = np.full((480, 640), 128, dtype=np.uint8)
    uniform = uniform + np.random.normal(0, 10, uniform.shape).astype(np.int16)
    uniform = np.clip(uniform, 0, 255).astype(np.uint8)
    
    images = [
        ("Center-Bright (Portrait)", center_bright),
        ("Edge-Bright (Backlit)", edge_bright),
        ("Uniform (Even Lighting)", uniform),
    ]
    
    print("\n2. Comparing Metering Modes...")
    print("-" * 60)
    
    for name, image in images:
        metering = compare_metering_modes(image)
        
        print(f"\n{name}:")
        print(f"  Average Metering:      {metering['average']:.1f}")
        print(f"  Center-Weighted:       {metering['center_weighted']:.1f}")
        print(f"  Spot Metering:         {metering['spot']:.1f}")
        
        # Show difference
        diff = metering['center_weighted'] - metering['average']
        if abs(diff) > 5:
            print(f"  Difference:            {diff:+.1f} "
                  f"({'brighter' if diff > 0 else 'darker'} center)")
    
    print("\n" + "-" * 60)
    print("\n3. Exposure Zone Classification...")
    print("-" * 60)
    
    for name, image in images:
        zones = classify_exposure_zones(image)
        
        print(f"\n{name}:")
        print(f"  Mean Brightness:      {zones['brightness_mean']:.1f}")
        print(f"  Std Deviation:        {zones['brightness_std']:.1f}")
        print(f"  Highlights:           {zones['highlights_ratio']*100:.1f}%")
        print(f"  Midtones:             {zones['midtones_ratio']*100:.1f}%")
        print(f"  Shadows:               {zones['shadows_ratio']*100:.1f}%")
        
        # Interpretation
        if zones['highlights_ratio'] > 0.3:
            print(f"  ⚠️  Warning: High highlight ratio - risk of overexposure")
        if zones['shadows_ratio'] > 0.3:
            print(f"  ⚠️  Warning: High shadow ratio - risk of underexposure")
        if zones['midtones_ratio'] > 0.6:
            print(f"  ✓ Good: Well-balanced exposure")
    
    print("\n" + "-" * 60)
    print("\n4. Spatial Statistics (64x48 grid)...")
    print("-" * 60)
    
    for name, image in images:
        stats = extract_spatial_statistics(image, grid_size=(64, 48))
        
        print(f"\n{name}:")
        print(f"  Grid Size:            {stats['grid_size']}")
        print(f"  Center-Weighted:       {stats['center_weight']:.1f}")
        print(f"  Mean Brightness:      {stats['brightness_mean']:.1f}")
        print(f"  Std Deviation:        {stats['brightness_std']:.1f}")
        print(f"  Highlights:           {stats['highlights_ratio']*100:.1f}%")
        print(f"  Midtones:             {stats['midtones_ratio']*100:.1f}%")
        print(f"  Shadows:               {stats['shadows_ratio']*100:.1f}%")
    
    print("\n" + "=" * 60)


def main():
    """
    Main function demonstrating spatial analysis.
    """
    print("\n" + "=" * 60)
    print("CHAPTER 8 - EXAMPLE 3: SPATIAL ANALYSIS AND METERING")
    print("=" * 60)
    print("\nThis example demonstrates:")
    print("1. Center-weighted metering algorithm")
    print("2. Exposure zone classification")
    print("3. Spatial brightness distribution")
    print("4. Comparison of different metering modes")
    print("\n" + "=" * 60)
    
    demonstrate_spatial_analysis()
    
    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("=" * 60)
    print("1. Center-weighted metering prioritizes center of image")
    print("2. Zone classification helps identify over/under exposure")
    print("3. Grid-based statistics are efficient for real-time processing")
    print("4. Different metering modes suit different scenes")
    print("\n" + "=" * 60)
    print("Next: Run 04_histogram_analysis.py to learn about")
    print("      histogram-based exposure analysis")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()


