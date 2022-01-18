#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Kayla Barginda

This files runs CoGran for the simulated data. Note: File names need to be changed manually.

'''

import os 
import sys
import subprocess

'''
London
'''
#target = r'london_citydistricts.geojson'
#input_file = r'simulatedInterpolation_as_polygon_LondonUK_30x30.geojson'
#result = r'simulatedDisaggregation_relArealWeighting_LondonUK_30x30.geojson'

'''
Hamburg
'''
target = r'districts/hamburg_citydistricts.geojson'
input_file = r'interpolated/simulatedInterpolation_as_polygon_HamburgDE_30x30.geojson'
result = r'disaggregated/simulatedDisaggregation_relArealWeighting_HamburgDE_30x30.geojson'

'''
CoGran
'''

#cogran -d -i path/input.geojson -t path/target.geojson -o path/output.geojson --attr attributeName    
cogran = subprocess.run(["cogran", "-d", "-i", input_file, "-t", target, "-o", result, "--attr", "interpolated", "--mode", "arealWeightingRelative"])
