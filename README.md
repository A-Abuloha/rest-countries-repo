## File Structure:
#### README.md
--> Explains what the project is, who made it, how to install it and how to run it.

#### requirements.txt
--> The list of Python libraries the project needs so anyone can install them all in one go.

#### src/extract.py
--> Connects to the REST Countries API, downloads all countries page by page and saves the raw JSON.

#### src/flatten.py
--> Turns the nested JSON (languages, currencies, borders) into one table, one row per country.

#### src/profile.py
--> Checks data quality: missing values, data types, summary statistics, outliers and region counts.

#### src/clean.py
--> Fixes missing and inconsistent values using the strategy we chose (drop, impute or flag).

#### src/enrich.py
--> Downloads GDP per capita from the World Bank and joins it to the countries by ISO code.

#### src/visualize.py
--> Creates the exploratory charts and saves them in the figures folder.

#### data/raw/
--> The untouched data exactly as it came from the API and the World Bank.

#### data/interim/
--> The flattened table before cleaning.

#### data/clean/
--> The final cleaned and enriched dataset.

#### figures/
--> The charts used in the report.

#### report/
--> The profiling report (PDF).

#### ai-logs/milestone1/index.md
--> AI chats, which tool and what it helped with..