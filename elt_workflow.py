import datetime
from prefect import task, flow
from src.elt.client import Client
from src.elt.s3 import S3
from sodapy import Socrata
from settings import USER_NAME, PASSWORD, AWS_ACCESS_KEY, AWS_SECRET_KEY, APP_TOKEN
import pandas as pd
from src.utils import get_past_days

url = "data.seattle.gov"
username = USER_NAME
password = PASSWORD
identifier = "tazs-3rd5"
client = Client(url=url, username=username, password=password, identifier=identifier)


@task
def make_request(socrata_client: Socrata, query: str) -> pd.DataFrame:
    client = Client(
        url=url, username=username, password=password, identifier=identifier
    )
    return client.make_request(socrata_client=socrata_client, query=query)


@task
def load_to_bucket(
    df: pd.DataFrame,
    bucket_name: str = "s3-bucket-seattle-crime",
) -> None:
    s3 = S3(aws_access_key=AWS_ACCESS_KEY, aws_secret_key=AWS_SECRET_KEY)
    return s3.load_to_bucket(df=df, bucket_name=bucket_name)


@flow(log_prints=True)
def extract_and_load():
    socrata_client = Socrata(
        url,
        APP_TOKEN,
        username=username,
        password=password,
    )
    s3_client = S3(aws_access_key=AWS_ACCESS_KEY, aws_secret_key=AWS_SECRET_KEY)
    # initial query="select * where date_extract_y(report_datetime) = 2023 limit 100000"
    from_date = s3_client.find_most_recent_date(bucket_name="s3-bucket-seattle-crime")
    until_date = datetime.date.today()

    if from_date + datetime.timedelta(days=1) == until_date:
        print("There is no new data to ingest")
        return

    past_days = get_past_days(from_date=from_date, until_date=until_date)
    for day in past_days:
        query = f"SELECT * WHERE date_trunc_ymd(report_datetime) = '{day}T00:00:00.000'"
        crime_df = make_request(socrata_client=socrata_client, query=query)
        load_to_bucket(df=crime_df, bucket_name="s3-bucket-seattle-crime")


if __name__ == "__main__":
    extract_and_load()
