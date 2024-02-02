from pydantic import BaseModel
import datetime


class Offense(BaseModel):
    __table__: str = "offenses"
    columns: list[str] = [
        "id",
        "report_id",
        "offense_detail_id",
        "offense_start_datetime",
        "offense_end_datetime",
    ]
    report_id: int
    offense_detail_id: int
    offense_start_datetime: datetime.datetime
    offense_end_datetime: datetime.datetime

    def report(self):
        pass

    def offense_detail(self):
        pass
