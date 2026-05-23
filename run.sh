#!/bin/bash

# Work Logger Application Launcher for Linux/Mac

# Check if Conda is installed
if ! command -v conda &> /dev/null; then
    echo "ERROR: Conda is not installed"
    echo "Please install Anaconda or Miniconda"
    echo "Visit: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Source conda
eval "$(conda shell.bash hook)"

# Activate environment
echo "Activating conda environment 'worklogger'..."
conda activate worklogger

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Environment 'worklogger' not found"
    echo "Please run setup first:"
    echo "  conda env create -f environment.yml"
    exit 1
fi

echo "Starting Work Logger Application..."
python launcher.py

# Deactivate environment
conda deactivate
