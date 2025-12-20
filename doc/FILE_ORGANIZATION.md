# File Organization Guide

## Auto Exposure System Files

### Main Implementation

**Use this file:** `core/auto_exposure_system.py`

This is the **production-ready** implementation of the Auto Exposure System. It contains:
- Complete AE system with all 6 core components
- Production-ready code optimized for real-world use
- Full API with all features
- Well-tested and documented

### How to Import

```python
# Correct import (use this)
from core.auto_exposure_system import AutoExposureSystem, SensorInfo, SceneType

# Initialize and use
ae_system = AutoExposureSystem()
sensor_info = SensorInfo(exposure_time=1/60, analog_gain=2.0, digital_gain=1.0, iso=200, aperture=2.8)
result = ae_system.process_frame(image, sensor_info)
```

### Why `core/auto_exposure_system.py`?

1. **Organization**: Follows standard project structure
   - `core/` = Production code
   - `examples/` = Learning examples
   - `doc/` = Documentation

2. **Clarity**: Clear separation between:
   - Production implementation (`core/`)
   - Educational examples (`examples/`)
   - Test scripts (root)

3. **Maintainability**: Easier to maintain and extend
   - Core code in one place
   - Examples can reference core modules
   - Clear dependencies

## File Structure

```
AutoExposure/
├── core/
│   └── auto_exposure_system.py    ← USE THIS (Production code)
│
├── examples/
│   ├── 01_basic_exposure.py       (Educational examples)
│   ├── 02_image_statistics.py
│   ├── ...
│   └── 09_complete_ae_system.py
│
├── tests/                          # Test suite
│   └── test_ae_system.py          (Complete test - imports from core)
└── README.md                       (Documentation)
```

## Migration from Old Import

If you have code using the old import:

**Old (removed):**
```python
from auto_exposure_system import AutoExposureSystem
```

**New (use this):**
```python
from core.auto_exposure_system import AutoExposureSystem
```

## Examples Usage

The example files in `examples/` are self-contained and don't import from core. They demonstrate concepts step-by-step.

For production use, import from `core/auto_exposure_system.py`.

## Summary

- **For production/real use**: Import from `core/auto_exposure_system.py`
- **For learning**: Use files in `examples/` directory
- **For testing**: Use `tests/test_ae_system.py` (already updated)

The root `auto_exposure_system.py` has been removed to avoid confusion. All code now uses `core/auto_exposure_system.py`.
