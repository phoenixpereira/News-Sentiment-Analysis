import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the combined topic data from the CSV
combined_data = pd.read_csv('combined_topic_data_grouped.csv')
combined_data['publish_date'] = pd.to_datetime(combined_data['publish_date'])

# List of valid topic names (make sure these match the column names in your CSV)
topic_labels = ['Education & Reference', 'Computers & Internet', 'Sports',
                'Business & Finance', 'Entertainment & Music', 'Health', 'Politics & Government', 'Family & Relationships']

# Plotting the stacked area chart with colored areas
plt.figure(figsize=(10, 6))

# Calculate the center position for each data point
x_values = np.arange(len(combined_data))

# Initialize a variable to keep track of the y-values for stacking
y_values = np.zeros(len(combined_data))

# Plot the stacked area chart with colored areas
for i, topic in enumerate(topic_labels):
    plt.fill_between(x_values, y_values, y_values +
                     combined_data[topic], color=f'C{i}', alpha=0.6)
    y_values += combined_data[topic]

# Define fixed x-axis intervals (e.g., every 4 quarters)
fixed_x_intervals = np.arange(0, len(combined_data), step=4)

# Adjust the interval as needed
plt.xticks(ticks=fixed_x_intervals, labels=combined_data['publish_date'][fixed_x_intervals].dt.strftime(
    '%Y'), rotation=45)  # Show only the year

plt.xlabel('Date')
plt.ylabel('Count')
plt.title('Headline Topic Analysis Count Over Time')

# Move the legend to the upper left corner and adjust its position
plt.legend(topic_labels, loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()

plt.show()
