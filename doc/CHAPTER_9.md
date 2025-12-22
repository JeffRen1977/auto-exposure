# Chapter 9: Auto Exposure System Implementation

## Abstract

This chapter presents a complete Auto Exposure (AE) system implementation for mobile camera devices. The system processes RAW10 Bayer data, extracts image statistics, analyzes scene characteristics, and automatically determines optimal exposure settings. It features real-time operation, scene-aware adjustments, flicker detection, and APEX value calculations. The implementation is organized as progressive learning examples that build from basic concepts to a complete system, making it ideal for understanding the fundamentals of auto exposure in computational photography.

**Keywords:** Auto Exposure, Mobile Camera, RAW10 Bayer, Image Processing, Real-time Exposure, Flicker Detection, Scene Analysis, Exposure Control, APEX Values, Computational Photography

**GitHub Repository:** https://github.com/JeffRen1977/auto-exposure

## 9.1 Overview

The Auto Exposure System automatically adjusts camera exposure to achieve optimal image brightness. It processes camera sensor data through multiple analysis stages to intelligently determine exposure time and gain settings.

### Key Features

- **RAW10 Bayer data support** - Direct processing of 10-bit packed raw sensor data
- **Real-time operation** - Processes frames at 33+ fps
- **Scene-aware exposure** - Adapts to different scene types (indoor, outdoor, backlit, low-light)
- **Flicker detection** - Prevents banding artifacts from AC lighting (50Hz/60Hz)
- **APEX value calculation** - Generates standard exposure metadata (Bv, Av, Tv, Sv)
- **Progressive learning structure** - Nine examples that build from basics to complete system

### System Architecture

The system consists of five main processing modules:

1. **SpatialFrameAnalyzer** - Analyzes brightness distribution across the image using center-weighted metering
2. **HistogramAnalyzer** - Evaluates light distribution, dynamic range, and exposure bias
3. **SceneAnalyzer** - Classifies scene type and detects faces for intelligent exposure adjustment
4. **ExposureController** - Calculates Total Exposure Sensitivity (TES) and distributes it between exposure time and gain
5. **FlickerDetector** - Detects and mitigates flickering from artificial lighting

### Processing Pipeline

```
RAW10 Input → Unpack → Demosaic → Extract Statistics
                                    ↓
                    ┌───────────────────────────────┐
                    │  Spatial Analysis            │
                    │  Histogram Analysis           │
                    │  Scene Analysis               │
                    └───────────────────────────────┘
                                    ↓
                    Calculate Total Exposure Sensitivity (TES)
                                    ↓
                    Distribute Exposure (Time vs Gain)
                                    ↓
                    Flicker Detection & Adjustment
                                    ↓
                    Output: Exposure Settings + APEX Values
```

## 9.2 Installation and Setup

### Prerequisites

- Python 3.7 or higher
- Virtual environment (recommended)

### Installation Steps

**Table 9.2-1. Installation**

```bash
# Navigate to AutoExposure directory
cd AutoExposure

# Activate virtual environment (located one directory above)
source ../virtual_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Required Dependencies:**
- `numpy>=1.21.0` - Numerical computations
- `opencv-python>=4.5.0` - Image processing and demosaicing
- `matplotlib>=3.3.0` - Visualization

## 9.3 Learning Path: Progressive Examples

The implementation is organized as nine progressive examples that teach auto exposure concepts step by step. Each example builds on previous concepts and includes detailed comments.

### Example 1: Basic Exposure (`01_basic_exposure.py`)

**Concepts:** Exposure triangle, brightness measurement, exposure compensation

**Key Learning:**
- Understanding exposure: time, gain, and aperture
- Measuring image brightness
- Calculating exposure compensation: `compensation = target_brightness / current_brightness`

**Table 9.3.1-1. Basic Exposure Calculation**

```python
def calculate_exposure_compensation(current_brightness, target_brightness=128):
    """Calculate exposure adjustment needed"""
    return target_brightness / max(current_brightness, 1.0)
```

### Example 2: Image Statistics (`02_image_statistics.py`)

**Concepts:** Bayer statistics grid, histogram generation, saturation detection

**Key Learning:**
- Extracting statistics from Bayer pattern data
- Creating 64×48 grid for efficient computation
- Generating histograms and detecting saturated pixels

### Example 3: Spatial Analysis (`03_spatial_analysis.py`)

**Concepts:** Center-weighted metering, exposure zones (highlights, midtones, shadows)

**Key Learning:**
- Center-weighted metering implementation using distance-based weighting
- Classifying pixels into exposure zones based on standard deviation

**Table 9.3.3-1. Center-Weighted Metering**

```python
def _calculate_center_weight(self, stats: np.ndarray) -> float:
    """Calculate center-weighted brightness"""
    h, w = stats.shape
    center_h, center_w = h // 2, w // 2
    
    # Distance-based weight: center = 1.0, edges = 0.1
    y, x = np.ogrid[:h, :w]
    center_dist = np.sqrt((x - center_w)**2 + (y - center_h)**2)
    max_dist = np.sqrt(center_w**2 + center_h**2)
    weight_mask = 1.0 - (center_dist / max_dist)
    weight_mask = np.maximum(weight_mask, 0.1)
    
    return np.average(stats, weights=weight_mask)
```

### Example 4: Histogram Analysis (`04_histogram_analysis.py`)

**Concepts:** Dynamic range, exposure bias, Shannon entropy

**Key Learning:**
- Percentile-based analysis (5th, 25th, 50th, 75th, 95th)
- Dynamic range: `p95 - p5`
- Exposure bias: `(p50 - 128) / 128.0`
- Entropy: `-Σ(p(i) × log₂(p(i)))` - measures image complexity

### Example 5: Scene Analysis (`05_scene_analysis.py`)

**Concepts:** Scene classification, face detection, motion estimation

**Key Learning:**
- Classifying scenes: indoor, outdoor, backlit, low-light, high-contrast
- Face detection using Haar Cascade classifier
- Motion estimation for exposure time adjustment

**Table 9.3.5-1. Scene Type Adjustments**

| Scene Type | Target Brightness Multiplier | Rationale |
|------------|------------------------------|-----------|
| LOW_LIGHT | 0.8× (102) | Prevent blown highlights |
| HIGH_CONTRAST | 1.2× (154) | Boost for bright scenes |
| BACKLIT | 1.1× (141) | Compensate for backlight |
| OUTDOOR | 1.0× (128) | Standard exposure |
| INDOOR | 0.9× (115) | Slightly darker |
| FACE_DETECTED | 1.1× (141) | Brighten faces |

### Example 6: Exposure Controller (`06_exposure_controller.py`)

**Concepts:** Total Exposure Sensitivity (TES), exposure distribution, motion blur vs noise trade-off

**Key Learning:**
- TES calculation: `TES = adjusted_target / current_brightness`
- Distributing exposure between time and gain
- Balancing motion blur (short exposure) vs noise (low gain)

**Table 9.3.6-1. Exposure Distribution Algorithm**

```python
def distribute_exposure(self, tes, sensor_info, motion_level):
    """Distribute TES into exposure time and gain"""
    # Motion factor: 0.5 (high motion) to 1.0 (no motion)
    motion_factor = 1.0 - (motion_level * 0.5)
    
    # Calculate optimal exposure time based on motion
    optimal_time = min_time + (max_time - min_time) * motion_factor
    
    # Calculate required gain
    required_gain = tes / optimal_time
    
    # Clamp to valid ranges
    exposure_time = np.clip(optimal_time, min_time, max_time)
    analog_gain = np.clip(required_gain, min_gain, max_gain)
    
    return exposure_time, analog_gain, 1.0  # digital_gain = 1.0
```

### Example 7: Flicker Detection (`07_flicker_detection.py`)

**Concepts:** AC flicker detection (50Hz/60Hz), flicker mitigation

**Key Learning:**
- AC lighting flickers at 2× power frequency (50Hz → 100Hz, 60Hz → 120Hz)
- Detecting problematic exposure times
- Adjusting to safe exposure times (multiples of flicker period)

**Table 9.3.7-1. Safe Exposure Times**

| AC Frequency | Flicker Period | Safe Times |
|--------------|----------------|------------|
| 60Hz | 8.33ms (1/120s) | 8.33ms, 16.67ms, 25ms, 33.33ms |
| 50Hz | 10ms (1/100s) | 10ms, 20ms, 30ms, 40ms |

### Example 8: APEX Calculation (`08_apex_calculation.py`)

**Concepts:** APEX (Additive System of Photographic Exposure) values, EXIF metadata

**Key Learning:**
- Calculating standard APEX values for metadata
- Bv (Brightness), Av (Aperture), Tv (Time), Sv (Sensitivity)

**Table 9.3.8-1. APEX Value Formulas**

```python
# Brightness Value
bv = log₂(exposure_time × gain × aperture)

# Aperture Value
av = log₂(aperture²)

# Time Value (larger = faster shutter)
tv = -log₂(exposure_time)

# Sensitivity Value
sv = log₂(gain × 100)  # ISO equivalent
```

### Example 9: Complete System (`09_complete_ae_system.py`)

**Concepts:** System integration, processing pipeline, temporal consistency

**Key Learning:**
- Integrating all components into a complete pipeline
- Maintaining exposure history for smooth transitions
- Real-time processing optimization

## 9.4 Running the Examples

### Quick Start: Run All Examples

**Table 9.4-1. Run All Examples**

```bash
# From AutoExposure directory
cd AutoExposure
source ../virtual_env/bin/activate
cd examples

# Run all examples sequentially
python run_all_examples.py

# Or run without pauses
python run_all_examples.py --skip

# Or start from a specific example
python run_all_examples.py 3  # Start from example 3
```

### Run Individual Examples

**Table 9.4-2. Run Individual Examples**

```bash
# Activate virtual environment
cd AutoExposure
source ../virtual_env/bin/activate

# Navigate to examples
cd examples

# Run examples in order
python 01_basic_exposure.py
python 02_image_statistics.py
python 03_spatial_analysis.py
# ... continue through all examples
```

## 9.5 Using the Complete System

### Basic Usage

**Table 9.5-1. Basic Usage Example**

```python
from core.auto_exposure_system import AutoExposureSystem, SensorInfo
import cv2

# Initialize the system
ae_system = AutoExposureSystem()

# Configure current sensor information
sensor_info = SensorInfo(
    exposure_time=1/60,      # Current exposure time (seconds)
    analog_gain=2.0,         # Current analog gain
    digital_gain=1.0,        # Current digital gain
    iso=200,                 # ISO value
    aperture=2.8             # F-number
)

# Load and process an image
image = cv2.imread('your_image.jpg')
result = ae_system.process_frame(image, sensor_info)

# Access exposure recommendations
print(f"Exposure Time: {result.exposure_time:.6f}s")
print(f"Analog Gain: {result.analog_gain:.2f}x")
print(f"Total Exposure Sensitivity: {result.total_exposure_sensitivity:.2f}")
print(f"Brightness Value (Bv): {result.brightness_value:.2f}")
```

### Processing RAW10 Bayer Data

**Table 9.5-2. RAW10 Processing**

```python
from tests.test_ae_system import load_raw10_image
import cv2

# Load RAW10 file (dimensions from filename or metadata)
raw_bayer = load_raw10_image('data/20250929_*.raw', width=4032, height=756)

# Convert Bayer to RGB (BayerBG pattern)
image_rgb = cv2.cvtColor(raw_bayer, cv2.COLOR_BayerBG2BGR)

# Process with AE system
result = ae_system.process_frame(image_rgb, sensor_info)
```

### Advanced Configuration

**Table 9.5-3. Custom Configuration**

```python
# Customize exposure controller
ae_system.exposure_controller.target_brightness = 140  # Default: 128
ae_system.exposure_controller.min_exposure_time = 1/8000  # 0.125ms
ae_system.exposure_controller.max_exposure_time = 1/30   # 33ms
ae_system.exposure_controller.min_gain = 1.0
ae_system.exposure_controller.max_gain = 16.0

# Customize flicker detection
ae_system.flicker_detector.flicker_frequencies = [50, 60]  # Hz
ae_system.flicker_detector.detection_threshold = 0.1

# Process frame
result = ae_system.process_frame(image, sensor_info)
```

## 9.6 Core Components - Implementation Details

### 9.6.1 SpatialFrameAnalyzer

Analyzes spatial brightness distribution using a 64×48 grid for efficient computation.

**Key Methods:**
- `analyze_spatial_distribution()` - Main analysis function
- `_calculate_center_weight()` - Center-weighted metering

**Output Structure:**

```python
{
    'center_weight': 126.85,      # Center-weighted brightness [0-255]
    'brightness_mean': 126.18,     # Average brightness [0-255]
    'brightness_std': 74.17,       # Standard deviation
    'highlights_ratio': 0.21,      # Fraction of highlight pixels
    'shadows_ratio': 0.21,         # Fraction of shadow pixels
    'midtones_ratio': 0.57         # Fraction of midtone pixels
}
```

### 9.6.2 HistogramAnalyzer

Analyzes the image histogram (256 bins) to understand light distribution.

**Key Methods:**
- `analyze_histogram()` - Main analysis function
- `_calculate_entropy()` - Shannon entropy calculation

**Output Structure:**

```python
{
    'p5': 45,                      # 5th percentile
    'p50': 120,                    # Median (50th percentile)
    'p95': 245,                    # 95th percentile
    'dynamic_range': 200,          # p95 - p5
    'exposure_bias': -0.06,         # (p50 - 128) / 128.0
    'histogram_entropy': 7.2        # Information content
}
```

**Interpretation:**
- **Dynamic Range > 200:** High contrast scene, consider HDR
- **Exposure Bias > 0:** Image trending bright
- **Exposure Bias < 0:** Image trending dark
- **Entropy > 7.5:** High detail/texture
- **Entropy < 5:** Low detail/smooth regions

### 9.6.3 SceneAnalyzer

Classifies scene type and detects faces for intelligent exposure adjustment.

**Key Methods:**
- `analyze_scene()` - Main analysis function
- `_classify_scene()` - Scene type classification
- `_detect_faces()` - Face detection using Haar Cascade
- `_estimate_motion()` - Motion level estimation

**Scene Classification Logic:**

```python
if brightness_mean < 80:
    return SceneType.LOW_LIGHT
elif brightness_mean > 200:
    return SceneType.HIGH_CONTRAST
elif brightness_std > 50:
    return SceneType.BACKLIT
else:
    return SceneType.OUTDOOR
```

### 9.6.4 ExposureController

Calculates Total Exposure Sensitivity (TES) and distributes it between exposure time and gain.

**Key Methods:**
- `calculate_total_exposure_sensitivity()` - TES calculation
- `distribute_exposure()` - Exposure distribution algorithm
- `_adjust_target_for_scene()` - Scene-based target adjustment

**TES Calculation:**

```python
def calculate_total_exposure_sensitivity(self, current_stats, scene_info):
    current_brightness = current_stats.brightness_mean
    adjusted_target = self._adjust_target_for_scene(128, scene_info)
    tes = adjusted_target / max(current_brightness, 1.0)
    
    # Boost for faces
    if scene_info.face_rois:
        tes *= 1.2
    
    return tes
```

### 9.6.5 FlickerDetector

Detects and mitigates flickering from AC-powered artificial lighting.

**Key Methods:**
- `detect_flicker()` - Detect problematic exposure times
- `adjust_for_flicker()` - Adjust to safe exposure times

**Detection Algorithm:**

```python
def detect_flicker(self, exposure_time: float) -> bool:
    for freq in [50, 60]:  # Common AC frequencies
        period = 1.0 / freq
        if abs(exposure_time - period) < 0.1:  # 100ms threshold
            return True
    return False
```

### 9.6.6 AutoExposureSystem

Main coordinator that orchestrates all components.

**Processing Pipeline:**

```python
def process_frame(self, image, sensor_info):
    # 1. Extract image statistics
    image_stats = self._extract_image_statistics(image)
    
    # 2. Spatial analysis
    spatial_stats = self.spatial_analyzer.analyze_spatial_distribution(
        image_stats.bayer_stats
    )
    
    # 3. Histogram analysis
    histogram_stats = self.histogram_analyzer.analyze_histogram(
        image_stats.histogram
    )
    
    # 4. Scene analysis
    scene_info = self.scene_analyzer.analyze_scene(image, spatial_stats)
    
    # 5. Calculate TES
    tes = self.exposure_controller.calculate_total_exposure_sensitivity(
        image_stats, scene_info
    )
    
    # 6. Distribute exposure
    exposure_time, analog_gain, digital_gain = \
        self.exposure_controller.distribute_exposure(
            tes, sensor_info, scene_info.motion_level
        )
    
    # 7. Flicker detection and adjustment
    if self.flicker_detector.detect_flicker(exposure_time):
        exposure_time = self.flicker_detector.adjust_for_flicker(exposure_time)
    
    # 8. Calculate APEX values
    apex_values = self._calculate_apex_values(
        exposure_time, analog_gain, sensor_info.aperture
    )
    
    # 9. Create and return result
    return ExposureResult(
        exposure_time=exposure_time,
        analog_gain=analog_gain,
        digital_gain=digital_gain,
        total_exposure_sensitivity=tes,
        **apex_values
    )
```

**Temporal Consistency:**

The system maintains exposure history (last 10 frames) for:
- Temporal smoothing (averaging recent exposures)
- Change detection (sudden scene changes)
- Motion estimation (frame-to-frame comparison)

## 9.7 Test Results

### Real-World Test with RAW10 Bayer Data

**Table 9.7-1. Test Results**

| Metric | Value |
|--------|-------|
| Input Format | RAW10 Bayer (BayerBG pattern) |
| Image Dimensions | 4032×756 |
| Exposure Time | 30ms (33.3 fps) |
| Analog Gain | 16.00× |
| Digital Gain | 1.00× |
| TES | 3.53 |
| Scene Type | Backlit |
| Brightness (Bv) | 0.43 |
| Dynamic Range | 227 levels |
| Exposure Bias | -0.07 (slight underexposure) |

### Performance Metrics

- **Processing Speed:** Real-time (33+ fps)
- **Spatial Grid:** 64×48 (efficient computation)
- **Histogram Bins:** 256
- **Memory:** Low overhead with frame history (10 frames)
- **Latency:** < 1 frame delay

## 9.8 Summary

This chapter presented a complete Auto Exposure system implementation organized as progressive learning examples. The system demonstrates:

1. **Fundamental Concepts** - Exposure triangle, brightness measurement, compensation
2. **Spatial Analysis** - Center-weighted metering, exposure zones
3. **Histogram Analysis** - Dynamic range, exposure bias, entropy
4. **Scene Understanding** - Scene classification, face detection, motion estimation
5. **Exposure Control** - TES calculation, exposure distribution
6. **Advanced Features** - Flicker detection, APEX values
7. **System Integration** - Complete pipeline with temporal consistency

The implementation provides both educational examples for learning and a production-ready core module for practical use. Readers can progress through the examples to understand each concept, then use the complete system for real-world applications.

## 9.9 Exercises

1. **Modify target brightness** - Experiment with different target values and observe the effects
2. **Implement spot metering** - Modify the spatial analyzer to use only the center region
3. **Add new scene types** - Extend scene classification (e.g., sunset, night mode)
4. **Experiment with exposure distribution** - Try different strategies for balancing time vs gain
5. **Test flicker detection** - Use different AC frequencies and verify safe exposure times
6. **Add temporal smoothing** - Implement averaging of recent exposure values for smoother transitions

---

**Note:** All code examples and the complete implementation are available in the GitHub repository: https://github.com/JeffRen1977/auto-exposure

