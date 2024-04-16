import pandas as pd
import numpy as np
import yfinance as yf

class MeanReversionStrategy:
    def __init__(self, tickers, start_date, end_date, amount):
        """
        Initialize the mean reversion strategy with specific stock tickers, date range, and investment amount.
        :param tickers: List of stock ticker symbols.
        :param start_date: Start date for the data in 'YYYY-MM-DD' format.
        :param end_date: End date for the data in 'YYYY-MM-DD' format.
        :param amount: Total amount of money to trade with.
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.amount = amount
        self.data = self.download_data()

    def download_data(self):
        """
        Download historical stock data for given tickers and timeframe using yfinance.
        :return: DataFrame with closing prices for each ticker.
        """
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date)
        return data['Close']  # Focus on closing prices

    def execute_strategy(self):
        """
        Execute the mean reversion strategy by analyzing price deviations from the mean, selecting stocks, and allocating trades.
        :return: Dictionary with buy and short orders specifying amounts for each stock.
        """
        deviations = {}
        for ticker in self.tickers:
            prices = self.data[ticker].dropna()  # Ensure no NaN values
            mean_price = np.mean(prices)
            current_price = prices.iloc[-1]
            deviation = (current_price - mean_price) / mean_price
            deviations[ticker] = deviation

        # Sort tickers based on the absolute deviation from the mean
        sorted_tickers = sorted(deviations, key=lambda x: abs(deviations[x]), reverse=True)
        num_stocks = len(sorted_tickers)

        # Identify the cut-off for the top 10% in the sorted list
        top_10_percent_cutoff = int(0.1 * num_stocks)

        # Select top 10% for shorting and buying
        short_stocks = sorted_tickers[:top_10_percent_cutoff]
        buy_stocks = sorted_tickers[-top_10_percent_cutoff:]

        # Allocate funds equally for buying and shorting
        buy_amount = self.amount * 0.5
        short_amount = self.amount * 0.5

        # Allocate funds proportionally to the deviations
        buy_deviation_sum = sum(abs(deviations[ticker]) for ticker in buy_stocks)
        short_deviation_sum = sum(abs(deviations[ticker]) for ticker in short_stocks)

        buy_orders = {ticker: (abs(deviations[ticker]) / buy_deviation_sum) * buy_amount for ticker in buy_stocks}
        short_orders = {ticker: (abs(deviations[ticker]) / short_deviation_sum) * short_amount for ticker in short_stocks}

        return {
            'buy': buy_orders,
            'short': short_orders
        }
