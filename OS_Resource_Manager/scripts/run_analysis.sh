#!/bin/bash
# Bash Script for Automated OS Resource Manager Analysis
# This script demonstrates Bash integration with Python

echo "========================================================================"
echo "     OS RESOURCE MANAGER - AUTOMATED ANALYSIS SCRIPT"
echo "========================================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed or not in PATH"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"
echo ""

# Create output directory if not exists
mkdir -p ../output/automated_runs

# Run automated tests
echo "📊 Running Automated Analysis..."
echo "--------------------------------"

# You can add automated runs here when the application supports CLI arguments
echo "1. Running scheduling algorithm comparison..."
echo "   (Manual mode: Please run main.py and select options)"

echo ""
echo "2. Running memory allocation comparison..."
echo "   (Manual mode: Please run main.py and select options)"

echo ""
echo "3. Running deadlock detection..."
echo "   (Manual mode: Please run main.py and select options)"

echo ""
echo "========================================================================"
echo "AUTOMATED ANALYSIS COMPLETE"
echo "========================================================================"
echo ""
echo "Results saved in: output/automated_runs/"
echo "Charts saved in: output/charts/"
echo "Logs saved in: output/system.log"
echo ""
echo "To view detailed results, run:"
echo "  python3 ../main.py"
echo ""
