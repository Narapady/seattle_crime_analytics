from src.elt.client import Client
from src.elt.s3 import S3
from settings import USER_NAME, PASSWORD, AWS_SECRET_KEY, AWS_ACCESS_KEY
import pandas as pd
import time


def main() -> None:
    s3 = S3(aws_access_key=AWS_ACCESS_KEY, aws_secret_key=AWS_SECRET_KEY)
    s3.load_local_csv_to_bucket(
        csv_file_path="data/2008-2023-spd-crime-data.csv",
        key="2008-2023-spd-crime/2008-2023-spd-crime-data.csv",
        bucket_name="s3-bucket-seattle-crime",
    )


if __name__ == "__main__":
    main()
