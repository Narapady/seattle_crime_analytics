from pydantic import BaseModel


class OffenseDetail(BaseModel):
    __table__: str = "offense_details"
    columns: list[str] = [
        "id",
        "offense_location_id",
        "designated_police_location_id",
        "offense_group_id",
    ]
    offense_location_id: int
    designated_police_location_id: int
    offense_group_id: int

    def offsense_location(self):
        pass

    def offsense_group(self):
        pass

    def designated_police_location(self):
        pass

    def offenses(self):
        pass
