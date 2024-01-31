import datetime
from io import StringIO

import boto3
import pandas as pd
import pytz
from botocore.exceptions import ClientError
from sodapy import Socrata

from settings import APP_TOKEN, AWS_ACCESS_KEY, AWS_SECRET_KEY
from src.utils import find_most_recent_date, get_past_days


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

    # TODO: load ingested files to s3
    def load_to_s3(
        self,
        s3_client: boto3.client,
        df: pd.DataFrame,
        bucket_name: str = "s3-bucket-seattle-crime",
    ):
        """
        Loads a pandas DataFrame to an S3 bucket using the provided S3 client.

        Parameters:
            s3_client (boto3.client): The S3 client object.
            df (pd.DataFrame): The DataFrame to be loaded to S3.
            bucket_name (str): The name of the S3 bucket. Default is "s3-bucket-seattle-crime".

        Returns:
            None
        """
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        key = str(df["report_datetime"].iloc[0])[:10] + "-spd-crime.csv"
        try:
            s3_client.put_object(
                Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=key
            )
            print(f"loaded {key} to S3")
        except ClientError as e:
            # Handle the specific client error
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            print(f"error code: {error_code}, error message: {error_message}")

    def run(self) -> None:
        socrata_client = Socrata(
            self.url,
            APP_TOKEN,
            username=self.username,
            password=self.password,
        )
        s3_client = boto3.client(
            "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
        )
        # initial query="select * where date_extract_y(report_datetime) = 2023 limit 100000"
        from_date = find_most_recent_date(s3_client=s3_client)
        until_date = datetime.datetime.now(tz=pytz.timezone("Pacific/Apia")).date()

        if from_date + datetime.timedelta(days=1) == until_date:
            print("There is no new data to ingest")
            return

        past_days = get_past_days(from_date=from_date, until_date=until_date)
        for day in past_days:
            query = (
                f"SELECT * WHERE date_trunc_ymd(report_datetime) = '{day}T00:00:00.000'"
            )
            crime_df = self.make_request(socrata_client=socrata_client, query=query)
            self.load_to_s3(s3_client=s3_client, df=crime_df)
