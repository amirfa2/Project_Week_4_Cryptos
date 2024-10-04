import pandas as pd
import matplotlib.pyplot as plt

# Load preprocessed hypothesis 2 data:
monthly_avg = pd.read_csv('CSVs/merged_df_for_h2.csv')
monthly_avg['year_month'] = pd.to_datetime(monthly_avg['year_month'].astype(str))

# Set size of the figure:
plt.figure(figsize=(12, 6))

# Plot monthly volume changes:
plt.plot(monthly_avg['year_month'], monthly_avg['btc_volume_change'], label='BTC', color='#f2a900')
plt.plot(monthly_avg['year_month'], monthly_avg['eth_volume_change'], label='ETH', color='#8c8c8c')
plt.plot(monthly_avg['year_month'], monthly_avg['doge_volume_change'], label='DOGE', color='#c2a37e')

# Set x-ticks to show only the years:
unique_years = monthly_avg['year_month'].dt.year.unique()
plt.xticks([pd.Timestamp(f'{year}-01-01') for year in unique_years], unique_years, rotation=45)

# Formatting plot:
plt.title('Cryptocurrency Volume Changes Over Time')
plt.xlabel('Year')
plt.ylabel('Volume Change (%)')
plt.legend(title='Cryptocurrency')
plt.grid(visible=True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()