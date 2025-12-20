# Running All Examples

This directory contains scripts to easily run all progressive learning examples.

## Quick Start

### Run All Examples (Recommended)

```bash
# From AutoExposure directory
cd AutoExposure
source ../virtual_env/bin/activate
cd examples

# Run all examples with pauses between each
python run_all_examples.py
```

### Options

```bash
# Run without pauses (faster)
python run_all_examples.py --skip

# Start from a specific example number
python run_all_examples.py 3        # Start from example 3
python run_all_examples.py 5        # Start from example 5

# Using shell script (Unix/Mac)
./run_all_examples.sh
./run_all_examples.sh --skip

# Using batch script (Windows)
run_all_examples.bat
run_all_examples.bat --skip
```

## What the Script Does

1. **Finds all examples** - Automatically detects `01_*.py` through `09_*.py`
2. **Runs in order** - Executes examples sequentially (Level 1 → Level 7)
3. **Shows progress** - Displays which example is running
4. **Provides summary** - Shows which examples passed/failed at the end

## Example Output

```
================================================================================
CHAPTER 8 - AUTO EXPOSURE: RUNNING ALL EXAMPLES
================================================================================

Found 9 example file(s) to run:
  1. 01_basic_exposure.py
  2. 02_image_statistics.py
  3. 03_spatial_analysis.py
  ...

Press Enter to start, or Ctrl+C to cancel...

================================================================================
Running: 01_basic_exposure.py
================================================================================
[Example output...]
✓ 01_basic_exposure.py completed successfully

[Continues through all examples...]

================================================================================
SUMMARY
================================================================================

Completed: 9/9 examples

Results:
  ✓ PASSED: 01_basic_exposure.py
  ✓ PASSED: 02_image_statistics.py
  ...
  ✓ PASSED: 09_complete_ae_system.py

🎉 All examples completed successfully!
```

## Running Individual Examples

If you prefer to run examples one at a time:

```bash
cd examples
python 01_basic_exposure.py
python 02_image_statistics.py
# ... continue manually
```

## Troubleshooting

### Issue: "No example files found"

**Solution:** Make sure you're in the `examples/` directory:
```bash
cd examples
python run_all_examples.py
```

### Issue: Import errors

**Solution:** Make sure virtual environment is activated:
```bash
source ../virtual_env/bin/activate
```

### Issue: Permission denied (shell script)

**Solution:** Make script executable:
```bash
chmod +x run_all_examples.sh
```

## Tips

- Use `--skip` flag for faster execution during testing
- Start from a specific example number if you've already completed earlier ones
- Read the output of each example to understand the concepts
- Refer to Chapter 8 in the book while running examples

## Next Steps

After running all examples:
1. Review the output to understand each concept
2. Experiment by modifying example code
3. Run the complete test suite: `python tests/test_ae_system.py`
4. Use the production code: `from core.auto_exposure_system import AutoExposureSystem`
