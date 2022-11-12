#!/bin/sh
python makesite.py
cd _site
python -m http.server