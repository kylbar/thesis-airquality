#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Kayla Barginda


About format_satellite.py: 
    
    This code formats the CAMS satellite data so that it can be interpretated by GIS 
    softwares and read by the barnes_interpolation.py script. 
    
    Resolution of grid (as specified by the ESA): 10km x 10 km = 0.1 deg x 0.1 deg 
    
    changeDirectory(): changes the current working directory.
    convertnetCDF_city(): converts the CAMS netCDF files to 'pandas-friendly' CSV files. 
    formatSatelliteData_city(): formats the converted satellite data into the proper format for further data processing 
    and analysis. 
    
    All output files are saved as geoJSONs with the CRS: WGS84. 
    
'''

import sys
import os

import pandas as pd
import geopandas 
from shapely.geometry import Polygon
import xarray as xr #needed for the netCDF files
import matplotlib.pyplot as plt 

GET_PATH = r'Data/Copernicus/CAMS Data/'
SAVE_PATH = r'Data/Copernicus/CSV Data/'
DIR_PATH = ''

def changeDirectory():
    print('\nDirectory Change:' + '\nCode is located in: ' + os.getcwd()) #for double checking
    os.chdir(DIR_PATH)
    print('\nCurrent working directory: ' + os.getcwd()) #for double checking
    
def convertnetCDF_hamburg(nc_file):
    nc = xr.open_dataset(nc_file)
    nc.no2_conc.to_dataframe().to_csv(SAVE_PATH + 'hamburg_no2conc_07082021.csv')
    
def convertnetCDF_london(nc_file):
    nc = xr.open_dataset(nc_file)
    nc.no2_conc.to_dataframe().to_csv(SAVE_PATH + 'london_no2conc_13092020.csv')
    

def formatSatelliteData_hamburg(data):

    input_df = pd.read_csv(data)
    
    capture_date = '2021-08-07'
    
    # date reformatting
    input_df['time'] = input_df['time'].map(lambda time: str(time)[6:])
    input_df['time'] = input_df[['time']].astype('string') + ' ' + capture_date
    input_df['level'] = input_df[['level']].astype('int')
    input_df['time'] = pd.to_datetime(input_df['time']) #Y-M-D H-M-S
    
    input_df.drop(input_df[input_df['longitude'] >= 10.35].index, inplace = True) #removes excess tiles

    
    input_df = geopandas.GeoDataFrame(input_df, geometry=geopandas.points_from_xy(input_df.longitude, input_df.latitude))
    input_df = geopandas.GeoDataFrame(input_df, crs='EPSG:4326')
    
    output_df = input_df.copy()
    res = 0.1
    satellite_tiles = []
    
    # create polygons out of point (raster) data
    for index, row in output_df.iterrows():
        lon = row.longitude
        lat = row.latitude
        satellite_tile = Polygon([(lon, lat), 
                                  ((lon + res), lat), 
                                  ((lon + res), (lat - res)), 
                                  (lon, (lat - res))])
        satellite_tiles.append(satellite_tile)
    output_df['geometry'] = satellite_tiles
    
    #output_df.to_file('Output/hamburg_no2conc_satellitedata_07082021_all.geojson', driver = 'GeoJSON')

    output_df0 = output_df.copy()
    output_df0 = output_df0.loc[output_df0['time'] == '2021-08-07 00:00:00']
        
    output_df0.to_file('Output/hamburg_no2conc_satellitedata_07082021_00.geojson', driver = 'GeoJSON')
        
    
def formatSatelliteData_london(data): 
    
    input_df = pd.read_csv(data)
    
    capture_date = '2020-09-13'
    
    input_df['time'] = input_df['time'].map(lambda val: str(val)[6:])
    input_df['time'] = input_df[['time']].astype('string') + ' ' + capture_date
    input_df['time'] = pd.to_datetime(input_df['time'])
    input_df['level'] = input_df[['level']].astype('int')
    input_df['longitude'] = (input_df['longitude'] + 180) % 360 - 180 #convert negative coordinates to positive coordinates
    
        
    input_df = geopandas.GeoDataFrame(input_df, geometry=geopandas.points_from_xy(input_df.longitude, input_df.latitude))
    input_df = geopandas.GeoDataFrame(input_df, crs='EPSG:4326')
        
    output_df = input_df.copy()
    res = 0.1 
    satellite_tiles = []
    
    for index, row in output_df.iterrows():
        lon = row.longitude
        lat = row.latitude
        satellite_tile = Polygon([(lon, lat), 
                                  ((lon + res), lat), 
                                  ((lon + res), (lat - res)), 
                                  (lon, (lat - res))])
        satellite_tiles.append(satellite_tile)
    output_df['geometry'] = satellite_tiles
    
    
    output_df.to_file('Output/london_no2conc_satellitedata_13092020_all.geojson', driver = 'GeoJSON')

    output_df0 = output_df.copy()
    output_df0  = output_df0.loc[output_df0['time'] == '2020-09-13 00:00:00']

    output_df0.to_file('Output/london_no2conc_satellitedata_13092020_00.geojson', driver = 'GeoJSON')
    


    
def main(): 

    try:
        changeDirectory()
        
        '''
        Data cleaning
        '''
       
        hamburg_ncDataset = GET_PATH + r'HamburgDE/HH_NO_NO2_ENSEMBLE_08072021_ANALYSIS.nc'        
        hamburg_csvDataset = SAVE_PATH + r'hamburg_no2conc_07082021.csv'
        
    
        london_ncDataset = GET_PATH + r'LondonUK/LONDON_ALLE_13092021_ENSEMBLE_ANALYSIS.nc'
        london_csvDataset = SAVE_PATH + r'london_no2conc_13092020.csv'
    
        
        '''
        Export and format data
        '''
    
        convertnetCDF_hamburg(hamburg_ncDataset)
        convertnetCDF_london(london_ncDataset)
        
        formatSatelliteData_hamburg(hamburg_csvDataset)
        formatSatelliteData_london(london_csvDataset)
     
        
        sys.exit(0)
   
    except Exception as ex:
        print('Error: ' + str(ex))
        sys.exit(1)
        
if __name__ == '__main__':
    main()




