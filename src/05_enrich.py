import os
import requests
import pandas as pd

# World Bank API: GDP per capita (current US$), no key needed
URL = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD"
YEAR = "2023"

GDP_RAW = "data/raw/worldbank_gdp_per_capita.csv"
COUNTRIES = "data/clean/countries_clean.csv" 
OUTPUT = "data/clean/countries_enriched.csv"


# 1. Download GDP data and save the raw copy
response = requests.get(URL, params={"format": "json", "date": YEAR, "per_page": 400})
rows = response.json()[1]          # The data is the second item

gdp = pd.DataFrame([
    {"ISO3": r["countryiso3code"], "WB_Name": r["country"]["value"], "GDP_per_capita": r["value"]}
    for r in rows
])

gdp = gdp[gdp["ISO3"] != ""]

gdp.to_csv(GDP_RAW, index=False)
print(f"Downloaded {len(gdp)} World Bank rows")


# 2. Join GDP onto the countries table (left join keeps every country)
countries = pd.read_csv(COUNTRIES)
enriched = pd.merge(countries, gdp[["ISO3", "GDP_per_capita"]], on="ISO3", how="left")


# 3. Report countries that got no GDP value
missing = enriched[enriched["GDP_per_capita"].isnull()]
print(f"{len(missing)} of {len(enriched)} countries have no GDP value:")
print(missing["Country"].tolist())

enriched.to_csv(OUTPUT, index=False)
print(f"Saved {OUTPUT}")