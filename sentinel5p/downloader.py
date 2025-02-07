import datetime
import numpy as np
from pathlib import Path

from sentinelhub import (
    SHConfig,
    CRS,
    BBox,
    DataCollection,
    MimeType,
    SentinelHubRequest,
    bbox_to_dimensions
)


class Sentinel5PDownloader:
    def __init__(self, client_id, client_secret, bbox_name, bbox_coords, resolution=1000, data_folder="./data"):
        self.config = SHConfig()
        self.config.sh_client_id = client_id
        self.config.sh_client_secret = client_secret
        self.config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        self.config.sh_base_url = "https://sh.dataspace.copernicus.eu"
        self.data_folder = data_folder

        self.bbox_name = bbox_name
        self.bbox = BBox(bbox=bbox_coords, crs=CRS.WGS84).transform(CRS(3857))
        self.resolution = resolution
        self.size = bbox_to_dimensions(self.bbox, resolution=self.resolution)
        print(f"Image shape at {self.resolution} m resolution: {self.size} pixels")

    def generate_time_slots(self, start_date, period_days, time_interval_days):
        dates = [(start_date + datetime.timedelta(days=i * time_interval_days)).date().isoformat() for i in
                 range(period_days + 1)]
        time_slots = [(dates[i], dates[i + 1]) for i in range(len(dates) - 1)]
        print("Time windows:\n")
        for slot in time_slots:
            print(slot)
        return time_slots

    def generate_evalscripts(self, band):
        evalscript = """
        //VERSION=3
        function setup() {{
           return {{
            input: ["{band}"], // This specifies the bands that are looked at
            output: {{
              bands: 1,
              sampleType: "FLOAT32"
            }},
            mosaicking: "SIMPLE"
          }};
        }}

        function evaluatePixel(sample) {{
            return [sample.{band}];
        }}
        """
        return [evalscript.format(band=band) for band in bands]

    def get_true_color_request(self, time_slot, evalscript):
        return SentinelHubRequest(
            evalscript=evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL5P.define_from("5p", service_url=self.config.sh_base_url),
                    time_interval=time_slot,
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=self.bbox,
            size=self.size,
            config=self.config
        )

    def download_data(self, time_slots, evalscripts, bands):
        for i, time_slot in enumerate(time_slots):
            for j, evalscript in enumerate(evalscripts):
                request = self.get_true_color_request(time_slot, evalscript)
                band_name = bands[j]
                start_date = time_slot[0].replace("-", "")
                end_date = time_slot[1].replace("-", "")
                folder_path = Path(self.data_folder) / Path(self.bbox_name) / f"{band_name}"
                folder_path.mkdir(parents=True, exist_ok=True)
                image_path_to = folder_path / f"{start_date}_{end_date}.npy"
                data = request.get_data(save_data=False)
                # Save the numpy data
                np.save(str(image_path_to), data[0])
                print(f"Downloaded data saved to {image_path_to}")


if __name__ == '__main__':
    # Usage
    client_id = "sh-2078a4e9-e65d-4584-bc24-cc911bb6cb2c"
    client_secret = "yLftovOUNqMvIhnT9gzQqLNABAgmpVn7"

    # bbox_name = "UK"
    # bbox_coords = (-7.57216793459, 49.959999905, 1.68153079591, 58.6350001085) # UK

    bbox_name = "Ghana"
    bbox_coords = (-3.24437008301, 4.71046214438, 1.0601216976, 11.0983409693) # Ghana

    # bbox_name = "Europe"
    # bbox_coords = (-12.30, 34.59, 32.52, 63.15)  # Europe

    # bbox_name = "Germany"
    # bbox_coords = (5.98865807458, 47.3024876979, 15.0169958839, 54.983104153)  # Germany


    # bbox_name = "WestAfrica"
    # bbox_coords = (-17.781181,2.108901,15.784238,25.005974) # West Africa

    downloader = Sentinel5PDownloader(client_id, client_secret, bbox_name, bbox_coords, resolution=1000)

    # Define time period for downloading data
    start_date = datetime.datetime(2024, 9, 1)  # year, month, day
    period_days = 49
    time_interval_days = 1
    time_slots = downloader.generate_time_slots(start_date, period_days, time_interval_days)

    '''
        # CO = Carbon monoxide
        # HCHO 	Formaldehyde
        # NO2 	Nitrogen oxide
        # O3 	Ozone
        # SO2 	Sulphur dioxide
        # CH4 	Methane
        # AER_AI_340_380 	UV (Ultraviolet) Aerosol Index calculated based on wavelengths of 340 nm and 380 nm.
        # AER_AI_354_388 	UV (Ultraviolet) Aerosol Index calculated based on wavelengths of 354 nm and 388 nm. 
    '''
    # bands = ["O3"]
    bands = ["CH4"]

    # create the evalscripts using the bands
    evalscripts = downloader.generate_evalscripts(bands)

    # Download data
    downloader.download_data(time_slots, evalscripts, bands)