#!/bin/sh
python3 makesite.py
echo "Finished generating site"
cd _site
python3 -m http.server
