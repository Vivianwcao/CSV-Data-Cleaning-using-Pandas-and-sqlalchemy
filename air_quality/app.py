import pandas as pd
from sqlalchemy import create_engine
engine=create_engine('postgresql://postgres:1234@127.0.0.1:5432/data_cleaning')

SCHEMA = {
    'CSDUID': 'int64', 
    'CSD': 'string', 
    'Period': 'int64', 
    'Air Quality Health Index': 'int64', 
    'Health Risk': 'string', 
    'OriginalValue': 'float64'
}
df = pd.read_csv('air_quality/download.csv')
print(df.head())
print(df.dtypes)
print(df.shape)
print(df.isna().sum())
df = df[SCHEMA.keys()]
print(df.columns)

df['Air Quality Health Index']=df['Air Quality Health Index'].str.extract(r"(\d+)").astype('int64')
print(df['Air Quality Health Index'].value_counts())
print(df.dtypes)

df.to_sql(
    name="air_quality",
    con=engine,
    if_exists='append',
    index=False,
)