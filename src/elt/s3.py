import boto3
from io import StringIO
import pandas as pd
from botocore.exceptions import ClientError, NoCredentialsError
import datetime
from src.utils import build_file_path, extract_date_substrings


# TODO: Migrate to AWS wrangler
class S3:
    def __init__(self, aws_access_key: str | None, aws_secret_key: str | None) -> None:
        self.client = boto3.client(
            "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
        )

    def load_local_csv_to_bucket(
        self,
        csv_file_path: str,
        key: str,
        bucket_name: str = "s3-bucket-seattle-crime",
    ) -> None:
        try:
            self.client.upload_file(csv_file_path, bucket_name, key)
            print("File uploaded successfully!")
        except FileNotFoundError:
            print("The file does not exist.")
        except NoCredentialsError:
            print("Credentials not available.")

    def load_to_bucket(
        self,
        df: pd.DataFrame,
        bucket_name: str = "s3-bucket-seattle-crime",
    ):
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        key = build_file_path(df=df)
        try:
            self.client.put_object(
                Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=key
            )
            print(f"loaded {key} to S3")
        except ClientError as e:
            # Handle the specific client error
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            print(f"error code: {error_code}, error message: {error_message}")

    def delete_all_files_in_bucket(self, bucket_name: str = "s3-bucket-seattle-crime"):
        bucket = self.client.Bucket(bucket_name)
        bucket.objects.all().delete()

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
