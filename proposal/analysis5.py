from transformers import pipeline
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from datetime import timedelta
import concurrent.futures

# Read the data from the CSV file
data = pd.read_csv('data_10_per_day_filtered.csv')
df = pd.DataFrame(data, columns=['publish_date', 'headline_text'])

# Extract the publish dates and headlines from the DataFrame
publish_dates = pd.to_datetime(df['publish_date'], format='%Y-%m-%d')
headlines = df['headline_text'].tolist()

# Using a specific model for topic classification
specific_model = pipeline(
    task="text-classification", model="jonaskoenig/topic_classification_04", device=0)  # Use GPU

batch_size = 1  # Increased batch size for faster processing
total_headlines = len(headlines)

topics = defaultdict(lambda: defaultdict(int))

# Function to process a batch of headlines


def process_batch(batch_headlines):
    results = specific_model(batch_headlines)
    batch_topics = defaultdict(int)

    for result in results:
        topic_name = result['label']
        batch_topics[topic_name] += 1

    return batch_topics


# Add tqdm progress bar
with tqdm(total=total_headlines, desc="Analyzing Topics", unit="headline", dynamic_ncols=True) as pbar:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for batch_start in range(0, total_headlines, batch_size):
            batch_headlines = headlines[batch_start:batch_start + batch_size]

            # Process the batch using parallel threads
            batch_topics = executor.submit(
                process_batch, batch_headlines).result()

            for topic_name, topic_count in batch_topics.items():
                sentiment_date = publish_dates[batch_start]
                sentiment_month = sentiment_date.replace(
                    day=1, hour=0, minute=0, second=0, microsecond=0)
                topics[sentiment_month][topic_name] += topic_count

            pbar.update(len(batch_headlines))

# Convert the data into a format suitable for plotting
combined_data = {
    'interval': [],
    'publish_date': []
}

# Add topic counts to the combined_data dictionary
for topic_name in topics[list(topics.keys())[0]]:
    combined_data[topic_name] = []

for sentiment_month, topic_counts in topics.items():
    combined_data['interval'].append(sentiment_month)
    combined_data['publish_date'].append(sentiment_month)

    for topic_name in combined_data.keys():
        if topic_name != 'interval' and topic_name != 'publish_date':
            combined_data[topic_name].append(topic_counts[topic_name])

combined_data = pd.DataFrame(combined_data)
combined_data['interval'] = pd.to_datetime(combined_data['interval'])
combined_data['interval'] = combined_data['interval'].dt.to_period('Q')

# Group and aggregate by quarter-year intervals
grouped_data = combined_data.groupby('interval', as_index=False).agg({
    'publish_date': 'min',
    **{topic_name: 'sum' for topic_name in topics[list(topics.keys())[0]]}
})

# Save the combined topic data to CSV
grouped_data.to_csv('combined_topic_data_grouped.csv', index=False)

print("Results saved to combined_topic_data_grouped.csv")
