from src.elt.client import Client
from src.elt.s3 import S3
from settings import USER_NAME, PASSWORD, AWS_SECRET_KEY, AWS_ACCESS_KEY
import pandas as pd
import time


def main() -> None:
    s3 = S3(aws_access_key=AWS_ACCESS_KEY, aws_secret_key=AWS_SECRET_KEY)
    most_recent_file = s3.find_most_recent_date()
    print(most_recent_file)


if __name__ == "__main__":
    main()
