import pandas as pd
import sys
sys.stdout.reconfigure(encoding="utf-8")

data = "data/interim/rest_countries_raw.csv"

df = pd.read_csv(data)
print(f"Loaded {len(df)} rows")

text_cols = ["Country", "Region", "Subregion", "Languages", "Currencies", "Borders", "Capital"]
for col in text_cols:
    df[col] = df[col].str.strip()

# Inconsistency: Nauru is listed by its native name
df["Country"] = df["Country"].replace({"Naoero": "Nauru"})

# Borders: missing means the place is an island with no land neighbours
df["Borders"] = df["Borders"].fillna("No land borders")

# Subregion: Antarctic entries have no subregion, so we use their region
df["Subregion"] = df["Subregion"].fillna(df["Region"])

# Capital: Macau is a single city, so it is its own capital; the rest are none
df.loc[df["Country"] == "Macau", "Capital"] = "Macau"
df["Capital"] = df["Capital"].fillna("No capital")

# Currencies and Languages: missing only for uninhabited places, so the value is none
df["Currencies"] = df["Currencies"].fillna("No currency")
df["Languages"] = df["Languages"].fillna("No official language")

# Gini: genuinely unknown (never measured), so filling it with a random number would be misleading
# ISO3: the missing data stays empty (we use Parent ISO3 so we don't have duplicates)
# Flag: left as they are, cosmatic and not relevant for analysis
# Parent ISO3: it is excpected to be mostly empty, because it is a support column for the ISO3 column, so it is left as is
# Outliers: real values, so they are kept

df.to_csv("data/clean/countries_clean.csv", index=False)
print(f"Saved {len(df)} rows to {"data/clean/countries_clean.csv"}")
print(f"Missing values left:\n{df.isnull().sum()[df.isnull().sum() > 0]}")