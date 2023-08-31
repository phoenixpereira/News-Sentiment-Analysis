import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the combined sentiment data from the CSV
combined_data = pd.read_csv('combined_sentiment_data_grouped.csv')
combined_data['publish_date'] = pd.to_datetime(combined_data['publish_date'])

# Plotting the plain line graph
plt.figure(figsize=(10, 6))
plt.plot(combined_data['publish_date'], combined_data['Positive'],
         label='Positive', color='green', linewidth=2)
plt.plot(combined_data['publish_date'], combined_data['Negative'],
         label='Negative', color='red', linewidth=2)
plt.xlabel('Date')
plt.ylabel('Count')
plt.title('Headline Sentiment Analysis Over Time')
plt.legend()

# Set x-axis labels for every year
years = pd.to_datetime(combined_data['publish_date']).dt.year.unique()
plt.xticks(ticks=pd.to_datetime(years, format='%Y'), labels=years, rotation=45)

plt.tight_layout()

plt.show()
