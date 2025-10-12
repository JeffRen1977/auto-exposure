# Auto Exposure System - Quick Reference

## Running the Analysis

### Prerequisites
```bash
# Activate virtual environment
source /Users/jeffren/Documents/Learning/Mobile_Computational_photograph/virtual_env/bin/activate

# Navigate to project directory
cd /Users/jeffren/Documents/Learning/Mobile_Computational_photograph/AutoExposure
```

### Run the Test
```bash
python test_ae_system.py
```

## Input Data

**RAW10 File**: `20250929_223233_713_RAW10_4032x756_RS_5056_PS_1_cam_3_sensor_raw_pd_frame__default_pd_type_622.raw`
- Format: RAW10 (10-bit packed Bayer pattern)
- Dimensions: 4032 x 756 pixels
- Bayer Pattern: BayerBG

## Output Files

### 1. Annotated Image
`ae_analysis_output/raw_bayer_4032x756_analyzed.png`
- Original image with exposure information overlay
- Shows: Exposure time, gains, TES, and brightness value

### 2. Analysis Chart
`ae_test_results.png`
- Bar charts showing all exposure metrics

### 3. Detailed Summary
`TEST_RESULTS_SUMMARY.md`
- Complete analysis results
- Component test results
- Observations and conclusions

## Key Results

| Metric | Value |
|--------|-------|
| **Exposure Time** | 0.030s (33.3 fps) |
| **Analog Gain** | 16.00x |
| **Digital Gain** | 1.00x |
| **TES** | 3.53 |
| **Scene Type** | Backlit |
| **Brightness (Bv)** | 0.43 |

## Analysis Components

### Spatial Analysis
- Center-weighted metering
- Exposure zone distribution (highlights/midtones/shadows)
- Brightness statistics

### Histogram Analysis
- Dynamic range calculation
- Exposure bias detection
- Entropy measurement

### Scene Analysis
- Scene type classification
- Face detection
- Motion level estimation

### Flicker Detection
- 50Hz/60Hz flicker detection
- Automatic exposure time adjustment

## System Architecture

```
Input: RAW10 Bayer Data
    ↓
Unpack RAW10 (10-bit → 8-bit)
    ↓
Demosaic (Bayer → RGB)
    ↓
Extract Statistics (64x48 grid, histogram)
    ↓
Analyze Scene (type, motion, faces)
    ↓
Calculate TES (Total Exposure Sensitivity)
    ↓
Distribute Exposure (time vs gain)
    ↓
Check Flicker & Adjust
    ↓
Output: Exposure Settings + APEX Values
```

## Customization

### Adjust Target Brightness
```python
ae_system.exposure_controller.target_brightness = 140  # Default: 128
```

### Change Exposure Limits
```python
ae_system.exposure_controller.min_exposure_time = 1/8000
ae_system.exposure_controller.max_exposure_time = 1/30
ae_system.exposure_controller.min_gain = 1.0
ae_system.exposure_controller.max_gain = 16.0
```

### Enable/Disable Features
```python
# To include JPEG/PNG reference images, edit test_ae_system.py line 103-110
# Uncomment the image loading code
```

## Files Overview

| File | Description |
|------|-------------|
| `auto_exposure_system.py` | Main AE system implementation |
| `test_ae_system.py` | Test script with RAW10 loader |
| `README.md` | Complete documentation |
| `requirements.txt` | Python dependencies |
| `design_reference.txt` | Original design document |

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis
python test_ae_system.py

# View results
open ae_analysis_output/raw_bayer_4032x756_analyzed.png
open ae_test_results.png
cat TEST_RESULTS_SUMMARY.md
```

## Interpreting Results

### Total Exposure Sensitivity (TES)
- **< 1.0**: Scene is bright, reduce exposure
- **1.0 - 2.0**: Well-exposed scene
- **2.0 - 4.0**: Moderate underexposure
- **> 4.0**: Significant underexposure, scene is dark

### Brightness Value (Bv)
- **< 0**: Very dark scene
- **0 - 3**: Low light
- **3 - 7**: Normal daylight
- **> 7**: Bright daylight

### Scene Types
- **INDOOR**: Lower target brightness
- **OUTDOOR**: Standard exposure
- **BACKLIT**: Compensated for backlight
- **LOW_LIGHT**: Optimized for darkness
- **HIGH_CONTRAST**: HDR-like handling

## Notes

- The system uses BayerBG demosaicing by default
- Face detection uses OpenCV's Haar Cascade
- Flicker detection targets 50Hz and 60Hz AC lighting
- All Google-related references have been removed from code and documentation
