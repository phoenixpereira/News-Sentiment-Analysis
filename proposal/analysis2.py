from transformers import pipeline
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from datetime import timedelta

# Read the data from the CSV file
data = pd.read_csv('data_10_per_day_filtered.csv')
df = pd.DataFrame(data, columns=['publish_date', 'headline_text'])

# Extract the publish dates and headlines from the DataFrame
publish_dates = pd.to_datetime(df['publish_date'], format='%Y-%m-%d')
headlines = df['headline_text'].tolist()

# Using a specific model for sentiment analysis
specific_model = pipeline(
    model="siebert/sentiment-roberta-large-english", device=0)  # Use device 0 for GPU

batch_size = 64  # Increased batch size for faster processing
total_headlines = len(headlines)

sentiments = defaultdict(lambda: defaultdict(int))

# Add tqdm progress bar
with tqdm(total=total_headlines, desc="Analysing Sentiments", unit="headline", dynamic_ncols=True) as pbar:
    for batch_start in range(0, total_headlines):
        batch_headline = headlines[batch_start]
        sentiment_date = publish_dates[batch_start]
        sentiment_month = sentiment_date.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)
        result = specific_model(batch_headline)
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
grouped_data.to_csv('combined_sentiment_data_grouped.csv', index=False)
