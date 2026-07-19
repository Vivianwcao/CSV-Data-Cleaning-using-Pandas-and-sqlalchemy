import pandas as pd 
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:1234@127.0.0.1:5432/data_cleaning')

df = pd.read_csv('age_death/deaths-by-gender-and-age.csv', header=1)
print(df.head())
# print(df.shape)
print(df.dtypes)
# print(df.index)
print(df.columns)
print(df.isna().sum())
# print(df[df['90+'].isna()])

int_list = ['Calendar Year', '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+', 'NS', 'Res Total', 'Non  Res Total', 'Grand Total']

# converted = df[int_list].apply(pd.to_numeric, errors='coerce')
# print(converted)
# invalid_mask = converted.isna() & df[int_list].notna()
# print(invalid_mask)
# print(invalid_mask.any()) # True if any column has at least one invalid value
# print(invalid_mask.any().any()) # True if any column has any invalid value
# if invalid_mask.any().any():
#     print('At least one invalid entry exists in the selected columns')
#     df[int_list] = converted.astype('Int64')

# This method does to_numeric twice but print the exact invalid cells
for col_label in int_list:
    bad = df[pd.to_numeric(df[col_label], errors='coerce').isna() & df[col_label].notna()][col_label]
    if not bad.empty:
        print(col_label, bad.unique())

df[int_list] = df[int_list].apply(pd.to_numeric, errors='coerce').astype('Int64')

print(df.dtypes)

df.to_sql(
    name='gender_age_death',
    con=engine,
    if_exists="append",
    index=False
)