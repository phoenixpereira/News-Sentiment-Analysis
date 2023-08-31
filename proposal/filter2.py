import pandas as pd

# Read the input csv file as a pandas dataframe
df = pd.read_csv("data.csv")

# Convert the publish_date column to datetime format
df["publish_date"] = pd.to_datetime(df["publish_date"], format="%Y%m%d")

# Exclude rows containing "abc" and group the dataframe by date
grouped = df[~df["headline_text"].str.contains(
    "abc")].groupby(df["publish_date"].dt.date)

# Initialize an empty list to store the filtered results
filtered_data_list = []

# Iterate through each group and append the first 10 rows to the filtered list
for _, group_df in grouped:
    filtered_data_list.append(group_df.head(10))

# Concatenate the filtered dataframes in the list into a single dataframe
filtered_data = pd.concat(filtered_data_list)

# Write the output dataframe to a new csv file
filtered_data.to_csv("filtered_data_10_per_day.csv", index=False)
