import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load and preprocess CSV data:
df = pd.read_csv('merged_df.csv')
df['date'] = pd.to_datetime(df['date'])

# Calculate Bitcoin market dominance:
marketcap_df = df.groupby(['date', 'symbol'])['marketcap'].sum().unstack().fillna(0)
marketcap_df['total_marketcap'] = marketcap_df.sum(axis=1)
marketcap_df['btc_dominance'] = (marketcap_df['BTC'] / marketcap_df['total_marketcap']) * 100

# Create custom color palette:
custom_palette = {'BTC': '#f2a900'}

# Plot market dominance over time:
plt.figure(figsize=(14, 8))
sns.lineplot(data=marketcap_df, x=marketcap_df.index, y='btc_dominance', color=custom_palette['BTC'], linewidth=2.5)
plt.title('Bitcoin Market Dominance (2015-08-08 to 2021-07-06)')
plt.xlabel('Date')
plt.ylabel('BTC Market Dominance (%)')
plt.grid(True)
plt.tight_layout()
plt.show()