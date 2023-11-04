# python.exe -m pip install --upgrade pip
# pip install requests
# pip install pandas
# pip install PyPortfolioOpt
# pip install matplotlib

import requests
from datetime import datetime
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import matplotlib.pyplot as plt


def get_htx_historical_data(url_link, start, end, period, contract_code):

    # Set the parameters for the request
    params = {
        'contract_code': contract_code,
        'period': period,
        'from': start,
        'to': end
    }

    # Get the data from the API
    response = requests.get(url_link, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert the response to JSON format
        data = response.json()
        return data

    else:
        print(f"Request failed with status code: {response.status_code}")
        return None


# Risk-free rate needs to be below the max of the returns, hence below -0.095532 in this exercise
rf_rate = -0.1

# Base URL for the Huobi API
base_url = 'https://api.hbdm.com'

# Endpoint (I could not get the LTC data with /market/history/kline)
endpoint = '/linear-swap-ex/market/history/kline'

# URL link
total_url = base_url + endpoint

# Start and End time
start_time = datetime.fromisoformat('2023-09-01 00:00:00+00:00')
end_time = datetime.fromisoformat('2023-09-01 23:00:00+00:00')

# Convert the datetime to epoch time
start_epoch = int(start_time.timestamp())
end_epoch = int(end_time.timestamp())

# Get the data
data_btc = get_htx_historical_data(total_url, start_epoch, end_epoch, period='60min', contract_code='BTC-USDT')
data_eth = get_htx_historical_data(total_url, start_epoch, end_epoch, period='60min', contract_code='ETH-USDT')
data_ltc = get_htx_historical_data(total_url, start_epoch, end_epoch, period='60min', contract_code='LTC-USDT')

# Extract necessary data for plotting
timestamps = [entry['id'] for entry in data_btc['data']]
btc_closing_prices = [entry['close'] for entry in data_btc['data']]
eth_closing_prices = [entry['close'] for entry in data_eth['data']]
ltc_closing_prices = [entry['close'] for entry in data_ltc['data']]

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(timestamps, btc_closing_prices, marker='o', label='BTC')
plt.plot(timestamps, eth_closing_prices, marker='o', label='ETH')
plt.plot(timestamps, ltc_closing_prices, marker='o', label='LTC')
plt.xlabel('Timestamp')
plt.ylabel('Closing Price')
plt.title('Historical Closing Prices')
plt.legend()
plt.show()

# Combine the closing prices into a dictionary
closing_prices_dict = {
    'BTC': btc_closing_prices,
    'ETH': eth_closing_prices,
    'LTC': ltc_closing_prices
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(closing_prices_dict)

# Calculate expected returns and sample covariance
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)
print("Expected Returns:")
print(mu)

# Optimize for maximal Sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe(risk_free_rate=rf_rate)

# Get the raw weights
raw_weights = ef.clean_weights()

# Convert the output weights to a dictionary
output_dict = dict(raw_weights)
print("\nOutputs Weights:")
print(output_dict)

# Write output allocation for a 100,000 USD portfolio
output_allocation = {key: value * 100000 for key, value in output_dict.items()}
print("\nAllocation output for a portfolio of 100,000 USD:")
print(output_allocation)
