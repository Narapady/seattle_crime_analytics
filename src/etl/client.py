import json

from settings import APP_TOKEN, USER_NAME, PASSWORD
import pandas as pd
from sodapy import Socrata
from datetime import datetime, timedelta


# data from https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5/about_data
class Client:
    url = "data.seattle.gov"
    username = USER_NAME
    password = PASSWORD
    identitier = "tazs-3rd5"

    def make_request(self) -> pd.DataFrame:
        # TODO: change date to ingest data daily
        client = Socrata(
            self.url,
            APP_TOKEN,
            username=self.username,
            password=self.password,
        )
        date = str(datetime.today().date() - timedelta(days=1))

        # initial query="SELECT * WHERE date_extract_y(report_datetime) = 2023 LIMIT 100000"
        # subsequence query is daily data
        results = client.get(
            self.identitier,
            query=f"SELECT * WHERE date_trunc_ymd(report_datetime) = '{date}T00:00:00.000'",
        )
        results_df = pd.DataFrame.from_records(results)
        return results_df


def print_json(json_data):
    formatted = json.dumps(json_data, indent=2)
    print(formatted)
