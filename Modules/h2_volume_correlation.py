import pandas as pd
import matplotlib.pyplot as plt

# Load and preprocess CSV data:
df = pd.read_csv('merged_df.csv')
df['date'] = pd.to_datetime(df['date'])

# Ensure we have the data for all relevant symbols:
df = df[df['symbol'].isin(['BTC', 'ETH', 'DOGE'])]

# Create 'year_month' for grouping:
df['year_month'] = df['date'].dt.to_period('M')

# Percentage change:
monthly_volume_change = df.groupby(['year_month', 'symbol'])['volume'].sum().unstack().pct_change().multiply(100).reset_index()

# Rename columns to match:
monthly_avg = monthly_volume_change.rename(columns={'BTC': 'btc_volume_change', 'ETH': 'eth_volume_change', 'DOGE': 'doge_volume_change'})

# Convert 'year_month' to datetime for plotting purposes:
monthly_avg['year_month'] = pd.to_datetime(monthly_avg['year_month'].astype(str))

# Set up figure:
plt.figure(figsize=(12, 6))

# Plot monthly volume changes:
plt.plot(monthly_avg['year_month'], monthly_avg['btc_volume_change'], label='BTC', color='#f2a900')
plt.plot(monthly_avg['year_month'], monthly_avg['eth_volume_change'], label='ETH', color='#8c8c8c')
plt.plot(monthly_avg['year_month'], monthly_avg['doge_volume_change'], label='DOGE', color='green')

# Set x-ticks to show only the years:
unique_years = monthly_avg['year_month'].dt.year.unique()
plt.xticks([pd.Timestamp(f'{year}-01-01') for year in unique_years], unique_years, rotation=45)

# Formatting plot:
plt.title('Cryptocurrencies changes over time')
plt.xlabel('Year')
plt.ylabel('Volume Change (%)')
plt.legend()
plt.grid(visible=True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()