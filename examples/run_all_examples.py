#!/usr/bin/env python3
"""
Run All Examples - Chapter 8 Auto Exposure

This script runs all progressive learning examples in order,
from basic concepts to the complete system.

Usage:
    python run_all_examples.py          # Run all examples
    python run_all_examples.py --skip   # Skip pauses between examples
    python run_all_examples.py 3        # Start from example 3
"""

import sys
import os
import subprocess
import time
from pathlib import Path


def get_example_files():
    """Get all example files in order"""
    examples_dir = Path(__file__).parent
    example_files = []
    
    # Get all numbered example files
    for i in range(1, 10):
        filename = f"{i:02d}_*.py"
        matches = list(examples_dir.glob(filename))
        if matches:
            example_files.append(matches[0])
    
    return sorted(example_files)


def run_example(filepath, skip_pause=False):
    """Run a single example file"""
    print("\n" + "=" * 80)
    print(f"Running: {filepath.name}")
    print("=" * 80)
    
    try:
        # Run the example
        result = subprocess.run(
            [sys.executable, str(filepath)],
            cwd=str(filepath.parent),
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✓ {filepath.name} completed successfully")
            return True
        else:
            print(f"\n✗ {filepath.name} failed with exit code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\n✗ Error running {filepath.name}: {e}")
        return False


def main():
    """Main function to run all examples"""
    # Parse arguments
    skip_pause = '--skip' in sys.argv or '-s' in sys.argv
    start_from = None
    
    # Check for start number
    for arg in sys.argv[1:]:
        if arg.isdigit():
            start_from = int(arg)
            break
    
    # Get all example files
    example_files = get_example_files()
    
    if not example_files:
        print("No example files found!")
        return
    
    # Filter by start number if specified
    if start_from:
        example_files = [f for f in example_files if int(f.stem.split('_')[0]) >= start_from]
    
    print("\n" + "=" * 80)
    print("CHAPTER 8 - AUTO EXPOSURE: RUNNING ALL EXAMPLES")
    print("=" * 80)
    print(f"\nFound {len(example_files)} example file(s) to run:")
    for i, f in enumerate(example_files, 1):
        print(f"  {i}. {f.name}")
    
    if not skip_pause:
        print("\nPress Enter to start, or Ctrl+C to cancel...")
        try:
            input()
        except KeyboardInterrupt:
            print("\nCancelled.")
            return
    
    # Run each example
    results = []
    for i, example_file in enumerate(example_files, 1):
        success = run_example(example_file, skip_pause)
        results.append((example_file.name, success))
        
        # Pause between examples (unless skipped)
        if not skip_pause and i < len(example_files):
            print("\n" + "-" * 80)
            print(f"Next: {example_files[i].name}")
            print("Press Enter to continue, or Ctrl+C to stop...")
            try:
                input()
            except KeyboardInterrupt:
                print("\n\nStopped by user.")
                break
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nCompleted: {successful}/{total} examples")
    print("\nResults:")
    for name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"  {status}: {name}")
    
    if successful == total:
        print("\n🎉 All examples completed successfully!")
        print("\nYou've completed the full learning path from basic concepts")
        print("to the complete auto exposure system!")
    else:
        print(f"\n⚠️  {total - successful} example(s) had issues.")
        print("Check the output above for details.")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

