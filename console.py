from src.elt.client import Client
from src.elt.s3 import S3
from settings import USER_NAME, PASSWORD, AWS_SECRET_KEY, AWS_ACCESS_KEY
from src.api.models.report import Report
import pandas as pd
from rich import print
from src.elt.transform import Transform


def main() -> None:
    file_path = "./data/2023-12-31-spd-crime-data.csv"
    transformer = Transform(file_path)
    transformer.preprocess()


if __name__ == "__main__":
    main()
