#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kayla Barginda (6066945) 

Runs COGRAN inside Python script. 

Needs: 
    - VALID geoJSONs
    
Uses python "subprocess" -> all command line "commands" must be given as strings in list. Variables not. 
    
"""

import os 
import subprocess


target = r'Ortsteile_-_Hamburg.geojson'

input_file = r'POLYGONno2_conc_HamburgDE_07082021.geojson'
result = r'COGRAN/sat_data_ortsteile_no2.geojson'

#Change working directory (due to save style of folders/data)
print("Code is located in: " + os.getcwd()) #for double checking
os.chdir('/Users/kayla/OneDrive/Geodäsie und Geoninformatik (M.Sc.)/4. Semester/Thesis/Output/geoJSON')
print("Current working directory: " + os.getcwd())


list_files = subprocess.run(["ls", "-l"])

#cogran --input <input_shape.shp> --target <target_shape.shp> --output <output_shape.shp> --attr <attribute_name>
#cogran -d -i path/input.geojson -t path/target.geojson -o path/output.geojson --attr attributeName
# test run
cogran = subprocess.run(["cogran", "-d", "-i", input_file, "-t", target, "-o", result, "--attr", "no2_conc", "--mode", "arealWeightingRelative"])