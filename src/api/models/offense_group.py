from pydantic import BaseModel


class OffenseGroup(BaseModel):
    __table__: str = "offense_groups"
    columns: list[str] = [
        "id",
        "group_a_b",
        "parent_group",
        "description",
        "offense_code",
        "crime_category",
    ]
    staging_cols: list[str] = [
        "offense_id",
        "group_a_b",
        "parent_group",
        "description",
        "offense_code",
        "crime_category",
    ]
    group_a_b: str
    parent_group: str
    description: str
    offense_code: str
    crime_category: str

    def offense_details(self):
        pass
