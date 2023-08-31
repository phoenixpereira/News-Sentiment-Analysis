# Import pandas
import pandas as pd

# Read the input csv file as a pandas dataframe
df = pd.read_csv("data.csv")

# Convert the publish_date column to datetime format
df["publish_date"] = pd.to_datetime(df["publish_date"], format="%Y%m%d")

# Group the dataframe by date and get the first 10 rows for each group
df = df.groupby(df["publish_date"].dt.date).head(10)

# Write the output dataframe to a new csv file
df.to_csv("data_10_per_day.csv", index=False)
