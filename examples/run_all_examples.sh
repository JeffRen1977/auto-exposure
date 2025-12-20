#!/bin/bash
# Run All Examples - Chapter 8 Auto Exposure
# 
# This script runs all progressive learning examples in order
#
# Usage:
#   ./run_all_examples.sh          # Run all examples with pauses
#   ./run_all_examples.sh --skip   # Run all without pauses
#   ./run_all_examples.sh 3        # Start from example 3

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment should be activated
if [ -f "../../virtual_env/bin/activate" ]; then
    echo "Activating virtual environment..."
    source ../../virtual_env/bin/activate
fi

# Run the Python script
python3 run_all_examples.py "$@"
