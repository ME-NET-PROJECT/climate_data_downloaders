import cdsapi
import yaml
import datetime
from pathlib import Path


class ADSCAMSDownloader:
    def __init__(self, credentials_file, bbox, bbox_name, cams_dataset, start_date, period_days, time_interval_days, bands,
                 data_folder="data"):
        self.credentials_file = credentials_file
        self.bbox = bbox
        self.bbox_name = bbox_name
        self.cams_dataset = cams_dataset
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        self.period_days = period_days
        self.time_interval_days = time_interval_days
        self.bands = bands
        self.data_folder = data_folder
        self.client = self.authenticate()
        self.folder_path = Path(self.data_folder) / Path(self.bbox_name)
        self.folder_path.mkdir(parents=True, exist_ok=True)

    def authenticate(self):
        with open(self.credentials_file, 'r') as f:
            credentials = yaml.safe_load(f)
        return cdsapi.Client(url=credentials['url'], key=credentials['key'])

    def generate_time_slots(self):
        dates = [(self.start_date + datetime.timedelta(days=i * self.time_interval_days)).date().isoformat() for i in
                 range(self.period_days + 1)]
        time_slots = [(dates[i], dates[i + 1]) for i in range(len(dates) - 1)]
        print("Time windows:\n")
        for slot in time_slots:
            print(slot)
        return time_slots

    def download_data(self):
        ml_change_date = "2019-07-09"  # model_level_change_date
        time_slots = self.generate_time_slots()
        for time_slot in time_slots:
            start_date = time_slot[0].replace("-", "")
            end_date = time_slot[1].replace("-", "")

            if datetime.datetime.strptime(time_slot[0], "%Y-%m-%d") < datetime.datetime.strptime(ml_change_date,
                                                                                                 "%Y-%m-%d"):
                model_level = '60'
            else:
                model_level= '137'

            image_path_to = self.folder_path / f"{start_date}_{end_date}.nc"
            date_range = str(time_slot[0]) + "/" + str(time_slot[0])
            print(image_path_to, date_range)
            self.client.retrieve(
                'cams-global-atmospheric-composition-forecasts',
                {
                    'variable': self.bands,
                    'date': date_range,  # this is for one day's data
                    'model_level': model_level,
                    'time': '12:00',
                    'leadtime_hour': '0',
                    'type': 'forecast',
                    'area': [self.bbox[3], self.bbox[0], self.bbox[1], self.bbox[2]],  # Specify the geographical area
                    'format': 'netcdf',
                },
                image_path_to)


# Example usage
if __name__ == '__main__':
    credentials_file = 'security/.adsapircV2'

    # bbox = (-7.57216793459, 49.959999905, 1.68153079591, 58.6350001085)  # UK
    # bbox_name = "UK"

    bbox = (-3.24437008301, 4.71046214438, 1.0601216976, 11.0983409693)   # Ghana
    bbox_name = "Ghana"

    cams_dataset = "cams-global-atmospheric-composition-forecasts"

    # bands = [
    #     'surface_pressure',
    #     'uv_biologically_effective_dose',
    #     'uv_biologically_effective_dose_clear_sky',
    # ]

    bands = [
            'carbon_monoxide', 'formaldehyde', 'methane',
            'nitrogen_dioxide', 'nitrogen_monoxide', 'ozone',
            'sulphur_dioxide', 'temperature', 'u_component_of_wind',
            'v_component_of_wind',
    ]

    start_date = "2019-01-01"
    period_days = 365
    time_interval_days = 1

    downloader = ADSCAMSDownloader(
        credentials_file,
        bbox, bbox_name, cams_dataset,
        start_date, period_days,
        time_interval_days, bands
    )
    downloader.download_data()
