from transformers import pipeline
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from datetime import datetime

# Read the data from the CSV file
data = pd.read_csv('filteredDatasets/AU.csv')
df = pd.DataFrame(data, columns=['publish_date', 'headline_text'])

# Extract the publish dates and headlines from the DataFrame
headlines = df['headline_text'].tolist()
publish_dates = df['publish_date'].tolist()

# Using a specific model for keyword extraction
specific_model = pipeline(
    model="yanekyuk/bert-keyword-extractor", device=0)  # Use GPU for faster processing

total_headlines = len(headlines)
keywords = defaultdict(lambda: defaultdict(int))

# Function to extract keywords from a batch of headlines
def extract_keywords(batch_headlines):
    batch_results = specific_model(batch_headlines)

    keywords = []

    for result in batch_results:
        for keyword_info in result:
            keyword = keyword_info.get('word')
            # Filter words with less than 3 letters, exclude hashtags, and exclude "chin"
            if keyword and len(keyword) >= 3 and not keyword.startswith('#') and keyword.lower() != 'chin':
                keywords.append(keyword)

    return keywords

# Determine the time periods (e.g., quarterly intervals)
start_date = datetime.strptime(min(publish_dates), '%Y-%m-%d')
end_date = datetime.strptime(max(publish_dates), '%Y-%m-%d')

# Initialise a list to store keyword data for the CSV file
csv_data = []

# Add tqdm progress bar
with tqdm(total=total_headlines, desc="Extracting Keywords", unit="headline", dynamic_ncols=True) as pbar:
    for i in range(total_headlines):
        batch_headline = headlines[i]
        batch_date = publish_dates[i]

        # Check if the headline is within the current time period (quarter)
        publish_date = datetime.strptime(batch_date, '%Y-%m-%d')

        # Determine the quarter for the current headline
        quarter = f'{publish_date.year}Q{int((publish_date.month - 1) / 3) + 1}'

        # Extract keywords from the headline and update counts for the current time period (quarter)
        keywords_list = extract_keywords([batch_headline])
        for keyword in keywords_list:
            keywords[quarter][keyword] += 1

        pbar.update(1)

# Create intervals based on the available data
available_quarters = sorted(keywords.keys())
for quarter in available_quarters:
    # Sort and extract the top 50 keywords for the current time period (quarter)
    top_keywords = sorted(keywords[quarter], key=keywords[quarter].get, reverse=True)[:50]
    
    # Add keyword data to the CSV data list
    for keyword in top_keywords:
        csv_data.append({
            'Interval': quarter,
            'Top Keyword': keyword,
            'Count': keywords[quarter][keyword]
        })

# Create a DataFrame from the CSV data
csv_df = pd.DataFrame(csv_data)

# Save the CSV data to a file
csv_df.to_csv('keywords/results/AU.csv', index=False)

print("Top keywords data saved")
