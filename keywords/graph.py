import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # Import Vader

# Define the countries and their corresponding CSV files
countries = {
    'Australia': 'AU.csv',
    'Ireland': 'IE.csv',
    'India': 'IN.csv',
    'United States': 'US.csv',
    'England': 'GB.csv'
}

# Create a color mapping for sentiment (you can adjust these colors)
sentiment_colors = {
    'positive': 'green',
    'neutral': 'gray',
    'negative': 'red'
}

# Create a subplot for the word clouds with 2 rows and 3 columns
fig, axes = plt.subplots(2, 3, figsize=(10, 6))  # Adjust the figure size as needed

# Flatten the 2D array of subplots into a 1D array
axes = axes.ravel()

# Center the top two subplots
fig.subplots_adjust(top=0.85, wspace=0.4)

# Initialise the time interval slider
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])  # Adjust the position and size of the slider
intervals = list(range(58))  # Modify the number of intervals as needed
interval_slider = Slider(ax_slider, 'Interval', 0, len(intervals) - 1, valinit=0, valstep=1)

# Create a play/pause button to the left of the slider
ax_play_pause = plt.axes([0.05, 0.02, 0.075, 0.03])  # Adjust the position and size of the button
play_pause_button = Button(ax_play_pause, 'Play')

# Read all CSV data files for the countries
all_data = {country: pd.read_csv(f'keywords/results/{csv_file}') for country, csv_file in countries.items()}

# Create a title for the top keywords and current interval
title = fig.suptitle("", fontsize=16)

# Variables for animation control
animation_running = False

# Initialise Vader sentiment analyser
analyzer = SentimentIntensityAnalyzer()

# Function to analyze sentiment and assign colors to words using Vader
def analyze_sentiment_and_color(text):
    sentiment = analyzer.polarity_scores(text)
    compound_score = sentiment['compound']
    
    if compound_score > 0:
        return sentiment_colors['positive']
    elif compound_score < 0:
        return sentiment_colors['negative']
    else:
        return sentiment_colors['neutral']

# Function to update the word clouds based on the selected interval
def update(val):
    selected_interval = int(interval_slider.val)
    for i, (country, data) in enumerate(all_data.items()):
        # Filter the data for the selected interval
        filtered_data = data[data['Interval'] == data['Interval'].unique()[selected_interval]]

        # Analyse sentiment and assign colors to words
        filtered_data_copy = filtered_data.copy()
        filtered_data_copy['Color'] = filtered_data['Top Keyword'].apply(analyze_sentiment_and_color)

        # Create a word cloud with colored words
        wordcloud = WordCloud(
            width=400, height=200, max_words=50, background_color='white',
            color_func=lambda word, font_size, position, orientation, random_state=None, **kwargs: filtered_data_copy.set_index('Top Keyword')['Color'].get(word, 'black')
        ).generate_from_frequencies(filtered_data_copy.set_index('Top Keyword')['Count'].to_dict())


        # Update the word cloud on the corresponding subplot
        axes[i].clear()
        axes[i].imshow(wordcloud, interpolation='bilinear')
        axes[i].set_title(country)
        axes[i].axis('off')

    # Update the title to show the current interval and top keywords
    current_interval = filtered_data['Interval'].values[0]
    title.set_text(f"Top 25 Keywords - {current_interval}")
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

# Initialise the word clouds with the first interval
update(0)

# Hide any remaining empty subplots
for i in range(len(countries), len(axes)):
    axes[i].axis('off')

# Create an animation for intervals
ani = FuncAnimation(fig, animate_intervals, frames=len(intervals), repeat=True, interval=1000)

# Display the plot
plt.tight_layout()
plt.show()