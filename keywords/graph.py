import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation

# Define the countries and their corresponding CSV files
countries = {
    'Australia': 'AU.csv',
    'Ireland': 'IE.csv',
    'India': 'IN.csv',
    'United States': 'US.csv',
    'United Kingdom': 'UK.csv'
}

# Create a numerical mapping for sentiment
sentiment_values = {
    'positive': 2,
    'neutral': 1,
    'negative': 0
}

# Create a color mapping for sentiment
sentiment_colors = {
    'positive': 'green',
    'neutral': 'gray',
    'negative': 'red'
}

# Create a subplot for the word clouds with 2 rows and 3 columns
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.ravel()
fig.subplots_adjust(top=0.85, wspace=0.4)

# Initialize the time interval slider
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
intervals = list(range(58))
interval_slider = Slider(ax_slider, 'Interval', 0, len(intervals) - 1, valinit=0, valstep=1)

# Create a play/pause button to the left of the slider
ax_play_pause = plt.axes([0.05, 0.02, 0.085, 0.03])
play_pause_button = Button(ax_play_pause, 'Play')

# Read all CSV data files for the countries
all_data = {country: pd.read_csv(f'keywords/results/{csv_file}') for country, csv_file in countries.items()}

# Create a title for the top keywords and current interval
title = fig.suptitle("", fontsize=16)

# Variables for animation control
animation_running = False

# Initialize an empty word cloud
empty_wordcloud = WordCloud(width=400, height=200, max_words=50, background_color='white')

# Function to retrieve sentiment for a given country and keyword (replace with your data retrieval logic)
def retrieve_sentiment_for_keyword(country, keyword):
    # Implement your logic to retrieve sentiment for each keyword based on your data source
    # Return 'positive', 'neutral', or 'negative' for each keyword
    # For demonstration purposes, we'll return 'neutral' for all keywords
    return 'neutral'

# Function to update the word clouds based on the selected interval
def update(val):
    selected_interval = int(interval_slider.val)
    for i, (country, data) in enumerate(all_data.items()):
        # Filter the data for the selected interval
        filtered_data = data[data['Interval'] == data['Interval'].unique()[selected_interval]]

        # Create an empty word cloud
        wordcloud = empty_wordcloud

        for _, row in filtered_data.iterrows():
            keyword = row['Top Keyword']
            # Sentiment should be retrieved from your data source using retrieve_sentiment_for_keyword
            sentiment = retrieve_sentiment_for_keyword(country, keyword)

            # Set value based on sentiment
            value = sentiment_values[sentiment]

            # Add the keyword with its value to the word cloud
            wordcloud.generate_from_frequencies({keyword: value})

            # Convert the value to color
            color = sentiment_colors[sentiment]

        # Update the word cloud on the corresponding subplot
        axes[i].clear()
        axes[i].imshow(wordcloud, interpolation='bilinear')
        axes[i].set_title(country)
        axes[i].axis('off')

    # Update the title to show the current interval and top keywords
    current_interval = filtered_data['Interval'].values[0]
    title.set_text(f"Top 25 Keywords - {current_interval}")

    plt.tight_layout()
    fig.canvas.draw_idle()

# Function to handle play/pause button click event
def play_pause(event):
    global animation_running
    if play_pause_button.label.get_text() == 'Play':
        play_pause_button.label.set_text('Pause')
        animation_running = True
        ani.event_source.start()
    else:
        play_pause_button.label.set_text('Play')
        animation_running = False
        ani.event_source.stop()

play_pause_button.on_clicked(play_pause)

# Function to animate intervals
def animate_intervals(i):
    if not animation_running:
        return
    current_interval = int(interval_slider.val)
    next_interval = (current_interval + 1) % len(intervals)
    interval_slider.set_val(next_interval)
    update(next_interval)

# Attach the update function to the slider
interval_slider.on_changed(update)

# Initialize the word clouds with the first interval
update(0)

# Hide any remaining empty subplots
for i in range(len(countries), len(axes)):
    axes[i].axis('off')

# Display the plot
plt.tight_layout()
plt.show()
