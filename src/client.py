import json

from settings import APP_TOKEN, USER_NAME, PASSWORD
import pandas as pd
from sodapy import Socrata


# data from https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5/about_data
class Client:
    url = "data.seattle.gov"
    username = USER_NAME
    password = PASSWORD
    identitier = "tazs-3rd5"

    def make_request(self) -> dict:
        client = Socrata(
            self.url,
            APP_TOKEN,
            username=self.username,
            password=self.password,
        )
        client = Socrata(self.url, None)
        results = client.get(self.identitier, limit=10000)
        results_df = pd.DataFrame.from_records(results)
        return results_df


def print_json(json_data):
    formatted = json.dumps(json_data, indent=2)
    print(formatted)
