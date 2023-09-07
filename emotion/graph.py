import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation

# Define the countries and their full names
countries = {
    'AU': 'Australia',
    'IE': 'Ireland',
    'IN': 'India',
    'GB': 'England',
    'US': 'United States'
}

# Read the csv files into a dictionary of dataframes
dfs = {}
for country in countries:
    filename = f'emotion/results/{country}.csv'
    dfs[country] = pd.read_csv(filename)

# Map the country codes to their full names
for country in dfs:
    dfs[country]['Country'] = countries[country]

# Concatenate the dataframes into a single dataframe
df = pd.concat(dfs.values())

# Set the index to the interval column
df.set_index('interval', inplace=True)

# Define the colors for each emotion
colors = {
    "joy": "pink",
    "surprise": "yellow",
    "neutral": "orange",
    "disgust": "green",
    "sadness": "blue",
    "fear": "purple",
    "anger": "red"
}

# Define the figure and axes with a larger figure size
fig, ax = plt.subplots(figsize=(12, 6))

# Define the bar width
width = 0.8

# Define the y positions for each bar
y_positions = list(range(len(countries)))

# Plot each emotion for each country initially
stacked_heights = [0] * len(countries)
legend_artists = []

for emotion in colors:
    for i, country in enumerate(countries):
        data = df[df['Country'] == countries[country]][emotion]
        ax.barh(y_positions[i], data.iloc[0], height=width, color=colors[emotion], left=stacked_heights[i], label=emotion)
        stacked_heights[i] += data.iloc[0]
    legend_artists.append(mpatches.Patch(color=colors[emotion], label=emotion))

# Add a title with the current interval
current_interval = df.index.unique()[0]
ax.set_title(f'Headline Emotion Analysis - {current_interval}')

# Invert the y-axis to have the top country at the top
ax.invert_yaxis()

# Initialise labels and legend
ax.set_yticks(y_positions)
y_labels = ax.set_yticklabels([countries[country] for country in countries.keys()])
legend = ax.legend(handles=legend_artists, loc='center left', bbox_to_anchor=(1, 0.5))
x_axis = ax.set_xlabel('Emotion Count')
y_axis = ax.set_ylabel('Country')

# Add a slider to change the selected time for the data
slider_ax = fig.add_axes([0.15, 0.001, 0.7, 0.03])  # Adjust the vertical position here
slider = Slider(slider_ax, 'Time', 0, len(df.index.unique()) - 1, valinit=0, valstep=1)

# Play/pause button
play_pause_ax = fig.add_axes([0.01, 0.05, 0.1, 0.04])  # Adjust the horizontal and vertical position here
play_pause_button = Button(play_pause_ax, 'Play')

# Flag to control animation
animation_playing = False
current_index = 0  # Track the current index of the slider

# Function to update the plot when the slider is moved
def update(val):
    global current_index
    index = int(slider.val)
    
    if index != current_index:
        current_index = index
        ax.clear()
        stacked_heights = [0] * len(countries)
        legend_artists = []

        for emotion in colors:
            for i, country in enumerate(countries):
                data = df[df['Country'] == countries[country]][emotion]
                ax.barh(y_positions[i], data.iloc[index], height=width, color=colors[emotion], left=stacked_heights[i], label=emotion)
                stacked_heights[i] += data.iloc[index]
            legend_artists.append(mpatches.Patch(color=colors[emotion], label=emotion))

        current_interval = df.index.unique()[index]
        ax.set_title(f'Headline Emotion Analysis - {current_interval}')
        # Set the x-axis label
        ax.set_xlabel('Emotion Count')

        # Set the y-axis label
        ax.set_ylabel('Country')
        
        # Restore y-axis labels and legend
        ax.set_yticks(y_positions)
        y_labels = ax.set_yticklabels([countries[country] for country in countries.keys()])
        legend = ax.legend(handles=legend_artists, loc='center left', bbox_to_anchor=(1, 0.5))
        x_axis = ax.set_xlabel('Emotion Count')
        y_axis = ax.set_ylabel('Country') 

        if not animation_playing:
            slider.set_val(index)

slider.on_changed(update)

# Animation function
def animate(i):
    global animation_playing
    if not animation_playing:
        return
    
    index = i % len(df.index.unique())
    ax.clear()
    stacked_heights = [0] * len(countries)
    legend_artists = []

    for emotion in colors:
        for i, country in enumerate(countries):
            data = df[df['Country'] == countries[country]][emotion]
            ax.barh(y_positions[i], data.iloc[index], height=width, color=colors[emotion], left=stacked_heights[i], label=emotion)
            stacked_heights[i] += data.iloc[index]
        legend_artists.append(mpatches.Patch(color=colors[emotion], label=emotion))

    current_interval = df.index.unique()[index]
    ax.set_title(f'Headline Emotion Analysis - {current_interval}')
    
    # Restore y-axis labels and legend
    ax.set_yticks(y_positions)
    y_labels = ax.set_yticklabels([countries[country] for country in countries.keys()])
    legend = ax.legend(handles=legend_artists, loc='center left', bbox_to_anchor=(1, 0.5))
    x_axis = ax.set_xlabel('Emotion Count')
    y_axis = ax.set_ylabel('Country') 

    slider.set_val(index)

# Play/pause button click event
def play_pause(event):
    global animation_playing, current_index
    if play_pause_button.label.get_text() == 'Play':
        play_pause_button.label.set_text('Pause')
        animation_playing = True
        current_index = 0
        ani.event_source.start()
    else:
        play_pause_button.label.set_text('Play')
        animation_playing = False
        ani.event_source.stop()

play_pause_button.on_clicked(play_pause)

ani = FuncAnimation(fig, animate, frames=len(df.index.unique()) * 2, interval=1000, repeat=True)

# Set the slider labels to the interval values (e.g., 2007Q1, 2007Q2, etc.)
slider_labels = df.index.unique().tolist()
slider_ax.set_xticks(range(len(slider_labels)))
slider_ax.set_xticklabels(slider_labels, rotation=45)

# Adjust the position of the graph to the right
plt.subplots_adjust(right=0.85)

plt.show()
