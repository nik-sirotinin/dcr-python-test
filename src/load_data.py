from urllib.request import urlopen
import json

from db import Country, Region


class LoadData:
    URL = "https://storage.googleapis.com/dcr-django-test/countries.json"

    def __init__(self):
        # Cache of regions
        self.regions = {}

    def get_raw_data(self):
        data = None
        with urlopen(self.URL) as response:
            body = response.read()
            data = json.loads(body)
        return data

    def add_country(self, data):
        region_name = data.get("region", "Unknown")
        region_id = self.get_region_id(region_name)

        country = Country()
        found = country.get_by_name(data["name"])
        if found:
            return
        country.insert(
            data["name"],
            data["alpha2Code"],
            data["alpha3Code"],
            data["population"],
            region_id,
        )
        print(country.data)

    def get_region_id(self, region_name):
        if region_name not in self.regions:
            region = Region()
            region.get_or_create_by_name(region_name)
            self.regions[region.data["name"]] = region.data["id"]
        return self.regions[region_name]

    def run(self):
        data = self.get_raw_data()
        for row in data:
            self.add_country(row)


if __name__ == "__main__":
    LoadData().run()
