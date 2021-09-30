#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 11:31:05 2021

@author: kayla
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os
import sklearn.neighbors

PATH = r'Output/misc/'


def formatting(df): 
    
    df_t0 = df.loc[df['Messzeit'] == "2021-07-08 00:00:00"]
    df_t1 = df.loc[df['Messzeit'] == "2021-07-08 05:00:00"]
    df_t2 = df.loc[df['Messzeit'] == "2021-07-08 10:00:00"]
    df_t3 = df.loc[df['Messzeit'] == "2021-07-08 15:00:00"]
    df_t4 = df.loc[df['Messzeit'] == "2021-07-08 20:00:00"]
    
    
    #Sensorstandorte
    standortA = df_t4.copy()
    standortA = standortA.rename(columns ={'Station' : 'Station A'})
    
    standortB = df_t4.copy()
    standortB = standortB.rename(columns ={'Station' : 'Station B'})

    #convert to radians
    standortA[['latitude_radA', 'longitude_radA']] = (np.radians(standortA.loc[:,['latitude', 'longitude']]))
    standortB[['latitude_radB', 'longitude_radB']] = (np.radians(standortB.loc[:,['latitude', 'longitude']]))
    
    #calc distances
    distances = sklearn.neighbors.DistanceMetric.get_metric('haversine') 
    
    distance_matrix = (distances.pairwise(standortA[['latitude_radA','longitude_radA']], standortB[['latitude_radB','longitude_radB']])*3959)
    
    df_distances = (pd.DataFrame(distance_matrix, index = standortA['Station A'], columns = standortB['Station B']))

    df_distances_long = (pd.melt(df_distances.reset_index(), id_vars='Station A'))
    df_distances_long = df_distances_long.rename(columns={'value':'km'})
    
    #check
    print(df_distances_long)
    

    #add no & no2
    
    df_with_concentration = pd.merge(df_distances_long, df_t4, left_on='Station B', right_on= 'Station', right_index=False)
    
    df_with_concentration = df_with_concentration.rename(columns={'NO':'NO B', 'NO2': 'NO2 B'})

    print(df_with_concentration.columns)
    
    #print(standortB.columns)
    standortA_reduced = standortA.copy()
    standortA_reduced = standortA_reduced.drop(['Messzeit', 'longitude', 'latitude', 'geometry', 'latitude_radA', 'longitude_radA'], axis = 1)
    print(standortA_reduced.columns)
    
    #merged_df = pd.merge(standortB_reduced, df_with_concentration, left_on ='Station B', right_on = 'Station A', right_index = False)
    result = pd.merge(df_with_concentration, standortA_reduced, on = "Station A", how = "outer")
    print(result[["Station A", "Station B", "NO2 B", "NO B", "NO", "NO2"]])
    print(result.columns)
    
    result = result.rename(columns={'NO': 'NO A', 'NO2': 'NO2 A'})
    print(result[["Station A", "Station B", "NO2 B", "NO B", "NO A", "NO2 A"]])
    
    cols = ["Station A", "Station B", "NO A", "NO B", "NO2 A", "NO2 B", "km"]
    
    result[cols].to_excel('Output/misc/hh_Messstationwerte_distances_20.xlsx')
    result[cols].to_csv('Output/misc/hh_Messstationwerte_distances_20.csv')

def correlationPlot(df):
    
    #print(df.columns)
    #df = df[df.km != 0]
   
    
    #df['NO differenz'] = abs(df['NO A'] - df['NO B'])
    df['NO2 differenz'] = 0.5 * ((df['NO2 A'] - df['NO2 B']) / (df['NO2 A'] + df['NO2 B']))
    #print(df.columns)
    print(df[['NO2 differenz']])
    df.drop(df.loc[df['NO2 differenz']==0].index, inplace=True)
    
    plt.scatter(df["km"], df["NO2 differenz"])
    plt.xlabel('Distanz zwischen den Sensoren')
    plt.ylabel('gemessene NO2-Konzentration')
    plt.title('Korrelationsdiagramm')
    plt.legend()
    #plot2 = plt.scatter(df["km"], df["NO2 differenz"])
    
    #plot1.show()
    #plot2.show()
def main(): 
    
    print("\n------------------" + "\nDirectory Check:" + "\n------------------" + "\nCode is located in: " + os.getcwd()) #for double checking
    os.chdir('/Users/kayla/OneDrive/Geodäsie und Geoninformatik (M.Sc.)/4. Semester/Thesis/')
    print("\nCurrent working directory: " + os.getcwd()) #for double checking
    
    #input_df = pd.read_csv(PATH + "hh_Messstationwerte.csv", delimiter=(','), header=0, index_col = 0)
    #formatting(input_df)
    
    plot_df0 = pd.read_csv(PATH + "hh_Messstationwerte_distances_00.csv", delimiter=(','), header=0, index_col = 0)
    plot_df1 = pd.read_csv(PATH + "hh_Messstationwerte_distances_05.csv", delimiter=(','), header=0, index_col = 0)
    plot_df2 = pd.read_csv(PATH + "hh_Messstationwerte_distances_10.csv", delimiter=(','), header=0, index_col = 0)
    plot_df3 = pd.read_csv(PATH + "hh_Messstationwerte_distances_15.csv", delimiter=(','), header=0, index_col = 0)
    plot_df4 = pd.read_csv(PATH + "hh_Messstationwerte_distances_20.csv", delimiter=(','), header=0, index_col = 0)
    
    
    correlationPlot(plot_df0)
    correlationPlot(plot_df1)
    correlationPlot(plot_df2)
    correlationPlot(plot_df3)
    correlationPlot(plot_df4)

if __name__ == "__main__":
    main()