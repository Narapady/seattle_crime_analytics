from pydantic import BaseModel


class DesignatedPoliceLocation:
    __table__: str = "designated_police_location"
    columns: list[str] = ["id", "precinct", "sector", "mcpp", "address_100_block"]
    precinct: str
    sector: str
    mcpp: str
    address_100_block: str

    def offense_details(self):
        pass
