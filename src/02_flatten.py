import numpy as np
import pandas as pd
import json

with open("data/raw/rest_countries_data.json", encoding="utf-8") as file:
    raw_json = json.load(file)

country_list = raw_json
parsed_data = []

for country in country_list:
    name = country.get("names", {}).get("common", np.nan)

    iso_code = country.get("codes", {}).get("alpha_3", np.nan)
    if pd.isna(iso_code) or iso_code == "":
        iso_code = country.get('parent', {}).get('alpha_3', np.nan)

    region = country.get("region", np.nan)
    subregion = country.get("subregion", np.nan)
    population = country.get("population", np.nan)
    area = country.get("area", {}).get("kilometers", np.nan)
    
    languages = country.get("languages", [])
    langs_str = ", ".join([lang.get("name", "") for lang in languages]) if languages else np.nan

    currencies = country.get("currencies", [])
    curr_str = ", ".join([curr.get("name", "") for curr in currencies]) if currencies else np.nan

    borders = country.get("borders", [])
    borders_str = ", ".join(borders) if borders else np.nan

    latitude = country.get("coordinates", {}).get("lat", np.nan)
    longitude = country.get("coordinates", {}).get("lng", np.nan)

    capitals = country.get("capitals") or []
    capital = capitals[0].get("name", np.nan) if capitals else np.nan

    un_member = country.get("classification", {}).get("un_member", np.nan)
    disputed = country.get("classification", {}).get("disputed", np.nan)
    flag = country.get("flag", {}).get("emoji", np.nan)
    

    parsed_data.append({
            "Country": name,
            "ISO3": iso_code,
            "Region": region,
            "Subregion": subregion,
            "Population": population,
            "Area": area,
            "Languages": langs_str,
            "Currencies": curr_str,
            "Borders": borders_str,
            "Latitude": latitude,
            "Longitude": longitude,
            "Capital": capital,
            "UN Member": un_member,
            "Disputed": disputed,
            "Flag": flag
        })

df_raw = pd.DataFrame(parsed_data)
df_raw.to_csv("data/interim/rest_countries_raw.csv", index=False)
print(df_raw.head())
