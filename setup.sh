#!/bin/bash

mkdir bitmaps tmp

python -m venv .venv

source .venv/bin/activate && pip install -r requirements.txt