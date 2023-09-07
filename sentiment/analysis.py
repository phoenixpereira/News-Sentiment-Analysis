from transformers import pipeline
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from datetime import timedelta

# Read CSV file
# Change for AU, IE, IN, GB, US
filtered_path = 'filteredDatasets/australia.csv'
data = pd.read_csv(filtered_path)
headlines_data = []
headlines_data.append(data)

headlines_df = pd.concat(headlines_data, ignore_index=True)

# Using a specific model for sentiment analysis
specific_model = pipeline(
    model="siebert/sentiment-roberta-large-english", device=0)  # Use device 0 for GPU

total_headlines = len(headlines_df)

sentiments = defaultdict(lambda: defaultdict(int))

# Add tqdm progress bar
with tqdm(total=total_headlines, desc="Analysing Sentiments", unit="headline", dynamic_ncols=True) as pbar:
    for idx in range(total_headlines):
        row = headlines_df.iloc[idx]
        headline = row['headline_text']
        sentiment_date = pd.to_datetime(row['publish_date'], format='%Y-%m-%d')
        sentiment_month = sentiment_date.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)
        result = specific_model(headline)
        label = result[0]['label']

        if label == 'POSITIVE':
            sentiments[sentiment_month]['POSITIVE'] += 1
        elif label == 'NEGATIVE':
            sentiments[sentiment_month]['NEGATIVE'] += 1

        pbar.update(1)

# Convert the data into a format suitable for plotting
combined_data = {
    'interval': [],
    'publish_date': [],
    'Positive': [],
    'Negative': []
}

for sentiment_month, sentiment_counts in sentiments.items():
    combined_data['interval'].append(sentiment_month)
    combined_data['publish_date'].append(sentiment_month)
    combined_data['Positive'].append(sentiment_counts['POSITIVE'])
    combined_data['Negative'].append(sentiment_counts['NEGATIVE'])

combined_data = pd.DataFrame(combined_data)
combined_data['interval'] = pd.to_datetime(combined_data['interval'])
combined_data['interval'] = combined_data['interval'].dt.to_period('Q')

# Group and aggregate by 3-month intervals
grouped_data = combined_data.groupby('interval', as_index=False).agg({
    'publish_date': 'min',
    'Positive': 'sum',
    'Negative': 'sum'
})

# Save the combined sentiment data to CSV
# Change for AU, IE, IN, GB, US
grouped_data.to_csv('results/AU.csv', index=False)
