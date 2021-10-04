#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Was mache ich? 
    - Alle Sensoren werden in einer Datei gespeichert 
            -> siehe verschiedene Funktionen (Länderabhängig)
    - Koordinaten der Sensoren werden ebenfalls zusammengefügt
    - Unnötige Daten (e.g. SO, etc.) werden gelöscht
    - Messzeiten werden richtig formatiert 
    - CRS wird zu WGS84 gesetzt
    - Output wird als CSV gespeichert
    - Output zu einem spezifischen Zeitpunkt (e.g. 00:00:00) wird als geoJSON gespeichert

TO ADD: 
    - Tagesdurchschnitt? (does this really matter in the end???)
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

def controlSavepath(path):
    print("\nInput files located in " + "[ " + path + " ]" + " converted to geoJSON")

#hamburg
def sensorDatenHamburg(): 
    
    '''
    Read in data. Multiple files!
    '''
    input_path = r'Daten/luft.hamburg/Stündlich/07_08_2021'
    sensor_koordinaten = r'Daten/luft.hamburg/koordinaten_hhSensoren.csv'
    sensor_dateien = glob.glob(input_path + r"/*.csv")
    input_dfs = (pd.read_csv(datei, delimiter=(';'), header=0) for datei in sensor_dateien) #read in and combine all csvs
   
    '''
    Data Formatting
    '''
    temp = pd.concat(input_dfs, ignore_index = True)
    temp = temp.drop(["SO2", "SO2 (4m)", "NO (4m)", "NO2 (4m)", "Ozon", "CO"], axis=1) #delete columns I don't need
    temp = temp.fillna(0)
    
    koord_df = pd.read_csv(sensor_koordinaten, delimiter=(';'), header = 0)
    output_df = pd.merge(temp, koord_df, left_on='Station', right_on='Station', right_index=False, how = 'left')
    
    # REFORMAT output_df MESSZEIT!! WRONG FORMAT. MONTH AND DAY ARE SWITCHED. 
    #AUGUS 8th is CORRECT. format='%Y-%m-%d %H:%M:%S'
    output_df['Messzeit'] = pd.to_datetime(output_df['Messzeit'])
    
    '''
    Convert to Geopandas and set CRS
    '''
    output_df = geopandas.GeoDataFrame(output_df, geometry=geopandas.points_from_xy(output_df.longitude, output_df.latitude))
    output_df = geopandas.GeoDataFrame(output_df, crs='EPSG:4326') #set CRS to WGS84

    '''
    Sanity plot
    '''    
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    ax = world[world.name == 'Germany'].plot(color = 'white', edgecolor = 'black')
    ax.set(xlim=(9,11), ylim=(53.2,54))
    output_df.plot(ax=ax, color='orange')
    plt.show()
    
    '''
    Export and Save
    '''
    output_df.to_csv('Output/misc/hh_Messstationwerte.csv')
    output_df0 = output_df.loc[output_df['Messzeit'] == "2021-07-08 00:00:00"]
    output_df0.to_file('Output/geoJSON/no2_conc_HamburgDE_Messstationen_07082021.geojson', driver = 'GeoJSON')
    
    controlSavepath(input_path)

#london
def sensorDatenLondon(): 
    input_path = r'Daten/openAQ/London_13092020.csv'
    input_df = pd.read_csv(input_path, delimiter=(';'), header=0)
    input_df = input_df.drop(["locationId", "city", "country", "local"], axis=1)
    
    temp = input_df.copy()
    temp['utc'] = pd.to_datetime(temp['utc'])
    #temp = temp.loc[temp["utc"] == "2020-09-13T00:00:00+00:00"]
    temp = temp.fillna(0)

    temp.loc[temp['unit'] == 'ppm', 'value'] = (temp["value"] * 0.0409 * 46.01)
    temp['unit'].replace({'ppm': 'µg/m³'}, inplace = True)
  
    output_df = temp
    output_df = geopandas.GeoDataFrame(output_df, geometry=geopandas.points_from_xy(output_df.longitude, output_df.latitude))
    output_df = geopandas.GeoDataFrame(output_df, crs='EPSG:4326')

    #print(output_df.loc[output_df["unit"] == 'ppm'])
    output_df = output_df.copy()
   
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    ax = world[world.name == 'United Kingdom'].plot(color = 'white', edgecolor = 'black')
    ax.set(xlim=(0.23, -0.4), ylim=(51.35,51.7))
    output_df.plot(ax=ax, color='orange')
    plt.show()
    
    output_df.to_csv('Output/misc/London_Messstationwerte.csv')
    output_df0 = output_df.copy()
    
    output_df0 = output_df.loc[output_df['utc'] == '2020-09-13 00:00:00+00:00']
    output_NO2 = output_df.loc[output_df['parameter'] == 'no2']
    
    #print(output_NO2)
    #print(output_NO2[["location", "parameter", "value"]])
    output_df0.to_file('Output/geoJSON/London_Messstationen_13092020.geojson', driver = 'GeoJSON')
    controlSavepath(input_path)
    
#paris
def sensorDatenParis(): 
    input_path = r'Daten/openAQ/Paris' #no2 units = mg/m^3
    
    sensor_dateien = glob.glob(input_path+ r'/*.csv')
    input_dfs = (pd.read_csv(datei, delimiter =',', header =0) for datei in sensor_dateien)
    temp = pd.concat(input_dfs, ignore_index = True)
    temp = temp.drop(["city", "locationId", "local", "country"], axis = 1)
    
    
    #print(temp.loc[temp['parameter'] == 'no2'])
    
    temp = temp.fillna(0)
    temp['utc'] = pd.to_datetime(temp['utc'])
    #print(temp.dtypes)
    output_df = temp
    output_df = geopandas.GeoDataFrame(output_df, geometry=geopandas.points_from_xy(output_df.longitude, output_df.latitude))
    output_df = geopandas.GeoDataFrame(output_df, crs='EPSG:4326') #set CRS to WGS84

    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    ax = world[world.name == 'France'].plot(color = 'white', edgecolor = 'black')
    ax.set(xlim=(2.25,2.425), ylim=(48.82,48.9))
    output_df.plot(ax=ax, color='orange')
    plt.show()
    
    #output DF für ALLE Messzeiten
    output_df.to_csv('Output/misc/Paris_Messstationwerte.csv')
    
    #output DF für specifische Messzeiten
    output_df0 = output_df.loc[output_df['utc'] == "2019-05-16 00:00:00"]
    output_NO2 = output_df0.loc[output_df0['parameter'] == 'no2'] #only NO2
    
    output_NO2.to_file('Output/geoJSON/ParisNO2_Messstationen_16052019.geojson', driver = 'GeoJSON')
    
    controlSavepath(input_path)
        
    
def main(): 
    
    try: 
        change_dir()
        sensorDatenHamburg()
        sensorDatenLondon()
        sensorDatenParis()
        sys.exit(0)
        
    except Exception as ex:
        print("Error: " + str(ex))
        sys.exit(1)

if __name__ == "__main__":
    main()
