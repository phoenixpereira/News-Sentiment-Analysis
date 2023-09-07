import pandas as pd
import matplotlib.pyplot as plt
import os

# Map country codes to full names
country_mapping = {
    'AU': 'Australia',
    'IE': 'Ireland',
    'IN': 'India',
    'GB': 'England',
    'US': 'United States'
}

# Read sentiment data from CSV files
sentiment_directory = 'sentiment/results'
sentiments_data = []

for country_code in country_mapping.keys():
    file_path = os.path.join(sentiment_directory, f'{country_code}.csv')
    data = pd.read_csv(file_path)
    data['Country'] = country_mapping[country_code]
    sentiments_data.append(data)

# Concatenate all sentiment data
combined_data = pd.concat(sentiments_data, ignore_index=True)

# Convert publish_date to datetime
combined_data['publish_date'] = pd.to_datetime(combined_data['publish_date'])

# Calculate the total count of headlines for each country and interval
combined_data['Total'] = combined_data['Positive'] + combined_data['Negative']

# Calculate the percentage of positive headlines for each country and interval
combined_data['Positive Percentage'] = (
    combined_data['Positive'] / combined_data['Total']) * 100

# Calculate y-axis values based on sentiment percentage
combined_data['Sentiment'] = combined_data['Positive Percentage'].apply(
    lambda x: x - 100 if x <= 50 else x - 50)

# Plotting the combined graph
fig, ax = plt.subplots(figsize=(12, 8))

for country_name, country_data in combined_data.groupby('Country'):
    ax.plot(country_data['publish_date'],
            country_data['Sentiment'], label=country_name)

ax.set_ylabel('Sentiment Score')
ax.set_xlabel('Year')
ax.set_title('News Headline Sentiment Over Time')
ax.set_ylim(-100, 100)  # Set y-axis limits to -100 to 100

# Set x-axis labels for every year
years = pd.to_datetime(combined_data['publish_date']).dt.year.unique()
plt.xticks(ticks=pd.to_datetime(years, format='%Y'), labels=years, rotation=45)

# Add horizontal lines at 0, 50, and -50 for reference
ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
ax.axhline(y=50, color='gray', linestyle='--', linewidth=0.8)
ax.axhline(y=-50, color='gray', linestyle='--', linewidth=0.8)

# Add legend
ax.legend()

plt.tight_layout()
plt.show()
