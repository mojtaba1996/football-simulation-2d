#!/bin/bash

# Directory containing your Python files
CODE_DIR="."

# Run pylint for all Python files in the directory and subdirectories
echo "Running pylint on all Python files..."
find $CODE_DIR -name "*.py" | xargs pylint

# Run mypy for type checking on all Python files in the directory and subdirectories
echo "Running mypy on all Python files..."
find $CODE_DIR -name "*.py" | xargs mypy
