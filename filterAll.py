import pandas as pd
import os

# Create the output directory if it doesn't exist
output_directory = 'filteredDatasets'
os.makedirs(output_directory, exist_ok=True)

# List of input files
input_files = ['AU.csv', 'IN.csv', 'IE.csv', 'GB.csv', 'US.csv']

for input_file in input_files:
    input_path = os.path.join('rawDatasets', input_file)
    output_path = os.path.join(output_directory, input_file)

    # Read the input CSV file using pandas
    df = pd.read_csv(input_path)

    # Remove extra spacing within headlines
    df['headline_text'] = df['headline_text'].str.replace(r'\s+', ' ', regex=True).str.strip()

    # Truncate headlines to 128 characters
    df['headline_text'] = df['headline_text'].str.slice(stop=128)

    # Convert publish_date to datetime
    df['publish_date'] = pd.to_datetime(df['publish_date'], format='%Y%m%d')

    # Filter conditions
    start_date = pd.Timestamp('2007-01-01')
    end_date = pd.Timestamp('2021-06-30')
    filtered_df = df[(df['publish_date'] >= start_date) & (df['publish_date'] <= end_date) &
                     (df['headline_text'].str.split().apply(lambda x: len(x) if isinstance(
                         x, list) else 0) > 3) & (~df['headline_text'].str.contains('abc', na=False))]
    filtered_df = filtered_df.groupby(['publish_date']).head(10)

    # Write the filtered dataframe to a new CSV file
    filtered_df[['publish_date', 'headline_text']].to_csv(
        output_path, index=False)

print("Filtering and outputting complete.")
