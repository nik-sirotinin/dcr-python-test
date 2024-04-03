# Digital Control Room - Python Test

Thank you for thaking the time to complete this exercise.

## Introduction

Please clone (don't fork) this repository, complete the exercises below and then upload to a public repository on github and send us the link.

Please don't spend more than 2 hours on this task (not including initial download and setup). If you reach 2 hours, please commit your code as-is to your repository.

## Project Setup

You will need python3.8+ to run this code.

```bash
git clone git@github.com:<TBC>

cd dcr-python-test
git remote remove origin
git remote add origin <Your Repository>

cd src
python3 list_countries.py
```

## Exercises

### Exercise 1 - Add Stats

Please add a script that will provide aggregated stats for each region. The stats should contain:

- The region's name
- The number of countries in that region (a simple count)
- The total population of the region (the sum of the population of each country)

The output should be JSON with a format:

```json
{
    "regions": [
        {
        "name": "Africa",
        "number_countries": xxx,
        "total_population": xxx
        },
        {
        "name": "Americas",
        "number_countries": xxx,
        "total_population": xxx
        },
        ...
    ]
}
```

#### Solution

Created the script at `src/region_stats.py`

### Exercise 2 - Integrate with API

The script:

```bash
python load_data.py
```

currently populates the database from a local JSON file. Please update this management command to obtain the JSON input data from this url: `https://storage.googleapis.com/dcr-django-test/countries.json`

#### Solution

Updated to retrieve JSON from the API using the standard library `urllib` module.

### Exercise 3 - Store additional Data

The previous script:

```bash
python load_data.py
```

currently extracts and stores the data:

- name
- alpha2Code
- alpha3Code
- population
- region

Please update the database tables and management command to also import:

- topLevelDomain
- capital

Please record any SQL commands executed to modify the database schema.

#### Solution

Created a manual migration script:

1. Adds a "capital" column to the "country" table
1. Creates a "topLevelDomain" table
1. Creates a "countryTopLevelDomain" junction table for the many-to-many relationship between countries and top-level domains

Created some new classes in the DB module to handle the new tables, updated `Country` methods to accommodate "capital" column.

Updated the `load_data` script and `Country.list_all()` function to query new data with a JOIN and output all the new information.

**TODO**: the top-level domains from `list_all()` seem to come out as Tuples, I'm not entirely sure why. Also, the way `load_data` clobbers the capital column seems inelegant, I couldn't think of a better place to put it.
