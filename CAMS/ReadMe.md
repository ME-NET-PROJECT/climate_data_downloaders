# ADSCAMSDownloader

## Overview

`ADSCAMSDownloader` is a Python utility for downloading atmospheric composition forecast data from the CAMS (Copernicus Atmosphere Monitoring Service) dataset. This tool uses the `cdsapi` package to authenticate and retrieve NetCDF files for a specified geographic bounding box over a given time period.

## Features

- Authenticates using user-provided credentials
- Downloads atmospheric composition forecast data for a specified region
- Supports multiple pollutant and meteorological variables
- Saves the downloaded data as NetCDF files in a structured directory

## Prerequisites

Before using this tool, ensure you have the following installed:

- Python 3.x
- Required Python packages:
  ```sh
  pip install cdsapi pyyaml
  ```

## Setup

### 1. Obtain CAMS API Credentials

To access the CAMS dataset, you need to create an account on the Copernicus Atmosphere Data Store and generate an API key. Save the credentials in a YAML file (e.g., `security/.adsapircV2`) in the following format:

```yaml
url: https://cds.climate.copernicus.eu/api/v2
key: your-unique-api-key
```

### 2. Configure Your Download

Modify the script parameters as needed:

- **Bounding Box (****`bbox`****)**: Define the latitude and longitude range of the area of interest.
- **Dataset (****`cams_dataset`****)**: Specify the dataset to be downloaded.
- **Variables (****`bands`****)**: Select the atmospheric variables to retrieve.
- **Date Range (****`start_date`****, ****`period_days`****)**: Define the start date and duration.
- **Download Interval (****`time_interval_days`****)**: Set the time interval between downloads.

## Usage

Run the script using:

```sh
python your_script.py
```

### Example Configuration

```python
credentials_file = 'security/.adsapircV2'
bbox = (-3.24437008301, 4.71046214438, 1.0601216976, 11.0983409693)  # Ghana
bbox_name = "Ghana"
cams_dataset = "cams-global-atmospheric-composition-forecasts"
bands = [
    'carbon_monoxide', 'formaldehyde', 'methane',
    'nitrogen_dioxide', 'nitrogen_monoxide', 'ozone',
    'sulphur_dioxide', 'temperature', 'u_component_of_wind',
    'v_component_of_wind',
]
start_date = "2019-01-01"
period_days = 365
time_interval_days = 1
```

## Output

Downloaded NetCDF files will be saved in:

```
data/<bbox_name>/<start_date>_<end_date>.nc
```

## License

This project is licensed under the MIT License.

## Contributing

Feel free to submit issues and pull requests to improve the scrip
