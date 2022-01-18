#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 12:24:36 2021

@author: kayla
"""

import os
import pandas as pd 
import glob
import geopandas 
import matplotlib.pyplot as plt 
import sys


def change_dir():
    print("\nDirectory Change:" + "\nCode is located in: " + os.getcwd()) #for double checking
    os.chdir('/Users/kayla/OneDrive/Geodäsie und Geoninformatik (M.Sc.)/4. Semester/Thesis/')
    print("\nCurrent working directory: " + os.getcwd()) #for double checking

def convertCRS_London(): 
    file_path  = r"Data/Stadtteile/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp"
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