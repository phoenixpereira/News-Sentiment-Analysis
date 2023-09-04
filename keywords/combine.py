import pandas as pd

# Load the sentiments data
sentiments_df = pd.read_csv('keywords/results/sentiments.csv')

# Define the countries and their corresponding CSV files
countries = {
    'Australia': 'AU.csv',
    'Ireland': 'IE.csv',
    'India': 'IN.csv',
    'United States': 'US.csv',
    'United Kingdom': 'UK.csv'
}

# Iterate through each country's CSV file
for country, csv_file in countries.items():
    # Load the country's CSV data
    country_df = pd.read_csv(f'keywords/results/{csv_file}')

    # Merge sentiments data with the country's CSV data using 'Top Keyword' as the key
    merged_df = pd.merge(country_df, sentiments_df, on='Top Keyword', how='inner')

    # Save the merged data back to the country's CSV file
    merged_df.to_csv(f'keywords/results/{csv_file}', index=False)