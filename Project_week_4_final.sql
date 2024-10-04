CREATE DATABASE merged_cryptos;

USE merged_cryptos;

CREATE TABLE initial_data (
  sno INT,
  name VARCHAR(10),
  symbol VARCHAR(10),
  date DATETIME, 
  high DECIMAL(20,8),
  low DECIMAL(20,8),
  open DECIMAL(20,8),
  close DECIMAL(20,8),
  volume DECIMAL(20,8),
  marketcap DECIMAL(20,8)
  );
  
# 1. HYPOTHESIS: Significant price drop / increase in Bitcoin lead to price drops in the major cryptocurrencies.

SELECT DISTINCT symbol, MIN(date) AS first_date, MAX(date) AS last_date 
FROM initial_data 
GROUP BY symbol;

SELECT 
    btc.date AS btc_date,
    btc.close AS btc_close,
    eth.close AS eth_close,
    doge.close AS doge_close
FROM initial_data btc
JOIN initial_data eth ON DATE(btc.date) = DATE(eth.date) AND eth.symbol = 'ETH'
JOIN initial_data doge ON DATE(btc.date) = DATE(doge.date) AND doge.symbol = 'DOGE'
WHERE btc.symbol = 'BTC' 
AND btc.date BETWEEN '2015-08-08' AND '2021-07-06'
ORDER BY 
    btc.date;

# 2. HYPOTHESIS:Increases in Bitcoin's trading volume are followed by increases in the trading volumes of other cryptocurrencies.

CREATE TEMPORARY TABLE New_Table AS
SELECT a.name, a.symbol, DATE(a.date) AS date, a.volume
FROM initial_data a
JOIN (
    SELECT DATE(date) AS date
    FROM initial_data
    WHERE symbol IN ('BTC', 'ETH', 'DOGE')
    GROUP BY DATE(date)
    HAVING COUNT(DISTINCT symbol) = 3
) b
ON DATE(a.date) = b.date
WHERE a.symbol IN ('BTC', 'ETH', 'DOGE')
ORDER BY a.date;

SELECT * FROM New_Table;
# Calculate the volume percentage change for Bitcoin (BTC), ETH and DOGE separately
SELECT symbol, 
       date,
       volume,
       LAG(volume) OVER (PARTITION BY symbol ORDER BY date) AS prev_volume,
       100 * (volume - LAG(volume) OVER (PARTITION BY symbol ORDER BY date)) / LAG(volume) OVER (PARTITION BY symbol ORDER BY date) AS volume_pct_change
FROM New_Table
WHERE symbol = 'BTC';

SELECT symbol, 
       date,
       volume,
       LAG(volume) OVER (PARTITION BY symbol ORDER BY date) AS prev_volume,
       100 * (volume - LAG(volume) OVER (PARTITION BY symbol ORDER BY date)) / LAG(volume) OVER (PARTITION BY symbol ORDER BY date) AS volume_pct_change
FROM New_Table
WHERE symbol = 'ETH';

SELECT symbol, 
       date,
       volume,
       LAG(volume) OVER (PARTITION BY symbol ORDER BY date) AS prev_volume,
       100 * (volume - LAG(volume) OVER (PARTITION BY symbol ORDER BY date)) / LAG(volume) OVER (PARTITION BY symbol ORDER BY date) AS volume_pct_change
FROM New_Table
WHERE symbol = 'DOGE';


# Calculate Cryptos volume percentage change with proper precision for volume_pct_change,avoiding division by zero

CREATE TEMPORARY TABLE btc_volume_change (
    symbol VARCHAR(10),
    date DATE,
    volume DECIMAL(30,10), 
    volume_pct_change DECIMAL(30,10)  
) AS
SELECT symbol, 
       date,
       volume,
       CASE 
           WHEN LAG(volume) OVER (PARTITION BY symbol ORDER BY date) = 0 THEN NULL
           ELSE ROUND(100 * (volume - LAG(volume) OVER (PARTITION BY symbol ORDER BY date)) / LAG(volume) OVER (PARTITION BY symbol ORDER BY date), 10)
       END AS volume_pct_change  
FROM New_Table
WHERE symbol = 'BTC';

CREATE TEMPORARY TABLE eth_volume_change (
    symbol VARCHAR(10),
    date DATE,
    volume DECIMAL(30,10),  -- Increase precision for volume
    volume_pct_change DECIMAL(30,10)  -- Increase precision for percentage change
) AS
SELECT symbol, 
       date,
       volume,
       CASE 
           WHEN LAG(volume) OVER (PARTITION BY symbol ORDER BY date) = 0 THEN NULL
           ELSE ROUND(100 * (volume - LAG(volume) OVER (PARTITION BY symbol ORDER BY date)) / LAG(volume) OVER (PARTITION BY symbol ORDER BY date), 10)
       END AS volume_pct_change  -- Round to 10 decimal places
FROM New_Table
WHERE symbol = 'ETH';

CREATE TEMPORARY TABLE doge_volume_change (
    symbol VARCHAR(10),
    date DATE,
    volume DECIMAL(30,10),  -- Increase precision for volume
    volume_pct_change DECIMAL(30,10)  -- Increase precision for percentage change
) AS
SELECT symbol, 
       date,
       volume,
       CASE 
           WHEN LAG(volume) OVER (PARTITION BY symbol ORDER BY date) = 0 THEN NULL
           ELSE ROUND(100 * (volume - LAG(volume) OVER (PARTITION BY symbol ORDER BY date)) / LAG(volume) OVER (PARTITION BY symbol ORDER BY date), 10)
       END AS volume_pct_change  -- Round to 10 decimal places
FROM New_Table
WHERE symbol = 'DOGE';

SELECT * FROM btc_volume_change;
SELECT * FROM eth_volume_change;
SELECT * FROM doge_volume_change;
#Compare volume changes across BTC, ETH, and DOGE
#AND Create a temporary table with rounded values for volume percentage changes
CREATE TEMPORARY TABLE rounded_volume_changes AS
SELECT 
    btc.date AS date,
    ROUND(btc.volume_pct_change, 2) AS btc_volume_change,
    ROUND(eth.volume_pct_change, 2) AS eth_volume_change,
    ROUND(doge.volume_pct_change, 2) AS doge_volume_change
FROM btc_volume_change btc
LEFT JOIN eth_volume_change eth ON btc.date = eth.date
LEFT JOIN doge_volume_change doge ON btc.date = doge.date
WHERE btc.volume_pct_change > 0
ORDER BY btc.date;

SELECT * FROM rounded_volume_changes;

#3 HYPOTHESIS: Bitcoin’s market dominance has decreased over time compared to Ethereum and Dogecoin.

 -- Check if data is loaded correctly
SELECT * FROM initial_data LIMIT 10;

-- Filter Bitcoin data from the 'inicial_data' table
SELECT * 
FROM initial_data
WHERE symbol = 'BTC'
ORDER BY date;

-- Calculate total market cap for Bitcoin, Ethereum, and Dogecoin combined
SELECT date, SUM(marketcap) AS total_marketcap
FROM initial_data
WHERE symbol IN ('BTC', 'ETH', 'DOGE')
GROUP BY date
ORDER BY date;
    
    -- Calculate Bitcoin's market dominance
SELECT 
    btc.date, 
    btc.marketcap AS bitcoin_marketcap,
    total_market.total_marketcap,
    (btc.marketcap / total_market.total_marketcap) * 100 AS bitcoin_market_dominance
FROM 
    initial_data btc
JOIN 
    (SELECT date, SUM(marketcap) AS total_marketcap 
     FROM initial_data 
     WHERE symbol IN ('BTC', 'ETH', 'DOGE')
     GROUP BY date) total_market
ON 
    btc.date = total_market.date
WHERE 
    btc.symbol = 'BTC'
ORDER BY 
    btc.date;
    
   #4. HYPOTHESIS: The volatility of Bitcoin is lower compared to other cryptos.
   
SELECT symbol,
    ROUND(STDDEV((close - open)/open * 100), 2) AS volatility
FROM initial_data 
WHERE symbol IN ('BTC', 'ETH', 'DOGE')
    AND date BETWEEN '2015-08-08' AND '2021-07-06'
GROUP BY symbol;
   








