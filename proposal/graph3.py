import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the combined emotion data from the CSV
combined_data = pd.read_csv('combined_emotion_data_grouped.csv')
combined_data['publish_date'] = pd.to_datetime(combined_data['publish_date'])

# List of valid emotion labels
valid_emotions = ['joy', 'surprise',
                  'sadness', 'fear', 'anger', 'disgust', 'neutral']

# Plotting the stacked area chart with colored areas
plt.figure(figsize=(10, 6))

# Calculate the center position for each data point
x_values = np.arange(len(combined_data))

# Initialize a variable to keep track of the y-values for stacking
y_values = np.zeros(len(combined_data))

# Plot the stacked area chart with colored areas
for i, emotion in enumerate(valid_emotions):
    plt.fill_between(x_values, y_values, y_values +
                     combined_data[emotion], color=f'C{i}', alpha=0.6, label=emotion.capitalize())
    y_values += combined_data[emotion]

plt.xlabel('Date')
plt.ylabel('Count')
plt.title('Headline Emotion Analysis Over Time')

# Define fixed x-axis intervals (e.g., every 4 quarters)
fixed_x_intervals = np.arange(0, len(combined_data), step=4)

plt.xticks(ticks=fixed_x_intervals,
           labels=combined_data['publish_date'][fixed_x_intervals].dt.strftime('%Y'), rotation=45)

# Move the legend to the upper left corner and adjust its position
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Emotion")

plt.tight_layout()

plt.show()
