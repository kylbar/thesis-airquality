-*- coding: utf-8 -*-

# Masterarbeit: Untersuchung und Visualisierung von disaggregrieten Luftqualitätsdaten

## Technische Details
### Programmierung

netCDF -> geoJSON: mit Python (3 step process) 

## Datenquellen
### Sensordaten
#### Europa
1. luft.hamburg

2. London Air (?) <https://www.londonair.org.uk/london/asp/dataspecies.asp?site1=&site2=&site3=&site4=&site5=&site6=&day1=1&month1=jan&year1=2020&day2=1&month2=jan&year2=2021&period=15min&species=PM25&ratidate=&res=6&Submit=Plot+graph> 

#### USA
1. EPA Sensordaten <https://www.epa.gov/outdoor-air-quality-data/download-daily-data>
   - EPA: ganz USA 

#### Etc.
1. OpenAir <https://openaq.org/#/countries> 

2. Google? / DPD ? 

### Satellitendaten
#### Europa
1. CAMS <https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-europe-air-quality-forecasts?tab=form>
   - Satellitendaten (high res für EU)

2. NASA <https://urs.earthdata.nasa.gov/>
   - Login 

### Karten
1. Stadtteile/ Bezirke Hamburg: ESRI <https://opendata-esri-de.opendata.arcgis.com/datasets/esri-de-content::stadtteile-hamburg/about>



# Wichtig
## TO DO
- [ ] API Konfigurieren (automatisieren?) :hear_no_evil:
- [ ] Satellitendaten von Kalifornien 
- [ ] Sensordaten: USA, England(?), Dubai, DE, Holland(?) -> Highres für EU (Copernicus)
- [ ] Disaggregation mit Cogran (Wie/Wo/Was)
- [ ] Orte finalisieren
- [ ] Visualisierung (Statisch/ Dynamisch - noch nicht festgelegt)

## Fertig
- [x] Cogran mit Python ausführen 
- [x] netCDF -> csv -> geoJSON
- [x] Luftqualitätsdaten von Google? (ACCEPTED) :dizzy:
- [x] ESRI Stadtteile/Bezirke (England, Cali., HH) 
