import pandas as pd
import matplotlib.pyplot as plt
import os

# Map country codes to full names
country_mapping = {
    'AU': 'Australia',
    'IE': 'Ireland',
    'IN': 'India',
    'UK': 'UK',
    'US': 'US'
}

# Read sentiment data from CSV files
sentiment_directory = 'sentiment/results'
sentiments_data = []

for country_code in country_mapping.keys():
    file_path = os.path.join(
        sentiment_directory, f'sentiments_{country_code}.csv')
    data = pd.read_csv(file_path)
    data['Country'] = country_mapping[country_code]
    sentiments_data.append(data)

# Concatenate all sentiment data
combined_data = pd.concat(sentiments_data, ignore_index=True)

# Convert publish_date to datetime
combined_data['publish_date'] = pd.to_datetime(combined_data['publish_date'])

# Plotting the combined trend lines
plt.figure(figsize=(12, 8))

for country_name, country_data in combined_data.groupby('Country'):
    plt.plot(country_data['publish_date'],
             country_data['Positive'], label=f'{country_name} (Positive)')
    plt.plot(country_data['publish_date'],
             country_data['Negative'], label=f'{country_name} (Negative)')

plt.xlabel('Date')
plt.ylabel('Count')
plt.title('News Headline Sentiment Over Time')
plt.legend()

# Set x-axis labels for every year
years = pd.to_datetime(combined_data['publish_date']).dt.year.unique()
plt.xticks(ticks=pd.to_datetime(years, format='%Y'), labels=years, rotation=45)

plt.tight_layout()
plt.show()
