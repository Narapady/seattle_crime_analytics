from src.elt.aws import AWS
from src.elt.client import SocrataClient
from settings import USER_NAME, PASSWORD, AWS_SECRET_KEY, AWS_ACCESS_KEY, APP_TOKEN
from src.api.models.report import Report
import pandas as pd
from rich import print
from src.elt.transform import Transform
from src.utils import fix_col_dtypes
from datetime import datetime

domain = "data.seattle.gov"
username = USER_NAME
password = PASSWORD
app_token = APP_TOKEN
identifier = "tazs-3rd5"


def main() -> None:
    aws = AWS(aws_access_key=AWS_ACCESS_KEY, aws_secret_key=AWS_SECRET_KEY)
    # aws.create_glue_db("seattle_crime")
    # aws.crawl_dataset("seattle_crime", "spd_crime_data")
    # df = aws.display_schema("seattle_crime", "spd_crime_data")
    # s3.delete_all_files_in_bucket()

    socrata_client = SocrataClient(domain, APP_TOKEN, USER_NAME, PASSWORD, identifier)
    df = socrata_client.make_request()
    breakpoint()


if __name__ == "__main__":
    main()
