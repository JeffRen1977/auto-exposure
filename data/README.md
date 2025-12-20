# Data Folder

This folder contains input data files for the Auto Exposure System.

## RAW10 Files

Place your RAW10 camera data files here. The test script (`tests/test_ae_system.py`) automatically looks for `*.raw` files in this folder.

### File Naming Convention

For automatic dimension detection, include dimensions in the filename:
- Format: `*_WIDTHxHEIGHT_*.raw`
- Example: `20250929_223233_713_RAW10_4032x756_RS_5056_PS_1_cam_3_sensor_raw_pd_frame__default_pd_type_622.raw`

### Current Data

- `20250929_223233_713_RAW10_4032x756_RS_5056_PS_1_cam_3_sensor_raw_pd_frame__default_pd_type_622.raw`
  - Dimensions: 4032 x 756 pixels
  - Format: RAW10 (10-bit packed Bayer)

## Adding Your Own Data

1. Copy your RAW10 files to this folder
2. Ensure filename contains dimensions (WIDTHxHEIGHT) for automatic parsing
3. Run `python tests/test_ae_system.py` from the parent directory

## Note

RAW files are typically large and are excluded from git (see `.gitignore`). 
This folder structure helps organize input data separately from code and outputs.
