from pydantic import BaseModel


class DesignatedPoliceLocation(BaseModel):
    __table__: str = "designated_police_location"
    columns: list[str] = ["id", "precinct", "sector", "mcpp", "address_100_block"]
    staging_cols: list[str] = [
        "offense_id",
        "precinct",
        "sector",
        "mcpp",
        "address_100_block",
    ]
    precinct: str
    sector: str
    mcpp: str
    address_100_block: str

    def offense_details(self):
        pass
