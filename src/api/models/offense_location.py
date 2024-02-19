from pydantic import BaseModel


class Offense_Location(BaseModel):
    __table__: str = "offense_locations"
    columns: list[str] = ["id", "longitude", "latitude"]
    staging_cols: list[str] = ["offense_id", "longitude", "latitude"]
    longitude: float
    latitude: float

    def offense_details(self):
        pass
