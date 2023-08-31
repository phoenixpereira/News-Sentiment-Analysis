import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('winemag-data_first150k.csv')

filtered_data = data[(data['price'] < 100) & (data['country'] == 'France')]

plt.figure(figsize=(10, 6))
plt.hexbin(filtered_data['price'],
           filtered_data['points'], gridsize=20, cmap='Greens')

plt.ylabel('Points')
plt.colorbar(label='Frequency')
plt.show()
