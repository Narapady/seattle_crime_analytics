from src.elt.client import Client
from src.elt.s3 import S3
from settings import USER_NAME, PASSWORD, AWS_SECRET_KEY, AWS_ACCESS_KEY
from src.api.models.report import Report
import pandas as pd


def main() -> None:
    crime_df = pd.read_csv("./data/2023-12-31-spd-crime-data.csv")
    report_df = crime_df[["report_number", "report_datetime"]].head(20)
    reports = report_df.to_dict(orient="records")
    first_report = reports[0]
    first_report["report_number"] = 123123
    report = Report(**first_report)
    print(report.__dict__)


if __name__ == "__main__":
    main()
