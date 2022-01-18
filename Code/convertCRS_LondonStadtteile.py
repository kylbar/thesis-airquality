#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kayla Barginda
"""

import os
import pandas as pd 
import glob
import geopandas 
import matplotlib.pyplot as plt 
import sys

PATH = ''
DATA = ''

def change_dir():
    print("\nDirectory Change:" + "\nCode is located in: " + os.getcwd()) #for double checking
    os.chdir(PATH)
    print("\nCurrent working directory: " + os.getcwd()) #for double checking

def convertCRS_London(): 
    file_path  = DATA
    df = geopandas.read_file(file_path)
    
    temp = df[['NAME', 'geometry']]
    temp = temp.to_crs(epsg=4326)
    
    output_df = temp
    
    output_df.to_file('Output/LondonBoroughs.geojson', driver = 'GeoJSON')
    #print(temp.crs)
    
    

def main(): 
    
    try: 
        change_dir()
        convertCRS_London()
        sys.exit(0)
        
    except Exception as ex:
        print("Error: " + str(ex))
        sys.exit(1)

if __name__ == "__main__":
    main()
