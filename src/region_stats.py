import json
from typing import Dict, List, TypedDict
from db import Country


class RegionData(TypedDict):
    number_countries: int
    total_population: int


class Region(RegionData):
    name: str


class AggregatedRegionStats(TypedDict):
    regions: List[Region]


def aggregate_region_stats():
    region_dict: Dict[str, RegionData] = dict()

    for country in Country.list_all():
        region_name = country.data["region_name"]
        population = country.data["population"]

        region = region_dict.get(region_name)
        if region is None:
            region_dict[region_name] = RegionData(
                number_countries=1, total_population=population
            )
        else:
            region["number_countries"] += 1
            region["total_population"] += population

    regions = [
        Region(
            name=name,
            number_countries=region["number_countries"],
            total_population=region["total_population"],
        )
        for [name, region] in region_dict.items()
    ]
    return AggregatedRegionStats(regions=regions)


if __name__ == "__main__":
    print(json.dumps(aggregate_region_stats()))
