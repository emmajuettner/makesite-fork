#!/bin/sh
python makesite.py
echo "Finished generating site"
cd _site
python -m http.server