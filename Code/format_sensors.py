#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Kayla Barginda | 6066945

About: 
    
    This code formats the sensor data so that it is compatible with the satellite data and can be
    further processed/ used for further analysis.
    
    The functions formatSensorData_hamburg() and formatSensorData_london() are both built on the 
    same logic. Due to the differences in the dataset formats, the formatting was split into two
    functions, one for each respective city used in the investigation of this thesis. 
    
    Some specifications about the functions: 
        
        - Both functions plot the positions of the sensors as a 'sanity check' measure. If something
        is wrong with the data or the data was not processed correctly by geopandas, the plot will
        indicate it (by being empty). 
        
        - All irrelevant data is dropped from the dataframes once read in by pandas (SO2, SO, etc.)
        
        - In the function formatSensorData_hamburg() the following should be considered:

            . Due to the original format of the date, the conversion using pd.to_datetime is wrong 
            such that the month position and day position are switched. Instead of 'Y-%m-%d %H:%M:%S'
            the date is formatted to 'Y-%d-%m %H:%M:%S'. 
    
    NOTE: 
        - The directory path in changeDirectory(), os.chdir() needs to be changed to the correct
        directory when running on a different machine. 
    
'''

import os
import pandas as pd 
import glob
import geopandas 
import matplotlib.pyplot as plt 
import sys

def changeDirectory():
    print(r'\nDirectory Change:' + '\nCode is located in: ' + os.getcwd()) #for double checking
    os.chdir(r'/Users/kayla/OneDrive/Geodäsie und Geoninformatik (M.Sc.)/4. Semester/Thesis/')
    print(r'\nCurrent working directory: ' + os.getcwd()) #for double checking

def controlSavepath(path):
    print(r'\nInput files located in ' + '[ ' + path + ' ]' + ' converted to geoJSON')


def formatSensorData_hamburg(): 
    
    '''
    Read in data. Multiple files!
    '''
    
    input_path = r'Data/luft.hamburg/hourly/07_08_2021'
    sensor_coordinates = r'Data/luft.hamburg/hamburg_sensor_coords.csv' #coordinates not included in measured data csv. added here
    sensor_files = glob.glob(input_path + r'/*.csv')
    input_dfs = (pd.read_csv(file, delimiter=(';'), header=0) for file in sensor_files) #read in and combine all csvs
   
    '''
    Data Formatting
    '''
    
    temp = pd.concat(input_dfs, ignore_index = True)
    temp = temp.drop(['SO2', 'NO (4m)', 'NO2 (4m)', 'Ozon', 'CO', 'NO'], axis=1) #delete columns I don't need
    temp = temp.fillna(0)

    coordinate_df = pd.read_csv(sensor_coordinates, delimiter=(';'), header = 0)
    output_df = pd.merge(temp, coordinate_df, left_on='Station', right_on='Station', right_index=False, how = 'left')
    
    output_df.rename(columns={'Messzeit': 'time'}, inplace = True) 
    output_df['time'] = pd.to_datetime(output_df['time']) # Month & day switched from standard. Formats to:'Y-%d-%m %H:%M:%S'
  
    
    '''
    Convert to Geopandas and set CRS
    '''
    
    output_df = geopandas.GeoDataFrame(output_df, geometry=geopandas.points_from_xy(output_df.longitude, output_df.latitude))
    output_df = geopandas.GeoDataFrame(output_df, crs='EPSG:4326')

    '''
    Plot for sanity check
    '''  
    
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    ax = world[world.name == 'Germany'].plot(color = 'white', edgecolor = 'black')
    ax.set(xlim=(9,11), ylim=(53.2,54))
    output_df.plot(ax=ax, color='orange')
    plt.show()
    
    '''
    Export Data
    '''
    
    output_df.to_csv(r'Output/misc/hamburg_no2conc_sensordata_07082021_all.csv')
    
    output_df0 = output_df.loc[output_df['time'] == '2021-07-08 00:00:00']
        
    output_df0.to_file(r'Output/hamburg_no2conc_sensordata_07082021_0.geojson', driver = 'GeoJSON') 
    controlSavepath(input_path)


def formatSensorData_london(): 
    input_path = r'Data/openAQ/London/London_13092020.csv'
    input_df = pd.read_csv(input_path, delimiter=(';'), header=0)
    input_df = input_df.drop(['locationId', 'city', 'country', 'local'], axis=1)
    
    temp = input_df.copy()
    temp['utc'] = temp['utc'].map(lambda val: str(val)[:-6])
    temp['utc'] = pd.to_datetime(temp['utc'])
    temp.rename(columns={'utc': 'time'}, inplace = True)
    
    
    temp.loc[temp['unit'] == 'ppm', 'value'] = 1000 * (temp['value'] * 0.0409 * 46.01) #convert ppm to mcg/m³
    temp['unit'].replace({'ppm': 'mcg/m3'}, inplace = True)
    
    output_df = temp
    output_df = geopandas.GeoDataFrame(output_df, geometry=geopandas.points_from_xy(output_df.longitude, output_df.latitude))
    output_df = geopandas.GeoDataFrame(output_df, crs='EPSG:4326')
    output_df = output_df.copy()
   
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    ax = world[world.name == 'United Kingdom'].plot(color = 'white', edgecolor = 'black')
    ax.set(xlim=(0.23, -0.4), ylim=(51.35,51.7))
    output_df.plot(ax=ax, color='orange')
    plt.show()
    
    output_df.to_csv(r'Output/misc/london_no2conc_sensordata_13092020_all.csv')
    output_df0 = output_df.copy()
    
    output_df0 = output_df.loc[output_df['time'] == '2020-09-13 00:00:00']
    output_df0 = output_df0.loc[output_df0['parameter'] == 'no2']
    
    output_df0.to_file(r'Output/london_no2conc_sensordata_13092020_00.geojson', driver = 'GeoJSON')
    controlSavepath(input_path)
    
    
def main(): 
    
    try: 
        changeDirectory()
        
        formatSensorData_hamburg()
        formatSensorData_london()
        
        sys.exit(0)
        
    except Exception as ex:
        print('Error: ' + str(ex))
        sys.exit(1)

if __name__ == '__main__':
    main()
