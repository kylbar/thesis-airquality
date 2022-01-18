********************

Author: Kayla Barginda | 6066945

README to use in combination with the code for the Master's Thesis "Untersuchung und Visualisierung von disaggregierten Luftqualitätsdaten" (Investigation and Visualisation of Disaggregated Air Quality Data)

Note: all data that is created by the scripts format_sensors.py and format_satellite.py are already available within the project folder. The main script, barnes_interpolation.py, can be executed without executing the data formatting files first. However, in the event that the data is not already available in it's formatted form or different datasets are used, the sensor and satellite data needs to be formatted prior to the interpolation. The order of execution of these two scripts is arbitrary. 

********************
NEEDED PYTHON PACKAGES: 

numpy 
matplotlib
pandas
geopandas
shapely 
xarray

[Internal packages used: os, sys, subprocess and glob]

********************

The files need to be executed in the following order:

1. format_sensors.py
--> This code formats the sensor data so that it is compatible with the satellite data and can be further processed/ used for further analysis.

2. format_satellite.py
--> This code formats the CAMS satellite data so that it can be interpretated by GIS 
    softwares and read by the barnes_interpolation.py script. 

--> Output files are saved as geoJSONs with the CRS: WGS84. 

--> Conversion only for one data set, change: output_df0  = output_df0.loc[output_df0['time'] == '2020-09-13 00:00:00'] to the desired time to save different times. 

3. barnes_interpolation.py
--> Calculates the first and second pass of the Barnes Interpolationscheme

4. run_cogran.py
--> Runs the CoGran command line tool within a python script for convenience 

********************

See individual code files for explicit explanations 

********************

The simulation scripts for the Barnes interpolation in 1D and 2D data are found in the following folder: "Simulations". All data for the simulation scripts is also found in this folder. 

Districts: contains city districts for Hamburg and London
Disaggregated: contains the disaggregated files from CoGran
Interpolated: contains the interpolated files from the simulated scripts
Plots: contains the plots for Hamburg and London simulated data
