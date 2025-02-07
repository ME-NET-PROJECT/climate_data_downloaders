# Climate Data Downloaders

## Overview
This repository contains scripts for downloading atmospheric composition forecast data from multiple sources:
- **CAMS (Copernicus Atmosphere Monitoring Service)** dataset
- **Sentinel-5P** atmospheric composition data
- **AURN (Automatic Urban and Rural Network)** air quality data

## Features
- **CAMS Data:** Downloads global atmospheric composition forecasts in NetCDF format.
- **Sentinel-5P Data:** Retrieves Sentinel-5P atmospheric data using the Sentinel Hub API.
- **AURN Data:** Extracts air quality data from manually downloaded HTML pages and saves them as CSV files.

## Prerequisites
Ensure you have Python installed along with the required dependencies:

```sh
pip install cdsapi pyyaml numpy sentinelhub
```

---

## **CAMS Dataset Downloader**

### **Dataset Information**
- **Source:** [CAMS Dataset](https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts?tab=overview)
- **Model Level:** 137
- **Time:** 00:00 UTC
- **Leadtime Hour:** 0
- **Geographical Areas:**
  - **UK:** [-7.57216793459, 49.959999905, 1.68153079591, 58.6350001085]
  - **Ghana:** [-3.24437008301, 4.71046214438, 1.0601216976, 11.0983409693]
- **Data Format:** Zipped NetCDF (experimental)
- **Variables:**
  - **Multi-variable:** ['carbon_monoxide', 'formaldehyde', 'methane', 'nitrogen_dioxide', 'nitrogen_monoxide', 'ozone', 'sulphur_dioxide', 'temperature', 'u_component_of_wind', 'v_component_of_wind']
  - **Single-variable:** ['surface_pressure', 'uv_biologically_effective_dose', 'uv_biologically_effective_dose_clear_sky']

### **Authentication & Setup**
To access CAMS data, create an account on Copernicus and generate an API key. Save credentials in a YAML file:
```yaml
url: https://cds.climate.copernicus.eu/api/v2
key: your-unique-api-key
```

### **Running the Script**
```sh
python cams_downloader.py
```

---

## **Sentinel-5P Dataset Downloader**

### **Dataset Information**
- **Source:** [Sentinel-5P Dashboard](https://shapps.dataspace.copernicus.eu/dashboard/#/account/settings)
- **Authentication:** Requires `client_id` and `client_secret` from Sentinel Hub.
- **Geographical Areas:** Supports flexible bounding boxes.
- **Available Bands:** CO, HCHO, NO2, O3, SO2, CH4, AER_AI_340_380, AER_AI_354_388

### **Authentication & Setup**
Set up API credentials in a config file:
```sh
config.sh_client_id = "your_client_id"
config.sh_client_secret = "your_client_secret"
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
config.sh_base_url = "https://sh.dataspace.copernicus.eu"
```

### **Running the Script**
```sh
python sentinel5p_downloader.py
```

### **Downloaded Data Structure**
```
./data/
  ├── Ghana/
      ├── CH4/
          ├── 20240901_20240902.npy
          ├── 20240902_20240903.npy
```

---

## **AURN Dataset Downloader**

### **Dataset Information**
- **Source:** [UK AURN Data](https://uk-air.defra.gov.uk/data/data_selector_service)
- **Data Processing:**
  1. Data is manually downloaded as HTML files.
  2. Tables are extracted from HTML files and saved as CSV.

### **Running the Script**
```sh
python aurn_data_extractor.py
```

### **Output**
Extracted data is saved in CSV format for further analysis.

---

## **License**
This project is licensed under the MIT License.

## **Acknowledgments**
- [CAMS - Copernicus Atmosphere Monitoring Service](https://ads.atmosphere.copernicus.eu/)
- [Sentinel-5P - Copernicus Programme](https://www.copernicus.eu/en)
- [UK-AIR - Department for Environment, Food & Rural Affairs (DEFRA)](https://uk-air.defra.gov.uk/)

