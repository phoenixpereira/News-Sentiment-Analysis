from transformers import pipeline
import pandas as pd
from tqdm import tqdm
from collections import defaultdict

# Read the top keywords data from the CSV file
top_keywords_data = pd.read_csv('top_keywords.csv')
top_keywords_df = pd.DataFrame(top_keywords_data, columns=['Top Keyword'])

# Convert the top keywords to a list
top_keywords_list = top_keywords_df['Top Keyword'].tolist()
total_keywords = len(top_keywords_list)

# Using a specific model for emotion analysis
specific_model = pipeline(
    model="j-hartmann/emotion-english-distilroberta-base", device=0)  # Use PyTorch, GPU

emotions_data = []

# List of valid emotion labels
valid_emotions = ['joy', 'surprise',
                  'sadness', 'fear', 'anger', 'disgust', 'neutral']

# Add tqdm progress bar
with tqdm(total=total_keywords, desc="Analyzing Emotions", unit="keyword", dynamic_ncols=True) as pbar:
    for keyword in top_keywords_list:
        results = specific_model(keyword)

        keyword_emotions = defaultdict(int)

        for result in results:
            label = result['label']
            if label in valid_emotions:
                keyword_emotions[label] += 1

        for emotion, count in keyword_emotions.items():
            emotions_data.append({
                'Keyword': keyword,
                'Count': count,
                'Emotion': emotion
            })

        pbar.update(1)

# Create a DataFrame for the emotions data
emotions_df = pd.DataFrame(emotions_data)

# Save the emotions data to a CSV file
emotions_df.to_csv('keyword_emotions.csv', index=False)
print("Keyword emotions data saved to keyword_emotions.csv")
