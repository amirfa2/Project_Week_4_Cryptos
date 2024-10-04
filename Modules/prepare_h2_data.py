import pandas as pd

def prepare_h2_data():
    # Load main merged dataset:
    df = pd.read_csv('merged_df.csv')
    df['date'] = pd.to_datetime(df['date'])

    # Ensure we have correct data structure:
    df = df[df['symbol'].isin(['BTC', 'ETH', 'DOGE'])]

    # Create 'year_month' for grouping:
    df['year_month'] = df['date'].dt.to_period('M')

    # Calculate monthly total volumes:
    monthly_volume = df.groupby(['year_month', 'symbol'])['volume'].sum().unstack()

    # Calculate percentage change from month to month:
    monthly_avg = monthly_volume.pct_change().multiply(100).reset_index()

    # Rename columns to follow convention:
    monthly_avg.columns = ['year_month', 'btc_volume_change', 'eth_volume_change', 'doge_volume_change']

    # Save CSV for visualization:
    monthly_avg.to_csv('CSVs/merged_df_for_h2.csv', index=False)
    print("Hypothesis 2 data (monthly volume change) saved as 'merged_df_for_h2.csv' in CSVs folder.")

if __name__ == "__main__":
    prepare_h2_data()