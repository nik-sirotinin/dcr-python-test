from urllib.request import urlopen
import json

from db import Country, CountryTopLevelDomain, Region, TopLevelDomain


class LoadData:
    URL = "https://storage.googleapis.com/dcr-django-test/countries.json"

    def __init__(self):
        # Cache of regions
        self.regions = {}
        # Cache of top level domains
        self.tlds = {}

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
        if found is None:
            country.insert(
                data["name"],
                data["alpha2Code"],
                data["alpha3Code"],
                data["population"],
                region_id,
                data["capital"],
            )
            print(country.data)

        country_id = country.data["id"]
        country.update_capital(data["capital"])
        tld_names = data.get("topLevelDomain", [])
        for tld_name in tld_names:
            tld_id = self.get_tld_id(tld_name)
            ctld = CountryTopLevelDomain()
            ctld.get_or_create(country_id, tld_id)

    def get_region_id(self, region_name):
        if region_name not in self.regions:
            region = Region()
            region.get_or_create_by_name(region_name)
            self.regions[region.data["name"]] = region.data["id"]
        return self.regions[region_name]

    def get_tld_id(self, tld_name):
        if tld_name not in self.tlds:
            tld = TopLevelDomain()
            tld.get_or_create_by_name(tld_name)
            self.tlds[tld.data["name"]] = tld.data["id"]
        return self.tlds[tld_name]

    def run(self):
        data = self.get_raw_data()
        for row in data:
            self.add_country(row)


if __name__ == "__main__":
    LoadData().run()
