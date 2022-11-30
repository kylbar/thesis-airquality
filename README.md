********************

Author: Kayla Barginda

README to use in combination with the code for the Master's Thesis "Untersuchung und Visualisierung von disaggregierten Luftqualitätsdaten" (Investigation and Visualisation of Disaggregated Air Quality Data)

Note: all data that is created by the scripts format_sensors.py and format_satellite.py are already available within the project folder. The main script, barnes_interpolation.py, can be executed without executing the data formatting files first. However, in the event that the data is not already available in it's formatted form or different datasets are used, the sensor and satellite data needs to be formatted prior to the interpolation. The order of execution of these two scripts is arbitrary. 

Double check DIR_PATH and PATH --> change to your own PATH(s)

********************
**Needed Python Packages:** numpy, matplotlib, pandas, geopandas, shapely, xarray

[Internal packages used: os, sys, subprocess and glob]

********************

The files need to be executed in the following order:

1. _format_sensors.py_ 
    - This code formats the sensor data so that it is compatible with the satellite data and can be further processed/ used for further analysis.
2. _format_satellite.py_ 
    - This code formats the CAMS satellite data so that it can be interpretated by GIS 
    softwares and read by the barnes_interpolation.py script. 
    - Output files are saved as geoJSONs with the CRS: WGS84. 
    - Conversion only for one data set, change: output_df0  = output_df0.loc[output_df0['time'] == '2020-09-13 00:00:00'] to the desired time to save different times. 

3. _barnes_interpolation.py_ 
    - Calculates the first and second pass of the Barnes Interpolationscheme

4. _run_cogran.py_ 
    - Runs the CoGran command line tool within a python script for convenience 

See individual code files for explicit explanations 

********************

The simulation scripts for the Barnes interpolation in 1D and 2D data are found in the following folder: "Simulations". All data for the simulation scripts is also found in this folder. 

- Districts: contains city districts for Hamburg and London
- Disaggregated: contains the disaggregated files from CoGran
- Interpolated: contains the interpolated files from the simulated scripts
- Plots: contains the plots for Hamburg and London simulated data

********************
**Selected Visualisations from Thesis**

**Standard deviation of the Barnes Interpolation scheme on simulated data**

Compares the standard deviation of the Barnes Interpolation based on simulated data for different values of γ at different grid resolutions for Hamburg and London. The results of the simulated data were used set number of iterations and best value for γ for Hamburg and London respectively. 
<img width="670" alt="Screenshot 2022-11-30 at 22 58 04" src="https://user-images.githubusercontent.com/22305662/204921046-9d76ed69-5ffa-4abc-a87a-bb908169240e.png">

**Visual comparison of the first and second Barnes Interpolation passes**

<img width="516" alt="Screenshot 2022-11-30 at 22 58 53" src="https://user-images.githubusercontent.com/22305662/204919461-4b0b5ab6-4104-48ef-8db3-04e81a94f75e.png">

**Visualisation of the interpolation and disaggregation of air quality data for London**

<img width="487" alt="Screenshot 2022-11-30 at 22 59 45" src="https://user-images.githubusercontent.com/22305662/204919055-1c5d0026-640f-4a69-8f97-101b5ede3089.png">
