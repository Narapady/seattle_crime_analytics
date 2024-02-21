from src.elt.s3 import S3
from src.elt.client import SocrataClient
from settings import USER_NAME, PASSWORD, AWS_SECRET_KEY, AWS_ACCESS_KEY, APP_TOKEN
from src.api.models.report import Report
import pandas as pd
from rich import print
from src.elt.transform import Transform
from src.utils import fix_col_dtypes


domain = "data.seattle.gov"
username = USER_NAME
password = PASSWORD
app_token = APP_TOKEN
identifier = "tazs-3rd5"


def main() -> None:
    s3 = S3(aws_access_key=AWS_ACCESS_KEY, aws_secret_key=AWS_SECRET_KEY)
    # s3.create_glue_db("seattle_crime")
    # s3.crawl_dataset("seattle_crime", "spd-crime-data")
    df = s3.display_schema("seattle_crime", "spd-crime-data")
    breakpoint()
    # s3.delete_all_files_in_bucket()

    # socrata_client = SocrataClient(domain, APP_TOKEN, USER_NAME, PASSWORD, identifier)
    # query = "SELECT * WHERE date_trunc_ymd(report_datetime) = '2024-02-19T00:00:00.000'"
    # df = socrata_client.make_request(query)
    # df = s3.read_parquet_from_s3()


if __name__ == "__main__":
    main()
