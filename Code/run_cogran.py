#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Kayla Barginda

Runs COGRAN inside Python script. For this the command line tool COGRAN is needed.

Uses python 'subprocess': all command line 'commands' must be given as strings in list. Variables are not given as strings. 
    
'''

import os 
import sys
import glob
import subprocess

DIR_PATH = ''

def changeDirectory(): 
  print(r'Code is located in: ' + os.getcwd()) #for double checking
  os.chdir(DIR_PATH)
  print(r'Current working directory: ' + os.getcwd())


def setData(country, iterate):

    if iterate == True:
        if country == 'London':
            for interpolated_data in glob.glob(r'interpolated/interpolatedData_as_polygon_LondonUK__*.geojson'):
                
                timestamp = str(interpolated_data[-16:-14])
                
                target = r'Districts/london_citydistricts.geojson'
                input_file = interpolated_data
                result = r'CoGran Output/London_disaggregated_30x30_'+ timestamp + '.geojson'
        
                runCogran(input_file, target, result)
            
        if country == 'Hamburg':
            for interpolated_data in glob.glob(r'interpolated/interpolatedData_as_polygon_HamburgDE_*.geojson'):
            
                timestamp = str(interpolated_data[-16:-14])
                target = r'Districts/hamburg_citydistricts.geojson'
                input_file = interpolated_data
        
                result = r'CoGran Output/Hamburg_disaggregated_30x30_' + timestamp + '.geojson'
            
                runCogran(input_file, target, result)
   
    if iterate == False: #default: t = 00:00
       if country == 'London':
           target = r'Districts/london_citydistricts.geojson'
           input_file = r'interpolated/interpolatedData_as_polygon_LondonUK__16_30x30.geojson'
           #input_file = r'london_no2conc_satellitedata_13092020_16.geojson'
           result = r'CoGran Output/London_disaggregated_30x30'+ '_16' + '.geojson'
           
           runCogran(input_file, target, result)
           
       if country == 'Hamburg':
           target = r'Districts/hamburg_citydistricts.geojson'
           input_file = r'interpolated/interpolatedData_as_polygon_HamburgDE_08_30x30.geojson'
           result = r'CoGran Output/Hamburg_disaggregated_30x30'+ '_08'+ '.geojson'
           
           runCogran(input_file, target, result)
      
    
    #cogran -d -i path/input.geojson -t path/target.geojson -o path/output.geojson --attr attributeName    

def runCogran(input_file, target, result):
    cogran = subprocess.run(['cogran', '-d', '-i', input_file, '-t', target, '-o', result, '--attr', 'no2_interpolated', '--mode', 'arealWeightingRelative'])

def main(): 

    try:
        changeDirectory()
        
        setData(country = 'London', iterate = True)

        sys.exit(0)
   
    except Exception as ex:
        print('Error: ' + str(ex))
        sys.exit(1)
        
if __name__ == '__main__':
    main()
