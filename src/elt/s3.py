import boto3
from io import StringIO
import pandas as pd
from botocore.exceptions import ClientError, NoCredentialsError
import datetime
from src.utils import build_file_path, extract_date_substrings
import awswrangler as wr


# TODO: Migrate to AWS wrangler
# TODO: Change class name to AWS instead of S3


class S3:
    def __init__(self, aws_access_key: str | None, aws_secret_key: str | None) -> None:
        self.client = boto3.client(
            "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
        )

    def write_to_parquet(
        self,
        df: pd.DataFrame,
        file_path: str = "s3://s3-bucket-seattle-crime/crime_data.parquet",
    ) -> None:
        wr.s3.to_parquet(
            df, file_path, dataset=True, partition_cols=["report_year", "report_month"]
        )

    def create_glue_db(self, db_name: str):
        wr.catalog.create_database(db_name)

    def delete_glue_db(self, db_name: str):
        wr.catalog.delete_database(db_name)

    def crawl_dataset(self, glue_db: str, table_name: str):
        res = wr.s3.store_parquet_metadata(
            path="s3://s3-bucket-seattle-crime/",
            database=glue_db,
            table=table_name,
            dataset=True,
            mode="overwrite",
        )

    def display_schema(self, glue_db: str, table_name: str):
        return wr.catalog.table(database=glue_db, table=table_name)

    def read_parquet_from_s3(
        self, file_path: str = "s3://s3-bucket-seattle-crime/crime_data.parquet"
    ):
        df = wr.s3.read_parquet(file_path, dataset=True)

        return df

    def delete_all_files_in_bucket(self, bucket_name: str = "s3-bucket-seattle-crime"):
        response = self.client.list_objects_v2(Bucket=bucket_name)
        if "Contents" in response:
            objects = [{"Key": obj["Key"]} for obj in response["Contents"]]
            self.client.delete_objects(Bucket=bucket_name, Delete={"Objects": objects})

    # FIXME: find most recent data using athena and glue
    def find_most_recent_date(
        self, bucket_name="s3-bucket-seattle-crime"
    ) -> datetime.date:
        response = self.client.list_objects_v2(Bucket=bucket_name)

        # Iterate through the response to get the file names
        files = []
        for obj in response["Contents"]:
            file_name = obj["Key"]
            files.append(file_name)

        file_date = extract_date_substrings(input_str=str(files[-1]))
        date_object = datetime.datetime.strptime(file_date, "%Y-%m-%d").date()

        return date_object
