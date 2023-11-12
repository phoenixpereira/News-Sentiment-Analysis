# News Sentiment Analysis

This project analyses the evolution of sentiment in news headlines over time, utilising Python and Pandas for data manipulation, and Hugging Face Transformers models for sentiment analysis, emotion analysis, and keyword analysis.

## Data Sources

The dataset comprises of news headlines spanning from 2007 to 2021, sourced from Kaggle:

- **Australia:** [ABC News](https://www.kaggle.com/datasets/therohk/million-headlines)

- **Ireland:** [The Irish Times](https://www.kaggle.com/datasets/therohk/ireland-historical-news)

- **India:** [Times of India](https://www.kaggle.com/datasets/therohk/india-headlines-news-dataset)

- **England:** [Daily Mail](https://www.kaggle.com/datasets/jordankrishnayah/45m-headlines-from-2007-2022-10-largest-sites)

- **United States:** [The New York Times](https://www.kaggle.com/datasets/jordankrishnayah/45m-headlines-from-2007-2022-10-largest-sites)

## Usage

### Step 1 - Filtering Data
1. Run `python filterGBandUS.py` to filter data specific to the United Kingdom and the United States.
2. Run `python filterAll.py` to filter data in the whole dataset.

### Step 2 - Sentiment Analysis
1. Run `python sentiment/analysis.py` for sentiment analysis.
2. Run `python sentiment/graph.py` to generate visualisations based on the sentiment data.
   
![Sentiment](https://github.com/phoenixpereira/News-Sentiment-Evolution/assets/47909638/85fd44fa-1299-438c-a19d-bf4da9c1e235)

### Step 3 - Emotion Analysis
1. Run `python emotion/analysis.py` for emotion analysis.
2. Run `python emotion/graph.py` to visualise the emotion analysis results.
   
![Emotion](https://github.com/phoenixpereira/News-Sentiment-Evolution/assets/47909638/b787d5c4-2b2e-493b-9c06-1190b85b5890)

### Step 4 - Keywords Analysis
1. Run `python keywords/analysis.py`, `python keywords/analysis2.py`, and `python keywords/combine.py` for keyword analysis.
2. Run `python keywords/graph.py` to visualise the keyword analysis results.
   
![Keywords](https://github.com/phoenixpereira/News-Sentiment-Evolution/assets/47909638/9a84487a-2880-4df1-89d6-0e33bf8ce959)
