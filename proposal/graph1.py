from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import joblib

# Read the data from the CSV file
data = pd.read_csv('data_10_per_day.csv')
df = pd.DataFrame(data, columns=['headline_text'])

# Extract the headlines from the DataFrame
headlines = df['headline_text'].tolist()

# Using a specific model for sentiment analysis
specific_model = pipeline(
    model="siebert/sentiment-roberta-large-english", device="gpu")  # Use GPU

batch_size = 64  # Increased batch size for faster processing
total_headlines = len(headlines)

# Define cache file name
cache_file = "sentiment_cache.joblib"

# Check if cached results exist, otherwise perform sentiment analysis
try:
    sentiments = joblib.load(cache_file)
    print("Cached results loaded.")
except FileNotFoundError:
    sentiments = {'POSITIVE': 0, 'NEGATIVE': 0}

    # Add tqdm progress bar
    with tqdm(total=total_headlines, desc="Analyzing Sentiments", unit="headline", dynamic_ncols=True) as pbar:
        for batch_start in range(0, total_headlines, batch_size):
            batch_headlines = headlines[batch_start:batch_start + batch_size]
            results = specific_model(batch_headlines)

            for result in results:
                label = result['label']
                if label == 'POSITIVE':
                    sentiments['POSITIVE'] += 1
                else:
                    sentiments['NEGATIVE'] += 1

            pbar.update(len(batch_headlines))

    # Cache sentiment analysis results
    joblib.dump(sentiments, cache_file)
    print("Sentiment analysis results cached.")

# Export data to a pandas DataFrame and save it as a CSV file
output_df = pd.DataFrame.from_dict(
    sentiments, orient='index', columns=['Count'])
output_df.index.name = 'Sentiment'
output_file = "sentiment_analysis_results.csv"
output_df.to_csv(output_file)

# Bar graph
labels = sentiments.keys()
values = sentiments.values()

plt.bar(labels, values, color=['green', 'red'])
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.title('Sentiment Analysis Results')
plt.show()
