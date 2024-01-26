from src.etl.client import Client, get_past_days
from rich import print
import pandas as pd
import datetime

if __name__ == "__main__":
    client = Client()
    client.run()
