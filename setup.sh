#!/bin/bash

mkdir -p tmp/svg tmp/bitmaps # Create the tmp dirs

mkdir -p ~/.local/share/fonts
cp source/fonts/Aldrich/Aldrich-Regular.ttf ~/.local/share/fonts/

python -m venv .venv # Build python virtual environment

source .venv/bin/activate && pip install -r requirements.txt # activate python virtual environment and install required packages