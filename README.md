# Masterarbeit: Untersuchung und Visualisierung von disaggregrieten Luftqualitätsdaten

## Technische Details
### Programmierung

netCDF -> geoJSON: mit Python (3 step process) 

## Datenquellen
### Sensordaten
1. luft.hamburg

2. ??
### Satellitendaten
#### Europa
1. CAMS <https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-europe-air-quality-forecasts?tab=form>
   - Satellitendaten (high res für EU)

2. EPA Sensordaten <https://www.epa.gov/outdoor-air-quality-data/download-daily-data>
   - EPA: ganz USA 

3. Google? / DPD ? 
### Karten
1. Stadtteile/ Bezirke Hamburg: ESRI <https://opendata-esri-de.opendata.arcgis.com/datasets/esri-de-content::stadtteile-hamburg/about>



# Wichtig
## TO DO
- [ ] API Konfigurieren (automatisieren?)
- [ ] Satellitendaten von Kalifornien 
- [ ] Luftqualitätsdaten von Google? -> Wenn nicht möglich, welche?
- [ ] Sensordaten: USA, England(?), Dubai, DE, Holland(?) -> Highres für EU (Copernicus)
- [ ] Disaggregation mit Cogran (Wie/Wo/Was)
- [ ] Orte finalisieren
- [ ] Visualisierung (Statisch/ Dynamisch - noch nicht festgelegt)

## Fertig
- [x] Cogran mit Python ausführen 
- [x] netCDF -> csv -> geoJSON
