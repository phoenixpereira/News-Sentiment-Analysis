import pandas as pd

data = pd.read_csv('parks.csv')
df = pd.DataFrame(data)

records = df[(df['Latitude'] > 60) & (df['Acres'] > 10**6)].head(5)

print(records)
