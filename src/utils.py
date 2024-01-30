import datetime
import json
import boto3


def print_json(json_data) -> None:
    formatted = json.dumps(json_data, indent=2)
    print(formatted)


def get_past_days(from_date: datetime.date, until_date: datetime.date) -> list[str]:
    past_days = []
    while from_date < until_date:
        past_days.append(str(from_date))
        from_date += datetime.timedelta(days=1)
    return past_days


def find_most_recent_date(
    s3_client: boto3.client, bucket_name="s3-bucket-seattle-crime"
) -> datetime.date:
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Iterate through the response to get the file names
    files = []
    for obj in response["Contents"]:
        file_name = obj["Key"]
        files.append(file_name)
    files.remove("2023-spd-crime.csv")

    return max(
        [datetime.datetime.strptime(file[:10], "%Y-%m-%d").date() for file in files]
    )
