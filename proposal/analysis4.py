from transformers import pipeline
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
import re

# Read the data from the CSV file
data = pd.read_csv('filtered_data_10_per_day.csv')
df = pd.DataFrame(data, columns=['publish_date', 'headline_text'])

# Extract the publish dates and headlines from the DataFrame
headlines = df['headline_text'].tolist()

# Using a specific model for keyword extraction
specific_model = pipeline(
    model="yanekyuk/bert-keyword-extractor", device=0)  # Use GPU

batch_size = 64  # Increased batch size for faster processing
total_headlines = len(headlines)

keywords = defaultdict(int)

# Add tqdm progress bar
with tqdm(total=total_headlines, desc="Extracting Keywords", unit="headline", dynamic_ncols=True) as pbar:
    for batch_start in range(0, total_headlines):
        batch_headline = headlines[batch_start]
        results = specific_model(batch_headline)

        for result in results:
            keyword = result['word']
            # Filter out hashtags and words with less than 3 letters
            if len(keyword) >= 3 and not keyword.startswith('#'):
                # Check if the keyword appears as a whole word within the headlines
                if any(re.search(rf'\b{re.escape(keyword)}\b', headline, re.IGNORECASE) for headline in headlines):
                    keywords[keyword] += 1

        pbar.update(1)

# Get the top 500 keywords
top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:500]

# Save the top keyword data to a CSV file
top_keywords_data = []

for keyword, count in top_keywords:
    top_keywords_data.append({
        'Top Keyword': keyword,
        'Count': count
    })

top_keywords_df = pd.DataFrame(top_keywords_data)
top_keywords_df.to_csv('top_keywords.csv', index=False)
print("Top keywords data saved to top_keywords.csv")
