import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the top keywords data from the CSV file
top_keywords_df = pd.read_csv('keywords/results/AU.csv')

# Create a WordCloud
wordcloud = WordCloud(width=800, height=400,
                      background_color='white', colormap='viridis', max_words=500)

# Generate the word cloud using top keywords
wordcloud.generate_from_frequencies(
    dict(zip(top_keywords_df['Top Keyword'], top_keywords_df['Count'])))

# Display the word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
