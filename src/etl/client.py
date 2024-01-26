import json

from settings import APP_TOKEN, USER_NAME, PASSWORD, AWS_ACCESS_KEY, AWS_SECRET_KEY
import pandas as pd
from sodapy import Socrata
import datetime
from io import StringIO
import boto3
from botocore.exceptions import ClientError


def print_json(json_data) -> None:
    formatted = json.dumps(json_data, indent=2)
    print(formatted)


def get_past_days(from_date: datetime.date, until_date: datetime.date) -> list[str]:
    """
    Returns a list of past days starting from January 1, 2024 until today.
    """
    past_days = []
    while from_date < until_date:
        past_days.append(str(from_date))
        from_date += datetime.timedelta(days=1)
    return past_days


# data from https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5/about_data
class Client:
    url = "data.seattle.gov"
    username = USER_NAME
    password = PASSWORD
    identitier = "tazs-3rd5"

    def make_request(self, socrata_client: Socrata, query: str) -> pd.DataFrame:
        # TODO: change date to ingest data daily

        results = socrata_client.get(
            self.identitier,
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
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        key = str(df["report_datetime"].iloc[0])[:10] + "-spd-crime.csv"
        try:
            s3_client.put_object(
                Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=key
            )
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
        # NOTE: initial query="select * where date_extract_y(report_datetime) = 2023 limit 100000"
        from_date = datetime.date(2024, 1, 1)
        until_date = datetime.date.today()
        past_days = get_past_days(from_date=from_date, until_date=until_date)
        for day in past_days:
            query = (
                f"SELECT * WHERE date_trunc_ymd(report_datetime) = '{day}T00:00:00.000'"
            )
            df = self.make_request(socrata_client=socrata_client, query=query)
            self.load_to_s3(s3_client=s3_client, df=df)
