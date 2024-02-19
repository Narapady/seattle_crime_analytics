import datetime
from pydantic import BaseModel


class Report(BaseModel):
    __table__: str = "reports"
    columns: list[str] = ["id", "report_number", "report_datetime"]
    staging_cols: list[str] = ["offense_id", "report_number", "report_datetime"]
    report_number: str
    report_datetime: datetime.datetime

    def offenses(self):
        pass
