import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:1234@127.0.0.1:5432/data_cleaning')

df=pd.read_excel('age_death/deaths-by-gender-and-age.xlsx', engine="openpyxl", header=1)
print(df.head())
print(df.dtypes)
print(df.isna().sum())

int_list = ['Calendar Year', '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+', 'NS', 'Res Total', 'Non  Res Total', 'Grand Total']

cleaned = df[int_list].apply(pd.to_numeric, errors='coerce')
has_bad_cols = cleaned.isna() & df[int_list].notna()
if has_bad_cols.any().any():
    df[int_list] = cleaned.astype('Int64')

print(df.dtypes)

df.to_sql(
    name="gender_age_death_xlsx",
    index=False,
    con=engine,
    if_exists='append'
)


