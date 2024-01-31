import datetime
import json


def print_json(json_data) -> None:
    formatted = json.dumps(json_data, indent=2)
    print(formatted)


def get_past_days(from_date: datetime.date, until_date: datetime.date) -> list[str]:
    past_days = []
    while from_date < until_date:
        past_days.append(str(from_date))
        from_date += datetime.timedelta(days=1)
    return past_days
