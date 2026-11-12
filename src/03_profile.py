import pandas as pd
import sys
sys.stdout.reconfigure(encoding="utf-8")

Data = "data/interim/rest_countries_raw.csv"

df = pd.read_csv(Data)

print(f"Shape (Rows, Columns): ({df.shape[0]}, {df.shape[1]})\n")


print(df.head(), "\n")

df.info()

print("\nMissing values per column:")
print(df.isnull().sum())

print(f"\nMissing values % per column: \n{(df.isnull().mean() * 100).round(1)}\n")
print(f"Empty strings per column: \n{(df == "").sum()}\n")
print(f"Zero values in population and area: \n{(df[["Population", "Area"]] == 0).sum()}\n")

print(f"Countries with no borders: \n{df[df["Borders"].isnull()][["Country", "Region"]]}\n")

print(f"Summary statistics: \n{df[['Population', 'Area', 'Number of Languages', 'Number of Currencies', 'Number of Borders', 'Gini']].describe().T.to_string(float_format='{:,.1f}'.format)}")

print(f"\nMean and Median:")
for col in ["Population", "Area"]:
    print(f"{col}: mean = {df[col].mean():,.0f}, median = {df[col].median():,.0f}")

print("\nSkewness (0 = symmetric, > 0 = right-skewed, < 0 = left-skewed):")
print(df[["Population", "Area"]].skew(), "\n")

print(f"Countries per region: \n{df["Region"].value_counts()}\n")

print(f"Duplicated rows: {df.duplicated().sum()}\n")
print(f"Duplicated ISO3 codes:\n Count: {df['ISO3'].dropna().duplicated().sum()}\n")
duplicates = df[df["ISO3"].notna() & df.duplicated("ISO3", keep=False)]
if len(duplicates) > 0:
    print(duplicates[["Country", "ISO3"]], "\n")

print(f"Missing ISO3 codes: {df['ISO3'].isnull().sum()}")
print(df[df["ISO3"].isnull()][["Country", "Parent ISO3"]], "\n")

for col in ["Sovereign", "Dependency", "UN Member", "Disputed"]:
    print(f"{col}: \n{df[col].value_counts()}\n")

print("Outliers (IQR Method):")
for col in ["Population", "Area"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lowerBound = Q1 - 1.5 * IQR
    upperBound = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lowerBound) | (df[col] > upperBound)]

    print(f"\n{col}: Q1 = {Q1:,.0f}, Q3 = {Q3:,.0f}, IQR = {IQR:,.0f}")
    print(f"Lower bound = {lowerBound:,.0f}, Upper bound: {upperBound:,.0f}")
    print(f"Number of outliers: {len(outliers)}")
    print(outliers[["Country", col]].sort_values(col, ascending=False))