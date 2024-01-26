import pandas as pd
import os
from datetime import date


def selected_unprocessed_files(file_path: str) -> list[str]:
    files = os.listdir(file_path)
    today = date.today()
    for file in files:
        file_date = file[:10]
        pass


class CrimeAdapter:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def preprocess() -> None:
        pass

    def load_to_postgres():
        pass

    def load_files_to_postgres():
        pass

    def run():
        file_path = "./data"
