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

# Calculate volatility:
volatility_data = df.groupby('symbol')['percent_change'].std().reset_index()
volatility_data.columns = ['symbol', 'volatility']

# Plot volatility:
plt.figure(figsize=(8, 5))
sns_bar = sns.barplot(x='symbol', y='volatility', data=volatility_data, palette=custom_palette, hue='symbol', dodge=False)
plt.title('Cryptocurrency Volatility (2015-08-08 to 2021-07-06)')
plt.xlabel('Cryptocurrency')
plt.ylabel('Volatility (%)')
plt.ylim(0, max(volatility_data['volatility']) + 2)
plt.legend([], [], frameon=False)
for index, row in volatility_data.iterrows():
    sns_bar.text(index, row.volatility + 0.3, f'{row.volatility:.2f}%', color='black', ha="center")
plt.tight_layout()
plt.show()

# Box Plot for Distribution of Daily Percentage Changes:
plt.figure(figsize=(10, 6))
sns.boxplot(x='symbol', y='percent_change', data=df, palette=custom_palette, hue='symbol', dodge=False)
plt.title('Distribution of Daily Percentage Changes (2015-08-08 to 2021-07-06)')
plt.xlabel('Cryptocurrency')
plt.ylabel('Daily Percentage Change (%)')
plt.ylim(-50, 50)
plt.grid(True)
plt.legend([], [], frameon=False)
plt.tight_layout()
plt.show()