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
    - Tagesdurchschnitt? 
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
    
def sensorDatenHH(): 
    input_path = r'Daten/luft.hamburg/Stündlich/07_08_2021'
    sensor_koordinaten = r'Daten/luft.hamburg/koordinaten_hhSensoren.csv'
    
    sensor_dateien = glob.glob(input_path + r"/*.csv")
    
    input_dfs = (pd.read_csv(datei, delimiter=(';'), header=0) for datei in sensor_dateien) #read in and combine all csvs
    temp = pd.concat(input_dfs, ignore_index = True)
    
    temp = temp.drop(["SO2", "SO2 (4m)", "NO (4m)", "NO2 (4m)", "Ozon", "CO"], axis=1) #delete columns I don't need
    temp = temp.fillna(0)
    
    koord_df = pd.read_csv(sensor_koordinaten, delimiter=(';'), header = 0)
    
    output_df = pd.merge(temp, koord_df, left_on='Station', right_on='Station', right_index=False, how = 'left')
    
    # REFORMAT output_df MESSZEIT!! WRONG FORMAT. MONTH AND DAY ARE SWITCHED. 
    #AUGUS 8th is CORRECT. format='%Y-%m-%d %H:%M:%S'
    output_df['Messzeit'] = pd.to_datetime(output_df['Messzeit'])
    
    output_df = geopandas.GeoDataFrame(output_df, geometry=geopandas.points_from_xy(output_df.longitude, output_df.latitude))
    output_df = geopandas.GeoDataFrame(output_df, crs='EPSG:4326') #set CRS to WGS84
    
    #Plottet die Sensordaten mit Bezug auf ihre (räumlichen) Positionen (nur als vis. Test)
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    ax = world[world.name == 'Germany'].plot(color = 'white', edgecolor = 'black')
    ax.set(xlim=(9,11), ylim=(53.2,54))
    output_df.plot(ax=ax, color='orange')
    plt.show()
    
    #output DF für ALLE Messzeiten
    output_df.to_csv('Output/misc/hh_Messstationwerte.csv')
    
    #output DF für specifische Messzeiten
    output_df0 = output_df.loc[output_df['Messzeit'] == "2021-07-08 00:00:00"]
    output_df0.to_file('Output/geoJSON/no2_conc_HamburgDE_Messstationen_07082021.geojson', driver = 'GeoJSON')
    
    #Control
    print("\nInput files located in " + "[ " + input_path + " ]" + " converted to geoJSON")

def main(): 
    
    try: 
        change_dir()
        sensorDatenHH()
        
        sys.exit(0)
        
    except Exception as ex:
        print("Error: " + ex)
        sys.exit(1)

if __name__ == "__main__":
    main()
