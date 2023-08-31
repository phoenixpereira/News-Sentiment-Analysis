import pandas as pd
from transformers import pipeline
from tqdm import tqdm
from collections import defaultdict
import concurrent.futures

# Read the data from the CSV file
data = pd.read_csv('data_1_per_day.csv')
df = pd.DataFrame(data, columns=['publish_date', 'headline_text'])

# Extract the publish dates and headlines from the DataFrame
publish_dates = pd.to_datetime(df['publish_date'], format='%Y-%m-%d')
headlines = df['headline_text'].tolist()

# Using a specific model for topic classification
specific_model = pipeline(
    task="text-classification", model="ebrigham/EYY-Topic-Classification", device=0)  # Use GPU

batch_size = 1  # Increased batch size for faster processing
total_headlines = len(headlines)

topics = defaultdict(lambda: defaultdict(int))

# Function to process a batch of headlines


def process_batch(batch_headlines):
    results = specific_model(batch_headlines)
    batch_topics = defaultdict(int)

    for result in results:
        topic_name = result['label']
        if topic_name not in batch_topics:
            batch_topics[topic_name] = 0
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

            for topic_name, count in batch_topics.items():
                sentiment_date = publish_dates[batch_start]
                sentiment_month = sentiment_date.replace(
                    day=1, hour=0, minute=0, second=0, microsecond=0)
                topics[sentiment_month][topic_name] += count

            pbar.update(len(batch_headlines))
# Convert the data into a format suitable for CSV
combined_data = defaultdict(list)

all_topic_names = set()
skip_next_topic = False

for sentiment_month, topic_counts in topics.items():
    topic_names = list(topic_counts.keys())
    for i, topic_name in enumerate(topic_names):
        if skip_next_topic:
            skip_next_topic = False
            continue
        if i + 1 < len(topic_names):
            all_topic_names.add(topic_names[i + 1])
            skip_next_topic = True
            continue

        all_topic_names.add(topic_name)
        combined_data[topic_name].append(topic_counts.get(topic_name, 0))

for topic_name in all_topic_names:
    combined_data[topic_name] = []

for sentiment_month, topic_counts in topics.items():
    for topic_name in all_topic_names:
        combined_data[topic_name].append(topic_counts.get(topic_name, 0))

combined_data['interval'] = pd.to_datetime(list(topics.keys()))
combined_data['interval'] = combined_data['interval'].to_period('Q')

# Group and aggregate by quarter-year intervals
grouped_data = pd.DataFrame(combined_data)

# Save the combined topic data to CSV
grouped_data.to_csv('combined_topic2_data_grouped.csv', index=False)

print("Results saved to combined_topic2_data_grouped.csv")
