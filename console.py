from src.client import Client
from rich import print
import pandas as pd

# Convert to pandas DataFrame
if __name__ == "__main__":
    client = Client()
    df = client.make_request()
    df.head()
    # df.to_csv("./data/crime_raw.csv", index=False)

    # print_json(data[0])
