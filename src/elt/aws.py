import boto3
import pandas as pd
import datetime
from src.utils import build_file_path, extract_date_substrings
import awswrangler as wr
from settings import AWS_ACCESS_KEY, AWS_SECRET_KEY

# TODO: Migrate to AWS wrangler
# TODO: Change class name to AWS instead of S3


class AWS:
    def __init__(
        self,
        aws_access_key: str | None = AWS_ACCESS_KEY,
        aws_secret_key: str | None = AWS_SECRET_KEY,
    ) -> None:
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key

    def s3_client(self):
        client = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
        )
        return client

    def write_parquet_to_s3(
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
        response = self.s3_client().list_objects_v2(Bucket=bucket_name)
        if "Contents" in response:
            objects = [{"Key": obj["Key"]} for obj in response["Contents"]]
            self.client.delete_objects(Bucket=bucket_name, Delete={"Objects": objects})

    @classmethod
    def find_most_recent_date(cls, glub_db: str, table: str) -> datetime.datetime:
        query = f"SELECT MAX(report_datetime) most_recent_date FROM {table}"
        result = wr.athena.read_sql_query(sql=query, database=glub_db)
        date = result["most_recent_date"].iloc[0]
        date_str = date.strftime("%Y-%m-%d")
        return date_str
