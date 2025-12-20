# Tests Directory

This directory contains test scripts for the Auto Exposure System.

## Test Suite

### `test_ae_system.py`

Complete test suite that:
- Loads RAW10 Bayer data from `../data/` folder
- Tests the complete auto exposure pipeline
- Tests individual components
- Generates analysis output and visualizations

**Usage:**
```bash
# From AutoExposure directory
cd AutoExposure
source ../virtual_env/bin/activate
python tests/test_ae_system.py
```

**Output:**
- `../ae_analysis_output/` - Annotated images with exposure overlays
- `../ae_test_results.png` - Comparative analysis charts
- Console output with detailed metrics

## Running Tests

### From AutoExposure Root Directory

```bash
# Activate virtual environment
source ../virtual_env/bin/activate

# Run the test suite
python tests/test_ae_system.py
```

### From Tests Directory

```bash
# Navigate to tests directory
cd tests

# Activate virtual environment (two levels up)
source ../../virtual_env/bin/activate

# Run the test
python test_ae_system.py
```

## Test Coverage

The test suite covers:
1. **Complete System Test** - End-to-end pipeline with real RAW10 data
2. **Component Tests** - Individual component testing:
   - SpatialFrameAnalyzer
   - HistogramAnalyzer
   - SceneAnalyzer
   - FlickerDetector
3. **Visualization** - Generates charts and annotated images

## Input Data

Tests automatically look for RAW10 files in `../data/` folder.

Place your RAW10 camera data files in the `data/` folder with dimensions in filename:
- Format: `*_WIDTHxHEIGHT_*.raw`
- Example: `20250929_223233_713_RAW10_4032x756_*.raw`

## Output

Test results are saved to:
- `../ae_analysis_output/` - Annotated images
- `../ae_test_results.png` - Analysis charts

These folders are created automatically if they don't exist.
