import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('winemag-data_first150k.csv')

filtered_data = data[data['price'] < 100]

plt.figure(figsize=(10, 6))
plt.hist(filtered_data['price'], bins=10, edgecolor='black')

plt.ylabel('Frequency')
plt.show()
