from src.etl.client import Client
from settings import USER_NAME, PASSWORD
import pandas as pd
import time


def main() -> None:
    url = "data.seattle.gov"
    username = USER_NAME
    password = PASSWORD
    identifier = "tazs-3rd5"
    client = Client(
        url=url, username=str(username), password=str(password), identifier=identifier
    )
    client.run()


if __name__ == "__main__":
    main()
