# Chapter 8: Auto Exposure - Code Organization Guide

This repository contains the complete implementation for Chapter 8 of "Mobile Computational Photography". The code is organized to help readers understand the concepts progressively, from basic principles to advanced techniques.

## 📚 Learning Path

### Level 1: Core Concepts (Start Here)
**Files:** `01_basic_exposure.py`, `02_image_statistics.py`

**Concepts Covered:**
- What is exposure? (Exposure Time, Gain, Aperture)
- How to measure image brightness
- Basic exposure calculation

**Learning Objectives:**
- Understand the exposure triangle
- Calculate simple exposure compensation
- Extract basic image statistics

### Level 2: Spatial Analysis
**Files:** `03_spatial_analysis.py`

**Concepts Covered:**
- Center-weighted metering
- Exposure zones (highlights, midtones, shadows)
- Spatial brightness distribution

**Learning Objectives:**
- Implement center-weighted metering
- Classify pixels into exposure zones
- Understand spatial statistics

### Level 3: Histogram Analysis
**Files:** `04_histogram_analysis.py`

**Concepts Covered:**
- Histogram interpretation
- Dynamic range calculation
- Exposure bias detection
- Shannon entropy

**Learning Objectives:**
- Analyze image histograms
- Calculate dynamic range
- Detect exposure bias
- Understand entropy as image complexity measure

### Level 4: Scene Understanding
**Files:** `05_scene_analysis.py`

**Concepts Covered:**
- Scene type classification
- Face detection for exposure
- Motion estimation
- Scene-aware exposure adjustment

**Learning Objectives:**
- Classify different scene types
- Detect faces and prioritize exposure
- Estimate motion levels
- Adjust exposure based on scene context

### Level 5: Exposure Control
**Files:** `06_exposure_controller.py`

**Concepts Covered:**
- Total Exposure Sensitivity (TES)
- Exposure distribution (Time vs Gain)
- Motion blur vs noise trade-off
- Exposure limits

**Learning Objectives:**
- Calculate TES from brightness
- Distribute exposure between time and gain
- Balance motion blur and noise
- Apply exposure constraints

### Level 6: Advanced Features
**Files:** `07_flicker_detection.py`, `08_apex_calculation.py`

**Concepts Covered:**
- AC flicker detection (50Hz/60Hz)
- Flicker mitigation
- APEX value calculation
- EXIF metadata generation

**Learning Objectives:**
- Detect and prevent flicker artifacts
- Calculate APEX values (Bv, Av, Tv, Sv)
- Generate EXIF metadata

### Level 7: Complete System
**Files:** `09_complete_ae_system.py`, `auto_exposure_system.py`

**Concepts Covered:**
- System integration
- Processing pipeline
- Temporal consistency
- Real-time operation

**Learning Objectives:**
- Integrate all components
- Build complete AE pipeline
- Maintain temporal consistency
- Optimize for real-time performance

## 🗂️ File Organization

```
AutoExposure/
├── README.md                    # Technical documentation
│
├── doc/                         # Documentation folder
│   ├── CHAPTER_8_GUIDE.md      # This file - learning roadmap
│   ├── CODE_ORGANIZATION.md    # Code organization guide
│   └── HOW_TO_RUN.md           # Quick start guide
│
├── examples/                    # Progressive learning examples
│   ├── 01_basic_exposure.py           # Level 1: Core concepts
│   ├── 02_image_statistics.py        # Level 1: Statistics extraction
│   ├── 03_spatial_analysis.py         # Level 2: Spatial metering
│   ├── 04_histogram_analysis.py       # Level 3: Histogram analysis
│   ├── 05_scene_analysis.py          # Level 4: Scene understanding
│   ├── 06_exposure_controller.py     # Level 5: Exposure control
│   ├── 07_flicker_detection.py       # Level 6: Flicker handling
│   ├── 08_apex_calculation.py       # Level 6: APEX values
│   └── 09_complete_ae_system.py      # Level 7: Full system
│
├── core/                        # Core implementation modules
│   ├── auto_exposure_system.py       # Complete AE system
│   ├── spatial_analyzer.py           # Spatial analysis module
│   ├── histogram_analyzer.py         # Histogram analysis module
│   ├── scene_analyzer.py             # Scene analysis module
│   ├── exposure_controller.py        # Exposure control module
│   └── flicker_detector.py           # Flicker detection module
│
└── tests/                       # Test suite
    └── test_ae_system.py            # Complete test suite with RAW10 loader
```

## 🎯 How to Use This Code with Chapter 8

### For Students/Learners

1. **Start with Level 1** - Read the book section, then run `examples/01_basic_exposure.py`
2. **Progress sequentially** - Each example builds on previous concepts
3. **Experiment** - Modify parameters and see the effects
4. **Read the code** - Extensive comments explain each concept
5. **Check the book** - Code examples map to book sections

### For Instructors

1. **Use examples in lectures** - Each file demonstrates specific concepts
2. **Assign progressive exercises** - Start with Level 1, progress to Level 7
3. **Reference code in book** - Code is organized to match book structure
4. **Use test suite** - Demonstrate real-world application

### For Practitioners

1. **Use core modules** - Production-ready implementation in `core/`
2. **Customize components** - Each module is independent
3. **Extend functionality** - Clear interfaces for adding features
4. **Reference documentation** - Complete API docs in README

## 📖 Code-to-Book Mapping

### Section 8.1: Introduction to Auto Exposure
- **Code:** `examples/01_basic_exposure.py`
- **Concepts:** Exposure triangle, brightness measurement

### Section 8.2: Image Statistics Extraction
- **Code:** `examples/02_image_statistics.py`
- **Concepts:** Bayer statistics, histogram generation

### Section 8.3: Spatial Analysis and Metering
- **Code:** `examples/03_spatial_analysis.py`, `core/spatial_analyzer.py`
- **Concepts:** Center-weighted metering, exposure zones

### Section 8.4: Histogram-Based Analysis
- **Code:** `examples/04_histogram_analysis.py`, `core/histogram_analyzer.py`
- **Concepts:** Dynamic range, exposure bias, entropy

### Section 8.5: Scene Understanding
- **Code:** `examples/05_scene_analysis.py`, `core/scene_analyzer.py`
- **Concepts:** Scene classification, face detection, motion

### Section 8.6: Exposure Control Algorithms
- **Code:** `examples/06_exposure_controller.py`, `core/exposure_controller.py`
- **Concepts:** TES calculation, exposure distribution

### Section 8.7: Advanced Features
- **Code:** `examples/07_flicker_detection.py`, `examples/08_apex_calculation.py`
- **Concepts:** Flicker mitigation, APEX values

### Section 8.8: System Integration
- **Code:** `examples/09_complete_ae_system.py`, `core/auto_exposure_system.py`
- **Concepts:** Pipeline integration, real-time operation

## 🚀 Quick Start for Chapter 8

### Option 1: Run All Examples Automatically (Recommended)

```bash
# 1. Setup environment (from AutoExposure directory)
cd AutoExposure
source ../virtual_env/bin/activate
pip install -r requirements.txt

# 2. Run all examples in order
cd examples
python run_all_examples.py

# Or run without pauses
python run_all_examples.py --skip

# Or start from a specific example
python run_all_examples.py 3  # Start from example 3
```

### Option 2: Run Examples Individually

```bash
# 1. Setup environment (from AutoExposure directory)
cd AutoExposure
source ../virtual_env/bin/activate
pip install -r requirements.txt

# 2. Start with Level 1
python examples/01_basic_exposure.py

# 3. Progress through examples
python examples/02_image_statistics.py
python examples/03_spatial_analysis.py
# ... continue through Level 7

# 4. Run complete system
python tests/test_ae_system.py
```

## 💡 Key Concepts Demonstrated

### Concept 1: Exposure Triangle
**File:** `examples/01_basic_exposure.py`
- Shows relationship between exposure time, gain, and aperture
- Demonstrates exposure compensation

### Concept 2: Metering Modes
**File:** `examples/03_spatial_analysis.py`
- Center-weighted metering implementation
- Zone-based exposure analysis

### Concept 3: Histogram Analysis
**File:** `examples/04_histogram_analysis.py`
- Dynamic range calculation
- Exposure bias detection
- Entropy as complexity measure

### Concept 4: Scene-Aware Exposure
**File:** `examples/05_scene_analysis.py`
- Scene type classification
- Face-aware exposure
- Motion-based adjustment

### Concept 5: Exposure Distribution
**File:** `examples/06_exposure_controller.py`
- TES calculation
- Time vs gain trade-off
- Motion blur vs noise balance

### Concept 6: Flicker Mitigation
**File:** `examples/07_flicker_detection.py`
- AC flicker detection
- Exposure time adjustment

### Concept 7: APEX System
**File:** `examples/08_apex_calculation.py`
- Bv, Av, Tv, Sv calculation
- EXIF metadata generation

### Concept 8: Complete Pipeline
**File:** `examples/09_complete_ae_system.py`
- End-to-end processing
- Real-time operation

## 📝 Exercises and Assignments

### Exercise 1: Basic Exposure (Level 1)
- Modify target brightness and observe changes
- Calculate exposure compensation for different scenes

### Exercise 2: Metering (Level 2)
- Implement spot metering (center region only)
- Compare center-weighted vs average metering

### Exercise 3: Histogram Analysis (Level 3)
- Calculate histogram for different exposure levels
- Detect over/under exposure from histogram

### Exercise 4: Scene Classification (Level 4)
- Add new scene types (e.g., sunset, night)
- Implement custom scene detection

### Exercise 5: Exposure Control (Level 5)
- Modify TES calculation formula
- Experiment with different exposure distribution strategies

### Exercise 6: Flicker (Level 6)
- Test with different AC frequencies
- Implement adaptive flicker detection

### Exercise 7: Integration (Level 7)
- Add temporal smoothing
- Implement exposure bracketing

## 🔗 Additional Resources

- **README.md** - Complete technical documentation
- **doc/HOW_TO_RUN.md** - Detailed usage instructions
- **doc/CODE_ORGANIZATION.md** - Code organization guide
- **Book Chapter 8** - Theoretical foundations
- **Test Suite** - Real-world examples with RAW data

## 📧 Questions?

Refer to:
1. Code comments (extensive inline documentation)
2. README.md (technical details)
3. Book Chapter 8 (theoretical background)
4. Example files (progressive learning)

---

**Note:** This code is designed to complement Chapter 8 of "Mobile Computational Photography". Each example file focuses on specific concepts and includes detailed comments explaining the implementation.
