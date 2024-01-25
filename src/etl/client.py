import json

from settings import APP_TOKEN, USER_NAME, PASSWORD, AWS_ACCESS_KEY, AWS_SECRET_KEY
import pandas as pd
from sodapy import Socrata
from datetime import datetime, timedelta
from io import StringIO
import boto3


def print_json(json_data) -> None:
    formatted = json.dumps(json_data, indent=2)
    print(formatted)


# data from https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5/about_data
class Client:
    url = "data.seattle.gov"
    username = USER_NAME
    password = PASSWORD
    identitier = "tazs-3rd5"

    def make_request(self, client: Socrata, query: str) -> pd.DataFrame:
        # TODO: change date to ingest data daily
        date = str(datetime.today().date() - timedelta(days=1))

        results = client.get(
            self.identitier,
            query=query,
        )
        results_df = pd.DataFrame.from_records(results)
        return results_df

    # TODO: load ingested files to s3
    def load_to_s3(self, df: pd.DataFrame, bucket_name: str = "s3-bucket-seattle-crime", key: str):
        s3 = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY',
                  aws_secret_access_key='YOUR_SECRET_KEY')
        

    def run(self) -> None:
        client = Socrata(
            self.url,
            APP_TOKEN,
            username=self.username,
            password=self.password,
        )
        # initial: query="SELECT * WHERE date_extract_y(report_datetime) = 2023 LIMIT 100000"
        # subsequence: query=f"SELECT * WHERE date_trunc_ymd(report_datetime) = '{date}T00:00:00.000'"
        query = "SELECT * WHERE date_extract_y(report_datetime) = 2023 LIMIT 100000"
        df = self.make_request(client=client, query=query)
        self.load_to_s3(df)
