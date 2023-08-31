import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('pokemon.csv')

pokemon_stats_by_generation = data.groupby(
    'Generation')[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].mean()

plt.figure(figsize=(10, 6))

pokemon_stats_by_generation.plot(kind='area', stacked=True, alpha=0.7)

plt.xlabel('Generation')
plt.title('Pokemon Stats by Generation')
plt.legend(loc='lower right')
plt.show()
