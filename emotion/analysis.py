from transformers import pipeline
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from datetime import timedelta

# Read the data from the CSV file
# Change for AU, IE, IN, GB, US
filtered_path = 'filteredDatasets/AU.csv'
data = pd.read_csv(filtered_path)
df = pd.DataFrame(data, columns=['publish_date', 'headline_text'])

# Extract the publish dates and headlines from the DataFrame
publish_dates = pd.to_datetime(df['publish_date'], format='%Y-%m-%d')
headlines = df['headline_text'].tolist()

# Using a specific model for emotion analysis
specific_model = pipeline(
    model="finiteautomata/bertweet-base-emotion-analysis", device=0) # Use device 0 for GPU

batch_size = 64  # Increased batch size for faster processing
total_headlines = len(headlines)

emotions = defaultdict(lambda: defaultdict(int))

# List of valid emotion labels
valid_emotions = ['joy', 'others', 'surprise',
                  'sadness', 'fear', 'anger', 'disgust']

# Add tqdm progress bar
with tqdm(total=total_headlines, desc="Analysing Emotions", unit="headline", dynamic_ncols=True) as pbar:
    for batch_start in range(0, total_headlines):
        batch_headline = headlines[batch_start]
        sentiment_date = publish_dates[batch_start]
        sentiment_month = sentiment_date.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)
        results = specific_model(batch_headline)

        for result in results:
            label = result['label']
            if label in valid_emotions:
                emotions[sentiment_month][label] += 1

        pbar.update(1)

# Convert the data into a format suitable for plotting
combined_data = {
    'interval': [],
    'publish_date': []
}

# Add emotion counts to the combined_data dictionary
for emotion in valid_emotions:
    combined_data[emotion] = []

for sentiment_month, emotion_counts in emotions.items():
    combined_data['interval'].append(sentiment_month)

    for emotion in valid_emotions:
        combined_data[emotion].append(emotion_counts[emotion])

combined_data = pd.DataFrame(combined_data)
combined_data['interval'] = pd.to_datetime(combined_data['interval'])
combined_data['interval'] = combined_data['interval'].dt.to_period('Q')

# Group and aggregate by 3-month intervals
grouped_data = combined_data.groupby('interval', as_index=False).agg({
    'joy': 'sum',
    'others': 'sum',
    'surprise': 'sum',
    'sadness': 'sum',
    'fear': 'sum',
    'anger': 'sum',
    'disgust': 'sum'
})

# Save the combined emotion data to CSV
# Change for AU, IE, IN, GB, US
grouped_data.to_csv('results/AU.csv', index=False)
