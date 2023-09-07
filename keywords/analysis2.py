import pandas as pd
from tqdm import tqdm
from transformers import pipeline
from collections import defaultdict

# Define the countries and their corresponding CSV files
countries = {
    'Australia': 'AU.csv',
    'Ireland': 'IE.csv',
    'India': 'IN.csv',
    'United States': 'US.csv',
    'England': 'GB.csv'
}

# Using a specific model for sentiment analysis
specific_model = pipeline(
    model="cardiffnlp/twitter-roberta-base-sentiment-latest", device=0)  # Use device 0 for GPU

# Initialise a list to store sentiment data
sentiment_data = []

# Loop through each country's CSV file
for country, csv_file in countries.items():
    data = pd.read_csv(f'keywords/results/{csv_file}')
    total_headlines = len(data)

    # Add tqdm progress bar
    with tqdm(total=total_headlines, desc=f"Analysing Keyword Sentiments for {country}", unit="keywords", dynamic_ncols=True) as pbar:
        for idx in range(total_headlines):
            row = data.iloc[idx]
            keyword = row['Top Keyword']

            # Perform sentiment analysis
            result = specific_model(keyword)
            label = result[0]['label']

            # Append sentiment data to the list
            sentiment_data.append({
                'country': country,
                'keyword': keyword,
                'sentiment': label
            })

            pbar.update(1)

# Create a DataFrame for sentiment data
sentiments_df = pd.DataFrame(sentiment_data)

# Save the sentiment data to a CSV file
sentiments_df.to_csv('keywords/results/sentiments.csv', index=False)
