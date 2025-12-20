# Chapter 8 Examples - Progressive Learning

This directory contains progressive examples that build from basic concepts to a complete auto exposure system. Each example focuses on specific concepts from Chapter 8 of "Mobile Computational Photography".

## 📚 Learning Path

### Level 1: Foundation
- **01_basic_exposure.py** - Exposure triangle, brightness measurement, compensation
- **02_image_statistics.py** - Bayer statistics, histograms, saturation detection

### Level 2: Spatial Analysis
- **03_spatial_analysis.py** - Center-weighted metering, exposure zones

### Level 3: Histogram Analysis
- **04_histogram_analysis.py** - Dynamic range, exposure bias, entropy

### Level 4: Scene Understanding
- **05_scene_analysis.py** - Scene classification, face detection, motion

### Level 5: Exposure Control
- **06_exposure_controller.py** - TES calculation, exposure distribution

### Level 6: Advanced Features
- **07_flicker_detection.py** - AC flicker detection and mitigation
- **08_apex_calculation.py** - APEX values for EXIF metadata

### Level 7: Complete System
- **09_complete_ae_system.py** - Full pipeline integration

## 🚀 How to Use

### Quick Start - Run All Examples

**Easiest way:** Run all examples automatically in order:

```bash
# From AutoExposure directory
cd AutoExposure
source ../virtual_env/bin/activate
cd examples

# Run all examples (with pauses between each)
python run_all_examples.py

# Or run without pauses
python run_all_examples.py --skip

# Or start from a specific example (e.g., example 3)
python run_all_examples.py 3
```

**Using shell script:**
```bash
cd examples
./run_all_examples.sh          # With pauses
./run_all_examples.sh --skip   # Without pauses
```

### For Learning - Run Individual Examples
1. Start with `01_basic_exposure.py`
2. Progress sequentially through each example
3. Read the comments and experiment with parameters
4. Refer to Chapter 8 in the book for theoretical background

### Running Individual Examples

```bash
# Activate virtual environment (from AutoExposure directory)
cd AutoExposure
source ../virtual_env/bin/activate

# Navigate to examples directory
cd examples

# Run examples individually
python 01_basic_exposure.py
python 02_image_statistics.py
python 03_spatial_analysis.py
# ... continue through all examples
```

## 📖 Code Structure

Each example file follows this structure:

1. **Header Comments** - Learning objectives and book section reference
2. **Function Definitions** - Core algorithms with detailed comments
3. **Demonstration Functions** - Step-by-step examples
4. **Main Function** - Runs demonstrations and shows results

## 💡 Key Concepts

### Example 1: Basic Exposure
- Exposure triangle (Time, Gain, Aperture)
- Brightness measurement
- Exposure compensation

### Example 2: Image Statistics
- Bayer statistics grid
- Histogram generation
- Saturated pixel detection

### Example 3: Spatial Analysis
- Center-weighted metering
- Exposure zone classification
- Spatial brightness distribution

### Example 4: Histogram Analysis
- Percentile calculation
- Dynamic range
- Exposure bias
- Entropy

### Example 5: Scene Analysis
- Scene type classification
- Face detection
- Motion estimation

### Example 6: Exposure Control
- TES calculation
- Exposure distribution
- Motion blur vs noise trade-off

### Example 7: Flicker Detection
- AC frequency detection
- Flicker mitigation
- Safe exposure times

### Example 8: APEX Calculation
- Bv, Av, Tv, Sv formulas
- EXIF metadata generation

### Example 9: Complete System
- Pipeline integration
- Real-time processing
- Temporal consistency

## 🎯 Exercises

After each example, try:

1. **Modify parameters** - See how changes affect results
2. **Add features** - Extend the functionality
3. **Test with real images** - Use your own camera data
4. **Compare algorithms** - Try different approaches

## 📝 Notes

- All examples are self-contained and can run independently
- Extensive comments explain each concept
- Examples build on previous concepts progressively
- Code matches the structure and concepts in Chapter 8

## 🔗 Related Files

- **../core/** - Production-ready implementation modules
- **../doc/CHAPTER_8_GUIDE.md** - Complete learning roadmap
- **../README.md** - Technical documentation
- **../doc/HOW_TO_RUN.md** - Quick start guide
