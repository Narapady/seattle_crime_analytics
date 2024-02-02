import pandas as pd
from sodapy import Socrata


# data from https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5/about_data
class Client:
    def __init__(
        self, url: str, username: str | None, password: str | None, identifier: str
    ):
        self.url = url
        self.username = username
        self.password = password
        self.identifier = identifier

    def make_request(self, socrata_client: Socrata, query: str) -> pd.DataFrame:
        """
        Makes a request to the Socrata API using the provided client and query.

        Args:
            socrata_client (Socrata): The Socrata client used to make the request.
            query (str): The query string used to filter the data.
        Returns:
            pd.DataFrame: A DataFrame containing the results of the request.
        """
        # TODO: change date to ingest data daily

        results = socrata_client.get(
            self.identifier,
            query=query,
        )
        results_df = pd.DataFrame.from_records(results)

        return results_df
