import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:1234@127.0.0.1:5432/data_cleaning")

df = pd.read_csv("cancer_age/13100158.csv")

# # Explore the database
# print(df.shape)
# print(df.dtypes)
# print(df.head())

# In pandas, there is no difference between df.isnull() vs df.isna():
# print(df.isna().sum())
# print(df['UOM'].unique())
# print(df['Characteristics'].unique())
# print(df['GEO'].unique())
# # print(df['REF_DATE'].unique())
# print(df['DGUID'].unique())
# print(df['STATUS'].unique())
# print(df['Sex'].unique())
# print(df['Age group'].unique())
# print(df['Primary types of cancer (ICD-O-3)'].unique())
# print(df.loc[df['VALUE'].isna()])
# print(df.loc[df['VALUE'].isna(), 'Characteristics'].value_counts())
print(df.loc[df["VALUE"].isna(), "Age group"].value_counts())

# # how many rows have a value but also have F status?
# print((df['VALUE'].notna() & (df['STATUS'] == 'F')).sum())

# # how many rows have E status with no value?
# print((df['VALUE'].isna() & (df['STATUS'] == 'E')).sum())

# # full breakdown
# print(df['VALUE'].isna().groupby(df['STATUS'].fillna('null')).sum())
# # print(df['VALUE'].notna().groupby(df['STATUS'].fillna('null')).sum())

# # show all unique STATUS values for rows where VALUE is null
# print(df.loc[df['VALUE'].isna()]['STATUS'].value_counts(dropna=False))

# drop null VALUEs
df = df[df["VALUE"].notna()]
df = df[
    [
        "REF_DATE",
        "GEO",
        "Age group",
        "Sex",
        "Primary types of cancer (ICD-O-3)",
        "Characteristics",
        "VALUE",
    ]
]
print(df.shape)
print(df.isna().sum())
# verify every combination is unique
key_cols = [
    "REF_DATE",
    "GEO",
    "Age group",
    "Sex",
    "Primary types of cancer (ICD-O-3)",
    "Characteristics",
]

# Return all rows that have at least one duplicate match in key_cols
duplicates = df[df.duplicated(subset=key_cols, keep=False)]
print(duplicates.shape[0])

# Take the values inside the 'Characteristics' column and turn them into new column headers.
df_wide = df.pivot(
    index=["REF_DATE", "GEO", "Age group", "Sex", "Primary types of cancer (ICD-O-3)"],
    columns="Characteristics",
    values="VALUE",
)
# print(df_wide.shape)
# print(df_wide.index.is_unique)
# Returns the names of the index (or levels)
print(df_wide.index.names)
# Returns the Index object itself (RangeIndex, Index, or MultiIndex)
print(df_wide.index)
# # Returns an integer (1 for standard index, 2+ for MultiIndex)
# print(df_wide.index.nlevels)
# # Lists the names of all your data columns.
# print(df_wide.columns)
# # print(df_wide.head(100))

print(df_wide.isna().sum())
df_wide = df_wide.reset_index()
# print(df_wide[df_wide['High 95% confidence interval, 5-year net survival'].isna()]['Age group'].value_counts())
# print(df_wide[df_wide['Low 95% confidence interval, 5-year net survival'].isna()]['Age group'].value_counts())

df_wide = df_wide.rename(
    columns={
        "REF_DATE": "year_range",
        "GEO": "region",
        "Age group": "age_group",
        "Sex": "sex",
        "Primary types of cancer (ICD-O-3)": "cancer_type",
        "Number of eligible cases": "cases_count",
        "5-year net survival": "survival_5yr_pct",
        "Low 95% confidence interval, 5-year net survival": "low_95_ci_pct",
        "High 95% confidence interval, 5-year net survival": "high_95_ci_pct",
    }
)
df_wide["cases_count"] = df_wide["cases_count"].astype("Int64")

df_wide[["year_start", "year_end"]] = (
    df_wide["year_range"].str.split("/", expand=True).astype(int)
)
df_wide = df_wide.drop(columns=["year_range"])
print(df_wide[["year_start", "year_end"]].head())
print(df_wide.dtypes)

df_wide.columns.name = None
print(df_wide.columns.names)
print(df_wide.columns.tolist())
# discards the old index instead of promoting it to a column
df_wide = df_wide.reset_index(drop=True)
print(df_wide.index)

df_wide.to_sql(
    name="cancer_survival",
    con=engine,
    # 'append' tells pandas the table already exists, just insert the data, don't touch the schema.
    # use 'replace' to drop if existing table and have pandas (re-)create schema and insert data.
    if_exists="append",
    index=False,  # Without index=False, pandas writes the RangeIndex as a column to the database.
)
print("done")
