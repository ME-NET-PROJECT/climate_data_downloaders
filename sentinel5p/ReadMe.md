# Sentinel-5P Data Downloader

This repository provides a Python script to download Sentinel-5P atmospheric composition data using the Sentinel Hub API. The script enables users to extract data for specified geographical regions and time intervals, storing it in NumPy format.

## Features
- Downloads Sentinel-5P atmospheric data (e.g., Ozone, Methane, Carbon Monoxide, etc.).
- Supports flexible bounding box (BBox) selection for various regions.
- Retrieves data for specified time periods and intervals.
- Saves downloaded data as NumPy files for easy analysis.

## Requirements
Ensure you have the following dependencies installed:

```bash
pip install numpy sentinelhub
```

## Usage

### 1. Set Up Your Sentinel Hub Credentials
You need to obtain Sentinel Hub API credentials:
- Go to [Sentinel Hub](https://www.sentinel-hub.com/)
- Register and obtain a `client_id` and `client_secret`

### 2. Define Bounding Box & Parameters
Modify the `bbox_name` and `bbox_coords` variables in `main`:
```python
bbox_name = "Ghana"
bbox_coords = (-3.24437008301, 4.71046214438, 1.0601216976, 11.0983409693)  # Ghana
```

Other pre-configured bounding boxes include:
- UK
- Europe
- Germany
- West Africa

### 3. Set the Time Range and Bands
Modify the following parameters:
```python
start_date = datetime.datetime(2024, 9, 1)  # Start date
period_days = 49  # Number of days to fetch data for
time_interval_days = 1  # Time interval between requests
bands = ["CH4"]  # Select gas/particle bands
```
Available bands:
- `CO` (Carbon monoxide)
- `HCHO` (Formaldehyde)
- `NO2` (Nitrogen oxide)
- `O3` (Ozone)
- `SO2` (Sulphur dioxide)
- `CH4` (Methane)
- `AER_AI_340_380` (UV Aerosol Index)
- `AER_AI_354_388` (UV Aerosol Index)

### 4. Run the Script
Execute the script with:
```bash
python sentinel5p_downloader.py
```

### 5. Downloaded Data
The script saves the downloaded Sentinel-5P data in the following structure:
```
./data/
  ├── Ghana/
      ├── CH4/
          ├── 20240901_20240902.npy
          ├── 20240902_20240903.npy
          ├── ...
```
Each `.npy` file contains the requested atmospheric data for the given time slot.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Acknowledgments
- [Sentinel Hub API](https://www.sentinel-hub.com/)
- [Copernicus Programme](https://www.copernicus.eu/en)

