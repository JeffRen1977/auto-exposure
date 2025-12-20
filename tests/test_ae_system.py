"""
Test script for the Auto Exposure System
"""

import numpy as np
import cv2
import sys
import os
# Add parent directory to path to import from core
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # Go up one level from tests/ to AutoExposure/
sys.path.insert(0, parent_dir)
from core.auto_exposure_system import AutoExposureSystem, SensorInfo, SceneType
import matplotlib.pyplot as plt
import glob


def load_raw10_image(filepath, width, height):
    """
    Load RAW10 image from file
    RAW10 format: 10-bit packed raw data
    """
    # Read the raw file
    with open(filepath, 'rb') as f:
        raw_data = np.frombuffer(f.read(), dtype=np.uint8)
    
    # RAW10 unpacking: 4 pixels stored in 5 bytes
    # Each pixel is 10 bits, packed as: [P0[9:2]][P1[9:2]][P2[9:2]][P3[9:2]][P3[1:0]P2[1:0]P1[1:0]P0[1:0]]
    num_pixels = width * height
    num_bytes_needed = (num_pixels * 10) // 8
    
    if len(raw_data) < num_bytes_needed:
        print(f"Warning: File size mismatch. Expected {num_bytes_needed}, got {len(raw_data)}")
        # Try to process what we have
        num_pixels = (len(raw_data) * 8) // 10
        height = num_pixels // width
    
    # Unpack RAW10 to 16-bit values
    unpacked = []
    for i in range(0, len(raw_data) - 4, 5):
        # Read 5 bytes containing 4 10-bit pixels
        byte0, byte1, byte2, byte3, byte4 = raw_data[i:i+5]
        
        # Extract 4 pixels
        p0 = (byte0 << 2) | ((byte4 >> 0) & 0x03)
        p1 = (byte1 << 2) | ((byte4 >> 2) & 0x03)
        p2 = (byte2 << 2) | ((byte4 >> 4) & 0x03)
        p3 = (byte3 << 2) | ((byte4 >> 6) & 0x03)
        
        unpacked.extend([p0, p1, p2, p3])
    
    # Convert to numpy array and reshape
    unpacked = np.array(unpacked[:width * height], dtype=np.uint16)
    image = unpacked.reshape((height, width))
    
    # Convert 10-bit to 8-bit for processing
    image_8bit = (image >> 2).astype(np.uint8)
    
    return image_8bit


def load_real_images():
    """Load real image data from the data folder"""
    images = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Data folder is one level up from tests/
    data_dir = os.path.join(os.path.dirname(current_dir), "data")
    
    # Look for RAW files in data folder
    raw_files = glob.glob(os.path.join(data_dir, "*.raw"))
    
    if raw_files:
        print(f"Found {len(raw_files)} RAW file(s)")
        for raw_file in raw_files:
            filename = os.path.basename(raw_file)
            print(f"Processing: {filename}")
            
            # Parse filename to extract dimensions
            # Format: date_time_..._WIDTHxHEIGHT_...raw
            try:
                parts = filename.split('_')
                for part in parts:
                    if 'x' in part:
                        dims = part.split('x')
                        if len(dims) == 2 and dims[0].isdigit() and dims[1].isdigit():
                            width = int(dims[0])
                            height = int(dims[1])
                            print(f"  Dimensions: {width}x{height}")
                            
                            # Load the RAW image (Bayer format)
                            raw_bayer = load_raw10_image(raw_file, width, height)
                            
                            # Convert Bayer to RGB for visualization and processing
                            # Using simple demosaicing for now
                            image_rgb = cv2.cvtColor(raw_bayer, cv2.COLOR_BayerBG2BGR)
                            
                            # Store with descriptive name
                            images[f'raw_bayer_{width}x{height}'] = image_rgb
                            
                            print(f"  Successfully loaded RAW Bayer image")
                            print(f"  Converted to RGB: {image_rgb.shape}")
                            
                            break
            except Exception as e:
                print(f"  Error parsing dimensions: {e}")
                continue
    
    # Skip loading JPEG/PNG images - focus on RAW data only
    # If you want to include reference images, uncomment the code below:
    # for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
    #     img_files = glob.glob(os.path.join(data_dir, ext))
    #     for img_file in img_files:
    #         filename = os.path.basename(img_file)
    #         print(f"Loading: {filename}")
    #         image = cv2.imread(img_file)
    #         if image is not None:
    #             images[f'photo_{filename}'] = image
    
    # Fallback to synthetic images if no real images found
    if not images:
        print("No real images found, creating synthetic test images")
        images = create_synthetic_test_images()
    
    return images


def create_synthetic_test_images():
    """Create synthetic test images for testing (fallback)"""
    images = {}
    
    # Low light image
    images['synthetic_low_light'] = np.random.randint(0, 80, (480, 640, 3), dtype=np.uint8)
    
    # High contrast image
    high_contrast = np.zeros((480, 640, 3), dtype=np.uint8)
    high_contrast[:240, :] = 255  # Bright top half
    high_contrast[240:, :] = 50   # Dark bottom half
    images['synthetic_high_contrast'] = high_contrast
    
    # Normal outdoor image
    images['synthetic_outdoor'] = np.random.randint(100, 200, (480, 640, 3), dtype=np.uint8)
    
    # Backlit scene (bright background, dark foreground)
    backlit = np.random.randint(200, 255, (480, 640, 3), dtype=np.uint8)
    backlit[300:, 200:440] = np.random.randint(0, 50, (180, 240, 3), dtype=np.uint8)
    images['synthetic_backlit'] = backlit
    
    return images


def test_ae_system():
    """Test the Auto Exposure System with various scenarios"""
    print("Testing Auto Exposure System...")
    print("=" * 60)
    
    # Initialize the system
    ae_system = AutoExposureSystem()
    
    # Load real images
    print("\nLoading images...")
    test_images = load_real_images()
    print(f"\nLoaded {len(test_images)} test image(s)\n")
    
    # Test sensor configuration
    sensor_info = SensorInfo(
        exposure_time=1/60,
        analog_gain=2.0,
        digital_gain=1.0,
        iso=200,
        aperture=2.8
    )
    
    results = {}
    
    # Test each scenario
    for scenario, image in test_images.items():
        print(f"\nTesting {scenario} scenario...")
        print(f"  Image shape: {image.shape}")
        
        # Process the frame
        result = ae_system.process_frame(image, sensor_info)
        results[scenario] = result
        
        # Print results
        print(f"  Exposure Time: {result.exposure_time:.6f}s ({1/result.exposure_time:.1f} fps)")
        print(f"  Analog Gain: {result.analog_gain:.2f}x")
        print(f"  Digital Gain: {result.digital_gain:.2f}x")
        print(f"  Total Exposure Sensitivity: {result.total_exposure_sensitivity:.2f}")
        print(f"  Brightness Value (Bv): {result.brightness_value:.2f}")
        print(f"  Aperture Value (Av): {result.aperture_value:.2f}")
        print(f"  Time Value (Tv): {result.time_value:.2f}")
        print(f"  Sensitivity Value (Sv): {result.sensitivity_value:.2f}")
    
    return results, test_images


def test_individual_components():
    """Test individual components of the AE system"""
    print("\nTesting individual components...")
    
    # Test SpatialFrameAnalyzer
    from core.auto_exposure_system import SpatialFrameAnalyzer
    spatial_analyzer = SpatialFrameAnalyzer()
    
    # Create test Bayer stats
    bayer_stats = np.random.randint(0, 255, (64, 48), dtype=np.uint8)
    spatial_results = spatial_analyzer.analyze_spatial_distribution(bayer_stats)
    
    print("Spatial Analysis Results:")
    for key, value in spatial_results.items():
        print(f"  {key}: {value:.2f}")
    
    # Test HistogramAnalyzer
    from core.auto_exposure_system import HistogramAnalyzer
    histogram_analyzer = HistogramAnalyzer()
    
    # Create test histogram
    histogram = np.random.randint(0, 1000, 256, dtype=np.uint32)
    histogram_results = histogram_analyzer.analyze_histogram(histogram)
    
    print("\nHistogram Analysis Results:")
    for key, value in histogram_results.items():
        print(f"  {key}: {value:.2f}")
    
    # Test SceneAnalyzer
    from core.auto_exposure_system import SceneAnalyzer
    scene_analyzer = SceneAnalyzer()
    
    # Create test image
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    scene_info = scene_analyzer.analyze_scene(test_image, spatial_results)
    
    print("\nScene Analysis Results:")
    print(f"  Scene Type: {scene_info.scene_type}")
    print(f"  Confidence: {scene_info.confidence:.2f}")
    print(f"  Face ROIs: {len(scene_info.face_rois)}")
    print(f"  Motion Level: {scene_info.motion_level:.2f}")
    print(f"  Dynamic Range: {scene_info.dynamic_range:.2f}")


def test_flicker_detection():
    """Test flicker detection functionality"""
    print("\nTesting Flicker Detection...")
    
    from core.auto_exposure_system import FlickerDetector
    flicker_detector = FlickerDetector()
    
    # Test various exposure times
    test_times = [1/50, 1/60, 1/100, 1/200, 1/500]
    
    for exposure_time in test_times:
        has_flicker = flicker_detector.detect_flicker(exposure_time)
        adjusted_time = flicker_detector.adjust_for_flicker(exposure_time)
        
        print(f"  Exposure Time: {exposure_time:.6f}s")
        print(f"    Has Flicker: {has_flicker}")
        print(f"    Adjusted Time: {adjusted_time:.6f}s")


def save_analyzed_images(test_images, results):
    """Save processed images with analysis overlays"""
    print("\nSaving analyzed images...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Output folder is one level up from tests/
    output_dir = os.path.join(os.path.dirname(current_dir), "ae_analysis_output")
    os.makedirs(output_dir, exist_ok=True)
    
    for scenario, image in test_images.items():
        if scenario in results:
            result = results[scenario]
            
            # Create a copy for annotation
            annotated = image.copy()
            
            # Add text with exposure information
            font = cv2.FONT_HERSHEY_SIMPLEX
            y_offset = 30
            line_height = 30
            
            info_lines = [
                f"Scenario: {scenario}",
                f"Exp Time: {result.exposure_time:.6f}s ({1/result.exposure_time:.1f} fps)",
                f"Analog Gain: {result.analog_gain:.2f}x",
                f"Digital Gain: {result.digital_gain:.2f}x",
                f"TES: {result.total_exposure_sensitivity:.2f}",
                f"Bv: {result.brightness_value:.2f}",
            ]
            
            for i, line in enumerate(info_lines):
                y_pos = y_offset + i * line_height
                # Add background rectangle for better readability
                (text_width, text_height), _ = cv2.getTextSize(line, font, 0.6, 2)
                cv2.rectangle(annotated, (5, y_pos - 20), (15 + text_width, y_pos + 5), (0, 0, 0), -1)
                cv2.putText(annotated, line, (10, y_pos), font, 0.6, (0, 255, 0), 2)
            
            # Save annotated image
            output_path = os.path.join(output_dir, f"{scenario}_analyzed.png")
            cv2.imwrite(output_path, annotated)
            print(f"  Saved: {scenario}_analyzed.png")


def visualize_results(results):
    """Visualize the test results"""
    print("\nCreating visualization...")
    
    scenarios = list(results.keys())
    exposure_times = [results[s].exposure_time for s in scenarios]
    analog_gains = [results[s].analog_gain for s in scenarios]
    brightness_values = [results[s].brightness_value for s in scenarios]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Exposure Time
    axes[0, 0].bar(scenarios, exposure_times, color='steelblue')
    axes[0, 0].set_title('Exposure Time by Scenario', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Exposure Time (s)')
    axes[0, 0].tick_params(axis='x', rotation=45, labelsize=8)
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Analog Gain
    axes[0, 1].bar(scenarios, analog_gains, color='coral')
    axes[0, 1].set_title('Analog Gain by Scenario', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('Analog Gain')
    axes[0, 1].tick_params(axis='x', rotation=45, labelsize=8)
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Brightness Value
    axes[1, 0].bar(scenarios, brightness_values, color='lightgreen')
    axes[1, 0].set_title('Brightness Value by Scenario', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Brightness Value (Bv)')
    axes[1, 0].tick_params(axis='x', rotation=45, labelsize=8)
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Total Exposure Sensitivity
    tes_values = [results[s].total_exposure_sensitivity for s in scenarios]
    axes[1, 1].bar(scenarios, tes_values, color='mediumpurple')
    axes[1, 1].set_title('Total Exposure Sensitivity by Scenario', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('TES')
    axes[1, 1].tick_params(axis='x', rotation=45, labelsize=8)
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ae_test_results.png', dpi=300, bbox_inches='tight')
    print("Results chart saved to 'ae_test_results.png'")


def main():
    """Main test function"""
    print("Auto Exposure System Test Suite")
    print("=" * 60)
    
    # Test the complete system
    results, test_images = test_ae_system()
    
    # Save analyzed images
    save_analyzed_images(test_images, results)
    
    # Test individual components
    test_individual_components()
    
    # Test flicker detection
    test_flicker_detection()
    
    # Visualize results
    try:
        visualize_results(results)
    except ImportError:
        print("\nMatplotlib not available for visualization")
    except Exception as e:
        print(f"\nError creating visualization: {e}")
    
    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("Check 'ae_analysis_output' folder for processed images")
    print("Check 'ae_test_results.png' for analysis charts")


if __name__ == "__main__":
    main()


