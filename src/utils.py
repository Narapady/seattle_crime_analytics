import datetime
import json
import re
import pandas as pd


def print_json(json_data) -> None:
    formatted = json.dumps(json_data, indent=2)
    print(formatted)


def get_past_days(from_date: datetime.date, until_date: datetime.date) -> list[str]:
    past_days = []
    while from_date < until_date:
        past_days.append(str(from_date))
        from_date += datetime.timedelta(days=1)
    return past_days


def extract_date_substrings(input_str: str) -> str:
    date_pattern = r"\d{4}-\d{2}-\d{2}"  # Regular expression pattern for "yyyy-mm-dd"
    dates = re.findall(date_pattern, input_str)
    return str(dates[0])


def build_file_path(df: pd.DataFrame) -> str:
    dir = str(df["report_datetime"].iloc[0])[:4] + "-spd-crime/"
    sub_dir = str(df["report_datetime"].iloc[0])[:7] + "/"
    file_name = str(df["report_datetime"].iloc[0])[:10] + "-spd-crime.csv"
    return dir + sub_dir + file_name
