import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load and preprocess CSV data:
df = pd.read_csv('merged_df.csv')
df['date'] = pd.to_datetime(df['date'])

# Filter data to specified date range and symbols:
df = df[(df['date'] >= '2015-08-08') & (df['date'] <= '2021-07-06')]
df = df[df['symbol'].isin(['BTC', 'ETH', 'DOGE'])]

# Calculate daily percentage change:
df['percent_change'] = ((df['close'] - df['open']) / df['open']) * 100

# Create custom color palette:
custom_palette = {'BTC': '#f2a900', 'ETH': '#8c8c8c', 'DOGE': '#c2a37e'}

# Visualization:
symbols = ['BTC', 'ETH', 'DOGE']
fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

for i, symbol in enumerate(symbols):
    data = df[df['symbol'] == symbol]
    sns.lineplot(ax=axes[i], data=data, x='date', y='percent_change', color=custom_palette[symbol], linewidth=2.5)
    axes[i].set_title(f'Daily Percentage Changes for {symbol}')
    axes[i].axhline(0, color='gray', linestyle='--', linewidth=0.8)
    axes[i].set_ylabel('Percentage Change (%)')
    if i == 2:
        axes[i].set_xlabel('Date')

plt.tight_layout()
plt.show()