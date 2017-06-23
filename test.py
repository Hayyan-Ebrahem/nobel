import pandas as pd

df = pd.read_json("/home/oracle/learn/python/nobel/nobel_winners/bio.json")

df = df.set_index('name')
print(df)

