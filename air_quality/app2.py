import pandas as pd
from pandas import json_normalize

df = pd.read_json('air_quality/download.json')
print(df.shape)
# break list → rows
# df = df.explode("Dimensions").reset_index(drop=True)
# print(df.head())
# # break dict → columns
# dim_df=pd.json_normalize(df['Dimensions'])
dim_df = df['Dimensions'].explode()
dim_df = pd.json_normalize(dim_df)
print(dim_df.head())
df_wide = dim_df.pivot(
    columns="Name",
    values='Value'
)
df = df.join(df_wide).drop(
    columns=['Dimensions', 'IndicatorSummaryDescription', 'UnitOfMeasure']
    )
print(df.index.is_unique)
print(df.head())
print(df.columns)
print(df.index)
print(df.shape)