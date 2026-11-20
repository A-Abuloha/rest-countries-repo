import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.stdout.reconfigure(encoding="utf-8")

data = "data/clean/countries_enriched.csv"
figures = "figures/"

df = pd.read_csv(data)
sns.set_theme(style="whitegrid")

darkBlue = "#4C72B0"
lightBlue = "#A6BDDB"

# Figure 1: Population Distribution by Region
# Question: How is population spread across the regions?
# Chart: Box plot, log scale because population goes from around 30 people to 1.4 billion
# Why: Shows the median, spread and outliers of each region in one chart
populated = df[df["Population"] > 0]
order = populated.groupby("Region")["Population"].median().sort_values(ascending=False).index

fig, ax = plt.subplots(figsize=(10,6))
sns.boxplot(data=populated, x="Region", y = "Population", order=order, ax=ax, color = darkBlue)
ax.set_yscale("log")
ax.set_title("Population distribution by region")
ax.set_xlabel("Region")
ax.set_ylabel("Population (log scale)")

plt.tight_layout()
plt.savefig(figures + "01_population_by_region.png", dpi=150)
plt.close()
print("Saved fig 1")

# Figure 2: Countries and Territories per Region
# Question: How many entries are in each region and how many are sovereign?
# Chart: Stacked bar chart
# Why: Shows the total per region and the sovereign/dependency split at the same time
counts = df.groupby(["Region", "Sovereign"]).size().unstack(fill_value=0)
counts.columns = ["Dependency", "Sovereign"]
counts = counts.sort_values("Sovereign", ascending=False)
counts = counts[["Sovereign", "Dependency"]]

fig, ax = plt.subplots(figsize=(10,6))
counts.plot(kind="bar", stacked = True, color = [darkBlue, lightBlue], ax=ax, edgecolor = "white")
ax.set_title("Number of countries and territories per region")
ax.set_xlabel("Region")
ax.set_ylabel("Number of entries")
ax.legend(title = "Status")
ax.grid(axis = "x", visible=False)
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig(figures + "02_countries_per_region.png", dpi=150)
plt.close()
print("Saved fig 2")

# Figure 3: Global Reach of Official Languages
# Question: Which languages are official in the most countries and how many people live there?
# Chart: Two horizontal bar charts side by side
# Why: Compares number of countries vs population for the same languages (population is not speakers)
languages = df[df["Languages"] != "No official language"].copy()
languages["Language"] = languages["Languages"].str.split(", ")
languages = languages.explode("Language")

reach = languages.groupby("Language").agg(Countries = ("Country", "count"), Population = ("Population", "sum"))
top = reach.sort_values("Countries", ascending=False).head(10)
top = top.sort_values("Countries")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6), sharey=True)
ax1.barh(top.index, top["Countries"], color = darkBlue)
ax1.set_title("Countries where it is official")
ax1.set_xlabel("Number of countries")
ax2.barh(top.index, top["Population"] / 1e9, color = darkBlue)
ax2.set_title("Population of those countries")
ax2.set_xlabel("Population (billions)")
ax1.grid(axis = "y", visible=False)
ax2.grid(axis = "y", visible=False)
fig.suptitle("Global reach of official languages (top 10)")

plt.tight_layout()
plt.savefig(figures + "03_language_reach.png", dpi=150)
plt.close()
print("Saved fig 3")

# Figure 4: Population Density and Microstate Outliers
# Question: Which countries and territories are the most crowded?
# Chart: Top 15 horizontal bar chart
# Why: Ranking is easy to read and shows that small microstates beat every big country
density = populated.copy()
density["Density"] = density["Population"] / density["Area"]
topDensity = density.sort_values("Density", ascending=False).head(15)
topDensity = topDensity.sort_values("Density")

colors = []
for sovereign in topDensity["Sovereign"]:
    if sovereign:
        colors.append(darkBlue)
    else:
        colors.append(lightBlue)

fig, ax = plt.subplots(figsize=(10,7))
ax.barh(topDensity["Country"], topDensity["Density"], color = colors)
ax.set_title("Top 15 most densely populated countries and territories")
ax.set_xlabel("People per km²")
ax.grid(axis = "y", visible=False)
ax.legend(handles = [plt.Rectangle((0,0), 1, 1, color = darkBlue), plt.Rectangle((0,0), 1, 1, color = lightBlue)],
          labels = ["Sovereign", "Dependency"], title = "Status", loc = "lower right")

plt.tight_layout()
plt.savefig(figures + "04_population_density.png", dpi=150)
plt.close()
print("Saved fig 4")

# Figure 5: Land Border Connectivity Across Continents
# Question: How many land neighbours do countries have in each region?
# Chart: Box plot with a jittered strip plot on top
# Why: The box sums up each region and the dots show every country, islands sit at 0
borderOrder = df.groupby("Region")["Number of Borders"].median().sort_values(ascending=False).index

fig, ax = plt.subplots(figsize=(10,6))
sns.boxplot(data=df, x="Region", y = "Number of Borders", order=borderOrder, ax=ax, color = lightBlue, showfliers=False)
sns.stripplot(data=df, x="Region", y = "Number of Borders", order=borderOrder, ax=ax, color = darkBlue, jitter=0.25, size=4, alpha=0.7)
ax.set_title("Number of land borders per country by region")
ax.set_xlabel("Region")
ax.set_ylabel("Number of land borders")

plt.tight_layout()
plt.savefig(figures + "05_land_borders.png", dpi=150)
plt.close()
print("Saved fig 5")

# Figure 6: Currency Blocs vs Own Currencies
# Question: How many countries share a currency (Euro, US dollar...) vs have their own?
# Chart: Stacked horizontal bar chart
# Why: Shows the total per region and the shared/own split, a currency is shared if more than one entry uses it
withCurrency = df[df["Currencies"] != "No currency"].copy()
withCurrency["Currency"] = withCurrency["Currencies"].str.split(", ")
currencyRows = withCurrency.explode("Currency")

usersPerCurrency = currencyRows["Currency"].value_counts()
sharedCurrencies = usersPerCurrency[usersPerCurrency > 1].index

usesShared = []
for currencies in withCurrency["Currency"]:
    shared = False
    for currency in currencies:
        if currency in sharedCurrencies:
            shared = True
    usesShared.append(shared)
withCurrency["Uses Shared"] = usesShared

currencyCounts = withCurrency.groupby(["Region", "Uses Shared"]).size().unstack(fill_value=0)
currencyCounts.columns = ["Own currency", "Shared currency"]
currencyCounts = currencyCounts[["Shared currency", "Own currency"]]
currencyCounts = currencyCounts.loc[currencyCounts.sum(axis=1).sort_values().index]

fig, ax = plt.subplots(figsize=(10,6))
currencyCounts.plot(kind="barh", stacked = True, color = [darkBlue, lightBlue], ax=ax, edgecolor = "white")
ax.set_title("Shared currencies vs own currencies by region")
ax.set_xlabel("Number of entries")
ax.set_ylabel("Region")
ax.legend(title = "Currency type", loc = "lower right")
ax.grid(axis = "y", visible=False)

plt.tight_layout()
plt.savefig(figures + "06_currency_blocs.png", dpi=150)
plt.close()
print("Saved fig 6")

# Figure 7: Income Inequality (Gini) by Region and Data Completeness
# Question: Which regions are the most unequal and how much Gini data do we actually have?
# Chart: Box plot with the number of countries that have data under each region
# Why: Compares inequality and shows the missing Gini data from profiling, Antarctic is removed (no data)
gini = df[df["Region"] != "Antarctic"]
giniOrder = gini.groupby("Region")["Gini"].median().sort_values(ascending=False).index
withData = gini.groupby("Region")["Gini"].count()
total = gini.groupby("Region").size()

labels = []
for region in giniOrder:
    labels.append(f"{region}\n({withData[region]} of {total[region]} have data)")

fig, ax = plt.subplots(figsize=(10,6))
sns.boxplot(data=gini, x="Region", y = "Gini", order=giniOrder, ax=ax, color = darkBlue)
ax.set_xticks(range(len(giniOrder)))
ax.set_xticklabels(labels)
ax.set_title("Income inequality (Gini index) by region")
ax.set_xlabel("")
ax.set_ylabel("Gini index (0 = equal, 100 = unequal)")

plt.tight_layout()
plt.savefig(figures + "07_gini_by_region.png", dpi=150)
plt.close()
print("Saved fig 7")