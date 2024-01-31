import datetime

import boto3
import pandas as pd
import pytz
from sodapy import Socrata

from settings import APP_TOKEN, AWS_ACCESS_KEY, AWS_SECRET_KEY
from src.etl.s3 import S3
from src.utils import get_past_days


# data from https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5/about_data
class Client:
    def __init__(self, url: str, username: str, password: str, identifier: str):
        self.url = url
        self.username = username
        self.password = password
        self.identifier = identifier

    def make_request(self, socrata_client: Socrata, query: str) -> pd.DataFrame:
        """
        Makes a request to the Socrata API using the provided client and query.

        Args:
            socrata_client (Socrata): The Socrata client used to make the request.
            query (str): The query string used to filter the data.

        Returns:
            pd.DataFrame: A DataFrame containing the results of the request.
        """
        # TODO: change date to ingest data daily

        results = socrata_client.get(
            self.identifier,
            query=query,
        )
        results_df = pd.DataFrame.from_records(results)
        return results_df

    def run(self) -> None:
        socrata_client = Socrata(
            self.url,
            APP_TOKEN,
            username=self.username,
            password=self.password,
        )
        s3_client = S3(aws_access_key=AWS_ACCESS_KEY, aws_secret_key=AWS_SECRET_KEY)
        # initial query="select * where date_extract_y(report_datetime) = 2023 limit 100000"
        from_date = s3_client.find_most_recent_date(
            bucket_name="s3-bucket-seattle-crime"
        )
        until_date = datetime.date.today()

        if from_date + datetime.timedelta(days=1) == until_date:
            print("There is no new data to ingest")
            return

        past_days = get_past_days(from_date=from_date, until_date=until_date)
        breakpoint()
        for day in past_days:
            if day != until_date:
                query = f"SELECT * WHERE date_trunc_ymd(report_datetime) = '{day}T00:00:00.000'"
                crime_df = self.make_request(socrata_client=socrata_client, query=query)
                s3_client.load_to_bucket(
                    df=crime_df, bucket_name="s3-bucket-seattle-crime"
                )
