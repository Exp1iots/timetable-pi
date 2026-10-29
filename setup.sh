#!/bin/bash

mkdir -p tmp/svg tmp/bitmaps

python -m venv .venv

source .venv/bin/activate && pip install -r requirements.txt