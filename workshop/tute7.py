import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('CompleteDataset.csv')

# Filter data based on the criteria (overall value in [80, 85))
filtered_data = data[(data['Overall'] >= 80) & (data['Overall'] < 85)]

# Define x, y, and circle size variables
x = filtered_data['Value']
y = filtered_data['Overall']
circle_size = filtered_data['Aggression']

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(x, y, s=circle_size, alpha=0.7, cmap='viridis')

# Add labels and title
plt.xlabel('Value')
plt.ylabel('Overall')
plt.title('Scatter Plot of FIFA Soccer Data')
plt.colorbar(label='Aggression')

# Show the plot
plt.show()
