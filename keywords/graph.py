import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define the countries and their corresponding CSV files
countries = {
    'Australia': 'AU.csv',
    'Ireland': 'IE.csv',
    'India': 'IN.csv',
    'United States': 'US.csv',
    'United Kingdom': 'UK.csv'
}

# Create a subplot for the word clouds with 2 rows and 3 columns
fig, axes = plt.subplots(2, 3, figsize=(12, 8))  # Adjust the figure size as needed

# Flatten the 2D array of subplots into a 1D array
axes = axes.ravel()

# Center the top two subplots
fig.subplots_adjust(top=0.85, wspace=0.4)

# Initialize the time interval slider
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])  # Adjust the position and size of the slider
intervals = list(range(60))  # Modify the number of intervals as needed
interval_slider = Slider(ax_slider, 'Intervals', 0, len(intervals) - 1, valinit=0, valstep=1)

# Read all CSV data files for the countries
all_data = {country: pd.read_csv(f'keywords/results/{csv_file}') for country, csv_file in countries.items()}

# Create a title for the top keywords and current interval
title = fig.suptitle("", fontsize=16)

# Function to update the word clouds based on the selected interval
def update(val):
    selected_interval = int(interval_slider.val)
    for i, (country, data) in enumerate(all_data.items()):
        # Filter the data for the selected interval
        filtered_data = data[data['Interval'] == data['Interval'].unique()[selected_interval]]

        # Create a word cloud
        wordcloud = WordCloud(width=400, height=200, max_words=50, background_color='white').generate_from_frequencies(
            filtered_data.set_index('Top Keyword')['Count'].to_dict())

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
