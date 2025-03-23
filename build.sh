#!/bin/bash

# Create a directory to store the dependencies and source code
rm -r build
mkdir build

# Install dependencies into the directory
pip install -r requirements.txt --target build

# Copy the source code into the directory
cp -r webpig build/

# Create an executable archive with an entry point (assuming main() is in main.py)
python -m zipapp build -c -o webpig.pyz -m webpig.__main__:main -p "/usr/bin/env python"
