# REST Countries – Data Engineering Project

## How to Run
1. Install the libraries: `pip install -r requirements.txt`
2. Put your REST Countries API key in `src/01_extract.py`
3. Run the scripts in order from the main folder:
```
python src/01_extract.py
python src/02_flatten.py
python src/03_profile.py
python src/04_clean.py
python src/05_enrich.py
python src/06_visualize.py
```

## File Structure:
#### README.md
--> Explains what the project is, who made it, how to install it and how to run it.

#### requirements.txt
--> The list of Python libraries the project needs so anyone can install them all in one go.

#### src/01_extract.py
--> Connects to the REST Countries API, downloads all countries page by page and saves the raw JSON.

#### src/02_flatten.py
--> Turns the nested JSON (languages, currencies, borders) into one table, one row per country.

#### src/03_profile.py
--> Checks data quality: missing values, data types, summary statistics, outliers and region counts.

#### src/04_clean.py
--> Fixes missing and inconsistent values using the strategy we chose (drop, impute or flag).

#### src/05_enrich.py
--> Downloads GDP per capita from the World Bank and joins it to the countries by ISO code.

#### src/06_visualize.py
--> Creates the 7 exploratory charts and saves them in the figures folder.

#### data/raw/rest_countries_data.json
--> The untouched data exactly as it came from the REST Countries API.

#### data/raw/worldbank_gdp_per_capita.csv
--> The GDP per capita data exactly as it came from the World Bank.

#### data/interim/rest_countries_raw.csv
--> The flattened table before cleaning.

#### data/clean/countries_clean.csv
--> The cleaned dataset.

#### data/clean/countries_enriched.csv
--> The cleaned dataset with GDP per capita added.

#### figures/
--> The 7 charts used in the report.

#### report/profile_output.txt
--> The full output of the profiling script.

#### report/
--> The profiling report (PDF).

#### ai-logs/milestone1/index.md
--> AI chats, which tool and what it helped with.