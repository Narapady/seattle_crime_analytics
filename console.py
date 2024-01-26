from src.etl.client import Client, get_past_days
from rich import print
import pandas as pd
import datetime

if __name__ == "__main__":
    client = Client()
    client.run()
    # from_date = datetime.date(2024, 1, 1)
    # until_date = datetime.date.today()
    # days = get_past_days(from_date, until_date)
    # print(days)
