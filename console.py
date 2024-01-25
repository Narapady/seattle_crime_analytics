from src.client import Client
from rich import print
import pandas as pd

if __name__ == "__main__":
    client = Client()
    data = client.get_dataset()
    # data.to_csv("./data/spd-crime-data-2023.csv", index=False)
    print(data.head())
