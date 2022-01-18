#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Kayla Barginda

Functions: 
    changeDirectory(): changes current working directory
    
    calcDistance(X, Y, coords): calculates the distance between points
        
    findIndicesofClosestPoints(x, y, coords): finds the point (or the closest point) on the interpolation grid
    for the second Barnes pass comparison (compares the real data to the interpolated value that is at that point)
    
    formatData(): formats the data such that it can be passed to the Barnes interpolation functions. Returns 4
    numpy arrays
    
    barnes_firstPass()/ barnes_secondPass(): calculates the first and second pass of the Barnes Interpolationscheme
    ---> Interpolates sensor data with satellite data
        
        x: one dimensional coordinate array, e.g. x = np.linspace(45, 55, 100)
        y: one dimensional coordinate array, e.g. y = np.linspace(0, 10, 200)
        sensor_coords: coordinates of the point measurements. Array of 2-element arrays, e.g. [[x1, y1], [x2, y2], [x3, y3]]
        no2_sensor: measurment values of the messstationen, in the same order as the coordinates. 1-dimensional array, e.g. [m1, m2, m3]
        centroid_sat: center position of the kacheln. Array of 2-element arrays, e.g. [[x1, y1], [x2, y2], [x3, y3]]
        no2_sat: measurment values of the kacheln, in the same order as the coordinates. 1-dimensional array, e.g. [m1, m2, m3]
        params: default None, defaults defined within the function; otherwise [k_sensor, k_satellite, relative_tileWeight]
        k_sensor: range of influence of the point measurements
        k_satellite: range of influence of the kacheln measurements
        relative_tileWeight: relative weight of the kacheln. should be between 0 and 1, defaults to 0.2
        
        return: xpos, ypos, vals
        three one-dimensional arrays of x-position, y-position, and interpolated value

    numpy_to_pandas(): converts the numpy arrays (returned from the second pass) into pandas dataframes and then 
    into geoJSONs. Reconstructs the tiles into polygons with their new resolution (e.g. 10 x 10, 15 x 15 or 30 x 30)
    
    plotColormesh/plotDifference: plots the results of the Barnes inteprolation
    
    interpolateHamburg/interpolateLondon: sets the interpolation parameters and calls the interpolation functions
    barnes_firstPass() and barnes_secondPass()
    
    interpolateAirQuality(): controls what should be interpolated
    
**** IMPORTANT NOTE ****

The directory path in changeDirectory(), os.chdir() needs to be changed to the correct directory when running on a different machine. 

'''

import os
import sys
import glob

import numpy as np
import matplotlib.pyplot as plt 

import pandas as pd 
import geopandas
from shapely.geometry import shape, Point, Polygon, MultiPolygon

import locale 

locale.setlocale(locale.LC_NUMERIC, "de_DE")
plt.rcdefaults()
plt.rcParams['axes.formatter.use_locale'] = True

PATH = r'Output/'

def changeDirectory():
    print(r'\nDirectory Change:' + '\nCode is located in: ' + os.getcwd()) #for double checking
    os.chdir(r'/Users/kayla/OneDrive/Geodäsie und Geoninformatik (M.Sc.)/4. Semester/Thesis/')
    print(r'\nCurrent working directory: ' + os.getcwd()) #for double checking

def calcDistance(X, Y, coords): #euklied distance between interpol  grid and sensor pt
    distance = np.sqrt((X-coords[0])**2 + (Y - coords[1])**2)
    return distance

def findIndicesOfClosestPoints(x, y, coords):
    inds = []
    for i in range(len(coords)):
        dist = ((x - coords[i, 0])**2 + (y - coords[i, 1])**2)**0.5
        ind = np.argmin(dist)
        inds.append(ind)
    inds = np.asarray(inds)
    return inds
    
def formatData(points, tiles, city):
    
    satellite_df = tiles.copy()
    
    if city == 'Hamburg':
        satellite_df = satellite_df.to_crs('ETRS89') #local Datum Germany (EPSG:5243)
    
    if city == 'London':
        satellite_df = satellite_df.to_crs('OSGB 1936') #local Datum London (EPSG:27700)
    
    centroid_values = satellite_df[['geometry']].centroid  #better for centroid method, local CRS
    centroid_array = []
    for pts in centroid_values: 
        centroid_array.append([pts.x, pts.y])
    centroidCoords_sat = np.array(centroid_array)
    
    no2values_sat = tiles['no2_conc'].to_numpy()    
    
    sensor_values = points['geometry']
    sensor_array = []
    for pts in sensor_values: 
        sensor_array.append([pts.x, pts.y])
    
    sensorValues_array = np.array(sensor_array)
    
    if city == 'Hamburg':
        no2values_sensor = points['NO2'].to_numpy()
    if city == 'London':
        no2values_sensor = points['value'].to_numpy()
    
    return centroidCoords_sat, no2values_sat, sensorValues_array, no2values_sensor
    

def barnes_firstPass(x, y, sensor_coords, no2_sensor, centroidCoords_sat, no2_satellite, params = None):
    
    X, Y = np.meshgrid(x, y)
    
    sensor_coords = np.asarray(sensor_coords)
    no2_sensor = np.asarray(no2_sensor)
    
    centroidCoords_sat = np.asarray(centroidCoords_sat)
    no2_satellite = np.asarray(no2_satellite)
    
    k_sensor = None
    k_satellite = None
    relative_tileWeight = None
    
    if params == None or len(params) != 3: #default
        k_sensor = 0.03**2
        k_satellite = 0.06**2
        relative_tileWeight = 0.2
    else:
        k_sensor = params[0]
        k_satellite = params[1]
        relative_tileWeight = params[2]
    
    #calc weights for the points (sensors) and the tiles (satellite)
    weights_points = np.asarray([(1.0 - relative_tileWeight) * np.exp(-1 * (calcDistance(X, Y, pointpos))**2/k_sensor) for pointpos in sensor_coords])
    
    weights_tiles = np.asarray([relative_tileWeight * np.exp(-1 * (calcDistance(X, Y, tile_pos))**2/k_satellite) for tile_pos in centroidCoords_sat])
    
    # Multiply weights with the measured values
    weighted_no2_sensorValues = np.zeros(weights_points.shape)
    for i in range(len(no2_sensor)):
        weighted_no2_sensorValues[i, :] = no2_sensor[i] * weights_points[i, :]
    
    weighted_no2_satelliteValues = np.zeros(weights_tiles.shape)
    for i in range(len(no2_satellite)):
        weighted_no2_satelliteValues[i, :] = no2_satellite[i] * weights_tiles[i, :]
        
    weightedSum_no2SensorValues = np.sum(weighted_no2_sensorValues, axis = 0)
    
    weightedSum_no2SatelliteValues = np.sum(weighted_no2_satelliteValues, axis = 0)
    
    #Interpolation function
    interpol = (weightedSum_no2SensorValues + weightedSum_no2SatelliteValues)/ (np.sum(weights_points, axis = 0) + np.sum(weights_tiles, axis = 0))
    
    # Create 1-dim arrays for the coordinates and value pairs --> use C-style iteration to preserve structure
    vals = np.ravel(interpol, order = 'C')
    positions = np.vstack([X.ravel(), Y.ravel()])
    
    xpos = positions[0]
    ypos = positions[1]
    
    return xpos, ypos, vals


def barnes_secondPass(x, y, first_pass, sensor_coords, no2_sensor, centroidCoords_sat, no2_satellite, gamma, params = None):
    
    sensor_coords = np.asarray(sensor_coords)
    no2_sensor = np.asarray(no2_sensor)
    centroidCoords_sat = np.asarray(centroidCoords_sat)
    no2_satellite = np.asarray(no2_satellite)
    
    k_sensor = None
    k_satellite = None
    relative_tileWeight = None
    
    if params == None or len(params) != 3:
        k_sensor = 0.03**2
        k_satellite = 0.06**2
        relative_tileWeight = 0.2
    else: 
        k_sensor = params[0]
        k_satellite = params[1]
        relative_tileWeight = params[2]
    
    weights_points = np.asarray([(1. - relative_tileWeight) * np.exp(-1 * (calcDistance(x, y, sensor_positions))**2/(gamma * k_sensor)) for sensor_positions in sensor_coords])
       
    weights_tiles = np.asarray([relative_tileWeight * np.exp(-1 * (calcDistance(x, y, sat_positions))**2/(gamma * k_satellite)) for sat_positions in centroidCoords_sat]) 
    
    corrected_barnes = np.zeros(first_pass.shape) + first_pass
    
    sensor_interpolatedIndices = findIndicesOfClosestPoints(x, y, sensor_coords)
    
    satellite_interpolatedIndices = findIndicesOfClosestPoints(x, y, centroidCoords_sat)
  
    for i in range(len(no2_sensor)):
        diff = no2_sensor[i] - corrected_barnes[sensor_interpolatedIndices[i]]
        corrected_barnes += diff * weights_points[i, :]
    
    for i in range(len(no2_satellite)):
        diff = no2_satellite[i] - corrected_barnes[satellite_interpolatedIndices[i]]
        corrected_barnes += diff * weights_tiles[i, :]
    
    vals = np.ravel(corrected_barnes, order = 'C')
    positions = np.vstack([x.ravel(), y.ravel()])
    
    xpos = positions[0]
    ypos = positions[1]
    return xpos, ypos, vals

def numpy_to_pandas(xpos, ypos, interpol, res_lon, res_lat, timestamp, city):
    lon = pd.DataFrame(xpos, columns = ['longitude'])
    lat = pd.DataFrame(ypos, columns = ['latitude'])
    interpolated_df = pd.DataFrame(interpol, columns = ['no2_interpolated'])
    
    
    result_df = pd.concat([interpolated_df, lon, lat], axis = 1)
    result_df = geopandas.GeoDataFrame(result_df, geometry=geopandas.points_from_xy(result_df.longitude, result_df.latitude))
    result_df = geopandas.GeoDataFrame(result_df, crs='EPSG:4326')

    
    kacheln = []    
    polygon_df = result_df.copy()

    for index, row in polygon_df.iterrows():
        lon = row.longitude
        lat = row.latitude

        kachel = Polygon([
            (lon - 0.5*res_lon, lat + 0.5*res_lat), 
            ((lon + 0.5*res_lon), lat + 0.5*res_lat), 
            ((lon + 0.5*res_lon), (lat - 0.5*res_lat)), 
            (lon - 0.5*res_lon, (lat - 0.5*res_lat))])
        
        kacheln.append(kachel)
    polygon_df['geometry'] = kacheln
    polygon_df = geopandas.GeoDataFrame(polygon_df, crs='EPSG:4326')
        
    
    if city == 'Hamburg':
        #result_df.to_file('Output/interpolated/interpolatedData_points_HamburgDE_'+ timestamp + '_30x30.geojson', driver = 'GeoJSON')
        polygon_df.to_file(r'Output/interpolated/interpolatedData_as_polygon_HamburgDE_'+ timestamp + '_30x30.geojson', driver = 'GeoJSON')

    if city == 'London':
        #result_df.to_file('Output/interpolated/interpolatedData_points_LondonUK_' + timestamp + '_30x30.geojson', driver = 'GeoJSON')
        polygon_df.to_file(r'Output/interpolated/interpolatedData_as_polygon_LondonUK__' + timestamp + '_30x30.geojson', driver = 'GeoJSON')

    print(r'\nFiles Saved')


def plotColormesh(x, y, interpol, timestamp, title, city):
    plt.figure()
    plt.pcolormesh(x, y, np.reshape(interpol, (len(y), len(x))), cmap = 'YlGnBu', shading = 'auto')
    plt.colorbar()
    plt.title(title)
    plt.ylabel('Breitengrad')
    plt.xlabel('Längengrad')
    plt.clim(0, 35)

        
    if city == 'Hamburg':
        plt.savefig(r'plots/hamburg30x30_interpolated_' + timestamp + '.png', dpi = 600)
    
    if city == 'London':
        plt.savefig(r'plots/London30x30_interpolated_' + timestamp + '.png', dpi = 600)

def plotDifference(x, y, interpol, sp, timestamp, title, city):
    plt.figure()
    plt.pcolormesh(x, y, np.reshape(sp, (30, 30)) - np.reshape(interpol, (30, 30)), shading = 'auto', cmap = 'YlGnBu')
    plt.title(title)
    plt.ylabel('Breitengrad')
    plt.xlabel('Längengrad')
    plt.clim(0, 8)
    plt.colorbar()
    
    if city == 'Hamburg':
        plt.savefig(r'plots/hamburg30x30_diff_' + timestamp +'.png', dpi = 600)
        
    if city == 'London':
        plt.savefig(r'plots/London30x30_diff_' + timestamp + '.png', dpi = 600)
        
    
#interpolate Hamburg data
def interpolateHamburg(sensor_data, satellite_data, timestamp):
    
    satelliteTiles_hh = satellite_data
    sensorStations_hh = sensor_data
    
    satellite_data = geopandas.read_file(satelliteTiles_hh)
    sensor_data = geopandas.read_file(sensorStations_hh)
    

    coords, no2_sat, sensor_coords, no2_sensor = formatData(sensor_data, satellite_data, city = 'Hamburg')
    
    x = np.linspace(9.7, 10.4, 30)
    y = np.linspace(53.35, 53.75, 30)
    res_lon = x[1]-x[0]
    res_lat = y[1]-y[0]
    
    #Define kappa, gamma and w_r
    k_sensor = 0.03**2
    k_satellite = 0.06**2 
    relative_tileWeight = 0.2
    interpol_parameters = [k_sensor, k_satellite, relative_tileWeight]
    
    #fFirst pass Barnes
    xpos, ypos, interpol = barnes_firstPass(x, y, sensor_coords, no2_sensor, coords, no2_sat, interpol_parameters)
    
    #sSecond pass Barnes
    sp = np.zeros(interpol.shape) + interpol 
    for i in range(2):
        
        #(x, y, first_pass, sensor_coords, no2_sensor, centroidCoords_sat, no2_satellite, gamma = 0.3, params = None)
        xpos, ypos, sp = barnes_secondPass(xpos, ypos, sp, sensor_coords, no2_sensor, coords, no2_sat, gamma = 1, params = interpol_parameters)
   
    plotColormesh(x, y, interpol, timestamp, title = 'Barnes-Interpolation, erster Pass\n Hamburg [t = ' + timestamp + ':00]' , city = 'Hamburg') 
    plotColormesh(x, y, sp, timestamp, title = 'Barnes-Interpolation, zweiter Pass\n Hamburg [γ = 1,0, i = 2, t = ' + timestamp + ':00]', city = 'Hamburg') 
    plotDifference(x, y, interpol, sp, timestamp, title = 'Differenz des ersten und zweiten Barnes-Interpolationspasses\n Hamburg [γ = 1,0, i = 2, t = ' + timestamp +':00]', city = 'Hamburg')

    numpy_to_pandas(xpos, ypos, sp, res_lon, res_lat, timestamp, city = 'Hamburg')

#Interpolate London data
def interpolateLondon(sensor_data, satellite_data, timestamp): 
    satelliteTiles_london = satellite_data
    sensorStations_london = sensor_data
    
    satellite_data = geopandas.read_file(satelliteTiles_london)
    sensor_data = geopandas.read_file(sensorStations_london)
    
    coords, no2_sat, sensor_coords, no2_sensor = formatData(sensor_data, satellite_data, city = 'London')
    
    x = np.linspace(-0.65, 0.35, 30) 
    y = np.linspace(51.25, 51.75, 30) 
    res_lon = x[1]-x[0]
    res_lat = y[1]-y[0]
    
    k_sensor = 0.03**2
    k_satellite = 0.06**2 
    relative_tileWeight = 0.2
    interpol_parameters = [k_sensor, k_satellite, relative_tileWeight]
    
    xpos, ypos, interpol = barnes_firstPass(x, y, sensor_coords, no2_sensor, coords, no2_sat, interpol_parameters)
        
    sp = np.zeros(interpol.shape) + interpol 
    for i in range(1):
        
        #(x, y, first_pass, sensor_coords, no2_sensor, centroidCoords_sat, no2_satellite, gamma = 0.3, params = None)
        xpos, ypos, sp = barnes_secondPass(xpos, ypos, sp, sensor_coords, no2_sensor, coords, no2_sat, gamma = 0.2, params = interpol_parameters)
    
    plotColormesh(x, y, interpol, timestamp, title = 'Barnes-Interpolation, erster Pass\n London [t = ' + timestamp + ':00]', city = 'London')    
    plotColormesh(x, y, sp, timestamp, title = 'Barnes-Interpolation, zweiter Pass\n London [γ = 0,2, i = 1, t = ' + timestamp + ':00]', city = 'London') 
    plotDifference(x, y, interpol, sp, timestamp, title = 'Differenz des ersten und zweiten Barnes-Interpolationspasses\n London [γ = 0,2, i = 1, t = ' + timestamp +':00]', city = 'London')

    numpy_to_pandas(xpos, ypos, sp, res_lon, res_lat, timestamp, city = 'London')
    

def interpolateAirQuality(timeindex = '00', city = 'Hamburg'): #E.g.: timeindex = '00', city = 'Hamburg'
    
    if timeindex == 'all':
        for sensor_data in glob.glob(PATH + r'/hamburg/analysis/hamburg_no2conc_sensordata*.geojson'):
            satellite_data = sensor_data.replace('sensordata', 'satellitedata')
            print(sensor_data)
            print(satellite_data)
            print('===')
                
            timestamp = str(sensor_data[-10:-8])
            print(timestamp)

            interpolateHamburg(sensor_data, satellite_data, timestamp)
            
        for sensor_data in glob.glob(PATH + r'/london/analysis/london_no2conc_sensordata*.geojson'):
            satellite_data = sensor_data.replace('sensordata', 'satellitedata')
            print(sensor_data)
            print(satellite_data)
            print('===')
                
            timestamp = str(sensor_data[-10:-8])
            print(timestamp)
                
            interpolateLondon(sensor_data, satellite_data, timestamp)
    else:
        if city == 'Hamburg':
            sensor_data = PATH + r'hamburg/analysis/hamburg_no2conc_sensordata_07082021_' + timeindex + '.geojson'
            satellite_data = PATH + r'hamburg/analysis/hamburg_no2conc_satellitedata_07082021_'+ timeindex + '.geojson'
            interpolateHamburg(sensor_data, satellite_data, timeindex)
        elif city == 'London':
            sensor_data = PATH + r'london/analysis/london_no2conc_sensordata_13092020_' + timeindex + '.geojson'
            satellite_data = PATH + r'london/analysis/london_no2conc_satellitedata_13092020_' + timeindex + '.geojson'
            interpolateLondon(sensor_data, satellite_data, timeindex)
        else:
            print(r'Error: unknown city')
            


def main(): 

    try:
        changeDirectory()
        
        interpolateAirQuality(timeindex ='all', city = 'Hamburg')

        sys.exit(0)
   
    except Exception as ex:
        print('Error: ' + str(ex))
        sys.exit(1)
        
if __name__ == '__main__':
    main()

