from pydantic import BaseModel


class Offense_Location(BaseModel):
    __table__: str = "offense_locations"
    columns: list[str] = ["id", "longitude", "latitude"]
    longitude: float
    latitude: float

    def offense_details(self):
        pass
