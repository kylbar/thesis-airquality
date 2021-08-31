#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kayla Barginda (6066945) 

Runs COGRAN inside Python script. 

Needs: 
    - VALID geoJSONs
    
"""

import os 
import subprocess

#GET_PATH = r'/geoJSON/'
testData1= r'wohnflaecheProEW_Stadtteile.geojson'
testData2 = r'arealWeightingRelative_wohnflaeche_stadtteileToBezirk.geojson'
testData = r'7_bezirke.geojson'

#Change working directory (due to save style of folders/data)
print("Code is located in: " + os.getcwd()) #for double checking
os.chdir('/Users/kayla/OneDrive/Geodäsie und Geoninformatik (M.Sc.)/4. Semester/Thesis/Output/geoJSON')
print("Current working directory: " + os.getcwd()) #for double checking


list_files = subprocess.run(["ls", "-l"])

#cogran --input <input_shape.shp> --target <target_shape.shp> --output <output_shape.shp> --attr <attribute_name>


# test run
TEST_run_cogran = subprocess.run(["cogran", "-d", "-i", testData1, "-t", testData, "-o", testData2, "--attr", "WFl_m2", "--mode", "arealWeightingRelative"])