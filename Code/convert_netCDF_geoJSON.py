#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kayla Barginda (6066945)

netCDF zu geoJSON Datei 

+ forces WGS84 projection on raster netCDF data


"""

#from netCDF4 import Dataset
import sys
import os

import pandas as pd
import geopandas 
from shapely.geometry import Polygon
import xarray as xr
import matplotlib.pyplot as plt 

GET_PATH = r'Daten/Copernicus/CAMS Dateien/HamburgDE/'
SAVE_PATH = r'Daten/Copernicus/CSV Dateien/'
SET_DATE = '2021-08-07'

def change_dir():
    print("\nDirectory Change:" + "\nCode is located in: " + os.getcwd()) #for double checking
    os.chdir('/Users/kayla/OneDrive/Geodäsie und Geoninformatik (M.Sc.)/4. Semester/Thesis/')
    print("\nCurrent working directory: " + os.getcwd()) #for double checking
    
#convert netCDF to a CSV file
def netCDF_csv(nc_file):
    nc_1 = xr.open_dataset(nc_file)
    nc_1.no2_conc.to_dataframe().to_csv(SAVE_PATH + 'no2_conc_DE_070821.csv')
    
    no_1 = xr.open_dataset(nc_file)
    no_1.no_conc.to_dataframe().to_csv(SAVE_PATH + 'no_conc_DE_070821.csv')
    

def setDataframe_ESA(df):

    input_df = pd.read_csv(df)
    
    #removes "[0] days" ---> keeps time only
    input_df['time'] = input_df['time'].map(lambda val: str(val)[6:])
    input_df['time'] = input_df[['time']].astype('string') + " " + SET_DATE
    
    #level -> int 
    input_df['level'] = input_df[['level']].astype('int')
    
    #Y-M-D H-M-S
    input_df['time'] = pd.to_datetime(input_df['time'])
    
    input_df.drop(input_df[input_df["longitude"] >= 10.35].index, inplace = True)
    print(input_df)
          
    
    input_df = geopandas.GeoDataFrame(input_df, geometry=geopandas.points_from_xy(input_df.longitude, input_df.latitude))
    input_df = geopandas.GeoDataFrame(input_df, crs='EPSG:4326') #set CRS to WGS84
    
  
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    ax = world[world.name == 'Germany'].plot(color = 'white', edgecolor = 'black')
    ax.set(xlim=(9,11), ylim=(53.2,54))
    input_df.plot(ax=ax, color='blue')
    plt.show()
    
    
    polygon_df = input_df.copy()
    res = 0.1 #Aufflösung laut ESA: 0.1º x 0.1 º = 10km x 10km 
    kacheln = []
    
    for index, row in polygon_df.iterrows():
        lon = row.longitude
        lat = row.latitude
        kachel = Polygon([(lon, lat), ((lon + res), lat), ((lon + res), (lat - res)), (lon, (lat - res))])
        kacheln.append(kachel)
    polygon_df['geometry'] = kacheln
    
    
    #Testing to see if data is correctly formatted 
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    ax = world[world.name == 'Germany'].plot(color = 'white', edgecolor = 'black')
    ax.set(xlim=(9,11), ylim=(53.2,54))
    polygon_df.plot(ax=ax, color='pink')
    plt.show()
    
    
    if {'no2_conc'}.issubset(input_df.columns):
        polygon_df_0 = polygon_df.copy()
        polygon_df_0 = polygon_df_0.loc[polygon_df_0['time'] == "2021-08-07 00:00:00"]
    
        input_df.to_file('Output/geoJSON/no2_conc_HamburgDE_07082021.geojson', driver = 'GeoJSON')
        polygon_df_0.to_file('Output/geoJSON/POLYGONno2_conc_HamburgDE_07082021.geojson', driver = 'GeoJSON')
        print(input_df.columns)
        print(polygon_df_0.columns)
        
        print("\nInput file " + "[ " + df[29:] + " ]" + " converted to geoJSON")
        
    if {'no_conc'}.issubset(input_df.columns):
        polygon_df_0 = polygon_df.copy()
        polygon_df_0 = polygon_df_0.loc[polygon_df_0['time'] == "2021-08-07 00:00:00"]
    
        input_df.to_file('Output/geoJSON/no_conc_HamburgDE_07082021.geojson', driver = 'GeoJSON')
        polygon_df_0.to_file('Output/geoJSON/POLYGONno_conc_HamburgDE_07082021.geojson', driver = 'GeoJSON')
        print(input_df.columns)
        print(polygon_df_0.columns)
        
        print("\nInput file " + "[ " + df[29:] + " ]" + " converted to geoJSON")
"""
def setDataframe_openAQ(df): 
    input_df = pd.read_csv(df)
    
    #sets UTC column to datatime formate + UTC stamp
    input_df['utc'] = pd.to_datetime(input_df['utc'], 
                                       format='%Y-%m-%d %H:%M:%S.%f', 
                                       errors='coerce')
    
    temp_df = input_df.rename({'value': 'pm25_value'}, axis = 1)
    temp_df = temp_df.drop(['parameter', 'unit', 'local', 'country'], axis = 1)
    
    input_df = temp_df

    input_df = geopandas.GeoDataFrame(input_df, geometry=geopandas.points_from_xy(input_df.longitude, input_df.latitude))
    input_df = geopandas.GeoDataFrame(input_df, crs='EPSG:4326') #set CRS to WGS84
    

    
    input_df.to_csv('quebec_csv2.csv',index=False)
    
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    #print(world.columns)
    
    
    #Testing to see if data is correctly formatted 
    ax = world[world.name == 'Canada'].plot(color = 'white', edgecolor = 'black')
    ax.set(xlim= (-77, -70), ylim=(45.5, 48))
    input_df.plot(ax=ax, color='blue')
    plt.show()
"""  
    
    
def main(): 

    try:
        change_dir()
        
        # ESA
       
        dataESA_HH_layer0 = GET_PATH + r'HH_NO_NO2_08072021_EURADIM_ANALYSIS.nc'
        
        dataESA_HH_layer0_csv_no2 = SAVE_PATH + r'no2_conc_DE_070821.csv' #no2    
        dataESA_HH_layer0_csv_no = SAVE_PATH + r'no_conc_DE_070821.csv' #no
 
        #Calling functions
        netCDF_csv(dataESA_HH_layer0)
        
        setDataframe_ESA(dataESA_HH_layer0_csv_no2)  #no2
        setDataframe_ESA(dataESA_HH_layer0_csv_no)  #no
        
        
        
        # OpenAQ
        
        #dataOpenAQ_csv = r'Daten/openAQ/Quebec_pm25_240721_250721.csv'
        #setDataframe_openAQ(dataOpenAQ_csv)

        sys.exit(0)
   
    except Exception as ex:
        print("Error: " + ex)
        sys.exit(1)
        
if __name__ == "__main__":
    main()




