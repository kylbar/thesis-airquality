#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 14:23:04 2021

@author: kayla
"""

from netCDF4 import Dataset, num2date, date2num
import pandas as pd
import xarray as xr
#import os 

getPath = r'Daten/Copernicus/CAMS Dateien/'
savePath = r'Daten/Copernicus/CSV Dateien/'
dataESA = getPath + r'EURADIM_ANALYSIS.nc'

#Using Xarray
nc_1 = xr.open_dataset(dataESA)
nc_1.pm2p5_conc.to_dataframe().to_csv(savePath + 'pm2p5_DE.csv')

#Using pandas.Series

nc_2 = Dataset(dataESA, mode='r')
nc_2.variables.keys()

lon = nc_2.variables['longitude'][:]
lat = nc_2.variables['latitude'][:]
lvl = nc_2.variables['level'][:]

"""

Time format: 
    0 days 14:00:00
"""
t = nc_2.variables['time']
dtime = date2num(t[:], t.units, calendar=None)
pm2p5 = nc_2.variables['pm2p5_conc'][:]
#pm10
#no2

pm25_ts = pd.Series(pm2p5, index = dtime)
pm25_ts.to_csv('pandasTest.csv', index = True, header = True)




#nc_fid = Dataset(nc_DE, 'r')

#print(nc_fid)
#nc_fid.close()