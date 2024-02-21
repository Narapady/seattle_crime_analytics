import pandas as pd
from sodapy import Socrata
from settings import USER_NAME, PASSWORD, AWS_ACCESS_KEY, AWS_SECRET_KEY, APP_TOKEN


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

    def make_request(self, query: str) -> pd.DataFrame:
        # TODO: change date to ingest data daily
        results = self.build_client().get(
            self.identifier,
            query=query,
        )
        results_df = pd.DataFrame.from_records(results)
        return results_df
