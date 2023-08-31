import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the combined topic data from the CSV
combined_data = pd.read_csv('combined_topic2_data_grouped.csv')
combined_data['publish_date'] = pd.to_datetime(combined_data['publish_date'])

# List of topic names (extracted from column names)
# Exclude interval and publish_date columns
topic_labels = combined_data.columns[2:]

# Plotting the line graph for topics
plt.figure(figsize=(10, 6))

# Calculate the center position for each data point
x_values = np.arange(len(combined_data))

# Plot each topic as a line
for i, topic in enumerate(topic_labels):
    plt.plot(x_values, combined_data[topic], label=topic, linewidth=2)

# Define fixed x-axis intervals (e.g., every 4 quarters)
fixed_x_intervals = np.arange(0, len(combined_data), step=4)

# Adjust the interval as needed
plt.xticks(ticks=fixed_x_intervals,
           labels=combined_data['publish_date'][fixed_x_intervals].dt.strftime('%Y'), rotation=45)

plt.xlabel('Date')
plt.ylabel('Score')
plt.title('Headline Topic Analysis Score Over Time')

# Move the legend to the upper left corner and adjust its position
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()

plt.show()
