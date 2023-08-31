import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('pokemon.csv')

attack_values = data['Attack']

plt.figure(figsize=(10, 6))
plt.hist(attack_values, bins=10, edgecolor='black')

plt.ylabel('Frequency')
plt.show()
