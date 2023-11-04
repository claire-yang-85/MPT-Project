## Modern Portfolio Theory Exercise

This exercise was made as a coding challenge for SingAlliance.

## Objective

The objective is to create an optimal portfolio using free historical data from the Huobi.com (now known as htx.com) by applying mean-variance optimization.

## Details

* **Contracts:** Linear Swap contracts of BTC, ETH and LTC
* **Time Period:** From 2023-09-01 00:00:00+00:00 to 2023-09-01 23:00:00+00:00
* **Data Frequency:** 1 hour data
* **Python version used:** 3.11.1

## What to Expect

The program will:
* Collect the data from Huobi
* Plot the data
* Compute the mean-variance optimization
* Print the weights of the portfolio based on maximal Sharpe Ratio
* Print the allocation for a portfolio of 100,000 USD

## Notes

Given the time period, all the expected returns were negative, hence I had to adjust the default risk-free rate for the mean-variance optimization. This will need to be changed back if another time period is used.
