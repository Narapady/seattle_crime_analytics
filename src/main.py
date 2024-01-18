import requests


# data from https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5/about_data
class Client:
    url = "https://data.seattle.gov/resource/tazs-3rd5.json"

    def make_request(self) -> dict:
        res = requests.get(self.url)
        return res.json()


if __name__ == "__main__":
    client = Client()
    data = client.make_request()
    print(data[0].keys())
