import pandas as pd
import os

def merge_and_clean():
    # Define the paths for CSV files:
    base_path = 'CSVs'
    btc_path = os.path.join(base_path, 'coin_Bitcoin.csv')
    eth_path = os.path.join(base_path, 'coin_Ethereum.csv')
    doge_path = os.path.join(base_path, 'coin_Dogecoin.csv')

    # Load datasets:
    try:
        btc_data = pd.read_csv(btc_path)
        eth_data = pd.read_csv(eth_path)
        doge_data = pd.read_csv(doge_path)
    except FileNotFoundError as e:
        print("Error:", e)
        return None

    # Clean data: Drop missing values and convert 'Date' to datetime:
    datasets = [btc_data, eth_data, doge_data]
    for data in datasets:
        data.dropna(inplace=True)
        data['Date'] = pd.to_datetime(data['Date'])

    # Concatenate datasets:
    merged_df = pd.concat(datasets, ignore_index=True)

    # Standardize column names to lowercase:
    merged_df.columns = merged_df.columns.str.lower()

    # Ensure correct columns for analysis:
    merged_df = merged_df[['name', 'symbol', 'date', 'high', 'low', 'open', 'close', 'volume', 'marketcap']]
    merged_df.dropna(inplace=True)

    # Save cleaned dataframe to the root directory:
    merged_df.to_csv('merged_df.csv', index=False)
    print("Data Preparation Complete. Cleaned data saved as 'merged_df.csv' in the root directory.")

    return merged_df

if __name__ == "__main__":
    merge_and_clean()