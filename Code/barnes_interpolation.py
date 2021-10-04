#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Barnes Interpolation 
    - Interpolates sensor data with satellite data

TO DO: 
    - add comparison of interpolation (warum "Barnes" denn überhaupt?)
        -> Kriging (out wegen missing point data: how does it look for other data? England?)
        -> IDW (too simple -> out), show issue!!


@author: kayla
"""

import os
#import fiona
import numpy as np
import pandas as pd 
import glob
import geopandas
import matplotlib.pyplot as plt 
import sys
from shapely.geometry import shape, Point, Polygon, MultiPolygon

PATH = r'Interpolation/'

def change_dir():
    print("\nDirectory Change:" + "\nCode is located in: " + os.getcwd()) #for double checking
    os.chdir('/Users/kayla/OneDrive/Geodäsie und Geoninformatik (M.Sc.)/4. Semester/Thesis/')
    print("\nCurrent working directory: " + os.getcwd()) #for double checking
    
def barnes(punkte, kacheln):
    punkte = punkte.drop(['NO'], axis = 1)
    print(punkte.columns)
    #print(punkte.geometry)
    
    print(punkte[['latitude', 'longitude']].to_numpy())
    print(punkte[['NO2']].to_numpy())
    #print(df)

def main(): 

    try:
        change_dir()
        
        kacheln = PATH + 'POLYGONno2_conc_HamburgDE_07082021.geojson'
        poly = PATH + 'sat_data_ortsteile_no2.geojson'
        points = PATH + 'no2_conc_HamburgDE_Messstationen_07082021.geojson'
        
        hamburg_kacheln = geopandas.read_file(kacheln)
        hamburg_poly = geopandas.read_file(poly)
        hamburg_sensors = geopandas.read_file(points)
        print(hamburg_sensors.geometry.values)
        print(type(hamburg_sensors.geometry.values))
        barnes(hamburg_sensors, hamburg_kacheln)
      
            
            
            
            
        sys.exit(0)
   
    except Exception as ex:
        print("Error: " + ex)
        sys.exit(1)
        
if __name__ == "__main__":
    main()

