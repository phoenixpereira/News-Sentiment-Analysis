import pandas as pd

# Load the sentiments data
sentiments_df = pd.read_csv('keywords/results/sentiments.csv')

# Define the countries and their corresponding CSV files
countries = {
    'Australia': 'AU.csv',
    'Ireland': 'IE.csv',
    'India': 'IN.csv',
    'United States': 'US.csv',
    'England': 'GB.csv'
}

# Iterate through each country's CSV file
for country, csv_file in countries.items():
    # Load the country's CSV data
    country_df = pd.read_csv(f'keywords/results/{csv_file}')
    
    # Merge sentiments data with the country's CSV data using 'Top Keyword' and 'Interval' as the keys
    merged_df = country_df.merge(sentiments_df, on=['Top Keyword'], how='left')
    
    # Fill missing sentiment values with 'neutral'
    merged_df['sentiment'].fillna('neutral', inplace=True)

    # Drop duplicate rows keeping only the first occurrence within the same 'Interval'
    merged_df = merged_df.drop_duplicates(subset=['Interval', 'Top Keyword'], keep='first')

    # Save the modified data back to the country's CSV file
    merged_df.to_csv(f'keywords/results/{csv_file}', index=False, columns=['Interval', 'Top Keyword', 'Count', 'sentiment'])
