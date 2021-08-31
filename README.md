# Masterarbeit: Untersuchung und Visualisierung von disaggregrieten Luftqualit√§tsdaten

## Technische Details
### Programmierung

netCDF -> geoJSON: mit Python (3 step process) 

## Datenquellen
### Europa
1. CAMS <https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-europe-air-quality-forecasts?tab=form>
   - Satellitendaten (high res f√ºr EU)

2. EPA Sensordaten <https://www.epa.gov/outdoor-air-quality-data/download-daily-data>
   - EPA: ganz USA 


### Karten
1. Stadtteile/ Bezirke Hamburg: ESRI <https://opendata-esri-de.opendata.arcgis.com/datasets/esri-de-content::stadtteile-hamburg/about>



# Wichtig
## TO DO
- [ ] Satellitendaten von Kalifornien 
- [ ] Luftqualit‰tsdaten von Google? -> Wenn nicht mˆglich, welche?
- [ ] Sensordaten: USA, England(?), Dubai, DE, Holland(?) -> Highres f¸r EU (Copernicus)
- [ ] Disaggregation mit Cogran (Wie/Wo/Was)
- [ ] Orte finalisieren
- [ ] Visualisierung (Statisch/ Dynamisch - noch nicht festgelegt)

## Fertig
- [x] Cogran mit Python ausf¸hren 
- [x] netCDF -> csv -> geoJSON
