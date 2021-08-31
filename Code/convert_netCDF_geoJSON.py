#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kayla Barginda (6066945)

netCDF zu geoJSON Datei 

+ forces WGS84 projection on raster netCDF data


"""

#from netCDF4 import Dataset
#import shapely
import pandas as pd
import geopandas 
import xarray as xr
import matplotlib.pyplot as plt 
import os


GET_PATH = r'Daten/Copernicus/CAMS Dateien/HH_layer0/'
SAVE_PATH = r'Daten/Copernicus/CSV Dateien/'
SET_DATE = '2021-08-07'

#convert netCDF to a CSV file
def netCDF_csv(nc_file):
    nc_1 = xr.open_dataset(nc_file)
    nc_1.pm2p5_conc.to_dataframe().to_csv(SAVE_PATH + 'pm2p5_DE_070821.csv')

#import CSV file, set as DF, reformat time column 
#-> get ready to add projection + convert to geoJSON
def setDataframe(df):
    df_1 = pd.read_csv(df)
    
    #removes "[0] days" ---> keeps time only
    df_1['time'] = df_1['time'].map(lambda val: str(val)[6:])
    
    #level -> int 
    df_1['level'] = df_1[['level']].astype('int')
    
    #Y-M-D H-M-S
    df_1['time'] = pd.to_datetime(SET_DATE) + pd.Series([pd.Timedelta(t) for t in df_1['time']])
    
    
    df_1 = geopandas.GeoDataFrame(df_1, geometry=geopandas.points_from_xy(df_1.longitude, df_1.latitude))
    df_1 = geopandas.GeoDataFrame(df_1, crs='EPSG:4326') #set CRS to WGS84
    
    df_1.to_csv('pandas_csv.csv',index=False)
    
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    #print(world.columns)
    
    
    #Testing to see if data is correctly formatted 
    ax = world[world.name == 'Germany'].plot(color = 'white', edgecolor = 'black')
    df_1.plot(ax=ax, color='pink')
    plt.show()
    
    
    
    #print(df_1)
    #print(df_1.crs)
    #print(df_1.dtypes)

    df_1.to_file('Output/geoJSON Dateien/geopandas_df1.geojson', driver = 'GeoJSON')

def main(): 
    #Change working directory (due to save style of folders/data)
    print("Code is located in: " + os.getcwd()) #for double checking
    os.chdir('/Users/kayla/OneDrive/Geodäsie und Geoninformatik (M.Sc.)/4. Semester/Thesis/')
    print("Current working directory: " + os.getcwd()) #for double checking
    
    
    #data
    dataESA_HH_layer0 = GET_PATH + r'EURADIM_ANALYSIS_070821.nc'
    dataESA_HH_layer0_csv = SAVE_PATH + r'pm2p5_DE_070821.csv'
    
    #calling my functions
    netCDF_csv(dataESA_HH_layer0)
    
    setDataframe(dataESA_HH_layer0_csv)
    
    
    print("I'm converting things right now...")
    
if __name__ == "__main__":
    main()




