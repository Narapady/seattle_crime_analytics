import pandas as pd
from sodapy import Socrata
from settings import USER_NAME, PASSWORD, AWS_ACCESS_KEY, AWS_SECRET_KEY, APP_TOKEN
from datetime import datetime
from src.elt.aws import AWS


# data from https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5/about_data
class SocrataClient:
    def __init__(
        self,
        domain: str,
        app_token: str | None,
        username: str | None,
        password: str | None,
        identifier: str,
    ):
        self.domain = domain
        self.app_token = app_token
        self.username = username
        self.password = password
        self.identifier = identifier

    def build_client(self) -> Socrata:
        client = Socrata(self.domain, self.app_token, self.username, self.password)
        return client

    def build_query(self) -> str:
        most_recent_date = AWS().find_most_recent_date(
            "seattle_crime", "spd_crime_data"
        )
        today_date = datetime.today().date()
        date_str = today_date.strftime("%Y-%m-%d")
        query = f"""SELECT *
                    WHERE report_datetime between '{most_recent_date}T00:00:00.000' and '{date_str}T00:00:00.000'
                    LIMIT 10000
                """
        return query

    def make_request(self) -> pd.DataFrame:
        query = self.build_query()
        results = self.build_client().get(self.identifier, query=query)
        results_df = pd.DataFrame.from_records(results)
        return results_df
